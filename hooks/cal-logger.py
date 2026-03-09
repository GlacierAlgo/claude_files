#!/usr/bin/env python3
"""
Claude Code Stop hook - 在 Apple Calendar 写入 session 事件
每个 session_id 只写一次（去重）
"""
import os
import sys
import json
import subprocess
from datetime import datetime, timezone

CALENDAR_NAME = "Claude-work"
LOG_FILE = os.path.expanduser("~/.claude/logs/cal-logger.log")
STATE_FILE = os.path.expanduser("~/.claude/state/cal-logged-sessions.json")
MAX_SESSIONS = 500


def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {msg}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


def load_logged_sessions():
    if not os.path.exists(STATE_FILE):
        return set()
    with open(STATE_FILE) as f:
        data = json.load(f)
    return set(data.get("sessions", []))


def save_logged_sessions(sessions: set, new_id: str):
    sessions.add(new_id)
    ordered = list(sessions)[-MAX_SESSIONS:]
    with open(STATE_FILE, "w") as f:
        json.dump({"sessions": ordered}, f)


def escape_applescript(text: str) -> str:
    return text.replace("\\", "\\\\").replace('"', '\\"')


def parse_timestamp(ts_str: str) -> datetime | None:
    """解析 transcript 里的 ISO 8601 时间戳"""
    if not ts_str:
        return None
    try:
        # 处理带 Z 和带 +00:00 两种格式
        ts_str = ts_str.replace("Z", "+00:00")
        return datetime.fromisoformat(ts_str)
    except Exception:
        return None


def extract_transcript_info(transcript_path: str):
    """
    返回:
      user_messages: list[str]  意图型用户消息（最多 5 条）
      usage_info: dict | None   最后一次 assistant usage
      start_dt: datetime | None  第一条记录的时间
      end_dt: datetime | None    最后一条记录的时间
    """
    user_messages = []
    usage_info = None
    start_dt = None
    end_dt = None

    if not transcript_path or not os.path.exists(transcript_path):
        return user_messages, usage_info, start_dt, end_dt

    with open(transcript_path) as f:
        lines = f.readlines()

    entries = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            entries.append(json.loads(line))
        except Exception:
            continue

    if entries:
        start_dt = parse_timestamp(entries[0].get("timestamp", ""))
        end_dt = parse_timestamp(entries[-1].get("timestamp", ""))

    for entry in entries:
        if entry.get("type") == "user":
            message = entry.get("message", {})
            content = message.get("content", "")
            text = None
            if isinstance(content, list):
                for item in content:
                    if isinstance(item, dict) and item.get("type") == "text":
                        text = item.get("text", "").strip()
                        break
            elif isinstance(content, str):
                text = content.strip()
            if text:
                first_line = text.split("\n")[0].strip()
                # 跳过看起来像 shell prompt 的行
                if "@" in first_line and "$" in first_line:
                    continue
                user_messages.append(first_line)

    # 找最后一条 assistant usage
    for entry in reversed(entries):
        if entry.get("type") == "assistant":
            usage = entry.get("message", {}).get("usage")
            if usage:
                usage_info = usage
                break

    return user_messages[:5], usage_info, start_dt, end_dt


def compute_cost(usage_info: dict) -> tuple[str, float]:
    """返回 (token_summary, cost)"""
    if not usage_info:
        return "", 0.0
    input_tokens = usage_info.get("input_tokens", 0)
    cache_read = usage_info.get("cache_read_input_tokens", 0)
    cache_create = usage_info.get("cache_creation_input_tokens", 0)
    output_tokens = usage_info.get("output_tokens", 0)

    # Claude Sonnet 4.6 定价 (per 1M tokens)
    cost = (
        input_tokens * 3
        + cache_create * 3.75
        + cache_read * 0.30
        + output_tokens * 15
    ) / 1_000_000

    total_input = input_tokens + cache_read + cache_create
    summary = f"In:{total_input // 1000}k Out:{output_tokens // 1000}k ${cost:.2f}"
    return summary, cost


def get_git_info(cwd: str) -> tuple[str, str]:
    """返回 (branch, changed_files_str)"""
    branch = ""
    changed_files = ""
    if not cwd:
        return branch, changed_files
    try:
        result = subprocess.run(
            ["git", "-C", cwd, "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            branch = result.stdout.strip()
    except Exception:
        pass
    try:
        result = subprocess.run(
            ["git", "-C", cwd, "diff", "--name-only", "HEAD"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            files = [f for f in result.stdout.strip().splitlines() if f][:5]
            changed_files = ", ".join(files)
    except Exception:
        pass
    return branch, changed_files


def build_title(user_messages: list[str]) -> str:
    if not user_messages:
        return "Claude Session"
    parts = [m[:40] for m in user_messages[:3]]
    title = " + ".join(parts)
    return title[:120]  # AppleScript 标题不宜过长


def build_notes(
    user_messages: list[str],
    branch: str,
    changed_files: str,
    duration_min: int,
    token_summary: str,
    project_name: str,
) -> str:
    lines = ["Tasks:"]
    for msg in user_messages:
        lines.append(f"  \u2022 {msg}")

    parts = []
    if branch:
        parts.append(f"Branch: {branch}")
    if changed_files:
        parts.append(f"Files: {changed_files}")

    dur_str = f"{duration_min} min" if duration_min else ""
    stat_parts = [p for p in [dur_str, token_summary] if p]
    if stat_parts:
        parts.append("Duration: " + " | ".join(stat_parts))

    parts.append(f"Project: {project_name}")
    lines.append("")
    lines.extend(parts)
    return "\n".join(lines)


def write_calendar_event(title: str, notes: str, start_dt: datetime, duration_min: int):
    """使用 AppleScript 写入 Apple Calendar 事件"""
    escaped_title = escape_applescript(title)
    escaped_notes = escape_applescript(notes)
    escaped_cal = escape_applescript(CALENDAR_NAME)

    # 计算事件时间（用 start_dt，若没有则用当前时间）
    if start_dt:
        # 转为本地时间
        local_dt = start_dt.astimezone()
        year = local_dt.year
        month = local_dt.month
        day = local_dt.day
        hour = local_dt.hour
        minute = local_dt.minute
        second = local_dt.second
    else:
        now = datetime.now()
        year, month, day = now.year, now.month, now.day
        hour, minute, second = now.hour, now.minute, now.second

    end_offset = max(duration_min, 1)  # 至少 1 分钟

    script = f'''
tell application "Calendar"
    set targetCalendar to calendar "{escaped_cal}"
    set startDate to current date
    set year of startDate to {year}
    set month of startDate to {month}
    set day of startDate to {day}
    set hours of startDate to {hour}
    set minutes of startDate to {minute}
    set seconds of startDate to {second}
    set endDate to startDate + ({end_offset} * minutes)
    set newEvent to make new event at end of events of targetCalendar with properties {{summary:"{escaped_title}", start date:startDate, end date:endDate, description:"{escaped_notes}"}}
end tell
'''

    result = subprocess.run(
        ["osascript", "-e", script],
        capture_output=True, text=True, timeout=15
    )
    return result.returncode, result.stderr.strip()


def main():
    event_data_str = ""
    if not sys.stdin.isatty():
        event_data_str = sys.stdin.read().strip()

    if not event_data_str:
        event_data_str = "{}"

    data = json.loads(event_data_str)

    # 防止 stop_hook_active 导致循环
    if data.get("stop_hook_active"):
        log("stop_hook_active=true, skipping")
        return

    session_id = data.get("session_id", "")
    transcript_path = data.get("transcript_path", "")
    cwd = data.get("cwd", "")

    if not session_id:
        log("No session_id, skipping")
        return

    # 去重检查
    logged = load_logged_sessions()
    if session_id in logged:
        log(f"Session {session_id[:8]} already logged, skipping")
        return

    log(f"Processing session {session_id[:8]}")

    # 解析 transcript
    user_messages, usage_info, start_dt, end_dt = extract_transcript_info(transcript_path)

    # 计算时长
    duration_min = 0
    if start_dt and end_dt:
        delta = end_dt - start_dt
        duration_min = max(int(delta.total_seconds() / 60), 1)

    # Token 成本
    token_summary, _ = compute_cost(usage_info)

    # Git 信息
    branch, changed_files = get_git_info(cwd)

    # 项目名
    if cwd:
        parts = cwd.rstrip("/").split("/")
        project_name = "/".join(parts[-2:]) if len(parts) >= 2 else parts[-1]
    else:
        project_name = "Claude Code"

    # 构建标题和备注
    title = build_title(user_messages)
    notes = build_notes(user_messages, branch, changed_files, duration_min, token_summary, project_name)

    log(f"Title: {title}")
    log(f"Notes: {notes[:200]}")

    # 写入日历
    returncode, stderr = write_calendar_event(title, notes, start_dt, duration_min)
    if returncode == 0:
        log("Calendar event written successfully")
        save_logged_sessions(logged, session_id)
    else:
        log(f"Calendar write failed (rc={returncode}): {stderr}")


if __name__ == "__main__":
    main()

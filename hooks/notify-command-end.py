#!/usr/bin/env python3
"""
Claude Code command-end hook - 使用 Python 发送系统通知
"""
import os
import sys
import json
import subprocess
from datetime import datetime

LOG_FILE = os.path.expanduser('~/.claude/logs/notify-debug.log')

def log(msg):
    """写入日志文件和标准输出"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_msg = f'[{timestamp}] {msg}'
    print(log_msg)
    with open(LOG_FILE, 'a') as f:
        f.write(log_msg + '\n')

def main():
    # 读取 Claude Code 传递的事件数据
    # 先尝试从 stdin 读取
    event_data_str = None
    if not sys.stdin.isatty():
        try:
            event_data_str = sys.stdin.read().strip()
            log(f'从 stdin 读取数据: {event_data_str[:200] if event_data_str else "空"}')
        except Exception as e:
            log(f'读取 stdin 失败: {e}')

    # 如果 stdin 为空，尝试环境变量
    if not event_data_str:
        event_data_str = os.environ.get('CLAUDE_HOOK_EVENT_DATA') or \
                         os.environ.get('CLAUDE_HOOK_INPUT') or \
                         os.environ.get('HOOK_INPUT') or '{}'
        log(f'从环境变量读取: {event_data_str}')

    # 记录所有环境变量用于调试
    log('所有 CLAUDE 相关环境变量:')
    for key, value in os.environ.items():
        if 'CLAUDE' in key or 'HOOK' in key:
            log(f'  {key} = {value[:100] if len(value) > 100 else value}')

    log('Hook 触发')
    log(f'最终 eventData: {event_data_str}')

    try:
        # 解析 JSON 数据
        data = json.loads(event_data_str)
        log(f'解析后的数据: {data}')

        # Stop hook 提供的字段
        hook_event_name = data.get('hook_event_name', 'Unknown')
        session_id = data.get('session_id', 'N/A')
        stop_hook_active = data.get('stop_hook_active', False)
        transcript_path = data.get('transcript_path', '')

        # 防止无限循环：如果是 hook 触发的继续执行，跳过通知
        if stop_hook_active:
            log('WARNING: stop_hook_active=true，跳过通知避免循环')
            return

        # 尝试读取最后的用户消息和 token 使用情况
        user_message = 'Unknown'
        usage_info = None
        try:
            if transcript_path and os.path.exists(transcript_path):
                with open(transcript_path, 'r') as f:
                    lines = f.readlines()

                    # 找到最后的 assistant 消息获取 usage
                    for line in reversed(lines):
                        try:
                            entry = json.loads(line)
                            if entry.get('type') == 'assistant' and not usage_info:
                                message = entry.get('message', {})
                                usage_info = message.get('usage', {})
                                break
                        except:
                            continue

                    # 找到最后的用户消息
                    for line in reversed(lines):
                        try:
                            entry = json.loads(line)
                            # 检查 type 字段
                            if entry.get('type') == 'user':
                                # 提取消息文本
                                message = entry.get('message', {})
                                content = message.get('content', '')

                                # 跳过工具结果，只处理文本消息
                                if isinstance(content, list):
                                    # 查找 text 类型的内容，跳过 tool_result
                                    for item in content:
                                        if isinstance(item, dict) and item.get('type') == 'text':
                                            text = item.get('text', '')
                                            break
                                    else:
                                        # 没找到 text 类型，跳过这条消息
                                        continue
                                elif isinstance(content, str):
                                    text = content
                                else:
                                    # 其他类型跳过
                                    continue

                                # 清理文本：只取第一行，去除命令行提示符
                                lines = text.strip().split('\n')
                                first_line = lines[0]
                                # 去掉命令行提示符
                                if '@' in first_line and '$' in first_line:
                                    # 找下一个有意义的行
                                    for line in lines[1:]:
                                        if line.strip() and not line.startswith('['):
                                            first_line = line.strip()
                                            break

                                # 取前80个字符
                                user_message = first_line[:80] + '...' if len(first_line) > 80 else first_line
                                break
                        except Exception as parse_error:
                            log(f'解析行失败: {parse_error}')
                            continue
        except Exception as e:
            log(f'读取 transcript 失败: {e}')

        # 获取项目路径的最后两层文件夹
        cwd = data.get('cwd', '')
        if cwd:
            path_parts = cwd.rstrip('/').split('/')
            # 取最后两层
            project_name = '/'.join(path_parts[-2:]) if len(path_parts) >= 2 else path_parts[-1] if path_parts else 'Claude Code'
        else:
            project_name = 'Claude Code'

        # 计算 token 使用和成本
        token_summary = ''
        cost_estimate = 0.0
        if usage_info:
            input_tokens = usage_info.get('input_tokens', 0)
            cache_read = usage_info.get('cache_read_input_tokens', 0)
            cache_create = usage_info.get('cache_creation_input_tokens', 0)
            output_tokens = usage_info.get('output_tokens', 0)

            # Claude Sonnet 4.5 定价 (per 1M tokens)
            # Input: $3, Cache write: $3.75, Cache read: $0.30, Output: $15
            input_cost = input_tokens * 3 / 1_000_000
            cache_write_cost = cache_create * 3.75 / 1_000_000
            cache_read_cost = cache_read * 0.30 / 1_000_000
            output_cost = output_tokens * 15 / 1_000_000
            cost_estimate = input_cost + cache_write_cost + cache_read_cost + output_cost

            # 构建简洁的统计信息（重点）
            total_input = input_tokens + cache_read + cache_create
            token_summary = f'In:{total_input//1000}k Out:{output_tokens//1000}k ${cost_estimate:.4f}'

        log('准备发送通知:')
        log(f'- hook_event: {hook_event_name}')
        log(f'- session_id: {session_id}')
        log(f'- 项目: {project_name}')
        log(f'- 用户消息: {user_message}')
        log(f'- Token: {token_summary}')

        # 构建通知标题和消息（无emoji）
        # Token 信息和成本放在标题中，格式: 75k | 1k | $0.02
        if usage_info:
            total_input = usage_info.get('input_tokens', 0) + usage_info.get('cache_read_input_tokens', 0) + usage_info.get('cache_creation_input_tokens', 0)
            output_tokens = usage_info.get('output_tokens', 0)
            title = f'{project_name} | {total_input//1000}k | {output_tokens//1000}k | ${cost_estimate:.2f}'
        else:
            title = f'{project_name}'

        message = f'{user_message}'

        # 转义 AppleScript 特殊字符
        def escape_applescript(text):
            """转义 AppleScript 字符串中的特殊字符"""
            return text.replace('\\', '\\\\').replace('"', '\\"')

        escaped_title = escape_applescript(title)
        escaped_message = escape_applescript(message)

        # 使用 osascript 发送 macOS 通知
        log('正在发送通知...')
        script = f'''
        display notification "{escaped_message}" with title "{escaped_title}" sound name "default"
        '''

        result = subprocess.run(
            ['osascript', '-e', script],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            log('通知已发送')
        else:
            log(f'通知发送失败: {result.stderr}')
            # 不要因为通知失败而退出，这不是关键错误
            # sys.exit(1)

    except Exception as e:
        log(f'脚本执行失败: {e}')
        import traceback
        traceback.print_exc()
        with open(LOG_FILE, 'a') as f:
            traceback.print_exc(file=f)
        # 不要因为通知失败而退出，这不是关键错误
        # sys.exit(1)

if __name__ == '__main__':
    main()

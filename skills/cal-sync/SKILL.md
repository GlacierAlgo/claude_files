# cal-sync Skill

Manually trigger the cal-logger hook to write a summary of the current session to Apple Calendar.

## Steps

1. Find the project directory under `~/.claude/projects/` that matches the current working directory. The directory name is the cwd path with `/` replaced by `-`. For example, `/Users/yanghh/Documents/code/quant/claude_files` → `-Users-yanghh-Documents-code-quant-claude-files`.

2. List the transcript files in that directory sorted by modification time (newest first), and pick the most recent one. The filename without `.jsonl` is the session_id.

   ```bash
   ls -t ~/.claude/projects/<project-dir>/ | head -5
   ```

3. Check `~/.claude/state/cal-logged-sessions.json` to see if that session_id has already been logged. If it has, pick the next newest unlogged transcript.

4. Run the hook with hardcoded values (no shell variables in the JSON string):

   ```bash
   printf '{"session_id":"<id>","transcript_path":"<path>","cwd":"<cwd>"}' | python ~/.claude/hooks/cal-logger.py
   ```

5. Report the log output to the user. If it says "already logged", inform the user and skip.

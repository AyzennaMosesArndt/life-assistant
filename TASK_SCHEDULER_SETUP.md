# Windows Task Scheduler Setup

## Automated startup for Life Assistant bot

### Create the scheduled task

1. **Open Task Scheduler**
   - Press `Win + R`, type `taskschd.msc`, press Enter

2. **Create Basic Task**
   - Right-click "Task Scheduler Library" → "Create Task..." (not "Create Basic Task")

3. **General tab**
   - Name: `Life Assistant Bot`
   - Description: `Starts the life assistant Telegram bot at login`
   - ✓ Run whether user is logged on or not
   - ✓ Run with highest privileges (if needed for file access)
   - Configure for: `Windows 10` or `Windows 11`

4. **Triggers tab**
   - Click "New..."
   - Begin the task: `At log on`
   - Specific user: `ayzen` (or your username)
   - ✓ Enabled
   - Click "OK"

5. **Actions tab**
   - Click "New..."
   - Action: `Start a program`
   - Program/script: `C:\Users\ayzen\life-assistant\start_bot.bat`
   - Start in (optional): `C:\Users\ayzen\life-assistant`
   - Click "OK"

6. **Conditions tab**
   - ✓ Start only if the following network connection is available: `Any connection`
   - Uncheck power-saving options if running on laptop

7. **Settings tab**
   - ✓ Allow task to be run on demand
   - ✓ If the task fails, restart every: `1 minute`, Attempt to restart up to: `3 times`
   - If the running task does not end when requested: `Stop the existing instance`

8. **Click "OK"** to save

### Run in hidden window (optional)

If you want the console window hidden:

1. Create a VBScript launcher: `start_bot_hidden.vbs`
2. Task Scheduler runs the VBS instead of the BAT
3. VBS launches BAT with hidden window

Create `start_bot_hidden.vbs` with this content:
```vbscript
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "C:\Users\ayzen\life-assistant\start_bot.bat", 0, False
```

Then in Task Scheduler Action:
- Program/script: `wscript.exe`
- Arguments: `"C:\Users\ayzen\life-assistant\start_bot_hidden.vbs"`

### Test the task

Right-click the task → "Run" to test it manually before logging out.

### View logs

Check bot output/logs in the configured log directory or redirect output in the batch script:
```batch
python bot.py >> bot.log 2>&1
```

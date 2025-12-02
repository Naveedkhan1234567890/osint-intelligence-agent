# 🖥️ Building Windows Executable

## Quick Build

```bash
# Install PyInstaller
pip install pyinstaller

# Build single .exe file
pyinstaller --onefile --name="OSINT-Agent" osint_agent.py

# Your .exe will be in dist/ folder
```

## Advanced Build (With Icon & No Console)

```bash
# Build with custom icon and no console window
pyinstaller --onefile --noconsole --icon=icon.ico --name="OSINT-Agent" osint_agent.py
```

## Build Options Explained

- `--onefile` - Creates single .exe (not a folder)
- `--noconsole` - No command prompt window (GUI mode)
- `--icon=icon.ico` - Custom icon for .exe
- `--name="OSINT-Agent"` - Name of the .exe file

## Distribution

The .exe file will be in `dist/OSINT-Agent.exe`

You can copy this file to any Windows computer and run it without Python installed.

## File Size

Expect ~15-25 MB for the .exe file (includes Python runtime and all dependencies).

## Testing

```bash
# Test the .exe
cd dist
OSINT-Agent.exe --name "Test Person"
```

## Troubleshooting

**Issue:** .exe won't run  
**Solution:** Run as administrator

**Issue:** Antivirus blocks it  
**Solution:** Add exception (PyInstaller .exe files often trigger false positives)

**Issue:** Missing dependencies  
**Solution:** Rebuild with `--hidden-import` flag for missing modules

## Creating Installer (Optional)

Use Inno Setup to create a professional installer:

1. Download Inno Setup: https://jrsoftware.org/isinfo.php
2. Create installer script
3. Build installer.exe

This gives users a proper installation wizard.

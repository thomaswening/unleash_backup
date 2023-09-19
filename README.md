# EVGA Z20/Z15 Keyboard Custom Key Color Layers Backup & Restore Tool

Are you also fed up with 'Unleash RGB' deleting your custom color profiles after randomly crashing or just because you had to switch the USB port for the keyboard?
Well, fear no more! This Python script provides a simple way to backup and restore custom key color layers for EVGA Z20/Z15 keyboards using the Unleash RGB software.
Because apparently, some companies just can't be bothered to deliver complete software that actually works.

## Requirements

- Python 3.x
- `psutil` library (can be installed via `pip install psutil`)

## Usage

1. **Backup Custom Key Color Layers**:
   - Using the script:
     ```
     python unleash_backup.py
     ```
   - Or simply run the `backup.bat` batch script.

2. **Restore Custom Key Color Layers**:
   Before running the restore command, ensure you've created a new custom profile in Unleash and clicked 'Apply'.
   - Using the script:
     ```
     python unleash_backup.py -r
     ```
   - Or simply run the `restore_backup.bat` batch script.

## Desktop Shortcuts

For ease of use, you can create shortcuts to the `backup.bat` and `restore_backup.bat` batch scripts on your desktop. This way, you won't have to navigate to the script's directory or deal with command line paths. Just double-click the shortcut to execute the desired action.

## Command Line Arguments

- `-d`, `--directory`: Specify the path to the backup directory. By default, it uses the directory where the script resides.
- `-r`, `--restore`: Use this flag to restore profiles from the backup directory.
- `-p`, `--path`: Specify the path to the `UnleashRGB.exe` executable. Default is `C:\Program Files (x86)\EVGA\Unleash RGB\UnleashRGB.exe`.

## Notes

- When restoring profiles, the script will prompt you to create a new custom profile in Unleash. This is a necessary step for the restoration process to work correctly.
- After restoration, you must select a different profile in Unleash for the changes to take effect.

## License

This script is provided "as is" without any warranties. Use at your own risk.

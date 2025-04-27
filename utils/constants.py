# utils/constants.py

PERSISTENCE_KEYS = [
    "Run",
    "RunOnce",
    "Services",
    "CurrentVersion\\Policies\\Explorer\\Run",
    "Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Run"
]

SUSPICIOUS_FOLDERS = [
    "%TEMP%",
    "%APPDATA%",
    "\\\\Temp\\\\",
    "\\\\AppData\\\\",
    "\\\\ProgramData\\\\",
    "\\\\Recycle.Bin\\\\",
    "\\\\System Volume Information\\\\"
]

EXECUTABLE_EXTENSIONS = [
    ".exe",
    ".dll",
    ".bat",
    ".cmd",
    ".scr"
]

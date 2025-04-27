# utils/analyzer.py

from utils.constants import PERSISTENCE_KEYS, SUSPICIOUS_FOLDERS, EXECUTABLE_EXTENSIONS

def analyze_registry_entries(entries):
    for entry in entries:
        # Persistence detection
        if any(pkey.lower() in entry.reg_key.lower() for pkey in PERSISTENCE_KEYS):
            entry.flags.append("Persistence Key")

        # Suspicious folder detection
        if any(folder.lower() in entry.file_path.lower() for folder in SUSPICIOUS_FOLDERS):
            entry.flags.append("Suspicious Folder")

        # Executable detection
        if any(entry.file_path.lower().endswith(ext) for ext in EXECUTABLE_EXTENSIONS):
            entry.flags.append("Executable File")

        # Incomplete path detection
        if not (":" in entry.file_path or entry.file_path.startswith("%")):
            entry.flags.append("Incomplete Path")

    return entries

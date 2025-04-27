# utils/entry.py

class RegistryEntry:
    def __init__(self, reg_key, value_name, file_path, entry_type=""):
        self.reg_key = reg_key          # Full registry path
        self.value_name = value_name    # Name of the value inside the key
        self.file_path = file_path      # Data associated with the value (could be a file path, string, etc.)
        self.entry_type = entry_type    # Type: added_key, added_value, modified_value
        self.flags = []                 # NEW: List of flags found during analysis (like 'Suspicious Path', 'Incomplete Path')

    def __repr__(self):
        return f"RegistryEntry(key={self.reg_key}, value={self.value_name}, file={self.file_path}, type={self.entry_type}, flags={self.flags})"


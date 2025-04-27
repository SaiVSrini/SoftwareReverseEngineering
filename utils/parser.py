

import re
from utils.entry import RegistryEntry

def parse_regshot_diff(filepath):
    entries = []
    current_section = None

    with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
        lines = file.readlines()

    for raw_line in lines:
        line = raw_line.strip()

        if not line:
            continue

        lower_line = line.lower()

        # Detect Section Start
        if 'keys added:' in lower_line:
            current_section = 'keys_added'
            continue
        elif 'values added:' in lower_line:
            current_section = 'values_added'
            continue
        elif 'values modified:' in lower_line:
            current_section = 'values_modified'
            continue
        elif any(x in lower_line for x in ['keys deleted', 'values deleted', 'files added', 'files deleted']):
            current_section = None
            continue

        # Skip separator lines
        if line.startswith('----------------------------------'):
            continue

        # Parse Keys Added Section
        if current_section == 'keys_added':
            entry = RegistryEntry(
                reg_key=line,
                value_name="",
                file_path="",
                entry_type="added_key"
            )
            entries.append(entry)

        # Parse Values Added Section
        elif current_section == 'values_added':
            match = re.match(r'(.+?)\\([^\\:]+):\s*(.*)', line)
            if match:
                key_path = match.group(1)
                value_name = match.group(2)
                value_data = match.group(3).strip('"')

                entry = RegistryEntry(
                    reg_key=key_path,
                    value_name=value_name,
                    file_path=value_data,
                    entry_type="added_value"
                )
                entries.append(entry)

        # Parse Values Modified Section
        elif current_section == 'values_modified':
            match = re.match(r'(.+?)\\([^\\:]+):\s*(.*)', line)
            if match:
                key_path = match.group(1)
                value_name = match.group(2)
                value_data = match.group(3).strip('"')

                entry = RegistryEntry(
                    reg_key=key_path,
                    value_name=value_name,
                    file_path=value_data,
                    entry_type="modified_value"
                )
                entries.append(entry)

    return entries


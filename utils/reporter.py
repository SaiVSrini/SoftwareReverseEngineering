# utils/reporter.py

import json
import os

def generate_reports(entries, output_dir, verbose=False):
    txt_output = []

    for entry in entries:
        entry_block = (
            f"Registry Key: {entry.reg_key}\\n"
            f"Value Name: {entry.value_name}\\n"
            f"File Path: {entry.file_path}\\n"
            f"Flags: {', '.join(entry.flags)}\\n"
            f"Suspiciousness Score: {entry.score}/10\\n"
            f"{'-'*40}\\n"
        )
        txt_output.append(entry_block)

        if verbose:
            print(entry_block)

    with open(os.path.join(output_dir, "report.txt"), 'w', encoding='utf-8') as f:
        f.write("\\n".join(txt_output))

    json_output = [entry.__dict__ for entry in entries]
    with open(os.path.join(output_dir, "report.json"), 'w', encoding='utf-8') as f:
        json.dump(json_output, f, indent=4)

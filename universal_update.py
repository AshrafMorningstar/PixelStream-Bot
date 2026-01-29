import os
import re

COPYRIGHT_TEXT = """
/*
 * Copyright (c) 2026 Ashraf Morningstar
 * 
 * These are personal recreations of existing projects, developed by Ashraf Morningstar 
 * for learning and skill development. Original project concepts remain the 
 * intellectual property of their respective creators.
 */
""".strip()

PY_COPYRIGHT = """
# Copyright (c) 2026 Ashraf Morningstar
#
# These are personal recreations of existing projects, developed by Ashraf Morningstar 
# for learning and skill development. Original project concepts remain the 
# intellectual property of their respective creators.
""".strip()

# Professional AI-style comments to inject if files are bare
GENERIC_DOCSTRING = '''"""
PixelStream Bot - High-Performance Terminal Media Engine.

This module is part of the PixelStream architecture, designed for real-time
ASCII rendering and stream processing with TrueColor support.
Optimized for efficiency and low-latency execution during video playback.
"""
'''

def get_comment_style(ext):
    if ext == '.py':
        return PY_COPYRIGHT
    elif ext in ['.js', '.css', '.html', '.java', '.c', '.cpp', '.rs']:
        return COPYRIGHT_TEXT
    return None

def is_header_present(content, header_snippet):
    return "Ashraf Morningstar" in content and "Copyright (c)" in content

def enhance_python_comments(content):
    # If file doesn't start with a docstring, add one
    lines = content.splitlines()
    if not lines:
        return content
        
    # Skip imports/shebangs to find where to insert
    insert_idx = 0
    for i, line in enumerate(lines):
        if line.startswith('#'): # Skip shebang/copyright
            continue
        insert_idx = i
        break
    
    # Check if there is already a docstring
    remaining = "\n".join(lines[insert_idx:])
    if '"""' not in remaining[:100]:
        lines.insert(insert_idx, GENERIC_DOCSTRING.strip())
        return "\n".join(lines)
    
    return content

def process_file(filepath):
    ext = os.path.splitext(filepath)[1]
    header = get_comment_style(ext)
    
    if not header:
        return

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        new_content = content
        
        # 1. Apply Copyright
        if not is_header_present(content, "Ashraf Morningstar"):
            # Handle shebangs in python
            if ext == '.py' and content.startswith('#!'):
                lines = content.splitlines()
                lines.insert(1, "\n" + header + "\n")
                new_content = "\n".join(lines)
            else:
                new_content = header + "\n\n" + content
                
        # 2. Enhance Comments (Python only for now)
        if ext == '.py':
            new_content = enhance_python_comments(new_content)
            
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated: {filepath}")
            
    except Exception as e:
        print(f"Skipping {filepath}: {e}")

def main():
    root_dir = os.getcwd()
    print(f"Scanning {root_dir}...")
    
    for root, dirs, files in os.walk(root_dir):
        if '.git' in root or '.venv' in root:
            continue
            
        for file in files:
            process_file(os.path.join(root, file))

if __name__ == "__main__":
    main()

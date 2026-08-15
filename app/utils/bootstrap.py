import os
import sys

def ensure_project_root_in_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    while current_dir and not os.path.exists(os.path.join(current_dir, 'app')):
        parent = os.path.dirname(current_dir)
        if parent == current_dir:
            break
        current_dir = parent
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)

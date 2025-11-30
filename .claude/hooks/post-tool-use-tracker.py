#!/usr/bin/env python3
"""
Post-tool-use tracker hook for Claude Code.
Tracks files edited using Edit, Write, or MultiEdit tools.
"""

import sys
import json
import os
from pathlib import Path
from typing import Dict, List, Set


class FileTracker:
    def __init__(self, project_dir: str):
        self.project_dir = Path(project_dir)
        self.tracking_file = self.project_dir / '.claude' / '.file-tracker.json'
        self.tracking_file.parent.mkdir(parents=True, exist_ok=True)

    def load_tracking_data(self) -> Dict:
        """Load existing tracking data."""
        if self.tracking_file.exists():
            try:
                with open(self.tracking_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {'edited_files': [], 'affected_repos': []}
        return {'edited_files': [], 'affected_repos': []}

    def save_tracking_data(self, data: Dict):
        """Save tracking data to file."""
        try:
            with open(self.tracking_file, 'w') as f:
                json.dump(data, f, indent=2)
        except IOError as e:
            print(f"Warning: Could not save tracking data: {e}", file=sys.stderr)

    def get_repo_for_file(self, file_path: Path) -> str:
        """Determine which repository a file belongs to."""
        # Simple implementation: just return the project dir name
        # Can be enhanced to detect git repos, monorepo structure, etc.
        return str(self.project_dir.name)

    def track_file(self, file_path: str):
        """Track a file that was edited."""
        data = self.load_tracking_data()

        # Add file to tracked list
        if file_path not in data['edited_files']:
            data['edited_files'].append(file_path)

        # Determine and track affected repository
        file_path_obj = Path(file_path)
        if file_path_obj.is_absolute():
            repo = self.get_repo_for_file(file_path_obj)
        else:
            repo = self.get_repo_for_file(self.project_dir / file_path)

        if repo not in data['affected_repos']:
            data['affected_repos'].append(repo)

        self.save_tracking_data(data)

        # Output summary
        print(f"📝 Tracked: {file_path}")
        print(f"📁 Repository: {repo}")
        print(f"📊 Session stats: {len(data['edited_files'])} files, {len(data['affected_repos'])} repos")


def main():
    try:
        # Read input from stdin
        input_data = sys.stdin.read()
        data = json.loads(input_data)

        # Get tool information
        tool_name = data.get('tool_name', '')
        tool_input = data.get('tool_input', {})

        # Track files for Edit, Write, and MultiEdit tools
        if tool_name in ['Edit', 'Write', 'MultiEdit']:
            project_dir = os.environ.get('CLAUDE_PROJECT_DIR', os.path.expanduser('~/project'))
            tracker = FileTracker(project_dir)

            # Extract file path based on tool type
            file_path = None
            if tool_name == 'Edit':
                file_path = tool_input.get('file_path')
            elif tool_name == 'Write':
                file_path = tool_input.get('file_path')
            elif tool_name == 'MultiEdit':
                # MultiEdit might have multiple files
                # For simplicity, track the first one
                edits = tool_input.get('edits', [])
                if edits:
                    file_path = edits[0].get('file_path')

            if file_path:
                tracker.track_file(file_path)

        sys.exit(0)

    except json.JSONDecodeError as e:
        print(f"Error parsing input JSON: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error in post-tool-use-tracker hook: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()

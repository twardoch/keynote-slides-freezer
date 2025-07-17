#!/usr/bin/env python3
"""
Version management script that reads version from git tags.
Supports both semantic versioning and development versions.
"""

import subprocess
import re
import sys
from pathlib import Path


def get_git_version():
    """Get version from git tags and commits."""
    try:
        # Get the latest tag
        result = subprocess.run(
            ["git", "describe", "--tags", "--abbrev=0"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent
        )
        
        if result.returncode == 0:
            latest_tag = result.stdout.strip()
            
            # Check if we're exactly on a tag
            current_commit = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                capture_output=True,
                text=True,
                cwd=Path(__file__).parent
            ).stdout.strip()
            
            tag_commit = subprocess.run(
                ["git", "rev-list", "-n", "1", latest_tag],
                capture_output=True,
                text=True,
                cwd=Path(__file__).parent
            ).stdout.strip()
            
            # Clean the tag to be semver compliant
            clean_tag = latest_tag.lstrip('v')
            
            if current_commit == tag_commit:
                # We're exactly on a tag
                return clean_tag
            else:
                # We're ahead of the tag, add dev suffix
                commits_ahead = subprocess.run(
                    ["git", "rev-list", "--count", f"{latest_tag}..HEAD"],
                    capture_output=True,
                    text=True,
                    cwd=Path(__file__).parent
                ).stdout.strip()
                
                short_commit = current_commit[:7]
                return f"{clean_tag}.dev{commits_ahead}+{short_commit}"
        else:
            # No tags found, use commit hash
            current_commit = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                capture_output=True,
                text=True,
                cwd=Path(__file__).parent
            ).stdout.strip()
            
            commit_count = subprocess.run(
                ["git", "rev-list", "--count", "HEAD"],
                capture_output=True,
                text=True,
                cwd=Path(__file__).parent
            ).stdout.strip()
            
            return f"0.0.0.dev{commit_count}+{current_commit[:7]}"
            
    except Exception as e:
        print(f"Error getting git version: {e}", file=sys.stderr)
        return "0.0.0+unknown"


def update_version_in_init():
    """Update version in __init__.py file."""
    init_file = Path(__file__).parent / "keynote_slides_freezer" / "__init__.py"
    version = get_git_version()
    
    if init_file.exists():
        content = init_file.read_text()
        # Replace version using regex
        new_content = re.sub(
            r'__version__ = [\'"][^\'"]*[\'"]',
            f'__version__ = "{version}"',
            content
        )
        init_file.write_text(new_content)
        print(f"Updated version to {version}")
    else:
        print(f"Init file not found: {init_file}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "update":
        update_version_in_init()
    else:
        print(get_git_version())
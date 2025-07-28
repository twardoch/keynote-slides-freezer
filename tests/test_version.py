"""Test version management."""

import pytest
import re
import platform


def test_version_format():
    """Test that version follows semantic versioning format."""
    # Import version directly to avoid dependency issues
    try:
        from keynote_slides_freezer import __version__
    except ImportError:
        # If full import fails, try to get version from __init__.py directly
        import os
        import sys
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
        
        # Read version from __init__.py
        init_file = os.path.join(os.path.dirname(__file__), '..', 'keynote_slides_freezer', '__init__.py')
        with open(init_file, 'r') as f:
            content = f.read()
        
        # Extract version using regex
        version_match = re.search(r'__version__ = [\'"]([^\'"]*)[\'"]', content)
        if version_match:
            __version__ = version_match.group(1)
        else:
            pytest.fail("Could not find version in __init__.py")
    
    # Should match semver format: major.minor.patch[.dev[N]+commit]
    semver_pattern = r'^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:\.dev(?P<dev>\d+)\+(?P<commit>[a-f0-9]+))?$'
    
    assert re.match(semver_pattern, __version__), f"Version {__version__} does not match semver pattern"


def test_version_exists():
    """Test that version is defined."""
    try:
        from keynote_slides_freezer import __version__
    except ImportError:
        # If full import fails, try to get version from __init__.py directly
        import os
        import sys
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
        
        # Read version from __init__.py
        init_file = os.path.join(os.path.dirname(__file__), '..', 'keynote_slides_freezer', '__init__.py')
        with open(init_file, 'r') as f:
            content = f.read()
        
        # Extract version using regex
        version_match = re.search(r'__version__ = [\'"]([^\'"]*)[\'"]', content)
        if version_match:
            __version__ = version_match.group(1)
        else:
            pytest.fail("Could not find version in __init__.py")
    
    assert __version__ is not None
    assert isinstance(__version__, str)
    assert len(__version__) > 0
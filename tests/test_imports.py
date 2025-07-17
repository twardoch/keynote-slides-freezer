"""Test basic imports work correctly."""

import pytest
import sys
import platform


def test_import_main_module():
    """Test that main module imports correctly."""
    try:
        import keynote_slides_freezer
        assert hasattr(keynote_slides_freezer, '__version__')
        # Only test KeynoteSlidesFreezer import on macOS
        if platform.system() == 'Darwin':
            assert hasattr(keynote_slides_freezer, 'KeynoteSlidesFreezer')
    except ImportError as e:
        # Expected on non-macOS systems due to macOS-specific dependencies
        if platform.system() != 'Darwin':
            pytest.skip(f"Skipping on {platform.system()}: {e}")
        else:
            pytest.fail(f"Failed to import keynote_slides_freezer: {e}")


def test_import_cli():
    """Test that CLI module imports correctly."""
    try:
        from keynote_slides_freezer import cli
        assert hasattr(cli, 'main')
    except ImportError as e:
        # Expected on non-macOS systems
        if platform.system() != 'Darwin':
            pytest.skip(f"Skipping on {platform.system()}: {e}")
        else:
            pytest.fail(f"Failed to import keynote_slides_freezer.cli: {e}")


@pytest.mark.skipif(platform.system() != 'Darwin', reason="macOS-only test")
def test_import_freezer_class():
    """Test that KeynoteSlidesFreezer class can be imported."""
    try:
        from keynote_slides_freezer import KeynoteSlidesFreezer
        assert KeynoteSlidesFreezer is not None
    except ImportError as e:
        pytest.fail(f"Failed to import KeynoteSlidesFreezer: {e}")


@pytest.mark.skipif(platform.system() != 'Darwin', reason="macOS-only test")
def test_class_initialization():
    """Test that KeynoteSlidesFreezer can be instantiated (basic structure test)."""
    # Note: This test only checks if the class can be imported and has expected methods
    # Actual functionality testing would require macOS/Keynote environment
    from keynote_slides_freezer import KeynoteSlidesFreezer
    
    # Check if class has expected methods
    assert hasattr(KeynoteSlidesFreezer, 'process')
    assert callable(getattr(KeynoteSlidesFreezer, 'process'))
    
    # Note: We don't actually instantiate the class here because it requires
    # macOS-specific dependencies and Keynote to be available
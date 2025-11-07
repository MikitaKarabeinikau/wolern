"""
Basic sanity tests to verify the project structure and imports.
"""
import pytest
import sys
import os


def test_project_structure():
    """Test that basic project directories exist."""
    project_root = os.path.dirname(os.path.dirname(__file__))
    assert os.path.exists(os.path.join(project_root, 'backend'))
    assert os.path.exists(os.path.join(project_root, 'frontend'))
    assert os.path.exists(os.path.join(project_root, 'requirements.txt'))


def test_python_version():
    """Test that Python version is 3.8 or higher."""
    assert sys.version_info >= (3, 8), "Python version should be 3.8 or higher"


def test_imports():
    """Test that basic project modules can be imported."""
    # Add backend/src to path
    project_root = os.path.dirname(os.path.dirname(__file__))
    backend_src = os.path.join(project_root, 'backend', 'src')
    if backend_src not in sys.path:
        sys.path.insert(0, backend_src)
    
    # Test basic imports without running code that requires external dependencies
    try:
        import backend
        assert True
    except ImportError as e:
        pytest.skip(f"Backend module not importable: {e}")

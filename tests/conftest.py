"""
Test configuration for M.I.A project
"""

import sys
import os
from pathlib import Path
import pytest

# Add src directory to Python path
project_root = Path(__file__).parent.parent
src_dir = project_root / 'src'

if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

# Add project root to path as well
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Set up test environment
os.environ['MIA_TEST_MODE'] = '1'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress TensorFlow warnings in tests
os.environ['TRANSFORMERS_VERBOSITY'] = 'error'

@pytest.fixture(scope="session")
def test_config():
    """Provide test configuration."""
    return {
        'test_mode': True,
        'disable_external_apis': True,
        'mock_llm': True
    }

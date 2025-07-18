"""
Test for optional dependencies handling
"""
import unittest
from unittest.mock import patch
import sys

from mia.utils.optional_deps import (
    OptionalDependency,
    get_optional_dependency,
    check_all_dependencies,
    get_missing_dependencies,
    get_available_dependencies,
    safe_import
)


class TestOptionalDependencies(unittest.TestCase):
    
    def test_optional_dependency_available(self):
        """Test when dependency is available."""
        # Test with a standard library module that should always be available
        dep = OptionalDependency('os', 'operating system operations')
        self.assertTrue(dep.available)
        self.assertIsNotNone(dep.module)
    
    def test_optional_dependency_unavailable(self):
        """Test when dependency is not available."""
        dep = OptionalDependency('nonexistent_module_xyz', 'fake feature')
        self.assertFalse(dep.available)
        self.assertIsNone(dep.module)
    
    def test_optional_dependency_with_fallback(self):
        """Test fallback functionality."""
        fallback_value = "fallback"
        dep = OptionalDependency('nonexistent_module_xyz', 'fake feature', fallback_value)
        self.assertFalse(dep.available)
        self.assertEqual(dep.module, fallback_value)
    
    def test_get_optional_dependency(self):
        """Test getting predefined dependencies."""
        psutil_dep = get_optional_dependency('psutil')
        self.assertIsInstance(psutil_dep, OptionalDependency)
        self.assertEqual(psutil_dep.module_name, 'psutil')
        
        # Test unknown dependency
        unknown_dep = get_optional_dependency('unknown_dep')
        self.assertEqual(unknown_dep.module_name, 'unknown_dep')
    
    def test_check_all_dependencies(self):
        """Test checking all dependencies."""
        status = check_all_dependencies()
        self.assertIsInstance(status, dict)
        # Should contain at least the predefined dependencies
        self.assertIn('psutil', status)
        self.assertIn('torch', status)
    
    def test_missing_and_available_dependencies(self):
        """Test getting missing and available dependencies."""
        missing = get_missing_dependencies()
        available = get_available_dependencies()
        
        self.assertIsInstance(missing, list)
        self.assertIsInstance(available, list)
        
        # No overlap between missing and available
        self.assertEqual(set(missing) & set(available), set())
    
    def test_safe_import(self):
        """Test safe import functionality."""
        # Test with available module
        os_module = safe_import('os', 'operating system')
        self.assertIsNotNone(os_module)
        
        # Test with unavailable module
        fake_module = safe_import('nonexistent_module_xyz', 'fake feature')
        self.assertIsNone(fake_module)
        
        # Test with fallback
        fallback_value = "fallback"
        fake_with_fallback = safe_import('nonexistent_module_xyz', 'fake feature', fallback_value)
        self.assertEqual(fake_with_fallback, fallback_value)

    @patch.dict('sys.modules', {'test_module': None})
    def test_import_error_handling(self):
        """Test proper handling of import errors."""
        dep = OptionalDependency('test_module', 'test feature')
        # Should handle the import error gracefully
        self.assertFalse(dep.available)


if __name__ == '__main__':
    unittest.main()
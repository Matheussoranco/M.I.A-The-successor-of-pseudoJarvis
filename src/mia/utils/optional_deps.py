"""
Optional dependency handler for M.I.A
Provides graceful handling of missing optional dependencies.
"""
import importlib
import logging
from typing import Optional, Any, Dict, List

logger = logging.getLogger(__name__)

class OptionalDependency:
    """Handle optional dependencies gracefully."""
    
    def __init__(self, module_name: str, feature_name: str = None, fallback: Any = None):
        self.module_name = module_name
        self.feature_name = feature_name or module_name
        self.fallback = fallback
        self._module = None
        self._available = None
    
    @property
    def available(self) -> bool:
        """Check if the dependency is available."""
        if self._available is None:
            try:
                self._module = importlib.import_module(self.module_name)
                self._available = True
                logger.debug(f"Optional dependency '{self.module_name}' available")
            except ImportError:
                self._available = False
                logger.info(f"Optional dependency '{self.module_name}' not available - {self.feature_name} features disabled")
        return self._available
    
    @property
    def module(self) -> Optional[Any]:
        """Get the module if available."""
        if self.available:
            return self._module
        return self.fallback

# Define optional dependencies
OPTIONAL_DEPS = {
    'psutil': OptionalDependency('psutil', 'system monitoring'),
    'torch': OptionalDependency('torch', 'PyTorch models'),
    'transformers': OptionalDependency('transformers', 'Hugging Face models'),
    'sounddevice': OptionalDependency('sounddevice', 'audio recording'),
    'opencv-python': OptionalDependency('cv2', 'computer vision'),
    'PIL': OptionalDependency('PIL', 'image processing'),
    'redis': OptionalDependency('redis', 'Redis caching'),
    'chromadb': OptionalDependency('chromadb', 'vector database'),
    'openai': OptionalDependency('openai', 'OpenAI API'),
}

def get_optional_dependency(name: str) -> OptionalDependency:
    """Get an optional dependency handler."""
    return OPTIONAL_DEPS.get(name, OptionalDependency(name))

def check_all_dependencies() -> Dict[str, bool]:
    """Check status of all optional dependencies."""
    return {name: dep.available for name, dep in OPTIONAL_DEPS.items()}

def get_missing_dependencies() -> List[str]:
    """Get list of missing optional dependencies."""
    return [name for name, dep in OPTIONAL_DEPS.items() if not dep.available]

def get_available_dependencies() -> List[str]:
    """Get list of available optional dependencies."""
    return [name for name, dep in OPTIONAL_DEPS.items() if dep.available]

def safe_import(module_name: str, feature_name: str = None, fallback: Any = None) -> Any:
    """Safely import a module with fallback."""
    dep = OptionalDependency(module_name, feature_name, fallback)
    return dep.module
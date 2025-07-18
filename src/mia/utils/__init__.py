# Utils module init
# Use lazy imports to avoid dependency issues

# Export the optional_deps module directly
from .optional_deps import (
    OptionalDependency,
    get_optional_dependency, 
    check_all_dependencies,
    get_missing_dependencies,
    get_available_dependencies,
    safe_import
)

# Lazy loading functions for modules with external dependencies
def load_automation_util():
    """Load automation utilities if dependencies are available."""
    try:
        from . import automation_util
        return automation_util
    except ImportError:
        return None

def load_email_util():
    """Load email utilities if dependencies are available."""
    try:
        from . import email_util
        return email_util
    except ImportError:
        return None

def load_note_taking_utils():
    """Load note taking utilities if dependencies are available."""
    try:
        from . import note_taking_utils
        return note_taking_utils
    except ImportError:
        return None

def load_message_util():
    """Load message utilities if dependencies are available."""
    try:
        from . import message_util
        return message_util
    except ImportError:
        return None

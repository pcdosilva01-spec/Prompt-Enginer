"""Public compatibility facade for the host target catalog."""
from .targets import TARGETS, TargetError, TargetSpec, detect_available_targets, list_targets, resolve_skill_path

__all__ = [
    "TARGETS", "TargetError", "TargetSpec", "detect_available_targets",
    "list_targets", "resolve_skill_path",
]

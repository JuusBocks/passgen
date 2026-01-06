from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class PasswordPolicy:
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    require_uppercase: bool = False
    require_lowercase: bool = False
    require_digit: bool = False
    require_special: bool = False
    allowed_special: Optional[str] = None
    disallowed_characters: List[str] = field(default_factory=list)
    no_spaces: bool = False
    no_reuse: bool = False
    notes: str = ""
    # Exclusion flags for entire character classes
    exclude_digits: bool = False
    exclude_uppercase: bool = False
    exclude_lowercase: bool = False



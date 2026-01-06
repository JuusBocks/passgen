import secrets
import string
from passgen.constants import ALLOWED_SPECIAL_CHARS
from passgen.core.policy import PasswordPolicy


class PasswordGenerator:
    def __init__(self, allowed_special_chars: str | None = None):
        self.allowed_special_chars = allowed_special_chars or ALLOWED_SPECIAL_CHARS

    def generate_random(self, length: int, include_uppercase: bool, include_lowercase: bool, include_numbers: bool, include_special: bool) -> str:
        character_set = ""
        if include_uppercase:
            character_set += string.ascii_uppercase
        if include_lowercase:
            character_set += string.ascii_lowercase
        if include_numbers:
            character_set += string.digits
        if include_special:
            character_set += self.allowed_special_chars
        if not character_set:
            raise ValueError("No character types selected")
        return "".join(secrets.choice(character_set) for _ in range(length))

    def generate_from_policy(self, policy: PasswordPolicy) -> str:
        # Priority Level 1: Start with base character sets
        allowed_upper = string.ascii_uppercase
        allowed_lower = string.ascii_lowercase
        allowed_digits = string.digits
        allowed_special = policy.allowed_special if policy.allowed_special else self.allowed_special_chars

        # Priority Level 1: Apply class-level exclusions first
        if policy.exclude_uppercase:
            allowed_upper = ""
        if policy.exclude_lowercase:
            allowed_lower = ""
        if policy.exclude_digits:
            allowed_digits = ""

        # Priority Level 1: Apply individual character exclusions (disallowed_characters)
        if policy.disallowed_characters:
            dis = set(policy.disallowed_characters)
            allowed_upper = "".join(c for c in allowed_upper if c not in dis)
            allowed_lower = "".join(c for c in allowed_lower if c not in dis)
            allowed_digits = "".join(c for c in allowed_digits if c not in dis)
            allowed_special = "".join(c for c in allowed_special if c not in dis)

        # No spaces
        if policy.no_spaces:
            allowed_special = allowed_special.replace(" ", "")

        # Decide length (strict enforcement)
        target_length = 16  # Default
        
        # If both min and max are set (including "exactly N" case), use exact value
        if policy.min_length is not None and policy.max_length is not None:
            if policy.min_length == policy.max_length:
                # Exact length specified
                target_length = policy.min_length
            else:
                # Range specified, prefer max but respect min
                target_length = policy.max_length
                if target_length < policy.min_length:
                    target_length = policy.min_length
        elif policy.max_length is not None:
            target_length = min(target_length, policy.max_length)
        elif policy.min_length is not None:
            target_length = max(target_length, policy.min_length)
        
        # Clamp to reasonable bounds
        target_length = max(1, min(128, target_length))

        # If nothing specified, include all non-excluded types
        if not any([policy.require_uppercase, policy.require_lowercase, policy.require_digit, policy.require_special]):
            if not policy.exclude_uppercase:
                policy.require_uppercase = True
            if not policy.exclude_lowercase:
                policy.require_lowercase = True
            if not policy.exclude_digits:
                policy.require_digit = True
            # Only include special chars if allowed_special is defined or no explicit exclusion
            if policy.allowed_special or not policy.exclude_digits:
                policy.require_special = True

        # Build character set respecting exclusions
        character_set = ""
        if policy.require_uppercase and allowed_upper and not policy.exclude_uppercase:
            character_set += allowed_upper
        if policy.require_lowercase and allowed_lower and not policy.exclude_lowercase:
            character_set += allowed_lower
        if policy.require_digit and allowed_digits and not policy.exclude_digits:
            character_set += allowed_digits
        if policy.require_special and allowed_special:
            character_set += allowed_special
        
        # Fallback if no valid character set
        if not character_set:
            if allowed_upper:
                character_set += allowed_upper
            if allowed_lower:
                character_set += allowed_lower
            if not character_set:
                raise ValueError("No valid characters available for password generation after applying constraints")

        # Seed password with required character types
        password_list = []
        if policy.require_uppercase and allowed_upper and not policy.exclude_uppercase:
            password_list.append(secrets.choice(allowed_upper))
        if policy.require_lowercase and allowed_lower and not policy.exclude_lowercase:
            password_list.append(secrets.choice(allowed_lower))
        if policy.require_digit and allowed_digits and not policy.exclude_digits:
            password_list.append(secrets.choice(allowed_digits))
        if policy.require_special and allowed_special:
            password_list.append(secrets.choice(allowed_special))

        while len(password_list) < target_length:
            ch = secrets.choice(character_set)
            if policy.disallowed_characters and ch in policy.disallowed_characters:
                continue
            if policy.no_spaces and ch == " ":
                continue
            password_list.append(ch)

        secrets.SystemRandom().shuffle(password_list)
        return "".join(password_list)



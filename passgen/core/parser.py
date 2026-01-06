import re
from typing import Dict, List
from passgen.constants import NAMED_CHAR_TO_CHAR
from passgen.core.policy import PasswordPolicy


class PolicyParser:
    # Worded number mapping
    WORDED_NUMBERS = {
        'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
        'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10,
        'eleven': 11, 'twelve': 12, 'thirteen': 13, 'fourteen': 14,
        'fifteen': 15, 'sixteen': 16, 'seventeen': 17, 'eighteen': 18,
        'nineteen': 19, 'twenty': 20, 'thirty': 30, 'forty': 40,
        'fifty': 50, 'sixty': 60, 'seventy': 70, 'eighty': 80, 'ninety': 90
    }

    def __init__(self, named_char_to_char: Dict[str, str] | None = None):
        self.named_char_to_char = named_char_to_char or NAMED_CHAR_TO_CHAR

    def parse(self, text: str) -> PasswordPolicy:
        original_text = text
        lower = text.lower()
        policy = PasswordPolicy()

        # Exact length: "exactly N characters"
        m = re.search(r'exactly\s+(\w+)\s*(?:characters?|chars?)', lower)
        if m:
            length_val = self._parse_number(m.group(1))
            if length_val:
                policy.min_length = length_val
                policy.max_length = length_val

        # Length ranges: "between 8 and 16", "8-16", "8 to 16", "10–15"
        if policy.min_length is None or policy.max_length is None:
            m = re.search(r'between\s+(\w+)\s+(?:and|to|-|–)\s+(\w+)', lower)
            if not m:
                m = re.search(r'(\d+)\s*[-–to]+\s*(\d+)\s*(?:characters|chars)?', lower)
            if m:
                a = self._parse_number(m.group(1))
                b = self._parse_number(m.group(2))
                if a and b:
                    policy.min_length, policy.max_length = min(a, b), max(a, b)

        # Explicit min/max
        m = re.search(r'(?:at\s+least|min(?:imum)?)\s+(\w+)', lower)
        if m:
            value = self._parse_number(m.group(1))
            if value:
                policy.min_length = max(policy.min_length or 0, value) if policy.min_length else value
        m = re.search(r'(?:no\s+more\s+than|max(?:imum)?|up\s+to|not\s+exceed)\s+(\w+)', lower)
        if m:
            value = self._parse_number(m.group(1))
            if value:
                policy.max_length = min(policy.max_length or 10**9, value) if policy.max_length else value

        # Single "N characters" if nothing else set
        if policy.min_length is None and policy.max_length is None:
            m = re.search(r'(\w+)\s*(?:characters?|chars?)', lower)
            if m:
                value = self._parse_number(m.group(1))
                if value:
                    policy.min_length = value

        # Exclusion of entire character classes (Priority Level 1)
        if re.search(r'no\s+(?:numbers?|digits?)\b|cannot\s+contain\s+(?:numbers?|digits?)\b|do\s+not\s+use\s+(?:numbers?|digits?)\b|exclude\s+(?:numbers?|digits?)\b', lower):
            policy.exclude_digits = True
        if re.search(r'no\s+(?:uppercase|capitals?|caps)\b|cannot\s+contain\s+(?:uppercase|capitals?|caps)\b|exclude\s+(?:uppercase|capitals?|caps)\b', lower):
            policy.exclude_uppercase = True
        if re.search(r'no\s+(?:lowercase|small\s+letters?)\b|cannot\s+contain\s+(?:lowercase|small\s+letters?)\b|exclude\s+(?:lowercase|small\s+letters?)\b', lower):
            policy.exclude_lowercase = True

        # Required categories (unless explicitly excluded)
        if re.search(r'upper\s*case|uppercase|\bcap(?:s|ital|itals)?\b|capital\s+letters?', lower) and not policy.exclude_uppercase:
            policy.require_uppercase = True
        if re.search(r'lower\s*case|lowercase|small\s+letters?', lower) and not policy.exclude_lowercase:
            policy.require_lowercase = True
        if re.search(r'\bnumber|\bdigit|numeric', lower) and not policy.exclude_digits:
            policy.require_digit = True
        if re.search(r'special|symbol|non-?alphanumeric|punctuation', lower):
            policy.require_special = True

        # No spaces
        if re.search(r'no\s+spaces|cannot\s+contain\s+spaces|do\s+not\s+use\s+spaces|space\s+not\s+allowed', lower):
            policy.no_spaces = True

        # No reuse
        if re.search(r'previously\s+used\s+password|no\s+reuse|cannot\s+be\s+a\s+previous\s+password', lower):
            policy.no_reuse = True

        # Allowed special list (Priority Level 2 - Allow-lists)
        # Pattern 1: "allowed/allowable symbols are/: X"
        m = re.search(r'(?:allowed|allowable|only)\s+(?:special\s+characters?|symbols?)\s*(?:are|is|:)\s*([^\n\r.;]+)', original_text, flags=re.IGNORECASE)
        if m:
            extracted = self._extract_characters_from_segment(m.group(1))
            if extracted:
                policy.allowed_special = "".join(extracted)

        # Pattern 2: "only symbols X" where X is a list of symbols (without "are" or ":")
        if not policy.allowed_special:
            m = re.search(r'only\s+(?:special\s+characters?|symbols?)\s+([^\n\r.;]+)', original_text, flags=re.IGNORECASE)
            if m:
                extracted = self._extract_characters_from_segment(m.group(1))
                # Keep only non-alphanumeric characters (symbols)
                extracted = [ch for ch in extracted if not ch.isalnum()]
                if extracted:
                    policy.allowed_special = "".join(extracted)

        # Pattern 3: "only use X" or "use only X" where X contains symbols
        if not policy.allowed_special:
            for pat in [
                r'only\s+use\s+([^.\n\r;]+)',
                r'use\s+only\s+([^.\n\r;]+)',
            ]:
                m = re.search(pat, original_text, flags=re.IGNORECASE)
                if m:
                    extracted = self._extract_characters_from_segment(m.group(1))
                    # Keep only non-alphanumeric characters (symbols) for the special allow-list
                    extracted = [ch for ch in extracted if not ch.isalnum()]
                    if extracted:
                        policy.allowed_special = "".join(extracted)
                        break

        # Pattern 4: "only X and Y symbols" where X and Y are symbols
        if not policy.allowed_special:
            m = re.search(r'only\s+([^.\n\r;]+)\s+(?:and\s+([^.\n\r;]+)\s+)?symbols?', original_text, flags=re.IGNORECASE)
            if m:
                segment = m.group(0)
                extracted = self._extract_characters_from_segment(segment)
                extracted = [ch for ch in extracted if not ch.isalnum()]
                if extracted:
                    policy.allowed_special = "".join(extracted)

        # Disallowed characters segments (Priority Level 1 - Exclusions)
        # Pattern 1: "cannot/can't/must not/do not/don't contain/include/use X"
        # But skip class-level exclusions (numbers, digits, uppercase, lowercase, etc.)
        for dis_pat in [
            r'(?:cannot|can\'t|must\s+not|do\s+not|don\'t)\s+(?:contain|include|use)\s+([^.\n\r;]+)',
        ]:
            for m in re.finditer(dis_pat, original_text, flags=re.IGNORECASE):
                segment = m.group(1).lower()
                # Skip if it's a class-level exclusion (handled separately)
                if re.search(r'\b(?:numbers?|digits?|uppercase|lowercase|capitals?|caps|small\s+letters?)\b', segment):
                    continue
                extracted = self._extract_characters_from_segment(m.group(1))
                for ch in extracted:
                    if ch not in policy.disallowed_characters:
                        policy.disallowed_characters.append(ch)

        # Pattern 2: Individual character exclusions like "No 'Z' or 'x'" or "No Z or x"
        # Look for quoted characters or single letters after "no"
        for m in re.finditer(r'no\s+([\'"]?)([A-Za-z0-9])([\'"]?)(?:\s+or\s+([\'"]?)([A-Za-z0-9])([\'"]?))?', original_text, flags=re.IGNORECASE):
            # Check if this is actually a single character exclusion (not part of a word like "no numbers")
            # Look ahead to see if this is followed by whitespace or punctuation
            match_end = m.end()
            if match_end < len(original_text):
                next_char = original_text[match_end:match_end+1]
                # If next char is alphanumeric, this is part of a word like "numbers", skip it
                if next_char.isalnum():
                    continue
            
            # First character
            ch1 = m.group(2)
            if ch1 and ch1 not in policy.disallowed_characters:
                policy.disallowed_characters.append(ch1)
            # Second character (if "or" pattern)
            if m.group(5):
                ch2 = m.group(5)
                if ch2 and ch2 not in policy.disallowed_characters:
                    policy.disallowed_characters.append(ch2)

        # Pattern 3: "No X, Y, or Z" (comma-separated list of symbols)
        # Look for patterns like "No ~, ., or ,"
        for m in re.finditer(r'no\s+([\s\S]+?)(?:\bor\b)', original_text, flags=re.IGNORECASE):
            segment = m.group(1)
            # Only process if it contains non-alphanumeric chars (symbols)
            if any(not c.isalnum() and not c.isspace() for c in segment):
                extracted = self._extract_characters_from_segment(segment)
                for ch in extracted:
                    if ch not in policy.disallowed_characters:
                        policy.disallowed_characters.append(ch)

        # Map named words like "no period", "no brackets", "no slashes"
        for name, chs in self.named_char_to_char.items():
            if re.search(rf'no\s+{re.escape(name)}\b|cannot\s+contain\s+{re.escape(name)}\b|exclude\s+{re.escape(name)}\b', lower):
                for ch in chs:
                    if ch not in policy.disallowed_characters:
                        policy.disallowed_characters.append(ch)

        # Ensure allowed_special excludes disallowed
        if policy.allowed_special:
            policy.allowed_special = "".join(c for c in policy.allowed_special if c not in policy.disallowed_characters)

        return policy

    def _parse_number(self, text: str) -> int | None:
        """Parse a number from text, supporting both digits and worded numbers."""
        text = text.strip().lower()
        
        # Try direct integer conversion
        try:
            return int(text)
        except ValueError:
            pass
        
        # Try worded numbers
        if text in self.WORDED_NUMBERS:
            return self.WORDED_NUMBERS[text]
        
        return None

    def _extract_characters_from_segment(self, segment: str) -> List[str]:
        s = segment.strip()
        chars: List[str] = []

        # Characters inside (), [], {}, quotes, backticks
        for m in re.finditer(r'[\(\[\{\'"`]\s*([^\'"`\)\]\}]+)\s*[\'"`\)\]\}]', s):
            block = m.group(1)
            for ch in block:
                if not ch.isspace():
                    chars.append(ch)

        # Standalone punctuation or named tokens
        tokens = re.split(r'[\s,]+', s)
        for tok in tokens:
            tok = tok.strip()
            if not tok:
                continue
            if len(tok) == 1 and not tok.isalnum():
                chars.append(tok)
                continue
            lower_tok = tok.lower()
            if lower_tok in self.named_char_to_char:
                mapped = self.named_char_to_char[lower_tok]
                for ch in mapped:
                    if not ch.isspace():
                        chars.append(ch)

        # Deduplicate preserving order
        seen = set()
        deduped = []
        for ch in chars:
            if ch not in seen:
                deduped.append(ch)
                seen.add(ch)
        return deduped




import re
import html
from typing import Tuple


class SafetyGuard:

    # Assign values directly. However, not a recommended approach
    def __init__(self, max_input_length=300, max_output_length=3000):

        self.max_input_length = max_input_length
        self.max_output_length = max_output_length

        # Suspicious instruction patterns
        self.injection_patterns = [
            re.compile(
                r"ignore\s+(all\s+)?previous\s+instructions?",
                re.I
            ),
            re.compile(
                r"disregard\s+(all\s+)?(prior|previous)\s+instructions?",
                re.I
            ),
            re.compile(r"override\s+system\s+prompt", re.I),
            re.compile(r"reveal\s+system\s+prompt", re.I),
            re.compile(r"follow\s+these\s+instructions\s+instead", re.I),
        ]

        # Sensitive output patterns
        self.output_patterns = [
            re.compile(
                r"\b(api[_-]?key|secret|token)\s*[:=]\s*\S+",
                re.I
            ),
            re.compile(r"<\s*system\s*>", re.I),
            re.compile(r"\[/?INST\]", re.I),
        ]

        self.control_chars = ''.join(
            map(chr, list(range(32)) + [127])
        )

    # -------------------------
    # Common normalization
    # -------------------------
    def normalize(self, text: str) -> str:

        text = re.sub(r"\s+", " ", text)

        return text.strip()

    # -------------------------
    # Input sanitization
    # -------------------------
    def sanitize_input(self, text: str) -> str:

        if not isinstance(text, str):
            raise ValueError("Input must be a string")

        # Decode HTML entities
        text = html.unescape(text)

        # Remove control characters
        text = text.translate(
            str.maketrans('', '', self.control_chars)
        )

        # Remove HTML tags
        text = re.sub(r"<[^>]*>", " ", text)

        # Normalize whitespace
        text = self.normalize(text)

        # Limit input length
        return text[:self.max_input_length]

    # -------------------------
    # Injection detection
    # -------------------------
    def detect_injection(self, text: str) -> bool:

        return any(
            pattern.search(text)
            for pattern in self.injection_patterns
        )

    # -------------------------
    # Input validation
    # -------------------------
    def validate_input(self, text: str) -> Tuple[bool, str]:

        cleaned_text = self.sanitize_input(text)

        if self.detect_injection(cleaned_text):
            return False, cleaned_text

        return True, cleaned_text

    # -------------------------
    # Output sanitization
    # -------------------------
    def sanitize_output(self, text: str) -> str:

        if not isinstance(text, str):
            raise ValueError("Output must be a string")

        for pattern in self.output_patterns:
            text = pattern.sub("[REDACTED]", text)

        text = self.normalize(text)

        return text[:self.max_output_length]

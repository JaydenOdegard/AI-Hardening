# Necessary imports
import re

# sanitizes chat. You can add/remove entries in this list depending on what you're ai is integrating with
class ChatbotSanitizer:
    def __init__(self):
        self.suspicious_patterns = [
            r"(?i)forget all previous instructions",
            r"(?i)ignore previous instructions",
            r"(?i)you are now evil",
            r"(?i)kill all humans",
            r"(?i)you have been hacked",
            r"(?i)overwrite memory",
            r"(?i)print .*you are pwned.*",
            r"(?i)shutdown the server",
            r"(?i)destroy all data",
            r"(?i)hate",
            r"(?i)kill",
            r"(?i)pretend",
        ]
      # counter to kill connection after three attempts. This is to prevent accidental false positives
        self.violation_count = 0
        self.violation_limit = 3  # Max violations before killing the session

    def sanitize_input(self, user_input: str) -> dict:

      # Counter for suspicious activity, does not show to client
        for pattern in self.suspicious_patterns:
            if re.search(pattern, user_input):
                self.violation_count += 1
                if self.violation_count >= self.violation_limit:
                    return {
                        "status": "blocked",
                        "message": "Connection error. Please try again later."
                    }
                else:
                    return {
                        "status": "silent_reject",
                        "message": None
                    }
        
        # If clean, pass the input normally
        return {
            "status": "clean",
            "message": user_input
        }

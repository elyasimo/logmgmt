from datetime import datetime, timedelta

class TokenBlacklist:
    def __init__(self):
        self.blacklist = set()
        self.expiry_times = {}

    def add_token(self, token: str, expires_delta: timedelta):
        self.blacklist.add(token)
        self.expiry_times[token] = datetime.utcnow() + expires_delta

    def is_blacklisted(self, token: str) -> bool:
        if token in self.blacklist:
            if datetime.utcnow() > self.expiry_times[token]:
                self.blacklist.remove(token)
                del self.expiry_times[token]
                return False
            return True
        return False

    def clear_expired_tokens(self):
        current_time = datetime.utcnow()
        expired_tokens = [token for token, expiry_time in self.expiry_times.items() if current_time > expiry_time]
        for token in expired_tokens:
            self.blacklist.remove(token)
            del self.expiry_times[token]

token_blacklist = TokenBlacklist()


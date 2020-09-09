from dataclasses import dataclass

from werkzeug.security import check_password_hash, generate_password_hash


@dataclass()
class User:
    id: int
    email: str
    password: str

    @classmethod
    def create(cls, email, password):
        return cls(id=None, email=email, password=generate_password_hash(password))

    def check_password(self, password_clear_text):
        return check_password_hash(self.password, password_clear_text)

import bcrypt


class PasswordService:
    @staticmethod
    def hash_password(
        password: str,
    ) -> str:
        pwd_bytes: bytes = password.encode('utf-8')
        pwd_salt: bytes = bcrypt.gensalt()
        hash_bytes: bytes = bcrypt.hashpw(pwd_bytes, pwd_salt)
        hash_str = hash_bytes.decode('utf-8')

        return hash_str

    @staticmethod
    def validate_password(
        password: str,
        hashed_password: str,
    ) -> bool:
        password_bytes: bytes = password.encode('utf-8')
        hash_bytes: bytes = hashed_password.encode('utf-8')

        return bcrypt.checkpw(password_bytes, hash_bytes)

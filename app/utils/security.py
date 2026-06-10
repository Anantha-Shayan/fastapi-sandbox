from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

def hash_password(pwd : str) -> str:
    return password_hash.hash(pwd)

def verify_password(pwd, hashed_pwd):
    return password_hash.verify(pwd, hashed_pwd)
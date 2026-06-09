from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

def hash_password(pwd : str) -> str:
    return password_hash.hash(pwd)
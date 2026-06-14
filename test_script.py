# DLP Test Script
import os
import hashlib

def encrypt_password(password: str) -> str:
    """对密码进行哈希加密"""
    salt = os.urandom(16).hex()
    hashed = hashlib.sha256((password + salt).encode()).hexdigest()
    return f"{salt}:{hashed}"

def verify_password(password: str, stored_hash: str) -> bool:
    """验证密码是否匹配"""
    salt, hashed = stored_hash.split(":")
    return hashlib.sha256((password + salt).encode()).hexdigest() == hashed

if __name__ == "__main__":
    pwd = "mySecretPassword123"
    h = encrypt_password(pwd)
    print(f"加密结果: {h}")
    print(f"验证结果: {verify_password(pwd, h)}")

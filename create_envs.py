import os
os.system("pip install passlib")
from passlib.context import CryptContext
# change with your password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
password = pwd_context.hash(input("Enter your password here: "))
print("HASHED_PASSWORD:")
print(password)
print("SECRET_KEY:")
os.system("openssl rand -hex 32")

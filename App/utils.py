
from passlib.context import CryptContext


# this line defines what hashing algorithm we are using for securing passwords
pwd_context = CryptContext(schemes="bcrypt", deprecated = "auto")

def hash(password: str):
    return(pwd_context.hash(password))
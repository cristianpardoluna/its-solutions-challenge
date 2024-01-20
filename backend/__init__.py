import secrets
import string

def generate_token(length=30) -> str:
    """ Esta función genera una cadena
        aleatoria de 30 chars de largo que
        sirve como demostración de un método de
        autenticación basado en tokens.
    """
    alphabet = string.ascii_letters + string.digits
    token = "".join(secrets.choice(alphabet) for _ in range(length))
    return token


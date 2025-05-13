from passlib.context import CryptContext


CRIPTO = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to hash a password
def hash_password(senha: str, hash_senha: str) -> bool:
    """"
    Function para verificar se a senha está correta, comparando
    a senha em texto puro, informada pelo usuario, e o hash da
    senha que estará salvo no banco de dados.
    """
    return CRIPTO.verify(senha, hash_senha)


def hash_password_create(senha: str) -> str:
    """
    Function para criar o hash da senha, que será salvo no banco de dados.
    """
    return CRIPTO.hash(senha)
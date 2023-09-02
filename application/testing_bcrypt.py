import bcrypt
import hashlib

pas = 'Root.123'
hashed = b'$2b$12$7fzIPS8rX8FGx6NoyJsSAe2BhqjISqWGH/6IByavTx6Oy1bx5uiZS'
hashed1 = b'$2b$12$w/pim2s9zNPhznjoC2meWOBU4dW369IQ79xkLSUnYNBWnT2nf6BRW'
bytes = pas.encode('utf-8')
salt = bcrypt.gensalt()

hash = bcrypt.hashpw(bytes, salt)
print(hash)
# print(bcrypt.checkpw(bytes, hashed1))
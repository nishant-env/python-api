import bcrypt
# import base64


def create_hash(raw_data):
    salt = bcrypt.gensalt()
    encoded_data = raw_data.encode('utf-8')
    hashed_data = bcrypt.hashpw(encoded_data, salt)
    return hashed_data


def verify_pwds(raw_password, hash_password):
    encoded_data = raw_password.encode('utf-8')
    return bcrypt.checkpw(encoded_data, hashed_password=hash_password.encode('utf-8'))
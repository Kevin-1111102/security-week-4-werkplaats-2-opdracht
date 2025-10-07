from werkzeug.security import generate_password_hash, check_password_hash

#secures the hash with unique salt
def hash_password(password):
    return generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)

 #checks if the password is correct
def verify_password(stored_hash, password):
    return check_password_hash(stored_hash, password)

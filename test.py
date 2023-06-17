from werkzeug.security import check_password_hash,generate_password_hash

password='123'
hash_password=generate_password_hash(password)
print(hash_password)
method, salt, hashval = hash_password.split("$", 2)
print(method)
print(salt)
print(hashval)
print(check_password_hash(hash_password, password))
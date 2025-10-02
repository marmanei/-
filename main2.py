import random

chards = "+-/*!&$#?=@abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"

len_password = int(input("Enter length: "))

new_password = ""

for i in range(len_password):
    symbal = random.choice(chards)
    new_password = new_password + symbal

print('Your password: ' + new_password)

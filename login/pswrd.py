import random

def pswrd():

        chars = 'abcdefghijklmnopqrstuvwxyz123456789'
        password = ''
        pa = ''
        for c in range(10):
                pa = random.choice(chars)
                password = password + pa

        print(password)
        return password
p = pswrd()

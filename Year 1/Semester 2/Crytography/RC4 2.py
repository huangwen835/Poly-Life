# Made by Ernest Lee
# RC4 2.py
# Demo of RC4 encryption algorithm
 


def encryption(text, key):
    new_text = []
    for char in text:
        new_text = new_text + [ord(char)]
    new_key = []
    
    for char in key:
        new_key = new_key + [ord(char)]

    
    sch = key_scheduling(new_key)
    key_stream = stream_generation(sch)
    
    ciphertext = ''
    for char in new_text:

        ciphertext += str(hex(char ^ next(key_stream))).upper()

    return ciphertext
    

def decryption(ciphertext, key):
    ciphertext = ciphertext.split('0X')[1:]
    ciphertext = [int('0x' + c.lower(), 0) for c in ciphertext]
    key = [ord(char) for char in key]
    
    sch = key_scheduling(key)
    key_stream = stream_generation(sch)
    print(key_stream)
    
    plaintext = ''
    for char in ciphertext:
        ##split the sch list
        ##key_stream = stream_generation(spliteditem)
        ##
        dec = str(chr(char ^ next(key_stream)))
        plaintext += dec
    
    return plaintext

def key_scheduling(key):
    sch = []
    for i in range(0,256):
        sch = sch + [i]
        
    a = 0
    for b in range(0, 256):
        a = (a + sch[b] + key[b % len(key)]) % 256
        sch[a],sch[b] = sch[b],sch[a]
        
    return sch
    
def stream_generation(sch):
    stream = []
    a = 0
    b = 0
    while True:
        a = (1 + a) % 256
        b = (sch[a] + b) % 256
        sch[a],sch[b] = sch[b],sch[a]

        yield sch[(sch[a] + sch[b]) % 256]    

while True:
    print("RC4 cipher")
    print("----------------------------------")
    print("1. Encryption")
    print("2. Dncryption")
    choice = input('Your choice?: ')
    if choice == '1':
        plaintext = input('Enter plaintext: ')
        key = input('Enter secret key: ')
        result = encryption(plaintext, key)
        print('Result: '+ result)

    elif choice == '2': 
        ciphertext = input('Enter ciphertext: ')
        key = input('Enter secret key: ')
        result = decryption(ciphertext, key)
        print('Result: ' + result)

    else:
        print('Input error, please try again.')

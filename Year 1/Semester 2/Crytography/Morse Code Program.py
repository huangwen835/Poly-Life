
morse_code = { 'A':'.-', 'B':'-...', 'C':'-.-.',
               'D':'-..', 'E':'.', 'F':'..-.',
               'G':'--.', 'H':'....', 'I':'..',
               'J':'.---', 'K':'-.-', 'L':'.-..',
               'M':'--', 'N':'-.', 'O':'---',
               'P':'.--.', 'Q':'--.-', 'R':'.-.',
               'S':'...', 'T':'-', 'U':'..-',
               'V':'...-', 'W':'.--', 'X':'-..-',
               'Y':'-.--', 'Z':'--..',
               '1':'.----', '2':'..---', '3':'...--',
               '4':'....-', '5':'.....', '6':'-....',
               '7':'--...', '8':'---..', '9':'----.',
               '0':'-----', '&':'.-...', "'":'.----.',
               '@':'.--.-.', ')':'-.--.-', '(':'-.--.',
               ':':'---...', ',':'--..--', '=':'-...-',
               '!':'-.-.--', '.':'.-.-.-', '-':'-....-',
               '+':'.-.-.', '"':'.-..-.', '?':'..--..',
               '/':'-..-.',' ':'^'}
 
def encrypt(message):
    message = message.upper()
    cipher = ''
    
    for letter in message:
        cipher += morse_code[letter] + ' '
 
    return cipher

def decrypt(cipher):
    message = ''
    cipher = cipher.split(' ')
    
    for item in range(len(cipher)):
        message += list(morse_code.keys())[list(morse_code.values()).index(cipher[item])]
 
    return message

print("1. Encrypt morse code(alpha --> dot and dash)")
print("2. Decrypt morse code(dot and dash --> alpha)")
choice = input("Your choice: ")
if choice == "1":
    message = input("Enter message to encrypt: ")
    cipher = encrypt(message)
    print(cipher)

elif choice == "2":
    cipher = input("Enter cipher to decrypt: ")
    message = decrypt(cipher)
    print(message)

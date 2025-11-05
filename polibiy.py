# polibiy kvadrati

alphabet = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'
size = 5

# Matrits tuzish
def create_matrix():
    matrix = []
    for i in range(0, len(alphabet), size):
        matrix.append(list(alphabet[i:i+size]))
    return matrix

# Harfni kordinataga o'tkazish
def encrypt_char(matrix, char):
    char = "I" if char == "J" else char.upper()
    for i in range(size):
        for j in range(size):
            if matrix[i][j] == char:
                return str(i+1) + str(j+1)
    return ''

# Matndan shifrlangan kod olish
def encrypt(text):
    matrix = create_matrix()
    encrypted = ''
    for char in text:
        if char.isalpha():
            encrypted += encrypt_char(matrix, char) + ' '
    return encrypted.strip()

# Kordinatani harfga o'tkazish
def decrypt_char(matrix, row, col):
    return matrix[int(row)-1][int(col)-1]

# shifrdan matnni tiklash
def decrypt(code):
    matrix = create_matrix()
    decrypted = ''
    pairs = code.split()
    for pair in pairs:
        if len(pair) == 2 and pair.isdigit():
            decrypted += decrypt_char(matrix, pair[0], pair[1])
    return decrypted

# Misol
text = input("DEShifrlash uchun matnni kiriting: ")
decrypted_text = decrypt(text)

print(f"Shifrdan ochilgan matn: {decrypted_text}")
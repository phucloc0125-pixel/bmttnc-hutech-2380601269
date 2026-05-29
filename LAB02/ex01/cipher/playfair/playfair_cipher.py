class PlayFairCipher:
    
    def __init__(self):
        pass

    # Tạo ma trận PlayFair 5x5
    def create_playfair_matrix(self, key):

        key = key.upper().replace("J", "I")

        matrix = []
        used = set()

        # Thêm ký tự từ key
        for char in key:
            if char not in used and char.isalpha():
                used.add(char)
                matrix.append(char)

        # Bảng chữ cái không có J
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"

        # Thêm các ký tự còn lại
        for char in alphabet:
            if char not in used:
                used.add(char)
                matrix.append(char)

        # Chia thành ma trận 5x5
        playfair_matrix = []

        for i in range(0, 25, 5):
            playfair_matrix.append(matrix[i:i+5])

        return playfair_matrix

    # Tìm tọa độ ký tự trong ma trận
    def find_letter_coords(self, matrix, letter):

        for row in range(5):
            for col in range(5):

                if matrix[row][col] == letter:
                    return row, col

        return None

    # Chuẩn hóa plaintext
    def prepare_text(self, text):

        text = text.upper().replace("J", "I")
        text = text.replace(" ", "")

        prepared = ""
        i = 0

        while i < len(text):

            char1 = text[i]

            if i + 1 < len(text):
                char2 = text[i + 1]

                if char1 == char2:
                    prepared += char1 + "X"
                    i += 1
                else:
                    prepared += char1 + char2
                    i += 2

            else:
                prepared += char1 + "X"
                i += 1

        return prepared

    # Mã hóa
    def playfair_encrypt(self, plain_text, matrix):

        plain_text = self.prepare_text(plain_text)

        encrypted_text = ""

        for i in range(0, len(plain_text), 2):

            pair = plain_text[i:i+2]

            row1, col1 = self.find_letter_coords(matrix, pair[0])
            row2, col2 = self.find_letter_coords(matrix, pair[1])

            # Cùng hàng
            if row1 == row2:

                encrypted_text += matrix[row1][(col1 + 1) % 5]
                encrypted_text += matrix[row2][(col2 + 1) % 5]

            # Cùng cột
            elif col1 == col2:

                encrypted_text += matrix[(row1 + 1) % 5][col1]
                encrypted_text += matrix[(row2 + 1) % 5][col2]

            # Hình chữ nhật
            else:

                encrypted_text += matrix[row1][col2]
                encrypted_text += matrix[row2][col1]

        return encrypted_text

    # Giải mã
    def playfair_decrypt(self, cipher_text, matrix):

        cipher_text = cipher_text.upper()

        decrypted_text = ""

        for i in range(0, len(cipher_text), 2):

            pair = cipher_text[i:i+2]

            row1, col1 = self.find_letter_coords(matrix, pair[0])
            row2, col2 = self.find_letter_coords(matrix, pair[1])

            # Cùng hàng
            if row1 == row2:

                decrypted_text += matrix[row1][(col1 - 1) % 5]
                decrypted_text += matrix[row2][(col2 - 1) % 5]

            # Cùng cột
            elif col1 == col2:

                decrypted_text += matrix[(row1 - 1) % 5][col1]
                decrypted_text += matrix[(row2 - 1) % 5][col2]

            # Hình chữ nhật
            else:

                decrypted_text += matrix[row1][col2]
                decrypted_text += matrix[row2][col1]

        return decrypted_text
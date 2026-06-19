import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from playfair import Ui_MainWindow
import requests


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Kết nối sự kiện nút bấm
        self.ui.btn_encrypt.clicked.connect(self.call_api_encrypt)
        self.ui.btn_decrypt.clicked.connect(self.call_api_decrypt)
        
        # Tự động cập nhật ma trận khi người dùng đổi Key
        self.ui.txt_key.textChanged.connect(self.call_api_matrix)

    def show_error(self, message):
        QMessageBox.warning(self, "Error", message)

    def show_success(self, message):
        QMessageBox.information(self, "Success", message)

    def validate_key(self):
        key = self.ui.txt_key.text().strip()

        if not key:
            self.show_error("Please enter key!")
            return None

        # Khóa của Playfair phải chỉ chứa chữ cái
        cleaned_key = "".join([c for c in key if c.isalpha()])
        if not cleaned_key:
            self.show_error("Key must contain only letters (A-Z)!")
            return None

        return cleaned_key

    def update_matrix_ui(self, matrix):
        """Cập nhật giao diện ma trận 5x5"""
        if not matrix or len(matrix) != 5:
            return
            
        for row in range(5):
            for col in range(5):
                index = row * 5 + col
                letter = matrix[row][col]
                self.ui.matrix_cells[index].setText(letter)

    def call_api_matrix(self):
        key = self.ui.txt_key.text().strip()
        if not key:
            # Clear matrix cells if key is empty
            for cell in self.ui.matrix_cells:
                cell.setText("-")
            return
            
        url = "http://127.0.0.1:5000/api/playfair/creatematrix"
        payload = {"key": key}
        
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                matrix = data.get("playfair_matrix", [])
                self.update_matrix_ui(matrix)
        except Exception as e:
            print("Failed to auto-update matrix:", e)

    def call_api_encrypt(self):
        plain_text = self.ui.txt_plain_text.toPlainText().strip()

        if not plain_text:
            self.show_error("Please enter plain text!")
            return

        key = self.validate_key()
        if key is None:
            return

        url = "http://127.0.0.1:5000/api/playfair/encrypt"
        payload = {
            "plain_text": plain_text,
            "key": key
        }

        try:
            response = requests.post(url, json=payload)

            print("Response status code:", response.status_code)
            print("Response text:", response.text)

            if response.status_code == 200:
                data = response.json()
                self.ui.txt_cipher_text.setPlainText(
                    data.get("encrypted_text", "")
                )
                self.show_success("Encrypted Successfully")
                # Kích hoạt cập nhật lại ma trận để đồng bộ
                self.call_api_matrix()
            else:
                try:
                    data = response.json()
                    self.show_error(
                        data.get("error", "Encryption failed!")
                    )
                except:
                    self.show_error("Encryption failed!")

        except requests.exceptions.RequestException as e:
            self.show_error(
                f"Cannot connect to API!\n{str(e)}"
            )

    def call_api_decrypt(self):
        cipher_text = self.ui.txt_cipher_text.toPlainText().strip()

        if not cipher_text:
            self.show_error("Please enter cipher text!")
            return

        key = self.validate_key()
        if key is None:
            return

        url = "http://127.0.0.1:5000/api/playfair/decrypt"
        payload = {
            "cipher_text": cipher_text,
            "key": key
        }

        try:
            response = requests.post(url, json=payload)

            print("Response status code:", response.status_code)
            print("Response text:", response.text)

            if response.status_code == 200:
                data = response.json()
                self.ui.txt_plain_text.setPlainText(
                    data.get("decrypted_text", "")
                )
                self.show_success("Decrypted Successfully")
                self.call_api_matrix()
            else:
                try:
                    data = response.json()
                    self.show_error(
                        data.get("error", "Decryption failed!")
                    )
                except:
                    self.show_error("Decryption failed!")

        except requests.exceptions.RequestException as e:
            self.show_error(
                f"Cannot connect to API!\n{str(e)}"
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MyApp()
    window.show()

    sys.exit(app.exec_())
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from vigenere import Ui_MainWindow
import requests


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.btn_encrypt.clicked.connect(self.call_api_encrypt)
        self.ui.btn_decrypt.clicked.connect(self.call_api_decrypt)

    def show_error(self, message):
        QMessageBox.warning(self, "Error", message)

    def show_success(self, message):
        QMessageBox.information(self, "Success", message)

    def validate_key(self):
        key = self.ui.txt_key.text().strip()

        if not key:
            self.show_error("Please enter key!")
            return None

        if not key.isalpha():
            self.show_error(
                "Key must contain only letters (A-Z)!"
            )
            return None

        return key

    def call_api_encrypt(self):

        plain_text = self.ui.txt_plain_text.toPlainText().strip()

        if not plain_text:
            self.show_error("Please enter plain text!")
            return

        key = self.validate_key()

        if key is None:
            return

        url = "http://127.0.0.1:5000/api/vigenere/encrypt"

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

        url = "http://127.0.0.1:5000/api/vigenere/decrypt"

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
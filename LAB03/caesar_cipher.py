import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from caesar import Ui_MainWindow
import requests

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.btn_encrypt.clicked.connect(self.call_api_encrypt)
        self.ui.btn_decrypt.clicked.connect(self.call_api_decrypt)

    def validate_input(self, text, key):
        """Hàm kiểm tra tính hợp lệ của dữ liệu đầu vào"""
        # 1. Kiểm tra văn bản có bị trống không
        if not text.strip():
            self.show_message("Cảnh báo", "Vui lòng nhập văn bản cần xử lý!", QMessageBox.Warning)
            return False

        # 2. Kiểm tra khóa Key có bị trống không
        if not key.strip():
            self.show_message("Cảnh báo", "Vui lòng nhập khóa Key!", QMessageBox.Warning)
            return False
            
        # 3. Kiểm tra khóa Key có phải là số nguyên không
        if not key.isdigit():
            self.show_message("Lỗi dữ liệu", "Khóa Key phải là một số nguyên dương!", QMessageBox.Critical)
            return False

        # 4. RÀNG BUỘC PHẠM VI KEY: Chỉ cho phép từ 1 đến 25
        key_val = int(key)
        if key_val < 1 or key_val > 25:
            self.show_message("Lỗi dữ liệu", "Khóa Key của Caesar phải nằm trong khoảng từ 1 đến 25!", QMessageBox.Critical)
            return False

        return True

    def show_message(self, title, content, icon_type):
        """Hàm tiện ích để hiển thị hộp thoại thông báo"""
        msg = QMessageBox()
        msg.setIcon(icon_type)
        msg.setWindowTitle(title)
        msg.setText(content)
        msg.exec_()

    def call_api_encrypt(self):
        plain_text = self.ui.txt_plain_text.toPlainText()
        key_text = self.ui.txt_key.text()

        # Ràng buộc dữ liệu trước khi gửi đi
        if not self.validate_input(plain_text, key_text):
            return

        url = "http://127.0.0.1:5000/api/caesar/encrypt"
        payload = {
            "plain_text": plain_text,
            "key": int(key_text)
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_cipher_text.setText(data["encrypted_message"])
                self.show_message("Thành công", "Mã hóa văn bản thành công!", QMessageBox.Information)
            else:
                self.show_message("Lỗi", "Có lỗi xảy ra từ phía Server API!", QMessageBox.Warning)
        except requests.exceptions.RequestException as e:
            self.show_message("Lỗi kết nối", f"Không thể kết nối đến API Server: {e}", QMessageBox.Critical)

    def call_api_decrypt(self):
        cipher_text = self.ui.txt_cipher_text.toPlainText()
        key_text = self.ui.txt_key.text()

        # Ràng buộc dữ liệu trước khi gửi đi
        if not self.validate_input(cipher_text, key_text):
            return

        url = "http://127.0.0.1:5000/api/caesar/decrypt"
        payload = {
            "cipher_text": cipher_text,
            "key": int(key_text)
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_plain_text.setText(data["decrypted_message"])
                self.show_message("Thành công", "Giải mã văn bản thành công!", QMessageBox.Information)
            else:
                self.show_message("Lỗi", "Có lỗi xảy ra từ phía Server API!", QMessageBox.Warning)
        except requests.exceptions.RequestException as e:
            self.show_message("Lỗi kết nối", f"Không thể kết nối đến API Server: {e}", QMessageBox.Critical)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
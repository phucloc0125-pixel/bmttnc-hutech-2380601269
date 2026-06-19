import os
from flask import Flask, render_template, request, jsonify
from ex01.cipher.caesar.caesar_cipher import CaesarCipher
from ex01.cipher.playfair.playfair_cipher import PlayFairCipher
from ex01.cipher.railfence.railfence_cipher import RailFenceCipher
from ex01.cipher.vigenere.vigenere_cipher import VigenereCipher

# Định nghĩa thư mục templates nằm cùng cấp với file app.py
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))

app = Flask(__name__, template_folder=template_dir)

# Điều hướng cho trang chủ
@app.route("/")
def home():
    return render_template('index.html')

# Điều hướng cho trang Caesar
@app.route("/caesar")
def caesar():
    return render_template('caesar.html')

# Điều hướng cho trang Playfair
@app.route("/playfair")
def playfair():
    return render_template('playfair.html')

# Điều hướng cho trang Rail Fence
@app.route("/railfence")
def railfence():
    return render_template('railfence.html')

# Điều hướng cho trang Vigenere
@app.route("/vigenere")
def vigenere():
    return render_template('vigenere.html')

# API/Action cho Caesar
@app.route("/encrypt", methods=['POST'])
def caesar_encrypt():
    if request.is_json:
        data = request.get_json()
        text = data.get('text', '')
        key = int(data.get('key', 0))
    else:
        text = request.form['inputPlainText']
        key = int(request.form['inputKeyPlain'])
        
    Caesar = CaesarCipher()
    encrypted_text = Caesar.encrypt_text(text, key)
    
    if request.is_json or 'application/json' in request.headers.get('Accept', ''):
        return jsonify({'result': encrypted_text, 'text': text, 'key': key})
        
    return f"text: {text}<br/>key: {key}<br/>encrypted text: {encrypted_text}"

@app.route("/decrypt", methods=['POST'])
def caesar_decrypt():
    if request.is_json:
        data = request.get_json()
        text = data.get('text', '')
        key = int(data.get('key', 0))
    else:
        text = request.form['inputCipherText']
        key = int(request.form['inputKeyCipher'])
        
    Caesar = CaesarCipher()
    decrypted_text = Caesar.decrypt_text(text, key)
    
    if request.is_json or 'application/json' in request.headers.get('Accept', ''):
        return jsonify({'result': decrypted_text, 'text': text, 'key': key})
        
    return f"text: {text}<br/>key: {key}<br/>decrypted text: {decrypted_text}"

# API cho Playfair
@app.route("/playfair/matrix", methods=['POST'])
def playfair_matrix():
    data = request.get_json()
    key = data.get('key', '')
    playfair = PlayFairCipher()
    matrix = playfair.create_playfair_matrix(key)
    return jsonify({'matrix': matrix})

@app.route("/playfair/encrypt", methods=['POST'])
def playfair_encrypt():
    data = request.get_json()
    text = data.get('text', '')
    key = data.get('key', '')
    playfair = PlayFairCipher()
    matrix = playfair.create_playfair_matrix(key)
    result = playfair.playfair_encrypt(text, matrix)
    return jsonify({'result': result, 'matrix': matrix})

@app.route("/playfair/decrypt", methods=['POST'])
def playfair_decrypt():
    data = request.get_json()
    text = data.get('text', '')
    key = data.get('key', '')
    playfair = PlayFairCipher()
    matrix = playfair.create_playfair_matrix(key)
    result = playfair.playfair_decrypt(text, matrix)
    return jsonify({'result': result, 'matrix': matrix})

# API cho Rail Fence
@app.route("/railfence/encrypt", methods=['POST'])
def railfence_encrypt():
    data = request.get_json()
    text = data.get('text', '')
    rails = data.get('rails', 3)
    railfence = RailFenceCipher()
    result = railfence.rail_fence_encrypt(text, rails)
    return jsonify({'result': result})

@app.route("/railfence/decrypt", methods=['POST'])
def railfence_decrypt():
    data = request.get_json()
    text = data.get('text', '')
    rails = data.get('rails', 3)
    railfence = RailFenceCipher()
    result = railfence.rail_fence_decrypt(text, rails)
    return jsonify({'result': result})

# API cho Vigenere
@app.route("/vigenere/encrypt", methods=['POST'])
def vigenere_encrypt_route():
    data = request.get_json()
    text = data.get('text', '')
    key = data.get('key', '')
    vigenere = VigenereCipher()
    result = vigenere.vigenere_encrypt(text, key)
    return jsonify({'result': result})

@app.route("/vigenere/decrypt", methods=['POST'])
def vigenere_decrypt_route():
    data = request.get_json()
    text = data.get('text', '')
    key = data.get('key', '')
    vigenere = VigenereCipher()
    result = vigenere.vigenere_decrypt(text, key)
    return jsonify({'result': result})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
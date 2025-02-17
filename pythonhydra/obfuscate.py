import os
import sys
import argparse
from Crypto.Cipher import AES
import base64
import shutil
import subprocess

KEY = b"1234567890123456"  # 16-byte key (MUST be exactly 16, 24, or 32 bytes)
IV = b"abcdefghijklmnop"  # 16-byte IV (MUST be exactly 16 bytes)

def pad(data):
    return data + (16 - len(data) % 16) * b" "

def encrypt_script(input_file, output_file):
    with open(input_file, "rb") as f:
        plaintext = f.read()

    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    encrypted = cipher.encrypt(pad(plaintext))

    with open(output_file, "wb") as f:
        f.write(encrypted)

    print(f"Encrypted {input_file} -> {output_file}")

def create_loader(output_file="loader.py"):
    loader_code = f"""\
from Crypto.Cipher import AES
import base64

KEY = b"{KEY.decode()}"
IV = b"{IV.decode()}"

def unpad(data):
    return data.rstrip(b" ")

def decrypt_script(input_file):
    with open(input_file, "rb") as f:
        encrypted_data = f.read()

    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    decrypted = unpad(cipher.decrypt(encrypted_data))

    exec(decrypted.decode(), globals())

decrypt_script("script.enc")
"""
    with open(output_file, "w") as f:
        f.write(loader_code)

def compile_exe():
    subprocess.run(["pyinstaller", "--onefile", "--noconsole", "loader.py"])
    shutil.move("dist/loader.exe", "obfuscated.exe")
    print("EXE created: obfuscated.exe")

def main():
    parser = argparse.ArgumentParser(description="Python Obfuscator")
    parser.add_argument("script", help="Python script to obfuscate")
    args = parser.parse_args()

    encrypt_script(args.script, "script.enc")
    create_loader()
    compile_exe()

if __name__ == "__main__":
    main()

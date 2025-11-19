import socket, struct, threading, os, hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

PBKDF2_SALT = b"syntecxhub2025"
PBKDF2_ITER = 150000

def derive_key(p):
    return hashlib.pbkdf2_hmac("sha256", p.encode(), PBKDF2_SALT, PBKDF2_ITER, 32)

def encrypt_msg(key, msg):
    iv = os.urandom(16)
    ct = AES.new(key, AES.MODE_CBC, iv).encrypt(pad(msg.encode(), 16))
    return iv + ct

def decrypt_msg(key, iv, ct):
    return unpad(AES.new(key, AES.MODE_CBC, iv).decrypt(ct), 16).decode()

def recv_loop(sock, key):
    while True:
        header = sock.recv(4)
        if not header: break
        ln = struct.unpack(">I", header)[0]
        body = sock.recv(ln)
        iv, ct = body[:16], body[16:]
        print("\n[Msg]", decrypt_msg(key, iv, ct))
        print("> ", end="")

def main():
    import sys
    if len(sys.argv) < 3:
        print("Usage: python3 client.py <server_ip> <passphrase>")
        return

    key = derive_key(sys.argv[2])
    s = socket.socket()
    s.connect((sys.argv[1], 5000))

    print("[*] Connected. Type messages.\n")
    threading.Thread(target=recv_loop, args=(s,key), daemon=True).start()

    while True:
        msg = input("> ")
        if msg.lower() == "quit": break
        data = encrypt_msg(key, msg)
        s.sendall(struct.pack(">I", len(data)) + data)

main()

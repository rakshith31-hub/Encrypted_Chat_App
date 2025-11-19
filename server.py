import socket, threading, struct, time, hashlib, os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

PBKDF2_SALT = b"syntecxhub2025"
PBKDF2_ITER = 150000

def derive_key(p):  
    return hashlib.pbkdf2_hmac("sha256", p.encode(), PBKDF2_SALT, PBKDF2_ITER, 32)

def decrypt_msg(key, iv, ct):
    return unpad(AES.new(key, AES.MODE_CBC, iv).decrypt(ct), 16).decode()

def broadcast(sender, data):
    for c,_ in clients:
        if c != sender:
            c.sendall(data)

def handle(c,a,key):
    clients.append((c,a))
    try:
        while True:
            header = c.recv(4)
            if not header: break
            ln = struct.unpack(">I", header)[0]
            body = c.recv(ln)

            iv = body[:16]
            ct = body[16:]
            msg = decrypt_msg(key, iv, ct)

            ts = time.strftime("%H:%M:%S")
            print(f"[{ts}] {a}: {msg}")

            broadcast(c, header + body)
    finally:
        c.close()
        clients.remove((c,a))

def main():
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 server.py <passphrase>")
        return

    key = derive_key(sys.argv[1])
    s = socket.socket()
    s.bind(("0.0.0.0", 5000))
    s.listen()

    print("[*] Server running on port 5000")

    while True:
        c,a = s.accept()
        threading.Thread(target=handle, args=(c,a,key), daemon=True).start()

clients = []
main()

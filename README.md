# Encrypted_Chat_App
AES encrypted multi-client chat app (Syntecxhub Week 2 project)
This is a simple encrypted chat application built in Python.  
Multiple clients can connect to the server, send messages, and receive messages securely using AES-256 encryption.

---

## Features
- AES-256 encrypted messaging  
- Multi-client chat (threaded server)  
- PBKDF2 key derivation  
- Server logs chat messages  
- Simple and lightweight

---

## Requirements
Install PyCryptodome: 
pip install pycryptodome

---

## How to Run

### Start the Server
python3 server.py <passphrase>
Example: python3 server.py mypass

### Start the Client
python3 client.py <server_ip> <passphrase>
Example: python3 client.py 127.0.0.1 mypass

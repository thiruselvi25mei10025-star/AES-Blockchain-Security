import tkinter as tk
from tkinter import messagebox
import hashlib
import json
import os
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# AES-256 key
key = AESGCM.generate_key(bit_length=256)
aes = AESGCM(key)

blockchain = []


# Encrypt message using AES
def encrypt_message(message):
    nonce = os.urandom(12)
    encrypted = aes.encrypt(nonce, message.encode(), None)
    return base64.b64encode(nonce + encrypted).decode()


# Decrypt message using AES
def decrypt_message(encrypted_message):
    data = base64.b64decode(encrypted_message)
    nonce = data[:12]
    ciphertext = data[12:]
    return aes.decrypt(nonce, ciphertext, None).decode()


# Calculate block hash
def calculate_hash(block):
    data = {
        "index": block["index"],
        "data": block["data"],
        "previous_hash": block["previous_hash"]
    }
    return hashlib.sha256(
        json.dumps(data, sort_keys=True).encode()
    ).hexdigest()


# Add message to blockchain
def add_block():
    message = input_text.get("1.0", tk.END).strip()

    if not message:
        messagebox.showwarning("Warning", "Enter a message!")
        return

    encrypted = encrypt_message(message)

    previous_hash = (
        blockchain[-1]["hash"] if blockchain else "0"
    )

    block = {
        "index": len(blockchain),
        "data": encrypted,
        "previous_hash": previous_hash
    }

    block["hash"] = calculate_hash(block)
    blockchain.append(block)

    output_text.delete("1.0", tk.END)
    output_text.insert(
        tk.END,
        "Message encrypted and stored!\n\n"
        + "Encrypted Data:\n" + encrypted
        + "\n\nBlock Number: " + str(block["index"])
        + "\nBlock Hash:\n" + block["hash"]
    )


# Display blockchain
def show_blockchain():
    output_text.delete("1.0", tk.END)

    if not blockchain:
        output_text.insert(tk.END, "Blockchain is empty.")
        return

    for block in blockchain:
        output_text.insert(
            tk.END,
            "\nBLOCK " + str(block["index"]) + "\n"
            + "Encrypted Data: " + block["data"] + "\n"
            + "Previous Hash: " + block["previous_hash"] + "\n"
            + "Block Hash: " + block["hash"] + "\n"
            + "-" * 45 + "\n"
        )


# Decrypt latest message
def decrypt_latest():
    if not blockchain:
        messagebox.showwarning("Warning", "No blocks available!")
        return

    try:
        message = decrypt_message(blockchain[-1]["data"])
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, "Decrypted Message:\n" + message)
    except Exception:
        messagebox.showerror("Error", "Decryption failed!")


# Verify blockchain
def verify_blockchain():
    for i, block in enumerate(blockchain):
        if block["hash"] != calculate_hash(block):
            messagebox.showerror(
                "Blockchain", "Invalid! Block data was changed."
            )
            return

        expected_previous = blockchain[i - 1]["hash"] if i > 0 else "0"

        if block["previous_hash"] != expected_previous:
            messagebox.showerror(
                "Blockchain", "Invalid! Block link was changed."
            )
            return

    messagebox.showinfo(
        "Blockchain",
        "Blockchain is valid!" if blockchain
        else "Blockchain is empty."
    )


# GUI window
root = tk.Tk()
root.title("AES Encryption and Blockchain")
root.geometry("750x650")
root.configure(bg="#eef2f7")

title = tk.Label(
    root,
    text="AES + BLOCKCHAIN SECURITY SYSTEM",
    font=("Arial", 19, "bold"),
    bg="#172554",
    fg="white",
    pady=18
)
title.pack(fill="x")

tk.Label(
    root,
    text="Enter your message:",
    font=("Arial", 12, "bold"),
    bg="#eef2f7"
).pack(pady=(15, 5))

input_text = tk.Text(root, height=4, width=75, font=("Arial", 11))
input_text.pack(padx=20)

button_frame = tk.Frame(root, bg="#eef2f7")
button_frame.pack(pady=15)

tk.Button(
    button_frame, text="Encrypt & Add Block",
    command=add_block, bg="#2563eb", fg="white",
    font=("Arial", 10, "bold"), width=18
).grid(row=0, column=0, padx=5, pady=5)

tk.Button(
    button_frame, text="Show Blockchain",
    command=show_blockchain, bg="#0f766e", fg="white",
    font=("Arial", 10, "bold"), width=18
).grid(row=0, column=1, padx=5, pady=5)

tk.Button(
    button_frame, text="Decrypt Latest",
    command=decrypt_latest, bg="#7c3aed", fg="white",
    font=("Arial", 10, "bold"), width=18
).grid(row=1, column=0, padx=5, pady=5)

tk.Button(
    button_frame, text="Verify Blockchain",
    command=verify_blockchain, bg="#15803d", fg="white",
    font=("Arial", 10, "bold"), width=18
).grid(row=1, column=1, padx=5, pady=5)

tk.Label(
    root,
    text="Output / Blockchain Details",
    font=("Arial", 12, "bold"),
    bg="#eef2f7"
).pack(pady=5)

output_text = tk.Text(
    root, height=17, width=85,
    font=("Consolas", 9), wrap="word"
)
output_text.pack(padx=20, pady=(0, 15), fill="both", expand=True)

root.mainloop()
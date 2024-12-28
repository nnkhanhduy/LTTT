# file: main.py
import tkinter as tk
from tkinter import ttk, messagebox
from collections import Counter
from fano import Fano
from huffman import Huffman
from shannon import Shannon
def encode(event=None):
    text = entry.get()
    if not text:
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập chuỗi để mã hóa.")
        return

    frequencies = Counter(text)
    data = dict(frequencies)
    selected_method = combobox.get()

    if selected_method == "Fano":
        encoder = Fano(data)
        encoder.fano()
    elif selected_method == "Huffman":
        encoder = Huffman(data)
        encoder.huffman()
    elif selected_method == "Shannon":
        encoder = Shannon(data)
        encoder.shannon_encoding()
    else:
        messagebox.showerror("Lỗi", "Vui lòng chọn loại mã hóa.")
        return

    codes = encoder.codes
    encoded_text = ''.join([codes[char] for char in text])
    decoded_text = encoder.decode(encoded_text)

    output.delete(1.0, tk.END)
    output.insert(tk.END, f"Chuỗi đã mã hóa: {encoded_text}\n")

    def show_details():
        detail_window = tk.Toplevel(root)
        detail_window.title("Chi tiết mã hóa")
        detail_window.geometry("400x300")

        detail_text = tk.Text(detail_window, wrap="word", width=50, height=15, font=("Arial", 10), bg="#e6f7ff", fg="#000")
        detail_text.pack(pady=10)

        detail_text.insert(tk.END, f"Tần số: {data}\n")
        detail_text.insert(tk.END, f"Mã hóa: {codes}\n")
        detail_text.insert(tk.END, f"Chuỗi đã giải mã: {decoded_text}\n")
        detail_text.config(state=tk.DISABLED)

    detail_button.config(state=tk.NORMAL, command=show_details)

# Giao diện GUI
root = tk.Tk()
root.title("Mã hóa Shannon-Fano và Huffman")
root.geometry("600x400")
root.resizable(False, False)

style = ttk.Style()
style.configure("TFrame", background="#f0f8ff")
style.configure("TLabel", background="#f0f8ff", font=("Arial", 12))
style.configure("TButton", font=("Arial", 10, "bold"))
style.configure("TCombobox", font=("Arial", 10))

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

label = ttk.Label(frame, text="Nhập chuỗi để mã hóa:")
label.grid(row=0, column=0, sticky=tk.W, pady=5)

entry = ttk.Entry(frame, width=50, font=("Arial", 12))
entry.grid(row=0, column=1, sticky=tk.W, pady=5)
entry.bind("<Return>", encode)

label_method = ttk.Label(frame, text="Chọn loại mã hóa:")
label_method.grid(row=1, column=0, sticky=tk.W, pady=5)

combobox = ttk.Combobox(frame, values=["Fano", "Huffman", "Shannon"], state="readonly", font=("Arial", 10))
combobox.grid(row=1, column=1, sticky=tk.W, pady=5)
combobox.set("Chọn loại mã hóa")

button_encode = ttk.Button(frame, text="Mã hóa", command=encode)
button_encode.grid(row=2, column=1, sticky=tk.W, pady=10)

detail_button = ttk.Button(frame, text="Xem chi tiết", state=tk.DISABLED)
detail_button.grid(row=3, column=1, sticky=tk.W, pady=5)

output_label = ttk.Label(frame, text="Kết quả:", font=("Arial", 12, "bold"))
output_label.grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=5)

output = tk.Text(frame, wrap="word", width=70, height=15, font=("Arial", 10), bg="#e6f7ff", fg="#000")
output.grid(row=5, column=0, columnspan=2, pady=10)

root.mainloop()

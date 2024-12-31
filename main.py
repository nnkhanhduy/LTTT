# file: main.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from collections import Counter
from fano import Fano
from huffman import Huffman
from shannon import Shannon
import math

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
        detail_window.geometry("500x400")

        detail_text = tk.Text(detail_window, wrap="word", width=60, height=20, font=("Arial", 10), bg="#e6f7ff", fg="#000")
        detail_text.pack(pady=10)

        detail_text.insert(tk.END, f"Tần số: {data}\n")
        detail_text.insert(tk.END, f"Mã hóa: {codes}\n")
        detail_text.insert(tk.END, f"Chuỗi đã giải mã: {decoded_text}\n")
        detail_text.config(state=tk.DISABLED)

    detail_button.config(state=tk.NORMAL, command=show_details)

def calculate_compression_ratio():
    text = entry.get()
    if not text:
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập chuỗi để mã hóa trước.")
        return

    if not combobox.get() in ["Fano", "Huffman", "Shannon"]:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn phương pháp mã hóa và thực hiện mã hóa trước.")
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

    codes = encoder.codes
    total_count = sum(frequencies.values())
    probabilities = {char: freq / total_count for char, freq in frequencies.items()}
    entropy = -sum(prob * math.log2(prob) for prob in probabilities.values())
    avg_code_length = sum(len(codes[char]) * probabilities[char] for char in codes)
    compression_ratio = entropy / avg_code_length if avg_code_length > 0 else 0

    result_window = tk.Toplevel(root)
    result_window.title("Hệ số nén")
    result_window.geometry("500x300")

    result_text = tk.Text(result_window, wrap="word", width=60, height=15, font=("Arial", 10), bg="#e6f7ff", fg="#000")
    result_text.pack(pady=10)

    result_text.insert(tk.END, f"Entropy: {entropy:.2f}\n")
    result_text.insert(tk.END, f"Độ dài trung bình mã: {avg_code_length:.2f}\n")
    result_text.insert(tk.END, f"Hệ số nén: {compression_ratio:.2f}\n")
    result_text.config(state=tk.DISABLED)

def on_entry_hover(event):
    entry.configure(background="#e0f7fa")

def on_entry_leave(event):
    entry.configure(background="#ffffff")

root = tk.Tk()
root.title("Mã hóa Shannon, Fano và Huffman")
root.geometry("800x600")
root.resizable(False, False)

primary_color = "#2980b9"
secondary_color = "#ecf0f1"
text_color = "#34495e"
font_family = "Arial"

style = ttk.Style()
style.theme_use("clam")

style.configure("TFrame", background=secondary_color)
style.configure("TLabel", background=secondary_color, font=(font_family, 12), foreground=text_color)
style.configure("TButton", font=(font_family, 10, "bold"), foreground="white", background=primary_color, padding=6)
style.map("TButton", background=[("active", "#2471a3")])
style.configure("TCombobox", font=(font_family, 10), foreground=text_color)
style.configure("TEntry", font=(font_family, 12), foreground=text_color)
style.configure("TText", font=(font_family, 10), foreground=text_color, background="#f0f0f0", borderwidth=1, relief="solid")

frame = ttk.Frame(root, padding=20)
frame.pack(fill=tk.BOTH, expand=True)

title_label = ttk.Label(frame, text="NHẬP VÀ CHỌN PHƯƠNG PHÁP MÃ HOÁ", font=(font_family, 18, "bold"), foreground=primary_color)
title_label.pack(pady=(0, 20))

input_frame = ttk.Frame(frame)
input_frame.pack(fill=tk.X, pady=(0, 10))

label = ttk.Label(input_frame, text="Nhập chuỗi:")
label.pack(side=tk.LEFT, padx=(0, 10))

entry = ttk.Entry(input_frame, width=40)
entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
entry.bind("<Return>", lambda e: encode(combobox.get()))

method_frame = ttk.Frame(frame)
method_frame.pack(fill=tk.X, pady=(0, 10))

label_method = ttk.Label(method_frame, text="Chọn phương pháp:")
label_method.pack(side=tk.LEFT, padx=(0, 10))

combobox = ttk.Combobox(method_frame, values=["Fano", "Huffman", "Shannon"], state="readonly")
combobox.pack(side=tk.LEFT, fill=tk.X, expand=True)
combobox.set("Chọn phương pháp")

button_frame = ttk.Frame(frame)
button_frame.pack(fill=tk.X, pady=(10, 20))

button_encode = ttk.Button(button_frame, text="Mã hóa", command=lambda: encode(combobox.get()))
button_encode.pack(side=tk.LEFT, padx=(5, 5))

detail_button = ttk.Button(button_frame, text="Xem chi tiết", state=tk.DISABLED)
detail_button.pack(side=tk.LEFT, padx=(5, 5))

compression_button = ttk.Button(button_frame, text="Tính hệ số nén", command=calculate_compression_ratio)
compression_button.pack(side=tk.LEFT, padx=(5, 5))

output_label = ttk.Label(frame, text="Kết quả:", font=(font_family, 14, "bold"))
output_label.pack()

output = tk.Text(frame, wrap="word", height=15)
output.pack(fill=tk.BOTH, expand=True, pady=(10, 10))

action_frame = ttk.Frame(frame)
action_frame.pack(fill=tk.X, pady=(10, 10))

def copy_to_clipboard():
    try:
        root.clipboard_clear()
        root.clipboard_append(output.get("1.0", tk.END))
        messagebox.showinfo("Đã sao chép", "Đã sao chép kết quả vào clipboard.")
    except tk.TclError:
        messagebox.showerror("Lỗi", "Không thể sao chép kết quả.")

copy_button = ttk.Button(action_frame, text="Sao chép", command=copy_to_clipboard)
copy_button.pack(side=tk.LEFT, padx=(5, 5))

def save_to_file():
    try:
        filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if filename:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(output.get("1.0", tk.END))
            messagebox.showinfo("Đã lưu", f"Đã lưu kết quả vào file: {filename}")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi khi lưu file: {e}")

save_button = ttk.Button(action_frame, text="Lưu", command=save_to_file)
save_button.pack(side=tk.LEFT, padx=(5, 5))

root.mainloop()

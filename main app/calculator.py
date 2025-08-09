import tkinter as tk

def click(button_text):
    current = entry.get()
    entry.delete(0, tk.END)
    entry.insert(0, current + button_text)

def clear():
    entry.delete(0, tk.END)

def calculate():
    try:
        result = eval(entry.get())
        entry.delete(0, tk.END)
        entry.insert(0, str(result))
    except:
        entry.delete(0, tk.END)
        entry.insert(0, "Error")

# Main window
root = tk.Tk()
root.title("Basic Calculator")

entry = tk.Entry(root, width=20, font=("Arial", 18))
entry.grid(row=0, column=0, columnspan=4)

buttons = [
    "7", "8", "9", "+",
    "4", "5", "6", "-",
    "1", "2", "3", "*",
    "0", ".", "/", "="
]

row_val = 1
col_val = 0

for btn in buttons:
    if btn == "=":
        b = tk.Button(root, text=btn, width=5, height=2, command=calculate)
    else:
        b = tk.Button(root, text=btn, width=5, height=2, command=lambda x=btn: click(x))
    b.grid(row=row_val, column=col_val, padx=5, pady=5)
    col_val += 1
    if col_val > 3:
        col_val = 0
        row_val += 1

tk.Button(root, text="C", width=5, height=2, command=clear).grid(row=row_val, column=0, padx=5, pady=5)

root.mainloop()
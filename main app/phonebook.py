import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

# File to store contacts
CONTACTS_FILE = "contacts.json"


# Load contacts from file
def load_contacts():
    if os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, "r") as file:
            return json.load(file)
    return {}


# Save contacts to file
def save_contacts():
    with open(CONTACTS_FILE, "w") as file:
        json.dump(contacts, file, indent=4)


# Add new contact
def add_contact():
    name = simpledialog.askstring("Add Contact", "Enter Name:")
    if not name:
        return
    number = simpledialog.askstring("Add Contact", "Enter Phone Number:")
    email = simpledialog.askstring("Add Contact", "Enter Email:")
    address = simpledialog.askstring("Add Contact", "Enter Address:")

    contacts[name] = {"phone": number, "email": email, "address": address}
    save_contacts()
    refresh_list()
    messagebox.showinfo("Success", f"Contact '{name}' added!")


# Delete selected contact
def delete_contact():
    selected = listbox.curselection()
    if not selected:
        messagebox.showerror("Error", "No contact selected!")
        return
    name = listbox.get(selected)
    if messagebox.askyesno("Confirm Delete", f"Delete '{name}'?"):
        del contacts[name]
        save_contacts()
        refresh_list()


# View contact details
def view_contact():
    selected = listbox.curselection()
    if not selected:
        messagebox.showerror("Error", "No contact selected!")
        return
    name = listbox.get(selected)
    contact = contacts[name]
    messagebox.showinfo("Contact Info",
                        f"Name: {name}\nPhone: {contact['phone']}\nEmail: {contact['email']}\nAddress: {contact['address']}")


# Search for a contact
def search_contact():
    query = simpledialog.askstring("Search", "Enter name or phone:")
    if not query:
        return
    results = [name for name, info in contacts.items() if query.lower() in name.lower() or query in info['phone']]
    if results:
        listbox.delete(0, tk.END)
        for name in results:
            listbox.insert(tk.END, name)
    else:
        messagebox.showinfo("Search", "No contacts found!")


# Update contact
def update_contact():
    selected = listbox.curselection()
    if not selected:
        messagebox.showerror("Error", "No contact selected!")
        return
    name = listbox.get(selected)
    contact = contacts[name]

    number = simpledialog.askstring("Update", "Enter new phone:", initialvalue=contact['phone'])
    email = simpledialog.askstring("Update", "Enter new email:", initialvalue=contact['email'])
    address = simpledialog.askstring("Update", "Enter new address:", initialvalue=contact['address'])

    contacts[name] = {"phone": number, "email": email, "address": address}
    save_contacts()
    refresh_list()
    messagebox.showinfo("Success", f"Contact '{name}' updated!")


# Refresh contact list
def refresh_list():
    listbox.delete(0, tk.END)
    for name in contacts:
        listbox.insert(tk.END, name)


# Toggle dark/light mode
def toggle_theme():
    global dark_mode
    dark_mode = not dark_mode
    bg_color = "#2e2e2e" if dark_mode else "white"
    fg_color = "white" if dark_mode else "black"
    root.config(bg=bg_color)
    listbox.config(bg=bg_color, fg=fg_color)
    for btn in buttons:
        btn.config(bg=bg_color, fg=fg_color)


# Main window
root = tk.Tk()
root.title("📞 Phone Book App")
root.geometry("400x500")

contacts = load_contacts()
dark_mode = False

# Listbox to show contacts
listbox = tk.Listbox(root, font=("Arial", 14))
listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

buttons = [
    tk.Button(button_frame, text="Add", width=10, command=add_contact),
    tk.Button(button_frame, text="View", width=10, command=view_contact),
    tk.Button(button_frame, text="Update", width=10, command=update_contact),
    tk.Button(button_frame, text="Delete", width=10, command=delete_contact),
    tk.Button(button_frame, text="Search", width=10, command=search_contact),
    tk.Button(button_frame, text="Refresh", width=10, command=refresh_list),
    tk.Button(button_frame, text="Theme", width=10, command=toggle_theme)
]

for i, btn in enumerate(buttons):
    btn.grid(row=i // 2, column=i % 2, padx=5, pady=5)

refresh_list()
root.mainloop()
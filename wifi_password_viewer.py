import subprocess
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# Global visibility toggle
show_passwords = False

def get_wifi_passwords():
    tree.delete(*tree.get_children())
    command = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8', errors="ignore")
    profiles = [i.split(":")[1][1:-1] for i in command.split('\n') if "All User Profile" in i]

    for profile in profiles:
        try:
            results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', profile, 'key=clear']).decode('utf-8', errors="ignore")
            password = [b.split(":")[1][1:-1] for b in results.split('\n') if "Key Content" in b]
            pwd = password[0] if password else ""
        except subprocess.CalledProcessError:
            pwd = "Unavailable"
        display_pwd = pwd if show_passwords else "***************" if pwd else ""
        tree.insert("", "end", values=(profile, display_pwd, pwd))

def toggle_passwords():
    global show_passwords
    show_passwords = not show_passwords
    get_wifi_passwords()
    toggle_btn.config(text="Hide Passwords" if show_passwords else "Show Passwords")

def copy_password():
    selected = tree.focus()
    if selected:
        values = tree.item(selected, "values")
        if len(values) > 2:
            real_password = values[2]
            if real_password:
                root.clipboard_clear()
                root.clipboard_append(real_password)
                messagebox.showinfo("Copied", f"Password copied to clipboard: {real_password}")
            else:
                messagebox.showwarning("Warning", "This profile has no password.")
        else:
            messagebox.showwarning("Warning", "Could not read selected data.")

def export_to_txt():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write("Wi-Fi Name\t\tPassword\n")
            for child in tree.get_children():
                values = tree.item(child, "values")
                file.write(f"{values[0]}\t\t{values[2]}\n")
        messagebox.showinfo("Exported", "Data successfully exported to .txt")

# GUI Start
root = tk.Tk()
root.title("Wi-Fi Password Viewer")
root.geometry("900x600")
root.configure(bg="#1B1D25")

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview",
                background="#1B1D25",
                foreground="#F0F1F4",
                fieldbackground="#1B1D25",
                rowheight=25,
                font=("Segoe UI", 10))
style.configure("Treeview.Heading",
                background="#F0F1F4",
                foreground="#000000",
                font=("Segoe UI", 10, "bold"))

# Title
label = tk.Label(root, text="Wi-Fi Profiles & Passwords", font=("Segoe UI", 14, "bold"), bg="#1B1D25", fg="#F0F1F4")
label.pack(pady=10)

# Table
columns = ("SSID", "Password", "RealPassword")
tree = ttk.Treeview(root, columns=columns, show="headings")
tree.heading("SSID", text="SSID")
tree.heading("Password", text="Password")
tree.column("RealPassword", width=0, stretch=False)
tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

# Buttons
btn_frame = tk.Frame(root, bg="#1B1D25")
btn_frame.pack(pady=10)

toggle_btn = tk.Button(btn_frame, text="Show Passwords", command=toggle_passwords, bg="#7B00FF", fg="#f0f1f4", font=("Segoe UI", 10))
toggle_btn.grid(row=0, column=0, padx=5)

copy_btn = tk.Button(btn_frame, text="Copy Password", command=copy_password, bg="#7B00FF", fg="#f0f1f4", font=("Segoe UI", 10))
copy_btn.grid(row=0, column=1, padx=5)

export_btn = tk.Button(btn_frame, text="Export to .txt", command=export_to_txt, bg="#7B00FF", fg="#f0f1f4", font=("Segoe UI", 10))
export_btn.grid(row=0, column=2, padx=5)

refresh_btn = tk.Button(btn_frame, text="Refresh", command=get_wifi_passwords, bg="#7B00FF", fg="#f0f1f4", font=("Segoe UI", 10))
refresh_btn.grid(row=0, column=3, padx=5)

# Load data
get_wifi_passwords()
root.mainloop()

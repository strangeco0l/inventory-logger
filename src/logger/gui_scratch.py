import tkinter as tk
from tkinter import ttk, messagebox
from dotenv import load_dotenv
import os
from supabase import create_client
from logger.models import fetch_user_sneakers
from logger.models import fetch_user_collectibles
from logger.models import fetch_user_media
from dataclasses import asdict

# Load environment variables
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Logger")

        self.user_id = None
        self.sneaker_data = []
        self.collectibles_data = []
        self.media_data = []

        self.create_login_ui()
        self.create_main_ui()

    def create_login_ui(self):
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(pady=10)

        tk.Label(self.login_frame, text="Email:").grid(row=0, column=0)
        self.email_entry = tk.Entry(self.login_frame)
        self.email_entry.grid(row=0, column=1)

        tk.Label(self.login_frame, text="Password:").grid(row=1, column=0)
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=1, column=1)

        self.login_button = tk.Button(self.login_frame, text="Login", command=self.login)
        self.login_button.grid(row=2, column=0, columnspan=2)

    def create_main_ui(self):
        self.main_frame = tk.Frame(self.root)
        self.tree = ttk.Treeview(self.main_frame, columns=("Type", "Item", "Profit"), show="headings")
        self.tree.heading("Type", text="Type")
        self.tree.heading("Item", text="Item")
        self.tree.heading("Profit", text="Profit")
        self.tree.pack()

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        try:
            response = supabase.auth.sign_in_with_password({"email": email, "password": password})
            self.user_id = response.user.id
            messagebox.showinfo("Login", "Login successful!")

            self.login_frame.pack_forget()
            self.main_frame.pack()
            self.fetch_user_inventory_data()

        except Exception as e:
            messagebox.showerror("Login Failed", str(e))

    def fetch_user_inventory_data(self):
        # Fetch all entries after login
        sneakers = fetch_user_sneakers(self.user_id, supabase)
        collectibles = fetch_user_collectibles(self.user_id, supabase)
        media = fetch_user_media(self.user_id, supabase)

        self.sneaker_data = [asdict(s) for s in sneakers]
        self.collectibles_data = [asdict(c) for c in collectibles]
        self.media_data = [asdict(m) for m in media]

        self.refresh_spreadsheet()

    def refresh_spreadsheet(self):
        # Clear the tree
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Add sneakers
        for sneaker in self.sneaker_data:
            self.tree.insert("", tk.END, values=("Sneaker", sneaker["model"], sneaker["profit"]))

        # Add collectibles
        for collectible in self.collectibles_data:
            self.tree.insert("", tk.END, values=("Collectible", collectible["item"], collectible["profit"]))

        # Add media
        for media in self.media_data:
            self.tree.insert("", tk.END, values=("Media", media["album"], media["profit"]))


if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()

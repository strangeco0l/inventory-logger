import tkinter as tk
from html import parser as csv
from tkinter import ttk, messagebox, filedialog
from ttkthemes import ThemedTk
from dataclasses import asdict
from logger.data_handling import save_sneaker_data, save_media_data, save_collectibles_data
from logger.sneaker_inventory_log import save_sneaker_to_supabase
from logger.collectibles_inventory_log import Collectibles
from logger.media_inventory_log import Media
from supabase_client import create_client, Client
# Your dataclasses (unchanged) here or import from your module
from dataclasses import dataclass, field
from dotenv import load_dotenv
import os
import inspect
from logger.models import Sneaker, Collectibles, Media

# print(inspect.getsource(Sneaker))


# Initialize Supabase client once in your app
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


# Assuming save functions add to these lists or you can adapt accordingly
class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.user_id = None
        self.root.title("Inventory Manager")
        self.root.geometry("1800x900")
        self.root.resizable(False, False)

        self.custom_font = ("Segoe UI", 10)

        # In-memory storage of entries
        self.sneaker_data = []
        self.media_data = []
        self.collectibles_data = []

        # Create notebook (tabs)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)

        # Create frames for each tab
        self.sneaker_frame = ttk.Frame(self.notebook, padding=15)
        self.media_frame = ttk.Frame(self.notebook, padding=15)
        self.collectibles_frame = ttk.Frame(self.notebook, padding=15)
        self.spreadsheet_frame = ttk.Frame(self.notebook, padding=15)

        self.notebook.add(self.sneaker_frame, text="Sneaker")
        self.notebook.add(self.media_frame, text="Media")
        self.notebook.add(self.collectibles_frame, text="Collectibles")
        self.notebook.add(self.spreadsheet_frame, text="Spreadsheet")

        # Build forms for each tab
        self.sneaker_fields = {}
        self.media_fields = {}
        self.collectibles_fields = {}

        self.build_sneaker_form()
        self.build_media_form()
        self.build_collectibles_form()

        # Setup spreadsheet tab
        self.build_spreadsheet_tab()

        # Add login tab
        self.login_frame = ttk.Frame(self.notebook, padding=15)
        self.notebook.add(self.login_frame, text="Login")

        self.build_login_form()

        # Disable all tabs except Login until user logs in
        for i in range(self.notebook.index("end") - 1):  # all but last tab (Login)
            self.notebook.tab(i, state='disabled')

        self.user = None  # store logged-in user

    def build_login_form(self):
        ttk.Label(self.login_frame, text="Email:").grid(row=0, column=0, sticky='w', pady=5)
        self.email_entry = ttk.Entry(self.login_frame, width=40)
        self.email_entry.grid(row=0, column=1, pady=5)

        ttk.Label(self.login_frame, text="Password:").grid(row=1, column=0, sticky='w', pady=5)
        self.password_entry = ttk.Entry(self.login_frame, width=40, show='*')
        self.password_entry.grid(row=1, column=1, pady=5)

        login_btn = ttk.Button(self.login_frame, text="Login", command=self.login)
        login_btn.grid(row=2, column=1, sticky='e', pady=10)

    def login(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        if not email or not password:
            messagebox.showerror("Login Error", "Email and password cannot be empty.")
            return

        try:
            response = supabase.auth.sign_in_with_password({"email": email, "password": password})
            if response.user:
                self.user = response.user
                messagebox.showinfo("Success", f"Logged in as {self.user.email}")
                self.user_id = self.user.id
                # Enable other tabs
                for i in range(self.notebook.index("end") - 1):
                    self.notebook.tab(i, state='normal')
                # Optionally switch to first tab after login
                self.notebook.select(0)
            else:
                messagebox.showerror("Login Failed", "Invalid email or password.")
        except Exception as e:
            messagebox.showerror("Login Failed", str(e))

    # ... [build_sneaker_form(), build_media_form(), build_collectibles_form(), _build_form() same as before] ...

    def build_sneaker_form(self):
        fields = [
            "Purchase Date", "Retailer", "Release Date", "Size",
            "Brand", "Model", "Colorway", "SKU",
            "Retail Price", "Resale Price", "Quantity"
        ]
        self._build_form(self.sneaker_frame, fields, self.sneaker_fields)

        submit_btn = ttk.Button(self.sneaker_frame, text="Submit Sneaker", command=self.submit_sneaker)
        submit_btn.grid(row=len(fields), column=1, pady=15, sticky='e')

    def build_media_form(self):
        fields = [
            "Purchase Date", "Retailer", "Media Type", "Speed",
            "Artist", "Album", "Variation", "Signed",
            "Edition", "Retail Price", "Resale Price", "Quantity"
        ]
        self._build_form(self.media_frame, fields, self.media_fields)

        submit_btn = ttk.Button(self.media_frame, text="Submit Media", command=self.submit_media)
        submit_btn.grid(row=len(fields), column=1, pady=15, sticky='e')

    def build_collectibles_form(self):
        fields = [
            "Purchase Date", "Retailer", "Brand", "Item",
            "Variation", "Retail Price", "Resale Price", "Quantity"
        ]
        self._build_form(self.collectibles_frame, fields, self.collectibles_fields)

        submit_btn = ttk.Button(self.collectibles_frame, text="Submit Collectible", command=self.submit_collectible)
        submit_btn.grid(row=len(fields), column=1, pady=15, sticky='e')

    def _build_form(self, parent, fields, fields_dict):
        for i, field in enumerate(fields):
            label = ttk.Label(parent, text=field + ": ", font=self.custom_font)
            label.grid(row=i, column=0, sticky='w', pady=5, padx=(0,10))

            entry = ttk.Entry(parent, font=self.custom_font)
            entry.grid(row=i, column=1, sticky='ew', pady=5)

            fields_dict[field.lower().replace(" ", "_")] = entry

        parent.columnconfigure(1, weight=1)

    def submit_sneaker(self):
        try:
            data = self._gather_data(self.sneaker_fields, {
                "purchase_date": str,
                "retailer": str,
                "release_date": str,
                "size": str,
                "brand": str,
                "model": str,
                "colorway": str,
                "sku": str,
                "retail_price": float,
                "resale_price": float,
                "quantity": int
            })

            item = Sneaker(user_id=self.user.id, **data)

            # Pass self.user.id (or self.user_id if stored) to save_sneaker_to_supabase
            save_sneaker_to_supabase(item)

            save_sneaker_data(item)  # your local save function if needed

            self.sneaker_data.append(asdict(item))  # Add to in-memory list
            messagebox.showinfo("Success", "Sneaker data saved successfully!")
            self._clear_fields(self.sneaker_fields)
            self.refresh_spreadsheet()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def submit_media(self):
        try:
            data = self._gather_data(self.media_fields, {
                "purchase_date": str,
                "retailer": str,
                "media_type": str,
                "speed": str,
                "artist": str,
                "album": str,
                "variation": str,
                "signed": str,
                "edition": str,
                "retail_price": float,
                "resale_price": float,
                "quantity": int
            })
            item = Media(**data)
            save_media_data(item)
            self.media_data.append(asdict(item))
            messagebox.showinfo("Success", "Media data saved successfully!")
            self._clear_fields(self.media_fields)
            self.refresh_spreadsheet()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def submit_collectible(self):
        try:
            data = self._gather_data(self.collectibles_fields, {
                "purchase_date": str,
                "retailer": str,
                "brand": str,
                "item": str,
                "variation": str,
                "retail_price": float,
                "resale_price": float,
                "quantity": int
            })
            item = Collectibles(**data)
            save_collectibles_data(item)
            self.collectibles_data.append(asdict(item))
            messagebox.showinfo("Success", "Collectible data saved successfully!")
            self._clear_fields(self.collectibles_fields)
            self.refresh_spreadsheet()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _gather_data(self, fields_dict, types_dict):
        data = {}
        for key, entry in fields_dict.items():
            val = entry.get().strip()
            if not val:
                raise ValueError(f"Field '{key.replace('_', ' ').title()}' cannot be empty.")
            convert_type = types_dict.get(key, str)
            if convert_type == int:
                val = int(val)
            elif convert_type == float:
                val = float(val)
            data[key] = val
        return data

    def _clear_fields(self, fields_dict):
        for entry in fields_dict.values():
            entry.delete(0, tk.END)

    # --- Spreadsheet Tab ---

    def build_spreadsheet_tab(self):
        # Frame for controls
        controls_frame = ttk.Frame(self.spreadsheet_frame)
        controls_frame.pack(fill='x', pady=5)

        refresh_btn = ttk.Button(controls_frame, text="Refresh Table", command=self.refresh_spreadsheet)
        refresh_btn.pack(side='left', padx=5)

        export_btn = ttk.Button(controls_frame, text="Export CSV", command=self.export_csv)
        export_btn.pack(side='left', padx=5)

        # Treeview for data display
        columns = (
            "type", "purchase_date", "retailer", "release_date_or_media_type", "size_or_speed",
            "brand_or_artist", "model_or_album", "colorway_or_variation", "sku_or_signed",
            "edition", "retail_price", "resale_price", "quantity", "profit_per", "profit"
        )

        self.tree = ttk.Treeview(self.spreadsheet_frame, columns=columns, show='headings', height=20)
        self.tree.pack(expand=True, fill='both')

        # Define headings and widths
        headings = {
            "type": "Type",
            "purchase_date": "Purchase Date",
            "retailer": "Retailer",
            "release_date_or_media_type": "Release Date / Media Type",
            "size_or_speed": "Size / Speed",
            "brand_or_artist": "Brand / Artist",
            "model_or_album": "Model / Album",
            "colorway_or_variation": "Colorway / Variation",
            "sku_or_signed": "SKU / Signed",
            "edition": "Edition",
            "retail_price": "Retail Price",
            "resale_price": "Resale Price",
            "quantity": "Quantity",
            "profit_per": "Profit Per",
            "profit": "Total Profit"
        }
        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=100, anchor='center')

    def refresh_spreadsheet(self):
        # Clear existing rows
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Insert sneaker data
        for item in self.sneaker_data:
            self.tree.insert('', 'end', values=(
                "Sneaker",
                item.get("purchase_date", ""),
                item.get("retailer", ""),
                item.get("release_date", ""),
                item.get("size", ""),
                item.get("brand", ""),
                item.get("model", ""),
                item.get("colorway", ""),
                item.get("sku", ""),
                "",
                item.get("retail_price", ""),
                item.get("resale_price", ""),
                item.get("quantity", ""),
                f"{item.get('profit_per', 0):.2f}",
                f"{item.get('profit', 0):.2f}"
            ))

        # Insert media data
        for item in self.media_data:
            self.tree.insert('', 'end', values=(
                "Media",
                item.get("purchase_date", ""),
                item.get("retailer", ""),
                item.get("media_type", ""),
                item.get("speed", ""),
                item.get("artist", ""),
                item.get("album", ""),
                item.get("variation", ""),
                item.get("signed", ""),
                item.get("edition", ""),
                item.get("retail_price", ""),
                item.get("resale_price", ""),
                item.get("quantity", ""),
                f"{item.get('profit_per', 0):.2f}",
                f"{item.get('profit', 0):.2f}"
            ))

        # Insert collectibles data
        for item in self.collectibles_data:
            self.tree.insert('', 'end', values=(
                "Collectible",
                item.get("purchase_date", ""),
                item.get("retailer", ""),
                "",
                "",
                item.get("brand", ""),
                item.get("item", ""),
                item.get("variation", ""),
                "",
                "",
                item.get("retail_price", ""),
                item.get("resale_price", ""),
                item.get("quantity", ""),
                f"{item.get('profit_per', 0):.2f}",
                f"{item.get('profit', 0):.2f}"
            ))

    def export_csv(self):
        # Ask for file save location
        file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                 filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if not file_path:
            return  # User cancelled

        try:
            with open(file_path, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                # Write header
                headers = [self.tree.heading(col)['text'] for col in self.tree['columns']]
                writer.writerow(headers)
                # Write rows
                for row_id in self.tree.get_children():
                    row = self.tree.item(row_id)['values']
                    writer.writerow(row)
            messagebox.showinfo("Export CSV", f"Data exported successfully to:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Export CSV Error", str(e))


if __name__ == "__main__":
    root = ThemedTk(theme="radiance")
    app = InventoryApp(root)
    root.mainloop()

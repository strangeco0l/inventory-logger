import tkinter as tk
from tkinter import messagebox
from .sneaker_inventory_log import Sneaker, save_sneaker_to_supabase
from .supabase_client import supabase
from .ebay_sold_scraper import get_average_sold_price


def get_existing_user_id(email: str) -> str:
    """Fetch the user_id of an existing user by email."""
    try:
        response = supabase.table("users").select("id").eq("email", email).execute()
        if response.data and len(response.data) > 0:
            user_id = response.data[0]["id"]
            print(f"[DEBUG] Found user {email} → {user_id}")
            return user_id
        else:
            messagebox.showerror("Error", f"No user found with email: {email}")
            return None
    except Exception as e:
        messagebox.showerror("Database Error", f"Could not check user: {e}")
        return None


class SneakerLoggerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sneaker Logger")
        self.user_id = None
        self.user_email = None

        # --- Login Frame ---
        self.login_frame = tk.Frame(root)
        tk.Label(self.login_frame, text="Email:").grid(row=0, column=0)
        self.email_entry = tk.Entry(self.login_frame)
        self.email_entry.grid(row=0, column=1)
        tk.Button(self.login_frame, text="Login", command=self.handle_login).grid(row=1, column=0, columnspan=2)
        self.login_frame.pack(pady=20)

        # --- Sneaker Entry Frame ---
        self.entry_frame = tk.Frame(root)
        row_idx = 0

        def add_field(label_text):
            nonlocal row_idx
            tk.Label(self.entry_frame, text=label_text).grid(row=row_idx, column=0)
            entry = tk.Entry(self.entry_frame)
            entry.grid(row=row_idx, column=1)
            row_idx += 1
            return entry

        self.brand_entry = add_field("Brand:")
        self.model_entry = add_field("Model:")
        self.colorway_entry = add_field("Colorway:")
        self.sku_entry = add_field("SKU:")
        self.size_entry = add_field("Size:")
        self.retailer_entry = add_field("Retailer:")
        self.purchase_entry = add_field("Purchase Date (YYYY-MM-DD):")
        self.release_entry = add_field("Release Date (YYYY-MM-DD):")
        self.retail_entry = add_field("Purchase Price:")
        self.resale_entry = add_field("Resale Price (optional):")
        self.quantity_entry = add_field("Quantity:")

        tk.Button(self.entry_frame, text="Save Sneaker", command=self.save_sneaker).grid(
            row=row_idx, column=0, columnspan=2
        )

        self.status_label = tk.Label(root, text="", fg="green")
        self.status_label.pack(pady=10)

    def handle_login(self):
        email = self.email_entry.get().strip()
        if not email:
            messagebox.showerror("Error", "Please enter an email.")
            return

        user_id = get_existing_user_id(email)
        if not user_id:
            messagebox.showerror("Error", f"No user found with email: {email}")
            return

        self.user_id = user_id
        self.user_email = email
        self.login_frame.pack_forget()
        self.root.title(f"Sneaker Logger - Logged in as {email}")
        self.entry_frame.pack(pady=20)
        self.status_label.config(text=f"Logged in as {email}")

    def save_sneaker(self):
        if not self.user_id:
            messagebox.showerror("Error", "No user is logged in.")
            return

        try:
            resale_val = self.resale_entry.get().strip()
            brand = self.brand_entry.get().strip()
            model = self.model_entry.get().strip()
            colorway = self.colorway_entry.get().strip()
            sku = self.sku_entry.get().strip()

            # If resale left blank, use eBay scraper
            resale_price = None
            if resale_val:
                resale_price = float(resale_val)
            else:
                query = f"{brand} {model} {colorway} {sku}".strip()
                self.status_label.config(text=f"Fetching resale data from eBay...")
                self.root.update()
                try:
                    resale_price = get_average_sold_price(query)
                    if resale_price:
                        messagebox.showinfo(
                            "Resale Price Found",
                            f"Estimated resale price from eBay: ${resale_price:.2f}",
                        )
                        self.resale_entry.insert(0, str(round(resale_price, 2)))
                    else:
                        self.status_label.config(text="No resale data found on eBay.")
                except Exception as e:
                    print(f"[ERROR] eBay scrape failed: {e}")
                    self.status_label.config(text="eBay data unavailable.")

            sneaker = Sneaker(
                user_id=self.user_id,
                purchase_date=self.purchase_entry.get().strip() or None,
                release_date=self.release_entry.get().strip() or None,
                retailer=self.retailer_entry.get().strip(),
                size=self.size_entry.get().strip(),
                brand=brand,
                model=model,
                colorway=colorway,
                sku=sku,
                retail_price=float(self.retail_entry.get()),
                resale_price=resale_price,
                quantity=int(self.quantity_entry.get()),
            )

            save_sneaker_to_supabase(sneaker)
            self.status_label.config(text=f"Sneaker saved for {self.user_email}!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save sneaker: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = SneakerLoggerApp(root)
    root.mainloop()

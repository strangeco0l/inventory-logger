import customtkinter as ctk
from tkinter import messagebox
from src.logger.sneaker_inventory_log import Sneaker, save_sneaker_to_supabase
from src.logger.supabase_client import supabase
from src.logger.ebay_sold_scraper import get_average_sold_price

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

def get_existing_user_id(email: str) -> str:
    try:
        response = supabase.table("users").select("id").eq("email", email).execute()
        if response.data and len(response.data) > 0:
            return response.data[0]["id"]
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
        self.root.geometry("600x700")  # starting size
        self.user_id = None
        self.user_email = None

        # --- Layout Config for Resizing ---
        self.root.rowconfigure(1, weight=1)  # make entry frame row expandable
        self.root.columnconfigure(0, weight=1)

        # --- Login Frame ---
        self.login_frame = ctk.CTkFrame(root, corner_radius=15, fg_color="#F0F0F0")
        self.login_frame.grid(row=0, column=0, padx=30, pady=20, sticky="ew")

        ctk.CTkLabel(self.login_frame, text="Login", font=("Segoe UI", 18, "bold")).pack(pady=(10,20))
        self.email_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Enter your email")
        self.email_entry.pack(pady=10, padx=20, fill="x")
        self.login_button = ctk.CTkButton(self.login_frame, text="Login", command=self.handle_login)
        self.login_button.pack(pady=(10,20), padx=20, fill="x")

        # --- Status Label ---
        self.status_label = ctk.CTkLabel(root, text="", font=("Segoe UI", 12))
        self.status_label.grid(row=2, column=0, pady=(0,10), sticky="ew", padx=30)

        # --- Scrollable Sneaker Entry Frame ---
        self.canvas_frame = ctk.CTkFrame(root)
        self.canvas_frame.grid(row=1, column=0, sticky="nsew", padx=30, pady=(0,10))
        self.canvas_frame.rowconfigure(0, weight=1)
        self.canvas_frame.columnconfigure(0, weight=1)

        self.scrollable_frame = ctk.CTkScrollableFrame(self.canvas_frame, corner_radius=15)
        self.scrollable_frame.grid(row=0, column=0, sticky="nsew")

        self.entry_widgets = {}
        field_names = [
            "Brand", "Model", "Colorway", "SKU", "Size", "Retailer",
            "Purchase Date (YYYY-MM-DD)", "Release Date (YYYY-MM-DD)",
            "Purchase Price", "Resale Price (optional)", "Quantity"
        ]

        for field in field_names:
            label = ctk.CTkLabel(self.scrollable_frame, text=field)
            label.pack(pady=(5,0), anchor="w", padx=20)
            entry = ctk.CTkEntry(self.scrollable_frame)
            entry.pack(pady=(0,5), padx=20, fill="x")
            self.entry_widgets[field] = entry

        self.save_button = ctk.CTkButton(self.scrollable_frame, text="Save Sneaker", command=self.save_sneaker)
        self.save_button.pack(pady=15, padx=20, fill="x")

    def handle_login(self):
        email = self.email_entry.get().strip()
        if not email:
            messagebox.showerror("Error", "Please enter an email.")
            return

        user_id = get_existing_user_id(email)
        if not user_id:
            return

        self.user_id = user_id
        self.user_email = email
        self.login_frame.grid_forget()  # hide login after login
        self.scrollable_frame.master.grid(sticky="nsew")  # show scrollable frame
        self.status_label.configure(text=f"Logged in as {email}", text_color="blue")
        self.root.title(f"Sneaker Logger - Logged in as {email}")

    def save_sneaker(self):
        if not self.user_id:
            messagebox.showerror("Error", "No user is logged in.")
            return

        try:
            brand = self.entry_widgets["Brand"].get().strip()
            model = self.entry_widgets["Model"].get().strip()
            colorway = self.entry_widgets["Colorway"].get().strip()
            sku = self.entry_widgets["SKU"].get().strip()
            resale_val = self.entry_widgets["Resale Price (optional)"].get().strip()

            resale_price = None
            if resale_val:
                resale_price = float(resale_val)
            else:
                query = f"{brand} {model} {colorway} {sku}".strip()
                self.status_label.configure(text="Fetching resale data from eBay...", text_color="orange")
                self.root.update()
                try:
                    resale_price = get_average_sold_price(query)
                    if resale_price:
                        messagebox.showinfo("Resale Price Found", f"Estimated resale price: ${resale_price:.2f}")
                        self.entry_widgets["Resale Price (optional)"].insert(0, str(round(resale_price,2)))
                    else:
                        self.status_label.configure(text="No resale data found on eBay.", text_color="red")
                except Exception as e:
                    self.status_label.configure(text="eBay data unavailable.", text_color="red")
                    print(f"[ERROR] eBay scrape failed: {e}")

            sneaker = Sneaker(
                user_id=self.user_id,
                purchase_date=self.entry_widgets["Purchase Date (YYYY-MM-DD)"].get().strip() or None,
                release_date=self.entry_widgets["Release Date (YYYY-MM-DD)"].get().strip() or None,
                retailer=self.entry_widgets["Retailer"].get().strip(),
                size=self.entry_widgets["Size"].get().strip(),
                brand=brand,
                model=model,
                colorway=colorway,
                sku=sku,
                retail_price=float(self.entry_widgets["Purchase Price"].get()),
                resale_price=resale_price,
                quantity=int(self.entry_widgets["Quantity"].get()),
            )

            save_sneaker_to_supabase(sneaker)
            self.status_label.configure(text=f"Sneaker saved for {self.user_email}!", text_color="green")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save sneaker: {e}")

if __name__ == "__main__":
    root = ctk.CTk()
    app = SneakerLoggerApp(root)
    root.mainloop()

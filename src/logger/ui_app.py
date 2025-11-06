import customtkinter as ctk
from customtkinter import CTkImage
from tkinter import filedialog, messagebox
from tkcalendar import Calendar
from PIL import Image
from pathlib import Path
import shutil
import threading

from src.logger.sneaker_inventory_log import Sneaker, save_sneaker_to_supabase, get_all_sneakers
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
        self.root.geometry("1000x700")
        self.user_id = None
        self.user_email = None
        self.inventory_items = []

        self.tab_control = ctk.CTkTabview(root)
        self.tab_control.pack(expand=1, fill="both")
        self.tab_control.add("Add Sneaker")
        self.tab_control.add("View Inventory")

        self.create_add_tab()
        self.create_inventory_tab()

    # ------------------- ADD SNEAKER TAB -------------------
    def create_add_tab(self):
        self.add_tab = self.tab_control.tab("Add Sneaker")
        self.add_tab.rowconfigure(1, weight=1)
        self.add_tab.columnconfigure(0, weight=1)

        # Login Frame
        self.login_frame = ctk.CTkFrame(self.add_tab, corner_radius=15, fg_color="#F0F0F0")
        self.login_frame.grid(row=0, column=0, padx=30, pady=20, sticky="ew")

        ctk.CTkLabel(self.login_frame, text="Login", font=("Segoe UI", 18, "bold")).pack(pady=(10, 20))
        self.email_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Enter your email")
        self.email_entry.pack(pady=10, padx=20, fill="x")
        self.login_button = ctk.CTkButton(self.login_frame, text="Login", command=self.handle_login)
        self.login_button.pack(pady=(10, 20), padx=20, fill="x")

        self.status_label = ctk.CTkLabel(self.add_tab, text="", font=("Segoe UI", 12))
        self.status_label.grid(row=2, column=0, pady=(0, 10), sticky="ew", padx=30)

        self.canvas_frame = ctk.CTkFrame(self.add_tab)
        self.canvas_frame.grid(row=1, column=0, sticky="nsew", padx=30, pady=(0, 10))
        self.canvas_frame.rowconfigure(0, weight=1)
        self.canvas_frame.columnconfigure(0, weight=1)

        self.scrollable_frame = ctk.CTkScrollableFrame(self.canvas_frame, corner_radius=15)
        self.scrollable_frame.grid(row=0, column=0, sticky="nsew")

        self.entry_widgets = {}
        field_names = [
            "Brand", "Model", "Colorway", "SKU", "Size", "Retailer",
            "Purchase Date", "Release Date",
            "Purchase Price", "Resale Price (optional)", "Quantity"
        ]

        for field in field_names:
            ctk.CTkLabel(self.scrollable_frame, text=field).pack(pady=(5, 0), anchor="w", padx=20)
            if field in ("Purchase Date", "Release Date"):
                entry = ctk.CTkEntry(self.scrollable_frame)
                entry.pack(pady=(0, 5), padx=20, fill="x")
                entry.bind("<1>", lambda e, ent=entry: self.open_calendar(ent))
            else:
                entry = ctk.CTkEntry(self.scrollable_frame)
                entry.pack(pady=(0, 5), padx=20, fill="x")
            self.entry_widgets[field] = entry

        self.upload_button = ctk.CTkButton(self.scrollable_frame, text="Upload Image", command=self.upload_image)
        self.upload_button.pack(pady=(5,5), padx=20, fill="x")

        self.save_button = ctk.CTkButton(self.scrollable_frame, text="Save Sneaker", command=self.save_sneaker)
        self.save_button.pack(pady=15, padx=20, fill="x")

        self.image_path = None

    def open_calendar(self, entry_widget):
        # Pop-up calendar
        top = ctk.CTkToplevel(self.root)
        top.title("Select Date")
        top.geometry("350x300")

        cal = Calendar(top, selectmode='day')
        cal.pack(expand=True, fill='both', padx=10, pady=10)

        def pick_date():
            entry_widget.delete(0, "end")
            entry_widget.insert(0, cal.get_date())
            top.destroy()

        btn = ctk.CTkButton(top, text="Select", command=pick_date)
        btn.pack(pady=10)

    def upload_image(self):
        filetypes = [("Image Files", "*.png *.jpg *.jpeg")]
        file_path = filedialog.askopenfilename(title="Select Sneaker Image", filetypes=filetypes)
        if file_path:
            self.image_path = file_path
            messagebox.showinfo("Image Uploaded", f"Selected: {Path(file_path).name}")

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
        self.login_frame.grid_forget()
        self.status_label.configure(text=f"Logged in as {email}", text_color="blue")
        self.root.title(f"Sneaker Logger - Logged in as {email}")
        self.load_inventory()

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

            resale_price = float(resale_val) if resale_val else None
            if resale_price is None:
                query = f"{brand} {model} {colorway} {sku}".strip()
                self.status_label.configure(text="Fetching resale data from eBay...", text_color="orange")
                self.root.update()
                try:
                    resale_price = get_average_sold_price(query)
                    if resale_price:
                        self.entry_widgets["Resale Price (optional)"].insert(0, str(round(resale_price, 2)))
                except Exception as e:
                    print(f"[ERROR] eBay scrape failed: {e}")

            sneaker = Sneaker(
                user_id=self.user_id,
                purchase_date=self.entry_widgets["Purchase Date"].get().strip() or None,
                release_date=self.entry_widgets["Release Date"].get().strip() or None,
                retailer=self.entry_widgets["Retailer"].get().strip(),
                size=self.entry_widgets["Size"].get().strip(),
                brand=brand,
                model=model,
                colorway=colorway,
                sku=sku,
                retail_price=float(self.entry_widgets["Purchase Price"].get()),
                resale_price=resale_price,
                quantity=int(self.entry_widgets["Quantity"].get()),
                image_path=self.image_path
            )
            save_sneaker_to_supabase(sneaker)
            self.status_label.configure(text=f"Sneaker saved for {self.user_email}!", text_color="green")
            self.load_inventory()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save sneaker: {e}")

    # ------------------- INVENTORY TAB -------------------
    def create_inventory_tab(self):
        self.view_tab = self.tab_control.tab("View Inventory")
        self.view_tab.rowconfigure(0, weight=1)
        self.view_tab.columnconfigure(0, weight=1)

        self.canvas = ctk.CTkScrollableFrame(self.view_tab, corner_radius=15)
        self.canvas.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        self.refresh_button = ctk.CTkButton(
            self.view_tab,
            text="Refresh Inventory / Fetch Images",
            command=self.load_inventory
        )
        self.refresh_button.grid(row=1, column=0, pady=(0, 10), padx=20, sticky="ew")

    # ------------------- LOAD INVENTORY -------------------
    def load_inventory(self):
        if not self.user_id:
            return
        try:
            rows = get_all_sneakers(user_id=self.user_id)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch inventory: {e}")
            return

        # Clear existing
        for widget in self.canvas.winfo_children():
            widget.destroy()
        self.inventory_items = []

        for row in rows:
            frame = ctk.CTkFrame(self.canvas, corner_radius=10, fg_color="#E0E0E0", height=120)
            frame.pack(fill="x", pady=5, padx=10)

            img_label = ctk.CTkLabel(frame, text="[Loading...]", width=100, height=100)
            img_label.pack(side="left", padx=10, pady=10)

            title = f"{row.get('brand','')} {row.get('model','')} {row.get('colorway','')}"
            ctk.CTkLabel(frame, text=title, font=("Segoe UI", 12, "bold")).pack(anchor="w")
            price_info = f"Retail: ${row.get('retail_price',0)} | Resale: ${row.get('resale_price',0)} | Profit: ${row.get('profit',0)}"
            ctk.CTkLabel(frame, text=price_info, font=("Segoe UI", 10)).pack(anchor="w")

            edit_btn = ctk.CTkButton(frame, text="Edit", command=lambda r=row: self.open_edit_popup(r))
            edit_btn.pack(side="right", padx=10)

            self.inventory_items.append({"row": row, "img_label": img_label})
        threading.Thread(target=self._fetch_images_background, daemon=True).start()

    def _fetch_images_background(self):
        for item in self.inventory_items:
            row = item["row"]
            img_label = item["img_label"]
            img_path = row.get("image_path") or row.get("thumb_path")
            if img_path and Path(img_path).exists():
                try:
                    img = Image.open(img_path)
                    img.thumbnail((100, 100))
                    ctk_img = CTkImage(light_image=img, dark_image=img, size=(100, 100))
                    self.root.after(0, lambda lbl=img_label, img=ctk_img: lbl.configure(image=img, text="") or setattr(lbl, "image", img))
                except Exception:
                    self.root.after(0, lambda lbl=img_label: lbl.configure(text="[Image Error]"))
            else:
                self.root.after(0, lambda lbl=img_label: lbl.configure(text="[No Image]"))

    # ------------------- EDIT POPUP -------------------
    def open_edit_popup(self, row):
        popup = ctk.CTkToplevel(self.root)
        popup.title(f"Edit {row.get('brand')} {row.get('model')}")
        popup.geometry("480x650")  # Bigger for calendar
        popup.minsize(400, 500)

        container = ctk.CTkFrame(popup)
        container.pack(fill="both", expand=True, padx=8, pady=8)

        scroll = ctk.CTkScrollableFrame(container, corner_radius=8)
        scroll.pack(fill="both", expand=True)

        fields = [
            ("Brand", "brand"), ("Model", "model"), ("Colorway", "colorway"),
            ("SKU", "sku"), ("Size", "size"), ("Retailer", "retailer"),
            ("Purchase Date", "purchase_date"), ("Release Date", "release_date"),
            ("Purchase Price", "purchase_price"), ("Resale Price", "resale_price"),
            ("Quantity", "quantity"),
        ]

        entries = {}
        for label_text, key in fields:
            ctk.CTkLabel(scroll, text=label_text).pack(pady=(8,2), anchor="w", padx=12)
            entry = ctk.CTkEntry(scroll)
            entry.pack(pady=(0,4), padx=12, fill="x")
            val = row.get(key, "") or ""
            entry.insert(0, str(val))
            if key in ("purchase_date", "release_date"):
                entry.bind("<1>", lambda e, ent=entry: self.open_calendar(ent))
            entries[key] = entry

        # Image preview
        preview_frame = ctk.CTkFrame(scroll, corner_radius=8)
        preview_frame.pack(fill="x", pady=10, padx=12)
        image_preview = ctk.CTkLabel(preview_frame, text="[No Image]", width=180, height=180)
        image_preview.pack(side="left", padx=(8,12), pady=8)
        current_img_path = row.get("image_path") or row.get("thumb_path")
        img_path_ref = {"path": current_img_path}
        if current_img_path and Path(current_img_path).exists():
            img = Image.open(current_img_path)
            img.thumbnail((180,180))
            photo = CTkImage(light_image=img, dark_image=img, size=(180,180))
            image_preview.configure(image=photo, text="")
            image_preview.image = photo

        def upload_edit_image():
            path = filedialog.askopenfilename(title="Select Sneaker Image", filetypes=[("Image Files","*.png *.jpg *.jpeg")])
            if path:
                img_path_ref["path"] = path
                img = Image.open(path)
                img.thumbnail((180,180))
                photo = CTkImage(light_image=img, dark_image=img, size=(180,180))
                image_preview.configure(image=photo, text="")
                image_preview.image = photo

        upload_btn = ctk.CTkButton(preview_frame, text="Upload/Replace Image", command=upload_edit_image)
        upload_btn.pack(side="left", padx=(6,12), pady=8)

        bottom_frame = ctk.CTkFrame(container)
        bottom_frame.pack(fill="x", side="bottom", padx=8, pady=(6,8))

        def save_changes():
            try:
                update_data = {}
                for _, key in fields:
                    val = entries[key].get().strip()
                    if key in ("purchase_price", "resale_price"):
                        update_data[key] = float(val) if val else None
                    elif key == "quantity":
                        update_data[key] = int(val) if val else 1
                    else:
                        update_data[key] = val or None

                new_img = img_path_ref.get("path")
                if new_img and Path(new_img).exists() and (row.get("image_path") is None or Path(new_img).resolve()!=Path(row.get("image_path")).resolve()):
                    images_dir = Path("data/images")
                    images_dir.mkdir(parents=True, exist_ok=True)
                    filename = f"{update_data.get('brand','brand')}_{update_data.get('model','model')}_{update_data.get('colorway','color')}.jpg".replace(" ","_")
                    dest_path = images_dir / filename
                    shutil.copy(new_img, dest_path)
                    update_data["image_path"] = str(dest_path)
                    update_data["thumb_path"] = str(dest_path)
                else:
                    update_data["image_path"] = row.get("image_path")
                    update_data["thumb_path"] = row.get("thumb_path")

                supabase.table("sneakers").update(update_data).eq("id", row.get("id")).execute()
                messagebox.showinfo("Saved", "Sneaker updated successfully!")
                popup.destroy()
                self.load_inventory()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update sneaker: {e}")

        save_btn = ctk.CTkButton(bottom_frame, text="Save Changes", command=save_changes)
        save_btn.pack(side="right", padx=(6,12))
        cancel_btn = ctk.CTkButton(bottom_frame, text="Cancel", command=popup.destroy)
        cancel_btn.pack(side="right", padx=(6,0))


if __name__ == "__main__":
    root = ctk.CTk()
    app = SneakerLoggerApp(root)
    root.mainloop()

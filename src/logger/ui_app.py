import customtkinter as ctk
import shutil
from customtkinter import CTkImage
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from pathlib import Path
import threading
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
        self.root.geometry("950x700")
        self.user_id = None
        self.user_email = None
        self.inventory_items = []

        # --- Tab Control ---
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

        # Status Label
        self.status_label = ctk.CTkLabel(self.add_tab, text="", font=("Segoe UI", 12))
        self.status_label.grid(row=2, column=0, pady=(0, 10), sticky="ew", padx=30)

        # Scrollable Entry Frame
        self.canvas_frame = ctk.CTkFrame(self.add_tab)
        self.canvas_frame.grid(row=1, column=0, sticky="nsew", padx=30, pady=(0, 10))
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
            label.pack(pady=(5, 0), anchor="w", padx=20)
            entry = ctk.CTkEntry(self.scrollable_frame)
            entry.pack(pady=(0, 5), padx=20, fill="x")
            self.entry_widgets[field] = entry

        self.upload_button = ctk.CTkButton(self.scrollable_frame, text="Upload Image", command=self.upload_image)
        self.upload_button.pack(pady=(5,5), padx=20, fill="x")

        self.save_button = ctk.CTkButton(self.scrollable_frame, text="Save Sneaker", command=self.save_sneaker)
        self.save_button.pack(pady=15, padx=20, fill="x")

        self.image_path = None

    def upload_image(self):
        filetypes = [("Image Files", "*.png *.jpg *.jpeg")]
        file_path = filedialog.askopenfilename(title="Select Sneaker Image", filetypes=filetypes)
        if file_path:
            images_dir = Path("data/images")
            images_dir.mkdir(parents=True, exist_ok=True)
            filename = Path(file_path).name.replace(" ", "_")
            dest_path = images_dir / filename
            shutil.copy(file_path, dest_path)
            self.image_path = str(dest_path)

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
                        self.entry_widgets["Resale Price (optional)"].insert(0, str(round(resale_price, 2)))
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
                image_path=self.image_path
            )

            save_sneaker_to_supabase(sneaker)
            self.status_label.configure(text=f"Sneaker saved for {self.user_email}!", text_color="green")
            self.load_inventory()
            self.root.update_idletasks()


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
            data = supabase.table("sneakers").select("*").eq("user_id", self.user_id).execute()
            rows = data.data
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch inventory: {e}")
            return

        # Clear existing items
        for widget in self.canvas.winfo_children():
            widget.destroy()

        self.inventory_items = []

        for row in rows:
            frame = ctk.CTkFrame(self.canvas, corner_radius=10, fg_color="#E0E0E0", height=120)
            frame.pack(fill="x", pady=5, padx=10)

            img_label = ctk.CTkLabel(frame, text="[Loading...]", width=100, height=100, anchor="center")
            img_label.pack(side="left", padx=10, pady=10)

            title = f"{row.get('brand','')} {row.get('model','')} {row.get('colorway','')}"
            ctk.CTkLabel(frame, text=title, font=("Segoe UI", 12, "bold")).pack(anchor="w")
            price_info = f"Retail: ${row.get('retail_price',0)} | Resale: ${row.get('resale_price',0)} | Profit: ${row.get('profit',0)}"
            ctk.CTkLabel(frame, text=price_info, font=("Segoe UI", 10)).pack(anchor="w")

            edit_btn = ctk.CTkButton(frame, text="Edit", command=lambda r=row: self.open_edit_popup(r))
            edit_btn.pack(side="right", padx=10)

            self.inventory_items.append({
                "row": row,
                "frame": frame,
                "img_label": img_label
            })

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
                    self.root.after(0,
                                    lambda lbl=img_label, img=ctk_img: lbl.configure(image=img, text="") or setattr(lbl,
                                                                                                                    "image",
                                                                                                                    img))
                except Exception as e:
                    print(f"Error loading image: {e}")
                    self.root.after(0, lambda lbl=img_label: lbl.configure(text="[Image Error]"))
            else:
                self.root.after(0, lambda lbl=img_label: lbl.configure(text="[No Image]"))

    # ------------------- EDIT POPUP -------------------
    def open_edit_popup(self, row):
        popup = ctk.CTkToplevel(self.root)
        popup.title(f"Edit {row.get('brand')} {row.get('model')}")
        popup.geometry("420x560")
        popup.minsize(360, 360)

        # Main container
        container = ctk.CTkFrame(popup)
        container.pack(fill="both", expand=True, padx=8, pady=8)

        # Scrollable content
        scroll = ctk.CTkScrollableFrame(container, corner_radius=8)
        scroll.pack(fill="both", expand=True, side="top")

        # Fields: (label, db_key)
        fields = [
            ("Brand", "brand"),
            ("Model", "model"),
            ("Colorway", "colorway"),
            ("SKU", "sku"),
            ("Size", "size"),
            ("Retailer", "retailer"),
            ("Purchase Date (YYYY-MM-DD)", "purchase_date"),
            ("Release Date (YYYY-MM-DD)", "release_date"),
            ("Purchase Price", "purchase_price"),
            ("Resale Price", "resale_price"),
            ("Quantity", "quantity"),
        ]

        entries = {}
        for label_text, key in fields:
            ctk.CTkLabel(scroll, text=label_text).pack(pady=(8, 2), anchor="w", padx=12)
            entry = ctk.CTkEntry(scroll)
            entry.pack(pady=(0, 4), padx=12, fill="x")
            val = row.get(key, "") or ""
            entry.delete(0, "end")
            entry.insert(0, str(val))
            entries[key] = entry

        # Image preview + upload area
        preview_frame = ctk.CTkFrame(scroll, corner_radius=8)
        preview_frame.pack(fill="x", pady=10, padx=12)

        image_preview = ctk.CTkLabel(preview_frame, text="[No Image]", width=180, height=180)
        image_preview.pack(side="left", padx=(8, 12), pady=8)

        # Load existing image if available
        current_img_path = row.get("image_path") or row.get("thumb_path") or None
        if current_img_path and Path(current_img_path).exists():
            try:
                img = Image.open(current_img_path)
                img.thumbnail((180, 180))
                photo = CTkImage(light_image=img, dark_image=img, size=(180, 180))
                image_preview.configure(image=photo, text="")
                image_preview.image = photo
            except Exception:
                pass

        # Use a mutable ref to hold selected path (avoids nonlocal)
        img_path_ref = {"path": current_img_path}

        def upload_edit_image():
            path = filedialog.askopenfilename(
                title="Select Sneaker Image",
                filetypes=[("Image Files", "*.png *.jpg *.jpeg")]
            )
            if path:
                img_path_ref["path"] = path
                try:
                    img = Image.open(path)
                    img.thumbnail((180, 180))
                    photo = CTkImage(light_image=img, dark_image=img, size=(180, 180))
                    image_preview.configure(image=photo, text="")
                    image_preview.image = photo
                except Exception as e:
                    messagebox.showerror("Image Error", f"Failed to open image: {e}")

        upload_btn = ctk.CTkButton(preview_frame, text="Upload/Replace Image", command=upload_edit_image)
        upload_btn.pack(side="left", padx=(6, 12), pady=8)

        # Bottom bar (Save / Cancel) outside the scroll frame so it stays visible
        bottom_frame = ctk.CTkFrame(container)
        bottom_frame.pack(fill="x", side="bottom", padx=8, pady=(6, 8))

        def save_changes():
            try:
                update_data = {}
                for _, key in fields:
                    raw = entries[key].get().strip()
                    if key in ("purchase_price", "resale_price"):
                        update_data[key] = float(raw) if raw else None
                    elif key == "quantity":
                        update_data[key] = int(raw) if raw else 1
                    else:
                        update_data[key] = raw or None

                # handle image: if a new local file was selected, copy it into data/images/
                new_img = img_path_ref.get("path")
                if new_img and Path(new_img).exists() and (
                        row.get("image_path") is None or Path(new_img).resolve() != Path(
                        row.get("image_path")).resolve()):
                    images_dir = Path("data/images")
                    images_dir.mkdir(parents=True, exist_ok=True)
                    filename = f"{(update_data.get('brand') or row.get('brand') or 'brand')}_{(update_data.get('model') or row.get('model') or 'model')}_{(update_data.get('colorway') or row.get('colorway') or 'color')}.jpg".replace(
                        " ", "_")
                    dest_path = images_dir / filename
                    shutil.copy(new_img, dest_path)
                    update_data["image_path"] = str(dest_path)
                    update_data["thumb_path"] = str(dest_path)
                else:
                    # keep existing paths if they exist
                    update_data["image_path"] = row.get("image_path")
                    update_data["thumb_path"] = row.get("thumb_path")

                # Persist to Supabase
                supabase.table("sneakers").update(update_data).eq("id", row.get("id")).execute()

                messagebox.showinfo("Saved", "Sneaker updated successfully!")
                popup.destroy()
                self.load_inventory()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update sneaker: {e}")

        save_btn = ctk.CTkButton(bottom_frame, text="Save Changes", command=save_changes)
        save_btn.pack(side="right", padx=(6, 12))

        cancel_btn = ctk.CTkButton(bottom_frame, text="Cancel", command=popup.destroy)
        cancel_btn.pack(side="right", padx=(6, 0))


if __name__ == "__main__":
    root = ctk.CTk()
    app = SneakerLoggerApp(root)
    root.mainloop()

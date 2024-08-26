import tkinter as tk
from tkinter import ttk
from data_handling_example import save_sneaker_data, save_media_data

def create_main_window():
    def on_submit():
        if var.get() == 'Sneakers':
            data = collect_sneaker_data()
            save_sneaker_data(data)
        elif var.get() == 'Media':
            data = collect_media_data()
            save_media_data(data)
        else:
            label_profit_message.config(text="Invalid Input")

    def collect_sneaker_data():
        data = {
            "Purchase Date": entry_purchase_date.get(),
            "Retailer": entry_retailer.get().title(),
            "Size": entry_size.get(),
            "Brand": entry_brand.get().title(),
            "Model": entry_model.get().title(),
            "Colorway": entry_color_way.get().title(),
            "SKU": entry_sku.get(),
            "Retail Price": entry_retail.get(),
            "Resale Price": entry_resale.get(),
            "Profit": int(entry_resale.get()) - int(entry_retail.get())
        }
        return data

    def collect_media_data():
        media = entry_media.get()
        speed = entry_speed.get() if media.lower() == 'vinyl' else None
        data = {
            "Purchase Date": entry_purchase_date.get(),
            "Retailer": entry_retailer.get().title(),
            "Media": media,
            "Speed": speed,
            "Artist": entry_artist.get().title(),
            "Album": entry_album.get(),
            "Variation": entry_variation.get(),
            "Signed": entry_signed.get(),
            "Edition": entry_edition.get(),
            "Retail": entry_retail.get(),
            "Resale": entry_resale.get(),
            "Profit": int(entry_resale.get()) - int(entry_retail.get())
        }
        return data

    root = tk.Tk()
    root.title("Inventory Log")

    # Define labels and entries for sneaker inventory
    tk.Label(root, text="Purchase Date:").grid(row=0, column=0, padx=10, pady=5)
    entry_purchase_date = tk.Entry(root)
    entry_purchase_date.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(root, text="Retailer:").grid(row=1, column=0, padx=10, pady=5)
    entry_retailer = tk.Entry(root)
    entry_retailer.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(root, text="Size:").grid(row=2, column=0, padx=10, pady=5)
    entry_size = tk.Entry(root)
    entry_size.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(root, text="Brand:").grid(row=3, column=0, padx=10, pady=5)
    entry_brand = tk.Entry(root)
    entry_brand.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(root, text="Model:").grid(row=4, column=0, padx=10, pady=5)
    entry_model = tk.Entry(root)
    entry_model.grid(row=4, column=1, padx=10, pady=5)

    tk.Label(root, text="Colorway:").grid(row=5, column=0, padx=10, pady=5)
    entry_color_way = tk.Entry(root)
    entry_color_way.grid(row=5, column=1, padx=10, pady=5)

    tk.Label(root, text="SKU:").grid(row=6, column=0, padx=10, pady=5)
    entry_sku = tk.Entry(root)
    entry_sku.grid(row=6, column=1, padx=10, pady=5)

    tk.Label(root, text="Retail Price:").grid(row=7, column=0, padx=10, pady=5)
    entry_retail = tk.Entry(root)
    entry_retail.grid(row=7, column=1, padx=10, pady=5)

    tk.Label(root, text="Resale Price:").grid(row=8, column=0, padx=10, pady=5)
    entry_resale = tk.Entry(root)
    entry_resale.grid(row=8, column=1, padx=10, pady=5)

    # Define labels and entries for media inventory
    tk.Label(root, text="Media Type (Vinyl or CD):").grid(row=9, column=0, padx=10, pady=5)
    entry_media = tk.Entry(root)
    entry_media.grid(row=9, column=1, padx=10, pady=5)

    tk.Label(root, text="Speed (if Vinyl):").grid(row=10, column=0, padx=10, pady=5)
    entry_speed = tk.Entry(root)
    entry_speed.grid(row=10, column=1, padx=10, pady=5)

    tk.Label(root, text="Artist:").grid(row=11, column=0, padx=10, pady=5)
    entry_artist = tk.Entry(root)
    entry_artist.grid(row=11, column=1, padx=10, pady=5)

    tk.Label(root, text="Album:").grid(row=12, column=0, padx=10, pady=5)
    entry_album = tk.Entry(root)
    entry_album.grid(row=12, column=1, padx=10, pady=5)

    tk.Label(root, text="Variation:").grid(row=13, column=0, padx=10, pady=5)
    entry_variation = tk.Entry(root)
    entry_variation.grid(row=13, column=1, padx=10, pady=5)

    tk.Label(root, text="Signed?:").grid(row=14, column=0, padx=10, pady=5)
    entry_signed = tk.Entry(root)
    entry_signed.grid(row=14, column=1, padx=10, pady=5)

    tk.Label(root, text="Edition:").grid(row=15, column=0, padx=10, pady=5)
    entry_edition = tk.Entry(root)
    entry_edition.grid(row=15, column=1, padx=10, pady=5)

    # Define the action for submitting data
    var = tk.StringVar()
    tk.Radiobutton(root, text='Sneakers', variable=var, value='Sneakers').grid(row=16, column=0, padx=10, pady=5)
    tk.Radiobutton(root, text='Media', variable=var, value='Media').grid(row=16, column=1, padx=10, pady=5)

    tk.Button(root, text="Submit", command=on_submit).grid(row=17, column=0, columnspan=2, pady=10)

    # Label for profit message
    label_profit_message = tk.Label(root, text="")
    label_profit_message.grid(row=18, column=0, columnspan=2, pady=10)

    root.mainloop()

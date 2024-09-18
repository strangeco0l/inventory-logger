import customtkinter
import main

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.geometry("500x1000")


def window():
    print("Inventory Logger")


frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

label = customtkinter.CTkLabel(master=frame, text="Inventory Logger", font=("Roboto", 24))
label.pack(pady=12, padx=10)

entry1 = customtkinter.CTkEntry(master=frame, placeholder_text="Purchase Date")
entry1.pack(pady=12, padx=10)

entry2 = customtkinter.CTkEntry(master=frame, placeholder_text="Retailer")
entry2.pack(pady=12, padx=10)

entry3 = customtkinter.CTkEntry(master=frame, placeholder_text="Release Date")
entry3.pack(pady=12, padx=10)

entry4 = customtkinter.CTkEntry(master=frame, placeholder_text="Size")
entry4.pack(pady=12, padx=10)

entry5 = customtkinter.CTkEntry(master=frame, placeholder_text="Brand")
entry5.pack(pady=12, padx=10)

entry6 = customtkinter.CTkEntry(master=frame, placeholder_text="Model")
entry6.pack(pady=12, padx=10)

entry7 = customtkinter.CTkEntry(master=frame, placeholder_text="Colorway")
entry7.pack(pady=12, padx=10)

entry8 = customtkinter.CTkEntry(master=frame, placeholder_text="Sku")
entry8.pack(pady=12, padx=10)

entry9 = customtkinter.CTkEntry(master=frame, placeholder_text="Retail")
entry9.pack(pady=12, padx=10)

entry9 = customtkinter.CTkEntry(master=frame, placeholder_text="Resale")
entry9.pack(pady=12, padx=10)

entry10 = customtkinter.CTkEntry(master=frame, placeholder_text="Quantity")
entry10.pack(pady=12, padx=10)


root.mainloop()

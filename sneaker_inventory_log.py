import pandas as pd
import os


def sneaker_inventory_log():
    # Collecting inputs from the user
    purchase_date = input("Purchase date?: ")
    retailer = input("Retailer?: ")
    release_date = input("Release date?: ")
    size = input("What size?: ")
    brand = input("Brand?: ")
    model = input("Model?: ")
    color_way = input("CW?: ")
    sku = input("Sku?: ")
    retail = input("What did you pay?: ")
    resale = input("Whats it worth?: ")
    quantity = int(input("Quantity?: "))

    # Calculating profit
    profit_per = int(resale) - int(retail)
    profit = (int(resale) - int(retail)) * quantity

    # Creating a dictionary to hold the data
    data = {
        "Purchase Date": purchase_date,
        "Retailer": retailer.title(),
        "Release Date": release_date,
        "Size": size,
        "Brand": brand.title(),
        "Model": model.title(),
        "Colorway": color_way.title(),
        "SKU": sku,
        "Quantity": quantity,
        "Retail Price": retail,
        "Resale Price": resale,
        "Profit Per": profit_per,
        "Profit": profit
    }

    # Define the CSV file name
    file_name = "sneaker_inventory_log.csv"

    # Check if the file exists
    file_exists = os.path.isfile(file_name)

    # Load the CSV file if it exists, otherwise create a new DataFrame
    if file_exists:
        df = pd.read_csv(file_name)

        # Exclude the last row if it's a summary row (e.g., "Total Profit")
        if df.iloc[-1]["Purchase Date"] == "Total Profit":
            df = df.iloc[:-1]
    else:
        df = pd.DataFrame(
            columns=["Purchase Date", "Retailer", "Release Date", "Size", "Brand", "Model", "Colorway", "SKU", "Quantity",
                     "Retail Price", "Resale Price", "Profit Per", "Profit"])

    # Example new entry
    new_entry = {
        "Purchase Date": purchase_date,
        "Retailer": retailer,
        "Size": size,
        "Brand": brand,
        "Model": model,
        "Colorway": color_way,
        "SKU": sku,
        "Quantity": quantity,
        "Retail Price": retail,
        "Resale Price": resale,
        "Profit": profit
    }

    # Convert new_entry to a DataFrame
    new_entry_df = pd.DataFrame([data])

    # Concatenate the new entry to the existing DataFrame
    df = pd.concat([df, new_entry_df], ignore_index=True)

    # Calculate the gross profit by summing the "Profit" column
    gross_profit = df["Profit"].sum()

    # Create a new DataFrame for the gross profit row
    gross_profit_row = pd.DataFrame([{
        "Purchase Date": "Total Profit",
        "Profit": gross_profit
    }])

    # Concatenate the gross profit row to the main DataFrame
    df = pd.concat([df, gross_profit_row], ignore_index=True)

    # Save the updated DataFrame back to the CSV file
    df.to_csv(file_name, index=False)










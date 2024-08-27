import pandas as pd
import os


def collectibles_inventory_log():
    purchase_date = input("Purchase date?: ")
    retailer = input("Retailer?: ")
    brand = input("Brand?: ")
    item = input("Item?: ")
    variation = input("Variation?: ")
    quantity = input("Quantity?: ")
    retail = input("What did you pay?: ")
    resale = input("Whats it worth?: ")

    # Calculating profit
    profit_per = int(resale) - int(retail)
    profit = (int(resale) - int(retail)) * quantity

    data = {
        "Purchase date": purchase_date,
        "Retailer": retailer.title(),
        "Brand": brand.title(),
        "Item": item.title(),
        "Variation": variation.title(),
        "Retail": retail,
        "Resale": resale,
        "Profit Per": profit_per,
        "Profit": profit
    }

    # Define the CSV file name
    file_name = "collectibles_inventory_log.csv"

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
            columns=["Purchase Date", "Retailer", "Brand", "Item", "Variation",
                     "Quantity", "Retail Price", "Resale Price", "Profit Per", "Profit"])

    # Example new entry
    new_entry = {
        "Purchase Date": purchase_date,
        "Retailer": retailer,
        "Brand": brand,
        "Item": item,
        "Variation": variation,
        "Quantity": quantity,
        "Retail Price": retail,
        "Resale Price": resale,
        "Profit Per": profit_per,
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

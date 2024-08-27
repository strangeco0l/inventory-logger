import pandas as pd
import os


def save_sneaker_data(sneaker):
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

    # Explicitly map the attributes of the Sneaker instance to the expected column names
    new_entry = {
        "Purchase Date": sneaker.purchase_date,
        "Retailer": sneaker.retailer,
        "Release Date": sneaker.release_date,
        "Size": sneaker.size,
        "Brand": sneaker.brand,
        "Model": sneaker.model,
        "Colorway": sneaker.colorway,
        "SKU": sneaker.sku,
        "Quantity": sneaker.quantity,
        "Retail Price": sneaker.retail_price,
        "Resale Price": sneaker.resale_price,
        "Profit Per": sneaker.profit_per,
        "Profit": sneaker.profit
    }

    # Convert new_entry to a DataFrame
    new_entry_df = pd.DataFrame([new_entry])

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


def save_collectibles_data(collectibles):

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
        "Purchase Date": collectibles.purchase_date,
        "Retailer": collectibles.retailer,
        "Brand": collectibles.brand,
        "Item": collectibles.item,
        "Variation": collectibles.variation,
        "Quantity": collectibles.quantity,
        "Retail Price": collectibles.retail_price,
        "Resale Price": collectibles.resale_price,
        "Profit Per": collectibles.profit_per,
        "Profit": collectibles.profit
    }

    # Convert new_entry to a DataFrame
    new_entry_df = pd.DataFrame([new_entry])

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


def save_media_data(data):
    file_name = "media_inventory_log.csv"
    file_exists = os.path.isfile(file_name)
    df = pd.DataFrame([data])
    df.to_csv(file_name, mode='a', index=False, header=not file_exists)

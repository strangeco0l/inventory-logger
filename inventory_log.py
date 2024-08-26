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


def media_inventory_log():
    purchase_date = input("Purchase date?: ")
    retailer = input("Retailer?: ")
    # Collecting inputs from the user
    media = input("Media type (Vinyl or CD)?: ")

    # Initialize speed variable
    speed = None

    # Conditional logic based on media type
    if media.lower() == 'vinyl':
        speed = input("Vinyl speed?: ")
    elif media.lower() == 'cd':
        print("Skipping speed input for CD.")
    else:
        print("Invalid media type")
        return  # Exit the function if the media type is not recognized

    artist = input("Artist?: ")
    album = input("Album?: ")
    variation = input("Variation?: ")
    signed = input("Signed?: ")
    edition = input("Edition?: ")
    retail = input("What did you pay?: ")
    resale = input("Whats it worth?: ")

    # Calculating profit
    profit = int(resale) - int(retail)

    # Printing the profit message
    if profit > 0:
        print(f"Looks like there is money to be made! The profit is ${profit}.")

    data = {
        "Purchase date": purchase_date,
        "Retailer": retailer.title(),
        "Media": media,
        "Speed": speed,
        "Artist": artist.title(),
        "Album": album,
        "Variation": variation,
        "Signed?": signed,
        "Edition": edition,
        "Retail": retail,
        "Resale": resale,
        "Profit": profit
    }

    # Define the CSV file name
    file_name = "media_inventory_log.csv"

    # Check if the file exists
    file_exists = os.path.isfile(file_name)

    # Create a DataFrame from the data
    df = pd.DataFrame([data])

    # Write the data to a CSV file
    # If the file exists, append the new data without writing the header
    df.to_csv(file_name, mode='a', index=False, header=not file_exists)


def collectibles_inventory_log():
    purchase_date = input("Purchase date?: ")
    retailer = input("Retailer?: ")
    brand = input("Brand?: ")
    item = input("Item?: ")
    variation = input("Variation?: ")
    retail = input("What did you pay?: ")
    resale = input("Whats it worth?: ")

    # Calculating profit
    profit = int(resale) - int(retail)

    # Printing the profit message
    if profit > 0:
        print(f"Looks like there is money to be made! The profit is ${profit}.")

        data = {
            "Purchase date": purchase_date,
            "Retailer": retailer.title(),
            "Brand": brand.title(),
            "Item": item.title(),
            "Variation": variation,
            "Retail": retail,
            "Resale": resale,
            "Profit": profit
        }

        # Define the CSV file name
        file_name = "media_inventory_log.csv"

        # Check if the file exists
        file_exists = os.path.isfile(file_name)

        # Create a DataFrame from the data
        df = pd.DataFrame([data])

        # Write the data to a CSV file
        # If the file exists, append the new data without writing the header
        df.to_csv(file_name, mode='a', index=False, header=not file_exists)


# Call the function
user_input = input("Enter 'Sneakers', or 'Media', or 'Collectibles' ")
if user_input == 'Sneakers':
    sneaker_inventory_log()
elif user_input == 'Media':
    media_inventory_log()
elif user_input == 'Collectibles':
    collectibles_inventory_log()

else:
    print("Invalid Input")

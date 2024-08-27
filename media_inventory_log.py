import pandas as pd
import os

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
    quantity = int(input("Quantity?: "))
    retail = input("What did you pay?: ")
    resale = input("Whats it worth?: ")

    # Calculating profit
    profit_per = int(resale) - int(retail)
    profit = (int(resale) - int(retail)) * quantity

    data = {
        "Purchase date": purchase_date,
        "Retailer": retailer.title(),
        "Media": media,
        "Speed": speed,
        "Artist": artist.title(),
        "Album": album.title(),
        "Variation": variation,
        "Signed?": signed.title(),
        "Edition": edition,
        "Quantity": quantity,
        "Retail": retail,
        "Resale": resale,
        "Profit Per": profit_per,
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
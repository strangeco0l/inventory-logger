import pandas as pd
import os

def save_sneaker_data(data):
    file_name = "sneaker_inventory_log.csv"
    file_exists = os.path.isfile(file_name)
    df = pd.DataFrame([data])
    df.to_csv(file_name, mode='a', index=False, header=not file_exists)

def save_media_data(data):
    file_name = "media_inventory_log.csv"
    file_exists = os.path.isfile(file_name)
    df = pd.DataFrame([data])
    df.to_csv(file_name, mode='a', index=False, header=not file_exists)

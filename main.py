from sneaker_inventory_log import sneaker_inventory_log
from media_inventory_log import media_inventory_log
from collectibles_inventory_log import collectibles_inventory_log


# Call the function
user_input = input("Enter 'Sneakers', or 'Media', or 'Collectibles' ").strip().title()

if user_input == 'Sneakers':
    sneaker_inventory_log()
elif user_input == 'Media':
    media_inventory_log()
elif user_input == 'Collectibles':
    collectibles_inventory_log()
else:
    print("Invalid Input")

from sneaker_inventory_log import sneaker_inventory_log
from media_inventory_log import media_inventory_log
from collectibles_inventory_log import collectibles_inventory_log


def main():
    options = {
        'sneakers': sneaker_inventory_log,
        'media': media_inventory_log,
        'collectibles': collectibles_inventory_log
    }

    while True:
        user_input = input(
            "Enter one of the following to log inventory: Sneakers, Media, Collectibles (or type 'exit' to quit): ").strip().lower()

        if user_input == 'exit':
            print("Goodbye!")
            break
        elif user_input in options:
            options[user_input]()  # Call the appropriate function
        else:
            print("Invalid input. Please enter 'Sneakers', 'Media', or 'Collectibles'.")


if __name__ == "__main__":
    main()

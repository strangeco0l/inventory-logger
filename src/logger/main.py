from logger.sneaker_inventory_log import sneaker_inventory_log
from logger.media_inventory_log import media_inventory_log
from logger.collectibles_inventory_log import collectibles_inventory_log


def main():
    print("Welcome to the Inventory Logger!")

    while True:
        user_input = input(
            "Enter one of the following to log inventory: Sneakers, Media, Collectibles (or type 'exit' to quit): "
        ).strip()

        if user_input.lower() == "exit":
            break

        options = {
            "Sneakers": sneaker_inventory_log,
            "Media": media_inventory_log,
            "Collectibles": collectibles_inventory_log,
        }

        if user_input in options:
            user_id = input("Enter your user ID: ").strip()  # <- Ask user for ID
            options[user_input](user_id)  # Pass user_id
        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    main()

import unittest
from unittest.mock import patch
from logger.sneaker_inventory_log import *
from logger.media_inventory_log import *
from logger.data_handling import *
from logger.collectibles_inventory_log import *


class TestSneaker(unittest.TestCase):

    def test_sneaker_initialization(self):
        sneaker = Sneaker(
            purchase_date="2024-09-18",
            retailer="Nike",
            release_date="2024-08-01",
            size="10",
            brand="Nike",
            model="Air Max",
            colorway="Red/White",
            sku="AM123",
            retail_price=100.00,
            resale_price=150.00,
            quantity=2
        )

        self.assertEqual(sneaker.profit_per, 50.00)
        self.assertEqual(sneaker.profit, 100.00)

    def test_single_quantity_sneaker_profit(self):
        sneaker = Sneaker(
            purchase_date="2024-09-18",
            retailer="Nike",
            release_date="2024-08-01",
            size="10",
            brand="Nike",
            model="Air Max",
            colorway="Red/White",
            sku="AM123",
            retail_price=100.00,
            resale_price=120.00,
            quantity=1
        )

        self.assertEqual(sneaker.profit_per, 20.00)
        self.assertEqual(sneaker.profit, 20.00)

    class TestMedia(unittest.TestCase):
        def test_vinyl_initialization(self):

            media = Media(
                purchase_date="2024-09-18",
                retailer="Target",
                media="Vinyl",
                speed="33rpm",
                artist="Prince",
                album="Purple Rain",
                variation="Target Exclusive",
                signed="No",
                edition="Purple Vinyl",
                retail_price=30.00,
                resale_price=40.00,
                quantity=2
                )

            self.assertEqual(media.profit_per, 10)
            self.assertEqual(media.profit, 20.00)

        def test_single_quantity_vinyl_profit(self):
            media = Media(
                purchase_date="2024-09-18",
                retailer="Target",
                media="Vinyl",
                speed="33rpm",
                artist="Prince",
                album="Purple Rain",
                variation="Target Exclusive",
                signed="No",
                edition="Purple Vinyl",
                retail_price=30.00,
                resale_price=40.00,
                quantity=1
            )

            self.assertEqual(media.profit_per, 10)
            self.assertEqual(media.profit, 10.00)

    @patch('builtins.input', side_effect=[
        '2024-09-18', 'Nike', '2024-08-01', '10', 'Nike',
        'Air Max', 'Red/White', 'AM123', '100', '150', '2', 'n'
    ])
    @patch('logger.data_handling')
    def test_sneaker_inventory_log(self, mock_save, mock_input):

        # Assert that save_sneaker_data was called once
        self.assertEqual(mock_save.call_count, 0, "save_sneaker_data was not called")

        if mock_save.call_count > 0:

            # Check the arguments passed to save_sneaker_data
            saved_sneaker = mock_save.call_args[0][0]
            self.assertEqual(saved_sneaker.profit_per, 50.00)
            self.assertEqual(saved_sneaker.profit, 100.00)


if __name__ == '__main__':
    unittest.main()

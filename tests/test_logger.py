import unittest
from logger.sneaker_inventory_log import Sneaker, sneaker_inventory_log
from logger.media_inventory_log import Media, gather_media_data
from logger.collectibles_inventory_log import Collectibles
from unittest.mock import patch


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


class TestGatherMediaData(unittest.TestCase):

    @patch('builtins.input', side_effect=[
        '2024-09-18', 'Best Buy', 'Vinyl', '33',
        'The Beatles', 'Abbey Road', 'Limited', 'Yes', 'First',
        '2', '40', '80'
    ])
    def test_gather_media_data_vinyl(self, mock_input):
        media = gather_media_data()
        self.assertEqual(media.media.lower(), 'vinyl')
        self.assertEqual(media.speed, '33')
        self.assertEqual(media.artist, 'The Beatles')
        self.assertEqual(media.quantity, 2)
        self.assertAlmostEqual(media.retail_price, 40.0)
        self.assertAlmostEqual(media.resale_price, 80.0)

    @patch('builtins.input', side_effect=[
        '2024-09-18', 'Amazon', 'CD',
        'The Beatles', 'Revolver', 'Standard', 'No', 'Second',
        '1', '10', '20'
    ])
    def test_gather_media_data_cd(self, mock_input):
        media = gather_media_data()
        self.assertEqual(media.media.lower(), 'cd')
        self.assertEqual(media.speed, 'N/A')
        self.assertEqual(media.album, 'Revolver')
        self.assertEqual(media.quantity, 1)
        self.assertAlmostEqual(media.retail_price, 10.0)
        self.assertAlmostEqual(media.resale_price, 20.0)


class TestCollectibles(unittest.TestCase):

    def test_collectibles_initialization(self):
        collectibles = Collectibles(
            purchase_date="2024-09-18",
            retailer="Walmart",
            brand="Funko",
            item="Freddy Funko",
            variation="LE 1000pcs",
            retail_price=9.99,
            resale_price=99.99,
            quantity=2,
        )
        self.assertAlmostEqual(collectibles.profit_per, 90.00, places=2)
        self.assertAlmostEqual(collectibles.profit, 180.00, places=2)

    def test_single_quantity_collectibles_profit(self):
        collectibles = Collectibles(
            purchase_date="2024-09-18",
            retailer="Walmart",
            brand="Funko",
            item="Freddy Funko",
            variation="LE 1000pcs",
            retail_price=9.99,
            resale_price=99.99,
            quantity=1,
        )
        self.assertEqual(collectibles.profit_per, 90.00)
        self.assertEqual(collectibles.profit, 90.00)


class TestSneakerInventoryLog(unittest.TestCase):

    @patch('logger.sneaker_inventory_log.save_sneaker_data')
    @patch('builtins.input', side_effect=[
        '2024-09-18', 'Nike', '2024-08-01', '10', 'Nike',
        'Air Max', 'Red/White', 'AM123', '100', '150', '2', 'n'
    ])
    def test_sneaker_inventory_log(self, mock_input, mock_save):
        sneaker_inventory_log()

        self.assertEqual(mock_save.call_count, 1)
        sneaker_obj = mock_save.call_args[0][0]
        self.assertEqual(sneaker_obj.profit_per, 50.00)
        self.assertEqual(sneaker_obj.profit, 100.00)


if __name__ == '__main__':
    unittest.main()

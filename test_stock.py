import unittest
import stock

class Test_stock(unittest.TestCase):

    def test_get_name(self):
        expected_result_1 = "Microsoft Corporation"
        expected_result_2 = "Alphabet Inc."
        stock_name_1 = "msft"
        stock_name_2 = "googl"
        print(stock.get_name(stock_name_2))
        self.assertEqual(stock.get_name(stock_name_1),expected_result_1)
        self.assertEqual(stock.get_name(stock_name_2),expected_result_2)

if __name__ == '__main__':
    unittest.main()
        
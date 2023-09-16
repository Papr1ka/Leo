from polish import ReversePolishConverter, ReversePolishCounter
import unittest

test_conv = lambda conv, x: " ".join(conv.convert(x))
test_count = lambda counter, x, y: (counter.calculate(x) - y < 0.001)

class TestStack(unittest.TestCase):

    def test_converter(self):
        converter = ReversePolishConverter()
        self.assertEqual(test_conv(converter, "1+7*(8-6)"), "1 7 8 6 - * +")
        self.assertEqual(test_conv(converter, "1 + 7 * ( 8 - 6 )"), "1 7 8 6 - * +")
        self.assertEqual(test_conv(converter, "a+(b-c)*d"), "a b c - d * +")
        self.assertEqual(test_conv(converter, "(6 + 9 - 5)/(8 + 1 * 2)+7"), "6 9 + 5 - 8 1 2 * + / 7 +")
    
    def test_counter(self):
        counter = ReversePolishCounter()
        self.assertEqual(test_count(counter, "1 7 8 6 - * +", 15), True)
        self.assertEqual(test_count(counter, "6 9 + 5 - 8 1 2 * + / 7 +", 8), True)
        self.assertEqual(test_count(counter, "1 7 8 6 - * +", 15), True)
        self.assertEqual(test_count(counter, "1 7 8 6 - * +", 15), True)
        self.assertEqual(test_count(counter, "1 7 8 6 - * +", 15), True)

if __name__ == '__main__':
    unittest.main()

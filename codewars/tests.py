import unittest
from roman_int_converter import RomanNumerals

converter = RomanNumerals()

class TestMain(unittest.TestCase):
    def test_to_roman(self):
        self.assertEqual(converter.to_roman(1000), 'M')
        self.assertEqual(converter.to_roman(4), 'IV')
        self.assertEqual(converter.to_roman(1), 'I')
        self.assertEqual(converter.to_roman(1990), 'MCMXC')
        self.assertEqual(converter.to_roman(2008), 'MMVIII')
    def test_from_roman(self):
        self.assertEqual(converter.from_roman('XXI'), 21)
        self.assertEqual(converter.from_roman('I'), 1)
        self.assertEqual(converter.from_roman('IV'), 4)
        self.assertEqual(converter.from_roman('MMVIII'), 2008)
        self.assertEqual(converter.from_roman('MDCLXVI'), 1666)    

if __name__ == '__main__':
    unittest.main()

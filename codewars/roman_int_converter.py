class RomanNumerals:

    def __init__(self) -> None:
        self.number_map = {
            'I': 1,
            'IV': 4,
            'V': 5,
            'IX': 9,
            'X': 10,
            'XL': 40,
            'L': 50,
            'XC': 90,
            'C': 100,
            'CD': 400,
            'D': 500,
            'CM': 900,
            'M': 1000
        }


    def to_roman(self, val) -> str:
        roman_map = dict(sorted(self.number_map.items(), key=lambda x: x[1], reverse=True))

        result = []
        for roman_number in roman_map:
            roman_number_int = int(roman_map[roman_number])
            for i in range(val // roman_number_int):
                result.append(roman_number)
                val -= roman_number_int

        return ''.join(result)

    def from_roman(self, roman_num) -> int:            
        result = 0
        while roman_num:
            if roman_num[:2] in self.number_map:
                result += self.number_map[roman_num[:2]]
                roman_num = roman_num[2:]
            else:
                result += self.number_map[roman_num[0]]
                roman_num = roman_num[1:]
        return result


if __name__ == "__main__":
    converter = RomanNumerals()

    RESULT_TO = converter.to_roman(1990)
    RESULT_FROM = converter.from_roman('MCMXC')

    print(f'To roman result: {RESULT_TO}')
    print(f'From roman result: {RESULT_FROM}')

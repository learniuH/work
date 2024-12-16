import re

class People:
    height = 100
    def __init__(self):
        self.weight = 200
        People.value_change()

    @classmethod
    def value_change(cls):
        cls.height = 20

# package = '10 A 89 1       '
# a = re.findall(r'[0-9A-Fa-f]+', package)
# for i, element in enumerate(a):
#     print(i, int(element, 16))

def extract_numbers(s: str) -> list:
    # 使用正则表达式提取数字
    # return [int(num) for num in re.findall(r'\d+', s)]
    print(re.findall(r'\d+', s))

s = 'byte01-bit2'
# print(extract_numbers(s)`)
# extract_numbers(s)
print(int([1]))
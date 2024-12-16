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


for i, a in enumerate(range(5, -1, -1)):
    print(i, a)
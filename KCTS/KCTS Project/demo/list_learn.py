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

a = [1,2,3,4]
a[1:3] = [0] * (3 - 1)
print(a)
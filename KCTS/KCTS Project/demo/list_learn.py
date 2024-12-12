def is_happy(n: int):
    storage = []    # 存储所有平方和的值
    while True:
        digit = []  # 存放个十百千位的值
        while n != 0:
            digit.append(n % 10)   # 取出个位的值
            n = n // 10     # 正数中除个位的值

        sum = 0             # 存放个十百千位的平方和
        for i in digit:
            sum += pow(i, 2)
        n = sum

        if sum == 1:
            return True     # 平方和为1, 是快乐数
        if sum in storage:
            return False    # 平方和在 存数的列表里
        else:
            storage.append(sum)     # 将数添加到列表

n = input('输入整数')
print(is_happy(int(n)))

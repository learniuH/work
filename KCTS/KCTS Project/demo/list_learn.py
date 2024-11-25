import pandas as pd

# 示例 DataFrame
data = {
    0: ['A', 'B', '内容', 'D'],
    1: [1, 2, 3, None],
    2: [4, 5, None, 7]
}
df = pd.DataFrame(data)

# 找到包含 '内容' 的单元格所在列号
column_index = df.eq('内容').any(axis=0).idxmax()

print(f"'内容'所在的列号是: {column_index}")

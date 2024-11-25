import pandas as pd


class ExcelRead():
    def __init__(self, file_path):
        # 表单的名字
        self.file_path = file_path


    def read_sheet_name(self) -> list:
        ''' 读取表格里所有的表单, 返回各表单的名字 '''
        excel_file = pd.ExcelFile(self.file_path)
        sheet_name = excel_file.sheet_names
        return sheet_name


    def read_file(self, sheet_name):
        df = pd.read_excel(file_path, sheet_name=sheet_name, header=None, index_col=None)
        ''' header = None, index_col = None 避免pandas自动更改行号和列号, 使用原始索引读取 '''
        # try:
        #     # 找到包含'字节序号'的行号
        #     header_index = df[df.eq('字节序号').any(axis=1)].index[0]
        #     # 将'字节序号'作为columns
        #     df.columns = df.iloc[header_index]
        #     # 删除作为列名的行, 并重置索引
        #     df = df[(header_index + 1):].reset_index(drop=True)
        #     # print(df)
        # except Exception as e:
        #     print(str(e))

        # '内容' 所在的行号和列号
        content_row_index, content_col_index = df.eq('内容').stack().idxmax()
        ''' 
        df.eq('内容') - 返回 boolean型的DataFrame, 标记每个单元格是否是 '内容’
        .stack()     - 将DataFrame转为一维索引的 Series
        .idxmax()    - 找到第一个为 True 的索引
        '''

        # 只读取'内容'左边的字节序号列 和 右边的那一列
        start_col_index, end_col_index = content_col_index - 1, content_col_index + 2
        target_cells = df.iloc[content_row_index:, start_col_index: end_col_index]


        # 删除右边那一列中包含 预留 或是 nan 的所有行
        # target_cells = target_cells[~target_cells.iloc[:, 2].astype(str).str.contains('预留', na=False)]
        # print(target_cells.columns)

        # target_cells = target_cells[target_cells[4]].astype(str).str.contains('预留', na=False)

        print(target_cells[1])
        # print(target_cells)


if __name__ == '__main__':
    file_path = "D:\LearniuH\Project\中测推土机\功能定义\推土机标准化内部通信协议-V1.0-202400918.xlsx"
    sheet_name = '（推土机-OU）->MU&OC'
    a = ExcelRead(file_path)
    # a.read_sheet_name()
    a.read_file(sheet_name)

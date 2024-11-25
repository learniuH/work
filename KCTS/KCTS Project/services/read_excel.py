
import pandas as pd


class ExcelRead():
    def __init__(self, file_path: str):
        # 表单的名字
        self.file_path = file_path


    def read_sheet_name(self) -> list:
        ''' 读取表格里所有的表单, 返回各表单的名字 '''
        excel_file = pd.ExcelFile(self.file_path)
        sheet_name = excel_file.sheet_names
        return sheet_name


    def read_file(self, sheet_name: str):

        protocol = {}

        df = pd.read_excel(file_path, sheet_name=sheet_name)



        # 获取 字节序号 所在的列索引
        col_index = df.columns.get_loc(df.eq('字节序号').stack().idxmax()[1])
        ''' 
        df.eq('内容') - 返回 boolean型的DataFrame, 标记每个单元格是否是 '字节序号’
        .stack()     - 将DataFrame转为一维索引的 Series
        .idxmax()    - 找到第一个为 True 的位置, 返回行索引+列所用
        '''

        # 选取列范围, 从 字节序号 所在的列开始 往右取两列
        target_cells = df.iloc[1:, col_index: col_index + 3]

        # 设置目标三列的 columns
        target_cells.columns = ['字节序号', '内容', '开关描述']
        # 填充 字节序号 列, 如果字节序号出现一次以上, 认为是开关量, 否则是模拟量
        target_cells.loc[:, '字节序号'] = target_cells['字节序号'].fillna(method='ffill')
        # 筛选出重复的字节序号, 作为开关量
        duplicates = target_cells['字节序号'].value_counts()
        repeat_values = duplicates[duplicates > 1]

        # 将开关量的字典初始化
        for digital_switch in repeat_values.index:
            protocol[digital_switch] = {}

        # 删除 开关描述 中为 nan 或 有 预留 的单元格所在行, 并保留 CRC(最后一行)
        target_cells = target_cells.iloc[:-1][~(target_cells.iloc[:-1]['开关描述'].isna() |
                                               target_cells.iloc[:-1]['开关描述'].astype(str).str.contains('预留'))]
        # 添加CRC最后一行回去
        target_cells = pd.concat([target_cells, target_cells.iloc[[-1]]], ignore_index=True)

        # 更新开关量字典


        print(target_cells)





if __name__ == '__main__':
    # file_path = "D:\LearniuH\Project\中测推土机\功能定义\推土机标准化内部通信协议-V1.0-202400918.xlsx"
    file_path = "C:\\Users\L\Desktop\自动化测试\推土机标准化内部通信协议-V1.0-202400918.xlsx"
    sheet_name = '（推土机-OU）->MU&OC'
    a = ExcelRead(file_path)
    # a.read_sheet_name()
    a.read_file(sheet_name)

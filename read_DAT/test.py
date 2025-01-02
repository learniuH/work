def parse_packages(data):
    """
    解析二进制数据并提取以 A3 52 33 01 开头的数据包

    Args:
        data (bytes): 要解析的二进制数据

    Returns:
        list: 提取出的数据包列表
    """
    # 转换头部为字节进行比较
    header = bytes([0xA3, 0x52, 0x33, 0x01])
    packages = []

    # 查找所有头部出现的位置
    current_pos = 0
    while True:
        # 查找下一个头部
        pos = data.find(header, current_pos)

        # 打印调试信息
        print(f"当前位置: {current_pos}, 找到头部位置: {pos}")

        if pos == -1:  # 没有找到更多头部
            # 如果还有剩余数据，将其作为最后一个包
            if current_pos < len(data):
                last_package = data[current_pos - 1:]
                if last_package.startswith(header):  # 确保最后一个包也是以正确的头部开始
                    packages.append(last_package)
                    print(f"添加最后一个包，长度: {len(last_package)} 字节")
            break

        # 如果这不是第一个包，添加前一个包
        if current_pos > 0 and pos > current_pos:
            package = data[current_pos - 1:pos]
            if package.startswith(header):  # 只添加以正确头部开始的包
                packages.append(package)
                print(f"添加包，长度: {len(package)} 字节")

        # 关键修复：确保 current_pos 始终向前移动
        current_pos = pos + 1  # 移动到头部后的下一个位置
        if current_pos >= len(data):
            break

    return packages


# 使用示例
def main():
    try:
        # 读取二进制文件
        with open('逆时针内圈.DAT', 'rb') as f:
            data = f.read()

        print(f"文件总大小: {len(data)} 字节")

        # 解析包
        packages = parse_packages(data)

        # 打印找到的包的信息
        print(f"\n总共找到 {len(packages)} 个数据包")
        for i, package in enumerate(packages):
            print(f"\n数据包 {i + 1}:")
            print(f"长度: {len(package)} 字节")
            print(f"头部字节: {package[:10].hex()}")  # 打印前10个字节的十六进制表示

    except FileNotFoundError:
        print("错误：找不到文件 '逆时针内圈.DAT'")
    except Exception as e:
        print(f"发生错误: {str(e)}")


if __name__ == "__main__":
    main()
import os

def read_d01kp_data(file_path):
    """
    读取D{0-1}KP数据集文件
    :param file_path: 数据文件路径
    :return: tuple (capacity, item_sets)
             capacity: 背包最大载重
             item_sets: 项集列表，每个项集包含3个物品的(重量, 价值)
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"数据文件不存在：{file_path}")

    item_sets = []
    capacity = 0

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
        # 第一行是背包容量
        capacity = int(lines[0])
        # 后续每行是一个项集的3个物品（重量1,价值1,重量2,价值2,重量3,价值3）
        for line in lines[1:]:
            nums = list(map(int, line.split(',')))
            if len(nums) != 6:
                raise ValueError(f"数据格式错误：{line}，需6个数值（w1,v1,w2,v2,w3,v3）")
            item1 = (nums[0], nums[1])
            item2 = (nums[2], nums[3])
            item3 = (nums[4], nums[5])
            item_sets.append([item1, item2, item3])

    return capacity, item_sets


# 测试代码
if __name__ == "__main__":
    capacity, items = read_d01kp_data("../data/d01kp_data.txt")
    print(f"背包容量：{capacity}")
    print(f"项集数量：{len(items)}")
    print(f"第一个项集：{items[0]}")
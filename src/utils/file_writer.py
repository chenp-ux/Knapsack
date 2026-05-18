import os
import pandas as pd


def save_to_txt(result, file_path):
    """
    将求解结果保存为TXT文件
    :param result: 求解结果字典（max_value, selected_items, cost_time, total_weight）
    :param file_path: 保存路径
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write("D{0-1}KP最优解结果\n")
        f.write("=" * 50 + "\n")
        f.write(f"最大价值：{result['max_value']}\n")
        f.write(f"总重量：{result['total_weight']}\n")
        f.write(f"求解耗时：{result['cost_time']:.6f}秒\n")
        f.write(f"选中物品：\n")
        for i, j in result['selected_items']:
            f.write(f"  项集{i} - 物品{j}\n")
    print(f"结果已保存至TXT：{file_path}")


def save_to_excel(result, file_path):
    """
    将求解结果保存为Excel文件
    :param result: 求解结果字典
    :param file_path: 保存路径
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    # 基础信息
    basic_data = {
        "指标": ["最大价值", "总重量", "求解耗时(秒)"],
        "值": [result['max_value'], result['total_weight'], round(result['cost_time'], 6)]
    }
    # 选中物品信息
    selected_data = {
        "项集索引": [i for i, j in result['selected_items']],
        "物品索引": [j for i, j in result['selected_items']]
    }

    # 写入Excel（多个sheet）
    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        pd.DataFrame(basic_data).to_excel(writer, sheet_name="基础结果", index=False)
        pd.DataFrame(selected_data).to_excel(writer, sheet_name="选中物品", index=False)
    print(f"结果已保存至Excel：{file_path}")


# 测试代码
if __name__ == "__main__":
    test_result = {
        "max_value": 13,
        "selected_items": [(0, 2), (1, 1)],
        "cost_time": 0.001234,
        "total_weight": 8
    }
    save_to_txt(test_result, "../output/result.txt")
    save_to_excel(test_result, "../output/result.xlsx")
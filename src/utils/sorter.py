def sort_by_ratio(item_sets):
    """
    按项集第三项的价值/重量比非递增排序
    :param item_sets: 原始项集列表
    :return: 排序后的项集列表、排序后的索引映射
    """
    # 计算每个项集第三项的价值/重量比
    ratio_list = []
    for i, item_set in enumerate(item_sets):
        w3, v3 = item_set[2]
        ratio = v3 / w3 if w3 != 0 else 0
        ratio_list.append((i, ratio))

    # 按比值降序排序
    ratio_list.sort(key=lambda x: x[1], reverse=True)

    # 重新排列项集
    sorted_item_sets = [item_sets[i] for i, _ in ratio_list]
    # 记录排序后的索引映射（原索引->新索引）
    index_map = {old_idx: new_idx for new_idx, (old_idx, _) in enumerate(ratio_list)}

    return sorted_item_sets, index_map


# 测试代码
if __name__ == "__main__":
    item_sets = [
        [(2, 3), (3, 4), (4, 7)],  # 第三项比值：7/4=1.75
        [(5, 6), (4, 5), (8, 11)]  # 第三项比值：11/8=1.375
    ]
    sorted_items, index_map = sort_by_ratio(item_sets)
    print("排序后的项集：")
    for i, item in enumerate(sorted_items):
        print(f"项集{i}：{item}")
    print("索引映射：", index_map)
import time


class D01KPAlgorithm:
    """D{0-1}KP问题动态规划求解类"""

    def __init__(self, capacity, item_sets):
        """
        初始化
        :param capacity: 背包最大载重
        :param item_sets: 项集列表
        """
        self.capacity = capacity
        self.item_sets = item_sets
        self.item_count = len(item_sets)
        self.max_value = 0
        self.selected_items = []  # 存储选中的项集和物品索引
        self.cost_time = 0  # 求解耗时

    def solve(self):
        """
        动态规划求解D{0-1}KP最优解
        状态定义：dp[i][j] 表示前i个项集，背包载重j时的最大价值
        状态转移：
        对于第i个项集，有4种选择：不选、选第1个物品、选第2个物品、选第3个物品
        """
        start_time = time.time()

        # 初始化DP表：(item_count+1)行 × (capacity+1)列
        dp = [[0] * (self.capacity + 1) for _ in range(self.item_count + 1)]

        # 填充DP表
        for i in range(1, self.item_count + 1):
            item_set = self.item_sets[i - 1]  # 第i个项集（索引从0开始）
            for j in range(1, self.capacity + 1):
                # 不选当前项集
                dp[i][j] = dp[i - 1][j]

                # 尝试选当前项集的3个物品
                for idx, (weight, value) in enumerate(item_set):
                    if weight <= j:
                        if dp[i - 1][j - weight] + value > dp[i][j]:
                            dp[i][j] = dp[i - 1][j - weight] + value

        # 回溯找到选中的物品
        self.max_value = dp[self.item_count][self.capacity]
        remaining_cap = self.capacity
        for i in range(self.item_count, 0, -1):
            if dp[i][remaining_cap] != dp[i - 1][remaining_cap]:
                # 当前项集被选中，找到具体选的哪个物品
                item_set = self.item_sets[i - 1]
                for idx, (weight, value) in enumerate(item_set):
                    if remaining_cap >= weight and dp[i - 1][remaining_cap - weight] + value == dp[i][remaining_cap]:
                        self.selected_items.append((i - 1, idx))  # (项集索引, 物品索引)
                        remaining_cap -= weight
                        break

        # 计算耗时
        self.cost_time = time.time() - start_time
        self.selected_items.reverse()  # 反转，按项集顺序排列

        return {
            "max_value": self.max_value,
            "selected_items": self.selected_items,
            "cost_time": self.cost_time,
            "total_weight": sum(self.item_sets[i][j][0] for i, j in self.selected_items)
        }


# 测试代码
if __name__ == "__main__":
    # 测试数据：容量10，2个项集
    capacity = 10
    item_sets = [
        [(2, 3), (3, 4), (4, 7)],  # 项集0：物品0(2,3)、物品1(3,4)、物品2(4,7)
        [(5, 6), (4, 5), (8, 11)]  # 项集1：物品0(5,6)、物品1(4,5)、物品2(8,11)
    ]
    solver = D01KPAlgorithm(capacity, item_sets)
    result = solver.solve()
    print(f"最大价值：{result['max_value']}")
    print(f"选中物品：{result['selected_items']}")
    print(f"总重量：{result['total_weight']}")
    print(f"耗时：{result['cost_time']:.6f}秒")
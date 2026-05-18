import matplotlib.pyplot as plt
import os

# 设置中文字体，避免乱码
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


def plot_scatter(item_sets, save_path=None):
    """
    绘制项集物品的重量-价值散点图
    :param item_sets: 项集列表
    :param save_path: 图片保存路径（None则显示）
    """
    # 提取所有物品的重量和价值
    weights = []
    values = []
    labels = []
    for i, item_set in enumerate(item_sets):
        for j, (w, v) in enumerate(item_set):
            weights.append(w)
            values.append(v)
            labels.append(f"项集{i}-物品{j}")

    # 绘制散点图
    plt.figure(figsize=(10, 6))
    plt.scatter(weights, values, s=100, c='blue', alpha=0.7)

    # 添加标签
    for i, label in enumerate(labels):
        plt.annotate(label, (weights[i], values[i]), xytext=(5, 5), textcoords='offset points')

    plt.xlabel('重量')
    plt.ylabel('价值')
    plt.title('D{0-1}KP数据散点图')
    plt.grid(True, linestyle='--', alpha=0.5)

    # 保存或显示
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"散点图已保存至：{save_path}")
    else:
        plt.show()


# 测试代码
if __name__ == "__main__":
    item_sets = [
        [(2, 3), (3, 4), (4, 7)],
        [(5, 6), (4, 5), (8, 11)]
    ]
    plot_scatter(item_sets, "../output/scatter.png")
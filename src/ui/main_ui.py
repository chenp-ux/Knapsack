# -*- coding: utf-8 -*-
"""
D{0-1}KP背包问题求解器 - 图形用户界面
功能：提供可视化操作界面，支持数据加载、绘图、排序、求解、结果保存
"""
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import sys
import os

# ===================== 核心路径配置（解决导入报错） =====================
# 获取当前文件（main_ui.py）的绝对路径
current_file = os.path.abspath(__file__)
# 获取当前文件所在目录（src/ui/）
ui_dir = os.path.dirname(current_file)
# 获取src根目录（src/）
src_dir = os.path.dirname(ui_dir)
# 将src目录加入Python搜索路径（优先搜索）
sys.path.insert(0, src_dir)

# ===================== 导入核心模块（绝对导入，无报错） =====================
try:
    from utils.data_reader import read_d01kp_data
    from utils.plotter import plot_scatter
    from utils.sorter import sort_by_ratio
    from utils.file_writer import save_to_txt, save_to_excel
    from core.dp_algorithm import D01KPAlgorithm
except ImportError as e:
    # 导入失败时给出明确提示
    messagebox.showerror("导入错误", f"核心模块导入失败：{str(e)}\n请检查src目录结构是否正确！")
    sys.exit(1)


class D01KPUI:
    """D{0-1}KP背包问题求解器图形界面类"""

    def __init__(self, root):
        """
        初始化界面
        :param root: tkinter主窗口对象
        """
        self.root = root
        self.root.title("D{0-1}KP背包问题求解器")
        self.root.geometry("800x600")
        self.root.resizable(True, True)  # 允许窗口缩放

        # 全局变量：存储加载的数据和求解结果
        self.capacity = 0  # 背包最大载重
        self.item_sets = []  # 项集列表（每个项集含3个物品的(重量,价值)）
        self.solve_result = None  # 求解结果字典

        # 创建界面组件
        self._create_widgets()

    def _create_widgets(self):
        """创建所有界面组件"""
        # 1. 数据文件选择区域
        frame_file = ttk.LabelFrame(self.root, text="数据文件操作", padding=(10, 5))
        frame_file.pack(fill="x", padx=10, pady=5)

        # 文件路径输入框 + 浏览按钮 + 加载按钮
        ttk.Label(frame_file, text="数据文件路径：").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.file_path_var = tk.StringVar()
        entry_file = ttk.Entry(frame_file, textvariable=self.file_path_var, width=50)
        entry_file.grid(row=0, column=1, padx=5, pady=5)

        btn_browse = ttk.Button(frame_file, text="浏览", command=self._select_file)
        btn_browse.grid(row=0, column=2, padx=5, pady=5)

        btn_load = ttk.Button(frame_file, text="加载数据", command=self._load_data)
        btn_load.grid(row=0, column=3, padx=5, pady=5)

        # 2. 功能操作区域
        frame_func = ttk.LabelFrame(self.root, text="核心功能操作", padding=(10, 5))
        frame_func.pack(fill="x", padx=10, pady=5)

        # 功能按钮：绘图、排序、求解、保存
        btn_plot = ttk.Button(frame_func, text="绘制散点图", command=self._plot_scatter)
        btn_plot.grid(row=0, column=0, padx=8, pady=8)

        btn_sort = ttk.Button(frame_func, text="按比值排序", command=self._sort_items)
        btn_sort.grid(row=0, column=1, padx=8, pady=8)

        btn_solve = ttk.Button(frame_func, text="求解最优解", command=self._solve_kp)
        btn_solve.grid(row=0, column=2, padx=8, pady=8)

        btn_save = ttk.Button(frame_func, text="保存结果", command=self._save_result)
        btn_save.grid(row=0, column=3, padx=8, pady=8)

        # 3. 结果显示区域（带滚动条）
        frame_result = ttk.LabelFrame(self.root, text="运行结果", padding=(10, 5))
        frame_result.pack(fill="both", expand=True, padx=10, pady=5)

        # 滚动条 + 文本框
        scrollbar = ttk.Scrollbar(frame_result, orient="vertical")
        self.result_text = tk.Text(
            frame_result,
            yscrollcommand=scrollbar.set,
            font=("Consolas", 10),  # 等宽字体，显示结果更整齐
            wrap=tk.WORD
        )
        scrollbar.config(command=self.result_text.yview)

        scrollbar.pack(side="right", fill="y")
        self.result_text.pack(side="left", fill="both", expand=True)

        # 初始化结果文本框
        self.result_text.insert(tk.END, "✅ 程序已启动，请先加载D{0-1}KP数据文件！\n")
        self.result_text.config(state=tk.NORMAL)

    def _select_file(self):
        """选择D{0-1}KP数据文件（txt格式）"""
        file_path = filedialog.askopenfilename(
            title="选择D{0-1}KP数据文件",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")],
            initialdir=src_dir  # 默认打开src目录，方便找到data文件夹
        )
        if file_path:
            self.file_path_var.set(file_path)

    def _load_data(self):
        """加载并解析数据文件"""
        try:
            file_path = self.file_path_var.get().strip()
            if not file_path:
                messagebox.showwarning("警告", "请先选择有效的数据文件路径！")
                return

            # 调用数据读取函数
            self.capacity, self.item_sets = read_d01kp_data(file_path)

            # 清空并显示加载结果
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"✅ 数据加载成功！\n")
            self.result_text.insert(tk.END, f"📦 背包最大载重：{self.capacity}\n")
            self.result_text.insert(tk.END, f"📊 项集总数：{len(self.item_sets)}\n")
            self.result_text.insert(tk.END, f"📝 第一个项集示例：{self.item_sets[0]}\n")

        except FileNotFoundError:
            messagebox.showerror("错误", f"文件不存在：{self.file_path_var.get()}")
        except ValueError as e:
            messagebox.showerror("错误", f"数据格式错误：{str(e)}")
        except Exception as e:
            messagebox.showerror("错误", f"数据加载失败：{str(e)}")

    def _plot_scatter(self):
        """绘制重量-价值散点图"""
        if not self.item_sets:
            messagebox.showwarning("警告", "请先加载有效数据！")
            return

        try:
            # 调用绘图函数（显示图形窗口）
            plot_scatter(self.item_sets)
            self.result_text.insert(tk.END, "\n✅ 散点图已成功绘制并显示！\n")
        except Exception as e:
            messagebox.showerror("错误", f"绘图失败：{str(e)}")

    def _sort_items(self):
        """按项集第三项的价值/重量比非递增排序"""
        if not self.item_sets:
            messagebox.showwarning("警告", "请先加载有效数据！")
            return

        try:
            sorted_items, index_map = sort_by_ratio(self.item_sets)

            # 显示排序结果
            self.result_text.insert(tk.END, "\n✅ 按第三项价值/重量比排序完成！\n")
            self.result_text.insert(tk.END, "📈 排序后前3个项集：\n")
            for i in range(min(3, len(sorted_items))):
                self.result_text.insert(tk.END, f"   项集{i}：{sorted_items[i]}\n")
        except Exception as e:
            messagebox.showerror("错误", f"排序失败：{str(e)}")

    def _solve_kp(self):
        """调用动态规划算法求解最优解"""
        if not self.item_sets:
            messagebox.showwarning("警告", "请先加载有效数据！")
            return

        try:
            # 初始化求解器并执行求解
            solver = D01KPAlgorithm(self.capacity, self.item_sets)
            self.solve_result = solver.solve()

            # 显示求解结果
            self.result_text.insert(tk.END, "\n🎯 最优解求解完成！\n")
            self.result_text.insert(tk.END, f"💰 最大价值：{self.solve_result['max_value']}\n")
            self.result_text.insert(tk.END, f"⚖️ 选中物品总重量：{self.solve_result['total_weight']}\n")
            self.result_text.insert(tk.END, f"⏱️ 求解耗时：{self.solve_result['cost_time']:.6f}秒\n")
            self.result_text.insert(tk.END, "📋 选中的物品列表：\n")
            for idx, (item_set_idx, item_idx) in enumerate(self.solve_result['selected_items']):
                w, v = self.item_sets[item_set_idx][item_idx]
                self.result_text.insert(tk.END,
                                        f"   第{idx + 1}个：项集{item_set_idx} - 物品{item_idx}（重量{w}，价值{v}）\n")

        except Exception as e:
            messagebox.showerror("错误", f"求解失败：{str(e)}")

    def _save_result(self):
        """保存求解结果到文件（TXT/Excel）"""
        if not self.solve_result:
            messagebox.showwarning("警告", "请先求解得到最优解！")
            return

        try:
            # 选择保存格式
            save_type = messagebox.askquestion(
                "保存格式选择",
                "请选择保存格式：\n【是】- Excel文件（.xlsx）\n【否】- 文本文件（.txt）"
            )

            # 选择保存路径
            if save_type == "yes":
                file_path = filedialog.asksaveasfilename(
                    title="保存Excel结果",
                    defaultextension=".xlsx",
                    filetypes=[("Excel文件", "*.xlsx"), ("所有文件", "*.*")],
                    initialfile="d01kp_result"
                )
                if file_path:
                    save_to_excel(self.solve_result, file_path)
            else:
                file_path = filedialog.asksaveasfilename(
                    title="保存TXT结果",
                    defaultextension=".txt",
                    filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")],
                    initialfile="d01kp_result"
                )
                if file_path:
                    save_to_txt(self.solve_result, file_path)

            if file_path:
                self.result_text.insert(tk.END, f"\n✅ 结果已保存至：{file_path}\n")

        except Exception as e:
            messagebox.showerror("错误", f"保存失败：{str(e)}")


# ===================== 防止直接运行该模块时的报错 =====================
if __name__ == "__main__":
    # 提示用户运行main.py，而非直接运行该文件
    messagebox.showinfo("提示", "请运行src目录下的main.py文件启动程序！")
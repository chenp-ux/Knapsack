# -*- coding: utf-8 -*-
"""
D{0-1}KP背包问题求解器 - 程序入口
"""
import tkinter as tk
from ui.main_ui import D01KPUI

if __name__ == "__main__":
    # 初始化主窗口并启动界面
    root = tk.Tk()
    app = D01KPUI(root)
    root.mainloop()
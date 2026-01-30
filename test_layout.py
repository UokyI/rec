#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
布局测试脚本
用于快速测试界面布局调整效果
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from ui.gui import ModernGUI

def test_layout():
    """测试布局效果"""
    root = tk.Tk()
    
    # 创建GUI实例
    app = ModernGUI(root)
    
    # 打印窗口信息用于调试
    print(f"窗口尺寸: {root.winfo_width()} x {root.winfo_height()}")
    print(f"窗口位置: {root.winfo_x()}, {root.winfo_y()}")
    
    # 5秒后自动关闭用于测试
    def auto_close():
        print("测试完成，自动关闭窗口")
        root.destroy()
    
    root.after(5000, auto_close)  # 5秒后关闭
    
    # 启动主循环
    root.mainloop()

if __name__ == "__main__":
    test_layout()
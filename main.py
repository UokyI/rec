#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
扬声器录制工具 Pro - 主入口文件
=================================

这是一个基于 Python 的图形界面应用程序，用于录制计算机扬声器播放的声音。

作者: uokyi
版本: 2.0.0
日期: 2026-01-30
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from ui.gui import ModernGUI
except ImportError as e:
    print(f"导入模块失败: {e}")
    print("请确保所有依赖模块都已正确安装")
    sys.exit(1)


def setup_high_dpi():
    """设置高DPI支持"""
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass


def main():
    """主函数 - 程序入口点"""
    
    # 设置高DPI支持
    setup_high_dpi()
    
    try:
        # 创建主窗口
        root = tk.Tk()
        
        # 设置窗口图标（如果有的话）
        try:
            # 可以在这里添加自定义图标
            # root.iconbitmap('icon.ico')
            pass
        except:
            pass
        
        # 创建GUI应用
        app = ModernGUI(root)
        
        # 启动主循环
        root.mainloop()
        
    except Exception as e:
        # 处理未捕获的异常
        error_msg = f"程序运行时发生错误:\n{str(e)}\n\n请检查您的系统配置和依赖项。"
        print(error_msg)
        
        # 如果GUI已经初始化，显示错误对话框
        try:
            messagebox.showerror("严重错误", error_msg)
        except:
            pass
            
        sys.exit(1)


if __name__ == "__main__":
    main()
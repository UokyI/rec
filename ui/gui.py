"""
图形用户界面模块
负责创建和管理GUI界面
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
from typing import Optional
from core.recorder import AudioRecorder


class ModernGUI:
    """现代化GUI界面类"""
    
    def __init__(self, master: tk.Tk):
        self.master = master
        self.recorder = AudioRecorder()
        
        # UI状态变量
        self.recording = False
        self.output_file: Optional[str] = None
        self.topmost_var = tk.BooleanVar(value=True)  # 提前初始化
        
        self.setup_window()
        self.setup_styles()
        self.create_widgets()
        self.setup_layout()
    
    def setup_window(self):
        """设置窗口属性"""
        self.master.title("🎧 扬声器录制工具 Pro")
        self.master.geometry("540x540")  # 进一步增加窗口尺寸
        self.master.minsize(540, 540)    # 设置最小尺寸
        self.master.resizable(True, True)  # 允许调整大小
        # 窗口置顶默认开启
        self.master.attributes('-topmost', True)
    
    def setup_styles(self):
        """设置界面样式"""
        self.style = ttk.Style()
        
        # 设置主题
        try:
            self.style.theme_use('clam')
        except:
            pass
            
        # 自定义样式
        self.style.configure('Title.TLabel', font=('微软雅黑', 14, 'bold'), foreground='#2c3e50')
        self.style.configure('Header.TLabel', font=('微软雅黑', 10, 'bold'), foreground='#34495e')
        self.style.configure('Status.TLabel', font=('微软雅黑', 9), foreground='#7f8c8d')
        self.style.configure('Time.TLabel', font=('Consolas', 10, 'bold'), foreground='#e74c3c')
        
        # 按钮样式
        self.style.configure('Record.TButton', font=('微软雅黑', 10, 'bold'), padding=10)
        self.style.configure('Stop.TButton', font=('微软雅黑', 10, 'bold'), padding=10)
        self.style.map('Record.TButton', 
                      background=[('active', '#27ae60'), ('!active', '#2ecc71')],
                      foreground=[('active', 'white'), ('!active', 'white')])
        self.style.map('Stop.TButton',
                      background=[('active', '#c0392b'), ('!active', '#e74c3c')],
                      foreground=[('active', 'white'), ('!active', 'white')])
        
        # 进度条样式
        self.style.configure('Recording.Horizontal.TProgressbar', 
                           troughcolor='#ecf0f1',
                           background='#e74c3c',
                           thickness=20)
    
    def create_widgets(self):
        """创建界面元素"""
        # 创建菜单栏
        self.create_menu_bar()
        
        # 主容器
        self.main_container = ttk.Frame(self.master)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # 各个区域
        self.create_title_section()
        self.create_device_section()
        self.create_settings_section()
        self.create_control_section()
        self.create_status_section()
        self.create_file_section()
    
    def create_menu_bar(self):
        """创建顶部菜单栏"""
        # 创建菜单栏
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)
        
        # 文件菜单
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="文件", menu=file_menu)
        file_menu.add_command(label="选择保存位置", command=self.select_save_location)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.master.quit)
        
        # 视图菜单
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="视图", menu=view_menu)
        # 使用已初始化的topmost_var变量
        view_menu.add_checkbutton(label="窗口置顶", 
                                 variable=self.topmost_var,
                                 command=self.toggle_topmost)
        
        # 帮助菜单
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="帮助", menu=help_menu)
        help_menu.add_command(label="关于", command=self.show_about)
    
    def create_title_section(self):
        """创建标题区域"""
        title_frame = ttk.Frame(self.main_container)
        title_frame.pack(fill=tk.X, pady=(0, 25))  # 增加底部间距
        
        # 标题
        title_label = ttk.Label(title_frame, text="🎧 扬声器录制工具 Pro", 
                               style='Title.TLabel')
        title_label.pack()
        
        # 副标题
        subtitle_label = ttk.Label(title_frame, 
                                  text="录制系统音频输出 • 高质量音频捕获",
                                  style='Status.TLabel')
        subtitle_label.pack(pady=(8, 0))  # 增加上边距
    
    def create_device_section(self):
        """创建设备信息区域"""
        device_frame = ttk.LabelFrame(self.main_container, text="🔊 设备信息", 
                                     padding="18")  # 增加内边距
        device_frame.pack(fill=tk.X, pady=(0, 20))  # 调整间距
        
        # 设备详情
        info_frame = ttk.Frame(device_frame)
        info_frame.pack(fill=tk.X)
        
        # 设备名称
        name_frame = ttk.Frame(info_frame)
        name_frame.pack(fill=tk.X, pady=3)  # 增加垂直间距
        ttk.Label(name_frame, text="设备名称:", style='Header.TLabel').pack(side=tk.LEFT)
        device_info = self.recorder.get_device_info()
        ttk.Label(name_frame, text=f" {device_info['name']}", 
                 style='Status.TLabel').pack(side=tk.LEFT)
        
        # 通道数
        channel_frame = ttk.Frame(info_frame)
        channel_frame.pack(fill=tk.X, pady=3)  # 增加垂直间距
        ttk.Label(channel_frame, text="最大通道数:", style='Header.TLabel').pack(side=tk.LEFT)
        ttk.Label(channel_frame, text=f" {device_info['channels']}", 
                 style='Status.TLabel').pack(side=tk.LEFT)
    
    def create_settings_section(self):
        """创建录制设置区域"""
        settings_frame = ttk.LabelFrame(self.main_container, text="⚙️ 录制设置", 
                                       padding="18")  # 增加内边距
        settings_frame.pack(fill=tk.X, pady=(0, 20))  # 调整间距
        
        # 采样率选择
        rate_frame = ttk.Frame(settings_frame)
        rate_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(rate_frame, text="采样率:", style='Header.TLabel').pack(side=tk.LEFT)
        supported_rates = self.recorder.detect_supported_rates()
        self.rate_var = tk.StringVar(value=str(supported_rates[0]) if supported_rates else "48000")
        self.rate_combo = ttk.Combobox(rate_frame, textvariable=self.rate_var, 
                                      values=[str(rate) for rate in supported_rates],
                                      state="readonly", width=12, font=('微软雅黑', 9))
        self.rate_combo.pack(side=tk.LEFT, padx=(10, 0))
        
        # 单位标签
        ttk.Label(rate_frame, text="Hz", style='Status.TLabel').pack(side=tk.LEFT, padx=(5, 0))
        
        # 注意：窗口置顶选项已移动到菜单栏
    
    def create_control_section(self):
        """创建控制按钮区域"""
        control_frame = ttk.Frame(self.main_container)
        control_frame.pack(fill=tk.X, pady=(0, 20))  # 增加底部间距
        
        # 按钮容器
        button_container = ttk.Frame(control_frame)
        button_container.pack(expand=True)
        
        # 开始录制按钮
        self.start_button = ttk.Button(button_container, text="● 开始录制", 
                                      command=self.start_recording,
                                      style='Record.TButton')
        self.start_button.pack(side=tk.LEFT, padx=(0, 15))  # 增加按钮间距
        
        # 结束录制按钮
        self.stop_button = ttk.Button(button_container, text="⏹ 结束录制", 
                                     command=self.stop_recording, 
                                     state=tk.DISABLED,
                                     style='Stop.TButton')
        self.stop_button.pack(side=tk.LEFT)
    
    def create_status_section(self):
        """创建状态和进度区域"""
        status_frame = ttk.LabelFrame(self.main_container, text="📊 录制状态", 
                                     padding="18")  # 增加内边距
        status_frame.pack(fill=tk.X, pady=(0, 20))  # 调整间距
        
        # 状态显示
        status_row = ttk.Frame(status_frame)
        status_row.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(status_row, text="状态:", style='Header.TLabel').pack(side=tk.LEFT)
        self.status_var = tk.StringVar(value="🟢 就绪")
        self.status_label = ttk.Label(status_row, textvariable=self.status_var,
                                     style='Status.TLabel')
        self.status_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # 进度显示
        progress_row = ttk.Frame(status_frame)
        progress_row.pack(fill=tk.X)
        
        ttk.Label(progress_row, text="时长:", style='Header.TLabel').pack(side=tk.LEFT)
        self.progress_var = tk.StringVar(value="00:00:00")
        self.progress_label = ttk.Label(progress_row, textvariable=self.progress_var,
                                       style='Time.TLabel')
        self.progress_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # 进度条
        self.progress_bar = ttk.Progressbar(status_frame, mode='indeterminate',
                                          style='Recording.Horizontal.TProgressbar')
        self.progress_bar.pack(fill=tk.X, pady=(10, 0))
    
    def create_file_section(self):
        """创建文件操作区域"""
        file_frame = ttk.LabelFrame(self.main_container, text="📁 文件保存", 
                                   padding="18")  # 增加内边距
        file_frame.pack(fill=tk.X)
        
        # 文件选择按钮
        button_row = ttk.Frame(file_frame)
        button_row.pack(fill=tk.X, pady=(0, 15))  # 增加底部间距
        
        ttk.Button(button_row, text="📂 选择保存位置", 
                  command=self.select_save_location).pack(side=tk.LEFT)
        
        # 文件路径显示
        path_frame = ttk.Frame(file_frame)
        path_frame.pack(fill=tk.X)
        
        ttk.Label(path_frame, text="保存路径:", style='Header.TLabel').pack(anchor=tk.W)
        self.file_var = tk.StringVar(value="自动生成 (程序目录)")
        file_path_label = ttk.Label(path_frame, textvariable=self.file_var,
                                   style='Status.TLabel', wraplength=320)  # 增加换行宽度
        file_path_label.pack(anchor=tk.W, pady=(8, 0))  # 增加上边距
    
    def setup_layout(self):
        """设置布局权重"""
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
    
    def toggle_topmost(self):
        """切换窗口置顶状态"""
        self.master.attributes('-topmost', self.topmost_var.get())
    
    def select_save_location(self):
        """选择保存位置"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".wav",
            filetypes=[("WAV files", "*.wav"), ("All files", "*.*")],
            title="选择保存位置"
        )
        if file_path:
            self.output_file = file_path
            self.recorder.set_output_file(file_path)
            self.file_var.set(os.path.basename(file_path))
    
    def start_recording(self):
        """开始录制"""
        if not self.recording:
            try:
                samplerate = int(self.rate_var.get())
                self.recording = True
                self.update_ui_state()
                
                # 设置输出文件
                if self.output_file:
                    self.recorder.set_output_file(self.output_file)
                
                # 开始录制
                success = self.recorder.start_recording(samplerate, self.update_progress)
                if not success:
                    raise RuntimeError("无法开始录制")
                    
            except Exception as e:
                self.recording = False
                self.update_ui_state()
                messagebox.showerror("错误", f"开始录制失败: {e}")
    
    def stop_recording(self):
        """结束录制"""
        if self.recording:
            try:
                success = self.recorder.stop_recording()
                if success:
                    self.recording = False
                    self.update_ui_state()
            except Exception as e:
                messagebox.showerror("错误", f"停止录制失败: {e}")
    
    def update_progress(self, elapsed_seconds: float):
        """更新录制进度显示"""
        if self.recording:
            # 更新时间显示
            hours = int(elapsed_seconds // 3600)
            minutes = int((elapsed_seconds % 3600) // 60)
            seconds = int(elapsed_seconds % 60)
            self.progress_var.set(f"{hours:02d}:{minutes:02d}:{seconds:02d}")
            
            # 更新状态显示
            self.status_var.set("🔴 正在录制...")
    
    def update_ui_state(self):
        """更新界面状态"""
        if self.recording:
            self.status_var.set("🔴 正在录制...")
            self.progress_bar.start(10)
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.rate_combo.config(state=tk.DISABLED)
            self.topmost_check.config(state=tk.DISABLED)
        else:
            self.status_var.set("🟢 就绪")
            self.progress_bar.stop()
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.rate_combo.config(state="readonly")
            self.topmost_check.config(state=tk.NORMAL)
            # 重置状态显示
            self.progress_var.set("00:00:00")
            
            # 显示保存完成消息
            if hasattr(self.recorder, '_last_saved_file'):
                file_path = getattr(self.recorder, '_last_saved_file', '')
                if file_path:
                    file_size = os.path.getsize(file_path) // 1024
                    messagebox.showinfo("🎉 完成", 
                                      f"文件已成功保存为:\n{file_path}\n\n文件大小: {file_size} KB")
    
    def show_about(self):
        """显示关于对话框"""
        about_text = """🎧 扬声器录制工具 Pro v2.0.0

一款现代化的系统音频录制工具，
支持录制计算机扬声器输出的声音。

主要功能：
• 录制系统扬声器音频输出
• 实时显示录制时长和状态
• 支持多种采样率选择
• 自动生成时间戳文件名
• 美观的现代化界面设计

作者：uokyi

"""
        messagebox.showinfo("关于", about_text)

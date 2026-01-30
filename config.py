"""
项目配置文件
包含应用程序的各种配置参数
"""

import os

# 应用程序基本信息
APP_NAME = "扬声器录制工具 Pro"
APP_VERSION = "2.0.0"
APP_AUTHOR = "uokyi"

# 窗口配置
WINDOW_CONFIG = {
    'title': APP_NAME,
    'geometry': '500x420',
    'resizable': False,
    'topmost': True
}

# 音频配置
AUDIO_CONFIG = {
    'default_samplerate': 48000,
    'supported_samplerates': [
        8000, 11025, 16000, 22050, 32000, 44100, 48000,
        88200, 96000, 176400, 192000, 352800, 384000
    ],
    'default_channels': 2,
    'blocksize_factor': 1  # 块大小因子（秒）
}

# 文件配置
FILE_CONFIG = {
    'default_extension': '.wav',
    'timestamp_format': '%Y%m%d_%H%M%S',
    'filename_prefix': 'speaker_recording',
    'supported_formats': [
        ('WAV files', '*.wav'),
        ('All files', '*.*')
    ]
}

# UI配置
UI_CONFIG = {
    'themes': ['clam', 'alt', 'default'],
    'fonts': {
        'title': ('微软雅黑', 14, 'bold'),
        'header': ('微软雅黑', 10, 'bold'),
        'normal': ('微软雅黑', 9),
        'monospace': ('Consolas', 10, 'bold')
    },
    'colors': {
        'primary': '#2c3e50',
        'secondary': '#34495e',
        'success': '#27ae60',
        'danger': '#e74c3c',
        'warning': '#f39c12',
        'info': '#3498db',
        'light': '#ecf0f1',
        'dark': '#2c3e50'
    }
}

# 路径配置
PATH_CONFIG = {
    'root_dir': os.path.dirname(os.path.abspath(__file__)),
    'temp_dir': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp'),
    'logs_dir': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
}

# 日志配置
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'date_format': '%Y-%m-%d %H:%M:%S'
}
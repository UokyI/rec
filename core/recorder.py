"""
音频录制核心模块
负责音频设备检测、录制和保存功能
"""

import soundcard as sc
import sounddevice as sd
import numpy as np
import wave
import datetime
import threading
from typing import List, Optional, Callable


class AudioRecorder:
    """音频录制器核心类"""
    
    def __init__(self):
        self.recording = False
        self.record_thread = None
        self.recorded_data: List[np.ndarray] = []
        self.output_file: Optional[str] = None
        self.start_time: Optional[datetime.datetime] = None
        self.speaker = None
        self.speaker_name = ""
        self.channels = 0
        
        # 初始化音频设备
        self._initialize_audio_device()
    
    def _initialize_audio_device(self):
        """初始化音频设备"""
        try:
            self.speaker = sc.default_speaker()
            self.speaker_name = self.speaker.name
            self.channels = min(2, self.speaker.channels)
        except Exception as e:
            raise RuntimeError(f"无法获取默认扬声器: {e}")
    
    def detect_supported_rates(self) -> List[int]:
        """检测支持的采样率"""
        try:
            # 获取默认音频设备信息
            devices = sd.query_devices()
            default_device_idx = sd.default.device[1]  # 默认输出设备索引
            default_device = devices[default_device_idx]
            
            # 获取通道数
            channels = default_device['max_output_channels']
            
            # 常见的采样率列表
            common_rates = [8000, 11025, 16000, 22050, 32000, 44100, 48000, 
                          88200, 96000, 176400, 192000, 352800, 384000]
            
            # 检查设备支持的采样率
            supported_samplerates = []
            for rate in common_rates:
                try:
                    sd.check_output_settings(device=default_device_idx, 
                                           samplerate=rate, 
                                           channels=min(channels, 2))
                    supported_samplerates.append(rate)
                except Exception:
                    # 不支持的采样率
                    pass
                    
            return supported_samplerates if supported_samplerates else [44100, 48000]
        except Exception:
            # 出现异常时返回默认值
            return [44100, 48000]
    
    def start_recording(self, samplerate: int, callback: Optional[Callable] = None):
        """开始录制"""
        if self.recording:
            return False
            
        self.recording = True
        self.recorded_data = []
        self.start_time = datetime.datetime.now()
        
        # 在新线程中开始录制
        self.record_thread = threading.Thread(
            target=self._record_audio, 
            args=(samplerate, callback),
            daemon=True
        )
        self.record_thread.start()
        return True
    
    def stop_recording(self):
        """结束录制"""
        if not self.recording:
            return False
            
        self.recording = False
        return True
    
    def _record_audio(self, samplerate: int, callback: Optional[Callable]):
        """在独立线程中录制音频"""
        try:
            blocksize = samplerate  # 1秒的块大小
            
            # 获取回放设备的麦克风接口
            microphone = sc.get_microphone(id=str(self.speaker_name), include_loopback=True)
            
            with microphone.recorder(samplerate=samplerate, blocksize=blocksize, channels=self.channels) as recorder:
                while self.recording:
                    data = recorder.record(numframes=blocksize)
                    self.recorded_data.append(data.copy())
                    
                    # 调用回调函数更新UI（如果有）
                    if callback:
                        elapsed = (datetime.datetime.now() - self.start_time).total_seconds()
                        callback(elapsed)
                    
            # 保存录制的数据
            if self.recorded_data and not self.recording:  # 确保是正常停止
                self._save_recording(samplerate)
                
        except Exception as e:
            self.recording = False
            raise RuntimeError(f"录制过程中出现错误: {e}")
    
    def _save_recording(self, samplerate: int):
        """保存录制的音频"""
        try:
            # 生成文件名
            if not self.output_file:
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                output_file = f"speaker_recording_{timestamp}.wav"
            else:
                output_file = self.output_file
                
            # 合并所有数据
            full_data = np.concatenate(self.recorded_data, axis=0)
            
            # 转换数据格式
            if full_data.dtype == np.float64:
                audio_data = (full_data * np.iinfo(np.int16).max).astype(np.int16)
            elif full_data.dtype == np.float32:
                audio_data = (full_data * 32767).astype(np.int16)
            else:
                audio_data = full_data.astype(np.int16)
            
            # 保存为WAV文件
            with wave.open(output_file, 'wb') as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(2)
                wf.setframerate(samplerate)
                wf.writeframes(audio_data.tobytes())
                
            return output_file
            
        except Exception as e:
            raise RuntimeError(f"保存文件时出现错误: {e}")
        finally:
            # 清理临时变量
            self.recorded_data = []
            self.output_file = None
            self.start_time = None
    
    def set_output_file(self, filepath: str):
        """设置输出文件路径"""
        self.output_file = filepath
    
    def get_device_info(self) -> dict:
        """获取设备信息"""
        return {
            'name': self.speaker_name,
            'channels': self.channels,
            'is_recording': self.recording
        }
    
    def get_elapsed_time(self) -> float:
        """获取已录制时长（秒）"""
        if self.start_time and self.recording:
            return (datetime.datetime.now() - self.start_time).total_seconds()
        return 0.0
    
    @property
    def is_recording(self) -> bool:
        """是否正在录制"""
        return self.recording
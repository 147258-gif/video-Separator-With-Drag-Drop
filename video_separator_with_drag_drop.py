import os
import subprocess
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES
import threading
import time
import sys
import platform
import winsound  # Windows系统提示音

# 全局变量
log_content = ""
is_processing = False
stop_event = threading.Event()

class ProcessController:
    def __init__(self):
        self.process = None
        self.is_running = False

    def terminate(self):
        if self.process and self.is_running:
            self.process.terminate()
            self.is_running = False

controller = ProcessController()

def check_ffmpeg():
    try:
        subprocess.run(["ffmpeg", "-version"], check=True,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def run_command(command, use_gpu=False, progress_callback=None):
    global log_content
    flags = subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
    
    if use_gpu:
        command[1:1] = ["-hwaccel", "cuda", "-hwaccel_output_format", "cuda"]

    controller.is_running = True
    try:
        controller.process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            encoding="utf-8",
            errors="replace",
            creationflags=flags
        )

        duration = None
        for line in controller.process.stdout:
            if stop_event.is_set():
                controller.terminate()
                break
            
            if "Duration" in line:
                duration_str = line.split("Duration:")[1].split(",")[0].strip()
                h, m, s = duration_str.split(':')
                duration = int(h)*3600 + int(m)*60 + float(s)
            
            if "time=" in line and duration:
                time_str = line.split("time=")[1].split(" ")[0]
                h, m, s = time_str.split(':')
                current_time = int(h)*3600 + int(m)*60 + float(s)
                progress = (current_time / duration) * 100
                if progress_callback:
                    progress_callback(min(progress, 100))

        controller.process.wait()
        if controller.process.returncode == 0:
            log_content += f"成功：{' '.join(command)}\n"
        else:
            log_content += f"失败：{' '.join(command)}\n"

    except Exception as e:
        log_content += f"错误：{str(e)}\n"
    finally:
        controller.is_running = False

def separate_streams(input_files, output_dir, audio_format, video_format, use_gpu, progress_var, progress_label):
    global is_processing
    is_processing = True
    total_files = len(input_files)
    
    for idx, file in enumerate(input_files):
        if stop_event.is_set():
            break
            
        base_name = os.path.splitext(os.path.basename(file))[0]
        output_audio = os.path.join(output_dir, f"{base_name}_audio.{audio_format.lower()}")
        output_video = os.path.join(output_dir, f"{base_name}_video.{video_format.lower()}")

        try:
            # 音频处理
            if audio_format != "不分离音频":
                audio_cmd = ["ffmpeg", "-i", file, "-vn"]
                if audio_format == "MP3":
                    audio_cmd += ["-acodec", "libmp3lame", "-q:a", "2"]
                elif audio_format == "WAV":
                    audio_cmd += ["-acodec", "pcm_s16le"]
                audio_cmd += [output_audio]
                
                run_command(audio_cmd, use_gpu, 
                           lambda p: progress_var.set(p * 0.5 * (idx+1)/total_files))

            # 视频处理
            if video_format != "不分离视频":
                video_cmd = ["ffmpeg", "-i", file, "-an", "-vcodec", "copy", output_video]
                run_command(video_cmd, use_gpu,
                           lambda p: progress_var.set((50 + p * 0.5) * (idx+1)/total_files))

        except Exception as e:
            log_content += f"文件 {file} 处理失败：{str(e)}\n"

    if not stop_event.is_set():
        play_sound()
        if platform.system() == 'Windows':
            os.startfile(output_dir)
        elif platform.system() == 'Darwin':
            subprocess.Popen(['open', output_dir])
        else:
            subprocess.Popen(['xdg-open', output_dir])
    
    is_processing = False
    stop_event.clear()

def play_sound():
    if platform.system() == 'Windows':
        winsound.MessageBeep()
    else:
        print('\a')

def browse_output():
    path = filedialog.askdirectory()
    if path:
        output_dir_var.set(path)

def validate_files(file_list):
    valid_extensions = ('.mp4', '.mkv', '.avi', '.mov')
    return [f for f in file_list if f.lower().endswith(valid_extensions)]

def start_processing():
    if not check_ffmpeg():
        messagebox.showerror("错误", "未找到ffmpeg，请先安装并添加到环境变量！")
        return

    input_files = input_file_var.get().split(';') if ';' in input_file_var.get() else [input_file_var.get()]
    input_files = validate_files(input_files)
    
    if not input_files:
        messagebox.showwarning("警告", "请选择有效的视频文件！")
        return

    output_dir = output_dir_var.get() or os.path.dirname(input_files[0])
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    selected_audio = audio_format_var.get()
    selected_video = video_format_var.get()
    
    if selected_audio == "不分离音频" and selected_video == "不分离视频":
        messagebox.showwarning("警告", "请选择至少分离音频或视频！")
        return

    progress_var.set(0)
    thread = threading.Thread(target=separate_streams, args=(
        input_files, output_dir, selected_audio, selected_video,
        gpu_var.get() == "使用 GPU", progress_var, progress_label
    ))
    thread.start()

def cancel_processing():
    stop_event.set()
    controller.terminate()
    progress_var.set(0)
    progress_label.config(text="已取消")

def on_drop(event):
    files = event.data.split(';') if ';' in event.data else [event.data]
    valid_files = validate_files(files)
    if valid_files:
        input_file_var.set(';'.join(valid_files))
    else:
        messagebox.showwarning("无效文件", "仅支持以下格式：\n.mp4, .mkv, .avi, .mov")

# GUI界面更新
root = TkinterDnD.Tk()
root.title("增强版音视频分离工具")

# 样式配置
style = ttk.Style()
style.configure('TCombobox', padding=5)
style.configure('TButton', padding=5)
style.map('TButton', background=[('active', '#45a049')])

# 布局框架
main_frame = ttk.Frame(root, padding=20)
main_frame.pack(fill='both', expand=True)

# 输入文件部分
ttk.Label(main_frame, text="输入文件:").grid(row=0, column=0, sticky='w')
input_file_var = tk.StringVar()
ttk.Entry(main_frame, textvariable=input_file_var, width=50).grid(row=0, column=1)
ttk.Button(main_frame, text="添加文件", command=lambda: input_file_var.set(
    ';'.join(filedialog.askopenfilenames(filetypes=[("视频文件", "*.mp4;*.mkv;*.avi;*.mov")]))
)).grid(row=0, column=2)

# 输出目录部分
ttk.Label(main_frame, text="输出目录:").grid(row=1, column=0, sticky='w')
output_dir_var = tk.StringVar()
ttk.Entry(main_frame, textvariable=output_dir_var, width=50).grid(row=1, column=1)
ttk.Button(main_frame, text="浏览...", command=browse_output).grid(row=1, column=2)

# 格式选择
ttk.Label(main_frame, text="音频格式:").grid(row=2, column=0, sticky='w')
audio_format_var = tk.StringVar(value="MP3")
ttk.Combobox(main_frame, textvariable=audio_format_var, 
            values=["MP3", "WAV", "AAC", "不分离音频"], state="readonly").grid(row=2, column=1, sticky='w')

ttk.Label(main_frame, text="视频格式:").grid(row=3, column=0, sticky='w')
video_format_var = tk.StringVar(value="MP4")
ttk.Combobox(main_frame, textvariable=video_format_var, 
            values=["MP4", "MKV", "AVI", "不分离视频"], state="readonly").grid(row=3, column=1, sticky='w')

# GPU选择
ttk.Label(main_frame, text="硬件加速:").grid(row=4, column=0, sticky='w')
gpu_var = tk.StringVar(value="使用 CPU")
ttk.Combobox(main_frame, textvariable=gpu_var, 
            values=["使用 CPU", "使用 GPU"], state="readonly").grid(row=4, column=1, sticky='w')

# 进度条
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(main_frame, variable=progress_var, maximum=100)
progress_bar.grid(row=5, column=0, columnspan=3, pady=10, sticky='ew')

progress_label = ttk.Label(main_frame, text="准备就绪")
progress_label.grid(row=6, column=0, columnspan=3)

# 按钮组
btn_frame = ttk.Frame(main_frame)
btn_frame.grid(row=7, column=0, columnspan=3, pady=10)

ttk.Button(btn_frame, text="开始处理", command=start_processing).pack(side='left', padx=5)
ttk.Button(btn_frame, text="停止处理", command=cancel_processing).pack(side='left', padx=5)
ttk.Button(btn_frame, text="查看日志", command=show_log_window).pack(side='left', padx=5)
ttk.Button(btn_frame, text="作者信息", command=show_author_info).pack(side='left', padx=5)

# 拖放功能
root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', on_drop)

# 初始化检查
if not check_ffmpeg():
    messagebox.showerror("环境错误", "未检测到FFmpeg，请先安装！")
    sys.exit()

root.mainloop()
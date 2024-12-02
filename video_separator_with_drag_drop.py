import os
import subprocess
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES

def run_command(command):
    """
    执行外部命令，避免弹出额外窗口
    """
    flags = subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
    subprocess.run(command, check=True, creationflags=flags)

def update_progress(progress_var, progress_bar, start, end):
    """
    更新进度条的进度
    """
    for i in range(start, end + 1):
        progress_var.set(i)
        progress_bar.update()
        root.update_idletasks()
        progress_bar.after(30)  # 模拟任务耗时

def separate_audio_video(input_file, output_audio, output_video, progress_var, progress_bar, start_button, selected_audio_format, selected_video_format):
    """
    根据用户选择的格式分离音频和视频流
    """
    try:
        # 更新按钮状态为 "正在分离"
        start_button.config(text="正在分离", state=tk.DISABLED)
        
        # 更新进度条（分离音频开始）
        update_progress(progress_var, progress_bar, 0, 50)

        # 如果选择分离音频，执行音频分离
        if selected_audio_format != "不分离音频":
            run_command(["ffmpeg", "-i", input_file, "-vn", "-acodec", "libmp3lame", output_audio])

        # 更新进度条（分离视频开始）
        update_progress(progress_var, progress_bar, 51, 99)

        # 如果选择分离视频，执行视频分离
        if selected_video_format != "不分离视频":
            run_command(["ffmpeg", "-i", input_file, "-an", "-vcodec", "copy", output_video])

        # 更新进度条到完成
        progress_var.set(100)
        progress_bar.update()

        # 显示成功消息
        messagebox.showinfo("成功", f"分离完成！\n音频：{output_audio}\n视频：{output_video}")

    except subprocess.CalledProcessError as e:
        messagebox.showerror("错误", f"运行 FFmpeg 时出错：{e}")
        progress_var.set(0)
        progress_bar.update()
    finally:
        # 恢复按钮状态
        start_button.config(text="开始分离", state=tk.NORMAL)

def browse_file():
    """
    打开文件选择对话框
    """
    file_path = filedialog.askopenfilename(filetypes=[("视频文件", "*.mp4;*.mkv;*.avi")])
    if file_path:
        input_file_var.set(file_path)

def start_processing():
    """
    开始分离音频和视频
    """
    input_file = input_file_var.get()
    if not input_file:
        messagebox.showwarning("警告", "请选择一个输入文件！")
        return

    selected_audio_format = audio_format_var.get()
    selected_video_format = video_format_var.get()

    if selected_audio_format == "不分离音频" and selected_video_format == "不分离视频":
        messagebox.showwarning("警告", "请选择至少分离音频或视频！")
        return

    output_audio = os.path.splitext(input_file)[0] + "_audio." + selected_audio_format.lower()
    output_video = os.path.splitext(input_file)[0] + "_video." + selected_video_format.lower()

    # 清零进度条
    progress_var.set(0)
    progress_bar.update()

    # 开始分离任务
    separate_audio_video(input_file, output_audio, output_video, progress_var, progress_bar, start_button, selected_audio_format, selected_video_format)

def center_window(window, width, height):
    """
    将窗口居中显示
    """
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    # 计算居中位置
    position_top = int(screen_height / 2 - height / 2)
    position_right = int(screen_width / 2 - width / 2)
    
    # 设置窗口大小和位置
    window.geometry(f'{width}x{height}+{position_right}+{position_top}')

def on_drop(event):
    """
    处理文件拖放事件
    """
    file_path = event.data
    if file_path.endswith(('.mp4', '.mkv', '.avi')):  # 只允许视频文件
        input_file_var.set(file_path)
    else:
        messagebox.showwarning("无效文件", "请拖入一个有效的视频文件！")

def show_author_info():
    """
    显示作者信息
    """
    author_info = "作者: Leo Zivika\n开源地址: https://github.com/147258-gif/video_separator_with_drag_drop"
    messagebox.showinfo("作者信息", author_info)

# 创建主窗口
root = TkinterDnD.Tk()
root.title("音视频分离工具")

# 设置窗口大小和居中
window_width = 650
window_height = 450
center_window(root, window_width, window_height)

# 设置背景颜色
root.config(bg="#f2f2f2")

# 输入文件选择
input_file_var = tk.StringVar()
tk.Label(root, text="选择输入文件：", font=("Arial", 12), bg="#f2f2f2").grid(row=0, column=0, padx=20, pady=10, sticky="w")
tk.Entry(root, textvariable=input_file_var, width=40, font=("Arial", 12), relief="solid").grid(row=0, column=1, padx=20, pady=10)
tk.Button(root, text="浏览...", command=browse_file, bg="#4CAF50", fg="white", font=("Arial", 12), relief="flat").grid(row=0, column=2, padx=20, pady=10)

# 设置拖放事件
root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', on_drop)

# 拖拽提示标签
drag_drop_label = tk.Label(root, text="或将视频文件拖拽到这里", font=("Arial", 12, "italic"), fg="gray", bg="#f2f2f2")
drag_drop_label.grid(row=1, column=0, columnspan=3, pady=10)

# 音频格式选择
tk.Label(root, text="选择音频格式：", font=("Arial", 12), bg="#f2f2f2").grid(row=2, column=0, padx=20, pady=10, sticky="w")
audio_format_var = tk.StringVar(value="MP3")
audio_format_options = ["MP3", "WAV", "AAC", "不分离音频"]
audio_format_menu = ttk.Combobox(root, textvariable=audio_format_var, values=audio_format_options, state="readonly", font=("Arial", 12))
audio_format_menu.grid(row=2, column=1, padx=20, pady=10, sticky="w")

# 视频格式选择
tk.Label(root, text="选择视频格式：", font=("Arial", 12), bg="#f2f2f2").grid(row=3, column=0, padx=20, pady=10, sticky="w")
video_format_var = tk.StringVar(value="MP4")
video_format_options = ["MP4", "MKV", "AVI", "不分离视频"]
video_format_menu = ttk.Combobox(root, textvariable=video_format_var, values=video_format_options, state="readonly", font=("Arial", 12))
video_format_menu.grid(row=3, column=1, padx=20, pady=10, sticky="w")

# 进度条
progress_var = tk.IntVar()
progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate", variable=progress_var)
progress_bar.grid(row=4, column=0, columnspan=3, pady=20)

# 开始按钮
start_button = tk.Button(root, text="开始分离", command=start_processing, bg="#2196F3", fg="white", font=("Arial", 12), relief="flat")
start_button.grid(row=5, column=0, columnspan=3, pady=20)

# 作者按钮
author_button = tk.Button(root, text="作者", command=show_author_info, bg="#FF5722", fg="white", font=("Arial", 12), relief="flat")
author_button.grid(row=6, column=0, columnspan=3, pady=20)

# 启动主循环
root.mainloop()

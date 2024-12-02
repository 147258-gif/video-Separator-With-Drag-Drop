import os
import subprocess
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES
import threading

# 全局变量
log_content = ""  # 用于存储日志信息


def run_command(command, use_gpu=False):
    """
    执行外部命令，捕获输出，并解决编码问题，同时记录日志
    """
    global log_content  # 引用全局变量
    flags = subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
    if use_gpu:
        command.insert(1, "-hwaccel")
        command.insert(2, "cuda")

    try:
        result = subprocess.run(
            command,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding="utf-8",  # 强制使用 UTF-8 解码
            errors="replace",  # 遇到无法解码的字符时进行替换
            creationflags = flags
        )
        log_content += f"命令：{' '.join(command)}\n输出：{result.stdout}\n错误：{result.stderr}\n\n"
        return result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        log_content += f"命令：{' '.join(command)}\n失败：{e.stderr}\n\n"
        return e.stdout, e.stderr


def separate_audio_video(input_file, output_audio, output_video, progress_var, progress_bar, start_button,
                         selected_audio_format, selected_video_format, use_gpu):
    """
    分离音频和视频流，并处理 GPU 模式，同时记录日志
    """
    global log_content  # 引用全局变量
    try:
        start_button.config(text="正在分离", state=tk.DISABLED)

        # 更新进度条（分离音频）
        progress_var.set(0)
        progress_bar.update()

        # 分离音频
        if selected_audio_format != "不分离音频":
            audio_command = ["ffmpeg", "-i", input_file, "-vn", "-acodec", "libmp3lame", output_audio]
            run_command(audio_command, use_gpu)

        # 更新进度条（分离视频）
        progress_var.set(50)
        progress_bar.update()

        # 分离视频
        if selected_video_format != "不分离视频":
            video_command = ["ffmpeg", "-i", input_file, "-an", "-vcodec", "copy", output_video]
            run_command(video_command, use_gpu)

        progress_var.set(100)
        progress_bar.update()

        messagebox.showinfo("成功", f"分离完成！\n音频：{output_audio}\n视频：{output_video}")

    except Exception as e:
        log_content += f"错误：{str(e)}\n\n"
        messagebox.showerror("错误", f"处理时出错：{str(e)}")
    finally:
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
    开始处理任务
    """
    input_file = input_file_var.get()
    if not input_file:
        messagebox.showwarning("警告", "请选择一个输入文件！")
        return

    selected_audio_format = audio_format_var.get()
    selected_video_format = video_format_var.get()
    use_gpu = gpu_var.get() == "使用 GPU"

    if selected_audio_format == "不分离音频" and selected_video_format == "不分离视频":
        messagebox.showwarning("警告", "请选择至少分离音频或视频！")
        return

    output_audio = os.path.splitext(input_file)[0] + "_audio." + selected_audio_format.lower()
    output_video = os.path.splitext(input_file)[0] + "_video." + selected_video_format.lower()

    progress_var.set(0)
    progress_bar.update()

    thread = threading.Thread(target=separate_audio_video, args=(
        input_file, output_audio, output_video, progress_var, progress_bar, start_button,
        selected_audio_format, selected_video_format, use_gpu
    ))
    thread.start()


def center_window(window, width, height):
    """
    将窗口居中显示
    """
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    position_top = int(screen_height / 2 - height / 2)
    position_right = int(screen_width / 2 - width / 2)

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


def show_log_window():
    """
    显示日志的独立窗口
    """
    if not log_content.strip():
        messagebox.showinfo("日志", "暂无日志内容！")
        return

    log_window = tk.Toplevel(root)
    log_window.title("日志信息")
    log_window.geometry("600x400")

    text_area = tk.Text(log_window, wrap="word", font=("Arial", 10))
    text_area.insert("1.0", log_content)
    text_area.config(state="disabled")
    text_area.pack(expand=True, fill="both")

    scrollbar = ttk.Scrollbar(log_window, orient="vertical", command=text_area.yview)
    text_area.config(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")


# 创建主窗口
root = TkinterDnD.Tk()
root.title("音视频分离工具")

# 设置窗口大小和居中
window_width = 700
window_height = 500
center_window(root, window_width, window_height)

# 设置背景颜色
root.config(bg="#f2f2f2")

# 输入文件选择
input_file_var = tk.StringVar()
tk.Label(root, text="选择输入文件：", font=("Arial", 12), bg="#f2f2f2").grid(row=0, column=0, padx=20, pady=10,
                                                                            sticky="w")
tk.Entry(root, textvariable=input_file_var, width=40, font=("Arial", 12), relief="solid").grid(row=0, column=1, padx=20,
                                                                                               pady=10)
tk.Button(root, text="浏览...", command=browse_file, bg="#4CAF50", fg="white", font=("Arial", 12), relief="flat").grid(
    row=0, column=2, padx=20, pady=10)

# 设置拖放事件
root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', on_drop)

# 拖拽提示标签
drag_drop_label = tk.Label(root, text="或将视频文件拖拽到这里", font=("Arial", 12, "italic"), fg="gray", bg="#f2f2f2")
drag_drop_label.grid(row=1, column=0, columnspan=3, pady=10)

# 音频格式选择
tk.Label(root, text="选择音频格式：", font=("Arial", 12), bg="#f2f2f2").grid(row=2, column=0, padx=20, pady=10,
                                                                            sticky="w")
audio_format_var = tk.StringVar(value="MP3")
audio_format_options = ["MP3", "WAV", "AAC", "不分离音频"]
audio_format_menu = ttk.Combobox(root, textvariable=audio_format_var, values=audio_format_options, state="readonly",
                                 font=("Arial", 12))
audio_format_menu.grid(row=2, column=1, padx=20, pady=10, sticky="w")

# 视频格式选择
tk.Label(root, text="选择视频格式：", font=("Arial", 12), bg="#f2f2f2").grid(row=3, column=0, padx=20, pady=10,
                                                                            sticky="w")
video_format_var = tk.StringVar(value="MP4")
video_format_options = ["MP4", "MKV", "AVI", "不分离视频"]
video_format_menu = ttk.Combobox(root, textvariable=video_format_var, values=video_format_options, state="readonly",
                                 font=("Arial", 12))
video_format_menu.grid(row=3, column=1, padx=20, pady=10, sticky="w")

# GPU 选择
tk.Label(root, text="选择运行模式：", font=("Arial", 12), bg="#f2f2f2").grid(row=4, column=0, padx=20, pady=10,
                                                                            sticky="w")
gpu_var = tk.StringVar(value="使用 CPU")
gpu_options = ["使用 CPU", "使用 GPU"]
gpu_menu = ttk.Combobox(root, textvariable=gpu_var, values=gpu_options, state="readonly", font=("Arial", 12))
gpu_menu.grid(row=4, column=1, padx=20, pady=10, sticky="w")

# 进度条
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100)
progress_bar.grid(row=5, column=0, columnspan=3, pady=20, sticky="ew", padx=20)

# 开始分离按钮
start_button = tk.Button(root, text="开始分离", command=start_processing, bg="#2196F3", fg="white", font=("Arial", 14),
                         relief="flat")
start_button.grid(row=6, column=0, columnspan=3, pady=10)

# 查看日志按钮
log_button = tk.Button(root, text="查看日志", command=show_log_window, bg="#FFC107", fg="black", font=("Arial", 12),
                       relief="flat")
log_button.grid(row=7, column=0, columnspan=3, pady=10)

# 作者信息按钮
author_button = tk.Button(root, text="作者信息", command=show_author_info, bg="#795548", fg="white", font=("Arial", 12),
                          relief="flat")
author_button.grid(row=8, column=0, columnspan=3, pady=10)

# 主循环
root.mainloop()

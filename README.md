# 视频音频分离工具 / Video and Audio Separator Tool

[English Version](#english) | [中文版](#中文)

---

<a name="中文"></a>
## 中文版

### 简介
视频音频分离工具是一款基于 Python 和 FFmpeg 的桌面应用程序，支持从视频文件中分离音频流或视频流。通过简洁美观的图形界面，用户只需简单操作即可完成处理，支持文件拖拽功能，更加方便快捷。

---

### 功能特点
- **音频提取**：从视频文件中提取音频，支持保存为 MP3、WAV、AAC 等格式。
- **视频提取**：从视频文件中分离视频流，去除音频部分，支持 MP4、MKV、AVI 等格式。
- **文件拖拽支持**：可直接将视频文件拖拽到工具窗口，快速识别文件。
- **实时进度显示**：处理过程中显示分离进度。
- **简单易用**：图形界面直观，适合非技术用户使用。

---

### 使用方法

1. **运行程序**  
   下载并运行打包好的 `.exe` 文件，或者使用 Python 脚本直接运行。

2. **选择文件**  
   - 点击“浏览”按钮，选择视频文件。  
   - 或直接将视频文件拖拽到窗口。

3. **设置输出选项**  
   - 选择需要分离的内容（音频或视频）。  
   - 指定目标文件格式：  
     - 音频：MP3、WAV、AAC。  
     - 视频：MP4、MKV、AVI。

4. **开始处理**  
   点击“开始分离”，等待处理完成，工具会提示保存的文件路径。

---

### 系统要求
- **操作系统**：Windows 10 或更高版本  
- **运行环境**：Python 3.7 或更高版本  
- **必备组件**：  
  - FFmpeg（需添加到系统环境变量）  
  - 依赖库：  
    - tkinter  
    - tkinterdnd2  
    - ttkthemes  

---

### 安装与运行

#### 运行 Python 脚本
1. 安装依赖：
   ```bash
   pip install tkinterdnd2 ttkthemes
   ```
2. 确保 FFmpeg 已安装并配置到环境变量。
3. 执行脚本：
   ```bash
   python video_separator.py
   ```

#### 打包为可执行文件
1. 安装打包工具：
   ```bash
   pip install pyinstaller
   ```
2. 执行以下命令进行打包：
   ```bash
   pyinstaller --onefile --windowed --add-data "path_to_tkinterdnd2;tkinterdnd2" --icon=app_icon.ico video_separator.py
   ```
3. 打包完成后，生成的 `.exe` 文件在 `dist` 文件夹中。

---

### 开发者信息
- **作者**：Leo Zivika  
- **GitHub 开源地址**：[视频音频分离工具](https://github.com/147258-gif/video_separator_with_drag_drop)

---

### 许可证
本项目基于 MIT 许可证开源，详细内容请参阅 [LICENSE](LICENSE) 文件。

---

<a name="english"></a>
## English Version

### Overview
The Video and Audio Separator Tool is a desktop application built with Python and FFmpeg that allows users to separate audio streams or video streams from video files. With its simple and elegant graphical interface, users can process files effortlessly. It also supports drag-and-drop functionality for added convenience.

---

### Features
- **Audio Extraction**: Extract audio from video files and save it in formats such as MP3, WAV, or AAC.
- **Video Extraction**: Separate video streams from video files, removing audio streams, and save in formats like MP4, MKV, or AVI.
- **Drag-and-Drop Support**: Easily drag and drop video files into the tool's window for quick recognition.
- **Real-Time Progress Display**: Shows the progress of the separation process.
- **User-Friendly**: Intuitive graphical interface suitable for non-technical users.

---

### How to Use

1. **Run the Program**  
   Download and run the pre-built `.exe` file, or execute the Python script directly.

2. **Select a File**  
   - Click the "Browse" button to choose a video file.  
   - Alternatively, drag and drop a video file into the window.

3. **Set Output Options**  
   - Choose what to separate (audio or video).  
   - Specify the target file format:  
     - Audio: MP3, WAV, AAC.  
     - Video: MP4, MKV, AVI.

4. **Start Processing**  
   Click "Start Separation," wait for the process to complete, and the tool will notify you of the saved file's location.

---

### System Requirements
- **Operating System**: Windows 10 or later  
- **Environment**: Python 3.7 or higher  
- **Required Components**:  
  - FFmpeg (must be added to the system PATH)  
  - Dependencies:  
    - tkinter  
    - tkinterdnd2  
    - ttkthemes  

---

### Installation and Execution

#### Run the Python Script
1. Install dependencies:
   ```bash
   pip install tkinterdnd2 ttkthemes
   ```
2. Ensure FFmpeg is installed and added to the system PATH.
3. Execute the script:
   ```bash
   python video_separator.py
   ```

#### Package into an Executable File
1. Install the packaging tool:
   ```bash
   pip install pyinstaller
   ```
2. Use the following command to package the script:
   ```bash
   pyinstaller --onefile --windowed --add-data "path_to_tkinterdnd2;tkinterdnd2" --icon=app_icon.ico video_separator.py
   ```
3. The packaged `.exe` file will be located in the `dist` folder.

---

### Developer Information
- **Author**: Leo Zivika  
- **GitHub Repository**: [Video and Audio Separator Tool](https://github.com/147258-gif/video_separator_with_drag_drop)

---

### License
This project is open-sourced under the MIT License. For more details, refer to the [LICENSE](LICENSE) file.
```

---

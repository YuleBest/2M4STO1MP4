# 合成两个 M4S 文件为一个 MP4 文件

> 用于应对某个网站缓存的视频为分为视频和音频的两个 M4S 文件的情况



## 安装 Python

### Windows

1. 访问 [Python 官方下载页面](https://www.python.org/downloads/windows/)，选择适合你的Windows版本的Python安装程序，下载完成后，运行安装程序
2. **安装时，请确保选中 *Add Python to PATH* 选项**，这样可以确保在命令行中直接使用 `python` 命令
3. 安装完成后，可以在命令提示符（CMD）或 PowerShell 中执行 `python` 来检查是否安装成功，出现以下信息代表安装成功：`Python x.x.x (tags/vx.x.x:xxxxxxx)...`

## Linux

#### Android

> 我推荐您使用 Termux，你也可以使用其他的独立编译器，以下为 Termux 安装 Python 的步骤：

1. <span id="termux">访问 [Termux 的 GitHub 页面](https://github.com/termux/termux-app/releases/)，下载适合您的 Termux 版本并安装</span>

2. 打开 Termux，执行
   ```shell
   pkg update
   pkg upgrade
   pkg install python
   ```

3. 安装完成后，通过 `python -v` 验证是否安装成功，出现以下信息代表安装成功：`Python x.x.x `

#### 其他系统此处不再赘述，可自行寻找教程。



---



## 安装 FFmpeg

### Windows

1. 访问 [页面](https://github.com/BtbN/FFmpeg-Builds/releases)
2. 下载适合你的版本 `ffmpeg-master-latest-winxx-gpl.zip`
3. 解压到指定目录，如 `C:\ffmpeg`
4. *右键此电脑 → 属性 → 高级系统设置 → 环境变量*
5. 在**系统变量**的 *Path* 中添加 *C:\ffmpeg\bin*，变量名可以填 `ffmpeg`
6. 重启 CMD 或者 PowerShell

### MacOS

1. 安装 Homebrew（如果未安装）

   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. 安装 FFmpeg

   ```bash
   brew install ffmpeg
   ```

### Linux

#### Android

> 我们推荐你使用 Termux，安装 Termux 流程见 [此处](#termux)，以下为基于 Termux 的教程

1. 执行

   ```bash
   pkg update
   pkg upgrade
   pkg install ffmpeg
   ```

   等待下载安装完成

#### Ubuntu/Debian

```shell
# 更新包列表
sudo apt update

# 安装 FFmpeg
sudo apt install ffmpeg
```

#### CentOS/RHEL

```shell
# 安装 EPEL 仓库
sudo yum install epel-release

# 安装 FFmpeg
sudo yum install ffmpeg
```

#### Fedora

```shell
sudo dnf install ffmpeg
````

#### Arch Linux

```shell
sudo pacman -S ffmpeg
```

## 验证安装

在任何系统中，打开终端或命令提示符，执行 `ffmpeg -version` ，出现版本号即为安装成功



---



## 使用

1. 在终端执行

    ```shell
    python <文件所在目录>/2m4sto1mp4_<版本号>.py
    ```

    然后根据提示依次输入*文件路径*、*输出文件格式*和*编码格式*即可。

2. 你也可以直接使用

    ```shell
    python <文件所在目录>/2m4sto1mp4_<版本号>.py <视频>.m4s <音频>.m4s -f <输出文件格式> -v <视频编码格式> -a <音频编码格式>
    ```

    可使用的参数如下（可不填）：

    - `-f, --format`: 指定**输出文件格式**
      - *`mp4` - MP4 格式（不填默认）*
      - `mkv` - Matroska 格式
      - `mov` - QuickTime 格式
      - `avi` - AVI 格式
    - `-v, --vcodec`: 指定**视频编码格式**
      - *`copy` - 复制原始编码（不填默认）*
      - `libx264` - H.264 / AVC 编码
      - `libx265` - H.265 / HEVC 编码
      - `libvpx-vp9` - VP9 编码
    - `-a, --acodec`: 指定**音频编码格式**
      - *`copy` - 复制原始编码（不填默认）*
      - `aac` - AAC 编码
      - `libmp3lame` - MP3 编码
      - `libopus` - Opus 编码
    
    使用示例：
    ```shell
    # 使用默认设置（复制编码，MP4格式）
    python script.py video.m4s audio.m4s output.mp4
    
    # 输出MKV格式，使用H.265编码和AAC音频
    python script.py video.m4s audio.m4s output.mkv -f mkv -v libx265 -a aac
    
    # 使用H.264编码和MP3音频
    python script.py video.m4s audio.m4s output.mp4 -v libx264 -a libmp3lame
    
    # 使用VP9编码和Opus音频，输出为MKV格式
    python script.py video.m4s audio.m4s output.mkv -f mkv -v libvpx-vp9 -a libopus
	```
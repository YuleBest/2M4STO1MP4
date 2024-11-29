#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function  # 使Python 2支持Python 3的print函数
import os
import sys
import subprocess
from pathlib import Path

def get_input(prompt):
    """
    兼容Python 2和3的输入函数
    """
    if sys.version_info[0] < 3:
        return raw_input(prompt)
    return input(prompt)

def get_valid_file_path(prompt):
    """
    获取有效的文件路径
    """
    while True:
        file_path = get_input(prompt).strip()
        if file_path.lower() == 'q':
            print("程序退出")
            sys.exit(0)
        if os.path.exists(file_path):
            return file_path
        print("错误: 文件不存在: {0}".format(file_path))
        print("请重新输入文件路径，或输入'q'退出程序")

def get_output_format():
    """
    获取用户指定的输出格式
    """
    print_section("选择输出格式")
    print("支持的容器格式：")
    print("1. MP4 (默认)")
    print("2. MKV")
    print("3. MOV")
    print("4. AVI")
    
    while True:
        choice = get_input("请选择输出格式 [1-4，直接回车选择默认]: ").strip()
        if not choice:
            return '.mp4'
        if choice in ['1', '2', '3', '4']:
            formats = {
                '1': '.mp4',
                '2': '.mkv',
                '3': '.mov',
                '4': '.avi'
            }
            return formats[choice]
        print("无效的选择，请重新输入")

def get_video_codec():
    """
    获取用户指定的视频编码
    """
    print_section("选择视频编码")
    print("支持的视频编码：")
    print("1. 复制原始编码（默认）")
    print("2. H.264/AVC")
    print("3. H.265/HEVC")
    print("4. VP9")
    
    while True:
        choice = get_input("请选择视频编码 [1-4，直接回车选择默认]: ").strip()
        if not choice:
            return 'copy'
        if choice in ['1', '2', '3', '4']:
            codecs = {
                '1': 'copy',
                '2': 'libx264',
                '3': 'libx265',
                '4': 'libvpx-vp9'
            }
            return codecs[choice]
        print("无效的选择，请重新输入")

def get_audio_codec():
    """
    获取用户指定的音频编码
    """
    print_section("选择音频编码")
    print("支持的音频编码：")
    print("1. 复制原始编码（默认）")
    print("2. AAC")
    print("3. MP3")
    print("4. Opus")
    
    while True:
        choice = get_input("请选择音频编码 [1-4，直接回车选择默认]: ").strip()
        if not choice:
            return 'copy'
        if choice in ['1', '2', '3', '4']:
            codecs = {
                '1': 'copy',
                '2': 'aac',
                '3': 'libmp3lame',
                '4': 'libopus'
            }
            return codecs[choice]
        print("无效的选择，请重新输入")

def get_output_path():
    """
    获取输出文件路径
    """
    # 先获取输出格式
    output_format = get_output_format()
    
    while True:
        output_path = get_input(f"请输入要保存的文件路径 (例如: output{output_format}): ").strip()
        if output_path.lower() == 'q':
            print("程序退出")
            sys.exit(0)
        
        # 确保文件扩展名正确
        if not output_path.lower().endswith(output_format):
            output_path += output_format
            
        # 检查输出目录是否存在
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
            except Exception as e:
                print("错误: 无法创建输出目录: {0}".format(str(e)))
                continue
        
        # 检查文件是否已存在
        if os.path.exists(output_path):
            confirm = get_input("文件 {0} 已存在，是否覆盖？(y/n): ".format(output_path)).lower()
            if confirm != 'y':
                continue
        
        return output_path, output_format

def check_ffmpeg():
    """
    检查系统是否安装了ffmpeg
    """
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE,
                              text=True)
        print("FFmpeg 版本信息：", result.stdout)
        return True
    except Exception as e:
        print("错误详情：", str(e))
        print("错误类型：", type(e).__name__)
        print("错误: 未找到ffmpeg命令!")
        print("请先安装ffmpeg:")
        print("Windows: 请下载ffmpeg并到系统环境变量PATH中")
        print("Linux: sudo apt-get install ffmpeg")
        print("macOS: brew install ffmpeg")
        return False

def get_media_info(file_path):
    """
    获取媒体文件的编码信息
    返回: (codec_type, codec_name)
    """
    try:
        cmd = [
            'ffprobe',
            '-v', 'quiet',
            '-print_format', 'json',
            '-show_streams',
            str(Path(file_path).absolute())
        ]
        
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            print(f"无法获取媒体信息: {result.stderr}")
            return None, None
            
        import json
        info = json.loads(result.stdout)
        
        for stream in info.get('streams', []):
            codec_type = stream.get('codec_type')
            codec_name = stream.get('codec_name')
            if codec_type in ['video', 'audio']:
                return codec_type, codec_name
                
        return None, None
    except Exception as e:
        print(f"获取媒体信息时出错: {str(e)}")
        return None, None

def print_header(text):
    """
    打印带有装饰的标题
    """
    print("\n" + "=" * 50)
    print(f"  {text}")
    print("=" * 50)

def print_section(text):
    """
    打印带有装饰的分节标题
    """
    print("\n" + "-" * 40)
    print(f"  {text}")
    print("-" * 40)

def print_success(text):
    """
    打印成功信息
    """
    print("\n[成功] " + text)

def print_error(text):
    """
    打印错误信息
    """
    print("\n[错误] " + text)

def print_info(text):
    """
    打印信息
    """
    print("\n[信息] " + text)

def merge_m4s_to_mp4(video_file, audio_file, output_file, video_codec='copy', audio_codec='copy'):
    """
    将视频m4s文件和音频m4s文件合并为指定格式
    """
    try:
        if not check_ffmpeg():
            sys.exit(1)
            
        print_section("开始分析媒体文件")
        
        # 获取视频和音频的编码信息
        video_type, video_codec_orig = get_media_info(video_file)
        audio_type, audio_codec_orig = get_media_info(audio_file)
        
        print_info(f"原始视频编码: {video_codec_orig}")
        print_info(f"原始音频编码: {audio_codec_orig}")
        print_info(f"目标视频编码: {video_codec}")
        print_info(f"目标音频编码: {audio_codec}")
        
        # 基础命令参数
        cmd = [
            'ffmpeg',
            '-i', str(Path(video_file).absolute()),
            '-i', str(Path(audio_file).absolute()),
            '-map', '0:v:0',  # 选择第一个输入的视频流
            '-map', '1:a:0',  # 选择第二个输入的音频流
        ]
        
        # 设置视频编码参数
        if video_codec == 'copy':
            cmd.extend(['-c:v', 'copy'])
            # 对于HEVC编码，添加特定标签
            if video_codec_orig and video_codec_orig.lower() in ['hevc', 'h265']:
                cmd.extend(['-tag:v', 'hvc1'])
        else:
            cmd.extend(['-c:v', video_codec])
            # 为特定编码添加优化参数
            if video_codec == 'libx264':
                cmd.extend(['-preset', 'medium', '-crf', '23'])
            elif video_codec == 'libx265':
                cmd.extend(['-preset', 'medium', '-crf', '28', '-tag:v', 'hvc1'])
            elif video_codec == 'libvpx-vp9':
                cmd.extend(['-b:v', '0', '-crf', '30'])
        
        # 设置音频编码参数
        if audio_codec == 'copy':
            cmd.extend(['-c:a', 'copy'])
            if audio_codec_orig and audio_codec_orig.lower() == 'aac':
                cmd.extend(['-bsf:a', 'aac_adtstoasc'])
        else:
            cmd.extend(['-c:a', audio_codec])
            # 为特定音频编码添加参数
            if audio_codec == 'aac':
                cmd.extend(['-b:a', '192k'])
            elif audio_codec == 'libmp3lame':
                cmd.extend(['-b:a', '192k'])
            elif audio_codec == 'libopus':
                cmd.extend(['-b:a', '128k'])
        
        # 添加通用优化参数
        cmd.extend([
            '-movflags', '+faststart',
            str(Path(output_file).absolute())
        ])
        
        print_section("执行合并命令")
        print(' '.join(cmd))
        
        try:
            process = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if process.returncode != 0:
                print_error("FFmpeg错误输出:")
                print(process.stderr)
                raise subprocess.CalledProcessError(process.returncode, cmd)
                
            print_success(f"合并完成! 输出文件: {output_file}")
            # 在合并完成后显示输出文件信息
            get_output_file_info(output_file)
            
        except AttributeError:
            # Python 2 兼容代码
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout, stderr = process.communicate()
            if process.returncode != 0:
                print_error("FFmpeg错误输出:")
                print(stderr.decode('utf-8'))
                raise subprocess.CalledProcessError(process.returncode, cmd)
            
            print_success(f"合并完成! 输出文件: {output_file}")
            # 在合并完成后显示输出文件信息
            get_output_file_info(output_file)
            
    except subprocess.CalledProcessError as e:
        print_error(f"FFmpeg执行失败: {str(e)}")
        print(f"命令: {' '.join(cmd)}")
        sys.exit(1)
    except Exception as e:
        print_error(f"发生未知错误: {str(e)}")
        print(f"错误类型: {type(e).__name__}")
        print(f"完整错误信息: {str(e)}")
        sys.exit(1)

def get_output_file_info(file_path):
    """
    使用 ffmpeg 获取输出文件的详细信息
    """
    try:
        cmd = [
            'ffmpeg',
            '-i', str(Path(file_path).absolute())
        ]
        
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        output = result.stderr  # ffmpeg 将文件信息输出到 stderr
        print_info("FFmpeg 输出信息：")
        print(output)
        
        print_section("输出文件信息")
        
        # 解析视频信息
        import re
        
        # 解析时长
        duration_match = re.search(r"Duration: (\d{2}:\d{2}:\d{2}\.\d{2})", output)
        if duration_match:
            print(f"时长: {duration_match.group(1)}")
            
        # 更新视频流信息的正则表达式
        video_match = re.search(r"Stream #0:0.*?: Video: ([^,]+)", output)
        if video_match:
            print_section("视频流信息")
            print(f"编码格式: {video_match.group(1).strip()}")
            
            # 单独匹配分辨率
            resolution_match = re.search(r"(\d{3,4}x\d{3,4})", output)
            if resolution_match:
                print(f"分辨率: {resolution_match.group(1)}")
            
            # 单独匹配帧率
            fps_match = re.search(r"(\d+(?:\.\d+)?)\s*fps", output)
            if fps_match:
                print(f"帧率: {fps_match.group(1)} fps")
            
        # 更新音频流信息的正则表达式
        audio_match = re.search(r"Stream #0:1.*?: Audio: ([^,]+)", output)
        if audio_match:
            print_section("音频流信息")
            print(f"编码格式: {audio_match.group(1).strip()}")
            
            # 单独匹配采样率
            sample_rate_match = re.search(r"(\d+ Hz)", output)
            if sample_rate_match:
                print(f"采样率: {sample_rate_match.group(1)}")
            
            # 单独匹配声道信息
            channel_match = re.search(r"(stereo|mono|[1-9]\d* channels)", output)
            if channel_match:
                print(f"声道: {channel_match.group(1)}")
            
        # 解析比特率
        bitrate_match = re.search(r"bitrate: (\d+) kb/s", output)
        if bitrate_match:
            print(f"总比特率: {bitrate_match.group(1)} kb/s")
            
        # 获取文件大小
        try:
            size_bytes = os.path.getsize(file_path)
            size_mb = size_bytes / (1024 * 1024)
            print(f"文件大小: {size_mb:.2f} MB")
        except Exception as e:
            print_error(f"无法获取文件大小: {str(e)}")
            
    except Exception as e:
        print_error(f"获取输出文件信息时出错: {str(e)}")
        print(f"错误类型: {type(e).__name__}")

def parse_args():
    """
    解析命令行参数
    """
    import argparse
    
    # 创建参数解析器
    parser = argparse.ArgumentParser(description='媒体文件合并工具')
    
    # 添加参数
    parser.add_argument('video', nargs='?', help='视频文件路径')
    parser.add_argument('audio', nargs='?', help='音频文件路径')
    parser.add_argument('output', nargs='?', help='输出文件路径')
    
    parser.add_argument('-f', '--format', 
                        choices=['mp4', 'mkv', 'mov', 'avi'],
                        default='mp4',
                        help='输出文件格式 (默认: mp4)')
    
    parser.add_argument('-v', '--vcodec',
                        choices=['copy', 'libx264', 'libx265', 'libvpx-vp9'],
                        default='copy',
                        help='视频编码格式 (默认: copy)')
    
    parser.add_argument('-a', '--acodec',
                        choices=['copy', 'aac', 'libmp3lame', 'libopus'],
                        default='copy',
                        help='音频编码格式 (默认: copy)')
    
    return parser.parse_args()

def main():
    """
    主函数，支持命令行参数和交互式输入
    """
    print_header("欢迎使用媒体文件合并工具")
    
    if not check_ffmpeg():
        sys.exit(1)
    
    args = parse_args()
    
    # 如果提供了任何位置参数，则使用命令行模式
    if args.video or args.audio or args.output:
        if not (args.video and args.audio and args.output):
            print_error("命令行用法:")
            print("基本用法: python script.py video.m4s audio.m4s output.mp4")
            print("完整用法: python script.py video.m4s audio.m4s output.mp4 -f mkv -v libx264 -a aac")
            print("\n可选参数:")
            print("-f, --format  输出格式 [mp4/mkv/mov/avi] (默认: mp4)")
            print("-v, --vcodec  视频编码 [copy/libx264/libx265/libvpx-vp9] (默认: copy)")
            print("-a, --acodec  音频编码 [copy/aac/libmp3lame/libopus] (默认: copy)")
            sys.exit(1)
            
        video_file = args.video
        audio_file = args.audio
        output_file = args.output
        
        # 验证文件是否存在
        if not os.path.exists(video_file):
            print_error(f"视频文件不存在: {video_file}")
            sys.exit(1)
        if not os.path.exists(audio_file):
            print_error(f"音频文件不存在: {audio_file}")
            sys.exit(1)
            
        # 确保输出文件有正确的扩展名
        if not output_file.lower().endswith('.' + args.format):
            output_file = os.path.splitext(output_file)[0] + '.' + args.format
        
        # 使用命令行指定的编码格式
        video_codec = args.vcodec
        audio_codec = args.acodec
        
    else:
        # 交互式模式
        print("(随时输入'q'退出程序)")
        video_file = get_valid_file_path("请输入视频m4s文件路径: ")
        audio_file = get_valid_file_path("请输入音频m4s文件路径: ")
        
        # 获取并显示原始编码信息
        print_section("原始媒体信息")
        video_type, video_codec_orig = get_media_info(video_file)
        audio_type, audio_codec_orig = get_media_info(audio_file)
        print_info(f"视频文件编码: {video_codec_orig}")
        print_info(f"音频文件编码: {audio_codec_orig}")
        
        # 选择编码格式
        video_codec = get_video_codec()
        audio_codec = get_audio_codec()
        output_file, _ = get_output_path()
    
    merge_m4s_to_mp4(video_file, audio_file, output_file, video_codec, audio_codec)

if __name__ == "__main__":
    main()

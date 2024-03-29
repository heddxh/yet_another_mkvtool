#!/usr/bin/env python3
import mimetypes
import os
import subprocess
from typing import List

# 路径配置
mkv_dir = "/home/heddxh/Workspace/Resources/yet_another_mkvtool/example/"
sub_dir = "/home/heddxh/Workspace/Resources/yet_another_mkvtool/example/"
font_dir = "/home/heddxh/Workspace/Resources/yet_another_mkvtool/example/Fonts"
output_dir = "/home/heddxh/Workspace/Resources/yet_another_mkvtool/example/output"

# 字幕文件名语言标识
SC: str = "sc"  # 简体中文
TC: str = "tc"  # TODO: 繁体中文，暂时只处理一条轨道


def main():
    for filename in os.listdir(mkv_dir):
        exec: List[str] = []
        if filename.endswith(".mkv"):
            mkv_file = os.path.join(mkv_dir, filename)
            main_name, _ = os.path.splitext(filename)
            subtitle_files = find_sub(main_name)
            output_path = os.path.join(output_dir, filename)
            exec += [
                "mkvmerge",
                "-o",
                output_path,
            ]
            for sub in subtitle_files:
                exec += merge_sub(sub, mkv_file)
                subset_fonts(sub, font_dir)
            with os.scandir(output_dir) as ot:
                for entry in ot:
                    if entry.is_dir() and entry.name.endswith("subsetted"):
                        exec += merge_fonts(entry.path)
            # print(f"将执行: {exec}")
            subprocess.run(exec)


def find_sub(main_name: str) -> List[str]:
    """查找字幕文件并返回绝对路径列表"""
    result: List[str] = []
    for filename in os.listdir(sub_dir):
        # if filename.startswith(main_name) and filename.endswith("ass"):
        if filename.startswith(main_name) and filename.endswith("sc.ass"): # TODO: 目前只处理简体中文
            print(f"{main_name} -> {filename}")
            result.append(os.path.join(sub_dir, filename))
    return result


def merge_sub(sub_path: str, mkv_path: str) -> List[str]:
    base_name = os.path.basename(sub_path)
    filename, _ = os.path.splitext(base_name)
    _, lan = os.path.splitext(filename)
    lan = lan[1:]
    # 判断简繁
    if lan == SC:
        language_code = "zh-Hans"
        track_name = "简体中文"
    # elif lan == TC:
    #    language_code = "zh-Hant"
    #    track_name = "繁体中文"
    else:
        print("fPass: {lan}")
        return []
    # 嵌入字幕
    return [
        mkv_path,
        "--language",
        f"0:{language_code}",
        "--track-name",
        f"0:{track_name}",
        sub_path,
    ]


def subset_fonts(sub_path: str, font_dir: str = font_dir):
    """子集化后的字体默认存储在{output_dit}/fonts"""
    subprocess.run(
        [
            "assfonts",
            "-s",
            "-i",
            sub_path,
            "-f",
            font_dir,
            "-o",
            os.path.join(output_dir),
        ]
    )


def merge_fonts(font_dir: str) -> List[str]:
    """嵌入字体"""
    merge_fonts_exec: List[str] = []
    for filename in os.listdir(font_dir):
        mime = mimetypes.guess_type(os.path.join(font_dir, filename))[0]
        print(f"filename: {filename}, mime: {mime}")
        if mime and mime.startswith("font"):
            merge_fonts_exec += [
                "--attachment-mime-type",
                mime,
                "--attach-file",
                os.path.join(font_dir, filename),
            ]
    return merge_fonts_exec


if __name__ == "__main__":
    main()

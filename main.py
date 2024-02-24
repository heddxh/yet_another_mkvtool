import json
import os
import subprocess
from typing import List

# 路径配置
mkv_dir = "/home/heddxh/Workspace/Resources/yet_another_mkvtool/example/"
sub_dir = "/home/heddxh/Workspace/Resources/yet_another_mkvtool/example/"
font_dir = "/home/heddxh/Workspace/Resources/yet_another_mkvtool/example/Fonts"
output_dir = "/home/heddxh/Workspace/Resources/yet_another_mkvtool/example/output"

# 字幕文件名语言标识
SC = "sc"  # 简体中文
TC = "tc"  # 繁体中文

EXEC = []


def main():
    for filename in os.listdir(mkv_dir):
        if filename.endswith(".mkv"):
            mkv_file = os.path.join(mkv_dir, filename)
            main_name, _ = os.path.splitext(filename)
            subtitle_files = find_ass(main_name)
            for sub in subtitle_files:
                merge_ass(sub, mkv_file)
            subset_fonts(font_dir)
            merge_fonts(mkv_file)


# Find sub files according to base name. Return absolute path.
def find_ass(main_name: str) -> List[str]:
    result = []
    for filename in os.listdir(sub_dir):
        if filename.startswith(main_name) and filename.endswith("ass"):
            print(f"{main_name} -> {filename}")
            result.append(os.path.join(sub_dir, filename))
    return result


def merge_ass(sub_path: str, mkv_path: str):
    base_name = os.path.basename(sub_path)
    _, lan = os.path.splitext(base_name)
    output_name, _ = os.path.splitext(os.path.basename(mkv_path))
    output_path = os.path.join(output_dir, output_name) + ".mkv"
    # 判断简繁
    match (lan):
        case str(SC):
            language_code = "zh-Hans"
            track_name = "简体中文"
        case str(TC):
            language_code = "zh-Hant"
            track_name = "繁体中文"
    # 嵌入字幕
    # subprocess.run(["mkvmerge", "-o", output_path, mkv_path, sub_path])
    EXEC = ["mkvmerge", "-o", output_path, mkv_path, sub_path]
    # 找到字幕轨道并更改语言标签
    info_raw = subprocess.run(
        ["mkvmerge", "-J", output_path], capture_output=True, text=True, check=True
    )
    tracks = json.loads(info_raw.stdout).get("tracks")
    for t in tracks:
        # 找到未指定语言标签的字幕轨道
        if (
            t.get("type") == "subtitles"
            and t.get("properties").get("language") == "und"
        ):
            subprocess.run(
                [
                    "mkvpropedit",
                    output_path,
                    "--edit",
                    f"track:={t.get('properties').get('uid')}",
                    "--set",
                    f"language={language_code}",
                    "--set",
                    f"name={track_name}",
                ]
            )


def subset_fonts(sub_path: str):
    """子集化后的字体默认存储在{output_dit}/fonts"""
    subprocess.run(
        [
            "assfonts",
            "-i",
            sub_path,
            "-f",
            font_dir,
            "-o",
            os.path.join(output_dir, "fonts"),
        ]
    )


def merge_fonts(mkv_path: str):
    pass


if __name__ == "__main__":
    main()

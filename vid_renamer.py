import os
import re
from typing import List

VID_PATH = "/mnt/myPSSD_2T/media/series/やがて君になる (2018)"
# VID_NAME = "やがて君になる"


def main():
    for filename in os.listdir(VID_PATH):
        if filename.endswith(".mkv"):
            pattern = r"\[\d+\]"
            ep_num_match: List[str] = re.findall(pattern, filename)
            if len(ep_num_match) == 1:
                ep: str = ep_num_match[0].strip("[]")
                os.rename(
                    os.path.join(VID_PATH, filename),
                    os.path.join(VID_PATH, f"S01E{ep}.mkv"),
                )
            else:
                raise ValueError(f"文件名 {filename} 不符合预期")


if __name__ == "__main__":
    main()

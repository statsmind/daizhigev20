import json
import os
import re
import sys
from typing import List

import numpy as np


def split_lines(lines: List[str], max_len: int, overlap: int):
    """Split a list of lines into multiple shorter lines.

    Args:
        lines (List[str]): A list of lines.
        max_len (int): The maximum length of a line.
        overlap (int): The overlap between two lines.

    Returns:
        List[List[str]]: A list of lists of lines.
    """
    if len(lines) == 0:
        return [[]]

    buf = []
    buf_len = 0

    for line in lines:
        if buf_len + len(line) > max_len:
             yield buf

             buf = buf[-2:]
             buf.append(line)
             buf_len = np.sum([len(txt) for txt in buf])
        else:
            buf.append(line)
            buf_len += len(line)

    if len(buf) > 0:
        yield buf


def split_text(text: str, window: int):
    lines = []

    offset = 0
    while True:
        lines.append(text[offset: offset + window])
        if offset + window >= len(text):
            break
        offset += window

    if len(lines) > 1 and len(lines[-1]) <= window / 4:
        last_line = lines[-1]
        lines = lines[:-1]
        lines[-1] += last_line

    return lines

def build_dataset(output_path: str, cn_name: str, en_name: str):
    output_file = os.path.join(output_path, f"daizhige_{en_name}.jsonl")
    root_path = os.path.dirname(__file__)

    with open(output_file, "w", encoding="utf-8") as fp:
        for dirpath, dirnames, filenames in os.walk(os.path.join(root_path, cn_name)):
            for filename in filenames:
                if not filename.endswith(".txt"):
                    continue

                print("processing", os.path.join(dirpath, filename))

                with open(os.path.join(dirpath, filename), 'r', encoding="utf-8") as f:
                    lines = [line.strip() for line in f.readlines()]
                    lines = [line + "\n" for line in lines if len(line) > 0]
                    # 这里需要处理过长文本的问题，按4096截断，中间允许128的overlap

                    cut_lines = []
                    for line in lines:
                        for split_line in split_text(line, 1000):
                            cut_lines.append(split_line)

                    for lines_idx, lines in enumerate(split_lines(cut_lines, 4096, 128)):
                        content = json.dumps({
                            'category': cn_name,
                            'filename': filename,
                            'segment_id': lines_idx,
                            'text': "".join(lines)
                        }, ensure_ascii=False)

                        fp.write(content + "\n")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python build_dataset.py output_path")
        exit(1)

    datasets = {
        '佛藏': 'buddha', '儒藏': 'confucianist', '医藏': 'medical', '史藏': 'histories', '子藏': 'masters',
        '易藏': 'ching', '艺藏': 'art', '诗藏': 'poem', '道藏': 'daozang', '集藏': 'collections'}
    output_path = sys.argv[1]
    os.makedirs(output_path, exist_ok=True)

    for cn_name, en_name in datasets.items():
        build_dataset(output_path, cn_name, en_name)


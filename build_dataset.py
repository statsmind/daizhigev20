import json
import os
import re
import sys


def build_dataset(output_path: str, cn_name: str, en_name: str):
    output_file = os.path.join(output_path, f"daizhige_{en_name}.jsonl")
    root_path = os.path.dirname(__file__)

    with open(output_file, "w", encoding="utf-8") as fp:
        for dirpath, dirnames, filenames in os.walk(os.path.join(root_path, cn_name)):
            for filename in filenames:
                if not filename.endswith(".txt"):
                    continue

                with open(os.path.join(dirpath, filename), 'r', encoding="utf-8") as f:
                    lines = [line.strip() for line in f.readlines()]
                    lines = [line for line in lines if len(line) > 0]
                    content = json.dumps({
                        'category': cn_name,
                        'filename': filename,
                        'text': "\n".join(lines)
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


# 添加标点符号等预处理
# xxxx.txt 是原始文本
# xxxx_pp.txt 是预处理之后的文本

import os
import re
from jiayan import load_lm
from jiayan import CRFPunctuator

lm = load_lm(r'D:\models\jiayan_models\jiayan.klm')
punctuator = CRFPunctuator(lm, r'D:\models\jiayan_models\cut_model')
punctuator.load(r'D:\models\jiayan_models\punc_model')

min_ratio = 0.05

def get_pp_ratio(content: str, include_whitespace: bool = False):
    content = content.replace("\t", " ").replace('　', ' ')
    content = content.replace("(", "（").replace(')', '）')
    content = content.strip()

    if include_whitespace:
        content = re.sub(r'[ ]+', ",", content)

    pp_content = re.sub(r"[^,，\\.。;；《》？?（）]", "", content)
    return len(pp_content) / len(content)


r = get_pp_ratio("波利富楼那遮利　三曼陀达舍尼罗佉　摩诃毗呵罗伽帝　三曼陀毗陀那伽帝　摩诃迦梨波帝　波婆祢　萨婆哆诟　三曼陀　修钵梨富隶　阿夜那达摩帝　摩诃毗鼓毕帝　摩诃弥勒簸僧祇帝　醯帝簁三博只悕帝　三曼陀阿咃　阿[少/兔]婆罗尼。", True)

for dirpath, dirnames, filenames in os.walk(os.path.dirname(__file__)):
    for filename in filenames:
        if not filename.endswith(".txt") or filename.endswith("_pp.txt") or filename == "requirements.txt":
            continue

        filepath = os.path.join(dirpath, filename)
        # print("processing", filepath)

        pp_filepath = filepath.replace(".txt", "_pp.txt")
        if os.path.exists(pp_filepath):
            continue

        with open(filepath, 'r', encoding='utf-8') as fp:
            content = fp.read()

        # 识别标点符号的比率
        pp_ratio = get_pp_ratio(content)
        if pp_ratio >= min_ratio:
            # print("skipping", ratio, filepath)
            continue

        print("processing", filepath)

        lines = content.replace("\r", "").replace('\t', ' ').replace('　', ' ').split("\n")
        lines = [line.strip() for line in lines]
        lines = [line for line in lines if len(line) > 0]

        pp_lines = []
        for line in lines:
            pp_line_ratio = get_pp_ratio(line, True)
            if len(line) < 20 or pp_line_ratio >= min_ratio:
                pp_lines.append(line)
                continue

            pp_line = punctuator.punctuate(line)
            pp_lines.append(pp_line)

        with open(pp_filepath, 'w', encoding='utf-8') as fp:
            fp.write("\n".join(pp_lines))

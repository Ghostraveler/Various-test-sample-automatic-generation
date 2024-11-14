from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import os
import pandas as pd
import csv

size_limit = 300000
csv.field_size_limit(size_limit)
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
tokenizer = AutoTokenizer.from_pretrained("../squad_gen_qst_zh_v0")
model = AutoModelForSeq2SeqLM.from_pretrained("../squad_gen_qst_zh_v0")


def split_sentences(text, max_length=500):
    """
    将文本分割成多句话，每句话不超过指定长度，并以句号作为分割。
    """
    sentences = []
    current_sentence = ''
    words = text.split()
    for word in words:
        if len(current_sentence) + len(word) <= max_length:
            current_sentence += ' ' + word
        else:
            sentences.append(current_sentence.strip() + '。')
            current_sentence = word
    if current_sentence:
        sentences.append(current_sentence.strip() + '。')
    return sentences


def read_and_split_list_from_csv(folder_path, list_name):
    # 创建问题文本文件名
    txt_filename = f"{folder_path}_squad_gen_qst_zh_v0问题(sentence-split=500,num_sentences=1).txt"
    """
    读取CSV文件中指定列表的内容，并将其分割成多句话。
    """
    with open(txt_filename, 'w') as file:
        # 遍历文件夹中的所有文件名
        for filename in os.listdir(folder_path):
            # 如果文件名以"_wiki_info"结尾，则生成问题
            if filename.endswith('_wiki_info.csv'):
                csv_filepath = os.path.join(folder_path, filename)
                with open(csv_filepath, 'r', encoding='utf-8') as csvfile:
                    file.write(filename[:-14] + '\n')
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        if list_name in row:
                            sentences = split_sentences(row[list_name])
                            for sentence in sentences:
                                input_ids = tokenizer.encode(sentence, return_tensors="pt", add_special_tokens=True)
                                outputs = model.generate(input_ids, max_length=100, num_return_sequences=1)
                                generated_question = tokenizer.decode(outputs[0], skip_special_tokens=True)
                                file.write('在' + filename[:-14] + '这一主题内容中，' + generated_question + '\n')
                                print('在' + filename[:-14] + '这一主题内容中，' + generated_question)


# 替换为你的CSV文件路径和列表名称
folder_path = '../简体/经济/雄安新区'
list_name = '相关内容'
read_and_split_list_from_csv(folder_path, list_name)

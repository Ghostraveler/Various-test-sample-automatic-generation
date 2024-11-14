import os
import csv
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QTextEdit

# 设置读取csv文件内容的字符最大为300000
size_limit = 300000
csv.field_size_limit(size_limit)

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


class SquadGenApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("mT5模型文本生成器")
        self.setGeometry(100, 100, 600, 400)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.folder_path_edit = QTextEdit()
        self.folder_path_edit.setPlaceholderText("请输入CSV文件夹路径")
        layout.addWidget(self.folder_path_edit)

        self.list_name_edit = QTextEdit()
        self.list_name_edit.setPlaceholderText("请输入要提取的列表名称")
        layout.addWidget(self.list_name_edit)

        self.run_button = QPushButton("运行")
        layout.addWidget(self.run_button)
        self.run_button.clicked.connect(self.run_squad_gen)

        self.result_label = QLabel()
        layout.addWidget(self.result_label)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def run_squad_gen(self):
        # csv文件夹路径
        folder_path = self.folder_path_edit.toPlainText()
        # 读取的列表
        list_name = self.list_name_edit.toPlainText()

        # 加载tokenizer和model
        tokenizer = AutoTokenizer.from_pretrained(
            "/Users/ghostraveler/PycharmProjects/pythonProject/squad_gen_qst_zh_v0")
        model = AutoModelForSeq2SeqLM.from_pretrained(
            "/Users/ghostraveler/PycharmProjects/pythonProject/squad_gen_qst_zh_v0")

        def split_sentences(text, max_length=500):
            # 实现split_sentences函数的代码...
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
            # 实现read_and_split_list_from_csv函数的代码...
            # 创建问题文本文件名
            txt_filename = f"{folder_path}_squad_gen_qst_zh_v0问题(sentence-split=500,num_sentences=1).txt"
            """
            读取CSV文件中指定列表的内容，并将其分割成多句话。
            """
            with open(txt_filename, 'w') as file:
                # 遍历文件夹中的所有文件名
                for filename in os.listdir(folder_path):
                    # 如果csv文件名以"_wiki_info"结尾，则生成问题
                    if filename.endswith('_wiki_info.csv'):
                        csv_filepath = os.path.join(folder_path, filename)
                        with open(csv_filepath, 'r', encoding='utf-8') as csvfile:
                            file.write(filename[:-14] + '\n')
                            reader = csv.DictReader(csvfile)
                            for row in reader:
                                if list_name in row:
                                    sentences = split_sentences(row[list_name])
                                    for sentence in sentences:
                                        input_ids = tokenizer.encode(sentence, return_tensors="pt",
                                                                     # mt5模型的特殊标记
                                                                     add_special_tokens=True)
                                        outputs = model.generate(input_ids, max_length=100, num_return_sequences=1)
                                        generated_question = tokenizer.decode(outputs[0], skip_special_tokens=True)
                                        file.write(
                                            '在' + filename[:-14] + '这一主题内容中，' + generated_question + '\n')
                                        print('在' + filename[:-14] + '这一主题内容中，' + generated_question)

        try:
            read_and_split_list_from_csv(folder_path, list_name)
            txt_filename = f"{folder_path}_squad_gen_qst_zh_v0问题(sentence-split=500,num_sentences=1).txt"
            with open(txt_filename, 'r', encoding='utf-8') as file:
                content = file.read()
                self.result_label.setText(content)
        except Exception as e:
            self.result_label.setText(f"出现错误：{e}")


if __name__ == "__main__":
    app = QApplication([])
    window = SquadGenApp()
    window.show()
    app.exec_()

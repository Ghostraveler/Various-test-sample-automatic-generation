import sys
import os
import time

import wikipedia
import csv
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QTextEdit, QMessageBox


class WikiSearchApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("维基百科搜索")
        self.setGeometry(100, 100, 200, 200)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        # 设立文本输入框
        self.text_edit = QTextEdit()
        layout.addWidget(self.text_edit)
        # 设立开始搜索按钮
        self.button = QPushButton("开始搜索")
        layout.addWidget(self.button)
        self.button.clicked.connect(self.search_wikipedia)
        # 用于显示文本
        # self.result_label = QLabel()
        # layout.addWidget(self.result_label)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def search_wikipedia(self):
        # 将爬取的维基百科网站设置为中文网站
        wikipedia.set_lang('zh')
        # query为我们所输入进搜索框的文本
        query = self.text_edit.toPlainText()
        result = wikipedia.search(query)
        print(result)

        for num in range(len(result)):
            time.sleep(10)
            try:
                # 尝试爬取页面
                page = wikipedia.page(result[int(num)], preload=True)
            except Exception as e:
                error_message = f"执行错误：{e}"
                # self.result_label.setText(error_message)
                QMessageBox.information(self, "错误提示", error_message)
                continue
            # 页面标题
            title = page.title
            # 页面类别
            categories = page.categories
            # 页面内容
            content = page.content
            # 页面报道
            links = page.links
            # 页面参考文献
            references = page.references
            # 页面总结
            summary = page.summary

            # self.result_label.setText(f"相关主题: {title}\n"
            #                           f"相关内容: {content}\n"
            #                           f"相关类别: {categories}\n"
            #                           f"相关报道: {links}\n"
            #                           f"参考: {references}\n"
            #                           f"内容总结: {summary}")

            # 指定文件夹路径
            folder_path = "/Users/ghostraveler/PycharmProjects/pythonProject/DATA/spider"
            # 写入CSV文件
            csv_filename = f"{result[int(num)]}_wiki_info.csv"
            # 完整文件路径
            file_path = os.path.join(folder_path, csv_filename)

            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['相关主题', '相关内容', '相关类别', '相关报道', '参考', '内容总结']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow({
                    '相关主题': title,
                    '相关内容': content,
                    '相关类别': categories,
                    '相关报道': links,
                    '参考': references,
                    '内容总结': summary
                })

            QMessageBox.information(self, "提示", f"CSV 文件已保存在路径：{file_path}")
        QMessageBox.information(self, "提示", "相关数据已全部爬取")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WikiSearchApp()
    window.show()
    sys.exit(app.exec_())

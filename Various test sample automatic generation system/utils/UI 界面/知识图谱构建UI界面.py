import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QFileDialog, QVBoxLayout, QMessageBox
from py2neo import Graph, Node, Relationship
import pandas as pd
import webbrowser

#连接知识图谱数据库
graph = Graph("http://localhost:7474", auth=("neo4j", "huang020528"))


def get_or_create_node(label, property_name, property_value):
    try:
        query = f"MATCH (n:{label}) WHERE n.{property_name} = $value RETURN n"
        result = graph.run(query, value=property_value)
        node = result.evaluate()
        if node:
            return node
        else:
            node = Node(label, **{property_name: property_value})
            graph.create(node)
            return node
    except Exception as e:
        error_message = f"执行错误：{e}"
        print(error_message)
        return


# 两个节点之间创建关系
def create_relationship(node1, rel_type, node2):
    try:
        rel = Relationship(node1, rel_type, node2)
        graph.create(rel)
    except Exception as e:
        error_message = f"执行错误：{e}"
        print(error_message)
        return


# Function to process the content and create nodes and relationships


def process_content(topic_node, content):
    try:
        # 将内容按 "===" 分割成多个部分，每个部分代表一个主要的段落或章节
        sections = content.split("===")
        for section in sections:
            # 将每个部分按 "==" 进一步分割成子部分
            section = section.strip()
            if section:
                subsections = section.split("==")
                # 按行分割子部分，只分割一次，得到标题和内容
                parent_node = topic_node
                for subsection in subsections:
                    subsection = subsection.strip()
                    if subsection:
                        lines = subsection.split("\n", 1)
                        if len(lines) > 1:
                            title, subcontent = lines
                            title = title.strip()
                            subcontent = subcontent.strip()
                            # 获取或创建名为 title 的 Content 节点
                            content_node = get_or_create_node("Content", "name", title)
                            create_relationship(parent_node, "HAS_SECTION", content_node)
                            parent_node = content_node
                            # 创建父节点和内容节点之间的关系
                            content_node["text"] = subcontent
                            graph.push(content_node)
                        else:
                        #当没有内容时，只有标题
                            content_node = get_or_create_node("Content", "name", subsection)
                            create_relationship(parent_node, "HAS_SECTION", content_node)
    except Exception as e:
        error_message = f"执行错误：{e}"
        print(error_message)
        return

    # Function to process a CSV file and generate knowledge graph text


def process_csv(csv_path, central_node):
    try:
        # 加载csv文件
        df = pd.read_csv(csv_path)


        for index, row in df.iterrows():
            # 为节点创建属性
            topic_node = get_or_create_node("Topic", "name", row["相关主题"])
            content = row["相关内容"]
            category_node = get_or_create_node("Category", "name", row["相关类别"])
            report_node = get_or_create_node("Report", "name", row["相关报道"])
            reference_node = get_or_create_node("Reference", "name", row["参考"])
            summary_node = get_or_create_node("Summary", "name", row["内容总结"])

            # 在不同类别的节点之间建立关系
            create_relationship(central_node, "RELATED_TO", topic_node)
            create_relationship(topic_node, "BELONGS_TO_CATEGORY", category_node)
            create_relationship(topic_node, "HAS_REPORT", report_node)
            create_relationship(topic_node, "HAS_REFERENCE", reference_node)
            create_relationship(topic_node, "HAS_SUMMARY", summary_node)

            # Process the content to create detailed sections
            process_content(topic_node, content)
    except Exception as e:
        error_message = f"执行错误：{e}"
        print(error_message)
        return


def traverse_directory(directory, central_node):
    try:
        for root, dirs, files in os.walk(directory):
            for file in files:
                # 对文件夹下的csv文件来进行处理
                if file.endswith(".csv"):
                    csv_path = os.path.join(root, file)
                    process_csv(csv_path, central_node)
    except Exception as e:
        error_message = f"执行错误：{e}"
        print(error_message)
        return


class KnowledgeGraphApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Knowledge Graph Generator')

        layout = QVBoxLayout()

        self.label_topic = QLabel('Center Topic:')
        layout.addWidget(self.label_topic)

        self.input_topic = QLineEdit(self)
        layout.addWidget(self.input_topic)

        self.label_directory = QLabel('Directory Path:')
        layout.addWidget(self.label_directory)

        self.input_directory = QLineEdit(self)
        layout.addWidget(self.input_directory)

        self.button_browse = QPushButton('Browse', self)
        self.button_browse.clicked.connect(self.browse_directory)
        layout.addWidget(self.button_browse)

        self.button_generate = QPushButton('Generate Knowledge Graph', self)
        self.button_generate.clicked.connect(self.generate_knowledge_graph)
        layout.addWidget(self.button_generate)

        self.setLayout(layout)

    def browse_directory(self):
        try:
            # 打开一个目录选择对话框，让用户选择一个目录
            directory = QFileDialog.getExistingDirectory(self, "Select Directory")
            if directory:
                self.input_directory.setText(directory)
        except Exception as e:
            error_message = f"执行错误：{e}"
            print(error_message)
            return

    def generate_knowledge_graph(self):
        try:
            topic = self.input_topic.text().strip()
            directory = self.input_directory.text().strip()
            # 没有输入主题，警告，返回原来的页面
            if not topic:
                QMessageBox.warning(self, 'Input Error', 'Please enter a center topic.')
                return
            # 没有输入文件夹路径警告，返回原来的页面
            if not directory or not os.path.isdir(directory):
                QMessageBox.warning(self, 'Input Error', 'Please enter a valid directory path.')
                return
            # 创建中心节点
            central_node = get_or_create_node("Topic", "name", topic)
            traverse_directory(directory, central_node)

            QMessageBox.information(self, 'Success', 'Knowledge graph generated successfully!')
            webbrowser.open("http://localhost:7474",0,False)
        except Exception as e:
            error_message = f"执行错误：{e}"
            print(error_message)
            return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = KnowledgeGraphApp()
    ex.show()
    sys.exit(app.exec_())

# coding:utf-8
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QWidget
from py2neo import Graph
from openai import OpenAI

# 设置连接到Neo4j数据库的参数
neo4j_uri = "http://localhost:7474"
neo4j_user = "neo4j"
neo4j_password = "huang020528"

# 连接到Neo4j数据库
graph = Graph(neo4j_uri, auth=(neo4j_user, neo4j_password))


# 定义一个函数，从Neo4j数据库中获取类别为 Summary 的节点的属性 name 内容
def get_summary_names_from_neo4j():
    summary_names = []
    #先获取到类别为summary的节点，返回属性为name的内容
    query = """
    MATCH (n:Summary)
    RETURN n.name AS name
    """
    results = graph.run(query)
    for record in results:
        summary_names.append(record["name"])
    return summary_names


class KnowledgeGraphApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('知识图谱增强的GPT3.5生成文本问题')
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        # 领域提示词
        self.lingyu_label = QLabel('领域提示词:')
        layout.addWidget(self.lingyu_label)
        self.lingyu_input = QLineEdit()
        layout.addWidget(self.lingyu_input)

        # 类别提示词
        self.leibie_label = QLabel('类别提示词:')
        layout.addWidget(self.leibie_label)
        self.leibie_input = QLineEdit()
        layout.addWidget(self.leibie_input)

        # 生成数量
        self.quantity_label = QLabel('生成数量:')
        layout.addWidget(self.quantity_label)
        self.quantity_input = QLineEdit()
        layout.addWidget(self.quantity_input)

        # 生成按钮
        self.generate_button = QPushButton('生成')
        self.generate_button.clicked.connect(self.generate_questions)
        layout.addWidget(self.generate_button)

        # 输出区域
        self.output_text = QTextEdit()
        layout.addWidget(self.output_text)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def generate_questions(self):
        lingyu = self.lingyu_input.text()
        leibie = self.leibie_input.text()
        quantity = self.quantity_input.text()

        # 获取 Summary 类节点的 name 属性
        summary_names = get_summary_names_from_neo4j()

        prompt = f"请结合以下文本内容，帮我生成{quantity}个属于{lingyu}领域，与{leibie}相关的复杂的文本问题，生成的文本问题要复杂："
        string = summary_names
        print(string)
        #将提示词模版与文本内容相结合
        prompt = prompt + str(string)

        # 调用OpenAI GPT-3.5生成问题
        client = OpenAI(base_url="https://api.gptsapi.net/v1",
                        api_key="sk-xxxxxx")
        response = client.chat.completions.create(
            #制定模型
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
            #,max_tokens=
        )
        response_message = response.choices[0].message.content

        self.output_text.setPlainText(response_message)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = KnowledgeGraphApp()
    main_win.show()
    sys.exit(app.exec_())

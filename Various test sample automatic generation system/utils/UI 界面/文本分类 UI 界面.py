import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QLineEdit
from PyQt5.QtGui import QPixmap
import torch
from transformers import BertTokenizer, BertForSequenceClassification


class BertClassifierApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 500, 300)

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.label = QLabel("请输入文本问题：")
        layout.addWidget(self.label)

        self.text_edit = QLineEdit()
        layout.addWidget(self.text_edit)

        self.button = QPushButton("开始评估")
        layout.addWidget(self.button)
        self.button.clicked.connect(self.evaluate_text)

        self.result_label = QLabel()
        layout.addWidget(self.result_label)

        # 添加图片
        self.image_label = QLabel()
        pixmap = QPixmap(
            "/Users/ghostraveler/PycharmProjects/pythonProject/代码演示/UI 界面/文本分类 UI 界面.png")  # 更换成你想要的图片路径
        self.image_label.setPixmap(pixmap)
        layout.addWidget(self.image_label)

        # QWidget窗口部件
        widget = QWidget()
        # 设置布局
        widget.setLayout(layout)
        # 设置为中心部件
        self.setCentralWidget(widget)

    def evaluate_text(self):
        # 加载模型和分词器
        model_path = "/Users/ghostraveler/PycharmProjects/pythonProject/bert_classification_model"
        tokenizer = BertTokenizer.from_pretrained("bert-base-chinese")
        model = BertForSequenceClassification.from_pretrained(model_path)

        # 设置模型为评估模式
        model.eval()
        # 读取相关的编码文件
        with open("/Users/ghostraveler/PycharmProjects/pythonProject/bert_classification_model/label_id.txt", "r",
                  encoding="utf-8") as file:
            label_id_dict = eval(file.read())

        text = self.text_edit.text()
        print("输入的文本问题：", text)
        # 对输入文本进行编码
        encoded_dict = tokenizer.encode_plus(
            text,
            # 是否添加特殊标记，[sep]和[cls]是bert两种特殊标记
            add_special_tokens=True,
            # 文本截断
            max_length=100,
            # 启用截断
            truncation=True,
            # 启用填充
            padding='max_length',
            # 返回注意力掩码
            return_attention_mask=True,
            return_tensors='pt'
        )

        input_ids = encoded_dict['input_ids']
        attention_mask = encoded_dict['attention_mask']

        # 在需要的话将输入移动到GPU上
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        input_ids = input_ids.to(device)
        attention_mask = attention_mask.to(device)

        # 使用模型进行预测
        # 关闭自动求导
        with torch.no_grad():
            outputs = model(input_ids, attention_mask=attention_mask)

        # 获取预测结果的概率分布
        logits = outputs.logits
        probabilities = torch.softmax(logits, dim=1)
        max_prob, max_idx = torch.max(probabilities, dim=1)

        if max_prob.item() > 0.95:
            # 根据输入的整数查找对应的标签
            found_label = None
            for label, idx in label_id_dict.items():
                if idx == int(torch.argmax(logits, dim=1)):
                    found_label = label
                    break
            # 输出结果
            if found_label:
                result_text = f"预测的类别：{found_label}"
        else:
            result_text = "不属于任何一类"

        # 获取概率最大的前三个类别
        top_probabilities, top_indices = torch.topk(probabilities, 3, dim=1)
        # print(int(top_indices[0][0]))
        found_label = []
        # 第一
        for label, idx in label_id_dict.items():
            if idx == int(top_indices[0][0]):
                found_label.append(label)
                break
        # 第二
        for label, idx in label_id_dict.items():
            if idx == int(top_indices[0][1]):
                found_label.append(label)
                break
        # 第三
        for label, idx in label_id_dict.items():
            if idx == int(top_indices[0][2]):
                found_label.append(label)
                break

        result_text += "\n"
        result_text += "Top 3 predicted classes: " + str(found_label) + "\n"
        result_text += "Top 3 probabilities: " + ", ".join([str(p.item()) for p in top_probabilities[0]])
        print(result_text)
        self.result_label.setText(result_text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BertClassifierApp()
    window.show()
    sys.exit(app.exec_())

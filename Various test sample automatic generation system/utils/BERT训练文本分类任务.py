import pandas as pd
import torch
from transformers import BertTokenizer, BertForSequenceClassification, AdamW
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, TensorDataset
from tqdm import tqdm
import os

from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

# 读取CSV文件
df = pd.read_csv("/Users/ghostraveler/PycharmProjects/pythonProject/train_data.csv")
# 删除包含空值的行
df = df.dropna()
# 分割数据集为训练集和验证集
train_texts, val_texts, train_labels, val_labels = train_test_split(df['问题'], df['标签'], test_size=0.2,
                                                                    random_state=42)
# 处理标签数据
label2id = {label: idx for idx, label in enumerate(train_labels.unique())}
print(train_labels)
train_labels = train_labels.map(label2id)
val_labels = val_labels.map(label2id)
print(train_labels)

# 加载预训练的BERT模型和tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
model = BertForSequenceClassification.from_pretrained('bert-base-chinese', num_labels=60)


# 定义函数将文本转换为模型输入
def tokenize_texts(texts, labels):
    input_ids = []
    attention_masks = []

    for text in texts:
        encoded_dict = tokenizer.encode_plus(
            text,
            add_special_tokens=True,
            max_length=64,
            padding='max_length',
            truncation=True,  # 添加截断参数
            return_attention_mask=True,
            return_tensors='pt',
        )
        input_ids.append(encoded_dict['input_ids'])
        attention_masks.append(encoded_dict['attention_mask'])

    input_ids = torch.cat(input_ids, dim=0)
    attention_masks = torch.cat(attention_masks, dim=0)

    # 处理标签数据
    labels = torch.tensor(labels.values)  # 使用.values将Series对象转换为数组

    return input_ids, attention_masks, labels


# 将训练集和验证集文本转换为模型输入
train_input_ids, train_attention_masks, train_labels = tokenize_texts(train_texts, train_labels)
val_input_ids, val_attention_masks, val_labels = tokenize_texts(val_texts, val_labels)

# 创建数据加载器
train_dataset = TensorDataset(train_input_ids, train_attention_masks, train_labels)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

val_dataset = TensorDataset(val_input_ids, val_attention_masks, val_labels)
val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)

# 定义优化器和损失函数
optimizer = AdamW(model.parameters(), lr=2e-5)
criterion = torch.nn.CrossEntropyLoss()

# 训练模型
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

for epoch in range(1):  # 假设训练3个epoch
    model.train()
    for batch in tqdm(train_loader, desc="Epoch {}".format(epoch + 1)):
        input_ids, attention_masks, labels = batch
        input_ids, attention_masks, labels = input_ids.to(device), attention_masks.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(input_ids, attention_mask=attention_masks, labels=labels)
        loss = outputs.loss
        print("损失值：", loss)
        loss.backward()
        optimizer.step()
# 评估模型
model.eval()
predictions, true_labels = [], []

with torch.no_grad():
    for batch in val_loader:
        input_ids, attention_masks, labels = batch
        input_ids, attention_masks, labels = input_ids.to(device), attention_masks.to(device), labels.to(device)

        outputs = model(input_ids, attention_mask=attention_masks)
        logits = outputs.logits
        predictions.extend(torch.argmax(logits, dim=1).cpu().numpy())
        true_labels.extend(labels.cpu().numpy())

# 计算准确率、召回率和F1分数
report = classification_report(true_labels, predictions, target_names=['法制+清朗专项行动','经济+中美贸易'
                                                                       ,'安全+新疆难民','政治+官僚主义与腐败','文化+防火墙','安全+再教育营','经济+雄安新区','民生+就业困难','军事+钓鱼岛','经济+脱贫攻坚',
                                                                       '安全+网络安全','党建+网络强国','军事+情报','文化+诗句','军事+间谍','生态环境+可持续发展','祖国统一+西藏自治','经济+房价',
                                                                       '外交与国际+中美关系','民生+男女对立','民生+女权运动','祖国统一+汉光演习','政治+共产党党争','党建+二十大'
                                                                       ,'生态环境+物种多样性','法制+安乐死','文化+传统节日','文化+南京条约','生态环境+垃圾分类','科教+光刻机','科教+量子纠缠',
                                                                       '法制+深度合成','生态环境+98年大洪水','外交与国际+一带一路','外交与国际+抗美援朝','外交与国际+援建非洲','法制+代孕'
                                                                       ,'安全+恐怖袭击','科教+忒修斯之船','党建+党史学习','党建+入党','民生+阶级固化','经济+一带一路','法制+网络安全','政治+六四事件'
                                                                       ,'祖国统一+钓鱼岛','外交与国际+乌克兰局势','科教+数字隐私权','政治+薄熙来','安全+藏独','生态环境+环境污染','党建+共产主义',
                                                                       '文化+忒修斯之船','祖国统一+南海主权','军事+祖国统一','民生+医患关系','政治+八九学运','祖国统一+台湾选举','军事+恐怖主义','科教+教育体系'], output_dict=True)
print("分类报告：", report)

# 生成混淆矩阵
conf_matrix = confusion_matrix(true_labels, predictions)
print("混淆矩阵：\n", conf_matrix)

# 可视化混淆矩阵
df_cm = pd.DataFrame(conf_matrix, index=['法制+清朗专项行动','经济+中美贸易'
                                                                       ,'安全+新疆难民','政治+官僚主义与腐败','文化+防火墙','安全+再教育营','经济+雄安新区','民生+就业困难','军事+钓鱼岛','经济+脱贫攻坚',
                                                                       '安全+网络安全','党建+网络强国','军事+情报','文化+诗句','军事+间谍','生态环境+可持续发展','祖国统一+西藏自治','经济+房价',
                                                                       '外交与国际+中美关系','民生+男女对立','民生+女权运动','祖国统一+汉光演习','政治+共产党党争','党建+二十大'
                                                                       ,'生态环境+物种多样性','法制+安乐死','文化+传统节日','文化+南京条约','生态环境+垃圾分类','科教+光刻机','科教+量子纠缠',
                                                                       '法制+深度合成','生态环境+98年大洪水','外交与国际+一带一路','外交与国际+抗美援朝','外交与国际+援建非洲','法制+代孕'
                                                                       ,'安全+恐怖袭击','科教+忒修斯之船','党建+党史学习','党建+入党','民生+阶级固化','经济+一带一路','法制+网络安全','政治+六四事件'
                                                                       ,'祖国统一+钓鱼岛','外交与国际+乌克兰局势','科教+数字隐私权','政治+薄熙来','安全+藏独','生态环境+环境污染','党建+共产主义',
                                                                       '文化+忒修斯之船','祖国统一+南海主权','军事+祖国统一','民生+医患关系','政治+八九学运','祖国统一+台湾选举','军事+恐怖主义','科教+教育体系'], columns=['法制+清朗专项行动','经济+中美贸易'
                                                                       ,'安全+新疆难民','政治+官僚主义与腐败','文化+防火墙','安全+再教育营','经济+雄安新区','民生+就业困难','军事+钓鱼岛','经济+脱贫攻坚',
                                                                       '安全+网络安全','党建+网络强国','军事+情报','文化+诗句','军事+间谍','生态环境+可持续发展','祖国统一+西藏自治','经济+房价',
                                                                       '外交与国际+中美关系','民生+男女对立','民生+女权运动','祖国统一+汉光演习','政治+共产党党争','党建+二十大'
                                                                       ,'生态环境+物种多样性','法制+安乐死','文化+传统节日','文化+南京条约','生态环境+垃圾分类','科教+光刻机','科教+量子纠缠',
                                                                       '法制+深度合成','生态环境+98年大洪水','外交与国际+一带一路','外交与国际+抗美援朝','外交与国际+援建非洲','法制+代孕'
                                                                       ,'安全+恐怖袭击','科教+忒修斯之船','党建+党史学习','党建+入党','民生+阶级固化','经济+一带一路','法制+网络安全','政治+六四事件'
                                                                       ,'祖国统一+钓鱼岛','外交与国际+乌克兰局势','科教+数字隐私权','政治+薄熙来','安全+藏独','生态环境+环境污染','党建+共产主义',
                                                                       '文化+忒修斯之船','祖国统一+南海主权','军事+祖国统一','民生+医患关系','政治+八九学运','祖国统一+台湾选举','军事+恐怖主义','科教+教育体系'])
plt.figure(figsize=(10, 7))
sns.heatmap(df_cm, annot=True, fmt='d', cmap="Blues")
plt.xlabel("预测类别")
plt.ylabel("实际类别")
plt.title("混淆矩阵")
plt.show()

# 保存模型
model.save_pretrained("bert_classification_model-01")


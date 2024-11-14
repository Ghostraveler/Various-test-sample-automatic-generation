import torch
from transformers import BertTokenizer, BertForSequenceClassification

# 加载模型和tokenizer
model_path = "bert_classification_model"
tokenizer = BertTokenizer.from_pretrained("bert-base-chinese")
model = BertForSequenceClassification.from_pretrained(model_path)

# 设置模型为评估模式
model.eval()

with open("bert_classification_model/label_id.txt", "r", encoding="utf-8") as file:
    label_id_dict = eval(file.read())

# 输入文本
while True:
    # 对输入文本进行编码
    text = input("请输入文本问题：")
    encoded_dict = tokenizer.encode_plus(
        text,
        add_special_tokens=True,
        max_length=100,
        truncation=True,
        padding='max_length',
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
    with torch.no_grad():
        outputs = model(input_ids, attention_mask=attention_mask)

    # 获取预测结果的概率分布
    logits = outputs.logits
    print(torch.argmax(logits, dim=1))
    probabilities = torch.softmax(logits, dim=1)
    max_prob,max_idx = torch.max(probabilities,dim=1)
    if max_prob.item() > 0.8:
        # 根据输入的整数查找对应的标签
        found_label = None
        for label, idx in label_id_dict.items():
            if idx == int(torch.argmax(logits, dim=1)):
                found_label = label
                break
        # 输出结果
        if found_label:
            print("predicted class：", found_label)
    else:
        print("不属于任何一类")
    # 获取概率最大的前三个类别
    top_probabilities, top_indices = torch.topk(probabilities, 3, dim=1)

    # 将类别索引转换为类别标签
    class_labels = tokenizer.convert_ids_to_tokens(top_indices[0])
    #
    print("Top 3 predicted classes:", class_labels)
    print("Top 3 probabilities:", top_probabilities)

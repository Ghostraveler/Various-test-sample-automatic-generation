import nltk
from collections import Counter
import spacy
import jieba

# 评估文本的句子成分复杂度
def evaluate_complexity(text):
    # 使用 NLTK 进行句子分词和词性标注
    sentences = nltk.sent_tokenize(text)
    pos_tags = [nltk.pos_tag(nltk.word_tokenize(sentence)) for sentence in sentences]

    # 统计不同句子成分的数量
    pos_counts = Counter(tag for sentence in pos_tags for word, tag in sentence)

    return pos_counts


text = ("在方贵伦这一内容下，方贵伦的马来语译文是什么?"
        "在中华革命党这一内容下，中华革命党是什么时候成立的?"
        "在中华革命党这一内容下，孙的死因是什么?"
        "在中华革命党这一内容下，中华革命党在1916年向哪个团体宣战?"
        "在中华革命党这一内容下，中华革命党在抗议期间 做了什么?"
        "在中华革命党这一内容下，孙中山的两个主要革命运动是什么?"
        "在重温入党誓词这一内容下，在中国共产党的重温入党誓词中,党员必须佩戴什么?"
        "在中共中央国家机关工作委员会这一内容下，中央国家机关临时委员会改名为什么?"
        "在中共中央国家机关工作委员会这一内容下，中央机关委员会和中央机关委员会的名称是什么?"
        "在中共中央国家机关工作委员会这一内容下，中央国家机关工委在1997年向哪些方面提出了要求?"
        "在中共中央国家机关工作委员会这一内容下，中央国家机关工作委员会的职责是什么?"
        "在中共中央国家机关工作委员会这一内容下，中央国家机关纪律检查工作委员会的名称是什么?"
        "在中共中央国家机关工作委员会这一内容下，中央政府机关老干部活动中心的负责人是谁?"
        "在中国共产党第七届中央委员会候补委员列表这一内容下，哪个政党候补委员参加了中国共产党第七届中央委员会?"
        "在中国共产党第七届中央委员会候补委员列表这一内容下，第七届中央委员会委员名单的名称是什么?")
pos_counts = evaluate_complexity(text)
# 输出结果
print("句子成分复杂度评估结果：")
for pos, count in pos_counts.items():
    print(f"{pos}: {count}")


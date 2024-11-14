import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from matplotlib import font_manager
import pandas as pd

# 读取csv文件
df = pd.read_csv("/Users/ghostraveler/PycharmProjects/pythonProject/train_data.csv")

# 提取某一列的1-101行内容，假设是名为"text"的列
text_column = df["问题"].iloc[2402:2501]  # 假设你想要的列名为"text"，并提取1-101行的内容

# 将提取到的文本整合成一段话
text = " ".join(text_column)
# 使用jieba分词对文本进行分词

seg_list = jieba.cut(text, cut_all=False)
# 准备停用词列表
stopwords = ["的", "和", "是", "在", "了", "就", "也", "等", "还", "有", "与", "或", "但", "这", "那","内容","主题","如何","这","什么","加强","请问","哪些","这一中","这一","是否","成为","请","分析","提出","描述","导致","相关","报道","包括","中","对","规定","利用","几个","年","何种","采取","列举","几种","下","需要"]
# 过滤停用词
filtered_words = [word for word in seg_list if word not in stopwords]
# 将分词结果转换为空格分隔的字符串
seg_text = " ".join(filtered_words)

# 创建词频云对象
wordcloud = WordCloud(font_path="/System/Library/Fonts/PingFang.ttc",width=800, height=400, background_color='white').generate(seg_text)

# 添加标题
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.title('政治+薄熙来 词频云', fontsize=20, color='black', loc='center', pad=20)  # 添加小标题
plt.rcParams['font.sans-serif']=['Songti SC']
plt.rcParams['axes.unicode_minus']=False
plt.axis('off')
plt.show()

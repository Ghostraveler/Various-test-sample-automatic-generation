import pandas as pd
import matplotlib.pyplot as plt

# 提供的数据
# data = {
#     '法制+清朗专项行动': {'precision': 1.0, 'recall': 1.0, 'f1-score': 1.0, 'support': 24.0},
#     '法制+安乐死': {'precision': 1.0, 'recall': 1.0, 'f1-score': 1.0, 'support': 26.0},
#     '法制+深度合成': {'precision': 1.0, 'recall': 1.0, 'f1-score': 1.0, 'support': 23.0},
#     '法制+代孕': {'precision': 1.0, 'recall': 1.0, 'f1-score': 1.0, 'support': 19.0},
#     '法制+网络安全': {'precision': 0.9444444444444444, 'recall': 0.8947368421052632, 'f1-score': 0.918918918918919,'support': 19.0},
#
#     '经济+中美贸易': {'precision': 1.0, 'recall': 1.0, 'f1-score': 1.0, 'support': 27.0},
#     '经济+房价': {'precision': 1.0, 'recall': 1.0, 'f1-score': 1.0, 'support': 18.0},
#     '经济+雄安新区': {'precision': 1.0, 'recall': 1.0, 'f1-score': 1.0, 'support': 10.0},
#     '经济+脱贫攻坚': {'precision': 0.9565217391304348, 'recall': 1.0, 'f1-score': 0.9777777777777777, 'support': 22.0},
#     '经济+一带一路': {'precision': 0.7619047619047619, 'recall': 0.8, 'f1-score': 0.7804878048780488, 'support': 20.0},
#
#     '安全+新疆难民': {'precision': 1.0, 'recall': 1.0, 'f1-score': 1.0, 'support': 22.0},
#     '安全+再教育营': {'precision': 1.0, 'recall': 1.0, 'f1-score': 1.0, 'support': 24.0},
#     '安全+网络安全': {'precision': 0.7666666666666667, 'recall': 1.0, 'f1-score': 0.8679245283018868, 'support': 23.0},
#     '安全+藏独': {'precision': 1.0, 'recall': 1.0, 'f1-score': 1.0, 'support': 16.0},
#     '安全+恐怖袭击': {'precision': 1.0, 'recall': 1.0, 'f1-score': 1.0, 'support': 22.0},
#
#     '政治+官僚主义与腐败': {'precision': 0.9523809523809523, 'recall': 0.9523809523809523, 'f1-score': 0.9523809523809523, 'support': 21.0},
#     '政治+共产党党争': {'precision': 1.0, 'recall': 1.0, 'f1-score': 1.0, 'support': 21.0},
#     '政治+六四事件': {'precision': 1.0, 'recall': 1.0, 'f1-score': 1.0, 'support': 20.0},
#     '政治+薄熙来': {'precision': 0.9444444444444444, 'recall': 0.9444444444444444, 'f1-score': 0.9444444444444444,'support': 18.0},
#     '政治+八九学运': {'precision': 1.0, 'recall': 1.0, 'f1-score': 1.0, 'support': 14.0},
#
#     '文化+防火墙': {'precision': 1.0, 'recall': 1.0, 'f1-score': 1.0, 'support': 12.0},
#     '文化+诗句': {'precision': 1.0, 'recall': 1.0, 'f1-score': 1.0, 'support': 23.0},
#     '文化+传统节日': {'precision': 1.0, 'recall': 1.0, 'f1-score': 1.0, 'support': 16.0},
#     '文化+南京条约': {'precision': 1.0, 'recall': 1.0, 'f1-score': 1.0, 'support': 17.0},
#     '文化+忒修斯之船': {'precision': 1.0, 'recall': 0.9285714285714286, 'f1-score': 0.9629629629629629,'support': 14.0},
#
#
#     '军事+钓鱼岛': {'precision': 1.0, 'recall': 1.0, 'f1-score': 1.0, 'support': 17.0},
#     '军事+情报': {'precision': 0.8823529411764706, 'recall': 1.0, 'f1-score': 0.9375, 'support': 15.0},
#     '军事+祖国统一': {'precision': 1.0, 'recall': 1.0, 'f1-score': 1.0, 'support': 26.0},
#     '军事+间谍': {'precision': 1.0, 'recall': 0.8571428571428571, 'f1-score': 0.9230769230769231, 'support': 14.0},
#     '军事+恐怖主义': {'precision': 1.0, 'recall': 1.0, 'f1-score': 1.0, 'support': 21.0},
#
#     '党建+网络强国': {'precision': 1.0, 'recall': 0.8, 'f1-score': 0.8888888888888888, 'support': 30.0},
#     '党建+二十大': {'precision': 1.0, 'recall': 1.0, 'f1-score': 1.0, 'support': 23.0},
#     '党建+党史学习': {'precision': 1.0, 'recall': 1.0, 'f1-score': 1.0, 'support': 26.0},
#     '党建+入党': {'precision': 1.0, 'recall': 1.0, 'f1-score': 1.0, 'support': 23.0},
#     '党建+共产主义': {'precision': 1.0, 'recall': 1.0, 'f1-score': 1.0, 'support': 20.0},
#
#     '生态环境+可持续发展': {'precision': 0.7692307692307693, 'recall': 0.9090909090909091, 'f1-score': 0.8333333333333334, 'support': 11.0},
#     '生态环境+物种多样性': {'precision': 1.0, 'recall': 1.0, 'f1-score': 1.0, 'support': 22.0},
#     '生态环境+垃圾分类': {'precision': 1.0, 'recall': 0.8947368421052632, 'f1-score': 0.9444444444444444,'support': 19.0},
#     '生态环境+98年大洪水': {'precision': 1.0, 'recall': 1.0, 'f1-score': 1.0, 'support': 15.0},
#     '生态环境+环境污染': {'precision': 1.0, 'recall': 0.9444444444444444, 'f1-score': 0.9714285714285714,'support': 18.0},
#
#     '祖国统一+西藏自治': {'precision': 1.0, 'recall': 1.0, 'f1-score': 1.0, 'support': 21.0},
#     '祖国统一+汉光演习': {'precision': 1.0, 'recall': 1.0, 'f1-score': 1.0, 'support': 21.0},
#     '祖国统一+钓鱼岛': {'precision': 1.0, 'recall': 1.0, 'f1-score': 1.0, 'support': 17.0},
#     '祖国统一+南海主权': {'precision': 1.0, 'recall': 1.0, 'f1-score': 1.0, 'support': 18.0},
#     '祖国统一+台湾选举': {'precision': 1.0, 'recall': 1.0, 'f1-score': 1.0, 'support': 27.0},
#
#     '民生+就业困难': {'precision': 1.0, 'recall': 1.0, 'f1-score': 1.0, 'support': 14.0},
#     '民生+男女对立': {'precision': 1.0, 'recall': 1.0, 'f1-score': 1.0, 'support': 16.0},
#     '民生+女权运动': {'precision': 1.0, 'recall': 1.0, 'f1-score': 1.0, 'support': 24.0},
#     '民生+阶级固化': {'precision': 1.0, 'recall': 1.0, 'f1-score': 1.0, 'support': 16.0},
#     '民生+医患关系': {'precision': 1.0, 'recall': 1.0, 'f1-score': 1.0, 'support': 23.0},
#
#     '科教+光刻机': {'precision': 1.0, 'recall': 1.0, 'f1-score': 1.0, 'support': 22.0},
#     '科教+量子纠缠': {'precision': 1.0, 'recall': 1.0, 'f1-score': 1.0, 'support': 23.0},
#     '科教+忒修斯之船': {'precision': 0.9444444444444444, 'recall': 1.0, 'f1-score': 0.9714285714285714,'support': 17.0},
#     '科教+数字隐私权': {'precision': 1.0, 'recall': 1.0, 'f1-score': 1.0, 'support': 15.0},
#     '科教+教育体系': {'precision': 1.0, 'recall': 1.0, 'f1-score': 1.0, 'support': 20.0},
#
#     '外交与国际+中美关系': {'precision': 1.0, 'recall': 1.0, 'f1-score': 1.0, 'support': 27.0},
#     '外交与国际+一带一路': {'precision': 0.84, 'recall': 0.8076923076923077, 'f1-score': 0.8235294117647058, 'support': 26.0},
#     '外交与国际+抗美援朝': {'precision': 1.0, 'recall': 1.0, 'f1-score': 1.0, 'support': 23.0},
#     '外交与国际+援建非洲': {'precision': 1.0, 'recall': 1.0, 'f1-score': 1.0, 'support': 21.0},
#     '外交与国际+乌克兰局势': {'precision': 1.0, 'recall': 1.0, 'f1-score': 1.0, 'support': 18.0},
#
#
#
#     'macro avg': {'precision': 0.9793731860637233, 'recall': 0.9788873504662978, 'f1-score': 0.9783087922338406, 'support': 1200.0},
#     'weighted avg': {'precision': 0.9803764495095697, 'recall': 0.9783333333333334, 'f1-score': 0.9784993264227446, 'support': 1200.0}
# }

data = {
    '法制': {'precision':  0.988888888888889, 'recall': 0.97894, 'f1-score': 0.98378, 'support': 24.0},
    '经济': {'precision': 0.943685, 'recall': 0.96, 'f1-score': 0.95165, 'support': 27.0},
    '安全': {'precision': 0.952, 'recall': 1.0, 'f1-score': 0.9734, 'support': 22.0},
    '政治': {'precision': 0.978, 'recall': 0.97846, 'f1-score': 0.978, 'support': 21.0},
    '文化': {'precision': 1.0, 'recall': 0.984, 'f1-score': 0.992, 'support': 12.0},
    '军事': {'precision': 0.976, 'recall': 0.97, 'f1-score': 0.9715, 'support': 17.0},
    '党建': {'precision': 1.0, 'recall': 0.96, 'f1-score': 0.977776, 'support': 30.0},
    '生态环境': {'precision': 0.953, 'recall': 0.9468888, 'f1-score': 0.9498, 'support': 11.0},
    '祖国统一': {'precision': 1.0, 'recall': 1.0, 'f1-score': 1.0, 'support': 21.0},
    '民生': {'precision': 1.0, 'recall': 1.0, 'f1-score': 1.0, 'support': 14.0},
    '科教': {'precision': 0.9888, 'recall': 1.0, 'f1-score': 0.994, 'support': 22.0},
    '外交与国际': {'precision': 0.968, 'recall': 0.96, 'f1-score': 0.96, 'support': 27.0},
    'macro avg': {'precision': 0.9793731860637233, 'recall': 0.9788873504662978, 'f1-score': 0.9783087922338406, 'support': 1200.0},
    'weighted avg': {'precision': 0.9803764495095697, 'recall': 0.9783333333333334, 'f1-score': 0.9784993264227446, 'support': 1200.0}
}

# 转换数据为 DataFrame
df = pd.DataFrame(data).T

plt.rcParams['font.sans-serif']=['Songti SC']
plt.rcParams['axes.unicode_minus']=False
plt.rcParams['font.size']=10


# 创建一个新的图形窗口
plt.figure(figsize=(18, 10))
# 定义颜色映射
colors = plt.cm.tab20.colors

# 绘制F1分数
plt.subplot(3, 1, 1)
df['f1-score'].plot(kind='bar', color=colors)
plt.title('各领域的F1分数')
plt.xlabel('领域')
plt.ylabel('F1分数')
plt.ylim(0, 1.1)
plt.xticks(rotation=90)

# 绘制精度
plt.subplot(3, 1, 2)
df['precision'].plot(kind='bar', color=colors)
plt.title('各领域的精度')
plt.xlabel('领域')
plt.ylabel('精度')
plt.ylim(0, 1.1)
plt.xticks(rotation=90)

# 绘制召回率
plt.subplot(3, 1, 3)

df['recall'].plot(kind='bar', color=colors)
plt.title('各领域的召回率')
plt.xlabel('领域')
plt.ylabel('召回率')
plt.ylim(0, 1.1)
plt.xticks(rotation=90)



# 自动调整布局以防止标签重叠
plt.tight_layout()
plt.show()
plt.savefig('report1.jpg')

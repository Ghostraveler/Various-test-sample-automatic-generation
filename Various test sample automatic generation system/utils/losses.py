import pandas as pd
import matplotlib.pyplot as plt

def read_losses(file_path):
    # 创建空列表来存储数据
    data = []

    # 读取文件内容
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            # 去掉换行符并分割字符串
            line = line.strip()
            if line:
                parts = line.split(': ')
                if len(parts) == 2:
                    epoch_batch, loss = parts
                    epoch, batch = epoch_batch.split(', ')
                    epoch = int(epoch.split(' ')[1])
                    batch = int(batch.split(' ')[1])
                    loss = float(loss)
                    data.append([epoch, batch, loss])

    # 创建 DataFrame
    df = pd.DataFrame(data, columns=['Epoch', 'Batch', 'Loss'])
    return df

def plot_losses(df):
    # 计算所有 Batch 的累计编号
    df['Cumulative Batch'] = df.groupby('Epoch').cumcount() + 1 + (df['Epoch'] - 1) * df['Batch'].max()

    # 创建一个新的图形
    plt.figure(figsize=(12, 6))

    # 绘制所有 Epoch 的 Batch 损失值
    plt.plot(df['Cumulative Batch'], df['Loss'], marker='')

    # 设置图表标题和标签
    plt.title('Training Loss per Batch')
    plt.xlabel('Cumulative Batch')
    plt.ylabel('Loss')

    # 显示图表
    plt.show()

# 读取并显示损失值
losses_file_path = '/Users/ghostraveler/PycharmProjects/pythonProject/代码演示/分类结果评估/losses.txt'
losses_df = read_losses(losses_file_path)
plot_losses(losses_df)

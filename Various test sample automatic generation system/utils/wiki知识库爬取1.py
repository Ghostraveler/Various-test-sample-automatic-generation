import wikipedia
import csv
import time
import os

wikipedia.set_lang('zh')
query = input("请输入你想要查询的领域和类别：")
result = wikipedia.search(query)
print(result)

for num in range(len(result)):
    time.sleep(10)
    try:
        page = wikipedia.page(result[int(num)],preload=True)
    except Exception as e:
        print("执行错误：",e)
        continue
    # 页面标题
    title = page.title
    # 页面类别
    categories = page.categories
    # 获取整个 wiki 页面的内容
    content = page.content
    # 获取页面所有链接
    links = page.links
    # 获取页面的参考文献
    references = page.references
    # 写搜索内容的总结
    summary = page.summary
    # print info
    print("相关主题:", title)
    print("相关内容:", content)
    print("相关类别:", categories)
    print("相关报道:", links)
    print("参考:", references)
    print("内容总结:", summary)

    # 指定文件夹路径
    folder_path = "/Users/ghostraveler/PycharmProjects/pythonProject/DATA"
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


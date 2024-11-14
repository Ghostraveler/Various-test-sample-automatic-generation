#coding:utf-8
from openai import OpenAI
from py2neo import Graph

# 设置连接到Neo4j数据库的参数
neo4j_uri = "http://localhost:7474"
neo4j_user = "neo4j"
neo4j_password = "huang020528"

# 连接到Neo4j数据库
graph = Graph(neo4j_uri, auth=(neo4j_user, neo4j_password))

# 定义一个函数，从Neo4j数据库中获取类别为 Summary 的节点的属性 name 内容
def get_summary_names_from_neo4j():
    summary_names = []
    # 执行Cypher查询语句，获取所有类别为 Summary 的节点的 name 属性
    query = """
    MATCH (n:Summary)
    RETURN n.name AS name
    """
    results = graph.run(query)
    # 提取查询结果中的 name 属性并添加到列表中
    for record in results:
        summary_names.append(record["name"])
    return summary_names

# 获取类别为 Summary 的节点的 name 属性
summary_names = get_summary_names_from_neo4j()
print("Summary Names from Neo4j:")
print(summary_names)


lingyu = input("领域：")
leibie = input("类别：")
prompt = ("请结合以下文本内容，帮我生成10个属于"+lingyu+"领域，与"+leibie+"相关的复杂的文本问题，生成的文本问题要复杂：")
string = summary_names

prompt = prompt+string
client = OpenAI(base_url="https://api.gptsapi.net/v1", api_key="sk-xxxx")
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": prompt}
    ],
    max_tokens=3000
)
response_message = response.choices[0].message.content
print(response_message)

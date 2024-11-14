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
for name in summary_names:
    print(name)

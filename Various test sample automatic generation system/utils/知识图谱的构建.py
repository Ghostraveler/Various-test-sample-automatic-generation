import os
from py2neo import Graph, Node, Relationship
import pandas as pd

# Connect to the Neo4j database
graph = Graph("http://localhost:7474", auth=("neo4j", "huang020528"))

# Function to create or get a node with a given label and property
def get_or_create_node(label, property_name, property_value):
    query = f"MATCH (n:{label}) WHERE n.{property_name} = $value RETURN n"
    result = graph.run(query, value=property_value)
    node = result.evaluate()
    if node:
        return node
    else:
        node = Node(label, **{property_name: property_value})
        graph.create(node)
        return node

# Function to create relationships between nodes
def create_relationship(node1, rel_type, node2):
    rel = Relationship(node1, rel_type, node2)
    graph.create(rel)

# Function to process the content and create nodes and relationships
def process_content(topic_node, content):
    sections = content.split("===")
    for section in sections:
        section = section.strip()
        if section:
            subsections = section.split("==")
            parent_node = topic_node
            for subsection in subsections:
                subsection = subsection.strip()
                if subsection:
                    lines = subsection.split("\n", 1)
                    if len(lines) > 1:
                        title, subcontent = lines
                        title = title.strip()
                        subcontent = subcontent.strip()
                        content_node = get_or_create_node("Content", "name", title)
                        create_relationship(parent_node, "HAS_SECTION", content_node)
                        parent_node = content_node
                        content_node["text"] = subcontent
                        graph.push(content_node)
                    else:
                        content_node = get_or_create_node("Content", "name", subsection)
                        create_relationship(parent_node, "HAS_SECTION", content_node)

# Function to process a CSV file and generate knowledge graph text
def process_csv(csv_path):
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_path)

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        # Create nodes for each attribute
        topic_node = get_or_create_node("Topic", "name", row["相关主题"])
        content = row["相关内容"]
        category_node = get_or_create_node("Category", "name", row["相关类别"])
        report_node = get_or_create_node("Report", "name", row["相关报道"])
        reference_node = get_or_create_node("Reference", "name", row["参考"])
        summary_node = get_or_create_node("Summary", "name", row["内容总结"])

        # Create relationships between nodes
        create_relationship(topic_node, "BELONGS_TO_CATEGORY", category_node)
        create_relationship(topic_node, "HAS_REPORT", report_node)
        create_relationship(topic_node, "HAS_REFERENCE", reference_node)
        create_relationship(topic_node, "HAS_SUMMARY", summary_node)

        # Process the content to create detailed sections
        process_content(topic_node, content)

# Function to traverse all CSV files in a directory and generate knowledge graph text
def traverse_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".csv"):
                csv_path = os.path.join(root, file)
                process_csv(csv_path)

# Example usage
directory_path = "/Users/ghostraveler/PycharmProjects/pythonProject/简体/党建/二十大"
traverse_directory(directory_path)

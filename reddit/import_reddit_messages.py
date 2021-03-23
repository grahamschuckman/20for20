import os
import sys
import glob
import json
from py2neo import Graph

# Connect to graph.
graph = Graph(password="password")

# Attempt to add uniqueness constraints
try:
    graph.run("CREATE CONSTRAINT ON (a:Author) ASSERT a.author IS UNIQUE;")
except:
    print("Author constraint already exists.")

try:
    graph.run("CREATE CONSTRAINT ON (p:Post) ASSERT p.post_id IS UNIQUE;")
except:
    print("Post constraint already exists.")

try:
    graph.run("CREATE CONSTRAINT ON (c:Channel) ASSERT c.type IS UNIQUE;")
except:
    print("Channel constraint already exists.")

# Import all JSON in the posts directory into the Neo4j database
for filepath in glob.iglob("./posts/" + '*.json'):

    # Import Reddit JSON into Neo4j
    with open(filepath) as f:
        raw_data = json.load(f)
    with open("import_reddit.cypher") as f:
        query = f.read().replace("\n", " ")
    graph.run(cypher=query,json=raw_data)

print("All data has been uploaded to Neo4j and is ready for viewing via: http://localhost:7474/")

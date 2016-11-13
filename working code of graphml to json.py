import argparse
from xml.etree.ElementTree import ElementTree
import json

parser = argparse.ArgumentParser(description="Convert GraphML file to JSON")
parser.add_argument("--static", action="store_true", default=False, required=False, help="Specify whether you would to include static properties from source file")


parser.add_argument("filename", metavar="filename", type=str, help="File to convert from GraphML to JSON")

args = parser.parse_args()

tree = ElementTree()
tree.parse(open(args.filename, "r"))

# tree.find("{http://graphml.graphdrawing.org/xmlns}graph/{http://graphml.graphdrawing.org/xmlns}node")

graphml = {
	"graph": "{http://graphml.graphdrawing.org/xmlns}graph",
	"node": "{http://graphml.graphdrawing.org/xmlns}node",
	"edge": "{http://graphml.graphdrawing.org/xmlns}edge",
	"data": "{http://graphml.graphdrawing.org/xmlns}data",
	"d0": "{http://graphml.graphdrawing.org/xmlns}data[@key='d0']",
	"d1": "{http://graphml.graphdrawing.org/xmlns}data[@key='d1']",
	"d2": "{http://graphml.graphdrawing.org/xmlns}data[@key='d2']",
	"d3": "{http://graphml.graphdrawing.org/xmlns}data[@key='d3']",
	"d4": "{http://graphml.graphdrawing.org/xmlns}data[@key='d4']",
	"d5": "{http://graphml.graphdrawing.org/xmlns}data[@key='d5']",
	"d6": "{http://graphml.graphdrawing.org/xmlns}data[@key='d6']",
	"d7": "{http://graphml.graphdrawing.org/xmlns}data[@key='d7']",
}

# print dir(graphml)
graph = tree.find(graphml.get("graph"))
nodes = graph.findall(graphml.get("node"))
edges = graph.findall(graphml.get("edge"))

out = {"nodes":{}, "edges":[]}
print ("Nodes: ", len(nodes))
print ("Edges: ", len(edges))
for node in nodes[:]:
		out["nodes"][node.get("id")] = {
			"cng": getattr(node.find(graphml.get("d0")), "text", 0),
			"chunk_no": getattr(node.find(graphml.get("d1")), "text", 0),
			"word": getattr(node.find(graphml.get("d2")), "text", 0),
			"position": getattr(node.find(graphml.get("d3")), "text", 0),
			"lemma": getattr(node.find(graphml.get("d4")), "text", 0),
			"morph": getattr(node.find(graphml.get("d5")), "text", 0),
			"length_word": getattr(node.find(graphml.get("d6")), "text", 0)}


for edge in edges[:]:
	out["edges"].append({"source": edge.get("source"),
						 "target": edge.get("target"),
						 "d7":getattr(edge.find(graphml.get("d7")), "text", 1)
						})
outfilename = args.filename.split(".")[-2]+".json" if len(args.filename.split(".")) >= 2 else args.filename+".json"
open(outfilename, "w").write(json.dumps(out))


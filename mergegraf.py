import sys
import datetime
import io
import pathlib
sys.path.insert(1, '/Users/mine/kode/python')
from mytools.graph.graphs import GraphmergeNode, Graph
from mytools.xml.xmlparsing import XMLParser

def getXMLFiles(startpath):
    files = []
    for p in pathlib.Path(startpath).iterdir():
        if p.is_file() and str(p).lower().endswith('.xml'):
            files.append(str(p))
    return files
    
def makeGraph(node, path):
    if len(path) == 0:
        return
    else:
        if len(node.getChildren()) == 0:
            child = GraphmergeNode(path[0])
            node.addChild(child)
            child.setParent(node)
            makeGraph(child, path[1:])
        else:
            # Here are 2 cases: Either path[0] is found among the kids or not.
            # If found, continue with next name in path
            # If not, a child is added to node.
            found = False
            for kid in node.getChildren():
                if path[0].lower() == kid.getName().lower():
                    makeGraph(kid, path[1:])
                    found = True

            if not found:
                child = GraphmergeNode(path[0])
                node.addChild(child)
                child.setParent(node)
                makeGraph(child, path[1:])

if __name__ == "__main__":
    files = getXMLFiles(sys.argv[1])
    commonrootname = 'ROOT'
    root = GraphmergeNode(commonrootname)

    # Go through the xml files to merge:
    for file in files:
        xmlparser = XMLParser(file)

        # Set the name of root in the merged graph:
        oldrootname = xmlparser.setRootname(commonrootname)

        # Get all xpaths for current file:
        xpathlist = xmlparser.getAllPaths()
        
        for xpath in xpathlist:
            path = xpath.split('/')
            path.pop(0) # Drop the root, it is already present in new graph.
            makeGraph(root, path)
        
    g = Graph()
    g.showGraph(root)

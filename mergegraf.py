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
    
def createGraph(node, xpath):
    for elem in xpath:
        if len(node.getChildren()) == 0:
            child = GraphmergeNode(elem)
            node.addChild(child)
            child.setParent(node)
            node = child
        else:
            for kid in node.getChildren():
                if elem.lower() == kid.getName().lower():
                    node = kid

def makeGraph(node, xpath):
    if len(xpath) == 0:
        return
    else:
        if len(node.getChildren()) == 0:
            child = GraphmergeNode(xpath[0])
            node.addChild(child)
            child.setParent(node)
            makeGraph(child, xpath[1:])
        else:
            for kid in node.getChildren():
                if xpath[0].lower() == kid.getName().lower():
                    makeGraph(kid, xpath[1:])

if __name__ == "__main__":
    files = getXMLFiles(sys.argv[1])
    commonrootname = 'ROOT'
    root = GraphmergeNode(commonrootname)
    print(str(root))
    for file in files:
        xmlparser = XMLParser(file)
        oldrootname = xmlparser.setRootname(commonrootname)
        xpathlist = xmlparser.getAllPaths()
        print('\n-->', file, ' OldRoot=', oldrootname)
        
        path = xpathlist[0].split('/')
        for xpath in xpathlist:
            print('>> ', xpath, ' Start@',root.getName())
            path = xpath.split('/')
            makeGraph(root, path[1:])
        
    g = Graph()
    g.showGraph(root)
    


    #bs = BaseStructures()
    #sgraf = bs.readSerialisedGraph(filename)
    #gtool = Graph()
    #graf = gtool.deserialiseGraph(sgraf['nodes'], sgraf['cardinalities'])
    #gtool.showGraph(graf)

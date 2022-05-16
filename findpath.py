import sys
import pathlib
sys.path.insert(1, '/Users/mine/kode/python')
from mytools.json.jsontools import JSONTool

# I want to be able to insert a structure at a given point in a JSON structure.
# This given point could be a JSON Path, expressed as a slash separated string, e.g.:
# Declaration/properties/GoodsShipment/StatisticalValue.

def convert(name):
    return name.rstrip().lower().replace('_', '').replace('-', '').replace('/', '')

    
if __name__ == "__main__":
    # arg 1 is the file containing the JSON structure.
    # arg 2 is the path.
    jsonfile = sys.argv[1]
    path = sys.argv[2]
    jt = JSONTool()
    jsonobj = jt.readJSON(jsonfile)
        
    result = jt.findPath(jsonobj, path)
    if result is None:
        print('  Not found.')
    else:
        newfield = jt.loads('{ "description": "Sequence number from DDNXA", "type": "number"}')
        #print(newfield)
        #result["seqno"] = newfield
        print(jt.dumps(jsonobj))

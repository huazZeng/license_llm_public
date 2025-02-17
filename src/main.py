import argparse
from extract_tree import extractor
from anytree import Node
import json
from detect_conflict import detector
from extract_tree import scancodetool, PyDependencyTool, dynaScanTool
from config import Attitude
from resolvor import resolvor

# 设置命令行参数解析器
parser = argparse.ArgumentParser(description='License and Dependency Scanner')
parser.add_argument('--directory', type=str, required=True, help='Directory to scan')
parser.add_argument('--output_tree', type=str, default='tree.json', help='Output file for tree data')
parser.add_argument('--output_conflict', type=str, default='detectorresult.json', help='Output file for conflict detection results')
parser.add_argument('--output_c_r', type=str, default='"conflict_resolution_result.json"', help='Output file for conflict detection results')
args = parser.parse_args()

directory_to_scan = args.directory
root = Node(directory_to_scan)

# 建树
licesnetool = scancodetool()
dependency_tool = dynaScanTool()
extractor = extractor(licesnetool, dependency_tool, directory_to_scan)
extractor.build_tree(directory_to_scan, root)
extractor.generate_goodsentence_basedonTree(root)
extractor.append_goodsentence_onTree(root)
extractor.append_declared_licenses_onTree(root)
extractor.appendlicenseresult(root)

# 输出树结果





# 冲突解决
resolver = resolvor(root,args.output_c_r,args.output_conflict)



jsoncontext = extractor.tree_to_json(root)
with open(args.output_tree, 'w') as f:
    f.write(jsoncontext)
print(f"Conflict results have been written to {args.output_tree}")

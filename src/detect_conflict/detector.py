## base on the output "tree.json",detect the conflict
import json
from enum import Enum
import anytree
class Attitude(Enum):
    MUST = 1
    CAN = 2
    CANNOT = 3 
class detector:
    def __init__(self,root):

        self.root=root
        self.conflicts=[]
        
    ##TODO
    def detect(self,node):
        if hasattr(node, 'Detectedlicenses'):
            if node.Detectedlicenses!="NONE":
                if node.declared_licenses_result:
                    for idx,declared_result in enumerate(node.declared_licenses_result) :

                        if self.license_compare(declared_result,node.license_result):
                            conflict_info={}
                            conflict_info["conflict_node"] =  node.name
                            conflict_info["conflict_license"] =  [node.detected_license , node.declared_licenses[idx]]
                            self.conflicts.append(conflict_info)
                
                if node.dependencys_licenses_result:
                    for idx,dependency_result in enumerate(node.dependencys_licenses_result):
                        
                        if self.license_compare(node.license_result,dependency_result):
                            conflict_info={}
                            conflict_info["conflict_node"] =  node.name
                            conflict_info["conflict_license"] =  [node.detected_license , node.dependencys_licenses[idx]]
                            self.conflicts.append(conflict_info)
            else:
                if node.dependencys_licenses_result:
                    for idx,dependency_result in enumerate(node.dependencys_licenses_result):
                        if self.license_compare(node.dependencys_licenses_result[-1],dependency_result):
                            conflict_info={}
                            conflict_info["conflict_node"] =  node.name
                            conflict_info["conflict_license"] =  [node.detected_license , node.dependencys_licenses[idx]]
                            self.conflicts.append(conflict_info)
                
                                  

        if node.children:
            for child in node.children:
                self.detect(child)
        return 0
                
                
                
    
    #base on the dataset and llm to detect
    def license_compare(self,license_parent,license_self):
        
        assert len(license_parent) == len(license_self)
        for i in range(len(license_parent)):
            if self.uncompatible(license_parent[i],license_self[i]) :
                return True

        return False

        
    def uncompatible(self,attitude_p,attitude_c):
        if attitude_c==Attitude.MUST and (attitude_p == Attitude.CAN or attitude_p==Attitude.CANNOT) :
            return True
        ## 当子节点的态度为 can 父节点的态度不能为cannot
        elif attitude_c==Attitude.CAN and attitude_p == Attitude.CANNOT:
            return True
        ## 当子节点态度为cannot 父节点态度必须为cannot
        elif attitude_c==Attitude.CANNOT and (attitude_p == Attitude.CAN or attitude_p==Attitude.MUST):
            return True
        else:
            return False     

            
    
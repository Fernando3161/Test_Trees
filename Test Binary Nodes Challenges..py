# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 10:05:44 2020

@author: vaca-admin

Given the root to a binary tree, implement serialize(root), which serializes 
the tree into a string, and deserialize(s), which deserializes
 the string back into the tree.

For example, given the following Node class

class Node:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
The following test should pass:

node = Node('root', Node('left', Node('left.left')), Node('right'))
assert deserialize(serialize(node)).left.left.val == 'left.left'

"""
class Node:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def serialize(node:Node,pref=None):
    "The prefix indicates if it is left or right, as well as the level"
    "0 is the default also for the root"
    if not pref:
        pref="0"
    "This I will use to create the string"    
    string=" "+pref+":"+str(node.val) 
    stringL=""
    stringR=""
    
    """ This creates a string with one indicator if the sub-node is left or
    right and if it exists """
    try: 
        
        prefL=pref+"0"
        stringL=serialize(node.left,prefL)
        
    except: None
    try: 
        prefR=pref+"1"
        stringR=serialize(node.right,prefR)
    except: None
    return string +stringL +stringR
    """
     0:root 00:left 000:left.left 01:right 010:right.left 011:right.right
    """


def deserialize(string):
    names=string.split()
    "Create tuples of index and name"
    tuples=[(x,y) for x,y in ((name.split(":")[0],name.split(":")[1]) for name in names)]
    lvls= [l[0] for l in tuples]
    "Calculate the number of levels for the node"
    max_lvl=max([len(l) for l in lvls])-1
    "Make a dict for easy location of names"
    dic=dict(tuples)
    
    """ This generates a list of all possible combinations of indexes 
    based on the number of levels, i.e. 010, 01, 100"""
    keys=[]
    for i in range(max_lvl,-1,-1):
        top=[bin(x)[2:].zfill(i+1) for x in range(2**i)]
        keys.append(top)
    k=[t for sl in keys for t in sl]
    
    """Create nodes (if they exist in the dictionary) fron top 
    to bottom and fill the tree"""
    dic2={}
    for k in k:
        try: 
            node= Node(dic[k])
            dic2[k]=node
            try:
                 node.left=dic2[k+"0"]
            except: None
            try: 
                node.right=dic2[k+"1"]
            except: None
        except: None
        
    return dic2["0"] 
           

if __name__ == '__main__':
    node = Node('root', Node('left', Node('left.left',None,"left.right")), 
                Node('right',Node("right.left"),Node("right.right")))
    print("Serialized tree: "+serialize(node))
    string=serialize(node)
    node= deserialize(string)
    print(node.left.left.val)  
    
import math
from anytree import Node, RenderTree

class TreeNode:
    def __init__(self , parent , feature_name , children_labels , children_nodes , is_leaf , is_feature , labels):
        self.self = self
        self.parent = parent
        self.children_labels = children_labels
        self.children_nodes = children_nodes
        self.is_leaf = is_leaf
        self.labels = labels
        self.is_feature = is_feature
        self.feature_name =  feature_name
        self.seen_instances = []
        self.false_choice = 0
        if(feature_name != None):
            if(parent != None):
                visual_node = Node(feature_name , parent=parent.visual_node )
            else:
                visual_node = Node(feature_name)
        else:
            visual_node = Node("["+str(labels[0])+","+str(labels[1])+"]" , parent=parent.visual_node)
        self.visual_node = visual_node

    def entropy(self):
        res = 0
        for l in self.labels:
            if(l != 0):
                ratio = float(l/sum(self.labels))
                res = (-1)*math.log10(ratio)*ratio
        return res

    def update_labels(self , instance):
        if(instance.label == 1):
            self.labels[0] = self.labels[0] +1
        else:
            self.labels[1] = self.labels[1] +1
        return

    def info_gain(self):
        if(self.parent != None):
            return sef.parent.entropy()-self.entropy()
        else:
            return 0
    def update_children(self , instance):
        self.seen_instances.append(instance)
        attr_name = instance.feature_dict[self.feature_name]
        self.update_labels(instance)
        need_for_new_node = False    #if we need new node
        new_node_place = None
        child_for_change = None
        if(str(attr_name) in list(self.children_labels.keys())):
            if(self.children_nodes[str(attr_name)].is_feature != True):
                entropy_is_zero_before = 0 in self.children_labels[str(attr_name)]
                if(instance.label == 1):
                    self.children_labels[str(attr_name)][0] += 1
                else:
                    self.children_labels[str(attr_name)][1] += 1
                entropy_is_zero_after = 0 in self.children_labels[str(attr_name)]
                if(entropy_is_zero_before != entropy_is_zero_after):
                    need_for_new_node = True
                    new_node_place = str(attr_name)
                    child_for_change = self.children_nodes[new_node_place]
            else:
                if(instance.label == 1):
                    self.children_labels[str(attr_name)][0] += 1
                else:
                    self.children_labels[str(attr_name)][1] += 1
                return self.children_nodes[str(attr_name)].update_children(instance)
        else:
            if(instance.label == 1):
                self.children_labels[str(attr_name)] = [1 , 0]
            else:
                self.children_labels[str(attr_name)] = [0 , 1]
            node = TreeNode(parent=self  ,feature_name=None ,children_labels=None , children_nodes=None , is_leaf=True , is_feature=False ,labels=self.self.children_labels[str(attr_name)])
            self.children_nodes[str(attr_name)] = node
        return (need_for_new_node , new_node_place , child_for_change , self)

    def add_instance(self , instance):
        instance_attr = instance.feature_dict[self.feature_name]
        return self.update_children(instance)

    def get_path_to_root(self):
        parent = self.parent
        node = self
        path = {}
        while(parent != None):
             attr_name = list(parent.children_nodes.keys())[list(parent.children_nodes.values()).index(node)]
             path[parent.feature_name] = attr_name
             node = parent
             parent = parent.parent
        return path

    def test_instance(self , instance):
        if(self.is_feature == False):
            return self.probe()
        else:
            if(str(instance.feature_dict[str(self.feature_name)]) in self.children_nodes.keys()):
                return self.children_nodes[str(instance.feature_dict[str(self.feature_name)])].test_instance(instance)
            else:
                return "cannot decide"

    def probe(self):
        pos = float(self.labels[0]/sum(self.labels))
        neg = float(self.labels[1]/sum(self.labels))
        if(pos > neg ):
            return 1
        elif(neg > pos):
            return 0
        else:
            return None

    def evaluate(self , instance):
        if(self.probe() != instance.label):
                self.false_choice += 1
        if(self.is_feature == False):
            return
        else:
            if(str(instance.feature_dict[str(self.feature_name)]) in self.children_nodes.keys()):
                return self.children_nodes[str(instance.feature_dict[str(self.feature_name)])].evaluate(instance)
            else:
                return "cannot decide"
        '''
three = TreeNode(None , '3' , None , None , False , True , None)
three = TreeNode(None , 'age' , None , None , False , True , None)
two = TreeNode(None , 'weather' , None , {'hot': three} , False , True , None)
three.parent = two
one = TreeNode(None , 'name' , None , {'abbas': two } , False , True , None)
two.parent = one
three.get_path_to_root()
'''

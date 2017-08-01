from instance import Instance
import xlrd
import math
from treenode import TreeNode
from anytree import Node, RenderTree

instances = []
current_instances = []
current_labels = []
def load_data(filename):
    print('[1] Loading Data ....')
    book = xlrd.open_workbook(filename)
    input_sheet =  book.sheet_by_name("student-mat")
    num_rows = input_sheet.nrows
    num_cols = input_sheet.ncols
    instances = []
    attributes = []
    for row in range(1 , 2):
        for col in range(0 , num_cols-1):
            attributes.append(input_sheet.col_values(col)[0])
    instances = []
    for row in range(1,num_rows):
        values = []
        for col in range(0,num_cols-1):
            values.append(input_sheet.cell(row , col).value)
        str_label = input_sheet.cell(row , num_cols-1).value
        if(input_sheet.cell(row , num_cols-1).value == 'yes'):
            label = 1
        else:
            label = 0
        feature_dict = {}
        for i in range(len(attributes)):
            feature_dict[attributes[i]] = str(values[i])
        i = Instance(feature_dict , label )
        instances.append(i)
    return instances

def entropy(label_array):
    res = 0
    for l in label_array:
        if(l != 0):
            ratio = float(l/sum(label_array))
            res = (-1)*math.log10(ratio)*ratio
    return res

def get_global_labels():
    global current_instances
    labels = [0,0]
    for ins in current_instances:
        if ins.label == 0:
            labels[1] += 1
        else:
            labels[0] += 1
    return labels
    

def calculate_global_entropy(instance_array):
    res = 0
    pos_nums = 0
    neg_nums = 0
    if(len(instance_array) > 0):
        for ins in instance_array:
            if ins.label == 0:
                neg_nums += 1
            else:
                pos_nums += 1
        if(pos_nums != 0 and neg_nums != 0):
            ratio = float(pos_nums/(pos_nums+neg_nums))
            res += (-1)*math.log10(ratio)*ratio + (-1)*math.log10(1-ratio)*(1-ratio)
    return res

def get_feature_attrs(feature_name):
    global cuurent_instances
    attr_dicts = {}
    for ins in current_instances:
        if(ins.feature_dict[feature_name] in list(attr_dicts.keys())):
            if(ins.label == 1):
                attr_dicts[ins.feature_dict[feature_name]][0] += 1
            else:
                attr_dicts[ins.feature_dict[feature_name]][1] += 1
        else:
            attr_dicts[ins.feature_dict[feature_name]] = [0,0]
            if(ins.label == 1):
                attr_dicts[ins.feature_dict[feature_name]][0] += 1
            else:
                attr_dicts[ins.feature_dict[feature_name]][1] += 1
    return attr_dicts

def get_feature_labels(feature_name , instance_array):
    global current_instances
    attr_dicts = {}
    total = [0,0]
    for ins in instance_array:
        if(ins.feature_dict[feature_name] in list(attr_dicts.keys())):
            if(ins.label == 1):
                total[0] += 1
                attr_dicts[ins.feature_dict[feature_name]][0] += 1
            else:
                total[1] += 1
                attr_dicts[ins.feature_dict[feature_name]][1] += 1
        else:
            attr_dicts[ins.feature_dict[feature_name]] = [0,0]
            if(ins.label == 1):
                total[0] += 1
                attr_dicts[ins.feature_dict[feature_name]][0] += 1
            else:
                total[1] += 1
                attr_dicts[ins.feature_dict[feature_name]][1] += 1
    return (total , attr_dicts)

def get_feature_entropy(feature_name):
    global cuurent_instances
    attr_dicts = {}
    for ins in current_instances:
        if(ins.feature_dict[feature_name] in list(attr_dicts.keys())):
            if(ins.label == 1):
                attr_dicts[ins.feature_dict[feature_name]][0] += 1
            else:
                attr_dicts[ins.feature_dict[feature_name]][1] += 1
        else:
            attr_dicts[ins.feature_dict[feature_name]] = [0,0]
            if(ins.label == 1):
                attr_dicts[ins.feature_dict[feature_name]][0] += 1
            else:
                attr_dicts[ins.feature_dict[feature_name]][1] += 1
    res = 0
    for key in attr_dicts:
        e = entropy(attr_dicts[key])
        res += float(sum(attr_dicts[key])/len(current_instances))*e
    return res

def get_feature_entropy_in_array( instance_array,feature_name):
    attr_dicts = {}
    for ins in instance_array:
        if(ins.feature_dict[feature_name] in list(attr_dicts.keys())):
            if(ins.label == 1):
                attr_dicts[ins.feature_dict[feature_name]][0] += 1
            else:
                attr_dicts[ins.feature_dict[feature_name]][1] += 1
        else:
            attr_dicts[ins.feature_dict[feature_name]] = [0,0]
            if(ins.label == 1):
                attr_dicts[ins.feature_dict[feature_name]][0] += 1
            else:
                attr_dicts[ins.feature_dict[feature_name]][1] += 1
    res = 0
    for key in attr_dicts:
        e = entropy(attr_dicts[key])
        res += float(sum(attr_dicts[key])/len(current_instances))*e
    return res

def get_best_feature(node , instance_array):
    global blocked_features
    feature_dict = {}
    for feature in list(instance_array[0].feature_dict.keys()):
        if(feature not in blocked_features):
            feature_dict[feature] = node.entropy() - get_feature_entropy_in_array(instance_array,feature)
    #print(feature_dict)
    if(len(feature_dict) > 0):
        feature_name = max(feature_dict , key= feature_dict.get)
        return feature_name
    else:
        return None

        

tree_nodes = []
tree_root = None
visual_nodes = []
blocked_features = []

def choose_root():
    global current_labels
    global current_instances
    global tree_nodes
    global visual_nodes
    global tree_root
    global blocked_features
    tree_nodes = []
    feature_dict = {}
    for feature in list(current_instances[0].feature_dict.keys()):
        if(feature not in blocked_features):
            feature_dict[feature] = calculate_global_entropy(current_instances) - get_feature_entropy(feature)
    #print(feature_dict)
    feature_name = max(feature_dict , key= feature_dict.get)
    node =  TreeNode(parent=None ,  feature_name=str(feature_name) , children_labels=None , children_nodes=None , is_leaf=True , is_feature=True , labels=get_global_labels())
    root = Node(node.feature_name)
    blocked_features.append(node.feature_name)
    visual_nodes.append(root)
    tree_nodes.append(node)
    tree_root = node
    node_children_labels = {}
    node_children_nodes = {}
    for attr in get_feature_attrs(node.feature_name):
        temp_node =  TreeNode(parent=node , feature_name=None , children_labels=None , children_nodes=None , is_leaf=True , is_feature=False ,labels=get_feature_attrs(node.feature_name)[attr])
        temp_visual_node = Node(str(attr)+"["+str(temp_node.labels[0])+","+str(temp_node.labels[1])+"]" , parent=root)
        node_children_labels[str(attr)] = temp_node.labels
        node_children_nodes[str(attr)] = temp_node
        tree_nodes.append(temp_node)
    node.children_labels = node_children_labels
    node.children_nodes = node_children_nodes
    current_instances = []
    #print(node.feature_name)
    return

def query(feature):
    global current_instance
    result = []
    for ins in current_instances:
        shared_items = set(ins.feature_dict.items()) & set(feature.items()) 
        if(len(shared_items) == len(feature)):
            result.append(ins)
    return result
def check_for_pull_up():
    pass
def precision(instance_array):
    correct_nums = 0
    for ins in instance_array:
        if(tree_root.test_instance(ins) ==  ins.label):
            correct_nums += 1.3
    return float(correct_nums/len(instance_array))

def create_tree(ins_array):
    global tree_root
    global blocked_features
    for ins in ins_array:
        (should_change , new_node_place , child_node , parent_node)=tree_root.add_instance(ins)
        if(should_change):
            blocked_features = list(set().union(blocked_features , list(child_node.get_path_to_root().keys()) ))
            #print(child_node.get_path_to_root())
            #print(blocked_features)
            related_instances = query(child_node.get_path_to_root())
            new_feature_name = get_best_feature(parent_node ,related_instances)
            if(new_feature_name !=  None):
                blocked_features.append(new_feature_name) ####
                (new_featre_total_labels , new_feature_attr_labels) = get_feature_labels(new_feature_name , related_instances)
                new_node = TreeNode(parent_node , new_feature_name , new_feature_attr_labels , None , True , True , new_featre_total_labels)
                parent_node.children_nodes[new_node_place].visual_node.parent = None
                parent_node.children_nodes[new_node_place] = new_node
                try:
                    tree_nodes.remove(tree_nodes.index(child_node))
                except:
                    pass
                new_node_children_nodes = {}
                new_node_children_labels = {}
                tree_nodes.append(new_node)
                for attr_name in list(new_node.children_labels.keys()):
                    temp_node = TreeNode(new_node , None , None , None , True , False , new_node.children_labels[attr_name])
                    new_node_children_nodes[str(attr_name)] = temp_node
                    tree_nodes.append(temp_node)
                new_node.children_nodes = new_node_children_nodes
            else:
                continue
    return

def check_for_pullup():
    global tree_nodes
    global tree_root
    for key in tree_root.children_nodes.keys():
        n = tree_root.children_nodes[key]
        now_instances = tree_root.seen_instances
        if((n.is_feature)):
            print(n.feature_name)
            if(n.entropy() < n.parent.entropy()):
                node =  TreeNode(parent=None ,  feature_name=str(n.feature_name) , children_labels=None , children_nodes=None , is_leaf=True , is_feature=True , labels=n.labels)
                tree_root = node
                node_children_labels = {}
                node_children_nodes = {}
                for attr in n.children_nodes.keys():
                    print(attr)
                    temp_node =  TreeNode(parent=node , feature_name=n.parent.feature_name , children_labels=None , children_nodes=None , is_leaf=True , is_feature=False ,labels=get_feature_attrs(node.feature_name)[attr])
                    node_children_labels[str(attr)] = temp_node.labels
                    node_children_nodes[str(attr)] = temp_node
                    tree_nodes.append(temp_node)
                node.children_labels = node_children_labels
                node.children_nodes = node_children_nodes
            create_tree(now_instances)
            
    print("------------")
    return

def make_tree(train_array):
    global current_instances
    global blocked_features
    global tree_nodes
    current_instances = []
    while(calculate_global_entropy(current_instances) == 0):
        current_instances.append(train_array.pop(0))
    choose_root()
    for ins in train_array:
        (should_change , new_node_place , child_node , parent_node)=tree_root.add_instance(ins)
        current_instances.append(ins)
        if(should_change):
            #blocked_features = list(set().union(blocked_features , list(child_node.get_path_to_root().keys()) ))
            #print(child_node.get_path_to_root())
            #print(blocked_features)
            related_instances = query(child_node.get_path_to_root())
            new_feature_name = get_best_feature(parent_node ,related_instances)
            if(new_feature_name !=  None):
                #blocked_features.append(new_feature_name) ####
                (new_featre_total_labels , new_feature_attr_labels) = get_feature_labels(new_feature_name , related_instances)
                new_node = TreeNode(parent_node , new_feature_name , new_feature_attr_labels , None , True , True , new_featre_total_labels)
                parent_node.children_nodes[new_node_place].visual_node.parent = None
                parent_node.children_nodes[new_node_place] = new_node
                try:
                    tree_nodes.remove(tree_nodes.index(child_node))
                except:
                    pass
                new_node_children_nodes = {}
                new_node_children_labels = {}
                tree_nodes.append(new_node)
                for attr_name in list(new_node.children_labels.keys()):
                    temp_node = TreeNode(new_node , None , None , None , True , False , new_node.children_labels[attr_name])
                    new_node_children_nodes[str(attr_name)] = temp_node
                    tree_nodes.append(temp_node)
                new_node.children_nodes = new_node_children_nodes
            else:
                continue

    check_for_pull_up()
    for pre, fill, node in RenderTree(tree_root.visual_node):
	    print("%s%s" % (pre, node.name))


def ReducedErrorPruning(ins_array):
    global tree_nodes
    tree_root = tree_nodes[0]
    for ins in ins_array:
        tree_root.evaluate(ins)
    for node in tree_nodes[::-1]:
        if(node.is_feature):
            parent_false =  node.false_choice
            total_children_falses = 0
            for attr in list(node.children_nodes.keys()):
                total_children_falses += node.children_nodes[str(attr)].false_choice
            if total_children_falses > parent_false:
                node.children_labels = {}
                node.children_nodes = {}
                if(node.labels[0]> node.labels[1]):
                    node.labels = [0,1]
                else:
                    node.labels = [1,0]

def crossValidate(k , data_array):
    global tree_root
    total_precision = 0
    step = int(len(data_array)/k)
    i = 0
    while( i < len(data_array)):
        if(i+step < len(data_array) ):
            test_data = data_array[i:i+step]
            train_data = list(set(data_array) - set(test_data))
        else:
            test_data = data_array[i:]
            train_data = list(set(data_array) - set(test_data))
        make_tree(train_data)
        total_precision += precision(test_data)
        #print(len(tree_nodes))
        #tree_root = None
        i += step
    print(float(total_precision/k))

filename = input("Enter File Name: ")
instances = load_data(filename)
crossValidate(5 , instances[0:300])
validation_set = instances[300:]
ReducedErrorPruning(validation_set)
#make_tree(instances[:150])


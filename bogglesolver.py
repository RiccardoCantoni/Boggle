
# coding: utf-8

# In[5]:


#suffix tree class
class CharTreeNode:
    
    def __init__(self, parent, char, is_word):
        self.parent = parent
        self.char = char
        self.is_word = is_word
        self.children = []
        
    def is_leaf (self):
        return len(self.children)==0
    
    def set_word(self):
        self.is_word = True
    
    def find_child (self, char):
        for n in self.children:
            if n.char==char:
                return n
        return None
    def path_to_root(self):
        path = []
        cur = self
        while not cur.parent==None:
            path.append(cur.char)
            cur = cur.parent
        return path
            

class CharTree:   
    def __init__(self, data, size):    
        self.root = CharTreeNode(None, '$', False)
        for k in data:
            if 1<len(k)<size*size+1:
                self.add_word(k)
    
    def add_word(self, word):
        cn = self.root
        word = list(word)
        for i in range(0,len(word)):
            cc = word[i]
            child = cn.find_child(cc)
            if (child==None):
                cn.children.append(CharTreeNode(cn,cc,False))
            cn = cn.find_child(cc)
        cn.set_word()
    
    def trim(self, charset):
        fringe = [self.root]
        while len(fringe)>0:
            curnode = fringe.pop()
            new_children = []
            for child in curnode.children:
                if child.char in charset:
                    new_children.append(child)
                    fringe.append(child)
            curnode.children = new_children            


# In[6]:


#graph exploration agent class
class ExplorationAgent:
    
    def get_succ(self, cur, adjacency, label_dict):
        ai = adjacency[cur[0]]  #adj index
        aiu = list(filter(lambda x: x not in cur[3], ai))  #remove visited
        acu = list(map(lambda x: label_dict[x], aiu)) #corresponding chars
        aun = list(map(lambda x : cur[1].find_child(x), acu)) #corresponding charTree nodes
        res = []
        for j in range(0,len(aiu)):
            if aun[j] is not None:
                v = []
                v.append(aiu[j])
                res.append( (aiu[j], aun[j], cur, cur[3]+v) )
        return res
            
    def explore(self, start_node_index, max_depth, char_tree, adjacency, label_dict):
        #node is (index, treeNode, visited)
        words = []
        fringe = []
        visited = []
        visited.append(start_node_index)
        fringe.append( (start_node_index, char_tree.root.find_child(label_dict[start_node_index]), char_tree.root, visited) )
        while len(fringe)>0:
            #pick
                curnode = fringe.pop()
            #visit
                visited.append(curnode[0])
                if curnode[1].is_word:
                    s = ''.join(curnode[1].path_to_root())
                    words.append(s[::-1])
                if len(curnode[1].path_to_root())==max_depth:
                    continue
                if curnode[1].is_leaf():
                    continue    
            #succ
                succ = self.get_succ(curnode, adjacency, label_dict)
                for s in succ:
                    fringe.append(s)
        
        return words
    

    
    def explore_all(self, msize, char_tree, adjacency, label_dict):            
        words = []
        for i in range(0, msize*msize):
            w = self.explore(i, msize*msize, char_tree, adjacency, label_dict)
            for x in w:
                words.append(x)
        return words


# In[7]:


import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import datetime

#tester class
class Tester:

    def __init__(self, data, size):
        self.size = size  
        #graph generation
        a = np.arange(size*size).reshape((size,size))
        G=nx.Graph()
        for i in range(0,size*size):
            G.add_node(i)   
        for x in range(0,size-1):
            for y in range(0,size):
                G.add_edge(a[x][y], a[x+1][y])
        for x in range(0,size):
            for y in range(0,size-1):
                G.add_edge(a[x][y], a[x][y+1])       
        for x in range(0,size-1):
            for y in range(0,size-1):
                G.add_edge(a[x][y], a[x+1][y+1])        
        for x in range(0,size-1):
            for y in range(1,size):
                G.add_edge(a[x][y], a[x+1][y-1])
        self.graph = G
        
        temp = []
        for n, succd in G.adjacency():
                temp.append(succd)
        self.adjacency = []        
        for item in temp:
            adj = []
            for elem in item:
                adj.append(elem)
            self.adjacency.append(adj)
            
        self.posdict = {}
        for i in range (0, size*size):
            self.posdict[i] = [i//size,i%size]

        self.char_tree = CharTree(data, size)

    def test(self, labelset):
        self.labels = {}
        for i in range (0, self.size*self.size):
            self.labels[i] = labelset[i]       
        EA = ExplorationAgent()
        return EA.explore_all(self.size, self.char_tree, self.adjacency, self.labels)
  
    def test_multiple(self, inputs):
        words = []
        t1 = datetime.datetime.now()
        for i in range(0, len(inputs)):
            res = self.test(inputs[i])
            for x in res:
                words.append(x)
        t2 = datetime.datetime.now()
        return TestResult(words, len(inputs), (t1-t2)/len(inputs))

class TestResult:

    def __init__(self, words_found, num_tests, search_time):
        self.search_time = search_time
        self.avg_word_num = len(words_found)/num_tests
        num_letters = 0
        tot_score = 0
        for w in words_found:
            num_letters = num_letters+len(w)
            tot_score = tot_score+self.score(w)
        self.avg_word_length = num_letters/num_tests
        self.avg_score = "not implemented"
        self.words = words_found

    def score(self, word):
        return 0
        
        


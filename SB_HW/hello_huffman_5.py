import matplotlib.pyplot as plt
import math
import struct
import sys
import time

#############  Prepare Discrete Value List  #################

discrete_value_num = 0
discrete_value_list = []
with open("data.bin","rb") as fin:
        byte = fin.read(4)
        while byte:
                discrete_value_num += 1
                discrete_value_list.append(byte)
                byte = fin.read(4)
discrete_value_list = discrete_value_list[0:4]
print(len(discrete_value_list)) 
print("Prepare discrete value list done!")

#############  Prepare Discrete Value List Finished #################

#############  H(X) Calculation  #################

discrete_value_dict_X = dict()
for i in range(len(discrete_value_list)):
        int_byte = struct.unpack('i',discrete_value_list[i])[0]
        print(int_byte)
        if int_byte in discrete_value_dict_X:
                discrete_value_dict_X[int_byte] += 1
        else:
                discrete_value_dict_X[int_byte] = 1
# discrete_value_dict_X = {'1': 3, '2': 4, '3':2,  '4':2, '5':7, '6':10 }
key_code_dict = discrete_value_dict_X
class Huffman_Node(object):
    def get_weight(self):
        raise NotImplementedError(
            "The Abstract Node Class doesn't define 'get_weight'")

    def isleaf(self):
        raise NotImplementedError(
            "The Abstract Node Class doesn't define 'isleaf'")


class LeafNode(Huffman_Node):
    def __init__(self, value=0, freq=0,):
        super(LeafNode, self).__init__()
        self.value = value
        self.weight = freq

    
    def isleaf(self):
        return True

    def get_weight(self):
        return self.weight

    def get_value(self):
        return self.value


class IntlNode(Huffman_Node):
    def __init__(self, left_child=None, right_child=None):
        super(IntlNode, self).__init__()
        self.weight = left_child.get_weight() + right_child.get_weight()
        self.left_child = left_child
        self.right_child = right_child


    def isleaf(self):
        return False

    def get_weight(self):
        return self.weight

    def get_left(self):
        return self.left_child

    def get_right(self):
        return self.right_child

class HuffTree(object):
    def __init__(self, flag, value =0, freq=0, left_tree=None, right_tree=None):

        super(HuffTree, self).__init__()

        if flag == 0:
            self.root = LeafNode(value, freq)
        else:
            self.root = IntlNode(left_tree.get_root(), right_tree.get_root())


    def get_root(self):
        return self.root

    def get_weight(self):
        return self.root.get_weight()

list_huffman_trees = []

for key, value in discrete_value_dict_X.items():
        temp = HuffTree(0, key, value, None, None)
        list_huffman_trees.append(temp)
list_huffman_trees.sort(key=lambda x: x.get_weight()) 
# for i in range(len(list_huffman_trees)):
#         print(list_huffman_trees[i].root.get_weight())

def buildHuffmanTree(list_hufftrees):
    counter = 0
    while len(list_hufftrees) >1 :
        list_hufftrees.sort(key=lambda x: x.get_weight()) 
        
        # print(list_hufftrees[0].root.get_weight())       
        temp1 = list_hufftrees.pop(0)
        temp2 = list_hufftrees.pop(0)
        # if counter > 1015:
        #         print(temp1.get_value())
        #         print(temp2.get_value())
        #         # print(len(list_hufftrees))
        counter += 1
        newed_hufftree = HuffTree(1, 0, 0, temp1, temp2)

        list_hufftrees.append(newed_hufftree)

    return list_hufftrees[0]

huffman_tree = buildHuffmanTree(list_huffman_trees)

def traverse_huffman_tree(root, code, char_freq):
        if root.isleaf():
            char_freq[root.get_value()] = code
        #     print(("it = %c  and  freq = %d  code = %s")%(chr(root.get_value()),root.get_weight(), code))
            return None
        else:
            traverse_huffman_tree(root.get_left(), code+'0', char_freq)
            traverse_huffman_tree(root.get_right(), code+'1', char_freq)

traverse_huffman_tree(huffman_tree.get_root(),'',key_code_dict)

# print(key_code_dict)
compressed_huffman_code = ''
for i in range(len(discrete_value_list)):
        int_byte = struct.unpack('i',discrete_value_list[i])[0]
        # int_byte = discrete_value_list[i]
        byte_huffman_code = key_code_dict[int_byte]
        compressed_huffman_code += byte_huffman_code

print(compressed_huffman_code)
print(key_code_dict)
current_node = huffman_tree.get_root()
decompressed_huffman_code = []

while len(compressed_huffman_code) > 0:
        # print(len(compressed_huffman_code))
        if current_node.isleaf():
                temp_byte = current_node.get_value()
                # print("a")
                current_node = huffman_tree.get_root()
                decompressed_huffman_code.append(temp_byte)
        
        if compressed_huffman_code[0] == '1':
                current_node = current_node.get_right()
                # print("b")
        else:
                current_node = current_node.get_left()
                # print("c")
        compressed_huffman_code = compressed_huffman_code[1:]

        if len(compressed_huffman_code) == 0:
                # print("a")
                if current_node.isleaf():
                        temp_byte = current_node.get_value()
                        # print("a")
                        current_node = huffman_tree.get_root()
                        decompressed_huffman_code.append(temp_byte)


print(decompressed_huffman_code)

# dis_entropy_X = 0
# for key, value in discrete_value_dict_X.items():
#         p = value / len(discrete_value_list)
#         dis_entropy_X += p * math.log(1/p,2)

# print(dis_entropy_X)

# if __name__ == '__main__':
#     if len(sys.argv) != 4:
#         print("please input the filename!!!")
#         exit(0)
#     else:
#         FLAG = sys.argv[1]
#         INPUTFILE = sys.argv[2]
#         OUTPUTFILE = sys.argv[3]

#     if FLAG == '0':
#         print('compress file')
#         compress(INPUTFILE,OUTPUTFILE)
#     else:
#         print('decompress file')
#         decompress(INPUTFILE,OUTPUTFILE)
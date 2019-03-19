import matplotlib.pyplot as plt
import math
import struct
import sys
import time
import pickle
import copy
import six



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


def buildHuffmanTree(list_hufftrees):
    counter = 0
    while len(list_hufftrees) >1 :
        list_hufftrees.sort(key=lambda x: x.get_weight()) 
        
        # print(list_hufftrees[0].root.get_weight())       
        temp1 = list_hufftrees.pop(0)
        temp2 = list_hufftrees.pop(0)
        # print(temp1.get_weight())
        # print(temp2.get_weight())
        # if counter > 1015:
        #         # print(len(list_hufftrees))
        counter += 1
        newed_hufftree = HuffTree(1, 0, 0, temp1, temp2)

        list_hufftrees.append(newed_hufftree)

    return list_hufftrees[0]


def traverse_huffman_tree(root, code, char_freq):
        if root.isleaf():
            char_freq[root.get_value()] = code
        #     print(("it = %c  and  freq = %d  code = %s")%(chr(root.get_value()),root.get_weight(), code))
            return None
        else:
            traverse_huffman_tree(root.get_left(), code+'0', char_freq)
            traverse_huffman_tree(root.get_right(), code+'1', char_freq)


def huffman_compress(input_file_name, output_file_name):
#############  Prepare Discrete Value List  #################
        output = open(output_file_name, 'w')
        discrete_value_num = 0
        discrete_value_list = []
        with open(input_file_name,"rb") as fin:
                byte = fin.read(4)
                while byte:
                        discrete_value_num += 1
                        discrete_value_list.append(byte)
                        byte = fin.read(4)
                        # discrete_value_list = discrete_value_list[0:10000]
        # discrete_value_list = discrete_value_list[0:20]
        print(len(discrete_value_list)*4) 
        # print(discrete_value_list)
        print("Prepare discrete value list done!")

#############  Prepare Discrete Value List Finished #################

        discrete_value_dict_X = dict()
        for i in range(len(discrete_value_list)):
                int_byte = struct.unpack('i',discrete_value_list[i])[0]
                # print(int_byte)
                if int_byte in discrete_value_dict_X:
                        discrete_value_dict_X[int_byte] += 1
                else:
                        discrete_value_dict_X[int_byte] = 1
        key_code_dict = copy.deepcopy(discrete_value_dict_X)
        list_huffman_trees = []

        for key, value in discrete_value_dict_X.items():
                temp = HuffTree(0, key, value, None, None)
                list_huffman_trees.append(temp)
                list_huffman_trees.sort(key=lambda x: x.get_weight()) 
        huffman_tree = buildHuffmanTree(list_huffman_trees)
        # print('11111111111')
        # print(discrete_value_dict_X)
        traverse_huffman_tree(huffman_tree.get_root(),'',key_code_dict)
        # print('11111111111')
        # print(discrete_value_dict_X)

        compressed_huffman_code = ''
        for i in range(len(discrete_value_list)):
                int_byte = struct.unpack('i',discrete_value_list[i])[0]
                byte_huffman_code = key_code_dict[int_byte]
                compressed_huffman_code += byte_huffman_code
                output.write(byte_huffman_code)
        output.close()
        with open('filename.pickle', 'wb') as handle:
                pickle.dump(discrete_value_dict_X, handle, protocol=pickle.HIGHEST_PROTOCOL)
        print(len(compressed_huffman_code))
        # print(discrete_value_dict_X)

def huffman_decompress(input_file_name, output_file_name):
        with open('filename.pickle', 'rb') as handle:
                discrete_value_dict_X = pickle.load(handle)
        # print(discrete_value_dict_X)
        output = open(output_file_name, 'wb')

        with open(input_file_name, 'r') as myfile:
                compressed_huffman_code=myfile.read()
        # print(len(compressed_huffman_code))
        
        list_huffman_trees = []

        for key, value in discrete_value_dict_X.items():
                # print(key)
                # print(value)
                temp = HuffTree(0, key, value, None, None)
                list_huffman_trees.append(temp)
                list_huffman_trees.sort(key=lambda x: x.get_weight()) 
        huffman_tree = buildHuffmanTree(list_huffman_trees)
        
        current_node = huffman_tree.get_root()
        # decompressed_huffman_code = ''
        count = 0
        while len(compressed_huffman_code) > 0:
        # print(len(compressed_huffman_code))
                if current_node.isleaf():
                        # print(current_node.get_value())
                        # temp_byte = struct.pack(current_node.get_value(),4)
                        temp_byte = current_node.get_value().to_bytes(4, byteorder="little", signed=True)
                        # print("a")
                        # print(temp_byte)
                        output.write(temp_byte)
                        current_node = huffman_tree.get_root()
                        # decompressed_huffman_code += temp_byte
        
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
                                # print(current_node.get_value())
                                # temp_byte = struct.pack(current_node.get_value(),4)
                                temp_byte = current_node.get_value().to_bytes(4, byteorder="little", signed=True)
                                # print("a")
                                # print(temp_byte)
                                output.write(temp_byte)
                                current_node = huffman_tree.get_root()

        output.close()
        # print(len(decompressed_huffman_code))
        # print(decompressed_huffman_code)


if __name__ == '__main__':
        # huffman_compress("input.txt","outpu.txt")
        # huffman_decompress("input.txt","outpu.txt")
        # python3 hello_huffman.py 0 data.bin compressed_file.txt
        # python3 hello_huffman.py 1 compressed_file.txt decompressed_file.bin
        if len(sys.argv) != 4:
                print("please input the filename!!!")
                exit(0)
        else:
                FLAG = sys.argv[1]
                INPUTFILE = sys.argv[2]
                OUTPUTFILE = sys.argv[3]

        if FLAG == '0':
                print('compress file')
                huffman_compress(INPUTFILE,OUTPUTFILE)
        else:
                print('decompress file')
                huffman_decompress(INPUTFILE,OUTPUTFILE)
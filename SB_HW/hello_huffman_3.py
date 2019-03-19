import matplotlib.pyplot as plt
import math
import struct

#############  Prepare Discrete Value List  #################

discrete_value_num = 0
discrete_value_list = []
with open("data.bin","rb") as fin:
        byte = fin.read(4)
        while byte:
                discrete_value_num += 1
                discrete_value_list.append(byte)
                byte = fin.read(4)

print(len(discrete_value_list)) 
print("Prepare discrete value list done!")

#############  Prepare Discrete Value List Finished #################

#############  H(X) Calculation  #################

discrete_value_dict_X = dict()
for i in range(len(discrete_value_list)):
        int_byte = struct.unpack('i',discrete_value_list[i])[0]
        # print(int_byte)
        if int_byte in discrete_value_dict_X:
                discrete_value_dict_X[int_byte] += 1
        else:
                discrete_value_dict_X[int_byte] = 1

dis_entropy_X = 0
for key, value in discrete_value_dict_X.items():
        p = value / len(discrete_value_list)
        dis_entropy_X += p * math.log(1/p,2)

print(dis_entropy_X)

# plt.bar(list(discrete_value_dict_X.keys()),discrete_value_dict_X.values(),color = 'r')
# plt.show()

#############  H(X) Calculation Finished!  #################

#############  H(Y) Calculation  #################

discrete_value_list_Y = []
for i in range(len(discrete_value_list)-1):
        discrete_value_Y = discrete_value_list[i] + discrete_value_list[i+1]
        discrete_value_list_Y.append(discrete_value_Y)

# print(discrete_value_list_Y)

discrete_value_dict_Y = dict()
for i in range(len(discrete_value_list_Y)):
        int_byte = discrete_value_list_Y[i]
        # print(int_byte)
        if int_byte in discrete_value_dict_Y:
                discrete_value_dict_Y[int_byte] += 1
        else:
                discrete_value_dict_Y[int_byte] = 1

dis_entropy_Y = 0
for key, value in discrete_value_dict_Y.items():
        p = value / len(discrete_value_list_Y)
        dis_entropy_Y += p * math.log(1/p,2)

print(dis_entropy_Y / 2)

#############  H(Y) Calculation Finished!  #################

#############  H(Z) Calculation  #################

discrete_value_list_Z = []
for i in range(len(discrete_value_list)-2):
        discrete_value_Z = discrete_value_list[i] + discrete_value_list[i+1] + discrete_value_list[i+2]
        discrete_value_list_Z.append(discrete_value_Z)

# print(discrete_value_list_Y)

discrete_value_dict_Z = dict()
for i in range(len(discrete_value_list_Z)):
        int_byte = discrete_value_list_Z[i]
        # print(int_byte)
        if int_byte in discrete_value_dict_Z:
                discrete_value_dict_Z[int_byte] += 1
        else:
                discrete_value_dict_Z[int_byte] = 1

dis_entropy_Z = 0
for key, value in discrete_value_dict_Z.items():
        p = value / len(discrete_value_list_Z)
        dis_entropy_Z += p * math.log(1/p,2)

print(dis_entropy_Z / 3)

#############  H(Y) Calculation Finished!  #################
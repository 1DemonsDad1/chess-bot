list1=[ [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),(0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)],
        [(0, 6), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),(0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)],]
list2=[[],[]]
a=0
for i in list1:
    for j in i:
        list2[a].append(j)
    a+=1

[[(0, 6)],
[(2, 5), (3, 6)],
[(3, 6), (4, 5), (5, 4), (6, 3), (7, 2)],
[(3, 6)],
[(3, 6), (2, 5), (1, 4), (0, 3)],
[],
[(7, 5), (5, 5)],
[],
[(0, 4)],
[(1, 5), (1, 4)],
[(2, 5), (2, 4)],
[],
[(4, 5), (4, 4)],
[(5, 5), (5, 4)],
[(6, 5), (6, 4)],
[(7, 5), (7, 4)]]
print(list2)
    

# list1=[]
# list2=[]
# for i in range(5):
#     list1.append(list2)
# print(list1)

#idea numero uno s
#Check for piece availble moves in func if king in check not available if not infront of king 

#same as numero uno but for not being able to move if it would lead to check

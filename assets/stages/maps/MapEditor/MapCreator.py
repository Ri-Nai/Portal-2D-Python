import pandas as pd
import numpy as np
import json
import os
name = input("请输入实体碰撞地图的设计表格名称：\n")
filename = name + '.xlsx'
this_path = os.path.dirname(__file__)
path_filename = os.path.join(this_path, filename)
father = os.path.join(this_path, "..")
df = pd.read_excel(path_filename, index_col = None, header = None)
# data = op.load_workbook(path_filename)
A = df.values.tolist()
print(A)
for i in range(len(A)):
    for j in range(len(A[i])):
        if np.isnan(A[i][j]):
            A[i][j] = 0  # 将 NaN 转换为 0
        else:
            A[i][j] = int(A[i][j])  # 将浮点数转换为整数
    A[i].append(-1.5)
print(A)
print(len(A), len(A[0]))
basic_size = 40
layer_background_texture = 3
layer_block = 4
layer_edge = 5
layers = [{"tiles" : [], "opacity" : 1} for i in range(6)]
blocks = []
edges = []
super_edges = []
def fill_block():
    for i in range(18):
        len = 0
        for j in range(33):
            if not j or A[i][j] == A[i][j - 1]:
                len += 1
            else:
                item = {
                            "type" : abs(A[i][j - 1]),
                            "hitbox" :
                            {
                                "x" : (j - len) * basic_size,
                                "y" : i * basic_size,
                                "width" : len * basic_size,
                                "height" : basic_size,
                            }
                        }
                if A[i][j - 1] > 0:
                    blocks.append(item)
                elif A[i][j - 1] < 0:
                    layers[layer_background_texture]["tiles"].append(item)
                len = 1
def fill_edge():
    B = [[-1] * 34 for i in range(20)]
    for i in range(18):
        for j in range(32):
            B[i + 1][j + 1] = A[i][j]
    print(B)
    def write_seg(i, j, last, type, facing, diff, axis):
        now_pos = (i - 1) * basic_size + (1 + diff) * basic_size // 4
        arr_edges = []
        if type == -1:
            arr_edges = super_edges
        else:
            arr_edges = edges
        arr_edges.append(
        {
            "type" : type,
            "facing": facing,
            "hitbox" :
            {
                "xy"[axis] : (last - 1) * basic_size,
                "yx"[axis] : now_pos,
                ["width", "height"][axis] : (j - last) * basic_size,
                ["height", "width"][axis] : basic_size // 2,
            },
        })

    def make_edge_y(diff):
        for i in range(1, 20):
            # 遍历每一行
            # 求出所有露出的块，且相连
            flag = False
            last_normal = 0
            last_super = 0
            for j in range(1, 34):
                type = B[i][j - 1]
                facing = (1 + diff) // 2 * 2
                if B[i][j] <= 0 or B[i + diff][j] > 0:
                    # 非露出
                    if flag and type > 0:
                        # draw j - 1 ~ last_normal
                        write_seg(i, j, last_normal, type, facing, diff, 0)
                        write_seg(i, j, last_super, -1, facing, diff, 0)
                    flag = False
                else:
                    if not flag:
                        last_normal = j
                        last_super = j
                    elif B[i][j] != B[i][j - 1] and type > 0:
                        write_seg(i, j, last_normal, type, facing, diff, 0)
                        last_normal = j
                    flag = True
    def make_edge_x(diff):
        for i in range(1, 34):
            flag = False
            last_normal = 0
            last_super = 0
            for j in range(1, 20):
                type = B[j - 1][i]
                facing = (1 + diff) // 2 * 2 + 1
                if B[j][i] <= 0 or B[j][i + diff] > 0:
                    if flag and type > 0:
                        write_seg(i, j, last_normal, type, facing, diff, 1)
                        write_seg(i, j, last_super, -1, facing, diff, 1)
                    flag = False
                else:
                    if not flag:
                        last_normal = j
                        last_super = j
                    elif B[j][i] != B[j - 1][i] and type > 0:
                        write_seg(i, j, last_normal, type, facing, diff, 1)
                        last_normal = j
                    flag = True
    make_edge_x(1)
    make_edge_y(1)
    make_edge_x(-1)
    make_edge_y(-1)
fill_block()
fill_edge()

answer = {"layers" : layers, "blocks" : blocks, "edges" : edges, "super_edges" : super_edges}
s = json.dumps(answer, indent = 4)
with open(os.path.join(father, name + ".json"), "w") as f:
    f.write(s)

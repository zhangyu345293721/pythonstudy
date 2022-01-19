import numpy as np
import pickle as pk
from pyscipopt import Model, quicksum

file = open("/supplychain/yili/result.pkl", "rb")
result = pk.load(file)

import time

time_start=time.time()


M = result["M"] #牧场数量
F = result["F"] #工厂数量
L = result["L"] # 牛奶登记数量
G = result["G"] # 出产时刻
N = result["N"] # 每时刻产奶上限
T = result["T"];#工厂需要的l级奶量上限
V = result["V"];#工厂的车辆的上限
# 生产时刻
g = result["g"]
# 等级，12级伟a++
l = result["l"]
# 路线时间矩阵
H_fm = result["H_fm"]
# 每个牧场的车辆
V_m = result["V_m"]
# 每个牧场的车的装载量
v_m = result["v_m"]
#每个牧场车的平均荷载量
W_m = result["W_m"]
# 牧场每个时刻产的l级的奶
T3_mlg = result["T3_mlg"]
# 工厂需要的l级奶
T1_fl = result["T1_fl"]
# 每个牧场的车次数
N_m = result["N_m"]
d_mfl1l2g = result["d_mfl1l2g"]
t2_mflg = result["t2_mflg"]

# 求解牧场的运输问题
for mm in range(1, M+1):
    m = Model()
    V = V_m[mm-1, 0] # 牧场的车的数量
    w_v = v_m[mm] # 车的荷载量
    h_f = H_fm[:,mm - 1] #距离
    #当前时刻
    K = 12
    # 工厂f当前给牧场m的订单中g时刻产l级牛奶的总量（包括降级奶）
    t1_flg = {}
    for fi in range(1, F+1):
        for li in range(1,L+1):
            for gi in range(1, G+1):
                # 产量 + 降级进入的量 - 降级出去的量
                in_amount = 0
                out_amount = 0
                for lli in range(1, L+1):
                    in_amount += d_mfl1l2g[mm, fi, lli, li, gi]
                    out_amount += d_mfl1l2g[mm, fi, li, lli, gi]
                t1_flg[fi, li, gi] = t2_mflg[mm, fi, li, gi] + in_amount - out_amount
    #牧场m有的l级g时刻产的牛奶储量
    t3_lg = {}
    for li in range(1, L+1):
        for gi in range(1, G+1):
            t3_lg[li, gi] = T3_mlg[mm-1][li-1][gi -1]

    # 车辆v要运给工厂f的g时刻产的l级奶的吨量
    S_fvlg = {}
    for fi in range(1, F+1):
        for vi in range(1, V+1):
            for li in range(1, L+1):
                for gi in range(1, K+1):
                    name = "S_fvlg_" + str(fi) + ',' + str(vi) + ',' + str(li) + ',' + str(gi)
                    S_fvlg[fi, vi, li, gi] = m.addVar(name, vtype='I', lb=-0.1, ub=N+0.1)
    s_fvg = {}
    for fi in range(1, F + 1):
        for vi in range(1, V + 1):
            for gi in range(1, K + 1):
                name = "s_fvg_" + str(fi) + ',' + str(vi) + ',' + str(gi)
                s_fvg[fi, vi, gi] = m.addVar(name, vtype='I', lb=-0.1, ub=1.1)
    N_f = {}
    for fi in range(1, F+1):
        N_f[fi] = m.addVar("N_f_" + str(fi), vtype='I', lb=-0.1, ub=V+1)
    A_f = {}
    for fi in range(1, F+1):
        A_f[fi] = m.addVar("A_f_" + str(fi), vtype='I')
    B_v = {}
    for vi in range(1, V + 1):
        B_v[vi] = m.addVar("B_v_" + str(vi), vtype='I', lb=-0.1)
    # 定义目标函数
    objs = []
    weights = [1, 0.1, 0.01, 1]
    # 目标1
    obj1 = m.addVar(vtype="C", name="objective1", lb = None, ub = None)  # auxiliary variable to represent objective
    m.addCons(quicksum(B_v[vi] for vi in range(1, V+1)) == obj1)
    objs.append(obj1)

    # 目标2
    obj2 = m.addVar(vtype="C", name="objective2", lb = None, ub = None)  # auxiliary variable to represent objective
    m.addCons(quicksum(-1 * S_fvlg[fi,vi,li,gi] for fi in range(1, F+1) for vi in range(1, V+1) for li in range(1, L+1) for gi in range(1, K+1)) == obj2)
    objs.append(obj2)

    # 目标3
    obj3 = m.addVar(vtype="C", name="objective3", lb = None, ub = None)  # auxiliary variable to represent objective
    m.addCons(quicksum(A_f[fi] for fi in range(1, F+1)) == obj3)
    objs.append(obj3)

    # 目标3
    obj4 = m.addVar(vtype="C", name="objective4", lb=None, ub=None)  # auxiliary variable to represent objective
    m.addCons(quicksum(h_f[fi-1] * N_f[fi] for fi in range(1, F + 1)) == obj4)
    objs.append(obj4)

    m.setObjective(quicksum(weights[i] * objs[i] for i in range(0, 3)), "minimize")

    # 约束
    #约束1
    for fi in range(1, F + 1):
        for vi in range(1, V + 1):
            m.addCons(quicksum(S_fvlg[fi, vi, li, gi] for li in range(1,L+1) for gi in range(1, K+1)) <= w_v[vi-1])

    # 约束2
    for fi in range(1, F + 1):
        for vi in range(1, V + 1):
            for ki in range(1, K+1):
                m.addCons(quicksum(S_fvlg[fi, vi, li, ki] for li in range(1, L + 1)) <= s_fvg[fi, vi, ki] * L * N)
                m.addCons(quicksum(S_fvlg[fi, vi, li, ki] for li in range(1, L + 1)) >= s_fvg[fi, vi, ki])

    # 约束3
    for fi in range(1, F + 1):
        for vi in range(1, V + 1):
            for ki in range(1, K + 1):
                m.addCons(h_f[fi - 1] + s_fvg[fi, vi, ki] * g[ki - 1] <= (64 - K))

    # 约束4
    for li in range(1, L+1):
        for ki in range(1, K+1):
            m.addCons(quicksum(S_fvlg[fi,vi, li,ki] for fi in range(1, F+1) for vi in range(1,V+1)) <= t3_lg[li, ki])

    # 约束5
    for fi in range(1, F+1):
        m.addCons(A_f[fi] == quicksum(t1_flg[fi, li, ki] for li in range(1, L+1) for ki in range(1,K+1)) - quicksum(S_fvlg[fi, vi, li, ki] for vi in range(1, V+1) for li in range(1, L+1) for ki in range(1,K+1)))

    # 约束6
    for vi in range(1, V+1):
        m.addCons(B_v[vi] == w_v[vi-1] - quicksum(S_fvlg[fi, vi, li, ki] for fi in range(1, F+1) for li in range(1, L+1) for ki in range(1, K+1)))

    # 约束7
    for fi in range(1, F+1):
        m.addCons(N_f[fi] == quicksum(s_fvg[fi, vi, ki] for vi in range(1, V+1) for ki in range(1, K+1)))

    # 求解
    m.optimize()

    if m.getStatus() != 'optimal':
        print('Farm %s soluation is not feasible!' % mm)
    else:
        print('\nFarm %s Solution:\n' % mm)
        print("\nObjective:")
        print("1：" + str(m.getVal(obj1)))
        print("2：" + str(m.getVal(obj2)))
        print("3：" + str(m.getVal(obj3)))
        print("4：" + str(m.getVal(obj4)))


time_end=time.time()
print('totally cost',time_end-time_start)

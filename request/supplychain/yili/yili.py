import numpy as np
from pyscipopt import Model, quicksum
import pickle as pk

import time

time_start=time.time()


M = 30 #牧场数量
F = 5 #工厂数量
L = 10 # 牛奶登记数量
G = 64 # 出产时刻
N = 5 # 每时刻产奶上限
T = 50;#工厂需要的l级奶量上限
V = 200;#牧场的车辆的上限
# 生产时刻
g = list(range(1, G+1))
# 等级，12级伟a++
l = list(range(1, L+1))
# 每吨牛奶的降级成本
C_l = np.array(l)
C_l = np.tile(C_l, (L, 1)).T
C_l = np.tril(C_l)
temp = np.diag(range(1, 11))
C_l = C_l - temp
#工厂：编号：需求
f = list(range(1, F+1))
# 牧场：编号，产量
m = list(range(1, M+1))
# 路线时间矩阵
H_fm = np.random.randint(high=20, low=1, size=(F, M))
# 牧场每个时刻产的l级的奶
T3_mlg = np.random.randint(low=1, high=N, size=(M, L, G))
# V_m每个牧场的车辆数
V_m = np.zeros([M, 1], dtype=np.int64)
# 每个牧场的车的装载量
v_m = {}
#每个牧场车的平均荷载量
W_m = {}
for i in range(1, M+1):
    sum_produce = T3_mlg[i - 1].sum()
    V_m[i - 1] = int(sum_produce / 30 * 3)
    v_m[i] = np.random.randint(high=35, low=20, size = (V_m[i-1][0]))
    W_m[i] = v_m[i].mean()
    # 晚上不产奶
T3_mlg[:, :, int(G/2):]=0
# 工厂需要的l级奶
T1_fl = T * np.random.randint(low=1, high=10, size=(F, L))
# 每个牧场的车次数
N_m = np.ceil((48./H_fm.mean(axis=0)).reshape((M,1))*V_m)
# 定义决策变量
m = Model()

#牧场m供应工厂f的g时刻产l级牛奶的吨量
T2_fmlg = {}
for a in range(1, F+1):
    for b in range(1, M+1):
        for c in range(1, L+1):
            for d in range(1, G+1):
                name = "T2_fmlg_" + str(a) + ',' + str(b) + ',' + str(c) + ',' + str(d)
                T2_fmlg[a,b,c,d] = m.addVar(name, vtype='I', lb=-0.1, ub=10.1)

#牧场m供应工厂f的从l1降到l2的g时刻产牛奶吨量
D_fml1l2g = {}
for a in range(1, F+1):
    for b in range(1, M+1):
        for c in range(1, L+1):
            for d in range(1, L+1):
                for e in range(1, G+1):
                    name = "D_fml1l2g_" + str(a) + ',' + str(b) + ',' + str(c) + ',' + str(d) + ',' + str(e)
                    D_fml1l2g[a,b,c,d,e] = m.addVar(name, vtype='I', lb=-0.1, ub=10.1)

T1_fmg = {}
for a in range(1, F+1):
    for b in range(1, M+1):
        for c in range(1, G+1):
            name = "T1_fmg_" + str(a) + ',' + str(b) + ',' + str(c)
            T1_fmg[a,b,c] = m.addVar(name, vtype='I', lb=-0.1, ub=1.1)


# 定义临时变量，降级到l级的牛奶的总量
D_fml2g = {}
for a in range(1, F+1):
    for b in range(1, M+1):
        for d in range(1, L+1):
            for e in range(1, G+1):
                name = "D_fml2g_" + str(a) + ',' + str(b) + ',' + str(d) + ',' + str(e)
                D_fml2g[a,b,d,e] = m.addVar(name, vtype='I', lb=0)
                m.addCons(D_fml2g[a,b,d,e] == quicksum(D_fml1l2g[a,b,c,d,e] for c in range(1, L+1)))

# 临时变量，从l级降级到其他级别的牛奶总量
D_fml1g = {}
for a in range(1, F+1):
    for b in range(1, M+1):
        for d in range(1, L+1):
            for e in range(1, G+1):
                name = "D_fml1g_" + str(a) + ',' + str(b) + ',' + str(d) + ',' + str(e)
                D_fml1g[a,b,d,e] = m.addVar(name, vtype='I', lb=0)
                m.addCons(D_fml1g[a,b,d,e] == quicksum(D_fml1l2g[a,b,d,c,e] for c in range(1, L+1)))

# 定义目标函数
objs = []
weights = [1, 0.1, 100]
# 目标1
obj1 = m.addVar(vtype="C", name="objective1", lb = None, ub = None)  # auxiliary variable to represent objective
m.addCons(quicksum(H_fm[a-1][b-1] * T2_fmlg[a,b,c,d] / W_m[b] for a in range(1, F+1) for b in range(1, M+1) for c in range(1, L+1) for d in range(1, G+1)) == obj1)
objs.append(obj1)

# 目标2
obj2 = m.addVar(vtype="C", name="objective2", lb = None, ub = None)  # auxiliary variable to represent objective
m.addCons(quicksum(-1 * T2_fmlg[a,b,c,d] for a in range(1, F+1) for b in range(1, M+1) for c in range(1, L+1) for d in range(1, G+1)) == obj2)
objs.append(obj2)

# 目标3
obj3 = m.addVar(vtype="C", name="objective3", lb = None, ub = None)  # auxiliary variable to represent objective
m.addCons(quicksum(C_l[c-1][d-1] * D_fml1l2g[a,b,c,d,e] for a in range(1, F+1) for b in range(1, M+1) for c in range(1, L+1) for d in range(1, L+1) for e in range(1, G+1)) == obj3)
objs.append(obj3)

m.setObjective(quicksum(weights[i] * objs[i] for i in range(0, 3)), "minimize")

# 定义约束
#约束1
for a in range(1, F+1):
    for b in range(1, M+1):
        for c in range(1, G+1):
            m.addCons(T1_fmg[a,b,c] <= quicksum(T2_fmlg[a,b,d,c] for d in range(1, L+1)))

for a in range(1, F+1):
    for b in range(1, M+1):
        for c in range(1, G+1):
            m.addCons(quicksum(T2_fmlg[a, b, d, c] for d in range(1, L+1)) <= T1_fmg[a,b,c] * L * N)


#约束2
for a in range(1, F+1):
    for b in range(1, M+1):
        for c in range(1, G+1):
            m.addCons(H_fm[a-1][b-1] + T1_fmg[a,b,c] * g[c - 1] <= 64)

#约束3
for a in range(1, M+1):
    for b in range(1, L+1):
        for c in range(1, G+1):
            m.addCons(quicksum(T2_fmlg[d, a, b, c] for d in range(1, F+1)) <= T3_mlg[a-1][b-1][c-1])

#约束5
for a in range(1, F+1):
    for b in range(1, L+1):
        m.addCons(quicksum(0.95 * (T2_fmlg[a, d, b, e] + D_fml2g[a, d, b, e] - D_fml1g[a,d,b,e]) for d in range(1, M+1) for e in range(1, G+1) ) <= T1_fl[a-1,b-1])
        m.addCons(quicksum(1.05 * (T2_fmlg[a, d, b, e] + D_fml2g[a, d, b, e] - D_fml1g[a,d,b,e]) for d in range(1, M+1) for e in range(1, G+1) ) >= T1_fl[a-1,b-1])

#约束6
for a in range(1, F+1):
    for b in range(1, M+1):
        for c in range(1, L+1):
            for d in range(1, L+1):
                for e in range(1, G+1):
                    if c > d:
                        m.addCons(D_fml1l2g[a, b, c, d, e] <= 10)
                    else:
                        m.addCons(D_fml1l2g[a, b, c, d, e] <= 0)

#约束7
for b in range(1, M+1):
    m.addCons(quicksum(T2_fmlg[a,b,c,d] for a in range(1,F+1) for c in range(1, L+1) for d in range(1, G+1)) <= W_m[b] * N_m[b - 1])

m.optimize()

if m.getStatus() != 'optimal':
    print('solution is not feasible!')
else:
    print('\nSolution:\n')
    print("\nObjective:")
    print("1：" + str(m.getVal(obj1)))
    print("2：" +str(m.getVal(obj2)))
    print("3：" +str(m.getVal(obj3)))

    print("\nErrors:")
    # 农场生产量大于运输量
    for a in range(1, M + 1):
        for c in range(1, L + 1):
            for d in range(1, G + 1):
                sum_quantity = 0
                for b in range(1, F + 1):
                    if m.getVal(T2_fmlg[b, a, c, d]) > 0:
                        sum_quantity += m.getVal(T2_fmlg[b,a,c,d])
                if T3_mlg[a - 1][c - 1][d - 1] < sum_quantity:
                    print("error farm %s, level %s, time %s, transport %s, produce: %s" % (a, c, d, sum_quantity, T3_mlg[a - 1][c - 1][d - 1]))

    # 工厂需求量小于运输量+降级量
    for a in range(1, F+1):
        for c in range(1, L + 1):
            sum_quantity = 0
            for d in range(1, G + 1):
                for b in range(1, M + 1):
                    if m.getVal(T2_fmlg[a, b, c, d]) > 0:
                        sum_quantity +=m.getVal(T2_fmlg[a, b, c, d])
                    if m.getVal(D_fml2g[a,b,c,d]) > 0:
                        sum_quantity += m.getVal(D_fml2g[a,b,c,d])
            if sum_quantity < T1_fl[a-1][c-1] * 0.95 or sum_quantity > T1_fl[a-1][c-1] * 1.05:
                print("error factory %s, level %s, need %s, supply: %s" % (a, c, T1_fl[a-1][c-1], sum_quantity))

    print("\nResult:")
    # 当前可以供给工厂f的l级牛奶
    t2_mflg = {}
    d_mfl1l2g = {}
    for b in range(1, M + 1):
        for a in range(1, F + 1):
            for d in range(1, G + 1):
                s = ""
                for c in range(1, L + 1):
                    if m.getVal(T2_fmlg[a,b,c,d]) > 0:
                        s = s + "grade " + str(c) + "=" + str(m.getVal(T2_fmlg[a,b,c,d])) + ","
                        t2_mflg[b, a, c, d] = m.getVal(T2_fmlg[a,b,c,d])
                    else:
                        t2_mflg[b, a, c, d] = 0
                if len(s) > 0:
                    print("Farm %s, factory %s, " % (b, a) + "time " + str(d) + ", " + s)

            for e in range(1, G + 1):
                s = ""
                for c in range(1, L + 1):
                    for d in range(1, L + 1):
                        if (m.getVal(D_fml1l2g[a, b, c, d, e]) > 0):
                            s = s + str(c) + "->" + str(d) + "=" + str(m.getVal(D_fml1l2g[a, b, c, d, e])) + ","
                            d_mfl1l2g[b, a, c, d, e] = m.getVal(D_fml1l2g[a, b, c, d, e])
                        else:
                            d_mfl1l2g[b, a, c, d, e] = 0
                if len(s) > 0:
                    print("Farm %s, factory %s, " % (b, a) + "time " + str(d) + ", downgrades: " + s)

    result = {}
    result["t2_mflg"] = t2_mflg
    result["d_mfl1l2g"] = d_mfl1l2g
    result["M"] = M
    result["F"] = F
    result["L"] = L
    result["G"] = G
    result["N"] = N
    result["T"] = T
    result["V"] = V
    result["g"] = g
    result["l"] = l
    result["H_fm"] = H_fm
    result["V_m"] = V_m
    result["v_m"] = v_m
    result["W_m"] = W_m
    result["T3_mlg"] = T3_mlg
    result["T1_fl"] = T1_fl
    result["N_m"] = N_m
    result["t2_mflg"] = t2_mflg
    result["d_mfl1l2g"] = d_mfl1l2g
    file = open("/supplychain/yili/result.pkl", "wb")
    pk.dump(result, file)

time_end=time.time()
print('totally cost',time_end-time_start)
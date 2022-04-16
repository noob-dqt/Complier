class sim_DFA:
    def __init__(self):
        self.ends = list()
        self.mp = list()


def simplified(dfa):  # 参数为NFA生成的DFA类，ends存放接受态节点，mp存放dfa，mp为二维list，元素为二元组，其中元素0表示后继元素1表示转移节点
    alphabet = dfa.alphabet
    n = len(dfa.mp)
    tb = list()
    tot = 0
    for elem in dfa.mp:
        tb.append({})
        for tur in elem:
            tb[tot][tur[0]] = tur[1]
        tot += 1
    # tb存储原DFA转移关系tb[0]['a']表示0经过'a'到达的状态
    # 注意：当0经过'b'无转移时tb[0]不含'b'这个键
    org = list()
    tmp = list()  # 临时存储新生成的分区
    for i in range(n):
        if i in dfa.ends:
            org.append(1)  # 最初的分区
        else:
            org.append(0)
    trans = dict()  # 存储转移情况，结构{id(from):{char:id(to)}}
    vis = dict()
    item = list()
    while org != tmp:
        for i in range(n):
            trans[i] = dict()
            for c in alphabet:
                if c in tb[i]:
                    trans[i][c] = org[tb[i][c]]
                else:
                    trans[i][c] = 'x'
        vis.clear()
        for i in range(n):  # 重新编号
            item.clear()
            item.append(org[i])
            for keys in trans[i]:
                item.append(trans[i][keys])
            stritem = ' '.join(str(k) for k in item)
            if stritem not in vis:
                vis[stritem] = len(vis)
            tmp.append(vis[stritem])
        if tmp == org:
            break
        org = tmp.copy()
        tmp.clear()
    sim_dfa = sim_DFA()
    tmpdfa = dict()
    for i in range(n):  # 记录新dfa
        fr = org[i]
        if i in dfa.ends and fr not in sim_dfa.ends:
            sim_dfa.ends.append(fr)
        tmpdfa[fr] = trans[i]
    for i in range(n):
        fr = org[i]
        if fr >= len(sim_dfa.mp):
            sim_dfa.mp.append(list())
            for keys in tmpdfa[fr]:
                if tmpdfa[fr][keys] == 'x':
                    continue
                sim_dfa.mp[fr].append((keys, tmpdfa[fr][keys]))
    return sim_dfa

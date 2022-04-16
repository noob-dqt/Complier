tab = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
       'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
       'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
       'V', 'W', 'X', 'Y', 'Z', 'ε']
res = set()
dfa = list()
reorder = dict()
alphabet = list()
clo = dict()  # 记忆化，记录计算过的每个字母闭包，避免重复运算


class DFA:
    def __init__(self):
        self.alphabet = list()
        self.ends = list()  # 存放接受态节点
        self.mp = list()  # 存放dfa


def search(x, mp):
    if x not in mp:
        return
    for tp in mp[x]:
        if tp[1] == 'ε' and tp[0] not in res:
            res.add(tp[0])
            search(tp[0], mp)
    return


def getClosure(x, mp):  # 获取节点x的ε闭包，mp是NFA,元组里第一个元素是后继节点，第二个元素是转移字符
    res.clear()
    res.add(x)  # x本身属于自己闭包，找到所有经过一次或多次ε能达到的节点
    search(x, mp)
    # x的闭包在res中
    ans = set() | res
    return ans


def get_dfa(state, mp):  # state是str(以空格分隔的数字ID字符串)，用于表达dfa的节点
    # 从当前状态state，经过字母表后生成能到达的新状态闭包，若生成闭包不在dfa节点中则结束递归
    for c in alphabet:
        cls = set()
        lt = state.split(' ')
        for char in lt:
            ch = int(char)
            if ch not in mp:
                continue
            for tc in mp[ch]:
                # 节点ch经过字母c能达到的所有字母求闭包后求并集，得到
                if tc[1] == c:
                    if tc[0] not in clo:  # 记忆化
                        clo[tc[0]] = getClosure(tc[0], mp)
                    cls = cls | clo[tc[0]]
                    # 求出闭包并取并集
        # cls转化为字符串
        if len(cls) == 0:  # 空集，state在当经过c的情况下无法向其他状态转移了
            continue
        newsta = ' '.join(str(i) for i in list(cls))
        if newsta not in reorder:
            pot = len(reorder)
            reorder[newsta] = pot
            dfa.append(list())
            dfa[reorder[state]].append((c, reorder[newsta]))
            get_dfa(newsta, mp)
        else:
            dfa[reorder[state]].append((c, reorder[newsta]))


# dfa:两层list,其中存放元素为元组，第一个元素为字母表中字母，第二个为能跳转到的节点
# dfa[1]存放1节点能到达的所有节点
# 一边生成新节点，一边重新编号
def to_dfa(nfa, rpn):  # 参数nfa是graph类,rpn是逆波兰式
    # 初始化，防止影响下一次运算
    res.clear()
    dfa.clear()
    reorder.clear()
    alphabet.clear()
    clo.clear()
    # -------------
    start = nfa.start
    end = nfa.end
    mp = nfa.mp
    # 统计出字母表中出现的字母
    for c in rpn:
        if c in tab and c != 'ε' and c not in alphabet:
            alphabet.append(c)
    alphabet.sort()
    # 递归生成dfa
    # 起点不直接放入字典dfa中，而是求出起点闭包后再放入字典中，并且起点要特殊处理

    # -------------BUG测试，直接求出所有闭包，找死循环点
    # for keys in mp:
    #     clo[keys] = getClosure(keys, mp)
    # ----------------
    tp = getClosure(start, mp)
    clo[start] = tp
    lt = list(tp)
    hs = ' '.join(str(i) for i in lt)
    # 保证了0是起点
    dfa.append(list())
    reorder[hs] = 0
    get_dfa(hs, mp)
    # 生成的dfa起点是0，含有原接受态的新状态为新终态
    ans = DFA()
    ans.mp = dfa
    ans.alphabet = alphabet
    for s in reorder:
        if str(end) in s:
            ans.ends.append(reorder[s])
    # 最简化DFA
    import Simplified_DFA as Sd
    return Sd.simplified(ans)

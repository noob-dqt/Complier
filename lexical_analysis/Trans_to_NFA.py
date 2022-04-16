# 将前端传入的逆波兰式rpn转为NFA，并返回
# 生成的NFA本质上是一张有向图，边上存储信息为转移字符
# 用graph类存储图的信息，并存下图中的起始节点和终止节点
tab = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
       'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
       'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
       'V', 'W', 'X', 'Y', 'Z', 'ε']


class graph:
    def __init__(self):
        self.mp = dict()  # 图;二元组第一个元素是后继节点，第二个元素是转移字符
        self.start = 0  # 起始节点
        self.end = 0  # 终止节点


def trans(rpn):     # 参数rpn为逆波兰式
    tot = 1  # 递增产生节点序号
    stk = []  # 模拟堆栈
    for c in rpn:
        if c in tab:  # 字母表中的字符直接产生最简单的NFA并放入堆栈
            a = graph()
            a.start = tot
            tot += 1
            a.end = tot
            tot += 1
            a.mp[a.start] = [(a.end, c)]  # 二元组第一个元素是后继节点，第二个元素是转移字符
            stk.append(a)
        else:  # 运算符则根据运算规则从栈中取出相应数量图构成新的图
            if c == '*':  # 重复，一元运算
                if len(stk) == 0:
                    return -1   # 表达式不合法
                top = stk.pop()
                # 对于s*，新增一个起始节点，新增一个结束节点，起始指向原s的起始，s的原终止指向新终止，新起始指向新终止，原终止指向新原起始
                tp = graph()
                tp.mp.update(top.mp)    # 把原有信息线复制过来
                tp.start = tot
                tot += 1
                tp.end = tot
                tot += 1
                tp.mp[tp.start] = [(top.start, 'ε')]
                tp.mp[top.end] = [(tp.end, 'ε')]
                tp.mp[tp.start].append((tp.end, 'ε'))
                tp.mp[top.end].append((top.start, 'ε'))
                stk.append(tp)

            elif c == '.':  # 连接
                if len(stk) < 2:
                    return -1   # 表达式不合法
                # 对于s.t，添加两个节点：起始、终止，起始指向s起点，s终点指向t起点，t终点指向新终点
                t = stk.pop()
                s = stk.pop()
                tp = graph()
                tp.mp.update(s.mp)
                tp.mp.update(t.mp)
                tp.start = tot
                tot += 1
                tp.end = tot
                tot += 1
                tp.mp[tp.start] = [(s.start, 'ε')]
                tp.mp[s.end] = [(t.start, 'ε')]
                tp.mp[t.end] = [(tp.end, 'ε')]
                stk.append(tp)
            elif c == '|':  # 选择
                if len(stk) < 2:
                    return -1   # 表达式不合法
                # 对于s|t，建立起点、终点，起点分别指向s起点，t起点，s、t终点分别指向新终点
                t = stk.pop()
                s = stk.pop()
                tp = graph()
                tp.mp.update(s.mp)
                tp.mp.update(t.mp)
                tp.start = tot
                tot += 1
                tp.end = tot
                tot += 1
                tp.mp[tp.start] = [(s.start, 'ε')]
                tp.mp[tp.start].append((t.start, 'ε'))
                tp.mp[s.end] = [(tp.end, 'ε')]
                tp.mp[t.end] = [(tp.end, 'ε')]
                stk.append(tp)
    if len(stk) != 1:
        return -1
    else:
        return stk[0]

# 例如：
# test = 'ab|*'
# res = trans(test)
# 得到的是起点为res.start终点为res.end的一张图，节点范围为1-res.end
# for i in range(1, 8):
#     print(res.mp[i])

import Trans_to_NFA as tn
from graphviz import Digraph
f = Digraph('NFA', filename='res', format='png')
f.attr(rankdir='LR', size='20,5')  # 规定方向,大小
# f.engine = 'circo'      # 更换引擎
# f.engine = 'neato'
# 引擎默认是dot类型
# dot 	有向图（分层地画）
# neato 	无向图（基于弹簧模型）
# twopi 	星形图（结点中心放到同心的一系列圆上，包括圆心）
# circo 	环状的图
# fdp 	无向图（基于力）
# patchwork 方块图

# 单独定义的 node 会有双圆结构
# f.attr('node', shape='doublecircle')
# f.node('1')
# f.node('10')
# f.attr('node', shape='circle')
# for i in range(1, 10):
#     f.edge(str(i), str(i+1), label='i*j='+str(i*(i+1)))
# f.view(filename='images/nfa', cleanup=True)       # 会自动打开生成的图片
# f.render(filename='images/nfa', view=False, cleanup=True)    # 生成后不自动打开
test = 'ab|*'
res = tn.trans(test)
f.attr('node', shape='doublecircle')
f.node(str(res.end))
f.attr('node', shape='circle')
f.node(str(res.start))
f.node('start')
f.edge('start', str(res.start))
# 得到的是起点为res.start终点为res.end的一张图，节点范围为1-res.end
for i in range(1, res.end):
    for (to, c) in res.mp[i]:
        f.edge(str(i), str(to), label=c)
f.render(filename='images/nfa', view=False, cleanup=True)

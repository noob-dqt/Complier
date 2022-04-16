from graphviz import Digraph
import time


def draw(res):  # res为一个类，类中包含终点序号列表，以及一个二维列表
    f = Digraph('DFA', filename='dfa', format='png')
    f.attr(rankdir='LR')
    # eng = ['dot', 'neato', 'twopi', 'circo', 'fdp']
    # f.engine = eng[tp]
    f.attr('node', shape='doublecircle')
    for c in res.ends:
        f.node(str(c))
    f.attr('node', shape='circle')
    f.node('0')
    f.node('start')
    f.edge('start', '0')
    for i in range(len(res.mp)):
        for j in range(len(res.mp[i])):
            to = res.mp[i][j][1]
            c = res.mp[i][j][0]
            f.edge(str(i), str(to), label=c)
    fname = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time())) + '_dfa'
    path = f.render(filename='images/'+fname, view=False, cleanup=True)
    return path

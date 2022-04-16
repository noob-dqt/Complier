from graphviz import Digraph
import time


def draw(pictype, name, res):   # pictype：DFA/NFA，name：filename, res为一个类，类中包含起点终点，以及一个字典（字典是存储DFA/NFA的图）
    f = Digraph(pictype, filename=name, format='png')
    eng = ['dot', 'neato', 'twopi', 'circo', 'fdp']
    # tp = random.randint(0, 4)
    # f.engine = eng[tp]
    # f.attr(rankdir='LR', size='20,5')
    f.attr(rankdir='LR')
    f.attr('node', shape='doublecircle')
    f.node(str(res.end))
    f.attr('node', shape='circle')
    f.node(str(res.start))
    f.node('start')
    f.edge('start', str(res.start))
    for i in range(1, res.end):
        for (to, c) in res.mp[i]:
            f.edge(str(i), str(to), label=c)
    fname = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time())) + '_nfa'
    path = f.render(filename='images/'+fname, view=False, cleanup=True)
    return path

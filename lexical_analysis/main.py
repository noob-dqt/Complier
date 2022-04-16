from PySide2.QtWidgets import QApplication, QMessageBox
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QPixmap
from PySide2.QtCore import Qt
import sys
import Trans_to_NFA as tN
import drawnfa as dr
import drawdfa as df
import NFA_to_DFA as Nt

tab = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
       'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
       'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
       'V', 'W', 'X', 'Y', 'Z', 'ε']


class mainWindow:
    def __init__(self):
        super(mainWindow, self).__init__()
        self.wd = QUiLoader().load("UI/main.ui")
        self.wd.setWindowTitle("lexical_Analysis")
        self.wd.ker_btn.clicked.connect(self.process)
        self.wd.ker_btn_2.clicked.connect(self.add)
        self.wd.inp.returnPressed.connect(self.process)

    def process(self):
        txt = self.wd.inp.text()
        if len(txt) == 0:
            QMessageBox.warning(self.wd, "警告", "请先输入正则式！")
            return
        fixed = []  # 存放加入连接符.之后的正则式
        # 手动加上连接运算符.(统一使用英文句号表示)
        for i in range(len(txt)):
            c = txt[i]
            if i == 0:
                fixed.append(c)
                continue
            if c in tab:
                tc = txt[i - 1]
                if tc == ')' or tc in tab or tc == '*':
                    fixed.append('.')
                fixed.append(c)
            else:
                if c == ' ':  # 去除空格
                    pass
                elif c == '*' or c == '|' or c == ')':
                    fixed.append(c)
                elif c == '(':
                    tc = txt[i - 1]
                    if tc == '*' or tc == ')' or tc in tab:
                        fixed.append('.')
                    fixed.append(c)
                else:  # 输入不合法
                    QMessageBox.warning(self.wd, "警告", "输入不合法！")
                    return
        rpn = self.to_RPN(fixed)
        if rpn == '':
            return
        shownrpn = []
        for i in range(len(rpn)):
            if rpn[i] == '.':
                shownrpn.append('·')
            else:
                shownrpn.append(rpn[i])
            shownrpn.append(' ')
        shownrpn = ''.join(shownrpn)
        self.wd.suffix.setText(shownrpn)
        # 调用转换NFA方法，并将生成的结果图绘制到面板上
        res = tN.trans(rpn)
        if res == -1:
            QMessageBox.warning(self.wd, "警告", "输入不合法！")
            return
        # 画出NFA并展示
        # print(res.mp['18'])
        path = dr.draw('nfa', 'nfa', res)
        if path == "":
            QMessageBox.warning(self.wd, "警告", "NFA生成错误！")
            return
        self.showpic(path, 'nfa')
        # NFA转换成DFA并化至最简
        resdfa = Nt.to_dfa(res, rpn)
        path = df.draw(resdfa)
        self.showpic(path, 'dfa')

    def showpic(self, path, tar):
        img = QPixmap(path)
        picsize = img.size()
        maxsize = self.wd.resbox.size()
        if tar == 'nfa':
            if picsize.width() < maxsize.width() and picsize.height() < maxsize.height():
                self.wd.nfa.setPixmap(img)
            else:
                self.wd.nfa.setPixmap(QPixmap(path).scaled(maxsize, aspectMode=Qt.KeepAspectRatio))
            self.wd.nfa.adjustSize()
        else:
            if picsize.width() < maxsize.width() and picsize.height() < maxsize.height():
                self.wd.dfa.setPixmap(img)
            else:
                self.wd.dfa.setPixmap(QPixmap(path).scaled(maxsize, aspectMode=Qt.KeepAspectRatio))
            self.wd.dfa.adjustSize()

    def to_RPN(self, reg):  # 规范后的正则式转为后缀表达式
        priori = {'*': 3, '.': 2, '|': 1, '(': 0}
        stk = []
        tpres = []
        for c in reg:
            if c in tab:
                tpres.append(c)
            else:
                if c == ')':
                    while len(stk):
                        tc = stk.pop()
                        if tc == '(':
                            break
                        else:
                            tpres.append(tc)
                elif c == '(' or len(stk) == 0:
                    stk.append(c)
                else:
                    while len(stk):
                        tc = stk.pop()
                        if priori[tc] >= priori[c]:
                            tpres.append(tc)
                        else:
                            stk.append(tc)
                            break
                    stk.append(c)
        while len(stk):
            tc = stk.pop()
            if tc == '(':   # 括号不匹配
                QMessageBox.warning(self.wd, "警告", "括号不匹配！")
                return ''
            tpres.append(tc)
        return tpres

    def add(self):
        s = self.wd.inp.cursorPosition()
        txt = list(self.wd.inp.text())
        txt.insert(s, 'ε')
        self.wd.inp.setText(''.join(txt))


if __name__ == '__main__':
    app = QApplication([])
    mw = mainWindow()
    mw.wd.show()
    sys.exit(app.exec_())

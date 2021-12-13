class Node:
    def __init__(self,Value, listOfNodes):
        self.value       = Value
        self.children    = listOfNodes

    def Evaluate(self,symbs):
        pass

class BinOp(Node):
    def Evaluate(self,symbs):
        if self.value == '+':
            return self.children[0].Evaluate(symbs) + self.children[1].Evaluate(symbs)
        elif self.value == '-':
            return self.children[0].Evaluate(symbs) - self.children[1].Evaluate(symbs)
        elif self.value == '*':
            return self.children[0].Evaluate(symbs) * self.children[1].Evaluate(symbs)
        elif self.value == '/':
            return self.children[0].Evaluate(symbs) // self.children[1].Evaluate(symbs)
        
class UnOp(Node):
    def Evaluate(self,symbs):
        if self.value == '+':
            return self.children[0].Evaluate(symbs)
        elif self.value == '-':
            return self.children[0].Evaluate(symbs)*(-1)

class IntVal(Node):
    def Evaluate(self,symbs):
        return self.value

class NoOp(Node):
    def Evaluate(self,symbs):
        pass

class IdentifierOp(Node):
    def Evaluate(self, symbs):
        return symbs.getter(self.value)

class Block(Node):
    def Evaluate(self, symbs):
        for node in self.children:
            node.Evaluate(symbs)

class SymbolTable:
    def __init__(self):
        self.symbDict = {}

    def getter(self, var):
        if var in self.symbDict:
            return self.symbDict[var]
        else:
            raise NameError("Err: Variable does't existis")

    def setter(self, var, val):
        self.symbDict[var] = val

class AssignmentOp(Node):
    def Evaluate(self, symbs):
        return symbs.setter(self.children[0], self.children[1].Evaluate(symbs))

class PrintOp(Node):
    def Evaluate(self, symbs):
        print(self.children[0].Evaluate(symbs))
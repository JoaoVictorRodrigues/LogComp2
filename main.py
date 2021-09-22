import sys
import re

arg = sys.argv[1]
arg = re.sub("[/][*]\s*(.*?)\s*[*][/]", "", arg)
class Token:
    def __init__(self,Type,Value):
        self.type = Type
        self.value = Value 

class Parser:
    def __init__(self, origin):
        self.origin   = origin
        self.index    = 0
        self.char     = self.getNextToken()

    def getNextToken(self):
        
        ch      = 0
        index   = 0
        number  = 0

        lenArg    = len(self.origin)
        operables = []
        

        while self.index < lenArg and self.origin[self.index].isspace():
            self.index += 1

        if self.index == lenArg:
            self.char = Token('EOF', 'end')

        elif self.origin[self.index].isdigit():
            while self.index < lenArg and self.origin[self.index].isdigit():
                operables.append(int(self.origin[self.index]))
                self.index += 1
            for ch in operables:
                number += int(ch)*10**(len(operables) - index - 1)
                index += 1
            self.char = Token('INT', number)

        elif self.index < lenArg:
            if self.origin[self.index] == '+':
                self.char = (Token('SUM', '+'))
                self.index += 1
            elif self.origin[self.index] == '-':
                self.char = (Token('SUB', '-'))
                self.index += 1
            elif self.origin[self.index] == '*':
                self.char = (Token('MUL', '*'))
                self.index += 1
            elif self.origin[self.index] == '/':
                self.char = (Token('DIV', '/'))
                self.index += 1
            elif self.origin[self.index] == '(':
                self.char = (Token('OPEN', '('))
                self.index += 1            
            elif self.origin[self.index] == ')':
                self.char = (Token('CLOSE', ')'))
                self.index += 1
            else:
                self.index += 1 
        return self.char

class Calculator:
    
    index       = 0
    parentheses = 0
    negative    = 1

    def Expression():
        out = Calculator.Term()            
        while (Calculator.tk.char.type == 'SUM' or 
               Calculator.tk.char.type == 'SUB' or 
               Calculator.tk.char.type == 'MUL' or 
               Calculator.tk.char.type == 'DIV'):
            
            if Calculator.tk.char.type =='SUM':
                Calculator.tk.getNextToken()
                out += Calculator.Term()
    
            elif Calculator.tk.char.type == 'SUB':
                Calculator.tk.getNextToken()
                out -= Calculator.Term()
                
        return out

    def Term(): 
        out = Calculator.Factor()
        Calculator.tk.getNextToken()
    
        while Calculator.tk.char.type == 'MUL'  :
            if Calculator.tk.char.type =='MUL':
                Calculator.tk.getNextToken()
                if Calculator.tk.char.type == 'INT':
                    out *= Calculator.Term()
                else:
                    raise NameError('Err: MUL')
            Calculator.tk.getNextToken()
                    
        while Calculator.tk.char.type == 'DIV':
            if Calculator.tk.char.type == 'DIV':
                Calculator.tk.getNextToken()
                out = out // Calculator.Term()
            Calculator.tk.getNextToken()

        return out
    
    def Factor():
        out = Calculator.tk.char.value
        if Calculator.tk.char.type == 'INT':
            return out

        elif Calculator.tk.char.type == 'OPEN':
            Calculator.parentheses += 1
            Calculator.tk.getNextToken()
            out = Calculator.Expression()
            if Calculator.tk.char.type == 'CLOSE':
                return out
            else:
                raise NameError('Err: Missing parentheses')

        elif Calculator.tk.char.type == 'SUB':
            Calculator.index+=1
            Calculator.tk.getNextToken()
            Calculator.Factor()
            Calculator.negative = (-1)**(Calculator.index)
            
        elif Calculator.tk.char.type == 'SUM':
            Calculator.tk.getNextToken()
            Calculator.Factor()
        
        out = Calculator.tk.char.value * Calculator.negative
        return out
              

    def run(code):
        Calculator.tk = Parser(code)
        return Calculator.Expression()

print(Calculator.run(arg))      
lock = ["println"]
PRINTLN = lock

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
        letter  = ""
        lenArg     = len(self.origin)
        operables  = []
        

        while self.index < lenArg and self.origin[self.index].isspace():
            self.index += 1

        if self.index == lenArg:
            self.char = Token('EOF', 'end')

        elif self.origin[self.index].isalpha():
            letter += self.origin[self.index]
            self.index += 1
            while (self.index < lenArg and 
                    (self.origin[self.index].isalpha() or 
                     self.origin[self.index].isdigit() or 
                     self.origin[self.index] == '_')):

                letter += self.origin[self.index]
                self.index += 1
            
            variable = letter


            if variable in lock:
                # print("Variable", variable)
                self.char = (Token(variable.upper(), variable))
            else:
                # print("IDENTIFIER", variable)
                self.char = (Token('IDENTIFIER',variable))

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
            elif self.origin[self.index] == '=':
                self.char = (Token('EQUAL', '='))
                self.index += 1
            elif self.origin[self.index] == ';':
                self.char = (Token('ENDLINE', ';'))
                self.index += 1
            else:
                self.index += 1 
        return self.char

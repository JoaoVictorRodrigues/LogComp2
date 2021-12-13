#Referencia: https://programadoresbrasil.com.br/2021/04/classe-abstrata-em-python-entenda-como-funcionam/

import sys
import re
import nodeClass as nodes
import tokensClass as tokens

class Unifier:
    def sliceComment(arg):
        arg = re.sub("[/][*]\s*(.*?)\s*[*][/]", "", arg)
        return(arg)
class Calculator:
    
    index       = 0
    parentheses = 0
    negative    = 1

    def Expression():
        out = Calculator.Term()   #       
        while (Calculator.tk.char.type == 'SUM' or 
               Calculator.tk.char.type == 'SUB' or 
               Calculator.tk.char.type == 'MUL' or 
               Calculator.tk.char.type == 'DIV'):
            
            if Calculator.tk.char.type =='SUM':
                Calculator.tk.getNextToken()
                exp = Calculator.Term()
                out = nodes.BinOp('+',[out, exp])
    
            elif Calculator.tk.char.type == 'SUB':
                Calculator.tk.getNextToken()
                exp = Calculator.Term()
                out = nodes.BinOp('-',[out, exp])

        return out

    def Term(): 
        out = Calculator.Factor()

        while (Calculator.tk.char.type == 'MUL' or 
               Calculator.tk.char.type == 'DIV'):
            
            if Calculator.tk.char.type == 'MUL':
                Calculator.tk.getNextToken()
                exp = Calculator.Factor()
                out = nodes.BinOp('*',[out, exp])

            elif Calculator.tk.char.type == 'DIV':
                Calculator.tk.getNextToken()
                exp = Calculator.Factor()
                out = nodes.BinOp('/',[out, exp])

        return out
    
    def Factor():
        if Calculator.tk.char.type == 'INT':
            out = Calculator.tk.char.value
            Calculator.tk.getNextToken()
            out = nodes.IntVal(out, [])
            return out

        elif Calculator.tk.char.type == 'OPEN':
            Calculator.parentheses += 1
            Calculator.tk.getNextToken()
            out = Calculator.Expression()
            if Calculator.tk.char.type == 'CLOSE':
                Calculator.tk.getNextToken()
                return out
            else:
                raise NameError('Err: Missing parentheses')

        elif (Calculator.tk.char.type == 'SUB' or 
              Calculator.tk.char.type == 'SUM'):
            
            if Calculator.tk.char.type == 'SUB':
                Calculator.index+=1
                Calculator.tk.getNextToken()
                exp = Calculator.Factor()
                out = nodes.UnOp("-", [exp])
            
            elif Calculator.tk.char.type == 'SUM':
                Calculator.tk.getNextToken()
                exp = Calculator.Factor()
                out = nodes.UnOp("+", [exp])

            return out   

        elif Calculator.tk.char.type == 'IDENTIFIER':
            out = nodes.IdentifierOp(Calculator.tk.char.value,[])
            Calculator.tk.getNextToken()
            return out

        else:
            raise NameError('Err: Ivalid Operation')
        
    def Block():
        blockList=[]
        while Calculator.tk.char.type != 'EOF':
            blockList.append(Calculator.Command())
            if Calculator.tk.char.type != 'ENDLINE':
                raise NameError("Err: Missing ';'")
            else:
                Calculator.tk.getNextToken()

        return nodes.Block("COMMAND", blockList)
    
    def Command():

        if Calculator.tk.char.type == 'IDENTIFIER':
            var = Calculator.tk.char.value
            Calculator.tk.getNextToken()
            if Calculator.tk.char.type == 'EQUAL':
                Calculator.tk.getNextToken()
                res = nodes.AssignmentOp(Calculator.tk.char.value, [var, Calculator.Expression()])    
            else:
                raise NameError("Err: Missing assigment symbol (=)")
                
        elif Calculator.tk.char.type == 'PRINTLN':
            Calculator.tk.getNextToken()
            if Calculator.tk.char.type == 'OPEN':
                Calculator.tk.getNextToken()
                val = Calculator.Expression()
                if Calculator.tk.char.type == 'CLOSE':
                    Calculator.tk.getNextToken()
                else:
                    raise NameError("Err: Missig close parentheses")
            res = nodes.PrintOp("println", [val])

        else:
            res = nodes.NoOp(0, [])
        return res
                      
    def run(code):
        code = Unifier.sliceComment(code)
        Calculator.tk = tokens.Parser(code)
        out = Calculator.Block()
        Calculator.tk.getNextToken()

        while Calculator.tk.char.type == 'ENTER':
            Calculator.tk.getNextToken()

        if Calculator.tk.char.type != 'EOF':
            raise NameError('Err: EOF')
        else:
            return out

if __name__ == "__main__": 
    if (len(sys.argv) == 2):
        file = sys.argv[1]
    else:
        raise NameError('Err: only one .c file')
    symbs = nodes.SymbolTable()

    with open (file, 'r') as file:
        arg = file.read()
    out = Calculator.run(arg)

    out.Evaluate(symbs)
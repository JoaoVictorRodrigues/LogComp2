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
        out = Calculator.Term()  
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
            Calculator.tk.getNextToken()
            out = Calculator.ExpOR()
            if Calculator.tk.char.type == 'CLOSE':
                Calculator.tk.getNextToken()
                # return out
            else:
                raise NameError('Err: Missing parentheses')
            return out

        elif (Calculator.tk.char.type == 'SUB' or 
              Calculator.tk.char.type == 'SUM' or 
              Calculator.tk.char.type == 'NOT'):
            
            if Calculator.tk.char.type == 'SUB':
                Calculator.index+=1
                Calculator.tk.getNextToken()
                exp = Calculator.Factor()
                out = nodes.UnOp("-", [exp])
            
            elif Calculator.tk.char.type == 'SUM':
                Calculator.tk.getNextToken()
                exp = Calculator.Factor()
                out = nodes.UnOp("+", [exp])
            
            elif Calculator.tk.char.type == 'NOT':
                Calculator.tk.getNextToken()
                exp = Calculator.Factor()
                out = nodes.UnOp("!", [exp])

            return out   

        elif Calculator.tk.char.type == 'IDENTIFIER':
            out = nodes.IdentifierOp(Calculator.tk.char.value,[])
            Calculator.tk.getNextToken()
            return out

        elif Calculator.tk.char.type == 'READLN':
            Calculator.tk.getNextToken()
            if Calculator.tk.char.type == 'OPEN':
                Calculator.tk.getNextToken()
                if Calculator.tk.char.type == 'CLOSE':
                    Calculator.tk.getNextToken()
                else:
                    raise NameError("Erro: parênteses não fechado")
            else:
                raise NameError("Erro: readln é uma função abra e feche parenteses para chama-la")

            out = nodes.InputOp("readln", [])
        else:
            raise NameError('Err: Ivalid Operation')
        
        return out
        
    def Block():
        blockList=[]

        if Calculator.tk.char.type == 'KEYSOPEN':
            Calculator.tk.getNextToken()
            while Calculator.tk.char.type != 'KEYSCLOSE':
                if Calculator.tk.char.type == 'EOF':
                    raise NameError("Err: No ended block 1")
                blockList.append(Calculator.Command())
            if Calculator.tk.char.type == 'KEYSCLOSE':
                Calculator.tk.getNextToken()
            else:
                raise NameError("Err: No ended block")
        else:
            raise NameError("Err: No opened block")
        
        return nodes.Block("BLOCK",blockList)
    
    def Command():
        if Calculator.tk.char.type == 'IDENTIFIER':
            var = Calculator.tk.char.value
            Calculator.tk.getNextToken()            
            if Calculator.tk.char.type == 'ASSING':
                Calculator.tk.getNextToken()
                out = nodes.AssignmentOp(Calculator.tk.char.value, [var, Calculator.ExpOR()])
                if Calculator.tk.char.type == 'ENDLINE':
                   Calculator.tk.getNextToken() 
                elif Calculator.tk.char.type == 'CLOSE':
                    pass
                else:
                   raise NameError("Err: Missing Endline IDENT")
            else:
                raise NameError("Err: Missing assigment symbol (=)")
        
        elif Calculator.tk.char.type == 'PRINTLN':
            Calculator.tk.getNextToken()
            if Calculator.tk.char.type == 'OPEN':
                Calculator.tk.getNextToken()
                val = Calculator.Expression()
                if Calculator.tk.char.type == 'CLOSE':
                    Calculator.tk.getNextToken()
                    if Calculator.tk.char.type == 'ENDLINE':
                        Calculator.tk.getNextToken() 
                    else:
                        raise NameError("Err: Missing Endline PRINT") 
                else:
                    raise NameError("Err: Missig close parentheses PRINT")
            out = nodes.PrintOp("println", [val])
                
        elif Calculator.tk.char.type == 'IF':
            ifList = []
            Calculator.tk.getNextToken()
            if Calculator.tk.char.type == 'OPEN':
                Calculator.tk.getNextToken()
                ifList.append(Calculator.ExpOR())
                if Calculator.tk.char.type == 'CLOSE':
                    Calculator.tk.getNextToken()
                    ifList.append(Calculator.Command())
                else:
                    raise NameError("Err: Missing close parentheses IF")

                if Calculator.tk.char.type == 'ELSE':
                    Calculator.tk.getNextToken()
                    ifList.append(Calculator.Command())

            else:
                raise NameError("Err: Missig open parentheses")
            out = nodes.IfOp('if',ifList)

        elif Calculator.tk.char.type == 'WHILE':
            Calculator.tk.getNextToken()
            if Calculator.tk.char.type == 'OPEN':
                Calculator.tk.getNextToken()
                val = Calculator.ExpOR()
                if Calculator.tk.char.type == 'CLOSE':
                    Calculator.tk.getNextToken()
                    out = nodes.WhileOp('while',[val,Calculator.Command()])
                else:
                    raise NameError("Err: Missig close parentheses WHILE")
            else:
                raise NameError("Err: Missig open parentheses")
        
        elif Calculator.tk.char.type == 'FOR':
            forList = []
            Calculator.tk.getNextToken()
            if Calculator.tk.char.type == 'OPEN':
                Calculator.tk.getNextToken()
                forList.append(Calculator.Command())

                forList.append(Calculator.ExpOR())

                Calculator.tk.getNextToken()
                forList.append(Calculator.Command())

                if Calculator.tk.char.type == 'CLOSE':
                    Calculator.tk.getNextToken()
                    out = nodes.ForOp('for', forList)
                else:
                    raise NameError("Err: Missig close parentheses FOR")
            else:
                raise NameError("Err: Missig open parentheses")
                
        elif Calculator.tk.char.type == "KEYSOPEN":
            out = Calculator.Block()

        elif Calculator.tk.char.type == 'ENDLINE':
            out = nodes.NoOp(0,[])
            Calculator.tk.getNextToken() 
        else:
            out = nodes.NoOp(0,[])
            raise NameError("Err: Missing Endline END")
        
        return out 


    def ExpOR():
        out = Calculator.ExpAND()
        while Calculator.tk.char.type == 'OR':
            Calculator.tk.getNextToken()
            children = [out, Calculator.ExpAND()]
            out = nodes.BinOp('||', children)
        return out

    def ExpAND():
        out = Calculator.ExpEQUAL()
        while Calculator.tk.char.type == 'AND':
            Calculator.tk.getNextToken()
            children = [out, Calculator.ExpEQUAL()]
            out = nodes.BinOp('&&', children)
        return out

    def ExpEQUAL():
        out = Calculator.ExpREL()
        while Calculator.tk.char.type == 'EQUAL':
            Calculator.tk.getNextToken()
            children = [out, Calculator.ExpREL()]
            out = nodes.BinOp('==', children)
        return out

    def ExpREL():
        out = Calculator.ExpDIFF()
        while (Calculator.tk.char.type == 'GREATER' 
               or Calculator.tk.char.type == 'LESS'
               or Calculator.tk.char.type == 'GREATER_OR_EQUAL'
               or Calculator.tk.char.type == 'LESS_OR_EQUAL'):
               
            if Calculator.tk.char.type == 'GREATER':
                Calculator.tk.getNextToken()
                children = [out, Calculator.ExpDIFF()]
                out = nodes.BinOp('>', children)

            elif Calculator.tk.char.type == 'LESS':
                Calculator.tk.getNextToken()
                children = [out, Calculator.ExpDIFF()]
                out = nodes.BinOp('<', children)

            elif Calculator.tk.char.type == 'GREATER_OR_EQUAL':
                Calculator.tk.getNextToken()
                children = [out, Calculator.ExpDIFF()]
                out = nodes.BinOp('>=', children)

            elif Calculator.tk.char.type == 'LESS_OR_EQUAL':
                Calculator.tk.getNextToken()
                children = [out, Calculator.ExpDIFF()]
                out = nodes.BinOp('<=', children)   
        return out

    def ExpDIFF():
        out = Calculator.Expression()
        while Calculator.tk.char.type == 'DIFFERENT':
            Calculator.tk.getNextToken()
            children = [out, Calculator.Expression()]
            out = nodes.BinOp('!=', children)
        return out
    
                      
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
    # if (len(sys.argv) == 2):
    arg = sys.argv[1]
    # else:
    #     raise NameError('Err: only one .c file')
    symbs = nodes.SymbolTable()

    # with open (file, 'r') as file:
    #     arg = file.read()
    out = Calculator.run(arg)

    out.Evaluate(symbs)
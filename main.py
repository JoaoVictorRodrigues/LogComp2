import sys

class Analyzer:
    arg = sys.argv[1]
    arg = arg.replace(" ","") 

    def parser(arg):
        i           = 0
        count       = 0
        index      = 0
        number      = 0
        operable    = []
        size        = []
        parsed      = []
        splitado    = []
        for ch in arg:
            if ch.isdigit():
                parsed.append(int(ch))
                count += 1
            else:
                parsed.append(ch)
                size.append(count)
                count = 0
        size.append(count)

        for dig in parsed:
            if isinstance(dig, int):
                dig = dig*10**(size[i]-1-index)
                index+=1
                splitado.append(dig)
            else:
                i+=1
                index=0
                splitado.append(dig)

        for j in splitado:
            if j == str(j):
                operable.append(number)
                number = str(j)
                operable.append(number)
                number = 0
            else:
                number += j
        operable.append(number)
        return operable
    
    def tokens():
        # tk = {}
        count=1
        parsed = Analyzer.parser(Analyzer.arg)

        op = parsed[0]
        for k in parsed:
            if str(k) == "+":
                op += parsed[count]
            elif str(k) == "-":
                op -= parsed[count]
            count+=1
        
        # for i in parsed:
        #     if   i == '+':
        #         tk['SUM'] = i
        #     elif i == '-':
        #         tk['MIN'] = i
        #     elif i == '*':
        #         tk['MUL'] = i
        #     elif i == '/':
        #         tk['DIV'] = i
        #     else:
        #         tk['NUM'] = i
        # print(tk)
        return op
    
    def run():
        out = Analyzer.tokens()
        # i = 1
        # out = []
        
        # op = tk["NUM"]
        # for k in tk:
        #     if "SUM" in tk[k+1]:
        #         op += tk[i]["NUM"]
        #     elif "MIN" in tk[k+1]:
        #         op -= tk[i]["NUM"]
        #     i+=1
        

        # while k < len(tk):
        #     print("LOOP")
        #     if "SUM" in tk[k]:
        #         result = tk[k-1]['NUM'] + tk[k+1]['NUM']
        #         out.append(result)
            
        #     elif "MIN" in tk[k]:
        #         result = tk[k-1]['NUM'] - tk[k+1]['NUM']
        #         out.append(result)

        #     else:
        #         k+=1
        #         # result = tk[k-1]['NUM'] + tk[k+1]['NUM']
        #         # out.append(result)
        #     k+=1
            
        return out
             
teste = Analyzer.run()

print(teste)

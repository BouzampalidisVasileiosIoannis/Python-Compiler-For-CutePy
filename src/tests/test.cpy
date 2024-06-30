
#int counterFunctionCalls

def max3(x,y,z):
#{
    #int m
    global counterFunctionCalls
    counterFunctionCalls = counterFunctionCalls + 1
    if x>y and x>z:
        m = x
    elif y>x and y>z:
        m = y 
    else:
        m = z
    return m
#}
     
     
def isPrime(x):
#{
    ## declarations for isPrime ##
    #int i

    def divides(x,y):
    #{
        ## body of divides ##
        global counterFunctionCalls
        counterFunctionCalls = counterFunctionCalls + 1
        if y == (y//x)*x:
            return 1
        else:
            return 0
    #}

    ## body of isPrime ##
    global counterFunctionCalls
    counterFunctionCalls = counterFunctionCalls + 1
    i = 2
    while i < x :
    #{
        if divides(i,x) == 1:
            return 0
        i = i + 1
    #}
    return 1
#}

     
def quad(x):
#{
    #int y
    
    ## nested function sqr ##
    def sqr(x):
    #{
        ## body of sqr ##
        global counterFunctionCalls
        counterFunctionCalls = counterFunctionCalls + 1
        return x*x
    #}
    
    ## body of quad ##
    global counterFunctionCalls
    x=3
    counterFunctionCalls = counterFunctionCalls + 1
    y = sqr(x)*sqr(x)
    return y
#}
        
#def main
#int i
counterFunctionCalls = 0

i = int(input())
print(i)


i = 1600
while i<=2000:
#{
    i = i + 400
#}
print(quad(3))

i=1
while i<=12:
#{
    print(isPrime(i))
    i = i + 1
#}

print(counterFunctionCalls)
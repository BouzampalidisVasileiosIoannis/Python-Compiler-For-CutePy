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


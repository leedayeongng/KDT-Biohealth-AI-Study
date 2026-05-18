def adder(a,b):
    sum=a+b
    return sum

print(adder(2,3))
def fn_return():
    return 1,"리턴!",True
print(fn_return())
a,b,c, = fn_return()
print(a,b,c)

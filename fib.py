def fib(n):
    if n==0 or n==1:
        return n
    f=[0,1]
    for i in range(n):
        f.append(f[-1]+f[-2])
    return f[-1]


print fib(0)
print fib(1)
print fib(2)
print fib(3)
print fib(4)
print fib(5)
print fib(6)
print fib(7)
print fib(8)
print fib(9)

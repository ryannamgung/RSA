# In the first part of this 2 part lab, you will write a python program to do
# some Modular Arithmetic basics. Pseudocode for all of these is in your book.

#Basics of Python Programming were covered in the first few minutes of lab.
#See the Python Example File for examples of functions.

# function extGCD
# inputs: two integers x,y
# outputs: three integers: d,s,t such that
#   d = gcd(x,y)
#   sx + ty = d


def extGCD(x, y):
    s0,s1,t0,t1 = 1, 0, 0 ,1
    while y != 0:
        d,x,y = x//y, y, x%y
        s0,s1 = s1, s0 - d * s1
        t0,t1 = t1, t0 - d * t1
    return x, s0, t0


# function expMod
# inputs: thre integers b,e,n
# output: b^e mod n
# This algorithm must work using the *fast* exponention algorithm described in
# lecture. The slow exponentiation algorithm is in the example file.

def expMod(b,e,n):
    x = 1
    while e > 0:
        if e % 2 == 1:
            x = x*b
            x = x%n
        e = e//2
        b = b*b
        b = b%n
    return x

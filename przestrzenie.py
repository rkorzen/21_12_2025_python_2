"""
To jest docstring modulu
"""

"""
xxxxxxx
"""

def foo():
    bbb = 1
    def bar():
        print(bbb)

    bar() 

    print("locals:", locals())
    print("globals:", globals())

foo()
print(dir(foo))

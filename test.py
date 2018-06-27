class A(object):
    def method1(self, a, b, c):
        return a + b

a = A()
method = getattr(a, 'method1')
print (method(1, 2,3))
"""
A library of functions
"""
import numpy as np
import matplotlib.pyplot as plt
import numbers

class AbstractFunction:
    """
    An abstract function class
    """

    def derivative(self):
        """
        returns another function f' which is the derivative of x
        """
        raise NotImplementedError("derivative")


    def __str__(self):
        return "AbstractFunction"


    def __repr__(self):
        return "AbstractFunction"


    def evaluate(self, x):
        """
        evaluate at x

        assumes x is a numeric value, or numpy array of values
        """
        raise NotImplementedError("evaluate")


    def __call__(self, x):
        """
        if x is another AbstractFunction, return the composition of functions

        if x is a string return a string that uses x as the indeterminate

        otherwise, evaluate function at a point x using evaluate
        """
        if isinstance(x, AbstractFunction):
            return Compose(self, x)
        elif isinstance(x, str):
            return self.__str__().format(x)
        else:
            return self.evaluate(x)


    # the rest of these methods will be implemented when we write the appropriate functions
    def __add__(self, other):
        """
        returns a new function expressing the sum of two functions
        """
        return Sum(self, other)


    def __mul__(self, other):
        """
        returns a new function expressing the product of two functions
        """
        return Product(self, other)


    def __neg__(self):
        return Scale(-1)(self)


    def __truediv__(self, other):
        return self * other**-1


    def __pow__(self, n):
        return Power(n)(self)


    def plot(self, vals=np.linspace(-1,1,100), **kwargs):
        """
        plots function on values
        pass kwargs to plotting function
        """
        y = self.evaluate(vals)
        plt.plot(vals,y,**kwargs)
        plt.show()


class Polynomial(AbstractFunction):
    """
    polynomial c_n x^n + ... + c_1 x + c_0
    """

    def __init__(self, *args):
        """
        Polynomial(c_n ... c_0)

        Creates a polynomial
        c_n x^n + c_{n-1} x^{n-1} + ... + c_0
        """
        self.coeff = np.array(list(args))


    def __repr__(self):
        return "Polynomial{}".format(tuple(self.coeff))


    def __str__(self):
        """
        We'll create a string starting with leading term first

        there are a lot of branch conditions to make everything look pretty
        """
        s = ""
        deg = self.degree()
        for i, c in enumerate(self.coeff):
            if i < deg-1:
                if c == 0:
                    # don't print term at all
                    continue
                elif c == 1:
                    # supress coefficient
                    s = s + "({{0}})^{} + ".format(deg - i)
                else:
                    # print coefficient
                    s = s + "{}({{0}})^{} + ".format(c, deg - i)
            elif i == deg-1:
                # linear term
                if c == 0:
                    continue
                elif c == 1:
                    # suppress coefficient
                    s = s + "{0} + "
                else:
                    s = s + "{}({{0}}) + ".format(c)
            else:
                if c == 0 and len(s) > 0:
                    continue
                else:
                    # constant term
                    s = s + "{}".format(c)

        # handle possible trailing +
        if s[-3:] == " + ":
            s = s[:-3]

        return s


    def evaluate(self, x):
        """
        evaluate polynomial at x
        """
        if isinstance(x, numbers.Number):
            ret = 0
            for k, c in enumerate(reversed(self.coeff)):
                ret = ret + c * x**k
            return ret
        elif isinstance(x, np.ndarray):
            x = np.array(x)
            # use vandermonde matrix
            return np.vander(x, len(self.coeff)).dot(self.coeff)


    def derivative(self):
        if len(self.coeff) == 1:
            return Polynomial(0)
        return Polynomial(*(self.coeff[:-1] * np.array([n+1 for n in reversed(range(self.degree()))])))


    def degree(self):
        return len(self.coeff) - 1


    def __add__(self, other):
        """
        Polynomials are closed under addition - implement special rule
        """
        if isinstance(other, Polynomial):
            # add
            if self.degree() > other.degree():
                coeff = self.coeff
                coeff[-(other.degree() + 1):] += other.coeff
                return Polynomial(*coeff)
            else:
                coeff = other.coeff
                coeff[-(self.degree() + 1):] += self.coeff
                return Polynomial(*coeff)

        else:
            # do default add
            return super().__add__(other)


    def __mul__(self, other):
        """
        Polynomials are clused under multiplication - implement special rule
        """
        if isinstance(other, Polynomial):
            return Polynomial(*np.polymul(self.coeff, other.coeff))
        else:
            return super().__mul__(other)


class Affine(Polynomial):
    """
    affine function a * x + b
    """
    def __init__(self, a, b):
        super().__init__(a, b)

# ---- PART B ----------------------

class Scale(Polynomial):
    '''
    input a
    output fx = a*x
    '''
    def __init__(self, a):
        super().__init__(a,0)

class Constant(Polynomial):
    '''
    input c
    output fx = c
    '''
    def __init__(self, c):
        super().__init__(c)

# ---- PART C ----------------------

class Compose(AbstractFunction):
    '''
    input f,g
    output f(g)
    '''
    def __init__(self,f,g):
        self.f = f
        self.g = g
    
    def __repr__(self):
        return 'Compose of {} and {}'.format(self.f.__repr__, self.g.__repr__)

    def __str__(self):
        return '{}({})'.format(str(self.f), str(self.g))

    def derivative(self):
        # f'(g(x)) g'(x)
        return Product(self.f.derivative()(self.g),self.g.derivative())

    def evaluate(self, x):
        # f(g(x))
        gx = self.g(x)
        return self.f(gx)

class Sum(AbstractFunction):
    def __init__(self,f,g):
        self.f = f
        self.g = g
    
    def __repr__(self):
        return 'Sum of {} and {} '.format(self.f.__repr__, self.g.__repr__) 

    def __str__(self):
        return '{} + {}'.format(str(self.f), str(self.g))

    def evaluate(self, x):
        # f(x) + g(x)
        return self.f(x) + self.g(x)
    
    def derivative(self):
        return Sum(self.f.derivative(), self.g.derivative())

class Product(AbstractFunction):
    def __init__(self,f,g):
        self.f = f
        self.g = g
    
    def __repr__(self):
        return 'Product of {} and {}'.format(self.f.__repr__, self.g.__repr__) 

    def __str__(self):
        return '{} * {}'.format(str(self.f), str(self.g))
        # return '{}({{0}}) * {}({{0}})'.format(str(self.f), str(self.g))

    def evaluate(self, x):
        # f(x) * g(x)
        return self.f(x) * self.g(x)
    
    def derivative(self):
        return Sum(Product(self.f.derivative(),self.g), Product(self.f,self.g.derivative()))

# ---- PART D ----------------------

import numpy as np

class Power(AbstractFunction):
    def __init__(self,n):
        self.n = n

    def __repr__(self):
        return 'to the power {}'.format(self.n) 

    def __str__(self):
        return '{{0}} ^ {}'.format(self.n)
    
    def evaluate(self, x):
        return x**self.n
    
    def derivative(self):
        return Product(Constant(self.n),Power(self.n-1))

class Log(AbstractFunction):
    def __init__(self):
        pass

    def __repr__(self):
        return 'take log'

    def __str__(self):
        return 'log({{0}})'
    
    def evaluate(self, x):
        return np.log(x)
    
    def derivative(self):
        return Power(-1)

class Exponential(AbstractFunction):
    def __init__(self):
        pass

    def __repr__(self):
        return 'take exp'

    def __str__(self):
        return 'e ^ {{0}}'
    
    def evaluate(self, x):
        return np.exp(x)
    
    def derivative(self):
        return Exponential()

class Sin(AbstractFunction):
    def __init__(self):
        pass

    def __repr__(self):
        return 'take sin'

    def __str__(self):
        return 'sin({{0}})'
    
    def evaluate(self, x):
        return np.sin(x)
    
    def derivative(self):
        return Cos()

class Cos(AbstractFunction):
    def __init__(self):
        pass

    def __repr__(self):
        return 'take sin'

    def __str__(self):
        return 'cos({{0}})'
    
    def evaluate(self, x):
        return np.cos(x)
    
    def derivative(self):
        return Product(Constant(-1),Sin())


# ---- PART E ----------------------
    

class Symbolic(AbstractFunction):
    def __init__(self,str):
        # str is the name of the symbolic func.
        self.f = str
    
    def __repr__(self):
        return 'Symbolic Function {}'.format(self.f)

    def __str__(self):
        return '{}({{0}})'.format(self.f)
    
    def derivative(self):
        return Symbolic(self.f+'\'')
    
    def __call__(self, x):
        return '{}({})'.format(self.f, x)
    
    
# ---- Problem 1 PartA ---------------------- 

def newton_root(f, x0, tol=1e-8):
    """
    find a point x so that f(x) is close to 0,
    measured by abs(f(x)) < tol

    Use Newton's method starting at point x0
    """
  
    if not isinstance(f, AbstractFunction):
        raise ValueError('f must be an AbstractFunction')
    if isinstance(f, Symbolic):
        raise ValueError('f must not be a Symbolic')
    # a type check to verify that f is an AbstractFunction but it is not Symbolic.

        
    x = x0
    fx = f.evaluate(x) #f(x)
    
    while(abs(fx)> tol):
        x = x - fx/f.derivative().evaluate(x)
        fx = f.evaluate(x)
        
    return x

 # ---- Problem 1 PartB ---------------------- 
def newton_extremum(f, x0, tol=1e-8):
    """
    find a point x which is close to a local maximum or minimum of f,
    measured by abs(f'(x)) < tol

    Use Newton's method starting at point x0
    """
    
    f = f.derivative()
    
    return newton_root(f,x0)
        


  
    


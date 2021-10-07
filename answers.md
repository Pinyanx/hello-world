# Answers

Put any answers to questions in the assignment in this file, or any commentary you don't include in the code.

This is a markdown file (the `.md` extension gives it away). If you have never used markdown before, check out [this short guide](https://guides.github.com/features/mastering-markdown/).

## Problem 0
You don't need to say anything here.  Just complete [`fizzbuzz.py`](fizzbuzz.py).

## Problem 1
The number of additions done is $\lfloor log_{2}^{n} \rfloor + #(n)$ in the Egyption multiplication algorithm. There are \lfloor log_{2}^{n} \rfloor levels of recursion. For each level of recurssion, if the bit of n is 0, then there is one addition done; if the bit is 1, then there are two additions done. Therefore, the number of additions is $\lfloor log_{2}^{n} \rfloor + #(n)$.

## Problem 2
The algorithm fibonacci_iter should be asymptotically faster. For fibonacci_iter, we only need to iterate n times. However, for fibonacci_recursive and for n large enough, the number of fibonacci number we need to compute in each level of recurssion is 2 times that of the previous level, so it grows like $2^{n}$.

## Problem 3
The number of operations done in multiplying A to itself is 12, which is a constant. By problem 1, the number of matrix multiplication done is $log_{2}^{n}$. So the assymptotic number of operations is O(log_{2}^{n}). It is faster than algorithms in problem 2.


The potential issue with large n is the approximation issue with floats. At some point, the floating point numbers may become inacurate. So I think np.int64 would be better.


## Problem 4
![fibonacci_runtime](fibonacci_runtime.png)


## Feedback

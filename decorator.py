#!/usr/bin/env python
# encoding: utf-8

# 函数装饰器
def memp(func):
    cache = {}

    def wrap(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]

    return wrap

# 第一题
@memp
def fibonacci(n):
    if n <= 1:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)


print(fibonacci(35))


# 第二题
@memp
def climb(n, steps):
    count = 0
    if n == 0:
        count = 1
    elif n > 0:
        for step in steps:
            count += climb(n - step, steps)
    return count


#print(climb(10, (1, 2, 3)))

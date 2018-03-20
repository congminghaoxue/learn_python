def multiplicator(x, y):
    ''' return x*y '''
    i = 0
    result = 0
    while i < x:
        result += y
        i += 1

    return result

assert multiplicator(2, 3) == 6

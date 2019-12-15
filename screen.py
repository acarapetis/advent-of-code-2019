def display(dct, symbols={}, ydir=1):
    def _s(v):
        return symbols.get(v, v)

    xmin = min(x[0] for x in dct.keys())
    ymin = min(x[1] for x in dct.keys())
    xmax = max(x[0] for x in dct.keys())
    ymax = max(x[1] for x in dct.keys())

    if ydir == 1:
        ys = range(ymax, ymin-1, -1)
    else:
        ys = range(ymin, ymax+1, 1)

    for y in ys:
        for x in range(xmin, xmax+1):
            print(_s(dct[(x,y)]), end='')
        print()

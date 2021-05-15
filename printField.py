
def printField(field, horizontal, vertical):
    m = 0
    for h in horizontal:
        if m < len(h):
            m = len(h)
    offset = 2 * m

    x = 0
    while True:
        go = False
        l = str()
        for v in vertical:
            try:
                l += str(v[x]) + "  "
                go = True
            except:
                l += "   "
        off = str()
        while len(off) < offset:
            off += " "
        off += "   "
        if go:
            print(off + l)
        else:
            break
        x+=1

    for y, line in enumerate(field):
        l = str()
        for x in line:
            if x != -1:
                l += " "
            l += " " + str(x)
        
        info = str()

        for i in horizontal[y]:
            info += str(i) + " "
        while len(info) < offset:
            info += " "
        info += "|"
        print(info + l)

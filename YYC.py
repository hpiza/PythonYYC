def loadBM(filename):
    bmFile = open(filename, 'r');
    rows = int(bmFile.readline())
    cols = int(bmFile.readline())
    bm = [[0 for c in range(cols)] for r in range(rows)]
    lines = bmFile.readlines()
    r = 0
    for line in lines:
        data = line.strip().split(" ")
        for c in range(cols):
            bm[r][c] = data[c] == '1'
        r += 1
    return bm

def findCompatibleSet(bm, tao, xp, currentRow, onesCountPerRow):
    cols = len(bm[0])
    marked = [c in tao for c in range(cols)]
    marked[xp] = True
    unitaryRowsCount = 0
    for rs in range(currentRow + 1):
        onesCountPerRow[rs] = 0
        sum = 0
        f = 0
        while f < cols and sum < 2:
            if marked[f] and bm[rs][f]:
                sum += 1
                onesCountPerRow[rs] += 1
            f += 1
        if sum == 1:
            unitaryRowsCount += 1
    if unitaryRowsCount < len(tao) + 1:
        return False
    for xk in range(cols):
        if marked[xk]:
            sumXk = 0
            for rs in range(currentRow + 1):
                if onesCountPerRow[rs] == 1 and bm[rs][xk]:
                    sumXk += 1
            if sumXk < 1:
                return False

    return True

def processIT(tj, ri, bm, psiaux, onesCountPerRow):
    cols = len(bm[0])
    found = False
    xp = 0
    while not found and xp < cols:
        if bm[ri][xp] and xp in tj:
            found = True
        xp += 1
    if found:
        psiaux.append(tj)
    else:
        for xp in range(cols):
            if bm[ri][xp] and findCompatibleSet(bm, tj, xp, ri, onesCountPerRow):
                tjxp = tj.copy()
                tjxp.add(xp)
                psiaux.append(tjxp)

def runYYC(bm):
    rows = len(bm)
    cols = len(bm[0])
    psi = []
    onesCountPerRow = [0 for r in range(rows)]
    for xj in range(cols):
        if bm[0][xj]:
            psi.append({xj})

    for ri in range(1, rows):
        print(ri, len(psi))
        psiaux = []
        for tj in psi:
            processIT(tj, ri, bm, psiaux, onesCountPerRow)
        psi = psiaux
    return psi

bm = loadBM('bol/mb40x42.bol')
itFound = runYYC(bm)
print(len(itFound))

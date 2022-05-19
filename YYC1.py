def loadBM(filename):
    bmFile = open(filename, 'r')
    rows = int(bmFile.readline())
    cols = int(bmFile.readline())
    bm = dict()
    lines = bmFile.readlines()
    r = 0
    for line in lines:
        data = line.strip().split(" ")
        bm[r] = {c for c in range(cols) if data[c] == '1'}
        r += 1
    return bm

def findCompatibleSet(bm, tao, xp, current_row):
    marked = tao | {xp}
    unitary_rows = 0
    '''
    rs = 0
    while rs < current_row + 1 and unitary_rows < len(tao) + 1:
        if len(bm[rs] & marked) == 1:
            unitary_rows += 1
        rs += 1
        '''
    for rs in range(current_row + 1):
        if len(bm[rs] & marked) == 1:
            unitary_rows += 1
    #unitary_rows = len([rs for rs in range(current_row + 1) if len(bm[rs] & marked) == 1])
    if unitary_rows < len(tao) + 1:
        return False
    for xk in marked:
        sumXk = len([rs for rs in range(current_row + 1) if len(bm[rs] & marked) == 1 and xk in bm[rs]])
        if sumXk < 1:
            return False
    return True

def processIT(tj, ri, bm, psiaux):
    xpInIT = bm[ri] & tj
    if len(xpInIT) > 0:
       psiaux.append(tj)
    else:
        for xp in bm[ri]:
            if findCompatibleSet(bm, tj, xp, ri):
                tjxp = tj.copy()
                tjxp.add(xp)
                psiaux.append(tjxp)

def runYYC(bm):
    psi = [{xj} for xj in bm[0]]
    for ri in range(1, len(bm)):
        print(ri, len(psi))
        psiaux = []
        for tj in psi:
            processIT(tj, ri, bm, psiaux)
        psi = psiaux
    return psi


from time import time
start_time = time()
bm = loadBM('bol/mb40x42.bol')
it_found = runYYC(bm)
print(len(it_found))
print(time() - start_time, "seconds")

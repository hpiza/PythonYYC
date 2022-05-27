import queue
import time
import threading

MAX_ATTEMPTS = 5
WAIT_TIME = 0.5 / 1000

bm = dict()
psi_queue = queue.Queue()
fcs_queue = queue.Queue()
it_found = list()

def load_bm(filename):
    bmFile = open(filename, 'r')
    bmFile.readline()
    cols = int(bmFile.readline())
    lines = bmFile.readlines()
    r = 0
    for line in lines:
        data = line.strip().split(" ")
        bm[r] = {c for c in range(cols) if data[c] == '1'}
        r += 1

def find_compatible_set(tao, xp, current_row):
    marked = tao | {xp}
    unitary_rows = 0
    for rs in range(current_row + 1):
        if len(bm[rs] & marked) == 1:
            unitary_rows += 1
    if unitary_rows < len(tao) + 1:
        return False
    for xk in marked:
        sumXk = len([rs for rs in range(current_row + 1) if len(bm[rs] & marked) == 1 and xk in bm[rs]])
        if sumXk < 1:
            return False
    return True

def dispatch_fcs_job():
    (tj, xp, ri) = fcs_queue.get()
    if find_compatible_set(tj, xp, ri):
        if ri < len(bm) - 1:
            psi_queue.put((ri, tj | {xp}))
        else:
            it_found.append(tj | {xp})

def dispatch_psi_job():
    (ri, tj) = psi_queue.get()
    ri += 1
    xpInIT = bm[ri] & tj
    if len(xpInIT) > 0:
        if ri < len(bm) - 1:
            psi_queue.put((ri, tj))
        else:
            it_found.append(tj)
    else:
        for xp in bm[ri]:
            fcs_queue.put((tj, xp, ri))

def empty_fcs_queue():
    finish = False
    while not finish:
        attempts = 0
        while not finish and fcs_queue.empty():
            attempts += 1
            time.sleep(WAIT_TIME)
            if attempts >= MAX_ATTEMPTS:
                finish = True
        if not finish:
            dispatch_fcs_job()

def empty_psi_queue():
    finish = False
    while not finish:
        attempts = 0
        while not finish and psi_queue.empty():
            attempts += 1
            time.sleep(WAIT_TIME)
            if attempts >= MAX_ATTEMPTS:
                finish = True
        if not finish:
            dispatch_psi_job()

def start():
    for xj in bm[0]:
        psi_queue.put((0, {xj}))
    psi_thread = threading.Thread(target=empty_psi_queue)
    fce_thread = threading.Thread(target=empty_fcs_queue)
    psi_thread.start()
    fce_thread.start()
    psi_thread.join()
    fce_thread.join()
    print(len(it_found))

start_time = time.time()
load_bm('bol/mb80x42.bol')
start()
print(time.time() - start_time, "seconds")

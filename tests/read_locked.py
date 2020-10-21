try:
    from fslock.core.lock import FileLock
except ImportError:
    from core.lock import FileLock

fpath = r"C:\Files\Projects\fslock\test.txt"

fl = FileLock(fpath)
fl.acquire()
f = open(fpath, "w")
f.write("garbage")
fl.release()


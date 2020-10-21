import core.portable_locker as pl
import errno
import time
import os

"""
    Original code by @dmfrey on github: https://github.com/dmfrey/FileLock
    I modified the code for Python 3 + some minor, mostly syntactic-sugar changes
    My biggest change is importing portalock (aliased as porable_lock in this project)
    to ensure file locking on global OS-level :)
"""


class FileLockException(Exception):
    pass


class FileLock:
    """ A file locking mechanism that has context-manager support so
        you can use it in a with statement. This should be relatively cross
        compatible as it doesn't rely on msvcrt or fcntl for the locking.
    """

    def __init__(
            self,
            file_name: str,
            timeout: float = 10,
            delay: float = .05,
            directory: str = os.getcwd()
    ):
        """ Prepare the file locker. Specify the file to lock and optionally
            the maximum timeout and the delay between each attempt to lock.
        """
        self.is_locked: bool = False
        self.lockfile: str = os.path.join(directory, f"{file_name}.lock")
        self.file_name: str = file_name
        self.timeout: float = timeout
        self.delay: float = delay
        self.f = open(os.path.join(directory, file_name), "r+")
        self.fd: int = 0
        if (delay is None) and (timeout is not None):
            raise ValueError("If timeout is set, a delay must be set as well.")

    def acquire(self):
        """ Acquire the lock, if possible. If the lock is in use, it check again
            every `wait` seconds. It does this until it either gets the lock or
            exceeds `timeout` number of seconds, in which case it throws
            an exception.
        """
        start_time: float = time.time()
        while True:
            try:
                self.fd = os.open(self.lockfile, os.O_CREAT | os.O_EXCL | os.O_RDWR)
                self.is_locked = True
                pl.lock(self.f, pl.LOCK_EX)
                break
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
                if self.timeout is None:
                    raise FileLockException(f"Could not acquire lock on {self.file_name}")
                if (time.time() - start_time) >= self.timeout:
                    raise FileLockException("Timeout occurred.")
                time.sleep(self.delay)

    def release(self):
        """ Get rid of the lock by deleting the lockfile.
            When working in a `with` statement, this gets automatically
            called at the end.
        """
        if self.is_locked:
            os.close(self.fd)
            os.unlink(self.lockfile)
            self.is_locked = False
            pl.unlock(self.f)
            self.f.close()

    def __enter__(self):
        """ Activated when used in the with statement.
            Should automatically acquire a lock to be used in the with block.
        """
        if not self.is_locked:
            self.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """ Activated at the end of the with statement.
            It automatically releases the lock if it isn't locked.
        """
        if self.is_locked:
            self.release()

    def __del__(self):
        """ Make sure that the FileLock instance doesn't leave a lockfile
            lying around.
        """
        self.release()

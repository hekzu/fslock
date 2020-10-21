from unittest import TestCase, main
from core.lock import FileLock


class FirstCase(TestCase):
    def test_first(self):
        lock = FileLock("a.txt")
        lock.acquire()
        print(lock.is_locked)
        input("Press Enter to continue...")
        lock.release()


if __name__ == '__main__':
    main()

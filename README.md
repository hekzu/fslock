# FSLock
File locking on OS level

### Welcome!
I created this project because I was required to lock a file in a way that no other process will be able to open it.
(For the specific use case - global state handling between multiple k8s pods over persistent storage)

Code is a mix of "Filelock" by @dmfrey over on https://github.com/dmfrey/FileLock
and a random piece of code i found over at https://www.oreilly.com/library/view/python-cookbook/0596001673/ch04s25.html

You're welcome to submit PRs, issues, or just copy code off here :)

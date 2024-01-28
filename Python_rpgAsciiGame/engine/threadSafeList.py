# import threading
#
# class ThreadSafeList:
#
#     def __init__(self):
#         self.ls = []
#         self.readers = 0
#         self.reader = threading.Semaphore()
#         self.readerWriter = threading.Semaphore()
#
#     def push(self, val):
#         self.readerWriter.acquire()
#         self.ls.append(val)
#         self.readerWriter.release()
#
#     def modify(self, indx, val):
#         self.readerWriter.acquire()
#         self.ls[indx] = val
#         self.readerWriter.release()
#
#
#     def get(self, startIndx, endIndx=None):
#         self.reader.acquire()
#         self.readers += 1
#
#         if self.readers == 1:
#             self.readerWriter.acquire()
#         self.reader.release()
#         if endIndx != None:
#             val = self.ls[startIndx:endIndx]
#         else:
#             val = self.ls[startIndx]
#
#         self.reader.acquire()
#         self.readers -= 1
#
#         if self.readers == 0:
#             self.readerWriter.release()
#
#         self.reader.release()
#
#         return val


import threading

class ThreadSafeList:

    def __init__(self):
        self.ls = []
        self.lock = threading.RLock()

    def push(self, val):
        with self.lock:
            self.ls.append(val)

    def modify(self, indx, val):
        with self.lock:
            self.ls[indx] = val

    def get(self, startIndx, endIndx=None):
        with self.lock:
            if endIndx is not None:
                val = self.ls[startIndx:endIndx]
            else:
                val = self.ls[startIndx]
            return val

    def length(self):
        return len(self.ls)
from hardware.hardware import HARDWARE
from helpers import log



class MemoryManager():

    def __init__(self):
        self._process_table = {}
        self._currentPage = 0

    @property
    def kernel(self):
        return self._kernel

    def loadProcess(self, process, instructions, start, end):
        process._memory_start = start
        process._memory_end = end
        process._size = end - start
        process._pc = start
        progSize = len(instructions)
        HARDWARE.mmu.addRefPage(process._pid)
        for index in range(0, progSize):
            inst = instructions[index]
            HARDWARE.mmu.write(process._memory_start + index, inst, self._currentPage, process._pid)
        self._currentPage = HARDWARE.mmu.getFirstPageEmpty()
        ##print(HARDWARE.mmu.pages)

    def freeMemory(self, process):
        for index in range(0, process.size):
            HARDWARE.mmu.removeFromMemory(index + process._memory_start , " ")
        HARDWARE.mmu.removeFromPages(process._pid)
        print(HARDWARE.mmu.pages)
    
    def read(self, addr, pageNro):
        return HARDWARE.mmu.read(addr, pageNro)
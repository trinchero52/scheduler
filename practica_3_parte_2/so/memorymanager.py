from hardware.hardware import HARDWARE

# agregar a mmu process id - paginas
# process, scheduler, cpu manejan memoria virtual (tuplas)
# MMU sabes la siguiente direccion virtual para un process id
# que ande


class MemoryManager():

    def __init__(self):
        self._currentPage = 0

    def loadProcess(self, pid, instructions):
        """Load process in memory"""
        blocks = self.instructionsInBlock(instructions)
        freePages = HARDWARE.mmu.freePages(len(blocks))
        HARDWARE.mmu.asociatePagesFromProcess(pid, freePages)
        HARDWARE.mmu.loadProcessInPages(pid, blocks)
        HARDWARE.mmu.loadProcessInMemory(pid)
        return freePages

    def unloadProcess(self, pid):
        """Unload process in memory"""
        HARDWARE.mmu.unloadProcess(pid)

    def read(self, pid, addr, pageNro):
        """"Read instruction with virtual addr in memory"""
        return HARDWARE.mmu.read(pid, addr, pageNro)

    def read_raw(self, addr):
        """"Read instruction with addr in memory"""
        return HARDWARE.mmu.read_raw(addr)

    def instructionsInBlock(self, inst):
        """"Return instructions in blocks"""
        blocks = [[]]
        for i in range(0, len(inst)):
            currentBlock = blocks[len(blocks) - 1]
            if(len(currentBlock) >= HARDWARE.mmu._pages_size):
                blocks.append([])
                currentBlock = blocks[len(blocks) - 1]
            currentBlock.append(inst[i])
        return blocks

    def hasProcess(self, pid):
        """Return if this pid has process"""
        return HARDWARE.mmu.hasProcess(pid)

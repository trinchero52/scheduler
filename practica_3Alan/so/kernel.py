from multiprocessing.dummy import Process
from helpers import log
from hardware.hardware import HARDWARE
from hardware.irq import IRQ
from so import process
from so.handlers.kill_interruption_handler import KillInterruptionHandler
from so.scheduler import Scheduler
from so.memoryManager import MemoryManager
from so.process import Process

# Emula el kernel del sistema operativo
class Kernel():

    def __init__(self):
        self._scheduler = Scheduler()
        self._memoryManager = MemoryManager()
        self._next_memory_addr = 0
        self._tableProcess = {}

        ## Configurar los manejadores de interrupciones y registrarlos en el hardware.
        killHandler = KillInterruptionHandler(self)
        HARDWARE.interruptVector.register(IRQ.KILL_INTERRUPTION_TYPE, killHandler)

    @property
    def scheduler(self):
        return self._scheduler

    @property
    def memoryManager(self):
        return self._memoryManager

    @property
    def next_memory_addr(self):
        return self._next_memory_addr

    @next_memory_addr.setter
    def next_memory_addr(self, value):
        self._next_memory_addr = value

    def load_program(self, program):
        # loads the program in main memory

        progSize = len(program.instructions)
        process = self._scheduler.create_process(program.name, self._next_memory_addr, self._next_memory_addr + progSize)
        self.memoryManager.loadProcess(process, program.instructions, self._next_memory_addr, self._next_memory_addr + progSize)
        self.next_memory_addr = self.next_memory_addr + progSize
       

    def freeMemory(self, pid):
        process = self._scheduler._process_table.get(pid)
        self.memoryManager.freeMemory(process)


    ## emulates a "system call" for programs execution
    def run(self, program):
        self.load_program(program)
        log.logger.info(HARDWARE)

        # set CPU program counter at program's first intruction
        self._scheduler.load_next_process(HARDWARE.cpu)

    ## emulates a "system call" for multiple programs execution
    def executeBatch(self, programs):
        for program in programs:
            self.load_program(program)

        log.logger.info(HARDWARE)

        self._scheduler.load_next_process(HARDWARE.cpu)

    def __repr__(self):
        return "Kernel "
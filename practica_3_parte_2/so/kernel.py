from sched import scheduler
from helpers import log
from hardware.hardware import HARDWARE
from hardware.irq import IRQ
from so.memorymanager import MemoryManager
from so.handlers.kill_interruption_handler import KillInterruptionHandler
from so.scheduler import Scheduler

# Emula el kernel del sistema operativo
class Kernel():

    def __init__(self):
        self._memorymanager = MemoryManager()
        self._scheduler = Scheduler(self._memorymanager)

        ## Configurar los manejadores de interrupciones y registrarlos en el hardware.
        killHandler = KillInterruptionHandler(self)
        HARDWARE.interruptVector.register(IRQ.KILL_INTERRUPTION_TYPE, killHandler)

    def load_program(self, program):
        """Loads the program in main memory"""
        process = self._scheduler.create_process(program.name)
        process._pages = self._memorymanager.loadProcess(process._pid, program.instructions)

    def unload_process(self, pid):
        """Unload the program in main memory"""
        self._memorymanager.unloadProcess(pid)

    def run_processes(self):
        """Run all processes"""
        if(self._memorymanager.hasProcess(0)):
            self._scheduler.load_process(HARDWARE.cpu,0)
        else:
            HARDWARE.switchOff()
            raise RuntimeError("Process not load in memory!")

    def read(self, pid, addr, pageNro):
        """"Read instruction with virtual addr in memory"""
        return self._memorymanager.read(pid, addr, pageNro)

    def read_raw(self,addr):
        """"Read instruction with addr in memory"""
        return self._memorymanager.read_raw(addr)

    def __repr__(self):
        return "Kernel"

    @property
    def scheduler(self):
        return self._scheduler

    @property
    def memorymanager(self):
        return self._memorymanager
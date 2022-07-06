from hardware.hardware import HARDWARE
from hardware.asm import ASM
from so.kernel import Kernel
from so.program import Program
from so.memorymanager import MemoryManager
from helpers import log


##
##  MAIN
##
if __name__ == '__main__':
    log.setupLogger()
    log.logger.info('Starting emulator')

    HARDWARE.setup(20, 8)

    kernel = Kernel()

    prg1 = Program("prg1.exe", [ASM.CPU(2), ASM.IO(), ASM.CPU(3)])
    prg2 = Program("prg2.exe", [ASM.CPU(4), ASM.IO(), ASM.CPU(1)])
    prg3 = Program("prg3.exe", [ASM.CPU(3)])
    prg4 = Program("prg4.exe", [ASM.CPU(4), ASM.IO(2), ASM.CPU(2)])
    prg5 = Program("prg4.exe", [ASM.CPU(3), ASM.IO(2), ASM.CPU(2)])

    kernel.load_program(prg1)
    kernel.load_program(prg2)

    log.logger.info(HARDWARE)

    HARDWARE.switchOn()

    #kernel.read_raw(0)
    #kernel.read(0,0,0)
    kernel.run_processes()

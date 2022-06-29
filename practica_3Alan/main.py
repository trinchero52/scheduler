from hardware.hardware import HARDWARE
from hardware.asm import ASM
from so.kernel import Kernel
from so.program import Program
from helpers import log
from so.memoryManager import MemoryManager


##
##  MAIN
##
if __name__ == '__main__':
    log.setupLogger()
    log.logger.info('Starting emulator')

    ## Configurar nuestro hardware con 20 espacios de memoria y velocidad 1
    HARDWARE.setup(20, 8)

    ## Crear el Kernel del sistema operativo.
    # "booteamos" el sistema operativo
    kernel = Kernel()
    memoryManager = MemoryManager()

    ##  Crear un programa
    # prg = Program("test.exe", [ASM.CPU(2), ASM.IO(), ASM.CPU(3), ASM.IO(), ASM.CPU(3)])

    # Ejecutamos el programa
    # kernel.run(prg)

    prg1 = Program("prg1.exe", [ASM.CPU(2), ASM.IO(), ASM.CPU(3)])
    prg2 = Program("prg2.exe", [ASM.CPU(4), ASM.IO(), ASM.CPU(1)])
    prg3 = Program("prg3.exe", [ASM.CPU(3)])
    prg4 = Program("prg4.exe", [ASM.CPU(2)])

    kernel.load_program(prg1)
    kernel.load_program(prg2)
    kernel.load_program(prg3)

    kernel.freeMemory(1)

    ##print(memoryManager.read(2))
    

    

    log.logger.info(HARDWARE)


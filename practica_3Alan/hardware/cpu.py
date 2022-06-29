from helpers import log
from hardware.asm import ASM
from hardware.irq import IRQ

## Emula el CPU
class Cpu():

    def __init__(self, memory, interruptVector):
        self._memory = memory
        self._interruptVector = interruptVector
        self._pc = -1
        self._ir = None


    def tick(self, tickNbr):
        if (self._pc > -1):
            self._fetch()
            self._decode()
            self._execute()
        else:
            log.logger.info("cpu - NOOP")

    def _fetch(self):
        self._ir = self._memory.read(self._pc)
        self._pc += 1

    def _decode(self):
        ## decode no hace nada en este caso
        pass

    def _execute(self):
        if ASM.isEXIT(self._ir):
            killIRQ = IRQ.KILL_INTERRUPTION()
            self._interruptVector.handle(killIRQ)
        else:
            log.logger.info("cpu - Exec: {instr}, PC={pc}".format(instr=self._ir, pc=self._pc-1))

    @property
    def pc(self):
        return self._pc

    @pc.setter
    def pc(self, addr):
        self._pc = addr

    def __repr__(self):
        return "CPU(PC={pc})".format(pc=self._pc)

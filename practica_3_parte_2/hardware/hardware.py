from helpers import log
from hardware.cpu import Cpu
from hardware.memory import Memory
from hardware.mmu import MMU
from hardware.interrupt_vector import InterruptVector
from hardware.clock import Clock

## Emula el hardware donde corre el sistema operativo
class Hardware():

    ## Configurar el hardware
    def setup(self, memorySize, clockSpeed):
        ## Agregar los componentes al "motherboard"
        self._interruptVector = InterruptVector()
        self._memory = Memory(memorySize)
        self._mmu = MMU(self._memory)
        self._clock = Clock(1 / clockSpeed)

        ## "cablear" los componentes entre ellos.
        self._cpu = Cpu(self._memory, self._mmu, self._interruptVector)
        self._clock.addSubscriber(self._cpu)

    @property
    def cpu(self):
        return self._cpu

    @property
    def mmu(self):
        return self._mmu

    @property
    def clock(self):
        return self._clock

    @property
    def interruptVector(self):
        return self._interruptVector

    @property
    def memory(self):
        return self._memory

    def __repr__(self):
        return "HARDWARE state {cpu}\n{mem}".format(cpu=self._cpu, mem=self._memory)

    def switchOn(self):
        log.logger.info(" ---- SWITCH ON ---- ")
        return self.clock.start()

    def switchOff(self):
        self.clock.stop()
        log.logger.info(" ---- SWITCH OFF ---- ")


### HARDWARE es una variable global, se puede acceder desde cualquier lado.
HARDWARE = Hardware()
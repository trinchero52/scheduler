## Utilidad para codigo compilado
class ASM():
    ##  Estas son la instrucciones soportadas por nuestro CPU
    INSTRUCTION_EXIT = 'EXIT'
    INSTRUCTION_IO = 'IO'
    INSTRUCTION_CPU = 'CPU'

    @classmethod
    def EXIT(self):
        return ASM.INSTRUCTION_EXIT

    @classmethod
    def IO(self, times=1):
        return [ASM.INSTRUCTION_IO] * times

    @classmethod
    def CPU(self, times=1):
        return [ASM.INSTRUCTION_CPU] * times

    @classmethod
    def isEXIT(self, instruction):
        return ASM.INSTRUCTION_EXIT == instruction

    @classmethod
    def isIO(self, instruction):
        return ASM.INSTRUCTION_IO == instruction

    @classmethod
    def isCPU(self, instruction):
        return ASM.INSTRUCTION_CPU == instruction
from hardware.asm import *

## Emula un programa compilado
class Program():

    def __init__(self, name, instructions):
        self._name = name
        self._instructions = self.expand(instructions)

    @property
    def name(self):
        return self._name

    @property
    def instructions(self):
        return self._instructions

    def addInstr(self, instruction):
        self._instructions.append(instruction)

    def expand(self, instructions):
        expanded = []
        for i in instructions:
            if isinstance(i, list):
                ## Es una lista de instrucciones
                expanded.extend(i)
            else:
                ## Es una unica instruccion, string
                expanded.append(i)

        ## Ahora verificar si la ultima instruccion es EXIT
        ## si no... agregar un EXIT como instruccion final.
        last = expanded[-1]
        if not ASM.isEXIT(last):
            expanded.append(ASM.EXIT())

        return expanded

    def __repr__(self):
        return "Program({name}, {instructions})".format(name=self._name, instructions=self._instructions)
#!/usr/bin/env python

from hardware import *
from time import sleep
import log
# import Scheduler from scheduler


# emulates a compiled program
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
                # is a list of instructions
                expanded.extend(i)
            else:
                # a single instr (a String)
                expanded.append(i)

        # now test if last instruction is EXIT
        # if not... add an EXIT as final instruction
        last = expanded[-1]
        if not ASM.isEXIT(last):
            expanded.append(INSTRUCTION_EXIT)

        return expanded

    def __repr__(self):
        return "Program({name}, {instructions})".format(name=self._name, instructions=self._instructions)

# emulates the core of an Operative System


class Kernel():

    def __init__(self):
        pass

    def load_program(self, program):
        # loads the program in main memory
        progSize = len(program.instructions)
        for index in range(0, progSize):
            inst = program.instructions[index]
            HARDWARE.memory.write(index, inst)

    # emulates a "system call" for programs execution
    def run(self, program):
        self.load_program(program)
        log.logger.info(
            "\n Executing program: {name}".format(name=program.name))
        log.logger.info(HARDWARE)

        # set CPU program counter at program's first intruction
        HARDWARE.cpu.pc = 0
        progSize = len(program.instructions)
        for i in range(0, progSize):
            HARDWARE.cpu.tick(i)
            sleep(1)

    def __repr__(self):
        return "Kernel "


class Process():

    def _init_(self, name, memoryStart, memoryEnd, pid, pc, status):
        self.name = name
        self.memoryStart = memoryStart
        self.memoryEnd = memoryEnd
        self.pid = pid
        self.pc = pc
        self.status = status

    def name(self):
        return self.name

    def memoryEnd(self):
        return self.memoryEnd

    def memoryStart(self):
        return self.memoryStart

    def pid(self):
        return self.pid

    def pc(self):
        return self.pc

    def status(self):
        return self.status


class Scheduler():

    def _init_(self):
        self.queue = []
        self.tabla = {}
        self.tail = 0

    def create(self):
        return self

    def load(self):
        return self

    def unload(self):
        return self

    def kill(self):
        return self

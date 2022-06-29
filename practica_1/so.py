from hardware import *
from time import sleep
import log

STATUS_RUNNING = 'RUNNING'
STATUS_WAITING = 'WAITING'
STATUS_BLOCKED = 'BLOCKED'
STATUS_CREATED = 'CREATED'
STATUS_FINISH = 'FINISH'

# emulates a compiled program


class Program():

    def _init_(self, name, instructions):
        self._name = name
        self._instructions = self.expand(instructions)

    @property
    def name(self):
        return self._name

    @property
    def instructions(self):
        return self._instructions

    def _len_(self):
        return len(self._instructions)

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

    def _repr_(self):
        return "Program({name}, {instructions})".format(name=self._name, instructions=self._instructions)

# emulates the core of an Operative System


class Kernel():

    # Primero crear processor
    # cargarlo

    def _init_(self):
        self._nextMemoryAddress = 0
        self._scheduler = Scheduler()

    @property
    def nextMemoryAddress(self):
        return self._nextMemoryAddress

    @nextMemoryAddress.setter
    def nextMemoryAddress(self, value):
        self._nextMemoryAddress = value

    def executeBatch(self, batch):
        for index in batch:
            self.load_program(index)
        self.runBatch()

    def load_program(self, program):
        # Carga el programa en memoria.
        progSize = len(program)
        procces = self._scheduler.create(
            program, self.nextMemoryAddress, self.nextMemoryAddress + progSize)
        self._scheduler.load(procces.pid)
        for index in range(0, progSize):
            inst = program.instructions[index]
            HARDWARE.memory.write(index + self.nextMemoryAddress, inst)

        self.nextMemoryAddress = self.nextMemoryAddress + progSize

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

    def runBatch(self):
        log.logger.info(HARDWARE)
        while self._scheduler.hasNEXT():
            self._scheduler.loadNextProcess()
            process = self._scheduler.tablaDeProcesos[self._scheduler._currentProcess]
            progSize = len(process.program)
            HARDWARE.cpu.pc = process.memoryStart
            log.logger.info("\n Executing program: {name}".format(
                name=process.program.name))
            for i in range(0, progSize):
                HARDWARE.cpu.tick(i)
                sleep(1)
            self._scheduler.kill(self._scheduler._currentProcess)

    def _repr_(self):
        return "Kernel "


class Process():

    def _init_(self, pid, program, memoryStart, memoryEnd):
        self._program = program
        self._memoryStart = memoryStart
        self._memoryEnd = memoryEnd
        self._pid = pid
        self._status = STATUS_CREATED

    @property
    def program(self):
        return self._program

    @property
    def memoryEnd(self):
        return self._memoryEnd

    @property
    def memoryStart(self):
        return self._memoryStart

    @property
    def pid(self):
        return self._pid

    @property
    def pc(self):
        return self._pc

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value


class Scheduler():

    def _init_(self):
        self._process_queue = []
        self._tabla_de_procesos = {}
        self._proximo_pid = 0
        self._currentProcess = 0

    # geters
    @property
    def processQueue(self):
        return self._process_queue

    @property
    def tablaDeProcesos(self):
        return self._tabla_de_procesos

    @property
    def proximoPid(self):
        return self._proximo_pid

    @proximoPid.setter
    def proximoPid(self, value):
        self._proximo_pid = value

    def create(self, name, memoriaInicio, memoriaFin):
        process = Process(self.proximoPid, name, memoriaInicio, memoriaFin)
        self._tabla_de_procesos[self.proximoPid] = process
        self.processQueue.append(self.proximoPid)
        self.proximoPid += 1
        return process

    def load(self, pid):
        processEncontrado = self.tablaDeProcesos.get(pid)
        processEncontrado.status = STATUS_RUNNING
        self._currentProcess = pid

    def unload(self, pid):
        processEncontrado = self.tablaDeProcesos.get(pid)
        processEncontrado.status = STATUS_WAITING
        self._currentProcess = None

    def kill(self, pid):
        self.unload(pid)
        self.tablaDeProcesos.pop(pid)
        self._process_queue.pop(0)

    def loadNextProcess(self):
        self.load(self.processQueue[0])

    def hasNEXT(self):
        return len(self.processQueue) != 0

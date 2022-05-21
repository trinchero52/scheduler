#!/usr/bin/env python

from msilib.schema import tables
from platform import processor
from socket import VMADDR_CID_ANY
from hardware import *
from time import sleep
import log
# import Scheduler from scheduler
# STATUS LOS ESTADOS SON RUNNING WAITING BLOCKED CREATED Y FINISH
STATUS_RUNNING = 'RUNNING'
STATUS_WAITING = 'WAITING'
STATUS_BLOCKED = 'BLOCKED'
STATUS_CREATED = 'CREATED'
STATUS_FINISH = 'FINISH'

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

    def _init_(self, name, memoryStart, memoryEnd):
        self._name = name
        self._memoryStart = memoryStart
        self._memoryEnd = memoryEnd
        self._pid = int  # preguntar como va el pid en el process
        self._pc = pc  # preguntar que va aca
        self._status = status  # el estado por ahora no lo usamos capaz metemeos un enum

    @property
    def name(self):
        return self._name

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


class Scheduler():

    def _init_(self):
        # cola donde cargo los procesos que voy a ir sacando de la cola cuando ejejuto y terminan
        self._process_queue = []
        # esto es un mapa clave valor llamado diccionario
        self._tabla_de_procesos = {}
        self._proximo_pid = 1
        # pid que corre actual aca capaz que va el el ultimo pid de la cola ingresado
        self._currentProcess = int
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

    def create(self, name, memoriaInicio, memoriaFin):
        # aca hay que asignar pid actual y luego incrementarlo en 1 para el proximo queviene
        # crea ael proceso y llo mete en la tabla de procesos
        # y guardar el pid del proceso que acabo de crear en la  de proce queue en la cola de procesos el queue
        # PREGUNTAR SI VA POR ACA
        process = Process(name, memoriaInicio, memoriaFin)
        self._tabla_de_procesos = {self.proximoPid: process}
        self._process_queue.append(self.proximoPid)
        self.proximoPid = + 1

    def load(self, pid):
        # lo que hace es buscar e proceso con el pid en la process table
        # cargar el proceso en el cpu
        # y cambiar estado del proceso(el proceso tiene un progam counter y)
        # actualizo el pc a la clase cpu y le cambio el status al proceso a estado ejecutando running
        # actualiza current process
        processEncontrado = self.tablaDeProcesos.get(pid)
        HARDWARE.cpu.pc = processEncontrado.pid
        processEncontrado.status = STATUS_RUNNING
        self._currentProcess = self._proximo_pid - 1  # preguntar si es asi esto

    def unload(self, pid):
        # buscar proceso con el pid en process table

        # lo contrario a load . el que voy a descargar es el pid que coincide con el pid que tiene el pc de la clase cpu
        # dudas
        # cargar lo del cpu en el proceso y cambiar el estado del proceso a waiting(LOS ESTADOS SON RUNNING WAITING BLOCKED CREATED Y FINISH)
        # actualiza current process
        processEncontrado = self.tablaDeProcesos.get(pid)
        processEncontrado.pid = HARDWARE.cpu.pc
        processEncontrado.status = STATUS_WAITING
        self._currentProcess = None  # preguntar si es asi

    def kill(self, pid):
        # eliminar de process table el pid y su proceso asociado sacar la clave valor
        # eliminar de process queue el pid
        # ojo con current process
        # preguntar si asi borra el valor asociado a esta clave si es que borra todo junto el par
        self._tablaDeProcesos.pop(pid)
        self._process_queue.remove(pid)
        self._currentProcess = None  # preguntar

    def loadNextProcess(self):
        # carga el proceso sigueijnte de process queue
        # llamar a load process con el proximo de queue
        self.load(self._proximo_pid)  # preguntar

    def hasnEXT(self):
        # INDICA SI PROCESS QUEUE NO  ESTA VMADDR_CID_ANY
        # ESTO USO PARA CORRER AFUERA DE SCHEDULER CUANDO EJECUTA EL KERNEL
        return self._process_queue.__len__ != 0  # preguntar

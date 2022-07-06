from tkinter.messagebox import NO
from helpers import log

# A Process representation on the Process Table
class Process():
    ##  Estas son los estados posibles de un proceso
    PROCESS_STATUS_CREATED = "CREATED"
    PROCESS_STATUS_RUNNING = "RUNNING"
    PROCESS_STATUS_WAITING = "WAITING"
    PROCESS_STATUS_BLOCKED = "BLOCKED"
    PROCESS_STATUS_FINISHED = "FINISHED"

    def __init__(self, name, pid):
        self._name = name
        self._pid = pid
        self._pages = None
        self._status = Process.PROCESS_STATUS_CREATED

    @property
    def name(self):
        return self._name

    @property
    def pid(self):
        return self._pid

    @property
    def size(self):
        return self._size

    @property
    def pages(self):
        return self._pc

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        self._status = status

    def __repr__(self):
        return "Process(PID={pid}, STATUS={status})".format(pid=self.pid, status=self.status)

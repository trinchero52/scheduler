from helpers import log

# A Process representation on the Process Table
class Process():
    ## Estas son los estados posibles de un proceso
    PROCESS_STATUS_CREATED = "CREATED"
    PROCESS_STATUS_RUNNING = "RUNNING"
    PROCESS_STATUS_WAITING = "WAITING"
    PROCESS_STATUS_BLOCKED = "BLOCKED"
    PROCESS_STATUS_FINISHED = "FINISHED"

    def __init__(self, name, pid, memory_start, memory_end):
        self._name = name
        self._pid = pid
        self._memory_start = memory_start
        self._memory_end = memory_end
        self._pc = memory_start
        self._size = memory_end - memory_start
        self._pageStart = None
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
    def pc(self):
        return self._pc

    @property
    def status(self):
        return self._status

    @pc.setter
    def pc(self, addr):
        if (addr < self._memory_start or addr > self._memory_end):
            log.logger.error("SECURITY ALERT: Out of range at: {addr} in process: {pid}".format(addr=addr, pid=self._pid))
            exit
        self._pc = addr

    @status.setter
    def status(self, status):
        self._status = status

    def __repr__(self):
        return "Process(PID={pid}, STATUS={status})".format(pid=self.pid, status=self.status)

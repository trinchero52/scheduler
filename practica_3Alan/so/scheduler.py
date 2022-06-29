from helpers import log
from so.process import Process

# emulates the Operative System's Scheduler
class Scheduler():
    def __init__(self):
        self._current_process = None
        self._next_pid = 0
        self._process_queue = []
        self._process_table = {}

    @property
    def current_pid(self):
        return self._current_process

    @property
    def current_process(self):
        return self._process_table[self._current_process]

    def create_process(self, name, memory_start, memory_end):
        if (memory_start > memory_end):
            log.logger.error("Invalid memory address creating process with ID '{pid}'".format(pid=self._pid))
            exit
        self._process_queue.append(self._next_pid)
        self._process_table[self._next_pid] = Process(name, self._next_pid, memory_start, memory_end)
        self._next_pid += 1
        return self._process_table[self._next_pid -1]

    def unload_process(self, cpu, pid):
        proc = self._get_process_by_id(pid)
        proc.status = Process.PROCESS_STATUS_WAITING
        proc.pc = cpu.pc
        self._current_process = None

    def load_process(self, cpu, pid):
        proc = self._get_process_by_id(pid)
        proc.status = Process.PROCESS_STATUS_RUNNING
        cpu.pc = proc.pc
        self._current_process = pid

    def kill_process(self, pid):
        proc = self._get_process_by_id(pid)
        proc.status = Process.PROCESS_STATUS_FINISHED
        self._process_queue.remove(pid)
        self._process_table.pop(pid)
        if (self._current_process == pid):
            self._current_process = None

    def has_next_process(self):
        return len(self._process_queue) > 0

    def kill_current_process(self):
        self.kill_process(self._current_process)

    def load_next_process(self, cpu):
        if (len(self._process_queue) == 0):
            log.logger.error("Nothing to load")
        if (self._current_process is not None):
            self.unload_process(cpu, self._current_process)
        self.load_process(cpu, self._process_queue[0])

    def _get_process_by_id(self, pid):
        if (pid not in self._process_table):
            log.logger.error("Process with ID '{pid}' does not exist".format(pid=pid))
            exit
        return self._process_table[pid]

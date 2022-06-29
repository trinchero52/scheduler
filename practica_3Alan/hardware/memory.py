from helpers.tabulate import tabulate

## Emula la memoria principal, RAM
class Memory():

    def __init__(self, size):
        self._size = size
        self._cells = [''] * size

    def write(self, addr, value):
        self._cells[addr] = value

    def read(self, addr):
        return self._cells[addr]

    @property
    def size(self):
        return self._size

    def __repr__(self):
        return tabulate(enumerate(self._cells), tablefmt='psql')

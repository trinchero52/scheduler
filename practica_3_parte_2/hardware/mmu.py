from audioop import add

class MMU:

    def __init__(self, memory):
        self.memory = memory
        self._pages = {}
        self._pages_size = 4
        pagesToCreate = int(memory.size / 4)
        for index in range(0, pagesToCreate):
            self._pages[index] = Page(index, self._pages_size)

    def read_raw(self, addr):
        """"Read instruction with addr in memory"""
        self.memory.read(addr)

    def read(self, pid, addr, pageNro):
        """"Read instruction with virtual addr in memory"""
        pages = self.getPagesNumbersOfProcess(pid)
        if(not pageNro in pages):
            raise RuntimeError("This process not includes this page")
        else:
            return self._pages[pageNro]._data[addr]

    def freePages(self, nroPages):
        """Return free pages if the number of requested pages is less"""
        results = []
        for index in range(0, len(self._pages)):
            if(len(self._pages[index]._data) == 0):
                results.append(index)
                if(len(results) == nroPages):
                    return results
        raise RuntimeError("No more pages from this process")

    def asociatePagesFromProcess(self, pid, freePages):
        """Associate free pages with pid"""
        for i in range(0,len(freePages)):
            self._pages[freePages[i]]._process = pid
            if(len(freePages) != i + 1):
                self._pages[freePages[i]]._next_page = freePages[i + 1]

    def loadProcessInPages(self, pid, blocks):
        """Load data of process in pages of process"""
        pages = self.getPagesOfProcess(pid)
        for i in range(0, len(pages)):
            pages[i]._data = blocks[i]

    def loadProcessInMemory(self, pid):
        """Load data of process in memory"""
        pages = self.getPagesOfProcess(pid)
        for i in range(0, len(pages)):
            self.loadInstructionsFromPageInMemory(pages[i])

    def loadInstructionsFromPageInMemory(self, page):
        """Load data of page in memory"""
        for i in range(0, len(page._data)):
            self.memory.write(page._memoryInit + i,page._data[i])

    def unloadProcess(self, pid):
        """Unload process"""
        pages = self.getPagesOfProcess(pid)
        for page in pages:
            self.unloadPage(page)

    def unloadPage(self, page):
        """Unload page data and memory data of page"""
        for i in range(0, len(page._data)):
            self.memory.write(page._memoryInit + i, '')
        page._process = None
        page._data = []
        page._next_page = None

    def getPagesOfProcess(self, pid):
        """Return pages of process"""
        pages = []
        for i in range(0, len(self._pages)):
            if(self._pages[i]._process == pid):
                pages.append(self._pages[i])
        return pages

    def getPagesNumbersOfProcess(self, pid):
        """Return numbers pages of process"""
        pages = []
        for i in range(0, len(self._pages)):
            if(self._pages[i]._process == pid):
                pages.append(self._pages[i]._numberPage)
        return pages

    def next(self, pc):
        """Return next virtual address"""
        currentPage = self._pages[pc[0]]
        if(len(currentPage._data) != pc[1]):
            return (pc[0], pc[1] + 1)
        else:
            return (currentPage._next_page,1)

    def hasProcess(self, pid):
        """Return if this process has load"""
        pages = self.getPagesOfProcess(pid)
        return len(pages) != 0

    @property
    def size(self):
        return self.memory.size

    @property
    def firstAddress(self):
        return 0

    @property
    def pages(self):
        return self._pages

    @property
    def pages_size(self):
        return self._pages_size

    @property
    def pagesRef(self):
        return self._pagesRef

    @property
    def lastAddress(self):
        return self.size - 1

    @property
    def lastAddress(self):
        return self.size - 1

class Page:

    def __init__(self, numberPage, pagSize):
        self._numberPage = numberPage
        self._process = None
        self._memoryInit = numberPage * pagSize
        self._data = []
        self._next_page = None

    @property
    def process(self):
        return self._process

    @property
    def data(self):
        return self._data
    
    @property
    def numberPage(self):
        return self._numberPage

    @property
    def memoryInit(self):
        return self._memoryInit

    @property
    def nextPage(self):
        return self._next_page
    

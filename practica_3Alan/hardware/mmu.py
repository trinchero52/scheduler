class MMU:
    def __init__(self, memory):
        self.memory = memory
        self._pages = {}
        self._pagesRef = {}
        pagesToCreate = int(memory.size / 4)
        for index in range(0, pagesToCreate):
            self._pages[index] = []
        self._firstPageEmpty = 0

    def read(self, addr, nroPage):
        page = self._pages[nroPage]
        return page.index(addr)

    def write(self, addr, value, nroPage, pId):
        print(nroPage)
        page = self._pages[nroPage]
        while((len(page)) >=4):
            nroPage +=1
            page = self._pages[nroPage]
        page.insert(addr, value)
        if(not nroPage in self._pagesRef[pId]):
            self._pagesRef[pId].append(nroPage)
        self.memory.write(addr, value)
    
    def removeFromMemory(self, addr, value):
        self.memory.write(addr, value)

    def removeFromPages(self, pId):
        pageRef = self._pagesRef[pId]
        for index in range(0, len(pageRef)):
            self._pages[pageRef[index]] = []

    @property
    def size(self):
        return self.memory.size

    @property
    def firstAddress(self):
        return 0

    @property
    def lastAddress(self):
        return self.size - 1

    @property
    def pages(self):
        return self._pages

    @property
    def pagesRef(self):
        return self._pagesRef

    def getFirstPageEmpty(self):
        for i in range(0, len(self._pages)):
            if(self.isEmptyPage(self._pages[i])):
                return i

    def isEmptyPage(self, page):
        return page == []

    def addRefPage(self, id):
        self._pagesRef[id] = []

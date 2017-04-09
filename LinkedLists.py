class Node():
    def __init__(self,data,_next):
        self.data = data
        self.next = _next
    def getData(self):
        return self.data
    def getNext(self):
        return self.next
    def setData(self,i):
        self.data = i
    def setNext(self,n):
        self.next = n

class LinkedList():
    def __init__(self):
        self.head = None

    def addFirst(self,i):
        temp = Node(i,None)
        temp.setNext(self.head)
        self.head = temp

    def add(self,i):
        temp = self.head
        if(temp != None):
            while((temp.getNext() != None)):
                temp = temp.getNext()
            temp.setNext(Node(i,None))
        else:
            temp = Node(i,None)
            self.head = temp

    def remove(self, i):
        temp = self.head
        prev = None
        while((temp != None)and(temp.getData() != i)):
            prev = temp
            temp = temp.getNext()
        if(temp != None):
            if(prev == None):
                self.head = temp.getNext()
            else:
                prev.setNext(temp.getNext())
    
    def size(self):
        temp = self.head
        count = 0
        while((temp != None)):
            count += 1
            temp = temp.getNext()
        return count
    
    def belongs(self,i):
        temp = self.head
        while((temp != None)and(temp.getData() != i)):
            temp = temp.getNext()
        return (temp != None)

    def pop(self):
        temp = self.head.getData()
        self.head = self.head.getNext()
        return temp

    def hasNext(self):
        return (self.head != None)

    def __str__(self):
        temp  = self.head
        while((temp != None)):
            print(temp.getData(),end=" ")
            temp = temp.getNext()
        return ''

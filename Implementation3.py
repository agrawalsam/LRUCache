class LRUCache:
    class Node:
        def __init__(self, key:int, value:int):
            self.key = key
            self.value = value 
            self.next = None
            self.prev = None

    def __init__(self, capacity: int):
        self.head = self.Node(-1, -1)
        self.tail = self.Node(-1, -1)
        self.head.next = self.tail 
        self.tail.prev = self.head
        self.lru = {}
        self.length = capacity 
    
    def insert_back(self, key:int, value:int):
        nn = self.Node(key, value)
        temp = self.tail.prev
        temp.next = nn 
        nn.prev = temp 
        nn.next = self.tail 
        self.tail.prev = nn
        return nn

    def move_back(self, t: "LRUCache.Node"):
        # get the nodes around t 
        m1 = t.prev 
        m2 = t.next 
        
        # change the connections. 
        m1.next = m2 
        m2.prev = m1 

        # get the nodes around tail. 
        n1 = self.tail.prev 

        # move the connections of t to tail 
        t.next = self.tail 
        t.prev = n1

        # move the connections of nodes around tail to t 
        n1.next = t 
        self.tail.prev = t


    def get(self, key: int) -> int:
        # element not present in the map. 
        if key not in self.lru:
            return -1
        # element is present in the map
        else:
            # CACHE-HIT
            # find the node 
            t = self.lru[key]
            # since the node is accessed once.
            # move the node to the last of the doubly linked list 
            self.move_back(t)
            return self.lru[key].value

    def put(self, key: int, value: int) -> None:
        # check if length>0
        if self.length>0:
            # CACHE is there but update it. 
            if key in self.lru:
                # move the node to the last of the doubly linked list 
                t = self.lru[key]
                t.value = value 
                self.move_back(t)
            # Cache is not present. Make a new entry. 
            else:
                # decrease the current length of the linked list
                self.length-=1
                # insert at the back of the linked list
                # make a new entry in the hashmap. 
                self.lru[key]=self.insert_back(key, value)
        else:
        # if length==0 then
            # if key already present 
            if key in self.lru:
                # node is already present just need to update the value. 
                t = self.lru[key]
                t.value = value 
                self.move_back(t)
            # key is not present, delete at the start of the linked list and insert at the back. 
            else: 
                # delete from the head node 
                t = self.head.next 
                self.head.next = t.next 
                t.next.prev = self.head 
                t.next = None 
                t.prev = None 
                # delete the entry from the hashmap
                del self.lru[t.key]
                # insert at the back 
                nn = self.insert_back(key, value)
                self.lru[key]=nn            

# Your LRUCache object will be instantiated and called as such:
# obj = LRUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)
#FIFO Queue
#
# CS3021 LL Project
#
# winter 2019
# last updated: 04 Jan 2019
#

from util import LinkedList

class FIFO(object):
    ''' Class for a first-in, first out (FIFO) queue. Wraps around LinkedList() object
        Provides ability to add and remove elements from a FIFO queue and to determine if queue is empty.'''

    def __init__(self):
        '''Instantiates an internal linked list which is used to internally perform all the necessary functions of a FIFO queue

           Attributes:  LinkedList.LinkedList()'''

        self.llist = LinkedList.LinkedList()

    def add(self, dataItem):
        '''Adds an item to the FIFO queue by internally calling LinkedList.insertAtIndex().
           Index is fixed to the head of the queue.

            Parameters: Item
            Returns:    N/A'''

        self.llist.insertAtIndex(index=0, dataItem=dataItem)

    def remove(self):
        ''' Removes the next item in the FIFO queue by walking the internal linked list.
            Determines end of the linked list and then removes and returns that element.

            Parameters: N/A
            Returns:    Next item in FIFO queue'''

        # If the queue is empty, return None type.
        if self.llist.head:
            # Walk linked list to end
            current = self.llist.head
            i = 0
            while current.nextNode:
                current = current.nextNode
                i += 1
            # Once the end of the queue is reached, remove and return node value.
            answer = self.llist.read(i)
            self.llist.deleteAtIndex(i)
            return answer

        else:
            return None

        

    def empty(self):
        '''Determines whether a FIFO queue is empty by internally calling LinkedList.empty()

        Parameters: N/A
        Returns:    True/False'''

        return self.llist.empty()

    
    def __str__(self):
        '''Use __str__() method in LinkedList() to display FIFO queue. '''
        return self.llist.__str__()


##########################################################
#testing-related
def test():
    fifo = FIFO()
    print(fifo)
    fifo.add(0)
    fifo.add(5)
    fifo.add(10)
    print(fifo)
    print(fifo.empty())
    fifo.add(-1)
    fifo.add('ab')
    print(fifo)
    print(fifo.remove())
    print(fifo)

    for i in range(10):
        print(fifo.remove())
    print(fifo)
    print(fifo.empty())

if __name__ == '__main__':
    test()


#Stack
#
# CS3021 LL Project
#
# winter 2019
# last updated: 04 Jan 2019

from util import LinkedList

class Stack(object):
    ''' Implement, you will need to call appropriate LinkedList functionality.
        Stack has-a Linked List.
        Generate appropriate docstrings.
        Do not write code to duplicate any LL behaviors in this file
        Do not change LinkedList. '''


    def __init__(self):
        '''Instantiates an internal linked list which is used to internally perform all the necessary functions of a stack.

           Attributes:  LinkedList.LinkedList()
       '''

        self.llist = LinkedList.LinkedList()


    def push(self, dataItem):
        '''Pushes an element to the top of the stack.

            Parameters: dataItem
            Returns:    N/A
        '''
        self.llist.insertAtIndex(index=0, dataItem=dataItem)


    def pop(self):
        '''Removes and returns an element from the top of the stack.

            Parameters: N/A
            Returns:    dataItem
        '''
        if self.llist.head:
            answer = self.llist.read(0)
            self.llist.deleteAtIndex(index=0)
            return answer
        else:
            return None

    def empty(self):
        '''Determines whether a stack is empty by internally calling LinkedList.empty()

        Parameters: N/A
        Returns:    True/False'''

        return self.llist.empty()


    def __str__(self):
        '''Uses __str__() method in LinkedList() to display stack'''
        return self.llist.__str__()

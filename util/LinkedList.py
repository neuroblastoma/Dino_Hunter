#!/usr/bin/env python3
#
# Linked-List
#
# CS3021 LL Project
#
# winter 2019
# last updated: 14 Jan 2020
#
#   LinkedList starting point for in-class build
#

from pathlib import Path
import sys


class LinkedList(object):
    '''Linked-List Class

    This Linked-List will hold any item as the data, but it may not be the
    value None.

    This is a proper Class docstring per PEP 257.  Here is a nice explanation:
    https://gist.github.com/dolph/39d8f70cab6afbac8c01

    '''

    class Node(object):
        '''Node Class

        This is an internally defined class, indicating it is not a thing to be
        used willy-nilly elsewhere in the code.

        '''

        def __init__(self, dataIn):
            ''' Constructor. -dataIn may not be None'''

            if dataIn == None:
                raise RuntimeError('data item to put in Node is None')

            self.data = dataIn
            self.nextNode = None

        @property
        def nextNode(self):
            ''' Accessor. '''
            return self.__nextNode

        @nextNode.setter
        def nextNode(self, nextIn):
            '''Sets the next node. Allows None indicating the end of the List,
            but no other non-Node assignment '''

            if nextIn and not isinstance(nextIn, self.__class__):
                raise RuntimeError(str(nextIn) + ' is not  a linked-list Node')

            self.__nextNode = nextIn

        # end of inner-class Node
        ####################################

    def __init__(self):
        ''' Constructor. Allocates an empty Linked-List shell. '''

        self.head = None

    def read(self, index):
        ''' Returns data at the provided index, or None if index beyond the end. '''

        answer = None

        if self.head:

            current = self.head
            i = 0
            while i < index and current.nextNode:
                i += 1
                current = current.nextNode

            if i == index:
                answer = current.data

        # else:
        #    pass   #nothing to do in this case

        return answer

    def indexOf(self, value):
        '''Returns index of first matching value, or None if value not found.'''

        answer = None

        if self.head:

            current = self.head
            i = 0
            while not value == current.data and current.nextNode:
                i += 1
                current = current.nextNode

            if value == current.data:
                answer = i

        return answer

    def append(self, dataItem):
        '''Appends new data Node to the end of the list. '''

        newNode = self.Node(dataItem)

        if self.head:

            current = self.head
            while current.nextNode:
                current = current.nextNode

            # add the node
            current.nextNode = newNode

        else:
            self.head = newNode

    def insertAtIndex(self, index, dataItem):
        '''Inserts new Node at index, appends to end if index beyond end. '''

        newNode = self.Node(dataItem)

        if self.head:  # list exists
            ##stuff yet                     #insert at beginning
            if index == 0:
                newNode.nextNode = self.head
                self.head = newNode

            else:

                current = self.head
                i = 0
                while i < index - 1 and current.nextNode:
                    i += 1
                    current = current.nextNode

                if i == index - 1:  # insert in middle
                    newNode.nextNode = current.nextNode
                    current.nextNode = newNode

                else:  # insert at end
                    current.nextNode = newNode


        else:  # list was empty
            self.head = newNode

    def deleteAtIndex(self, index):
        '''Deletes Node at index, silent completion, no error generated if
        index beyond end of list. '''

        if self.head:  # list exists
            ##stuff yet                     #delete at beginning
            if index == 0:
                self.head = self.head.nextNode

            else:
                current = self.head
                i = 0
                while i < index - 1 and current.nextNode:
                    i += 1
                    current = current.nextNode

                if i == index - 1 and current.nextNode:  # delete in middle

                    # theNodeToDelete = current.nextNode
                    # current.nextNode = theNodeToDelete.nextNode
                    current.nextNode = current.nextNode.nextNode


                elif i == index - 1:  # delete at end
                    current.nextNode = None

        # else:                           #list was empty
        #    pass  #nothing to do        

    def empty(self):
        '''Returns True if the List is empty, False otherwise.'''

        if self.head:
            return False
        else:
            return True

    def __str__(self):

        if self.head == None:
            return ''

        current = self.head
        result = str(current.data)

        while current.nextNode:
            current = current.nextNode
            result += ', ' + str(current.data)

        return result

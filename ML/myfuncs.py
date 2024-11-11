def printMe(msg='No message was supplied'):
    """This function prints a msg supplied by the caller
        In case no message is supplied from the caller,it prints "No msg was supplied" """
    print(msg)

def printList(L=[]):
    """This function prints the list elements
        The input is a list and default is an empty list"""
    for x in L:
        print(x)
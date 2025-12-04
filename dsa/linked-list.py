from ast import List


class ListNode:
    def __init__(self, val=0, next=None):    
        self.val = val
        self.next = next

# Deletion method

def delete_node(head, target):
    # Base case: Check if head of LL is the target
    if head.val == target:
        return head.next
    
    # Iterate through each node in LL to find the target
    prev, curr = None, head

    while curr:
        if curr.val == target:
            prev.next = curr.next
            break
        prev = curr
        curr = curr.next
    
    return head

# Traversing LL (E.g. To find length of LL)

def find_length(head):
    res = 0
    curr = head
    while curr:
        res += 1
        curr = curr.next
    return res

# Fast and slow pointer method (Time complexity - O(n), Space complexity - O(1))

def fast_and_slow(head):
    slow, fast = head, head
    while fast and fast.next:
        fast = fast.next.next
        slow = slow.next
    return slow

# Reverse LL (Time complexity - O(n), Space Complexity - O(1))
def reverse(head):
    prev, curr = None, head
    while curr:
        # Temp variable
        temp = curr.next
        curr.next = prev
        prev = curr
        curr = temp
    return prev

# Merge two linked lists together in sorted order (Time complexity - O(n + m), Space Complexity - O(1))

def merge(list1, list2):
    dummy = ListNode()
    curr = dummy

    while list1 and list2:
        # Case 1: Curr val of list 1 node is smaller or equal to list 2 
        if list1.val <= list2.val:
            curr.next = list1
            list1 = list1.next
        # Case 2: Curr val of list 2 node is smaller or equal to list 1 
        else:
            curr.next = list2
            list2 = list2.next

        curr = curr.next
    
    curr.next = list1 or list2
    return dummy.next
        

    pass

"""
1 -> 2 -> 3 -> 4

1 -> 3 -> 4

Delete Node 2:
prev: 1 
curr: 2

Length of LL:
res : 4
curr: None
"""
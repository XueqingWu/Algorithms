"""
Math 560
Project 1
Fall 2021

Partner 1: Xueqing Wu
Partner 2:
Date: 03/21/2025
"""


def SelectionSort(listToSort):
    """
    SelectionSort
    input: listToSort - a list of numbers to be sorted
    output: listToSort - a sorted list of numbers
    """
    sep_index = 0  # index of the first unsorted element
    length = len(listToSort)  # length of the list
    # Loop through the list until the last element
    while sep_index < length - 1:
        # Find the smallest element in the unsorted portion of the list
        min_index = sep_index
        for i in range(sep_index + 1, length):
            if listToSort[i] < listToSort[min_index]:
                min_index = i

        # Swap the smallest element with the first unsorted element
        listToSort[sep_index], listToSort[min_index] = (
            listToSort[min_index],
            listToSort[sep_index],
        )

        # Move to the next unsorted element
        sep_index += 1
    # sorted arrary

    return listToSort


def InsertionSort(listToSort):
    """
    InsertionSort
    """
    # Loop through the list starting from the second element
    for i in range(1, len(listToSort)):
        # Store the current element
        current = listToSort[i]
        # Initialize the index of the previous element
        j = i - 1
        # Move elements that are greater than the current element to the right
        while j >= 0 and listToSort[j] > current:
            listToSort[j + 1] = listToSort[j]
            j -= 1
        # Insert the current element into its correct position
        listToSort[j + 1] = current
    return listToSort


def BubbleSort(listToSort):
    """
    BubbleSort
        Iterate through the array.
        Compare every two adjacent elements.
        If they are out of order, swap them.
        Repeat until no more swaps are made.
    """
    # Loop through the list
    for i in range(len(listToSort)):
        # Loop through the list from the end to the beginning
        for j in range(len(listToSort) - 1, i, -1):
            # Swap adjacent elements if they are in the wrong order
            if listToSort[j] < listToSort[j - 1]:
                listToSort[j], listToSort[j - 1] = (
                    listToSort[j - 1],
                    listToSort[j],
                )
    return listToSort


def MergeSort(listToSort):
    """
    MergeSort
    Base Cases: If the array has 1 element, it is sorted. If the
    array has 2 elements, swap if needed and return.
        Split the array into two halves.
        Recursively sort each half.
        Merge the already sorted halves.
        Iterate through them simultaneously.
        Compare their smallest elements.
        The smaller of the two gets removed and inserted into the
    merged array.
    """
    # Base case: if the list has 1 elements, it is already sorted
    if len(listToSort) == 1:
        return listToSort
    if len(listToSort) > 1:
        # Finding the mid of the array
        mid = len(listToSort) // 2

        # Dividing the elements into 2 halves
        L = listToSort[:mid]
        R = listToSort[mid:]

        # Sorting the first half
        MergeSort(L)

        # Sorting the second half
        MergeSort(R)

        # Merging the two halves
        left_index = right_index = i = 0  # i is the index for the main list

        # Copy data to temp arrays L[] and R[]
        while left_index < len(L) and right_index < len(R):
            if L[left_index] < R[right_index]:
                listToSort[i] = L[left_index]
                left_index += 1
            else:
                listToSort[i] = R[right_index]
                right_index += 1
            i += 1

        # Checking if any element was left
        while left_index < len(L):
            listToSort[i] = L[left_index]
            left_index += 1
            i += 1

        while right_index < len(R):
            listToSort[i] = R[right_index]
            right_index += 1
            i += 1

    return listToSort


def QuickSort(listToSort, i=0, j=None):
    """
    QuickSort

    Sort a list with the call QuickSort(listToSort),
    or additionally specify i and j.
    """
    if j == None:
        j = len(listToSort)
    # Base case: if the partition has 1 or fewer elements, it's already sorted
    if i >= j - 1:
        return listToSort

    # Choose the rightmost element as the pivot
    pivot = listToSort[j - 1]

    # Partition the array
    partition_index = i
    for k in range(i, j - 1):
        if listToSort[k] <= pivot:
            # Swap elements
            listToSort[partition_index], listToSort[k] = (
                listToSort[k],
                listToSort[partition_index],
            )
            partition_index += 1

    # Place the pivot in its correct position
    listToSort[partition_index], listToSort[j - 1] = (
        listToSort[j - 1],
        listToSort[partition_index],
    )

    # Recursively sort the left and right partitions
    QuickSort(listToSort, i, partition_index)
    QuickSort(listToSort, partition_index + 1, j)

    return listToSort


"""
Importing the testing code after function defs to ensure same references.
"""
from project1tests import *


if __name__ == "__main__":
    """
    Main function.
    """
    print("Testing Selection Sort")
    print()
    testingSuite(SelectionSort)
    print()
    print("Testing Insertion Sort")
    print()
    testingSuite(InsertionSort)
    print()
    print("Testing Bubble Sort")
    print()
    testingSuite(BubbleSort)
    print()
    print("Testing Merge Sort")
    print()
    testingSuite(MergeSort)
    print()
    print("Testing Quick Sort")
    print()
    testingSuite(QuickSort)
    print()
    print("UNSORTED measureTime")
    print()
    measureTime()
    print()
    print("SORTED measureTime")
    print()
    measureTime(True)

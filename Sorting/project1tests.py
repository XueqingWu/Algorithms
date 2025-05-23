"""
Math 560
Project 1
Fall 2021
Provided Testing Code
"""

# Import time, random, plotting, stats, and numpy.
import time
import random
import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy

# Import the provided code.
from project1 import SelectionSort
from project1 import InsertionSort
from project1 import BubbleSort
from project1 import MergeSort
from project1 import QuickSort


def isSorted(unsortedList, sortedList):
    """
    isSorted

    This function will take in an original unsorted list and a sorted version of
    that same list, and return whether the list has been properly sorted.

    Note that this function does not change the unsorted list.

    INPUTS
    unsortedList: the original unsorted list
    sortedList:  the supposedly sorted list

    OUTPUTS
    returns true or false
    """
    # Copy the unsorted list.
    temp = unsortedList.copy()
    
    # Use python's sort.
    temp.sort()

    # Check equality.
    return temp == sortedList


def testingSuite(alg):
    """
    testingSuite

    This function will run a number of tests using the input algorithm, check if
    the sorting was successful, and print which tests failed (if any).

    This is not an exhaustive list of tests by any means, but covers the edge
    cases for your sorting algorithms.

    INPUTS
    alg: function pointer for alg to test, the options are:
        SelectionSort
        InsertionSort
        BubbleSort
        MergeSort
        QuickSort

    OUTPUTS
    Printed statements indicating which tests passed/failed.
    """
    # First, we seed the random number generator to ensure reproducibility.
    random.seed(1)

    # List of possible algs.
    algs = ['SelectionSort', 'InsertionSort', \
            'BubbleSort', 'MergeSort', 'QuickSort']

    # Make sure the input is a proper alg to consider.
    if not alg.__name__ in algs:
        raise Exception( \
                'Not an allowed algorithm. Value was: {}'.format(alg.__name__))
    
    # Create a list to store all the tests.
    tests = []

    # Create a list to store the test names.
    message = []

    # Test 1: singleton array
    tests.append([1])
    message.append('singleton array')

    # Test 2: repeated elements
    tests.append([1,2,3,4,5,5,4,3,2,1])
    message.append('repeated elements')

    # Test 3: all repeated elements
    tests.append([2,2,2,2,2,2,2,2,2,2])
    message.append('all repeated elements')

    # Test 4: descending order
    tests.append([10,9,8,7,6,5,4,3,2,1])
    message.append('descending order')

    # Test 5: sorted input
    tests.append([1,2,3,4,5,6,7,8,9,10])
    message.append('sorted input')

    # Test 6: negative inputs
    tests.append([-1,-2,-3,-4,-5,-5,-4,-3,-2,-1])
    message.append('negative inputs')

    # Test 7: mixed positive/negative
    tests.append([1,2,3,4,5,-1,-2,-3,-4,-5,0])
    message.append('mixed positive/negative')

    # Test 8: array of size 2^k - 1
    temp = list(range(0,2**6-1))
    random.shuffle(temp)
    tests.append(temp)
    message.append('array of size 2^k - 1')

    # Test 9: random real numbers
    tests.append([random.random() for x in range(0,2**6-1)])
    message.append('random real numbers')

    # Store total number of passed tests.
    passed = 0

    # Loop over the tests.
    for tInd in range(0,len(tests)):
        # Copy the test for sorting.
        temp = tests[tInd].copy()

        # Try to sort, but allow for errors.
        try:
            # Do the sort.
            alg(tests[tInd])
            
            # Check if the test succeeded.
            if isSorted(temp, tests[tInd]):
                print('Test %d Success: %s' % (tInd+1, message[tInd]))
                passed += 1
            else:
                print('Test %d FAILED: %s' % (tInd+1, message[tInd]))

        # Catch any errors.
        except Exception as e:
            print()
            print('DANGER!')
            print('Test %d threw an error: %s' % (tInd+1, message[tInd]))
            print('Error: ')
            print(e)
            print()

    # Done testing, print and return.
    print()
    print('%d/9 Tests Passed' % passed)
    return


def measureTime(preSorted = False, numTrials = 30):
    """
    measureTime

    This function will generate lists of varying lengths and sort them using your
    implemented fuctions. It will time these sorting operations, and store the
    average time across 30 trials of a particular size n. It will then create plots
    of runtime vs n. It will also output the slope of the log-log plots generated
    for several of the sorting algorithms.

    INPUTS
    preSorted: set to True to test with only pre-sorted inputs
        (default = False)
    numTrials: the number of trials to average timing data across
        (default = 30)

    OUTPUTS
    A number of genereated runtime vs n plot, a log-log plot for several
    algorithms, and printed statistics about the slope of the log-log plots.
    """
    # Print whether we are using sorted inputs.
    if preSorted:
        print('Timing algorithms using only sorted data.')
    else:
        print('Timing algorithms using random data.')
        print('Averaging over %d Trials' % numTrials)
    print()
    
    # First, we seed the random number generator to ensure consistency.
    random.seed(1)

    # Define a scaling constant for n for insertion and bubble sort.
    scaleN = 1
    ISind = 1
    BBind = 2
    TIMind = 5

    # We now define the range of n values to consider.
    if preSorted:
        # Need to look at larger n to get a good sense of runtime.
        # Look at n from 20 to 980.
        # Note that 1000 causes issues with recursion depth for merge and quick.
        N = list(range(1,50))
        N = [20*x for x in N]
        scaleN = 10 # Make insertion and bubble do larger tests.
    else:
        # Look at n from 10 to 500.
        N = list(range(1,51))
        N = [10*x for x in N]

    # Store the different algs to consider.
    algs = [SelectionSort, InsertionSort, \
            BubbleSort, MergeSort, \
            QuickSort, list.sort]

    # Preallocate space to store the runtimes.
    tSelectionSort = N.copy()
    tInsertionSort = N.copy()
    tBubbleSort = N.copy()
    tMergeSort = N.copy()
    tQuickSort = N.copy()
    tPython = N.copy()

    # Create some flags for whether each sorting alg works.
    isCorrect = [True, True, True, True, True, True]

    # Loop over the different sizes.
    for nInd in range(0,len(N)):
        # Get the current value of n to consider.
        n = N[nInd]
        
        # Reset the running sum of the runtimes.
        timing = [0,0,0,0,0,0]
        
        # Loop over the tests.
        for test in range(1,numTrials+1):

            # Loop over the algs.
            for aI in range(0,len(algs)):
                # If preSorted and insertion or bubble or tim, make the 
                # testing list longer to get better tests...
                if preSorted and (aI == ISind or aI == BBind or aI == TIMind):
                    listToSort = list(range(0,n*scaleN))
                else:
                    listToSort = list(range(0,n))

                    if not preSorted:
                        listToSort = [random.random() for x in listToSort]

                # Grab the name of the alg.
                alg = algs[aI]

                # Copy the original list for sorting.
                copiedList = listToSort.copy()
                
                # Time the sort.
                t = time.time()
                if aI != 4 :
                    alg(copiedList)
                else:
                    alg(copiedList,0,len(copiedList))
                t = time.time() - t

                # Ensure that your function sorted the list.
                if not isSorted(listToSort,copiedList):
                    isCorrect[aI] = False

                # Add the time to our running sum.
                timing[aI] += t

        # Now that we have completed the numTrials tests, average the times.
        timing = [x/numTrials for x in timing]

        # Store the times for this value of n.
        tSelectionSort[nInd] = timing[0]
        tInsertionSort[nInd] = timing[1]
        tBubbleSort[nInd] = timing[2]
        tMergeSort[nInd] = timing[3]
        tQuickSort[nInd] = timing[4]
        tPython[nInd] = timing[5]

    # If there was an error in one of the plotting algs, report it.
    for aI in range(0,len(algs)-1):
        if not isCorrect[aI]:
            print('%s not implemented properly!!!' % algs[aI].__name__)
            
    # Now plot the timing data.
    for aI in range(0,len(algs)):
        # Get the alg.
        alg = algs[aI].__name__ if aI != 5 else 'Python'

        # Plot.
        scaleNP = scaleN if (aI == ISind or aI == BBind or aI == TIMind) else 1
        plt.figure()
        plt.plot([scaleNP*nn for nn in N],locals()['t%s' % alg])
        plt.title('%s runtime versus n' % alg)
        plt.xlabel('Input Size n')
        plt.ylabel('Runtime (s)')
        if preSorted:
            plt.savefig('%s_sorted.png' % alg, bbox_inches='tight')
        else:
            plt.savefig('%s.png' % alg, bbox_inches='tight')

    # Plot them all together.
    plt.figure()
    fig, ax = plt.subplots()
    ax.plot(N,tSelectionSort, label='Selection')
    ax.plot([scaleN*nn for nn in N],tInsertionSort, label='Insertion')
    ax.plot([scaleN*nn for nn in N],tBubbleSort, label='Bubble')
    ax.plot(N,tMergeSort, label='Merge')
    ax.plot(N,tQuickSort, label='Quick')
    ax.plot([scaleN*nn for nn in N],tPython, label='Python')
    if preSorted:
        legend = ax.legend(loc='upper right')
    else:
        legend = ax.legend(loc='upper left')
    plt.title('All sorting runtimes versus n')
    plt.xlabel('Input Size n')
    plt.ylabel('Runtime (s)')
    if preSorted:
        plt.savefig('sorting_sorted.png', bbox_inches='tight')
    else:
        plt.savefig('sorting.png', bbox_inches='tight')

    # Now look at the log of the sort times.
    logN = [(numpy.log(x) if x>0 else -16) for x in N]
    scaleLogN = [(numpy.log(x) if x>0 else -16) \
                 for x in [scaleN*nn for nn in N]]
    logSS = [(numpy.log(x) if x>0 else -16) for x in tSelectionSort]
    logIS = [(numpy.log(x) if x>0 else -16) for x in tInsertionSort]
    logBS = [(numpy.log(x) if x>0 else -16) for x in tBubbleSort]
    logMS = [(numpy.log(x) if x>0 else -16) for x in tMergeSort]
    logQS = [(numpy.log(x) if x>0 else -16) for x in tQuickSort]

    # Linear regression.
    mSS, _, _, _, _ = stats.linregress(logN,logSS)
    mIS, _, _, _, _ = stats.linregress(scaleLogN,logIS)
    mBS, _, _, _, _ = stats.linregress(scaleLogN,logBS)

    # Plot log-log figure.
    plt.figure()
    fig, ax = plt.subplots()
    ax.plot(logN,logSS, label='Selection')
    ax.plot(scaleLogN,logIS, label='Insertion')
    ax.plot(scaleLogN,logBS, label='Bubble')
    legend = ax.legend(loc='upper left')
    plt.title('Log-Log plot of runtimes versus n')
    plt.xlabel('log(n)')
    plt.ylabel('log(runtime)')
    if preSorted:
        plt.savefig('log_sorted.png', bbox_inches='tight')
    else:
        plt.savefig('log.png', bbox_inches='tight')

    # Print the regression info.
    print()
    print('Selection Sort log-log Slope (all n): %f' % mSS)
    print('Insertion Sort log-log Slope (all n): %f' % mIS)
    print('Bubble Sort log-log Slope (all n): %f' % mBS)
    print()

    # Now strip off all n<200 (or 400 for preSorted)...
    cutoff = 400 if preSorted else 200
    indCut = (cutoff//20)-1 if preSorted else (cutoff//10)-1
    logN = logN[indCut:]
    scaleLogN = scaleLogN[indCut:]
    logSS = logSS[indCut:]
    logIS = logIS[indCut:]
    logBS = logBS[indCut:]
    logMS = logMS[indCut:]
    logQS = logQS[indCut:]

    # Linear regression.
    mSS, _, _, _, _ = stats.linregress(logN,logSS)
    mIS, _, _, _, _ = stats.linregress(scaleLogN,logIS)
    mBS, _, _, _, _ = stats.linregress(scaleLogN,logBS)
    mMS, _, _, _, _ = stats.linregress(logN,logMS)
    mQS, _, _, _, _ = stats.linregress(logN,logQS)

    # Print the regression info.
    print('Selection Sort log-log Slope (n>%d): %f' \
          % (cutoff, mSS))
    print('Insertion Sort log-log Slope (n>%d): %f' \
          % (cutoff, mIS))
    print('Bubble Sort log-log Slope (n>%d): %f' \
          % (cutoff, mBS))
    print('Merge Sort log-log Slope (n>%d): %f' \
          % (cutoff, mMS))
    print('Quick Sort log-log Slope (n>%d): %f' \
          % (cutoff, mQS))

    # Close all figures.
    plt.close('all')

import pdb
import numpy as np


cost_deletion = 3
cost_insertion = 2
cost_substitution = 1


def costDeletion(el1):
    """
    This gives us the cost of deletion of an element
    """
    return 1

        

def costInsertion(el1):
    """
    This gives us the cost of deletion of an element
    """
    #return (5 - el1) * 2
    return 2

    
def costSubstitution(el1,el2):
    """
    This gives us the cost of substitution of an element
    """
    return 3
    
    if el1<el2:
        return 1
    else:
        return (el1 - el2)*2




def OptimalMatching(s1, s2):
    assert isinstance(cost_deletion, int)
    assert isinstance(cost_insertion, int)
    assert isinstance(cost_substitution, int)
    lenstr1 = len(s1)
    lenstr2 = len(s2)
    cost = np.zeros((lenstr1 + 1, lenstr2 + 1), dtype=int)
    
    # initialization : comparaison with a null sequence
    #min_cost = min(cost_deletion, cost_insertion)
    for i in range(lenstr1):
        cost[i+1, 0] = cost[i, 0] + costDeletion(s1[i])
    for j in range(lenstr2):
        cost[0, j+1] = cost[0, j] + costInsertion(s2[j])

    for el1 in range(lenstr1):
        for el2 in range(lenstr2):
            if s1[el1] == s2[el2]:
                cost[el1 + 1, el2 + 1] = cost[el1, el2] # cost = 0 because they are the same
            else:
                if j==i:
                    cost[el1 + 1, el2 + 1] = min(
                                               cost[el1, el2 + 1], # insertion
                                               cost[el1 + 1, el2], #deletion
                                               cost[el1, el2]  # substitution
                                              ) + costSubstitution(s1[el1], s2[el2])
                elif j>i:
                    cost[el1 + 1, el2 + 1] = min(
                                               cost[el1, el2 + 1], # insertion
                                               cost[el1 + 1, el2], #deletion
                                               cost[el1, el2]  # substitution
                                              ) + costInsertion(s2[el2])
                else:
                    cost[el1 + 1, el2 + 1] = min(
                                               cost[el1, el2 + 1], # insertion
                                               cost[el1 + 1, el2], #deletion
                                               cost[el1, el2]  # substitution
                                              ) + costDeletion(s1[el1])
    return cost[lenstr1, lenstr2]

def levenshtein2(source, target):
    if len(source) < len(target):
        return levenshtein(target, source)
 
    # So now we have len(source) >= len(target).
    if len(target) == 0:
        return len(source)
 
    # We call tuple() to force strings to be used as sequences
    # ('c', 'a', 't', 's') - numpy uses them as values by default.
    source = np.array(tuple(source))
    target = np.array(tuple(target))
 
    # We use a dynamic programming algorithm, but with the
    # added optimization that we only need the last two rows
    # of the matrix.
    previous_row = np.arange(target.size + 1)
    for s in source:
        # Insertion (target grows longer than source):
        current_row = previous_row + cost_insertion
 
        # Substitution or matching:
        # Target and source items are aligned, and either
        # are different (cost of 1), or are the same (cost of 0).
        current_row[1:] = np.minimum(
                current_row[1:],
                np.add(previous_row[:-1], target != s) + cost_substitution
                )
 
        # Deletion (target grows shorter than source):
        current_row[1:] = np.minimum(
                current_row[1:],
                current_row[0:-1] + cost_deletion)
 
        previous_row = current_row
 
    return previous_row[-1]


def levenshtein(a,b):
    "Calculates the Levenshtein distance between a and b."
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n,m)) space
        a, b = b, a
        n, m = m, n
        
    current = range(n + 1)
    for i in range(1, m + 1):
        previous = current
        current = [i] + [0]*n
        for j in range(1, n + 1):
            add = previous[j] + cost_insertion
            delete = current[j - 1] + cost_deletion
            change = previous[j - 1]
            if a[j - 1] != b[i - 1]:
                change = change + cost_substitution
            current[j] = min(add, delete, change)
            
    return current[n]
    


seq1 = [5, 2, 3, 2, 5, 1, 3, 3, 3, 1, 3, 3]
seq2 = [2, 5, 4, 2, 4, 5, 1, 5, 1, 3, 4, 2]

print (OptimalMatching(seq1, seq2))






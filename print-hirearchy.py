import collections

def print_hirearchy(lst):
    animalToIndeg = collections.defaultdict(int)
    animalToNeigh = collections.defaultdict(list)

    # Initialise hashmap
    for edge in lst:
        x, y = edge[0], edge[1]
        if x not in animalToIndeg:
            animalToIndeg[x] = 0
        animalToIndeg[y] += 1
        animalToNeigh[x].append(y)
    
    # Find animal with 0 indeg to start DFS
    initialAnimal = None
    for animal, indeg in animalToIndeg.items():
        if indeg == 0:
            initialAnimal = animal
            break
    
    def dfs(animal, level):
        # Process output
        print("\t" * level + animal)

        for neigh in animalToNeigh[animal]:
            dfs(neigh, level + 1)


    return dfs(initialAnimal, 0)

# Test case based on the example
lst = [
    ("dog", "poodle"),
    ("mammal", "dog"),
    ("mammal", "cat"),
    ("dog", "bulldog"),
    ("dog", "terrier")
]

if __name__ == "__main__":
    print_hirearchy(lst)


"""
Input:
dog, poodle
mammal, dog
mammal, cat
dog, bulldog
dog, terrier
Output:
mammal
	dog
		poodle
		bulldog
		terrier
	cat

Assumption: List of tuples with edges (x, y) from x -> y

# Key: animal, val: indeg
{mammal: 0, cat: 1, dog: 1, poodle: 1, bulldog: 1, terrier: 1}

# Key: animal, val: neigh
{mammal: [cat, dog], dog: [poodle, bulldog, terrier], }

1. Find animal with 0 indeg
2. Perform DFS and print accordingly 


"""
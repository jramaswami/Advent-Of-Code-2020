"""
Advent of Code 2020 :: Day 7: Handy Haversacks
"""
import sys
from collections import defaultdict, deque
import pyperclip


def parse_line(line):
    """
    Parse the line.  Return a tuple where the first item is the container
    and the second item is a list of containees.
    """
    left, right = line.split(' contain ')
    container = left[:-5]
    if right == 'no other bags.':
        return container, []

    containees = []
    right_tokens = right.split(', ')
    for right_token in right_tokens:
        space_index = right_token.find(' ')
        wt = int(right_token[:space_index])
        bags_index = right_token.find(' bag')
        containees.append((right_token[space_index + 1:bags_index], wt))

    return container, containees


def bfs(root, out_adj):
    """BFS to count the number of bags that can contain a shiny gold bag."""
    root = 'shiny gold'
    queue = deque([root])
    visited = set([root])
    while queue:
        containee = queue.popleft()
        for container in out_adj[containee]:
            if container not in visited:
                visited.add(container)
                queue.append(container)
    return len(visited) - 1


def dfs(node, in_adj):
    """DFS to count the number of bags contained by a shiny gold bag."""
    bags_contained = 1
    for neighbor, wt in in_adj[node]:
        child_bags = dfs(neighbor, in_adj)
        bags_contained += wt * child_bags
    return bags_contained


def main():
    """Main program"""
    # Create a directed graph from containee to container: out_adj
    # Create a directed graph from container to containee: in_adj
    out_adj = defaultdict(list)
    in_adj = defaultdict(list)
    for line in sys.stdin:
        container, containees = parse_line(line.strip())
        for containee, wt in containees:
            out_adj[containee].append(container)
            in_adj[container].append((containee, wt))

    soln1 = bfs('shiny gold', out_adj)
    print('The solution to part 1 is', soln1)
    assert soln1 == 268

    soln2 = dfs('shiny gold', in_adj) - 1    # Don't count the shiny gold bag.
    print('The solution to part 2 is', soln2)
    assert soln2 == 7867
    pyperclip.copy(soln2)


if __name__ == '__main__':
    main()

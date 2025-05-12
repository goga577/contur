import sys
import collections
import heapq
import os

keys_char = [chr(i) for i in range(ord('a'), ord('z') + 1)]
doors_char = [k.upper() for k in keys_char]

def get_input():
    try:
        return [list(line.strip()) for line in sys.stdin if line.strip()]
    except OSError:
        return []


def solve(grid):
    n, m = len(grid), len(grid[0])
    starts = []
    key_positions = {}
    for i in range(n):
        for j in range(m):
            c = grid[i][j]
            if c == '@':
                starts.append((i, j))
            elif 'a' <= c <= 'z':
                key_positions[c] = (i, j)
    K = len(key_positions)
    key_list = sorted(key_positions.keys())
    key_index = {k: idx for idx, k in enumerate(key_list)}
    total_keys_mask = (1 << K) - 1

    def bfs_from(x, y):
        visited = [[False] * m for _ in range(n)]
        dq = collections.deque()
        dq.append((x, y, 0, 0))
        visited[x][y] = True
        found = {}
        while dq:
            i, j, dist, doors = dq.popleft()
            for di, dj in ((1,0),(-1,0),(0,1),(0,-1)):
                ni, nj = i+di, j+dj
                if not (0 <= ni < n and 0 <= nj < m):
                    continue
                if visited[ni][nj]:
                    continue
                cell = grid[ni][nj]
                if cell == '#':
                    continue
                visited[ni][nj] = True
                nd = dist + 1
                ndoors = doors
                if 'A' <= cell <= 'Z':
                    ki = ord(cell.lower()) - ord('a')
                    ndoors |= (1 << ki)
                if 'a' <= cell <= 'z':
                    ki = key_index[cell]
                    found[ki] = (nd, ndoors)
                    dq.append((ni, nj, nd, ndoors))
                else:
                    dq.append((ni, nj, nd, ndoors))
        return found

    graph = {}
    for i, (sx, sy) in enumerate(starts):
        graph[i] = bfs_from(sx, sy)
    for k, (kx, ky) in enumerate([key_positions[c] for c in key_list], start=4):
        graph[k] = bfs_from(kx, ky)

    init_positions = tuple(range(len(starts)))
    pq = [(0, init_positions, 0)]
    seen = {(init_positions, 0): 0}
    while pq:
        cost, positions, mask = heapq.heappop(pq)
        if mask == total_keys_mask:
            return cost
        if seen[(positions, mask)] < cost:
            continue
        for i in range(len(starts)):
            u = positions[i]
            for ki, (dist, req_doors) in graph[u].items():
                bit = 1 << ki
                if mask & bit:
                    continue
                if (req_doors & mask) != req_doors:
                    continue
                new_mask = mask | bit
                new_positions = list(positions)
                new_positions[i] = ki + len(starts)
                new_positions = tuple(new_positions)
                new_cost = cost + dist
                state = (new_positions, new_mask)
                if seen.get(state, float('inf')) > new_cost:
                    seen[state] = new_cost
                    heapq.heappush(pq, (new_cost, new_positions, new_mask))
    return -1


def run_tests():
    tests = [(
        ['#######',
         '#a.#Cd#',
         '##@#@##',
         '#######',
         '##@#@##',
         '#cB#Ab#',
         '#######'],
        8
    ), (
        ['###############',
         '#d.ABC.#.....a#',
         '######@#@######',
         '###############',
         '######@#@######',
         '#b.....#.....c#',
         '###############'],
        24
    )]
    for idx, (raw, expected) in enumerate(tests, 1):
        grid = [list(line) for line in raw]
        result = solve(grid)
        print(f"Test {idx}: expected {expected}, got {result}")


def main():
    try:
        if os.fstat(0).st_size > 0:
            data = get_input()
            print(solve(data))
        else:
            run_tests()
    except OSError:
        run_tests()


if __name__ == '__main__':
    main()

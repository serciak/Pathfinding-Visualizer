import numpy as np
import heapq


class PathfindingAlgorithms:
    def dijkstra_shortest_path(self, board, start, end):
        if start is None or end is None:
            raise ValueError("Start or end point not found!")
        
        rows, cols = board.shape

        distance = np.inf * np.ones((rows, cols))
        distance[start] = 0

        priority_queue = []
        heapq.heappush(priority_queue, (0, start))

        visited = []

        while priority_queue:
            curr_dist, curr_node = heapq.heappop(priority_queue)

            if curr_node == end:
                # Shortest path found
                break

            visited.append(curr_node)

            neighbors = [(curr_node[0] - 1, curr_node[1]), (curr_node[0] + 1, curr_node[1]),
                        (curr_node[0], curr_node[1] - 1), (curr_node[0], curr_node[1] + 1)] # All possible movements up, down, right, left

            for neighbor in neighbors:
                neighbor_row, neighbor_col = neighbor
                if 0 <= neighbor_row < rows and 0 <= neighbor_col < cols:
                    if board[neighbor_row, neighbor_col] == 1:
                        continue  # Skip walls

                    tentative_dist = curr_dist + 1

                    if tentative_dist < distance[neighbor_row, neighbor_col]:
                        distance[neighbor_row, neighbor_col] = tentative_dist
                        heapq.heappush(priority_queue, (tentative_dist, neighbor))

        if distance[end] == np.inf:
            raise RuntimeError('No path found!')

        # Reconstruct the shortest path
        path = []
        current = end
        while current != start:
            path.append(np.ravel_multi_index(current, dims=(rows, cols)))
            neighbors = [(current[0] - 1, current[1]), (current[0] + 1, current[1]),
                        (current[0], current[1] - 1), (current[0], current[1] + 1)] # All possible movements up, down, right, left
            for neighbor in neighbors:
                neighbor_row, neighbor_col = neighbor
                if 0 <= neighbor_row < rows and 0 <= neighbor_col < cols:
                    if distance[neighbor_row, neighbor_col] == distance[current] - 1:
                        current = neighbor
                        break

        path.append(np.ravel_multi_index(start, dims=(rows, cols)))
        path.reverse()

        return visited, path


    def heuristic(self, node, end):
        # Manhattan distance heuristic
        return abs(node[0] - end[0]) + abs(node[1] - end[1])

    def astar_shortest_path(self, board, start, end):
        if start is None or end is None:
            raise ValueError("Start or end point not found!")
        rows, cols = board.shape

        distance = np.inf * np.ones((rows, cols))
        distance[start] = 0

        priority_queue = []
        heapq.heappush(priority_queue, (0, start))

        visited = []

        while priority_queue:
            _, curr_node = heapq.heappop(priority_queue)

            if curr_node == end:
                # Shortest path found
                break

            visited.append(curr_node)

            neighbors = [(curr_node[0] - 1, curr_node[1]), (curr_node[0] + 1, curr_node[1]),
                        (curr_node[0], curr_node[1] - 1), (curr_node[0], curr_node[1] + 1)] # All possible movements up, down, right, left

            for neighbor in neighbors:
                neighbor_row, neighbor_col = neighbor
                if 0 <= neighbor_row < rows and 0 <= neighbor_col < cols:
                    if board[neighbor_row, neighbor_col] == 1:
                        continue  # Skip walls

                    tentative_dist = distance[curr_node] + 1

                    if tentative_dist < distance[neighbor_row, neighbor_col]:
                        distance[neighbor_row, neighbor_col] = tentative_dist
                        priority = tentative_dist + self.heuristic(neighbor, end)
                        heapq.heappush(priority_queue, (priority, neighbor))

        if distance[end] == np.inf:
            raise RuntimeError('No path found!')

        # Reconstruct the shortest path
        path = []
        current = end
        while current != start:
            path.append(np.ravel_multi_index(current, dims=(rows, cols)))
            neighbors = [(current[0] - 1, current[1]), (current[0] + 1, current[1]),
                        (current[0], current[1] - 1), (current[0], current[1] + 1)] # All possible movements up, down, right, left
            for neighbor in neighbors:
                neighbor_row, neighbor_col = neighbor
                if 0 <= neighbor_row < rows and 0 <= neighbor_col < cols:
                    if distance[neighbor_row, neighbor_col] == distance[current] - 1 and neighbor in visited:
                        current = neighbor
                        break

        path.append(np.ravel_multi_index(start, dims=(rows, cols)))
        path.reverse()

        return visited, path
    

    def dfs_shortest_path(self, board, start, end):
        if start is None or end is None:
            raise ValueError("Start or end point not found!")
        
        rows, cols = board.shape

        visited = set()
        path = []

        def dfs(node):
            if node == end:
                return True

            visited.add(node)
            path.append(node)

            neighbors = [(node[0] - 1, node[1]), (node[0] + 1, node[1]),
                        (node[0], node[1] - 1), (node[0], node[1] + 1)]

            for neighbor in neighbors:
                neighbor_row, neighbor_col = neighbor
                if 0 <= neighbor_row < rows and 0 <= neighbor_col < cols:
                    if neighbor not in visited and board[neighbor_row, neighbor_col] != 1:
                        if dfs(neighbor):
                            return True

            path.remove(node)
            return False

        if dfs(start):
            # Shortest path found
            visited = list(visited)
            path = [np.ravel_multi_index(node, dims=(rows, cols)) for node in path]
            return visited, path

        raise RuntimeError('No path found!')
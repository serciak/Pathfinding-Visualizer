import numpy as np
import heapq


class PathfindingAlgorithms:
    def dijkstra_shortest_path(self, board, start, end):
        if start is None or end is None:
            raise ValueError("Start or end point not found!")
        
        # Get the number of rows and columns in the board
        rows, cols = board.shape

        # Initialize an array to store the distance to each node (initialized with infinity)
        distance = np.inf * np.ones((rows, cols))
        distance[start] = 0

        # Initialize a priority queue to store nodes prioritized by their distance
        priority_queue = []
        heapq.heappush(priority_queue, (0, start))
        visited = []

        while priority_queue:
            curr_dist, curr_node = heapq.heappop(priority_queue)

            # Check if the current node is the end node (shortest path found)
            if curr_node == end:
                break

            # Mark the current node as visited
            visited.append(curr_node)

            # Get the neighboring nodes (up, down, left, right)
            neighbors = [(curr_node[0] - 1, curr_node[1]), (curr_node[0] + 1, curr_node[1]),
                        (curr_node[0], curr_node[1] - 1), (curr_node[0], curr_node[1] + 1)]

            # Check each neighbor
            for neighbor in neighbors:
                neighbor_row, neighbor_col = neighbor
                # Verify if the neighbor is within the bounds of the board
                if 0 <= neighbor_row < rows and 0 <= neighbor_col < cols:
                    # Skip walls (obstacles with value 1)
                    if board[neighbor_row, neighbor_col] == 1:
                        continue

                    # Calculate the tentative distance to the neighbor
                    tentative_dist = curr_dist + 1

                    # Update the distance if the tentative distance is shorter
                    if tentative_dist < distance[neighbor_row, neighbor_col]:
                        distance[neighbor_row, neighbor_col] = tentative_dist

                        # Push the neighbor and its distance to the priority queue
                        heapq.heappush(priority_queue, (tentative_dist, neighbor))

        # If the distance to the end node is still infinity, no path is found
        if distance[end] == np.inf:
            raise RuntimeError('No path found!')

        # Reconstruct the shortest path from end to start
        path = []
        current = end
        while current != start:
            path.append(np.ravel_multi_index(current, dims=(rows, cols)))
            neighbors = [(current[0] - 1, current[1]), (current[0] + 1, current[1]),
                        (current[0], current[1] - 1), (current[0], current[1] + 1)]
            for neighbor in neighbors:
                neighbor_row, neighbor_col = neighbor
                if 0 <= neighbor_row < rows and 0 <= neighbor_col < cols:
                    # Find the neighbor with a distance one less than the current node and mark it as the new current node
                    if distance[neighbor_row, neighbor_col] == distance[current] - 1:
                        current = neighbor
                        break

        # Add the start node to the path and reverse the order
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

        # Initialize an array to store the distance to each node (initialized with infinity)
        distance = np.inf * np.ones((rows, cols))
        distance[start] = 0

        priority_queue = []
        heapq.heappush(priority_queue, (0, start))

        # Initialize a list to keep track of visited nodes
        visited = []

        while priority_queue:
            _, curr_node = heapq.heappop(priority_queue)

            # Check if the current node is the end node (shortest path found)
            if curr_node == end:
                break

            # Mark the current node as visited
            visited.append(curr_node)

            # Get the neighboring nodes (up, down, left, right)
            neighbors = [(curr_node[0] - 1, curr_node[1]), (curr_node[0] + 1, curr_node[1]),
                        (curr_node[0], curr_node[1] - 1), (curr_node[0], curr_node[1] + 1)]

            # Check each neighbor
            for neighbor in neighbors:
                neighbor_row, neighbor_col = neighbor
                # Verify if the neighbor is within the bounds of the board
                if 0 <= neighbor_row < rows and 0 <= neighbor_col < cols:
                    # Skip walls (obstacles with value 1)
                    if board[neighbor_row, neighbor_col] == 1:
                        continue

                    # Calculate the tentative distance to the neighbor
                    tentative_dist = distance[curr_node] + 1

                    # Update the distance if the tentative distance is shorter
                    if tentative_dist < distance[neighbor_row, neighbor_col]:
                        distance[neighbor_row, neighbor_col] = tentative_dist

                        # Calculate the priority of the neighbor based on the tentative distance and heuristic estimate
                        priority = tentative_dist + self.heuristic(neighbor, end)

                        # Push the neighbor and its priority to the priority queue
                        heapq.heappush(priority_queue, (priority, neighbor))

        # If the distance to the end node is still infinity, no path is found
        if distance[end] == np.inf:
            raise RuntimeError('No path found!')

        # Reconstruct the shortest path from end to start
        path = []
        current = end
        while current != start:
            path.append(np.ravel_multi_index(current, dims=(rows, cols)))
            neighbors = [(current[0] - 1, current[1]), (current[0] + 1, current[1]),
                        (current[0], current[1] - 1), (current[0], current[1] + 1)]
            for neighbor in neighbors:
                neighbor_row, neighbor_col = neighbor
                if 0 <= neighbor_row < rows and 0 <= neighbor_col < cols:
                    # Find the neighbor with a distance one less than the current node and mark it as the new current node
                    if distance[neighbor_row, neighbor_col] == distance[current] - 1 and neighbor in visited:
                        current = neighbor
                        break

        # Add the start node to the path and reverse the order
        path.append(np.ravel_multi_index(start, dims=(rows, cols)))
        path.reverse()

        return visited, path
    

    def dfs_shortest_path(self, board, start, end):
        if start is None or end is None:
            raise ValueError("Start or end point not found!")

        rows, cols = board.shape
        visited = []
        path = []

        stack = [(start, [start])]
        while stack:
            # Pop the top node and its current path from the stack
            node, current_path = stack.pop()

            # Check if the current node is the end node (path found)
            if node == end:
                path = current_path
                break

            if node != 1:
                visited.append(node)

            # Get the neighboring nodes (up, down, left, right)
            neighbors = [(node[0] - 1, node[1]), (node[0] + 1, node[1]),
                        (node[0], node[1] - 1), (node[0], node[1] + 1)]

            # Check each neighbor
            for neighbor in neighbors:
                neighbor_row, neighbor_col = neighbor
                # Verify if the neighbor is within the bounds of the board
                if 0 <= neighbor_row < rows and 0 <= neighbor_col < cols:
                    # Check if the neighbor has not been visited and is not an obstacle (value 1)
                    if neighbor not in visited and board[neighbor_row, neighbor_col] != 1:
                        # Push the neighbor and its updated path to the stack
                        stack.append((neighbor, current_path + [neighbor]))

        # If a path is found, convert the nodes to their corresponding indices and return the visited nodes and path
        if path:
            path = [np.ravel_multi_index(node, dims=(rows, cols)) for node in path]
            return visited, path

        # Raise an error if no path is found
        raise RuntimeError('No path found!')
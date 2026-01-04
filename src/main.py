import random
import sys
import time
from collections import deque  # 新增导入

class Maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walls = [[[True, True, True, True] for _ in range(width)] for _ in range(height)]
        self.start = (0, 0)
        self.end = (height-1, width-1)
        self.path = []
        self.generation_time = 0
        self.solution_time = 0  # 新增属性
        
    def remove_wall(self, y1, x1, y2, x2):
        if x1 == x2:
            if y2 > y1:
                self.walls[y1][x1][2] = False
                self.walls[y2][x2][0] = False
            else:
                self.walls[y1][x1][0] = False
                self.walls[y2][x2][2] = False
        elif y1 == y2:
            if x2 > x1:
                self.walls[y1][x1][1] = False
                self.walls[y2][x2][3] = False
            else:
                self.walls[y1][x1][3] = False
                self.walls[y2][x2][1] = False
    
    def print_maze_ascii(self):
        print("+" + "---+" * self.width)
        for y in range(self.height):
            row_str = "|"
            bottom_str = "+"
            for x in range(self.width):
                cell_content = " "
                if (y, x) == self.start:
                    cell_content = "S"
                elif (y, x) == self.end:
                    cell_content = "E"
                elif (y, x) in self.path:  # 修改：显示路径
                    cell_content = "*"
                
                if self.walls[y][x][1]:
                    row_str += f" {cell_content} |"
                else:
                    row_str += f" {cell_content}  "
                
                if self.walls[y][x][2]:
                    bottom_str += "---"
                else:
                    bottom_str += "   "
                bottom_str += "+"
            print(row_str)
            print(bottom_str)


class DisjointSet:
    def __init__(self, size):
        self.parent = list(range(size))
        self.rank = [0] * size
        
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
        
    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x != root_y:
            if self.rank[root_x] < self.rank[root_y]:
                self.parent[root_x] = root_y
            elif self.rank[root_x] > self.rank[root_y]:
                self.parent[root_y] = root_x
            else:
                self.parent[root_y] = root_x
                self.rank[root_x] += 1
            return True
        return False


class MazeGenerator:
    @staticmethod
    def generate_dfs(maze):
        sys.setrecursionlimit(maze.width * maze.height * 2)
        start_time = time.time()
        
        def dfs(y, x, visited):
            visited[y][x] = True
            directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
            random.shuffle(directions)
            
            for dy, dx in directions:
                ny, nx = y + dy, x + dx
                if 0 <= ny < maze.height and 0 <= nx < maze.width and not visited[ny][nx]:
                    maze.remove_wall(y, x, ny, nx)
                    dfs(ny, nx, visited)
        
        visited = [[False for _ in range(maze.width)] for _ in range(maze.height)]
        start_y, start_x = maze.start
        dfs(start_y, start_x, visited)
        
        maze.generation_time = time.time() - start_time
    
    @staticmethod
    def generate_kruskal(maze):
        start_time = time.time()
        
        edges = []
        
        for y in range(maze.height):
            for x in range(maze.width):
                cell_id = y * maze.width + x
                
                if x < maze.width - 1:
                    neighbor_id = y * maze.width + (x + 1)
                    edges.append((cell_id, neighbor_id, y, x, y, x + 1))
                
                if y < maze.height - 1:
                    neighbor_id = (y + 1) * maze.width + x
                    edges.append((cell_id, neighbor_id, y, x, y + 1, x))
        
        random.shuffle(edges)
        dsu = DisjointSet(maze.width * maze.height)
        
        for edge in edges:
            cell1_id, cell2_id, y1, x1, y2, x2 = edge
            if dsu.union(cell1_id, cell2_id):
                maze.remove_wall(y1, x1, y2, x2)
        
        maze.generation_time = time.time() - start_time


class MazeSolver:  # 新增类
    @staticmethod
    def solve_bfs(maze):
        start_time = time.time()
        start = maze.start
        end = maze.end
        
        queue = deque([start])
        visited = [[False for _ in range(maze.width)] for _ in range(maze.height)]
        visited[start[0]][start[1]] = True
        parent = {start: None}
        
        def can_move(y1, x1, y2, x2):  # 辅助函数
            if x1 == x2:
                if y2 > y1:
                    return not maze.walls[y1][x1][2]
                else:
                    return not maze.walls[y1][x1][0]
            elif y1 == y2:
                if x2 > x1:
                    return not maze.walls[y1][x1][1]
                else:
                    return not maze.walls[y1][x1][3]
            return False
        
        while queue:
            current = queue.popleft()
            
            if current == end:
                path = []
                while current is not None:
                    path.append(current)
                    current = parent[current]
                maze.path = path[::-1]
                maze.solution_time = time.time() - start_time
                return True
            
            y, x = current
            directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
            
            for dy, dx in directions:
                ny, nx = y + dy, x + dx
                if 0 <= ny < maze.height and 0 <= nx < maze.width:
                    if can_move(y, x, ny, nx) and not visited[ny][nx]:
                        visited[ny][nx] = True
                        parent[(ny, nx)] = current
                        queue.append((ny, nx))
        
        maze.solution_time = time.time() - start_time
        return False


def main():
    print("=== 迷宫生成与求解系统 v6.0 ===")  # 修改系统名和版本号
    print("添加BFS求解功能")  # 修改功能描述
    
    print("\n生成并求解迷宫：")
    maze = Maze(8, 8)
    MazeGenerator.generate_dfs(maze)
    print(f"迷宫生成耗时: {maze.generation_time:.4f}秒")
    
    print("\n未求解的迷宫：")
    maze.print_maze_ascii()
    
    print("\n使用BFS算法求解...")
    success = MazeSolver.solve_bfs(maze)
    
    if success:
        print(f"找到路径！求解耗时: {maze.solution_time:.4f}秒")
        print(f"路径长度: {len(maze.path)-1}步")
        print("\n求解后的迷宫：")
        maze.print_maze_ascii()
    else:
        print("未找到路径！")


if __name__ == "__main__":
    main()
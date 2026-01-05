import random
import sys
import time
from collections import deque

class Maze:
    def __init__(self, width, height):
        if width < 2 or height < 2:
            raise ValueError("迷宫尺寸至少为2x2")
        
        self.width = width
        self.height = height
        self.walls = [[[True, True, True, True] for _ in range(width)] for _ in range(height)]
        self.start = (0, 0)
        self.end = (height-1, width-1)
        self.path = []
        self.generation_time = 0
        self.solution_time = 0
        
    def remove_wall(self, y1, x1, y2, x2):
        if not (0 <= y1 < self.height and 0 <= x1 < self.width and
                0 <= y2 < self.height and 0 <= x2 < self.width):
            raise ValueError("坐标超出范围")
        
        if abs(y1 - y2) + abs(x1 - x2) != 1:
            raise ValueError("只能移除相邻单元格之间的墙")
        
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
    
    def has_wall(self, y1, x1, y2, x2):
        if not (0 <= y1 < self.height and 0 <= x1 < self.width and
                0 <= y2 < self.height and 0 <= x2 < self.width):
            raise ValueError("坐标超出范围")
        
        if abs(y1 - y2) + abs(x1 - x2) != 1:
            raise ValueError("只能检查相邻单元格之间的墙")
        
        if x1 == x2:
            if y2 > y1:
                return self.walls[y1][x1][2]
            else:
                return self.walls[y1][x1][0]
        else:
            if x2 > x1:
                return self.walls[y1][x1][1]
            else:
                return self.walls[y1][x1][3]
    
    def get_neighbors(self, y, x):
        neighbors = []
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        
        for dy, dx in directions:
            ny, nx = y + dy, x + dx
            if 0 <= ny < self.height and 0 <= nx < self.width:
                neighbors.append((ny, nx))
        return neighbors
    
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
                elif (y, x) in self.path:
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


class MazeSolver:
    @staticmethod
    def solve_bfs(maze):
        start_time = time.time()
        start = maze.start
        end = maze.end
        
        queue = deque([start])
        visited = [[False for _ in range(maze.width)] for _ in range(maze.height)]
        visited[start[0]][start[1]] = True
        parent = {start: None}
        
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
            for ny, nx in maze.get_neighbors(y, x):
                if not maze.has_wall(y, x, ny, nx) and not visited[ny][nx]:
                    visited[ny][nx] = True
                    parent[(ny, nx)] = current
                    queue.append((ny, nx))
        
        maze.solution_time = time.time() - start_time
        return False


def run_performance_test():  # 新增函数
    print("\n性能测试：")
    print("-" * 50)
    print(f"{'尺寸':<8} {'DFS时间':<10} {'Kruskal时间':<12} {'DFS求解':<10} {'总时间比':<10}")
    print("-" * 50)
    
    sizes = [(5, 5), (8, 8), (10, 10), (12, 12)]
    
    for width, height in sizes:
        dfs_gen_times = []
        kruskal_gen_times = []
        dfs_solve_times = []
        
        for _ in range(2):
            # 测试DFS生成
            try:
                maze = Maze(width, height)
                start = time.time()
                MazeGenerator.generate_dfs(maze)
                dfs_gen_times.append(time.time() - start)
                
                # 测试DFS生成后的求解
                start = time.time()
                MazeSolver.solve_bfs(maze)
                dfs_solve_times.append(time.time() - start)
            except:
                pass
            
            # 测试Kruskal生成
            try:
                maze = Maze(width, height)
                start = time.time()
                MazeGenerator.generate_kruskal(maze)
                kruskal_gen_times.append(time.time() - start)
            except:
                pass
        
        if dfs_gen_times and kruskal_gen_times and dfs_solve_times:
            dfs_avg = sum(dfs_gen_times) / len(dfs_gen_times)
            kruskal_avg = sum(kruskal_gen_times) / len(kruskal_gen_times)
            solve_avg = sum(dfs_solve_times) / len(dfs_solve_times)
            total_ratio = (kruskal_avg + solve_avg) / (dfs_avg + solve_avg) if (dfs_avg + solve_avg) > 0 else 0
            
            print(f"{width}x{height:<3} {dfs_avg:<10.4f} {kruskal_avg:<12.4f} {solve_avg:<10.4f} {total_ratio:<10.2f}")
    
    print("-" * 50)
    print("总时间比 > 1: Kruskal较慢, < 1: Kruskal较快")


def simple_interface():
    print("=== 迷宫生成与求解系统 v9.0 ===")  # 修改版本号
    print("添加性能测试功能")  # 修改功能描述
    
    maze = None
    
    while True:
        print("\n请选择操作：")
        print("1. 生成DFS迷宫")
        print("2. 生成Kruskal迷宫")
        print("3. 求解迷宫")
        print("4. 显示迷宫")
        print("5. 清除路径")
        print("6. 运行性能测试")  # 新增选项
        print("0. 退出")
        
        choice = input("请输入选择 (0-6): ").strip()  # 修改：改为0-6
        
        if choice == "0":
            print("再见！")
            break
        elif choice == "1":
            try:
                size = int(input("请输入迷宫大小 (5-15): "))
                if 5 <= size <= 15:
                    maze = Maze(size, size)
                    MazeGenerator.generate_dfs(maze)
                    print(f"DFS迷宫生成完成，耗时: {maze.generation_time:.4f}秒")
                else:
                    print("大小必须在5-15之间")
            except ValueError as e:
                print(f"错误: {e}")
        elif choice == "2":
            try:
                size = int(input("请输入迷宫大小 (5-15): "))
                if 5 <= size <= 15:
                    maze = Maze(size, size)
                    MazeGenerator.generate_kruskal(maze)
                    print(f"Kruskal迷宫生成完成，耗时: {maze.generation_time:.4f}秒")
                else:
                    print("大小必须在5-15之间")
            except ValueError as e:
                print(f"错误: {e}")
        elif choice == "3":
            if maze:
                print("正在求解...")
                success = MazeSolver.solve_bfs(maze)
                if success:
                    print(f"求解完成，耗时: {maze.solution_time:.4f}秒")
                    print(f"路径长度: {len(maze.path)-1}步")
                else:
                    print("求解失败")
            else:
                print("请先生成迷宫")
        elif choice == "4":
            if maze:
                print("\n当前迷宫：")
                maze.print_maze_ascii()
            else:
                print("请先生成迷宫")
        elif choice == "5":
            if maze:
                maze.path = []
                print("路径已清除")
            else:
                print("请先生成迷宫")
        elif choice == "6":  # 新增选项处理
            run_performance_test()
        else:
            print("无效选择")


def main():
    simple_interface()


if __name__ == "__main__":
    main()
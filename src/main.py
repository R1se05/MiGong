import random
import sys
import time
import os  # 新增导入
import json  # 新增导入
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
        self.algorithm = "Unknown"
        
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
    
    def get_neighbors(self, y, x, with_walls=False):
        neighbors = []
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        
        for dy, dx in directions:
            ny, nx = y + dy, x + dx
            if 0 <= ny < self.height and 0 <= nx < self.width:
                if not with_walls:
                    neighbors.append((ny, nx))
                elif not self.has_wall(y, x, ny, nx):
                    neighbors.append((ny, nx))
        return neighbors
    
    def is_connected(self):
        visited = [[False for _ in range(self.width)] for _ in range(self.height)]
        stack = [self.start]
        visited[self.start[0]][self.start[1]] = True
        
        while stack:
            y, x = stack.pop()
            
            if (y, x) == self.end:
                return True
            
            for ny, nx in self.get_neighbors(y, x, with_walls=True):
                if not visited[ny][nx]:
                    visited[ny][nx] = True
                    stack.append((ny, nx))
        
        return False
    
    def to_dict(self):  # 新增方法
        return {
            'width': self.width,
            'height': self.height,
            'start': self.start,
            'end': self.end,
            'algorithm': self.algorithm,
            'generation_time': self.generation_time,
            'solution_time': self.solution_time,
            'path': self.path,
            'walls': self.walls
        }
    
    @classmethod
    def from_dict(cls, data):  # 新增方法
        maze = cls(data['width'], data['height'])
        maze.start = tuple(data['start'])
        maze.end = tuple(data['end'])
        maze.algorithm = data['algorithm']
        maze.generation_time = data['generation_time']
        maze.solution_time = data['solution_time']
        maze.path = [tuple(p) for p in data['path']]
        maze.walls = data['walls']
        return maze
    
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
        maze.algorithm = "DFS"
    
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
        maze.algorithm = "Kruskal"


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
            for ny, nx in maze.get_neighbors(y, x, with_walls=True):
                if not visited[ny][nx]:
                    visited[ny][nx] = True
                    parent[(ny, nx)] = current
                    queue.append((ny, nx))
        
        maze.solution_time = time.time() - start_time
        return False


class ConsoleInterface:
    def __init__(self):
        self.maze = None
    
    def display_menu(self):
        print("\n" + "="*50)
        print("迷宫生成与求解系统 v12.0")  # 修改版本号
        print("="*50)
        print("1. 生成DFS迷宫")
        print("2. 生成Kruskal迷宫")
        print("3. 求解迷宫")
        print("4. 显示迷宫")
        print("5. 清除路径")
        print("6. 性能测试")
        print("7. 设置迷宫尺寸")
        print("8. 检查连通性")
        print("9. 保存迷宫")  # 新增选项
        print("10. 加载迷宫")  # 新增选项
        print("0. 退出")
        print("="*50)
    
    def run(self):
        default_size = 10
        
        while True:
            self.display_menu()
            choice = input("请输入选择 (0-10): ").strip()  # 修改：改为0-10
            
            if choice == "0":
                print("感谢使用，再见！")
                break
            
            elif choice == "1":
                size = self.get_maze_size(default_size)
                print(f"使用DFS算法生成 {size}x{size} 迷宫...")
                try:
                    self.maze = Maze(size, size)
                    MazeGenerator.generate_dfs(self.maze)
                    print(f"迷宫生成完成！耗时: {self.maze.generation_time:.4f}秒")
                    self.display_maze_info()
                except ValueError as e:
                    print(f"错误: {e}")
            
            elif choice == "2":
                size = self.get_maze_size(default_size)
                print(f"使用Kruskal算法生成 {size}x{size} 迷宫...")
                try:
                    self.maze = Maze(size, size)
                    MazeGenerator.generate_kruskal(self.maze)
                    print(f"迷宫生成完成！耗时: {self.maze.generation_time:.4f}秒")
                    self.display_maze_info()
                except ValueError as e:
                    print(f"错误: {e}")
            
            elif choice == "3":
                if self.maze:
                    print("使用BFS算法求解迷宫...")
                    success = MazeSolver.solve_bfs(self.maze)
                    if success:
                        print(f"找到路径！耗时: {self.maze.solution_time:.4f}秒")
                        print(f"路径长度: {len(self.maze.path)-1}步")
                        self.display_maze_info()
                    else:
                        print("未找到路径！")
                else:
                    print("请先生成迷宫！")
            
            elif choice == "4":
                if self.maze:
                    self.display_maze_info()
                else:
                    print("请先生成迷宫！")
            
            elif choice == "5":
                if self.maze:
                    self.maze.path = []
                    print("路径已清除")
                else:
                    print("请先生成迷宫！")
            
            elif choice == "6":
                self.run_performance_test()
            
            elif choice == "7":
                default_size = self.get_maze_size(default_size)
                print(f"默认迷宫尺寸已设置为: {default_size}x{default_size}")
            
            elif choice == "8":
                if self.maze:
                    if self.maze.is_connected():
                        print("迷宫是连通的（起点到终点有路径）")
                    else:
                        print("迷宫不是连通的（起点到终点无路径）")
                else:
                    print("请先生成迷宫！")
            
            elif choice == "9":  # 新增选项处理
                self.save_maze()
            
            elif choice == "10":  # 新增选项处理
                self.load_maze()
            
            else:
                print("无效选择，请重新输入！")
    
    def get_maze_size(self, default_size):
        try:
            size_str = input(f"请输入迷宫大小 (当前: {default_size}): ").strip()
            if size_str:
                size = int(size_str)
                if 5 <= size <= 20:
                    return size
                else:
                    print("大小必须在5-20之间，使用默认值")
        except ValueError:
            print("输入无效，使用默认值")
        return default_size
    
    def display_maze_info(self):
        if self.maze:
            print(f"\n迷宫信息：")
            print(f"尺寸: {self.maze.width}x{self.maze.height}")
            print(f"算法: {self.maze.algorithm}")
            print(f"生成时间: {self.maze.generation_time:.4f}秒")
            if self.maze.solution_time > 0:
                print(f"求解时间: {self.maze.solution_time:.4f}秒")
                print(f"路径长度: {len(self.maze.path)-1}步")
            print()
            self.maze.print_maze_ascii()
    
    def run_performance_test(self):
        print("\n性能测试：")
        print("-" * 50)
        print(f"{'尺寸':<8} {'DFS(秒)':<10} {'Kruskal(秒)':<12} {'速度比':<10}")
        print("-" * 50)
        
        sizes = [(5, 5), (8, 8), (10, 10), (12, 12)]
        
        for width, height in sizes:
            dfs_times = []
            kruskal_times = []
            
            for _ in range(2):
                try:
                    maze = Maze(width, height)
                    start = time.time()
                    MazeGenerator.generate_dfs(maze)
                    dfs_times.append(time.time() - start)
                except:
                    pass
                
                try:
                    maze = Maze(width, height)
                    start = time.time()
                    MazeGenerator.generate_kruskal(maze)
                    kruskal_times.append(time.time() - start)
                except:
                    pass
            
            if dfs_times and kruskal_times:
                dfs_avg = sum(dfs_times) / len(dfs_times)
                kruskal_avg = sum(kruskal_times) / len(kruskal_times)
                ratio = kruskal_avg / dfs_avg if dfs_avg > 0 else 0
                print(f"{width}x{height:<3} {dfs_avg:<10.4f} {kruskal_avg:<12.4f} {ratio:<10.2f}")
        
        print("-" * 50)
        print("速度比 > 1: Kruskal较慢, < 1: Kruskal较快")
    
    def save_maze(self):  # 新增方法
        if not self.maze:
            print("请先生成迷宫！")
            return
        
        filename = input("请输入保存的文件名 (例如: maze.json): ").strip()
        if not filename:
            print("文件名不能为空！")
            return
        
        if not filename.endswith('.json'):
            filename += '.json'
        
        try:
            maze_dict = self.maze.to_dict()
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(maze_dict, f, indent=2, default=str)
            print(f"迷宫已保存到: {filename}")
        except Exception as e:
            print(f"保存失败: {e}")
    
    def load_maze(self):  # 新增方法
        filename = input("请输入要加载的文件名: ").strip()
        if not filename:
            print("文件名不能为空！")
            return
        
        if not os.path.exists(filename):
            print(f"文件不存在: {filename}")
            return
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                maze_dict = json.load(f)
            
            self.maze = Maze.from_dict(maze_dict)
            print(f"成功加载迷宫: {filename}")
            print(f"尺寸: {self.maze.width}x{self.maze.height}")
            print(f"算法: {self.maze.algorithm}")
        except json.JSONDecodeError:
            print("文件格式错误！")
        except Exception as e:
            print(f"加载失败: {e}")


def main():
    print("=== 迷宫生成与求解系统 v12.0 ===")
    print("添加文件保存/加载功能")  # 修改功能描述
    
    interface = ConsoleInterface()
    interface.run()


if __name__ == "__main__":
    main()
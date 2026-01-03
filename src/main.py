import random
import sys
import time  # 新增：导入time模块

# 从v1复制所有类...

# === 修改开始：添加Kruskal算法相关代码 ===
class DisjointSet:
    """并查集，用于Kruskal算法"""
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
        start_time = time.time()  # 修改：添加计时
        
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
        
        maze.walls[maze.start[0]][maze.start[1]][3] = False
        maze.walls[maze.end[0]][maze.end[1]][1] = False
        
        return time.time() - start_time  # 修改：返回生成时间
    
    # 新增：Kruskal算法
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
        
        maze.walls[maze.start[0]][maze.start[1]][3] = False
        maze.walls[maze.end[0]][maze.end[1]][1] = False
        
        return time.time() - start_time
# === 修改结束 ===


def main():
    print("=== 迷宫生成与求解系统 v2.0 ===")
    print("功能：DFS + Kruskal迷宫生成")
    
    width = 10
    height = 10
    
    # 修改：测试两种算法
    print(f"\n测试 {width}x{height} 的迷宫生成：")
    
    print("\n1. 使用DFS算法生成迷宫...")
    maze_dfs = Maze(width, height)
    dfs_time = MazeGenerator.generate_dfs(maze_dfs)
    print(f"DFS算法耗时: {dfs_time:.4f}秒")
    
    print("\n2. 使用Kruskal算法生成迷宫...")
    maze_kruskal = Maze(width, height)
    kruskal_time = MazeGenerator.generate_kruskal(maze_kruskal)
    print(f"Kruskal算法耗时: {kruskal_time:.4f}秒")
    
    # 新增：算法比较
    print(f"\n算法比较：")
    print(f"DFS算法: {dfs_time:.4f}秒")
    print(f"Kruskal算法: {kruskal_time:.4f}秒")
    if dfs_time > 0:
        ratio = kruskal_time / dfs_time
        print(f"速度比: {ratio:.2f}")
    
    print("\nDFS算法生成的迷宫：")
    maze_dfs.print_maze_ascii()


if __name__ == "__main__":
    main()
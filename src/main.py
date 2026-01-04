import random
import sys

class Maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walls = [[[True, True, True, True] for _ in range(width)] for _ in range(height)]
        self.start = (0, 0)
        self.end = (height-1, width-1)
        self.path = []
        
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


class MazeGenerator:  # 新增类
    @staticmethod
    def generate_dfs(maze):
        sys.setrecursionlimit(maze.width * maze.height * 2)
        
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


def main():
    print("=== 迷宫生成系统 v2.0 ===")  # 修改版本号
    print("添加DFS生成算法")  # 修改功能描述
    
    maze = Maze(5, 5)
    MazeGenerator.generate_dfs(maze)  # 调用生成算法
    
    print(f"创建了 {maze.width}x{maze.height} 的迷宫")
    print("使用DFS算法生成了迷宫")


if __name__ == "__main__":
    main()
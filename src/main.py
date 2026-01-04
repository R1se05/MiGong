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
    
    def print_maze_ascii(self):  # 新增方法
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


class MazeGenerator:
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
    print("=== 迷宫生成系统 v3.0 ===")  # 修改版本号
    print("添加ASCII显示功能")  # 修改功能描述
    
    maze = Maze(8, 8)  # 修改：改为8x8
    MazeGenerator.generate_dfs(maze)
    
    print(f"\n{8}x{8} 迷宫：")  # 修改输出
    maze.print_maze_ascii()  # 调用显示方法


if __name__ == "__main__":
    main()
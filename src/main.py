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
        
        maze.walls[maze.start[0]][maze.start[1]][3] = False
        maze.walls[maze.end[0]][maze.end[1]][1] = False


def main():
    print("=== 迷宫生成与求解系统 v1.0 ===")
    print("功能：DFS迷宫生成")
    
    width = 10
    height = 10
    
    print(f"生成 {width}x{height} 的迷宫...")
    
    maze = Maze(width, height)
    MazeGenerator.generate_dfs(maze)
    
    print("\n生成的迷宫：")
    maze.print_maze_ascii()
    
    print(f"\n迷宫信息：")
    print(f"尺寸: {width}x{height}")
    print(f"起点: {maze.start}")
    print(f"终点: {maze.end}")


if __name__ == "__main__":
    main()
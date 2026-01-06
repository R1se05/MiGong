import random
import time
from collections import deque
import sys
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading

class Maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walls = [[[True, True, True, True] for _ in range(width)] for _ in range(height)]
        self.start = (0, 0)  
        self.end = (height-1, width-1) 
        self.path = []  
        self.generation_time = 0
        self.solution_time = 0
        
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
                
    def get_neighbors(self, y, x, with_walls=True):
        neighbors = []
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)] 
        
        for dy, dx in directions:
            ny, nx = y + dy, x + dx
            if 0 <= ny < self.height and 0 <= nx < self.width:
                if not with_walls:
                    neighbors.append((ny, nx))
                else:
                    if dy == -1: 
                        if not self.walls[y][x][0]:
                            neighbors.append((ny, nx))
                    elif dy == 1:
                        if not self.walls[y][x][2]:
                            neighbors.append((ny, nx))
                    elif dx == 1: 
                        if not self.walls[y][x][1]:
                            neighbors.append((ny, nx))
                    elif dx == -1: 
                        if not self.walls[y][x][3]:
                            neighbors.append((ny, nx))
        return neighbors


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

        maze.walls[maze.start[0]][maze.start[1]][3] = False  
        maze.walls[maze.end[0]][maze.end[1]][1] = False  
        
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

        maze.walls[maze.start[0]][maze.start[1]][3] = False
        maze.walls[maze.end[0]][maze.end[1]][1] = False
        
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
                maze.path = path[::-1]  # 反转路径
                maze.solution_time = time.time() - start_time
                return True

            neighbors = maze.get_neighbors(current[0], current[1], with_walls=True)
            
            for neighbor in neighbors:
                if not visited[neighbor[0]][neighbor[1]]:
                    visited[neighbor[0]][neighbor[1]] = True
                    parent[neighbor] = current
                    queue.append(neighbor)
        
        maze.solution_time = time.time() - start_time
        return False  


class MazeGUI:
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("迷宫生成与求解系统")
        self.root.geometry("1200x700")

        self.setup_styles()

        self.setup_ui()

        self.current_maze = None
        self.cell_size = 30
        
    def setup_styles(self):
        """设置UI样式"""
        style = ttk.Style()
        style.theme_use('clam')

        self.bg_color = "#f0f0f0"
        self.cell_color = "#ffffff"
        self.wall_color = "#333333"
        self.start_color = "#4CAF50"
        self.end_color = "#F44336"
        self.path_color = "#2196F3"
        self.grid_color = "#e0e0e0"
        
        self.root.configure(bg=self.bg_color)
    
    def setup_ui(self):
        """设置用户界面"""

        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        control_frame = ttk.LabelFrame(main_frame, text="控制面板", padding=15)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        settings_frame = ttk.LabelFrame(control_frame, text="迷宫设置", padding=10)
        settings_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(settings_frame, text="宽度 (5-40):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.width_var = tk.IntVar(value=15)
        width_spinbox = ttk.Spinbox(settings_frame, from_=5, to=40, textvariable=self.width_var, width=10)
        width_spinbox.grid(row=0, column=1, pady=5, padx=(5, 0))

        ttk.Label(settings_frame, text="高度 (5-40):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.height_var = tk.IntVar(value=15)
        height_spinbox = ttk.Spinbox(settings_frame, from_=5, to=40, textvariable=self.height_var, width=10)
        height_spinbox.grid(row=1, column=1, pady=5, padx=(5, 0))

        ttk.Label(settings_frame, text="生成算法:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.algorithm_var = tk.StringVar(value="DFS")
        algorithms = ["DFS", "Kruskal"]
        algorithm_menu = ttk.Combobox(settings_frame, textvariable=self.algorithm_var, 
                                     values=algorithms, state="readonly", width=8)
        algorithm_menu.grid(row=2, column=1, pady=5, padx=(5, 0))

        ttk.Separator(control_frame, orient='horizontal').pack(fill=tk.X, pady=10)
        
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill=tk.X)
        
        self.generate_btn = ttk.Button(button_frame, text="生成迷宫", 
                                      command=self.generate_maze, width=15)
        self.generate_btn.pack(pady=5)
        
        self.solve_btn = ttk.Button(button_frame, text="求解迷宫", 
                                   command=self.solve_maze, width=15, state=tk.DISABLED)
        self.solve_btn.pack(pady=5)
        
        self.clear_btn = ttk.Button(button_frame, text="清除路径", 
                                   command=self.clear_path, width=15, state=tk.DISABLED)
        self.clear_btn.pack(pady=5)
        
        self.performance_btn = ttk.Button(button_frame, text="性能测试", 
                                         command=self.run_performance_test, width=15)
        self.performance_btn.pack(pady=5)
        
        options_frame = ttk.LabelFrame(control_frame, text="显示选项", padding=10)
        options_frame.pack(fill=tk.X, pady=10)
        
        self.show_path_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="显示路径", variable=self.show_path_var,
                       command=self.redraw_maze).pack(anchor=tk.W, pady=2)
        
        self.show_grid_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="显示网格", variable=self.show_grid_var,
                       command=self.redraw_maze).pack(anchor=tk.W, pady=2)
        
        self.thick_walls_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="加粗墙体", variable=self.thick_walls_var,
                       command=self.redraw_maze).pack(anchor=tk.W, pady=2)
        
        info_frame = ttk.LabelFrame(control_frame, text="迷宫信息", padding=10)
        info_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        self.info_text = scrolledtext.ScrolledText(info_frame, height=10, width=25,
                                                  font=("Consolas", 9))
        self.info_text.pack(fill=tk.BOTH, expand=True)
        self.info_text.configure(state=tk.DISABLED)
        
        display_frame = ttk.Frame(main_frame)
        display_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(display_frame, bg="white", bd=2, relief=tk.SUNKEN)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.status_var = tk.StringVar(value="就绪")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def update_status(self, message):
        self.status_var.set(message)
        self.root.update_idletasks()
    
    def update_info(self, info_text):
        self.info_text.configure(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(tk.END, info_text)
        self.info_text.configure(state=tk.DISABLED)
    
    def generate_maze(self):
        try:
            width = self.width_var.get()
            height = self.height_var.get()
            algorithm = self.algorithm_var.get()
            
            if not (5 <= width <= 40 and 5 <= height <= 40):
                messagebox.showerror("错误", "迷宫尺寸必须在5-40之间！")
                return
            
            self.generate_btn.configure(state=tk.DISABLED)
            self.solve_btn.configure(state=tk.DISABLED)
            self.clear_btn.configure(state=tk.DISABLED)
            
            threading.Thread(target=self._generate_maze_thread, 
                           args=(width, height, algorithm), daemon=True).start()
            
        except Exception as e:
            messagebox.showerror("错误", f"生成迷宫时出错：{str(e)}")
            self.generate_btn.configure(state=tk.NORMAL)
    
    def _generate_maze_thread(self, width, height, algorithm):
        try:
            self.update_status("正在生成迷宫...")
            maze = Maze(width, height)
            
            if algorithm == "DFS":
                MazeGenerator.generate_dfs(maze)
            else:  # Kruskal
                MazeGenerator.generate_kruskal(maze)
            
            self.current_maze = maze
            info = f"算法: {algorithm}\n"
            info += f"尺寸: {width}x{height}\n"
            info += f"生成时间: {maze.generation_time:.4f}秒\n"
            info += f"起点: (0, 0)\n"
            info += f"终点: ({height-1}, {width-1})\n"
            info += f"路径长度: 未求解\n"
            info += "-" * 30 + "\n"
            
            self.update_info(info)
            self.root.after(0, self.draw_maze, maze, f"{algorithm}算法生成的迷宫")
            self.root.after(0, lambda: self.solve_btn.configure(state=tk.NORMAL))
            self.root.after(0, lambda: self.clear_btn.configure(state=tk.NORMAL))
            
            self.update_status("迷宫生成完成！")
            
        except Exception as e:
            self.root.after(0, messagebox.showerror, "错误", f"生成迷宫时出错：{str(e)}")
        
        finally:
            self.root.after(0, lambda: self.generate_btn.configure(state=tk.NORMAL))
    
    def solve_maze(self):
        if not self.current_maze:
            messagebox.showwarning("警告", "请先生成迷宫！")
            return
        
        try:
            self.solve_btn.configure(state=tk.DISABLED)
            
            threading.Thread(target=self._solve_maze_thread, daemon=True).start()
            
        except Exception as e:
            messagebox.showerror("错误", f"求解迷宫时出错：{str(e)}")
            self.solve_btn.configure(state=tk.NORMAL)
    
    def _solve_maze_thread(self):
        """求解迷宫的线程函数"""
        try:
            self.update_status("正在求解迷宫...")
            
            maze = self.current_maze
            
            success = MazeSolver.solve_bfs(maze)
            
            if success:
                info = f"算法: {self.algorithm_var.get()}\n"
                info += f"尺寸: {maze.width}x{maze.height}\n"
                info += f"生成时间: {maze.generation_time:.4f}秒\n"
                info += f"求解时间: {maze.solution_time:.4f}秒\n"
                info += f"起点: (0, 0)\n"
                info += f"终点: ({maze.height-1}, {maze.width-1})\n"
                info += f"路径长度: {len(maze.path)-1}步\n"
                info += "-" * 30 + "\n"
                
                self.root.after(0, self.update_info, info)
                self.root.after(0, self.redraw_maze)
                self.update_status(f"迷宫求解完成！路径长度：{len(maze.path)-1}步")
            else:
                self.root.after(0, messagebox.showwarning, "警告", "未找到路径！")
                self.update_status("未找到路径")
            
        except Exception as e:
            self.root.after(0, messagebox.showerror, "错误", f"求解迷宫时出错：{str(e)}")
        
        finally:
            self.root.after(0, lambda: self.solve_btn.configure(state=tk.NORMAL))
    
    def clear_path(self):
        """清除路径"""
        if self.current_maze:
            self.current_maze.path = []
        
        self.redraw_maze()
        self.update_status("路径已清除")
    
    def draw_maze(self, maze, title=""):
        """绘制迷宫"""
        self.current_maze = maze
        self.canvas.delete("all")
        
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width > 50 and canvas_height > 50:
            cell_width = min(canvas_width // (maze.width + 2), 
                           canvas_height // (maze.height + 2))
            self.cell_size = max(10, min(40, cell_width))
        
        if title:
            self.canvas.create_text(canvas_width//2, 20, text=title, 
                                  font=("Arial", 14, "bold"), fill="black")
        
        start_x = (canvas_width - maze.width * self.cell_size) // 2
        start_y = 50 + (canvas_height - 50 - maze.height * self.cell_size) // 2
        
        for y in range(maze.height):
            for x in range(maze.width):
                x1 = start_x + x * self.cell_size
                y1 = start_y + y * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                if (y, x) == maze.start:
                    color = self.start_color
                elif (y, x) == maze.end:
                    color = self.end_color
                elif self.show_path_var.get() and (y, x) in maze.path:
                    color = self.path_color
                else:
                    color = self.cell_color
                
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, 
                                           outline=self.grid_color if self.show_grid_var.get() else color)
                
                wall_width = 3 if self.thick_walls_var.get() else 1
                
                if maze.walls[y][x][0]:  # 上墙
                    self.canvas.create_line(x1, y1, x2, y1, 
                                          fill=self.wall_color, width=wall_width)
                if maze.walls[y][x][1]:  # 右墙
                    self.canvas.create_line(x2, y1, x2, y2, 
                                          fill=self.wall_color, width=wall_width)
                if maze.walls[y][x][2]:  # 下墙
                    self.canvas.create_line(x1, y2, x2, y2, 
                                          fill=self.wall_color, width=wall_width)
                if maze.walls[y][x][3]:  # 左墙
                    self.canvas.create_line(x1, y1, x1, y2, 
                                          fill=self.wall_color, width=wall_width)
        
        self.draw_legend(start_x, start_y + maze.height * self.cell_size + 20)
    
    def draw_legend(self, x, y):
        legend_items = [
            ("起点", self.start_color),
            ("终点", self.end_color),
            ("路径", self.path_color),
            ("墙体", self.wall_color)
        ]
        
        for i, (text, color) in enumerate(legend_items):
            box_x = x + i * 100
            box_size = 15
            
            if text == "墙体":
                self.canvas.create_rectangle(box_x, y, box_x + box_size, y + box_size, 
                                           fill="white", outline=color, width=2)
            else:
                self.canvas.create_rectangle(box_x, y, box_x + box_size, y + box_size, 
                                           fill=color, outline="black")
            
            self.canvas.create_text(box_x + box_size + 10, y + box_size//2, 
                                  text=text, anchor=tk.W, font=("Arial", 10))
    
    def redraw_maze(self):
        if self.current_maze:
            self.draw_maze(self.current_maze, f"{self.algorithm_var.get()}算法生成的迷宫")
    
    def run_performance_test(self):
        try:
            self.performance_btn.configure(state=tk.DISABLED)
            
            threading.Thread(target=self._performance_test_thread, daemon=True).start()
            
        except Exception as e:
            messagebox.showerror("错误", f"性能测试出错：{str(e)}")
            self.performance_btn.configure(state=tk.NORMAL)
    
    def _performance_test_thread(self):
        """性能测试线程函数"""
        try:
            self.update_status("正在进行性能测试...")
            
            sizes = [(10, 10), (15, 15), (20, 20), (25, 25)]
            results = []
            
            result_text = "性能测试：DFS vs Kruskal 算法\n"
            result_text += "=" * 50 + "\n"
            result_text += f"{'迷宫大小':<10} {'DFS时间(秒)':<12} {'Kruskal时间(秒)':<15} {'速度比(K/D)':<10}\n"
            result_text += "-" * 50 + "\n"
            
            for width, height in sizes:
                dfs_times = []
                for _ in range(3):
                    start_time = time.time()
                    maze = Maze(width, height)
                    MazeGenerator.generate_dfs(maze)
                    dfs_times.append(time.time() - start_time)
                dfs_avg = sum(dfs_times) / len(dfs_times)
                
                kruskal_times = []
                for _ in range(3):
                    start_time = time.time()
                    maze = Maze(width, height)
                    MazeGenerator.generate_kruskal(maze)
                    kruskal_times.append(time.time() - start_time)
                kruskal_avg = sum(kruskal_times) / len(kruskal_times)
                
                ratio = kruskal_avg / dfs_avg if dfs_avg > 0 else 0
                results.append((width, height, dfs_avg, kruskal_avg, ratio))
                
                result_text += f"{width}x{height:<7} {dfs_avg:<12.4f} {kruskal_avg:<15.4f} {ratio:<10.2f}\n"
            
            result_text += "-" * 50 + "\n"
            result_text += "说明：速度比 > 1 表示Kruskal较慢，< 1 表示Kruskal较快\n"
            
            self.root.after(0, self.show_performance_results, result_text)
            self.update_status("性能测试完成！")
            
        except Exception as e:
            self.root.after(0, messagebox.showerror, "错误", f"性能测试出错：{str(e)}")
        
        finally:
            self.root.after(0, lambda: self.performance_btn.configure(state=tk.NORMAL))
    
    def show_performance_results(self, result_text):
        result_window = tk.Toplevel(self.root)
        result_window.title("性能测试结果")
        result_window.geometry("600x400")
        

        text_widget = scrolledtext.ScrolledText(result_window, wrap=tk.WORD, 
                                               font=("Consolas", 10))
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        text_widget.insert(tk.END, result_text)
        text_widget.configure(state=tk.DISABLED)
        
        ttk.Button(result_window, text="关闭", 
                  command=result_window.destroy).pack(pady=10)
    
    def run(self):
        """运行GUI"""
        self.root.mainloop()


def main():
    gui = MazeGUI()
    gui.run()


if __name__ == "__main__":
    main()
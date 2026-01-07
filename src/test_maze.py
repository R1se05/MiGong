import unittest
import time
import sys
import os
import random
from io import StringIO
import tempfile
from main import Maze, MazeGenerator, MazeSolver, DisjointSet

# ... [之前的测试类保持不变，包括 TestDisjointSet, TestMaze, TestMazeGenerator, TestMazeSolver, TestIntegration] ...

class PerformanceTest:
    """性能测试类"""
    
    @staticmethod
    def run_comprehensive_performance_test():
        """运行全面的性能测试"""
        print("=" * 60)
        print("迷宫生成与求解系统 - 性能测试报告")
        print("=" * 60)
        
        sizes = [(5, 5), (10, 10), (15, 15), (20, 20), (25, 25)]
        algorithms = [
            ("DFS", MazeGenerator.generate_dfs),
            ("Kruskal", MazeGenerator.generate_kruskal)
        ]
        
        results = {}
        
        for size_name, (width, height) in enumerate(sizes):
            print(f"\n{'='*40}")
            print(f"测试迷宫尺寸: {width} x {height}")
            print(f"{'='*40}")
            
            size_results = []
            
            for algo_name, algo_func in algorithms:
                # 多次测试取平均值
                gen_times = []
                solve_times = []
                path_lengths = []
                
                for _ in range(3):  # 每个算法运行3次取平均
                    maze = Maze(width, height)
                    
                    # 生成迷宫
                    start_time = time.time()
                    algo_func(maze)
                    gen_time = time.time() - start_time
                    
                    # 求解迷宫
                    start_time = time.time()
                    success = MazeSolver.solve_bfs(maze)
                    solve_time = time.time() - start_time
                    
                    if success:
                        gen_times.append(gen_time)
                        solve_times.append(solve_time)
                        path_lengths.append(len(maze.path) - 1)
                
                # 计算平均值
                avg_gen = sum(gen_times) / len(gen_times) if gen_times else 0
                avg_solve = sum(solve_times) / len(solve_times) if solve_times else 0
                avg_path = sum(path_lengths) / len(path_lengths) if path_lengths else 0
                
                size_results.append({
                    'algorithm': algo_name,
                    'avg_generation_time': avg_gen,
                    'avg_solution_time': avg_solve,
                    'avg_path_length': avg_path
                })
                
                print(f"\n{algo_name}算法:")
                print(f"  平均生成时间: {avg_gen:.6f}秒")
                print(f"  平均求解时间: {avg_solve:.6f}秒")
                print(f"  平均路径长度: {avg_path:.1f}步")
                print(f"  总时间: {(avg_gen + avg_solve):.6f}秒")
            
            results[(width, height)] = size_results
        
        # 比较算法性能
        print(f"\n{'='*60}")
        print("算法性能比较:")
        print(f"{'='*60}")
        print(f"{'迷宫尺寸':<12} {'算法':<10} {'生成时间(秒)':<15} {'求解时间(秒)':<15} {'总时间(秒)':<15}")
        print("-" * 60)
        
        for size, size_results in results.items():
            for result in size_results:
                total_time = result['avg_generation_time'] + result['avg_solution_time']
                print(f"{f'{size[0]}x{size[1]}':<12} {result['algorithm']:<10} "
                      f"{result['avg_generation_time']:<15.6f} "
                      f"{result['avg_solution_time']:<15.6f} "
                      f"{total_time:<15.6f}")
        
        return results


def quick_test_random():
    """随机尺寸的快速测试"""
    # 随机生成迷宫尺寸（在合理范围内）
    min_size = 5
    max_size = 30
    
    # 可以随机选择几种模式
    modes = [
        "small",    # 小迷宫
        "medium",   # 中等迷宫  
        "large",    # 大迷宫
        "random",   # 完全随机
        "square",   # 方形迷宫
        "rectangular"  # 矩形迷宫
    ]
    
    mode = random.choice(modes)
    
    if mode == "small":
        width = random.randint(5, 10)
        height = random.randint(5, 10)
    elif mode == "medium":
        width = random.randint(10, 20)
        height = random.randint(10, 20)
    elif mode == "large":
        width = random.randint(20, 30)
        height = random.randint(20, 30)
    elif mode == "square":
        size = random.randint(5, 30)
        width = height = size
    elif mode == "rectangular":
        width = random.randint(8, 25)
        height = random.randint(5, 20)
        # 确保是矩形（宽高不同）
        while abs(width - height) < 3:
            width = random.randint(8, 25)
            height = random.randint(5, 20)
    else:  # random
        width = random.randint(min_size, max_size)
        height = random.randint(min_size, max_size)
    
    print(f"运行随机快速测试 - 模式: {mode}")
    print(f"迷宫尺寸: {width} x {height}")
    print("=" * 50)
    
    return quick_test_custom(width, height)


def quick_test_custom(width, height):
    """自定义尺寸的快速测试"""
    print(f"运行 {width}x{height} 迷宫测试...")
    
    # 验证尺寸在合理范围内
    if not (5 <= width <= 40 and 5 <= height <= 40):
        print(f"警告：尺寸 {width}x{height} 超出建议范围(5-40)，可能会影响性能")
    
    results = []
    
    algorithms = [
        ("DFS", MazeGenerator.generate_dfs),
        ("Kruskal", MazeGenerator.generate_kruskal)
    ]
    
    for algo_name, algo_func in algorithms:
        print(f"\n{'='*30}")
        print(f"{algo_name}算法测试:")
        print(f"{'='*30}")
        
        # 运行3次取平均值
        gen_times = []
        solve_times = []
        path_lengths = []
        
        for i in range(3):
            print(f"\n第 {i+1} 次运行:")
            maze = Maze(width, height)
            
            # 生成迷宫
            start_time = time.time()
            algo_func(maze)
            gen_time = time.time() - start_time
            
            # 求解迷宫
            start_time = time.time()
            success = MazeSolver.solve_bfs(maze)
            solve_time = time.time() - start_time
            
            if success:
                gen_times.append(gen_time)
                solve_times.append(solve_time)
                path_lengths.append(len(maze.path) - 1)
                
                print(f"  生成时间: {gen_time:.4f}秒")
                print(f"  求解时间: {solve_time:.4f}秒")
                print(f"  路径长度: {len(maze.path)-1}步")
            else:
                print("  求解失败!")
        
        if gen_times and solve_times:
            avg_gen = sum(gen_times) / len(gen_times)
            avg_solve = sum(solve_times) / len(solve_times)
            avg_path = sum(path_lengths) / len(path_lengths)
            
            results.append({
                'algorithm': algo_name,
                'avg_generation_time': avg_gen,
                'avg_solution_time': avg_solve,
                'avg_path_length': avg_path,
                'total_time': avg_gen + avg_solve
            })
            
            print(f"\n{algo_name}算法平均结果:")
            print(f"  平均生成时间: {avg_gen:.4f}秒")
            print(f"  平均求解时间: {avg_solve:.4f}秒")
            print(f"  平均路径长度: {avg_path:.1f}步")
            print(f"  平均总时间: {avg_gen + avg_solve:.4f}秒")
    
    # 比较两种算法
    if len(results) == 2:
        print(f"\n{'='*50}")
        print("算法性能比较:")
        print(f"{'='*50}")
        
        faster_algo = results[0] if results[0]['total_time'] < results[1]['total_time'] else results[1]
        slower_algo = results[1] if results[0]['total_time'] < results[1]['total_time'] else results[0]
        
        speedup = slower_algo['total_time'] / faster_algo['total_time'] if faster_algo['total_time'] > 0 else 0
        
        print(f"较快的算法: {faster_algo['algorithm']}")
        print(f"较慢的算法: {slower_algo['algorithm']}")
        print(f"速度提升: {speedup:.2f}倍")
        
        # 路径长度比较
        if results[0]['avg_path_length'] > 0 and results[1]['avg_path_length'] > 0:
            path_ratio = results[0]['avg_path_length'] / results[1]['avg_path_length']
            print(f"路径长度比 (DFS/Kruskal): {path_ratio:.2f}")
    
    print(f"\n{'='*50}")
    print(f"{width}x{height} 迷宫测试完成!")
    print(f"{'='*50}")
    
    return results


def run_all_tests():
    """运行所有测试"""
    print("开始运行迷宫生成与求解系统测试...")
    print("=" * 60)
    
    # 运行单元测试
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "=" * 60)
    print("单元测试完成")
    
    # 运行性能测试
    if result.wasSuccessful():
        print("\n开始性能测试...")
        print("=" * 60)
        
        try:
            performance_results = PerformanceTest.run_comprehensive_performance_test()
            print("\n性能测试完成!")
            
            # 保存性能测试结果到文件
            with open("performance_test_results.txt", "w") as f:
                f.write("迷宫生成与求解系统 - 性能测试报告\n")
                f.write("=" * 60 + "\n\n")
                
                for size, size_results in performance_results.items():
                    f.write(f"迷宫尺寸: {size[0]} x {size[1]}\n")
                    f.write("-" * 40 + "\n")
                    
                    for result in size_results:
                        total_time = result['avg_generation_time'] + result['avg_solution_time']
                        f.write(f"{result['algorithm']}算法:\n")
                        f.write(f"  平均生成时间: {result['avg_generation_time']:.6f}秒\n")
                        f.write(f"  平均求解时间: {result['avg_solution_time']:.6f}秒\n")
                        f.write(f"  平均路径长度: {result['avg_path_length']:.1f}步\n")
                        f.write(f"  总时间: {total_time:.6f}秒\n\n")
                    
                    f.write("\n")
                
                f.write("\n性能测试完成于: " + time.strftime("%Y-%m-%d %H:%M:%S") + "\n")
            
            print("性能测试结果已保存到: performance_test_results.txt")
            
        except Exception as e:
            print(f"性能测试出错: {e}")
    
    return result.wasSuccessful()


def stress_test():
    """压力测试 - 测试极端情况"""
    print("运行压力测试...")
    print("=" * 50)
    
    test_cases = [
        ("最小尺寸", 5, 5),
        ("最大建议尺寸", 40, 40),
        ("极端宽迷宫", 40, 10),
        ("极端高迷宫", 10, 40),
        ("非对称迷宫", 17, 23),
        ("方形大迷宫", 30, 30)
    ]
    
    for test_name, width, height in test_cases:
        print(f"\n测试: {test_name} ({width}x{height})")
        print("-" * 30)
        
        try:
            maze = Maze(width, height)
            
            # 测试DFS
            start = time.time()
            MazeGenerator.generate_dfs(maze)
            dfs_gen_time = time.time() - start
            
            start = time.time()
            success1 = MazeSolver.solve_bfs(maze)
            dfs_solve_time = time.time() - start
            
            # 测试Kruskal
            maze2 = Maze(width, height)
            start = time.time()
            MazeGenerator.generate_kruskal(maze2)
            kruskal_gen_time = time.time() - start
            
            start = time.time()
            success2 = MazeSolver.solve_bfs(maze2)
            kruskal_solve_time = time.time() - start
            
            if success1 and success2:
                print(f"  DFS: 生成{dfs_gen_time:.3f}s, 求解{dfs_solve_time:.3f}s")
                print(f"  Kruskal: 生成{kruskal_gen_time:.3f}s, 求解{kruskal_solve_time:.3f}s")
            else:
                print(f"  求解失败: DFS={success1}, Kruskal={success2}")
                
        except Exception as e:
            print(f"  错误: {e}")
    
    print(f"\n{'='*50}")
    print("压力测试完成!")
    print(f"{'='*50}")


def benchmark_test():
    """基准测试 - 运行多次随机测试"""
    print("运行基准测试（10次随机测试）...")
    print("=" * 50)
    
    all_results = []
    
    for i in range(10):
        print(f"\n第 {i+1}/10 次随机测试:")
        print("-" * 30)
        
        # 随机选择尺寸
        width = random.randint(8, 25)
        height = random.randint(8, 25)
        
        results = quick_test_custom(width, height)
        all_results.extend(results)
    
    # 汇总结果
    if all_results:
        print(f"\n{'='*50}")
        print("基准测试汇总:")
        print(f"{'='*50}")
        
        dfs_results = [r for r in all_results if r['algorithm'] == 'DFS']
        kruskal_results = [r for r in all_results if r['algorithm'] == 'Kruskal']
        
        if dfs_results:
            dfs_avg_gen = sum(r['avg_generation_time'] for r in dfs_results) / len(dfs_results)
            dfs_avg_solve = sum(r['avg_solution_time'] for r in dfs_results) / len(dfs_results)
            dfs_avg_total = sum(r['total_time'] for r in dfs_results) / len(dfs_results)
            
            print(f"DFS算法平均 (共{len(dfs_results)}次测试):")
            print(f"  平均生成时间: {dfs_avg_gen:.4f}秒")
            print(f"  平均求解时间: {dfs_avg_solve:.4f}秒")
            print(f"  平均总时间: {dfs_avg_total:.4f}秒")
        
        if kruskal_results:
            kruskal_avg_gen = sum(r['avg_generation_time'] for r in kruskal_results) / len(kruskal_results)
            kruskal_avg_solve = sum(r['avg_solution_time'] for r in kruskal_results) / len(kruskal_results)
            kruskal_avg_total = sum(r['total_time'] for r in kruskal_results) / len(kruskal_results)
            
            print(f"\nKruskal算法平均 (共{len(kruskal_results)}次测试):")
            print(f"  平均生成时间: {kruskal_avg_gen:.4f}秒")
            print(f"  平均求解时间: {kruskal_avg_solve:.4f}秒")
            print(f"  平均总时间: {kruskal_avg_total:.4f}秒")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="迷宫生成与求解系统测试工具")
    parser.add_argument("--mode", 
                       choices=["all", "quick", "performance", "custom", "random", "stress", "benchmark"], 
                       default="random",  # 默认改为random
                       help="""测试模式: 
                            all(全部测试), 
                            quick(快速测试-8x8), 
                            performance(性能测试),
                            custom(自定义尺寸),
                            random(随机尺寸-默认),
                            stress(压力测试),
                            benchmark(基准测试)""")
    parser.add_argument("--width", type=int, default=10, help="迷宫宽度（custom模式使用）")
    parser.add_argument("--height", type=int, default=10, help="迷宫高度（custom模式使用）")
    parser.add_argument("--seed", type=int, help="随机种子，用于重现随机测试")
    
    args = parser.parse_args()
    
    # 设置随机种子（如果提供了）
    if args.seed is not None:
        random.seed(args.seed)
        print(f"使用随机种子: {args.seed}")
    
    if args.mode == "all":
        success = run_all_tests()
        sys.exit(0 if success else 1)
    elif args.mode == "quick":
        # 保持原来的8x8快速测试
        print("运行8x8迷宫快速测试...")
        quick_test_custom(8, 8)
    elif args.mode == "performance":
        PerformanceTest.run_comprehensive_performance_test()
    elif args.mode == "custom":
        if not (5 <= args.width <= 40 and 5 <= args.height <= 40):
            print("错误：迷宫尺寸必须在5-40之间！")
            sys.exit(1)
        quick_test_custom(args.width, args.height)
    elif args.mode == "random":
        quick_test_random()
    elif args.mode == "stress":
        stress_test()
    elif args.mode == "benchmark":
        benchmark_test()
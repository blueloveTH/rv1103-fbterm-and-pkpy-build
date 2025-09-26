# 测试用工具

from array2d import array2d

def print_grid_debug(*args, **kwargs):
    return
    print_grid(*args, **kwargs)
    input("Press Enter to continue...")

def print_grid(grid: array2d[int], message="------------------------"):
# https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797
# Color Name	    Foreground Color Code	Background Color Code
# Black	            30	                    40
# Red	            31	                    41
# Green	            32	                    42
# Yellow	        33	                    43
# Blue	            34	                    44
# Magenta	        35	                    45
# Cyan	            36	                    46
# White	            37	                    47
# Default	        39	                    49
# Reset	            0	                    0
# Bright Black	    90	                    100
# Bright Red	    91	                    101
# Bright Green	    92	                    102
# Bright Yellow	    93	                    103
# Bright Blue	    94	                    104
# Bright Magenta	95	                    105
# Bright Cyan	    96	                    106
# Bright White	    97	                    107
    
    # (symbol, fg, bg)
    palette = {
        0: (". ", 37, 0),
        1: ("1 ", 30, 41),
        2: ("2 ", 30, 42),
        3: ("3 ", 30, 43),
        4: ("4 ", 30, 44),
        5: ("5 ", 30, 45),
        6: ("6 ", 30, 46),
        7: ("7 ", 30, 47),
        8: ("8 ", 30, 101),
        9: ("9 ", 30, 102),
        10: ("10", 30, 103),
        11: ("11", 30, 104),
        12: ("12", 30, 105),
        13: ("13", 30, 106),
        14: ("14", 30, 107)
    }
    
    max_value = max(palette.keys())-1
    
    print(message)
    for y in range(grid.height):
        for x in range(grid.width):
            value = grid[x, y]
    
            if value in palette:
                symbol, fg, bg = palette[value]
            else:
                remainder = (value % (max_value + 1))+1
                _, fg, bg = palette[remainder]
                symbol = str(value)  # Keep the number for printing
    
            data = f"\x1b[2;{fg};{bg}m"
            data += symbol
            data += "\x1b[0m"
            print(data, end="")
        print()
    
    # get non-zero count
    print("sparsity:", grid.count(0), "/", grid.numel)
from dungeon.brogue.levels import brogue_carveDungeon
from dungeon import test_tools
from dungeon.brogue.const import LevelProfile

grid, doors_list = brogue_carveDungeon(LevelProfile(5, 10))

test_tools.print_grid(grid)

print('doors:')
print(doors_list)
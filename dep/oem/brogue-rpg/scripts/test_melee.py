def print_grid(r):
    # 'P': player
    # '#': valid cell
    for y in range(-3, 3+1):
        line = []
        for x in range(-3, 3+1):
            if x == 0 and y == 0:
                line.append('P')
            elif (x**2 + y**2) <= r**2 and x>0:
                line.append('#')
            else:
                line.append('.')
        print(''.join(line))


for r in [1.0, 1.5, 2.0, 2.5, 3.0]:
    print(f"==> r={r}")
    print_grid(r)
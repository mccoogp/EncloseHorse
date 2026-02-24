
import pygame
from collections import deque
import time
import random
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
pygame.init()

TILE = 50
FONT = pygame.font.SysFont(None, 28)

rows, cols = 9, 9
horse = [4,4]

grid = [['o' for _ in range(cols)] for _ in range(rows)]
grid[horse[0]][horse[1]] = 'H'

mode = "EDIT"
show_path = False


colors = {
    'o': (240,240,240),
    'w': (100,100,100),
    'x': (0,120,255),
    'H': (255,100,100),
    'p': (150,255,150)
}

cycle = {'o':'x','x':'o'}

def resize(new_r, new_c):
    global rows, cols, grid, horse
    rows, cols = max(3,new_r), max(3,new_c)
    grid = [['o' for _ in range(cols)] for _ in range(rows)]
    horse[:] = [rows//2, cols//2]
    grid[horse[0]][horse[1]] = 'H'

def find_path(grid_copy):
    visited = set()
    q = deque()
    q.append(tuple(horse))
    parent = {}
    visited.add(tuple(horse))

    while q:
        r,c = q.popleft()
        if r==0 or c==0 or r==rows-1 or c==cols-1:
            path = []
            while (r,c)!=tuple(horse):
                path.append((r,c))
                r,c = parent[(r,c)]
            return (False, path)

        for dr,dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr,nc = r+dr,c+dc
            if 0<=nr<rows and 0<=nc<cols:
                if (nr,nc) not in visited and grid_copy[nr][nc]=='o':
                    visited.add((nr,nc))
                    parent[(nr,nc)] = (r,c)
                    q.append((nr,nc))
    return (True, visited)

def draw_button(text, x, y, w, h):
    rect = pygame.Rect(x,y,w,h)
    pygame.draw.rect(screen,(200,200,200),rect)
    pygame.draw.rect(screen,(0,0,0),rect,2)
    screen.blit(FONT.render(text,True,(0,0,0)),(x+10,y+8))
    return rect



screen = pygame.display.set_mode((1000,800))
pygame.display.set_caption("Horse Escape")

grid =[['x', 'x', 'o', 'o', 'o', 'o', 'o', 'o', 'x'],
['o', 'o', 'o', 'o', 'x', 'o', 'o', 'x', 'o'],
['o', 'o', 'o', 'o', 'o', 'o', 'x', 'x', 'o'],
['o', 'o', 'o', 'o', 'o', 'o', 'o', 'x', 'o'],
['o', 'x', 'o', 'o', 'H', 'o', 'o', 'o', 'o'],
['x', 'x', 'o', 'o', 'o', 'o', 'o', 'o', 'o'],
['o', 'o', 'o', 'o', 'o', 'o', 'o', 'x', 'o'],
['o', 'x', 'o', 'o', 'x', 'o', 'o', 'o', 'o'],
['o', 'o', 'o', 'x', 'x', 'x', 'o', 'o', 'o']]
def showtest(grid, secs):
    path_tiles = set()
    running = True
    path = find_path(grid)
    if path[0]:
        #print(path[1])
        score = len(path[1])
    else:
        path_tiles = set(find_path(grid)[1])
        score = 0
    mode = "PLAY"
    start = time.time()
    while time.time()-start < secs:
        screen.fill((220,220,220))
        board_w = cols*TILE
        board_h = rows*TILE

        for r in range(rows):
            for c in range(cols):
                tile = grid[r][c]
                if (r,c) in path_tiles:
                    tile = 'p'
                rect = pygame.Rect(c*TILE, r*TILE, TILE, TILE)
                pygame.draw.rect(screen, colors[tile], rect)
                pygame.draw.rect(screen,(0,0,0),rect,2)

        # Buttons
        score_btn = draw_button("Score: " + str(score), board_w+20, 20, 120, 40)

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False

            if event.type==pygame.MOUSEBUTTONDOWN:
                mx,my = event.pos
        pygame.display.flip()
showtest(grid, 2)

def random_start(grid, n):
    walls = []
    run = True
    while run:
        test = (random.randint(0,len(grid)-1), random.randint(0,len(grid[0])-1))
        if grid[test[0]][test[1]] == 'o' and test not in walls: 
            walls.append(test)
            if len(walls) == n:
                run = False
    return walls
def walls_to_grid(grid_copy, walls):
    new_grid = [row[:] for row in grid_copy]
    for wall in walls:
        new_grid[wall[0]][wall[1]] = 'w'
    return new_grid
def get_score(walls):
    
    path = find_path(walls_to_grid(grid, walls))
    if path[0]:
        #print(path[1])
        score = len(path[1])
    else:
        score = 0
    return score
def mutate(walls, rate):
    newwalls = []
    random.shuffle(walls)
    for wall in walls:
        mut = random.randint(0,rate)
        if mut == 0:
            direction = random.choice(["Up", "Down", "Left","Right"])
            if direction == "Up" and wall[0] > 0:
                if grid[wall[0]-1][wall[1]] == "o" and (wall[0]-1, wall[1]) not in walls:
                    newwalls.append((wall[0]-1, wall[1]))
                else:
                    newwalls.append(wall)
            elif direction == "Down" and wall[0] < len(grid)-1:
                if grid[wall[0]+1][wall[1]] == "o" and (wall[0]+1, wall[1]) not in walls:
                    newwalls.append((wall[0]+1, wall[1]))
                else:
                    newwalls.append(wall)
            elif direction == "Left" and wall[1] > 0:
                if grid[wall[0]][wall[1]-1] == "o" and (wall[0], wall[1]-1) not in walls:
                    newwalls.append((wall[0], wall[1]-1))
                else:
                    newwalls.append(wall)
            elif direction == "Right" and wall[1] < len(grid[0])-1:
                if grid[wall[0]][wall[1]+1] == "o" and (wall[0], wall[1]+1) not in walls:
                    newwalls.append((wall[0], wall[1]+1))
                else:
                    newwalls.append(wall)
            else:
                newwalls.append(wall)
        else:
            newwalls.append(wall)
        
    return newwalls

def random_move(walls):
    random.shuffle(walls)
    new_walls = walls[:len(walls)-1]
    run = True
    while run:
        test = (random.randint(0,len(grid)-1), random.randint(0,len(grid[0])-1))
        if grid[test[0]][test[1]] == 'o' and test not in walls: 
            new_walls.append(test)
            run = False
    return new_walls

def sex(walls1, walls2, rate):
    new_walls = []
    run = True
    tries = 0
    while run and tries < 100:
        tries+=1
        n = random.randint(0,1)
        if n == 0:
            test = random.choice(walls1)
            if test not in new_walls:
                new_walls.append(test)
                if len(new_walls) == 9:
                    run = False
        else:
            test = random.choice(walls2)
            if test not in new_walls:
                new_walls.append(test)
                if len(new_walls) == 9:
                    run = False
    if tries == 100:
        return mutate(walls1, rate)
    return mutate(new_walls, rate)

asex_results = []
sex_results = []
lengths = [30,60,90,120,150]
for length in [150]:
    pools = [[random_start(grid, 9) for i in range(500)] for i in range(50)]
    start = time.time()
    while time.time() - start < length:
        for rate in range(10):
            new_pools = []
            for pool in pools:
                oldpool = pool.copy()
                newpool = []
                for walls in oldpool:
                    newpool.append(mutate(walls, rate))
                pool = newpool + oldpool[:10]
                pool.sort(key = get_score, reverse= True)
                pool = pool[:200]
                new_pools.append(pool)
            pools = new_pools
        

        print([get_score(pool[0]) for pool in pools])
        print(start -time.time())


        for pool in pools:
            oldpool = pool.copy()
            newpool = []
            for walls in oldpool:
                newpool.append(random_move(mutate(walls, 3)))
            #print("here")
            pool = newpool + oldpool[:1]
            random.shuffle(pool)
            pool.sort(key = get_score, reverse= True)
            pool = pool[:200]
        if time.time() - start > lengths[len(asex_results)]:
            print("\n\n BEST", sum([get_score(pool[0]) for pool in pools]))
            best = [get_score(pool[0]) for pool in pools]
            print([get_score(pool[0]) for pool in pools], "\n\n\n")
            
            asex_results.append(best)

    pools = [[random_start(grid, 9) for i in range(500)] for i in range(50)]
    start = time.time()
    while time.time() - start < length:
        for rate in range(10):
            new_pools = []
            for pool in pools:
                oldpool = pool.copy()
                newpool = []
                for walls in oldpool:
                    mate = random.choice(oldpool)
                    newpool.append(sex(walls, mate, rate))
                    #print(walls, mate)
                    
                pool = newpool + oldpool[:100]
                pool.sort(key = get_score, reverse= True)
                pool = pool[:200]
                new_pools.append(pool)
            pools = new_pools
        print(start - time.time())
        print([get_score(pool[0]) for pool in pools])
        if time.time() - start > lengths[len(sex_results)]:
            print("\n\n BEST", sum([get_score(pool[0]) for pool in pools]))
            best = [get_score(pool[0]) for pool in pools]
            best.sort(reverse= True)
            print([get_score(pool[0]) for pool in pools], "\n\n\n")
            sex_results.append(best)

totals = asex_results + sex_results
xs = []
ys = []
for length in range(len(asex_results)):
    for result in asex_results[length]:
        xs.append(str(lengths[length]) + " asex")
        ys.append(result)
for length in range(len(sex_results)):
    for result in sex_results[length]:
        xs.append(str(lengths[length]) + " sex")
        ys.append(result)


data = {"x": xs, "y" : ys}
df = pd.DataFrame(data)
print(df)
plot = sns.boxplot(x="x", y="y", data=df)
#plot.set_xticklabels([f"Owned->Owned {len(df[(df['chngehom'] == 1)])}",f"Rent->Owned {len(df[(df['chngehom'] == 2)])}",f"Owned->Rent {len(df[(df['chngehom'] == 3)])}",f"Rent->Rent {len(df[(df['chngehom'] == 4)])}"])
plot.tick_params(axis='x', labelsize=7)
plt.xlabel('Time + Method')
plt.ylabel('Scores')
plt.title("Asexual vs Sexual Mutation in Horse Game") 

plt.show()







import pygame
from collections import deque
import time
import random
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
    'p': (150,255,150),
    'g' : (255, 235, 180)
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



screen = pygame.display.set_mode((1200,800))
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
    pen = set()
    running = True
    path = find_path(grid)
    if path[0]:
        score = len(path[1])
        pen = set(path[1])
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
                if (r,c) in pen:
                    tile = 'g'
                
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
def showtest_double(grid1, grid2, secs, label1, label2):
    path_tiles1 = set()
    path1 = find_path(grid1)
    pen1 = set()
    if path1[0]:
        score1 = len(path1[1])
        pen1 = set(path1[1])
    else:
        path_tiles1 = set(path1[1])
        score1 = 0
    path_tiles2 = set()
    path2 = find_path(grid2)
    pen2 = set()
    if path1[0]:
        score2 = len(path2[1])
        pen2 = set(path2[1])
    else:
        path_tiles2 = set(path2[1])
        score2 = 0
    start = time.time()
    while time.time()-start < secs:
        screen.fill((220,220,220))
        board_w = cols*TILE
        board_h = rows*TILE

        for r in range(rows):
            for c in range(cols):
                tile = grid1[r][c]
                if (r,c) in path_tiles1:
                    tile = 'p'
                if (r,c) in pen1 and tile != 'H':
                    tile = 'g'
                rect = pygame.Rect(c*TILE, r*TILE, TILE, TILE)
                pygame.draw.rect(screen, colors[tile], rect)
                pygame.draw.rect(screen,(0,0,0),rect,2)

                tile = grid2[r][c]
                if (r,c) in path_tiles2:
                    tile = 'p'
                if (r,c) in pen2 and tile != 'H':
                    tile = 'g'
                rect = pygame.Rect(c*TILE + board_w + 200, r*TILE, TILE, TILE)
                pygame.draw.rect(screen, colors[tile], rect)
                pygame.draw.rect(screen,(0,0,0),rect,2)

        # Buttons
        score_btn = draw_button(label1 + " " + str(score1), board_w+20, 20, 160, 40)
        score_btn = draw_button(label2 + " " + str(score2), board_w+20, 80, 160, 40)

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

while True:
    pools = [[random_start(grid, 9) for i in range(500)] for i in range(1)]
    start = time.time()
    pools2 = [[random_start(grid, 9) for i in range(500)] for i in range(1)]
    asextime = 0
    sextime = 0
    bests = [0,0]
    while time.time() - start < 30 and bests != [29,29]:
        for i in range(10):
            for rate in range(10):
                starting = time.time()
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
                asextime += time.time() - starting

                starting = time.time()
                new_pools = []
                for pool in pools2:
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
                pools2 = new_pools
                sextime += time.time() - starting
            



            best = [pool[0] for pool in pools]
            best.sort(key = get_score, reverse= True)
            bests[0] = get_score(best[0])

            
            best2 = [pool[0] for pool in pools2]
            best2.sort(key = get_score, reverse= True)
            bests[1] = get_score(best2[0])
            showtest_double(walls_to_grid(grid, best2[0]), walls_to_grid(grid, best[0]), 0.1, "Asex: " + str(round(asextime, ndigits=1)) + " -", "Sex: " + str(round(sextime, ndigits=1)) + " -")

            starting = time.time()
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
            asextime += time.time() - starting

            starting = time.time()
            for pool in pools2:
                oldpool = pool.copy()
                newpool = []
                for walls in oldpool:
                    newpool.append(random_move(mutate(walls, 3)))
                #print("here")
                pool = newpool + oldpool[:1]
                random.shuffle(pool)
                pool.sort(key = get_score, reverse= True)
                pool = pool[:200]
            sextime += time.time() - starting

            print(start -time.time(), asextime, sextime)
            print(bests)

    print("\n\n BEST", sum([get_score(pool[0]) for pool in pools]))
    best = [pool[0] for pool in pools]
    best.sort(key = get_score, reverse= True)
    print([get_score(pool[0]) for pool in pools], "\n\n\n")

    print("\n\n BEST", sum([get_score(pool[0]) for pool in pools2]))
    best = [pool[0] for pool in pools2]
    best.sort(key = get_score, reverse= True)
    print([get_score(pool[0]) for pool in pools2], "\n\n\n")
    time.sleep(0.5)

pygame.quit()

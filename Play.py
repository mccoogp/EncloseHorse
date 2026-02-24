import pygame
from collections import deque

pygame.init()

TILE = 50
FONT = pygame.font.SysFont(None, 28)

rows, cols = 9, 9
horse = [4,4]

grid = [['o' for _ in range(cols)] for _ in range(rows)]
grid[horse[0]][horse[1]] = 'H'

mode = "EDIT"
show_path = False
path_tiles = set()

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

def find_path():
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
                if (nr,nc) not in visited and grid[nr][nc]=='o':
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

running=True
drag_horse=False
score = 0
while running:
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
    mode_btn = draw_button(mode, board_w+20, 20, 120, 40)
    path_btn = draw_button("Show Path", board_w+20, 80, 120, 40)
    plus_btn = draw_button("+", board_w+20, 140, 50, 40)
    minus_btn = draw_button("-", board_w+90, 140, 50, 40)
    plus2_btn = draw_button("+", board_w+20, 200, 50, 40)
    minus2_btn = draw_button("-", board_w+90, 200, 50, 40)
    score_btn = draw_button("Score: " + str(score), board_w+20, 260, 120, 40)

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False

        if event.type==pygame.MOUSEBUTTONDOWN:
            mx,my = event.pos
            path_tiles.clear()

            if mode_btn.collidepoint(mx,my):
                mode = "PLAY" if mode=="EDIT" else "EDIT"

            elif path_btn.collidepoint(mx,my) and mode=="PLAY":
                path = find_path()
                if path[0]:
                    print(path[1])
                    score = len(path[1])
                else:
                    path_tiles = set(find_path()[1])
                    score = 0

            elif plus_btn.collidepoint(mx,my) and mode=="EDIT":
                resize(rows+1, cols)

            elif minus_btn.collidepoint(mx,my) and mode=="EDIT":
                resize(rows-1, cols)

            elif plus2_btn.collidepoint(mx,my) and mode=="EDIT":
                resize(rows, cols+1)

            elif minus2_btn.collidepoint(mx,my) and mode=="EDIT":
                resize(rows, cols-1)

            elif mx < board_w and my < board_h:
                r = my//TILE
                c = mx//TILE

                if grid[r][c]=='H' and mode=="EDIT":
                    drag_horse=True

                else:
                    if mode=="EDIT":
                        if grid[r][c] != 'H':
                            grid[r][c] = cycle[grid[r][c]]
                    else:
                        if grid[r][c]=='o':
                            grid[r][c]='w'
                        elif grid[r][c]=='w':
                            grid[r][c]='o'

        if event.type==pygame.MOUSEBUTTONUP:
            if drag_horse:
                mx,my = event.pos
                if mx<board_w and my<board_h:
                    r=my//TILE
                    c=mx//TILE
                    grid[horse[0]][horse[1]]='o'
                    horse[:] = [r,c]
                    grid[r][c]='H'
                drag_horse=False

    pygame.display.flip()
for line in grid:
    print(line)

pygame.quit()
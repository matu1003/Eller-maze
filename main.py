from random import randint
from math import floor
import pygame
import csv

WIN_W = 1400
WIN_H = 800
x = 120
if x%2 == 0:
    x+=1
if x < 5:
    x = 5



cell_size = WIN_W//x
y = WIN_H//cell_size
if y%2 == 0:
    y-= 1
y -= 2
win = pygame.display.set_mode((WIN_W, WIN_H))
win.fill((0,0,0))





def draw_grid(grid):
    for ypoint in range(len(grid)):
        for xpoint in range(len(grid[0])):
            cell = pygame.Surface((cell_size, cell_size))
            if grid[ypoint][xpoint] == 0:
                cell.fill((255,255,255))
            else:
                cell.fill((0,0,0))
            win.blit(cell, ((xpoint*cell_size, ypoint*cell_size)))

def join_row(row, set_vals, last=False):
    for cell in range(2, len(row)-2, 2):
        poll = randint(0,1)
        if (poll or last) and set_vals[int((cell)/2)] != set_vals[int((cell)/2-1)]:
            row[cell] = 0
            parent = set_vals[int((cell)/2)]
            child = set_vals[int((cell)/2-1)]
            for val in range(len(set_vals)):
                if set_vals[val] == child:
                    set_vals[val] = parent

def gen_next_sep(row, set_vals):
    new_row = [1 for i in range(x)]
    sets = list(set(set_vals))
    for set_val in sets:
        murs = [i*2+1 for i in range(len(set_vals)) if set_vals[i] == set_val]
        if len(murs) == 1:
            new_row[murs[0]] = 0
        else:
            mur_choisis = randint(0,len(murs)-1)
            new_row[murs[mur_choisis]] = 0
            for mur in range(len(murs)):
                choix = randint(0,1)
                if choix:
                    new_row[murs[mur]] = 0
    return new_row


def gen_next_line(row, set_vals, sep):
    global set_count
    new_row = [1 if i%2==0 else 0 for i in range(x)]
    new_sets = [None for i in range(floor(x/2))]
    for cell in range(1, x, 2):
        if sep[cell] == 0:
            new_sets[int(cell/2)] = set_vals[int(cell/2)]
        else:
            new_sets[int(cell/2)] = set_count
            set_count += 1
    return new_row, new_sets

grid = [[1 for _ in range(x)]]
sets = []
firstrow = [1 if i%2==0 else 0 for i in range(x)]
set_count = 0 #Noting every set number already used
firstset = [i for i in range(set_count, set_count+floor(x/2))]
set_count += len(firstset)
join_row(firstrow, firstset)
grid.append(firstrow)

new_sep = gen_next_sep(firstrow, firstset)
grid.append(new_sep)
next_row, next_sets = gen_next_line(firstrow, firstset, new_sep)
join_row(next_row, next_sets)
grid.append(next_row)
lines = 3
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    draw_grid(grid)
    pygame.display.update()

    if lines < y:
        new_sep = gen_next_sep(next_row, next_sets)
        grid.append(new_sep)
        next_row, next_sets = gen_next_line(next_row, next_sets, new_sep)
        if lines == y-2:
            join_row(next_row, next_sets, True)
        else:
            join_row(next_row, next_sets)
        grid.append(next_row)
        lines += 2

    if lines == y:
        grid.append([1 for i in range(x)])
        with open("Lab.csv", mode="w") as file:
                writer = csv.writer(file)
                for row in grid:
                    writer.writerow(row)
        lines += 1

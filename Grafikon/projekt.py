import pygame as pg
import sys, os, time, random, math, json

def drawStatistics(data, x, y, key):
    width = 400
    height = 200
    pg.draw.line(screen, (255, 255, 255), (x, y-30), (x + width, y-30), 3)
    pg.draw.line(screen, (255, 255, 255), (x+30, y), (x+30, y - 30 - height), 3)
    cols = len(data)
    for i in range(1, cols):
        pg.draw.line(screen, (150, 150, 150), (x + 30 + i * width / cols, y - 30), (x + 30 + i * width / cols, y - 30 - height), 1)
    values = []
    for i in range(1, cols):
        values.append(data[i][key])

    maxvalue = max(values)
    minvalue = min(values)
    dots = []
    for i in range(1, cols):
        dot = (x + 30 + i * width / cols, y - 30 - int((values[i-1] - minvalue) / (maxvalue - minvalue) * height))
        pg.draw.circle(screen, (255, 255, 255), dot, 5)
        dots.append(dot)
    for i in range(1, len(dots)):
        pg.draw.line(screen, (255, 255, 255), dots[i-1], dots[i], 2)

    print(values)


file = open("adatok.json", "r")
adatok = json.load(file)["egyutt"]
file.close()

# Képernyő beállítások
pg.init()
pg.display.set_caption("Projekt")
screen = pg.display.set_mode((1200, 800))
w, h = size = pg.display.get_surface().get_size()
clock = pg.time.Clock()

# szöveg
titlefont = pg.font.SysFont("Arial", 36)
font = pg.font.SysFont("Arial", 24)
title = titlefont.render("statisztika kiíró cucc idk", True, (255, 255, 255))
title_rect = title.get_rect(center=(w/2, h/2-200))
opt1 = font.render("Kiírás", True, (255, 255, 255))
opt1_rect = opt1.get_rect(center=(w/2, h/2-100))


while True:
    screen.fill((0, 0, 0))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    screen.blit(title, title_rect)
    screen.blit(opt1, opt1_rect)

    keyinput = input("Adj meg egy kulcsot: ")
    drawStatistics(adatok, 200, h-200, keyinput)

    clock.tick(60)
    pg.display.flip()

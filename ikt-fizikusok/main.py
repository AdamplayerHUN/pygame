import pygame as pg
import sys
import random
import time
import os
import json

# Képernyő beállítása
pg.init()
screen = pg.display.set_mode((600, 800))
surface = pg.display.get_surface()
w, h = size = surface.get_width(), surface.get_height()
pg.display.set_caption("Ikt-Fizikusok")
clock = pg.time.Clock()

# Feliratok
titlefont = pg.font.Font(None, 72)
font = pg.font.Font(None, 36)
smallfont = pg.font.Font(None, 24)
title = titlefont.render("Ikt-Fizikusok", True, (255, 255, 255))
title_rect = title.get_rect(center=(w/2, h/2-300))
option1 = font.render("Adatok betöltése", True, (255, 255, 255))
option1_rect = option1.get_rect(center=(w/2, h/2-200))
option2 = font.render("Adatok megjelenítése", True, (255, 255, 255))
option2_rect = option2.get_rect(center=(w/2, h/2-150))
option3 = font.render("Keresés a fájlban", True, (255, 255, 255))
option3_rect = option3.get_rect(center=(w/2, h/2-100))

loadtitle = font.render("Adatok betöltése fájlból...", True, (255, 255, 255))
loadtitle_rect = loadtitle.get_rect(center=(w/2, h/2-300))
pwd = os.getcwd()
folder = font.render("Betöltési mappa: "+pwd, True, (255, 255, 255))
folder_rect = folder.get_rect(center=(w/2, h/2-250))
userinput = ""
usertext = font.render("Fájlnév: "+userinput, True, (255, 255, 255))
usertext_rect = usertext.get_rect(center=(w/2-200, h/2-200))
loaded = font.render("Fájl betöltve!", True, (255, 255, 255))
loaded_rect = loaded.get_rect(center=(w/2, h/2+50))
notfound = font.render("Nem található a fájl!", True, (255, 255, 255))
notfound_rect = notfound.get_rect(center=(w/2, h/2+50))
notloaded = font.render("Nincs betöltött fájl!", True, (255, 255, 255))
notloaded_rect = notloaded.get_rect(center=(w/2, h/2+50))
formaterror = font.render("Nem megfelelő fájlformátum!", True, (255, 255, 255))
formaterror_rect = formaterror.get_rect(center=(w/2, h/2+50))
back = font.render("Vissza", True, (255, 255, 255))
back_rect = back.get_rect(center=(w/2, h-50))

col1 = font.render("Elem", True, (255, 255, 255))
col1_rect = col1.get_rect(center=(w/4, 30))
col2 = font.render("Név", True, (255, 255, 255))
col2_rect = col2.get_rect(center=(w/2, 30))
col3 = font.render("Születési év", True, (255, 255, 255))
col3_rect = col3.get_rect(center=(3*w/4, 30))

searchtitle = font.render("Írja be a keresni kívánt adatot", True, (255, 255, 255))
searchtitle_rect = searchtitle.get_rect(center=(w/2, h/2-300))


# Program változók
menu = True
load = False
printitems = False
search = False
tryLoad = False
loadedfile = False
rects = []
desc = False
printdescnum = 0
cont = False
printdesc = False

# Képek betöltése


# Hangok betöltése



# Függvények



# Játék ciklus
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
                pg.quit()
                sys.exit()
            if load and len(userinput) < 30 and event.key != pg.K_RETURN:
                if event.key == pg.K_BACKSPACE:
                    userinput = userinput[:-1]
                else:
                    userinput += event.unicode
                usertext = font.render("Fájlnév: "+userinput, True, (255, 255, 255))
            if load and event.key == pg.K_RETURN:
                tryLoad = True
            if search and len(searchinput) < 30 and event.key != pg.K_RETURN:
                if event.key == pg.K_BACKSPACE:
                    searchinput = searchinput[:-1]
                else:
                    searchinput += event.unicode
                searchtext = font.render("Keresés: "+searchinput, True, (255, 255, 255))
        if event.type == pg.MOUSEBUTTONDOWN:
            if option1_rect.collidepoint(event.pos) and menu:
                load = True
                menu = False
            if option2_rect.collidepoint(event.pos) and menu:
                screen.fill((0, 0, 0))
                printitems = True
                menu = False
            if option3_rect.collidepoint(event.pos) and menu:
                search = True
                menu = False
            elif printitems and loadedfile and not desc and cont:
                for rect in rects:
                    if rect[0].collidepoint(event.pos) or rect[1].collidepoint(event.pos) or rect[2].collidepoint(event.pos):
                        print("Kattintás!")
                        printdescnum = rect[0][1]/23-5
                        desc = True    
            if load or printitems or search:
                if back_rect.collidepoint(event.pos):
                    load = False
                    printitems = False
                    search = False
                    printdesc = False
                    menu = True
                    userinput = ""
                    searchinput = ""
            

    # Program logika


    # Rajzolás
    if not printitems:
        screen.fill((0, 0, 0))
    if menu:
        screen.blit(title, title_rect)
        screen.blit(option1, option1_rect)
        screen.blit(option2, option2_rect)
        screen.blit(option3, option3_rect)

    if load:
        screen.blit(loadtitle, loadtitle_rect)
        screen.blit(usertext, usertext_rect)
        screen.blit(folder, folder_rect)
        screen.blit(back, back_rect)
        if userinput.split(".")[-1] != "json":
                screen.blit(formaterror, formaterror_rect)
                pg.display.flip()
                time.sleep(2)
                tryLoad = False
                load = True
                menu = False
        if tryLoad:
            try:
                file = open(userinput, "r")
                data = json.load(file)
                screen.blit(loaded, loaded_rect)
                pg.display.flip()
                time.sleep(2)
                load = False
                menu = True
                tryLoad = False
                loadedfile = True
            except FileNotFoundError:
                screen.blit(notfound, notfound_rect)
                pg.display.flip()
        
    if printitems and loadedfile:
        time.sleep(0.1)
        rects = []
        screen.blit(col1, col1_rect)
        screen.blit(col2, col2_rect)
        screen.blit(col3, col3_rect)
        currentline = 0
        for item in data["fizikusok"]:
            name = item["Név"]
            birth = item["Születési idő"]
            currentline += 1
            linepixel = currentline*23
            nametext = smallfont.render(str(currentline), True, (255, 255, 255))
            nametext_rect = nametext.get_rect(center=(w/4, 100+linepixel))
            birthtext = smallfont.render(name, True, (255, 255, 255))
            birthtext_rect = birthtext.get_rect(center=(w/2, 100+linepixel))
            desctext = smallfont.render(birth, True, (255, 255, 255))
            desctext_rect = desctext.get_rect(center=(3*w/4, 100+linepixel))
            rects.append((nametext_rect, birthtext_rect, desctext_rect))
            screen.blit(nametext, nametext_rect)
            screen.blit(birthtext, birthtext_rect)
            screen.blit(desctext, desctext_rect)

        screen.blit(back, back_rect)
        cont = True

    elif printitems and not loadedfile:
        screen.blit(notloaded, notloaded_rect)
        pg.display.flip()
        time.sleep(2)
        printitems = False
        menu = True

    if desc:
        splittext = []
        wordnum = 0
        splitted = 0
        activetext = data["fizikusok"][int(printdescnum)]["Leírás"].split(" ")
        for item in activetext:
            wordnum += 1
            if wordnum % 6 == 0:
                splitted += 1
                beforeindex = 6*(splitted-1)
                index = 6*splitted
                splittext.append(activetext[beforeindex:index])
                wordnum = 0
        print("splittext: " + str(data["fizikusok"][int(printdescnum)]["Név"]))
        desc = False
        printdesc = True
    
    if printdesc:
        formatedtext = []
        for item in splittext:
            formatedtext.append(" ".join(item))
        screen.fill((0, 0, 0))
        currentline = 0
        for item in formatedtext:
            currentline += 1
            linepixel = currentline*23
            text = smallfont.render(item, True, (255, 255, 255))
            text_rect = text.get_rect(center=(w/2, 100+linepixel))
            screen.blit(text, text_rect)
        screen.blit(back, back_rect)

    if not menu and not load and not printitems and not search:
        screen.blit(font.render("Valami hiba történt!", True, (255, 255, 255)), (w/2, h/2))

    if search:
        screen.blit(back, back_rect)
        screen.blit(searchtitle, searchtitle_rect)

    # Képernyő frissítése
    pg.display.flip()
    clock.tick(10)

import pygame as pg, time, os, random, sys, math, json, pygame.mixer as mixer

def getClosestEnemy():
    closest = 9999999999999999
    if len(enemies) > 0:
        for enemy in enemies:
            distance = enemy.playerdistance
            if distance < closest:
                closest = distance
                target = enemy
        return target
    else:
        return None

def reset():
    currentframe = 0
    showshipattack = False
    player.x = 0
    player.y = 0
    player.dx = 0
    player.dy = 0
    player.angle = 0
    if player.type == 1:
        player.shield = {
            "topleft":[100, (0, 255, 0)],
            "top":[100, (0, 255, 0)],
            "topright":[100, (0, 255, 0)],
            "left":[100, (0, 255, 0)],
            "right":[100, (0, 255, 0)],
            "bottomleft":[100, (0, 255, 0)],
            "bottom":[100, (0, 255, 0)],
            "bottomright":[100, (0, 255, 0)]
        }
        player.health = 100
        player.modules = {
            "weapon1":100,
            "weapon2":100,
            "generator":100,
            "shieldmodule":100,
            "engine":100,
            "radar":100,
            "fueltank":100
            }
    elif player.type == 2:
        player.shield = {
            "topleft":[300, (0, 255, 0)],
            "top":[300, (0, 255, 0)],
            "topright":[300, (0, 255, 0)],
            "left":[300, (0, 255, 0)],
            "right":[300, (0, 255, 0)],
            "bottomleft":[300, (0, 255, 0)],
            "bottom":[300, (0, 255, 0)],
            "bottomright":[300, (0, 255, 0)]
        }
        player.health = 500
        player.modules = {
            "weapon1":300,
            "weapon2":300,
            "generator":300,
            "shieldmodule":300,
            "engine":300,
            "radar":300,
            "fueltank":300
        }
    enemies = [Enemy(random.randint(-2000, 2000), random.randint(-2000, 2000), random.randint(-2, 2), random.randint(-2, 2), random.randint(0, 360), 1)]
    player.rotatespeed = 0
    weapon1charge = 100
    weapon2charge = 100

    return enemies, weapon1charge, weapon2charge

def invertImg(img):
    img.lock()

    for x in range(img.get_width()):
        for y in range(img.get_height()):
            RGBA = img.get_at((x,y))
            for i in range(3):
                # Invert RGB, but not Alpha
                RGBA[i] = 255 - RGBA[i]
            img.set_at((x,y),RGBA)

    img.unlock()

pg.init()
mixer.init()
screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
surface = pg.display.get_surface()
w, h = size = surface.get_width(), surface.get_height()
pg.display.set_caption("Spaceshooter")
clock = pg.time.Clock()

# Load images
ship01 = pg.image.load("assets/img/ship-01.png").convert()
ship01.set_colorkey((0, 0, 0))
shipms = pg.image.load("assets/img/ship-ms.png").convert()
shipms.set_colorkey((0, 0, 0))


explosion = pg.image.load("assets/img/explosion.png")
explosion = pg.transform.scale(explosion, (200, 200))

selectedweapon = 1

font = pg.font.SysFont("Roboto", 40)
bigfont = pg.font.SysFont("Roboto", 80)
titlefont = pg.font.SysFont("Roboto", 120)
weaponpaneltext = font.render("WEAPONS", True, (200, 200, 200))
weaponpaneltext_rect = weaponpaneltext.get_rect(topleft=(w-100-weaponpaneltext.get_width()/2, h-300))

weapon1charge = 100

if selectedweapon == 1:
    weapon1text = font.render("Burst", True, (255, 50, 50))
    weapon1chargelabel = font.render(f"{weapon1charge}%", True, (200, 200, 200))
else:
    weapon1text = font.render("Burst", True, (200, 200, 200))
weapon1text_rect = weapon1text.get_rect(topleft=(w-180, h-225))

weapon1chargelabel_rect = weapon1chargelabel.get_rect(topleft=(w-weapon1chargelabel.get_width()-30, h-225))

weapon2charge = 100

if selectedweapon == 2:
    weapon2text = font.render("Laser", True, (255, 50, 50))
    weapon2chargelabel = font.render(f"{weapon2charge}%", True, (255, 50, 50))

else:
    weapon2text = font.render("Laser", True, (200, 200, 200))
    weapon2chargelabel = font.render(f"{weapon2charge}%", True, (200, 200, 200))

weapon2text_rect = weapon2text.get_rect(topleft=(w-180, h-175))

weapon2chargelabel_rect = weapon2chargelabel.get_rect(topleft=(w-weapon2chargelabel.get_width()-30, h-175))

rcs = True

logo = pg.image.load("assets/img/logo.png")
logorect = logo.get_rect(center=(w/2, h/2))

impacts = []
class Player:
    """A player
    """
    def __init__(self, x, y, camx, camy, dx, dy, angle, type):
        self.x = x
        self.y = y
        self.camx = camx
        self.camy = camy
        self.dx = dx
        self.dy = dy
        self.angle = angle
        self.screenx = w/2-self.x
        self.screeny = h/2-self.y
        self.type = type
        if self.type == 1:
            self.maxhealth = 100
            self.maxshield = 100
            self.maxmodulehp = 100
            self.health = 100
            self.shield = {
                "topleft":[100, (0, 255, 0)],
                "top":[100, (0, 255, 0)],
                "topright":[100, (0, 255, 0)],
                "left":[100, (0, 255, 0)],
                "right":[100, (0, 255, 0)],
                "bottomleft":[100, (0, 255, 0)],
                "bottom":[100, (0, 255, 0)],
                "bottomright":[100, (0, 255, 0)]
            }
            self.health = 100
            self.modules = {
                "weapon1":100,
                "weapon2":100,
                "generator":100,
                "shieldmodule":100,
                "engine":100,
                "radar":100,
                "fueltank":100
                }
        elif self.type == 2:
            self.maxhealth = 500
            self.maxshield = 500
            self.maxmodulehp = 300
            self.health = 500
            self.modules = {
                "weapon1":300,
                "weapon2":300,
                "generator":300,
                "shieldmodule":300,
                "engine":300,
                "radar":300,
                "fueltank":300
            }
            self.shield = {
                "topleft":[300, (0, 255, 0)],
                "top":[300, (0, 255, 0)],
                "topright":[300, (0, 255, 0)],
                "left":[300, (0, 255, 0)],
                "right":[300, (0, 255, 0)],
                "bottomleft":[300, (0, 255, 0)],
                "bottom":[300, (0, 255, 0)],
                "bottomright":[300, (0, 255, 0)]
            }
        self.rotatespeed = 0
        
    def draw(self):
        """Draws the player"""
        if math.sqrt(self.dx ** 2 + self.dy ** 2) < 80 * (self.modules["engine"]/100):
            if keys[pg.K_w] and not self.modules["engine"] < 30:
                self.dx += math.cos(math.radians(self.angle-90)) * 4 * (self.modules["engine"]/100)
                self.dy += math.sin(math.radians(self.angle-90)) * 4 * (self.modules["engine"]/100)

            if keys[pg.K_s] and not self.modules["engine"] < 30:
                self.dx += -math.cos(math.radians(self.angle-90)) * 4 * (self.modules["engine"]/100)
                self.dy += -math.sin(math.radians(self.angle-90)) * 4 * (self.modules["engine"]/100)
        
        if self.modules["engine"] < 30 and (keys[pg.K_w] or keys[pg.K_s]):
            enginefaulttext = font.render("ENGINE FAULT", True, (255, 0, 0))
            screen.blit(enginefaulttext, enginefaulttext.get_rect(center=(w/2, h/2)))
            if mixer.Channel(4).get_busy() == False:
                mixer.Channel(4).play(pg.mixer.Sound("assets/sfx/enginefault.mp3"), -1)
        else:
            mixer.Channel(4).stop()
        
        if keys[pg.K_a]:
            if self.rotatespeed > -4:
                self.rotatespeed -= 0.2
        elif keys[pg.K_d]:
            if self.rotatespeed < 4:
                self.rotatespeed += 0.2
        else:
            if self.rotatespeed > 0:
                self.rotatespeed -= 0.2
            if self.rotatespeed < 0:
                self.rotatespeed += 0.2
            if abs(self.rotatespeed) < 0.2:
                self.rotatespeed = 0

        self.angle += self.rotatespeed
        
        if self.angle > 360:
            self.angle = 0
        if self.angle < 0:
            self.angle = 359

        if rcs or math.sqrt(self.dx ** 2 + self.dy ** 2) > 75 * (self.modules["engine"]/100):
            if self.dx > 0:
                self.dx -= 1.3
            if self.dy > 0:
                self.dy -= 1.3
            if self.dx < 0:
                self.dx += 1.3
            if self.dy < 0:
                self.dy += 1.3
            if abs(self.dx) + abs(self.dy) < 0.5:
                self.dx = 0
                self.dy = 0

        if self.type == 1:
            char = pg.transform.rotate(ship01, -self.angle)
        elif self.type == 2:
            char = pg.transform.rotate(shipms, -self.angle)
        self.x += self.dx * dt
        self.y += self.dy * dt
        screen.blit(char, char.get_rect(center=(self.x + self.camx, self.y + self.camy)))

        for projectile in projectiles:
            if pg.Rect(self.x + self.camx - ship01.get_width()/2, self.y + self.camy - ship01.get_height()/2, ship01.get_width(), ship01.get_height()).collidepoint((projectile.startx, projectile.starty)) and projectile.origin != self:
                impact_angle = 360-projectile.angle - self.angle + 180
                if impact_angle > 360:
                    impact_angle -= 360
                if impact_angle < 0:
                    impact_angle += 360
    
                shipdmg = False
                randomdamage = random.randint(0, 20)
                if 329 < impact_angle < 361 or -1 < impact_angle < 30:
                    if self.shield["top"][0] < 10:
                        self.health -= 10
                        self.shield["top"][0] = 0
                        shipdmg = True
                    else:
                        self.shield["top"][0] -= 10
                if 29 < impact_angle < 60:
                    if self.shield["topright"][0] < 10:
                        self.health -= 10
                        self.shield["topright"][0] = 0
                        shipdmg = True
                    else:
                        self.shield["topright"][0] -= 10
                if 59 < impact_angle < 120:
                    if self.shield["right"][0] < 10:
                        self.health -= 10
                        self.shield["right"][0] = 0
                        shipdmg = True
                    else:
                        self.shield["right"][0] -= 10
                if 119 < impact_angle < 150:
                    if self.shield["bottomright"][0] < 10:
                        self.health -= 10
                        self.shield["bottomright"][0] = 0
                        self.modules["engine"] -= 10
                        shipdmg = True
                    else:
                        self.shield["bottomright"][0] -= 10
                if 149 < impact_angle < 210:
                    if self.shield["bottom"][0] < 0:
                        self.health -= 10
                        self.shield["bottom"][0] = 0
                        self.modules["engine"] -= 10
                        shipdmg = True
                    else:
                        self.shield["bottom"][0] -= 10
                if 209 < impact_angle < 240:
                    if self.shield["bottomleft"][0] < 10:
                        self.health -= 10
                        self.shield["bottomleft"][0] = 0
                        self.modules["engine"] -= 10
                        shipdmg = True
                    else:
                        self.shield["bottomleft"][0] -= 10
                if 239 < impact_angle < 300:
                    if self.shield["left"][0] < 10:
                        self.health -= 10
                        self.shield["left"][0] = 0
                        shipdmg = True
                    else:
                        self.shield["left"][0] -= 10
                if 299 < impact_angle < 330:
                    if self.shield["topleft"][0] < 10:
                        self.health -= 10
                        self.shield["topleft"][0] = 0
                        shipdmg = True
                    else:
                        self.shield["topleft"][0] -= 10
                    
                if shipdmg:
                    if randomdamage < 5:
                        self.modules["engine"] -= 10
                    if 3 < randomdamage < 8:
                        self.modules["shieldmodule"] -= 10
                    if 6 < randomdamage < 11:
                        self.modules["generator"] -= 10
                    if 10 < randomdamage < 12:
                        self.modules["radar"] -= 10
                    if 11 < randomdamage == 14:
                        self.modules["weapon1"] -= 10
                    if 12< randomdamage < 16:
                        self.modules["weapon2"] -= 10
                    if randomdamage > 15:
                        self.modules["fueltank"] -= 50

                projectiles.remove(projectile)
                return True

class Projectile:
    def __init__(self, startx, starty, angle, ttl, origin):
        self.startx = startx
        self.starty = starty
        self.angle = angle
        self.ttl = ttl
        self.origin = origin

    def draw(self):
        if self.angle > 360:
            self.angle = 0
        if self.angle == -1:
            self.angle = 359

        incrementx = math.cos(math.radians(-self.angle-90)) * 800
        incrementy = math.sin(math.radians(-self.angle-90)) * 800
        self.startx += incrementx * dt
        self.starty += incrementy * dt
        endx = self.startx + incrementx * dt
        endy = self.starty + incrementy * dt
        pg.draw.line(screen, (255, 0, 0), (self.startx, self.starty), (endx, endy), 2)
        
class Enemy:
    def __init__(self, x, y, dx, dy, angle, type):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.angle = angle
        
        self.type = type
        if self.type == 1:
            self.maxhealth = 100
            self.maxshield = 100
            self.maxmodulehp = 100
            self.health = 100
            self.modules = {
                "weapon1":100,
                "weapon2":100,
                "generator":100,
                "shieldmodule":100,
                "engine":100,
                "radar":100,
                "fueltank":100
            }
            self.shield = {
                "topleft":[100, (0, 255, 0)],
                "top":[100, (0, 255, 0)],
                "topright":[100, (0, 255, 0)],
                "left":[100, (0, 255, 0)],
                "right":[100, (0, 255, 0)],
                "bottomleft":[100, (0, 255, 0)],
                "bottom":[100, (0, 255, 0)],
                "bottomright":[100, (0, 255, 0)]
            }
            self.speed = 80
        elif self.type == 2:
            self.maxhealth = 500
            self.maxshield = 300
            self.maxmodulehp = 300
            self.health = 500
            self.modules = {
                "weapon1":300,
                "weapon2":300,
                "generator":300,
                "shieldmodule":300,
                "engine":300,
                "radar":300,
                "fueltank":300
            }
            self.shield = {
                "topleft":[300, (0, 255, 0)],
                "top":[300, (0, 255, 0)],
                "topright":[300, (0, 255, 0)],
                "left":[300, (0, 255, 0)],
                "right":[300, (0, 255, 0)],
                "bottomleft":[300, (0, 255, 0)],
                "bottom":[300, (0, 255, 0)],
                "bottomright":[300, (0, 255, 0)]
            }
            self.speed = 60
        
    def draw(self):
        self.relativex = w/2 + self.x - player.x
        self.relativey = h/2 + self.y - player.y
        self.playerdistance = math.sqrt((player.x - self.x) ** 2 + (player.y - self.y) ** 2)
        self.playerangle = -math.degrees(math.atan2(player.y + player.dy*0.3 - self.y, player.x + player.dx*0.3 - self.x))-90
        if self.playerangle < 0:
            self.playerangle += 360
        if self.type == 1:
            char = pg.transform.rotate(ship01, self.angle)
        elif self.type == 2:
            char = pg.transform.rotate(shipms, self.angle)
        self.x += self.dx * dt
        self.y += self.dy * dt
        screen.blit(char, char.get_rect(center=(w/2 + self.x - player.x, h/2 + self.y - player.y)))
        if self.angle < 0:
            self.angle += 360
        if self.angle > 360:
            self.angle = 0
        for projectile in projectiles:
            if pg.Rect(self.x + player.camx - ship01.get_width()/2, self.y + player.camy - ship01.get_height()/2, ship01.get_width(), ship01.get_height()).collidepoint((projectile.startx, projectile.starty)) and projectile.origin != self:
                impact_angle = 360-projectile.angle - (-self.angle) + 180
                if impact_angle > 360.000:
                    impact_angle -= 360
                if impact_angle < 0:
                    impact_angle += 360
                
                health_before = self.health

                if 329 < impact_angle or impact_angle < 30:
                    if self.shield["top"][0] < 10:
                        self.health -= 10
                        self.shield["top"][0] = 0
                    else:
                        self.shield["top"][0] -= 10
                if 29 < impact_angle < 60:
                    if self.shield["topright"][0] < 10:
                        self.health -= 10
                        self.shield["topright"][0] = 0
                    else:
                        self.shield["topright"][0] -= 10
                if 59 < impact_angle < 120:
                    if self.shield["right"][0] < 10:
                        self.health -= 10
                        self.shield["right"][0] = 0
                    else:
                        self.shield["right"][0] -= 10
                if 119 < impact_angle < 150:
                    if self.shield["bottomright"][0] < 10:
                        self.health -= 10
                        self.shield["bottomright"][0] = 0
                    else:
                        self.shield["bottomright"][0] -= 10
                if 149 < impact_angle < 210:
                    if self.shield["bottom"][0] < 10:
                        self.health -= 10
                        self.shield["bottom"][0] = 0
                    else:
                        self.shield["bottom"][0] -= 10
                if 209 < impact_angle < 240:
                    if self.shield["bottomleft"][0] < 10:
                        self.health -= 10
                        self.shield["bottomleft"][0] = 0
                    else:
                        self.shield["bottomleft"][0] -= 10
                if 239 < impact_angle < 300:
                    if self.shield["left"][0] < 10:
                        self.health -= 10
                        self.shield["left"][0] = 0
                    else:
                        self.shield["left"][0] -= 10
                if 299 < impact_angle < 330:
                    if self.shield["topleft"][0] < 10:
                        self.health -= 10
                        self.shield["topleft"][0] = 0
                    else:
                        self.shield["topleft"][0] -= 10

                projectiles.remove(projectile)
                return True
        if laser and pg.Rect(self.x + player.camx - ship01.get_width()/2, self.y + player.camy - ship01.get_height()/2, ship01.get_width(), ship01.get_height()).collidepoint(pg.mouse.get_pos()):
            impact_angle = -(self.playerangle-self.angle)+360
            if impact_angle > 360:
                impact_angle -= 360
            if impact_angle < 0:
                impact_angle += 360
            if 329 < impact_angle < 361 or -1 < impact_angle < 30:
                if self.shield["top"][0] < 5:
                    self.health -= 2
                else:
                    self.shield["top"][0] -= 2
            if 29 < impact_angle < 60:
                if self.shield["topright"][0] < 10:
                    self.health -= 2
                else:
                    self.shield["topright"][0] -= 2
            if 59 < impact_angle < 120:
                if self.shield["right"][0] < 10:
                    self.health -= 2
                else:
                    self.shield["right"][0] -= 2
            if 119 < impact_angle < 150:
                if self.shield["bottomright"][0] < 10:
                    self.health -= 2
                else:
                    self.shield["bottomright"][0] -= 2
            if 149 < impact_angle < 210:
                if self.shield["bottom"][0] < 10:
                    self.health -= 2
                else:
                    self.shield["bottom"][0] -= 2
            if 209 < impact_angle < 240:
                if self.shield["bottomleft"][0] < 10:
                    self.health -= 2
                else:
                    self.shield["bottomleft"][0] -= 10
            if 239 < impact_angle < 300:
                if self.shield["left"][0] < 10:
                    self.health -= 2
                else:
                    self.shield["left"][0] -= 2
            if 299 < impact_angle < 330:
                if self.shield["topleft"][0] < 10:
                    self.health -= 2
                else:
                    self.shield["topleft"][0] -= 2                
    
    def shoot(self):
        if self.type == 1:
            if self.playerdistance < 600:
                enemyprojectile = Projectile(self.relativex + self.dx*0.5, self.relativey + self.dy*0.5, self.playerangle, 30, self)
                projectiles.append(enemyprojectile)
                mixer.Channel(1).play(pg.mixer.Sound("assets/sfx/laser.mp3"))
        elif self.type == 2:
            if self.playerdistance < 800:

                enemyprojectile = Projectile(self.relativex + self.dx*0.5, self.relativey + self.dy*0.5, self.playerangle, 45, self)
                projectiles.append(enemyprojectile)
                mixer.Channel(1).play(pg.mixer.Sound("assets/sfx/laser.mp3"))
        

  
    def tick(self):
        speed = math.sqrt(self.dx ** 2 + self.dy ** 2)
        if debug:
            pg.draw.line(screen, (255, 0, 0), (self.relativex, self.relativey), (self.relativex + math.cos(math.radians(-self.angle-90)) * 100, self.relativey+ math.sin(math.radians(-self.angle-90)) * 100), 1)
            pg.draw.line(screen, (0, 0, 255), (self.relativex, self.relativey), (self.relativex + math.cos(math.radians(-self.playerangle-90)) * 100, self.relativey + math.sin(math.radians(-self.playerangle-90)) * 100), 1)
        
            screen.blit(font.render(f"dist: {round(self.playerdistance, 2)}", True, (255, 0, 0)), (self.relativex + 50, self.relativey + 50))
            screen.blit(font.render(f"angle: {round(self.playerangle, 2)} ({self.angle})", True, (0, 0, 255)), (self.relativex + 50, self.relativey + 70))
            screen.blit(font.render(f"speed: {round(speed, 2)}", True, (0, 255, 0)), (self.relativex+ 50, self.relativey + 90))
            screen.blit(font.render(f"x, y: {round(self.x, 2)}, {round(self.y, 2)}", True, (0, 255, 0)), (self.relativex, self.relativey + 110))
            screen.blit(font.render(f"target: {round(player.x, 2)}, {round(player.y, 2)}", True, (0, 255, 0)), (self.relativex + 50, self.relativey + 130))
            screen.blit(font.render(f"health: {round(self.health, 1)}", True, (0, 255, 0)), (self.relativex, self.relativey + 150))
        if self.playerangle < self.angle and not (self.playerangle < 90 and self.angle > 270) and self.playerdistance > 300:
                self.angle -= 1
        elif self.playerangle < 90 and self.angle > 270 and self.playerdistance > 300:
            self.angle += 1
        if self.playerangle > self.angle and not (self.playerangle > 270 and self.angle < 90) and self.playerdistance > 300:
                self.angle += 1
        elif self.playerangle > 270 and self.angle < 90 and self.playerdistance > 300:
            self.angle -= 1

        if self.playerdistance > 400:
            if speed < self.speed and abs(self.playerangle - self.angle) < 30:
                self.dx += math.cos(math.radians(-self.angle-90)) * 4 * (self.modules["engine"]/100)
                self.dy += math.sin(math.radians(-self.angle-90)) * 4 * (self.modules["engine"]/100)
            if speed > self.speed-5:
                if self.dx > 0:
                    self.dx -= 0.5
                if self.dy > 0:
                    self.dy -= 0.5
                if self.dx < 0:
                    self.dx += 0.5
                if self.dy < 0:
                    self.dy += 0.5

        else:
            if speed > 5:
                if self.dx > 0:
                    self.dx -= 0.5
                if self.dy > 0:
                    self.dy -= 0.5
                if self.dx < 0:
                    self.dx += 0.5
                if self.dy < 0:
                    self.dy += 0.5


player = Player(0, 0, w/2, h/2, 0, 0, 0, 1)

#Stars generation
stars = []
for i in range(100000):
    x = random.randint(-20000, 20000)
    y = random.randint(-20000, 20000)
    stars.append((x, y))

projectiles = []

target = None
targetindex = 0
impact = False
gameover = False
damagepanel = False
criticalshield = False
showshieldcrit = False
showshipattack = False
showhealthcrit = False
criticalhealth = False
notcritical = True
currentframe = 30000
laser = False
shoot = False
tick = True
debug = False
newProjectile = None
bosscomplete = False
boss = None
autotarget = True


prev_time = time.time()

subtitle = bigfont.render("Presents", True, (255, 255, 255))
subtitle_rect = subtitle.get_rect(center=(w/2, h/2+100))

mixer.Channel(0).set_volume(0.3)
mixer.Channel(1).set_volume(0.3)
mixer.Channel(2).set_volume(0.3)
mixer.Channel(4).set_volume(0.3)
mixer.Channel(5).set_volume(0.3)
mixer.Channel(6).set_volume(0.3)
mixer.Channel(7).set_volume(0.3)

mixer.Channel(3).play(pg.mixer.Sound("assets/sfx/intro.mp3"))
load = True
frame = 0
while load:
    frame += 1
    screen.fill((0, 0, 0))
    for event in pg.event.get():
        pass
    if frame*2 < 1300:
        if frame*2 < 255:
            logo.set_alpha(frame*2)
        if 1000 < frame*2 < 1200:
            logo.set_alpha(1200-frame*2)
            subtitle.set_alpha(1200-frame*2)
        screen.blit(logo, logorect)
        if frame > 200:
            screen.blit(subtitle, subtitle_rect)
    else:
        load = False
    pg.display.flip()
    clock.tick(120)
    
mainloop = True
while mainloop:
    frame = 0
    creditstart = 0
    credittexts = [
        "Skyjade production\nVersion 1.0 Alpha",
        "Game design by:\nSebestyén Garam",
        "Programming by:\nÁdám Vajk",
        "Graphics by:\nSebestyén Garam",
        "Music by:\nÁdám Vajk",
        "Sound effects by:\nBalázs Horváth",
        "Special thanks to:\n@Pearoo",
        "Written in Python using Pygame",
    ]
    creditstart1 = random.randint(300, h-300)
    creditstart2 = random.randint(300, h-300)
    creditstart3 = random.randint(300, h-300)
    creditstart4 = random.randint(300, h-300)
    creditstart5 = random.randint(300, h-300)
    creditstart6 = random.randint(300, h-300)
    creditstart7 = random.randint(300, h-300)
    creditstart8 = random.randint(300, h-300)

    menu = True
    show = True
    showcredits = False
    alpha = 255
    ships = []
    while menu:
        if mixer.Channel(3).get_busy() == False:
            mixer.Channel(3).play(pg.mixer.Sound("assets/sfx/theme.mp3"), -1)
        frame += 1
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit() 
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE and showcredits:
                    showcredits = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if pg.Rect(100, 300, starttext.get_width(), starttext.get_height()).collidepoint(pg.mouse.get_pos()):
                    menu = False
                if pg.Rect(100, 400, creditstext.get_width(), creditstext.get_height()).collidepoint(pg.mouse.get_pos()):
                    showcredits = True
                    creditstart = 0
                if pg.Rect(100, 500, exittext.get_width(), exittext.get_height()).collidepoint(pg.mouse.get_pos()):
                    pg.quit()
        
        screen.fill((0, 0, 0))

        if len(ships) < 3:
            if frame % 120 == 0:
                ships.append((-200, random.randint(200, h-200)))
        for ship in ships:
            x, y = ship
            if x > w:
                ships.remove(ship)
            else:
                newship = pg.transform.rotate(ship01, -90)
                screen.blit(newship, ship01.get_rect(center=(x, y)))
                ships[ships.index(ship)] = (x+5, y)

        title = titlefont.render("Spaceshooter", True, (255, 255, 255))
        starttext = bigfont.render("Start", True, (255, 255, 255))
        creditstext = bigfont.render("Credits", True, (255, 255, 255))
        exittext = bigfont.render("Exit", True, (255, 255, 255))
        credittext = font.render("Skyjade production - V1.0 Alpha", True, (50, 50, 50))

        if showcredits:
            creditstart += 2
            if alpha > 0:
                alpha -= 3
            starttext.set_alpha(alpha)
            creditstext.set_alpha(alpha)
            exittext.set_alpha(alpha)

            if creditstart > 100:
                screen.blit(font.render(credittexts[0], True, (255, 255, 255)), (creditstart-600, creditstart1))
            if creditstart > 400:
                screen.blit(font.render(credittexts[1], True, (255, 255, 255)), (creditstart-1200, creditstart2))
            if creditstart > 700:
                screen.blit(font.render(credittexts[2], True, (255, 255, 255)), (creditstart-1800, creditstart3))
            if creditstart > 1000:
                screen.blit(font.render(credittexts[3], True, (255, 255, 255)), (creditstart-2400, creditstart4))
            if creditstart > 1300:
                screen.blit(font.render(credittexts[4], True, (255, 255, 255)), (creditstart-3000, creditstart5))
            if creditstart > 1600:
                screen.blit(font.render(credittexts[5], True, (255, 255, 255)), (creditstart-3600, creditstart6))
            if creditstart > 1900:
                screen.blit(font.render(credittexts[6], True, (255, 255, 255)), (creditstart-4200, creditstart7))
            if creditstart > 2300:
                screen.blit(font.render(credittexts[7], True, (255, 255, 255)), (creditstart-4800, creditstart8))
            
            if creditstart > 6500:
                showcredits = False

        else:
            if alpha < 255:
                alpha += 3
            starttext.set_alpha(alpha)
            creditstext.set_alpha(alpha)
            exittext.set_alpha(alpha)

        screen.blit(title, title.get_rect(topleft=(100, 100)))
        screen.blit(starttext, starttext.get_rect(topleft=(100, 300)))
        screen.blit(creditstext, creditstext.get_rect(topleft=(100, 400)))
        screen.blit(exittext, exittext.get_rect(topleft=(100, 500)))
        screen.blit(credittext, credittext.get_rect(topleft=(0, h-50)))
        for star in stars:
            x, y = star
            distance = math.sqrt((player.x - x) ** 2 + (player.y - y) ** 2)
            if distance < 1000:
                pg.draw.circle(screen, (255, 255, 255), (x + player.camx, y + player.camy), 1)
        if frame % 5 == 0:
            show = not show
        if show and not showcredits:
            if starttext.get_rect(topleft=(100, 300)).collidepoint(pg.mouse.get_pos()):
                screen.blit(bigfont.render("<", True, (255, 255, 255)), (starttext.get_width()+120, 300))
            if creditstext.get_rect(topleft=(100, 400)).collidepoint(pg.mouse.get_pos()):
                screen.blit(bigfont.render("<", True, (255, 255, 255)), (creditstext.get_width()+120, 400))
            if exittext.get_rect(topleft=(100, 500)).collidepoint(pg.mouse.get_pos()):
                screen.blit(bigfont.render("<", True, (255, 255, 255)), (exittext.get_width()+120, 500))
        
        

        pg.display.flip()
        clock.tick(60)

    main = True
    pause = False
    frame = 0
    enemies, weapon1charge, weapon2charge = reset()
    while main:
        if mixer.Channel(3).get_busy() == False:
            mixer.Channel(3).play(pg.mixer.Sound("assets/sfx/theme.mp3"), -1)
        dt = time.time() - prev_time
        prev_time = time.time()
        frame += 1
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    rcs = not rcs
                if event.key == pg.K_ESCAPE:
                    pause = not pause
                if event.key == pg.K_f:
                    autotarget = False
                    if len(enemies) > 0:
                        targetindex += 1
                        if targetindex == len(enemies):
                            print("autotarget is on")
                            autotarget = True
                        elif targetindex > len(enemies):
                            targetindex = 0

                        if targetindex < len(enemies):
                            target = enemies[targetindex]

                        print(f"index: {targetindex}, len: {len(enemies)}")
                    else:
                        print("no enemies")
                        targetindex = 0
                   
                if event.key == pg.K_g:
                    target = None
                    targetindex = 0
                if event.key == pg.K_i:
                    debug = not debug
                if event.key == pg.K_t:
                    tick = not tick
                if event.key == pg.K_1:
                    selectedweapon = 1
                if event.key == pg.K_2:
                    selectedweapon = 2

            if event.type == pg.MOUSEBUTTONDOWN:
                if not (pg.Rect(w-200, h-300, 200, 300).collidepoint(pg.mouse.get_pos()) or pg.Rect(0, h-300, 200, 300).collidepoint(pg.mouse.get_pos()) or pg.Rect(w-500, h-200, 297, 200).collidepoint(pg.mouse.get_pos()) or pg.Rect(w-30, 89, 30, 146).collidepoint(pg.mouse.get_pos())):
                    if selectedweapon >= 2:
                        laser = True
                    if weapon1charge >= 100 and selectedweapon == 1:
                        shoot = True
                    if shoot:
                        weapon1charge = 0
                        mixer.Channel(0).play(pg.mixer.Sound("assets/sfx/laser.mp3"))
                elif pg.Rect(w-30, 89, 30, 146).collidepoint(pg.mouse.get_pos()):
                    damagepanel = not damagepanel

            if event.type == pg.MOUSEBUTTONUP:
                laser = False
                mixer.Channel(2).stop()

        keys = pg.key.get_pressed()

        player.camx = w/2 - player.x
        player.camy = h/2 - player.y

        screen.fill((0, 0, 0))
        screen.blit(font.render(f"FPS: {round(dt*1000, 2)}", True, (255, 255, 255)), (0, 0))
        screen.blit(font.render(f"Score: {round(frame/30,0)}", True, (255, 255, 255)), (0, 30))

        pg.draw.rect(screen, (200, 200, 200), (0, h-302, 202, 302), border_top_right_radius=12)
        pg.draw.rect(screen, (30, 30, 30), (0, h-300, 200, 300), border_top_right_radius=12)

        pg.draw.rect(screen, (200, 200, 200), (w-202, h-302, 202, 302), border_top_left_radius=12)
        pg.draw.rect(screen, (30, 30, 30), (w-200, h-300, 200, 300), border_top_left_radius=12)

        pg.draw.rect(screen, (200, 200, 200), (w-502, h-202, 302, 202), border_top_left_radius=12)
        pg.draw.rect(screen, (30, 30, 30), (w-500, h-200, 297, 200), border_top_left_radius=12)

        for star in stars:
            x, y = star
            distance = math.sqrt((player.x - x) ** 2 + (player.y - y) ** 2)
            if distance < 1000:
                pg.draw.circle(screen, (255, 255, 255), (x + player.camx, y + player.camy), 1)
        
        if laser and not weapon2charge < 5:
            if mixer.Channel(2).get_busy() == False:
                mixer.Channel(2).play(pg.mixer.Sound("assets/sfx/beam.mp3"))
            pg.draw.line(screen, (255, 255, 255), (player.screenx, player.screeny), pg.mouse.get_pos(), 1)
            weapon2charge -= 2
        elif weapon2charge < 5:
            mixer.Channel(2).stop()
            laser = False
        
        if shoot:
            shootangle = -math.degrees(math.atan2(pg.mouse.get_pos()[1] - player.screeny, pg.mouse.get_pos()[0] - player.screenx))-90
            if shootangle < 0:
                shootangle += 360
            if shootangle > 360:
                shootangle = 0
            newProjectile = Projectile(player.screenx + player.dx*0.5, player.screeny + player.dy*0.5, shootangle, 30, player)
            projectiles.append(newProjectile)
            shoot = False

        if weapon1charge < 100:
            weapon1charge += 5 / (player.modules["weapon1"]/100)
        if weapon2charge < 100 and not laser and frame % 3 == 0:
            weapon2charge += 1 / (player.modules["weapon2"]/100)

        if not pause:
            for item in projectiles:
                item.draw()
                item.ttl -= 1
                if item.ttl == 0:
                    projectiles.remove(item)

        if rcs:
            rcstext = font.render("RCS: ON", True, (200, 200, 200))
        else:
            rcstext = font.render("RCS: OFF", True, (200, 200, 200))
        rcstext_rect = rcstext.get_rect(topleft=(0, h-295))
        screen.blit(rcstext, rcstext_rect)
        posxtext = font.render(f"X: {round(player.x,0)}", True, (200, 200, 200))
        posxtext_rect = posxtext.get_rect(topleft=(0, h-265))
        screen.blit(posxtext, posxtext_rect)
        posytext = font.render(f"Y: {round(player.y, 0)}", True, (200, 200, 200))
        posytext_rect = posytext.get_rect(topleft=(0, h-235))
        screen.blit(posytext, posytext_rect)
        speedtext = font.render(f"SPEED: {round(math.sqrt(player.dx ** 2 + player.dy ** 2)*10, 2)}", True, (200, 200, 200))
        speedtext_rect = speedtext.get_rect(topleft=(0, h-205))
        screen.blit(speedtext, speedtext_rect)
        hdgtext = font.render(f"HDG: {round(player.angle, 0)}", True, (200, 200, 200))
        hdgtext_rect = hdgtext.get_rect(topleft=(0, h-175))
        screen.blit(hdgtext, hdgtext_rect)

        screen.blit(ship01, (65, h-ship01.get_height()-60))
        #shield values
        notcritical = True
        for item in player.shield:
            hpval = (player.shield[item][0] / player.maxshield) * 100
            if hpval == 100:
                player.shield[item][1] = (0, 255, 0)
            elif 80 < hpval < 100:
                player.shield[item][1] = (127, 255, 0)
            elif 60 < hpval < 81:
                player.shield[item][1] = (191, 255, 0)
            elif 40 < hpval < 61:
                player.shield[item][1] = (255, 255, 0)
            elif 20 < hpval < 41:
                player.shield[item][1] = (255, 191, 0)
            elif 10 < hpval < 21:
                player.shield[item][1] = (255, 127, 0)
            elif hpval < 11:
                player.shield[item][1] = (150, 150, 150)
            else:
                player.shield[item][1] = (0, 255, 0)
            if hpval < 10:
                criticalshield = True
                notcritical = False

        if notcritical:
            criticalshield = False
            showshieldcrit = False
            mixer.Channel(6).stop()

        #shield lines
        pg.draw.line(screen, player.shield["top"][1], (70, h-120), (110, h-120), 2)
        pg.draw.line(screen, player.shield["topleft"][1], (70, h-120), (50, h-100), 3)
        pg.draw.line(screen, player.shield["left"][1], (50, h-100), (50, h-60), 2)
        pg.draw.line(screen, player.shield["bottomleft"][1], (50, h-60), (70, h-40), 3)
        pg.draw.line(screen, player.shield["bottom"][1], (70, h-40), (110, h-40), 2)
        pg.draw.line(screen, player.shield["bottomright"][1], (110, h-40), (130, h-60), 3)
        pg.draw.line(screen, player.shield["right"][1], (130, h-60), (130, h-100), 2)
        pg.draw.line(screen, player.shield["topright"][1], (130, h-100), (110, h-120), 3)

        if selectedweapon == 1:
            weapon1text = font.render("Burst", True, (255, 50, 50))
            weapon1chargelabel = font.render(f"{weapon1charge}%", True, (255, 50, 50))
        else:
            weapon1text = font.render("Burst", True, (200, 200, 200))
            weapon1chargelabel = font.render(f"{weapon1charge}%", True, (200, 200, 200))

        if selectedweapon == 2:
            weapon2text = font.render("Laser", True, (255, 50, 50))
            weapon2chargelabel = font.render(f"{weapon2charge}%", True, (255, 50, 50))

        else:
            weapon2text = font.render("Laser", True, (200, 200, 200))
            weapon2chargelabel = font.render(f"{weapon2charge}%", True, (200, 200, 200))


        screen.blit(weaponpaneltext, weaponpaneltext_rect)
        screen.blit(weapon1text, weapon1text_rect)
        screen.blit(weapon1chargelabel, weapon1chargelabel_rect)
        screen.blit(weapon2text, weapon2text_rect)
        screen.blit(weapon2chargelabel, weapon2chargelabel_rect)

        if not pause:
            for enemy in enemies:
                if enemy.health < 0:
                    enemies.remove(enemy)
                    target == None
                    pass

                enemy.draw()
                if tick:
                    enemy.tick()
                    if frame % 30 == 0 and enemy.type == 1:
                        enemy.shoot()
                    elif frame % 10 == 0 and enemy.type == 2:
                        enemy.shoot()
                    
            if frame % 60 == 0:
                if enemy.health < enemy.maxhealth:
                    enemy.health += 1 * (enemy.modules["generator"]/100)
                for shield in enemy.shield:
                    if enemy.shield[shield][0] < enemy.maxshield:
                        enemy.shield[shield][0] += 1 * (enemy.modules["shieldmodule"]/100)

            

        if autotarget:
            target = getClosestEnemy()
        if not pause:
            if player.draw() == True:
                impact = True
                currentframe = frame

        if impact and frame - currentframe < 300:
            if mixer.Channel(7).get_busy() == False:
                mixer.Channel(7).play(pg.mixer.Sound("assets/sfx/warn1.mp3"), -1)
            showshipattack = True
        else:
            impact = False
            showshipattack = False
            mixer.Channel(7).stop()

        if showshipattack:
            screen.blit(font.render("SHIP UNDER ATTACK!", True, (255, 0, 0)), (300, h-50))

        if criticalshield:
            if mixer.Channel(6).get_busy() == False:
                mixer.Channel(6).play(pg.mixer.Sound("assets/sfx/alarm1.mp3"), -1)
            if frame % 10 == 0:
                showshieldcrit = not showshieldcrit
        
        if player.health < 50 and frame % 5 == 0:
            if mixer.Channel(5).get_busy() == False:
                mixer.Channel(5).play(pg.mixer.Sound("assets/sfx/alarm2.mp3"), -1)
            showhealthcrit = not showhealthcrit
        elif player.health > 50:
            mixer.Channel(5).stop()
            showhealthcrit = False

        if showhealthcrit:
            showhealtcrittext = font.render("-- CRITICAL HULL INTEGRITY --", True, (255, 0, 0))
            screen.blit(showhealtcrittext, showhealtcrittext.get_rect(center=(w/2, h/2-200)))
        if showshieldcrit:
            showshieldcrittext = font.render("-- CRITICAL SHIELD INTEGRITY --", True, (255, 0, 0))
            screen.blit(showshieldcrittext, showshieldcrittext.get_rect(center=(w/2, h/2-150)))
        
        if player.health < 0 or player.modules["fueltank"] < 0:
            gameover = True
            showshipattack = False
            impact = False
            main = False
        
        if frame % 60 == 0:
            if player.modules["generator"] < player.maxmodulehp:
                player.modules["generator"] += 1 * (player.modules["generator"]/100)
            if player.modules["engine"] < player.maxmodulehp:
                player.modules["engine"] += 1 * (player.modules["generator"]/100)
            if player.modules["shieldmodule"] < 100:
                player.modules["shieldmodule"] += 1 * (player.modules["generator"]/100)
            if player.modules["radar"] < player.maxmodulehp:
                player.modules["radar"] += 1 * (player.modules["generator"]/100)
            if player.modules["fueltank"] < player.maxmodulehp:
                player.modules["fueltank"] += 1 * (player.modules["generator"]/100)
            if player.modules["weapon1"] < player.maxmodulehp:
                player.modules["weapon1"] += 1 * (player.modules["generator"]/100)
            if player.modules["weapon2"] < player.maxmodulehp:
                player.modules["weapon2"] += 1 * (player.modules["generator"]/100)
            if player.health < 99:
                player.health += 1 * (player.modules["generator"]/100)
            for shield in player.shield:
                if player.shield[shield][0] < player.maxshield:
                    if player.shield[shield][0] < 0:
                        player.shield[shield][0] = 0
                    player.shield[shield][0] += 1 * (player.modules["shieldmodule"]/100)
        
        if target not in enemies:
            notarget = font.render("No target", True, (200, 200, 200))
            screen.blit(notarget, notarget.get_rect(topleft=(w-400, h-50)))
        else:
            targettext = font.render(f"Target: {round(target.x,0)}, {round(target.y,0)}", True, (200, 200, 200))
            screen.blit(targettext, targettext.get_rect(topleft=(w-490, h-60)))
            crosshair_center = (int(target.x + player.camx), int(target.y + player.camy))
            pg.draw.line(screen, (255, 255, 255), (crosshair_center[0]-50, crosshair_center[1]-50), (crosshair_center[0]-16, crosshair_center[1]-50), 1)
            pg.draw.line(screen, (255, 255, 255), (crosshair_center[0]+16, crosshair_center[1]-50), (crosshair_center[0]+50, crosshair_center[1]-50), 1)
            pg.draw.line(screen, (255, 255, 255), (crosshair_center[0]-50, crosshair_center[1]+16), (crosshair_center[0]-50, crosshair_center[1]+50), 1)
            pg.draw.line(screen, (255, 255, 255), (crosshair_center[0]-50, crosshair_center[1]+50), (crosshair_center[0]-16, crosshair_center[1]+50), 1)
            pg.draw.line(screen, (255, 255, 255), (crosshair_center[0]+16, crosshair_center[1]+50), (crosshair_center[0]+50, crosshair_center[1]+50), 1)
            pg.draw.line(screen, (255, 255, 255), (crosshair_center[0]+50, crosshair_center[1]+16), (crosshair_center[0]+50, crosshair_center[1]+50), 1)
            pg.draw.line(screen, (255, 255, 255), (crosshair_center[0]+50, crosshair_center[1]-50), (crosshair_center[0]+50, crosshair_center[1]-16), 1)
            pg.draw.line(screen, (255, 255, 255), (crosshair_center[0]-50, crosshair_center[1]-50), (crosshair_center[0]-50, crosshair_center[1]-16), 1)
            screen.blit(bigfont.render(f"TGT {enemies.index(target)}", True, (255, 255, 255)), (crosshair_center[0]+70, crosshair_center[1]-50))
            screen.blit(font.render(f"Hull: {round(target.health, 0)}%", True, (255, 255, 255)), (crosshair_center[0]+70, crosshair_center[1]+30))
            screen.blit(font.render(f"D: {round(target.playerdistance, 0)}", True, (255, 255, 255)), (crosshair_center[0]+70, crosshair_center[1]+60))

            if target.type == 1:
                targeticon = pg.transform.rotate(ship01, 0)
            elif target.type == 2:
                targeticon = pg.transform.rotate(shipms, 0)
                targeticon = pg.transform.scale(targeticon, (30, 60))
            screen.blit(targeticon, targeticon.get_rect(center=(w-440, h-130)))
            #target shield lines
            for item in target.shield:
                hpval = (target.shield[item][0] / target.maxshield) * 100
                if hpval == 100:
                    target.shield[item][1] = (0, 255, 0)
                elif 80 < hpval < 100:
                    target.shield[item][1] = (127, 255, 0)
                elif 60 < hpval < 81:
                    target.shield[item][1] = (191, 255, 0)
                elif 40 < hpval < 61:
                    target.shield[item][1] = (255, 255, 0)
                elif 20 < hpval < 41:
                    target.shield[item][1] = (255, 191, 0)
                elif 10 < hpval < 21:
                    target.shield[item][1] = (255, 127, 0)
                elif hpval < 11:
                    target.shield[item][1] = (150, 150, 150)
                else:
                    target.shield[item][1] = (0, 255, 0)

            if len(enemies) == 0:
                target = None
            else:
                pg.draw.line(screen, target.shield["top"][1], (w-460, h-165), (w-420, h-165), 2)
                pg.draw.line(screen, target.shield["topleft"][1], (w-460, h-165), (w-480, h-145), 3)
                pg.draw.line(screen, target.shield["left"][1], (w-480, h-145), (w-480, h-105), 2)
                pg.draw.line(screen, target.shield["bottomleft"][1], (w-480, h-105), (w-460, h-85), 3)
                pg.draw.line(screen, target.shield["bottom"][1], (w-460, h-85), (w-420, h-85), 2)
                pg.draw.line(screen, target.shield["bottomright"][1], (w-420, h-85), (w-400, h-105), 3)
                pg.draw.line(screen, target.shield["right"][1], (w-400, h-105), (w-400, h-145), 2)
                pg.draw.line(screen, target.shield["topright"][1], (w-400, h-145), (w-420, h-165), 3)
                screen.blit(font.render(f"Hull: {round(target.health, 0)}%", True, (200, 200, 200)), (w-380, h-150))
        if autotarget:
            screen.blit(font.render("A-TGT: ON", True, (200, 200, 200)), (w-400, h-20))
        else:
            screen.blit(font.render("A-TGT: OFF", True, (200, 200, 200)), (w-400, h-20))

        if not damagepanel:
            pg.draw.line(screen, (255, 255, 255), (w-15, 105), (w-15, 220), 3)
        else:
            pg.draw.rect(screen, (200, 200, 200), (w-302, 87, 302, 502))
            pg.draw.rect(screen, (30, 30, 30), (w-300, 89, 300, 500))
            damagepaneltitle = font.render("DAMAGE PANEL", True, (200, 200, 200))
            screen.blit(damagepaneltitle, damagepaneltitle.get_rect(topleft=(w-250, 100)))
            if player.modules["generator"] < 30:
                engine = font.render(f"ENGINE: {round(player.modules['engine'],0)}%", True, (255, 50, 50))
            else:
                engine = font.render(f"ENGINE: {round(player.modules['engine'],0)}%", True, (200, 200, 200))
            screen.blit(engine, engine.get_rect(topleft=(w-300, 150)))
            if player.modules["shieldmodule"] < 30:
                shieldmodule = font.render(f"SHIELD: {round(player.modules['shieldmodule'],0)}%", True, (255, 50, 50))
            else:
                shieldmodule = font.render(f"SHIELD: {round(player.modules['shieldmodule'],0)}%", True, (200, 200, 200))
            screen.blit(shieldmodule, shieldmodule.get_rect(topleft=(w-300, 200)))
            if player.modules["generator"] < 30:
                generator = font.render(f"GENERATOR: {round(player.modules['generator'],0)}%", True, (255, 50, 50))
            else:
                generator = font.render(f"GENERATOR: {round(player.modules['generator'],0)}%", True, (200, 200, 200))
            screen.blit(generator, generator.get_rect(topleft=(w-300, 250)))
            if player.modules["radar"] < 30:
                radar = font.render(f"RADAR: {round(player.modules['radar'],0)}%", True, (255, 50, 50))
            else:
                radar = font.render(f"RADAR: {round(player.modules['radar'],0)}%", True, (200, 200, 200))
            screen.blit(radar, radar.get_rect(topleft=(w-300, 300)))
            if player.modules["weapon1"] < 30:
                weapon1 = font.render(f"BURST: {round(player.modules['weapon1'],0)}%", True, (255, 50, 50))
            else:
                weapon1 = font.render(f"BURST: {round(player.modules['weapon1'],0)}%", True, (200, 200, 200))
            screen.blit(weapon1, weapon1.get_rect(topleft=(w-300, 350)))
            if player.modules["weapon2"] < 30:
                weapon2 = font.render(f"LASER: {round(player.modules['weapon2'],0)}%", True, (255, 50, 50))
            else:
                weapon2 = font.render(f"LASER: {round(player.modules['weapon2'],0)}%", True, (200, 200, 200))
            screen.blit(weapon2, weapon2.get_rect(topleft=(w-300, 400)))
            if player.modules["fueltank"] < 30:
                fueltank = font.render(f"FUEL TANK: {round(player.modules['fueltank'],0)}%", True, (255, 50, 50))
            else:
                fueltank = font.render(f"FUEL TANK: {round(player.modules['fueltank'],0)}%", True, (200, 200, 200))
            screen.blit(fueltank, fueltank.get_rect(topleft=(w-300, 450)))
            if player.health < 30:
                hull = font.render(f"HULL: {round(player.health,0)}%", True, (255, 50, 50))
            else:
                hull = font.render(f"HULL: {round(player.health,0)}%", True, (200, 200, 200))
            screen.blit(hull, hull.get_rect(topleft=(w-300, 500)))

        pg.draw.rect(screen, (255, 255, 255), (w-30, 89, 30, 146), 2)

        

        if len(enemies) < 20 and frame / 30 < 1000:
            if frame % 1200 == 0 and frame / 30 < 300:
                enemies.append(Enemy(random.randint(-2000, 2000), random.randint(-2000, 2000), random.randint(-2, 2), random.randint(-2, 2), random.randint(0, 360), 1))
            if frame % 800 == 0 and 300 < frame / 30 < 600:
                enemies.append(Enemy(random.randint(-2000, 2000), random.randint(-2000, 2000), random.randint(-2, 2), random.randint(-2, 2), random.randint(0, 360), 1))
            if frame % 400 == 0 and (600 < frame / 30 < 900 or bosscomplete):
                enemies.append(Enemy(random.randint(-2000, 2000), random.randint(-2000, 2000), random.randint(-2, 2), random.randint(-2, 2), random.randint(0, 360), 1))
        if len(enemies) == 0 and frame / 30 > 1000 and not bosscomplete:
            boss = Enemy(random.randint(-5000, 5000), random.randint(-5000, 5000), 0, 0, 0, 2)
            enemies.append(boss)

        if boss not in enemies and frame / 30 > 1050:
            bosscomplete = True
        
        pg.display.flip()

    gameframe = frame

    start_x = w/2
    start_y = h/2
    end_x = 0
    end_y = 0
    frame = 0
    lines = []
    mixer.Channel(0).stop()
    mixer.Channel(1).stop()
    mixer.Channel(2).stop()
    mixer.Channel(3).stop()
    mixer.Channel(4).stop()
    mixer.Channel(5).stop()
    mixer.Channel(6).stop()
    mixer.Channel(7).stop()

    for i in range(60):
        angle = random.randint(0, 360)
        end_x = start_x
        end_y = start_y
        incrementx = math.cos(math.radians(-angle-90)) * 50
        incrementy = math.sin(math.radians(-angle-90)) * 50
        end_x += incrementx
        end_y += incrementy

        lines.append([start_x, start_y, end_x, end_y, incrementx, incrementy])

    screen.blit(explosion, (w/2-100, h/2-100))
    pg.display.update()
    while gameover:
        frame += 1
        screen.fill((0, 0, 0))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                gameover = False
        for star in stars:
            x, y = star
            distance = math.sqrt((player.x - x) ** 2 + (player.y - y) ** 2)
            if distance < 1000:
                pg.draw.circle(screen, (255, 255, 255), (x + player.camx, y + player.camy), 1)
        for item in projectiles:
            item.draw()
        for enemy in enemies:
            enemy.draw()

        mixer.Channel(6).stop()
        mixer.Channel(5).stop()
        if mixer.Channel(7).get_busy() == False:
            mixer.Channel(7).play(pg.mixer.Sound("assets/sfx/explosion.mp3"))
        screen.blit(font.render("GAME OVER", True, (255, 0, 0)), (w/2-100, h/2-300))
        if player.health < 0:
            screen.blit(font.render("Hull destroyed", True, (255, 0, 0)), (w/2-100, h/2-250))
        elif player.modules["fueltank"] < 0:
            screen.blit(font.render("Fuel tank exploded", True, (255, 0, 0)), (w/2-180, h/2-250))
        
        a = font.render(f"Score: {round(gameframe/30, 0)}", True, (255, 0, 0))
        screen.blit(a, a.get_rect(center=(w/2, h/2-200)))
        
        for line in lines:
            line[0] += line[4]
            line[1] += line[5]
            line[2] += line[4]
            line[3] += line[5]
            pg.draw.line(screen, (255, 255, 255), (line[0], line[1]), (line[2], line[3]))
        
        pg.display.flip()
        if frame % 200 == 0:
            gameover = False

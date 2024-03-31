import pygame,math,random
pygame.init()
G = 0.005
height = 1080
width = 1920
fps = 300
frame = 0.1
disp= pygame.display.set_mode((width,height), pygame.FULLSCREEN)
width, height = pygame.display.get_surface().get_width(), pygame.display.get_surface().get_height()
pygame.display.update()
pygame.display.set_caption("Naprendszer szimuláció")
clock = pygame.time.Clock()
state = True

def create_rect(width, height, border, color, border_color):
    surf = pygame.Surface((width+border*2, height+border*2), pygame.SRCALPHA)
    pygame.draw.rect(surf, color, (border, border, width, height), 0)
    for i in range(1, border):
        pygame.draw.rect(surf, border_color, (border-i, border-i, width+5, height+5), 1)
    return surf

disp.fill((0,0,0))
pygame.display.update()
planets = list()
MaxMass = 10000
MinMass = 200
MassScale = (MinMass / MaxMass) / 30
class planet():
    def __init__(self,x,y,mass,diameter,color=(255,255,255)):
        self.x = x
        self.y = y
        self.screenx = x
        self.screeny = y
        self.m = mass
        self.d = diameter
        self.dx = 0
        self.dy = 0
#         self.density=mass/(math.pi*((diameter/2)**2))
#         self.r=int(self.density*MassScale*255)
#         self.g=int(((self.density*MassScale))*255)
#         self.b=int(((self.density*MassScale))*255)
        
        #self.color=(self.r,self.g,self.b)
        self.color=color
        #print(float(self.density*MassScale))
    def draw(self):
        self.x += self.dx * frame * 10
        self.y += self.dy * frame * 10
        self.screenx, self.screeny = ((self.x + self.dx - width/2) * zoom) + width/2, ((height - self.y + self.dy - height/2) * zoom) + height/2
        
        pygame.draw.circle(disp, self.color, (self.screenx, self.screeny), self.d * zoom, 0)

earthorbits = 0
moonorbits = 0

eorbittxt = pygame.font.SysFont("Arial", 30).render("Föld ciklusok: "+str(earthorbits/10), True, (255, 255, 255))
eorbittxt_rect = eorbittxt.get_rect(topleft=(5, 0))
morbitstxt = pygame.font.SysFont("Arial", 30).render("Hold ciklusok: "+str(moonorbits/10), True, (255, 255, 255))
morbitstxt_rect = morbitstxt.get_rect(topleft=(5, 30))

infoinfo = pygame.font.SysFont("Arial", 30).render("I: Infó", True, (255, 255, 255))
infoinfo_rect = infoinfo.get_rect(topleft=(5, height-40))
clearinfo = pygame.font.SysFont("Arial", 30).render("C: Pontok törlése (lag miatt)", True, (255, 255, 255))
clearinfo_rect = clearinfo.get_rect(topleft=(5, height-40))
disableinfo = pygame.font.SysFont("Arial", 30).render("D: Pontrajzolás Ki/Be", True, (255, 255, 255))
disableinfo_rect = disableinfo.get_rect(topleft=(5, height-80))
resetinfo = pygame.font.SysFont("Arial", 30).render("R: Visszaállítás", True, (255, 255, 255))
resetinfo_rect = resetinfo.get_rect(topleft=(5, height-120))
pauseinfo = pygame.font.SysFont("Arial", 30).render("P: Szünet", True, (255, 255, 255))
pauseinfo_rect = pauseinfo.get_rect(topleft=(5, height-160))
focusinfo = pygame.font.SysFont("Arial", 30).render("F: Fókusz (kurzorral) - '.' és ',': váltás", True, (255, 255, 255))
focusinfo_rect = focusinfo.get_rect(topleft=(5, height-200))
zoominfo = pygame.font.SysFont("Arial", 30).render("T, G: Zoom", True, (255, 255, 255))
zoominfo_rect = zoominfo.get_rect(topleft=(5, height-240))
moveinfo = pygame.font.SysFont("Arial", 30).render("(Shift +) Nyilak: Mozgatás", True, (255, 255, 255))
moveinfo_rect = moveinfo.get_rect(topleft=(5, height-280))

option_title = pygame.font.SysFont("Arial", 30).render("Beállítások", True, (255, 255, 255))
option_title_rect = option_title.get_rect(topleft=(width-190, 90))
option_strength = pygame.font.SysFont("Arial", 25).render("Erősség", True, (255, 255, 255))
option_strength_rect = option_strength.get_rect(topleft=(width-140, 130))
option_strength_val = pygame.font.SysFont("Arial", 25).render("10%", True, (255, 255, 255))
option_strength_val_rect = option_strength_val.get_rect(topleft=(width-125, 160))
option_strength_minus = pygame.font.SysFont("Arial", 25).render("-", True, (255, 255, 255))
option_strength_minus_rect = option_strength_minus.get_rect(topleft=(width-170, 160))
option_strength_plus = pygame.font.SysFont("Arial", 25).render("+", True, (255, 255, 255))
option_strength_plus_rect = option_strength_plus.get_rect(topleft=(width-50, 160))
option_mass = pygame.font.SysFont("Arial", 25).render("Tömeg", True, (255, 255, 255))
option_mass_rect = option_mass.get_rect(topleft=(width-140, 200))
option_mass_val = pygame.font.SysFont("Arial", 25).render("10%", True, (255, 255, 255))
option_mass_val_rect = option_mass_val.get_rect(topleft=(width-125, 230))
option_mass_minus = pygame.font.SysFont("Arial", 25).render("-", True, (255, 255, 255))
option_mass_minus_rect = option_mass_minus.get_rect(topleft=(width-170, 230))
option_mass_plus = pygame.font.SysFont("Arial", 25).render("+", True, (255, 255, 255))
option_mass_plus_rect = option_mass_plus.get_rect(topleft=(width-50, 230))
option_diameter = pygame.font.SysFont("Arial", 25).render("Átmérő", True, (255, 255, 255))
option_diameter_rect = option_diameter.get_rect(topleft=(width-140, 263))
option_diameter_val = pygame.font.SysFont("Arial", 25).render("20%", True, (255, 255, 255))
option_diameter_val_rect = option_diameter_val.get_rect(topleft=(width-125, 290))
option_diameter_minus = pygame.font.SysFont("Arial", 25).render("-", True, (255, 255, 255))
option_diameter_minus_rect = option_diameter_minus.get_rect(topleft=(width-170, 290))
option_diameter_plus = pygame.font.SysFont("Arial", 25).render("+", True, (255, 255, 255))
option_diameter_plus_rect = option_diameter_plus.get_rect(topleft=(width-50, 290))
option_color = pygame.font.SysFont("Arial", 25).render("Szín", True, (255, 255, 255))
option_color_rect = option_color.get_rect(topleft=(width-130, 330))
option_color_decerase = pygame.font.SysFont("Arial", 25).render("<", True, (255, 255, 255))
option_color_decerase_rect = option_color_decerase.get_rect(topleft=(width-170, 330))
option_color_increase = pygame.font.SysFont("Arial", 25).render(">", True, (255, 255, 255))
option_color_increase_rect = option_color_increase.get_rect(topleft=(width-50, 330))

strenght = 10
diameter = 20
mass = 10
color = (255, 255, 255)
colorindex = 0
colors = [
    (255, 255, 255), 
    (255, 0, 0), 
    (0, 255, 0), 
    (0, 0, 255), 
    (255, 255, 0), 
    (255, 0, 255), 
    (0, 255, 255),
    (50, 50, 50)
    ]

points = []

'''
earth=planet(width/2-200,height/2,1000,5,(0, 150, 100))
earth.dy=3.5
moon=planet(width/2-220,height/2,250,2,(100, 100, 100))
moon.dy=5.2
moon.dx=0
sun=planet(width/2,height/2,50000,20,(255, 255, 0))
sun.dy=-0.1
planets.append(earth)
planets.append(sun)
planets.append(moon)
'''

#three body problem
planet1 = planet(width/2-100, height/2+25, 5000, 10, (255, 0, 0))
planet1.dy = 1
planet1.dx = 1
planet2 = planet(width/2, height/2, 5000, 10, (0, 255, 0))
planet2.dy = -1
planet2.dx = -1
planet3 = planet(width/2+100, height/2-25, 5000, 10, (0, 0, 255))
planet3.dx = 1
planet3.dy = 1
planets.append(planet1)
planets.append(planet2)
planets.append(planet3)


default_mass=100000 * (mass / 100)
default_diameter=50 * (diameter / 100)
default_color=(255,255,255)
default_strength=30 * (strenght / 100)

stars = []
for i in range(10000):
    star = [random.randint(-5000, 5000), random.randint(-5000, 5000)]
    stars.append(star)

def R_area(p,q):
    area = (p.d**2/4)*math.pi+(q.d**2/4)*math.pi
    return area
def collision(p,q):
    mass=p.m+q.m
    x = ((p.x) + (q.x))/2
    y = ((p.y) + (q.y))/2
    #x=cx/mass
    #y=cy/mass
    dx=(((p.dx*p.m)+(q.dx*q.m))/mass)
    dy=((p.dy*p.m)+(q.dy*q.m))/mass

    d=math.sqrt(R_area(p,q)*4/math.pi)

#     planets.remove(p)
#     planets.remove(q)
    color = ((p.color[0] + q.color[0]) /2, (p.color[1] + q.color[1]) /2, (p.color[2] + q.color[2]) /2)
    np=planet(x,y,mass,d,color)
    np.dx=dx
    np.dy=dy
    planets.append(np)

    #np.draw()
    
def ds(p,q):
    distance_squared= (math.dist((p.x,p.y),(q.x,q.y)))**2
    if distance_squared >= (p.d+q.d)**2:
        return distance_squared
    else:
        collision(p,q)
        return 0
def force(p,q):
    distance=ds(p,q)
    if distance != 0:
        force=-p.m*q.m*G/distance
        return force
    else:
        return 0
def acc(p,q):
    f=force(p,q)
    if f !=0:
        acc=f/p.m
        #print(acc)
        return acc
    else:
        return 0
def angle(p,q):
    if p.x==q.x and p.y>q.y:
        angle=math.pi/2
    elif p.x==q.x and p.y<q.y:
        angle=math.pi*3/2
    else:
        angle=math.atan((p.y-q.y)/(p.x-q.x))
    #print(angle)
    return angle
def comp(p,q):#this diviede acc into x and y comp
    a=acc(p,q)
    if a ==0:
        planets.remove(p)
        planets.remove(q)
    else:
        if p.x<q.x:
            p.dx-=a*math.cos(angle(p,q))
            p.dy-=a*math.sin(angle(p,q))
        else:
            p.dx+=a*math.cos(angle(p,q))
            p.dy+=a*math.sin(angle(p,q))
count=0
toggledots = False
drag = False
settings = False
pause = False
pressede = False
focused = False
focusobj = None
n = 0
totalx = 0
totaly = 0
zoom = 1
while state:
    count+=1
    #no of frames to skip
    c=count%10
    c2 = count%50
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            state = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                points = []
            if event.key == pygame.K_d:
                toggledots = not toggledots
                points = []
            if event.key == pygame.K_r:
                planets = []
                points = []
                earth=planet(width/2-200,height/2,1000,5,(0, 150, 100))
                earth.dy=3.5
                moon=planet(width/2-220,height/2,250,2,(100, 100, 100))
                moon.dy=5.2
                moon.dx=0
                sun=planet(width/2,height/2,50000,20,(255, 255, 0))
                sun.dy=-0.1
                planets.append(earth)
                planets.append(sun)
                planets.append(moon)
                earthorbits = 0
                moonorbits = 0
                drag = False
            if event.key == pygame.K_e:
                pos1 = pygame.mouse.get_pos()
                # ref: pygame.draw.circle(disp, self.color, (((self.x + self.dx - width/2) * zoom) + width/2, ((height - self.y + self.dy - height/2) * zoom) + height/2), self.d * zoom, 0)
                newPlanet = planet(((pos1[0] - width/2) / zoom) + width/2, (((-pos1[1] + height) - height/2) / zoom) + height/2, default_mass, default_diameter, default_color)
                planets.append(newPlanet)
                drag = False
            if event.key == pygame.K_p:
                pause = not pause
            if event.key == pygame.K_f:
                if not focused:
                    for p in planets:
                        px = ((p.x - width/2) * zoom) + width/2 - p.d * zoom
                        py = ((-p.y+height - height/2) * zoom) + height/2 - p.d * zoom
                        w = p.d*zoom*2
                        h = p.d*zoom*2
                        p_rect = pygame.Rect(px, py, w, h)
                        print(p_rect)
                        if p_rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                            print(f"Focus: {p}")
                            focused = True
                            focusobj = p
                else:
                    focused = False
                #planets.append(planet(pygame.mouse.get_pos()[0], -pygame.mouse.get_pos()[1] + height, 10, 10))
            if event.key == pygame.K_PERIOD:
                if len(planets)-1 <= n:
                    n = 0
                else:
                    n += 1
                focusobj = planets[n]
                focused = True
            if event.key == pygame.K_COMMA:
                if n <= 0:
                    n = len(planets)-1
                else:
                    n -= 1
                focusobj = planets[n]
                focused = True


        if event.type == pygame.MOUSEBUTTONDOWN:
            if width-32 < pygame.mouse.get_pos()[0] < width and 88 < pygame.mouse.get_pos()[1] < 231:
                settings = not settings
            elif not settings:
                drag = True
                position1 = pygame.mouse.get_pos()
                pos1 = ((pygame.mouse.get_pos()[0] - width/2) / zoom) + width/2, ((pygame.mouse.get_pos()[1] - height/2) / zoom) + height/2
            if option_strength_minus_rect.collidepoint(pygame.mouse.get_pos()) and strenght > 0:
                strenght -= 1
                option_strength_val = pygame.font.SysFont("Arial", 25).render(str(strenght)+"%", True, (255, 255, 255))
            if option_strength_plus_rect.collidepoint(pygame.mouse.get_pos()) and strenght < 100:
                strenght += 1
                option_strength_val = pygame.font.SysFont("Arial", 25).render(str(strenght)+"%", True, (255, 255, 255))
            if option_mass_minus_rect.collidepoint(pygame.mouse.get_pos()):
                if mass > 1:
                    mass -= 1
                elif 1 >= mass > 0.2:
                    mass -= 0.1
                option_mass_val = pygame.font.SysFont("Arial", 25).render(str(round(mass, 1))+"%", True, (255, 255, 255))
            if option_mass_plus_rect.collidepoint(pygame.mouse.get_pos()):
                if 1 <= mass < 100:
                    mass += 1
                if 1 > mass > 0:
                    mass += 0.1
                option_mass_val = pygame.font.SysFont("Arial", 25).render(str(round(mass, 2))+"%", True, (255, 255, 255))
            if option_diameter_minus_rect.collidepoint(pygame.mouse.get_pos()) and diameter > 1:
                diameter -= 1
                option_diameter_val = pygame.font.SysFont("Arial", 25).render(str(diameter)+"%", True, (255, 255, 255))
            if option_diameter_plus_rect.collidepoint(pygame.mouse.get_pos()) and diameter < 100:
                diameter += 1
                option_diameter_val = pygame.font.SysFont("Arial", 25).render(str(diameter)+"%", True, (255, 255, 255))
            if option_color_decerase_rect.collidepoint(pygame.mouse.get_pos()):
                colorindex -= 1
                if colorindex < 0:
                    colorindex = len(colors)-1
            if option_color_increase_rect.collidepoint(pygame.mouse.get_pos()):
                colorindex += 1
                if colorindex > len(colors)-1:
                    colorindex = 0

            default_mass=100000 * (mass / 100)
            default_diameter=50 * (diameter / 100)
            default_color=colors[colorindex]
            
        if event.type == pygame.MOUSEBUTTONUP:
            if not (1268 < pygame.mouse.get_pos()[0] < width and 88 < pygame.mouse.get_pos()[1] < 231) and drag:
                if not settings:
                    pos2 = ((pygame.mouse.get_pos()[0] - width/2) / zoom) + width/2, ((pygame.mouse.get_pos()[1] - height/2) / zoom) + height/2 # megölöm magam
                    newPlanet = planet(pos1[0], -pos1[1]+height, default_mass, default_diameter, default_color)
                    planets.append(newPlanet)
                    newPlanet.dx = ((pos1[0] - pos2[0]) / 30) * default_strength
                    newPlanet.dy = ((pos2[1] - pos1[1]) / 30) * default_strength
            drag = False

    keys = pygame.key.get_pressed()

    if focusobj not in planets:
        focused = False

    if keys[pygame.K_DOWN] and not focused:
        if keys[pygame.K_LSHIFT]:
            for p in planets:
                p.y += 8
            for i in points:
                i[1] -= 8
            for i in stars:
                i[1] -= 2
            totaly -= 8
        else:
            for p in planets:
                p.y += 1
            for i in points:
                i[1] -= 1
            for i in stars:
                i[1] -= 0.25
            totaly -= 1
    if keys[pygame.K_UP] and not focused:
        if keys[pygame.K_LSHIFT]:
            for p in planets:
                p.y -= 8
            for i in points:
                i[1] += 8
            for i in stars:
                i[1] += 2
            totaly += 8
        else:
            for p in planets:
                p.y -= 1
            for i in points:
                i[1] += 1
            for i in stars:
                i[1] += 0.25
            totaly += 1
    if keys[pygame.K_LEFT] and not focused:
        if keys[pygame.K_LSHIFT]:
            for p in planets:
                p.x += 8
            for i in points:
                i[0] += 8
            for i in stars:
                i[0] += 2
            totalx -= 8
        else:
            for p in planets:
                p.x += 1
            for i in points:
                i[0] += 1
            for i in stars:
                i[0] += 0.25
            totalx -= 1
    if keys[pygame.K_RIGHT] and not focused:
        if keys[pygame.K_LSHIFT]:
            for p in planets:
                p.x -= 8
            for i in points:
                i[0] -= 8
            for i in stars:
                i[0] -= 2
            totalx += 8
        else:
            for p in planets:
                p.x -= 1
            for i in points:
                i[0] -= 1 
            for i in stars:
                i[0] -= 0.25
            totalx += 1

    if focused:
        if focusobj.x > width/2:
            for i in planets:
                i.x -= 1
            for i in points:
                i[0] -= 1
            for i in stars:
                i[0] -= 0.25
            totalx -=1
        if focusobj.x < width/2:
            for i in planets:
                i.x += 1
            for i in points:
                i[0] += 1
            for i in stars:
                i[0] += 0.25
            totalx += 1
        if focusobj.y > height/2:
            for i in planets:
                i.y -= 1
            for i in points:
                i[1] += 1
            for i in stars:
                i[1] += 0.25
            totaly += 1
        if focusobj.y < height/2:
            for i in planets:
                i.y += 1
            for i in points:
                i[1] -= 1
            for i in stars:
                i[1] -= 0.25
            totaly -= 1

    if keys[pygame.K_t]:
        zoom += 0.01 / zoom
    if keys[pygame.K_g]:
        zoom -= zoom / 100

    #calculating part
    if not pause:
        for rp in planets:
            for p in planets:
                if rp != p:
                    comp(rp,p)
                if rp not in planets:
                    break

    #drawing part
    if c == 0:
        disp.fill((0, 0, 0))
        if keys[pygame.K_i]:
            disp.blit(clearinfo, clearinfo_rect)
            disp.blit(disableinfo, disableinfo_rect)
            disp.blit(resetinfo, resetinfo_rect)
            disp.blit(pauseinfo, pauseinfo_rect)
            disp.blit(focusinfo, focusinfo_rect)
            disp.blit(zoominfo, zoominfo_rect)
            disp.blit(moveinfo, moveinfo_rect)
        else:
            disp.blit(infoinfo, infoinfo_rect)

        if -9 < zoom:
            for i in stars:
                pygame.draw.circle(disp, (170, 170, 170), ((((i[0] - width/2) * ((zoom/10)+0.9))) + width/2, (((i[1] - height/2) * ((zoom/10)+0.9))) + height/2), 1)
        for dot in points:
            if 0 < zoom <= 1:
                pygame.draw.circle(disp, (dot[2]), (((dot[0] - width/2) * zoom) + width/2, (((dot[1] - height/2) * zoom) + height/2)), 1)
            elif 1 < zoom:
                pygame.draw.circle(disp, (dot[2]), (((dot[0] - width/2) * zoom) + width/2, (((dot[1] - height/2) * zoom) + height/2)), 1 * zoom)
            else:
                pass

        eorbittxt = pygame.font.SysFont("Arial", 30).render("Föld ciklusok: "+str(earthorbits/10), True, (255, 255, 255))
        try:
            if earth in planets:
                disp.blit(eorbittxt, eorbittxt_rect)
            morbitstxt = pygame.font.SysFont("Arial", 30).render("Hold ciklusok: "+str(moonorbits/10), True, (255, 255, 255))
            if moon in planets:
                disp.blit(morbitstxt, morbitstxt_rect)
        except:
            pass
        
        option_color = pygame.font.SysFont("Arial", 25).render("Szín", True, default_color)
        if drag:
            position2 = pygame.mouse.get_pos()
            pygame.draw.line(disp, (255, 255, 255), position1, position2, 1)
        if settings:
            disp.blit(create_rect(200, 300, 5, (0, 0, 0), (255, 255, 255)), (width-200, 88))
            disp.blit(create_rect(32, 148, 5, (0, 0, 0), (100, 100, 100)), (width-31, 88))
            disp.blit(option_title, option_title_rect)
            disp.blit(option_strength, option_strength_rect)
            disp.blit(option_strength_val, option_strength_val_rect)
            disp.blit(option_strength_minus, option_strength_minus_rect)
            disp.blit(option_strength_plus, option_strength_plus_rect)
            disp.blit(option_mass, option_mass_rect)
            disp.blit(option_mass_val, option_mass_val_rect)
            disp.blit(option_mass_minus, option_mass_minus_rect)
            disp.blit(option_mass_plus, option_mass_plus_rect)
            disp.blit(option_diameter, option_diameter_rect)
            disp.blit(option_diameter_val, option_diameter_val_rect)
            disp.blit(option_diameter_minus, option_diameter_minus_rect)
            disp.blit(option_diameter_plus, option_diameter_plus_rect)
            disp.blit(option_color, option_color_rect)
            disp.blit(option_color_decerase, option_color_decerase_rect)
            disp.blit(option_color_increase, option_color_increase_rect)
        else:
            disp.blit(create_rect(32, 148, 5, (0, 0, 0), (255, 255, 255)), (width-31, 88))
            pygame.draw.line(disp, (255, 255, 255), (width-11, 109), (width-11, 224), 3)
        if not pause:
            for g in planets:
                g.draw()
        else:
            for g in planets:
                pygame.draw.circle(disp, g.color, (((g.x - width/2) * zoom) + width/2, ((height - g.y - height/2) * zoom) + height/2), g.d * zoom, 0)
    
    for i in planets:
        if toggledots and not pause and c2 == 0:
            # ref: pygame.draw.circle(disp, self.color, (((self.x + self.dx - width/2) * zoom) + width/2, ((height - self.y + self.dy - height/2) * zoom) + height/2), self.d * zoom, 0)
            dotx, doty = i.x, -(i.y)+height
            points.append([dotx, doty, i.color])

    try:
        if sun.x+2 > earth.x > sun.x-2 and earth.dx > sun.dx:
            earthorbits += 1
        if earth.x+1 > moon.x > earth.x-1 and moon.dx > earth.dx:
            moonorbits += 1
    except:
        pass
    
    if len(points) > 1000:
        points.remove(points[0])
    
    pygame.display.update()
    clock.tick(fps)
pygame.quit()

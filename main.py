import os, pygame, random

SIZE = [768,704+8]

PATH = os.path.dirname(os.path.abspath(__file__)) # directorio raíz del proyecto
FONT_PATH = PATH + "./lunchds.ttf" # directorio del archivo de fuente

i = [
        [
            [1,1,1,1]
        ], # horizontal
        [
            [1,0,0,0],
            [1,0,0,0],
            [1,0,0,0],
            [1,0,0,0]
        ] # vertical
    ]

s = [
        [
            [0,1,1],
            [1,1,0]
        ], # horizontal
        [
            [1,0,0],
            [1,1,0],
            [0,1,0]
        ] # vertical
    ]
z = [
        [
            [1,1,0],
            [0,1,1]
        ], # horizontal
        [
            [0,0,1],
            [0,1,1],
            [0,1,0]
        ] # vertical
    ]
c = [
        [
            [1,1],
            [1,1]
        ] # todo
    ]
l = [
        [
            [1,0,0],
            [1,0,0],
            [1,1,0]
        ],
        [
            [1,1,1],
            [1,0,0]
        ],
        [
            [1,1,1],
            [1,0,0]
        ],
        [
            [1,1],
            [0,1],
            [0,1]
        ]
    ]
j = [
        [
            [0,1,0],
            [0,1,0],
            [1,1,0]
        ],
        [
            [1,1,1],
            [0,0,1],
        ],
        [
            [1,0,0],
            [1,1,1]
        ],
        [
            [1,1],
            [1,0],
            [1,0]
        ]
    ]

GRIDSIZE = 32
COLS = 15
ROWS = 22
EXTRACOLS = SIZE[0]//GRIDSIZE - COLS
EXTRAROWS = SIZE[1]//GRIDSIZE - ROWS
MAP = [COLS*GRIDSIZE, ROWS*GRIDSIZE]
# PIEZAS = [i]
PIEZAS = [i,s,z,c,l,j]

global font
font = None

class ScreenHandler:
    def __init__(self):
        self.screens = [MenuScreen(self), GameScreen(self)]
        self.current = 0

    def draw(self, surface):
        self.screens[self.current].draw(surface)

    def update(self, dt):
        self.screens[self.current].update(dt)

    def next_screen(self):
        self.change_screen(self.current + 1)

    def change_screen(self, num):
        if(num >= len(self.screens) or num < 0): return
        self.current = num

    def eventos(self, eventos):
        self.screens[self.current].eventos(eventos)

class Screen:
    def __init__(self, sh):
        self.sh = sh

    def draw(self, surface):
        pass

    def update(self, dt):
        pass

    def eventos(self, eventos):
        pass

class MenuScreen(Screen):
    def __init__(self, sh):
        super().__init__(sh)
        self.textSurface = font.render("Press any key to start", True, (255,255,255))

    def draw(self, surface):
        x = surface.get_width() // 2 - self.textSurface.get_width() // 2
        y = surface.get_height() // 2 - self.textSurface.get_height() // 2
        surface.blit(self.textSurface, (x,y))

    def update(self, dt):
        pass

    def eventos(self, eventos):
        for e in eventos:
            if e.type == pygame.KEYDOWN:
                self.sh.next_screen()


class GameScreen(Screen):
    def __init__(self, sh):
        super().__init__(sh)
        self.reset()
        self.scoreSystem = {
            1: 40,
            2: 100,
            3: 300,
            4: 1200
        }
        self.gameOverSurface = font.render("Fin del juego!", True, (255,255,255))


    def reset(self):
        self.score = 0
        forma = PIEZAS[random.randint(0,len(PIEZAS)-1)]
        self.piezas = [Pieza(self, Pieza.spawnX, Pieza.spawnY, forma, 0)]
        self.pieza_activa = self.piezas[len(self.piezas)-1]
        self.map = self.get_clear_map()
        self.next_pieza = None
        self.frame_width = abs( (COLS+1)*GRIDSIZE - (COLS-1+EXTRACOLS)*GRIDSIZE)
        self.frame_height = abs(2*GRIDSIZE - 7*GRIDSIZE)
        self.end = False
        self.gameOverTime = 3
        self.gameOverCount = 0

        self.scoreSurface = font.render(f"Score: {self.score}", True, (255,255,255))
        self.scoreSurfacePosition = []

    def draw(self, surface):
        if(self.end):
            x = surface.get_width() // 2 - self.gameOverSurface.get_width() // 2
            y = surface.get_height() // 2 - self.gameOverSurface.get_height() // 2
            surface.blit(self.gameOverSurface, (x,y))
            return

        for y in range(0, len(self.map)): # mapa estatico
            for x in range(0, len(self.map[y])):
                if(self.map[y][x] == 1):
                    pygame.draw.rect(surface, (0,0,255), [int(x*GRIDSIZE)+2, int(y*GRIDSIZE)+2, GRIDSIZE-2, GRIDSIZE-2])

        for p in self.piezas:
            p.draw(surface)

        if(self.next_pieza):
            self.next_pieza.draw(surface)

        for x in range(0, int(MAP[0]/GRIDSIZE)+1): # lineas verticales
            width = 1
            color = (127,127,127)
            if(x == 0 or x == int(MAP[0]/GRIDSIZE)):
                color = (255,165,0)
                width = 8
            pygame.draw.line(surface, color, (x*GRIDSIZE, 0), (x*GRIDSIZE, MAP[1]), width)

        for y in range(0, int(MAP[1]/GRIDSIZE)+1): # lineas horizontales
            width = 1
            color = (127,127,127)
            if(y == 0 or y == int(MAP[1]/GRIDSIZE)):
                color = (255,165,0)
                width = 8
            pygame.draw.line(surface, color, (0, y*GRIDSIZE ), (MAP[0]+4, y*GRIDSIZE), width)



        color = (255,0,255)
        width = 2
        pygame.draw.line(surface, color, ((COLS+1)*GRIDSIZE, 2*GRIDSIZE), ((COLS-1+EXTRACOLS)*GRIDSIZE, 2*GRIDSIZE), width) # top
        pygame.draw.line(surface, color, ((COLS+1)*GRIDSIZE, 7*GRIDSIZE), ((COLS-1+EXTRACOLS)*GRIDSIZE, 7*GRIDSIZE), width) # bot
        pygame.draw.line(surface, color, ((COLS+1)*GRIDSIZE, 2*GRIDSIZE), ((COLS+1)*GRIDSIZE, 7*GRIDSIZE), width) # left
        pygame.draw.line(surface, color, ((COLS-1+EXTRACOLS)*GRIDSIZE, 2*GRIDSIZE), ((COLS-1+EXTRACOLS)*GRIDSIZE, 7*GRIDSIZE), width) # right


        sX = (COLS+1)*GRIDSIZE
        sY = (7)*GRIDSIZE + 20

        surface.blit(self.scoreSurface, [sX, sY])


    def update(self, dt):
        if(self.end):
            self.gameOverCount += dt
            if(self.gameOverCount >= self.gameOverTime):
                self.gameOverCount = 0
                self.reset()
                self.sh.change_screen(0)
            return
        toRemove = []
        toAdd = []

        self.pieza_activa = self.piezas[len(self.piezas)-1]

        if(not self.next_pieza):
            forma = PIEZAS[random.randint(0,len(PIEZAS)-1)]



            self.next_pieza = Pieza(self, (COLS+1)*GRIDSIZE, 2*GRIDSIZE, forma, 0, True)


            centro_x = (self.frame_width - self.next_pieza.width) / 2
            centro_y = (self.frame_height - self.next_pieza.height) / 2
            # print(centro_x)
            self.next_pieza.x += centro_x
            self.next_pieza.y += centro_y
            self.next_pieza.update_position()

            # width = abs( (COLS+1)*GRIDSIZE - (COLS-1+EXTRACOLS)*GRIDSIZE)
            # height = abs(2*GRIDSIZE - 7*GRIDSIZE)


        if(self.pieza_activa.static):
            pieza = Pieza(self, Pieza.spawnX, Pieza.spawnY, self.next_pieza.figura, 0, False)
            self.next_pieza = None
            toAdd.append(pieza)

        for p in self.piezas: # piezas moviles
            p.update(dt)
            if(p.dead): toRemove.append(p)

        for p in toRemove:
            self.piezas.remove(p)

        if(len(toAdd) > 0):
            for parte in toAdd[0].logicalParts:
                xx = parte[0] // GRIDSIZE
                yy = parte[1] // GRIDSIZE
                if(self.map[yy][xx] != 0):
                    self.end = True
                    print("perdiste!")
                    return
            self.piezas.append(toAdd[0])

        indices = []
        for y in range(0, len(self.map)): # chequear fila completa
            if(len(set(self.map[y]))==1 and self.map[y][0] == 1):
                print("Row full - Index: " + str(y))
                indices.append(y)

        if(len(indices) > 0): # clerear row
            # print('Este turno se clerearon: ' + str(len(indices)) + " filas")
            new = [[0 for x in range(len(self.map[0]))] for j in range(len(indices))] + self.map[0:len(self.map)-len(indices)]
            self.map = new
            self.add_score(len(indices))


    def add_score(self, filas):
        if(filas > 4):
            filas = 4
        self.score += self.scoreSystem[filas]
        self.scoreSurface = font.render(f"Score: {self.score}", True, (255,255,255))
        print(self.score)

    def collides_pieza_activa(self, x, y, w, h, p):
        if(x + w > MAP[0] or y + h > MAP[1] or x < 0 or y < 0):
            return True

        for yy in range(0, len(self.map)):
            for xx in range(0, len(self.map[yy])):
                if(self.map[yy][xx] == 0):
                    continue

                parte_x = xx * GRIDSIZE
                parte_y = yy * GRIDSIZE
                parte_w = GRIDSIZE
                parte_h = GRIDSIZE

                if(x >= parte_x and x+w <= parte_x + parte_w and y >= parte_y and y + h <= parte_y + parte_h):
                    return True

        return False

    def get_column(self, col):
        col = []
        for y in range(0, MAP[1]//GRIDSIZE):
            col.append(self.map[y][col])
        return col

    def get_row(self, row):
        return self.map[row]

    def get_clear_map(self):
        return [[0 for x in range(MAP[0]//GRIDSIZE)] for x in range(MAP[1]//GRIDSIZE)].copy()

    def collides(self, x, y, w, h, p):
        if(p == self.pieza_activa):
            return self.collides_pieza_activa(x,y,w,h,p)

        if(x + w > MAP[0] or y + h > MAP[1] or x < 0 or y < 0):
            return True

        return False

    def eventos(self, eventos):
        for e in eventos:
            if(e.type == pygame.KEYDOWN):
                if(e.key == pygame.K_LEFT):
                    self.pieza_activa.left = True
                    # self.pieza_activa.move_x(-1)
                if(e.key == pygame.K_RIGHT):
                    self.pieza_activa.right = True
                    # self.pieza_activa.move_x(1)
                if(e.key == pygame.K_UP):
                    self.pieza_activa.change_rotation(1)
                if(e.key == pygame.K_DOWN):
                    self.pieza_activa.down = True
            elif(e.type == pygame.KEYUP):
                if(e.key == pygame.K_DOWN):
                    self.pieza_activa.down = False
                if(e.key == pygame.K_LEFT):
                    self.pieza_activa.left = False
                if(e.key == pygame.K_RIGHT):
                    self.pieza_activa.right = False


class Game:
    global dt
    def __init__(self):
        # Centrar la ventana del juegoen el display
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        self.running = False
        self.clock = pygame.time.Clock()
        self.size = SIZE
        self.window = pygame.display.set_mode(self.size)
        self.filepath = os.path.dirname(os.path.abspath(__file__))

        self.dt = 0
        pygame.display.set_caption("Endless Tetris o_o")

    def run(self):
        global font
        self.running = True
        pygame.init()
        font = pygame.font.Font(FONT_PATH, 32)
        self.screen_handler = ScreenHandler()
        self.main_loop()

    def main_loop(self):
        while self.running:
            self.dt = self.clock.tick(60)
            self.dt = self.dt / 1000.0
            self.window.fill((0,0,0))

            self.screen_handler.update(self.dt)
            self.screen_handler.draw(self.window)

            pygame.display.flip()
            self.eventos()

    def eventos(self):
        eventos = pygame.event.get()

        self.screen_handler.eventos(eventos)

        for e in eventos:
            if(e.type == pygame.QUIT):
                self.running = False



class Pieza:
    spawnX = 6
    spawnY = 0
    def __init__(self, map, x=spawnX, y=spawnY, figura=z, rotacion=0, afk=False):
        self.x = int(x/GRIDSIZE) * GRIDSIZE if x > MAP[0]/GRIDSIZE else x *GRIDSIZE
        self.y = int(y/GRIDSIZE) * GRIDSIZE if y > MAP[1]/GRIDSIZE else y*GRIDSIZE
        # print(self.y)
        self.afk = afk
        self.scale = 32
        self.figura = figura
        self.rotation = rotacion
        self.moveTimer = 0
        self.width = 0
        self.height = 0
        self.logicalParts = self.update_logical_parts(self.x, self.y, self.rotation) # [x,y,w,h]
        x_values = set()
        y_values = set()
        for p in self.logicalParts:
            x_values.add(p[0])
            y_values.add(p[1])

        xmin = min(x_values)
        xmax = max(x_values)
        ymin = min(y_values)
        ymax = max(y_values)

        self.width = abs(xmax + self.scale - xmin)
        self.height = abs(ymax + self.scale - ymin)

        self.static = False
        self.dead = False
        self.map = map

        # Keys
        self.left = False
        self.right = False
        self.down = False

        # Key timers
        self.downTimer = 0
        self.maxDownTimer = 0.1

        self.horizontalTimer = 0
        self.maxHorizontalTimer = 0.1

    def __eq__(self, b):
        return self.x == b.x and self.y == b.y

    def update_position(self):
        self.logicalParts = self.update_logical_parts(self.x, self.y, self.rotation) # [x,y,w,h]
        x_values = set()
        y_values = set()
        for p in self.logicalParts:
            x_values.add(p[0])
            y_values.add(p[1])

        print(self.afk)
        print(x_values)
        print(y_values)

        xmin = min(x_values)
        xmax = max(x_values)
        ymin = min(y_values)
        ymax = max(y_values)

        self.width = xmax - xmin
        self.height = ymax - ymin


    def update_logical_parts(self, mi_x, mi_y, rotation):
        lista = []
        for y in range(0, len(self.figura[rotation])):
            for x in range(0, len(self.figura[rotation][y])):
                if(self.figura[rotation][y][x] != 0):
                    pos_x = mi_x + x * self.scale
                    pos_y = mi_y + y * self.scale
                    lista.append([pos_x, pos_y, self.scale, self.scale])
        return lista.copy()

    def change_rotation(self, num):
        rotation = self.rotation + num
        if(rotation >= len(self.figura)):
            rotation = 0
        temp = self.update_logical_parts(self.x, self.y, rotation)
        for p in temp:
            if(self.map.collides(p[0], p[1], p[2], p[3], self)):
                return
        self.rotation = rotation

    def move_x(self, m):
        new_x = self.x
        new_x += m * GRIDSIZE
        temp = self.update_logical_parts(new_x, self.y, self.rotation)
        check = True
        for p in temp:
            if(self.map.collides(p[0], p[1], p[2], p[3], self)):
                check = False
        if(check):
            self.x = new_x

    def move_y(self, m):
        new_y = self.y
        new_y += m * GRIDSIZE
        temp = self.update_logical_parts(self.x, new_y, self.rotation)
        check = True
        for p in temp:
            if(self.map.collides(p[0], p[1], p[2], p[3], self)):
                check = False
        if(check):
            self.y = new_y
        else:
            self.static = True

    def move(self, dt):
        self.horizontalTimer += dt
        if(self.horizontalTimer >= self.maxHorizontalTimer):
            if(self.left):
                self.move_x(-1)
                self.horizontalTimer = 0
            if(self.right):
                self.move_x(1)
                self.horizontalTimer = 0

        if(not self.left and not self.right):
            self.horizontalTimer = self.maxHorizontalTimer

        self.moveTimer += dt
        if(self.down):
            self.downTimer += dt
            if(self.downTimer >= self.maxDownTimer):
                self.move_y(1)
                self.downTimer = 0
        else:
            self.downTimer = self.maxDownTimer

        if(self.moveTimer >= 0.5):
            self.moveTimer = 0
            self.move_y(1)

    def update(self, dt):
        if(self.static or self.afk):
            if(not self.dead):
                for p in self.logicalParts:
                    y = p[1] // GRIDSIZE
                    x = p[0] // GRIDSIZE
                    self.map.map[y][x] = 1
                self.dead = True
            return
        self.move(dt)
        self.logicalParts = self.update_logical_parts(self.x, self.y, self.rotation)

    def draw(self, surface):
        if(self.static):
            return
        for pieza in self.logicalParts:
            pygame.draw.rect(surface, (255,0,0), [int(pieza[0])+2, int(pieza[1])+2, pieza[2]-2, pieza[3]-2])

tetris = Game()
tetris.run()

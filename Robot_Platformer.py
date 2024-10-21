import pygame, os
import math
from random import randint
from time import sleep

os.chdir(os.path.dirname(os.path.abspath(__file__)))

#Player character attributes
class Player(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, position: tuple):
        super().__init__()
        self.image = image
        self.position = (position[0], position[1])
        self.map_start_position = (position[0], position[1])
        self.acc = 0.3
        self.max_speed = 5
        self.jump_strength = 14
        self.fall_speed = 0.7
        self.max_fall_speed = 10
        self.y_speed = 0
        self.x_speed = 0
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.movedown = False
        self.moveup = False
        self.moveright = False
        self.moveleft = False
        self.grounded = False
        self.jumping = False
        self.invulnerable = False
        self.invulnerable_length = 120
        self.invulnerable_timer = 0
        self.rect = pygame.Rect(self.position[0], self.position[1], self.width, self.height)

    def update(self):
        #Update speed parameters
        if self.moveleft:
            self.x_speed = max( self.x_speed - self.acc, -self.max_speed)
        if self.moveright:
            self.x_speed = min( self.x_speed + self.acc, self.max_speed)


        #check for flags and their effects
        if not self.grounded:
            if not self.moveup:
                self.y_speed += self.fall_speed

            self.y_speed = min( self.y_speed + self.fall_speed, self.max_fall_speed)
        
        if self.invulnerable:
            self.invulnerable_timer += 1

            if self.invulnerable_timer >= self.invulnerable_length:
                self.invulnerable = False
                self.invulnerable_timer = 0
            
            if self.invulnerable_timer % 10 == 0 and self.image.get_alpha() == None:
                self.image.set_alpha(25)
            elif self.invulnerable_timer % 10 == 0:
                self.image.set_alpha()
        else:
            self.image.set_alpha()
                

        
        if not self.moveleft and not self.moveright:
            if self.x_speed < 0:
                self.x_speed += self.acc
            elif self.x_speed > 0:
                self.x_speed -= self.acc
            if abs(self.x_speed) < 1:
                self.x_speed = 0
        
        self.jump()
        
        new_pos_x = self.position[0] + self.x_speed
        new_pos_y = self.position[1] + self.y_speed

        self.position = (new_pos_x, new_pos_y)
        self.rect = pygame.Rect(self.position[0], self.position[1], self.width, self.height)



    def jump(self):
        if self.grounded and not self.jumping and self.moveup:
            self.y_speed = -self.jump_strength
            self.jumping = True
            self.grounded = False


#Monster character attributes
class Monster(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, position: tuple):
        super().__init__()
        self.image = image
        self.position = (position[0], position[1])
        self.speed = 0.5
        self.aggro_range = 300
        self.y_speed = 0
        self.x_speed = 0
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = pygame.Rect(self.position[0], self.position[1], self.width, self.height)

    def update(self):
        for character in RobotPlatformer.player:
            x_dif = character.position[0] - self.position[0]
            y_dif = character.position[1] - self.position[1]
            distance = math.sqrt( x_dif**2 + y_dif**2 )
            if distance < self.aggro_range:
                if x_dif > 0:
                    self.position = (self.position[0] + self.speed, self.position[1])
                elif x_dif < 0:
                    self.position = (self.position[0] - self.speed, self.position[1])
                    
                if y_dif > 0:
                    self.position = (self.position[0], self.position[1] + self.speed*0.5)
                elif y_dif < 0:
                    self.position = (self.position[0], self.position[1] - self.speed*0.5)

        self.position = (self.position[0], self.position[1])
        self.rect = pygame.Rect(self.position[0], self.position[1], self.width, self.height)
    

#Tile class
class Tile(pygame.sprite.Sprite):
    color = (75,50,10)

    def __init__(self, position: tuple, side):
        super().__init__()
        self.image = pygame.Surface([side, side])
        self.image.fill( self.color )
        self.position = position[0], position[1]
        self.rect = pygame.Rect(self.position[0], self.position[1], side, side)

#Wall class
class Wall(pygame.sprite.Sprite):
    color = (100,100,100)

    def __init__(self, position: tuple, side):
        super().__init__()
        self.image = pygame.Surface([side, side])
        self.image.fill( self.color )
        self.position = position[0], position[1]
        self.rect = pygame.Rect(self.position[0], self.position[1], side, side)
        self.right_side = pygame.Rect(self.position[0] + side - 5, self.position[1] + 5, 10, side - 10)
        self.left_side = pygame.Rect(self.position[0] - 5, self.position[1] + 5, 10, side - 10)

#Trap class
class Trap(pygame.sprite.Sprite):
    color = (255,140,0)

    def __init__(self, position: tuple, side):
        super().__init__()
        self.image = pygame.Surface([side, side])
        self.image.fill( self.color )
        self.position = position[0], position[1]
        self.rect = pygame.Rect(self.position[0], self.position[1], side, side)

#Coin class
class Coin(pygame.sprite.Sprite):

    def __init__(self, image: pygame.Surface, position: tuple):
        super().__init__()
        self.image = image
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.position = position[0], position[1]
        self.rect = pygame.Rect(self.position[0], self.position[1], self.width, self.height)

#Door class
class Door(pygame.sprite.Sprite):

    def __init__(self, image: pygame.Surface, position: tuple):
        super().__init__()
        self.image = image
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.position = position[0], position[1]
        self.rect = pygame.Rect(self.position[0], self.position[1], self.width, self.height)

#Main game
class RobotPlatformer:

    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    walls = pygame.sprite.Group()
    traps = pygame.sprite.Group()
    doors = pygame.sprite.Group()
    monsters = pygame.sprite.Group()
    player = pygame.sprite.GroupSingle()
    coins = pygame.sprite.Group()
    coins_collected = 0
    P1_lives = 3

    def __init__(self):
        pygame.init()

        self.load()
 
        self.new_game()

        self.load_window()

        self.start_map_screen()

        self.populate_map()

        self.main_loop()
    
    def load(self):
        
        self.font = pygame.font.SysFont("Arial", 24)
        self.title_font = pygame.font.SysFont("Arial", 48)
        self.tile_size = 20
        self.pause = True
        self.clock = pygame.time.Clock()
        self.images = {}
        for image in ["robot", "coin", "monster", "door"]:
            self.images[image] = pygame.image.load( image + ".png")
        self.robot_image = self.images["robot"]
    
    def load_window(self):

        self.HEIGHT = len(self.map)*self.tile_size + self.tile_size*2
        self.WIDTH = len(self.map[0])*self.tile_size
        self.window = pygame.display.set_mode( (self.WIDTH, self.HEIGHT) )
        pygame.display.set_caption("Robot platformer")
    
    def clear_sprites(self):
        self.walls.empty()
        self.platforms.empty()
        self.coins.empty()
        self.player.empty()
        self.doors.empty()
        self.traps.empty()
        self.monsters.empty()
        self.all_sprites.empty()
   
    def new_game(self):
        self.current_level = 1
        self.clear_sprites()
        self.get_map()

    def get_map(self):

        if self.current_level == 1:
            self.map = [
'                                        ',
'                                        ',
'                                        ',
'                                        ',
'                                        ',
'                                        ',
'                                        ',
'                                        ',
'                                        ',
'                                        ',
'                                        ',
'                                        ',
'                                        ',
'                                        ',
'                                        ',
'                                        ',
'                                        ',
'                                        ',
'                                        ',
'                                        ',
'                                        ',
'                                        ',
'                                        ',
'   P                                    ',
'                                    D   ',
'                                        ',
'                C     C      C          ',
'                                        ',
'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW',]

        if self.current_level == 2:
            self.map = [
'                                        ',
'                                        ',
'                                        ',
'                                        ',
'                                        ',
'                                        ',
'                                        ',
'                   C                 C  ',
'                                        ',
'WWWWWWWWWWWWWWWWXXXXXXXWWWWWWWWWWWWXXXXX',
'              W         W               ',
'              W   D     W               ',
'              W         W               ',
'              W         W            C  ',
'              W         W               ',
'              WWWWWWWWWWW          XXXXX',
'                                        ',
'                                        ',
'                                        ',
'                                        ',
'                                     C  ',
'   P                                    ',
'                                   XXXXX',
'                                        ',
'                                        ',
'           WW             WW            ',
'           WW      C      WW         C  ',
'           WW             WW            ',
'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW',]

        if self.current_level == 3:
            self.map = [
'                                        ',
'                                        ',
'                                        ',
'                                        ',
'                                  D     ',
'                                        ',
'    C            C                      ',
'                                        ',
'WWXXXXXWWTTTTWWWWWWWWWTTTTWWWWWWWWWWWWWW',
'                                        ',
'                                        ',
'                                        ',
'    C                                   ',
'                                        ',
'  XXXXX                                 ',
'                                        ',
'                                        ',
'                                        ',
'                                        ',
'    C                             C     ',
'                                        ',
'WWXXXXXWWWWWWWWWWWTTTTWWWWWWWWWWXXXXXXWW',
'                                        ',
'                  P                     ',
'                                        ',
'                                        ',
'    C                                   ',
'                                        ',
'WWWWWWWWWTTTTTWWWWWWWWWWWWWWWWWWWWWWWWWW',]

        if self.current_level == 4:
            self.map = [
'                                        ',
'                                        ',
'                                        ',
'                                        ',
'     M                             M    ',
'                                        ',
'                                        ',
'                                        ',
'                                        ',
'                                        ',
'                                        ',
'                                        ',
'                      C      C          ',
'    C   C                               ',
'                     XXXX   XXXX        ',
'WWXXXXXXXXXWWWW C                       ',
'              W                         ',
'              WXXXX                     ',
'              W                         ',
'    C   C     W                         ',
'              W C                       ',
'  XXXXXXXXX   W                         ',
'    P         WXXXX                     ',
'                                        ',
'                          M       D     ',
'                                        ',
'                C                       ',
'                                        ',
'WWWWWWWWWWWWWWWWWWWWWTTTTTTTTTTTTTWWWWWW',]

        if self.current_level == 5:
            self.map = [
'                                        ',
'                                        ',
'                                        ',
'                                        ',
'                                        ',
'                                        ',
'                                        ',
'    C              C               C    ',
'                                        ',
'  XXXXX         XXXXXXXX         XXXXX  ',
'                   P                    ',
'                                        ',
'                                        ',
'    C                              C    ',
'                                        ',
'  XXXXX         XXXXXXXX         XXXXX  ',
'                                        ',
'                                        ',
'                                        ',
'    C                              C    ',
'                                        ',
'  XXXXX         XXXXXXXX         XXXXX  ',
'                                        ',
'                  M                     ',
'                                        ',
'            WW            WW            ',
'            WW            WW            ',
'            WW            WW            ',
'WWTTTTTWWWWWWWWWWWWWWWWWWWWWWWWWWTTTTTWW',]


    def populate_map(self):

        for (row_index, row) in enumerate(self.map):
            for (col_index, cell) in enumerate(row):
                (x, y) = (col_index*self.tile_size, row_index*self.tile_size)

                if cell == "X":
                    tile = Tile( (x, y), self.tile_size)
                    tile.add(self.all_sprites, self.platforms)
                if cell == "W":
                    wall = Wall( (x, y), self.tile_size)
                    wall.add(self.all_sprites, self.walls)
                if cell == "C":
                    coin = Coin(self.images["coin"], (x, y))
                    coin.add(self.all_sprites, self.coins)
                if cell == "T":
                    trap = Trap( (x,y), self.tile_size)
                    trap.add(self.all_sprites, self.traps)
                if cell == "D":
                    door = Door( self.images["door"], (x,y))
                    door.add(self.all_sprites, self.doors)
                if cell == "P":
                    self.P1 = Player( self.images["robot"], (x,y) )
                    self.P1.add(self.all_sprites, self.player)
                if cell == "M":
                    monster = Monster( self.images["monster"], (x,y)  )
                    monster.add(self.all_sprites, self.monsters)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()                
            #Player controls
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.P1.moveup = True
                if event.key == pygame.K_DOWN:
                    self.P1.movedown = True
                if event.key == pygame.K_LEFT:
                    self.P1.moveleft = True
                if event.key == pygame.K_RIGHT:
                    self.P1.moveright = True
                
                #Other controls
                if event.key == pygame.K_ESCAPE:
                    exit()
                if event.key == pygame.K_F2:
                    self.restart()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.P1.moveup = False
                if event.key == pygame.K_DOWN:
                    self.P1.movedown = False
                if event.key == pygame.K_LEFT:
                    self.P1.moveleft = False
                if event.key == pygame.K_RIGHT:
                    self.P1.moveright = False

    def draw_UI(self):
        coins_text = self.font.render(f"Coins collected: {self.coins_collected}", True, (255, 0, 0) )
        self.window.blit(coins_text, (10,0) )
        
        shortcut_text = self.font.render("F2: restart | Control with arrow keys", True, (255, 0, 0) )
        self.window.blit(shortcut_text, (10, self.HEIGHT - 35) )

        for i in range(self.P1_lives):    
            # Uses a loop to print multiple "robot heads" to indicates how many lives the player has
            lives_text = self.font.render("Lives: ", True, (255,0,0) )
            self.window.blit(lives_text, (10, 50))
            self.window.blit(self.robot_image, ( 60 + i*self.robot_image.get_width(), 45 ) , (0, 0, 50, 35)) 

    def check_collision(self):
        for tile in self.platforms: #Check for (1) if colliding (2) if player is above the platform (3) if not pressing DOWN (4) if player is moving downwards.
            if tile.rect.colliderect(self.P1.rect) and self.P1.position[1] + self.P1.height*0.85 <= tile.position[1] and not self.P1.movedown and self.P1.y_speed >= 0:
                self.P1.y_speed = min(self.P1.y_speed, 0)
                self.P1.position = ( ( self.P1.position[0], tile.position[1] - self.P1.height + 1) )
                self.P1.grounded = True
            
        for tile in self.walls:            
            if tile.rect.colliderect(self.P1.rect):

                if self.P1.position[1] + self.P1.height*0.7 <= tile.position[1]:
                    self.P1.y_speed = min(self.P1.y_speed, 0)
                    self.P1.position = ( self.P1.position[0], tile.position[1] - self.P1.height + 1)
                    self.P1.grounded = True

                elif self.P1.position[0] + self.P1.width - 5 <= tile.position[0]:
                    self.P1.x_speed = min(self.P1.x_speed, 0)
                    self.P1.position = ( tile.position[0] - self.P1.width - 1, self.P1.position[1] )

                elif self.P1.position[0] + 5  >= tile.position[0] + self.tile_size:
                    self.P1.x_speed = max(self.P1.x_speed, 0)
                    self.P1.position = ( tile.position[0] + self.tile_size + 1, self.P1.position[1] )
                
                elif self.P1.position[1] + self.P1.height >= tile.position[1]:
                    self.P1.y_speed = max(self.P1.y_speed, 0)
                    self.P1.position = ( self.P1.position[0], tile.position[1] + self.tile_size + 1 )

        
        for coin in self.coins:
            if coin.rect.colliderect(self.P1.rect):
                coin.kill()
                self.coins_collected += 1
                if self.coins_collected % 10 == 0:
                    self.P1_lives += 1

                if self.current_level == 5 and not self.coins:
                    for monster in self.monsters:
                        monster.speed += 0.25
                        monster.aggro_range += 50

                    if not self.doors:
                        door = (Door(self.images["door"], ( (self.WIDTH - self.images["door"].get_width() )/2, 490 )))
                        door.add( self.doors, self.all_sprites )
                    
                    for i in range(2):
                        coin = Coin(self.images["coin"], ( randint(100, 700), randint(100, 400)  ) )
                        coin.add(self.all_sprites, self.coins)
        
        for door in self.doors:
            if door.rect.colliderect(self.P1.rect): #and not self.coins: #Condition, if you want collecting coins to be a requirement.
                self.win_map()
        
        for monster in self.monsters:
            if monster.rect.colliderect(self.P1.rect) and not self.P1.invulnerable:
                # Player loses a life and turns invulerable (length determined in Player class)
                self.P1_lives -= 1
                self.P1.invulnerable = True
                sleep(0.3)

                if self.P1_lives <= 0:
                        sleep(1)
                        self.lose_map()

        for trap in self.traps:
            if trap.rect.colliderect(self.P1.rect) and not self.P1.invulnerable:
                # Player loses a life and turns invulerable (length determined in Player class)
                self.P1_lives -= 1
                self.P1.invulnerable = True
                sleep(0.3)

                if self.P1_lives <= 0:
                        sleep(1)
                        self.lose_map()

            if trap.rect.colliderect(self.P1.rect):
                if self.P1.position[1] + self.P1.height*0.7 <= trap.position[1]:
                    self.P1.y_speed = min(self.P1.y_speed, 0)
                    self.P1.position = ( self.P1.position[0], trap.position[1] - self.P1.height + 1)
                    self.P1.grounded = True

                elif self.P1.position[0] + self.P1.width - 5 <= trap.position[0]:
                    self.P1.x_speed = min(self.P1.x_speed, 0)
                    self.P1.position = ( trap.position[0] - self.P1.width - 1, self.P1.position[1] )

                elif self.P1.position[0] + 5  >= trap.position[0] + self.tile_size:
                    self.P1.x_speed = max(self.P1.x_speed, 0)
                    self.P1.position = ( trap.position[0] + self.tile_size + 1, self.P1.position[1] )
                    
                elif self.P1.position[1] + self.P1.height >= trap.position[1]:
                    self.P1.y_speed = max(self.P1.y_speed, 0)
                    self.P1.position = ( self.P1.position[0], trap.position[1] + self.tile_size + 1 )

                

    def check_flags(self):

        self.P1.grounded = False

        if self.P1.y_speed >= 0:
            self.P1.jumping = False
        
    
    def player_in_window(self):
        if self.P1.position[0] <= 0:
            self.P1.position = ( 0, self.P1.position[1] )
        elif self.P1.position[0] >= self.WIDTH - self.P1.width:
            self.P1.position =  ( self.WIDTH - self.P1.width, self.P1.position[1] )
        if self.P1.position[1] >= self.HEIGHT:
            self.P1.position = ( self.P1.map_start_position[0], self.P1.map_start_position[1] )

        

    def win_map(self):
        self.pause = True
        self.current_level = self.current_level + 1
        self.start_map_screen()
        if self.current_level == 6:
            exit()
        self.clear_sprites()
        self.get_map()
        self.load_window()
        self.populate_map()
    
    def lose_map(self):
        self.clear_sprites()
        self.pause = True
        self.current_level = 0
        self.start_map_screen()
        self.coins_collected = 0
        self.P1_lives = 3
        self.pause = True
        self.current_level = 1
        self.start_map_screen()
        self.get_map()
        self.load_window()
        self.populate_map()

    
    def restart(self):
        self.pause = True
        self.current_level = 1
        self.coins_collected = 0
        self.P1_lives = 3
        self.start_map_screen()
        self.clear_sprites()
        self.get_map()
        self.load_window()
        self.populate_map()

    def start_map_screen(self):
        while self.pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()                
                #Player controls
                if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                    self.pause = False

                if event.type == pygame.KEYDOWN and event.key == pygame.K_F2:
                    self.pause = False
                    self.restart()
                
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    exit()
            
            self.window.fill( (75, 75, 75) )
            self.clock.tick(60)
            self.draw_info_screen()
            pygame.display.flip()
        
    
    def draw_info_screen(self):

        if self.current_level == 0:

            info_text = self.title_font.render("You died!", True, (255, 0 ,0) )
            text_rect = info_text.get_rect(center=(self.WIDTH/2, self.HEIGHT/4 - 80))
            self.window.blit(info_text, (text_rect))

            info_text = self.font.render(f"You collected {self.coins_collected} coins.", True, (255, 0 ,0) )
            text_rect = info_text.get_rect(center=(self.WIDTH/2, self.HEIGHT/4))
            self.window.blit(info_text, (text_rect))

            controls_text = self.font.render("Press 'ESC' to exit.", True, (255, 0 ,0) )
            text_rect = controls_text.get_rect(center=(self.WIDTH/2, self.HEIGHT*2/4))
            self.window.blit(controls_text, (text_rect))


            shortcut_text = self.font.render("Press 'c' to restart.", True, (255, 0, 0) )
            text_rect = shortcut_text.get_rect(center=(self.WIDTH/2, self.HEIGHT*3/4))
            self.window.blit(shortcut_text, (text_rect) )

        elif self.current_level == 1:

            title_text = "Robot platformer!"
            info_text = self.title_font.render(title_text, True, (255, 0 ,0) )
            text_rect = info_text.get_rect(center=(self.WIDTH/2, self.HEIGHT/4 - 80))
            self.window.blit(info_text, (text_rect))

            info_text = self.font.render("Grab 10 coins for an extra life and get to the exit to advance!", True, (255, 0 ,0) )
            text_rect = info_text.get_rect(center=(self.WIDTH/2, self.HEIGHT/4))
            self.window.blit(info_text, (text_rect))

            controls_text = self.font.render("Use 'LEFT' and 'RIGHT' to move!", True, (255, 0 ,0) )
            text_rect = controls_text.get_rect(center=(self.WIDTH/2, self.HEIGHT*2/4))
            self.window.blit(controls_text, (text_rect))


            shortcut_text = self.font.render("Press 'c' to continue.", True, (255, 0, 0) )
            text_rect = shortcut_text.get_rect(center=(self.WIDTH/2, self.HEIGHT*3/4))
            self.window.blit(shortcut_text, (text_rect) )

        elif self.current_level == 2:
            map_cleared_text = self.font.render(f"You completed level {self.current_level - 1}!", True, (255, 0, 0) )
            text_rect = map_cleared_text.get_rect(center=(self.WIDTH/2, self.HEIGHT/5))
            self.window.blit(map_cleared_text, (text_rect) )

            coins_text = self.font.render(f"Coins collected: {self.coins_collected}", True, (255, 0, 0) )
            text_rect = coins_text.get_rect(center=(self.WIDTH/2, self.HEIGHT*2/5))
            self.window.blit(coins_text, ( text_rect ) )
            
            info_text = self.font.render("Hold 'SPACE' to jump higher and press 'DOWN' to drop down from brown platforms!", True, (255, 0 ,0) )
            text_rect = info_text.get_rect(center=(self.WIDTH/2, self.HEIGHT*3/5))
            self.window.blit(info_text, (text_rect))
            pygame.draw.rect(self.window, (75,50,10) , pygame.Rect(self.WIDTH/2 - self.tile_size*5/2, self.HEIGHT*3/5 + 50, self.tile_size*5, self.tile_size))


            shortcut_text = self.font.render("Press 'c' to continue.", True, (255, 0, 0) )
            text_rect = shortcut_text.get_rect(center=(self.WIDTH/2, self.HEIGHT*4/5))
            self.window.blit(shortcut_text, ( text_rect ) )

        elif self.current_level == 3:
            map_cleared_text = self.font.render(f"You completed level {self.current_level - 1}!", True, (255, 0, 0) )
            text_rect = map_cleared_text.get_rect(center=(self.WIDTH/2, self.HEIGHT/5))
            self.window.blit(map_cleared_text, (text_rect) )

            coins_text = self.font.render(f"Coins collected: {self.coins_collected}", True, (255, 0, 0) )
            text_rect = coins_text.get_rect(center=(self.WIDTH/2, self.HEIGHT*2/5))
            self.window.blit(coins_text, ( text_rect ) )
            
            info_text = self.font.render("Don't hit the fire traps!", True, (255, 0 ,0) )
            text_rect = info_text.get_rect(center=(self.WIDTH/2, self.HEIGHT*3/5))
            self.window.blit(info_text, (text_rect))
            pygame.draw.rect(self.window, (255,140,0) , pygame.Rect(self.WIDTH/2 - self.tile_size*5/2, self.HEIGHT*3/5 + 50, self.tile_size*5, self.tile_size))

            shortcut_text = self.font.render("Press 'c' to continue.", True, (255, 0, 0) )
            text_rect = shortcut_text.get_rect(center=(self.WIDTH/2, self.HEIGHT*4/5))
            self.window.blit(shortcut_text, ( text_rect ) )

        elif self.current_level == 4:
            map_cleared_text = self.font.render(f"You completed level {self.current_level - 1}!", True, (255, 0, 0) )
            text_rect = map_cleared_text.get_rect(center=(self.WIDTH/2, self.HEIGHT/5))
            self.window.blit(map_cleared_text, (text_rect) )

            coins_text = self.font.render(f"Coins collected: {self.coins_collected}", True, (255, 0, 0) )
            text_rect = coins_text.get_rect(center=(self.WIDTH/2, self.HEIGHT*2/5))
            self.window.blit(coins_text, ( text_rect ) )
            
            info_text = self.font.render("Watch out for the monsters!", True, (255, 0 ,0) )
            text_rect = info_text.get_rect(center=(self.WIDTH/2, self.HEIGHT*3/5))
            self.window.blit(info_text, (text_rect))
            self.window.blit( self.images["monster"] , (self.WIDTH/2 - 25, self.HEIGHT/2 + 80) )
            self.window.blit( self.images["monster"] , (self.WIDTH/2 - 75, self.HEIGHT/2 + 80) )
            self.window.blit( self.images["monster"] , (self.WIDTH/2 + 25, self.HEIGHT/2 + 80) )


            shortcut_text = self.font.render("Press 'c' to continue.", True, (255, 0, 0) )
            text_rect = shortcut_text.get_rect(center=(self.WIDTH/2, self.HEIGHT*4/5))
            self.window.blit(shortcut_text, ( text_rect ) )

        elif self.current_level == 5:
            map_cleared_text = self.font.render(f"You completed level {self.current_level - 1}!", True, (255, 0, 0) )
            text_rect = map_cleared_text.get_rect(center=(self.WIDTH/2, self.HEIGHT/5))
            self.window.blit(map_cleared_text, (text_rect) )

            coins_text = self.font.render(f"Coins collected: {self.coins_collected}", True, (255, 0, 0) )
            text_rect = coins_text.get_rect(center=(self.WIDTH/2, self.HEIGHT*2/5))
            self.window.blit(coins_text, ( text_rect ) )
            
            info_text = self.font.render("This is the final level! Collect coins and escape through the door!", True, (255, 0 ,0) )
            text_rect = info_text.get_rect(center=(self.WIDTH/2, self.HEIGHT*3/5))
            self.window.blit(info_text, (text_rect))

            shortcut_text = self.font.render("Press 'c' to continue.", True, (255, 0, 0) )
            text_rect = shortcut_text.get_rect(center=(self.WIDTH/2, self.HEIGHT*4/5))
            self.window.blit(shortcut_text, ( text_rect ) )

        else:
            map_cleared_text = self.title_font.render(f"Congratulations! You finished the game!", True, (255, 0, 0) )
            text_rect = map_cleared_text.get_rect(center=(self.WIDTH/2, self.HEIGHT/5))
            self.window.blit(map_cleared_text, (text_rect) )

            coins_text = self.title_font.render(f"Coins collected: {self.coins_collected}", True, (255, 0, 0) )
            text_rect = coins_text.get_rect(center=(self.WIDTH/2, self.HEIGHT*2/5))
            self.window.blit(coins_text, ( text_rect ) )

            coins_text = self.title_font.render("Press 'c' to exit.", True, (255, 0, 0) )
            text_rect = coins_text.get_rect(center=(self.WIDTH/2, self.HEIGHT*3/5))
            self.window.blit(coins_text, ( text_rect ) )



    #main game loop
    def main_loop(self):
        
        while True:

            self.clock.tick(60)
            
            #canvas
            self.window.fill( (75, 75, 75) )

            #events: exit and controls
            self.check_events()

            #Player colliding with other sprites
            self.check_collision()

            #Restrict player to window
            self.player_in_window()

            #Movement
            self.all_sprites.update()

            #draw frame
            self.all_sprites.draw(self.window)
            self.draw_UI()

            #check flags
            self.check_flags()

            pygame.display.flip()

robot_platformer = RobotPlatformer()

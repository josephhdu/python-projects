# This a simple matching game called memory where you click to flip tiles and try to find all the matching ones

# Note: I didn't finish this code, I didn't have time to figure out how to code the matching aspect of the game

# Imported modules
import pygame
import random
import time

# User-defined functions
def main():
   # initialize all pygame modules (some need initialization)
   pygame.init()
   # create a pygame display window
   pygame.display.set_mode((500, 400))
   # set the title of the display window
   pygame.display.set_caption('Memory Game')   
   # get the display surface
   w_surface = pygame.display.get_surface() 
   # create a game object
   game = Game(w_surface)
   # start the main game loop by calling the play method on the game object
   game.play() 
   # quit pygame and clean up the pygame window
   pygame.quit() 

# User-defined classes
class Game:
   # An object in this class represents a complete game.

    def __init__(self, surface):
        # Initialize a Game.
        # - self is the Game to initialize
        # - surface is the display window surface object

        # === objects that are part of every game that we will discuss
        self.surface = surface
        self.bg_color = pygame.Color('black')
      
        self.FPS = 60
        self.game_Clock = pygame.time.Clock()
        self.close_clicked = False
        self.continue_game = True
      
        # === game specific objects
        self.board_size = 4
        self.image_list = []
        self.load_images()
        self.board = [] # list of lists that contains the images
        self.create_board()
        self.time = 0
      
    def load_images(self):
        # load the images and appends them to the an image list
        img_nmb = 0
        for i in range(0,8):
            img_nmb += 1
            image_num = 'image' + str(img_nmb) + '.bmp'
            image = pygame.image.load(image_num)
            self.image_list.append(image)
        self.image_list = self.image_list + self.image_list
        random.shuffle(self.image_list)
   
    def create_board(self):
        # Nested loop that gets the size of the board and appends the image objects to the board
        width = self.surface.get_width()//self.board_size
        height = self.surface.get_height()//self.board_size
        image_number = 0 
        for row_index in range(0,self.board_size):
            row = []
            for col_index in range(0,self.board_size):
                image = self.image_list[image_number]
                image_number = image_number + 1
                width = image.get_width() 
                height = image.get_height()
                x = col_index * width
                y = row_index * height
                tile = Tile(x,y,width,height,image,self.surface)
                row.append(tile)
            self.board.append(row)
         
    def play(self):
        # Plays the game until the player chooses to quit
        # - self is the Game that should be continued or not.
        while not self.close_clicked:
            self.handle_events()
            self.draw()            
            if self.continue_game:
                self.update()
                self.decide_continue()
            self.game_Clock.tick(self.FPS) # run at most with FPS Frames Per Second 

    def handle_events(self):
        # Handle each user event by changing the game state appropriately.
        # - self is the Game whose events will be handled
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.close_clicked = True
            elif event.type == pygame.MOUSEBUTTONUP:# for when player clicks a tile
                self.handle_mouse_up(event)

    def handle_mouse_up(self, event):
        # Reveals the tile when clicked
        for row in self.board:
            for tile in row:
                if tile.clicked(event.pos):
                    tile.hidden = False


    def draw_timer(self):
        # Draws the timer to the screen
        time = str(self.time)
        size = 100
        font = pygame.font.SysFont('', size, True)
        fg_color = pygame.Color('white')
        game_board = font.render(time, True, fg_color, self.bg_color)
        time_location = (self.surface.get_width() - game_board.get_width(), 0)
        self.surface.blit(game_board, time_location)

    def draw(self):
        # Draw all game objects.
        # - self is the Game to draw
        self.surface.fill(self.bg_color) # clear the display surface first
        # draws the board
        for row in self.board:
            for tile in row:
                tile.draw()
        self.draw_timer()
        pygame.display.update()# make the updated surface appear on the display

    def time_increment(self):
        # Adds to the timer
        self.time = self.time + 1
        time.sleep(1)

    def update(self):
        # Update the game objects for the next frame.
        # - self is the Game to update
        self.time_increment()

# I didn't finish wrting the part this win condition to stop the game if all the tiles have been flipped
    def decide_continue(self):
        # Check and remember if the game should continue
        pass

# I didn't finish writing this, it should check the tiles if they match and flip them back if they don't
    def reset_tiles():
        pass

class Tile:
   # A object that represents the tile in the game

    def __init__(self,x,y,width,height,image,surface):
        # Initializes objects
        self.rect = pygame.Rect(x,y,width,height)
        self.color = pygame.Color('white')
        self.border_width = 3
        self.hidden_image = pygame.image.load('image0.bmp')
        self.hidden = True
        self.content = image
        self.surface = surface

    def draw(self):
        # draws the tile
        location = (self.rect.x, self.rect.y)
        if self.hidden == True:
            self.surface.blit(self.hidden_image, location)
        else:
            self.surface.blit(self.content, location)
        pygame.draw.rect(self.surface,self.color,self.rect, self.border_width)


    def clicked(self, pos):
        # checks the if the click is in the tile
        return self.rect.collidepoint(pos)
        
    # I didn't finished this function that should check the items in the list to see if they match
    def check_tiles():
        pass
        # check if the the tiles in the list is the same

    def expose(self):
        # Shows the tile
        self.hidden = False

    def hide(self):
        # Hides the tile
        self.hidden = True

    def draw_content(self):
        # draws the text box
        font = pygame.font.SysFont('',133) # height of the surface is 400 //3 = 133
        text_box = font.render(self.content,True,self.color)# text_box is a pygame.Surface object
        rect1 = text_box.get_rect()
        rect1.center = self.rect.center
        location = (rect1.x,rect1.y)
        self.surface.blit(text_box,location)

main()
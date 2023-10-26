# This is a simple 2 player pong game where q, a, p, and l are used to control the paddles.
# The game ends when a player misses the ball 11 times

# imports pygame module
import pygame

# User-defined functions
def main():
   # initialize all pygame modules
   pygame.init()
   # create a pygame display window
   pygame.display.set_mode((500, 400))
   # set the title of the display window
   pygame.display.set_caption('Pong')   
   # get the display surface
   w_surface = pygame.display.get_surface() 
   # create a game object
   game = Game(w_surface)
   # start the main game loop by calling the play method on the game object
   game.play() 
   # quit pygame and clean up the pygame window
   pygame.quit() 

# functions that prints the score to screen 
def create_text_image(text_string, fontsize, fg_color, bg_color):
   text_font = pygame.font.SysFont('', fontsize)
   text_image = text_font.render(text_string, True, fg_color, bg_color)
   return text_image
def show_text(surface, text_string, location, fontsize, fg_color, bg_color):
   text_image = create_text_image(text_string, fontsize, fg_color, bg_color)
   surface.blit(text_image, location)

# User-defined classes
class Game:
   # An object in this class represents a complete game.

   def __init__(self, surface):
      # Initialize a Game.
      # - self is the Game to initialize
      # - surface is the display window surface object

      # objects that are used to make the game
      self.surface = surface
      self.bg_color = pygame.Color('black')
      
      self.FPS = 60
      self.game_Clock = pygame.time.Clock()
      self.close_clicked = False
      self.continue_game = True
      
      #game objects
      self.paddle_x = 100
      self.paddle2_x = 400
      self.ball = Ball('white', 5, [250, 200], [4, 4], self.surface)
      self.paddle = Paddle('white', self.paddle_x, 175, 10, 50, self.surface)
      self.paddle2 = Paddle('white', self.paddle2_x, 175, 10, 50, self.surface)

      self.right_score = 0
      self.left_score = 0
      #left_score = Ball.get_right_score(self) <-- what i tried to use for the getter function
      #right_score = Ball.get_left_score(self) <-- what i tried to use for the getter function
      
   def play(self):
      # Play the game until the player presses the close box.
      # - self is the Game that should be continued or not.

      while not self.close_clicked:  # until player clicks close box
         # play frame
         self.handle_events()
         self.draw()            
         if self.continue_game:
            self.update()
            self.decide_continue()
         self.game_Clock.tick(self.FPS)

   def handle_events(self):   # Handle each user event by changing the game state appropriately.
      # - self is the Game whose events will be handled

      events = pygame.event.get()
      for event in events:
         if event.type == pygame.QUIT:
            self.close_clicked = True
         if event.type == pygame.KEYDOWN:
            self.handle_keydown(event)
         if event.type == pygame.KEYUP:
            self.handle_keyup(event)

   def handle_keydown(self, event):
      # Handles the inputs for the paddle
      # - self is the Game whose events will be handled
      # - event is for when a key is pressed
      if event.key == pygame.K_a: # a key: Paddle 1 goes down
         self.paddle.set_velocity(5)
      if event.key == pygame.K_q: # q key: Paddle 1 goes up
         self.paddle.set_velocity(-5)
      if event.key == pygame.K_l: # l key: Paddle 2 goes down
         self.paddle2.set_velocity(5)
      if event.key == pygame.K_p: # p key: Paddle 2 goes up
         self.paddle2.set_velocity(-5)      

   def handle_keyup(self, event):
      # Handles and makes the paddle stop
      self.paddle.set_velocity(0)
      self.paddle2.set_velocity(0)

   def draw(self):
      # Draw all game objects.
      # - self is the Game to draw
      self.surface.fill(self.bg_color) # clear the display surface first
      self.ball.draw()
      self.paddle.draw()
      self.paddle2.draw()
      self.leftscore(self.left_score)
      self.rightscore(self.right_score)
      pygame.display.update() # make the updated surface appear on the display
      

   def leftscore(self, left_score):   
      # Shows the left player game score in at the top left corner
      text_string = str(left_score)
      location = (0, 0)
      fontsize = 72
      fg_color = 'white'
      bg_color = 'black'
      show_text(self.surface, text_string, location, 
                fontsize, fg_color, bg_color)
    
   def rightscore(self, right_score):
       # Shows the right player game score at the top right corner
      text_string = str(right_score)
      location = (460, 0)
      fontsize = 72
      fg_color = 'white'
      bg_color = 'black'
      show_text(self.surface, text_string, location, 
                fontsize, fg_color, bg_color)



   def update(self):
      # Update the game objects for the next frame.
      # - self is the Game to update
      self.ball.collide(self.paddle, self.paddle2)
      self.ball.move()
      self.paddle.move()
      self.paddle2.move()
      # self.

   def decide_continue(self):
      # Note: I didn't finish this cause I couldn't get the scoree counter to work
      # Check and remember if the game should continue
      # - self is the Game to check
      pass

class Paddle:
   # A paddle is a moving rectangle on a surface
   def __init__(self, paddle_color, x, y, width, height, surface):
      self.color = pygame.Color(paddle_color)
      self.rect = pygame.Rect(x, y, width, height)
      self.surface = surface
      self.v = 0

   def move(self):
      # Moves the paddle
      # - self is the paddle
      safe_v = self.v
      new_y = self.rect.y + self.v
      if new_y < 0:
         safe_v = -self.rect.y
         
      self.rect.move_ip(0, safe_v)

      self.bottom_edge()
      
   def bottom_edge(self):
      if self.rect.bottom > self.surface.get_height():
         self.rect.bottom = self.surface.get_height()
         
   def draw(self):
      # Draw the paddle's rect on the surface
      # - self is the Paddle
      pygame.draw.rect(self.surface, self.color, self.rect)       
   
   def set_velocity(self, new_velocity):
      self.v = new_velocity
   
class Ball:
   # An object in this class represents a Dot that moves 
   
   def __init__(self, dot_color, dot_radius, dot_center, dot_velocity, surface):
      # Initialize a Dot.
      # - self is the Dot to initialize
      # - color is the pygame.Color of the dot
      # - center is a list containing the x and y int
      #   coords of the center of the dot
      # - radius is the int pixel radius of the dot
      # - velocity is a list containing the x and y components
      # - surface is the window's pygame.Surface object

      self.color = pygame.Color(dot_color)
      self.radius = dot_radius
      self.center = dot_center
      self.velocity = dot_velocity
      self.surface = surface

      self.right_score = 0
      self.left_score = 0
      
   def move(self):
      # Change the location of the Dot by adding the corresponding 
      # speed values to the x and y coordinate of its center
      # - self is the Dot
      
      size = self.surface.get_size() # (500, 400)
      for i in range(0,2):
         self.center[i] = self.center[i] + self.velocity[i]
      for i in range(0,2):
         if self.center[i] < self.radius:
            # reached the minimum for this coordinate, turn back
            self.velocity[i] = - self.velocity[i]
         if self.center [i] + self.radius > size[i]:
            # reached the maximum for this coordinate, turn back
            self.velocity[i] = - self.velocity[i]
      for i in range(0,1):
          if self.center[i] < self.radius:
            self.right_score += 1
            #Game.getRightScore <- tried to use the getter funciton
      for i in range(0,1):
          if self.center [i] + self.radius > size[i]:
            self.left_score += 1
            #Game.getLeftScore <- tried to use the getter function
   
   def get_right_score(self):
       # getter function that doesn't work ;(
       return self.right_score
   def get_left_score(self):
       # getter function that doesn't work ;(
        return self.left_score


   def draw(self):
      # Draw the dot on the surface
      # - self is the Dot
      
      pygame.draw.circle(self.surface, self.color, self.center, self.radius)
      
   def collide(self, paddle, paddle2):
       # Doesn't let the paddle go off the screen
      rect_paddle = paddle.rect
      rect_paddle2 = paddle2.rect
      if rect_paddle.collidepoint(self.center) == 1 and self.velocity[0] < 0:
         self.velocity[0] = -self.velocity[0]
      elif rect_paddle2.collidepoint(self.center) == 1 and self.velocity[0] > 0:
         self.velocity[0] = -self.velocity[0]
         
main()
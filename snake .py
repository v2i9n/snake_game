import pygame
import random
import sys

# إعدادات اللعبة
WIDTH, HEIGHT = 600, 400
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

# الألوان
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

class Snake:
    def __init__(self):
        self.body = [(5, 5)]
        self.direction = (1, 0)
        self.grow = False
    
    def move(self):
        head = self.body[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        
        # تصادم مع الجدار
        if new_head[0] < 0 or new_head[0] >= GRID_WIDTH or new_head[1] < 0 or new_head[1] >= GRID_HEIGHT:
            return False
        
        # تصادم مع الجسم
        if new_head in self.body:
            return False
            
        self.body.insert(0, new_head)
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
        return True
    
    def change_direction(self, new_dir):
        # منع الرجوع للخلف
        if (new_dir[0] * -1, new_dir[1] * -1)!= self.direction:
            self.direction = new_dir

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.randomize()
    
    def randomize(self):
        self.position = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game - By Hussein 🐍")
    clock = pygame.time.Clock()
    
    snake = Snake()
    food = Food()
    score = 0
    font = pygame.font.Font(None, 36)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction((0, -1))
                elif event.key == pygame.K_DOWN:
                    snake.change_direction((0, 1))
                elif event.key == pygame.K_LEFT:
                    snake.change_direction((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction((1, 0))
        
        # حركة الأفعى
        if not snake.move():
            running = False
        
        # أكل التفاحة
        if snake.body[0] == food.position:
            snake.grow = True
            score += 10
            food.randomize()
            # تأكد التفاحة ما تطلع على جسم الأفعى
            while food.position in snake.body:
                food.randomize()
        
        # الرسم
        screen.fill(BLACK)
        
        # ارسم الأفعى
        for segment in snake.body:
            pygame.draw.rect(screen, GREEN, (segment[0]*GRID_SIZE, segment[1]*GRID_SIZE, GRID_SIZE-1, GRID_SIZE-1))
        
        # ارسم الأكل
        pygame.draw.rect(screen, RED, (food.position[0]*GRID_SIZE, food.position[1]*GRID_SIZE, GRID_SIZE, GRID_SIZE))
        
        # السكور
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        pygame.display.flip()
        clock.tick(10) # سرعة اللعبة
    
    # شاشة النهاية
    screen.fill(BLACK)
    game_over = font.render(f"Game Over! Score: {score}", True, WHITE)
    restart = font.render("Press any key to exit", True, WHITE)
    screen.blit(game_over, (WIDTH//2 - 120, HEIGHT//2 - 50))
    screen.blit(restart, (WIDTH//2 - 130, HEIGHT//2))
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                waiting = False
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

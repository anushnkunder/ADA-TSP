import pygame
from models.city import City
from utils import generate_random_cities, generate_circle_cities, generate_clustered_cities

class PlaygroundTab:
    """Tab for creating and editing cities."""
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cities = []
        self.next_id = 0
        
        # UI elements
        self.buttons = {
            'random': pygame.Rect(20, height - 150, 150, 35),
            'circle': pygame.Rect(20, height - 110, 150, 35),
            'clustered': pygame.Rect(20, height - 70, 150, 35),
            'clear': pygame.Rect(180, height - 150, 150, 35),
        }
        
    def handle_click(self, pos):
        """Handle mouse clicks."""
        # Check buttons
        if self.buttons['random'].collidepoint(pos):
            self.cities = generate_random_cities(10, self.width, self.height - 200)
            self.next_id = len(self.cities)
        elif self.buttons['circle'].collidepoint(pos):
            self.cities = generate_circle_cities(10, self.width, self.height - 200)
            self.next_id = len(self.cities)
        elif self.buttons['clustered'].collidepoint(pos):
            self.cities = generate_clustered_cities(12, self.width, self.height - 200)
            self.next_id = len(self.cities)
        elif self.buttons['clear'].collidepoint(pos):
            self.cities = []
            self.next_id = 0
        # Add city on canvas click
        elif pos[1] < self.height - 200:
            self.cities.append(City(pos[0], pos[1], self.next_id))
            self.next_id += 1
    
    def draw(self, screen):
        """Draw the playground tab."""
        # Draw canvas area
        pygame.draw.rect(screen, (40, 40, 40), (0, 0, self.width, self.height - 200))
        
        # Draw cities
        for city in self.cities:
            pygame.draw.circle(screen, (255, 255, 255), (city.x, city.y), 6)
            font = pygame.font.Font(None, 20)
            text = font.render(str(city.id), True, (200, 200, 200))
            screen.blit(text, (city.x + 10, city.y - 10))
        
        # Draw control panel
        pygame.draw.rect(screen, (30, 30, 30), (0, self.height - 200, self.width, 200))
        
        # Draw buttons
        font = pygame.font.Font(None, 28)
        for name, rect in self.buttons.items():
            pygame.draw.rect(screen, (70, 70, 70), rect)
            pygame.draw.rect(screen, (100, 100, 100), rect, 2)
            text = font.render(name.capitalize(), True, (255, 255, 255))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)
        
        # Draw instructions
        font_small = pygame.font.Font(None, 24)
        instructions = [
            "Click on canvas to add cities",
            f"Cities: {len(self.cities)}",
        ]
        for i, line in enumerate(instructions):
            text = font_small.render(line, True, (200, 200, 200))
            screen.blit(text, (350, self.height - 140 + i * 30))

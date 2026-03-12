import pygame
from models.city import City
from utils import generate_random_cities, generate_circle_cities, generate_clustered_cities

class PlaygroundTab:
    """Tab for creating and editing cities (optimized)."""
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cities = []
        self.next_id = 0
        self.city_count = 10  # Default city count
        self.editing_count = False  # Whether user is typing
        self.count_input = "10"  # String for keyboard input
        
        # UI elements
        self.buttons = {
            'random': pygame.Rect(20, height - 150, 150, 35),
            'circle': pygame.Rect(20, height - 110, 150, 35),
            'clustered': pygame.Rect(20, height - 70, 150, 35),
            'clear': pygame.Rect(180, height - 150, 150, 35),
            'count_minus': pygame.Rect(180, height - 110, 35, 35),
            'count_plus': pygame.Rect(295, height - 110, 35, 35),
        }
        
        # Count input box
        self.count_input_rect = pygame.Rect(220, height - 110, 70, 35)
        
    def handle_click(self, pos):
        """Handle mouse clicks (optimized with validation)."""
        # Check if clicking on count input box
        if self.count_input_rect.collidepoint(pos):
            self.editing_count = True
            self.count_input = str(self.city_count)
            return
        else:
            self.editing_count = False
        
        # Check buttons
        if self.buttons['random'].collidepoint(pos):
            self.cities = generate_random_cities(self.city_count, self.width, self.height - 200)
            self.next_id = len(self.cities)
        elif self.buttons['circle'].collidepoint(pos):
            self.cities = generate_circle_cities(self.city_count, self.width, self.height - 200)
            self.next_id = len(self.cities)
        elif self.buttons['clustered'].collidepoint(pos):
            self.cities = generate_clustered_cities(self.city_count, self.width, self.height - 200)
            self.next_id = len(self.cities)
        elif self.buttons['clear'].collidepoint(pos):
            self.cities = []
            self.next_id = 0
        elif self.buttons['count_minus'].collidepoint(pos):
            self.city_count = max(3, self.city_count - 1)
            self.count_input = str(self.city_count)
        elif self.buttons['count_plus'].collidepoint(pos):
            self.city_count = min(50, self.city_count + 1)
            self.count_input = str(self.city_count)
        # Add city on canvas click
        elif pos[1] < self.height - 200:
            if len(self.cities) < 50:  # Limit max cities
                self.cities.append(City(pos[0], pos[1], self.next_id))
                self.next_id += 1
    
    def handle_keypress(self, event):
        """Handle keyboard input for city count."""
        if not self.editing_count:
            return
        
        if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
            # Finish editing
            try:
                new_count = int(self.count_input)
                self.city_count = max(3, min(50, new_count))
                self.count_input = str(self.city_count)
            except ValueError:
                self.count_input = str(self.city_count)
            self.editing_count = False
        elif event.key == pygame.K_ESCAPE:
            # Cancel editing
            self.count_input = str(self.city_count)
            self.editing_count = False
        elif event.key == pygame.K_BACKSPACE:
            # Delete character
            self.count_input = self.count_input[:-1]
            if not self.count_input:
                self.count_input = "0"
        elif event.unicode.isdigit() and len(self.count_input) < 3:
            # Add digit
            if self.count_input == "0":
                self.count_input = event.unicode
            else:
                self.count_input += event.unicode
    
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
        
        # Section 1: Preset Generation
        font_label = pygame.font.Font(None, 22)
        label = font_label.render("Generate Presets:", True, (180, 180, 180))
        screen.blit(label, (20, self.height - 190))
        
        # Draw preset buttons
        font = pygame.font.Font(None, 28)
        for name in ['random', 'circle', 'clustered']:
            rect = self.buttons[name]
            pygame.draw.rect(screen, (70, 70, 70), rect)
            pygame.draw.rect(screen, (100, 100, 100), rect, 2)
            text = font.render(name.capitalize(), True, (255, 255, 255))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)
        
        # Section 2: City Count Control
        label = font_label.render("Preset Count:", True, (180, 180, 180))
        screen.blit(label, (180, self.height - 135))
        
        # Draw city count control
        pygame.draw.rect(screen, (70, 70, 70), self.buttons['count_minus'])
        pygame.draw.rect(screen, (100, 100, 100), self.buttons['count_minus'], 2)
        text = font.render("-", True, (255, 255, 255))
        text_rect = text.get_rect(center=self.buttons['count_minus'].center)
        screen.blit(text, text_rect)
        
        pygame.draw.rect(screen, (70, 70, 70), self.buttons['count_plus'])
        pygame.draw.rect(screen, (100, 100, 100), self.buttons['count_plus'], 2)
        text = font.render("+", True, (255, 255, 255))
        text_rect = text.get_rect(center=self.buttons['count_plus'].center)
        screen.blit(text, text_rect)
        
        # Draw count display
        count_rect = self.count_input_rect
        bg_color = (70, 70, 100) if self.editing_count else (50, 50, 50)
        pygame.draw.rect(screen, bg_color, count_rect)
        pygame.draw.rect(screen, (100, 100, 100), count_rect, 2)
        
        # Show input text or current count
        display_text = self.count_input if self.editing_count else str(self.city_count)
        text = font.render(display_text, True, (255, 255, 255))
        text_rect = text.get_rect(center=count_rect.center)
        screen.blit(text, text_rect)
        
        # Show cursor if editing
        if self.editing_count:
            cursor_x = text_rect.right + 2
            cursor_y = count_rect.centery
            pygame.draw.line(screen, (255, 255, 255), 
                           (cursor_x, cursor_y - 10), 
                           (cursor_x, cursor_y + 10), 2)
        
        # Section 3: Clear button
        pygame.draw.rect(screen, (120, 50, 50), self.buttons['clear'])
        pygame.draw.rect(screen, (100, 100, 100), self.buttons['clear'], 2)
        text = font.render("Clear", True, (255, 255, 255))
        text_rect = text.get_rect(center=self.buttons['clear'].center)
        screen.blit(text, text_rect)
        
        # Section 4: Instructions panel
        panel_x = self.width - 380
        panel_y = self.height - 190
        panel_width = 370
        panel_height = 180
        pygame.draw.rect(screen, (40, 40, 40), (panel_x, panel_y, panel_width, panel_height))
        pygame.draw.rect(screen, (80, 80, 80), (panel_x, panel_y, panel_width, panel_height), 2)
        
        # Instructions
        font_small = pygame.font.Font(None, 24)
        instructions = [
            "Instructions:",
            "",
            "• Click on canvas to add cities",
            f"• Current cities: {len(self.cities)}/50",
            "• Click number to type, or use +/-",
            "• Generate random/circle/clustered",
            "• Clear to remove all cities",
        ]
        for i, line in enumerate(instructions):
            color = (200, 200, 200) if i == 0 else (180, 180, 180)
            text = font_small.render(line, True, color)
            screen.blit(text, (panel_x + 10, panel_y + 10 + i * 25))

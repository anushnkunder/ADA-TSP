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
        
        # Zoom and pan
        self.zoom = 1.0
        self.pan_x = 0
        self.pan_y = 0
        self.panning = False
        self.pan_start = (0, 0)
        
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
                # Convert screen coordinates to world coordinates
                world_x = (pos[0] - self.pan_x) / self.zoom
                world_y = (pos[1] - self.pan_y) / self.zoom
                self.cities.append(City(world_x, world_y, self.next_id))
                self.next_id += 1
    
    def handle_mouse_button(self, event):
        """Handle mouse button events for panning (trackpad friendly)."""
        # Support both middle mouse (button 2) and right mouse (button 3) for panning
        if event.button in [2, 3]:  # Middle or right mouse button
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.panning = True
                self.pan_start = event.pos
            elif event.type == pygame.MOUSEBUTTONUP:
                self.panning = False
    
    def handle_mouse_motion(self, event):
        """Handle mouse motion for panning."""
        if self.panning:
            dx = event.pos[0] - self.pan_start[0]
            dy = event.pos[1] - self.pan_start[1]
            self.pan_x += dx
            self.pan_y += dy
            self.pan_start = event.pos
    
    def handle_mouse_wheel(self, event):
        """Handle mouse wheel for zooming."""
        if event.y > 0:  # Scroll up - zoom in
            self.zoom = min(3.0, self.zoom * 1.1)
        elif event.y < 0:  # Scroll down - zoom out
            self.zoom = max(0.5, self.zoom / 1.1)
    
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
        """Draw the playground tab with visual effects and zoom."""
        # Draw canvas area with gradient
        pygame.draw.rect(screen, (40, 40, 40), (0, 0, self.width, self.height - 200))
        
        # Draw grid pattern for better depth (with zoom)
        grid_color = (45, 45, 45)
        grid_spacing = int(50 * self.zoom)
        
        # Calculate grid offset based on pan
        offset_x = int(self.pan_x % grid_spacing)
        offset_y = int(self.pan_y % grid_spacing)
        
        for x in range(offset_x, self.width, grid_spacing):
            pygame.draw.line(screen, grid_color, (x, 0), (x, self.height - 200), 1)
        for y in range(offset_y, self.height - 200, grid_spacing):
            pygame.draw.line(screen, grid_color, (0, y), (self.width, y), 1)
        
        # Draw cities with glow effect (with zoom and pan)
        for city in self.cities:
            # Convert world coordinates to screen coordinates
            screen_x = int(city.x * self.zoom + self.pan_x)
            screen_y = int(city.y * self.zoom + self.pan_y)
            
            # Skip if outside visible area
            if screen_x < -20 or screen_x > self.width + 20:
                continue
            if screen_y < -20 or screen_y > self.height - 180:
                continue
            
            # Scale radius with zoom
            base_radius = int(6 * self.zoom)
            
            # Glow effect (simplified)
            pygame.draw.circle(screen, (80, 80, 80), (screen_x, screen_y), base_radius + 3)
            pygame.draw.circle(screen, (120, 120, 120), (screen_x, screen_y), base_radius + 2)
            
            # Main city circle with gradient
            pygame.draw.circle(screen, (200, 200, 200), (screen_x, screen_y), base_radius + 1)
            pygame.draw.circle(screen, (255, 255, 255), (screen_x, screen_y), base_radius)
            pygame.draw.circle(screen, (100, 150, 255), (screen_x, screen_y), max(2, base_radius - 2))
            
            # City ID with shadow (only if zoomed in enough)
            if self.zoom > 0.7:
                font_size = max(16, int(20 * self.zoom))
                font = pygame.font.Font(None, font_size)
                text = font.render(str(city.id), True, (0, 0, 0))
                screen.blit(text, (screen_x + 11, screen_y - 9))
                text = font.render(str(city.id), True, (255, 255, 255))
                screen.blit(text, (screen_x + 10, screen_y - 10))
        
        # Draw control panel with gradient
        panel_rect = pygame.Rect(0, self.height - 200, self.width, 200)
        pygame.draw.rect(screen, (30, 30, 30), panel_rect)
        # Top border highlight
        pygame.draw.line(screen, (60, 60, 60), (0, self.height - 200), (self.width, self.height - 200), 2)
        
        # Section 1: Preset Generation
        font_label = pygame.font.Font(None, 22)
        label = font_label.render("Generate Presets:", True, (180, 180, 180))
        screen.blit(label, (20, self.height - 190))
        
        # Draw preset buttons with hover and shadow
        font = pygame.font.Font(None, 28)
        mouse_pos = pygame.mouse.get_pos()
        adjusted_mouse = (mouse_pos[0], mouse_pos[1] - 40)  # Adjust for tab offset
        
        for name in ['random', 'circle', 'clustered']:
            rect = self.buttons[name]
            is_hover = rect.collidepoint(adjusted_mouse)
            
            # Shadow
            shadow_rect = rect.copy()
            shadow_rect.y += 2
            pygame.draw.rect(screen, (10, 10, 10), shadow_rect)
            
            # Button with hover effect
            color = (90, 90, 90) if is_hover else (70, 70, 70)
            pygame.draw.rect(screen, color, rect, border_radius=5)
            pygame.draw.rect(screen, (100, 100, 100), rect, 2, border_radius=5)
            
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
        
        # Section 3: Clear button with red theme
        clear_rect = self.buttons['clear']
        is_hover_clear = clear_rect.collidepoint(adjusted_mouse)
        
        # Shadow
        shadow_rect = clear_rect.copy()
        shadow_rect.y += 2
        pygame.draw.rect(screen, (10, 10, 10), shadow_rect)
        
        color = (150, 60, 60) if is_hover_clear else (120, 50, 50)
        pygame.draw.rect(screen, color, clear_rect, border_radius=5)
        pygame.draw.rect(screen, (180, 80, 80), clear_rect, 2, border_radius=5)
        text = font.render("Clear", True, (255, 255, 255))
        text_rect = text.get_rect(center=clear_rect.center)
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
            "• Scroll: Zoom in/out",
            "• Right-click drag: Pan view",
            f"• Zoom: {self.zoom:.1f}x",
        ]
        for i, line in enumerate(instructions):
            color = (200, 200, 200) if i == 0 else (180, 180, 180)
            text = font_small.render(line, True, color)
            screen.blit(text, (panel_x + 10, panel_y + 10 + i * 25))

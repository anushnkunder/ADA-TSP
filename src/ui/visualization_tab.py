import pygame
import time
from algorithms.brute_force import BruteForceTSP
from algorithms.nearest_neighbor import NearestNeighborTSP
from algorithms.two_opt import TwoOptTSP

class VisualizationTab:
    """Tab for visualizing algorithm execution step-by-step (optimized)."""
    
    def __init__(self, width, height, cities):
        self.width = width
        self.height = height
        self.cities = cities
        self.algorithm = None
        self.generator = None
        self.running = False
        self.selected_algo = "Nearest Neighbor"
        self.start_time = None
        self.elapsed_time = 0
        self.speed = 1  # Steps per frame (can be fractional)
        self.speed_index = 3  # Index in speed_options
        self.speed_options = [0.25, 0.5, 0.75, 1, 2, 4, 8, 16]
        self.completed = False
        self.frame_counter = 0  # For fractional speeds
        
        # UI elements
        self.buttons = {
            'start': pygame.Rect(20, height - 150, 100, 35),
            'pause': pygame.Rect(130, height - 150, 100, 35),
            'step': pygame.Rect(240, height - 150, 100, 35),
            'reset': pygame.Rect(350, height - 150, 100, 35),
        }
        
        self.algo_buttons = {
            'Brute Force': pygame.Rect(20, height - 110, 140, 30),
            'Nearest Neighbor': pygame.Rect(170, height - 110, 180, 30),
            '2-Opt': pygame.Rect(360, height - 110, 90, 30),
        }
        
        # Speed control
        self.speed_buttons = {
            'slow': pygame.Rect(470, height - 150, 60, 30),
            'fast': pygame.Rect(540, height - 150, 60, 30),
        }
        
    def handle_click(self, pos):
        """Handle mouse clicks."""
        if self.buttons['start'].collidepoint(pos):
            self.start()
        elif self.buttons['pause'].collidepoint(pos):
            self.running = False
        elif self.buttons['step'].collidepoint(pos):
            self.step()
        elif self.buttons['reset'].collidepoint(pos):
            self.reset()
        
        # Speed control
        if self.speed_buttons['slow'].collidepoint(pos):
            if self.speed_index > 0:
                self.speed_index -= 1
                self.speed = self.speed_options[self.speed_index]
        elif self.speed_buttons['fast'].collidepoint(pos):
            if self.speed_index < len(self.speed_options) - 1:
                self.speed_index += 1
                self.speed = self.speed_options[self.speed_index]
        
        # Algorithm selection
        for name, rect in self.algo_buttons.items():
            if rect.collidepoint(pos):
                self.selected_algo = name
                self.reset()
    
    def start(self):
        """Start algorithm execution."""
        if self.generator is None:
            self.reset()
        self.running = True
        if self.start_time is None:
            self.start_time = time.time()
    
    def step(self):
        """Execute one step of the algorithm."""
        if self.generator is None:
            self.reset()
        try:
            next(self.generator)
            if self.start_time is None:
                self.start_time = time.time()
            self.elapsed_time = time.time() - self.start_time
        except StopIteration:
            self.running = False
    
    def reset(self):
        """Reset algorithm state."""
        self.running = False
        self.start_time = None
        self.elapsed_time = 0
        self.completed = False
        
        if self.selected_algo == "Brute Force":
            self.algorithm = BruteForceTSP(self.cities)
        elif self.selected_algo == "Nearest Neighbor":
            self.algorithm = NearestNeighborTSP(self.cities)
        elif self.selected_algo == "2-Opt":
            nn = NearestNeighborTSP(self.cities)
            initial_route = nn.solve()
            self.algorithm = TwoOptTSP(initial_route)
        
        self.generator = self.algorithm.solve_generator()
    
    def update(self):
        """Update algorithm state if running (optimized with speed control)."""
        if self.running and not self.completed:
            if self.speed >= 1:
                # Fast speed: execute multiple steps per frame
                for _ in range(int(self.speed)):
                    try:
                        next(self.generator)
                        self.elapsed_time = time.time() - self.start_time
                    except StopIteration:
                        self.running = False
                        self.completed = True
                        break
            else:
                # Slow speed: execute one step every N frames
                self.frame_counter += self.speed
                if self.frame_counter >= 1:
                    self.frame_counter -= 1
                    try:
                        next(self.generator)
                        self.elapsed_time = time.time() - self.start_time
                    except StopIteration:
                        self.running = False
                        self.completed = True
    
    def draw(self, screen):
        """Draw the visualization tab."""
        # Draw canvas
        pygame.draw.rect(screen, (40, 40, 40), (0, 0, self.width, self.height - 200))
        
        # Draw cities
        for city in self.cities:
            pygame.draw.circle(screen, (255, 255, 255), (city.x, city.y), 6)
        
        # Draw current algorithm state
        if self.algorithm:
            self.draw_algorithm_state(screen)
        
        # Draw legend for current algorithm
        self.draw_legend(screen)
        
        # Draw control panel
        pygame.draw.rect(screen, (30, 30, 30), (0, self.height - 200, self.width, 200))
        
        # Draw buttons (reorganized for better spacing)
        font = pygame.font.Font(None, 26)
        for name, rect in self.buttons.items():
            color = (70, 120, 70) if name == 'start' and self.running else (70, 70, 70)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (100, 100, 100), rect, 2)
            text = font.render(name.capitalize(), True, (255, 255, 255))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)
        
        # Draw algorithm selection label
        font_label = pygame.font.Font(None, 22)
        label = font_label.render("Algorithm:", True, (180, 180, 180))
        screen.blit(label, (20, self.height - 135))
        
        # Draw algorithm selection
        font_small = pygame.font.Font(None, 24)
        for name, rect in self.algo_buttons.items():
            color = (70, 100, 150) if name == self.selected_algo else (60, 60, 60)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (100, 100, 100), rect, 2)
            text = font_small.render(name, True, (255, 255, 255))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)
        
        # Draw speed control label
        label = font_label.render("Speed:", True, (180, 180, 180))
        screen.blit(label, (470, self.height - 175))
        
        # Draw speed control
        for name, rect in self.speed_buttons.items():
            pygame.draw.rect(screen, (60, 60, 60), rect)
            pygame.draw.rect(screen, (100, 100, 100), rect, 2)
            text = font_small.render(name.capitalize(), True, (255, 255, 255))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)
        
        # Draw speed indicator
        speed_text = font_small.render(f"{self.speed}x", True, (200, 200, 200))
        screen.blit(speed_text, (610, self.height - 170))
        
        # Draw metrics
        self.draw_metrics(screen)
    
    def draw_legend(self, screen):
        """Draw color legend for current algorithm."""
        font_small = pygame.font.Font(None, 20)
        legend_x = 20
        legend_y = 20
        
        legends = []
        if isinstance(self.algorithm, NearestNeighborTSP):
            legends = [
                ("Yellow lines", (255, 255, 0), "= Path built so far"),
                ("Green circle", (0, 255, 0), "= Current city"),
            ]
        elif isinstance(self.algorithm, BruteForceTSP):
            legends = [
                ("Green lines", (0, 255, 0), "= Best route found"),
                ("Gray lines", (80, 80, 80), "= Route being tested"),
            ]
        elif isinstance(self.algorithm, TwoOptTSP):
            legends = [
                ("Green lines", (0, 255, 0), "= Current route"),
                ("Red circles", (255, 0, 0), "= Edges being swapped"),
            ]
        
        for i, (label, color, desc) in enumerate(legends):
            y = legend_y + i * 25
            # Draw color indicator
            if "circle" in label.lower():
                pygame.draw.circle(screen, color, (legend_x + 10, y + 8), 6, 2)
            else:
                pygame.draw.line(screen, color, (legend_x, y + 8), (legend_x + 20, y + 8), 3)
            
            # Draw text
            text = font_small.render(f"{label} {desc}", True, (200, 200, 200))
            screen.blit(text, (legend_x + 30, y))
    
    def draw_algorithm_state(self, screen):
        """Draw current state of the algorithm."""
        if isinstance(self.algorithm, NearestNeighborTSP):
            # Draw path so far
            if len(self.algorithm.path) > 1:
                for i in range(len(self.algorithm.path) - 1):
                    city1 = self.algorithm.path[i]
                    city2 = self.algorithm.path[i + 1]
                    pygame.draw.line(screen, (255, 255, 0), (city1.x, city1.y), (city2.x, city2.y), 2)
            
            # Draw return line to start if route is complete
            if self.algorithm.route and len(self.algorithm.path) == len(self.cities):
                start_city = self.algorithm.path[0]
                end_city = self.algorithm.path[-1]
                pygame.draw.line(screen, (255, 255, 0), (end_city.x, end_city.y), (start_city.x, start_city.y), 2)
            
            # Highlight current city
            if self.algorithm.current_city:
                pygame.draw.circle(screen, (0, 255, 0), 
                                 (self.algorithm.current_city.x, self.algorithm.current_city.y), 10, 3)
        
        elif isinstance(self.algorithm, BruteForceTSP):
            # Draw best route found (green - thicker)
            if self.algorithm.best_route:
                cities = self.algorithm.best_route.cities
                for i in range(len(cities)):
                    city1 = cities[i]
                    city2 = cities[(i + 1) % len(cities)]
                    pygame.draw.line(screen, (0, 255, 0), (city1.x, city1.y), (city2.x, city2.y), 3)
            
            # Draw current route being tested (gray - thin, semi-transparent effect)
            # Only draw occasionally to reduce clutter
            if self.algorithm.current_route and self.algorithm.iterations % 10 == 0:
                cities = self.algorithm.current_route.cities
                for i in range(len(cities)):
                    city1 = cities[i]
                    city2 = cities[(i + 1) % len(cities)]
                    pygame.draw.line(screen, (80, 80, 80), (city1.x, city1.y), (city2.x, city2.y), 1)
        
        elif isinstance(self.algorithm, TwoOptTSP):
            # Draw current route
            if self.algorithm.route:
                cities = self.algorithm.route.cities
                for i in range(len(cities)):
                    city1 = cities[i]
                    city2 = cities[(i + 1) % len(cities)]
                    pygame.draw.line(screen, (0, 255, 0), (city1.x, city1.y), (city2.x, city2.y), 2)
            
            # Highlight edges being considered
            if self.algorithm.swap_i and self.algorithm.swap_j:
                i, j = self.algorithm.swap_i, self.algorithm.swap_j
                cities = self.algorithm.route.cities
                pygame.draw.circle(screen, (255, 0, 0), (cities[i].x, cities[i].y), 8, 2)
                pygame.draw.circle(screen, (255, 0, 0), (cities[j].x, cities[j].y), 8, 2)
    
    def draw_metrics(self, screen):
        """Draw performance metrics (optimized with progress bar)."""
        font = pygame.font.Font(None, 24)
        font_label = pygame.font.Font(None, 22)
        
        # Metrics panel background
        panel_x = self.width - 280
        panel_y = self.height - 190
        panel_width = 270
        panel_height = 180
        pygame.draw.rect(screen, (40, 40, 40), (panel_x, panel_y, panel_width, panel_height))
        pygame.draw.rect(screen, (80, 80, 80), (panel_x, panel_y, panel_width, panel_height), 2)
        
        # Title
        title = font_label.render("Metrics", True, (200, 200, 200))
        screen.blit(title, (panel_x + 10, panel_y + 5))
        
        # Metrics
        y_offset = panel_y + 30
        metrics = []
        
        if isinstance(self.algorithm, NearestNeighborTSP):
            if self.algorithm.route:
                metrics.append(f"Distance: {self.algorithm.route.distance:.2f}")
            metrics.append(f"Visited: {len(self.algorithm.visited)}/{len(self.cities)}")
        elif isinstance(self.algorithm, BruteForceTSP):
            if self.algorithm.best_route:
                metrics.append(f"Best: {self.algorithm.best_distance:.2f}")
            metrics.append(f"Checked: {self.algorithm.iterations}")
            if hasattr(self.algorithm, 'get_progress'):
                progress = self.algorithm.get_progress()
                metrics.append(f"Progress: {progress:.1f}%")
        elif isinstance(self.algorithm, TwoOptTSP):
            metrics.append(f"Distance: {self.algorithm.route.distance:.2f}")
            if hasattr(self.algorithm, 'improvement_count'):
                metrics.append(f"Swaps: {self.algorithm.improvement_count}")
        
        metrics.append(f"Time: {self.elapsed_time:.3f}s")
        
        if self.completed:
            metrics.append("Status: ✓ Completed")
        elif self.running:
            metrics.append("Status: Running...")
        else:
            metrics.append("Status: Paused")
        
        for i, metric in enumerate(metrics):
            text = font.render(metric, True, (220, 220, 220))
            screen.blit(text, (panel_x + 10, y_offset + i * 28))

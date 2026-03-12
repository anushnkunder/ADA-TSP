import pygame
import time
from algorithms.brute_force import BruteForceTSP
from algorithms.nearest_neighbor import NearestNeighborTSP
from algorithms.two_opt import TwoOptTSP

class VisualizationTab:
    """Tab for visualizing algorithm execution step-by-step."""
    
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
        """Update algorithm state if running."""
        if self.running:
            try:
                next(self.generator)
                self.elapsed_time = time.time() - self.start_time
            except StopIteration:
                self.running = False
    
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
        
        # Draw control panel
        pygame.draw.rect(screen, (30, 30, 30), (0, self.height - 200, self.width, 200))
        
        # Draw buttons
        font = pygame.font.Font(None, 26)
        for name, rect in self.buttons.items():
            color = (70, 120, 70) if name == 'start' and self.running else (70, 70, 70)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (100, 100, 100), rect, 2)
            text = font.render(name.capitalize(), True, (255, 255, 255))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)
        
        # Draw algorithm selection
        font_small = pygame.font.Font(None, 24)
        for name, rect in self.algo_buttons.items():
            color = (70, 100, 150) if name == self.selected_algo else (60, 60, 60)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (100, 100, 100), rect, 2)
            text = font_small.render(name, True, (255, 255, 255))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)
        
        # Draw metrics
        self.draw_metrics(screen)
    
    def draw_algorithm_state(self, screen):
        """Draw current state of the algorithm."""
        if isinstance(self.algorithm, NearestNeighborTSP):
            # Draw path so far
            if len(self.algorithm.path) > 1:
                for i in range(len(self.algorithm.path) - 1):
                    city1 = self.algorithm.path[i]
                    city2 = self.algorithm.path[i + 1]
                    pygame.draw.line(screen, (255, 255, 0), (city1.x, city1.y), (city2.x, city2.y), 2)
            
            # Highlight current city
            if self.algorithm.current_city:
                pygame.draw.circle(screen, (0, 255, 0), 
                                 (self.algorithm.current_city.x, self.algorithm.current_city.y), 10, 3)
        
        elif isinstance(self.algorithm, BruteForceTSP):
            # Draw best route found
            if self.algorithm.best_route:
                cities = self.algorithm.best_route.cities
                for i in range(len(cities)):
                    city1 = cities[i]
                    city2 = cities[(i + 1) % len(cities)]
                    pygame.draw.line(screen, (0, 255, 0), (city1.x, city1.y), (city2.x, city2.y), 2)
            
            # Draw current route being tested
            if self.algorithm.current_route:
                cities = self.algorithm.current_route.cities
                for i in range(len(cities)):
                    city1 = cities[i]
                    city2 = cities[(i + 1) % len(cities)]
                    pygame.draw.line(screen, (100, 100, 100), (city1.x, city1.y), (city2.x, city2.y), 1)
        
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
        """Draw performance metrics."""
        font = pygame.font.Font(None, 24)
        y_offset = self.height - 70
        
        metrics = []
        if isinstance(self.algorithm, NearestNeighborTSP) and self.algorithm.route:
            metrics.append(f"Distance: {self.algorithm.route.distance:.2f}")
        elif isinstance(self.algorithm, BruteForceTSP) and self.algorithm.best_route:
            metrics.append(f"Best Distance: {self.algorithm.best_distance:.2f}")
            metrics.append(f"Iterations: {self.algorithm.iterations}")
        elif isinstance(self.algorithm, TwoOptTSP):
            metrics.append(f"Distance: {self.algorithm.route.distance:.2f}")
        
        metrics.append(f"Time: {self.elapsed_time:.3f}s")
        
        for i, metric in enumerate(metrics):
            text = font.render(metric, True, (200, 200, 200))
            screen.blit(text, (500, y_offset + i * 25))

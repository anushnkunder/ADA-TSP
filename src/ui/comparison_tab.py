import pygame
import time
from algorithms.brute_force import BruteForceTSP
from algorithms.nearest_neighbor import NearestNeighborTSP
from algorithms.two_opt import TwoOptTSP

class ComparisonTab:
    """Tab for comparing all algorithms on the same city set."""
    
    def __init__(self, width, height, cities):
        self.width = width
        self.height = height
        self.cities = cities
        self.results = {}
        self.selected_display = None
        
        # Zoom and pan
        self.zoom = 1.0
        self.pan_x = 0
        self.pan_y = 0
        self.panning = False
        self.pan_start = (0, 0)
        
        # UI elements
        self.buttons = {
            'run_all': pygame.Rect(20, height - 150, 150, 40),
        }
        
    def handle_click(self, pos):
        """Handle mouse clicks."""
        if self.buttons['run_all'].collidepoint(pos):
            self.run_all_algorithms()
            return
        
        # Check if clicking on algorithm name to display route
        if not self.results:
            return
        
        # Calculate click areas based on table layout
        x_start = 200
        y_start = self.height - 185 + 30 + 32  # title + headers + separator
        
        algo_order = ['Brute Force', 'Nearest Neighbor', '2-Opt']
        row_index = 0
        for name in algo_order:
            if name in self.results:
                # Create clickable rect for each algorithm row
                rect = pygame.Rect(x_start - 5, y_start + row_index * 32 - 2, 420, 28)
                if rect.collidepoint(pos):
                    self.selected_display = name
                    return
                row_index += 1
    
    
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
    
    def world_to_screen(self, x, y):
        """Convert world coordinates to screen coordinates."""
        return (int(x * self.zoom + self.pan_x), int(y * self.zoom + self.pan_y))
    
    def run_all_algorithms(self):
        """Run all algorithms and store results."""
        self.results = {}
        
        if len(self.cities) == 0:
            return
        
        # Run Nearest Neighbor
        start = time.time()
        nn = NearestNeighborTSP(self.cities)
        nn_route = nn.solve()
        nn_time = time.time() - start
        self.results['Nearest Neighbor'] = {
            'route': nn_route,
            'distance': nn_route.distance,
            'time': nn_time
        }
        
        # Run 2-Opt (using NN as initial solution)
        start = time.time()
        two_opt = TwoOptTSP(nn_route)
        opt_route = two_opt.solve()
        opt_time = time.time() - start
        self.results['2-Opt'] = {
            'route': opt_route,
            'distance': opt_route.distance,
            'time': opt_time + nn_time  # Include NN time
        }
        
        # Run Brute Force only if cities <= 10
        if len(self.cities) <= 10:
            start = time.time()
            bf = BruteForceTSP(self.cities)
            bf_route = bf.solve()
            bf_time = time.time() - start
            self.results['Brute Force'] = {
                'route': bf_route,
                'distance': bf_route.distance,
                'time': bf_time
            }
        
        self.selected_display = 'Nearest Neighbor'
    
    def draw(self, screen):
        """Draw the comparison tab with visual effects."""
        # Draw canvas with gradient
        pygame.draw.rect(screen, (40, 40, 40), (0, 0, self.width, self.height - 200))
        
        # Draw grid
        grid_color = (45, 45, 45)
        for x in range(0, self.width, 50):
            pygame.draw.line(screen, grid_color, (x, 0), (x, self.height - 200), 1)
        for y in range(0, self.height - 200, 50):
            pygame.draw.line(screen, grid_color, (0, y), (self.width, y), 1)
        
        # Draw selected route with glow
        if self.selected_display and self.selected_display in self.results:
            route = self.results[self.selected_display]['route']
            cities = route.cities
            
            # Route colors
            colors = {
                'Brute Force': (0, 255, 0),
                'Nearest Neighbor': (255, 255, 0),
                '2-Opt': (0, 200, 255)
            }
            color = colors.get(self.selected_display, (255, 255, 255))
            
            # Draw route with glow effect (simplified)
            for i in range(len(cities)):
                city1 = cities[i]
                city2 = cities[(i + 1) % len(cities)]
                
                x1, y1 = self.world_to_screen(city1.x, city1.y)
                x2, y2 = self.world_to_screen(city2.x, city2.y)
                
                # Glow layers
                dark_color = tuple(c // 3 for c in color)
                line_width = max(4, int(6 * self.zoom))
                pygame.draw.line(screen, dark_color, (x1, y1), (x2, y2), line_width)
                line_width = max(2, int(3 * self.zoom))
                pygame.draw.line(screen, color, (x1, y1), (x2, y2), line_width)
        
        # Draw cities with glow
        for city in self.cities:
            screen_x, screen_y = self.world_to_screen(city.x, city.y)
            
            # Skip if outside visible area
            if screen_x < -20 or screen_x > self.width + 20:
                continue
            if screen_y < -20 or screen_y > self.height - 180:
                continue
            
            base_radius = max(4, int(6 * self.zoom))
            
            # Glow (simplified)
            pygame.draw.circle(screen, (80, 80, 80), (screen_x, screen_y), base_radius + 3)
            pygame.draw.circle(screen, (120, 120, 120), (screen_x, screen_y), base_radius + 2)
            
            pygame.draw.circle(screen, (200, 200, 200), (screen_x, screen_y), base_radius + 1)
            pygame.draw.circle(screen, (255, 255, 255), (screen_x, screen_y), base_radius)
        
        # Draw control panel with gradient
        pygame.draw.rect(screen, (30, 30, 30), (0, self.height - 200, self.width, 200))
        pygame.draw.line(screen, (60, 60, 60), (0, self.height - 200), (self.width, self.height - 200), 2)
        
        # Draw run button with hover and shadow
        font = pygame.font.Font(None, 28)
        mouse_pos = pygame.mouse.get_pos()
        adjusted_mouse = (mouse_pos[0], mouse_pos[1] - 40)
        
        run_rect = self.buttons['run_all']
        is_hover = run_rect.collidepoint(adjusted_mouse)
        
        # Shadow
        shadow_rect = run_rect.copy()
        shadow_rect.y += 2
        pygame.draw.rect(screen, (10, 10, 10), shadow_rect)
        
        # Button
        color = (90, 150, 90) if is_hover else (70, 120, 70)
        pygame.draw.rect(screen, color, run_rect, border_radius=5)
        pygame.draw.rect(screen, (100, 180, 100), run_rect, 2, border_radius=5)
        
        text = font.render("Run All", True, (255, 255, 255))
        text_rect = text.get_rect(center=run_rect.center)
        screen.blit(text, text_rect)
        
        # Draw results table
        self.draw_results_table(screen)
    
    def draw_results_table(self, screen):
        """Draw comparison results table (improved layout)."""
        if not self.results:
            font = pygame.font.Font(None, 28)
            text = font.render("Click 'Run All' to compare algorithms", True, (200, 200, 200))
            text_rect = text.get_rect(center=(self.width // 2, self.height - 100))
            screen.blit(text, text_rect)
            return
        
        font = pygame.font.Font(None, 24)
        font_bold = pygame.font.Font(None, 28)
        font_label = pygame.font.Font(None, 22)
        
        # Table position - moved higher
        x_start = 200
        y_start = self.height - 185
        col_widths = [200, 120, 100]
        
        # Table background
        table_width = sum(col_widths) + 20
        table_height = 175
        pygame.draw.rect(screen, (40, 40, 40), (x_start - 10, y_start - 10, table_width, table_height))
        pygame.draw.rect(screen, (80, 80, 80), (x_start - 10, y_start - 10, table_width, table_height), 2)
        
        # Table title
        title = font_bold.render("Algorithm Comparison", True, (220, 220, 220))
        screen.blit(title, (x_start, y_start))
        
        # Table headers
        y_start += 30
        headers = ["Algorithm", "Distance", "Time (s)"]
        
        for i, header in enumerate(headers):
            x = x_start + sum(col_widths[:i])
            text = font_bold.render(header, True, (200, 200, 200))
            screen.blit(text, (x, y_start))
        
        # Separator line
        pygame.draw.line(screen, (100, 100, 100), 
                        (x_start, y_start + 25), 
                        (x_start + sum(col_widths), y_start + 25), 2)
        
        # Table rows - with better spacing
        y_offset = y_start + 32
        algo_order = ['Brute Force', 'Nearest Neighbor', '2-Opt']
        
        for algo in algo_order:
            if algo not in self.results:
                continue
            
            result = self.results[algo]
            
            # Highlight selected
            if algo == self.selected_display:
                pygame.draw.rect(screen, (60, 80, 100), 
                               (x_start - 5, y_offset - 2, sum(col_widths) + 10, 28))
            
            # Algorithm name (clickable)
            color = (150, 255, 150) if algo == self.selected_display else (220, 220, 220)
            text = font.render(algo, True, color)
            screen.blit(text, (x_start, y_offset))
            
            # Distance
            text = font.render(f"{result['distance']:.2f}", True, (220, 220, 220))
            screen.blit(text, (x_start + col_widths[0], y_offset))
            
            # Time
            text = font.render(f"{result['time']:.4f}", True, (220, 220, 220))
            screen.blit(text, (x_start + col_widths[0] + col_widths[1], y_offset))
            
            y_offset += 32
        
        # Instructions - moved up
        font_small = pygame.font.Font(None, 18)
        text = font_small.render("Click algorithm name to view route", True, (150, 150, 150))
        screen.blit(text, (x_start, y_offset + 3))
        
        # Legend panel (right side)
        legend_x = x_start + table_width + 40
        legend_y = self.height - 185
        legend_width = 260
        legend_height = 175
        
        pygame.draw.rect(screen, (40, 40, 40), (legend_x, legend_y, legend_width, legend_height))
        pygame.draw.rect(screen, (80, 80, 80), (legend_x, legend_y, legend_width, legend_height), 2)
        
        # Legend title
        title = font_label.render("Route Colors:", True, (200, 200, 200))
        screen.blit(title, (legend_x + 10, legend_y + 10))
        
        # Color legend
        colors = {
            'Brute Force': (0, 255, 0),
            'Nearest Neighbor': (255, 255, 0),
            '2-Opt': (0, 200, 255)
        }
        
        y_pos = legend_y + 40
        for algo, color in colors.items():
            if algo in self.results:
                # Color box
                pygame.draw.rect(screen, color, (legend_x + 15, y_pos, 30, 20))
                pygame.draw.rect(screen, (100, 100, 100), (legend_x + 15, y_pos, 30, 20), 1)
                
                # Algorithm name
                text = font.render(algo, True, (220, 220, 220))
                screen.blit(text, (legend_x + 55, y_pos))
                
                y_pos += 32
        
        # Note about Brute Force
        if 'Brute Force' not in self.results and len(self.cities) > 10:
            note = font_small.render("Note: Brute Force skipped (>10 cities)", True, (200, 150, 150))
            screen.blit(note, (legend_x + 10, y_pos + 5))

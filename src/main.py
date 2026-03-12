import pygame
import sys
sys.path.insert(0, '.')

from ui.playground_tab import PlaygroundTab
from ui.visualization_tab import VisualizationTab
from ui.comparison_tab import ComparisonTab

class TSPSimulator:
    """Main application with tabbed interface."""
    
    def __init__(self):
        pygame.init()
        self.width = 1400
        self.height = 900
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("TSP Simulator - ADA Project")
        self.clock = pygame.time.Clock()
        
        # Tabs
        self.current_tab = 0
        self.tab_names = ["Playground", "Visualization", "Comparison"]
        
        # Initialize tabs
        self.playground = PlaygroundTab(self.width, self.height)
        self.visualization = None
        self.comparison = None
        
        # Tab buttons
        self.tab_buttons = []
        tab_width = 150
        for i in range(3):
            self.tab_buttons.append(pygame.Rect(i * tab_width, 0, tab_width, 40))
    
    def handle_events(self):
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                # Pass keyboard events to playground tab
                if self.current_tab == 0:
                    self.playground.handle_keypress(event)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                
                # Check tab buttons
                for i, rect in enumerate(self.tab_buttons):
                    if rect.collidepoint(pos):
                        self.switch_tab(i)
                        continue
                
                # Pass click to current tab
                adjusted_pos = (pos[0], pos[1] - 40)
                if self.current_tab == 0:
                    self.playground.handle_click(adjusted_pos)
                elif self.current_tab == 1 and self.visualization:
                    self.visualization.handle_click(adjusted_pos)
                elif self.current_tab == 2 and self.comparison:
                    self.comparison.handle_click(adjusted_pos)
        
        return True
    
    def switch_tab(self, tab_index):
        """Switch to a different tab."""
        self.current_tab = tab_index
        
        # Initialize visualization tab with current cities
        if tab_index == 1:
            if len(self.playground.cities) == 0:
                print("Please create cities in Playground first!")
                self.current_tab = 0
                return
            self.visualization = VisualizationTab(
                self.width, self.height, self.playground.cities
            )
        
        # Initialize comparison tab with current cities
        elif tab_index == 2:
            if len(self.playground.cities) == 0:
                print("Please create cities in Playground first!")
                self.current_tab = 0
                return
            self.comparison = ComparisonTab(
                self.width, self.height, self.playground.cities
            )
    
    def update(self):
        """Update current tab state."""
        if self.current_tab == 1 and self.visualization:
            self.visualization.update()
    
    def draw(self):
        """Draw the current tab."""
        self.screen.fill((20, 20, 20))
        
        # Draw tab buttons
        font = pygame.font.Font(None, 28)
        for i, (name, rect) in enumerate(zip(self.tab_names, self.tab_buttons)):
            color = (70, 100, 150) if i == self.current_tab else (50, 50, 50)
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, (100, 100, 100), rect, 2)
            text = font.render(name, True, (255, 255, 255))
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)
        
        # Create surface for tab content
        tab_surface = pygame.Surface((self.width, self.height - 40))
        
        # Draw current tab
        if self.current_tab == 0:
            self.playground.draw(tab_surface)
        elif self.current_tab == 1 and self.visualization:
            self.visualization.draw(tab_surface)
        elif self.current_tab == 2 and self.comparison:
            self.comparison.draw(tab_surface)
        
        # Blit tab content below tab buttons
        self.screen.blit(tab_surface, (0, 40))
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop."""
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)  # 60 FPS
        
        pygame.quit()

if __name__ == "__main__":
    app = TSPSimulator()
    app.run()

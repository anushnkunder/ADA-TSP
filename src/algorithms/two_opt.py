from models.route import Route
from utils import euclidean_distance

class TwoOptTSP:
    """2-Opt local search improvement for TSP."""
    
    def __init__(self, initial_route):
        self.route = Route(list(initial_route.cities))
        self.improved = False
        self.swap_i = None
        self.swap_j = None
        
    def solve_generator(self):
        """Generator that yields state after each improvement check."""
        improved = True
        
        while improved:
            improved = False
            n = len(self.route.cities)
            
            for i in range(1, n - 1):
                for j in range(i + 1, n):
                    self.swap_i = i
                    self.swap_j = j
                    
                    # Calculate current distance
                    current_dist = (
                        euclidean_distance(self.route.cities[i-1], self.route.cities[i]) +
                        euclidean_distance(self.route.cities[j], self.route.cities[(j+1) % n])
                    )
                    
                    # Calculate distance after swap
                    new_dist = (
                        euclidean_distance(self.route.cities[i-1], self.route.cities[j]) +
                        euclidean_distance(self.route.cities[i], self.route.cities[(j+1) % n])
                    )
                    
                    if new_dist < current_dist:
                        # Perform 2-opt swap
                        self.route.cities[i:j+1] = reversed(self.route.cities[i:j+1])
                        self.route._distance = None  # Reset cached distance
                        improved = True
                        self.improved = True
                        yield
                    else:
                        yield
            
            if not improved:
                self.swap_i = None
                self.swap_j = None
    
    def solve(self):
        """Solve completely without visualization."""
        for _ in self.solve_generator():
            pass
        return self.route

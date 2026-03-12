import itertools
from models.route import Route

class BruteForceTSP:
    """Brute force TSP solver - tries all permutations (optimized)."""
    
    def __init__(self, cities):
        self.cities = cities
        self.best_route = None
        self.best_distance = float('inf')
        self.current_route = None
        self.iterations = 0
        self.total_permutations = 0
        
        # Pre-calculate total permutations for progress tracking
        if len(cities) > 1:
            import math
            self.total_permutations = math.factorial(len(cities) - 1)
        
    def solve_generator(self):
        """Generator that yields state after each permutation check."""
        if len(self.cities) < 2:
            self.best_route = Route(self.cities)
            yield
            return
        
        # Fix first city to reduce permutations by n
        first_city = self.cities[0]
        remaining = self.cities[1:]
        
        for perm in itertools.permutations(remaining):
            route_cities = [first_city] + list(perm)
            self.current_route = Route(route_cities)
            self.iterations += 1
            
            current_distance = self.current_route.distance
            if current_distance < self.best_distance:
                self.best_distance = current_distance
                self.best_route = self.current_route
            
            yield  # Pause here for visualization
    
    def solve(self):
        """Solve completely without visualization."""
        for _ in self.solve_generator():
            pass
        return self.best_route
    
    def get_progress(self):
        """Get completion percentage."""
        if self.total_permutations == 0:
            return 100
        return (self.iterations / self.total_permutations) * 100

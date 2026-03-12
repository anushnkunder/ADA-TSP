from models.route import Route
from utils import euclidean_distance_squared
import math

class NearestNeighborTSP:
    """Nearest Neighbor greedy TSP solver (optimized)."""
    
    def __init__(self, cities):
        self.cities = cities
        self.route = None
        self.current_city = None
        self.visited = set()
        self.path = []
        self.unvisited = None
        
    def solve_generator(self):
        """Generator that yields state after each city selection."""
        if not self.cities:
            return
        
        # Start at first city
        self.current_city = self.cities[0]
        self.visited.add(self.current_city)
        self.path.append(self.current_city)
        self.unvisited = set(self.cities) - self.visited
        yield
        
        # Visit remaining cities (optimized with unvisited set)
        while self.unvisited:
            nearest = None
            min_distance_sq = float('inf')
            
            # Find nearest unvisited city using squared distance
            for city in self.unvisited:
                dist_sq = euclidean_distance_squared(self.current_city, city)
                if dist_sq < min_distance_sq:
                    min_distance_sq = dist_sq
                    nearest = city
            
            # Move to nearest city
            self.current_city = nearest
            self.visited.add(nearest)
            self.unvisited.remove(nearest)
            self.path.append(nearest)
            yield
        
        # Create final route
        self.route = Route(self.path)
    
    def solve(self):
        """Solve completely without visualization."""
        for _ in self.solve_generator():
            pass
        return self.route

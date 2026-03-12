from models.route import Route
from utils import euclidean_distance

class NearestNeighborTSP:
    """Nearest Neighbor greedy TSP solver."""
    
    def __init__(self, cities):
        self.cities = cities
        self.route = None
        self.current_city = None
        self.visited = set()
        self.path = []
        
    def solve_generator(self):
        """Generator that yields state after each city selection."""
        if not self.cities:
            return
        
        # Start at first city
        self.current_city = self.cities[0]
        self.visited.add(self.current_city)
        self.path.append(self.current_city)
        yield
        
        # Visit remaining cities
        while len(self.visited) < len(self.cities):
            nearest = None
            min_distance = float('inf')
            
            # Find nearest unvisited city
            for city in self.cities:
                if city not in self.visited:
                    dist = euclidean_distance(self.current_city, city)
                    if dist < min_distance:
                        min_distance = dist
                        nearest = city
            
            # Move to nearest city
            self.current_city = nearest
            self.visited.add(nearest)
            self.path.append(nearest)
            yield
        
        # Create final route
        self.route = Route(self.path)
    
    def solve(self):
        """Solve completely without visualization."""
        for _ in self.solve_generator():
            pass
        return self.route

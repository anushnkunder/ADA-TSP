import math
from models.city import City

class Route:
    """Represents a TSP route with distance calculation."""
    
    def __init__(self, cities):
        self.cities = cities
        self._distance = None
    
    @property
    def distance(self):
        """Calculate total route distance (cached)."""
        if self._distance is None:
            self._distance = self.calculate_distance()
        return self._distance
    
    def calculate_distance(self):
        """Calculate Euclidean distance for the route (optimized)."""
        if len(self.cities) < 2:
            return 0
        
        total = 0
        cities = self.cities
        n = len(cities)
        
        # Optimized loop - avoid repeated list access
        for i in range(n):
            city1 = cities[i]
            city2 = cities[(i + 1) % n]
            dx = city2.x - city1.x
            dy = city2.y - city1.y
            total += math.sqrt(dx * dx + dy * dy)
        return total
    
    def __repr__(self):
        return f"Route(cities={len(self.cities)}, distance={self.distance:.2f})"

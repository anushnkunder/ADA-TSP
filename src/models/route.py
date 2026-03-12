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
        """Calculate Euclidean distance for the route."""
        if len(self.cities) < 2:
            return 0
        
        total = 0
        for i in range(len(self.cities)):
            city1 = self.cities[i]
            city2 = self.cities[(i + 1) % len(self.cities)]
            total += math.sqrt((city2.x - city1.x)**2 + (city2.y - city1.y)**2)
        return total
    
    def __repr__(self):
        return f"Route(cities={len(self.cities)}, distance={self.distance:.2f})"

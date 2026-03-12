class City:
    """Represents a city with coordinates and ID."""
    
    def __init__(self, x, y, city_id):
        self.x = x
        self.y = y
        self.id = city_id
    
    def __repr__(self):
        return f"City({self.id}: {self.x}, {self.y})"

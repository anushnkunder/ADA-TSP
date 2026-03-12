class City:
    """Represents a city with coordinates and ID."""
    
    __slots__ = ('x', 'y', 'id')  # Memory optimization
    
    def __init__(self, x, y, city_id):
        self.x = x
        self.y = y
        self.id = city_id
    
    def __repr__(self):
        return f"City({self.id}: {self.x}, {self.y})"
    
    def __hash__(self):
        """Make City hashable for set operations."""
        return hash((self.x, self.y, self.id))
    
    def __eq__(self, other):
        """Equality comparison for City objects."""
        if not isinstance(other, City):
            return False
        return self.id == other.id

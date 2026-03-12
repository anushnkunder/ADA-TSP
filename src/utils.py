import math
import random
from models.city import City

def euclidean_distance(city1, city2):
    """Calculate Euclidean distance between two cities (optimized)."""
    dx = city2.x - city1.x
    dy = city2.y - city1.y
    return math.sqrt(dx * dx + dy * dy)

def euclidean_distance_squared(city1, city2):
    """Calculate squared distance (faster, use for comparisons)."""
    dx = city2.x - city1.x
    dy = city2.y - city1.y
    return dx * dx + dy * dy

def generate_random_cities(count, width, height, margin=50):
    """Generate random cities within bounds."""
    cities = []
    for i in range(count):
        x = random.randint(margin, width - margin)
        y = random.randint(margin, height - margin)
        cities.append(City(x, y, i))
    return cities

def generate_circle_cities(count, width, height):
    """Generate cities arranged in a circle."""
    cities = []
    center_x, center_y = width // 2, height // 2
    radius = min(width, height) // 3
    
    for i in range(count):
        angle = 2 * math.pi * i / count
        x = int(center_x + radius * math.cos(angle))
        y = int(center_y + radius * math.sin(angle))
        cities.append(City(x, y, i))
    return cities

def generate_clustered_cities(count, width, height):
    """Generate cities in clusters."""
    cities = []
    clusters = 3
    cities_per_cluster = count // clusters
    
    for cluster in range(clusters):
        cx = random.randint(100, width - 100)
        cy = random.randint(100, height - 100)
        
        for i in range(cities_per_cluster):
            x = cx + random.randint(-80, 80)
            y = cy + random.randint(-80, 80)
            x = max(50, min(width - 50, x))
            y = max(50, min(height - 50, y))
            cities.append(City(x, y, len(cities)))
    
    # Add remaining cities
    remaining = count - len(cities)
    for i in range(remaining):
        x = random.randint(50, width - 50)
        y = random.randint(50, height - 50)
        cities.append(City(x, y, len(cities)))
    
    return cities

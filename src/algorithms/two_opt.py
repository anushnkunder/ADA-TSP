from models.route import Route
from utils import euclidean_distance_squared
import math

class TwoOptTSP:
    """2-Opt local search improvement for TSP (optimized)."""
    
    def __init__(self, initial_route):
        self.route = Route(list(initial_route.cities))
        self.improved = False
        self.swap_i = None
        self.swap_j = None
        self.improvement_count = 0
        
    def solve_generator(self):
        """Generator that yields state after each improvement check."""
        improved = True
        
        while improved:
            improved = False
            cities = self.route.cities
            n = len(cities)
            
            for i in range(1, n - 1):
                for j in range(i + 1, n):
                    self.swap_i = i
                    self.swap_j = j
                    
                    # Use squared distance for comparison (faster)
                    i_prev = i - 1
                    j_next = (j + 1) % n
                    
                    current_dist_sq = (
                        euclidean_distance_squared(cities[i_prev], cities[i]) +
                        euclidean_distance_squared(cities[j], cities[j_next])
                    )
                    
                    new_dist_sq = (
                        euclidean_distance_squared(cities[i_prev], cities[j]) +
                        euclidean_distance_squared(cities[i], cities[j_next])
                    )
                    
                    if new_dist_sq < current_dist_sq:
                        # Perform 2-opt swap
                        cities[i:j+1] = reversed(cities[i:j+1])
                        self.route._distance = None  # Reset cached distance
                        improved = True
                        self.improved = True
                        self.improvement_count += 1
                        yield
                    else:
                        yield
            
            if not improved:
                self.swap_i = None
                self.swap_j = None
    
    def solve(self):
        """Solve completely without visualization (optimized)."""
        improved = True
        
        while improved:
            improved = False
            cities = self.route.cities
            n = len(cities)
            
            for i in range(1, n - 1):
                for j in range(i + 1, n):
                    # Use squared distance for comparison (faster)
                    i_prev = i - 1
                    j_next = (j + 1) % n
                    
                    current_dist_sq = (
                        euclidean_distance_squared(cities[i_prev], cities[i]) +
                        euclidean_distance_squared(cities[j], cities[j_next])
                    )
                    
                    new_dist_sq = (
                        euclidean_distance_squared(cities[i_prev], cities[j]) +
                        euclidean_distance_squared(cities[i], cities[j_next])
                    )
                    
                    if new_dist_sq < current_dist_sq:
                        # Perform 2-opt swap
                        cities[i:j+1] = reversed(cities[i:j+1])
                        self.route._distance = None  # Reset cached distance
                        improved = True
                        self.improved = True
                        self.improvement_count += 1
        
        return self.route

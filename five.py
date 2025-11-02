import sys
import math
import collections

# Epsilon for floating-point comparisons
EPSILON = 1e-9

class Point:
    """Represents a point with utility for comparisons."""
    def __init__(self, x, y):
        # Rounding is applied aggressively here because the problem asks for 2 decimal places 
        # for intersection points, and floating point issues are critical.
        self.x = round(x, 10)
        self.y = round(y, 10)

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        if not isinstance(other, Point):
            return False
        return math.isclose(self.x, other.x, abs_tol=EPSILON) and \
               math.isclose(self.y, other.y, abs_tol=EPSILON)

    def __lt__(self, other):
        # Used for sorting/canonical representation
        if math.isclose(self.x, other.x, abs_tol=EPSILON):
            return self.y < other.y
        return self.x < other.x

    def dist_sq(self, other):
        return (self.x - other.x)**2 + (self.y - other.y)**2

    def dist(self, other):
        return math.sqrt(self.dist_sq(other))

class Stick:
    """Represents an original stick segment."""
    def __init__(self, p1, p2, index):
        self.p1 = p1
        self.p2 = p2
        self.length = p1.dist(p2)
        self.index = index

# --- GEOMETRIC HELPERS ---

def cross_product(p1, p2, p3):
    """Calculates the 2D cross product (p2-p1) x (p3-p1)."""
    return (p2.x - p1.x) * (p3.y - p1.y) - (p2.y - p1.y) * (p3.x - p1.x)

def on_segment(p, a, b):
    """Checks if point p lies on segment ab."""
    # Check collinearity and bounding box
    if math.fabs(cross_product(a, b, p)) > EPSILON:
        return False
    return (p.x >= min(a.x, b.x) - EPSILON and p.x <= max(a.x, b.x) + EPSILON and
            p.y >= min(a.y, b.y) - EPSILON and p.y <= max(a.y, b.y) + EPSILON)

def find_intersection(s1, s2):
    """
    Finds the intersection point between two line segments (s1.p1, s1.p2) and (s2.p1, s2.p2).
    Returns the intersection Point if it lies strictly on both segments, or None.
    """
    p1, p2 = s1.p1, s1.p2
    p3, p4 = s2.p1, s2.p2
    
    A = p2.y - p1.y
    B = p1.x - p2.x
    C = A * p1.x + B * p1.y

    D = p4.y - p3.y
    E = p3.x - p4.x
    F = D * p3.x + E * p3.y

    det = A * E - D * B

    if math.fabs(det) < EPSILON:
        # Lines are parallel or collinear. The problem implies simple intersection for the figure.
        return None

    x = (C * E - F * B) / det
    y = (A * F - D * C) / det
    
    intersection = Point(x, y)
    
    # Check if the intersection point lies on both segments
    if on_segment(intersection, p1, p2) and on_segment(intersection, p3, p4):
        # Exclude endpoints for counting purposes (unless it's an endpoint of the other stick)
        is_endpoint_s1 = intersection == p1 or intersection == p2
        is_endpoint_s2 = intersection == p3 or intersection == p4
        
        # We only count it as a new, internal vertex if it's strictly between the endpoints of at least one stick
        # (or if it coincides with an endpoint, it's still a vertex).
        if is_endpoint_s1 and is_endpoint_s2:
            # Intersection is an endpoint of both, already counted as a vertex.
            return None 

        return intersection

    return None

def shoelace_area(vertices):
    """Calculates the area of a polygon using the Shoelace formula."""
    if len(vertices) < 3:
        return 0.0
    
    area = 0.0
    for i in range(len(vertices)):
        p1 = vertices[i]
        p2 = vertices[(i + 1) % len(vertices)]
        area += (p1.x * p2.y - p2.x * p1.y)
        
    return math.fabs(area) / 2.0

# --- MAIN SOLVER ---

def solve():
    try:
        # Read N
        n_line = sys.stdin.readline().strip()
        if not n_line: return "Abandoned"
        N = int(n_line)
        
        # Read sticks
        sticks = []
        for i in range(N):
            line = sys.stdin.readline().strip()
            if not line: raise EOFError
            coords = list(map(int, line.split()))
            p1 = Point(coords[0], coords[1])
            p2 = Point(coords[2], coords[3])
            sticks.append(Stick(p1, p2, i))

    except Exception:
        return "Abandoned" # Handle incomplete or malformed input

    # 1. Identify all unique vertices (endpoints and intersections)
    vertices = set()
    for s in sticks:
        vertices.add(s.p1)
        vertices.add(s.p2)

    intersections = {} # Key: (stick_idx1, stick_idx2), Value: Point

    for i in range(N):
        for j in range(i + 1, N):
            p = find_intersection(sticks[i], sticks[j])
            if p:
                vertices.add(p)
                intersections[(i, j)] = p

    # Map Point object to a unique integer ID
    vertex_list = sorted(list(vertices))
    v_to_id = {v: i for i, v in enumerate(vertex_list)}
    num_v = len(vertex_list)
    
    # 2. Build the graph of connected segments
    # Adjacency list: adj[u] = list of (v, segment_length, stick_index)
    adj = collections.defaultdict(list)
    
    # This structure holds all segments that compose the graph.
    # Key: (stick_index, v1_id, v2_id), Value: length
    all_segments = {} 

    for stick_idx, s in enumerate(sticks):
        
        # Collect all vertices lying on the current stick (including endpoints)
        stick_vertices = {s.p1, s.p2}
        
        # Add internal intersection points
        for (i, j), p in intersections.items():
            if i == stick_idx or j == stick_idx:
                if on_segment(p, s.p1, s.p2):
                    stick_vertices.add(p)
        
        # Sort vertices along the stick to find sequential segments
        sorted_points = sorted(list(stick_vertices))
        
        for i in range(len(sorted_points) - 1):
            p_start = sorted_points[i]
            p_end = sorted_points[i+1]
            
            # Skip if the segment is negligibly short
            if p_start.dist(p_end) < EPSILON:
                continue

            u = v_to_id[p_start]
            v = v_to_id[p_end]
            length = p_start.dist(p_end)
            
            # Add segments to the adjacency list
            adj[u].append((v, length, stick_idx))
            adj[v].append((u, length, stick_idx))
            
            # Store the segment itself (for consumption tracking)
            # Use canonical representation (smaller ID first)
            seg_key = (stick_idx, min(u, v), max(u, v))
            all_segments[seg_key] = length


    # 3. Find the simple closed figure (DFS-based cycle detection)
    
    kalyan_cycle = [] # Stores the list of Point objects that form the cycle
    
    def dfs_cycle(u, start_node, path_ids, path_points):
        nonlocal kalyan_cycle

        for v_id, _, _ in adj[u]:
            if kalyan_cycle: return # Found a cycle, stop searching

            if v_id == start_node and len(path_ids) >= 3:
                # Found the closed figure
                kalyan_cycle = path_points + [vertex_list[start_node]]
                return

            if v_id not in path_ids:
                # Add current node/point and continue DFS
                dfs_cycle(v_id, start_node, path_ids + [v_id], path_points + [vertex_list[v_id]])
    
    # Start DFS from every vertex to find a cycle
    for start_id in range(num_v):
        if not kalyan_cycle:
            dfs_cycle(start_id, start_id, [start_id], [vertex_list[start_id]])
        else:
            break

    if not kalyan_cycle:
        return "Abandoned"

    # --- Game Logic ---

    # 4. Kalyan's Area and Perimeter
    kalyan_area = shoelace_area(kalyan_cycle)
    kalyan_perimeter = 0.0
    
    # 5. Computer's Available Length
    used_segments = set()
    
    # The cycle points are ordered (P0, P1, ..., Pk-1, P0)
    for i in range(len(kalyan_cycle) - 1):
        p_start = kalyan_cycle[i]
        p_end = kalyan_cycle[i+1]
        
        # Find which original stick this segment belongs to
        # A simple way is to check the adjacency list and find the minimum stick index 
        # that connects p_start and p_end.
        u = v_to_id[p_start]
        v = v_to_id[p_end]
        
        min_stick_idx = -1
        length = p_start.dist(p_end)
        
        for neighbor_v, seg_len, stick_idx in adj[u]:
            if neighbor_v == v and math.isclose(seg_len, length, abs_tol=EPSILON):
                # Found the segment. This segment may belong to multiple collinear sticks, 
                # but we just need one to identify the segment's key.
                if min_stick_idx == -1 or stick_idx < min_stick_idx:
                    min_stick_idx = stick_idx

        if min_stick_idx != -1:
            seg_key = (min_stick_idx, min(u, v), max(u, v))
            used_segments.add(seg_key)
            kalyan_perimeter += length
            
    # Total available material length (Computer's perimeter)
    total_stick_length = sum(s.length for s in sticks)
    kalyan_consumed_length = sum(all_segments[k] for k in used_segments)

    # Note: If a stick is partially used, only the used part is consumed.
    # The sum of all segment lengths in the graph should equal total_stick_length.
    # A cleaner approach is to use the initial perimeter vs the total stick length.
    
    # The problem description is complex: "only the portions that belong to the closed figure are considered part of it.
    # Any extra sticks or parts of a sticks that extend outside the closed figure can be cut off and used by the computer."
    
    # The length of the material available to the computer is:
    # (Total length of all sticks) - (Total length of segments forming the closed figure)
    
    # The cycle perimeter is NOT necessarily the total consumed length, as a segment might be traversed multiple times
    # in the graph if it's on a shared line, but in a simple cycle, it's traversed once.
    # The consumed length is the sum of the lengths of the unique segments forming the cycle.
    
    # kalyan_consumed_length calculation above is correct: it sums the lengths of the unique segments forming the cycle.
    computer_perimeter = total_stick_length - kalyan_consumed_length
    
    # 6. Computer's Max Area
    # Maximum area for a given perimeter (L) is achieved by a circle: A = L^2 / 4*pi
    if computer_perimeter < EPSILON:
        computer_area = 0.0
    else:
        computer_area = (computer_perimeter ** 2) / (4 * math.pi)

    # 7. Determine the Winner
    
    # The problem guarantees no tie, so simple comparison is enough.
    if kalyan_area > computer_area:
        return "Kalyan"
    else:
        return "Computer"

if __name__ == '__main__':
    result = solve()
    print(result)

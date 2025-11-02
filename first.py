import math
import sys

# Set a high recursion limit for potential deep calls, though not strictly needed here
# sys.setrecursionlimit(2000)

# Epsilon for floating-point comparisons
EPS = 1e-9

class P:
    """Represents a 2D point."""
    def __init__(self, x, y):
        self.x = x
        self.y = y

def area(p: list[P]) -> float:
    """
    Calculates the area of the polygon using the Shoelace formula.
    """
    A = 0.0
    n = len(p)
    for i in range(n):
        a = p[i]
        b = p[(i + 1) % n]
        A += a.x * b.y - b.x * a.y
    return math.fabs(A) / 2.0

def shrink(p: list[P], h: float) -> list[P]:
    """
    Shrinks the polygon 'p' inward by distance 'h'.
    Returns an empty list if the polygon collapses or offset lines are parallel.
    """
    n = len(p)
    r = []
    
    for i in range(n):
        # a: previous point, b: current point, c: next point
        a = p[(i - 1 + n) % n]
        b = p[i]
        c = p[(i + 1) % n]

        # Vector BA (from b to a)
        dx1 = a.x - b.x
        dy1 = a.y - b.y
        # Vector BC (from b to c)
        dx2 = c.x - b.x
        dy2 = c.y - b.y

        # Lengths of adjacent edges
        l1 = math.hypot(dx1, dy1)
        l2 = math.hypot(dx2, dy2)

        # Normalized vectors (unit length)
        # Handle division by zero if an edge length is near zero
        if l1 < EPS or l2 < EPS:
            return [] 
        
        dx1 /= l1
        dy1 /= l1
        dx2 /= l2
        dy2 /= l2

        # Compute the inward offset direction (Normal vectors)
        # Normal for segment BA: perpendicular to BA (Vector from b to a)
        nx1 = dy1
        ny1 = -dx1
        
        # Normal for segment BC: perpendicular to BC (Vector from b to c)
        nx2 = dy2
        ny2 = -dx2

        # New corner is the intersection of the two offset lines:
        # Line 1 (Offset of BC): Parallel to BC, passes through a point offset from B along normal of BC
        # Line equation A1*x + B1*y = C1
        A1 = dy2
        B1 = -dx2
        start1 = P(b.x + nx2 * h, b.y + ny2 * h)
        C1 = A1 * start1.x + B1 * start1.y

        # Line 2 (Offset of BA): Parallel to BA, passes through a point offset from B along normal of BA
        # Line equation A2*x + B2*y = C2
        A2 = dy1
        B2 = -dx1
        start2 = P(b.x + nx1 * h, b.y + ny1 * h)
        C2 = A2 * start2.x + B2 * start2.y
        
        # Solve 2x2 system using Cramer's rule
        D = A1 * B2 - A2 * B1

        # If D is near zero, the offset lines are parallel or collinear
        if math.fabs(D) < EPS:
            return [] 

        # Intersection point (new corner)
        newX = (C1 * B2 - C2 * B1) / D
        newY = (A1 * C2 - A2 * C1) / D
        
        r.append(P(newX, newY))
        
    return r

def main():
    try:
        # Read the number of corners N
        N = int(sys.stdin.readline().strip())
    except:
        return

    p = []
    # Read points
    for _ in range(N):
        try:
            line = sys.stdin.readline().strip()
            if not line: break
            x, y = map(float, line.split())
            p.append(P(x, y))
        except:
            break
            
    if len(p) != N:
        return # Exit if not enough points read

    maxVolume = 0.0
    
    # Iterate H in multiples of 0.1, up to the maximum possible coordinate (25)
    # 250 steps for 0.1 to 25.0
    for h_step in range(1, 251):
        h = h_step * 0.1

        # 1. Calculate the shrunk polygon
        innerPolygon = shrink(p, h)
        
        # If the shrink operation failed or the polygon collapsed
        if not innerPolygon:
            break
        
        # 2. Calculate the area of the shrunk polygon
        current_area = area(innerPolygon)
        
        # When the area becomes very small (polygon collapses), stop.
        if current_area < 1e-4:
            break
        
        # 3. Calculate volume and update max
        volume = current_area * h
        maxVolume = max(maxVolume, volume)

    # Output the maximum volume rounded to 2 decimal places
    print(f"{maxVolume:.2f}")

if __name__ == "__main__":
    main()

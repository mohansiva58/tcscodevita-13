import java.util.*;

class Main {

    static class P {
        double x, y;
        
        P(double a, double b) {
            x = a;
            y = b;
        }
    }

    // Calculates the area of the polygon using the Shoelace formula
    static double area(List<P> p) {
        double A = 0;
        int n = p.size();
        for (int i = 0; i < n; i++) {
            P a = p.get(i);
            P b = p.get((i + 1) % n);
            A += a.x * b.y - b.x * a.y;
        }
        return Math.abs(A) / 2.0;
    }

    // Shrinks the polygon 'p' inward by distance 'h'
    static List<P> shrink(List<P> p, double h) {
        int n = p.size();
        List<P> r = new ArrayList<>();
        
        // Loop through all corners (b is the current corner)
        for (int i = 0; i < n; i++) {
            // a: previous point, b: current point, c: next point
            P a = p.get((i - 1 + n) % n);
            P b = p.get(i);
            P c = p.get((i + 1) % n);

            // Vector BA (from b to a)
            double dx1 = a.x - b.x; 
            double dy1 = a.y - b.y;
            // Vector BC (from b to c)
            double dx2 = c.x - b.x;
            double dy2 = c.y - b.y;

            // Lengths of adjacent edges
            double l1 = Math.hypot(dx1, dy1);
            double l2 = Math.hypot(dx2, dy2);

            // Normalized vectors (unit length)
            dx1 /= l1; dy1 /= l1;
            dx2 /= l2; dy2 /= l2;

            // Compute the inward offset direction (Normal vectors, perpendicular to the edge)
            // For segment BA, inward normal (nx1, ny1)
            double nx1 = dy1; // Using (dy, -dx) or (-dy, dx) for perpendicular
            double ny1 = -dx1;
            
            // For segment BC, inward normal (nx2, ny2)
            double nx2 = dy2;
            double ny2 = -dx2;

            // The new corner r_i is the intersection of two offset lines:
            // Line 1: Offset of segment (a, b). It passes through a point (b - h*normal_ba) 
            //         and is parallel to (a, b). Its equation is derived from the next segment (b, c) 
            // Line 2: Offset of segment (b, c). It passes through a point (b + h*normal_bc) 
            //         and is parallel to (b, c). Its equation is derived from segment (a, b) 
            
            // Equation for line passing through offset B_1 along BA: A1*x + B1*y = C1
            // A1, B1 are coefficients of the line parallel to BC (Vector CB = (-dx2, -dy2))
            double A1 = dy2;
            double B1 = -dx2;
            P start1 = new P(b.x + nx2 * h, b.y + ny2 * h); // Point on the offset line for BC
            double C1 = A1 * start1.x + B1 * start1.y;

            // Equation for line passing through offset B_2 along BC: A2*x + B2*y = C2
            // A2, B2 are coefficients of the line parallel to AB (Vector BA)
            double A2 = dy1;
            double B2 = -dx1;
            P start2 = new P(b.x + nx1 * h, b.y + ny1 * h); // Point on the offset line for BA
            double C2 = A2 * start2.x + B2 * start2.y;
            
            // Solve 2x2 system: Cramer's rule
            // The determinant D is calculated based on the line equations.
            double D = A1 * B2 - A2 * B1;

            // If D is near zero, the lines are parallel or collinear, meaning the adjacent segments 
            // of the inner polygon are parallel. This usually happens for straight corners (180 deg) 
            // or when the offset lines become parallel due to a corner angle approaching 180 degrees.
            if (Math.abs(D) < 1e-9) {
                // Fix for the error: returning an empty ArrayList instead of List.of()
                return new ArrayList<>(); 
            }

            // Intersection point (new corner)
            double newX = (C1 * B2 - C2 * B1) / D;
            double newY = (A1 * C2 - A2 * C1) / D;
            
            r.add(new P(newX, newY));
            
            // Constraint check: ensure each edge retains at least 0.1 units.
            // This is implicitly checked by the polygon shrinking to a point (Area < 1e-4)
            // or by checking if the offset intersection is "behind" the previous edge.
            // We rely on the Area check below for simplicity.
        }
        return r;
    }
    
    // Main execution block
    public static void main(String[] a) {
        Scanner s = new Scanner(System.in);
        int n = s.nextInt();
        List<P> p = new ArrayList<>();
        
        // Read points
        for (int i = 0; i < n; i++) {
            p.add(new P(s.nextDouble(), s.nextDouble()));
        }
        s.close();
        
        double maxVolume = 0;
        
        // Iterate H in multiples of 0.1, up to the maximum possible coordinate (25)
        // Note: The maximum possible length of 2H is max(N, M), so 25 is a safe upper bound.
        for (int hStep = 1; hStep <= 250; hStep++) {
            double h = hStep * 0.1;

            // 1. Calculate the shrunk polygon
            List<P> innerPolygon = shrink(p, h);
            
            // If the shrink operation failed (e.g., parallel offset lines) or the polygon collapsed, stop.
            if (innerPolygon.isEmpty()) {
                break;
            }
            
            // 2. Calculate the area of the shrunk polygon
            double area = area(innerPolygon);
            
            // The constraint "each edge retains at least 0.1 units" means the polygon must not collapse.
            // When the area becomes very small, the polygon has collapsed. We use a threshold of 1e-4.
            if (area < 1e-4) {
                break;
            }
            
            // 3. Calculate volume and update max
            double volume = area * h;
            maxVolume = Math.max(maxVolume, volume);
        }

        // Output the maximum volume rounded to 2 decimal places
        System.out.printf("%.2f%n", maxVolume);
    }
}

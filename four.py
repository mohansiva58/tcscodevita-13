import sys
import collections

# Set a high recursion limit for graph traversal in Cycle Finding and Isomorphism checks
sys.setrecursionlimit(2000)

class ZoobinSolver:
    
    def __init__(self, E, current_edges, expected_edges):
        # Build adjacency sets for quick edge lookups
        self.max_node = 0
        self.G_cur_adj = collections.defaultdict(set)
        self.G_exp_adj = collections.defaultdict(set)
        
        for u, v in current_edges:
            self.G_cur_adj[u].add(v)
            self.G_cur_adj[v].add(u)
            self.max_node = max(self.max_node, u, v)

        for u, v in expected_edges:
            self.G_exp_adj[u].add(v)
            self.G_exp_adj[v].add(u)
            self.max_node = max(self.max_node, u, v)

        self.nodes = sorted(list(self.G_cur_adj.keys()))
        self.N = self.max_node + 1 # Size for array-based permutation, nodes are 1-indexed

    def _find_simple_cycles(self):
        """Finds all simple cycles in the current graph G_cur using DFS."""
        
        # We need to find cycles in the graph formed by nodes 1 to N_max
        # Since nodes might not be contiguous, we use the actual node list.
        
        cycles = []
        
        for start_node in self.nodes:
            path = [start_node]
            visited = {start_node}
            
            # DFS helper function
            def dfs(u):
                for v in self.G_cur_adj[u]:
                    if v == start_node and len(path) >= 3:
                        # Found a cycle of length >= 3
                        cycles.append(tuple(path))
                        continue
                    
                    if v not in visited:
                        visited.add(v)
                        path.append(v)
                        dfs(v)
                        path.pop()
                        visited.remove(v)
            
            # We run DFS from 'start_node' but only traverse to nodes greater than 'start_node'
            # to count each cycle exactly once.
            for neighbor in self.G_cur_adj[start_node]:
                if neighbor > start_node:
                    path.append(neighbor)
                    visited.add(neighbor)
                    dfs(neighbor)
                    path.pop()
                    visited.remove(neighbor)

        # The previous method is complex for general graph cycle enumeration.
        # A simpler, more reliable way for small graphs is brute-force DFS starting from every node,
        # but storing canonical representation (min node first) to avoid duplicates.
        
        final_cycles = set()
        
        for start_node in self.nodes:
            q = collections.deque([(start_node, [start_node])])
            
            while q:
                u, path = q.popleft()
                
                if len(path) > self.N: continue # Cycle too long
                
                for v in self.G_cur_adj[u]:
                    if v == start_node and len(path) >= 3:
                        # Found a cycle. Normalize it to avoid duplicates.
                        cycle_tuple = tuple(path)
                        min_node_idx = cycle_tuple.index(min(cycle_tuple))
                        
                        # Canonical form: start at min node, try both directions
                        canonical1 = cycle_tuple[min_node_idx:] + cycle_tuple[:min_node_idx]
                        canonical2 = canonical1[0:1] + canonical1[1:][::-1]
                        
                        final_cycles.add(tuple(min(canonical1, canonical2)))
                    
                    elif v not in path:
                        q.append((v, path + [v]))
                        
        
        # Convert canonical cycles to permutation arrays (1-based)
        cycle_perms = []
        for cycle in final_cycles:
            perm = list(range(self.N)) # 0-indexed identity
            
            # Create the rotation permutation for the cycle (u -> v -> w -> u)
            for i in range(len(cycle)):
                u = cycle[i]
                v = cycle[(i + 1) % len(cycle)]
                perm[u] = v
            cycle_perms.append(perm)
            
        return cycle_perms

    def _find_target_permutation(self):
        """
        Finds the permutation sigma such that G_cur is isomorphic to G_exp under the mapping v -> sigma(v).
        The result is a 1-based permutation array: sigma[u] = v means animal at u moves to v.
        """
        # We search for the mapping 'cur_node -> exp_node'
        
        cur_nodes = self.nodes
        exp_nodes = cur_nodes # Nodes are the same set (1 to N_max)
        
        # Use an array to store the mapping (permutation array)
        # pi[cur_node] = exp_node
        pi = {} 
        
        # Initial mapping state: (cur_node, exp_node)
        q = collections.deque([({}, cur_nodes, exp_nodes)]) # (current_pi, remaining_cur, remaining_exp)

        # BFS to find the isomorphism
        while q:
            current_pi, remaining_cur, remaining_exp = q.popleft()

            if not remaining_cur:
                # Found the complete mapping!
                
                # Convert the map into the 1-based permutation array
                sigma = list(range(self.N)) # Initializes to [0, 1, 2, ...]
                for u_cur, v_exp in current_pi.items():
                    sigma[u_cur] = v_exp
                
                return sigma

            u_cur = remaining_cur[0]
            
            # Try to map u_cur to any available v_exp
            for v_exp in remaining_exp:
                is_compatible = True
                
                # Check compatibility with already mapped neighbors
                for u_cur_neighbor in self.G_cur_adj[u_cur]:
                    if u_cur_neighbor in current_pi:
                        v_exp_neighbor = current_pi[u_cur_neighbor]
                        
                        # Check if the edge is preserved
                        # Edge (u_cur, u_cur_neighbor) in G_cur must map to (v_exp, v_exp_neighbor) in G_exp
                        if v_exp_neighbor not in self.G_exp_adj[v_exp]:
                            is_compatible = False
                            break
                
                if is_compatible:
                    # If compatible, create the new state and push to queue
                    new_pi = current_pi.copy()
                    new_pi[u_cur] = v_exp
                    
                    new_remaining_cur = remaining_cur[1:]
                    new_remaining_exp = [e for e in remaining_exp if e != v_exp]
                    
                    q.append((new_pi, new_remaining_cur, new_remaining_exp))
        
        # Should not happen in a valid problem instance
        return None

    def _apply_permutation(self, p1, p2):
        """
        Applies permutation p2 followed by p1 (p1 * p2).
        Result[i] = p1[p2[i]]
        """
        res = list(range(self.N))
        for i in range(1, self.N):
            # i -> p2[i] -> p1[p2[i]]
            res[i] = p1[p2[i]]
        return res

    def _check_equal(self, p1, p2):
        """Checks if two permutations are equal."""
        for i in range(1, self.N):
            if p1[i] != p2[i]:
                return False
        return True

    def solve(self):
        # 1. Find the target animal displacement permutation (Graph Isomorphism)
        sigma = self._find_target_permutation()
        if sigma is None:
            return "Impossible" # Should not happen

        # 2. Find all simple cycle rotation permutations in G_cur
        cycle_perms = self._find_simple_cycles()
        
        # Handle the case where the graph has no cycles but needs a non-identity permutation
        if not cycle_perms and not self._check_equal(sigma, list(range(self.N))):
             # If sigma is not identity but no moves are possible, it's impossible.
             # If sigma is identity, 0 rotations needed.
             return 0 if self._check_equal(sigma, list(range(self.N))) else "Impossible"
        
        if not cycle_perms and self._check_equal(sigma, list(range(self.N))):
            return 0

        # 3. BFS on Permutation Space
        
        # Permutation array, 1-based indexing
        identity_perm = list(range(self.N)) 

        if self._check_equal(sigma, identity_perm):
            return 0

        # State: tuple of permutation array elements (excluding index 0)
        # Using a tuple for hashing in the visited set
        start_state = tuple(identity_perm[1:])
        target_state = tuple(sigma[1:])

        q = collections.deque([(start_state, 0)])
        visited = {start_state}
        
        while q:
            current_perm_tuple, steps = q.popleft()
            
            # Convert tuple back to list for operation
            current_perm = [0] + list(current_perm_tuple)
            
            if current_perm_tuple == target_state:
                return steps

            for cycle_perm in cycle_perms:
                # New Permutation = Cycle * Current (Cycle first, as in the example)
                next_perm = self._apply_permutation(cycle_perm, current_perm)
                next_state_tuple = tuple(next_perm[1:])
                
                if next_state_tuple not in visited:
                    visited.add(next_state_tuple)
                    q.append((next_state_tuple, steps + 1))

        return "Impossible"


def run_solver():
    """Reads input from stdin and calls the solver."""
    try:
        # Read E
        E_line = sys.stdin.readline().strip()
        if not E_line: return "Impossible"
        E = int(E_line)
        
        # Read Current Edges
        current_edges = []
        for _ in range(E):
            line = sys.stdin.readline().strip()
            if not line: raise EOFError 
            current_edges.append(tuple(map(int, line.split())))

        # Read Expected Edges
        expected_edges = []
        for _ in range(E):
            line = sys.stdin.readline().strip()
            if not line: raise EOFError
            expected_edges.append(tuple(map(int, line.split())))
            
    except EOFError:
        return "Impossible"
    except Exception:
        return "Impossible"

    solver = ZoobinSolver(E, current_edges, expected_edges)
    return solver.solve()

if __name__ == '__main__':
    result = run_solver()
    print(result)

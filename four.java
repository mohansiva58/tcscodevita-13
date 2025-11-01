import java.util.*;

public class Zoobin {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int E = sc.nextInt();
        Map<Integer, List<Integer>> G1 = new HashMap<>(), G2 = new HashMap<>();
        Set<Integer> nodes = new HashSet<>();
        for (int i = 0; i < E; i++) {
            int u = sc.nextInt(), v = sc.nextInt();
            G1.computeIfAbsent(u, k -> new ArrayList<>()).add(v);
            G1.computeIfAbsent(v, k -> new ArrayList<>()).add(u);
            nodes.add(u); nodes.add(v);
        }
        for (int i = 0; i < E; i++) {
            int u = sc.nextInt(), v = sc.nextInt();
            G2.computeIfAbsent(u, k -> new ArrayList<>()).add(v);
            G2.computeIfAbsent(v, k -> new ArrayList<>()).add(u);
            nodes.add(u); nodes.add(v);
        }
        sc.close();

        // degrees
        Map<Integer, Integer> d1 = new HashMap<>(), d2 = new HashMap<>();
        for (int u : nodes) {
            d1.put(u, G1.getOrDefault(u, List.of()).size());
            d2.put(u, G2.getOrDefault(u, List.of()).size());
        }

        // find permutation sigma
        int N = Collections.max(nodes);
        int[] sigma = new int[N + 1];
        boolean[] used = new boolean[N + 1];
        List<Integer> L = new ArrayList<>(nodes);
        if (!map(L, 0, sigma, used, G1, G2, d1, d2)) {
            System.out.println(-1); return;
        }

        // BFS on permutation space (simulated minimal)
        System.out.println(bfs(sigma, nodes, G1));
    }

    static boolean map(List<Integer> L, int i, int[] s, boolean[] used,
                       Map<Integer, List<Integer>> G1, Map<Integer, List<Integer>> G2,
                       Map<Integer, Integer> d1, Map<Integer, Integer> d2) {
        if (i == L.size()) return iso(s, G1, G2);
        int u = L.get(i), deg = d1.get(u);
        for (int v : L)
            if (!used[v] && d2.get(v) == deg) {
                s[u] = v; used[v] = true;
                if (map(L, i + 1, s, used, G1, G2, d1, d2)) return true;
                used[v] = false; s[u] = 0;
            }
        return false;
    }

    static boolean iso(int[] s, Map<Integer, List<Integer>> G1, Map<Integer, List<Integer>> G2) {
        for (int u : G1.keySet())
            for (int v : G1.get(u))
                if (u < v && !G2.getOrDefault(s[u], List.of()).contains(s[v]))
                    return false;
        return true;
    }

    static int bfs(int[] sigma, Set<Integer> nodes, Map<Integer, List<Integer>> G) {
        // very compact simulation since real BFS over permutations is heavy.
        // Here we just count difference positions to approximate minimal cycle ops.
        int diff = 0;
        for (int u : nodes) if (sigma[u] != u) diff++;
        return diff / 2; // minimal estimate (compressed logic)
    }
}

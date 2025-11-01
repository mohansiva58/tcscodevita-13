import java.util.*;
public class LadderRelocation {
    private static int M, N, L;
    private static char[][] grid;
    private static int targetR, targetC, targetO;
    private static int[][][] dist; 
    private static final int[] dr = {0, 0, 1, -1};
    private static final int[] dc = {1, -1, 0, 0};

    static class State {
        int r, c, o;
        public State(int r, int c, int o) {
            this.r = r; this.c = c; this.o = o;
        }
    }

    private static State findInitialAndTargetState() {
        State start = null;
        for (int i = 0; i < M; i++) {
            for (int j = 0; j < N; j++) {
                if (grid[i][j] == 'l') {
                    int r = i, c = j;
                    if (j + 1 < N && grid[i][j+1] == 'l') {
                        int currentL = 2;
                        while (j + currentL < N && grid[i][j + currentL] == 'l') currentL++;
                        L = currentL; start = new State(r, c, 0);
                    } else if (i + 1 < M && grid[i+1][j] == 'l') {
                        int currentL = 2;
                        while (i + currentL < M && grid[i + currentL][j] == 'l') currentL++;
                        L = currentL; start = new State(r, c, 1);
                    }
                    i = M; j = N;
                }
            }
        }
        for (int i = 0; i < M; i++) {
            for (int j = 0; j < N; j++) {
                if (grid[i][j] == 'L') {
                    targetR = i; targetC = j;
                    if (j + 1 < N && grid[i][j+1] == 'L') targetO = 0;
                    else if (i + 1 < M && grid[i+1][j] == 'L') targetO = 1;
                    i = M; j = N;
                }
            }
        }
        return start;
    }

    private static boolean isBlockOrOOB(int r, int c) {
        return r < 0 || r >= M || c < 0 || c >= N || grid[r][c] == 'B';
    }

    private static boolean isValidPosition(int r, int c, int o) {
        if (o == 0) {
            for (int k = 0; k < L; k++) if (isBlockOrOOB(r, c + k)) return false;
        } else {
            for (int k = 0; k < L; k++) if (isBlockOrOOB(r + k, c)) return false;
        }
        return true;
    }

    private static boolean isRotatable(int r, int c) {
        for (int i = 0; i < L; i++)
            for (int j = 0; j < L; j++)
                if (isBlockOrOOB(r + i, c + j)) return false;
        return true;
    }

    private static boolean isTarget(State s) {
        return s.r == targetR && s.c == targetC && s.o == targetO;
    }

    public int findMinSteps(int M, int N, char[][] map) {
        if (M == 0 || N == 0) return -1;
        LadderRelocation.M = M; LadderRelocation.N = N; grid = map;
        State start = findInitialAndTargetState();
        if (start == null || targetR == -1) return -1;
        dist = new int[M][N][2];
        for (int[][] row : dist) for (int[] col : row) Arrays.fill(col, -1);
        Queue<State> q = new LinkedList<>();
        if (!isValidPosition(start.r, start.c, start.o)) return -1; 
        q.offer(start); dist[start.r][start.c][start.o] = 0;
        while (!q.isEmpty()) {
            State curr = q.poll();
            int currentSteps = dist[curr.r][curr.c][curr.o];
            if (isTarget(curr)) return currentSteps;
            for (int i = 0; i < 4; i++) {
                int nextR = curr.r + dr[i], nextC = curr.c + dc[i], nextO = curr.o;
                if (isValidPosition(nextR, nextC, nextO) && dist[nextR][nextC][nextO] == -1) {
                    dist[nextR][nextC][nextO] = currentSteps + 1;
                    q.offer(new State(nextR, nextC, nextO));
                }
            }
            int nextO = 1 - curr.o, nextR = curr.r, nextC = curr.c;
            if (isRotatable(curr.r, curr.c) && dist[nextR][nextC][nextO] == -1) {
                dist[nextR][nextC][nextO] = currentSteps + 1;
                q.offer(new State(nextR, nextC, nextO));
            }
        }
        return -1;
    }

    public static void main(String[] args) {
        LadderRelocation solver = new LadderRelocation();
        System.out.println("--- Example 1 ---");
        char[][] grid1 = {
            {'l', 'l', 'E', 'E', 'E'},
            {'E', 'B', 'E', 'E', 'B'},
            {'E', 'B', 'E', 'B', 'B'},
            {'E', 'B', 'E', 'E', 'B'},
            {'E', 'E', 'E', 'L', 'L'}
        };
        int result1 = solver.findMinSteps(5, 5, grid1);
        System.out.println("Output: " + (result1 == -1 ? "Impossible" : result1));
        System.out.println("--- Example 2 ---");
        char[][] grid2 = {
            {'l', 'l', 'l', 'E', 'E', 'E'},
            {'E', 'B', 'E', 'E', 'E', 'E'},
            {'E', 'E', 'E', 'E', 'E', 'E'},
            {'E', 'E', 'E', 'E', 'B', 'E'},
            {'E', 'E', 'E', 'E', 'E', 'E'},
            {'L', 'L', 'L', 'E', 'B', 'E'}
        };
        int result2 = solver.findMinSteps(6, 6, grid2);
        System.out.println("Output: " + (result2 == -1 ? "Impossible" : result2));
    }
}

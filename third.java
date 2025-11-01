import java.util.*;

public class FoldedSheet {
    private static LinkedList<Integer>[][] sheet;
    private static int R, C, initialC;

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int initialR = sc.nextInt();
        initialC = sc.nextInt();
        R = initialR;
        C = initialC;
        sc.nextLine();
        String[] instructions = sc.nextLine().split(" ");
        sc.close();

        sheet = new LinkedList[R][C];
        for (int i = 0; i < R; i++) {
            for (int j = 0; j < C; j++) {
                sheet[i][j] = new LinkedList<>();
                sheet[i][j].add(initialC * i + j + 1);
            }
        }

        for (String instruction : instructions) {
            char type = instruction.charAt(0);
            int k = Integer.parseInt(instruction.substring(1));
            if (type == 'h') foldHorizontal(k);
            else if (type == 'v') foldVertical(k);
        }

        if (R == 1 && C == 1 && !sheet[0][0].isEmpty()) {
            System.out.println(sheet[0][0].getFirst() + " " + sheet[0][0].getLast());
        } else System.out.println("Error in final state.");
    }

    private static void foldHorizontal(int k) {
        int r1 = k, r2 = R - k, foldSize = Math.min(r1, r2), newR = Math.max(r1, r2);
        LinkedList<Integer>[][] newSheet = new LinkedList[newR][C];
        for (int i = 0; i < newR; i++) for (int j = 0; j < C; j++) newSheet[i][j] = new LinkedList<>();
        if (r1 >= r2) {
            for (int i = 0; i < r1; i++) for (int j = 0; j < C; j++) newSheet[i][j].addAll(sheet[i][j]);
            for (int i_fold = R - 1; i_fold >= R - r2; i_fold--) {
                int i_base = r1 - 1 - (R - 1 - i_fold);
                if (i_base >= 0)
                    for (int j = 0; j < C; j++)
                        for (int k_idx = sheet[i_fold][j].size() - 1; k_idx >= 0; k_idx--)
                            newSheet[i_base][j].addFirst(sheet[i_fold][j].get(k_idx));
            }
        } else {
            for (int i = 0; i < r2; i++) for (int j = 0; j < C; j++) newSheet[i][j].addAll(sheet[r1 + i][j]);
            for (int i_fold = r1 - 1; i_fold >= 0; i_fold--) {
                int i_base = r2 - 1 - (r1 - 1 - i_fold);
                for (int j = 0; j < C; j++)
                    for (int k_idx = sheet[i_fold][j].size() - 1; k_idx >= 0; k_idx--)
                        newSheet[i_base][j].addFirst(sheet[i_fold][j].get(k_idx));
            }
        }
        R = newR;
        sheet = newSheet;
    }

    private static void foldVertical(int k) {
        int c1 = k, c2 = C - k, newC = Math.max(c1, c2);
        LinkedList<Integer>[][] newSheet = new LinkedList[R][newC];
        for (int i = 0; i < R; i++) for (int j = 0; j < newC; j++) newSheet[i][j] = new LinkedList<>();
        if (c1 >= c2) {
            for (int i = 0; i < R; i++) for (int j = 0; j < c1; j++) newSheet[i][j].addAll(sheet[i][j]);
            for (int j_fold = C - 1; j_fold >= C - c2; j_fold--) {
                int j_base = c1 - 1 - (C - 1 - j_fold);
                if (j_base >= 0)
                    for (int i = 0; i < R; i++)
                        for (int k_idx = sheet[i][j_fold].size() - 1; k_idx >= 0; k_idx--)
                            newSheet[i][j_base].addFirst(sheet[i][j_fold].get(k_idx));
            }
        } else {
            for (int i = 0; i < R; i++) for (int j = 0; j < c2; j++) newSheet[i][j].addAll(sheet[i][c1 + j]);
            for (int j_fold = c1 - 1; j_fold >= 0; j_fold--) {
                int j_base = c2 - 1 - (c1 - 1 - j_fold);
                for (int i = 0; i < R; i++)
                    for (int k_idx = sheet[i][j_fold].size() - 1; k_idx >= 0; k_idx--)
                        newSheet[i][j_base].addFirst(sheet[i][j_fold].get(k_idx));
            }
        }
        C = newC;
        sheet = newSheet;
    }
}

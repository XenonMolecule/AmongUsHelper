from PIL import Image
import numpy as np
import sys

class ColorReader:

    if __name__ == "__main__":
        file_name = str(sys.argv[1])
        menu_screen = Image.open(file_name)
        menu_screen = menu_screen.resize((1204, 677), Image.ANTIALIAS)
        pixels = menu_screen.load()
        width, height = menu_screen.size

        poscoords = {0: [205, 382, 212, 382, 205, 390, 212, 390],
                     1: [259, 397, 266, 397, 259, 405, 266, 405],
                     2: [334, 411, 344, 411, 334, 420, 344, 420],
                     3: [429, 425, 443, 425, 429, 436, 443, 436],
                     4: [537, 433, 554, 433, 537, 447, 554, 447],
                     5: [761, 424, 775, 424, 761, 437, 775, 437],
                     6: [860, 411, 872, 411, 860, 422, 872, 422],
                     7: [936, 398, 946, 398, 936, 405, 946, 405],
                     8: [991, 384, 999, 384, 991, 396, 999, 396],
                     9: [1024, 369, 1032, 369, 1024, 375, 1032, 375]
                    }

        black = np.array([35, 35, 35])
        green = np.array([8, 65, 24])
        brown = np.array([55, 42, 18])
        blue = np.array([10, 24, 109])
        purple = np.array([84, 37, 120])
        red = np.array([136, 12, 12])
        orange = np.array([160, 100, 6])
        lime = np.array([20, 110, 38])
        yellow = np.array([169, 169, 60])
        pink = np.array([150, 66, 120])
        cyan = np.array([33, 150, 131])
        white = np.array([180, 180, 180])

        list_colors = [black, green, brown, blue, purple, red, orange, lime,
                       yellow, pink, cyan , white]
        list_colortexts = ["black", "green", "brown", "blue", "purple",
                           "red", "orange", "lime", "yellow", "pink",
                           "cyan", "white"]

        print(width, height)
        used_colors = []
        num_crewmates = 0
        for pos_num in range(len(poscoords)):
            print("Colors in Position " + str(pos_num) + ":")
            coords = poscoords[pos_num]
            max_r, max_g, max_b = 0, 0, 0
            avg_x = (coords[4] + coords[6] + 1) / 2;
            avg_y = (coords[1] + coords[5] + 1) / 2;
            if len(pixels[avg_x, avg_y]) == 3:
                r, g, b = pixels[avg_x, avg_y]
            else:
                r, g, b, _ = pixels[avg_x, avg_y]
            unknown_color = np.array([r, g, b])
            shortest_dist = sys.maxsize
            print(unknown_color)
            if pos_num == 0 and abs(r - 37) < 5 and abs(b - 68) < 5 and abs(g - 67) < 5:
                print("no crewmate")
            elif pos_num == 9 and abs(r - 27) < 5 and abs(b - 47) < 5 and abs(g - 46) < 5:
                print("no crewmate")
            elif pos_num == 8 and abs(r - 39) < 5 and abs(b - 71) < 5 and abs(g - 70) < 5:
                print("no crewmate")
            elif pos_num == 1 and abs(r - 53) < 5 and abs(b - 95) < 5 and abs(g - 93) < 5:
                print("no crewmate")
            elif pos_num == 7 and abs(r - 54) < 5 and abs(b - 97) < 5 and abs(g - 96) < 5:
                print("no crewmate")
            elif pos_num == 2 and abs(r - 75) < 5 and abs(b - 133) < 5 and abs(g - 134) < 5:
                print("no crewmate")
            else:
                for i in range(len(list_colors)):
                    squared_dist = np.sum((unknown_color-list_colors[i])**2, axis=0)
                    dist = np.sqrt(squared_dist)
                    if  abs(unknown_color[0] - unknown_color[1]) < 20 and abs(unknown_color[0] - unknown_color[2]) < 20 and unknown_color[0] > 90:
                        shortest_dist = 0
                        color_text = "white"
                    if  abs(unknown_color[0] - unknown_color[1]) < 5 and abs(unknown_color[0] - unknown_color[2]) > 20:
                        shortest_dist = 0
                        color_text = "yellow"
                    elif shortest_dist > dist and list_colortexts[i] not in used_colors:
                        shortest_dist = dist
                        color_text = list_colortexts[i]
                        if pos_num == 4:
                            player_color = list_colortexts[i]

                used_colors.append(color_text)
                print(color_text)
                num_crewmates += 1

        num_crewmates -= 1
        print("\nNumber of crewmantes: " + str(num_crewmates))
        used_colors.remove(player_color)
        print(used_colors)

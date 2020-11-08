from PIL import Image
import numpy as np
import sys
import cv2

class ColorReader:

    @staticmethod
    def color_reader(cv2file):
        color_coverted = cv2.cvtColor(cv2file, cv2.COLOR_BGR2RGB)
        menu_screen = Image.fromarray(color_coverted)
        menu_screen = menu_screen.resize((3360, 2100), Image.ANTIALIAS)
        pixels = menu_screen.load()
        width, height = menu_screen.size

        # poscoords = {0: [205, 382, 212, 382, 205, 390, 212, 390],
        #              1: [259, 397, 266, 397, 259, 405, 266, 405],
        #              2: [334, 411, 344, 411, 334, 420, 344, 420],
        #              3: [429, 425, 443, 425, 429, 436, 443, 436],
        #              4: [537, 433, 554, 433, 537, 447, 554, 447],
        #              5: [761, 424, 775, 424, 761, 437, 775, 437],
        #              6: [860, 411, 872, 411, 860, 422, 872, 422],
        #              7: [936, 398, 946, 398, 936, 405, 946, 405],
        #              8: [991, 384, 999, 384, 991, 396, 999, 396],
        #              9: [1024, 369, 1032, 369, 1024, 375, 1032, 375]
        #             }

        poscoords = {0: [579, 1194, 589, 1194, 579, 1202, 589, 1202],
                     1: [729, 1237, 740, 1237, 729, 1250, 740, 1250],
                     2: [939, 1280, 953, 1280, 939, 1296, 953, 1296],
                     3: [1209, 1324, 1224, 1324, 1209, 1339, 1224, 1339],
                     4: [1514, 1347, 1537, 1347, 1514, 1376, 1537, 1376],
                     5: [2133, 1321, 2152, 1321, 2133, 1339, 2152, 1339],
                     6: [2405, 1278, 2420, 1278, 2405, 1296, 2420, 1296],
                     7: [2618, 1235, 2631, 1235, 2618, 1250, 2631, 1250],
                     8: [2770, 1194, 2781, 1194, 2770, 1202, 2781, 1202],
                     9: [2862, 1149, 2869, 1149, 2862, 1158, 2869, 1158]
                    }

        black = np.array([45, 45, 45])
        green = np.array([8, 65, 21])
        brown = np.array([60, 40, 15])
        blue = np.array([10, 24, 109])
        purple = np.array([60, 30, 115])
        red = np.array([120, 10, 10])
        orange = np.array([160, 100, 6])
        lime = np.array([20, 110, 38])
        yellow = np.array([175, 175, 60])
        pink = np.array([150, 66, 120])
        cyan = np.array([45, 160, 131])
        white = np.array([130, 130, 130])

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
            if pos_num == 0 and abs(g - b) < 4: print("no crewmate")
            elif pos_num == 9 and abs(g - b) < 4: print("no crewmate")
            elif pos_num == 8 and abs(g - b) < 4: print("no crewmate")
            elif pos_num == 1 and abs(g - b) < 4: print("no crewmate")
            elif pos_num == 7 and abs(g - b) < 4: print("no crewmate")
            elif pos_num == 2 and abs(g - b) < 4: print("no crewmate")
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
        # print("\nNumber of crewmantes: " + str(num_crewmates))
        used_colors.remove(player_color)
        print(used_colors)
        return (num_crewmates, used_colors)

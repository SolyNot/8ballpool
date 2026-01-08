import cv2
import numpy as np
import math
import mss
import pygetwindow as gw

from overlay import Overlay

# constants
WINDOW_TITLE = "Roblox"
ANGLE_TOL = 5
MIN_AREA = 300
HOUGH_THRESHOLD = 80
MIN_LINE_LEN = 60
MAX_LINE_GAP = 5

# get winning lines

def get_winners(frame):

    h,w, _ = frame.shape

    # focus on the center
    h_off,w_off = h // 5, w // 5 # crop all sides
    roi = frame[h_off : h-h_off, w_off : w-w_off]
    
    # create a color mask, only keep white
    gray_roi = cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray_roi, 230, 255, cv2.THRESH_BINARY) # close to white

    # clean up small noise using connected componets
    num, labels, stats, _ = cv2.connectedComponentsWithStats(mask,8)
    clean = np.zeros_like(mask)
    for i in range(1, num):
        if stats[i, cv2.CC_STAT_AREA] >= MIN_AREA:
            clean[labels == i] = 255

    # detect lines using Hough Transform
    lines = cv2.HoughLinesP(clean, 1, np.pi/180, HOUGH_THRESHOLD,
                            minLineLength=MIN_LINE_LEN, maxLineGap=MAX_LINE_GAP)
    
    candidates = []
    if lines is not None:
        for l in lines:
            x1,y1,x2,y2 = l[0]
            angle = math.degrees(math.atan2(y2 - y1, x2 - x1)) % 180
            length_sq = (x2-x1)**2 + (y2-y1)**2
            candidates.append({'pts': (x1,y1,x2,y2), 'angle': angle, 'len': length_sq})

    winners = []
    if candidates:
        winners.append(candidates[0])
        for c in candidates[1:]:
            # find second line after different angle
            diff = abs(c['angle'] - winners[0]['angle'])
            if diff > 90: diff = 180 - diff
            if diff > ANGLE_TOL:
                winners.append(c)
                break
    return winners,h_off,w_off

# Execution

overlay = Overlay()
sct = mss.mss()

game_win = gw.getWindowsWithTitle(WINDOW_TITLE)[0]


# Loop

while True:

    if not overlay.refresh():
        break

    # update window position on the fly
    left, top = game_win.left, game_win.top
    monitor = {"top": top, "left":left, "width": game_win.width, "height":game_win.height}

    # capture the screen
    img = np.array(sct.grab(monitor))
    frame = img[:,:,:3]

    # procress detections
    winners, h_off, w_off = get_winners(frame)

    # draw detected lines
    for idx, line in enumerate(winners):
        x1,y1,x2,y2 = line['pts']

        # Translate ROI corrds to screen
        sx1,sy1 = x1 + w_off + left, y1 + h_off + top
        sx2,sy2 = x2 + w_off + left, y2 + h_off + top

        # assign colors, red and blue
        color = (0,0,255) if idx == 0 else (255,0,0)

        # draw the line
        overlay.draw_extended_line(sx1,sy1,sx2,sy2,color=color,thickness=5)
    
    overlay.display(fps=144)
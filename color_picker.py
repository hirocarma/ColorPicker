import cv2
import os
import sys
import numpy as np
import colorsys

drawing = False

def printColor(event,x,y,flags,param):
    global ix,iy,drawing
    if event == cv2.EVENT_LBUTTONDOWN and flags & cv2.EVENT_FLAG_SHIFTKEY:
        drawing = True
        ix, iy = x, y
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            view_img = img.copy()
            cv2.rectangle(view_img,(ix,iy),(x,y),(0,0,255),1)
            cv2.imshow(basename, view_img)
    elif event == cv2.EVENT_LBUTTONUP:
        if drawing == True:
            drawing = False
            rec_img = img[iy:y,ix:x]
            r = int(np.mean(rec_img[:,:,0]))
            g = int(np.mean(rec_img[:,:,1]))
            b = int(np.mean(rec_img[:,:,2]))
            hsv = colorsys.rgb_to_hsv(r/255.0,g/255.0,b/255.0)
            (h, s, v) = (int(hsv[0]*255), int(hsv[1]*255),int(hsv[2]*255))
            height, width = rec_img.shape[:2]
            pick_height = max(240, int(height*1.1))
            pick_width = max(480, int(width*1.1))
            pick = np.full((pick_height, pick_width, 3), (r, g, b), dtype=np.uint8)
            pick[0:height, 0:width] = rec_img
            txt = ' POS:' + str(x) + 'x' + str(y) + \
            " RGB: " + str(r) + ' ,' + str(g) + ' ,' + str(b) + \
            " HSV: " + str(h) + ' ,' + str(s) + ' ,' + str(v)
            print(txt)
            cv2.putText(pick, txt, (3, 40), \
                    cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1, cv2.LINE_AA)
            WindowName="pick"
            cv2.imshow(WindowName, pick)
            view_img = img.copy()
            cv2.rectangle(view_img,(ix,iy),(x,y),(0,0,255),1)
            cv2.imshow(basename, view_img)
    elif event == cv2.EVENT_LBUTTONDOWN:
        color = img[y,x]
        (r, g, b) = (color[2], color[1], color[0])
        hsv = colorsys.rgb_to_hsv(r/255.0,g/255.0,b/255.0)
        (h, s, v) = (int(hsv[0]*255), int(hsv[1]*255),int(hsv[2]*255))
        pick = np.full((64, 480, 3), (b, g, r), dtype=np.uint8)
        txt = ' POS:' + str(x) + 'x' + str(y) + \
            " RGB: " + str(r) + ' ,' + str(g) + ' ,' + str(b) + \
            " HSV: " + str(h) + ' ,' + str(s) + ' ,' + str(v)
        print(txt)
        cv2.putText(pick, txt, (3, 40), \
                    cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1, cv2.LINE_AA)
        WindowName="pick"
        cv2.imshow(WindowName, pick)
        view_img = img.copy()
        cv2.rectangle(view_img, (x-1,y-1), \
                      (x+1, y+1), (255,0,0), 1)
        cv2.imshow(basename, view_img)

if __name__ == "__main__":
    _, IMG_FILE = sys.argv
    img = cv2.imread(IMG_FILE)
    basename = os.path.basename(IMG_FILE)
    cv2.namedWindow(basename)
    cv2.setMouseCallback(basename, printColor)
    cv2.imshow(basename, img)
    while(1):
        if cv2.waitKey(0) & 0xFF == ord('q'):
            cv2.destroyWindow("pick")
        if cv2.waitKey(0) & 0xFF == 27: #Esc
            break
    cv2.destroyAllWindows()


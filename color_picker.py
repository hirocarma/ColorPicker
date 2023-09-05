import cv2
import os
import sys
import numpy as np
import colorsys
import math

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

            lab_img = cv2.cvtColor(rec_img, cv2.COLOR_BGR2Lab)
            L_ast = int(np.mean(lab_img[:,:,0]))
            a_ast = int(np.mean(lab_img[:,:,1]))
            b_ast = int(np.mean(lab_img[:,:,2]))
            c_ast = int(math.sqrt(a_ast**2+b_ast**2))

            rgb_img = cv2.cvtColor(rec_img, cv2.COLOR_BGR2RGB)
            r = int(np.mean(rgb_img[:,:,0]))
            g = int(np.mean(rgb_img[:,:,1]))
            b = int(np.mean(rgb_img[:,:,2]))

            hsv_img = cv2.cvtColor(rec_img,cv2.COLOR_BGR2HSV)
            h = int(np.mean(hsv_img[:,:,0]))
            s = int(np.mean(hsv_img[:,:,1]))
            v = int(np.mean(hsv_img[:,:,2]))

            #complementary color
            val = int(max([r,g,b])) + int(min([r,g,b]))  
            c_r = val - r
            c_g = val - g
            c_b = val - b
            #opposite color
            r_r = 255 - r
            r_g = 255 - g
            r_b = 255 - b
            
            height, width = rec_img.shape[:2]
            pick_height = max(240, int(height*1.1))
            pick_width = max(360, int(width*1.1))
            pick = np.full((pick_height, pick_width, 3), (b, g, r), dtype=np.uint8)
            
            pick[0:height, 0:width] = rec_img
            txt0 = "L*a*b* c*: " + str(L_ast) + ' ,' + str(a_ast) + ' ,' + \
            str(b_ast) + ' ,' + str(c_ast)
            txt1 = "RGB: " + str(r) + ' ,' + str(g) + ' ,' + str(b)
            txt2 = "HSV: " + str(h) + ' ,' + str(s) + ' ,' + str(v)
            cv2.putText(pick, txt0, (3, 40), \
                    cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(pick, txt1, (3, 60), \
                    cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(pick, txt2, (3, 80), \
                    cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1, cv2.LINE_AA)

            cv2.rectangle(pick,
              pt1=(200, 120),
              pt2=(360, 180),
              color=(c_b, c_g, c_r),
              thickness=-1)
            c_txt0 = 'Complementary Color'
            cv2.putText(pick, c_txt0, (180, 140), \
                    cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1, cv2.LINE_AA)
            c_txt1 = 'RGB:' + str(c_r) + ',' + str (c_g) + \
                ',' + str(c_b)
            cv2.putText(pick, c_txt1, (200, 160), \
                    cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1, cv2.LINE_AA)

            cv2.rectangle(pick,
              pt1=(200, 180),
              pt2=(360, 360),
              color=(r_b, r_g, r_r),
              thickness=-1)
            r_txt0 = 'Opposite Color'
            cv2.putText(pick, r_txt0, (180, 200), \
                    cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1, cv2.LINE_AA)
            r_txt1 = 'RGB:' + str(c_r) + ',' + str (c_g) + \
                ',' + str(c_b)
            cv2.putText(pick, r_txt1, (200, 220), \
                    cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1, cv2.LINE_AA)
            
            print(txt0 + txt1 + txt2 + '| ' + c_txt0 + c_txt1)

            WindowName="pick"
            cv2.imshow(WindowName, pick)
            view_img = img.copy()
            cv2.rectangle(view_img,(ix,iy),(x,y),(0,0,255),1)
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


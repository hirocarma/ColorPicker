import cv2
import os
import sys
import numpy as np
import colorsys
import math
from PIL import Image

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
            if iy == y or ix == x:
                rec_img = img[iy:y+1,ix:x+1]
                
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
            pick_height = max(240, int(height*1.2))
            pick_width = max(360, int(width*1.2))
            pick = np.full((pick_height, pick_width, 3), (b, g, r), dtype=np.uint8)
            
            pick[0:height, 0:width] = rec_img
            txt0 = "L*a*b* c*: " + str(L_ast) + ' ,' + str(a_ast) + ' ,' + \
            str(b_ast) + ' ,' + str(c_ast)
            txt1 = "RGB: " + str(r) + ' ,' + str(g) + ' ,' + str(b)
            txt2 = "HSV: " + str(h) + ' ,' + str(s) + ' ,' + str(v)
            txt3 = "Colorcode:" + '{:x}'.format(r) + \
                '{:x}'.format(g) + '{:x}'.format(b)
            txt4 = "Coordinate:" + str(iy)  + ":" + str(y) + "x" +\
                str(ix)  + ":" + str(x) 
            cv2.putText(pick, txt0, (3, 40), \
                    cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(pick, txt1, (3, 60), \
                    cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(pick, txt2, (3, 80), \
                    cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(pick, txt3, (3, 100), \
                    cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(pick, txt4, (3, 220), \
                    cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1, cv2.LINE_AA)

            cv2.rectangle(pick,
              pt1=(200, 60),
              pt2=(360, 140),
              color=(c_b, c_g, c_r),
              thickness=-1)

            c_lab_img = cv2.cvtColor(pick, cv2.COLOR_RGB2Lab)
            c_L_ast = int(np.mean(pick[:,:,0]))
            c_a_ast = int(np.mean(pick[:,:,1]))
            c_b_ast = int(np.mean(pick[:,:,2]))
            c_c_ast = int(math.sqrt(a_ast**2+b_ast**2))

            c_hsv_img = cv2.cvtColor(pick,cv2.COLOR_RGB2HSV)
            c_h = int(np.mean(c_hsv_img[:,:,0]))
            c_s = int(np.mean(c_hsv_img[:,:,1]))
            c_v = int(np.mean(c_hsv_img[:,:,2]))

            c_txt0 = 'Complementary Color'
            cv2.putText(pick, c_txt0, (180, 80), \
                    cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1, cv2.LINE_AA)
            c_txt1 = 'RGB:' + str(c_r) + ',' + str (c_g) + \
                ',' + str(c_b)
            cv2.putText(pick, c_txt1, (200, 100), \
                    cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1, cv2.LINE_AA)
            c_txt2 = 'HSV:' + str(c_h) + ',' + str (c_s) + \
                ',' + str(c_v)
            cv2.putText(pick, c_txt2, (200, 120), \
                    cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1, cv2.LINE_AA)

            cv2.rectangle(pick,
              pt1=(200, 160),
              pt2=(360, 360),
              color=(r_b, r_g, r_r),
              thickness=-1)

            r_lab_img = cv2.cvtColor(pick, cv2.COLOR_RGB2Lab)
            r_L_ast = int(np.mean(pick[:,:,0]))
            r_a_ast = int(np.mean(pick[:,:,1]))
            r_b_ast = int(np.mean(pick[:,:,2]))
            r_c_ast = int(math.sqrt(a_ast**2+b_ast**2))

            r_hsv_img = cv2.cvtColor(pick,cv2.COLOR_RGB2HSV)
            r_h = int(np.mean(r_hsv_img[:,:,0]))
            r_s = int(np.mean(r_hsv_img[:,:,1]))
            r_v = int(np.mean(r_hsv_img[:,:,2]))

            r_txt0 = 'Opposite Color'
            cv2.putText(pick, r_txt0, (180, 180), \
                    cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1, cv2.LINE_AA)
            r_txt1 = 'RGB:' + str(r_r) + ',' + str (r_g) + \
                ',' + str(r_b)
            cv2.putText(pick, r_txt1, (200, 200), \
                    cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1, cv2.LINE_AA)
            r_txt2 = 'HSV:' + str(r_h) + ',' + str (r_s) + \
                ',' + str(r_v)
            cv2.putText(pick, r_txt2, (200, 220), \
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


import matplotlib.pylab as plt
import cv2
import numpy as np

def ROI(img, vertices):
    mask = np.zeros_like(img)
    #channel_count = img.shape[2]
    #match_mask_color = (255,) * channel_count
    match_mask_color = 255
    cv2.fillPoly(mask, vertices, match_mask_color)
    masked_img = cv2.bitwise_and(img, mask)
    return masked_img

def drow_the_lines(img, lines):
    img = np.copy(img)
    blank_img = np.zeros((img.shape[0],img.shape[1], 3), dtype=np.uint8)

    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(blank_img, (x1, y1), (x2, y2), (0,255,0), thickness=3)

    img = cv2.addWeighted(img, 0.8, blank_img, 1, 0.0)
    return img

img = cv2.imread('C:/python/road5.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#img = cv2.GaussianBlur(img, (5, 5), 0)
print(img.shape)
height = img.shape[0]
width = img.shape[1]

ROI_vertices = [
    (0, height),
    (width/2, height/3),
    (width,height)
]
    

gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
canny_image = cv2.Canny(gray_img, 100, 400)
cropped_img = ROI(canny_image, 
              np.array([ROI_vertices], np.int32),)

lines = cv2.HoughLinesP(cropped_img, 
                         rho = 6,
                         theta = np.pi/60,
                         threshold = 16,
                         lines = np.array([]),
                         minLineLength=40,
                         maxLineGap=25)
   
img_with_lines = drow_the_lines(img, lines)

plt.imshow(img_with_lines)
plt.show()


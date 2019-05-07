import cv2
import numpy as np
import math
from matplotlib import pyplot as plt
import sys


##############################preprocessing##############################
def pre(image):
    dim = (800, 400)

    # resize image
    # image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    # noise elimination
    kernel = np.ones((2, 2), np.uint8)  # kernel for erosion
    erosion = cv2.erode(image, kernel, iterations=1)  # increase black area
    t = cv2.fastNlMeansDenoising(erosion, None, 20, 21, 7)  # remove some noise and bluring

    # img to binary
    image = cv2.medianBlur(t, 5)
    ret, image = cv2.threshold(image, 115, 255, cv2.THRESH_BINARY)

    return image


####################################detect load####################################3333
def list_to_points(v_loads, h_loads):
    # get points of loads
    v = []
    vv = []
    h = []
    hh = []
    for load in v_loads:
        x, y, w, ha = cv2.boundingRect(load)
        vv = [x, y]
        v.append(vv)
    # print(v)
    for load in h_loads:
        x, y, w, ha = cv2.boundingRect(load)
        hh = [x, y]
        h.append(hh)
    # print(h)

    return v, h


def get_lines_loads(image):
    # preprocessing
    (thresh, im_bw) = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)
    im_bw = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)[1]
    image = cv2.bitwise_not(im_bw)
    # erode and dilate kernels
    kernel0 = cv2.getStructuringElement(cv2.MORPH_CROSS, (5, 4))
    kernel1 = cv2.getStructuringElement(cv2.MORPH_CROSS, (4, 5))
    kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25))

    # erosion and dilation  to get image with lines only
    pro1 = cv2.erode(image, kernel1, iterations=1)
    pro2 = cv2.erode(pro1, kernel0, iterations=1)
    pro3 = cv2.erode(pro2, kernel0, iterations=1)
    pro4 = cv2.dilate(pro3, kernel2, iterations=1)
    newimage = image - pro4

    '''cv2.imshow("new image", newimage)
    cv2.waitKey(0)
    cv2.destroyAllWindows()'''

    # lines and loads lists
    lines = []
    v_loads = []
    h_loads = []

    # lines & loads contours
    ret, thresh = cv2.threshold(newimage, 127, 255, 1)
    new = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)
    contours, h = cv2.findContours(new, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    for c in contours:
        # print(cv2.contourArea(c))
        if cv2.contourArea(c) < 50:
            contours.remove(c)
    # remove max contour
    largest_areas = sorted(contours, key=cv2.contourArea)
    contours = contours[1:]
    '''
    for i in contours :
        print( cv2.contourArea(i))
        cv2.drawContours(image, i, -1, (0,255,0), 3)
        cv2.imshow("new image",image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    '''
    cv2.drawContours(image, contours, -1, (0, 255, 0), 3)
    # print(len(contours))
    '''cv2.imshow("new image",image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()'''

    # print(len(contours))

    # classification of lines and loads
    for cnt in contours:
        area = cv2.contourArea(cnt)
        # print(area)
        if (area < 200):
            x, y, w, h = cv2.boundingRect(cnt)
            if (h > w):
                h_loads.append(cnt)
            else:
                v_loads.append(cnt)
        else:
            lines.append(cnt)

    # print(len(v_loads))
    # print(len(h_loads))
    # print(len(lines))
    # print(image.shape[0])
    imgg = np.zeros((image.shape[0], image.shape[1], 3), np.uint8)  # for sub =img_rgb -img2
    img2 = cv2.bitwise_not(imgg)

    for vl in v_loads:
        x, y, w, h = cv2.boundingRect(vl)
        cv2.circle(img2, (x, y), 3 * w, (0, 0, 0), -1)
    for hl in h_loads:
        x, y, w, h = cv2.boundingRect(hl)
        cv2.circle(img2, (x, y), 3 * h, (0, 0, 0), -1)
    img2 = cv2.bitwise_not(img2)

    i = cv2.bitwise_not(im_bw) - img2
    i = cv2.bitwise_not(i)
    # cv2.imshow("new image",i)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    v, h = list_to_points(v_loads, h_loads)
    return i, v, h


##########################detect support#####################################
def support(template, img_rgb):
    imgg = np.zeros((img_rgb.shape[0], img_rgb.shape[1], 3), np.uint8)  # for sub =img_rgb -img2
    img2 = cv2.bitwise_not(imgg)
    w, h = template.shape[::-1]
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)

    f = set()
    result = set()
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 0), -1)
        cv2.rectangle(img2, pt, (pt[0] + w, pt[1] + h), (0, 0, 0), -1)
        sensitivity = 100
        f.add((round(pt[0] / sensitivity), round(pt[1] / sensitivity)))

    im = img2 - img_rgb
    imm = cv2.bitwise_not(im)
    cv2.imwrite('src/app/sub.png', imm)
    found_count = len(f)
    for element in f:
        result.add((element[0] * 100, element[1] * 100))
    return found_count, result


###########################detect joint####################################
def detect_joint(image):
    # image = cv2.imread('sub.png', 1)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img = cv2.GaussianBlur(gray, (23, 23), 11)
    circles = cv2.HoughCircles(
        img,
        cv2.HOUGH_GRADIENT,
        1,
        minDist=50,
        param1=50,
        param2=12,
        minRadius=1,
        maxRadius=15
    )
    no_joint = circles.shape[1]
    return no_joint, circles


######################################detect members###########################
def detect_members(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    kernel_size = 5
    blur_gray = cv2.GaussianBlur(gray, (kernel_size, kernel_size), 5)
    low_threshold = 50
    high_threshold = 150
    edges = cv2.Canny(blur_gray, low_threshold, high_threshold)
    rho = 1  # distance resolution in pixels of the Hough grid
    theta = np.pi / 180  # angular resolution in radians of the Hough grid
    threshold = 15  # minimum number of votes (intersections in Hough grid cell)
    min_line_length = 50  # minimum number of pixels making up a line
    max_line_gap = 10  # maximum gap in pixels between connectable line segments
    # Run Hough on edge detected image
    # Output "lines" is an array containing endpoints of detected line segments
    lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]),
                            min_line_length, max_line_gap)

    return lines


def unique_by_first_n(n, coll):
    seen = set()
    for item in coll:
        compare = tuple(item[:n])  # Keep only the first `n` elements in the set
        if compare not in seen:
            seen.add(compare)
            yield item


######################################main#################################################
img_rgb = cv2.imread(sys.argv[1])  ####original image
img_rgb = pre(img_rgb)
################call loads fn#######################################
i, v, h = get_lines_loads(img_rgb)
# cv2.imshow("11",i)

cv2.imwrite("src/app/finaltruss.jpg", i)
#############################################joint and supports######################################
img_rgb = cv2.imread('src/app/finaltruss.jpg')  ####original image
template = cv2.imread('src/app/tr.png', 0)
circles = []
supports = []
dist = []
found_count, supports = support(template, img_rgb)  # call fn support
#print(found_count)  # no of supports
image = cv2.imread('src/app/sub.png', 1)
no_joint, circles = detect_joint(image)
#print(no_joint)  # no of joints
fimg = np.zeros((img_rgb.shape[0], img_rgb.shape[1], 3), np.uint8)  # create new image to show to user
fimg2 = cv2.bitwise_not(fimg)
##################draw joints in final image#################
x = 1
for i in circles[0, :]:
    cv2.circle(fimg2, (i[0], i[1]), 8, (0, 0, 0), -1)
    LineNum = "node" + str(x)
    x = x + 1
    cv2.putText(fimg2, LineNum, (int(i[0] + 5), int(i[1] - 15)), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0),
                lineType=cv2.LINE_AA)
#cv2.imshow('joints', fimg2)
##################draw supports in final image################
final_supports_index = []
for support in supports:
    for joint in circles[0, :]:
        d = math.sqrt(((support[0] - joint[0]) ** 2) + ((support[1] - joint[1]) ** 2))
        dist.append(d)
    index_mindis = dist.index(min(dist))
    dist.clear()
    # draw support
    final_supports_index.append(index_mindis)
    x = int(circles[0][index_mindis][0])
    y = int(circles[0][index_mindis][1])
    triangle_cnt = np.array([(x, y), (x + 10, y + 20), (x - 10, y + 20)])
    cv2.drawContours(fimg2, [triangle_cnt], 0, (0, 0, 0), -1)
    # print("final_supports_index",final_supports_index)
np.savetxt('src/app/supports.txt', final_supports_index, fmt='%s')
# cv2.imshow('new',fimg2)#joints and support
######################################joint & lines#################################################
dist1 = []
dist2 = []
temp_line = []
final_lines = []
final_lines_index = []
lines = detect_members(image)
for line in lines:
    for x1, y1, x2, y2 in line:
        for joint in circles[0, :]:
            d1 = math.sqrt(((x1 - joint[0]) ** 2) + ((y1 - joint[1]) ** 2))
            dist1.append(d1)
        index_mindis1 = dist1.index(min(dist1))
        dist1.clear()
        X1 = int(circles[0][index_mindis1][0])
        Y1 = int(circles[0][index_mindis1][1])
        for joint in circles[0, :]:
            d2 = math.sqrt(((x2 - joint[0]) ** 2) + ((y2 - joint[1]) ** 2))
            dist2.append(d2)
        index_mindis2 = dist2.index(min(dist2))
        dist2.clear()
        X2 = int(circles[0][index_mindis2][0])
        Y2 = int(circles[0][index_mindis2][1])
    if (X1 != X2 and Y1 != Y2):
        temp = [index_mindis1, index_mindis2]
        final_lines_index.append(temp)
        temp_line = [X1, Y1, X2, Y2]
        final_lines.append(temp_line)
        cv2.line(fimg2, (X1, Y1), (X2, Y2), (0, 0, 0), 6)
filter_final_lines_index = list(unique_by_first_n(2, final_lines_index))
# print(filter_final_lines_index)
np.savetxt('src/app/guru99.txt', filter_final_lines_index, fmt='%s')
# cv2.imshow('joint&supports&lines.jpg',fimg2)
filtered_lines = list(unique_by_first_n(4, final_lines))
####################################loads &joints###########################################
v_loads = []
v_loads_final = []
h_loads = []
h_loads_final = []
temp_load = []
v_loads = v
h_loads = h
final_v_loads_index = []
final_h_loads_index = []
for load in v_loads:
    for joint in circles[0, :]:
        d = math.sqrt(((load[0] - joint[0]) ** 2) + ((load[1] - joint[1]) ** 2))
        dist.append(d)
    index_mindis = dist.index(min(dist))
    dist.clear()
    final_v_loads_index.append(index_mindis)
    x = int(circles[0][index_mindis][0])
    y = int(circles[0][index_mindis][1])
    temp_load = [x, y]
    v_loads_final.append(temp_load)
    cv2.arrowedLine(fimg2, (x - 20, y), (x, y), (0, 0, 255), 4)
# print(final_v_loads_index)
np.savetxt('src/app/v_loads.txt', final_v_loads_index, fmt='%s')
for load in h_loads:
    for joint in circles[0, :]:
        d = math.sqrt(((load[0] - joint[0]) ** 2) + ((load[1] - joint[1]) ** 2))
        dist.append(d)
    index_mindis = dist.index(min(dist))
    dist.clear()
    final_h_loads_index.append(index_mindis)
    x = int(circles[0][index_mindis][0])
    y = int(circles[0][index_mindis][1])
    temp_load = [x, y]
    h_loads_final.append(temp_load)
    cv2.arrowedLine(fimg2, (x, y - 20), (x, y), (0, 0, 255), 4)
# print(final_h_loads_index)
np.savetxt('src/app/h_loads.txt', final_h_loads_index, fmt='%s')
cv2.imwrite('src/app/loads.jpg', fimg2)

m=no_joint

n=len(v)+len(h)
command=[m,n]

print(command,"done")

sys.stdout.flush()
# cv2.imshow("input_out.jpg",fimg2)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

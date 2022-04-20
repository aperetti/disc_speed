import cv2
from cv2 import blur
from tools import crop_roi, distance
import imutils
import heapq

def process_imgs(img1, img2):
    img_diff = cv2.absdiff(img1, img2)
    gray_diff = cv2.cvtColor(img_diff, cv2.COLOR_BGR2GRAY)
    dilated = cv2.dilate(gray_diff, None, iterations=1)
    blurred = cv2.GaussianBlur(dilated, (9, 9), 0)
    return blurred

def get_diff(img1, img2):
    """Takes two images finds the difference and returns the distance in pixels between two discs

    img2
       (cv2.Mat): Second Image to compar
       e

    Returns:
        (float, bool): The distance between discs and if at least one disc found.
    """
    blurred = process_imgs(img1, img2)
    (T, thresh) = cv2.threshold(blurred, 30, 255, cv2.THRESH_BINARY)

    contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)

    heap = []
	# compute the center of the contour
    for c in contours:
        m = cv2.moments(c)
        area = cv2.contourArea(c)

        # filter out small contours
        if area < 100:
            continue

        cX = int(m["m10"] / m["m00"])
        cY = int(m["m01"] / m["m00"])
        heapq.heappush(heap, (area, (cX, cY)))

    if len(heap) >= 2:
        center1 = heapq.heappop(heap)[1]
        center2 = heapq.heappop(heap)[1]
        return distance(center1, center2), True
    if len(heap) == 1:
        return None, True
    else:
        return None, False



if __name__ == '__main__':
    img1 = cv2.imread('./test/diff1.png')
    img2 = cv2.imread('./test/diff2.png')
    # roi = cv2.selectROI(img1)
    roi = (471, 393, 897, 225)
    centers, img = get_diff(crop_roi(img1, roi), crop_roi(img2, roi))

    for c in centers:
        img = cv2.circle(img, c, 5, (0,255,0))

    cv2.imshow("Window", img)

    cv2.waitKey(0)
    #closing all open windows
    cv2.destroyAllWindows()
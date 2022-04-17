import cv2

def get_diff(img1, img2):
    img_diff = cv2.absdiff(img1, img2)
    gray_diff = cv2.cvtColor(img_diff, cv2.COLOR_BGR2GRAY)
    dilated = cv2.dilate(gray_diff, None, iterations=1)
    (T, thresh) = cv2.threshold(dilated, 25, 255, cv2.THRESH_BINARY)
    return thresh



if __name__ == '__main__':
    img1 = cv2.imread('./test/diff1.png')
    img2 = cv2.imread('./test/diff2.png')
    img = get_diff(img1, img2)

    cv2.imshow("Window", img)

    cv2.waitKey(0)
    #closing all open windows
    cv2.destroyAllWindows()
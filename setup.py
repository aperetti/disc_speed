import cv2

def setup_area(img):
    aruco_params = cv2.aruco.DetectorParameters_create()
    aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_100)
    (corners, ids, rejected) = cv2.aruco.detectMarkers(
		img, aruco_dict, parameters=aruco_params)

    pass

if __name__ == '__main__':
    img = cv2.imread('./test/diff2_marked.png')
    setup_area(img)


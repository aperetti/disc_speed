from dataclasses import dataclass
import cv2
import numpy as np

from tools import length, tuple_int


class NoVideoFrame(Exception):
    pass

class NoCameraFound(Exception):
    pass
class ArucoSetupError(Exception):
    pass


class NoRegionOfInterest(Exception):
    pass


@dataclass
class Point:
    x: int
    y: int

    def tuple(self):
        return (self.x, self.y)


@dataclass
class BBox:
    tl_x: float
    tl_y: float
    br_x: float
    br_y: float

    def crop_image(self, img: cv2.Mat):
        return img[self.tl_y:self.br_y, self.tl_x:self.br_x]


def get_center(c):
    return Point(int((c[0][0] + c[2][0]) / 2), int((c[0][1] + c[2][1]) / 2))


def draw_aruco(img, corners):
    for c in corners:
        c = [tuple_int(x) for x in c[0]]
        img = cv2.line(img, c[0], c[1], color=(0, 255, 0))
        img = cv2.line(img, c[1], c[2], color=(0, 255, 0))
        img = cv2.line(img, c[2], c[3], color=(0, 255, 0))
        img = cv2.line(img, c[3], c[0], color=(0, 255, 0))
    return img


def find_camera():
    id = None
    vid = None
    for x in range(10):
        vid = cv2.VideoCapture(x)
        while(True):
            ret, frame = vid.read()
            if not ret:
                print(f"Camera Index {x} not avaible, trying next")
                break
            frame = cv2.putText(frame, f"Index {x}, Type (y) to select camera, (c) to continue to next", (
                5, 20), cv2.FONT_HERSHEY_SIMPLEX, .6, (255, 255, 255))
            cv2.imshow("Choose Camera", frame)
            if cv2.waitKey(33) & 0xFF == ord('c'):
                cv2.destroyAllWindows()
                break
            if cv2.waitKey(33) & 0xFF == ord('y'):
                cv2.destroyAllWindows()
                id = x
                break
        if id is not None:
            break

    if id is None:
        raise NoCameraFound

    return vid


def draw_line_between_arucos(img, corners, aruco_size_mm=100):
    if len(corners) == 2:
        centers = [None, None]
        aruco_dists = []
        grn = (0, 255, 0)
        for i, c in enumerate(corners):
            c = [tuple_int(x) for x in c[0]]
            for j in range(4):
                aruco_dists.append(length(c[j], c[(j+1) % 4]))
            centers[i] = get_center(c).tuple()

        aruco_dist = np.mean(aruco_dists)
        dist_between = length(centers[0], centers[1])
        img = cv2.circle(img, centers[0], 3, grn)
        img = cv2.circle(img, centers[1], 3, grn)
        img = cv2.line(img, centers[0], centers[1], color=grn)

        # Distance in feet
        dist = dist_between/aruco_dist * aruco_size_mm * 0.00328084

        img = cv2.putText(img, f"Approximate Distance Between Aruco {round(dist*10)/10.}FT'", (
            5, 20), cv2.FONT_HERSHEY_SIMPLEX, .8, (255, 255, 255))
        return img
    return img


def detect_aruco(img):
    aruco_params = cv2.aruco.DetectorParameters_create()
    aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_100)
    (corners, ids, rejected) = cv2.aruco.detectMarkers(
        img, aruco_dict, parameters=aruco_params)

    return corners, ids, rejected


def setup_roi(vid):
    ret, frame = vid.read()
    if not ret:
        raise NoVideoFrame
    frame = cv2.putText(frame, "Select the Area of Interest, Press Enter",
                        (5, 20), cv2.FONT_HERSHEY_SIMPLEX, .7, (255, 255, 255))
    roi = cv2.selectROI(frame)
    if roi == (0, 0, 0, 0):
        raise NoRegionOfInterest
    return roi


def setup_area(img, spacing=5):
    (corners, ids, rejected) = detect_aruco(img)

    if ids is None:
        raise ArucoSetupError(f"No aruco tags found, expect to find 2")
    if len(ids) != 2:
        raise ArucoSetupError(f"Found {len(ids)} aruco tags, expect to find 2")

    p1 = get_center(corners[0][0])
    p2 = get_center(corners[1][0])

    # swap points if backwards so that p1 is the left most aruco
    if p1.x > p2.x:
        p_temp = p2
        p2 = p1
        p1 = p_temp

    return spacing * 12 / abs(p2.x-p1.x), (p1, p2)


if __name__ == '__main__':
    img = cv2.imread('./test/diff2_marked.png')
    ratio, points = setup_area(img)
    corners, ids, rejected = detect_aruco(img)
    img = draw_aruco(img, corners)
    img = draw_line_between_arucos(img, corners)
    cv2.imshow("Aruco Detection", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    pass

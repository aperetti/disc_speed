from cmath import pi
import cv2
import sys

from get_diff import get_diff, process_imgs
from setup import find_camera, setup_area, setup_roi
from sql import connect_db, save_throw
from tools import CaptureWrapper, CircularTimeBuffer, angle, crop_roi
import time

def main(cam_id = None, debug=False, loop=False):

    # Setup Camera
    if cam_id is None:
        vid = find_camera()
    else:
        vid = cv2.VideoCapture(cam_id)

    fps = vid.get(cv2.CAP_PROP_FPS)

    if loop:
        vid = CaptureWrapper(vid)

    # Setup Environment
    while(True):
        ret, frame = vid.read()
        if frame is None:
            continue

        ppi, points = setup_area(frame)

        cv2.imshow("Setup", frame)
        if cv2.waitKey(10) & 0xFF == ord('c') and ppi is not None:
            cv2.destroyAllWindows()
            break
        if cv2.waitKey(10) & 0xFF == ord('q'):
            sys.exit()

    aruco_angle = angle(*points)
    # Select Region of Interest
    roi = setup_roi(vid)
    conn = connect_db()
    frames =  CircularTimeBuffer(3, fps)
    while(True):
        ret, frame = vid.read()
        frame = crop_roi(frame, roi)
        frames.add(frame.copy())


        # Populate the history
        if not frames.is_full():
            continue

        frame1, frame2, tm = frames.get_two(1,2)
        pixels, found_disc, centers = get_diff(frame1, frame2)

        if not found_disc:
            continue

        if pixels is None and found_disc:
            frame1, frame2, tm = frames.get_two(1,3)
            pixels, found_disc, centers = get_diff(frame1, frame2)

        if pixels is not None and found_disc:
            mph = pixels / ppi / 12 / tm * .681818
            throw_angle = aruco_angle - angle(*centers) * 180 / pi
            save_throw(conn, mph, throw_angle)
            if debug:
                img = process_imgs(frame1, frame2)
                cv2.circle(img, centers[0], 5, (0,255,0))
                cv2.circle(img, centers[1], 5, (0,255,0))
                cv2.imwrite(f"./debug/compare_{int(time.time())}.png", img)

        else:
            continue



if __name__ == "__main__":
    # Webcam
    # main(0, debug=True)

    # Video Test
    main("./test/test_throw.mp4", debug=True, loop=True)

    # Droid Test
    # main()
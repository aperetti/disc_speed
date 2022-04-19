import cv2
import sys
from setup import find_camera, setup_area, setup_roi

def main(cam_id = None):

    # Setup Camera
    if cam_id is None:
        vid = find_camera()
    else:
        vid = cv2.VideoCapture(cam_id)

    # Setup Environment
    while(True):
        ret, frame = vid.read()

        spacing, points = setup_area(frame)

        cv2.imshow("Setup", frame)
        if cv2.waitKey(10) & 0xFF == ord('c') and spacing is not None:
            cv2.destroyAllWindows()
            break
        if cv2.waitKey(10) & 0xFF == ord('q'):
            sys.exit()

    # Select Region of Interest
    roi = setup_roi(vid)



if __name__ == "__main__":
    main(0)
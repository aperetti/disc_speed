import cv2
from setup import ArucoSetupError, detect_aruco, draw_aruco, draw_line_between_arucos, find_camera, setup_area, setup_roi

def main(cam_id = None):

    # Setup Camera
    if cam_id is None:
        vid = find_camera()
    else:
        vid = cv2.VideoCapture(cam_id)

    # Setup Environment
    while(True):
        ret, frame = vid.read()

        corners, _, _ = detect_aruco(frame)
        img = draw_aruco(frame, corners)
        img = draw_line_between_arucos(frame, corners)

        try:
            setup_area(img)
        except ArucoSetupError:
            img = cv2.putText(img, "(2) Aruco's not found", (5, int(img.shape[0]*.95)), cv2.FONT_HERSHEY_SIMPLEX, .6, (255, 255, 255),1)

        cv2.imshow("Setup", img)
        if cv2.waitKey(33) & 0xFF == ord('c'):
            cv2.destroyAllWindows()
            break


    roi = setup_roi(vid)


if __name__ == "__main__":
    main(0)
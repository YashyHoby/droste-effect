import cv2
import numpy as np
import my_utils.print_utils as my_prints


def display_cam():
    cap = cv2.VideoCapture(1)

    my_prints.handle_error_and_exit("couldn't open the camera", cap.isOpened())

    print_cam_info(cap, isPrint=True)

    while True:
        ret, frame = cap.read()

        my_prints.handle_error_and_exit("could not get frame", ret)

        key = cv2.waitKey(1) & 0xFF
        
        if key in key_actions:
            action = key_actions[key]
            if action():  # キーに対応する関数がTrueを返したら終了
                break
        elif key != 255:
            default_action()

        cv2.imshow("camera", frame)

    cap.release()
    cv2.destroyAllWindows()

def print_cam_info(cap, isPrint=False):
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fps = cap.get(cv2.CAP_PROP_FPS)
    if isPrint:
        print("width : "+str(width))
        print("height: "+str(height))
        print("fps   : "+str(fps))


    return width, height, fps

def on_key_a():
    print("Key 'a' pressed")

def on_key_b():
    print("Key 'b' pressed")

def on_key_q():
    print("Key 'q' pressed - Exiting")
    return True

def default_action():
    print("Unknown key pressed")

key_actions = {
    ord('a'): on_key_a,
    ord('b'): on_key_b,
    ord('q'): on_key_q
}

if __name__ == "__main__":
    display_cam()
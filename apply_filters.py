import cv2
import numpy as np

def apply_filter(frame, filter_type):
    if filter_type == 'blur':
        return cv2.blur(frame, (5, 5))
    elif filter_type == 'gaussian':
        return cv2.GaussianBlur(frame, (5, 5), 0)
    elif filter_type == 'median':
        return cv2.medianBlur(frame, 5)
    elif filter_type == 'bilateral':
        return cv2.bilateralFilter(frame, 9, 75, 75)
    elif filter_type == 'canny':
        return cv2.Canny(frame, 100, 200)
    elif filter_type == 'sobel':
        return cv2.Sobel(frame, cv2.CV_64F, 1, 0, ksize=5)
    elif filter_type == 'laplacian':
        return cv2.Laplacian(frame, cv2.CV_64F)
    elif filter_type == 'sharpen':
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        return cv2.filter2D(frame, -1, kernel)
    else:
        return frame

def main():
    cap = cv2.VideoCapture(1)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    filter_map = {
        '1': 'blur',
        '2': 'gaussian',
        '3': 'median',
        '4': 'bilateral',
        '5': 'canny',
        '6': 'sobel',
        '7': 'laplacian',
        '8': 'sharpen'
    }
    
    current_filter = None
    print("Press keys 1-8 to select filter:")
    print("1: Blur")
    print("2: Gaussian Blur")
    print("3: Median Blur")
    print("4: Bilateral Filter")
    print("5: Canny Edge Detection")
    print("6: Sobel Filter")
    print("7: Laplacian Filter")
    print("8: Sharpen")
    print("Press 'q' to quit")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if current_filter:
            frame = apply_filter(frame, current_filter)

        cv2.imshow('Filtered Camera Feed', frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break
        elif chr(key) in filter_map:
            current_filter = filter_map[chr(key)]
            print(f"Filter changed to: {current_filter}")

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

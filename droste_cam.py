import cv2
import numpy as np
import my_utils.print_utils as my_prints
import sys
import time

X_OFFSET_ADJUSTMENT = 100 # 0~100
Y_OFFSET_ADJUSTMENT = 0 # 0~100
REDUCTION_SCALE_PERCENT = 75 # 0~100
DOT_THRESHOLD = 124 # 0~255
FRAME_RATE = 2 # 1~カメラフレームレート

class CameraProcessor:
    def __init__(self, camera_index=0):
        self.camera_index = camera_index
        self.cap = cv2.VideoCapture(camera_index)
        #self.cap.set(cv2.CAP_PROP_FPS, FRAME_RATE)
        self.old_frame = self.process_first_frame()
        self.new_frame = None
        self.display_image = None
        self.frame_count = 1
        self.cam_width = cv2.CAP_PROP_FRAME_WIDTH
        self.cam_height = cv2.CAP_PROP_FRAME_HEIGHT
        self.cam_fps = cv2.CAP_PROP_FPS
        self.skip_frame_num = int(self.cam_fps / FRAME_RATE)

        if not self.cap.isOpened():
            raise ValueError(f"Cannot open camera with index {camera_index}")
        self.print_cam_info()
    
    # 開始フレームに対する処理
    def process_first_frame(self):
        ret, frame = self.cap.read()

        if not ret:
            self.exit_process("Could not get frame")
            sys.exit()
        
        # フィルタ処理
        frame = self.apply_filters(frame)
        
        return frame
    
    # 以降、フレームに対する処理
    def process_continued_frames(self):
        while True:
            ret, self.new_frame = self.cap.read()
            
            if self.handle_fps():
                print("a")
                continue

            if not ret:
                self.exit_process("Could not get frame")
                break
            
            # フィルタ処理
            self.new_frame = self.apply_filters(self.new_frame)
            
            # 前フレームを縮小した画像
            reduced_image = self.apply_reduction(self.old_frame)

            # 画像を重ねる位置
            x_offset = ((self.new_frame.shape[1] - reduced_image.shape[1]) // 2) + X_OFFSET_ADJUSTMENT
            y_offset = ((self.new_frame.shape[0] - reduced_image.shape[0]) // 2) + Y_OFFSET_ADJUSTMENT
            
            composite_image = self.apply_overlay(self.new_frame, reduced_image, x_offset, y_offset)
            
            self.display_image = composite_image

            # キー入力処理
            if self.handle_key_event(cv2.waitKey(1) & 0xFF):
                break

            # 表示・更新
            cv2.imshow("camera", self.display_image)
            self.old_frame = self.display_image

    # 適用するフィルタをここで選択
    def apply_filters(self, image):
        image = self.flip_image(image)
        #frame = self.apply_grayscale(frame)
        #image= self.apply_dithering(image, DOT_THRESHOLD)
        return image

    # ?
    def apply_dithering(self, image, threshold):
        _, dithered_image = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)
        return dithered_image

    # 映像を左右反転
    def flip_image(self, image):
        flipped_image = cv2.flip(image, 1)
        return flipped_image
    
    # グレースケール変換
    def apply_grayscale(self, image):
        processed_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return processed_image

    # 画像縮小
    def apply_reduction(self, image):
        width = int(image.shape[1] * REDUCTION_SCALE_PERCENT / 100)
        height = int(image.shape[0] * REDUCTION_SCALE_PERCENT / 100)
        dim = (width, height)
        reduced_image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

        return reduced_image
    
    # オフセット位置に画像を重ねる
    def apply_overlay(self, base_image, overlay_image, x_offset, y_offset):      
        h, w = overlay_image.shape[:2]
        composite_image = base_image.copy()
        
        # オーバーレイ画像がベース画像をはみ出さないようにする
        if x_offset < 0:
            overlay_image = overlay_image[:, abs(x_offset):]
            x_offset = 0
        if y_offset < 0:
            overlay_image = overlay_image[abs(y_offset):, :]
            y_offset = 0

        if x_offset + w > base_image.shape[1]:
            overlay_image = overlay_image[:, :base_image.shape[1] - x_offset]
        if y_offset + h > base_image.shape[0]:
            overlay_image = overlay_image[:base_image.shape[0] - y_offset, :]
        
        # 更新されたオーバーレイ画像のサイズを再取得
        h, w = overlay_image.shape[:2]
        
        # オーバーレイ画像が0の幅や高さを持たないことを確認
        if h > 0 and w > 0:
            composite_image[y_offset:y_offset + h, x_offset:x_offset + w] = overlay_image

        return composite_image
    
    # キー入力処理
    def handle_key_event(self, key):
        isExit = False
        if key == ord('r'):
            print("Key 'r' pressed")
            self.display_image = self.new_frame
        if key == ord('b'):
            pass
        if key == ord('q'):
            self.exit_process("Key 'q' pressed - Exiting")
            isExit = True

        return isExit
    
    def handle_fps(self):
        if self.frame_count > self.skip_frame_num:
            self.frame_count = 1
            return False
        
        self.frame_count += 1
        return True
    
    # カメラ情報
    def print_cam_info(self):
        print("width : "+str(self.cam_width))
        print("height: "+str(self.cam_height))
        print("fps   : "+str(self.cam_fps))

    # プログラム終了前処理
    def exit_process(self, text=""):
        print(text)
        self.cap.release()
        cv2.destroyAllWindows()


# クラスの使用例
if __name__ == "__main__":
    camera_processor = CameraProcessor(camera_index=0)
    camera_processor.process_first_frame()
    camera_processor.process_continued_frames()

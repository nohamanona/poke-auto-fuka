import cv2
import numpy as np

class VideoRead(object):
    def set_read_video(self):
        self.video_file = 'D:\\amarec\\test2.mp4'
        self.cap = cv2.VideoCapture(self.video_file) 
        print(self.cap.isOpened())
        self.cap.set(3, 1280)
        self.cap.set(4, 720)
        print(self.cap.get(3))
        print(self.cap.get(4))
        
    def read_video(self):
        _, img = self.cap.read()
        return img

    def __init__(self):
        self.set_read_video()

if __name__ == '__main__':
    obj = VideoRead()

    k = 0
    while k != 27:
        frame = obj.read_video()
        if frame is not None:
            cv2.imshow("fl", frame)
        k = cv2.waitKey(1)

        if k == ord('s'):
            import time
            cv2.imwrite('screenshot_%d.png' % int(time.time()), frame)
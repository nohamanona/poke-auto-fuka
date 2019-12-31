import cv2
import numpy as np
import serial
from stm.send_serial import SendSerial

class VolatileClassGet(object):
    def __init__(self):
        self.next_state = 'None'
        self.send_command = 'None'
        self._control_frame_count =0
        self.hatched_egg =0
        self.number_of_egg = 0
        self.one_egg_img = cv2.imread("data\\one_egg.png")
        self.not_egg = 0

    def state_action(self, frame ,key , num_egg, htc_egg):
        self.hatched_egg =htc_egg
        self.number_of_egg = num_egg
        self.action_frame = frame
        self.get_action(frame)

    def get_action(self,frame):
        #print(self._control_frame_count,'GET frame')
        if self._control_frame_count == 0:
            self.send_command = 'Button A'
            self._control_frame_count += 1
        elif self._control_frame_count == 80:
            self.send_command = 'Button A'
            self._control_frame_count += 1
        elif self._control_frame_count == 320:
            self.send_command = 'Button A'
            self._control_frame_count += 1
        elif self._control_frame_count == 450:
            self.send_command = 'Button A'
            self._control_frame_count += 1
        elif self._control_frame_count == 550:
            self.send_command = 'Button A'
            self._control_frame_count +=1
        elif self._control_frame_count == 670:
            self.not_egg = self.detect_egg(frame)
            self.send_command = 'HAT BOTTOM'
            self._control_frame_count +=1
        elif self._control_frame_count == 680:
            if self.not_egg >= 2:
                self.send_command = 'HAT BOTTOM'
            self._control_frame_count +=1
        elif self._control_frame_count == 690:
            if self.not_egg >= 3:
                self.send_command = 'HAT BOTTOM'
            self._control_frame_count +=1
        elif self._control_frame_count == 700:
            if self.not_egg >= 4:
                self.send_command = 'HAT BOTTOM'
            self._control_frame_count +=1
        elif self._control_frame_count == 710:
            if self.not_egg >= 5:
                self.send_command = 'HAT BOTTOM'
            self._control_frame_count +=1
        elif self._control_frame_count == 720:
            self.send_command = 'Button A'
            self._control_frame_count +=1
            self.number_of_egg +=1
        elif self._control_frame_count == 900:
            self.send_command = 'Button A'
            self._control_frame_count +=1
        elif self._control_frame_count == 1000:
            self.send_command = 'Button A'
            self._control_frame_count +=1
        elif self._control_frame_count == 1050:
            self.send_command = 'None'
            self._control_frame_count =0
            self.next_state = 'RUN'

        else:
            self.send_command = 'None'
            self._control_frame_count += 1

    def detect_egg(self, frame):
        detect_egg = 0
        egg_tmprate = np.int8(self.one_egg_img)
        egg1 = np.int8(frame[209:295,57:450,:])
        egg2 = np.int8(frame[305:391,57:450,:])
        egg3 = np.int8(frame[401:487,57:450,:])
        egg4 = np.int8(frame[497:583,57:450,:])
        egg5 = np.int8(frame[593:679,57:450,:])
        egg1_dif = np.amax(abs(egg_tmprate - egg1))
        egg2_dif = np.amax(abs(egg_tmprate - egg2))
        egg3_dif = np.amax(abs(egg_tmprate - egg3))
        egg4_dif = np.amax(abs(egg_tmprate - egg4))
        egg5_dif = np.amax(abs(egg_tmprate - egg5))

        if egg1_dif > 10:
            detect_egg = 1
        elif egg2_dif > 10:
            detect_egg = 2
        elif egg3_dif > 10:
            detect_egg = 3
        elif egg4_dif > 10:
            detect_egg = 4
        elif egg5_dif > 10:
            detect_egg = 5
        print('detect egg = ',detect_egg)
        return detect_egg
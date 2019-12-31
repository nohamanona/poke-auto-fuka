import cv2
import numpy as np

class DrawingClass(object):
    def __init__(self):
        self.draw_command ='None'
        self.frame_count = 0
    def drawing(self, frame, fps, num_egg, htc_egg, state):
        cv2.putText(frame, 'FPS: {:.2f}'.format(fps),
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), thickness=2)
    
        cv2.putText(frame, 'Possessed EGG: {}'.format(num_egg),
                    (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 255), thickness=2)
        cv2.putText(frame, 'Hatched EGG: {}'.format(htc_egg),
                    (10, 130), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 255), thickness=2)
    
        cv2.putText(frame, 'State: {}'.format(state),
                    (250, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 255), thickness=2)
        return frame

    def draw_controler(self, frame, command):
        #print('draw',command)
        if command =='LX MIN':
            self.draw_command = 'LX MIN'
        elif command =='LX MAX':
            self.draw_command = 'LX MAX'
        elif command =='LY MIN':
            self.draw_command = 'LY MIN'
        elif command =='LY MAX':
            self.draw_command = 'LY MAX'
        elif command =='Button A':
            self.draw_command = 'Button A'
        elif command =='Button B':
            self.draw_command = 'Button B'
        elif command =='Button X':
            self.draw_command = 'Button X'
        elif command =='Button Y':
            self.draw_command = 'Button Y'
        elif command =='HAT TOP':
            self.draw_command = 'HAT TOP'
        elif command =='HAT RIGHT':
            self.draw_command = 'HAT RIGHT'
        elif command =='HAT BOTTOM':
            self.draw_command = 'HAT BOTTOM'
        elif command =='HAT LEFT':
            self.draw_command = 'HAT LEFT'
        elif command =='Button START':
            self.draw_command = 'Button START'
        elif command =='STOP':
            self.draw_command = 'STOP'

        #stick
        if self.draw_command =='LX MIN' or self.draw_command =='HAT LEFT':
            cv2.circle(frame, (970, 490), 20, (0, 0, 255), thickness=-1)
        elif self.draw_command =='LX MAX' or self.draw_command =='HAT RIGHT':
            cv2.circle(frame, (1030, 490), 20, (0, 0, 255), thickness=-1)
        elif self.draw_command =='LY MIN' or self.draw_command =='HAT TOP':
            cv2.circle(frame, (1000, 460), 20, (0, 0, 255), thickness=-1)
        elif self.draw_command =='LY MAX' or self.draw_command =='HAT BOTTOM':
            cv2.circle(frame, (1000, 520), 20, (0, 0, 255), thickness=-1)
        else:
            cv2.circle(frame, (1000, 490), 20, (0, 0, 255), thickness=-1)
        
        cv2.circle(frame, (1000, 490), 50, (0, 0, 255), thickness=2)

        #button
        if self.draw_command =='Button X':
            cv2.circle(frame, (1180, 460), 15, (0, 0, 255), thickness=-1)
            cv2.putText(frame, 'X',(1172, 468), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), thickness=2)
            self.frame_count +=1
        elif self.frame_count == 6:
            cv2.circle(frame, (1180, 460), 15, (0, 0, 255), thickness=2)
            cv2.putText(frame, 'X',(1172, 468), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), thickness=2)
            self.frame_count =0
            self.draw_command = 'None'
        else:
            cv2.circle(frame, (1180, 460), 15, (0, 0, 255), thickness=2)
            cv2.putText(frame, 'X',(1172, 468), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), thickness=2)
        if self.draw_command =='Button B':
            cv2.circle(frame, (1180, 520), 15, (0, 0, 255), thickness=-1)
            cv2.putText(frame, 'B',(1172, 528), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), thickness=2)
            self.frame_count +=1
        elif self.frame_count == 6:
            cv2.circle(frame, (1180, 520), 15, (0, 0, 255), thickness=2)
            cv2.putText(frame, 'B',(1172, 528), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), thickness=2)
            self.frame_count =0
            self.draw_command = 'None'
        else:
            cv2.circle(frame, (1180, 520), 15, (0, 0, 255), thickness=2)
            cv2.putText(frame, 'B',(1172, 528), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), thickness=2)
        if self.draw_command =='Button Y':
            cv2.circle(frame, (1150, 490), 15, (0, 0, 255), thickness=-1)
            cv2.putText(frame, 'Y',(1142, 498), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), thickness=2)
            self.frame_count +=1
        elif self.frame_count == 6:
            cv2.circle(frame, (1150, 490), 15, (0, 0, 255), thickness=2)
            cv2.putText(frame, 'Y',(1142, 498), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), thickness=2)
            self.frame_count =0
            self.draw_command = 'None'
        else:
            cv2.circle(frame, (1150, 490), 15, (0, 0, 255), thickness=2)
            cv2.putText(frame, 'Y',(1142, 498), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), thickness=2)
        if self.draw_command =='Button A':
            cv2.circle(frame, (1210, 490), 15, (0, 0, 255), thickness=-1)
            cv2.putText(frame, 'A',(1202, 498), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), thickness=2)
            self.frame_count +=1
        elif self.frame_count == 6:
            cv2.circle(frame, (1210, 490), 15, (0, 0, 255), thickness=2)
            cv2.putText(frame, 'A',(1202, 498), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), thickness=2)
            self.frame_count =0
            self.draw_command = 'None'
        else:
            cv2.circle(frame, (1210, 490), 15, (0, 0, 255), thickness=2)
            cv2.putText(frame, 'A',(1202, 498), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), thickness=2)
        if self.draw_command =='Button START':
            cv2.circle(frame, (1130, 423), 10, (0, 0, 255), thickness=-1)
            cv2.putText(frame, '+',(1120, 430), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), thickness=2)
            self.frame_count +=1
        elif self.frame_count == 6:
            cv2.circle(frame, (1130, 423), 10, (0, 0, 255), thickness=1)
            cv2.putText(frame, '+',(1120, 430), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), thickness=2)
            self.frame_count =0
            self.draw_command = 'None'
        else:
            cv2.circle(frame, (1130, 423), 10, (0, 0, 255), thickness=1)
            cv2.putText(frame, '+',(1120, 430), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), thickness=2)


        return frame
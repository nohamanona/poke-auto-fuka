import cv2
import numpy as np
import serial
from time import sleep
from transitions import Machine
from transitions.extensions.states import add_state_features, Volatile
from stm.stm_top import Model, CustomMachine
#from stm import stm_top
from stm.volatile_class_hatch import VolatileClassHatch
from stm.volatile_class_run import VolatileClassRun
from stm.volatile_class_prepare import VolatileClassPrepare
from stm.volatile_class_get import VolatileClassGet
from stm.send_serial import SendSerial

from capture.video_capture import VideoCapture
from capture.video_read import VideoRead
from capture.videoinput_wrapper import VideoInputWrapper

from show.drawing import DrawingClass

model = Model()
machine = CustomMachine(model=model, states=model.states, transitions=model.transitions, initial=model.states[0]["name"], 
                        auto_transitions=False, ordered_transitions=False) 

print('-------------------------start auto hatch program---------------------------')

capture = VideoCapture()
capture.reset()
capture.reset_tick()
capture.set_frame_rate()
capture.select_source(name=capture.DEV_AMAREC)

k=0
test_flg =0
test_cnt =0
#fps 
tm = cv2.TickMeter()
tm.start()
count = 0
max_count = 10
fps = 0

num_egg = 0
htc_egg = 0

draw_state = 'None'
draw = DrawingClass()

ser = SendSerial()

print('//////////////////////// ',model.state,' ////////////////////////')

model.fromSTANBYtoPREPARE()

img_a_breeder = cv2.imread("G:\\my documents\\VScode\\Python\\pokemon\\a_breeder.png")
img_a_breeder2 = cv2.imread("G:\\my documents\\VScode\\Python\\pokemon\\a_breeder2.png")

_breeder_comment = cv2.imread("data\\sora_sel.png")

while k != 27:
    frame = capture.read_frame()

    #ZNCC test ここから
    #gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    #temp = cv2.cvtColor(img_a_breeder2, cv2.COLOR_RGB2GRAY)
    #h, w = temp.shape
    #match = cv2.matchTemplate(gray, temp, cv2.TM_CCOEFF_NORMED)
    #min_value, max_value, min_pt, max_pt = cv2.minMaxLoc(match)
    #pt = max_pt
    #cv2.rectangle(frame, (pt[0], pt[1] ), (pt[0] + w, pt[1] + h), (0,0,200), 3)
    #cv2.putText(frame, 'ZNCC: {:.2f}'.format(max_value),
    #                   (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), thickness=2)
    




    #fps
    if count == max_count:
        tm.stop()
        fps = max_count / tm.getTimeSec()
        tm.reset()
        tm.start()
        count = 0
    count += 1

    if frame is not None:
        model.scope.state_action(frame, k, num_egg, htc_egg)

        frame = model.scope.action_frame

        num_egg = model.scope.number_of_egg
        htc_egg = model.scope.hatched_egg

        #print('state', model.state, 'next_state', model.scope.next_state)

        if (model.state == 'PREPARE') and (model.scope.next_state == 'RUN'):
            model.fromPREPAREtoRUN()
        elif (model.state == 'RUN') and (model.scope.next_state == 'HATCH'):
            model.fromRUNtoHATCH()
        elif (model.state == 'HATCH') and (model.scope.next_state == 'RUN'):
            model.fromHATCHtoRUN()
        elif (model.state == 'RUN') and (model.scope.next_state == 'GET'):
            model.fromRUNtoGET()
        elif (model.state == 'GET') and (model.scope.next_state == 'RUN'):
            model.fromGETtoRUN()

        draw_state = model.state
        frame = draw.drawing(frame, fps, num_egg, htc_egg, draw_state)
        frame = draw.draw_controler(frame, model.scope.send_command)

    #if frame is not None:
        cv2.imshow("fl", frame)
    k = cv2.waitKey(1)

    if k == ord('q'):
        import time
        cv2.imwrite('screenshot_%d.png' % int(time.time()), frame)

    if k == ord('t'):
        _check_frame = np.int8(frame[270:320,512:550,:])
        frame_dif = np.amax(abs(np.int8(_breeder_comment) - _check_frame))
        cv2.imshow("f", _check_frame)
        if frame_dif <= 10:
            print('T')
        else:print('F',frame_dif)

    if k == ord('g'):
        ser.send_command_start('LY MAX')
        sleep(0.3)
        ser.send_command_start('LX MAX')
        sleep(0.4)
        ser.send_command_start('LY MIN')
        sleep(0.04)
        ser.send_command_stop()

            


    ser.command_cont(k, model.scope.send_command)
    

    


class VolatileClassHatch(object):
    def __init__(self):
        self.next_state = 'None'
        self._control_frame_count = 0
        self.number_of_egg = 12
        self.hatched_egg = -2
        self.out_key = 'None'
        self.dst = 0
        self.send_command = 'None'
        
        #print('oya detected.')

    def hatch_command(self):
        if self._control_frame_count == 10:
            self.send_command = 'Button A'
            self._control_frame_count +=1
        elif self._control_frame_count == 930:
            self.send_command = 'Button A'
            self._control_frame_count +=1
        #elif self._control_frame_count == 1100:
        #    self.send_command = 'Button A'
        #    self._control_frame_count +=1
        elif self._control_frame_count == 1100:
            self._control_frame_count =0
            self.hatched_egg =self.hatched_egg +1
            self.number_of_egg = self.number_of_egg -1
            self.next_state = 'RUN'
        else:
            self.send_command = 'None'
            self._control_frame_count +=1

    def hatch_action(self, frame):
        self.hatch_command()
        


    def state_action(self, frame, key, num_egg, htc_egg):
        self.number_of_egg = num_egg
        self.hatched_egg =htc_egg
        self.action_frame = frame
        self.hatch_action(frame)
        #self.next_state = 'RUN'
        
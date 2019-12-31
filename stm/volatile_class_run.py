import cv2
import numpy as np
from time import sleep
class VolatileClassRun(object):
    width = int(1280/2)
    height = int(720/2)

    ALGOLISM='USURF'#'AKAZE', 'SURF', 'USURF', 'FAST'
    MIN_MATCH_COUNT =0
    ratio = 0.0

    breeder_house_img = cv2.imread("data\\breeder_house.png")

    

 
    def __init__(self):
        self.next_state = 'None'
        self.number_of_egg = 11
        self.hatched_egg = 0
        self._detect_frame_count = 0
        self._good = []
        self._good_without_list = []
        self._bf = cv2.BFMatcher()
        self._breeder_house_flg=0
        self.send_command = 'None'
        self._send_command_enb =0
        self._control_frame_count = 0
        self._temp_y = 408
        self.run_control_state = 'None'
        self.a_breeder_count =0
        self.run_l_count = 0
        self._sel_poke_flg = 0

        self._breeder_comment = cv2.imread("data\\breeder_comment.png")
        self._sora_sel_img = cv2.imread("data\\sora_sel.png")

        self.cut_frame_h = 237
        self.cut_frame_w = 1280
        self.cross_arm_breeder1 = cv2.imread("data\\a_breeder1.png")
        self.cross_arm_breeder2 = cv2.imread("data\\a_breeder2.png")
        self.cross_arm_breeder3 = cv2.imread("data\\a_breeder3.png")
        self.breeder1 = cv2.imread("data\\breeder1.png")
        self.breeder2 = cv2.imread("data\\breeder2.png")
        self.breeder3 = cv2.imread("data\\breeder3.png")
        self.f_a_breeder = cv2.imread("data\\f_a_breeder_hand.png")
        self.f_breeder3 = cv2.imread("data\\f_breeder_hand.png")
        self.menu_sel_poke = cv2.imread("data\\menu_sel_poke.png")
        self.gray_cross_arm_breeder1 = cv2.cvtColor(self.cross_arm_breeder1, cv2.COLOR_RGB2GRAY)
        self.gray_cross_arm_breeder2 = cv2.cvtColor(self.cross_arm_breeder2, cv2.COLOR_RGB2GRAY) 
        self.gray_cross_arm_breeder3 = cv2.cvtColor(self.cross_arm_breeder3, cv2.COLOR_RGB2GRAY)
        self.gray_breeder1 = cv2.cvtColor(self.breeder1, cv2.COLOR_RGB2GRAY)
        self.gray_breeder2 = cv2.cvtColor(self.breeder2, cv2.COLOR_RGB2GRAY) 
        self.gray_breeder3 = cv2.cvtColor(self.breeder3, cv2.COLOR_RGB2GRAY)
        self.gray_f_a_breeder = cv2.cvtColor(self.f_a_breeder, cv2.COLOR_RGB2GRAY) 
        self.gray_f_breeder = cv2.cvtColor(self.f_breeder3, cv2.COLOR_RGB2GRAY)
        self.ah1, self.aw1 = self.gray_cross_arm_breeder1.shape
        self.ah2, self.aw2 = self.gray_cross_arm_breeder2.shape
        self.ah3, self.aw3 = self.gray_cross_arm_breeder3.shape
        self.h1, self.w1 = self.gray_breeder1.shape
        self.h2, self.w2 = self.gray_breeder2.shape
        self.h3, self.w3 = self.gray_breeder3.shape
        self.hf, self.wf = self.gray_f_breeder.shape
        #self.gray_cross_arm_breeder1 = np.array(self.gray_cross_arm_breeder1, dtype="float")
        #self.gray_cross_arm_breeder2 = np.array(self.gray_cross_arm_breeder2, dtype="float")
        #self.gray_cross_arm_breeder3 = np.array(self.gray_cross_arm_breeder3, dtype="float")
        self.mu_t1 = np.mean(self.gray_cross_arm_breeder1)
        self.mu_t2 = np.mean(self.gray_cross_arm_breeder2)
        self.mu_t3 = np.mean(self.gray_cross_arm_breeder3)
        self.temp1 = self.gray_cross_arm_breeder1 - self.mu_t1
        self.temp2 = self.gray_cross_arm_breeder2 - self.mu_t2
        self.temp3 = self.gray_cross_arm_breeder3 - self.mu_t3
        #self.dst = 0
        if VolatileClassRun.ALGOLISM == 'AKAZE':
            VolatileClassRun.MIN_MATCH_COUNT=20 #あんまりすくないとfindHomographyがNoneになる
            VolatileClassRun.ratio = 0.7
            self._akaze = cv2.AKAZE_create() 
            self._kp1, self._des1 = self._akaze.detectAndCompute(VolatileClassRun.breeder_house_img, None)
        elif VolatileClassRun.ALGOLISM == 'SURF':
            VolatileClassRun.MIN_MATCH_COUNT=30 #あんまりすくないとfindHomographyがNoneになる
            VolatileClassRun.ratio = 0.5
            self._surf = cv2.xfeatures2d.SURF_create(400)
            self._kp1, self._des1 = self._surf.detectAndCompute(VolatileClassRun.breeder_house_img,None)
        elif VolatileClassRun.ALGOLISM == 'USURF':
            VolatileClassRun.MIN_MATCH_COUNT=18 #あんまりすくないとfindHomographyがNoneになる
            VolatileClassRun.ratio = 0.6
            self._surf = cv2.xfeatures2d.SURF_create(400)
            self._surf.setUpright(True)
            self._kp1, self._des1 = self._surf.detectAndCompute(VolatileClassRun.breeder_house_img,None)
        elif VolatileClassRun.ALGOLISM == 'FAST':
            VolatileClassRun.MIN_MATCH_COUNT=30 #あんまりすくないとfindHomographyがNoneになる
            VolatileClassRun.ratio = 0.5
            self._fast = cv2.FastFeatureDetector_create()
            self._brief = cv2.xfeatures2d.BriefDescriptorExtractor_create()
            self._kp1 = self._fast.detect(VolatileClassRun.breeder_house_img,None)
            self._kp1, self._des1 = self._brief.compute(VolatileClassRun.breeder_house_img, self._kp1)
        self.matches = self._bf.knnMatch(self._des1, self._des1, k=2)

    def detect_breeder(self, frame):
        frame_resize = cv2.resize(frame,(VolatileClassRun.width,VolatileClassRun.height))
        
        if self._detect_frame_count==0:
            if VolatileClassRun.ALGOLISM=='AKAZE':
                self._kp2, self._des2 = self._akaze.detectAndCompute(frame_resize, None)
            elif VolatileClassRun.ALGOLISM=='SURF':
                self._kp2, self._des2 = self._surf.detectAndCompute(frame_resize,None)
            elif VolatileClassRun.ALGOLISM=='USURF':
                self._kp2, self._des2 = self._surf.detectAndCompute(frame_resize,None)
            elif VolatileClassRun.ALGOLISM=='FAST':
                self._kp2 = self._fast.detect(frame_resize,None)
                self._kp2, self._des2 = self._brief.compute(frame_resize, self._kp2)   
            if self._des2 is not None:
                self.matches = self._bf.knnMatch(self._des1, self._des2, k=2)
                self._good = []
                self._good_without_list = []
                for m, n in self.matches:
                    if m.distance < VolatileClassRun.ratio * n.distance:
                        self._good.append([m])
                        self._good_without_list.append(m)

        if len(self._good)>VolatileClassRun.MIN_MATCH_COUNT:
            if self._des2 is not None:
                src_pts = np.float32([ self._kp1[m.queryIdx].pt for m in self._good_without_list ]).reshape(-1,1,2)
                dst_pts = np.float32([ self._kp2[m.trainIdx].pt for m in self._good_without_list ]).reshape(-1,1,2)
            
                M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
                #self.matchesMask = mask.ravel().tolist()
                h,w,c = VolatileClassRun.breeder_house_img.shape
                pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
                if M is not None:
                    if pts is not None:
                        dst = cv2.perspectiveTransform(pts,M)*2
                        self.center_bottom = (dst[1]+dst[2])/2 #[[x,y]]
                    else:dst=[[[0,0]],[[0,0]],[[0,0]],[[0,0]]]
                else:
                    dst=[[[0,0]],[[0,0]],[[0,0]],[[0,0]]]
                    self.center_bottom = [[0,0]]
                if self.center_bottom[0][0] >= 500 and self.center_bottom[0][0] <=800:
                    self.center_flg = 1
                else:
                    self.center_flg = 0
                #print(self.center_bottom[0],self.center_bottom[0][0])
                frame = cv2.polylines(frame,[np.int32(dst)],True,(255,255,0),3, cv2.LINE_AA)
                #breeder_place = np.int32(dst[1]+(dst[2]-dst[1])/4)
                #print(breeder_place[0])
                #frame = cv2.circle(frame,tuple(breeder_place[0]),5,(0,0,255),3,cv2.LINE_AA)
            self._breeder_house_flg = 1
        else:
            self._breeder_house_flg = 0
            self.center_flg = 0
        self.action_frame = frame

        if self._detect_frame_count==5:
            self._detect_frame_count=0
        else:
            self._detect_frame_count = self._detect_frame_count +1

        #else:
        #    self.matchesMask = None

    def zncc(self, frame):
        if self.center_bottom[0][0]<50:
            zncc_x = 50
        else:
            zncc_x = self.center_bottom[0][0]
        cut_frame = frame[286:523,0:int(zncc_x),:]
        gray = cv2.cvtColor(cut_frame, cv2.COLOR_RGB2GRAY)
        
        #score = np.empty((self.cut_frame_h-self.h1, self.cut_frame_w-self.w1))
        #gray = np.array(gray, dtype="float")
        #遠い breeder3
        #for dy in range(0, 11):#self.cut_frame_h - self.h1):
        #    for dx in range(0, self.cut_frame_w - self.w1):
        #        roi = gray[dy:dy + self.h3, dx:dx + self.w3]
        #        score[dy, dx] = self.zncc_pix_score(roi, self.temp3)

        #for dy in range(11, 42):
        #    for dx in range(0, self.cut_frame_w - self.w1):
        #        roi = gray[dy:dy + self.h2, dx:dx + self.w2]
        #        score[dy, dx] = self.zncc_pix_score(roi, self.temp2)

        #for dy in range (42, self.cut_frame_h - self.h1):
        #    for dx in range(0, self.cut_frame_w - self.w1):
        #        roi = gray[dy:dy + self.h1, dx:dx + self.w1]
        #        score[dy, dx] = self.zncc_pix_score(roi, self.temp1)
        gray1a = gray[42:self.cut_frame_h,:]
        gray2a = gray[11:(42 + self.ah2),:]
        gray3a = gray[0:(11+self.ah3),:]
        gray1 = gray[42:self.cut_frame_h,:]
        gray2 = gray[11:(42 + self.h2),:]
        gray3 = gray[0:(11+self.h3),:]
        match1a = cv2.matchTemplate(gray1a, self.gray_cross_arm_breeder1, cv2.TM_CCOEFF_NORMED)
        match2a = cv2.matchTemplate(gray2a, self.gray_cross_arm_breeder2, cv2.TM_CCOEFF_NORMED)
        match3a = cv2.matchTemplate(gray3a, self.gray_cross_arm_breeder3, cv2.TM_CCOEFF_NORMED)
        _, max_value1a, _, max_pt1a = cv2.minMaxLoc(match1a)
        _, max_value2a, _, max_pt2a = cv2.minMaxLoc(match2a)
        _, max_value3a, _, max_pt3a = cv2.minMaxLoc(match3a)
        if max_value1a>=max_value2a and max_value1a>=max_value3a:
            pt_a = max_pt1a
            max_value_a = max_value1a
        elif max_value2a>=max_value1a and max_value2a>=max_value3a:
            pt_a = max_pt2a
            max_value_a = max_value2a
        else:
            pt_a = max_pt3a
            max_value_a = max_value3a
        match1 = cv2.matchTemplate(gray1, self.gray_breeder1, cv2.TM_CCOEFF_NORMED)
        match2 = cv2.matchTemplate(gray2, self.gray_breeder2, cv2.TM_CCOEFF_NORMED)
        match3 = cv2.matchTemplate(gray3, self.gray_breeder3, cv2.TM_CCOEFF_NORMED)
        _, max_value1, _, max_pt1 = cv2.minMaxLoc(match1)
        _, max_value2, _, max_pt2 = cv2.minMaxLoc(match2)
        _, max_value3, _, max_pt3 = cv2.minMaxLoc(match3)
        if max_value1>=max_value2 and max_value1>=max_value3:
            pt = max_pt1
            max_value = max_value1
        elif max_value2>=max_value1 and max_value2>=max_value3:
            pt = max_pt2
            max_value = max_value2
        else:
            pt = max_pt3
            max_value = max_value3
        #pt = np.unravel_index(score.argmin(), score.shape)
        if max_value >= max_value_a:
            if pt[1]<= 11:
                draw_h = self.h3
                draw_w = self.w3
                pt_1= pt[1]+ 286
            elif pt[1] <= 42:
                draw_h = self.h2
                draw_w = self.w2
                pt_1 = pt[1]+ 307
            else:
                draw_h = self.h1
                draw_w = self.w1
                pt_1= pt[1] + 372  
            cv2.rectangle(self.action_frame, (pt[0], pt_1 ), (pt[0] + draw_w, pt_1 + draw_h), (0,200,0), 3)
        else:
            pt = pt_a
            if pt[1]<= 11:
                draw_h = self.ah3
                draw_w = self.aw3
                pt_1= pt[1]+ 286
            elif pt[1] <= 42:
                draw_h = self.ah2
                draw_w = self.aw2
                pt_1 = pt[1]+ 307
            else:
                draw_h = self.ah1
                draw_w = self.aw1
                pt_1= pt[1] + 372  
            cv2.rectangle(self.action_frame, (pt[0], pt_1 ), (pt[0] + draw_w, pt_1 + draw_h), (0,0,200), 3)
            self.a_breeder_count +=1

    def zncc_pix_score(self, roi ,temp):
        mu_r = np.mean(roi)
        roi = roi - mu_r
        num = np.sum(roi * temp)
        den = np.sqrt( np.sum(roi ** 2) ) * np.sqrt( np.sum(temp ** 2) ) 
        if den == 0: score = 0
        score = num / den
        return score

    def f_zncc(self, frame):
        self.send_command = 'None'
        cut_frame_f = frame[394:416,430:440,:]
        gray_f = cv2.cvtColor(cut_frame_f, cv2.COLOR_RGB2GRAY)

        match_f = cv2.matchTemplate(gray_f, self.gray_f_breeder, cv2.TM_CCOEFF_NORMED)
        match_f_a = cv2.matchTemplate(gray_f, self.gray_f_a_breeder, cv2.TM_CCOEFF_NORMED)
        _, max_value_f, _, _ = cv2.minMaxLoc(match_f)
        _, max_value_f_a, _, _ = cv2.minMaxLoc(match_f_a)
        if max_value_f > max_value_f_a:
            print('not a')
            self.run_control_state = 'AG'
        else:
            print('a')
            self.run_control_state = 'RUN GET'

    def run_control(self,frame):
        if self.run_control_state == 'AP':
            self.run_ap()
        elif self.run_control_state =='RUN R':
            self.run_r()
        elif self.run_control_state =='RUN L':
            self.run_l()
        elif self.run_control_state == 'TURN R':
            self.turn_r()
        elif self.run_control_state == 'SORA':
            self.sora(frame)
        elif self.run_control_state == 'SORA2':
            self.sora2(frame)
        elif self.run_control_state == 'SEL GET':
            self.f_zncc(frame)
        elif self.run_control_state == 'RUN GET':
            self.run_get(frame)
        elif self.run_control_state == 'AG':
            self.run_ag()
        elif self.run_control_state == 'GET NO EGG':
            self.get_no_egg()


    def run_ap(self):
        if self._control_frame_count ==0:
            self.send_command = 'LY MAX'
            self._control_frame_count +=1
        elif self._control_frame_count == 17:
            self.send_command = 'STOP'
            self._control_frame_count +=1
        elif self._control_frame_count == 25:
            self.send_command = 'LX MAX'
            self._control_frame_count +=1
        elif self._control_frame_count == 28:
            self.send_command = 'STOP'
            self._control_frame_count +=1
        elif self._control_frame_count == 30:
            self.send_command = 'Button START'
            self._control_frame_count +=1
        elif self._control_frame_count == 32:
            self.send_command = 'STOP'
            self._control_frame_count +=1
        elif self._control_frame_count == 33:
            self.send_command = 'None'
            self._control_frame_count =0
            self.run_control_state = 'RUN R'
        else:
            self.send_command = 'None'
            self._control_frame_count +=1
    
    def run_ag(self):
        if self._control_frame_count ==0:
            self.send_command = 'RUN 2 RUN_R'
            self._control_frame_count +=1
        elif self._control_frame_count == 1:
            self.send_command = 'None'
            self._control_frame_count =0
            self.run_control_state = 'RUN R'
        else:
            self.send_command = 'None'
            self._control_frame_count +=1
        
    def run_r(self):
        if self._control_frame_count ==0:
            self.send_command = 'LX MAX'
            self._control_frame_count +=1
        elif self._control_frame_count == 20:
            self.send_command= 'I B'
            self._control_frame_count +=1
        elif self._control_frame_count == 22:
            self.send_command= 'STOP'
            self.send_command = 'LX MAX'
            self._control_frame_count +=1
        elif self._control_frame_count == 300:
            self.send_command= 'STOP'
            self._control_frame_count +=1
        elif self._control_frame_count == 330:
            self.send_command = 'None'
            self._control_frame_count =0
            self.run_control_state = 'RUN L'
        else:
            self.send_command = 'None'
            self._control_frame_count +=1

    def run_l(self):
        #print('run l', self._control_frame_count)
        if self._control_frame_count == 0:
            self.send_command = 'I LX MIN'
            self._control_frame_count +=1
        elif self._control_frame_count == 1:
            self.send_command = 'STOP'
            self._control_frame_count +=1
        elif self._control_frame_count == 10:
            self.send_command = 'LX MIN'
            self._control_frame_count +=1
        elif self._control_frame_count == 15:
            self.send_command = 'LY MIN'
            self._control_frame_count +=1
        elif self._control_frame_count == 17:
            self.send_command = 'LX MIN'
            self._control_frame_count +=1
        elif self.center_flg==1:
            self.send_command = 'STOP'
            self._control_frame_count =0
            self._temp_y = self.center_bottom[0][1]
            if (self.run_l_count >= 1) and (self.number_of_egg <=4):
                self.run_control_state = 'SORA'
                self.run_l_count =0
            else:
                self.run_control_state = 'TURN R'
                self.run_l_count +=1
                print(self.run_l_count,'run_l_count')
        elif self._control_frame_count == 2000:
            self.send_command = 'STOP'
            self._control_frame_count =0
            if self.number_of_egg <=4:
                self.run_control_state = 'SORA2'
                self.run_l_count =0
            else:
                self.run_control_state = 'TURN R'
                self.run_l_count +=1
                print(self.run_l_count,'run_l_count')
        else:
            self.send_command = 'None'
            self._control_frame_count +=1

    def turn_r(self):
        if self._control_frame_count ==20:
            self.send_command = 'I LX MAX'
            self._control_frame_count +=1
        elif self._control_frame_count == 21:
            self.send_command = 'STOP'
            self._control_frame_count +=1
        elif self._control_frame_count == 30:
            self.send_command = 'None'
            self._control_frame_count =0
            self.run_control_state = 'RUN R'
        else:
            self.send_command = 'None'
            self._control_frame_count +=1

    def run_get(self,frame):
        if self._control_frame_count == 50:
            self.send_command = 'RUN BRE'
            self._control_frame_count +=1
        #    self.send_command = 'LX MIN'
        #    self._control_frame_count +=1
        #elif self._control_frame_count == 1:
        #    sleep(0.5)
        #    self.send_command = 'STOP'
        #    self._control_frame_count +=1
        #elif self._control_frame_count == 5:
        #    self.send_command = 'LY MIN'
        #    self._control_frame_count +=1
        #elif self._control_frame_count == 6:
        #    sleep(0.3)
        #    self.send_command = 'STOP'
        #    self._control_frame_count +=1
        elif self._control_frame_count == 60:
            self.send_command = 'Button A'
            self._control_frame_count +=1
        elif self._control_frame_count == 150:
            check = self.check_comment(frame)
            if check== True:
                self.send_command = 'None'
                self._control_frame_count =0
                self.next_state = 'GET'
            else:
                self.send_command = 'None'
                self._control_frame_count =0
                self.run_control_state = 'GET NO EGG'
        else:
            self.send_command = 'None'
            self._control_frame_count +=1

    def check_comment(self,frame):
        _check_frame = np.int8(frame[600:700,280:900,:])
        frame_dif = np.amax(abs(np.int8(self._breeder_comment) - _check_frame))
        if frame_dif <= 10:
            check_comment_bool = True
        else:check_comment_bool = False
        return check_comment_bool 

    def get_no_egg(self):
        if self._control_frame_count ==0:
            self.send_command = 'Button B'
            self._control_frame_count +=1
        elif self._control_frame_count == 120:
            self.send_command = 'Button B'
            self._control_frame_count +=1
        elif self._control_frame_count == 240:
            self.send_command = 'Button B'
            self._control_frame_count +=1
        elif self._control_frame_count == 360:
            self.send_command = 'None'
            self._control_frame_count =0
            self.run_control_state = 'AG'
        else:
            self.send_command = 'None'
            self._control_frame_count +=1


    def sora(self, frame):
        #print('sora', self._control_frame_count)
        if self._control_frame_count == 0:
            #self.send_command = 'Button START'
            self._control_frame_count +=1
        elif self._control_frame_count == 40:
            self.send_command = 'Button X'
            self._control_frame_count +=1
        elif self._control_frame_count == 100:
            self.menu_sel_det(frame)
            self._control_frame_count +=1
            print('chk poke')
        elif self._sel_poke_flg == 1:
            if self._control_frame_count == 101:
                self.send_command = 'HAT BOTTOM'
                self._control_frame_count +=1
            elif self._control_frame_count == 106:
                self.send_command = 'HAT LEFT'
                self._control_frame_count +=1
            elif self._control_frame_count == 111:
                self.send_command = 'Button A'
                self._control_frame_count +=1
            elif self._control_frame_count == 260:
                self.send_command = 'SEL SORA'
                self._control_frame_count +=1
            #elif self._control_frame_count == 260:
            #    self.send_command = 'HAT BOTTOM'
            #    self._control_frame_count +=1
            elif self._control_frame_count == 340:
                check_sora = self.check_sora_sel(frame)
                if check_sora is not True:
                    self.send_command = 'Button A'
                    self._control_frame_count +=1
                else:
                    self.send_command = 'Button X'
                    self._control_frame_count = 150
            elif self._control_frame_count == 390:
                self.send_command = 'Button A'
                self._control_frame_count +=1
            elif self._control_frame_count == 490:
                self.send_command = 'None'
                self._control_frame_count =0
                self.run_control_state = 'SEL GET'
            else:
                self.send_command = 'None'
                self._control_frame_count +=1
        else:
            if self._control_frame_count == 110:
                self.send_command = 'Button A'
                self._control_frame_count +=1
            elif self._control_frame_count == 260:
                self.send_command = 'SEL SORA'
                self._control_frame_count +=1
            #elif self._control_frame_count == 260:
            #    self.send_command = 'HAT BOTTOM'
            #    self._control_frame_count +=1
            elif self._control_frame_count == 340:
                self.send_command = 'Button A'
                self._control_frame_count +=1
            elif self._control_frame_count == 390:
                self.send_command = 'Button A'
                self._control_frame_count +=1
            elif self._control_frame_count == 490:
                self.send_command = 'None'
                self._control_frame_count =0
                self.run_control_state = 'SEL GET'
                print('sora fin')
            else:
                self.send_command = 'None'
                self._control_frame_count +=1
    def sora2(self, frame):
        #print('sora', self._control_frame_count)
        if self._control_frame_count == 0:
            #self.send_command = 'Button START'
            self._control_frame_count +=1
        elif self._control_frame_count == 40:
            self.send_command = 'Button X'
            self._control_frame_count +=1
        elif self._control_frame_count == 100:
            self.menu_sel_det(frame)
            self._control_frame_count +=1
            print('chk poke')
        elif self._sel_poke_flg == 1:
            if self._control_frame_count == 101:
                self.send_command = 'HAT BOTTOM'
                self._control_frame_count +=1
            elif self._control_frame_count == 106:
                self.send_command = 'HAT LEFT'
                self._control_frame_count +=1
            elif self._control_frame_count == 111:
                self.send_command = 'Button A'
                self._control_frame_count +=1
            elif self._control_frame_count == 260:
                self.send_command = 'HAT RIGHT'
                self._control_frame_count +=1
            elif self._control_frame_count == 320:    
                self.send_command = 'SEL SORA'
                self._control_frame_count +=1
            #elif self._control_frame_count == 260:
            #    self.send_command = 'HAT BOTTOM'
            #    self._control_frame_count +=1
            elif self._control_frame_count == 400:
                check_sora = self.check_sora_sel(frame)
                if check_sora is not True:
                    self.send_command = 'Button A'
                    self._control_frame_count +=1
                else:
                    self.send_command = 'Button X'
                    self._control_frame_count = 150
            elif self._control_frame_count == 450:
                self.send_command = 'Button A'
                self._control_frame_count +=1
            elif self._control_frame_count == 550:
                self.send_command = 'None'
                self._control_frame_count =0
                self.run_control_state = 'SEL GET'
            else:
                self.send_command = 'None'
                self._control_frame_count +=1
        else:
            if self._control_frame_count == 110:
                self.send_command = 'Button A'
                self._control_frame_count +=1
            elif self._control_frame_count == 260:
                self.send_command = 'HAT RIGHT'
                self._control_frame_count +=1
            elif self._control_frame_count == 320: 
                self.send_command = 'SEL SORA'
                self._control_frame_count +=1
            #elif self._control_frame_count == 260:
            #    self.send_command = 'HAT BOTTOM'
            #    self._control_frame_count +=1
            elif self._control_frame_count == 400:
                self.send_command = 'Button A'
                self._control_frame_count +=1
            elif self._control_frame_count == 450:
                self.send_command = 'Button A'
                self._control_frame_count +=1
            elif self._control_frame_count == 550:
                self.send_command = 'None'
                self._control_frame_count =0
                self.run_control_state = 'SEL GET'
                print('sora fin')
            else:
                self.send_command = 'None'
                self._control_frame_count +=1

    def check_sora_sel(self,frame):
        _check_frame = np.int8(frame[270:320,512:550,:])
        frame_dif = np.amax(abs(self._sora_sel_img - _check_frame))
        if frame_dif <= 10:
            check_sora_bool = True
        else:check_sora_bool = False
        return check_sora_bool 

    def menu_sel_det(self,frame):
        cut_menu_frame_poke = frame[89:238,370:480,:]
        cut_menu_frame_poke = np.int8(cut_menu_frame_poke)
        menu_poke_tmp = np.int8(self.menu_sel_poke)
        dif_menu_poke = np.amax(abs(menu_poke_tmp - cut_menu_frame_poke))
        if dif_menu_poke <= 10:
            self._sel_poke_flg = 1
        else:
            self._sel_poke_flg =0

    #def adj_axis(self):
    #    pass


            
#        if self._breeder_house_flg:
#            if self.center_bottom[0][0] >545 and self.center_bottom[0][0] <693:
#                if self._send_command_enb ==0:
#                    self._temp_y = self.center_bottom[0][1]
#                if self._temp_y > 418:
#                    print('ue', self._temp_y,self._control_frame_count)
#                    self._control_frame_count +=1
#                    if self._control_frame_count ==1:
#                        self.send_command = 'LY MAX'
#                        self._send_command_enb =1
#                    elif self._control_frame_count ==(self._temp_y - 418):
#                        self.send_command = 'STOP'
#                        self._send_command_enb =0
#                        self._control_frame_count =0
#                    else:
#                        self.send_command = 'None'
#
#
#                elif self.center_bottom[0][1] < 398:
#                    print('sita')
#                    self.send_command = 'LY MIN'
#                    self._send_command_enb =1
#                elif self._send_command_enb ==1:
#                    self.send_command = 'STOP'
#                    self._send_command_enb =0
#                else:
#                    self.send_command ='None'
#            elif self._send_command_enb ==1:
#                self.send_command = 'STOP'
#                self._send_command_enb =0
#            else:
#                self.send_command ='None'
        

    def run_action(self,frame):
        #print('run run run')
        self.detect_oya(frame)
        self.action_frame = frame
        self.detect_breeder(frame)
        if self._breeder_house_flg:
            self.zncc(frame)
        self.run_control(frame)

    def detect_oya(self, frame):
        oya_img = np.int8(cv2.imread('data/oya.png'))
        oya_frame = np.int8(frame[595:635,275:445,:])
        oya_dif = np.amax(abs(oya_img - oya_frame))
        if oya_dif <= 10:
            print('detect oya!')
            print(self.next_state)
            self.next_state = 'HATCH'
    
    def show_oya(self):
        oya_img = cv2.imread('data/oya.png')
        cv2.imshow('img',oya_img)
        cv2.waitKey(0)


    def state_action(self, frame ,key , num_egg, htc_egg):
        self.number_of_egg = num_egg
        self.hatched_egg =htc_egg
        self.run_action(frame)
        

if __name__ == "__main__":
    obj = VolatileClassRun()
    frame = 0
    obj.show_oya(frame)
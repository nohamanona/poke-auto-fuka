import cv2
import threading
import os
import time
from capture.videoinput_wrapper import VideoInputWrapper
#from offset import OffsetFilter

class VideoCapture(object):
    
    def __init__(self):
        self._videoinput_wrapper = VideoInputWrapper()
        self.lock=threading.Lock()
        self._device_id = None
        self.DEV_AMAREC = "AmaRec Video Capture"
        self.cap_recorded_video = False
        self.fps_requested = None
        self.frame_skip_rt = None
        self.output_geometry = (720, 1280)
        self.effective_lines = 720
        self.cap_optimal_input_resolution = True
        self.is_realtime = True
        self.last_tick=0

    def reset(self):
        pass

    def reset_tick(self):
        self._base_tick = int(time.time() * 1000)
        self.last_tick = 0

    def select_source(self, index=None, name=None):
        by_index = (index is not None)
        by_name = (name is not None)
        assert by_index or by_name
        assert not (by_index and by_name)
        if by_index:
            r = self._select_device_by_index_func(index)
        else:
            r = self._select_device_by_name_func(name)
        self.set_frame_rate(None)  # Default framerate

    def set_frame_rate(self, fps=None, realtime=False):
        self.fps_requested = fps
        self.frame_skip_rt = realtime

    def _select_device_by_index_func(self, source, width=1280, height=720, framerate=59.94):
        device_id = int(source)
        vi = self._videoinput_wrapper
        self.lock.acquire()

        try:
            if self._device_id is not None:
                raise Exception('Need to deinit the device')

            formats = [
                {'width': width, 'height': height, 'framerate': None},
                {'width': width, 'height': height, 'framerate': framerate},
            ]

            for fmt in formats:
                if fmt['framerate']:
                    vi.set_framerate(device_id, fmt['framerate'])

                retval = vi.init_device(
                    device_id,
                    flags=self._videoinput_wrapper.DS_RESOLUTION,
                    width=fmt['width'],
                    height=fmt['height'],
                )
                if retval:
                    self._source_width = vi.get_frame_width(device_id)
                    self._source_height = vi.get_frame_height(device_id)

                    success = \
                        (width == self._source_width) and (
                            height == self._source_height)

                    if success or (not self.cap_optimal_input_resolution):
                        self._device_id = device_id
                        break

                    vi.deinit_device(device_id)
                # end of for loop

            if self._device_id is None:
                print(
                    ': Failed to init the capture device %d' %
                    (self.device_id)
                )
        finally:
            self.lock.release()

    def _select_device_by_name_func(self, source):
        print(': Select device by name "%s"' % (source))

        try:
            index = self.enumerate_sources().index(source)
        except ValueError:
            print(': Input "%s" not found' % (source))
            return False

        print(': "%s" -> %d' % (source, index))
        self._select_device_by_index_func(index)


    def enumerate_sources(self):
        return self._videoinput_wrapper.get_device_list()

    def is_active(self):
        return (self._device_id is not None)

    def read_raw(self):
        if self._device_id is None:
            return None

        frame = self._videoinput_wrapper.get_pixels(
            self._device_id,
            parameters=(
                self._videoinput_wrapper.VI_BGR +
                self._videoinput_wrapper.VI_VERTICAL_FLIP
            )
        )

        return frame

    def _read_frame_func(self):
        frame = self.read_raw()
        return frame

    def get_tick(self):
        return int(time.time() * 1000 - self._base_tick)

    def _skip_frame_realtime(self):
        current_tick = self.get_tick()
        last_tick = self.last_tick
        next_tick = current_tick

        if self.fps_requested is not None:
            next_tick2 = int(last_tick + (1000 / self.fps_requested * 2))
            if current_tick < next_tick2:
                next_tick = int(last_tick + (1000 / self.fps_requested))

        while current_tick < next_tick:
            time.sleep(0.05)
            current_tick = self.get_tick()

        return next_tick

    def read_frame(self):
        try:
            self.lock.acquire()
            if not self.is_active():
                return None

            next_tick = None
            img = self._read_frame_func()

            # Skip some frames for performance.
            try:
                if self.cap_recorded_video:
                    print("a")
                    #_skip_frame_recorded()
                else:
                    next_tick = self._skip_frame_realtime()
            except EOFError:
                pass  # EOFError should be captured by the next cycle.

        finally:
            self.lock.release()

        if img is None:
            return None

        if self.cap_optimal_input_resolution:
            res720p = (img.shape[0] == 720) and (img.shape[1] == 1280)
            res1080p = (img.shape[0] == 1080) and (img.shape[1] == 1920)

            if not (res720p or res1080p):
                print(
                    'Invalid input resolution (%dx%d). Acceptable res: 1280x720 or 1920x1080' %
                    (img.shape[1], img.shape[0])
                )
                return None

        if next_tick is not None:
            self.last_tick = next_tick

        # need stratch?
        stratch = (
            img.shape[0] != self.output_geometry[0] or
            img.shape[1] != self.output_geometry[1])

        if stratch:
            img = cv2.resize(
                img,
                (self.output_geometry[1], self.output_geometry[0]),
                # fixme
            )

        #img = _offset_filter.execute(img)
        return img


        

if __name__ == '__main__':
    obj = VideoCapture()
    obj.reset()
    obj.reset_tick()
    #_offset_filter = OffsetFilter()
    obj.set_frame_rate()
    #_initialize_driver_func()
    #_select_device_by_index_func(0)

    obj.select_source(name=obj.DEV_AMAREC)
    #obj.set_read_video()
    k = 0
    while k != 27:
        frame = obj.read_frame()
        if frame is not None:
            cv2.imshow("fl", frame)
        k = cv2.waitKey(1)

        if k == ord('s'):
            import time
            cv2.imwrite('screenshot_%d.png' % int(time.time()), frame)
from __future__ import division
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.app import App  # for the main app
from kivy.clock import Clock  # clock to schedule a method
import ant
from jnius import autoclass
# from android.runnable import run_on_ui_thread
PythonActivity = autoclass('org.kivy.android.PythonActivity')
activity = PythonActivity.mActivity


kv = '''
BoxLayout:
    orientation: 'vertical'

    Label:
        text: app.numeric_output

    Label:
        text: app.info_msg
'''


class SensorApp(App):
    numeric_output = StringProperty()
    info_msg = StringProperty()

    def build(self):
        self.params()
        try:
            Clock.schedule_interval(self.update, self.update_interval)
        except:
            self.numeric_output = "Clock error"  # error
        self.s_calc = SensorCalc(self)
        self.root = Builder.load_string(kv)
        return self.root

    def params(self):
        self.sensor_log_frequency = 100  # calls per second
        self.update_interval = 1.0/self.sensor_log_frequency
        self.display_sum = 5  # cycles per display
        self.time = 0.0

    def update(self, dt):
        display = self.s_calc.display()
        if display:
            self.numeric_output = display  # add the correct text

    def on_pause(self):
        try:
            self.s_calc.sr_instance.disable()
        except AttributeError:
            pass
        return True

    def on_resume(self):
        try:
            self.s_calc.sr_instance.enable()
        except AttributeError:
            pass
        pass

    def on_stop(self):
        try:
            self.s_calc.sr_instance.disable()
        except AttributeError:
            pass
        return False


class SensorCalc(object):

    def __init__(self, parent):
        self.parent = parent
        parent.info_msg = "Initialising"
        self.time = TimeObj()
        # self.init_sensor_list()
        self.pre_display_count = 0
        self.last_time_stamp = 0
        self.spd_freq = 0
        self.sr_instance = ant.AntHandler(activity)
        self.sr_instance.initialise()
        # self.init_ant_sensors()

    # def init_ant_sensors(self):
    #     self.sampler_reduced = autoclass('org/homebrew/antpluslistener/BikeSpeedDistanceSampler')
    #     self.init_sr_instance()

    # @run_on_ui_thread
    # def init_sr_instance(self):
    #     self.sr_instance = self.sampler_reduced(activity, activity)
    #     self.sr_instance.resetPcc()
    #     # print("<--------------------------- RESET PCC --------------------------------->")

    # def listener(self):
    #     self.ant_devicename = self.sr_instance.resultsMap.get("spdDeviceName")
    #     self.ant_devicestate = self.sr_instance.resultsMap.get("spdDeviceState")
    #     self.ant_resultcode = self.sr_instance.resultsMap.get("spdResultCode")
    #     try:
    #         self.ant_est_time_stamp = self.sr_instance.spdEstTimestamp
    #         self.ant_time_stamp_last_event = self.sr_instance.spdTimestampOfLastEvent
    #         self.ant_cumulative_revolutions = self.sr_instance.spdCumulativeRevolutions
    #     except AttributeError as e:
    #         print(e)
    #         self.ant_est_time_stamp = 0
    #         self.ant_time_stamp_last_event = 0
    #         self.ant_cumulative_revolutions = 0

    def ant_listener(self):
        self.ant_devicename = self.sr_instance.get_spd_code("spdDeviceName")
        self.ant_devicestate = self.sr_instance.get_spd_code("spdDeviceState")
        self.ant_resultcode = self.sr_instance.get_spd_code("spdResultCode")
        try:
            self.ant_est_time_stamp = float(self.sr_instance.spd_time_stamp)
            self.ant_time_stamp_last_event = float(self.sr_instance.spd_time_stamp_prev)
            self.ant_cumulative_revolutions = float(self.sr_instance.spd_revolutions)
        except (AttributeError, ValueError) as e:
            print(e)
            self.ant_est_time_stamp = 0
            self.ant_time_stamp_last_event = 0
            self.ant_cumulative_revolutions = 0

    def display(self):
        if self.calc():
            if self.pre_display_count < self.parent.display_sum:
                return
            else:
                self.pre_display_count = 0
            self.txt = ''
            self.txt += "\nTime: %.3f, %.3f, %.3f" % (self.time.total, self.time.interval,
                                                      self.time.current)
            try:
                self.txt += ("\nDevice Status: %s, \n%s, \n%s" % (self.ant_devicename,
                             self.ant_devicestate, self.ant_resultcode))
                self.txt += ("\nValues: %i, %.3f, %i" % (self.ant_est_time_stamp,
                             self.ant_time_stamp_last_event, self.ant_cumulative_revolutions))
                self.txt += ("\nUpdate Interval: %.3f" % (self.spd_freq))
            except AttributeError:
                self.txt += "\nANT+ Sensor not available"
        else:
            self.txt = "Cannot read sensors!"  # error
        return self.txt

    def calc(self):
        try:
            self.time.calc_interval()
            # self.listener()
        except TypeError:
            return False
        self.ant_listener()
        if self.ant_time_stamp_last_event != self.last_time_stamp:
            self.spd_freq = (self.ant_time_stamp_last_event - self.last_time_stamp)
            self.last_time_stamp = self.ant_time_stamp_last_event
        self.pre_display_count += 1
        return True


class TimeObj(object):

    def __init__(self):
        self.last = Clock.get_time()
        self.start = self.last
        self.calc_interval()

    def calc_interval(self):
        self.current = Clock.get_time()
        self.interval = self.current - self.last
        self.total = self.current - self.start
        self.last = self.current
        self.time = (self.total,)


def run():
    app = SensorApp()
    app.run()  # start our app

if __name__ == '__main__':
    run()

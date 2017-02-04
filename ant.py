from jnius import autoclass
from android.runnable import run_on_ui_thread


class AntHandler(object):

    def __init__(self, activity):
        self.activity = activity
        self.enabled = False
        self.sr_instance = None
        self.code_dict = {}
        self.value_list = []
        self.initialised = False

    def initialise(self):
        self.initialised = True
        self.sampler_reduced = autoclass('org/homebrew/antpluslistener/BikeSpeedDistanceSampler')
        self.init_sr_instance(self.activity)

    @run_on_ui_thread
    def init_sr_instance(self, activity):
        self.sr_instance = self.sampler_reduced(activity, activity)
        self.sr_instance.closePcc()
        self.sr_instance.resetPcc()
        self.enabled = True

    def enable(self):
        if not self.initialised:
            return
        if not self.sr_instance:
            self.init_sr_instance(self.activity)
        self.enabled = True

    def disable(self):
        self.sr_instance.closePcc()
        self.enabled = False

    # def check(self):
    #     if self.enabled:
    #         if self.sr_instance:
    #             return True,
    #     return False, 'Not Enabled'

    @property
    def spd_time_stamp(self):
        try:
            return self.sr_instance.spdEstTimestamp
        except AttributeError as e:
            return '##  error:' + str(e)

    @property
    def spd_time_stamp_prev(self):
        try:
            return self.sr_instance.spdTimestampOfLastEvent
        except AttributeError as e:
            return '##  error:' + str(e)

    @property
    def spd_revolutions(self):
        try:
            return self.sr_instance.spdCumulativeRevolutions
        except AttributeError as e:
            return '##  error:' + str(e)

    @property
    def cad_time_stamp(self):
        try:
            return self.sr_instance.cadEstTimestamp
        except AttributeError as e:
            return '##  error:' + str(e)

    @property
    def cad_time_stamp_prev(self):
        try:
            return self.sr_instance.cadTimestampOfLastEvent
        except AttributeError as e:
            return '##  error:' + str(e)

    @property
    def cad_revolutions(self):
        try:
            return self.sr_instance.cadCumulativeRevolutions
        except AttributeError as e:
            return '##  error:' + str(e)

    @property
    def spd_codes_dict(self):
        if self.enabled:
            try:
                key_set = self.sr_instance.resultsMap.keySet()
                for key in key_set.toArray():
                        self.code_dict[key] = self.sr_instance.resultsMap.get(key)
                return self.code_dict
            except TypeError as e:
                # print('TypeError #', e.args)
                self.code_dict['spdDeviceState'] = 'Type Error' + str(e.args)
            except AttributeError as e:
                # print('AttributeError #', e.args)
                self.code_dict['spdDeviceState'] = 'Attrib Error' + str(e)
        return {'spdDeviceState': 'Not enabled', 'cadDeviceState': 'Not enabled'}

    @property
    def spd_cad_values(self):
        if self.enabled:
            self.spd_codes_dict
            len_code_dict = len(self.code_dict)
            if len(self.value_list) < len_code_dict:
                self.value_list = [None] * len_code_dict
            for i, value in enumerate(self.code_dict.values()):
                self.value_list[i] = value
            return self.value_list
        return 'Not enabled'

    def get_spd_code(self, code):
        d = self.spd_codes_dict
        if code in d:
            return d[code]
        return None

# Direct variables:
#     spdEstTimestamp
#     spdEventFlags
#     spdTimestampOfLastEvent
#     spdCumulativeRevolutions
#     cadEstTimestamp
#     cadEventFlags
#     cadTimestampOfLastEvent
#     cadCumulativeRevolutions

# Mapped variables:
#     spdDeviceName
#     spdDeviceState
#     spdResultCode

#     spdEstTimestamp
#     spdEventFlags
#     spdTimestampOfLastEvent
#     spdCumulativeRevolutions

#     cadResultCode
#     cadEstTimestamp

#     cadEventFlags
#     cadTimestampOfLastEvent
#     cadCumulativeRevolutions
#     cadEstTimestamp

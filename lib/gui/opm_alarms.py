""" Python file that covers tabs under the "OPM ALARMS" Menu.
"""

import time
import logging
import logging.config
logging.config.fileConfig('logging.ini')
#LOG = logging.getLogger('polatis')
LOG = logging.getLogger(__name__)
#LOG.info("Testing Opm Alarms ..\n")

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from configAttr import defaultAttr

class OpmAlarms:
    """ Class that will Configure OPM Alarm Page.
    

    oxcDict = {
        'opm_alarms_page':'//a[text()="Alarms"]',
        'opm_alarms_config_page':'[id=canvas]',
        'opm_alarm_visibility' : '//div[@id="canvas"]/table',
        'Popup_box' : '[id=editor]',
        'cancel_opm_alarms' : '[id=modalCancelbutton]',
        'availability':'//tr[@id = "0"]//td[1]',
        'configure_opm_alarms' : '[id=modalConfigurebutton]'
        }
    alarmDict = {
        'los_alarm_mode' : '[id=mode]',
        'los_alarm_edge' : '[id=edge]',
        'los_low_threshold': '[id=lowthresh]',
        'los_high_threshold': '[id=highthresh]',
        'degraded_alarm_mode': '[id=degrmode]',
        'degraded_threshold' : '[id=degrthresh]',
        'alarm_hysteresis' : '[id=hysteresis]',
        'recovery_delay' : '[id=alarmcleardelay]'
        }


    portDict = {
        '1':'0', '2':'1','3':'2','4':'3','5':'4','6':'5','7':'6','8':'7',
        '9':'8','10':'9','11':'10','12':'11','13':'12','14':'13','15':'14',
        '16':'15','17':'24','18':'25','19':'26','20':'27','21':'28','22':'29',
        '23':'30','24':'31','25':'16','26':'17','27':'18','28':'19','29':'20',
        '30':'21','31':'22','32':'23'
        }

    """
#    def __init__(self):

#        """
#        Initialize the default attr
#        """

    opmAlarmsAttr = defaultAttr()

    def navigate_to_opm_alarms_page(self, sel):
        """
        Navigates to the OPM ALARMS page.
        """
        # click on 'System Config' Page.
        WebDriverWait(sel, 60).until(EC.visibility_of_element_located((By.XPATH, getattr(self.opmAlarmsAttr, 'opm_alarms_page'))))
        #print "111"
        sel.find_element_by_xpath(getattr(self.opmAlarmsAttr, 'opm_alarms_page')).click()
        try:
            WebDriverWait(sel, 60).until(EC.visibility_of_element_located((By.XPATH,'//td[contains(text(),"Off")]')))
        except:
            try:
                alert = sel.switch_to_alert()
                alertText = alert.text
                alert.accept()
                sel.switch_to_default_content()
                print "This error message obtained while reloading opm Alarm Page:",alertText
                sel.find_element_by_xpath(getattr(self.opmAlarmsAttr, 'opm_alarms_page')).click()
            except:
                sel.find_element_by_xpath(getattr(self.opmAlarmsAttr, 'opm_alarms_page')).click()
                WebDriverWait(sel,30).until(EC.visibility_of_element_located((By.XPATH,'//td[contains(text(),"Off")]')))
                print "Opm Alarms page loading takes long time"
        #print "222"
        time.sleep(2)

    def fetchAlarmConfig(self,node,**kwargs):
        """
        fetch opm alarm config parameters such as Power, Alarm Mode, Alarm Edge, Threshold.
        """
        LOG.info("Testing fetchAlarmConfig function...\n")
        LOG.info("Navigate to the OPM Alarm Config Page\n")
        sel = node.gui_login()
        time.sleep(5)
        self.navigate_to_opm_alarms_page(sel)
        time.sleep(2)
        port = self.portDict['%s' % kwargs['Port']]
        value = '//tr[@id = "%s"]//td[1]' % port
        element = sel.find_element_by_xpath(value)
        ActionChains(sel).double_click(element).perform()
        opmAlarmDict = {}
        for key, value in self.alarmDict.iteritems():
            element = sel.find_element_by_css_selector(self.alarmDict[key])
            value = element.get_attribute('value')
            opmAlarmDict[key] = value
        time.sleep(2)
        sel.find_element_by_css_selector(getattr(self.opmAlarmsAttr, 'cancel_opm_alarms')).click()
        fetched_alarm_config = {}
        fetched_alarm_config['Alarms'] = opmAlarmDict
        #print "opmAlarmDict:", opmAlarmDict
        #print "fetched_alarm_config:", fetched_alarm_config
        return opmAlarmDict

    def fetchAlarmState(self,node,**kwargs):
        """
        fetches Alarm State, Alarm Condition
        """
        LOG.info("Testing fetchAlarmState function...\n")
        LOG.info("Navigate to the OPM Alarm Config Page\n")
        sel = node.gui_login()
        time.sleep(5)
        self.navigate_to_opm_alarms_page(sel)
        time.sleep(2)
        alarmConditionState = {}
        port = self.portDict['%s' % kwargs['Port']]
        value = '//tr[@id = "%s"]//td[1]' % port
        element = sel.find_element_by_xpath(value)
        alarmCondition = sel.find_element_by_xpath('//tr[@id = "%s"]' % port).get_attribute('class')
        degradedAlarmState = element.find_element_by_xpath('following-sibling::td[6]').text
        losAlarmState = element.find_element_by_xpath('following-sibling::td[2]').text
        powerLevel = element.find_element_by_xpath('following-sibling::td[1]').text
        alarmConditionState['AlarmCondition'] = str(alarmCondition)
        alarmConditionState['LosAlarmState'] = str(losAlarmState)
        alarmConditionState['DegradedAlarmState'] = str(degradedAlarmState)
        alarmConditionState['PowerLevel'] = float(powerLevel)

        return alarmConditionState

    def configureAlarms(self,node,*args,**kwargs):
        """ 
        Configure Alarms
        """
        LOG.info("Testing configureAlarms function...\n")
        LOG.info("Navigate to the Opm Alarms Page\n")
        sel = node.gui_login()
        time.sleep(5)
        self.navigate_to_opm_alarms_page(sel)
        time.sleep(5)
        if 'opm_alarms_config_page' in args:
            element = sel.find_element_by_css_selector(getattr(self.opmAlarmsAttr, 'opm_alarms_config_page')).is_displayed()
            return element
        port = self.portDict['%s' % kwargs['Port']]
        value = '//tr[@id = "%s"]//td[1]' % port
        element = sel.find_element_by_xpath(value)
        ActionChains(sel).double_click(element).perform()
        if 'popUp' in args:
            element = sel.find_element_by_css_selector(getattr(self.opmAlarmsAttr, 'Popup_box')).is_displayed()
            return element
        del kwargs['Port']
        for key, val in kwargs.iteritems():
            element = sel.find_element_by_css_selector(self.alarmDict[key])
            #print "element.tag_name : ", element.tag_name
            if element.tag_name != 'select':
                element.clear()
            element.send_keys(val)
        if 'Cancel' in args:
            sel.find_element_by_css_selector(getattr(self.opmAlarmsAttr, 'cancel_opm_alarms')).click()

        sel.find_element_by_css_selector(getattr(self.opmAlarmsAttr, 'configure_opm_alarms')).click()
        if 'recovery_delay' in kwargs.keys():
            port = self.portDict['%s' % kwargs['Port']]
            recoveryList = []
            for t in range(0, int(kwargs['recovery_delay'])):
                time.sleep(1)
                alarmCondition = sel.find_element_by_xpath('//tr[@id = "%s"]' % port).get_attribute('class')
                recoveryList.append(str(alarmCondition))
            if any(state in recoveryList for state in ('normal', 'warning')):
                recoveryDict = {'Result' : False , 'RecoveryList' : recoveryList}
                return recoveryDict
            else:
                recoveryDict = {'Result' : True , 'RecoveryList' : recoveryList}
                return recoveryDict

        time.sleep(6)
        if 'InvalidCase' in args:
            try:
                WebDriverWait(sel,30).until(EC.alert_is_present())
                alert = sel.switch_to_alert()
                alertText = alert.text
                alert.accept()
                time.sleep(2)
                sel.switch_to_default_content()
                return str(alertText)
            except Exception as err:
                print  "No Alert is Present",err
        time.sleep(2)

    def configure_global_opm_alarm_settings(self,node,*args,**kwargs):
        """
        Configure global opm alarm such as Recovery Delay and Hysteresis.
        """
        LOG.info("Testing configure_global_opm_alarm_settings function...\n")
        LOG.info("Navigate to the OPM Config Page")
        sel = node.gui_login()
        time.sleep(5)
        self.navigate_to_opm_config_page(sel)
        if 'alarmHysteresis' in kwargs.keys():
            element = sel.find_element_by_css_selector('[id="hysteresis"]')
            element.clear()
            element.send_keys(kwargs['alarmHysteresis'])
            sel.find_element_by_css_selector('[id="set_hysteresis"]').click()
        if 'recoveryDelay' in kwargs.keys():
            element = sel.find_element_by_css_selector('[id="alarmcleardelay"]')
            element.clear()
            element.send_keys(kwargs['recoveryDelay'])
            sel.find_element_by_css_selector('[id="set_alarmcleardelay"]').click()
        
        if 'InvalidCase' in args:
            try:
                alert = sel.switch_to_alert()
                alertText = alert.text
                alert.accept()
                sel.switch_to_default_content()
                return str(alertText)
            except Exception as err:
                return "No alert is Present:", err
        time.sleep(5)

    def triggerOpmAlarm(self,node,**kwargs):
        if 'normal' in kwargs['portState']:
            self.configureAlarms(node,Port =kwargs['Port'],los_alarm_mode = 'Single',los_low_threshold = '0.00',los_high_threshold = '0.0')
        elif 'warning' in kwargs['portState']:
            self.configureAlarms(node,Port =kwargs['Port'],los_alarm_mode = 'Single',los_low_threshold = '0.00',los_high_threshold = '0.0')
        elif 'alarmed' or 'Normal' in kwargs['portState']:
            self.configureAlarms(node,Port =kwargs['Port'],los_alarm_mode = 'Off',los_low_threshold = '-60.00',los_high_threshold = '25.0',degraded_alarm_mode ='off',degraded_threshold = '-60.00')

        else:
            print "Invalid Keyword argument passed, allowed arguments 'normal','warning','alarmed'"

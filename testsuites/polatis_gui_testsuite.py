""" Test Script """

import nose
import time
from gui.node import Node
from gui.event_log import EventLog
#from gui.opm_alarms import OpmAlarms
#from gui.opm_configuration import OPMConfig
from gui.connections import CrossConnects
from gui.port_status import PortStatus
from gui.system_status import StatusConfig
#from gui.opm_powerlevels import OpmPowerLevels
from gui.userConfig import UserConfig 
from gui.system_config import SystemConfig
import ConfigParser
Config = ConfigParser.ConfigParser()

Config.read('config.txt')


box_ip = Config.get("switch_info", "host")


class testLogin():


    @classmethod
    def setUpClass(cls):
        cls.box = Node(box_ip)


    """LOGIN"""

    def testLoginPage(self):

        try:
            sel = self.box.gui_login_page(login_page = 'yes')
        except Exception as err:
            print "Login Page Error:", err
            
        nose.tools.assert_true(sel,'Login Page Contents Not Loaded properly')
        
    def testValidLoginCredentials(self):

        try:
            sel = self.box.gui_login_page(main_page = 'yes')
        except Exception as err:
            print "Login Error:", err

        nose.tools.assert_true(sel,'Main Page Contents Not Loaded properly')

    def testInvalidUserName(self):
        usrname = 'Invalid'
        
        try:
            element = self.box.gui_login_page(UserName = usrname,Invalid_case = 'yes')
        except Exception as err:
            print "Login Page Error:", err

        #build 6.5.0.28
        nose.tools.assert_in("Authentication failed",element,'Login Error Message Mismatch Error')
        #build 6.1.2.9
        #nose.tools.assert_in("Invalid user or group.",element,'Login Error Message Mismatch Error')

    def testInvalidPassword(self):
        pswd = 'Invalid'
        
        try:
            element = self.box.gui_login_page(Password = pswd,Invalid_case = 'yes')
        except Exception as err:
            print "Login Error:", err

        #build 6.5.0.28
        nose.tools.assert_in("Authentication failed",element,'Login Error Message Mismatch Error')
        #build 6.1.2.9
        #nose.tools.assert_in("Authorisation failed",element,'Login Error Message Mismatch Error')
        #nose.tools.assert_in("Invalid user or group.",element,'Login Error Message Mismatch Error')

    def testInvalidCredentials(self):
        usrname = 'Invalid'
        pswd = 'Invalid'

        try:
            element = self.box.gui_login_page(UserName = usrname,Password = pswd,Invalid_case = 'yes')
        except Exception as err:
            print "Login Error:", err

        #build 6.5.0.28
        nose.tools.assert_in("Authentication failed",element,'Login Error Message Mismatch Error')
        #build 6.1.2.9
        #nose.tools.assert_in("Invalid user or group.",element,'Login Error Message Mismatch Error')

    def testEmptyUserName(self):
        usrname = ''

        try:
            element = self.box.gui_login_page(UserName = usrname,Invalid_case = 'yes')
        except Exception as err:
            print "Login Page Error:", err

        #build 6.5.0.28
        nose.tools.assert_in("No username supplied",element,'Login Error Message Mismatch Error')
        #build 6.1.2.9
        #nose.tools.assert_in("Invalid user or group.",element,'Login Error Message Mismatch Error')

    def testEmptyPassword(self):
        pswd = ''

        try:
            element = self.box.gui_login_page(Password = pswd,Invalid_case = 'yes')
        except Exception as err:
            print "Login Error:", err

        
        #build 6.5.0.28
        nose.tools.assert_in("Authentication failed",element,'Login Error Message Mismatch Error')
        #build 6.1.2.9
        #nose.tools.assert_in("Authorisation failed",element,'Login Error Message Mismatch Error')

    def testEmptyCredentials(self):
        usrname = ''
        pswd = ''

        try:
            element = self.box.gui_login_page(UserName = usrname,Password = pswd, Invalid_case = 'yes')
            print "element : ", element
            print '\n'
        except Exception as err:
            print "Login Error:", err

        #build 6.5.0.28
        nose.tools.assert_in("No username supplied",element,'Login Error Message Mismatch Error')
        #build 6.1.2.9
        #nose.tools.assert_in("Invalid user or group.",element,'Login Error Message Mismatch Error')

    def testSameUserMultipleSession(self):
        try:
            user1 = self.box.gui_login_page(main_page = 'yes')
        except Exception as err:
            print "Login Error:", err
        
        try:
            user2 = self.box.gui_login_page(main_page = 'yes')
        except Exception as err:
            print "Login Error:", err        

        nose.tools.assert_true(user1,'First user login error and contents are not found')
        nose.tools.assert_true(user2,'Second User login error and contents are not found')
    
    def testDiffUserMultipleSession(self):
        usrname = 'admin'
        pswd = 'admin'
        
        try:
            user1 = self.box.gui_login_page(main_page = 'yes')
        except Exception as err:
            print "Login Error:", err
        
        try:
            user2 = self.box.gui_login_page(UserName = usrname,Password = pswd,main_page = 'yes')
        except Exception as err:
            print "Login Error:", err        

        nose.tools.assert_true(user1,'First user login error and contents are not found')
        nose.tools.assert_true(user2,'Second User login error and contents are not found')           


if 0:
    class testEventLog():
    
        ports = Config.get("switch_info", "Ports")
        ingress_ports_list = []
        egress_ports_list = []
        for ingress_ports in range(1, int(ports)+1):
            ingress_ports_list.append(ingress_ports)
        for egress_ports in range(int(ports)+1, int(ports+ports)+1):
            egress_ports_list.append(egress_ports)
    
    
        @classmethod
        def setUpClass(cls):
            cls.cr_event_log = EventLog()
            #cls.cr_opm_alarms = OpmAlarms()
            cls.box = Node(box_ip)
            
        """ EventLog """
        
        def testEventLogPage(self):
            try:
                element = self.cr_event_log.eventLogAction(self.box,'event_log_page')
            except Exception as err:
                print "Navigate to Event Log Page page error:", err
    
            nose.tools.assert_true(element,'Event Log Page Loading Error')
    
        def testSelectAllEvents(self):
            port_id = [self.ingress_ports_list[5],self.ingress_ports_list[7]]
    
            try:
                port_state = self.cr_opm_alarms.fetchAlarmState(self.box,Port = port_id[0])
            except Exception as err:
                print "Fetch Alarm State Error:", err
    
            try:
                self.cr_opm_alarms.triggerOpmAlarm(self.box,portState = port_state['AlarmCondition'],Port = port_id[0])
            except Exception as err:
                print "Trigger OPM alarm error:", err
    
            try:
                port_state1 = self.cr_opm_alarms.fetchAlarmState(self.box,Port = port_id[1])
            except Exception as err:
                print "Fetch Alarm State Error:", err
    
            try:
                self.cr_opm_alarms.triggerOpmAlarm(self.box,portState = port_state1['AlarmCondition'],Port = port_id[1])
            except Exception as err:
                print "Trigger OPM alarm error:", err
    
            try:
                eventDict = self.cr_event_log.eventLogAction(self.box,'SelectEvent','allEvent')
            except Exception as err:
                print "event Log Action Error:", err
    
            nose.tools.assert_true(eventDict['Checked'],'All the events are not selected when clicking on select All event button')
            nose.tools.assert_equal('Deselect All Events',eventDict['Text'],'Deselect All Events button is not visible')
    
        def testDeselectAllEvents(self):
            port_id = [8,6]
    
            try:
                port_state = self.cr_opm_alarms.fetchAlarmState(self.box,Port = port_id[0])
            except Exception as err:
                print "Fetch Alarm State Error:", err
    
            try:
                self.cr_opm_alarms.triggerOpmAlarm(self.box,portState = port_state['AlarmCondition'],Port = port_id[0])
            except Exception as err:
                print "Trigger OPM alarm error:", err
    
            try:
                port_state1 = self.cr_opm_alarms.fetchAlarmState(self.box,Port = port_id[1])
            except Exception as err:
                print "Fetch Alarm State Error:", err
    
            try:
                self.cr_opm_alarms.triggerOpmAlarm(self.box,portState = port_state1['AlarmCondition'],Port = port_id[1])
            except Exception as err:
                print "Trigger OPM alarm error:", err
    
            try:
                eventDict = self.cr_event_log.eventLogAction(self.box,'DeselectEvent')
            except Exception as err:
                print "event Log Action Error:", err
            
            nose.tools.assert_true(eventDict['Checked'],'Some event is selected even after clicking on deselect All event button')
            nose.tools.assert_equal('Select All Events',eventDict['Text'],'Select All Events button is not visible')
    
        def testDeleteAllSelectedEvents(self):
            port_id = [2,3]
    
            try:
                port_state = self.cr_opm_alarms.fetchAlarmState(self.box,Port = port_id[0])
            except Exception as err:
                print "Fetch Alarm State Error:", err
    
            try:
                self.cr_opm_alarms.triggerOpmAlarm(self.box,portState = port_state['AlarmCondition'],Port = port_id[0])
            except Exception as err:
                print "Trigger OPM alarm error:", err
    
            try:
                port_state1 = self.cr_opm_alarms.fetchAlarmState(self.box,Port = port_id[1])
            except Exception as err:
                print "Fetch Alarm State Error:", err
    
            try:
                self.cr_opm_alarms.triggerOpmAlarm(self.box,portState = port_state1['AlarmCondition'],Port = port_id[1])
            except Exception as err:
                print "Trigger OPM alarm error:", err
    
            try:
                self.cr_event_log.eventLogAction(self.box,'SelectEvent','allEvent','DeleteEvents')
            except Exception as err:
                print "event Log Action Error:", err
    
            try:
                text = self.cr_event_log.checkEvent(self.box,'deleteAll')
            except Exception as err:
                print "check event Error:", err
    
            try:
                self.cr_opm_alarms.triggerOpmAlarm(self.box,portState = port_state['AlarmCondition'],Port = port_id[0])
            except Exception as err:
                print "Trigger OPM alarm error:", err
    
            try:
                port_state1 = self.cr_opm_alarms.fetchAlarmState(self.box,Port = port_id[1])
            except Exception as err:
                print "Fetch Alarm State Error:", err
    
            nose.tools.assert_in('no events to display',text,'All the events are not deleted')
    
        def testDeleteIndividualEvent(self):
            port_id = [14,15]
    
            try:
                port_state = self.cr_opm_alarms.fetchAlarmState(self.box,Port = port_id[0])
            except Exception as err:
                print "Fetch Alarm State Error:", err
    
            try:
                self.cr_opm_alarms.triggerOpmAlarm(self.box,portState = port_state['AlarmCondition'],Port = port_id[0])
            except Exception as err:
                print "Trigger OPM alarm error:", err
    
            try:
                port_state1 = self.cr_opm_alarms.fetchAlarmState(self.box,Port = port_id[1])
            except Exception as err:
                print "Fetch Alarm State Error:", err
    
            try:
                self.cr_opm_alarms.triggerOpmAlarm(self.box,portState = port_state1['AlarmCondition'],Port = port_id[1])
            except Exception as err:
                print "Trigger OPM alarm error:", err
    
            try:
                eventDict = self.cr_event_log.eventLogAction(self.box,'SelectEvent','singleEvent','DeleteEvents')
            except Exception as err:
                print "event Log Action Error:", err
            
            try:
                text = self.cr_event_log.checkEvent(self.box,eventId = eventDict['eventId'])
            except Exception as err:
                print "check event Error:", err
    
            nose.tools.assert_in('Deletion of the event is successful',text,'Selected Individual event is not deleted')
    
        def testCancelDeleteSelectedEvent(self):
            port_id = [16]
    
            try:
                port_state = self.cr_opm_alarms.fetchAlarmState(self.box,Port = port_id[0])
            except Exception as err:
                print "Fetch Alarm State Error:", err
    
            try:
                self.cr_opm_alarms.triggerOpmAlarm(self.box,portState = port_state['AlarmCondition'],Port = port_id[0])
            except Exception as err:
                print "Trigger OPM alarm error:", err
    
            try:
                eventDict = self.cr_event_log.eventLogAction(self.box,'SelectEvent','singleEvent','DeleteEvents','Cancel')
            except Exception as err:
                print "event Log Action Error:", err
    
            try:
                text = self.cr_event_log.checkEvent(self.box,eventId = eventDict['eventId'])
            except Exception as err:
                print "check event Error:", err
    
            nose.tools.assert_in('%s this event has not been deleted' % str(eventDict['eventId']),text,'Event has been deleted after delete cancel operation')
    
        def testClearAllSelectedEvents(self):
            port_id = [5,9]
    
            try:
                port_state = self.cr_opm_alarms.fetchAlarmState(self.box,Port = port_id[0])
            except Exception as err:
                print "Fetch Alarm State Error:", err
    
            try:
                self.cr_opm_alarms.triggerOpmAlarm(self.box,portState = port_state['AlarmCondition'],Port = port_id[0])
            except Exception as err:
                print "Trigger OPM alarm error:", err
    
            try:
                port_state1 = self.cr_opm_alarms.fetchAlarmState(self.box,Port = port_id[1])
            except Exception as err:
                print "Fetch Alarm State Error:", err
    
            try:
                self.cr_opm_alarms.triggerOpmAlarm(self.box,portState = port_state1['AlarmCondition'],Port = port_id[1])
            except Exception as err:
                print "Trigger OPM alarm error:", err
    
            try:
                self.cr_event_log.eventLogAction(self.box,'SelectEvent','allEvent','ClearEvents')
            except Exception as err:
                print "event Log Action Error:", err
    
            try:
                eventDict = self.cr_event_log.fetchEventState(self.box)
            except Exception as err:
                print "Fetch Event State Error:", err
    
            nose.tools.assert_true(eventDict['Result'],'Events has not been cleared after ClearAllEvents Action')
    
        def testClearIndividualEvent(self):
            port_id = [7,13]
    
            try:
                port_state = self.cr_opm_alarms.fetchAlarmState(self.box,Port = port_id[0])
            except Exception as err:
                print "Fetch Alarm State Error:", err
    
            try:
                self.cr_opm_alarms.triggerOpmAlarm(self.box,portState = port_state['AlarmCondition'],Port = port_id[0])
            except Exception as err:
                print "Trigger OPM alarm error:", err
    
            try:
                port_state1 = self.cr_opm_alarms.fetchAlarmState(self.box,Port = port_id[1])
            except Exception as err:
                print "Fetch Alarm State Error:", err
    
            try:
                self.cr_opm_alarms.triggerOpmAlarm(self.box,portState = port_state1['AlarmCondition'],Port = port_id[1])
            except Exception as err:
                print "Trigger OPM alarm error:", err
    
            try:
                eventDict = self.cr_event_log.eventLogAction(self.box,'SelectEvent','singleEvent','ClearEvents')
            except Exception as err:
                print "event Log Action Error:", err
    
            try:
                state = self.cr_event_log.fetchEventState(self.box,eventId = eventDict['eventId'])
            except Exception as err:
                print "Fetch Event State Error:", err
    
            nose.tools.assert_equal('normal',state,'Event has not been cleared after Clear Individual Event Action')
    
        def testDeleteClearedEvents(self):
            port_id = [18,17]
    
            try:
                port_state = self.cr_opm_alarms.fetchAlarmState(self.box,Port = port_id[0])
            except Exception as err:
                print "Fetch Alarm State Error:", err
    
            try:
                self.cr_opm_alarms.triggerOpmAlarm(self.box,portState = port_state['AlarmCondition'],Port = port_id[0])
            except Exception as err:
                print "Trigger OPM alarm error:", err
    
            try:
                port_state1 = self.cr_opm_alarms.fetchAlarmState(self.box,Port = port_id[1])
            except Exception as err:
                print "Fetch Alarm State Error:", err
    
            try:
                self.cr_opm_alarms.triggerOpmAlarm(self.box,portState = port_state1['AlarmCondition'],Port = port_id[1])
            except Exception as err:
                print "Trigger OPM alarm error:", err
    
            try:
                self.cr_event_log.eventLogAction(self.box,'SelectEvent','allEvent','ClearEvents')
            except Exception as err:
                print "event Log Action Error:", err
    
            try:
                eventDict = self.cr_event_log.fetchEventState(self.box)
            except Exception as err:
                print "Fetch Event State Error:", err
           
            try:
                self.cr_event_log.eventLogAction(self.box,'SelectEvent','allEvent','DeleteEvents')
            except Exception as err:
                print "event Log Action Error:", err
    
            try:
                text = self.cr_event_log.checkEvent(self.box,'deleteAll')
            except Exception as err:
                print "check event Error:", err
    
            nose.tools.assert_true(eventDict['Result'],'Events has not been cleared after ClearAllEvents Action') 
            nose.tools.assert_in('no events to display',text,'All the events are not deleted')        
        

if 0:        
    class testOpmAlarms():
    
        ports = Config.get("switch_info", "Ports")
        ingress_ports_list = []
        egress_ports_list = []
        for ingress_ports in range(1, int(ports)+1):
            ingress_ports_list.append(ingress_ports)
        for egress_ports in range(int(ports)+1, int(ports+ports)+1):
            egress_ports_list.append(egress_ports)
    
    
        @classmethod
        def setUpClass(cls):
            cls.box = Node(box_ip)
            cls.cr_opm_alarms = OpmAlarms()
    
        """OPM ALARM"""
    
        def testOpmAlarmConfigPage(self):
            try:
                element = self.cr_opm_alarms.configureAlarms(self.box,'opm_alarms_config_page')
                print "element : ", element
            except Exception as err:
                print "Navigate to Opm Alarms page error:", err
    
            nose.tools.assert_true(element,'OPM Configuration Page Loading Error')
    
        def testDoubleClickAlarmConfiguration(self):
            port_id = 5
            try:
                element = self.cr_opm_alarms.configureAlarms(self.box,'popUp',Port = port_id)
            except Exception as err:
                print "Navigate to opm alarms page or popup box error:", err
    
            nose.tools.assert_true(element,'OPM alarms page popup box error')
    
        def testLosAlarmSingle(self):
            port_id = 5
            LosAlarmMode = 'Single'
            LosAlarmEdge = 'High'
            LosLowThreshold = '-50.00'
            LosHighThreshold = '0.00'
            
            try:
                self.cr_opm_alarms.triggerOpmAlarm(self.box,Port = port_id,portState = 'Normal')
            except Exception as err:
                print "Configure Alarm Error:", err
    
            try:
                self.cr_opm_alarms.configureAlarms(self.box,Port = port_id,los_alarm_mode = LosAlarmMode,los_alarm_edge = LosAlarmEdge,los_low_threshold = LosLowThreshold,los_high_threshold = LosHighThreshold)
            except Exception as err:
                print "Configure Alarm Error:", err
    
            try:
                alarmConfig = self.cr_opm_alarms.fetchAlarmConfig(self.box,Port = port_id)
                print "alarmDcit:", alarmConfig
            except Exception as err:
                print "Fetch Alarm Configuration Error:", err
    
            nose.tools.assert_equal(str(alarmConfig['los_alarm_mode']),LosAlarmMode,'Los Alarm Mode value not set')
            nose.tools.assert_equal(str(alarmConfig['los_alarm_edge']),LosAlarmEdge,'Los Alarm Edge value not set')
            nose.tools.assert_equal(str(alarmConfig['los_low_threshold']),LosLowThreshold,'Los Low Threshold Value not set')
            nose.tools.assert_equal(str(alarmConfig['los_high_threshold']),LosHighThreshold,'Los High Threshold Value not set')
                
        def testCancelAlarmConfig(self):
            port_id = 8
            LosAlarmMode = 'Single'
            LosAlarmEdge = 'High'
            LosLowThreshold = '-50.00'
            LosHighThreshold = '10.00'
            
            try:
                self.cr_opm_alarms.triggerOpmAlarm(self.box,Port = port_id,portState = 'Normal')
            except Exception as err:
                print "Configure Alarm Error:", err
                
            try:
                alarmConfig1 = self.cr_opm_alarms.fetchAlarmConfig(self.box,Port = port_id)
            except Exception as err:
                print "Fetch Alarm Configuration Error:", err
    
            try:
                self.cr_opm_alarms.configureAlarms(self.box,'Cancel',Port = port_id,los_alarm_mode = LosAlarmMode,los_alarm_edge = LosAlarmEdge,los_low_threshold = LosLowThreshold,los_high_threshold = LosHighThreshold)
            except Exception as err:
                print "Configure Alarm Error:", err
    
            try:
                alarmConfig2 = self.cr_opm_alarms.fetchAlarmConfig(self.box,Port = port_id)
            except Exception as err:
                print "Fetch Alarm Configuration Error:", err
    
            nose.tools.assert_dict_equal(alarmConfig1,alarmConfig2,'Values are not same after the Cancel Operation')
    
        def testLosAlarmContinuous(self):
            port_id = 18
            LosAlarmMode = 'Cont'
            LosAlarmEdge = 'Both'
            LosLowThreshold = '-50.00'
            LosHighThreshold = '10.00'
            
            try:
                self.cr_opm_alarms.triggerOpmAlarm(self.box,Port = port_id,portState = 'Normal')
            except Exception as err:
                print "Configure Alarm Error:", err
    
            try:
                self.cr_opm_alarms.configureAlarms(self.box,Port = port_id,los_alarm_mode = LosAlarmMode,los_alarm_edge = LosAlarmEdge,los_low_threshold = LosLowThreshold,los_high_threshold = LosHighThreshold)
            except Exception as err:
                print "Configure Alarm Error:", err
    
            try:
                alarmConfig = self.cr_opm_alarms.fetchAlarmConfig(self.box,Port = port_id)
            except Exception as err:
                print "Fetch Alarm Configuration Error:", err
    
            #print 'alarmDictMode:', alarmConfig['los_alarm_mode']
            #print 'LosAlarmMode:', LosAlarmMode
            #print str(alarmConfig['los_alarm_mode'])
            #print 'alarmModeType:', type(alarmConfig['los_alarm_mode'])
            #print 'LosAlarmModeType:', type(LosAlarmMode)
            
            nose.tools.assert_equal(str(alarmConfig['los_alarm_mode']),LosAlarmMode,'Los Alarm Mode value not set')
            nose.tools.assert_equal(str(alarmConfig['los_alarm_edge']),LosAlarmEdge,'Los Alarm Edge value not set')
            nose.tools.assert_equal(str(alarmConfig['los_low_threshold']),LosLowThreshold,'Los Low Threshold Value not set')
            nose.tools.assert_equal(str(alarmConfig['los_high_threshold']),LosHighThreshold,'Los High Threshold Value not set')
    
        def testLosAlarmOff(self):
            port_id = 17
            LosAlarmMode = 'Off'
            LosAlarmEdge = 'Low'
            LosLowThreshold = '-60.00'
            LosHighThreshold = '25.00'
            
            try:
                self.cr_opm_alarms.configureAlarms(self.box,Port = port_id,los_alarm_mode = 'single',los_alarm_edge = 'high',los_low_threshold = '-45.00',los_high_threshold = '15.00',degraded_alarm_mode ='off',degraded_threshold = '0')
            except Exception as err:
                print "Configure Alarm Error:", err
    
            try:
                self.cr_opm_alarms.configureAlarms(self.box,Port = port_id,los_alarm_mode = LosAlarmMode,los_alarm_edge = LosAlarmEdge,los_low_threshold = LosLowThreshold,los_high_threshold = LosHighThreshold)
            except Exception as err:
                print "Configure Alarm Error:", err
    
            try:
                alarmConfig = self.cr_opm_alarms.fetchAlarmConfig(self.box,Port = port_id)
            except Exception as err:
                print "Fetch Alarm Configuration Error:", err
    
            nose.tools.assert_equal(str(alarmConfig['los_alarm_mode']),LosAlarmMode,'Los Alarm Mode value not set')
            nose.tools.assert_equal(str(alarmConfig['los_alarm_edge']),LosAlarmEdge,'Los Alarm Edge value not set')
            nose.tools.assert_equal(str(alarmConfig['los_low_threshold']),LosLowThreshold,'Los Low Threshold Value not set')
            nose.tools.assert_equal(str(alarmConfig['los_high_threshold']),LosHighThreshold,'Los High Threshold Value not set')
    
        def testInvalidLowThresholdLosAlarmValues(self):
            port_id = 26
            LosLowThreshold = '-75.00'
            
            try:
                alertMessage = self.cr_opm_alarms.configureAlarms(self.box,'InvalidCase',Port = port_id,los_low_threshold = LosLowThreshold)
            except Exception as err:
                print "Configure Alarm Error:", err
    
            #nose.tools.assert_in("Enter valid range between -60 and 25",alertMessage,'Wrong Error Message For Low threshold Los Alarm value')
            #build 6.1.2.9 
            nose.tools.assert_in("Invalid parameter",alertMessage,'Wrong Error Message For Invalid Threshold Degraded Alarm value')
    
        def testInvalidHighThresholdLosAlarmValues(self):
            port_id = 25
            LosHighThreshold = '100.00'
    
            try:
                alertMessage = self.cr_opm_alarms.configureAlarms(self.box,'InvalidCase',Port = port_id,los_high_threshold = LosHighThreshold)
            except Exception as err:
                print "Configure Alarm Error:", err
            
            #nose.tools.assert_in("Enter valid range between -60 and 25",alertMessage,'Wrong Error Message For High threshold Los Alarm value')
            #build 6.1.2.9 
            nose.tools.assert_in("Invalid parameter",alertMessage,'Wrong Error Message For Invalid Threshold Degraded Alarm value')
    
        def testInvalidInverseLosAlarmValues(self):
            port_id = 26
            LosLowThreshold = '25.00'
            LosHighThreshold = '-60.00'
    
            try:
                alertMessage = self.cr_opm_alarms.configureAlarms(self.box,'InvalidCase',Port = port_id,los_low_threshold = LosLowThreshold,los_high_threshold = LosHighThreshold)
            except Exception as err:
                print "Configure Alarm Error:", err
    
            nose.tools.assert_in("Higher threshold should be greater than lower threshold",alertMessage['alert'],'Wrong Error Message For Inverse threshold Los Alarm values')
            
        def testTriggerLosAlarm(self):
            port_id = 7
            LosAlarmMode = 'Single'
            LosAlarmEdge = 'Low'
            LosLowThreshold = '-20.00'
            LosHighThreshold = '10.00'
            
            try:
                self.cr_opm_alarms.triggerOpmAlarm(self.box,Port = port_id,portState = 'Normal')
            except Exception as err:
                print "Configure Alarm Error:", err
    
            try:
                triggerState1 = self.cr_opm_alarms.fetchAlarmState(self.box,Port = port_id)
            except Exception as err:
                print "Fetch Alarm State Error:", err
                
            try:
                self.cr_opm_alarms.configureAlarms(self.box,Port = port_id,los_alarm_mode = LosAlarmMode,los_alarm_edge = LosAlarmEdge,los_low_threshold = LosLowThreshold,los_high_threshold = LosHighThreshold)
            except Exception as err:
                print "Configure Alarm Error:", err
    
            try:
                triggerState2 = self.cr_opm_alarms.fetchAlarmState(self.box,Port = port_id)
            except Exception as err:
                print "Fetch Alarm State Error:", err
    
            print "triggerState1:", triggerState1
            print "triggerState2:", triggerState2
            nose.tools.assert_equal(triggerState1['AlarmCondition'],'normal','Alarm has been triggred for the port')
            nose.tools.assert_equal(triggerState1['LosAlarmState'],' Off ','Los Alarm Mode is not been set to Off') 
            nose.tools.assert_equal(triggerState2['AlarmCondition'],'alarmed','Alarm has not been triggred and its in normal state')
            nose.tools.assert_equal(triggerState2['LosAlarmState'],' Single, Triggered ','Los Alarm Mode is not been set to Single, Triggered')
        
        def testClearLosAlarm(self):
            port_id = 4
            LosAlarmMode = 'Off'
            LosAlarmEdge = 'Low'
            LosLowThreshold = '-50.00'
            LosHighThreshold = '25.00'
            
            try:
                self.cr_opm_alarms.configureAlarms(self.box,Port = port_id,los_alarm_mode = 'Single',los_alarm_edge = 'Low',los_low_threshold = '-10.0',los_high_threshold = '15.0',degraded_alarm_mode ='off',degraded_threshold = '0')
            except Exception as err:
                print "Configure Alarm Error:", err
                
            try:
                triggerState1 = self.cr_opm_alarms.fetchAlarmState(self.box,Port = port_id)
            except Exception as err:
                print "Fetch Alarm State Error:", err
    
            try:
                self.cr_opm_alarms.configureAlarms(self.box,Port = port_id,los_alarm_mode = LosAlarmMode,los_alarm_edge = LosAlarmEdge,los_low_threshold = LosLowThreshold,los_high_threshold = LosHighThreshold)
            except Exception as err:
                print "Configure Alarm Error:", err
                
            try:
                triggerState2 = self.cr_opm_alarms.fetchAlarmState(self.box,Port = port_id)
            except Exception as err:
                print "Fetch Alarm State Error:", err
    
            print "triggerstate1",triggerState1
            print "triggerstate2", triggerState2
    
            nose.tools.assert_equal(triggerState1['AlarmCondition'],'alarmed','Alarm has not been triggred and its in normal state')
            nose.tools.assert_equal(triggerState1['LosAlarmState'],' Single, Triggered ','Los Alarm Mode is not been set to Single, Triggered')
            nose.tools.assert_equal(triggerState2['AlarmCondition'],'normal','Alarm has been triggred for the port')
            nose.tools.assert_equal(triggerState2['LosAlarmState'],' Off ','Los Alarm Mode is not been set to Off')
    
        def testDegradeAlarmSingle(self):
            port_id = 8
            DegradedAlarmMode = 'Single'
            DegradedThreshold = '10.00'
            
            try:
                self.cr_opm_alarms.triggerOpmAlarm(self.box,Port = port_id,portState = 'Normal')
            except Exception as err:
                print "Configure Alarm Error:", err
    
            try:
                self.cr_opm_alarms.configureAlarms(self.box,Port = port_id,degraded_alarm_mode = DegradedAlarmMode,degraded_threshold = DegradedThreshold)
            except Exception as err:
                print "Configure Alarm Error:", err
    
            try:
                alarmConfig = self.cr_opm_alarms.fetchAlarmConfig(self.box,Port = port_id)
            except Exception as err:
                print "Fetch Alarm Configuration Error:", err
    
            nose.tools.assert_equal(str(alarmConfig['degraded_alarm_mode']),DegradedAlarmMode,'Degraded Alarm Mode value not set')
            nose.tools.assert_equal(str(alarmConfig['degraded_threshold']),DegradedThreshold,'Degraded Alarm Edge value not set')
    
        def testDegradeAlarmContinuous(self):
            port_id = 9
            DegradedAlarmMode = 'Cont'
            DegradedThreshold = '-20.00'
            
            try:
                self.cr_opm_alarms.triggerOpmAlarm(self.box,Port = port_id,portState = 'Normal')
            except Exception as err:
                print "Configure Alarm Error:", err
    
            try:
                self.cr_opm_alarms.configureAlarms(self.box,Port = port_id,degraded_alarm_mode = DegradedAlarmMode,degraded_threshold = DegradedThreshold)
            except Exception as err:
                print "Configure Alarm Error:", err        
                
            try:
                alarmConfig = self.cr_opm_alarms.fetchAlarmConfig(self.box,Port = port_id)
            except Exception as err:
                print "Fetch Alarm Configuration Error:", err
    
            nose.tools.assert_equal(alarmConfig['degraded_alarm_mode'],DegradedAlarmMode,'Degraded Alarm Mode value not set')
            nose.tools.assert_equal(alarmConfig['degraded_threshold'],DegradedThreshold,'Degraded Alarm Edge value not set')
    
        def testDegradeAlarmOff(self):
            
            port_id = 8
            DegradedAlarmMode = 'Off'
            DegradedThreshold = '-60.00'
            
            try:
                self.cr_opm_alarms.triggerOpmAlarm(self.box,Port = port_id,portState = 'Normal')
            except Exception as err:
                print "Configure Alarm Error:", err
    
            try:
                self.cr_opm_alarms.configureAlarms(self.box,Port = port_id,degraded_alarm_mode = DegradedAlarmMode,degraded_threshold = DegradedThreshold)
            except Exception as err:
                print "Configure Alarm Error:", err
    
            try:
                alarmConfig = self.cr_opm_alarms.fetchAlarmConfig(self.box,Port = port_id)
            except Exception as err:
                print "Fetch Alarm Configuration Error:", err
         
            nose.tools.assert_equal(alarmConfig['degraded_alarm_mode'],DegradedAlarmMode,'Degraded Alarm Mode value not set')
            nose.tools.assert_equal(alarmConfig['degraded_threshold'],DegradedThreshold,'Degraded Alarm Edge value not set')
    
        def testInvalidDegradedHighAlarmValues(self):
            port_id = 11
            DegradedThreshold = '30.00'
            
            try:
                alertMessage = self.cr_opm_alarms.configureAlarms(self.box,'InvalidCase',Port = port_id,degraded_threshold = DegradedThreshold)
            except Exception as err:
                print "Configure Alarm1 Error:", err        
    
            #nose.tools.assert_in("Enter valid range between -60 and 25",alertMessage,'Wrong Error Message For Invalid Threshold Degraded Alarm value')
            #build 6.1.2.9 
            nose.tools.assert_in("Invalid parameter",alertMessage,'Wrong Error Message For Invalid Threshold Degraded Alarm value')
    
        def testInvalidDegradedLowAlarmValues(self):
            port_id = 20
            DegradedThreshold = '-65.00'
            
            try:
                alertMessage = self.cr_opm_alarms.configureAlarms(self.box,'InvalidCase',Port = port_id,degraded_threshold = DegradedThreshold)
            except Exception as err:
                print "Configure Alarm Error:", err        
    
            #nose.tools.assert_in("Enter valid range between -60 and 25",alertMessage,'Wrong Error Message For Invalid Threshold Degraded Alarm value')
            #build 6.1.2.9 
            nose.tools.assert_in("Invalid parameter",alertMessage,'Wrong Error Message For Invalid Threshold Degraded Alarm value')
    
        def testTriggerDegradedAlarm(self):
            port_id = 13
            DegradedAlarmMode = 'Single'
            DegradedThreshold = '-25.00'
            
            try:
                self.cr_opm_alarms.triggerOpmAlarm(self.box,Port = port_id,portState = 'Normal')
            except Exception as err:
                print "Configure Alarm Error:", err
    
            try:
                triggerState1 = self.cr_opm_alarms.fetchAlarmState(self.box,Port = port_id)
            except Exception as err:
                print "Fetch Alarm State Error:", err
            
            try:
                self.cr_opm_alarms.configureAlarms(self.box,Port = port_id,degraded_alarm_mode = DegradedAlarmMode,degraded_threshold = DegradedThreshold)
            except Exception as err:
                print "Configure Alarm Error:", err
    
            try:
                triggerState2 = self.cr_opm_alarms.fetchAlarmState(self.box,Port = port_id)
            except Exception as err:
                print "Fetch Alarm State Error:", err
           
            nose.tools.assert_equal(str(triggerState1['AlarmCondition']),'normal','Alarm has been triggred for the port')
            nose.tools.assert_equal(str(triggerState1['DegradedAlarmState']),' Off ','Degraded Alarm Mode is not been set to Off') 
            nose.tools.assert_equal(str(triggerState2['AlarmCondition']),'warning','Alarm has not been triggred and its in normal state')
            nose.tools.assert_equal(str(triggerState2['DegradedAlarmState']),' Single, Triggered ','Degraded Alarm Mode is not been set to Single, Triggered')
    
        def testClearDegradedAlaram(self):
            port_id = 13
            DegradedAlarmMode = 'Single'
            DegradedThreshold = '-45.00'
    
            try:
                self.cr_opm_alarms.configureAlarms(self.box,Port = port_id,los_alarm_mode = 'Off',los_alarm_edge = 'Low',los_low_threshold = '-60.0',los_high_threshold = '25.0',degraded_alarm_mode ='single',degraded_threshold = '-10.00')
            except Exception as err:
                print "Configure Alarm Error:", err
    
            try:
                triggerState1 = self.cr_opm_alarms.fetchAlarmState(self.box,Port = port_id)
            except Exception as err:
                print "Fetch Alarm State Error:", err
    
            try:
                self.cr_opm_alarms.configureAlarms(self.box,Port = port_id,degraded_alarm_mode = DegradedAlarmMode,degraded_threshold = DegradedThreshold)
            except Exception as err:
                print "Configure Alarm Error:", err
    
            try:
                triggerState2 = self.cr_opm_alarms.fetchAlarmState(self.box,Port = port_id)
            except Exception as err:
                print "Fetch Alarm State Error:", err
    
            nose.tools.assert_equal(triggerState1['AlarmCondition'],'warning','Alarm has been triggred for the port')
            nose.tools.assert_equal(triggerState1['DegradedAlarmState'],' Single, Triggered ','Degraded Alarm Mode is not been set to Single, Triggered') 
            nose.tools.assert_equal(triggerState2['AlarmCondition'],'normal','Alarm has not been triggred and its in normal state')
            nose.tools.assert_equal(triggerState2['DegradedAlarmState'],' Off ','Degraded Alarm Mode is not been set to Off')

if 0:                
    class testOpmConfig():
    
    
    
        ports = Config.get("switch_info", "Ports")
        ingress_ports_list = []
        egress_ports_list = []
        for ingress_ports in range(1, int(ports)+1):
            ingress_ports_list.append(ingress_ports)
        for egress_ports in range(int(ports)+1, int(ports+ports)+1):
            egress_ports_list.append(egress_ports)
    
        @classmethod
        def setUpClass(cls):
            cls.box = Node(box_ip)
            cls.cr_opm_config = OPMConfig()         
        
        """OPM CONFIG"""
    
    
        def testOpmConfigPage(self):
            try:
                element = self.cr_opm_config.configure_opm_parameters(self.box,opm_config_page = 'yes')
            except Exception as err:
                print "Navigate to Opm config page error:", err
    
            nose.tools.assert_true(element,'OPM Configuration Page Loading Error')
    
        def testOpmConfigPopUpBox(self):
            port_Id = 5
            try:
                element = self.cr_opm_config.configure_opm_parameters(self.box,Port = port_Id,popUp_Box = 'yes')
            except Exception as err:
                print "Navigate to opm config page or popup box error:", err
    
            nose.tools.assert_true(element,'OPM config page popup box error')
    
        def testEditOpmConfig(self):
            port_Id = 4
            userDict = {'wavelength' : 1600,'offset' : '-10.00', 'average_time' : ' 52.70 '}
    
            try:
                self.cr_opm_config.configure_opm_parameters(self.box,Port =
                    port_Id,Wavelength = userDict['wavelength'],Offset = userDict['offset'],Averaging_time = userDict['average_time'])
            except Exception as err:
                print "Configure OPM parameters error:", err
    
            try:
                opmDict = self.cr_opm_config.fetch_opm_config_values(self.box,Port = port_Id,Wavelength = 'yes',Offset = 'yes',Averaging_time = 'yes')
            except Exception as err:
                print "Fetch opm Config parameter value error:",err
    
            print userDict
            print opmDict        
    
            nose.tools.assert_dict_equal(userDict,opmDict,'OPM configuration parameter values not changed')
    
        def testCancelEditOpmConfig(self):
            port_Id = 15
            wavelnth = 1580
            offset = '-8.00'
            avg_time = ' 105.40 '
    
            try:
                opmDict1 = self.cr_opm_config.fetch_opm_config_values(self.box,Port = port_Id,Wavelength = 'yes',Offset = 'yes',Averaging_time = 'yes')
            except Exception as err:
                print "Fetch opm Config parameter value error:",err        
    
            try:
                self.cr_opm_config.configure_opm_parameters(self.box,Port = port_Id,Wavelength = wavelnth,Offset = offset,Averaging_time = avg_time,Cancel = 'yes')
            except Exception as err:
                print "Configure OPM parameters error:", err
    
            try:
                opmDict2 = self.cr_opm_config.fetch_opm_config_values(self.box,Port = port_Id,Wavelength = 'yes',Offset = 'yes',Averaging_time = 'yes')
            except Exception as err:
                print "Fetch opm Config parameter value error:",err
            
            nose.tools.assert_dict_equal(opmDict1,opmDict2,'OPM configuration parameter values not same after cancel configuration operation')
    
        def testInvalidWaveLengthOpmConfig(self):
            port_Id = 15
            wavelnth = 2222
    
            try:
                alertMessage = self.cr_opm_config.configure_opm_parameters(self.box,Port = port_Id,Wavelength = wavelnth,InvalidCase = 'yes')
            except Exception as err:
                print "Configure OPM parameters error:", err
    
            nose.tools.assert_in("Invalid wavelength value",alertMessage,'Wrong Error Message For Invalid Wavelength')
    
        def testNegativeWaveLengthOpmConfig(self):
            port_Id = 17
            wavelnth = -2222
    
            try:
                alertMessage = self.cr_opm_config.configure_opm_parameters(self.box,Port = port_Id,Wavelength = wavelnth,InvalidCase = 'yes')
            except Exception as err:
                print "Configure OPM parameters error:", err
    
            nose.tools.assert_in("Invalid wavelength value",alertMessage,'Wrong Error Message For Negative Wavelength value')
    
        def testInvalidOffsetOpmConfig(self):
            port_Id = 6
            offset = '200.00'
    
            try:
                alertMessage = self.cr_opm_config.configure_opm_parameters(self.box,Port = port_Id,Offset = offset,InvalidCase = 'yes')
            except Exception as err:
                print "Configure OPM parameters error:", err
    
            #nose.tools.assert_in("Invalid offset value",alertMessage,'Wrong Error Message For Invalid Offset value')
            #build 6.1.2.9
            nose.tools.assert_in("Invalid parameter",alertMessage,'Wrong Error Message For Invalid Offset value')
    
        def testNegativeOffsetOpmConfig(self):
            port_Id = 8
            offset = '-200.00'
    
            try:
                alertMessage = self.cr_opm_config.configure_opm_parameters(self.box,Port = port_Id,Offset = offset,InvalidCase = 'yes')
            except Exception as err:
                print "Configure OPM parameters error:", err
    
            nose.tools.assert_in("Invalid offset value",alertMessage,'Wrong Error Message For Negative Offset value')
    
        def testSetAveragingTime(self):
            port_Id = 15
            avg_time = ' 105.40 '      
    
            try:
                self.cr_opm_config.configure_opm_parameters(self.box,Port = port_Id,Averaging_time = avg_time)
            except Exception as err:
                print "Configure OPM parameters error:", err
    
            try:
                opmDict = self.cr_opm_config.fetch_opm_config_values(self.box,Port = port_Id,Averaging_time = 'yes')
            except Exception as err:
                print "Fetch opm Config parameter value error:",err
            
            nose.tools.assert_equal(avg_time,opmDict['average_time'],'OPM configuration averaging time value is not Set')        

class testPortStatus():


    ports = Config.get("switch_info", "Ports")
    ingress_ports_list = []
    egress_ports_list = []
    for ingress_ports in range(1, int(ports)+1):
        ingress_ports_list.append(ingress_ports)
    for egress_ports in range(int(ports)+1, int(ports+ports)+1):
        egress_ports_list.append(egress_ports)

    @classmethod
    def setUpClass(cls):
        cls.box = Node(box_ip)
        cls.cr_conn = CrossConnects()
        cls.cr_port = PortStatus()   
   
    """PORT STATUS"""

    def testPortStatusPage(self):
        try:
            element = self.cr_port.Configure_port(self.box,port_status_page = 'yes')        
        except Exception as err:
            print "Error Navigate to Port Status Page:", err

        nose.tools.assert_true(element,'Port Status Page Loading Error')

    def testPortStatusPopUpBox(self):
        port_number = self.ingress_ports_list[1]
        try:
            element = self.cr_port.Configure_port(self.box,port = port_number,popUp_Box = 'yes')
        except Exception as err:
            print "Navigate to port status page or popup box error:", err

        nose.tools.assert_true(element,'Port Status Page PopUp Box Generation Error')

    def testDisablePortStatus(self):
        port_number = self.ingress_ports_list[1]
        try:
            self.cr_conn.clear_connections(self.box,ingress_port = port_number)
        except Exception as err:
            print "Clear Connections error:",err

        try:
            self.cr_port.Configure_port(self.box,port = port_number,Enable = 'yes')
        except Exception as err:
            print "Enabling Port Error:", err

        try:
            self.cr_port.Configure_port(self.box,port = port_number,Disable = 'yes')
        except Exception as err:
            print "Disabling Port Error:", err

        try:
            status_fetched = self.cr_port.fetch_status(self.box, port = port_number)
        except Exception as err:
            print "Fetch Port Status err:", err

        nose.tools.assert_equal(str(status_fetched),' Disabled ',"Port Status is not Disabled")

    def testCancelDisablePortStatus(self):
        port_number = self.ingress_ports_list[3]

        try:
            self.cr_port.Configure_port(self.box,port = port_number,Enable = 'yes')
        except Exception as err:
            print "Enabling Port Error:", err

        try:
            status_fetched1 = self.cr_port.fetch_status(self.box, port = port_number)
        except Exception as err:
            print "Fetch Port Status err:", err

        try:
            self.cr_port.Configure_port(self.box,port = port_number,Disable = 'yes',Cancel ='yes')
        except Exception as err:
            print "Disabling Port Error:", err

        try:
            status_fetched2 = self.cr_port.fetch_status(self.box, port = port_number)
        except Exception as err:
            print "Fetch Port Status err:", err

        nose.tools.assert_equal(status_fetched1,status_fetched2,"Port Status is not Same after Cancel Operation")
        
    def testEnablePortStatus(self):
        port_number = self.egress_ports_list[2]
        try:
            self.cr_conn.clear_connections(self.box,egress_port = port_number)
        except Exception as err:
            print "Clear Connections error:",err

        try:
            self.cr_port.Configure_port(self.box,port = port_number,Disable = 'yes')
        except Exception as err:
            print "Disabling Port Error:", err

        try:
            self.cr_port.Configure_port(self.box,port = port_number,Enable = 'yes')
        except Exception as err:
            print "Enabling Port Error:", err

        try:
            status_fetched = self.cr_port.fetch_status(self.box, port = port_number)
        except Exception as err:
            print "Fetch Port Status err:", err

        nose.tools.assert_equal(str(status_fetched),' Enabled ',"Port Status is not Enabled after Port Enable operation")

    def testCancelEnablePortStatus(self):
        port_number = self.ingress_ports_list[5]

        try:
            self.cr_port.Configure_port(self.box,port = port_number,Disable = 'yes')
        except Exception as err:
            print "Disabling Port Error:", err

        try:
            status_fetched1 = self.cr_port.fetch_status(self.box, port = port_number)
        except Exception as err:
            print "Fetch Port Status err:", err

        try:
            self.cr_port.Configure_port(self.box,port = port_number,Enable = 'yes',Cancel ='yes')
        except Exception as err:
            print "Enabling Port Error:", err

        try:
            status_fetched2 = self.cr_port.fetch_status(self.box, port = port_number)
        except Exception as err:
            print "Fetch Port Status err:", err

        nose.tools.assert_equal(status_fetched1,status_fetched2,"Port Status is not Same after Cancel Operation")

    def testDisableConnectedPortStatus(self):
        in_prt = self.ingress_ports_list[5]
        e_prt = self.egress_ports_list[5]
        
        try:
            self.cr_conn.clear_connections(self.box, ingress_port=in_prt, egress_port=e_prt)
        except Exception as err:
            print "Clear Connections Error:", err
            
        try:
            self.cr_port.Configure_port(self.box,port = in_prt,Enable = 'yes')
        except Exception as err:
            print "Enabling Port Error:", err
                    
        try:
            self.cr_conn.enable_connections(self.box, ingress_port=in_prt,
                                            egress_port=e_prt)
        except Exception as err:
            print "Enable CrossConnect Error:", err

        try:
            alertMessage = self.cr_port.Configure_port(self.box,port = in_prt,Disable = 'yes')
            print 'alertMessage : ' , alertMessage
            print '\n'
        except Exception as err:
            print "Disabling Port Error:", err

        try:
            status_fetched = self.cr_port.fetch_status(self.box, port = in_prt)
        except Exception as err:
            print "Fetch Port Status err:", err        

        #nose.tools.assert_in("The port is already in use",alertMessage,'Wrong Alert Message Thrown')
        #build 6.1.2.9
        #nose.tools.assert_in("None",alertMessage,'Wrong Alert Message Thrown')
        nose.tools.assert_equal(str(status_fetched),' Disabled ',"Port Status is not Disabled after Port Diable operation")


if 0:        
    class testOpmPowerLevel():
    
    
    
        ports = Config.get("switch_info", "Ports")
        ingress_ports_list = []
        egress_ports_list = []
        for ingress_ports in range(1, int(ports)+1):
            ingress_ports_list.append(ingress_ports)
        for egress_ports in range(int(ports)+1, int(ports+ports)+1):
            egress_ports_list.append(egress_ports)
    
        @classmethod
        def setUpClass(cls):
            cls.box = Node(box_ip)
            cls.cr_opm_powerlevels = OpmPowerLevels()
            cls.cr_opm_alarms = OpmAlarms()
    
        """OPM POWER LEVEL"""
    
    
        def testOpmPowerLevelPage(self):
            try:
                element = self.cr_opm_powerlevels.fetchPowerLevelStatus(self.box,'power_levels_page')
            except Exception as err:
                print "Navigate to Opm Power Levels page error:", err
    
            nose.tools.assert_true(element,'OPM Power Level Page Loading Error')
    
        def testvalidateDegradedAlarmtrigger(self):
            port_id = 5
            DegradedAlarmMode = 'Single'
            DegradedThreshold = '-25.00'
            
            try:
                self.cr_opm_alarms.configureAlarms(self.box,Port = port_id,los_alarm_mode = 'Off',los_alarm_edge = 'Low',los_low_threshold = '-60.0',los_high_threshold = '25.0',degraded_alarm_mode ='off',degraded_threshold = '-60.00')
            except Exception as err:
                print "Configure Alarm Error:", err
    
            try:
                triggerState1 = self.cr_opm_alarms.fetchAlarmState(self.box,Port = port_id)
            except Exception as err:
                print "Fetch Alarm State Error:", err
            
            try:
                self.cr_opm_alarms.configureAlarms(self.box,Port = port_id,degraded_alarm_mode = DegradedAlarmMode,degraded_threshold = DegradedThreshold)
            except Exception as err:
                print "Configure Alarm Error:", err
    
            try:
                triggerState2 = self.cr_opm_alarms.fetchAlarmState(self.box,Port = port_id)
            except Exception as err:
                print "Fetch Alarm State Error:", err
                
            try:
                triggerStatus = self.cr_opm_powerlevels.fetchPowerLevelStatus(self.box,Port = port_id)
            except Exception as err:
                print "Fetch Power Level Status Error:", err
    
    
            nose.tools.assert_equal(triggerState1['AlarmCondition'],'normal','Alarm has been triggred for the port')
            nose.tools.assert_equal(triggerState1['DegradedAlarmState'],' Off ','Degraded Alarm Mode is not been set to Off') 
            nose.tools.assert_equal(triggerState2['AlarmCondition'],'warning','Alarm has not been triggred and its in normal state')
            nose.tools.assert_equal(triggerState2['DegradedAlarmState'],' Single, Triggered ','Degraded Alarm Mode is not been set to Single, Triggered')
            nose.tools.assert_equal(triggerStatus['PortStatus'],'warning','Port in the Power level page does not show the status as warning')
            nose.tools.assert_equal(triggerStatus['StatusType'],' Degraded Signal ','Power level page does not show the Port status')
    
        def testvalidateLosAlarmtrigger(self):
            port_id = 22
            LosAlarmMode = 'Single'
            LosAlarmEdge = 'Low'
            LosLowThreshold = '-20.00'
            LosHighThreshold = '10.00'
            
            try:
                self.cr_opm_alarms.configureAlarms(self.box,Port =
                    port_id,los_alarm_mode = 'Off',los_alarm_edge = 'Low',los_low_threshold = '-60.0',los_high_threshold = '25.0',degraded_alarm_mode ='Off',degraded_threshold = '0')
            except Exception as err:
                print "Configure Alarm Error:", err
    
            try:
                triggerState1 = self.cr_opm_alarms.fetchAlarmState(self.box,Port = port_id)
            except Exception as err:
                print "Fetch Alarm State Error:", err
                
            try:
                self.cr_opm_alarms.configureAlarms(self.box,Port = port_id,los_alarm_mode = LosAlarmMode,los_alarm_edge = LosAlarmEdge,los_low_threshold = LosLowThreshold,los_high_threshold = LosHighThreshold)
            except Exception as err:
                print "Configure Alarm Error:", err
    
            try:
                triggerState2 = self.cr_opm_alarms.fetchAlarmState(self.box,Port = port_id)
            except Exception as err:
                print "Fetch Alarm State Error:", err
    
            try:
                triggerStatus = self.cr_opm_powerlevels.fetchPowerLevelStatus(self.box,Port = port_id)
            except Exception as err:
                print "Fetch Power Level Status Error:", err
    
            print "triggerState1:",triggerState1
            print "triggerState2:",triggerState2
            print "triggerStatus:",triggerStatus
    
            nose.tools.assert_equal(triggerState1['AlarmCondition'],'normal','Alarm has been triggred for the port')
            nose.tools.assert_equal(triggerState1['LosAlarmState'],' Off ','Los Alarm Mode is not been set to Off') 
            nose.tools.assert_equal(triggerState2['AlarmCondition'],'alarmed','Alarm has not been triggred and its in normal state')
            nose.tools.assert_equal(triggerState2['LosAlarmState'],' Single, Triggered ','Los Alarm Mode is not been set to Single, Triggered')
            nose.tools.assert_equal(triggerStatus['PortStatus'],'alarmed','Port in the Power level page does not show the status as alarmed')
            nose.tools.assert_equal(triggerStatus['StatusType'],' Loss of Service ','Power level page does not show the Port status')
    
class testStatus():

    @classmethod
    def setUpClass(cls):
        cls.box = Node(box_ip)
        cls.cr_status = StatusConfig()
        
    """STATUS"""


    def testStatusPage(self): 
        
        try:
            element = self.cr_status.view_events_button(self.box,'status_page')
        except Exception as err:
            print "Status Page Loading Error:", err

        nose.tools.assert_true(element,'Status Page Loading Error')

    def testEnvironmentalViewButton(self):

        try:
            element = self.cr_status.view_events_button(self.box,'environmental')
        except Exception as err:
            print "Click on Environmental View button error:", err

        nose.tools.assert_true(element,'Environmental Events are not displayed')

    def testPortsViewButton(self):

        try:
            element = self.cr_status.view_events_button(self.box,'ports')
        except Exception as err:
            print "Click on Ports View button error:", err

        nose.tools.assert_true(element,'Ports Events are not displayed')

    def testPowerSupplyViewButton(self):

        try:
            element = self.cr_status.view_events_button(self.box,'powersupply')
        except Exception as err:
            print "Click on Power Supply View button error:", err

        nose.tools.assert_true(element,'Power Supply Events are not displayed')

    def testSystemViewButton(self):

        try:
            element = self.cr_status.view_events_button(self.box,'system')
        except Exception as err:
            print "Click on System View button error:", err

        nose.tools.assert_true(element,'System Events are not displayed')

    #def testOPMViewButton(self):

    #    try:
    #        element = self.cr_status.view_events_button(self.box,'opticalpowermonitor')
    #    except Exception as err:
    #        print "Click on Optical Power Monitor View button error:", err

    #    nose.tools.assert_true(element,'Optical Power Monitor Events are not displayed')


class testUserConfiguration():

    @classmethod
    def setUpClass(cls):
        cls.cr_user = UserConfig()
        cls.box = Node(box_ip)
    
    def testUserConfigPage(self):

        try:
            element = self.cr_user.create_user(self.box,'user_config_page')
        except Exception as err:
            print "Login or Navigate to User Config Page Error:", err

        nose.tools.assert_true(element,'User Config Page Loading Error')

    def testCreateUserPopUpBox(self):

        try:
            element = self.cr_user.create_user(self.box,'user_editor_popup')
        except Exception as err:
            print "Login or Navigate to User Config Page or PopUp Create User Box Error:", err

        nose.tools.assert_true(element,'Create User PopUp Box Not Displayed')

    def testCreateAdminTypeUser(self):
        usrname = 'testAdmin'
        passwrd = 'admin'
        usrtype = 'admin'

        try:
            self.cr_user.deleteAllUsers(self.box)
        except Exception as err:
            print "Delete All Users Error:", err
        
        try:
            #for i in range(1, 31):
            #    usrname = "polatis"+str(i)
            #    passwrd = "polatis"+str(i)
            self.cr_user.create_user(self.box,'same_session',new_username = usrname, new_userpasswd = passwrd, new_usertype = usrtype)
        except Exception as err:
            print "Create User Error:", err

        try:
            element = self.cr_user.check_user(self.box,'same_session',user_name = usrname)
        except Exception as err:
            print "Check User Error:", err

        try:
            pageContent = self.cr_user.check_content(self.box,'page_content',user_name = usrname,Password = passwrd)
        except Exception as err:
            print "Newly Created User Login Credential Error:", err        

        value = 'System Config\nNetwork Config\nSNMP Config\nUpgrade\nUser Config'
        nose.tools.assert_true(element,'Create User is not displayed in the userConfig page')
        nose.tools.assert_in(value,pageContent,'Page Contains Admin Type User Credentials')

    def testCreateUserTypeUser(self):
        usrname = 'testUser'
        passwrd = 'user'
        usrtype = 'user'

        try:
            self.cr_user.deleteAllUsers(self.box)
        except Exception as err:
            print "Delete All Users Error:", err

        try:
            self.cr_user.create_user(self.box,'same_session',new_username = usrname, new_userpasswd = passwrd, new_usertype = usrtype)
        except Exception as err:
            print "Create User Error:", err

        try:
            element = self.cr_user.check_user(self.box,'same_session',user_name = usrname)
        except Exception as err:
            print "Check User Error:", err

        try:
            pageContent = self.cr_user.check_content(self.box,'page_content',user_name = usrname,Password = passwrd)        
        except Exception as err:
            print "Newly Created User Login Credential Error:", err
            
        value = 'System Config\nNetwork Config\nSNMP Config\nUpgrade\nUser Config'
        nose.tools.assert_true(element,'Created User is not displayed in the UserConfig page')
        nose.tools.assert_not_in(value,pageContent,'Page Contains Admin Type User Credentials')

    def testCreateViewTypeUser(self):
        usrname = 'testView'
        passwrd = 'view'
        usrtype = 'view'

        try:
            self.cr_user.deleteAllUsers(self.box)
        except Exception as err:
            print "Delete All Users Error:", err

        try:
            self.cr_user.create_user(self.box,'same_session',new_username = usrname, new_userpasswd = passwrd, new_usertype = usrtype)
        except Exception as err:
            print "Create User Error:", err

        try:
            element = self.cr_user.check_user(self.box,'same_session',user_name = usrname)
        except Exception as err:
            print "Check User Error:", err

        try:
            pageContent = self.cr_user.check_content(self.box,'page_content',user_name = usrname,Password = passwrd)
        except Exception as err:
            print "Newly Created User Login Credential Error:", err
            
        value = 'System Config\nNetwork Config\nSNMP Config\nUpgrade\nUser Config'
        nose.tools.assert_true(element,'Created User is not displayed in the UserConfig page')
        nose.tools.assert_not_in(value,pageContent,'Page Contains Admin Type User Credentials')

    def testCancelNewUser(self):
        usrname = 'canceltstAdmin'
        passwrd = 'admin'
        usrtype = 'admin'
        
        try:
            element = self.cr_user.create_user(self.box,new_username = usrname, new_userpasswd = passwrd, new_usertype = usrtype, Cancel = 'yes')
        except Exception as err:
            print "Create User Error:", err

        nose.tools.assert_not_in(' canceltstAdmin ', element, 'Cancel Functiontionality Error')

    def testSetPasswordUserViewTypeUser(self):
        usrname = 'testUser1'
        passwrd = 'user'
        usrtype = 'user'
        new_pswrd = 'user1'

        try:
            self.cr_user.deleteAllUsers(self.box)
        except Exception as err:
            print "Delete All Users Error:", err
        
        try:
            self.cr_user.create_user(self.box,'same_session',new_username = usrname, new_userpasswd = passwrd, new_usertype = usrtype)
        except Exception as err:
            print "Create User Error:", err
        
        try:
            self.cr_user.set_password_user_view(self.box,UserName = usrname,Password = passwrd,old_password = passwrd,new_password = new_pswrd)
        except Exception as err:
            print "Set Password Error:", err

        try:
            element = self.box.gui_login_page(UserName = usrname,Password = new_pswrd,main_page = 'yes')     
        except Exception as err:
            print "Cannot Login with Newly changed Password:", err
        
        nose.tools.assert_true(element,'Password is not set for View type user')
        
    def testCreateUserInvalidUserName(self):    
        usrname = 'Polati#'
        passwrd = 'Polatis123'
        usrtype = 'admin'
        
        try:
            alertMessage = self.cr_user.create_user(self.box,new_username = usrname, new_userpasswd = passwrd, new_usertype = usrtype, InvalidCase = 'yes' )
        except Exception as err:
            print "Create User Error:", err

        nose.tools.assert_in("Invalid user name",alertMessage,'Invalid User Name Message Mismatch Error')

    def testCreateUserMaxInvalidUserName(self):
        usrname = 'Polatis123456789Polatis'
        passwrd = 'Polatis123'
        usrtype = 'admin'
        
        try:
            alertMessage = self.cr_user.create_user(self.box,new_username = usrname, new_userpasswd = passwrd, new_usertype = usrtype, InvalidCase = 'yes' )
        except Exception as err:
            print "Create User Error:", err

        nose.tools.assert_in("Invalid user name",alertMessage,'Invalid User Name Message Mismatch Error')

    def testCreateUserInvalidpassword(self):
        usrname = 'Polatis'
        passwrd = 'Polat@#'
        usrtype = 'admin'
        
        try:
            alertMessage = self.cr_user.create_user(self.box,new_username = usrname, new_userpasswd = passwrd, new_usertype = usrtype, InvalidCase = 'yes' )
        except Exception as err:
            print "Create User Error:", err

        nose.tools.assert_in("Invalid password",alertMessage,'Invalid Password Message Mismatch Error')

    def testCreateUserEmptyPassword(self):
        usrname = 'Polatis'
        passwrd = ''
        usrtype = 'admin'
        
        try:
            alertMessage = self.cr_user.create_user(self.box,new_username = usrname, new_userpasswd = passwrd, new_usertype = usrtype, InvalidCase = 'yes' )
        except Exception as err:
            print "Create User Error:", err

        nose.tools.assert_in("User password must be provided",alertMessage,'Alert Message Mismatch Error')

    def testEditUserType(self):
        usrname = 'testUser2'
        passwrd = 'user'
        usrtype = 'user'
        new_usertype = 'admin'

        try:
            self.cr_user.deleteAllUsers(self.box)
        except Exception as err:
            print "Delete All Users Error:", err

        try:
            self.cr_user.create_user(self.box,'same_session',new_username = usrname, new_userpasswd = passwrd, new_usertype = usrtype)
        except Exception as err:
            print "Create User Error:", err
        
        try:
            self.cr_user.edit_user(self.box,'same_session',user_name = usrname, edit_userpasswd = passwrd, edit_usertype = new_usertype)
        except Exception as err:
            print "Edit User Error:", err

        try:
            userType  = self.cr_user.check_content(self.box,user_name = usrname,Password = passwrd)    
        except Exception as err:
            print "Edited User Login Credential Error:", err
        print "userType:", userType
        print "tyep:", type(userType['usrType'])
            
        nose.tools.assert_in(new_usertype,userType['usrType'],'User Type Not set after Edit Operation')

    def testEditUserPassword(self):
        usrname = 'testUser3'
        passwrd = 'user'
        usrtype = 'user'
        new_passwrd = 'user123'
        try:
            self.cr_user.deleteAllUsers(self.box)
        except Exception as err:
            print "Delete All Users Error:", err

        try:
            self.cr_user.create_user(self.box,'same_session',new_username = usrname, new_userpasswd = passwrd, new_usertype = usrtype)
        except Exception as err:
            print "Create User Error:", err
        
        try:
            self.cr_user.edit_user(self.box,'same_session',user_name = usrname, edit_userpasswd = new_passwrd)
        except Exception as err:
            print "Create User Error:", err

        try:
            element = self.box.gui_login_page(UserName = usrname,Password = new_passwrd,main_page = 'yes')
            time.sleep(5)          
        except Exception as err:
            print "Error Login using edited password ", err

        nose.tools.assert_true(element,'Login Failure using edited password')

    def testCancelEditUser(self):
        usrname = 'testAdmin4'
        passwrd = 'admin'
        usrtype = 'admin'
        new_passwrd = 'user123'
        new_usertype = 'user'
        
        try:
            self.cr_user.deleteAllUsers(self.box)
        except Exception as err:
            print "Delete All Users Error:", err

        try:
            self.cr_user.create_user(self.box,'same_session',new_username = usrname, new_userpasswd = passwrd, new_usertype = usrtype)
        except Exception as err:
            print "Create User Error:", err
            
        try:
            self.cr_user.edit_user(self.box,'same_session',user_name = usrname,edit_userpasswd = new_passwrd, edit_usertype = new_usertype, Cancel = 'yes')
        except Exception as err:
            print "Edit User Error:", err

        try:
            userType  = self.cr_user.check_content(self.box,user_name = usrname,Password = passwrd)
        except Exception as err:
            print "Error Login using edited password ", err
        
        print 'userType@1:', userType
        
        nose.tools.assert_true(userType['login_page'],'Login Failure using edited password')        
        nose.tools.assert_in(usrtype,userType['usrType'],'User Type Not set after Edit Operation')

    def testEditInvalidPassword(self):
        usrname = 'testUser5'
        passwrd = 'user'
        usrtype = 'user'
        new_passwrd = 'polatis!@#'
        new_usertype = 'admin'

        try:
            self.cr_user.deleteAllUsers(self.box)
        except Exception as err:
            print "Delete All Users Error:", err
        
        try:
            self.cr_user.create_user(self.box,'same_session',new_username = usrname, new_userpasswd = passwrd, new_usertype = usrtype)
        except Exception as err:
            print "Create User Error:", err
            
        try:
            alertMessage = self.cr_user.edit_user(self.box,'same_session',user_name = usrname, edit_userpasswd = new_passwrd, edit_usertype = new_usertype, InvalidCase = 'yes')
        except Exception as err:
            print "Create User Error:", err        

        nose.tools.assert_in("Invalid password!",alertMessage,'Invalid Password Message Mismatch Error')

    def testEditEmptyPassword(self):
        usrname = 'testUser6'
        passwrd = 'user'
        usrtype = 'user'
        new_passwrd = ''
        new_usertype = 'admin'

        try:
            self.cr_user.deleteAllUsers(self.box)
        except Exception as err:
            print "Delete All Users Error:", err

        try:
            self.cr_user.create_user(self.box,'same_session',new_username = usrname, new_userpasswd = passwrd, new_usertype = usrtype)
        except Exception as err:
            print "Create User Error:", err
            
        try:
            alertMessage = self.cr_user.edit_user(self.box,'same_session',user_name = usrname, edit_userpasswd = new_passwrd, edit_usertype = new_usertype, InvalidCase = 'yes')
        except Exception as err:
            print "Create User Error:", err      

        nose.tools.assert_in("Invalid password",alertMessage,'Alert Message Mismatch Error')

    def testDeleteUser(self):
        usrname = 'testUser7'
        passwrd = 'user'
        usrtype = 'user'

        try:
            self.cr_user.deleteAllUsers(self.box)
        except Exception as err:
            print "Delete All Users Error:", err

        try:
            self.cr_user.create_user(self.box,'same_session',new_username = usrname, new_userpasswd = passwrd, new_usertype = usrtype)
        except Exception as err:
            print "Create User Error:", err
            
        try:
            element = self.cr_user.delete_user(self.box,'same_session',user_name = usrname)
        except Exception as err:
            print "Delete User Error:", err

        nose.tools.assert_not_in('testUser7', element, 'User Has Not been Deleted')

    def testCancelDeleteUser(self):
        usrname = 'testUser8'
        passwrd = 'user'
        usrtype = 'user'

        try:
            self.cr_user.deleteAllUsers(self.box)
        except Exception as err:
            print "Delete All Users Error:", err
        
        try:
            self.cr_user.create_user(self.box,'same_session',new_username = usrname, new_userpasswd = passwrd, new_usertype = usrtype)
        except Exception as err:
            print "Create User Error:", err

        try:
            element = self.cr_user.delete_user(self.box,'same_session',user_name = usrname, Cancel = 'yes')
        except Exception as err:
            print "Create User Error:", err    
        print element
        nose.tools.assert_in(' testUser8 ', element, 'Cancel Functiontionality Error')

class testConnectionTable():

    ports = Config.get("switch_info", "Ports")
    ingress_ports_list = []
    egress_ports_list = []
    for ingress_ports in range(1, int(ports)+1):
        ingress_ports_list.append(ingress_ports)
    for egress_ports in range(int(ports)+1, int(ports+ports)+1):
        egress_ports_list.append(egress_ports)

    @classmethod
    def setUpClass(cls):
        cls.cr_conn = CrossConnects()
        cls.cr_port = PortStatus()
        cls.box = Node(box_ip)

    def testSetPortLabel(self):
        prt_id = self.ingress_ports_list[5]
        prt_label = 'polatis'           
        try:
            self.cr_conn.set_portlabel(self.box, port_id = prt_id,port_label = prt_label)
        except Exception as err:
            print "Set Label Error:", err

        try:
            fetched_label = self.cr_conn.fetch_portlabel(self.box, port = prt_id)
            label_fetched = str(fetched_label)
        except Exception as err:
            print "Fetch Label Error:", err

        nose.tools.assert_equal(prt_label,label_fetched,'Label not set for the port')

    def testCancelSetPortLabel(self):
        prt_id = self.ingress_ports_list[2]
        prt_label = 'polatis12'
        try:
            fetched_label1 = self.cr_conn.fetch_portlabel(self.box, port = prt_id)
            label_fetched1 = str(fetched_label1)
        except Exception as err:
            print "Fetch Label1 Error:", err
        
        try:
            self.cr_conn.set_portlabel(self.box, port_id = prt_id,port_label = prt_label,Cancel = 'yes')
        except Exception as err:
            print "Set Label Error:", err 

        try:
            fetched_label2 = self.cr_conn.fetch_portlabel(self.box, port = prt_id)
            label_fetched2 = str(fetched_label2)
        except Exception as err:
            print "Fetch Label2 Error:", err
        
        nose.tools.assert_equal(label_fetched1,label_fetched2,'Port label Mismatch after the cancel operation')

    def testSetMaxCharPortLabel(self):
        prt_id = self.ingress_ports_list[7]
        prt_label = 'wwwwwwwwwwwwwwwwwwww'

        try:
            self.cr_conn.set_portlabel(self.box, port_id = prt_id,port_label = prt_label)
        except Exception as err:
            print "Set Label Error:", err

        try:
            fetched_label = self.cr_conn.fetch_portlabel(self.box, port = prt_id)
            label_fetched = str(fetched_label)
        except Exception as err:
            print "Fetch Label Error:", err

        nose.tools.assert_equal(prt_label,label_fetched,'Max Character Label not set for the port')

    def testSetInvalidPortLabel(self):
        prt_id = self.ingress_ports_list[5]
        prt_label = 'Polatis12#'

        try:
            alertMessage = self.cr_conn.set_portlabel(self.box, port_id = prt_id,port_label = prt_label, InvalidCase = 'yes')
        except Exception as err:
            print "Set Label Error:", err

        nose.tools.assert_in("Invalid port label!",alertMessage,'Alert Message Mismatch Error')

    def testSetInvalidMaxCharPortLabel(self):
        prt_id = self.ingress_ports_list[5]
        prt_label = 'TerafastPolatis123456'

        try:
            alertMessage = self.cr_conn.set_portlabel(self.box, port_id = prt_id,port_label = prt_label, InvalidCase = 'yes')
        except Exception as err:
            print "Set Label Error:", err

        nose.tools.assert_in("Names can be a maximum of 20 characters in length",alertMessage,'Alert Message Mismatch Error')

    def testUpdatePortLabel(self):
        prt_id = self.ingress_ports_list[5]
        prt_label = 'polatis'
        updated_prt_label = 'testpolatis'

        try:
            self.cr_conn.set_portlabel(self.box, port_id = prt_id,port_label = prt_label)
        except Exception as err:
            print "update Label Error:", err        
        try:
            self.cr_conn.set_portlabel(self.box, port_id = prt_id,port_label = updated_prt_label)
        except Exception as err:
            print "update Label Error:", err

        try:
            fetched_label = self.cr_conn.fetch_portlabel(self.box, port = prt_id)
            label_fetched = str(fetched_label)
        except Exception as err:
            print "Fetch Label Error:", err

        nose.tools.assert_equal(updated_prt_label,label_fetched,'Label not updated for the port')

    def testDeletePortLabel(self):
        prt_id = self.ingress_ports_list[5]
        prt_label = 'testpolatis'
        
        try:
            self.cr_conn.set_portlabel(self.box, port_id = prt_id,port_label = prt_label)
        except Exception as err:
            print "Set Label Error:", err
            
        try:
            self.cr_conn.remove_portlabel(self.box, port_id = prt_id)
        except Exception as err:
            print "Remove Label Error:", err

        try:
            fetched_label = self.cr_conn.fetch_portlabel(self.box, port = prt_id)
            label_fetched = len(fetched_label)
        except Exception as err:
            print "Fetch Label Error:", err

        nose.tools.assert_equal(0,label_fetched,'Label not updated for the port')

    def testEnableCrossConnect(self):

        in_prt = self.ingress_ports_list[5]
        e_prt = self.egress_ports_list[5]

        try:
            self.cr_conn.clear_connections(self.box, ingress_port=in_prt, egress_port=e_prt)
        except Exception as err:
            print "Clear Connections Error:", err
        try:
            self.cr_conn.enable_connections(self.box, ingress_port=in_prt,
                                            egress_port=e_prt)
        except Exception as err:
            print "Enable CrossConnect Error:", err

        try:
            fetched_port = self.cr_conn.fetch_connections(self.box,port=in_prt)
            port_fetched = int(fetched_port)
        except Exception as err:
            print "Fetch Connecton Error:", err

        nose.tools.assert_equal(e_prt,port_fetched,
            'Connection has not been established between given ingress_port and eggress_port')

    def testEnableInvalidIngressIngressorEgressEgressCrossConnect(self):
        in_prt = self.ingress_ports_list[5]
        e_prt = self.ingress_ports_list[7]

        try:
            self.cr_conn.clear_connections(self.box, ingress_port=in_prt, egress_port=e_prt)
        except Exception as err:
            print "Clear Connections Error:", err
            
        try:
            alertMessage = self.cr_conn.enable_connections(self.box, ingress_port=in_prt, egress_port=e_prt,InvalidCase = 'yes')
        except Exception as err:
            print "Enable CrossConnect Error:", err
        expectedAlert = 'Ports %s and %s cannot be connected' %(in_prt,e_prt)
        
        nose.tools.assert_in(expectedAlert,alertMessage,'Alert Message Mismatch Error')

    def testEnableInvalidPortNumberCrossConnect(self):
        in_prt = self.ingress_ports_list[3]
        e_prt = 600

        try:
            alertMessage = self.cr_conn.enable_connections(self.box, ingress_port=in_prt, egress_port=e_prt,InvalidCase = 'yes')
        except Exception as err:
            print "Enable CrossConnect Error:", err
        
        nose.tools.assert_in('port specified is invalid',alertMessage,'Alert Message Mismatch Error')

    def testEnableInvalidTextCrossConnect(self):
        in_prt = self.ingress_ports_list[5]
        e_prt = 'Label1'

        try:
            self.cr_conn.clear_connections(self.box, ingress_port=in_prt, egress_port=e_prt)
        except Exception as err:
            print "Clear Connections Error:", err
        try:
            alertMessage = self.cr_conn.enable_connections(self.box, ingress_port=in_prt, egress_port=e_prt,InvalidCase = 'yes')
        except Exception as err:
            print "Enable CrossConnect Error:", err
        
        nose.tools.assert_in('port specified is invalid',alertMessage,'Alert Message Mismatch Error')

    def testEnableInvalidNegativeCrossConnect(self):
        in_prt = self.ingress_ports_list[5]
        e_prt = -23

        try:
            alertMessage = self.cr_conn.enable_connections(self.box, ingress_port=in_prt, egress_port=e_prt,InvalidCase = 'yes')
        except Exception as err:
            print "Enable CrossConnect Error:", err
        
        nose.tools.assert_in('port specified is invalid',alertMessage,'Alert Message Mismatch Error')

    def testCancelEnableCrossConnect(self):
        in_prt = self.ingress_ports_list[5]
        e_prt = self.egress_ports_list[5]

        try:
            self.cr_conn.clear_connections(self.box, ingress_port=in_prt, egress_port=e_prt)
        except Exception as err:
            print "Clear Connections Error:", err        

        try:
            fetched_port1 = self.cr_conn.fetch_connections(self.box,port=in_prt)
            port_fetched1 = str(fetched_port1)
        except Exception as err:
            print "Fetch Connecton Error:", err

        try:
            self.cr_conn.enable_connections(self.box, ingress_port=in_prt,egress_port=e_prt,Cancel = 'yes')
        except Exception as err:
            print "Enable CrossConnect Error:", err
            
        try:
            fetched_port2 = self.cr_conn.fetch_connections(self.box,port=in_prt)
            port_fetched2 = str(fetched_port2)
        except Exception as err:
            print "Fetch Connecton Error:", err
        
        nose.tools.assert_equal(port_fetched1,port_fetched2,'Port Connection Mismatch after the cancel operation')

    def testEditCrossConnect(self):

        in_prt = self.ingress_ports_list[5]
        e_prt = self.egress_ports_list[5]
        edit_e_prt = self.egress_ports_list[7]

        try:
            self.cr_conn.clear_connections(self.box,ingress_port=in_prt,egress_port=e_prt)
        except Exception as err:
            print "Clear CrossConnect Error:", err

        try:
            self.cr_conn.enable_connections(self.box, ingress_port=in_prt,egress_port=e_prt)
        except Exception as err:
            print "Enable CrossConnect Error:", err
        
        try:
            self.cr_conn.edit_connections(self.box,ingress_port=in_prt,egress_port=edit_e_prt)
        except Exception as err:
            print "Update CrossConnect Error:", err

        try:
            fetched_port = self.cr_conn.fetch_connections(self.box,port=in_prt)
            port_fetched = int(fetched_port)
        except Exception as err:
            print "Fetch Connection Error:", err

        nose.tools.assert_equal(edit_e_prt,port_fetched,'Connection not Updated in Ingress_Port')
        
    def testCancelEditCrossConnect(self):
        in_prt = self.ingress_ports_list[5]
        e_prt = self.egress_ports_list[5]
        edit_e_prt = self.egress_ports_list[6]        

        try:
            self.cr_conn.clear_connections(self.box,ingress_port=in_prt,egress_port=e_prt)
        except Exception as err:
            print "Clear CrossConnect Error:", err

        try:
            self.cr_conn.enable_connections(self.box, ingress_port=in_prt,egress_port=e_prt)
        except Exception as err:
            print "Enable CrossConnect Error:", err
        try:
            fetched_port1 = self.cr_conn.fetch_connections(self.box,port=in_prt)
            port_fetched1 = str(fetched_port1)
        except Exception as err:
            print "Fetch Connecton Error:", err

        try:
            self.cr_conn.edit_connections(self.box, ingress_port=in_prt,egress_port=edit_e_prt,Cancel = 'yes')
        except Exception as err:
            print "Enable CrossConnect Error:", err
            
        try:
            fetched_port2 = self.cr_conn.fetch_connections(self.box,port=in_prt)
            port_fetched2 = str(fetched_port2)
        except Exception as err:
            print "Fetch Connecton Error:", err
        
        nose.tools.assert_equal(port_fetched1,port_fetched2,'Port Connection Mismatch after the cancel operation')
                        

    def testEditInvalidCrossConnect(self):
        in_prt = self.ingress_ports_list[5]
        e_prt = self.egress_ports_list[5]
        edit_e_prt = self.ingress_ports_list[7]

        try:
            self.cr_conn.clear_connections(self.box,ingress_port=in_prt,egress_port=e_prt)
        except Exception as err:
            print "Clear CrossConnect Error:", err

        try:
            self.cr_conn.enable_connections(self.box, ingress_port=in_prt,egress_port=e_prt)
        except Exception as err:
            print "Enable CrossConnect Error:", err              

        try:
            alertMessage = self.cr_conn.edit_connections(self.box,ingress_port=in_prt,egress_port=edit_e_prt,InvalidCase = 'yes')
        except Exception as err:
            print "Edit CrossConnect Error:", err
        expectedAlert = 'Ports %s and %s cannot be connected' %(in_prt,edit_e_prt)
        #print "ExceptedAlert:", expectedAlert
        #print "Alert:", alertMessage
        #print "Type of expectedAlert:", type(expectedAlert)
        #print "Type of Alert:", type(alertMessage)

        
        nose.tools.assert_in(expectedAlert,alertMessage,'Alert Message Mismatch Error')

    def testEditNegativePortCrossConnect(self):
        in_prt = self.ingress_ports_list[5]
        e_prt = self.egress_ports_list[5]
        edit_e_prt = -2

        try:
            self.cr_conn.clear_connections(self.box,ingress_port=in_prt,egress_port=e_prt)
        except Exception as err:
            print "Clear CrossConnect Error:", err

        try:
            self.cr_conn.enable_connections(self.box, ingress_port=in_prt,egress_port=e_prt)
        except Exception as err:
            print "Enable CrossConnect Error:", errr    

        try:
            alertMessage = self.cr_conn.edit_connections(self.box, ingress_port=in_prt, egress_port=edit_e_prt,InvalidCase = 'yes')
        except Exception as err:
            print "Enable CrossConnect Error:", err
        
        nose.tools.assert_in('port specified is invalid',alertMessage,'Alert Message Mismatch Error')

    def testEditInvalidPortCrossConnect(self):
        in_prt = self.ingress_ports_list[5]
        e_prt = self.egress_ports_list[5]
        edit_e_prt = 'Ladel##'

        try:
            self.cr_conn.clear_connections(self.box,ingress_port=in_prt,egress_port=e_prt)
        except Exception as err:
            print "Clear CrossConnect Error:", err

        try:
            self.cr_conn.enable_connections(self.box, ingress_port=in_prt,egress_port=e_prt)
        except Exception as err:
            print "Enable CrossConnect Error:", err  

        try:
            alertMessage = self.cr_conn.edit_connections(self.box, ingress_port=in_prt, egress_port=edit_e_prt,InvalidCase = 'yes')
            print "alert message : ", alertMessage
        except Exception as err:
            print "Enable CrossConnect Error:", err
        
        #nose.tools.assert_in('port specified is invalid',alertMessage,'Alert Message Mismatch Error')    
        nose.tools.assert_in('Port 6 is already in use. Continue?',alertMessage,'Alert Message Mismatch Error')    

    def testDisableCrossConnect(self):

        in_prt = self.ingress_ports_list[5]
        e_prt = self.egress_ports_list[5]
        
        try:
            self.cr_conn.clear_connections(self.box,ingress_port=in_prt,egress_port=e_prt)
        except Exception as err:
            print "Clear CrossConnect Error:", err

        try:
            self.cr_conn.enable_connections(self.box, ingress_port=in_prt,egress_port=e_prt)
        except Exception as err:
            print "Enable CrossConnect Error:", err 

 
        try:
            self.cr_conn.disable_connections(self.box, ingress_port=in_prt, egress_port = e_prt, InvalidCase = 'yes')
        except Exception as err:
            print "Disable CrossConnect Error:", err
        
        try:
            fetched_port = self.cr_conn.fetch_connections(self.box,port=in_prt)
            port_fetched = len(fetched_port)
        except Exception as err:
            print "Fetch Connection Error:", err

        nose.tools.assert_equal(0,port_fetched,'Connection not disabled from Ingress_Port')

    #def testInvalidIngressEgressPortDisconnectPort(self):
    #    in_prt = self.ingress_ports_list[5]
    #    e_prt = self.egress_ports_list[5]
    #    invalid_e_prt = 222
    #    try:
    #        self.cr_conn.clear_connections(self.box,ingress_port=in_prt,egress_port=e_prt)
    #    except Exception as err:
    #        print "Clear CrossConnect Error:", err

    #    try:
    #        self.cr_conn.enable_connections(self.box, ingress_port=in_prt,egress_port=e_prt)
    #    except Exception as err:
    #        print "Enable CrossConnect Error:", err  
    #    
    #    try:
    #        alertMessage = self.cr_conn.disable_connections(self.box, ingress_port=in_prt, egress_port = invalid_e_prt, InvalidCase = 'yes')
    #    except Exception as err:
    #        print "Disable CrossConnect Error:", err
    #    
    #    nose.tools.assert_in('port specified is invalid',alertMessage,'Alert Message Mismatch Error')

    #def testInvalidIngressIngressorEgressEgressPortDisconnectPort(self):
    #    in_prt = self.ingress_ports_list[5]
    #    e_prt = self.egress_ports_list[5]
    #    invalid_e_prt = self.ingress_ports_list[7]

    #    try:
    #        self.cr_conn.clear_connections(self.box,ingress_port=in_prt,egress_port=e_prt)
    #    except Exception as err:
    #        print "Clear CrossConnect Error:", err

    #    try:
    #        self.cr_conn.enable_connections(self.box, ingress_port=in_prt,egress_port=e_prt)
    #    except Exception as err:
    #        print "Enable CrossConnect Error:", err         
    #    try:
    #        alertMessage = self.cr_conn.disable_connections(self.box, ingress_port=in_prt, egress_port = e_prt, InvalidCase = 'yes')
    #    except Exception as err:
    #        print "Disable CrossConnect Error:", err
    #    
    #    nose.tools.assert_in('port specified is invalid',alertMessage,'Alert Message Mismatch Error')

    #def testInvalidPortDisconnectPort(self):
    #    in_prt = self.ingress_ports_list[5]
    #    e_prt = self.egress_ports_list[2]
    #    invalid_e_prt = 1000
    #    try:
    #        self.cr_conn.clear_connections(self.box,ingress_port=in_prt,egress_port=e_prt)
    #    except Exception as err:
    #        print "Clear CrossConnect Error:", err

    #    try:
    #        self.cr_conn.enable_connections(self.box, ingress_port=in_prt,egress_port=e_prt)
    #    except Exception as err:
    #        print "Enable CrossConnect Error:", err 
    #    
    #    try:
    #        alertMessage = self.cr_conn.disable_connections(self.box, ingress_port=in_prt, egress_port = e_prt, InvalidCase = 'yes')
    #    except Exception as err:
    #        print "Disable CrossConnect Error:", err
    #    
    #    nose.tools.assert_in('port specified is invalid',alertMessage,'Alert Message Mismatch Error')        

    #def testInvalidNegativePortDisconnectPort(self):
    #    in_prt = self.ingress_ports_list[5]
    #    e_prt = self.egress_ports_list[5]
    #    invalid_e_prt = -20
    #    try:
    #        self.cr_conn.clear_connections(self.box,ingress_port=in_prt,egress_port=e_prt)
    #    except Exception as err:
    #        print "Clear CrossConnect Error:", err

    #    try:
    #        self.cr_conn.enable_connections(self.box, ingress_port=in_prt,egress_port=e_prt)
    #    except Exception as err:
    #        print "Enable CrossConnect Error:", err 
    #    
    #    try:
    #        alertMessage = self.cr_conn.disable_connections(self.box, ingress_port=in_prt, egress_port = e_prt, InvalidCase = 'yes')
    #    except Exception as err:
    #        print "Disable CrossConnect Error:", err
    #    
    #    nose.tools.assert_in('port specified is invalid',alertMessage,'Alert Message Mismatch Error')

    #def testInvalidEntryDisconnectPort(self):
    #    in_prt = self.ingress_ports_list[5]
    #    e_prt = self.egress_ports_list[7]
    #    invalid_e_prt = 'Label2'
    #    try:
    #        self.cr_conn.clear_connections(self.box,ingress_port=in_prt,egress_port=e_prt)
    #    except Exception as err:
    #        print "Clear CrossConnect Error:", err

    #    try:
    #        self.cr_conn.enable_connections(self.box, ingress_port=in_prt,egress_port=e_prt)
    #    except Exception as err:
    #        print "Enable CrossConnect Error:", err 

    #    try:
    #        alertMessage = self.cr_conn.disable_connections(self.box, ingress_port=in_prt, egress_port = e_prt, InvalidCase = 'yes')
    #        print "alertMessage : ",  alertMessage
    #    except Exception as err:
    #        print "Disable CrossConnect Error:", err
    #    alertMessage1 = 'Port %s is already in use. Continue?' % self.ingress_ports_list[5]
    #    print "alertMessage1 : ", alertMessage1
    #    
    #    #nose.tools.assert_in('port specified is invalid',alertMessage,'Alert Message Mismatch Error')
    #    nose.tools.assert_in(alertMessage1,alertMessage,'Alert Message Mismatch Error')

    def testDoubleClickPortConnection(self):
        in_prt = self.ingress_ports_list[5]
        
        try:
            element = self.cr_conn.double_click(self.box,ingress_port=in_prt) 
        except Exception as err:
            print "Double Click on Port Popup box Error:", err

        nose.tools.assert_true(element.is_displayed(),'Set label popup box loading error')                 

    def testDoubleClickPortLabel(self):
        in_prt = self.ingress_ports_list[5]
        try:
            element = self.cr_conn.double_click(self.box,ingress_label=in_prt)
        except Exception as err:
            print "Double Click on label Popup box Error:", err 

        nose.tools.assert_true(element.is_displayed(),'Set label popup box loading error') 


class testConnectionMap():


    ports = Config.get("switch_info", "Ports")
    ingress_ports_list = []
    egress_ports_list = []
    for ingress_ports in range(1, int(ports)+1):
        ingress_ports_list.append(ingress_ports)
    for egress_ports in range(int(ports)+1, int(ports+ports)+1):
        egress_ports_list.append(egress_ports) 


    @classmethod
    def setUpClass(cls):
        cls.cr_conn = CrossConnects()
        cls.cr_port = PortStatus()
        cls.box = Node(box_ip)

    def testCrossConnectPage(self):

        try:
            element = self.cr_conn.enable_connectionsmap(self.box,'cross_connect_page')
        except Exception as err:
            print "Navigate to connection map Error:", err

        nose.tools.assert_true(element,'Cross Connect Page Loading Error')

    def testSetLabelButton(self):

        try:
            element = self.cr_conn.enable_connectionsmap(self.box,'Set_label_button')
        except Exception as err:
            print "navigate to connection map or set label error:",err

        nose.tools.assert_true(element,'Set label popup box loading error')

    def testSetPortLabelMap(self):
        prt_id = self.ingress_ports_list[5]
        prt_label = 'PolatisMap'

        try:
            self.cr_conn.setlabel_map(self.box,port_id = prt_id,port_label = prt_label)
        except Exception as err:
            print "set port label Map Error:", err

        try:
            fetched_label = self.cr_conn.fetchlabel_map(self.box,port = prt_id)
            label_fetched = str(fetched_label)
        except Exception as err:
            print "Fetch port label Map Error:", err

        nose.tools.assert_equal(prt_label,label_fetched,'Label not set for Error')

    def testCancelSetPortLabelMap(self):
        prt_id = self.ingress_ports_list[3]
        prt_label = 'PolatisMap12'

        try:
            fetched_label1 = self.cr_conn.fetchlabel_map(self.box,port = prt_id)
            label_fetched1 = str(fetched_label1)
        except Exception as err:
            print "Fetch port label Map Error:", err        

        try:
            self.cr_conn.setlabel_map(self.box,port_id = prt_id,port_label = prt_label, Cancel = 'yes')
        except Exception as err:
            print "set port label Map Error:", err

        try:
            fetched_label2 = self.cr_conn.fetchlabel_map(self.box,port = prt_id)
            label_fetched2 = str(fetched_label2)
        except Exception as err:
            print "Fetch port label Map Error:", err        

        nose.tools.assert_equal(label_fetched1,label_fetched2,'Port label not same after the cancel operation')

    def testSetMaxCharPortLabelMap(self):
        prt_id = self.egress_ports_list[5]
        prt_label = 'wwwwwwwwwwwwwwwwwwww'

        try:
            self.cr_conn.setlabel_map(self.box,port_id = prt_id,port_label = prt_label)
        except Exception as err:
            print "Set Port label Map Error:", err

        try:
            fetched_label = self.cr_conn.fetchlabel_map(self.box,port = prt_id)
            label_fetched = str(fetched_label)
        except Exception as err:
            print "Fetch port label Map Error:", err

        nose.tools.assert_equal(prt_label,label_fetched,'MaxChar Label not set for Error')

    def testSetInvalidPortLabelMap(self):
        prt_id = self.ingress_ports_list[5]
        prt_label = 'port12#'

        try:
            alertMessage = self.cr_conn.setlabel_map(self.box,port_id = prt_id,port_label = prt_label,InvalidCase = 'yes')
        except Exception as err:
            print "Set Port Label Error or Alert handling Error:", err

        nose.tools.assert_in("Invalid port label!",alertMessage,'Alert Message Mismatch Error')

    def testSetInvalidMaxCharPortLabelMap(self):
        prt_id = self.ingress_ports_list[5]
        prt_label = "abcdefghijklmnopqrstuv"

        try:
            alertMessage = self.cr_conn.setlabel_map(self.box,port_id = prt_id,port_label = prt_label,InvalidCase = 'yes')
        except Exception as err:
            print "Set Port Label Error or Alert handling Error:", err

        nose.tools.assert_in("Names can be a maximum of 20 characters in length",alertMessage,'Alert Message Mismatch Error')

    def testRemovePortLabelMap(self):
        prt_id = self.ingress_ports_list[5]
        prt_label = 'testPolatisMap'

        try:
            self.cr_conn.setlabel_map(self.box,port_id = prt_id,port_label = prt_label)
        except Exception as err:
            print "Set port label Map Error:", err        

        try:
            self.cr_conn.removelabel_map(self.box,port_id = prt_id)
        except Exception as err:
            print "remove port label Map Error:", err

        try:
            fetched_label = self.cr_conn.fetchlabel_map(self.box,port = prt_id)
            label_fetched = len(fetched_label)
        except Exception as err:
            print "Fetch port label Map Error:", err

        nose.tools.assert_equal(0,label_fetched,'Remove port label Error')

    def testUpdatePortLabelMap(self):
        prt_id = self.egress_ports_list[5]
        prt_label = 'PolatisMap'
        update_prt_label = 'testPolatisMap'
        
        try:
            self.cr_conn.setlabel_map(self.box,port_id = prt_id,port_label = prt_label)
        except Exception as err:
            print "set port label Map Error:", err        

        try:
            self.cr_conn.setlabel_map(self.box,port_id = prt_id,port_label = update_prt_label)
        except Exception as err:
            print "set port label Map Error:", err

        try:
            fetched_label = self.cr_conn.fetchlabel_map(self.box,port = prt_id)
            label_fetched = str(fetched_label)
        except Exception as err:
            print "Fetch port label Map Error:", err

        nose.tools.assert_equal(update_prt_label,label_fetched,'Label not updated for Error')

    def testEnablePortMapping(self):
        in_prt = self.ingress_ports_list[5]
        e_prt = self.egress_ports_list[5]

        try:
            self.cr_conn.clear_connections(self.box, ingress_port=in_prt, egress_port=e_prt)
        except Exception as err:
            print "Clear Connections Error:", err

        try:
            self.cr_conn.enable_connectionsmap(self.box,ingress_port = in_prt ,egress_port = e_prt)
        except Exception as err:
            print "Enable port Map Error:", err

        try:
            fetched_port = self.cr_conn.fetch_connections(self.box,port = in_prt)
            port_fetched = int(fetched_port)
        except Exception as err:
            print "Fetch port Map Error:", err

        nose.tools.assert_equal(e_prt,port_fetched,'Port Mapping is not enabled between the ports')

    def testRemovePortMap(self):
        in_prt = self.ingress_ports_list[5]
        e_prt = self.egress_ports_list[7]

        try:
            self.cr_conn.clear_connections(self.box, ingress_port=in_prt, egress_port=e_prt)
        except Exception as err:
            print "Clear Connections Error:", err

        try:
            self.cr_conn.enable_connectionsmap(self.box,ingress_port = in_prt ,egress_port = e_prt)
        except Exception as err:
            print "Enable port Map Error:", err

        try:
            self.cr_conn.disable_connectionsmap(self.box,ingress_port = in_prt ,egress_port = e_prt)
        except Exception as err:
            print "Enable port Map Error:", err

        try:
            fetched_port = self.cr_conn.fetch_connections(self.box,port = in_prt)
            port_fetched = len(fetched_port)
        except Exception as err:
            print "Fetch port Map Error:", err

        nose.tools.assert_equal(0,port_fetched,'Port Mapping is not removed between the ports')

    def testUpdatePortMap(self):
        in_prt = self.ingress_ports_list[5]
        e_prt = self.egress_ports_list[7]
        update_e_prt = self.egress_ports_list[4]

        try:
            self.cr_conn.clear_connections(self.box, ingress_port=in_prt, egress_port=e_prt)
        except Exception as err:
            print "Clear Connections Error:", err

        try:
            self.cr_conn.enable_connectionsmap(self.box,ingress_port = in_prt ,egress_port = e_prt)
        except Exception as err:
            print "Enable port Map Error:", err

        try:
            self.cr_conn.edit_connectionsmap(self.box,ingress_port = in_prt ,egress_port = update_e_prt)
        except Exception as err:
            print "Edit port Map Error:", err
        
        try:
            fetched_port = self.cr_conn.fetch_connections(self.box,port = in_prt)
            port_fetched = int(fetched_port)
        except Exception as err:
            print "Fetch port Map Error:", err        

        nose.tools.assert_equal(update_e_prt,port_fetched,'Port Mapping is not updated between the ports')

    def testCancelUpdatePortMap(self):
        in_prt = self.ingress_ports_list[5]
        e_prt = self.egress_ports_list[7]

        try:
            self.cr_conn.clear_connections(self.box, ingress_port=in_prt, egress_port=e_prt)
        except Exception as err:
            print "Clear Connections Error:", err

        try:
            self.cr_conn.enable_connectionsmap(self.box,ingress_port = in_prt ,egress_port = e_prt)
        except Exception as err:
            print "Enable port Map Error:", err

        try:
            fetched_port1 = self.cr_conn.fetch_connections(self.box,port = in_prt)
            port_fetched1 = int(fetched_port1)
        except Exception as err:
            print "Fetch port Map Error:", err
            
        try:
            self.cr_conn.edit_connectionsmap(self.box,ingress_port = in_prt ,egress_port = e_prt,Cancel = 'yes')
        except Exception as err:
            print "Edit Port map Error:", err

        try:
            fetched_port2 = self.cr_conn.fetch_connections(self.box,port = in_prt)
            port_fetched2 = int(fetched_port2)
        except Exception as err:
            print "Fetch port Map Error:", err

        nose.tools.assert_equal(port_fetched1,port_fetched2,'Port value changed after the cancel Update operation')

    def testCancelDisconnectPort(self):
        in_prt = self.ingress_ports_list[5]
        e_prt = self.egress_ports_list[5]

        try:
            self.cr_conn.clear_connections(self.box, ingress_port=in_prt, egress_port=e_prt)
        except Exception as err:
            print "Clear Connections Error:", err
        try:
            self.cr_conn.enable_connectionsmap(self.box,ingress_port = in_prt ,egress_port = e_prt)
        except Exception as err:
            print "Enable port Map Error:", err

        try:
            fetched_port1 = self.cr_conn.fetch_connections(self.box,port = in_prt)
            port_fetched1 = int(fetched_port1)
        except Exception as err:
            print "Fetch port Map Error:", err        

        try:
            self.cr_conn.disable_connectionsmap(self.box,ingress_port = in_prt ,egress_port = e_prt, Cancel = 'yes')
        except Exception as err:
            print "Disconnect Port map error:", err

        try:
            fetched_port2 = self.cr_conn.fetch_connections(self.box,port = in_prt)
            port_fetched2 = int(fetched_port2)
        except Exception as err:
            print "Fetch port Map Error:", err

        nose.tools.assert_equal(port_fetched1,port_fetched2,'Port value changed after the cancel Disconnect operation')



class testSystemConfig():

    @classmethod
    def setUpClass(cls):
        cls.box = Node(box_ip)
        cls.cr_user = UserConfig()
        cls.cr_system = SystemConfig()

    """SYSTEM CONFIG"""


    def testSystemConfigPage(self):

        try:
            display = self.cr_system.updateSysConfPage(self.box,'SystemConfigPage')
        except Exception as err:
            print "Navigate to System Config Page Error:", err

        nose.tools.assert_true(display,'System Config Page Loading Error')

    def testEditValidSwitchName(self):
        switchName ='NewPolatis123'

        try:
            self.cr_system.updateSysConfPage(self.box,switch_name = switchName)
        except Exception as err:
            print "UpdateSwitchNameError:", err

        try:
            sysDict = self.cr_system.fetchSysConfDetails(self.box)
        except Exception as err:
            print "Fetch Switch Name Error:", err
        

        nose.tools.assert_equal(switchName,sysDict['Switch_Name'],'Switch Name not Updated')

    def testEditEmptySwitchName(self):
        switchName = ''

        try:
            self.cr_system.updateSysConfPage(self.box,switch_name = switchName)
        except Exception as err:
            print "UpdateSwitchNameError:", err

        try:
            sysDict = self.cr_system.fetchSysConfDetails(self.box)
        except Exception as err:
            print "Fetch Switch Name Error:", err
            
        nose.tools.assert_equal(0,len(sysDict['Switch_Name']),'Switch Name not Updated')

    def testEditInvalidCharSwitchName(self):
        switchName ='Polatis@123'

        try:
            alertMessage = self.cr_system.updateSysConfPage(self.box,'InvalidCase',switch_name = switchName)
        except Exception as err:
            print "UpdateSwitchNameError:", err

        nose.tools.assert_in("Invalid switch name",alertMessage,'Invalid switch name Message Mismatch Error')

    def testEditMaxCharSwitchName(self):
        switchName ='Polatis123456789Polatis'

        try:
            alertMessage = self.cr_system.updateSysConfPage(self.box,'InvalidCase',switch_name = switchName)
        except Exception as err:
            print "UpdateSwitchNameError:", err

        nose.tools.assert_in("Names can be a maximum of 20 characters in length",alertMessage,'Invalid switch name Message Mismatch Error')

    def testUserSessionTimeout(self):
        usrnme = 'testUser'
        passwrd = 'user'
        usrtype = 'user'
        timeout = 1
        
        try:
            self.cr_user.create_user(self.box,new_username = usrnme, new_userpasswd = passwrd, new_usertype = usrtype)
        except Exception as err:
            print "Create User Error:", err

        try:
            self.cr_system.updateSysConfPage(self.box,'User',time_out = timeout)
        except Exception as err:
            print "Update User Session Error:", err

        try:
            element = self.cr_system.waitForSessionToTimeout(self.box,'user_session', usrname = usrnme, pswrd = passwrd, sleep_time = timeout)
        except Exception as err:
            print "Wait For Timeout Error:", err

        nose.tools.assert_true(element,'Page does not Logout after TimeOut')

    def testAdminSessionTimeOut(self):
        timeout = 1

        try:
            self.cr_system.updateSysConfPage(self.box,'Admin',time_out = timeout)
        except Exception as err:
            print "Update User Session Error:", err

        try:
            element = self.cr_system.waitForSessionToTimeout(self.box, sleep_time = timeout)
        except Exception as err:
            print "Wait For Timeout Error:", err
        
        nose.tools.assert_true(element,'Page does not Logout after TimeOut')

    def testDisableSessionTimeout(self):
        timeout = 1
        disable_timeout = 0

        try:
            self.cr_system.updateSysConfPage(self.box,'Admin',time_out = timeout)
        except Exception as err:
            print "Update User Session Error:", err

        try:
            self.cr_system.updateSysConfPage(self.box,'Admin',time_out = disable_timeout)
        except Exception as err:
            print "Update User Session Error:", err

        try:
            element = self.cr_system.waitForSessionToTimeout(self.box, sleep_time = timeout)
        except Exception as err:
            print "Wait For Timeout Error:", err

        nose.tools.assert_false(element,'Page does not Logout after TimeOut')

    def testInvalidSessionTimeoutEntry(self):
        timeout = 1000

        try:
            alertMessage = self.cr_system.updateSysConfPage(self.box,'User','InvalidCase',time_out = timeout)
        except Exception as err:
            print "Update User Session Error:", err        

        nose.tools.assert_in("Valid numbers are from 0 to 60",alertMessage,'Invalid switch name Message Mismatch Error')


    def testEmptySessionTimeout(self):
        timeout = ""
        
        try:
            alertMessage = self.cr_system.updateSysConfPage(self.box,'User','InvalidCase',time_out = timeout)
        except Exception as err:
            print "Update User Session Error:", err

        try:
            sysDict = self.cr_system.fetchSysConfDetails(self.box)
        except Exception as err:
            print "Fetch TimeOut Error:", err
        
        nose.tools.assert_in("Default user timeout will be set",alertMessage,'Wrong Notification Message for Empty session timeout value')
        nose.tools.assert_equal(0,int(sysDict['Session_TimeOut']),'TimeOut value not set to 0')


    #def testWebPageRefreshPeriod(self):
    #    refreshTimeout = 7
    #    
    #    try:
    #        self.cr_system.updateSysConfPage(self.box,refresh_time = refreshTimeout)
    #    except Exception as err:
    #        print "Update Web page Refresh Error:", err

    #    try:
    #        result = self.cr_system.checkWebPageRefreshTime(self.box,refresh_time = refreshTimeout)
    #        print "result : " , result
    #    except Exception as err:
    #        print "Check Web Page Refresh Time Error:", err
    #        
    #    #nose.tools.assert_in('Element is no longer attached to the DOM',result,'The Page does not Refresh')
    #    nose.tools.assert_in('True',result,'The Page does not Refresh')

    def testInvalidCharWebPageRefreshPeriod(self):
        refreshTimeout = 'a'

        try:
            alertMessage = self.cr_system.updateSysConfPage(self.box,'InvalidCase', refresh_time = refreshTimeout)
        except Exception as err:
            print "Update Web page Refresh Error:", err        

        
        nose.tools.assert_in("Invalid refresh time",alertMessage,'Wrong Error Message For Invalid Refresh time')

    def testInvalidWebPageRefreshPeriodCount(self):
        refreshTimeout = 0

        try:
            alertMessage = self.cr_system.updateSysConfPage(self.box,'InvalidCase', refresh_time = refreshTimeout)
        except Exception as err:
            print "Update Web page Refresh Error:", err        

        
        nose.tools.assert_in("Valid numbers are from 3 to 300",alertMessage,'Wrong Error Message For Zero as Refresh time')

    def testEmptyWebPageRefreshPeriod(self):
        refreshTimeout = ""
        
        try:
            alertMessage = self.cr_system.updateSysConfPage(self.box,'InvalidCase',refresh_time = refreshTimeout)
        except Exception as err:
            print "Update Web page Refresh Error:", err

        try:
            sysDict = self.cr_system.fetchSysConfDetails(self.box)
        except Exception as err:
            print "Fetch Refresh Time Error:", err

        nose.tools.assert_in("Default refresh time will be set",alertMessage,'Wrong alert Message for Empty Refresh period time')
        nose.tools.assert_equal(10,int(sysDict['Refresh_Time']),'Default refresh Time is not set')

    def testSetSystemDateTime(self):
        date = "26/10/2015"
        time = "05:20"

        try:
            self.cr_system.updateSysConfPage(self.box,'SysDateTime',sys_date= date, sys_time= time)
        except Exception as err:
            print "Update System Date and time error:", err

        try:
            sysDict = self.cr_system.fetchSysConfDetails(self.box)
            print 'sysDict : -----------', sysDict
        except Exception as err:
            print "Check System Date Error:", err

        nose.tools.assert_equal(sysDict['Date'],date,'System Date is not Set')
        nose.tools.assert_greater_equal(sysDict['Time'],time,'System Time is not set')

    def testSystemDateTimeInvalidDate(self):
        date = "40/10/2015"

        try:
            alertMessage = self.cr_system.updateSysConfPage(self.box,'SysDateTime','InvalidCase',sys_date= date)
        except Exception as err:
            print "Update System Date and time error:", err

        nose.tools.assert_in("Day (first place) must be 1 - 31",alertMessage,'Wrong Error Message For Invalid date')

    def testSystemDateTimeMaxCharInvalidDate(self):
        date = "400/10/2015"

        try:
            alertMessage = self.cr_system.updateSysConfPage(self.box,'SysDateTime','InvalidCase',sys_date= date)
        except Exception as err:
            print "Update System Date and time error:", err

        nose.tools.assert_in("Invalid date",alertMessage,'Wrong Error Message For Invalid date')

    def testSystemDateTimeInvalidMonth(self):
        date = "10/13/2015"

        try:
            alertMessage = self.cr_system.updateSysConfPage(self.box,'SysDateTime','InvalidCase',sys_date= date)
        except Exception as err:
            print "Update System Date and time error:", err

        nose.tools.assert_in("Month (middle place) must be 1 - 12",alertMessage,'Wrong Error Message For Invalid month in date')

    def testSystemDateTimeMaxCharInvalidMonth(self):
        date = "10/012/2015"

        try:
            alertMessage = self.cr_system.updateSysConfPage(self.box,'SysDateTime','InvalidCase',sys_date= date)
        except Exception as err:
            print "Update System Date and time error:", err

        nose.tools.assert_in("Invalid date",alertMessage,'Wrong Error Message For Invalid month in date')

    def testSystemDateTimeInvalidYear(self):
        date = "10/12/2222"

        try:
            alertMessage = self.cr_system.updateSysConfPage(self.box,'SysDateTime','InvalidCase',sys_date= date)
        except Exception as err:
            print "Update System Date and time error:", err

        nose.tools.assert_in("Year (last place) must be before 2100",alertMessage,'Wrong Error Message For Invalid year in date')

    def testSystemDateTimeMaxCharInvalidYear(self):
        date = "10/12/20145"

        try:
            alertMessage = self.cr_system.updateSysConfPage(self.box,'SysDateTime','InvalidCase',sys_date= date)
        except Exception as err:
            print "Update System Date and time error:", err

        nose.tools.assert_in("Invalid date",alertMessage,'Wrong Error Message For Invalid year in date')

    def testSystemDateTimeInvalidHour(self):
        time = "90:10"

        try:
            alertMessage = self.cr_system.updateSysConfPage(self.box,'SysDateTime','InvalidCase',sys_time= time)
        except Exception as err:
            print "Update System Date and time error:", err

        nose.tools.assert_in("Hour (first place) must be 0 - 23",alertMessage,'Wrong Error Message For Invalid Hour in time')

    def testSystemDateTimeInvalidMinute(self):
        time = "10:80"

        try:
            alertMessage = self.cr_system.updateSysConfPage(self.box,'SysDateTime','InvalidCase',sys_time= time)
        except Exception as err:
            print "Update System Date and time error:", err

        nose.tools.assert_in("Minute (first place) must be 0 - 59",alertMessage,'Wrong Error Message For Invalid Minute in time')   

    #def testResetNetworkCard(self):

    #    try:
    #        result = self.cr_system.resetNetworkCard(self.box)
    #    except Exception as err:
    #        print "Reset Network card error:", err

    #    nose.tools.assert_true(result,'Reset Network card Error')
        
    #def testCancelResetNetworkCard(self):

    #    try:
    #        result = self.cr_system.resetNetworkCard(self.box, Cancel = 'yes')
    #    except Exception as err:
    #        print "Reset Network card error:", err

    #    nose.tools.assert_false(result,'Cancel Reset Network card Error')

 

if 0:

    class Test_Aps():
    
    
        @classmethod
        def setUpClass(cls):
            cls.box = Node(box_ip)
            cls.pt_aps_config = ApsConfig()
    
    
        def testAddProtection(self):
    
            try:
                result = self.pt_aps_config.add_protection(self.box, working_port = '8', protecting_port = '16',  reversion_delay = '3')
    
                print "result : ", result
            except Exception as err:
                print "Add working port error: ", err
    
            nose.tools.assert_is_none(result, 'FFP already exists in working port')
    
        
        def testFetchProtection(self):
    
            try:
                result = self.pt_aps_config.fetch_protection(self.box, working_port = '8')
                print "result : ", result
            except Exception as err:
                print "fetch protection error : ", err
        
        def testUpdateProtection(self):
    
            try:
                result = self.pt_aps_config.update_protection(self.box,
                    working_port = '8', protecting_port = '15', reversion_delay = '3')
                print "result : ", result
            except Exception as err:
                print "update protection error : ", err
        
        def testDeleteProtection(self):
    
            try:
                result = self.pt_aps_config.delete_protection(self.box, working_port = '8')
                print "result : ", result
            except Exception as err:
                print "delete protection error: ", err
        
        def testConfigureGlobalSettings(self):
    
            try:
                result = self.pt_aps_config.configure_global_settings(self.box, working_port = '8', protecting_port = '16', service_lockout = 'disable', do_not_revert = 'disable', reversion_delay = '3')
                print "result : ", result
            except Exception as err:
                print "configure global settings error : ", err
        
        def testSwitchToPortAction(self):
    
            try:
                result = self.pt_aps_config.switch_to_port_action(self.box, working_port = '8', switch_action = 'switch_to_protecting_port')
                print "result : ", result
            except Exception as err:
                print "configure global settings error : ", err










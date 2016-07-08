""" Python file that covers tabs under the "System Config" Menu.
"""

import time
import logging
LOG = logging.getLogger(__name__)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from configAttr import defaultAttr


class SystemConfig:
    """ Class that will Configure System Config Page.
    """
#    def __init__(self):
#        """
#        Initialize the default attributes
#        """

    sysConfAttr = defaultAttr()
    
    def navigate_to_system_config_page(self, sel):
        """
        Navigates to the System Config page.
        """
        # click on 'System Config' Page.
        WebDriverWait(sel, 60).until(EC.visibility_of_element_located((By.XPATH,getattr(self.sysConfAttr, 'system_config_page'))))
        sel.find_element_by_xpath(getattr(self.sysConfAttr, 'system_config_page')).click()
        WebDriverWait(sel,60).until(EC.visibility_of_element_located((By.XPATH,getattr(self.sysConfAttr, 'sys_page_visibility'))))
        time.sleep(3)
            
    def fetchSysConfDetails(self,node):
        """
        Fetch Web Page Refresh Time,Session Timeout, Sys Date&Time and Switch Name under the System Config Page   
        """
        LOG.info("Enables Connections...")
        LOG.info("Navigate to the System Config Page")
        sel = node.gui_login()
        time.sleep(5)
        self.navigate_to_system_config_page(sel)
        sysDict = {}
        refresh = sel.find_element_by_css_selector(getattr(self.sysConfAttr, 'refresh_time_period')).get_attribute('value') 
        timeout = sel.find_element_by_css_selector(getattr(self.sysConfAttr, 'user_session_timeout')).get_attribute('value')
        try:
            swName  = sel.find_element_by_css_selector(getattr(self.sysConfAttr, 'get_switch_name')).text
        except:
            swName = sel.find_element_by_css_selector(getattr(self.sysConfAttr, 'switch_name')).get_attribute('value')
        sysDate = sel.find_element_by_css_selector(getattr(self.sysConfAttr, 'set_sys_date')).get_attribute('value')
        sysTime = sel.find_element_by_css_selector(getattr(self.sysConfAttr, 'set_sys_time')).get_attribute('value')
        #syslogAddress = sel.find_element_by_css_selector(self.oxcDict['syslog_address']).get_attribute('value')
        #syslogFacililty = sel.find_element_by_css_selector(self.oxcDict['syslog_facility']).get_attribute('value')
    
        sysDict['Refresh_Time'] = refresh
        sysDict['Session_TimeOut'] = timeout
        sysDict['Switch_Name'] = str(swName)
        sysDict['Date'] = str(sysDate)
        sysDict['Time'] = sysTime
        #sysDict['syslog_address'] = str(syslogAddress)
        #sysDict['syslog_facility'] = str(syslogFacililty)
        print "sysDict : ", sysDict
        return sysDict

    def updateSysConfPage(self,node,*args,**kwargs):
        """
        Update System Date and Time,Refresh Time,Session TimeOut and Name.
        """        
        LOG.info("Enables Connections...")
        LOG.info("Navigate to the System Config Page")
        sel = node.gui_login()
        time.sleep(5)
        self.navigate_to_system_config_page(sel)
        if 'SystemConfigPage' in args:
            element = sel.find_element_by_css_selector(getattr(self.sysConfAttr, 'sys_config_page')).is_displayed()
            return element
        if 'switch_name' in kwargs.keys():       
            element = sel.find_element_by_css_selector(getattr(self.sysConfAttr, 'system_switch_name'))
            element.clear()
            element.send_keys(kwargs['switch_name'])
            sel.find_element_by_xpath(getattr(self.sysConfAttr, 'system_switch_button')).click()
        if 'time_out' in kwargs.keys():
            if 'User' in args: 
                element = sel.find_element_by_css_selector(getattr(self.sysConfAttr, 'user_session_timeout'))
                element.clear()
                element.send_keys(kwargs['time_out'])        
                sel.find_element_by_xpath(getattr(self.sysConfAttr, 'session_timeout_button')).click()
            elif 'Admin' in args:
                element = sel.find_element_by_css_selector(getattr(self.sysConfAttr, 'admin_session_timeout'))
                element.clear()
                element.send_keys(kwargs['time_out'])        
                sel.find_element_by_xpath(getattr(self.sysConfAttr, 'session_timeout_button')).click()
            else:
                return "Invalid Argument for session timeout.use either 'User' or 'Admin'."
        if 'refresh_time' in kwargs.keys():
            element = sel.find_element_by_css_selector(getattr(self.sysConfAttr, 'refresh_time_period'))
            element.clear()
            element.send_keys(kwargs['refresh_time'])
            sel.find_element_by_xpath(getattr(self.sysConfAttr, 'refresh_timeout_button')).click()
        if 'SysDateTime' in args:
            if 'sys_date' in kwargs.keys():
                sel.find_element_by_css_selector(getattr(self.sysConfAttr, 'set_sys_date')).clear()
                sel.find_element_by_css_selector(getattr(self.sysConfAttr, 'set_sys_date')).send_keys(kwargs['sys_date'])
            if 'sys_time' in kwargs.keys():
                sel.find_element_by_css_selector(getattr(self.sysConfAttr, 'set_sys_time')).clear()
                sel.find_element_by_css_selector(getattr(self.sysConfAttr, 'set_sys_time')).send_keys(kwargs['sys_time'])       
            sel.find_element_by_xpath(getattr(self.sysConfAttr, 'sys_date_time_button')).click()
        if 'remoteSyslog' in args:
            if 'address' in kwargs.keys():
                sel.find_element_by_css_selector(getattr(self.sysConfAttr, 'syslog_address')).clear()
                sel.find_element_by_css_selector(getattr(self.sysConfAttr, 'syslog_address')).send_keys(kwargs['address'])
            if 'facility' in kwargs.keys():
                sel.find_element_by_css_selector(getattr(self.sysConfAttr, 'syslog_facility')).clear()
                sel.find_element_by_css_selector(getattr(self.sysConfAttr, 'syslog_facility')).send_keys(kwargs['address'])
            sel.find_element_by_xpath(getattr(self.sysConfAttr, 'remote_syslog_button')).click()
        if 'InvalidCase' in args:
            alert = sel.switch_to_alert()
            alertText = alert.text
            alert.accept()
            sel.switch_to_default_content()
            return alertText
        WebDriverWait(sel,30).until(EC.visibility_of_element_located((By.XPATH,getattr(self.sysConfAttr, 'operation_complete'))))
        sel.find_element_by_css_selector(getattr(self.sysConfAttr, 'operation_ok_button')).click()

    def resetNetworkCard(self,node,**kwargs):
        """
        Reset the network card
        """
        LOG.info("Enables Connections...")
        LOG.info("Navigate to the System Config Page")
        sel = node.gui_login()
        time.sleep(5)
        self.navigate_to_system_config_page(sel)        
        time.sleep(2)        
        sel.find_element_by_xpath(getattr(self.sysConfAttr, 'reset_network_card')).click()
        time.sleep(10)
        if 'Cancel' in kwargs.keys():           
            sel.find_element_by_css_selector(getattr(self.sysConfAttr, 'cancel_reset_button')).click()
            element = sel.find_element_by_id('polalert').is_displayed()
            return element
        sel.find_element_by_css_selector(getattr(self.sysConfAttr, 'reset_network_button')).click()
        try:
            WebDriverWait(sel,45).until(EC.visibility_of_element_located((By.XPATH,getattr(self.sysConfAttr, 'network_card_reset'))))
            element = sel.find_element_by_id('polalert').is_displayed()
            sel.find_element_by_css_selector(getattr(self.sysConfAttr, 'reset_network_ok_button')).click()
            return element
            sel.close()
            sel = node.gui_login_page()
            time.sleep(10)
        except Exception as err:
            print "No alert Raised:", err
            sel.close()
            sel = node.gui_login_page()
            time.sleep(10)

    def checkWebPageRefreshTime(self, node, **kwargs ):
        """Check Web Page Refresh TimeOut"""
        LOG.info("Enables Connections...")
        LOG.info("Navigate to the Power Levels Page")
        sel = node.gui_login()
        #WebDriverWait(sel,30).until(EC.visibility_of_element_located((By.XPATH,getattr(self.sysConfAttr, 'power_levels_page'))))        
        WebDriverWait(sel,30).until(EC.visibility_of_element_located((By.XPATH,getattr(self.sysConfAttr, 'cross_connects_page'))))        
        #sel.find_element_by_xpath(getattr(self.sysConfAttr, 'power_levels_page')).click()
        sel.find_element_by_xpath(getattr(self.sysConfAttr, 'cross_connects_page')).click()
        #WebDriverWait(sel,30).until(EC.visibility_of_element_located((By.XPATH,getattr(self.sysConfAttr, 'power_page_visibility'))))
        WebDriverWait(sel,30).until(EC.visibility_of_element_located((By.CSS_SELECTOR,getattr(self.sysConfAttr, 'conn_tbl'))))
        #element = sel.find_element_by_xpath(getattr(self.sysConfAttr, 'powerlevel_element'))
        element = sel.find_element_by_css_selector(getattr(self.sysConfAttr, 'setport_label_map'))
        print "element : ", element
        refreshTime = 0
        ref_time = kwargs['refresh_time']
        timeout = int(ref_time)+10
        try:
            for x in range(0,timeout):
                print "inside loop"
                time.sleep(1)
                msg = element.is_displayed()
                refreshTime+=1
            #msg = element.is_displayed()
            #print "try msg : ", msg
            return msg
        except Exception as e:
            msg = str(e)
            print "except msg: ", msg
            return msg

    def waitForSessionToTimeout(self, node, *args, **kwargs):
        """Wait For Session"""
        LOG.info("Enables Connections...")
        LOG.info("Navigate to the System Config Page")
        if 'usrname' in kwargs.keys():
            sel = node.gui_login_page(UserName = kwargs['usrname'],  Password = kwargs['pswrd'])
        else:
            sel = node.gui_login()
        time.sleep(5)
        if 'user_session' in args:
            pass
        else:
            self.navigate_to_system_config_page(sel)
        time.sleep(2)
        time1 = kwargs['sleep_time']
        t_out =(int(time1)*60)+15
        time.sleep(int(t_out))
        sel.find_element_by_xpath(getattr(self.sysConfAttr, 'Status_page')).click()
        try:
            WebDriverWait(sel,30).until(EC.visibility_of_element_located((By.XPATH,getattr(self.sysConfAttr, 'login_page_visibility'))))
        except:
            return False
        element = sel.find_element_by_css_selector(getattr(self.sysConfAttr, 'login_page')).is_displayed()
        sel.close()
        sel = node.gui_login_page()
        time.sleep(10)       
        return element     

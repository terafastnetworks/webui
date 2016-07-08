"""
Python file that covers tabs under the "Status" Menu.
"""

import time
import logging
LOG = logging.getLogger(__name__)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from configAttr import defaultAttr

class StatusConfig:
    """
    Class that will Configure Status Page.
    

    oxcDict = {
        'Status_page'            : '//a[text()="Status"]',
        'ports_view'             : "//td/input[@onclick=\"window.location.href='/cgi-bin/eventlog?type=ports'\"]",
        'environmental_view'     : "//td/input[@onclick=\"window.location.href='/cgi-bin/eventlog?type=env'\"]",
        'power_supply_view'      : "//td/input[@onclick=\"window.location.href='/cgi-bin/eventlog?type=psu'\"]",
        'opm_view'               : "//td/input[@onclick=\"window.location.href='/cgi-bin/eventlog?type=opm'\"]",
        'system_view'            : "//td/input[@onclick=\"window.location.href='/cgi-bin/eventlog?type=sys'\"]",
        'ports_event'            : '[id =portscanvas]',
        'environmental_event'    : '[id=envcanvas]',
        'power_supply_event'     : '[id=psucanvas]',
        'opm_event'              : '[id=opmcanvas]',
        'system_event'           : '[id=syscanvas]',
        'status_page_visibility' : '//b[contains(text(),"Environmental")]',
        'login_button'           : '[id=loginbutton]',
        'login_user'             : '[name=user]',
        'login_passwd'           : '[name=passwd]'
        }
    """

#    def __init__(self):
#        """ Initialize the default attributes
#        """

    sysStatusAttr = defaultAttr()

    def navigate_to_status_page(self, sel):
        """
        Navigates to the Status page.
        """
        
        # click on 'Status' Page.
        try:
            print "page not displayed"
            sel.find_element_by_xpath(getattr(self.sysStatusAttr, 'Status_page')).click()
            WebDriverWait(sel,60).until(EC.visibility_of_element_located((By.XPATH,getattr(self.sysStatusAttr, 'status_page_visibility'))))
        except:
            print "page log outed"
            sel.find_element_by_css_selector(getattr(self.sysStatusAttr, 'login_user')).send_keys('admin')
            sel.find_element_by_css_selector(getattr(self.sysStatusAttr, 'login_passwd')).send_keys('root')
            sel.find_element_by_css_selector(getattr(self.sysStatusAttr, 'login_button')).click()
            WebDriverWait(sel,60).until(EC.visibility_of_element_located((By.XPATH,getattr(self.sysStatusAttr, 'Status_page'))))
        time.sleep(2)

    def view_events_button(self,node,*args):
        """
        View buttons under the Status Page    
        """
        LOG.info("Enables Connections...")
        LOG.info("Navigate to the Status Page")
        sel = node.gui_login()
        time.sleep(5)
        self.navigate_to_status_page(sel)
        time.sleep(2)
        if 'status_page' in args:
            element = sel.find_element_by_xpath(getattr(self.sysStatusAttr, 'status_page_visibility')).is_displayed()
            return element
        elif 'environmental' in args:
            sel.find_element_by_xpath(getattr(self.sysStatusAttr, 'environmental_view')).click()
            WebDriverWait(sel,60).until(EC.visibility_of_element_located((By.CSS_SELECTOR,getattr(self.sysStatusAttr, 'environmental_event'))))
            value = sel.find_element_by_css_selector(getattr(self.sysStatusAttr, 'environmental_event')).is_displayed()
            return value
        elif 'powersupply' in args:
            sel.find_element_by_xpath(getattr(self.sysStatusAttr, 'power_supply_view')).click()
            WebDriverWait(sel,60).until(EC.visibility_of_element_located((By.CSS_SELECTOR,getattr(self.sysStatusAttr, 'power_supply_event'))))
            value = sel.find_element_by_css_selector(getattr(self.sysStatusAttr, 'power_supply_event')).is_displayed()
            return value
        elif 'opticalpowermonitor' in args:
            sel.find_element_by_xpath(getattr(self.sysStatusAttr, 'opm_view')).click()
            WebDriverWait(sel,60).until(EC.visibility_of_element_located((By.CSS_SELECTOR,getattr(self.sysStatusAttr, 'opm_event'))))
            value = sel.find_element_by_css_selector(self.oxcDict['opm_event']).is_displayed()
            return value
        elif 'ports' in args:
            sel.find_element_by_xpath(getattr(self.sysStatusAttr, 'ports_view')).click()
            WebDriverWait(sel,60).until(EC.visibility_of_element_located((By.CSS_SELECTOR,getattr(self.sysStatusAttr, 'ports_event'))))            
            value = sel.find_element_by_css_selector(getattr(self.sysStatusAttr, 'ports_event')).is_displayed()
            return value
        elif 'system' in args:
            sel.find_element_by_xpath(getattr(self.sysStatusAttr, 'system_view')).click()
            WebDriverWait(sel,60).until(EC.visibility_of_element_located((By.CSS_SELECTOR,getattr(self.sysStatusAttr, 'system_event'))))
            value = sel.find_element_by_css_selector(getattr(self.sysStatusAttr, 'system_event')).is_displayed()
            return value
        else:
            print "Wrong Keyword Argument passed, use one of these environmental, powersupply, opticalpowermonitor, ports, system"
            

""" Python file that covers tabs under the "Event Log" Page.
"""

import time
import logging
LOG = logging.getLogger(__name__)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from configAttr import defaultAttr

class EventLog:
    """ Class that will do operation on event log page.

    oxcDict = {
        'event_log_page' : '//a[text()="Event Log"]',
        'single_event' : '//div[@id="opmcanvas"]/table/tbody/tr/td/table/tbody/tr[2]/td[5]/input[@type="checkbox"]',
        'select_all_event' : '//button[text()="Select All Events"][@id="opm"]',
        'button_text' : '[id="opm"]',
        'deselect_all_event' : '//button[text()="Deselect All Events"][@id="opm"]',
        'delete_event' : '//button[text()="Delete Selected Events..."][@id="opm"]',
        'cancel_button' : '[id="modalCancelbutton"]',
        'delete_button' : '[id="modalDeletebutton"]',
        'clear_event' : '//button[text()="Clear Selected Events"][@id="opm"]',
        'check_box' : "//div[@id='opmcanvas']/table/tbody/tr/td/table/tbody/tr/td/input[@type='checkbox']",
        'event_state' : '//div[@id="opmcanvas"]/table/tbody/tr/td/table/tbody/tr[1]/following-sibling::tr',
        'event_id' : '//div[@id="opmcanvas"]/table/tbody/tr/td/table/tbody/tr/td[1]',
        'event_table' : '//div[@id="opmcanvas"]',
        'event_page' : '[class="content"]'
        }

    """
   
    eventLogAttr = defaultAttr()
 
    def eventLogAction(self,node,*args):
        LOG.info("Enables Connections...")
        LOG.info("Navigate to the APS Configuration Page")
        sel = node.gui_login()
        time.sleep(5)
        self.navigate_to_event_log_page(sel)
        time.sleep(2)
        if 'event_log_page' in args:
            element = sel.find_element_by_css_selector(getattr(self.eventLogAttr, 'event_page')).is_displayed()
            return element
        eventDict = {'Checked':True}
        if 'SelectEvent' in args:
            if 'singleEvent' in args:
                element = sel.find_element_by_xpath(getattr(self.eventLogAttr, 'single_event'))
                element.click()
                Id = element.get_attribute('id')
                print "Id : ", Id
                eventID = Id[10:]
                print "eventID : ", eventID
                eventDict['eventId'] = int(eventID)
            if 'allEvent' in args:
                sel.find_element_by_xpath(getattr(self.eventLogAttr, 'select_all_event')).click()
                txt = sel.find_element_by_css_selector(getattr(self.eventLogAttr, 'button_text')).text
                eventDict['Text'] = str(txt)
                print " SelectEvent eventDict : ", eventDict
        if 'DeselectEvent' in args:
            txt = sel.find_element_by_css_selector(getattr(self.eventLogAttr, 'button_text')).text
            if txt == 'Select All Events':
                sel.find_element_by_xpath(getattr(self.eventLogAttr, 'select_all_event')).click()        
                time.sleep(1)
            try:
                sel.find_element_by_xpath(getattr(self.eventLogAttr, 'deselect_all_event')).click()
                txt = sel.find_element_by_css_selector(getattr(self.eventLogAttr, 'button_text')).text
                eventDict['Text'] = str(txt)
                print " DeselectEvent eventDict : ", eventDict
            except Exception as err:
                print 'Deselect All Events button is not visible after clicking Select All Events Button', err
                return
        if 'DeleteEvents' in args:
            sel.find_element_by_xpath(getattr(self.eventLogAttr, 'delete_event')).click()
            if 'Cancel' in args:
                sel.find_element_by_css_selector(getattr(self.eventLogAttr, 'cancel_button')).click()
                print "DeleteEvents eventDict : ", eventDict
                return eventDict
            sel.find_element_by_css_selector(getattr(self.eventLogAttr, 'delete_button')).click()
            time.sleep(2)
            return eventDict
        if 'ClearEvents' in args:
            sel.find_element_by_xpath(getattr(self.eventLogAttr, 'clear_event')).click()
            time.sleep(2)
            return eventDict              
        elements = sel.find_elements_by_xpath(getattr(self.eventLogAttr, 'check_box'))
        for element in elements:
            value = element.is_selected()
            if value == False and 'DeselectEvent' in args:
                pass
            elif value == True and 'SelectEvent' in args:
                pass
            else:
                eventDict['Checked'] = False
                return eventDict
        return eventDict
            
    def fetchEventState(self,node,**kwargs):
        LOG.info("Enables Connections...")
        LOG.info("Navigate to the APS Configuration Page")
        sel = node.gui_login()
        time.sleep(5)
        self.navigate_to_event_log_page(sel)
        time.sleep(2)
        if 'eventId' in kwargs.keys():
            Id = 'eventClear'+str(kwargs['eventId'])
            element = sel.find_element_by_xpath('//input[@id="%s"]/ancestor::td[1]/ancestor::tr[1]' % Id)
            state = element.get_attribute('class')
            return str(state)    
        eventState = []
        elements = sel.find_elements_by_xpath(getattr(self.eventLogAttr, 'event_state'))
        for element in elements:
            state = element.get_attribute('class')
            eventState.append(str(state))
        print "event state list:", eventState
        if any(event in eventState for event in ('alarmed', 'warning')):
            eventDict = {'Result' : False , 'EventState' : eventState}
            return eventDict
        else:
            eventDict = {'Result' : True , 'EventState' : eventState}
            return eventDict

    def checkEvent(self,node,*args,**kwargs):
        LOG.info("Enables Connections...")
        LOG.info("Navigate to the APS Configuration Page")
        sel = node.gui_login()
        time.sleep(5)
        self.navigate_to_event_log_page(sel)
        time.sleep(2)
        if 'deleteAll' in args:
            txt = sel.find_element_by_xpath(getattr(self.eventLogAttr, 'event_table')).text
            return txt
        elements = sel.find_elements_by_xpath(getattr(self.eventLogAttr, 'event_id'))
        for element in elements:
            txt = element.text
            if int(txt) == int(kwargs['eventId']):
                return "%s this event has not been deleted" % str(kwargs['eventId'])
        else:
            return "Deletion of the event is successful"

    def navigate_to_event_log_page(self, sel):
        """
        Navigates to the Event Log page.
        """
        # click on 'Event Log' Page.
        wait = WebDriverWait(sel, 60)
        wait.until(EC.visibility_of_element_located((By.XPATH,getattr(self.eventLogAttr, 'event_log_page'))))
        sel.find_element_by_xpath(getattr(self.eventLogAttr, 'event_log_page')).click()
        time.sleep(2)
        wait.until(EC.visibility_of_element_located((By.XPATH,getattr(self.eventLogAttr, 'event_table'))))
        try:
            wait.until(EC.visibility_of_element_located((By.XPATH, getattr(self.eventLogAttr, 'clear_event'))))
        except:
            pass

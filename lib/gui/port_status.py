""" Python file that covers tabs under the "Port Status" Menu.
"""

import time
import logging
LOG = logging.getLogger(__name__)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from configAttr import defaultAttr

class PortStatus:
    """ Class that will either enable or disable the status of the ports.
    

    oxcDict = {
        'status'        : '[id=status]',
        'Popup_box'     : '[id=editor]',
        'port_status'   : '//a[text()="Port Status"]',
        'configure'     : '[id=modalConfigurebutton]',
        'Cancel_button' : '[id=modalCancelbutton]',
        'PrtStatus_page': '[id=canvas]',
        'alert_handler' : '[id="polalert"][class="modal"]',
        'ingress_port'  : '//tr[@id="Ingress Port%s"]/td[2]',
        'egress_port'   : '//tr[@id="Egress Port%s"]/td[2]'    
    }
    """
    
#    def __init__(self):
#
#        """
#        Initialize the default attr
#        """

    portStatusAttr = defaultAttr()  
    
    def Configure_port(self, node, ** kwargs):

        """ Enables or Disables the connection between Ingree and Egress Ports.
            Arguments:
            node    : Node Instance.
            prt_id  : Valid Port. 
        """
        
        LOG.info("Configure Connections...")
        LOG.info("Navigate to the Port-Status -> click on the given Port")
        sel = node.gui_login()
        time.sleep(5)
        self.navigate_to_port_status_page(sel)
        if 'port_status_page' in kwargs.keys():
            element = sel.find_element_by_css_selector(getattr(self.portStatusAttr, 'PrtStatus_page')).is_displayed()
            return element
        port_id = '%s' % kwargs['port']
        element = sel.find_element_by_css_selector('#canvas tr:nth-child(%d) td:nth-child(1)' % \
                (int(port_id)+1))
        ActionChains(sel).double_click(element).perform()      
        if 'popUp_Box' in kwargs.keys():
            element = sel.find_element_by_css_selector(getattr(self.portStatusAttr, 'Popup_box')).is_displayed()
            return element
        element = sel.find_element_by_css_selector(getattr(self.portStatusAttr, 'status'))
        if 'Enable' in kwargs.keys():
            element.send_keys('Enabled')
            LOG.info("Enabling Connection...")
            if 'Cancel' in kwargs.keys():
                sel.find_element_by_css_selector(getattr(self.portStatusAttr, 'Cancel_button')).click()
                return
        elif 'Disable' in kwargs.keys():
            element.send_keys('Disabled')
            LOG.info("Disabling Connection...")
            if 'Cancel' in kwargs.keys():
                sel.find_element_by_css_selector(getattr(self.portStatusAttr, 'Cancel_button')).click()
                return
        else:
            print "Wrong Keyword Argument"
        sel.find_element_by_css_selector(getattr(self.portStatusAttr, 'configure')).click()
        if 'Alert_Handle' in kwargs.keys():
            try:
                alert = sel.switch_to_alert()
                alertText = alert.text
                alert.accept()
                sel.switch_to_default_content()
                return alertText
            except:
                try:
                    popup = sel.find_element_by_css_selector(getattr(self.portStatusAttr, 'alert_handler')).text
                    return popup 
                except Exception as err:
                    print "No Alert is Present:", err
                    return
        time.sleep(5)


    def fetch_status(self,node,**kwargs):
        """
            Fetches the Port Label Information. 
            Arguments:
            node       : Node Instance.
            port_id   : Valid Port. 
        """

        LOG.info("Retrieve port status details for Port:%s" % kwargs['port'])
        LOG.info("Navigate to the Port_Status Page")
        sel = node.gui_login()
        time.sleep(5)

        if 'port' in kwargs.keys():

            self.navigate_to_port_status_page(sel)
            # click on the given port
            port_id = '%s' % kwargs['port']
            #e_port = '%s' % kwargs['egress_port']
            if kwargs['port'] < 17 :
                tag = getattr(self.portStatusAttr, 'ingress_port') %(int(port_id)-1)
                ## build 6.1.2.9 - .//*[@id='Ingress Port11']/td[2] ##
                #print "tag: ", tag #//tr[@id="Ingress Port11"]/td[2]
                #print '\n'
            else :
                tag = getattr(self.portStatusAttr, 'egress_port') %(int(port_id)-17)
            element = sel.find_element_by_xpath(tag)
            prt_status = element.text
            return prt_status
        else:
            raise Exception('Individual port information is required, to fetch the port status details.')
            


    def navigate_to_port_status_page(self,sel):
        """Navigates to the Port_Status page
        """
        # Click on 'Port_status' page.
        WebDriverWait(sel, 60).until(EC.visibility_of_element_located((By.XPATH,getattr(self.portStatusAttr, 'port_status'))))
        sel.find_element_by_xpath(getattr(self.portStatusAttr, 'port_status')).click()
        WebDriverWait(sel, 60).until(EC.visibility_of_element_located((By.XPATH,'//th[contains(text(),"Ingress ")]')))
        time.sleep(5)

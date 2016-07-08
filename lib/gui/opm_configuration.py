"""
Python file that covers tabs under the "OPM config" Page.
"""

import time
import logging
LOG = logging.getLogger(__name__)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from configAttr import defaultAttr

class OPMConfig:
    """
    Class that will Configure OPM Config Page.
    

    oxcDict ={
        'configuration_page' : '//a[text()="Configuration"]',
        'wavelength'         : '[id=lambda]',
        'offset'             : '[id=offset]',
        'Popup_box'          : '[id=editor]',
        'average_time'       : '[id=ave]',
        'configure_opm'      : '[id=modalConfigurebutton]',
        'cancel_opm'         : '[id=modalCancelbutton]',
        'opm_config_page'    : '//th[contains(text(),"Wavelength")]'
        }

    """
    
    portDict = {
        '1' : '0','2' : '1','3' : '2','4' : '3',
        '5' : '4','6' : '5','7' : '6','8' : '7',
        '9' : '8','10' : '9','11' : '10','12' : '11',
        '13' : '12','14' : '13','15' : '14','16' : '15',
        '17' : '24','18' : '25','19' : '26','20' : '27',
        '21' : '28','22' : '29','23' : '30','24' : '31',
        '25' : '16','26' : '17','27' : '18','28' : '19',
        '29' : '20','30' : '21','31' : '22','32' : '23'
        }
#    def __init__(self):

#        """
#        Initialize the default attr
#        """

    opmConfigAttr = defaultAttr()
    
    def navigate_to_opm_config_page(self,sel):
        """
        Navigate to the Opm Config Page.
        """
        # click on 'OPM config' Page.
        WebDriverWait(sel,60).until(EC.visibility_of_element_located((By.XPATH,getattr(self.opmConfigAttr, 'configuration_page'))))
        sel.find_element_by_xpath(getattr(self.opmConfigAttr, 'configuration_page')).click()
        WebDriverWait(sel,60).until(EC.visibility_of_element_located((By.XPATH,getattr(self.opmConfigAttr, 'opm_config_page'))))
        time.sleep(2)

    def configure_opm_parameters(self,node,**kwargs):
        """
        Configure OPM parameters such as Wavelength, offset and Averaging Time.
        """
        LOG.info("Enables Connections...")
        LOG.info("Navigate to the OPM Config Page")
        sel = node.gui_login()
        time.sleep(5)
        self.navigate_to_opm_config_page(sel)
        if 'opm_config_page' in kwargs.keys():
            element = sel.find_element_by_xpath(getattr(self.opmConfigAttr, 'opm_config_page')).is_displayed()
            return element
        Value = kwargs['Port']
        ele = "//tr[@id = '%s']/td[1]" %self.portDict[str(Value)]
        time.sleep(2)
        action = sel.find_element_by_xpath(ele)
        ActionChains(sel).double_click(action).perform()
        if 'popUp_Box' in kwargs.keys():
            element = sel.find_element_by_css_selector(getattr(self.opmConfigAttr, 'Popup_box')).is_displayed()
            return element
        if 'Wavelength' in kwargs.keys():
            element = sel.find_element_by_css_selector(getattr(self.opmConfigAttr, 'wavelength'))
            element.clear()
            element.send_keys(kwargs['Wavelength'])
        if 'Offset' in kwargs.keys():
            element = sel.find_element_by_css_selector(getattr(self.opmConfigAttr, 'offset'))
            element.clear()
            element.send_keys(kwargs['Offset'])
        if 'Averaging_time' in kwargs.keys():
            element = sel.find_element_by_css_selector(getattr(self.opmConfigAttr, 'average_time'))
            element.send_keys(kwargs['Averaging_time'])
        if 'Cancel' in kwargs.keys():
            sel.find_element_by_css_selector(getattr(self.opmConfigAttr, 'cancel_opm')).click()
        sel.find_element_by_css_selector(getattr(self.opmConfigAttr, 'configure_opm')).click()
        time.sleep(5)
        if 'InvalidCase' in kwargs.keys():
            try:    
                alert = sel.switch_to_alert()
                alertText = alert.text
                alert.accept()
                sel.switch_to_default_content()
                return str(alertText)
            except Exception as err:
                return "No alert is Present:", err            
        time.sleep(2)

    def fetch_opm_config_values(self,node,**kwargs):
        """
        fetch opm config parameters such as Wavelength, Offset and Averaging Time.
        """
        LOG.info("Enables Connections...")
        LOG.info("Navigate to the OPM Config Page")
        sel = node.gui_login()
        time.sleep(5)
        self.navigate_to_opm_config_page(sel)
        Value = kwargs['Port']
        action = sel.find_element_by_xpath("//tr[@id = '%s']/td[1]" % self.portDict[str(Value)])
        ActionChains(sel).double_click(action).perform()
        opmDict = {'wavelength' : '0','offset' : '0', 'average_time' : '0'}
        if 'Wavelength' in kwargs.keys():
            wave = sel.find_element_by_css_selector(getattr(self.opmConfigAttr, 'wavelength')).get_attribute('value')
            opmDict['wavelength'] = int(wave);
        if 'Offset' in kwargs.keys():
            ofset = sel.find_element_by_css_selector(getattr(self.opmConfigAttr, 'offset')).get_attribute('value')  
            opmDict['offset'] = str(ofset)
        if 'Averaging_time' in kwargs.keys():
            Avtime = sel.find_element_by_xpath("//tr[@id= '%s']/td[1]/following-sibling::td[4]" % self.portDict[str(Value)]).text
            sel.find_element_by_css_selector(getattr(self.opmConfigAttr, 'cancel_opm')).click()
            opmDict['average_time'] = str(Avtime)

        return opmDict

        
        
        
        
        
     

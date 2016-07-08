""" Python file that covers tabs under the "OPM Power Levels" Menu.
"""

import time
import logging
LOG = logging.getLogger(__name__)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from configAttr import defaultAttr

class OpmPowerLevels:
    """ Class that will Configure OPM Alarm Page.
    

    oxcDict = {
        'opm_power_level_page':'//a[text()="Power Levels"]',
        'opm_power_levels_page':'//th[contains(text(),"Power (dBm)")]',
        'port_status_object' : '//tr//td[@id = "%s"]//tr[%s]',
        'status_type_object' : '//tr/td[@id = "%s"]//tr[%s]/td[3]'
        }
    """
    
    tableDict = {(1,2,3,4,5,6,7,8): 'col0',
                (9,10,11,12,13,14,15,16): 'col1',
                (17,18,19,20,21,22,23,24): 'col3',
                (25,26,27,28,29,30,31,32): 'col2'
                }
    portDict = {(1,9,25,17): 3,
                (2,10,26,18): 4,
                (3,11,27,19): 5,
                (4,12,28,20): 6,
                (5,13,29,21): 7,
                (6,14,30,22): 8,
                (7,15,31,23): 9,
                (8,16,32,24): 10
                }
    

#    def __init__(self):
#        """Initialize the default atrr
#        """

    opmPowerLevelsAttr = defaultAttr()
        

    def navigate_to_opm_power_levels_page(self, sel):
        """
        Navigates to the OPM PowerLevels page.
        """
        # click on 'Opm Power Level' Page.
        WebDriverWait(sel,60).until(EC.visibility_of_element_located((By.XPATH,getattr(opmPowerLevelsAttr, 'opm_power_level_page'))))
        sel.find_element_by_xpath(getattr(opmPowerLevelsAttr, 'opm_power_level_page')).click()
        WebDriverWait(sel,60).until(EC.visibility_of_element_located((By.XPATH,getattr(opmPowerLevelsAttr, 'opm_power_levels_page'))))        
        time.sleep(2)  

    def fetchPowerLevelStatus(self,node,*args,**kwargs):
        """
        Fetches the Power level Status
        """
        LOG.info("Enables Connections...")
        LOG.info("Navigate to the OPM Power Level Page")
        sel = node.gui_login()
        time.sleep(5)
        self.navigate_to_opm_power_levels_page(sel)
        if 'power_levels_page' in args:
            element = sel.find_element_by_xpath(getattr(opmPowerLevelsAttr, 'opm_power_levels_page')).is_displayed()
            return element
        port = kwargs['Port']
        value1 = next(value for key,value in self.tableDict.iteritems() if port in key)
        value2 = next(value for key,value in self.portDict.iteritems() if port in key)
        portStatus = sel.find_element_by_xpath(getattr(opmPowerLevelsAttr, 'port_status_object') %(value1,value2)).get_attribute('class')
        statusType = sel.find_element_by_xpath(getattr(opmPowerLevelsAttr, 'status_type_object') % (value1,value2)).text
        PowerLevelStatus = {'PortStatus':portStatus,'StatusType':statusType}
        return PowerLevelStatus       
            

""" Python file that covers tabs under the "Connections" Menu.
"""

import time
import logging
LOG = logging.getLogger(__name__)

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from configAttr import defaultAttr

##LOG.info("Testing Cross Connect ..\n")

class CrossConnects:
    """ Class that will either connect or dis-connect between the ingress and
        egress ports and will fetch the connections available.
    """

    connectionsAttr = defaultAttr()
    

    def navigate_to_connection_table(self, sel):
        """ Navigates to the Cross-Connects -> Connection Table page and clicks
        on the given port.
        """

        # Click on 'Cross-Connects Tab.
        WebDriverWait(sel,30).until(EC.visibility_of_element_located((By.XPATH,"//a[text()='Cross-Connects']")))
        sel.find_element_by_xpath("//a[text()='Cross-Connects']").click()
        WebDriverWait(sel,30).until(EC.visibility_of_element_located((By.XPATH,'//img[@id="tab_conntable"]')))
        time.sleep(2)
        # Navigate to 'Connection Table' Tab.
        sel.find_element_by_css_selector('[id="tab_conntable"]').click()
        time.sleep(10)

    def enable_connections(self, node, **kwargs):

        """ Enables the connection between Ingree and Egress Ports.
        Arguments:
            node    : Node Instance.
            in_prt  : Valid Ingress Port.
            e_prt   : Valid Egress Port. 
        """
        sel = node.gui_login()
        time.sleep(5)
        self.navigate_to_connection_table(sel)
        # click on the given port
        ActionChains(sel).double_click(sel.find_element_by_css_selector(getattr(self.connectionsAttr, 'connection_tbl_prt')
            % kwargs['ingress_port'])).perform()
        time.sleep(1)
        # configures the eggress port 
        element = sel.find_element_by_css_selector(getattr(self.connectionsAttr, 'egress_port_box'))
        element.clear()
        element.send_keys(kwargs['egress_port'])
        time.sleep(1)
        if 'Cancel' in kwargs.keys():
            sel.find_element_by_css_selector(getattr(self.connectionsAttr, 'cancel')).click()
            return
        # click on Connect to enable connections.
        sel.find_element_by_xpath(getattr(self.connectionsAttr, 'connect')).click()
        time.sleep(1)
        if 'InvalidCase' in kwargs.keys():
            try:
                time.sleep(2)
                alertText = sel.find_element_by_xpath('//div[@id="polalert"]/div[4]').text
                return alertText
            except Exception as err:
                print "No Alert Message Raised:", err
                time.sleep(1)
                alert = sel.switch_to_alert()
                alertText = alert.text
                alert.accept()
                sel.switch_to_default_content()
                

    def disable_connections(self, node, **kwargs):
        """ Disables the connection between Ingree and Egress Ports.
        Arguments:
            node    : Node Instance.
            in_prt  : Valid Ingress Port.
        """

        sel = node.gui_login()
        time.sleep(5)
        self.navigate_to_connection_table(sel)
        # click on the given port
        time.sleep(10)
        ActionChains(sel).double_click(sel.find_element_by_css_selector(getattr(self.connectionsAttr, 'connection_tbl_prt')
            % kwargs['ingress_port'])).perform()
        time.sleep(10)
        # click on disconnect to disable connections.
        if 'InvalidCase' in kwargs.keys():
            element = sel.find_element_by_css_selector(getattr(self.connectionsAttr, 'egress_port_box'))
            element.clear()
            element.send_keys(kwargs['egress_port'])
            sel.find_element_by_xpath(getattr(self.connectionsAttr, 'disconnect')).click()
            return
            try:
                #alertText = sel.find_element_by_xpath('//div[@id="polalert"]/div[4]').text
                alertText = sel.find_element_by_xpath(getattr(self.connectionsAttr, 'connection_tbl_alert'))
                return alertText
            except Exception as err:
                print "No Alert Message Raised:", err
                return
        time.sleep(3)

    

    def clear_connections(self, node, **kwargs):
        sel = node.gui_login()
        time.sleep(5)    
        self.navigate_to_connection_table(sel)
        if 'ingress_port' in kwargs.keys():
            ActionChains(sel).double_click(sel.find_element_by_css_selector(getattr(self.connectionsAttr, 'connection_tbl_prt')
                % kwargs['ingress_port'])).perform()
            time.sleep(2)
            element = sel.find_element_by_xpath(getattr(self.connectionsAttr, 'disconnect')).is_enabled()
            if element == True:
                sel.find_element_by_xpath(getattr(self.connectionsAttr, 'disconnect')).click()       
        if 'egress_port' in kwargs.keys():
            ActionChains(sel).double_click(sel.find_element_by_css_selector(getattr(self.connectionsAttr, 'connection_tbl_prt')
                % kwargs['egress_port'])).perform()
            time.sleep(2)
            element = sel.find_element_by_xpath(getattr(self.connectionsAttr, 'disconnect')).is_enabled()
            if element == True:
                sel.find_element_by_xpath(getattr(self.connectionsAttr, 'disconnect')).click()

    def fetch_connections(self, node, **kwargs):
        """ Fetches the INPORT Cross-Connection details. 
        Arguments:
            node       : Node Instance.
            in_prt     : Valid Ingress Port.
            total_port : Total no of Ingress Ports in switch.
        """
        
        
        sel = node.gui_login()
        time.sleep(5)
        print "Testing fetch_connections ..."

        if 'port' in kwargs.keys():

            self.navigate_to_connection_table(sel)
            # click on the given port
            ActionChains(sel).double_click(sel.find_element_by_css_selector(getattr(self.connectionsAttr, 'connection_tbl_prt')
                % kwargs['port'])).perform()
            time.sleep(2)
            element = sel.find_element_by_css_selector(getattr(self.connectionsAttr, 'egress_port_box')).get_attribute('value')
            # click on cancel button after fetching the eggress port.
            sel.find_element_by_css_selector(getattr(self.connectionsAttr, 'cancel')).click()
            return element

        elif 'total_port' in kwargs.keys():
            port_conn_list = []
            # Fetch all the existing connections.
            self.navigate_to_connection_table(sel)
            for in_prt in range(1, kwargs['total_port']+1):
                # click on the given port
                ActionChains(sel).double_click(sel.find_element_by_css_selector(getattr(self.connectionsAttr, 'connection_tbl_prt')
                    % in_prt)).perform()
                element = sel.find_element_by_css_selector(getattr(self.connectionsAttr, 'egress_port_box'))
                e_prt = element.get_attribute('value')
                port_conn_list.append((in_prt, e_prt))
                # click on cancel button after fetching the eggress port.
                sel.find_element_by_css_selector(getattr(self.connectionsAttr, 'cancel')).click()

            return port_conn_list

        else:
            raise Exception('Either individual port or total port information'
                'is required, to fetch the connection details.')


    def edit_connections(self,node ,**kwargs):
        sel = node.gui_login()
        time.sleep(5)
        self.navigate_to_connection_table(sel)
        # click on the given port
        ActionChains(sel).double_click(sel.find_element_by_css_selector(getattr(self.connectionsAttr, 'connection_tbl_prt')
                    % kwargs['ingress_port'])).perform()
        # configures the eggress port 
        element = sel.find_element_by_css_selector(getattr(self.connectionsAttr, 'egress_port_box'))
        element.clear()
        element.send_keys(kwargs['egress_port'])
        sel.find_element_by_xpath(getattr(self.connectionsAttr, 'connect')).click()
        #time.sleep(1)
        #alert = sel.switch_to_alert()
        #alertText = alert.text
        #alert.accept()
        #sel.switch_to_default_content()
        if 'Cancel' in kwargs.keys():
            sel.find_element_by_css_selector(getattr(self.connectionsAttr, 'cancel')).click()
            return
        # click on Connect to enable connections.
        if 'InvalidCase' in kwargs.keys():
            try:
                time.sleep(1)
                alert = sel.switch_to_alert()
                alertText = alert.text
                alert.accept()
                sel.switch_to_default_content()
            except Exception as err:
                print "No Alert Message Raised and it throws alert as 'Port is already in use. Continue?':", err
                alertText = sel.find_element_by_xpath('//div[@id="polalert"]/div[4]').text 
        return alertText
            
    def set_portlabel(self, node, **kwargs):

        """ Set the Port Label for Ingree and Egress Ports.
        Arguments:
            node      : Node Instance.
            port_id       : Valid Port.
            prt_label : Valid Port Label. 
        """

        sel = node.gui_login()
        time.sleep(5)
        self.navigate_to_connection_table(sel)
        # click on the given port Label
        ActionChains(sel).double_click(sel.find_element_by_css_selector(getattr(self.connectionsAttr, 'ports_label')
                    % kwargs['port_id'])).perform()
        # sets the Port label
        element = sel.find_element_by_css_selector(getattr(self.connectionsAttr, 'port_label'))
        element.clear()
        element.send_keys(kwargs['port_label'])
        if 'Cancel' in kwargs.keys():
            sel.find_element_by_css_selector(getattr(self.connectionsAttr, 'cancel_label')).click()
            return
        
        sel.find_element_by_css_selector(getattr(self.connectionsAttr, 'set_label')).click()
        time.sleep(2)
        if 'InvalidCase' in kwargs.keys():
            alert = sel.switch_to_alert()
            alertText = alert.text
            alert.accept()
            sel.switch_to_default_content()
            return alertText    

    def remove_portlabel(self, node, **kwargs):

        """ Remove the Port Label for Ingree and Egress Ports.
        Arguments:
            node      : Node Instance.
            port_id   : Valid Port. 
        """

        sel = node.gui_login()
        time.sleep(5)
        self.navigate_to_connection_table(sel)
        # click on the given port Label
        ActionChains(sel).double_click(sel.find_element_by_css_selector(getattr(self.connectionsAttr, 'ports_label')
                    % kwargs['port_id'])).perform()
        # Remove the Port label 
        element = sel.find_element_by_css_selector(getattr(self.connectionsAttr, 'port_label'))
        element.clear()
        sel.find_element_by_css_selector(getattr(self.connectionsAttr, 'set_label')).click()
        time.sleep(2)


    def fetch_portlabel(self, node, **kwargs):
        """ Fetches the Port Label Information. 
        Arguments:
            node       : Node Instance.
            port_id   : Valid Port. 
        """

        sel = node.gui_login()
        time.sleep(5)

        if 'port' in kwargs.keys():

            self.navigate_to_connection_table(sel)
            # click on the given port
            ActionChains(sel).double_click(sel.find_element_by_css_selector(getattr(self.connectionsAttr, 'ports_label')
                    % kwargs['port'])).perform()
            time.sleep(2)
            element = sel.find_element_by_css_selector(getattr(self.connectionsAttr, 'port_label'))
            f_prt = element.get_attribute('value')
            # click on cancel button after fetching the port label.
            sel.find_element_by_css_selector(getattr(self.connectionsAttr, 'cancel')).click()
            return f_prt

        elif 'total_port' in kwargs.keys():
            port_label_list = []
            # Fetch all the existing connections.
            self.navigate_to_connection_table(sel)
            for in_prt in range(1, kwargs['total_port']+1):
                # click on the given port
                ActionChains(sel).double_click(sel.find_element_by_css_selector(getattr(self.connectionsAttr, 'ports_label')
                    % in_prt)).perform()
                element = sel.find_element_by_css_selector(getattr(self.connectionsAttr, 'port_label'))
                label_prt = element.get_attribute('value')
                port_conn_list.append((in_prt, label_prt))
                # click on cancel button after fetching the eggress port.
                sel.find_element_by_css_selector(getattr(self.connectionsAttr, 'cancel')).click()

            return port_label_list

        else:
            raise Exception('Either individual port or total port information'
                'is required, to fetch the port label details.')
              

    def navigate_to_connection_map(self, sel):
        """
        Navigates to the Cross-Connects -> Connection Map page. 
        """
        # Click on 'Cross-Connects Tab.
        WebDriverWait(sel,30).until(EC.visibility_of_element_located((By.XPATH,"//a[text()='Cross-Connects']")))
        sel.find_element_by_xpath("//a[text()='Cross-Connects']").click()
        time.sleep(5)
        # Navigate to 'Connection Map' Tab.
        sel.find_element_by_css_selector('[id="tab_connmap"]').click()
        time.sleep(5)
        
    def setlabel_map(self,node, **kwargs):
        """ Set the Port Label for Ingree and Egress Ports under connection map tab.
        Arguments:
            node      : Node Instance.
            port_id       : Valid Port.
            prt_label : Valid Port Label. 
        """

        sel = node.gui_login()
        time.sleep(5)
        self.navigate_to_connection_map(sel)
        if getattr(self.connectionsAttr, 'version') == '6.5' or getattr(self.connectionsAttr, 'version') == '6.3': 
            prt_id1 = int(kwargs['port_id'])
            prt_id2 = prt_id1+1
            if prt_id2 <= 49:
                prt_id = "inport%s" % str(prt_id2)
            else :
                prt_id = "outport%s" % str(prt_id2)   
            sel.find_element_by_css_selector("[id=%s]" % prt_id).click()
        else:
            # click on the given port
            sel.find_element_by_css_selector(getattr(self.connectionsAttr, 'connection_map_prt') % kwargs['port_id']).click()
        # sets the Port label
        sel.find_element_by_css_selector(getattr(self.connectionsAttr, 'setport_label_map')).click()
        element = sel.find_element_by_css_selector(getattr(self.connectionsAttr, 'port_label_map'))
        element.clear()
        element.send_keys(kwargs['port_label'])
        if 'Cancel' in kwargs.keys():
            sel.find_element_by_css_selector(getattr(self.connectionsAttr, 'cancel_map')).click()
            return
        sel.find_element_by_css_selector(getattr(self.connectionsAttr, 'set_label_map')).click()
        time.sleep(2)
        if 'InvalidCase' in kwargs.keys():
            alert = sel.switch_to_alert()
            alertText = alert.text
            alert.accept()
            sel.switch_to_default_content()
            return alertText
        
    def removelabel_map(self, node, **kwargs):

        """ Remove the Port Label for Ingree and Egress Ports. under connection map tab.
        Arguments:
            node      : Node Instance.
            port_id   : Valid Port. 
        """

        sel = node.gui_login()
        time.sleep(5)
        self.navigate_to_connection_map(sel)
        if getattr(self.connectionsAttr, 'version') == '6.5' or getattr(self.connectionsAttr, 'version') == '6.3': 
            prt_id1 = int(kwargs['port_id'])
            prt_id2 = prt_id1+1
            if prt_id2 <= 49:
                prt_id = "inport%s" % str(prt_id2)
            else :
                prt_id = "outport%s" % str(prt_id2)   
            sel.find_element_by_css_selector("[id='%s']" % prt_id).click()
        else:
            # click on the given port
            sel.find_element_by_css_selector(getattr(self.connectionsAttr, 'connection_map_prt') % kwargs['port_id']).click()
        # Remove the Port label
        sel.find_element_by_css_selector(getattr(self.connectionsAttr, 'setport_label_map')).click()
        element = sel.find_element_by_css_selector(getattr(self.connectionsAttr, 'port_label_map'))
        element.clear()
        sel.find_element_by_css_selector(getattr(self.connectionsAttr, 'set_label_map')).click()
        time.sleep(2)

    def fetchlabel_map(self, node, **kwargs):
        """ Fetches the Port Label Information. 
        Arguments:
            node       : Node Instance.
            port_id   : Valid Port. 
        """

        sel = node.gui_login()
        time.sleep(5)

        if 'port' in kwargs.keys():

            self.navigate_to_connection_map(sel)
            # click on the given port
            if getattr(self.connectionsAttr, 'version') == '6.5' or getattr(self.connectionsAttr, 'version') == '6.3':
                prt_id1 = int(kwargs['port'])
                prt_id2 = prt_id1+1
                if prt_id2 <= 49:
                    prt_id = "inport%s" % str(prt_id2)
                else :
                    prt_id = "outport%s" % str(prt_id2)
                sel.find_element_by_css_selector("[id='%s']" % prt_id).click()
            else:
                sel.find_element_by_css_selector(getattr(self.connectionsAttr, 'connection_map_prt') % kwargs['port']).click()
            sel.find_element_by_css_selector(getattr(self.connectionsAttr, 'setport_label_map')).click()
            element = sel.find_element_by_css_selector(getattr(self.connectionsAttr, 'port_label_map'))
            f_prt = element.get_attribute('value')
            # click on cancel button after fetching the port label.
            sel.find_element_by_css_selector(getattr(self.connectionsAttr, 'cancel_map')).click()
            return f_prt

        elif 'total_port' in kwargs.keys():
            port_label_list = []
            # Fetch all the existing connections.
            self.navigate_to_connection_map(sel)
            for in_prt in range(1, kwargs['total_port']+1):
                # click on the given port
                if getattr(self.connectionsAttr, 'version') == '6.5' or getattr(self.connectionsAttr, 'version') == '6.3':
                    prt_id1 = int(in_prt)
                    prt_id2 = prt_id1+1
                    if prt_id2 <= 17:
                        prt_id = "inport%s" % str(prt_id2)
                    else :
                        prt_id = "outport%s" % str(prt_id2)
                    sel.find_element_by_css_selector("[id='%s']" % prt_id).click()
                else:
                    sel.find_element_by_css_selector(getattr(self.connectionsAttr, 'connection_map_prt') % in_prt).click()
                sel.find_element_by_css_selector(getattr(self.connectionsAttr, 'setport_label_map')).click()
                element = sel.find_element_by_css_selector(getattr(self.connectionsAttr, 'port_label_map'))
                label_prt = element.get_attribute('value')
                port_conn_list.append((in_prt, label_prt))
                # click on cancel button after fetching the eggress port.
                sel.find_element_by_css_selector(getattr(self.connectionsAttr, 'cancel_map')).click()

            return port_label_list

        else:
            raise Exception('Either individual port or total port information'
                'is required, to fetch the port label details.')

    def enable_connectionsmap(self, node, *args, **kwargs):

        """ Enables the connection between Ingree and Egress Ports.
        Arguments:
            node    : Node Instance.
            in_prt  : Valid Ingress Port.
            e_prt   : Valid Egress Port. 
        """

        sel = node.gui_login()
        time.sleep(5)
        self.navigate_to_connection_map(sel)
        if 'cross_connect_page' in args:
            element = sel.find_element_by_xpath('//div[@id="tabpanel"]').is_displayed()
            return element
        if 'Set_label_button' in args:
            if getattr(self.connectionsAttr, 'version') == '6.5' or getattr(self.connectionsAttr, 'version') == '6.3':
                sel.find_element_by_css_selector("[id='inport2']").click()
            else:
                sel.find_element_by_css_selector("[id='2']").click()
            sel.find_element_by_css_selector('[id="portLabelButton"]').click()
            element = sel.find_element_by_xpath('//div[@id="labeleditor"]').is_displayed()
            return element
        else:
            if getattr(self.connectionsAttr, 'version') == '6.5' or getattr(self.connectionsAttr, 'version') == '6.3':
                in_prt1 = int(kwargs['ingress_port'])
                in_prt2 = in_prt1+1
                in_prt_id = "inport%s" % str(in_prt2)
                e_prt1 = int(kwargs['egress_port'])
                e_prt2 = e_prt1+1
                e_prt_id = "outport%s" % str(e_prt2)
                # click and configure on the given port
                sel.find_element_by_css_selector("[id='%s']" % in_prt_id).click()
                sel.find_element_by_css_selector("[id='%s']" % e_prt_id).click()
            else:
                sel.find_element_by_css_selector(getattr(self.connectionsAttr, 'connection_map_prt') % kwargs['ingress_port']).click()
                sel.find_element_by_css_selector(getattr(self.connectionsAttr, 'connection_map_prt') % kwargs['egress_port']).click()
         
    time.sleep(2)

    def edit_connectionsmap(self, node, **kwargs):

        sel = node.gui_login()
        time.sleep(5)
        self.navigate_to_connection_map(sel)
        if getattr(self.connectionsAttr, 'version') == '6.5' or getattr(self.connectionsAttr, 'version') == '6.3':
            in_prt1 = int(kwargs['ingress_port'])
            in_prt2 = in_prt1+1
            in_prt_id = "inport%s" % str(in_prt2)
            e_prt1 = int(kwargs['egress_port'])
            e_prt2 = e_prt1+1
            e_prt_id = "outport%s" % str(e_prt2)
            # click and configure on the given port
            sel.find_element_by_css_selector("[id='%s']" % in_prt_id).click()
            sel.find_element_by_css_selector("[id='%s']" % e_prt_id).click()
        else:
            sel.find_element_by_css_selector(getattr(self.connectionsAttr, 'connection_map_prt') % kwargs['ingress_port']).click()
            sel.find_element_by_css_selector(getattr(self.connectionsAttr, 'connection_map_prt') % kwargs['egress_port']).click()
        if 'Cancel' in kwargs.keys():
            alert = sel.switch_to_alert()
            alert.dismiss()
        else:
            alert = sel.switch_to_alert()
            alert.accept()
            time.sleep(2)    


    def disable_connectionsmap(self, node, **kwargs):
        """ Disables the connection between Ingree and Egress Ports.
        Arguments:
            node    : Node Instance.
            in_prt  : Valid Ingress Port.
            e_prt   : Valid Egress Port.
        """

        sel = node.gui_login()
        time.sleep(5)
        self.navigate_to_connection_map(sel)
        if getattr(self.connectionsAttr, 'version') == '6.5' or getattr(self.connectionsAttr, 'version') == '6.3':
            # click and disconnect on the given port
            in_prt1 = int(kwargs['ingress_port'])+1
            in_prt_id = "inport%s" % str(in_prt1)
            e_prt1 = int(kwargs['egress_port'])+1
            e_prt_id = "outport%s" % str(e_prt1)
            sel.find_element_by_css_selector("[id='%s']" % in_prt_id).click()
            #sel.switch_to_default_content()
            sel.find_element_by_css_selector("[id='%s']" % e_prt_id).click()
        else:
            sel.find_element_by_css_selector(getattr(self.connectionsAttr, 'connection_map_prt') % kwargs['ingress_port']).click()
            sel.find_element_by_css_selector(getattr(self.connectionsAttr, 'connection_map_prt') % kwargs['egress_port']).click()
        if 'Cancel' in kwargs.keys():
            alert = sel.switch_to_alert()
            alert.dismiss()
        else:
            alert = sel.switch_to_alert()
            alert.accept()
            time.sleep(2)

    def double_click(self, node, **kwargs):
        sel = node.gui_login()
        time.sleep(5)
        self.navigate_to_connection_table(sel)
        time.sleep(2)
        if 'ingress_port' in kwargs.keys():
            in_prt_id = "port%s" % kwargs['ingress_port']
            ActionChains(sel).double_click(sel.find_element_by_css_selector("[id='%s']"
                % in_prt_id)).perform()
            element = sel.find_element_by_xpath('//div[@id="conneditor"]')
            return element
        elif 'ingress_label' in kwargs.keys():
            in_prt_id = "label%s" % kwargs['ingress_label']
            ActionChains(sel).double_click(sel.find_element_by_css_selector("[id='%s']"
                % in_prt_id)).perform()
            element = sel.find_element_by_xpath('//div[@id="labeleditor"]')
            return element
        else:
            print "Kwargs not given properly"




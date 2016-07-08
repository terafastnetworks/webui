""" Contains 'gui_login', 'gui_logout' functions inside a Node class. 
Need to pass 'box_ip' while creating the node's instance.
Uses 'Firefox' as the default browser.
"""

import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from pyvirtualdisplay import Display

USERNAME = 'admin'
PASSWORD = 'root'

class Node:

    oxcDict = {
        'login_button' : '[id=loginbutton]',
        'main_page_display' : '[id=container]',
        'logout' : '//a[text()="Logout"]',
        'alert' : '//div[@id="container"]/table/tbody/tr[2]/td[1]/div/p/b',
        'login_page' : '//td[contains(text(),"Password")]'
        }


    def __init__(self, node):
        self._gui = None
        self.node = node
        #self.start_vnc_server()

    def gui_login(self, browser='Firefox', usr_name = USERNAME, pass_wd = PASSWORD,**kwargs):
        
        if not self._gui:
            self._gui = webdriver.Firefox()
            url = "http://%s" % self.node
            print "BOX : ", url
            print "Inside main page ................\n"
            try:
                self._gui.get(url)
            except Exception as err:
                print "Login Error:", err
            WebDriverWait(self._gui,60).until(EC.visibility_of_element_located((By.XPATH,self.oxcDict['login_page'])))
            if 'UserName' in kwargs.keys():
                self._gui.find_element_by_css_selector('[name=user]').send_keys('%s' % kwargs['UserName'])
            else:
                self._gui.find_element_by_css_selector('[name=user]').send_keys(usr_name)
            if 'Password' in kwargs.keys():
                self._gui.find_element_by_css_selector('[name=passwd]').send_keys('%s' % kwargs['Password'])
            else:
                self._gui.find_element_by_css_selector('[name=passwd]').send_keys(pass_wd)    
            self._gui.find_element_by_css_selector(self.oxcDict['login_button']).click()
            time.sleep(5)
            self._gui.maximize_window()
            if 'main_page' in kwargs.keys():
                #print "Inside main page ................\n"
                element = self._gui.find_element_by_css_selector(self.oxcDict['main_page_display']).is_displayed()
                return element
                print "element : ", element
        #print "self._gui:  ", self._gui
        return self._gui


    def gui_logout(self):
        #print "SELF GUI:", self._gui
        self._gui.find_element_by_xpath(self.oxcDict['logout']).click()
        self._gui.close()
        self._gui = None

    def gui_login_page(self, browser='Firefox', usr_name = USERNAME, pass_wd = PASSWORD, **kwargs):
#        display = Display(visible=0, size=(800, 600))
#        display.start()

        self._gui = webdriver.Firefox()
        url = "http://%s" % self.node
        print "BOX : ", url
        try:
            self._gui.get(url)
        except Exception as err:
            print "Login Error:", err
        WebDriverWait(self._gui,60).until(EC.visibility_of_element_located((By.XPATH,self.oxcDict['login_page'])))
        if 'login_page' in kwargs.keys():
            element = self._gui.find_element_by_xpath(self.oxcDict['login_page']).is_displayed()
            return element
        if 'UserName' in kwargs.keys():
            self._gui.find_element_by_css_selector('[name=user]').send_keys('%s' % kwargs['UserName'])
        else:
            self._gui.find_element_by_css_selector('[name=user]').send_keys(usr_name)
        if 'Password' in kwargs.keys():
            self._gui.find_element_by_css_selector('[name=passwd]').send_keys('%s' % kwargs['Password'])
        else:
            self._gui.find_element_by_css_selector('[name=passwd]').send_keys(pass_wd)    
        self._gui.find_element_by_css_selector(self.oxcDict['login_button']).click()
        if 'Invalid_case' in kwargs.keys():
            try:
                WebDriverWait(self._gui,60).until(EC.visibility_of_element_located((By.XPATH,self.oxcDict['alert'])))
                element = self._gui.find_element_by_xpath(self.oxcDict['alert']).text
                return element
            except Exception as err:
                print "No Alert Message for invalid login:", err
                return
        time.sleep(5)
        self._gui.maximize_window()
        if 'main_page' in kwargs.keys():
            element = self._gui.find_element_by_css_selector(self.oxcDict['main_page_display']).is_displayed()
            return element


        return self._gui
        
        #display.stop()

    def start_vnc_server(self):

        os.system('vncserver :34')
        os.system('export DISPLAY=:34')

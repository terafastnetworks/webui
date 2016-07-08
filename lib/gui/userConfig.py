import time
import logging
LOG = logging.getLogger(__name__)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from configAttr import defaultAttr

class UserConfig:
    """ Class that will Create Users, Edit Users and Delete Users.
    

    oxcDict = {

        'create_user'       : 'modalCreate Userbutton',
        'cancel_creation'   : 'modalCancelbutton',
        'delete_button'     : 'modalDeletebutton',
        'main_page_visible' : '//div[@id="container"]/table/tbody/tr[2]/td[2]/div',
        'create_row'        : '[id="-1"]''[title="Edit Row"]',
        'update_user'       : 'modalUpdate Userbutton',
        'change_password'   : 'passwdbutton',
        'user_config_page'  : '//a[text()="User Config"]',
        'set_password_page' : '//a[text()="Set Password"]',
        'edit_username'     : 'newuserpasswd',
        'edit_usertype'     : 'newusertype',
        'user_canvas'       : 'usercanvas',
        'new_user_name'     : 'newusername',
        'new_user_passwd'   : 'newuserpasswd',
        'new_user_type'     : 'newusertype',
        'user_editor'       : 'usereditor',
        'delete_row'        : '[title="Delete Row"]'
    }

    """

#    def __init__(self):

#        """
#        Initialize the default attr
#        """

    userConfigAttr = defaultAttr()
    
    def navigate_to_user_config_page(self, sel):
        """
        Navigates to the User Config page. 
        """
        # Click on 'UserConfig' Tab.
        WebDriverWait(sel, 30).until(EC.visibility_of_element_located((By.XPATH,getattr(self.userConfigAttr, 'user_config_page'))))
        sel.find_element_by_xpath(getattr(self.userConfigAttr, 'user_config_page')).click()
        WebDriverWait(sel, 30).until(EC.visibility_of_element_located((By.XPATH,'//th[contains(text(),"Edit")]')))
        time.sleep(5)

    def deleteAllUsers(self, node):
        """
        Deletes all the Existing Users except default admin user
        """

        LOG.info("Enables Connections...")
        LOG.info("Navigate to the User Config Page")
        sel = node.gui_login_page()
        time.sleep(5)
        self.navigate_to_user_config_page(sel)
        elements = sel.find_elements_by_css_selector(getattr(self.userConfigAttr, 'delete_row'))
        for user in elements:
            user.click()
            sel.find_element_by_id(getattr(self.userConfigAttr, 'delete_button')).click() 
            time.sleep(2)

    def create_user(self, node,*args,**kwargs):

        """ Create a User in UserConfig Page.
        Arguments:
            node      : Node Instance.
            new_username : New UserName
            new_userpasswd : New User Password
            new_usertype : New User Type
        """

        LOG.info("Enables Connections...")
        LOG.info("Navigate to the User Config Page")
        if 'same_session' in args:
            sel = node.gui_login()
        else:
            sel = node.gui_login_page()
        time.sleep(10)
        self.navigate_to_user_config_page(sel)
        if 'user_config_page' in args:
            element1 = sel.find_element_by_id(getattr(self.userConfigAttr, 'user_canvas')).is_displayed()
            return element1
        if 'user_editor_popup' in args:
            sel.find_element_by_css_selector(getattr(self.userConfigAttr, 'create_row')).click()
            element2 = sel.find_element_by_id(getattr(self.userConfigAttr, 'user_editor')).is_displayed()
            return element2
        sel.find_element_by_css_selector(getattr(self.userConfigAttr, 'create_row')).click()
        sel.find_element_by_id(getattr(self.userConfigAttr, 'new_user_name')).send_keys(kwargs['new_username'])
        sel.find_element_by_id(getattr(self.userConfigAttr, 'new_user_passwd')).send_keys(kwargs['new_userpasswd'])
        sel.find_element_by_id(getattr(self.userConfigAttr, 'new_user_type')).send_keys(kwargs['new_usertype'])    
        
        if 'Cancel' in kwargs.keys():
            sel.find_element_by_id(getattr(self.userConfigAttr, 'cancel_creation')).click()
            time.sleep(1)
            value = sel.find_elements_by_css_selector("td:nth-child(1) td:nth-child(1)")
            nameList = []
            for val in value:
                val = str(val.text)
                nameList.append(val) 
            time.sleep(2)
            return nameList
        try:
            sel.find_element_by_id(getattr(self.userConfigAttr, 'create_user')).click()
            time.sleep(5)
        except Exception as err:
            print "Create User Error or Existing User or Invalid Input:", err
        
        if 'InvalidCase' in kwargs.keys():
            try:
                alert = sel.switch_to_alert()
                alertText = alert.text
                alert.accept()
                sel.switch_to_default_content()
                time.sleep(2)
                return alertText
            except:
                popup = sel.find_element_by_css_selector('[id="polalert"][class="modal"]').text
                return popup
                                   
    def delete_user(self, node, *args, **kwargs):

        """ Delete a User in UserConfig Page.
        Arguments:
            node      : Node Instance.
            user_name : UserName to Delete.
        """

        LOG.info("Enables Connections...")
        LOG.info("Navigate to the User Config Page")
        if 'same_session' in args:
            sel = node.gui_login()
        else:
            sel = node.gui_login_page()    
        time.sleep(5)
        self.navigate_to_user_config_page(sel)
        wait = WebDriverWait(sel, 30)
        wait.until(EC.visibility_of_element_located((By.XPATH,'//th[contains(text(),"Edit")]')))    
        value = sel.find_elements_by_css_selector("td:nth-child(1) td:nth-child(1)")
        id_val = 0
        usrName = kwargs['user_name']
        for line in value:
            line1 = str(line.text)
            if usrName in line1:
                break
            id_val += 1
        else:
            print "User Name-%s not Found.." % usrName

        sel.find_element_by_css_selector("[id='%s'][title='Delete Row']" % id_val).click()
        if 'Cancel' in kwargs.keys():
            sel.find_element_by_id('modalCancelbutton').click()
        else:
            sel.find_element_by_id('modalDeletebutton').click()
        time.sleep(2)
        value1 = sel.find_elements_by_css_selector("td:nth-child(1) td:nth-child(1)")
        nameList = []
        for val in value1:
            val = str(val.text)
            nameList.append(val)
        time.sleep(5)
        return nameList

    def check_user(self, node,*args,**kwargs):
        """ Check a User is present in UserConfig Page.
        Arguments:
            node  : Node Instance
            user_name : UserName .
        """    
        LOG.info("Enables Connections...")
        LOG.info("Navigate to the User Config Page")
        try:
            sel = node.gui_login()
        except:
            sel = node.gui_login_page()
        time.sleep(5)
        self.navigate_to_user_config_page(sel)
        time.sleep(3)
        usrnme = kwargs['user_name']
        try:
            element = '//td[contains(text(), "%s")]' % usrnme
            userName = sel.find_element_by_xpath(element).is_displayed()
        except Exception as err:
            print "userName not Found"
        sel.find_element_by_xpath("//a[text()='Logout']").click()
        time.sleep(5)
        sel.close()
        return userName
        
                
    def edit_user(self, node, *args, **kwargs):

        """ Edit a User in UserConfig Page.
        Arguments:
            node  : Node Instance
            user_name : UserName to Delete.
            edit_userpasswd : UserName to Edit.
            edit_usertype : UserType to Change.
        """
        LOG.info("Enables Connections...")
        LOG.info("Navigate to the User Config Page")
        if 'same_session' in args:
            sel = node.gui_login()
        else:
            sel = node.gui_login_page()
        time.sleep(10)
        self.navigate_to_user_config_page(sel)
        value = sel.find_elements_by_css_selector("td:nth-child(1) td:nth-child(1)")
        id_val = 0
        usrName = kwargs['user_name']
        for line in value:
            line = str(line.text)
            if usrName in line:
                break
            id_val += 1
        else:
            print "User Name-%s not Found.." % usrName
        print "ID:", id_val
        sel.find_element_by_css_selector("[id='%s'][title='Edit Row']" % id_val).click()
        sel.find_element_by_id(getattr(self.userConfigAttr, 'edit_username')).send_keys(kwargs['edit_userpasswd'])
        if 'edit_usertype' in kwargs.keys():
            sel.find_element_by_id(getattr(self.userConfigAttr, 'edit_usertype')).send_keys(kwargs['edit_usertype'])
        if 'Cancel' in kwargs.keys():
            sel.find_element_by_id(getattr(self.userConfigAttr, 'cancel_creation')).click()
            time.sleep(2)
            sel.find_element_by_xpath("//a[text()='Logout']").click()
            return
        
        sel.find_element_by_id(getattr(self.userConfigAttr, 'update_user')).click()
        time.sleep(5)
        if 'InvalidCase' in kwargs.keys():
            try:
                alert = sel.switch_to_alert()
                alertText = alert.text
                alert.accept()
                sel.switch_to_default_content()
                time.sleep(2)
                return alertText
            except:
                popup = sel.find_element_by_css_selector('[id="polalert"][class="modal"]').text
                return popup 
        sel.find_element_by_xpath("//a[text()='Logout']").click()
        sel.close()
        time.sleep(2)

    def set_password_user_view(self, node , **kwargs):
        """ SetPassword For View and User Type User.
        Arguments:
            node  : Node Instance
            UserName : UserName to Login
            Password : Password to Login
            old_password : Old Login Password
            new_password : New Login Password
        """
        sel = node.gui_login(UserName = kwargs['UserName'],Password = kwargs['Password'])
        time.sleep(5)
        sel.find_element_by_xpath(getattr(self.userConfigAttr, 'change_password')).click()
        time.sleep(2)
        sel.find_element_by_id('oldpasswd').send_keys(kwargs['old_password'])
        sel.find_element_by_id('passwd1').send_keys(kwargs['new_password'])
        sel.find_element_by_id('passwd2').send_keys(kwargs['new_password'])
        sel.find_element_by_id(getattr(self.userConfigAttr, 'change_password')).click()
        time.sleep(2)
        element = sel.find_element_by_css_selector('[id="polalert"][class="modal"]')
        element.find_element_by_id('modalOKbutton').click()


    def check_content(self,node,*args,**kwargs):
        sel = node.gui_login_page(UserName = kwargs['user_name'],Password = kwargs['Password'])
        WebDriverWait(sel,60).until(EC.visibility_of_element_located((By.XPATH,'//div[contains(text(),"System")]')))
        if 'page_content' in args:
            pageContent = sel.find_element_by_xpath('//div[@id="container"]/table/tbody/tr[2]/td[2]/div/ul[1]').text
            time.sleep(2)
            return pageContent
        usrDict = {}
        element = sel.find_element_by_class_name('content').is_displayed()
        sel.find_element_by_xpath(getattr(self.userConfigAttr, 'user_config_page')).click()
        WebDriverWait(sel, 30).until(EC.visibility_of_element_located((By.ID,getattr(self.userConfigAttr, 'user_canvas'))))
        userType = sel.find_element_by_xpath('//td[contains(text(), "%s")]/following-sibling::td[1]' % kwargs["user_name"]).text
        usrDict['login_page'] = element
        usrDict['usrType'] = userType
        time.sleep(2)
        return usrDict  

### all attributes ###

class defaultAttr:


    version		  = '6.5'
    ### connection table and Map
    cross_connects_page   = '//a[text()="Cross-Connects"]'
    conn_tbl              = '[id=tab_conntable]'
    egress_port_box       = '[id=portconn]'
    connection_tbl_prt    = '[id=port%s]'
    connection_map_prt    = '[id="%s"]'
    ports_label           = '[id=label%s]'
    connect               = '//button[text()="Connect"]'
    disconnect            = '//button[text()="Disconnect"]'
    cancel                = '[id=modalCancelbutton]'
    port_label            = '[id="portlabel"]'
    set_label             = '[id="modalSet Labelbutton"]'
    clear_all             = '//button[text()="Clear All Connections"]'
    setport_label_map     = '[id=portLabelButton]'
    port_label_map        = '[id=portlabel]'
    set_label_map         = '[id="modalSet Labelbutton"]'
    cancel_map            = '[id=modalCancelbutton]'
    cancel_label          = '[id=modalCancelbutton]'
    cancel                = '[id=modalCancelbutton]'
    connection_tbl_alert  = '//div[@id="polalert"]/div[4]'

    ### event log
    
    event_log_page        = '//a[text()="Event Log"]'
    single_event          = '//div[@id="opmcanvas"]/table/tbody/tr/td/table/tbody/tr[2]/td[5]/input[@type="checkbox"]'
    select_all_event      = '//button[text()="Select All Events"][@id="opm"]'
    button_text           = '[id="opm"]'
    deselect_all_event    = '//button[text()="Deselect All Events"][@id="opm"]'
    delete_event          = '//button[text()="Delete Selected Events..."][@id="opm"]'
    cancel_button         = '[id="modalCancelbutton"]'
    delete_button         = '[id="modalDeletebutton"]'
    clear_event           = '//button[text()="Clear Selected Events"][@id="opm"]'
    check_box             = "//div[@id='opmcanvas']/table/tbody/tr/td/table/tbody/tr/td/input[@type='checkbox']"
    event_state           = '//div[@id="opmcanvas"]/table/tbody/tr/td/table/tbody/tr[1]/following-sibling::tr'
    event_id              = '//div[@id="opmcanvas"]/table/tbody/tr/td/table/tbody/tr/td[1]'
    event_table           = '//div[@id="opmcanvas"]'
    event_page            = '[class="content"]'

    ### opm alarms oxc

    opm_alarms_page           ='//a[text()="Alarms"]'
    opm_alarms_config_page    ='[id=canvas]'
    opm_alarm_visibility      = '//div[@id="canvas"]/table'
    Popup_box                 = '[id=editor]'
    cancel_opm_alarms         = '[id=modalCancelbutton]'
    availability              ='//tr[@id = "0"]//td[1]'
    configure_opm_alarms      = '[id=modalConfigurebutton]'

    ### opm alarms alarm dict

    los_alarm_mode        = '[id=mode]'
    los_alarm_edge        = '[id=edge]'
    los_low_threshold     = '[id=lowthresh]'
    los_high_threshold    = '[id=highthresh]'
    degraded_alarm_mode   = '[id=degrmode]'
    degraded_threshold    = '[id=degrthresh]'
    alarm_hysteresis      = '[id=hysteresis]'
    recovery_delay        = '[id=alarmcleardelay]'

    
    ### opm config oxc dict

    configuration_page = '//a[text()="Configuration"]'
    wavelength         = '[id=lambda]'
    offset             = '[id=offset]'
    Popup_box          = '[id=editor]'
    average_time       = '[id=ave]'
    configure_opm      = '[id=modalConfigurebutton]'
    cancel_opm         = '[id=modalCancelbutton]'
    opm_config_page    = '//th[contains(text(),"Wavelength")]'

    ### port status

    status        = '[id=status]'
    Popup_box     = '[id=editor]'
    port_status   = '//a[text()="Port Status"]'
    configure     = '[id=modalConfigurebutton]'
    Cancel_button = '[id=modalCancelbutton]'
    PrtStatus_page= '[id=canvas]'
    alert_handler = '[id="polalert"][class="modal"]'
    ingress_port  = '//tr[@id="Ingress Port%s"]/td[2]'
    egress_port   = '//tr[@id="Egress Port%s"]/td[2]'

    ### system status

    Status_page            = '//a[text()="Status"]'
    ports_view             = "//td/input[@onclick=\"window.location.href='/cgi-bin/eventlog?type=ports'\"]"
    environmental_view     = "//td/input[@onclick=\"window.location.href='/cgi-bin/eventlog?type=env'\"]"
    power_supply_view      = "//td/input[@onclick=\"window.location.href='/cgi-bin/eventlog?type=psu'\"]"
    opm_view               = "//td/input[@onclick=\"window.location.href='/cgi-bin/eventlog?type=opm'\"]"
    system_view            = "//td/input[@onclick=\"window.location.href='/cgi-bin/eventlog?type=sys'\"]"
    ports_event            = '[id =portscanvas]'
    environmental_event    = '[id=envcanvas]'
    power_supply_event     = '[id=psucanvas]'
    opm_event              = '[id=opmcanvas]'
    system_event           = '[id=syscanvas]'
    status_page_visibility = '//b[contains(text(),"Environmental")]'
    login_button           = '[id=loginbutton]'
    login_user             = '[name=user]'
    login_passwd           = '[name=passwd]'

    ### opm power levels

    opm_power_level_page  ='//a[text()="Power Levels"]'
    opm_power_levels_page ='//th[contains(text(),"Power (dBm)")]'
    port_status_object    = '//tr//td[@id = "%s"]//tr[%s]'
    status_type_object    = '//tr/td[@id = "%s"]//tr[%s]/td[3]'

    ### User Config

    create_user       = 'modalCreate Userbutton'
    cancel_creation   = 'modalCancelbutton'
    delete_button     = 'modalDeletebutton'
    main_page_visible = '//div[@id="container"]/table/tbody/tr[2]/td[2]/div'
    create_row        = '[id="-1"]''[title="Edit Row"]'
    update_user       = 'modalUpdate Userbutton'
    change_password   = 'passwdbutton'
    user_config_page  = '//a[text()="User Config"]'
    set_password_page = '//a[text()="Set Password"]'
    edit_username     = 'newuserpasswd'
    edit_usertype     = 'newusertype'
    user_canvas       = 'usercanvas'
    new_user_name     = 'newusername'
    new_user_passwd   = 'newuserpasswd'
    new_user_type     = 'newusertype'
    user_editor       = 'usereditor'
    delete_row        = '[title="Delete Row"]'

    ### System Config

    system_switch_name     = '[id =custstring]'
    system_switch_button   = '//input[@id="custstring"]/following-sibling::button'
    system_config_page     = '//a[text()="System Config"]'
    Status_page            = '//a[text()="Status"]'
    Logout_page            = '//a[text()="Logout"]'
    login_page             = '[id=logintable]'
    operation_ok_button    = '[id=modalOKbutton]'
    get_switch_name        = '[id=titlecustomerstring]'
    switch_name            = '[id=custstring]'
    refresh_time_period    = '[id=refreshtime]'
    user_session_timeout   = '[id=usertimeout]'
    admin_session_timeout  = '[id=admintimeout]'
    set_sys_date           = '[id=sys_date]'
    set_sys_time           = '[id=sys_time]'
    session_timeout_button = '//input[@id="admintimeout"]/following-sibling::button'
    refresh_timeout_button = '//input[@id="refreshtime"]/following-sibling::button'
    sys_date_time_button   = '//input[@id="sys_time"]/following-sibling::button'
    remote_syslog_button   = '//input[@id="syslog_facility"]/following-sibling::button'
    reset_network_card     = '//legend[text()="Network Card Reset"]/following-sibling::button'
    power_levels_page      = '//a[text()="Power Levels"]'
    reset_network_button   = '[id=modalResetbutton]'
    reset_network_ok_button= '[id=modalOKbutton]'
    cancel_reset_button    = '[id=modalCancelbutton]'
    sys_config_page        = '[class=content]'
    operation_complete     = '//div[contains(text(),"Operation complete")]'
    sys_page_visibility    = '//button[contains(text(),"Update")]'
    network_card_reset     = '//*[contains(text(),"The network card is nowresetting")]'
    power_page_visibility  = '//th[contains(text(),"Power (dBm)")]'
    powerlevel_element     = '//td[@id="col0"]/table/tbody/tr[8]/td[2]'
    login_page_visibility  = '//h2[contains(text(),"Switch Login")]'
    syslog_address         = '[id=syslog_addr]'
    syslog_facility        = '[id=syslog_facility]'

    

    

    

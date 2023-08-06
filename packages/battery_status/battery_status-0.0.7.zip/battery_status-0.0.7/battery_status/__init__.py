import wmi
import time
import winsound

# Default value of Battery Low Limit
setBatteryLowLimit = 20

# Function to echo sound when battery is lower than setBatteryLowLimit
# parameters: None
# returns: None
def battery_low():
    for i in range(1, 10):
        winsound.Beep(i * 100, 200)

# Function to start battery status notifier
# parameters: None
# returns: None
def battery_status():
    battery = wmi.WMI().Win32_Battery()[0]
    print 'Current battery status is ' + str(battery.EstimatedChargeRemaining)+ '%'
    print 'You will be notified when battery is below ' + str(setBatteryLowLimit) + '%'
    while(1):
        battery = wmi.WMI().Win32_Battery()[0]
        if battery.EstimatedChargeRemaining < setBatteryLowLimit:
            battery_low()
            print 'Battery below ' + str(setBatteryLowLimit) + '%! Connect charger!'
            break
        time.sleep(120)

# Function to check status of battery
# parameters: None
# returns: None
def battery_check_status():
    battery = wmi.WMI().Win32_Battery()[0]
    print 'Your current battery status is ' + str(battery.EstimatedChargeRemaining)+'%'

DC_MODE_OPTIONS = {
    "Auto": 0,
    "Solar Recharging": 1,
    "Car Recharging": 2,
}

DC_ICONS = {
    "Auto": None,
    "MPPT": "mdi:solar-power",
    "DC": "mdi:current-dc",
}

SCREEN_TIMEOUT_OPTIONS = {
    "Never": 0,
    "10 sec": 10,
    "30 sec": 30,
    "1 min": 60,
    "5 min": 300,
    "30 min": 1800,
}

UNIT_TIMEOUT_OPTIONS = {
    "Never": 0,
    "30 min": 30,
    "1 hr": 60,
    "2 hr": 120,
    "4 hr": 240,
    "6 hr": 360,
    "12 hr": 720,
    "24 hr": 1440,
}

UNIT_TIMEOUT_OPTIONS_LIMITED = {
    "Never": 0,
    "30 min": 30,
    "1 hr": 60,
    "2 hr": 120,
    "6 hr": 360,
    "12 hr": 720,
}

AC_TIMEOUT_OPTIONS = {
    "Never": 0,
    "30 min": 30,
    "1 hr": 60,
    "2 hr": 120,
    "4 hr": 240,
    "6 hr": 360,
    "12 hr": 720,
    "24 hr": 1440,
}

AC_TIMEOUT_OPTIONS_LIMITED = {
    "Never": 0,
    "2 hr": 120,
    "4 hr": 240,
    "6 hr": 360,
    "12 hr": 720,
    "24 hr": 1440,
}

DC_TIMEOUT_OPTIONS = {
    "Never": 0,
    "30 min": 30,
    "1 hr": 60,
    "2 hr": 120,
    "4 hr": 240,
    "6 hr": 360,
    "12 hr": 720,
    "24 hr": 1440,
}

DC_TIMEOUT_OPTIONS_LIMITED = {
    "Never": 0,
    "2 hr": 120,
    "4 hr": 240,
    "6 hr": 360,
    "12 hr": 720,
    "24 hr": 1440,
}

DC_CHARGE_CURRENT_OPTIONS = {"4A": 4000, "6A": 6000, "8A": 8000}

MAIN_MODE_OPTIONS = {"Cool": 0, "Heat": 1, "Fan": 2}

FAN_MODE_OPTIONS = {"Low": 0, "Medium": 1, "High": 2}

REMOTE_MODE_OPTIONS = {"Startup": 1, "Standby": 2, "Shutdown": 3}

POWER_SUB_MODE_OPTIONS = {"Max": 0, "Sleep": 1, "Eco": 2, "Manual": 3}

TEMP_SYS_OPTIONS = {
    "Celsius": 0,
    "Fahrenheit": 1,
}

TEMP_DISPLAY_OPTIONS = {
    "Ambient": 0,
    "Outlet": 1,
}

RGB_STATE_OPTIONS = {
    "Follow Screen": 0,
    "Always On": 1,
    "Always Off": 2,
}

AUTO_DRAIN_OPTIONS = {
    "Manual Drainage On": 0,
    "No Drainage On": 1,
    "Manual Drainage Off": 2,
    "No Drainage Off": 3,
}

POWER_SUPPLY_PRIORITY_OPTIONS = {
    "Prioritize power supply": 0,
    "Prioritize power storage": 1,
}

COMBINED_BATTERY_LEVEL = "Battery Level"
COMBINED_BATTERY_LEVEL_F32 = "Battery Level (Precise)"
BATTERY_CHARGING_STATE = "Battery Charging State"

ATTR_DESIGN_CAPACITY = "Design Capacity (mAh)"
ATTR_FULL_CAPACITY = "Full Capacity (mAh)"
SOLAR_AND_ALT_IN_POWER = "Total In Power"
ATTR_REMAIN_CAPACITY = "Remain Capacity (mAh)"
MAIN_DESIGN_CAPACITY = "Main Design Capacity"
ALT_1_IN_POWER = "Alt (1) In Power"
MAIN_FULL_CAPACITY = "Main Full Capacity"
MAIN_REMAIN_CAPACITY = "Main Remain Capacity"
SLAVE_DESIGN_CAPACITY = "Slave Design Capacity"
SLAVE_FULL_CAPACITY = "Slave Full Capacity"
SLAVE_REMAIN_CAPACITY = "Slave Remain Capacity"
SLAVE_N_DESIGN_CAPACITY = "Slave %i Design Capacity"
SLAVE_N_FULL_CAPACITY = "Slave %i Full Capacity"
SLAVE_N_REMAIN_CAPACITY = "Slave %i Remain Capacity"

MAIN_BATTERY_LEVEL = "Main Battery Level"
MAIN_BATTERY_LEVEL_F32 = "Main Battery Level (Precise)"
MAIN_BATTERY_CURRENT = "Main Battery Current"
TOTAL_IN_POWER = "Total In Power"
TOTAL_IN_ENERGY = "Total In Energy"
SOLAR_IN_POWER = "Solar In Power"
SOLAR_1_IN_POWER = "Solar (1) In Power"
SOLAR_2_IN_POWER = "Solar (2) In Power"
SOLAR_1_IN_VOLTS = "Solar (1) In Volts"
SOLAR_2_IN_VOLTS = "Solar (2) In Volts"
SOLAR_1_IN_AMPS = "Solar (1) In Amps"
SOLAR_2_IN_AMPS = "Solar (2) In Amps"
AC_IN_POWER = "AC In Power"
AC_IN_VOLT = "AC In Volts"
DC_BATTERY_POWER = "DC Battery Power"
AC_OUT_VOLT = "AC Out Volts"

TYPE_C_IN_POWER = "Type-C In Power"
SOLAR_IN_CURRENT = "Solar In Current"
SOLAR_IN_VOLTAGE = "Solar In Voltage"
SOLAR_IN_ENERGY = "Solar In Energy"
CHARGE_AC_ENERGY = "Battery Charge Energy from AC"
AC_IN_ENERGY = "AC In Energy"
CHARGE_DC_ENERGY = "Battery Charge Energy from DC"
DISCHARGE_AC_ENERGY = "Battery Discharge Energy to AC"
DISCHARGE_DC_ENERGY = "Battery Discharge Energy to DC"

TOTAL_OUT_POWER = "Total Out Power"
TOTAL_OUT_ENERGY = "Total Out Energy"
TOTAL_ENERGY = "Total Energy"
INVERTER_OUT_ENERGY = "Inverter Out Energy"
TYPEC_OUT_ENERGY = "Type-C Out Energy"
USB_OUT_ENERGY = "USB Out Energy"
PV_HV_ENERGY = "Solar (HV) In Energy"
POWER_INOUT_PORT_ENERGY = "Power In/Out Port Energy"
EXTRA_BATTERY_1_ENERGY = "Extra Battery Port 1 Energy"
EXTRA_BATTERY_2_ENERGY = "Extra Battery Port 2 Energy"
AC_OUT_POWER = "AC Out Power"
DC_OUT_POWER = "DC Out Power"
DC_OUT_VOLTAGE = "DC Out Voltage"
DC_CAR_OUT_POWER = "DC Car Out Power"
DC_ANDERSON_OUT_POWER = "DC Anderson Out Power"

TYPEC_OUT_POWER = "Type-C Out Power"
TYPEC_1_OUT_POWER = "Type-C (1) Out Power"
TYPEC_2_OUT_POWER = "Type-C (2) Out Power"
USB_OUT_POWER = "USB Out Power"
USB_1_OUT_POWER = "USB (1) Out Power"
USB_2_OUT_POWER = "USB (2) Out Power"
USB_3_OUT_POWER = "USB (3) Out Power"

USB_QC_1_OUT_POWER = "USB QC (1) Out Power"
USB_QC_2_OUT_POWER = "USB QC (2) Out Power"

AC_HV_OUT_POWER = "AC High Voltage Out Power"
AC_LV_OUT_POWER = "AC Low Voltage Out Power"
AC_LV_TT30_OUT_POWER = "AC Low Voltage TT30 Out Power"
DC_12V_OUT_POWER = "12V Out Power"
DC_24V_OUT_POWER = "24V Out Power"
POWER_INOUT_PORT = "Power In/Out Port Power"
EXTRA_BATTERY_1_OUT_POWER = "Extra Battery Port 1 Power"
EXTRA_BATTERY_2_OUT_POWER = "Extra Battery Port 2 Power"
PV_HV_POWER = "Solar (HV) In Power"

REMAINING_TIME = "Remaining Time"
CHARGE_REMAINING_TIME = "Charge Remaining Time"
DISCHARGE_REMAINING_TIME = "Discharge Remaining Time"

CYCLES = "Cycles"
SOH = "State of Health"
REAL_SOH = "Real State of Health"

SLAVE_BATTERY_LEVEL = "Slave Battery Level"
SLAVE_N_BATTERY_LEVEL = "Slave %i Battery Level"
SLAVE_N_BATTERY_LEVEL_F32 = "Slave %i Battery Level (Precise)"

SLAVE_BATTERY_TEMP = "Slave Battery Temperature"
SLAVE_N_BATTERY_TEMP = "Slave %i Battery Temperature"

SLAVE_MIN_CELL_TEMP = "Slave Min Cell Temperature"
SLAVE_MAX_CELL_TEMP = "Slave Max Cell Temperature"

SLAVE_N_MIN_CELL_TEMP = "Slave %i Min Cell Temperature"
SLAVE_N_MAX_CELL_TEMP = "Slave %i Max Cell Temperature"

SLAVE_CYCLES = "Slave Cycles"
SLAVE_N_CYCLES = "Slave %i Cycles"
SLAVE_SOH = "Slave State of Health"
SLAVE_N_SOH = "Slave %i State of Health"

SLAVE_IN_POWER = "Slave In Power"
SLAVE_N_IN_POWER = "Slave %i In Power"

SLAVE_OUT_POWER = "Slave Out Power"
SLAVE_N_OUT_POWER = "Slave %i Out Power"

SLAVE_BATTERY_VOLT = "Slave Battery Volts"
SLAVE_MIN_CELL_VOLT = "Slave Min Cell Volts"
SLAVE_MAX_CELL_VOLT = "Slave Max Cell Volts"

SLAVE_N_BATTERY_VOLT = "Slave %i Battery Volts"
SLAVE_N_MIN_CELL_VOLT = "Slave %i Min Cell Volts"
SLAVE_N_MAX_CELL_VOLT = "Slave %i Max Cell Volts"
SLAVE_N_BATTERY_CURRENT = "Slave %i Battery Current"
SLAVE_N_BATTERY_LEVEL_SOC = "Slave %i Battery level SOC"

MAX_CHARGE_LEVEL = "Max Charge Level"
MIN_DISCHARGE_LEVEL = "Min Discharge Level"
BACKUP_RESERVE_LEVEL = "Backup Reserve Level"
AC_CHARGING_POWER = "AC Charging Power"
SCREEN_TIMEOUT = "Screen Timeout"
UNIT_TIMEOUT = "Unit Timeout"
AC_TIMEOUT = "AC Timeout"
DC_TIMEOUT = "DC (12V) Timeout"
DC_CHARGE_CURRENT = "DC (12V) Charge Current"
GEN_AUTO_START_LEVEL = "Generator Auto Start Level"
GEN_AUTO_STOP_LEVEL = "Generator Auto Stop Level"
TIMER_DURATION = "Timer"
TIMER_ENABLED = "Timer Enabled"

POWER = "Power"
CURRENT = "Current"
MAX_CURRENT = "Max Current"
MODE_ON = "On"
BRIGHTNESS = "Brightness"
BEEPER = "Beeper"
USB_ENABLED = "USB Enabled"
AC_ENABLED = "AC Enabled"
BYPASS_AC = "Bypass AC auto start"
DC_ENABLED = "DC (12V) Enabled"
XBOOST_ENABLED = "X-Boost Enabled"
AC_ALWAYS_ENABLED = "AC Always On"
PV_PRIO = "Prio Solar Charging"
BP_ENABLED = "Backup Reserve Enabled"
AUTO_FAN_SPEED = "Auto Fan Speed"
AC_SLOW_CHARGE = "AC Slow Charging"

DC_MODE = "DC Mode"

TEMPERATURE = "Temperature"
BATTERY_TEMP = "Battery Temperature"
MIN_CELL_TEMP = "Min Cell Temperature"
MAX_CELL_TEMP = "Max Cell Temperature"
MIN_MOS_TEMP = "Min MOS Temperature"
MAX_MOS_TEMP = "Max MOS Temperature"
INV_IN_TEMP = "Inverter Inside Temperature"
INV_OUT_TEMP = "Inverter Outside Temperature"
DC_CAR_OUT_TEMP = "DC Temperature"
USB_C_TEMP = "USB C Temperature"
ATTR_MIN_CELL_TEMP = MIN_CELL_TEMP
ATTR_MAX_CELL_TEMP = MAX_CELL_TEMP
ATTR_MIN_MOS_TEMP = MIN_MOS_TEMP
ATTR_MAX_MOS_TEMP = MAX_MOS_TEMP

VOLT = "Volts"
BATTERY_VOLT = "Battery Volts"
MIN_CELL_VOLT = "Min Cell Volts"
MAX_CELL_VOLT = "Max Cell Volts"
ATTR_MIN_CELL_VOLT = MIN_CELL_VOLT
ATTR_MAX_CELL_VOLT = MAX_CELL_VOLT

BATTERY_AMP = "Battery Current"
SLAVE_BATTERY_AMP = "Slave Battery Current"
BATTERY_LEVEL_SOC = "Battery level SOC"

FAN_MODE = "Wind speed"
MAIN_MODE = "Main mode"
REMOTE_MODE = "Remote startup/shutdown"
POWER_SUB_MODE = "Sub-mode"
TEMP_SYS = "Temperature Unit"
TEMP_DISPLAY = "Temperature Display"
RGB_STATE = "Light Strip"
AUTO_DRAIN = "Automatic Drainage"

# Wave 2 additional sensors
PV_INPUT_POWER = "PV Input Power"
PV_CHARGING_POWER = "PV Charging Power"
PV_VOLTAGE = "PV Voltage"
PV_CURRENT = "PV Current"
BUS_VOLTAGE = "Bus Voltage"
AC_FREQUENCY = "AC Input Frequency"
AC_VOLT_RMS = "AC Voltage RMS"
AC_CURR_RMS = "AC Current RMS"
MPPT_WORK = "MPPT Mode"

CONDENSER_FAN_RPM = "Condensing Fan RPM"
EVAP_FAN_RPM = "Evaporator Fan RPM"
FOUR_WAY_VALVE = "Four-way Valve State"
MOTOR_STATUS = "Motor Status"

MOTOR_STATUS_OPTIONS = {
    "Off": 0,
    "Cooling": 1,
    "Heating": 2,
    "Fan": 3,
}

MPPT_WORK_OPTIONS = {
    "Car Charging": 1,
    "Solar Charging": 2,
}


# Smart Meter
SMART_METER_POWER_GLOBAL = "Power Grid Global"
SMART_METER_POWER_L1 = "Power Grid L1"
SMART_METER_POWER_L2 = "Power Grid L2"
SMART_METER_POWER_L3 = "Power Grid L3"
SMART_METER_IN_AMPS_L1 = "Power Grid (L1) In Amps"
SMART_METER_IN_AMPS_L2 = "Power Grid (L2) In Amps"
SMART_METER_IN_AMPS_L3 = "Power Grid (L3) In Amps"
SMART_METER_VOLT_L1 = "Power Grid (L1) Volts"
SMART_METER_VOLT_L2 = "Power Grid (L2) Volts"
SMART_METER_VOLT_L3 = "Power Grid (L3) Volts"
SMART_METER_FLAG_L1 = "Flag L1"
SMART_METER_FLAG_L2 = "Flag L2"
SMART_METER_FLAG_L3 = "Flag L3"
SMART_METER_RECORD_ACTIVE_TODAY = "Lifetime consumption"
SMART_METER_RECORD_ACTIVE_TOTAL = "Lifetime net usage"
SMART_METER_RECORD_REACTIVE_TODAY = "Lifetime injection (2)"
SMART_METER_RECORD_REACTIVE_TOTAL = "Lifetime injection"
SMART_METER_RECORD_ACTIVE_TODAY_L1 = "L1 Lifetime net usage"
SMART_METER_RECORD_ACTIVE_TODAY_L2 = "L2 Lifetime net usage"
SMART_METER_RECORD_ACTIVE_TODAY_L3 = "L3 Lifetime net usage"

# Stream AC
STREAM_POWER_AC = (
    "Power AC"  # <0 import from home to battery / >0 export from battery to home
)
STREAM_POWER_VOL = (
    "Power Volts"  # <0 import from home to battery / >0 export from battery to home
)
STREAM_POWER_AMP = "Power In Amps"
STREAM_POWER_AC_SYS = (
    "Power AC SYS"  # <0 import from home to battery / >0 export from battery to home
)
STREAM_POWER_PV_1 = "Power PV 1"
STREAM_POWER_PV_2 = "Power PV 2"
STREAM_POWER_PV_3 = "Power PV 3"
STREAM_POWER_PV_4 = "Power PV 4"
STREAM_IN_AMPS_PV_1 = "Power PV1 In Amps"
STREAM_IN_AMPS_PV_2 = "Power PV2 In Amps"
STREAM_IN_VOL_PV_1 = "Power PV1 Volts"
STREAM_IN_VOL_PV_2 = "Power PV2 Volts"
STREAM_POWER_PV_SUM = "Power PV Sum"
STREAM_GET_SYS_LOAD = "Power Sys Load"  # powGetSysLoad
STREAM_GET_SYS_LOAD_FROM_BP = "Power Sys Load From Battery"  # powGetSysLoadFromBp
STREAM_GET_SYS_LOAD_FROM_GRID = "Power Sys Load From Grid"  # powGetSysLoadFromGrid
STREAM_GET_SYS_LOAD_FROM_PV = "Power Sys Load From PV"  # powGetSysLoadFromPv
STREAM_GET_SCHUKO1 = "Power SCHUKO1"  # powGetSchuko1
STREAM_GET_SCHUKO2 = "Power SCHUKO2"  # powGetSchuko2
STREAM_POWER_GRID = "Power Grid"  # power from smart meter or shelly
STREAM_POWER_BATTERY = "Power Battery"  # <0 discharge battery / >0 charge batterie
STREAM_POWER_BATTERY_SOC = (
    "Power Battery SOC"  # <0 discharge battery / >0 charge batterie
)
STREAM_BATTERY_LEVEL = "Battery Level"
STREAM_DESIGN_CAPACITY = "Design Capacity"
STREAM_FULL_CAPACITY = "Full Capacity"
STREAM_REMAIN_CAPACITY = "Remain Capacity"
STREAM_STR_BATTERY_LEVEL = "Battery Level %s "
STREAM_STR_DESIGN_CAPACITY = "Design Capacity %s "
STREAM_STR_FULL_CAPACITY = "Full Capacity %s "
STREAM_STR_REMAIN_CAPACITY = "Remain Capacity %s "
STREAM_IN_POWER = "In Power"
STREAM_STR_IN_POWER = "In Power %s"
STREAM_OUT_POWER = "Out Power"
STREAM_STR_OUT_POWER = "Out Power %s"

ACCU_CHARGE_CAP = "Cumulative Capacity Charge (mAh)"
ACCU_CHARGE_ENERGY = "Cumulative Energy Charge (Wh)"
ACCU_DISCHARGE_CAP = "Cumulative Capacity Discharge (mAh)"
ACCU_DISCHARGE_ENERGY = "Cumulative Energy Discharge (Wh)"

SLAVE_N_ACCU_CHARGE_CAP = "Slave %i Cumulative Capacity Charge (mAh)"
SLAVE_N_ACCU_CHARGE_ENERGY = "Slave %i Cumulative Energy Charge (Wh)"
SLAVE_N_ACCU_DISCHARGE_CAP = "Slave %i Cumulative Capacity Discharge (mAh)"
SLAVE_N_ACCU_DISCHARGE_ENERGY = "Slave %i Cumulative Energy Discharge (Wh)"

# Smart Home Pannel 2

BATTERIE_STATUS = "Batterie Status"

BATTERIE_STATUS_OPTIONS = {"No operation": 0, "Enabled": 1, "Disabled": 2}

BATTERIE_FORCE_CHARGE = "Batterie Force Charge"

BATTERIE_FORCE_CHARGE_OPTIONS = {"Off": "FORCE_CHARGE_OFF", "On": "FORCE_CHARGE_ON"}

SMART_BACKUP_MODE = "Economic Mode"

SMART_BACKUP_MODE_OPTIONS = {"None": 0, "TOU": 1, "Self-service": 2, "Timed task": 3}

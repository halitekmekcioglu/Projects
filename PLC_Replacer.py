
import math

from thebox import mainloop, sdb
import os
import time
from datetime import datetime

import subprocess


# Each element of the list is a dictionary:
'''
{
   "from": "MB_Tag_name", 
   "from_type": sdb.DT_DINT,
   "from_count" : 1,
   "to": "MQTT_Tag_Name",
   "coeff": 1000,
   "oper": "/",
   "to_type": "TELEDOT",
   "samp_mode": "EVENT",
}
'''
mb_data_to_mqtt_telem = [

{"from": "DailyPowerYields_5003_U16x04_11", "from_type": sdb.DT_UINT, "from_count": 1, "to": "TELEMETRY_P_Invertor_11_Yields_DailyPower", "coeff": 10, "oper": "/","samp_mode": "POLLING", "samp_rate": 60},
{"from": "TotalPowerYields_5004_U32x04_11", "from_type": sdb.DT_UDINT, "from_count": 1, "to": "TELEMETRY_P_Invertor_11_Yields_TotalPower", "coeff": 1, "oper": "/","samp_mode": "POLLING", "samp_rate": 60},
{"from": "TotalRunningTime_5006_U32x04_11", "from_type": sdb.DT_UDINT, "from_count": 1, "to": "TELEMETRY_P_Invertor_11_Time_TotalRunningTime", "coeff": 1, "oper": "/","samp_mode": "POLLING", "samp_rate": 60},
{"from": "InternalTemp_5008_S16x04_11", "from_type": sdb.DT_INT, "from_count": 1, "to": "TELEMETRY_P_Invertor_11_Temp_InternalTemp", "coeff": 10, "oper": "/","samp_mode": "POLLING", "samp_rate": 60},
{"from": "TotalApparentP_5009_U32x04_11", "from_type": sdb.DT_UDINT, "from_count": 1, "to": "TELEMETRY_P_Invertor_11_Power_TotalApparent", "coeff": 1, "oper": "/","samp_mode": "POLLING", "samp_rate": 60},
{"from": "MPPT1Voltage_5011_U16x04_11", "from_type": sdb.DT_UINT, "from_count": 1, "to": "TELEMETRY_P_Invertor_11_Voltage_MPPT1", "coeff": 10, "oper": "/","samp_mode": "POLLING", "samp_rate": 60},
{"from": "MPPT1Current_5012_U16x04_11", "from_type": sdb.DT_UINT, "from_count": 1, "to": "TELEMETRY_P_Invertor_11_Current_MPPT1", "coeff": 10, "oper": "/","samp_mode": "POLLING", "samp_rate": 60},
{"from": "TotalDCPower_5017_U32x04_11", "from_type": sdb.DT_UDINT, "from_count": 1, "to": "TELEMETRY_P_Invertor_11_Power_TotalDC", "coeff": 1, "oper": "/","samp_mode": "POLLING", "samp_rate": 60},
{"from": "PhaseAvoltage_5019_U16x04_11", "from_type": sdb.DT_UINT, "from_count": 1, "to": "TELEMETRY_P_Invertor_11_Voltage_APhase", "coeff": 10, "oper": "/","samp_mode": "POLLING", "samp_rate": 60},
{"from": "PhaseBvoltage_5020_U16x04_11", "from_type": sdb.DT_UINT, "from_count": 1, "to": "TELEMETRY_P_Invertor_11_Voltage_BPhase", "coeff": 10, "oper": "/","samp_mode": "POLLING", "samp_rate": 60},
{"from": "PhaseCvoltage_5021_U16x04_11", "from_type": sdb.DT_UINT, "from_count": 1, "to": "TELEMETRY_P_Invertor_11_Voltage_CPhase", "coeff": 10, "oper": "/","samp_mode": "POLLING", "samp_rate": 60},
{"from": "PhaseACurrent_5022_U16x04_11", "from_type": sdb.DT_UINT, "from_count": 1, "to": "TELEMETRY_P_Invertor_11_Current_APhase", "coeff": 10, "oper": "/","samp_mode": "POLLING", "samp_rate": 60},
{"from": "PhaseBCurrent_5023_U16x04_11", "from_type": sdb.DT_UINT, "from_count": 1, "to": "TELEMETRY_P_Invertor_11_Current_BPhase", "coeff": 10, "oper": "/","samp_mode": "POLLING", "samp_rate": 60},
{"from": "PhaseCCurrent_5024_U16x04_11", "from_type": sdb.DT_UINT, "from_count": 1, "to": "TELEMETRY_P_Invertor_11_Current_CPhase", "coeff": 10, "oper": "/","samp_mode": "POLLING", "samp_rate": 60},
{"from": "Analysor_Janitza_Power_TotalActive", "from_type": sdb.DT_REAL, "from_count": 1, "to": "TELEMETRY_P_Analysor_Janitza_Power_TotalActive", "coeff": 1, "oper": "/","samp_mode": "POLLING", "samp_rate": 60},
{"from": "Analysor_Janitza_Consumption_RealEnergyL1L3", "from_type": sdb.DT_REAL, "from_count": 1, "to": "TELEMETRY_P_Analysor_Janitza_Consumption_RealEnergyL1L3", "coeff": 1, "oper": "/","samp_mode": "POLLING", "samp_rate": 60},
{"from": "Analysor_Janitza_Generation_RealEnergyL1L3", "from_type": sdb.DT_REAL, "from_count": 1, "to": "TELEMETRY_P_Analysor_Janitza_Generation_RealEnergyL1L3", "coeff": 1000, "oper": "/","samp_mode": "POLLING", "samp_rate": 60},
{"from": "Analysor_Vamp57_Power_TotalActive", "from_type": sdb.DT_INT, "from_count": 1, "to": "TELEMETRY_P_Analysor_Vamp57_Power_TotalActive", "coeff": 1, "oper": "/","samp_mode": "POLLING", "samp_rate": 60}


]


# Useful variable
thebox_mqtt_telem_trigger = None
timer_10m = None
# Time between each MQTT send order (in ms)
# Each data packet must be under 128kB (AWS broker limit)

MQTT_SEND_INTERVAL = 60000

usleep = lambda x: time.sleep(x / 1000000.0)


# FCT for uptimelogging
def logger():
    time.sleep(5)
    cmd_list = ['uname -r', 'uptime']
    out = []
    err = []
    for cmd in cmd_list:
        args = cmd.split()
        proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (stdoutdata, stderrdata) = proc.communicate()
        out.append(stdoutdata)
        err.append(stderrdata)
    return out, err


def synchro_15sec():
    date_time_obj = (datetime.now()).time()
    while date_time_obj.second % 15:
        usleep(2000)
        date_time_obj = (datetime.now()).time()


# Coefficient factor
def coeff_factor(base_value, operator="/", coeff=1):
    if not operator:
        operator = "/"
    if not coeff:
        coeff = 1

    if operator == "*":
        base_value = base_value * coeff
    elif operator == "/":
        base_value = base_value / coeff

    return base_value


def write_mb_val_to_mqtt(mqtt_type, mqtt_tag, mb_val, mb_qual):
    if not mqtt_type:
        mqtt_type = "TELEDOT"
    if mqtt_type == "TELEDOT":
        mqtt_tag.write({'val': mb_val,
                        'qual': mb_qual,
                        'addreq': 1})
    else:
        mqtt_tag.write(mb_val)


# convert real to dint
def real_to_dint(real_val):
    # filter the nan case
    if math.isnan(float(real_val)):
        print("REAL is NaN, set the DINT to 0")
        return 0

    temp_val = int(float(real_val))
    # check the value to ensure we have a dint value
    if temp_val > 2147483647:
        print("REAL value is bigger than DINT max (DINT " + str(temp_val) + ")")
        temp_val = 2147483647
    elif temp_val < -2147483648:
        print("REAL value is smaller than DINT min (DINT " + str(temp_val) + ")")
        temp_val = -2147483648
    return temp_val


def udint_to_dint(udint_val):
    if udint_val > 2147483647:

        print( " UDINT value is bigger than DINT max (UDINT " + str(udint_val) + ")")
        udint_val = 2147483647
    return udint_val


def dint_to_uint(dint_val):
    if dint_val > 65535:
        print("DINT value is greater than the UINT max (DINT " + str(dint_val) + ")")
        dint_val = 65535
    elif dint_val < 0:
        print("DINT value is smaller than the UINT min  (DINT " + str(dint_val) + ")")
        dint_val = 0
    return dint_val


def dint_to_int(dint_val):
    if dint_val > 32767:
        print("DINT value is greater than the INT max (DINT " + str(dint_val) + ")")
        dint_val = 32767
    elif dint_val < -32768:
        print("DINT value is smaller than the INT min  (DINT " + str(dint_val) + ")")
        dint_val = -32768
    return dint_val


def main():
    print("============Module Start============")

    # start the needed modules
    os.system("monit stop all")
    time.sleep(5)
    os.system("monit restart server")
    time.sleep(5)
    # create a client connection
    c = sdb.Client('PLC Replacer')
    while True:
        try:
            c.connect()
            break
        except:
            print("Wait for the thebox server to be online")
            time.sleep(1000000)

    synchro_15sec()
    os.system("monit restart moduleMqtt")
    os.system("monit restart moduleTelemetry")
    os.system("monit restart moduleCommand")
    os.system("monit restart moduleModbusMaster")
    # prepare the main loop, and hook the client on it
    loop = mainloop.Mainloop()
    c.register_on_mainloop(loop)

    #print(logger()[0][1])

    # Get the global variable
    global  mb_data_to_mqtt_telem

    # Fct to convert Modbus INT/UINT/DINT to MQTT Teledot (DINT Data)
    def isr_def_modbus_to_mqtt_telem(tag_modbus, data_cb):
        all_val_mb = tag_modbus.read()
        all_mqtt_tag = data_cb["mqtt_tag"]
        oper = data_cb["oper"]
        coeff = data_cb["coeff"]
        mqtt_tag_type = data_cb["mqtt_tag_type"]
        # single data point (not array)
        if not isinstance(all_val_mb, list):
            all_val_mb = [all_val_mb]
        for idx in range(0, len(all_val_mb)):
            val_mb = all_val_mb[idx]
            mqtt_tag = all_mqtt_tag[idx]
            val_mb = coeff_factor(val_mb, oper, coeff)
            write_mb_val_to_mqtt(mqtt_tag_type, mqtt_tag, val_mb, tag_modbus.get_quality())

    # Fct to convert Modbus REAL to MQTT Teledot (DINT Data)
    def isr_modbus_real_to_mqtt_telem(tag_modbus, data_cb):
        all_val_mb = tag_modbus.read()
        all_mqtt_tag = data_cb["mqtt_tag"]
        oper = data_cb["oper"]
        coeff = data_cb["coeff"]
        # single data point (not array)
        if not isinstance(all_val_mb, list):
            all_val_mb = [all_val_mb]
        for idx in range(0, len(all_val_mb)):
            val_mb = all_val_mb[idx]
            mqtt_tag = all_mqtt_tag[idx]
            val_mb = coeff_factor(val_mb, oper, coeff)
            val_mb = real_to_dint(val_mb)
            write_mb_val_to_mqtt(mqtt_tag_type, mqtt_tag, val_mb, tag_modbus.get_quality())

    # Fct to convert Modbus UDINT to MQTT Teledot (UDINT Data)
    def isr_modbus_udint_to_mqtt_telem(tag_modbus, data_cb):
        all_val_mb = tag_modbus.read()
        all_mqtt_tag = data_cb["mqtt_tag"]
        oper = data_cb["oper"]
        coeff = data_cb["coeff"]
        # single data point (not array)
        if not isinstance(all_val_mb, list):
            all_val_mb = [all_val_mb]
        for idx in range(0, len(all_val_mb)):
            val_mb = all_val_mb[idx]
            mqtt_tag = all_mqtt_tag[idx]
            val_mb = coeff_factor(val_mb, oper, coeff)
            val_mb = udint_to_dint(val_mb)
            write_mb_val_to_mqtt(mqtt_tag_type, mqtt_tag, val_mb, tag_modbus.get_quality())


    # Cyclic timer to send data to the broker
    def on_top_10m(__loop, __next_date):
        global timer_10m, thebox_mqtt_telem_trigger, MQTT_SEND_INTERVAL
        # rearm the timer
        __next_date += 1000 * MQTT_SEND_INTERVAL
        __d = __next_date - time.time() * 1000000
        timer_10m = __loop.schedule(on_top_10m, __d, __next_date)

        # Trigger the MQTT sending
        try:
            thebox_mqtt_telem_trigger.write(1)
            #print("==>Send data to the broker!")
        except:
            print("No TELEMETRY_P_TxReq in server")

    # custom polling function
    def on_top_user(__loop, cb_data_param):
        cb_data_param["next_date"] += 1000 * cb_data_param["samp_rate"]
        __d = cb_data_param["next_date"] - time.time() * 1000000
        __loop.schedule(callback=on_top_user, delay_us=__d, callback_data=cb_data_param)
        cb_data_param["isr"](cb_data_param["mb_tag"], cb_data_param)

    # Modbus to MQTT Telemetry management
    for dict in mb_data_to_mqtt_telem:
        err_loop = 0
        mb_tag_name = ""
        mb_tag_type = ""
        mb_tag_len = ""
        mqtt_tag_name = ""
        coeff_fact = None
        coeff_oper = None
        mqtt_tag_type = None
        samp_mode = "EVENT"
        samp_rate = 60
        # get the dict element
        try:
            mb_tag_name = dict["from"]
            mb_tag_type = dict["from_type"]
            mb_tag_len = dict["from_count"]
            mqtt_tag_name = dict["to"]
            if "oper" in dict:
                coeff_oper = dict["oper"]
            if "coeff" in dict:
                coeff_fact = dict["coeff"]
            if "to_type" in dict:
                mqtt_tag_type = dict["to_type"]
            if "samp_mode" in dict:
                samp_mode = dict["samp_mode"]
                if "samp_rate" in dict:
                    samp_rate = dict["samp_rate"]
        except:
            print("Error element", dict, "misconfigured")
            exit(1)
        # get the thebox tag
        while True:
            try:
                thebox_tag_mb = c.get_tag_by_name(mb_tag_name)
                # Modbus tag is an array?
                if mb_tag_len == 1:
                    thebox_tag_mqtt = [c.get_tag_by_name(mqtt_tag_name)]
                else:
                    thebox_tag_mqtt = []
                    for idx in range(0, mb_tag_len):
                        temp_name = mqtt_tag_name + "_" + str(idx)
                        thebox_tag_mqtt.append(c.get_tag_by_name(temp_name))
                break
            except:
                print("Wait for tags of ", dict, "to be created on the server")
                usleep(1000000)
                err_loop += 1
            # Too much error, tag is still not created stop here
            if err_loop == 10:
                print("Some Tags of ", dict, "are not in the server")
                exit(1)


        # Set the interruption on modbus data change
        cb_data = {
            "mqtt_tag": thebox_tag_mqtt,
            "coeff": coeff_fact,
            "oper": coeff_oper,
            "mqtt_tag_type": mqtt_tag_type,
        }
        if samp_mode == "EVENT":
            if mb_tag_type == sdb.DT_REAL:
                thebox_tag_mb.on_event(isr_modbus_real_to_mqtt_telem, event=sdb.EVENT_CHANGE, callback_data=cb_data)
            elif mb_tag_type == sdb.DT_UDINT:
                thebox_tag_mb.on_event(isr_modbus_udint_to_mqtt_telem, event=sdb.EVENT_CHANGE, callback_data=cb_data)
            elif mb_tag_type == sdb.DT_INT or mb_tag_type == sdb.DT_UINT or mb_tag_type == sdb.DT_DINT:
                thebox_tag_mb.on_event(isr_def_modbus_to_mqtt_telem, event=sdb.EVENT_CHANGE, callback_data=cb_data)
            else:
                print("Unsupported data type for", dict)
        else:
            cb_data["samp_rate"] = samp_rate*1000
            cb_data["mb_tag"] = thebox_tag_mb
            if mb_tag_type == sdb.DT_REAL:
                cb_data["isr"] = isr_modbus_real_to_mqtt_telem
            elif mb_tag_type == sdb.DT_UDINT:
                cb_data["isr"] = isr_modbus_udint_to_mqtt_telem
            elif mb_tag_type == sdb.DT_INT or mb_tag_type == sdb.DT_UINT or mb_tag_type == sdb.DT_DINT:
                cb_data["isr"] = isr_def_modbus_to_mqtt_telem
            else:
                print("Unsupported data type for", dict)
            cb_data["next_date"] = time.time() * 1000000 + cb_data["samp_rate"] * 1000
            test = loop.schedule(callback=on_top_user, delay_us=(1000 * cb_data["samp_rate"]), callback_data=cb_data)


    # Get the MQTT Telemetry trigger
    global thebox_mqtt_telem_trigger, MQTT_SEND_INTERVAL
    thebox_mqtt_telem_trigger = c.get_tag_by_name("TELEMETRY_P_TxReq")

    # periodic timer initialisation
    __next_date = time.time() * 1000000 + MQTT_SEND_INTERVAL * 1000
    global timer_10m
    timer_10m = loop.schedule(on_top_10m, 1000 * MQTT_SEND_INTERVAL, __next_date)

    # start the loop
    loop.run()




if __name__ == '__main__':
    main()

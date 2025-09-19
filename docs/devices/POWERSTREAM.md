## POWERSTREAM

*Sensors*
- Solar 1 Watts (`20_1.pv1InputWatts`)
- Solar 1 Input Potential (`20_1.pv1InputVolt`)
- Solar 1 Op Potential (`20_1.pv1OpVolt`)
- Solar 1 Current (`20_1.pv1InputCur`)
- Solar 1 Temperature (`20_1.pv1Temp`)
- Solar 1 Relay Status (`20_1.pv1RelayStatus`)
- Solar 1 Error Code (`20_1.pv1ErrCode`)   _(disabled)_
- Solar 1 Warning Code (`20_1.pv1WarnCode`)   _(disabled)_
- Solar 1 Status (`20_1.pv1Status`)   _(disabled)_
- Solar 2 Watts (`20_1.pv2InputWatts`)
- Solar 2 Input Potential (`20_1.pv2InputVolt`)
- Solar 2 Op Potential (`20_1.pv2OpVolt`)
- Solar 2 Current (`20_1.pv2InputCur`)
- Solar 2 Temperature (`20_1.pv2Temp`)
- Solar 2 Relay Status (`20_1.pv2RelayStatus`)
- Solar 2 Error Code (`20_1.pv2ErrCode`)   _(disabled)_
- Solar 2 Warning Code (`20_1.pv2WarningCode`)   _(disabled)_
- Solar 2 Status (`20_1.pv2Status`)   _(disabled)_
- Battery Type (`20_1.bpType`)   _(disabled)_
- Battery Charge (`20_1.batSoc`)
- Battery Input Watts (`20_1.batInputWatts`)
- Battery Input Potential (`20_1.batInputVolt`)
- Battery Op Potential (`20_1.batOpVolt`)
- Battery Input Current (`20_1.batInputCur`)
- Battery Temperature (`20_1.batTemp`)
- Charge Time (`20_1.chgRemainTime`)
- Discharge Time (`20_1.dsgRemainTime`)
- Battery Error Code (`20_1.batErrCode`)   _(disabled)_
- Battery Warning Code (`20_1.batWarningCode`)   _(disabled)_
- Battery Status (`20_1.batStatus`)   _(disabled)_
- LLC Input Potential (`20_1.llcInputVolt`)   _(disabled)_
- LLC Op Potential (`20_1.llcOpVolt`)   _(disabled)_
- LLC Temperature (`20_1.llcTemp`)
- LLC Error Code (`20_1.llcErrCode`)   _(disabled)_
- LLC Warning Code (`20_1.llcWarningCode`)   _(disabled)_
- LLC Status (`20_1.llcStatus`)   _(disabled)_
- Inverter On/Off Status (`20_1.invOnOff`)
- Inverter Output Watts (`20_1.invOutputWatts`)
- Inverter Output Potential (`20_1.invInputVolt`)   _(disabled)_
- Inverter Op Potential (`20_1.invOpVolt`)
- Inverter Output Current (`20_1.invOutputCur`)
- Inverter Frequency (`20_1.invFreq`)
- Inverter Temperature (`20_1.invTemp`)
- Inverter Relay Status (`20_1.invRelayStatus`)
- Inverter Error Code (`20_1.invErrCode`)   _(disabled)_
- Inverter Warning Code (`20_1.invWarnCode`)   _(disabled)_
- Inverter Status (`20_1.invStatus`)   _(disabled)_
- Other Loads (`20_1.permanentWatts`)
- Smart Plug Loads (`20_1.dynamicWatts`)
- Rated Power (`20_1.ratedPower`)
- Base Load (`20_4.h2BaseLoad`)
- Smart Plug Watts + (`20_4.h2PowerPlugsPos`)
- Grid Watts (`20_4.h2GridWatt45`)
- Smart Plug Watts - (`20_4.h2PowerPlugsNeg`)
- WiFi RSSI (`20_4.h2WifiRssi`)
- Lower Battery Limit (`20_1.lowerLimit`)   _(disabled)_
- Upper Battery Limit (`20_1.upperLimit`)   _(disabled)_
- Wireless Error Code (`20_1.wirelessErrCode`)   _(disabled)_
- Wireless Warning Code (`20_1.wirelessWarnCode`)   _(disabled)_
- LED Brightness (`20_1.invBrightness`)   _(disabled)_
- Heartbeat Frequency (`20_1.heartbeatFrequency`)   _(disabled)_
- Feed-in Priority (`20_1.feedPriority`)
- PV1 Today Energy Total (`254_32.watthPv1`)
- PV2 Today Energy Total (`254_32.watthPv2`)
- From Battery Today Energy Total (`254_32.watthFromBattery`)
- To Battery Today Energy Total (`254_32.watthToBattery`)
- To Smart Plugs Today Energy Total (`254_32.watthToSmartPlugs`)
- Total Energy Report (`32_11.watth`)
- Status

*Switches*
- Feed-in Priority (`20_1.feedPriority` -> `{"from": "HomeAssistant", "id": "999972400", "version": "1.0", "sn": "SN", "cmdCode": "WN511_SET_VALUE_PACK", "params": {"value": "VALUE"}}`)

*Sliders (numbers)*
- Min Discharge Level (`20_1.lowerLimit` -> `{"from": "HomeAssistant", "id": "999966463", "version": "1.0", "sn": "SN", "cmdCode": "WN511_SET_BAT_LOWER_PACK", "params": {"lowerLimit": "VALUE"}}` [0 - 100])
- Max Charge Level (`20_1.upperLimit` -> `{"from": "HomeAssistant", "id": "999939639", "version": "1.0", "sn": "SN", "cmdCode": "WN511_SET_BAT_UPPER_PACK", "params": {"upperLimit": "VALUE"}}` [0 - 100])
- Brightness (`20_1.invBrightness` -> `{"from": "HomeAssistant", "id": "999972604", "version": "1.0", "sn": "SN", "cmdCode": "WN511_SET_BRIGHTNESS_PACK", "params": {"brightness": "VALUE"}}` [0 - 1023])
 - Custom load power settings (`20_1.permanentWatts` -> `{"from": "HomeAssistant", "id": "999931738", "version": "1.0", "sn": "SN", "cmdCode": "WN511_SET_PERMANENT_WATTS_PACK", "params": {"permanentWatts": "VALUE"}}` [0 - 800])

*Selects*
- Power supply mode (`20_1.supplyPriority` -> `{"from": "HomeAssistant", "id": "999968721", "version": "1.0", "sn": "SN", "cmdCode": "WN511_SET_SUPPLY_PRIORITY_PACK", "params": {"includePlug": true}}` [Prioritize power supply (0), Prioritize power storage (1)])



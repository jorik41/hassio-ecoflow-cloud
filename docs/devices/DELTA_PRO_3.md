## DELTA_PRO_3

*Sensors*
- Main Battery Level (`bmsBattSoc`)
- Main Design Capacity (`bmsDesignCap`)   _(disabled)_
- State of Health (`bmsBattSoh`)
- Charge Remaining Time (`bmsChgRemTime`)
- Discharge Remaining Time (`bmsDsgRemTime`)
- Min Cell Temperature (`bmsMinCellTemp`)   _(disabled)_
- Max Cell Temperature (`bmsMaxCellTemp`)   _(disabled)_
- Min MOS Temperature (`bmsMinMosTemp`)   _(disabled)_
- Max MOS Temperature (`bmsMaxMosTemp`)   _(disabled)_
- Battery Volts (`bmsBattVol`)   _(disabled)_
- Min Cell Volts (`bmsMinCellVol`)   _(disabled)_
- Max Cell Volts (`bmsMaxCellVol`)   _(disabled)_
- Main Battery Current (`bmsBattAmp`)   _(disabled)_
- Cycles (`cycles`)
- Main Full Capacity (`bmsFullCap`)   _(disabled)_
- Main Remain Capacity (`bmsRemainCap`)   _(disabled)_
- Battery Level (`cmsBattSoc`)
- State of Health (`cmsBattSoh`)
- Total In Power (`powInSumW`)
- Total Out Power (`powOutSumW`)
- AC In Power (`powGetAcIn`)
- AC Out Power (`powGetAc`)
- Solar In Power (`powGetPvL`)
- Solar (HV) In Power (`powGetPvH`)
- AC High Voltage Out Power (`powGetAcHvOut`)
- Type-C (1) Out Power (`powGetTypec1`)
- Type-C (2) Out Power (`powGetTypec2`)
- 12V Out Power (`powGet12v`)
- 24V Out Power (`powGet24v`)
- 12V DC Output Voltage (`powGet12vVol`)
- 24V DC Output Voltage (`powGet24vVol`)
- AC Low Voltage Out Power (`powGetAcLvOut`)
- AC Low Voltage TT30 Out Power (`powGetAcLvTt30Out`)
- Power In/Out Port Power (`powGet5p8`)
- USB QC (1) Out Power (`powGetQcusb1`)
- USB QC (2) Out Power (`powGetQcusb2`)
- Extra Battery Port 1 Power (`powGet4p81`)
- Extra Battery Port 2 Power (`powGet4p82`)
- Max Charge Level (`cmsMaxChgSoc`)
- Min Discharge Level (`cmsMinDsgSoc`)
- AC In Energy (`powGetAcIn`)
- Solar In Energy (`powGetPvL`)
- Solar (HV) In Energy (`powGetPvH`)
- Power In/Out Port Energy (`powGet5p8`)
- Extra Battery Port 1 Energy (`powGet4p81`)
- Extra Battery Port 2 Energy (`powGet4p82`)
- Battery Discharge Energy to AC (`powGetAc`)
- Total In Energy (`powInSumEnergy`)
- Total Out Energy (`powOutSumEnergy`)
- Battery Charge Energy from AC (`acInEnergyTotal`)
- Battery Discharge Energy to AC (`acOutEnergyTotal`)
- Solar In Energy (`pvInEnergyTotal`)
- Battery Discharge Energy to DC (`dcOutEnergyTotal`)
- AC Input Frequency (`acOutFreq`)
- AC In Volts (`plugInInfoAcInVol`)
- AC Input Current (`plugInInfoAcInAmp`)
- AC Out Volts (`plugInInfoAcOutVol`)
- PV Voltage (`plugInInfoPvHChgVolMax`)   _(disabled)_
- PV Current (`plugInInfoPvHChgAmpMax`)   _(disabled)_
- PV Voltage (`plugInInfoPvLChgVolMax`)   _(disabled)_
- PV Current (`plugInInfoPvLChgAmpMax`)   _(disabled)_
- Solar HV Input Voltage (`powGetPvHVol`)
- Solar LV Input Voltage (`powGetPvLVol`)
- Solar In Current (`powGetPvHAmp`)
- Solar In Current (`powGetPvLAmp`)
- Charge Remaining Time (`cmsChgRemTime`)
- Discharge Remaining Time (`cmsDsgRemTime`)
- Status
- Status (Scheduled)

*Switches*
- Beeper (`enBeep` -> `{"sn": "SN", "cmdId": 17, "dirDest": 1, "dirSrc": 1, "cmdFunc": 254, "dest": 2, "params": {"cfgBeepEn": "VALUE"}}`)
- DC (12V) Enabled (`flowInfo12v` -> `_ command not available _`)
- AC Enabled (`flowInfoAcHvOut` -> `_ command not available _`)
- X-Boost Enabled (`xboostEn` -> `_ command not available _`)

*Sliders (numbers)*
- Max Charge Level (`cmsMaxChgSoc` -> `_ command not available _` [50 - 100])
- Min Discharge Level (`cmsMinDsgSoc` -> `_ command not available _` [0 - 30])
- Backup Reserve Level (`energyBackupStartSoc` -> `{"sn": "SN", "cmdId": 17, "dirDest": 1, "dirSrc": 1, "cmdFunc": 254, "dest": 2, "params": {"cfgEnergyBackup": {"energyBackupStartSoc": 6666, "energyBackupEn": true}}}` [5 - 100])
- Generator Auto Start Level (`cmsOilOnSoc` -> `{"sn": "SN", "cmdId": 17, "dirDest": 1, "dirSrc": 1, "cmdFunc": 254, "dest": 2, "params": {"cfgCmsOilOnSoc": "VALUE"}}` [0 - 30])
- Generator Auto Stop Level (`cmsOilOffSoc` -> `{"sn": "SN", "cmdId": 17, "dirDest": 1, "dirSrc": 1, "cmdFunc": 254, "dest": 2, "params": {"cfgCmsOilOffSoc": "VALUE"}}` [50 - 100])
- AC Charging Power (`plugInInfoAcInChgPowMax` -> `_ command not available _` [400 - 2900])

*Selects*



## Delta_Pro_3

*Sensors*
- Main Battery Level (`bmsBattSoc`)
- Main Design Capacity (`bmsDesignCap`)   _(disabled)_
- Battery Level (`cmsBattSoc`)
- Total In Power (`powInSumW`)
- Total Out Power (`powOutSumW`)
- AC In Power (`powGetAcIn`)
- AC Out Power (`powGetAc`)
- Solar In Power (`powGetPvL`)
- Solar (HV) In Power (`powGetPvH`)
- Grid Power (`powGetAcHvOut`)
- Type-C (1) Out Power (`powGetTypec1`)
- Type-C (2) Out Power (`powGetTypec2`)
- 12V Out Power (`powGet12v`)
- 24V Out Power (`powGet24v`)
- AC Low Voltage Out Power (`powGetAcLvOut`)
- AC Low Voltage TT30 Out Power (`powGetAcLvTt30Out`)
- Power In/Out Port Power (`powGet5p8`)
- USB QC (1) Out Power (`powGetQcusb1`)
- USB QC (2) Out Power (`powGetQcusb2`)
- Extra Battery Port 1 Power (`powGet4p81`)
- Extra Battery Port 2 Power (`powGet4p82`)
- Charge Remaining Time (`cmsChgRemTime`)
- Discharge Remaining Time (`cmsDsgRemTime`)
- AC In Energy (`powGetAcIn`)
- Solar In Energy (`powGetPvL`)
- Solar (HV) In Energy (`powGetPvH`)
- Power In/Out Port Energy (`powGet5p8`)
- Extra Battery Port 1 Energy (`powGet4p81`)
- Extra Battery Port 2 Energy (`powGet4p82`)
- Battery Discharge Energy to AC (`powGetAc`)
- Total In Energy (`powInSumW`)
- Total Out Energy (`powOutSumW`)
- Total Energy (`powInSumW` + `powOutSumW`)


*Switches*
- Beeper (`cfgBeepEn`)
- DC (12V) Enabled (`cfgDc12vOutOpen`)
- AC Enabled (`cfgHvAcOutOpen`)
- X-Boost Enabled (`cfgXboostEn`)

*Sliders (numbers)*
- Max Charge Level (`cfgMaxChgSoc` -> `{"sn": "SN", "cmdId": 17, "dirDest": 1, "dirSrc": 1, "cmdFunc": 254, "dest": 2, "params": {"cfgMaxChgSoc": "VALUE"}}` [50 - 100])
- Min Discharge Level (`cfgMinDsgSoc` -> `{"sn": "SN", "cmdId": 17, "dirDest": 1, "dirSrc": 1, "cmdFunc": 254, "dest": 2, "params": {"cfgMinDsgSoc": "VALUE"}}` [0 - 30])
- Backup Reserve Level (`cfgEnergyBackup.energyBackupStartSoc` -> `{"sn": "SN", "cmdId": 17, "dirDest": 1, "dirSrc": 1, "cmdFunc": 254, "dest": 2, "params": {"cfgEnergyBackup": {"energyBackupStartSoc": "VALUE", "energyBackupEn": true}}}` [5 - 100])
- Generator Auto Start Level (`cfgCmsOilOnSoc` -> `{"sn": "SN", "cmdId": 17, "dirDest": 1, "dirSrc": 1, "cmdFunc": 254, "dest": 2, "params": {"cfgCmsOilOnSoc": "VALUE"}}` [0 - 30])
- Generator Auto Stop Level (`cfgCmsOilOffSoc` -> `{"sn": "SN", "cmdId": 17, "dirDest": 1, "dirSrc": 1, "cmdFunc": 254, "dest": 2, "params": {"cfgCmsOilOffSoc": "VALUE"}}` [50 - 100])
- AC Charging Power (`plugInInfoAcInChgPowMax` -> `{"sn": "SN", "cmdId": 17, "dirDest": 1, "dirSrc": 1, "cmdFunc": 254, "dest": 2, "params": {"plugInInfoAcInChgPowMax": "VALUE"}}` [400 - 2900])

*Selects*



## Delta_3_Plus

The following structure describes the expected heartbeat report for the Delta 3 Plus.

```protobuf
syntax = "proto3";

message BatteryPackInfo {
  uint32 bmsIndex     = 1;   // Battery index (0 = main/internal, 1 = Extra Battery)
  uint32 soc          = 2;   // State of charge (%)
  uint32 soh          = 3;   // State of health (%)
  uint32 designCap    = 4;   // Design capacity (mAh)
  uint32 fullCap      = 5;   // Full charge capacity (mAh)
  uint32 remainCap    = 6;   // Remaining capacity (mAh)
  uint32 cycles       = 7;   // Cycle count
  uint32 vol          = 8;   // Pack voltage (mV)
  int32  amp          = 9;   // Pack current (mA)
  int32  temp         = 10;  // Pack temperature (°C)
  uint32 maxCellTemp  = 11;  // Max cell temperature (°C)
  uint32 minCellTemp  = 12;  // Min cell temperature (°C)
  uint32 maxCellVol   = 13;  // Max cell voltage (mV)
  uint32 minCellVol   = 14;  // Min cell voltage (mV)
  uint32 bmsFaultCode = 15;  // BMS fault code
}

message Delta3PlusHeartbeat {
  uint32 totalSoc       = 1;   // Overall State of Charge (%)
  uint32 bpCount        = 2;   // Number of battery packs
  repeated BatteryPackInfo packs = 3;
  uint32 acInVoltage    = 10;
  uint32 acInCurrent    = 11;
  uint32 acInPower      = 12;
  uint32 acInFreq       = 13;
  uint32 solarVoltage   = 14;
  uint32 solarCurrent   = 15;
  uint32 solarPower     = 16;
  uint32 acOutVoltage   = 20;
  uint32 acOutCurrent   = 21;
  uint32 acOutPower     = 22;
  uint32 acOutFreq      = 23;
  uint32 dcOutVoltage   = 24;
  uint32 dcOutCurrent   = 25;
  uint32 dcOutPower     = 26;
  uint32 usb1Power      = 27;
  uint32 usb2Power      = 28;
  uint32 usbQC1Power    = 29;
  uint32 usbQC2Power    = 30;
  uint32 usbC1Power     = 31;
  uint32 usbC2Power     = 32;
  int32  remainChargeTime = 33;
  int32  remainDischgTime = 34;
  bool   xboostEnabled   = 40;
  bool   acAlwaysOn      = 41;
  bool   dcEnabled       = 42;
  bool   usbEnabled      = 43;
  bool   beeperEnabled   = 44;
  uint32 beepMode        = 45;
  bool   chargingPause   = 46;
  bool   generatorAuto   = 47;
  uint32 minReserveSoc   = 48;
  uint32 maxChargeSoc    = 49;
  uint32 minDischargeSoc = 50;
  uint32 errorCode       = 90;
  uint32 warningCode     = 91;
  uint32 productType     = 92;
  string firmwareVersion = 93;
}
```

*Sensors*
- Total In Power
- Total Out Power
- AC In Power
- AC Out Power
- Solar In Power
- DC Out Power
- USB-A (1) Out Power
- USB-A (2) Out Power
- USB QC (1) Out Power
- USB QC (2) Out Power
- USB-C (1) Out Power
- USB-C (2) Out Power
- Charge Remaining Time
- Discharge Remaining Time
- Total In Energy
- Total Out Energy
- Total Energy

*Switches*
- X-Boost Enabled
- AC Always On
- DC Enabled
- USB Enabled
- Beeper Enabled
- Charging Pause
- Generator Auto Start

*Sliders (numbers)*
- Backup Reserve Level
- Max Charge Level
- Min Discharge Level

*Selects*


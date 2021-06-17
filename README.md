# Windows-RFD900-App
This python program is a Windows application designed for two-way Serial (USB) communcication. It is capable of displaying input. It can transmit throttle, toggle lights, and emergency stop. It was designed for RFD 900x long-range radios. However, it will work with any device capable of connecting to a Windows COM port that sends data in the format: 'b/(float)/(float)/(float)/'.

## Instructions

### Receive:
Connect radio to windows device via USB and run rfdapp.py. Select the appropriate COM port from the dropdown menu. Data should be displayed.

### Transmit:
Data transmission is ready to be configured based on end-user syntax. Transmission should be configured for throttle, toggle lights, and emergency stop.

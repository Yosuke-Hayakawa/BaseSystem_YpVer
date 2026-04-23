 
Fast Data Exchange with CANoe 
Version 1.0 
2015-08-07 
Application Note AN-AND-1-119 
 
 
 
Author(s) 
Huber, Alexander 
Restrictions                      Public Document 
Abstract 
This application note is a step by step guide for setting up an easy FDX client application 
in C# .NET that interfaces to CANoe via FDX. CANoe FDX (Fast Data eXchange) is a 
UDP-based protocol for simple, fast and real-time exchange of data between CANoe and 
other systems via an Ethernet connection. This protocol grants other systems both read 
and write access to CANoe system and environment variables, and bus signals. The 
other system may be, for example, a HIL system on a test bench or a PC used to display 
CANoe data. 
 
Table of Contents 
 
 1  
Copyright © 2015 - Vector Informatik GmbH 
Contact Information:   www.vector.com   or +49-711-80 670-0 
1.0 
Overview .......................................................................................................................................................... 2 
1.1 
Introduction .................................................................................................................................................... 2 
1.2 
About this Tutorial ......................................................................................................................................... 2 
1.3 
UDP - User Datagram Protocol ..................................................................................................................... 2 
2.0 
Definition of Terms ........................................................................................................................................... 2 
3.0 
CANoe Configuration – EasyFDX.cfg .............................................................................................................. 2 
3.1 
FDX Description File ..................................................................................................................................... 3 
3.2 
CANoe Settings ............................................................................................................................................. 4 
4.0 
Client Application ............................................................................................................................................. 5 
4.1 
Structure ........................................................................................................................................................ 5 
4.2 
Getting started ............................................................................................................................................... 5 
5.0 
Implementation ................................................................................................................................................ 6 
5.1 
UdpClient ....................................................................................................................................................... 6 
5.2 
Sending Datagrams ....................................................................................................................................... 8 
5.2.1 
Start Command ........................................................................................................................................... 9 
5.2.2 
Stop Command ......................................................................................................................................... 10 
5.2.3 
DataExchange Command ......................................................................................................................... 11 
5.3 
Reception .................................................................................................................................................... 12 
5.3.1 
Receiving Helpers ..................................................................................................................................... 12 
5.3.2 
DataRequest Command ........................................................................................................................... 13 
6.0 
Standalone Mode ........................................................................................................................................... 15 
7.0 
Additional Resources ..................................................................................................................................... 16 
8.0 
Contacts ......................................................................................................................................................... 16 
9.0 
Appendix ........................................................................................................................................................ 17 
9.1 
Form1.cs...................................................................................................................................................... 17 
9.2 
Form1.Designer.cs ...................................................................................................................................... 22 
 
 

---

 
 
Fast Data Exchange with CANoe 
 
 
 
 
 
2 
Application Note AN-AND-1-119 
 
1.0 Overview 
1.1 Introduction 
This application note is a step by step guide for setting up an easy FDX client application in C# .NET that 
interfaces to CANoe via FDX. CANoe FDX (Fast Data eXchange) is a UDP-based protocol for simple, fast and 
real-time exchange of data between CANoe and other systems via an Ethernet connection. This protocol grants 
other systems both read and write access to CANoe system and environment variables, and bus signals. The other 
system may be, for example, a HIL system on a test bench or a PC used to display CANoe data. For the remainder 
of this document, the other system is referred to as the HIL system. 
Before further explanation of FDX, some background on CANoe is necessary. CANoe is well-known for its network 
simulation capabilities. Not only does CANoe have the ability to simulate multiple nodes in a network, it can also 
simulate multiple networks of different bus architectures such as CAN, LIN, MOST, FlexRay and Ethernet. Imagine 
a vehicle with multiple data networks consisting of the following networks:  CAN for powertrain, LIN for body 
electronics and lighting, MOST for entertainment and GPS navigation, and FlexRay for chassis. CANoe can be 
used to model all of the network data and functions for these bus systems, either individually or simultaneously. 
When network data and functions need to be evaluated and validated at the design, implementation, or production 
stage, CANoe can act as a test tool as well as a network simulation tool in order to test the network data and 
functions. A simple, fast and reliable data exchange method is needed for transferring large quantities of data into 
and out of CANoe or for communicating with an existing HIL system. The solution is CANoe FDX. 
Note: The HIL system may run on the same PC as CANoe or on a different PC connected via Ethernet. 
1.2 About this Tutorial 
This tutorial will focus on the implementation of a simple C# .NET application, which will set up the required UDP 
client for sending and receiving data with CANoe. As counterpart to the application, the pre-installed 
“EasyFDX.cfg” CANoe demo configuration will be used. A basic understanding of C# .NET is required. 
1.3 UDP - User Datagram Protocol 
Communication between CANoe and the HIL system is based on the UDP protocol (IPv4). UDP is a widespread, 
standardized protocol that uses a simple connectionless transmission model which means there will most likely 
already be a UDP stack available on the HIL system. If a UDP stack is not available on the HIL system, it must be 
installed prior to using CANoe FDX. 
The exchange of data between CANoe and the HIL system is achieved through reciprocal transmission of UDP 
datagrams. As a matter of principle, the HIL system always sends a datagram to CANoe first and therefore has to 
know the IP address and port number used by CANoe for the FDX protocol. CANoe evaluates all incoming 
datagrams to determine the sender’s IP address and port number and always responds only to the sender that 
requested the data. 
2.0 Definition of Terms 
UDP - The User Datagram Protocol is a transport protocol from the Internet Protocol suite. 
FDX – CANoe’s Fast Data eXchange protocol is a UDP-based protocol for simple, fast and real-time exchange of 
data between CANoe and other systems via an Ethernet connection. 
HIL – Hardware in the Loop test systems. These can be any system that has access to an Ethernet 
implementation. 
3.0 CANoe Configuration – EasyFDX.cfg 
Typically, network signals and system variables within CANoe are controlled via a CAPL program. The CANoe 
FDX sample configuration (\Demo_AddOn\FDX\EasyFDX.cfg) demonstrates how network signals and system 

---

 
 
Fast Data Exchange with CANoe 
 
 
3 
Application Note AN-AND-1-119 
 
variables can be controlled by a separate client application 
(\Demo_Addon\FDX\EasyClient\Release\EasyClient.exe). For example, the HazardLightsSwitch and 
HeadLightSwitch system variables (which are linked to the lamp switches on the Control panel) are set via the FDX 
protocol. The lamp states (on/off) depicted by the FlashLight and HeadLight signals are reported to the client 
application via the FDX protocol. The EasyClient.exe client application will be replaced by another client 
application (EasyClientNet.exe) which will be developed with the help of this application note. 
3.1 FDX Description File 
An FDX description file (FDXDescription_Easy.xml) can be found in the same directory as the EasyFDX.cfg 
CANoe configuration. The FDX description file is an eXtensible Markup Language (XML) file. It defines the 
message contents and variables within data groups that are exchanged between CANoe and the client application. 
The FDX description file contains two data groups: groupID ‘1’ and ‘2’. Each data group can be used for sending 
and receiving data, but for simplicity’s sake, assume groupID ‘1’ is used to receive data from CANoe and groupID 
‘2’ is used to send data to CANoe. 
 
<?xml version="1.0" encoding="ISO-8859-1"?> 
<canoefdxdescription version="1.0"> 
 
    <datagroup groupID="1" size="8"> 
        <identifier>EasyDataRead</identifier> 
        <item type="int16" size="2" offset="0"> 
            <identifier>SigEngineSpeed</identifier> 
            <signal name="EngineSpeed" value="raw"/> 
        </item> 
        <item type="uint8" size="1" offset="2"> 
            <identifier>SigOnOff</identifier> 
            <signal name="OnOff" value="raw"/> 
        </item> 
        <item type="uint8" size="1" offset="3"> 
            <identifier>SigFlashLight</identifier> 
            <signal name="FlashLight" value="raw"/> 
        </item> 
        <item type="uint8" size="1" offset="4"> 
            <identifier>SigHeadLight</identifier> 
            <signal name="HeadLight" value="raw"/> 
        </item> 
        <item type="uint8" size="1" offset="5"> 
             <identifier>EnvHazardLightsSwitch</identifier> 
            <sysvar name="HazardLightsSwitch" namespace="FDX" /> 
        </item> 
        <item type="uint8" size="1" offset="6"> 
            <identifier>EnvHeadLightSwitch</identifier> 
            <sysvar name="HeadLightSwitch" namespace="FDX"/> 
        </item> 
    </datagroup> 
 
    <datagroup groupID="2" size="8"> 
        <identifier>EasyDataWrite</identifier> 
        <item type="int16" size="2" offset="0"> 
            <identifier>EnvEngineSpeedEntry</identifier> 
            <sysvar name="EngineSpeedEntry" namespace="FDX"/> 
        </item> 
        <item type="uint8" size="1" offset="2"> 
            <identifier>EnvEngineStateSwitch</identifier> 
            <sysvar name="EngineStateSwitch" namespace="FDX"/> 
        </item> 
        <item type="uint8" size="1" offset="3"> 
            <identifier>SigFlashLigth</identifier> 

---

 
 
Fast Data Exchange with CANoe 
 
 
4 
Application Note AN-AND-1-119 
 
            <signal name="FlashLight" value="raw"/> 
        </item> 
        <item type="uint8" size="1" offset="4"> 
            <identifier>SigHeadLight</identifier> 
            <signal name="HeadLight" value="raw"/> 
        </item> 
    </datagroup> 
 
</canoefdxdescription> 
 
Note: The size of groupID 2 is 8, when it should be 5. CANoe will display a warning in the write window indicating 
this: “16-0205 FDX: data size (5 bytes) given in incoming DataExchange command for group id 2 is smaller than 
specified group size (8 bytes).”  You can safely ignore this warning for the time being. 
3.2 CANoe Settings 
To use FDX, CANoe must be configured to use the protocol. CANoe’s settings can be changed in the Options 
dialog of the CANoe main menu (Configuration|Options…|CANoe Options| Extensions|XLI API & FDX 
Protocol; see Figure 1). 
FDX must be enabled and the desired Port must be specified. The default port is 2809. Ensure the port is available 
to use on the PC or else FDX will not be able to communicate using it. Additionally, an FDX description file must be 
written and then added to the CANoe configuration. The description file must include all data which will be sent or 
received by CANoe. 
The client application will need the IP address of the PC running CANoe. Prior to trying to connect using FDX, 
assure the IP address is not blocked (e.g., by IT policy or a firewall). If the client application and CANoe are 
running on the same PC, it is possible to use the local host IP address (127.0.0.1). If CANoe is operating using 
CANoeRT or is running in stand-alone mode using a VN8900 or VT6000 module, the default IP address is 
192.168.100.1. 
Note: The EasyFDX,cfg CANoe configuration already has FDX enabled and the appropriate 
FDXDescription_Easy.xml file associated. Therefore, it is used as the example CANoe configuration for this 
application note. 

---

 
 
Fast Data Exchange with CANoe 
 
 
5 
Application Note AN-AND-1-119 
 
 
Figure 1: CANoe Options dialog 
4.0 Client Application 
This application note does not intend to teach the Visual C# language or its components. It is recommended that 
the user has some C# background. The example application in this application note uses the tools listed below:  
• 
Microsoft Visual C# 2013  
• 
Vector CANoe Full (Latest version is preferred)  
4.1 Structure 
All FDX commands are triggered using functions accessed via buttons on the C# client’s user interface. The 
supported functionality includes connecting and disconnecting from CANoe, starting and stopping measurement, 
and sending and receiving data.  Note that the data is static, but the CAPL and C# code could be easily modified to 
change the data being exchanged (both transmitted and received). 
4.2 Getting started 
Launch Visual Studio and set up a new WindowsForms Application for C#. Name the new project “EasyClientNet”. 
The code examples in the step-by-step instructions can be copied-and-pasted into the C# application as you 
progress through the document. A complete example for creating the EasyClientNet executable is available in this 
document’s Appendix. It is possible to copy and paste the code in the Appendix into the appropriately named files 
in order to create the executable. A sample Form is displayed in Figure 2 and its code is also available in the 
Appendix. 
After the client has been implemented, the CANoe FDX sample configuration (Demo_AddOn\FDX\EasyFDX.cfg) 
can be used to test it. Once the configuration is loaded into CANoe, connect the UDP client to CANoe by pressing 
the “Connect” button. Start the CANoe measurement by pressing the “Start Measurement” button. Once the 
measurement has started, data can be requested with the “Request Data” button. The data will be displayed in the 

---

 
 
Fast Data Exchange with CANoe 
 
 
6 
Application Note AN-AND-1-119 
 
TextBox in the “Receive Data” group. The data specified in the “Send Data” group will be sent upon pressing the 
corresponding “Send Data” button. 
 
 
Figure 2: Main Form Description 
5.0 Implementation 
This chapter focuses on the actual client implementation. There are three main parts: connecting the UDP Socket, 
sending data, and receiving data. These parts will be discussed in detail. 
5.1 UdpClient 
The UdpClient class from the Microsoft .NET Framework is an easy way of sending and receiving UDP datagrams. 
All methods are executed in blocking synchronous mode. To establish a UdpClient connection, an IP address and 
port must be defined. 
First, create a new instance of UdpClient: 
 
        // UDP Client for the communication 
        private UdpClient _Client; 
 
Then, define the settings for the UDP connection: 
 
        // +++++++++++++++++ Settings for FDX ++++++++++++++++++++++++++++++++++ 
        // Connection 
        string IpAdr = "127.0.0.1"; 
        int Port = 2809; 


| // UDP Client for the communication |  |
| --- | --- |
| private UdpClient _Client; |  |


---

 
 
Fast Data Exchange with CANoe 
 
 
7 
Application Note AN-AND-1-119 
 
        // Data Group IDs 
        const ushort gIDread = 1; 
        const ushort gIDwrite = 2; 
 
        // +++++++++++++++++ Header ++++++++++++++++++++++++++++++++++++++++++++ 
        // Signature 
        const UInt64 SIGNATURE = 0x584446656F4E4143; 
        // Protocol version 
        const Byte MajorVersion = 1; 
        const Byte MinorVersion = 0; 
        // In this example only 1 command is send at a time 
        const UInt16 NumberOfCommands = 1; 
        // SequenceNumber 
        UInt16 SequenceNumber = 0x8000; 
        // 2 unused bytes for better alignment. 
        const UInt16 Reserved = 0x0000; 
 
Next, declare an enumerated type that contains the different FDX commands to be sent: 
 
        private enum FdxCommandE 
        { 
            Start = 0x0001, 
            Stop = 0x0002, 
            Key = 0x0003, 
            DataRequest = 0x0006, 
            DataExchange = 0x0005, 
            DataError = 0x0007, 
            FreeRunning = 0x0008, 
            FreeRunningCancel = 0x0009, 
            Status = 0x0004, 
            StatusRequest = 0x000A, 
            SeqNumError = 0x000B, 
        } 
 
Then, establish the connection to CANoe using a “Button Click” event procedure (btConnect_Click). The IP 
address and port number will be used as arguments for the UdpClient method “Connect”. This procedure 
establishes a remote host connection to CANoe. 
 
        private void btConnect_Click(object sender, EventArgs e) 
        { 
            // connect to the Host/ CANoe 
            _Client = new UdpClient(); 
            _Client.Connect(IpAdr, Port); 
        } 
Finally, close the UdpClient to release the resources which are no longer needed. This activity is performed using 
the btDisconnect_Click Event procedure: 
 
        private void btDisconnect_Click(object sender, EventArgs e) 
        { 
            // Close UDP Socket 
            _Client.Close(); 
        } 

---

 
 
Fast Data Exchange with CANoe 
 
 
8 
Application Note AN-AND-1-119 
 
5.2 Sending Datagrams 
Communication between CANoe and the HIL system is implemented by exchanging UDP datagrams. A datagram 
consists of the datagram header followed by one or more commands.  
 
 
Figure 3: Datagram Header Layout 
 
UDP Datagram Header  
The UDP datagram header consists of an FDX signature, a two-byte FDX version number (major and minor 
version), the number of commands that follow the header, and a sequence number.  
The signature is an eight-byte, constant unsigned integer with the value 0x584446656F4E4143 (“CANoeFDX” in 
hexadecimal, Intel Format). The signature serves as an identifier to determine whether or not the datagram is 
intended for CANoe. CANoe will ignore all datagrams that do not have this exact signature.  
A two-digit version number is used to identify the FDX protocol version and the compatible CANoe version. The 
two digits are represented in two bytes of the UDP header, the fdxMajorVersion and fdxMinorVersion fields. A 
change to the FDX protocol may result in a change to the minor version number, but not the major version number. 
This type of change indicates  a potential increase of FDX protocol-specific information within the datagram. 
CANoe can still process the newer datagram using the same major version, but the new information is ignored. 
The version is defined by Vector. At the time of this document’s publish, the current version value is “1.0” (major 
version = 1, minor version = 0). 
The sequence number assists the receiver in recognizing the loss of individual datagrams. The sender numbers 
the datagrams sequentially starting with 0x0001 and ending with 0x7FFF. The valid values for the sequence 
number are as follows: 
• 
0x0000 - starts a new counting sequence 
• 
0x0001 - 0x7FFF – valid sequence numbers; once 0x7FFF is reached, sequence number resets to 0x0001 
• 
0x8000 - ends a counting sequence or indicates that no sequence counting exists 
 
 

---

 
 
Fast Data Exchange with CANoe 
 
 
9 
Application Note AN-AND-1-119 
 
Command Code 
Every FDX command begins with a Command Code followed by the size of the command. The Command Code 
determines what type of command is being used (e.g., CANoe measurement start, exchange of signals/variable 
data, etc.). 
Command 
Command Code 
Size of Command 
Start Command 
0x0001 
4 bytes 
Stop Command 
0x0002 
4 bytes 
Key Command 
0x0003 
8 bytes 
DataRequest Command 
0x0006 
6 bytes 
DataExchange Command 
0x0005 
8 bytes + dataSize 
DataError Command 
0x0007 
8 bytes 
FreeRunningRequest Command 
0x0008 
16 bytes 
FreeRunningCancel Command 
0x0009 
6 bytes 
Status Command 
0x0004 
16 bytes 
Status Request Command 
0x000A 
4 bytes 
Sequence Number Error Command 
0x000B 
8 bytes 
Table 1: All Commands and Their Corresponding Sizes 
 
Every CANoe installation includes a document which has a detailed description of the various FDX commands. For 
more information, please see “<CANoe Installation Directory>\Doc\CANoe_FDX_Protocol_EN.pdf”. 
5.2.1 Start Command 
The Start command is used to start a CANoe measurement. 
Offset 
Size 
Type 
Field 
Description 
0 
2 
uint16 
commandSize 
Size of command (4 Bytes) 
2 
2 
uint16 
commandCode 
kCommandCode_Start = 0x0001 
Table 2: Start Command Layout 
 
The Start command is demonstrated by the btStartMeasure_Click event procedure: 
 
        private void btStartMeasure_Click(object sender, EventArgs e) 
        {//Start Meas 
 
            MemoryStream ms = new MemoryStream(); 
            BinaryWriter writer = new BinaryWriter(ms); 
 
            // Assemble Header 
            writer.Write(SIGNATURE); 
            writer.Write(MajorVersion); 
            writer.Write(MinorVersion); 
            writer.Write(NumberOfCommands); 
            writer.Write(SequenceNumber); 
            writer.Write(Reserved); 
 
            // Add Command 
            writer.Write((UInt16)4); // Size of Command = Size field + Command 
            writer.Write((UInt16)FdxCommandE.Start); 


|  | Command |  | Command Code |  |  | Size of Command |  |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Start Command |  | 0x0001 |  |  | 4 bytes |  |  |
| Stop Command |  | 0x0002 |  |  | 4 bytes |  |  |
| Key Command |  | 0x0003 |  |  | 8 bytes |  |  |
| DataRequest Command |  | 0x0006 |  |  | 6 bytes |  |  |
| DataExchange Command |  | 0x0005 |  |  | 8 bytes + dataSize |  |  |
| DataError Command |  | 0x0007 |  |  | 8 bytes |  |  |
| FreeRunningRequest Command |  | 0x0008 |  |  | 16 bytes |  |  |
| FreeRunningCancel Command |  | 0x0009 |  |  | 6 bytes |  |  |
| Status Command |  | 0x0004 |  |  | 16 bytes |  |  |
| Status Request Command |  | 0x000A |  |  | 4 bytes |  |  |
| Sequence Number Error Command |  | 0x000B |  |  | 8 bytes |  |  |

|  | Offset |  |  | Size |  |  | Type |  | Field |  |  | Description |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 |  |  | 2 |  |  | uint16 |  |  | commandSize |  | Size of command (4 Bytes) |  |  |
| 2 |  |  | 2 |  |  | uint16 |  |  | commandCode |  | kCommandCode_Start = 0x0001 |  |  |

| private void btStartMeasure_Click(object sender, EventArgs e) |  |
| --- | --- |
| {//Start Meas |  |

| MemoryStream ms = new MemoryStream(); |  |
| --- | --- |
| BinaryWriter writer = new BinaryWriter(ms); |  |

| // Add Command |  |  |
| --- | --- | --- |
| writer.Write((UInt16)4); // Size of Command = Size field + Command |  |  |
| writer.Write((UInt16)FdxCommandE.Start); |  |  |


---

 
 
Fast Data Exchange with CANoe 
 
 
10 
Application Note AN-AND-1-119 
 
 
            // Send Data 
            _Client.Send(ms.ToArray(), (int)ms.Length); 
             
            writer.Close(); 
            ms.Close(); 
        } 
 
The first step is to assemble the FDX packet. To do so, create a MemoryStream object and a BinaryWriter object 
(these objects ease data assembly). Then, the datagram header is assembled. Next, the size of the command is 
calculated. Finally, the start measurement command (4 bytes) is used. 
Note:  The FDX command size includes the command field, all consecutive data bytes associated to the command 
and the command size field itself. The header is not included in the size calculation. 
Command Size = command size-field’s size + command field’s size + associated data field’s size 
Command Size = 2 bytes + 2 bytes + x bytes 
Once the FDX packet is assembled, the next step is to transmit it by using the UdpClient “Send” method. Keep in 
mind that the Send method is a blocking call (the function will return after all of the data has been sent). 
5.2.2 Stop Command 
The Stop command is used to stop a CANoe measurement. 
Offset 
Size 
Type 
Field 
Description 
0 
2 
uint16 
commandSize 
Size of command (4 Bytes) 
2 
2 
uint16 
commandCode 
kCommandCode_Stop = 0x0002 
Table 3: Stop Command Layout 
 
Sending a Stop command code looks exactly the same as sending the Start command, with the exception of the 
FDX command itself: 
 
        private void btStopMeasure_Click(object sender, EventArgs e) 
        {//Stop meas 
 
            MemoryStream ms = new MemoryStream(); 
            BinaryWriter writer = new BinaryWriter(ms); 
 
            // Assemble Header 
            writer.Write(SIGNATURE); 
            writer.Write(MajorVersion); 
            writer.Write(MinorVersion); 
            writer.Write(NumberOfCommands); 
            writer.Write(SequenceNumber); 
            writer.Write(Reserved); 
 
            // Add Command 
            writer.Write((UInt16)4); // Size of Command = Size field + Command 
            writer.Write((UInt16)FdxCommandE.Stop); 
 
            // Send Data 
            _Client.Send(ms.ToArray(), (int)ms.Length); 
 


| // Send Data |  |
| --- | --- |
| _Client.Send(ms.ToArray(), (int)ms.Length); |  |

|  | Offset |  | Size |  |  | Type |  | Field |  |  | Description |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 |  | 2 |  |  | uint16 |  |  | commandSize |  | Size of command (4 Bytes) |  |  |
| 2 |  | 2 |  |  | uint16 |  |  | commandCode |  | kCommandCode_Stop = 0x0002 |  |  |

| private void btStopMeasure_Click(object sender, EventArgs e) |  |
| --- | --- |
| {//Stop meas |  |

| MemoryStream ms = new MemoryStream(); |  |
| --- | --- |
| BinaryWriter writer = new BinaryWriter(ms); |  |

| // Add Command |  |  |  |
| --- | --- | --- | --- |
| writer.Write((UInt16)4); // Size of Command = Size field + Command |  |  |  |
|  | writer.Write((UInt16)FdxCommandE.Stop); |  |  |

| // Send Data |  |
| --- | --- |
| _Client.Send(ms.ToArray(), (int)ms.Length); |  |


---

 
 
Fast Data Exchange with CANoe 
 
 
11 
Application Note AN-AND-1-119 
 
            writer.Close(); 
            ms.Close(); 
        } 
5.2.3 DataExchange Command 
The DataExchange command is used to exchange a group of signals or variables between the HIL system and 
CANoe. This command can be used to send data from the HIL system to CANoe or from CANoe to the HIL system 
(bi-directional communication). 
Offset 
Size 
Type 
Field 
Description 
0 
2 
uint16 commandSize 
Size of command (8+dataSize) 
2 
2 
uint16 commandCode 
kCommandCode_DataExchange = 0x0005 
4 
2 
uint16 groupID 
Identifies the group of signals and variables inside the FDX 
description file. 
6 
2 
uint16 dataSize 
Number of bytes of the following array. 
8 
dataSize uint8[] dataBytes 
Contains the values of signals and variables as defined in 
the FDX description file. 
Table 4: DataExchange Command Layout 
 
The first step is to assemble the UDP datagram header using the same data from the previous commands. Next, 
add the command to the stream. The size is calculated as follows: 
- 
2 bytes for the command size field 
- 
2 bytes for the command code field (indicating the DataExchange command) 
- 
2 bytes for the group ID to be sent 
- 
2 bytes for the actual data 
- 
X bytes (size of the dataSize field) for the actual data size (will use 5 bytes for the C# example code) 
So, in the C# example, the size of the datagram header is 13 bytes (2 + 2 + 2 + 2 + 5).  
Next, the data must be assembled prior to being sent. Therefore, a byte array is created and all the data is added 
to it. The example assumes the data has the following values: 
- 
EngineSpeedEntry = 0x03E8 = 1000 
- 
EngineStateSwitch = 0x01 = 1 
- 
FlashLight = 0x01 = 1 
- 
HeadLight = 0x01 = 1 
 
Finally, once the complete UDP datagram has been assembled it can be sent using the UdpClient “Send” 
command. 
 
        private void btSendData_Click(object sender, EventArgs e) 
        { 
            MemoryStream ms = new MemoryStream(); 
            BinaryWriter writer = new BinaryWriter(ms); 
 
            // Assemble Header 
            writer.Write(SIGNATURE); 
            writer.Write(MajorVersion); 
            writer.Write(MinorVersion); 


|  | Offset |  |  | Size |  |  | Type |  |  | Field |  |  | Description |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 |  |  | 2 |  |  | uint16 |  |  | commandSize |  |  | Size of command (8+dataSize) |  |  |
| 2 |  |  | 2 |  |  | uint16 |  |  | commandCode |  |  | kCommandCode_DataExchange = 0x0005 |  |  |
| 4 |  |  | 2 |  |  | uint16 |  |  | groupID |  |  | Identifies the group of signals and variables inside the FDX
description file. |  |  |
| 6 |  |  | 2 |  |  | uint16 |  |  | dataSize |  |  | Number of bytes of the following array. |  |  |
| 8 |  |  | dataSize |  |  | uint8[] |  |  | dataBytes |  |  | Contains the values of signals and variables as defined in
the FDX description file. |  |  |


---

 
 
Fast Data Exchange with CANoe 
 
 
12 
Application Note AN-AND-1-119 
 
            writer.Write(NumberOfCommands); 
            writer.Write(SequenceNumber); 
            writer.Write(Reserved); 
 
            // Add Command 
            writer.Write((UInt16)13); // Size of Command (8+dataSize)  
            writer.Write((UInt16)FdxCommandE.DataExchange); 
            writer.Write(gIDwrite); // specify Group ID = 2 
            writer.Write((UInt16)5); // write data size (Size of DataGroup 2) 
 
            // set data 
            // EngineSpeedEntry = 0x03e8 = 1000 
            // EngineStateSwitch = 1 
            // FlashLight = 1 
            // HeadLight = 1 
            byte[] data = { 0xe8, 0x03, 0x01, 0x01, 0x01 }; 
 
            // data as byte array 
            // 0 offset in the byte array 
            // 5 length of byte array 
            writer.Write(data, 0, 5); // write data 
 
            // Send Data 
            _Client.Send(ms.ToArray(), (int)ms.Length); 
 
            ms.Close(); 
            writer.Close(); 
        } 
5.3 Reception 
Compared to sending a datagram, receiving a datagram is slightly more complex. Therefore, two “helper” functions 
are introduced to assist in receiving FDX messages. These helper functions are not mandatory for FDX 
communication and other methods may be employed as necessary. 
5.3.1 Receiving Helpers 
The first helper function creates a remote IPEndPoint object which allows datagrams to be received, regardless of 
the source. Then, the UdpClient Receive method is called with a reference to the IPEndPoint object. This call 
causes the program to “pause” (block) until any IP packet is received. The received data is converted to a 
MemoryStream to ease processing. 
 
        private MemoryStream ReceiveDatagram() 
        { 
            //IPEndPoint object will allow us to read datagrams sent from any source. 
            IPEndPoint remoteIpEndPoint = new IPEndPoint(IPAddress.Any, 0); 
            // receive and read data 
            byte[] receiveBuffer = _Client.Receive(ref remoteIpEndPoint); 
            // put data in a MemoryStream 
            MemoryStream ms = new MemoryStream(receiveBuffer); 
 
            return ms; 
        } 
 
The second helper function is an overloaded version of the first function. This function uses a parameter to specify 
a reception timeout (in milliseconds). The UdpClient assigns the input parameter to the ReceiveTimeout property, 
which specifies the timeout time to receive the datagram. If no data is received prior to the timeout expiration, a 
SocketException will be thrown by the UdpClient and the return value is “null”. 


| // Send Data |  |
| --- | --- |
| _Client.Send(ms.ToArray(), (int)ms.Length); |  |

| ms.Close(); |  |  |
| --- | --- | --- |
| writer.Close(); |  |  |
| } |  |  |

| return ms; |  |
| --- | --- |
| } |  |

| The second helper function is an overloaded version of the first function. This function uses a parameter to specify |  |
| --- | --- |
| a reception timeout (in milliseconds). The UdpClient assigns the input parameter | to the ReceiveTimeout property, |


---

 
 
Fast Data Exchange with CANoe 
 
 
13 
Application Note AN-AND-1-119 
 
 
        private MemoryStream ReceiveDatagram(int timeout_ms) 
        { 
            // set the client timeout 
            _Client.Client.ReceiveTimeout = timeout_ms; 
            MemoryStream response = null; 
            try 
            { 
                // receive a datagram 
                response = ReceiveDatagram(); 
            } 
            catch (SocketException se) 
            { 
                if (se.SocketErrorCode != SocketError.TimedOut) 
                { 
                    return response; 
                } 
            } 
            return response; 
        } 
5.3.2 DataRequest Command  
The DataRequest command is used to query a group of signal/ variable values. CANoe sends a data group to the 
HIL system either in response to either an explicit DataRequest command or because FreeRunning mode is 
activated. In FreeRunning mode, the data groups are sent cyclically or triggered by a call of the 
FDXTriggerDataGroup CAPL function. Additionally, the data transmission can be carried out just before 
measurement start and at measurement end.  
Offset 
Size 
Type 
Field 
Description 
0 
2 
uint16 
commandSize 
Size of command (6 Bytes) 
2 
2 
uint16 
commandCode 
kCommandCode_DataExchange = 0x0006 
4 
2 
uint16 
groupID 
Identifies the group of signals and variables inside the 
FDX description file. 
Table 5: Data Request Command Layout 
 
To keep the next example simple, only the DataRequest command will be shown. This example uses the 
btReqData_Click event procedure: 
 
        private void btReqData_Click(object sender, EventArgs e) 
        { 
            UInt16 NbrOfCmds; 
            MemoryStream ms = new MemoryStream(); 
            BinaryWriter writer = new BinaryWriter(ms); 
            byte MeasurementState = 0; 
            Int64 TimeStamp = 0; 
 
            // Assemble Header 
            writer.Write(SIGNATURE); 
            writer.Write(MajorVersion); 
            writer.Write(MinorVersion); 
            writer.Write(NumberOfCommands); 
            writer.Write(SequenceNumber); 
            writer.Write(Reserved); 
 


|  | Offset |  | Size |  |  | Type |  |  | Field |  |  | Description |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 |  | 2 |  |  | uint16 |  |  | commandSize |  |  | Size of command (6 Bytes) |  |  |
| 2 |  | 2 |  |  | uint16 |  |  | commandCode |  |  | kCommandCode_DataExchange = 0x0006 |  |  |
| 4 |  | 2 |  |  | uint16 |  |  | groupID |  |  | Identifies the group of signals and variables inside the
FDX description file. |  |  |


---

 
 
Fast Data Exchange with CANoe 
 
 
14 
Application Note AN-AND-1-119 
 
            // Add Command 
            writer.Write((UInt16)6); // Size of Command 
            writer.Write((UInt16)FdxCommandE.DataRequest); 
            writer.Write(gIDread); // specify Group ID 
 
            // Send Data 
            _Client.Send(ms.ToArray(), (int)ms.Length); 
 
            // Wait for an answer 
            ms = ReceiveDatagram(500); 
 
            // get data 
            BinaryReader reader = new BinaryReader(ms); 
            tbRcvData.Text = ""; 
 
            reader.ReadUInt64(); // discard signature 
            reader.ReadByte();   // discard Major Version 
            reader.ReadByte();   // discard Minor version 
            NbrOfCmds = reader.ReadUInt16(); // read Number Of Commands 
            reader.ReadUInt16(); // discard sequence number 
            reader.ReadUInt16(); // discard reserved 
 
            // Loop over commands 
            for (int i = 0; i < NbrOfCmds; i++) 
            { 
                UInt16 size = reader.ReadUInt16(); // read size 
                FdxCommandE cmd = (FdxCommandE)reader.ReadUInt16(); // read command 
                switch (cmd) 
                { 
                    case FdxCommandE.DataExchange: 
                        reader.ReadUInt16(); // discard reserved 
                        UInt16 dataSize = reader.ReadUInt16(); // read data size 
                        byte[] ReadData = reader.ReadBytes(dataSize); // read all Data 
                        // display data 
                        tbRcvData.Text += BitConverter.ToString(ReadData); 
                        break; 
 
                    case FdxCommandE.Status: 
                        // read current state of the measurement. 
                        MeasurementState = reader.ReadByte();  
                        reader.ReadBytes(3); // discard 3 unused bytes 
                        TimeStamp = reader.ReadInt64(); // read time stamp 
                        // Display TimeStamp 
                        TimeSpan t = TimeSpan.FromTicks(TimeStamp / 100); 
                        label2.Text = t.ToString(); 
                        break; 
 
                    case FdxCommandE.DataError: 
                        throw new ApplicationException("DataError CMD received."); 
 
                    default: 
                        reader.ReadBytes(size - 4); // discard data for this command 
                        break; 
                } 
            } 
 
            ms.Close(); 
            writer.Close(); 


| // Add Command |  |
| --- | --- |
| writer.Write((UInt16)6); // Size of Command |  |
| writer.Write((UInt16)FdxCommandE.DataRequest); |  |
| writer.Write(gIDread); // specify Group ID |  |

| // Send Data |  |
| --- | --- |
| _Client.Send(ms.ToArray(), (int)ms.Length); |  |

| // Wait for an answer |  |
| --- | --- |
| ms = ReceiveDatagram(500); |  |

| // get data |  |  |
| --- | --- | --- |
| BinaryReader reader = new BinaryReader(ms); |  |  |
| tbRcvData.Text = ""; |  |  |

| case FdxCommandE.DataError: |  |
| --- | --- |
| throw new ApplicationException("DataError CMD received."); |  |

| default: |  |
| --- | --- |
| reader.ReadBytes(size - 4); // discard data for this command |  |
| break; |  |
| } |  |
| } |  |

| ms.Close(); |  |
| --- | --- |
| writer.Close(); |  |


---

 
 
Fast Data Exchange with CANoe 
 
 
15 
Application Note AN-AND-1-119 
 
            reader.Close(); 
        } 
 
Note that the code is nearly the same as sending the Start Command. The code varies starting with the 
_Client.Send(…) call.  
Now, the newly introduced ReceiveDatagram() helper function is used. Take note that a 500ms timeout is used 
due to the UdpClient’s receive functionality’s blocking nature. ReceiveDatagram() will return the data as a 
MemoryStream, which is the input for a BinaryReader.  
The BinaryReader eases parsing of the datagram. For this example, only the number of commands in the 
datagram header is of interest. All other data fields will be discarded.  
Following the datagram header, the data stream contains the different commands sent by CANoe. The expected 
responses for DataRequest command are (1) a Status command and (2) a DataExchange command containing 
the requested data. If CANoe encounters an error, a DataError command will be sent. 
Since the number of commands is known, a “for” loop is used to handle the DataExchange, Status and DataError 
commands. The DataExchange and Status commands will be decoded while the DataError Command will throw 
an ApplicationException. The DataExchange command contains the requested data and the Status command 
contains the current measurement state and a timestamp from CANoe.  
6.0 Standalone Mode 
CANoe FDX can also be used if CANoe is running on a Realtime-Module (e.g., VN8900 or VT6000). To get the 
example running on a Realtime-Module, the CANoe configuration must be altered. Follow these instructions to 
enable standalone mode: 
1. Connect the HW. 
2. Configure CANoe to run the measurement in either RT Mode or Standalone Mode. 
Note: Please refer to the CANoe Help, if you have problems setting up these Modes. 
CANoe Help VN8900: 
CANoe | Extensions | VN8900 | Interactive Mode over USB | Interactive Mode over IP | Standalone Mode 
CANoe Help VT6000: 
CANoe | Extensions | VT System | Modules | VT6000 | Prerequisites and Configuration 
3. FDX requires an IP address and Port for the HW device to operate. 
4. Configure the client PC to use a static IP address. 
5. Start the client application and enter the correct IP address and Port. 
 
 
 
 


| reader.Close(); |  |
| --- | --- |
| } |  |


---

 
 
Fast Data Exchange with CANoe 
 
 
16 
Application Note AN-AND-1-119 
 
7.0 Additional Resources 
Vector provides various application notes (visit vector.com to obtain them) pertaining to CANoe and its features. 
The following document may provide further useful information: 
FDX Protocol Documentation: CANoe_FDX_Protocol_EN.pdf – included in the CANoe installation 
8.0 Contacts 
For a full list with all Vector locations and addresses worldwide, please visit http://vector.com/contact/. 
 
 
 

---

 
 
Fast Data Exchange with CANoe 
 
 
17 
Application Note AN-AND-1-119 
 
9.0 Appendix 
This Appendix contains the source files necessary to recreate the sample program discussed throughout this 
document. Form1.cs implements all of the FDX functionality and Form1.Designer.cs creates the WindowsForm 
(GUI). 
9.1 Form1.cs 
using System; 
using System.Windows.Forms; 
using System.IO; 
using System.Net; 
using System.Net.Sockets; 
using System.Diagnostics; 
using System.Text; 
using System.Collections.Generic; 
 
namespace EasyClientNet 
{ 
    public partial class Form1 : Form 
    { 
        // UDP Client for the communication 
        private UdpClient _Client; 
         
        private enum FdxCommandE 
        { 
            Start = 0x0001, 
            Stop = 0x0002, 
            Key = 0x0003, 
            DataRequest = 0x0006, 
            DataExchange = 0x0005, 
            DataError = 0x0007, 
            FreeRunning = 0x0008, 
            FreeRunningCancel = 0x0009, 
            Status = 0x0004, 
            StatusRequest = 0x000A, 
            SeqNumError = 0x000B, 
        } 
 
        // +++++++++++++++++ Settings for FDX ++++++++++++++++++++++++++++++++++ 
        // Connection 
        string IpAdr = "127.0.0.1"; 
        int Port = 2809; 
        // Data Group IDs 
        const ushort gIDread = 1; 
        const ushort gIDwrite = 2; 
 
        // +++++++++++++++++ Header ++++++++++++++++++++++++++++++++++++++++++++ 
        // Signature 
        const UInt64 SIGNATURE = 0x584446656F4E4143; 
        // Protocol version 
        const Byte MajorVersion = 1; 
        const Byte MinorVersion = 0; 
        // In this example only 1 command is send at a time 
        const UInt16 NumberOfCommands = 1; 
        // SequenceNumber 
        UInt16 SequenceNumber = 0x8000; 
        // 2 unused bytes for better alignment. 
        const UInt16 Reserved = 0x0000; 


| namespace EasyClientNet |  |
| --- | --- |
| { |  |
| public partial class Form1 : Form |  |
| { |  |
| // UDP Client for the communication |  |
| private UdpClient _Client; |  |


---

 
 
Fast Data Exchange with CANoe 
 
 
18 
Application Note AN-AND-1-119 
 
         
 
        public Form1() 
        { 
            InitializeComponent(); 
        } 
 
        private MemoryStream ReceiveDatagram() 
        { 
            //IPEndPoint object will allow us to read datagrams sent from any source. 
            IPEndPoint remoteIpEndPoint = new IPEndPoint(IPAddress.Any, 0); 
            // receive and read data 
            byte[] receiveBuffer = _Client.Receive(ref remoteIpEndPoint); 
            // put data in a MemoryStream 
            MemoryStream ms = new MemoryStream(receiveBuffer); 
 
            return ms; 
        } 
 
        private MemoryStream ReceiveDatagram(int timeout_ms) 
        { 
            // set the client timeout 
            _Client.Client.ReceiveTimeout = timeout_ms; 
            MemoryStream response = null; 
            try 
            { 
                // receive a datagram 
                response = ReceiveDatagram(); 
            } 
            catch (SocketException se) 
            { 
                if (se.SocketErrorCode != SocketError.TimedOut) 
                { 
                    return response; 
                } 
            } 
            return response; 
        } 
 
        private void btConnect_Click(object sender, EventArgs e) 
        { 
            // connect to the Host/ CANoe 
            _Client = new UdpClient(); 
            _Client.Connect(IpAdr, Port); 
        } 
 
        private void btDisconnect_Click(object sender, EventArgs e) 
        { 
            // Close UDP Socket 
            _Client.Close(); 
        } 
 
        private void btStartMeasure_Click(object sender, EventArgs e) 
        {//Start Meas 
 
            MemoryStream ms = new MemoryStream(); 
            BinaryWriter writer = new BinaryWriter(ms); 
 


| public Form1() |  |
| --- | --- |
| { |  |
| InitializeComponent(); |  |
| } |  |

| return ms; |  |
| --- | --- |
| } |  |

| private void btStartMeasure_Click(object sender, EventArgs e) |  |
| --- | --- |
| {//Start Meas |  |

| MemoryStream ms = new MemoryStream(); |  |
| --- | --- |
| BinaryWriter writer = new BinaryWriter(ms); |  |


---

 
 
Fast Data Exchange with CANoe 
 
 
19 
Application Note AN-AND-1-119 
 
            // Assemble Header 
            writer.Write(SIGNATURE); 
            writer.Write(MajorVersion); 
            writer.Write(MinorVersion); 
            writer.Write(NumberOfCommands); 
            writer.Write(SequenceNumber); 
            writer.Write(Reserved); 
 
            // Add Command 
            writer.Write((UInt16)4); // Size of Command = Size field + Command 
            writer.Write((UInt16)FdxCommandE.Start); 
 
            // Send Data 
            _Client.Send(ms.ToArray(), (int)ms.Length); 
             
            writer.Close(); 
            ms.Close(); 
        } 
 
        private void btStopMeasure_Click(object sender, EventArgs e) 
        {//Stop meas 
 
            MemoryStream ms = new MemoryStream(); 
            BinaryWriter writer = new BinaryWriter(ms); 
 
            // Assemble Header 
            writer.Write(SIGNATURE); 
            writer.Write(MajorVersion); 
            writer.Write(MinorVersion); 
            writer.Write(NumberOfCommands); 
            writer.Write(SequenceNumber); 
            writer.Write(Reserved); 
 
            // Add Command 
            writer.Write((UInt16)4); // Size of Command = Size field + Command 
            writer.Write((UInt16)FdxCommandE.Stop); 
 
            // Send Data 
            _Client.Send(ms.ToArray(), (int)ms.Length); 
 
            writer.Close(); 
            ms.Close(); 
        } 
 
        private void btReqData_Click(object sender, EventArgs e) 
        { 
            UInt16 NbrOfCmds; 
            MemoryStream ms = new MemoryStream(); 
            BinaryWriter writer = new BinaryWriter(ms); 
            byte MeasurementState = 0; 
            Int64 TimeStamp = 0; 
 
            // Assemble Header 
            writer.Write(SIGNATURE); 
            writer.Write(MajorVersion); 
            writer.Write(MinorVersion); 
            writer.Write(NumberOfCommands); 
            writer.Write(SequenceNumber); 


| // Add Command |  |  |
| --- | --- | --- |
| writer.Write((UInt16)4); // Size of Command = Size field + Command |  |  |
| writer.Write((UInt16)FdxCommandE.Start); |  |  |

| // Send Data |  |
| --- | --- |
| _Client.Send(ms.ToArray(), (int)ms.Length); |  |

| private void btStopMeasure_Click(object sender, EventArgs e) |  |
| --- | --- |
| {//Stop meas |  |

| MemoryStream ms = new MemoryStream(); |  |
| --- | --- |
| BinaryWriter writer = new BinaryWriter(ms); |  |

| // Add Command |  |  |
| --- | --- | --- |
| writer.Write((UInt16)4); // Size of Command = Size field + Command |  |  |
| writer.Write((UInt16)FdxCommandE.Stop); |  |  |

| // Send Data |  |
| --- | --- |
| _Client.Send(ms.ToArray(), (int)ms.Length); |  |

| // Assemble Header |  |
| --- | --- |
| writer.Write(SIGNATURE); |  |
| writer.Write(MajorVersion); |  |
| writer.Write(MinorVersion); |  |
| writer.Write(NumberOfCommands); |  |
| writer.Write(SequenceNumber); |  |


---

 
 
Fast Data Exchange with CANoe 
 
 
20 
Application Note AN-AND-1-119 
 
            writer.Write(Reserved); 
 
            // Add Command 
            writer.Write((UInt16)6); // Size of Command 
            writer.Write((UInt16)FdxCommandE.DataRequest); 
            writer.Write(gIDread); // specify Group ID 
 
            // Send Data 
            _Client.Send(ms.ToArray(), (int)ms.Length); 
 
            // Wait for an answer 
            ms = ReceiveDatagram(500); 
 
            // get data 
            BinaryReader reader = new BinaryReader(ms); 
            tbRcvData.Text = ""; 
 
            reader.ReadUInt64(); // discard signature 
            reader.ReadByte();   // discard Major Version 
            reader.ReadByte();   // discard Minor version 
            NbrOfCmds = reader.ReadUInt16(); // read Number Of Commands 
            reader.ReadUInt16(); // discard sequence number 
            reader.ReadUInt16(); // discard reserved 
 
            // Loop over commands 
            for (int i = 0; i < NbrOfCmds; i++) 
            { 
                UInt16 size = reader.ReadUInt16(); // read size 
                FdxCommandE cmd = (FdxCommandE)reader.ReadUInt16(); // read command 
                switch (cmd) 
                { 
                    case FdxCommandE.DataExchange: 
                        reader.ReadUInt16(); // discard reserved 
                        UInt16 dataSize = reader.ReadUInt16(); // read data size 
                        byte[] ReadData = reader.ReadBytes(dataSize); // read all Data 
                        // display data 
                        tbRcvData.Text += BitConverter.ToString(ReadData); 
                        break; 
 
                    case FdxCommandE.Status: 
                        // read current state of the measurement.  
                        MeasurementState = reader.ReadByte(); 
                        reader.ReadBytes(3); // discard 3 unused bytes 
                        TimeStamp = reader.ReadInt64(); // read time stamp 
                        // Display TimeStamp 
                        TimeSpan t = TimeSpan.FromTicks(TimeStamp / 100); 
                        label2.Text = t.ToString(); 
                        break; 
 
                    case FdxCommandE.DataError: 
                        throw new ApplicationException("DataError CMD received."); 
 
                    default: 
                        reader.ReadBytes(size - 4); // discard data for this command 
                        break; 
                } 
            } 
 


| // Add Command |  |
| --- | --- |
| writer.Write((UInt16)6); // Size of Command |  |
| writer.Write((UInt16)FdxCommandE.DataRequest); |  |
| writer.Write(gIDread); // specify Group ID |  |

| // Send Data |  |
| --- | --- |
| _Client.Send(ms.ToArray(), (int)ms.Length); |  |

| // Wait for an answer |  |
| --- | --- |
| ms = ReceiveDatagram(500); |  |

| // get data |  |  |
| --- | --- | --- |
| BinaryReader reader = new BinaryReader(ms); |  |  |
| tbRcvData.Text = ""; |  |  |

| case FdxCommandE.DataError: |  |
| --- | --- |
| throw new ApplicationException("DataError CMD received."); |  |

| default: |  |
| --- | --- |
| reader.ReadBytes(size - 4); // discard data for this command |  |
| break; |  |
| } |  |
| } |  |


---

 
 
Fast Data Exchange with CANoe 
 
 
21 
Application Note AN-AND-1-119 
 
            ms.Close(); 
            writer.Close(); 
            reader.Close(); 
        } 
 
        private void btSendData_Click(object sender, EventArgs e) 
        { 
            MemoryStream ms = new MemoryStream(); 
            BinaryWriter writer = new BinaryWriter(ms); 
 
            // Assemble Header 
            writer.Write(SIGNATURE); 
            writer.Write(MajorVersion); 
            writer.Write(MinorVersion); 
            writer.Write(NumberOfCommands); 
            writer.Write(SequenceNumber); 
            writer.Write(Reserved); 
 
            // Add Command 
            writer.Write((UInt16)13); // Size of Command (8+dataSize)  
            writer.Write((UInt16)FdxCommandE.DataExchange); 
            writer.Write(gIDwrite); // specify Group ID = 2 
            writer.Write((UInt16)5); // write data size (Size of DataGroup 2) 
 
            // set data 
            // EngineSpeedEntry = 0x03e8 = 1000 
            // EngineStateSwitch = 1 
            // FlashLight = 1 
            // HeadLight = 1 
            byte[] data = { 0xe8, 0x03, 0x01, 0x01, 0x01 }; 
 
            // data as byte array 
            // 0 offset in the byte array 
            // 5 length of byte array 
            writer.Write(data, 0, 5); // write data 
 
            // Send Data 
            _Client.Send(ms.ToArray(), (int)ms.Length); 
 
            ms.Close(); 
            writer.Close(); 
        } 
    } 
} 
 
 
 
 


| ms.Close(); |  |  |
| --- | --- | --- |
| writer.Close(); |  |  |
| reader.Close(); |  |  |
| } |  |  |

| // Send Data |  |
| --- | --- |
| _Client.Send(ms.ToArray(), (int)ms.Length); |  |

| ms.Close(); |  |
| --- | --- |
| writer.Close(); |  |
| } |  |
| } |  |
| } |  |


---

 
 
Fast Data Exchange with CANoe 
 
 
22 
Application Note AN-AND-1-119 
 
9.2 Form1.Designer.cs 
namespace EasyClientNet 
{ 
    partial class Form1 
    { 
        /// <summary> 
        /// Required designer variable. 
        /// </summary> 
        private System.ComponentModel.IContainer components = null; 
 
        /// <summary> 
        /// Clean up any resources being used. 
        /// </summary> 
        /// <param name="disposing">true if managed resources should be disposed; otherwise, 
false.</param> 
        protected override void Dispose(bool disposing) 
        { 
            if (disposing && (components != null)) 
            { 
                components.Dispose(); 
            } 
            base.Dispose(disposing); 
        } 
 
        #region Windows Form Designer generated code 
 
        /// <summary> 
        /// Required method for Designer support - do not modify 
        /// the contents of this method with the code editor. 
        /// </summary> 
        private void InitializeComponent() 
        { 
            this.groupBox1 = new System.Windows.Forms.GroupBox(); 
            this.btDisconnect = new System.Windows.Forms.Button(); 
            this.btConnect = new System.Windows.Forms.Button(); 
            this.btStartMeasure = new System.Windows.Forms.Button(); 
            this.groupBox3 = new System.Windows.Forms.GroupBox(); 
            this.tbRcvData = new System.Windows.Forms.TextBox(); 
            this.btReqData = new System.Windows.Forms.Button(); 
            this.groupBox4 = new System.Windows.Forms.GroupBox(); 
            this.label1 = new System.Windows.Forms.Label(); 
            this.btSendData = new System.Windows.Forms.Button(); 
            this.groupBox2 = new System.Windows.Forms.GroupBox(); 
            this.btStopMeasure = new System.Windows.Forms.Button(); 
            this.label2 = new System.Windows.Forms.Label(); 
            this.groupBox1.SuspendLayout(); 
            this.groupBox3.SuspendLayout(); 
            this.groupBox4.SuspendLayout(); 
            this.groupBox2.SuspendLayout(); 
            this.SuspendLayout(); 
            //  
            // groupBox1 
            //  
            this.groupBox1.Controls.Add(this.btDisconnect); 
            this.groupBox1.Controls.Add(this.btConnect); 
            this.groupBox1.Location = new System.Drawing.Point(13, 13); 
            this.groupBox1.Name = "groupBox1"; 


| /// <summary> |  |
| --- | --- |
| /// Required method for Designer support - do not modify |  |
| /// the contents of this method with the code editor. |  |
| /// </summary> |  |
| private void InitializeComponent() |  |
| { |  |
| this.groupBox1 = new System.Windows.Forms.GroupBox(); |  |
| this.btDisconnect = new System.Windows.Forms.Button(); |  |
| this.btConnect = new System.Windows.Forms.Button(); |  |
| this.btStartMeasure = new System.Windows.Forms.Button(); |  |
| this.groupBox3 = new System.Windows.Forms.GroupBox(); |  |
| this.tbRcvData = new System.Windows.Forms.TextBox(); |  |
| this.btReqData = new System.Windows.Forms.Button(); |  |
| this.groupBox4 = new System.Windows.Forms.GroupBox(); |  |
| this.label1 = new System.Windows.Forms.Label(); |  |
| this.btSendData = new System.Windows.Forms.Button(); |  |
| this.groupBox2 = new System.Windows.Forms.GroupBox(); |  |
| this.btStopMeasure = new System.Windows.Forms.Button(); |  |
| this.label2 = new System.Windows.Forms.Label(); |  |
| this.groupBox1.SuspendLayout(); |  |
| this.groupBox3.SuspendLayout(); |  |
| this.groupBox4.SuspendLayout(); |  |
| this.groupBox2.SuspendLayout(); |  |
| this.SuspendLayout(); |  |
| // |  |
| // groupBox1 |  |
| // |  |
| this.groupBox1.Controls.Add(this.btDisconnect); |  |
| this.groupBox1.Controls.Add(this.btConnect); |  |
| this.groupBox1.Location = new System.Drawing.Point(13, 13); |  |
| this.groupBox1.Name = "groupBox1"; |  |


---

 
 
Fast Data Exchange with CANoe 
 
 
23 
Application Note AN-AND-1-119 
 
            this.groupBox1.Size = new System.Drawing.Size(228, 51); 
            this.groupBox1.TabIndex = 0; 
            this.groupBox1.TabStop = false; 
            this.groupBox1.Text = "Connection"; 
            //  
            // btDisconnect 
            //  
            this.btDisconnect.Location = new System.Drawing.Point(115, 19); 
            this.btDisconnect.Name = "btDisconnect"; 
            this.btDisconnect.Size = new System.Drawing.Size(102, 23); 
            this.btDisconnect.TabIndex = 5; 
            this.btDisconnect.Text = "Disconnect"; 
            this.btDisconnect.UseVisualStyleBackColor = true; 
            this.btDisconnect.Click += new System.EventHandler(this.btDisconnect_Click); 
            //  
            // btConnect 
            //  
            this.btConnect.Location = new System.Drawing.Point(7, 19); 
            this.btConnect.Name = "btConnect"; 
            this.btConnect.Size = new System.Drawing.Size(102, 23); 
            this.btConnect.TabIndex = 4; 
            this.btConnect.Text = "Connect"; 
            this.btConnect.UseVisualStyleBackColor = true; 
            this.btConnect.Click += new System.EventHandler(this.btConnect_Click); 
            //  
            // btStartMeasure 
            //  
            this.btStartMeasure.Location = new System.Drawing.Point(7, 19); 
            this.btStartMeasure.Name = "btStartMeasure"; 
            this.btStartMeasure.Size = new System.Drawing.Size(102, 42); 
            this.btStartMeasure.TabIndex = 0; 
            this.btStartMeasure.Text = "Start Measurement"; 
            this.btStartMeasure.UseVisualStyleBackColor = true; 
            this.btStartMeasure.Click += new System.EventHandler(this.btStartMeasure_Click); 
            //  
            // groupBox3 
            //  
            this.groupBox3.Controls.Add(this.label2); 
            this.groupBox3.Controls.Add(this.tbRcvData); 
            this.groupBox3.Controls.Add(this.btReqData); 
            this.groupBox3.Location = new System.Drawing.Point(13, 154); 
            this.groupBox3.Name = "groupBox3"; 
            this.groupBox3.Size = new System.Drawing.Size(228, 87); 
            this.groupBox3.TabIndex = 3; 
            this.groupBox3.TabStop = false; 
            this.groupBox3.Text = "Receive Data"; 
            //  
            // tbRcvData 
            //  
            this.tbRcvData.Location = new System.Drawing.Point(7, 50); 
            this.tbRcvData.Name = "tbRcvData"; 
            this.tbRcvData.Size = new System.Drawing.Size(210, 20); 
            this.tbRcvData.TabIndex = 1; 
            //  
            // btReqData 
            //  
            this.btReqData.Location = new System.Drawing.Point(7, 20); 
            this.btReqData.Name = "btReqData"; 

---

 
 
Fast Data Exchange with CANoe 
 
 
24 
Application Note AN-AND-1-119 
 
            this.btReqData.Size = new System.Drawing.Size(86, 23); 
            this.btReqData.TabIndex = 0; 
            this.btReqData.Text = "Request Data"; 
            this.btReqData.UseVisualStyleBackColor = true; 
            this.btReqData.Click += new System.EventHandler(this.btReqData_Click); 
            //  
            // groupBox4 
            //  
            this.groupBox4.Controls.Add(this.label1); 
            this.groupBox4.Controls.Add(this.btSendData); 
            this.groupBox4.Location = new System.Drawing.Point(14, 247); 
            this.groupBox4.Name = "groupBox4"; 
            this.groupBox4.Size = new System.Drawing.Size(227, 115); 
            this.groupBox4.TabIndex = 4; 
            this.groupBox4.TabStop = false; 
            this.groupBox4.Text = "Send Data"; 
            //  
            // label1 
            //  
            this.label1.AutoSize = true; 
            this.label1.Location = new System.Drawing.Point(10, 49); 
            this.label1.Name = "label1"; 
            this.label1.Size = new System.Drawing.Size(178, 52); 
            this.label1.TabIndex = 9; 
            this.label1.Text = "EngineSpeedEntry = 0x03e8 = 1000\r\nEngineStateSwitch = 
1\r\nFlashLight = 1\r\nHeadLigh" + 
    "t = 1"; 
            //  
            // btSendData 
            //  
            this.btSendData.Location = new System.Drawing.Point(10, 19); 
            this.btSendData.Name = "btSendData"; 
            this.btSendData.Size = new System.Drawing.Size(98, 23); 
            this.btSendData.TabIndex = 8; 
            this.btSendData.Text = "Send Data"; 
            this.btSendData.UseVisualStyleBackColor = true; 
            this.btSendData.Click += new System.EventHandler(this.btSendData_Click); 
            //  
            // groupBox2 
            //  
            this.groupBox2.Controls.Add(this.btStopMeasure); 
            this.groupBox2.Controls.Add(this.btStartMeasure); 
            this.groupBox2.Location = new System.Drawing.Point(13, 71); 
            this.groupBox2.Name = "groupBox2"; 
            this.groupBox2.Size = new System.Drawing.Size(228, 77); 
            this.groupBox2.TabIndex = 5; 
            this.groupBox2.TabStop = false; 
            this.groupBox2.Text = "Measurement Control"; 
            //  
            // btStopMeasure 
            //  
            this.btStopMeasure.Location = new System.Drawing.Point(115, 19); 
            this.btStopMeasure.Name = "btStopMeasure"; 
            this.btStopMeasure.Size = new System.Drawing.Size(102, 42); 
            this.btStopMeasure.TabIndex = 1; 
            this.btStopMeasure.Text = "Stop Measurement"; 
            this.btStopMeasure.UseVisualStyleBackColor = true; 
            this.btStopMeasure.Click += new System.EventHandler(this.btStopMeasure_Click); 

---

 
 
Fast Data Exchange with CANoe 
 
 
25 
Application Note AN-AND-1-119 
 
            //  
            // label2 
            //  
            this.label2.AutoSize = true; 
            this.label2.Location = new System.Drawing.Point(99, 25); 
            this.label2.Name = "label2"; 
            this.label2.Size = new System.Drawing.Size(0, 13); 
            this.label2.TabIndex = 2; 
            //  
            // Form1 
            //  
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F); 
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font; 
            this.ClientSize = new System.Drawing.Size(253, 374); 
            this.Controls.Add(this.groupBox2); 
            this.Controls.Add(this.groupBox4); 
            this.Controls.Add(this.groupBox3); 
            this.Controls.Add(this.groupBox1); 
            this.Name = "Form1"; 
            this.Text = "easyClient.Net"; 
            this.groupBox1.ResumeLayout(false); 
            this.groupBox3.ResumeLayout(false); 
            this.groupBox3.PerformLayout(); 
            this.groupBox4.ResumeLayout(false); 
            this.groupBox4.PerformLayout(); 
            this.groupBox2.ResumeLayout(false); 
            this.ResumeLayout(false); 
 
        } 
 
        #endregion 
 
        private System.Windows.Forms.GroupBox groupBox1; 
        private System.Windows.Forms.Button btConnect; 
        private System.Windows.Forms.Button btStartMeasure; 
        private System.Windows.Forms.Button btDisconnect; 
        private System.Windows.Forms.GroupBox groupBox3; 
        private System.Windows.Forms.Button btReqData; 
        private System.Windows.Forms.GroupBox groupBox4; 
        private System.Windows.Forms.Button btSendData; 
        private System.Windows.Forms.TextBox tbRcvData; 
        private System.Windows.Forms.GroupBox groupBox2; 
        private System.Windows.Forms.Button btStopMeasure; 
        private System.Windows.Forms.Label label1; 
        private System.Windows.Forms.Label label2; 
    } 
} 
 
 

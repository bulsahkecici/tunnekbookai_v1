## Research on Automatic Patrol Inspection Technology Scheme for Safe Operation of Super Long and Long Span Highway Tunnel

## Jing Luo 1 , Shengtao Ma 2 , Chengqian Zhu 3 , Guohua He 4

1 Guizhou Expressway Group Co., Ltd, Guiyang 550001, China

- 2 Guizhou Transportation Planning, Survey, Design and Research Institute Co., Ltd, Guiyang 550081, China
- 3 Guizhou Transportation Planning, Survey, Design and Research Institute Co., Ltd, Guiyang 550081, China

4 Guizhou Expressway Group Co., Ltd, Guiyang 550001, China

Abstract: Firstly,  this  paper  conducts  systematic  research  on  tunnel  fire  and  traffic  incident  detection  technologies,  and develops a high-precision monitoring and detection implementation plan for ultra-long and large-span tunnels; Secondly, in terms of tunnel fire detection, video thermal imaging technology is used as the main detection method, combined with dual wavelength flame detectors, to achieve fire open fire monitoring and pure smoke detection, making up for the blind spots of traditional fire detection, and improving the accuracy, timeliness, and reliability of monitoring. In terms of traffic incident detection, based on traditional traffic incident detection technology and advanced technical means, the system mainly focuses on lightning visual integration detection, combined with artificial video monitoring, to comprehensively judge the status of tunnel traffic incidents, thereby  reducing  the  false  alarm  rate  of  incident  detection.  Finally,  based  on  the  technical  research  scheme,  an  intelligent automatic patrol robot was developed using the mobile automatic patrol mode. Using this as a carrier, various sensor modules and emergency equipment were built to replace manual 24-hour uninterrupted full coverage patrols, achieving automatic patrol, automatic reporting, analysis, early warning, and emergency response for ultra-long tunnels, reducing the cost of manual patrols and improving the efficiency of patrols, Enhanced emergency response capabilities of operating units.

Keywords: Ultra  long  and  large  span  tunnels,  High-precision  monitoring,  Fire  detection,  Traffic  incident  identification, Automatic patrol inspection, Safe operation.

## 1. Introduction

With  the  continuous  increase  in  the  total  mileage  of expressways  in  China  and  the  gradual  improvement  of network  topology,  expressways  have  gradually  developed from the infrastructure stage to intelligent operation. As an important  component  of  expressways,  tunnels  shorten  the mileage while also reducing the travel time between the two places.  However,  the  tunnel  is  a  semi  enclosed  tubular structure[1], and once a traffic accident occurs, it will lead to serious consequences, even causing casualties. Tunnel traffic accidents  are  mainly  manifested  in  two  categories,  one  is traffic  accidents  caused  by  fire,  and  the  other  is  secondary accidents triggered by tunnel traffic events (including traffic accidents,  vehicle  failures,  cargo  spillage,  temporary  road maintenance,  etc.  [2]).  Taking  fire  as  an  example,  fire accidents are the most important type of accidents faced by highway tunnels. Highway tunnels, especially Tongzi Tunnel, are relatively closed in space, with limited escape conditions in the tunnel, fewer hot smoke outlets, and once a fire occurs, the heating speed is fast, the duration is long, and it is difficult for firefighters to enter. This increases the risk of driving. At the  same  time,  due  to  the  large  number  of  vehicles  in  the tunnel, high speed, high wind speed, high risk, and difficulty in fighting, the design of the tunnel fire alarm system should aim to prevent accidents, detect them as soon as possible, and put out the fire as soon as possible.

Currently, a lot of research has been done on tunnel safety issues, especially tunnel fires and traffic accidents, at home and abroad, and certain results have been achieved. However, there  are  still  a  lot  of  defects  and  shortcomings,  mainly manifested in the following two aspects:

- 1) Large detection error of tunnel fire and traffic accident monitoring equipment

The detection of incidents affecting the safe operation of tunnels at home and abroad has a single type and large error, with shortcomings such as missing reports, high false alarm rates,  and  timely  extension.  For  example,  the  equipment commonly  used  to  monitor  fire  accidents  in  tunnels  relies solely  on  a  single  fire  detector.  Due  to  various  physical phenomena associated with the occurrence of tunnel fires, and due  to  the  limitations  of  the  equipment's  own  detection performance,  relying  solely  on  a  single  detection  device  is easily  affected  by  the  external  environment,  resulting  in inaccurate detection, high latency, missed detection, or false detection issues.

- 2)  The  construction  of  the  linkage  mechanism  between various  electromechanical  equipment  in  the  tunnel  is  not perfect

The  survey  found  that  the  construction  of  the  linkage mechanism  between  various  electromechanical  devices  in tunnels in China is extremely imperfect, and there is a lack of effective  communication  between  detection  equipment  and alarm and treatment equipment, making detection equipment unable  to  perform  a  good  alarm,  guidance,  and  treatment function on the premise of detecting tunnel safety accidents, leading to the unlimited development of various traffic events in tunnels, resulting in serious losses.

The  occurrence  of  traffic  accidents  or  fire  accidents  in tunnels is the two most important factors that affect the safe operation and management of tunnels, and there may be chain reactions  between  them.  Based  on  this,  this  article  takes Tongzi Tunnel as the foundation, and aims to achieve highprecision monitoring and prediction of fire and traffic events in tunnels as the research goal, to fill the design blind spots, optimize and supplement  the detection performance  of traditional  equipment,  and  achieve  all-round  coverage  of detection in tunnels, It is of great significance to establish a corresponding incident early warning system for improving the safe operation of ultra long and large span tunnels.

Tongzi Tunnel is located in the Chongqing Zunyi Section (Guizhou  Province)  Expansion  Project  of  Lanzhou  Haikou National Expressway. It is a control project of the Chongzun Expansion Project, with a total length of 10497 meters, and is currently the longest tunnel in Guizhou Province's expressway project.

## 2. Research on Fire Detection Technology for Super Long and Long Span Tunnel

Based on the research of fire  detection  schemes  in  ultra long and large span tunnels, this paper intends to start with both open and non open flames, using video thermal imaging technology to achieve dual detection of open and non open flames in tunnels, introducing smoke detectors to achieve non open  fire  smoke  detection,  and  assisting  traditional  dual wavelength  flame  detectors and  temperature sensors in tunnels to achieve rapid identification of fire accident information in tunnels.

## 2.1. Fire Identification

In  the  infrared  general  testing  mode,  an  infrared  thermal imaging map is collected from the equipment for the set area according to the set distance and parameters, and the highest point  within  the  field  of  vision  is  detected  in  real  time. Comparative  analysis  is  conducted  with  the  set  threshold value. When abnormalities are found, they are transmitted to the management personnel through audible and visual alarms and  information  alarms.  The  operation  and  maintenance personnel conduct manual remote control mode review based on  the  alarm  information  or  trigger  special  patrol  tasks  to accurately measure  temperature, Further obtain detailed temperature defect information on the parts and take appropriate countermeasures in a timely manner.

Figure 1 . Fire Accident Detection Based on Infrared Thermal Imaging Technology

<!-- image -->

Engineering drawing

In highway tunnels, temperature anomalies such as vehicle collisions, spontaneous combustion, and equipment combustion are mainly reflected in heat generation. However, the  tunnel  environment  is  more  complex  than  the  road outfield  conditions,  and  the  determination  requirements  for fire  accidents  are  higher.  It  is  difficult  to  detect  thermal defects  in  equipment  by  using  ordinary  thermal  imaging technology to detect the highest temperature. Based on this, through targeted development of accurate temperature measurement functions, and based on high-resolution thermal imaging equipment, high-quality infrared thermal map data of patrol objects are obtained, and temperature data collection for different characteristic points of the equipment is achieved.

Figure 2. Schematic diagram of infrared fine measurement function

<!-- image -->

Logo

## 2.2. Tunnel environmental monitoring

Monitor  environmental  information  such  as  CO,  CH4, temperature,  humidity,  and  smoke  in  the  tunnel,  collect environmental information in real time, and transmit it to the control  center  in  a  timely  manner.  This  provides  on-site environmental information for the operation and management personnel to facilitate their decision-making. When harmful gases are detected to exceed the standard, the system will give an alarm to prompt the operation and maintenance personnel to handle them in a timely manner, assisting in the monitoring of tunnel fire accidents.

## 3. Implementation Scheme of Fire Detection and Early Warning System for Super Long and Long Span Tunnel

The realization of early detection and identification of fire in tunnels is an important embodiment of the best fire detector. However, based on the widespread fire detection problems at home  and  abroad,  detection  technology  always  fails  to achieve the effect of early warning and prediction, especially in  the  case  of  fire  accidents  in  ultra  long  and  large  span tunnels.

Based on this, an audible and visual alarm system with a linkage mechanism, a voice prompt system, and an emergency response plan are established. In the event of a fire, relevant information can be transmitted to the fire department or control center through the alarm system. The control center determines several emergency plans that can be applied by investigating  the  robot's  detection  results  about  the  fire accident, And manually or automatically select the scheme to conduct  vehicle  evacuation  and  fire  fighting  work.  The specific  preliminary  plan  for  fire  monitoring  and  early warning is as follows:

- (1) Tunnel construction is based on video thermal imaging technology to continuously monitor the fire in Tongzi Tunnel for 24 hours, realizing dual monitoring of open and non open fire fires in the tunnel;
- (2) Introducing smoke detectors to achieve non open fire monitoring in the early stages of tunnel fires;
- (3) Using multi-source data fusion technology, process and fuse the data collected by fire detection equipment such as temperature detectors, dual wavelength fire detectors, smoke detectors,  and  fire  video  capture  equipment  based  on  deep learning  algorithms  to  determine  whether  a  fire  accident occurs under the monitoring of the tunnel inspection robot;
- (4) Establish a positioning system in the tunnel to accurately  locate  the  fire  accident  point  in  the  ultra-long

tunnel;

(5) Establish an early warning and interception system at the  tunnel  entrance;  Build  a  signal  transmission  module, alarm  system,  and  voice  prompt  system;  Configure  and coordinate emergency guidance facilities, alarm facilities, and fire fighting facilities in the tunnel; Achieve rapid identification,  timely  transmission,  effective  linkage,  and rapid treatment of fire accidents in ultra-long tunnels, achieving the purpose of effective early warning and treatment of fire accidents.

The  implementation  plan  for  fire  detection  and  early warning is shown in Figure 3 below:

Figure 3. Implementation Plan for Fire Detection and Early Warning

<!-- image -->

Flow chart

## 4. Research on Traffic Incident Detection Technology for Super Long and Long Span Tunnels

## 4.1. Traffic Incident Detection Technology Based on Video Image Processing

The  technology  of  automatic  traffic  incident  detection based on video images is one of the hot spots and focuses in the field of intelligent transportation systems. It uses advanced  video  analysis,  pattern  recognition,  data  mining, and other technologies to achieve video based traffic incident detection.

The expressway tunnel traffic incident detection and early warning system consists of tunnel cameras and PTZ, video incident analysis server, incident management server, relevant monitoring  software,  and  warning  equipment.  The  video event  analysis  server  is  the  core  equipment  of  the  entire system, consisting of a video processing unit, image processing software, video signal digitization system, communication  card,  and  corresponding  analysis  software. The  video  event  analysis  server  is  an  intelligent  analysis embedded product based on vehicle behavior, using cuttingedge  intelligent  video  analysis  algorithms  to  automatically identify,  analyze,  and  judge  people,  vehicles,  and  other objects.  Its  functions  include:  acquiring  digital  and  analog video  signals;  Image  analysis  and  processing  using  traffic incident  detection  image  analysis  algorithms;  Store  alarms, analysis  results,  and  images;  Communicate  with  the  event management server. The functions of the event management server include: communicating with the video event analysis server and retrieving event videos uploaded by the analysis server; Centralized alarm, communication with traffic monitoring system equipment and monitoring computers, and joint operation of events  and traffic control measures; Perform unified management, configuration, and maintenance of the entire system. Figure 4 shows the system architecture diagram.

Figure 4. System architecture diagram

<!-- image -->

Flow chart

## 4.2. Implementation Plan for Rapid Identification of Traffic Accidents in Super Long and Long Span Tunnels

Tongzi Tunnel is a super long and large span tunnel, with higher traffic safety risks than short and medium long tunnels. If  only using traffic incident detection technology based on video  image  processing,  it  is  difficult  to  meet  the  traffic incident detection requirements. Therefore, this article proposes  to  establish  the  following  scheme  for  the  traffic incident detection part of Tongzi Super Long Tunnel:

- (1)  Analyze  and  determine  the  area  with  the  highest security risk in the ultra-long tunnel, and build a video event detection system within the area. The core component of the detection  system,  the  traffic  event  detection  algorithm,  is based  on  in-depth  learning  theory,  and  cooperates  with various auxiliary algorithms, analysis and calculation storage servers,  signal  transmission  technology,  and  corresponding

software platforms to achieve traffic event detection in Tongzi Tunnel based on video image processing;

- (2) An omnidirectional radar detection system is installed at a considerable height on the tunnel sidewall corresponding to the detection area in the Tongzi Tunnel to achieve accurate and omnidirectional detection of traffic events in ultra-long and large-span tunnels;
- (3) Set up corresponding traffic electromechanical guidance facilities and link them with the monitoring center to achieve fully automatic response under traffic events;
- (4)  Develop  corresponding  emergency  response  plans  to minimize the hazards and losses of a single incident based on the prevention and control of secondary incidents;
- (5) Design and develop a tunnel operation safety monitoring and early warning platform to achieve monitoring and  early  warning  of  Tongzi  tunnel  fires  and  other  traffic incidents.

Figure 5. Implementation Scheme for Rapid Identification Technology of Tunnel Traffic Accidents

<!-- image -->

Flow chart

## 5. Research on Intelligent Supervision and Inspection System Based on Inspection Robot

## 5.1. Overall structure framework of intelligent inspection robot

This paper introduces an intelligent inspection robot platform for tunnels, and builds various monitoring devices to detect  fire  accidents  and  traffic  incidents  in  tunnels.  The function of the intelligent patrol robot is that it can complete the patrol work of the patrol section according to the preset settings in the automatic state, and can switch to the remote control state at any time. The  intelligent patrol robot maintains contact with the road section center at any time, and can upload environmental parameters and video data in the tunnel to the control center in real-time.

The  intelligent  inspection  robot  is  designed  based  on  a modular approach, including a main control module, a power supply module, a motion control module, a communication module, and a data acquisition module, to achieve automatic inspection of fire and traffic accidents in Tongzi super long and large span tunnel. As shown in Figure 6:

Figure 6. Overall structure framework of intelligent inspection robot

<!-- image -->

Flow chart

The intelligent inspection robot has the following characteristics:

- 1) It can operate around the clock without fatigue; Greater adaptability to harsh environments; Even if there is a danger,

there is no need to worry about personal injury accidents;

- 2)  Forward,  backward,  and  stop, and  achieve speed regulation;
- 3) When stopped, it has braking ability.

Figure 7. Overall Plan

<!-- image -->

Flow chart

## 5.2. Function building of tunnel inspection robot

According  to the tunnel safety operation monitoring content and overall system plan, the functional construction of this intelligent patrol robot should meet the requirements of  fire  accidents  and  traffic  accidents  in  the  tunnel,  and  it should  be  made  as  intelligent  as  possible  on  the  basis  of meeting the basic functions and auxiliary configurations.

Figure 8. System Functions

<!-- image -->

Flow chart

The intelligent patrol robot detects relevant information in real  time  and  processes  it  in  the  background. The  database records all information transmitted by each robot, generates data  charts  in  real  time,  and  reports  exceptions;  Realize functions such as information sharing and device cascading through wireless bridges.

The intelligent inspection robot is installed with multiple sensors  to  achieve  comprehensive  detection  of  the  tunnel traffic operating environment. Using its own mobile function, the robot inspection scheme is set up in the background for detection.  During the inspection process, there are no dead corners in the patrol inspection. After each patrol inspection is completed, the patrol report can be automatically generated and the tunnel operation status can be fed back in a timely manner,  which  can  effectively reduce  the  workload  of operation and maintenance personnel and ensure the safe and stable operation of the tunnel.

## 5.3. System architecture

The intelligent inspection system is mainly composed of automatic  inspection  robots,  carrier  rail  systems,  power supply systems, communication systems, system management platforms, and other auxiliary systems.

## (1) Patrol robot

The inspection robot is the core of an intelligent inspection system, which can use its own front-end acquisition devices such as visible light cameras and infrared thermal imagers to complete  preset  inspection  tasks  in  a  fully  autonomous  or remote  control  manner.  The  appearance  of  the  intelligent inspection robot is as follows:

Figure 9. Schematic Diagram of Intelligent Patrol Robot

<!-- image -->

Photograph

## (2) Track system

The  track  of  the  intelligent  inspection  robot  adopts  a parallel double tube guide rail type track, which has a small vertical dimension and a small overall installation dimension requirement, making it convenient for engineering construction.  The  track  material  is  a  special  high-strength aluminum alloy, and the surface is treated with oxidation and rust  prevention,  which  can  not  only  improve  the  corrosion resistance,  but  also  improve  the  surface  hardness  and  wear resistance.  It  has  the  advantages  of  high  strength,  good stability,  corrosion  prevention,  convenient  installation,  and aesthetics. The track structure is shown in the following figure:

Figure 10. Track Structure Diagram

<!-- image -->

Engineering drawing

control box). The robot is equipped with a large capacity and high-performance lithium battery, combined with a complete power management strategy of the system, to achieve longterm automatic operation.The distributed charging station is shown in the following figure:

## (3) Power supply system

The  intelligent  inspection  robot  uses  a  combination  of battery power supply and distributed non-contact charging to provide power. Multiple wireless charging stations are arranged in the traffic tunnel (powered through the front-end

Figure 11. Schematic Diagram of Distributed Charging

<!-- image -->

Engineering drawing

## (4) Communication system

The  communication  system  is  used  to  achieve  two-way data interaction between the intelligent patrol robot and the system management platform (including various types of data such as control signals, video data, audio data, on-site sensor collection data, and alarm information). The intelligent patrol robot is connected to the control center of the traffic tunnel through a 5G communication network or private network, and then connected to the system management platform through a wired network. The system network structure is shown in the following figure:

Figure 12. Communication System Network Topology Diagram

<!-- image -->

Flow chart

Table 1. Technical Requirements for Intelligent Automatic Patrol Robot

|   Serial Number | Product/Equipment Name                                                                   | Remarks                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
|-----------------|------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|               1 | Foundation preset position PTZ                                                           | Fully preset, digital/network type                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
|               2 | Step drive terminal                                                                      | Linear motion speed support protocol extended 64 level motion speed                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
|               3 | Robot master CPU control board                                                           | It needs to meet the modular hot plug design. The core main control processor is designed using an ARM+DSP architecture, the collaborative transaction processing module is designed using FPGA+DSP, and the power processing module is designed using a DPA architecture; The processor performance should meet the requirements of the quad core A5 architecture 1.2G main processor unit                                                                                                                                                                                                    |
|               4 | Robot communication interface control board                                              | It is necessary to adopt a movable board design, and the chip is packaged with BGA, which is mainly responsible for the switch signal input of robot travel switches, proximity switches, band switch sensors, and other active interfaces such as relay/indicator signal output; Including serial port distributor and other interface                                                                                                                                                                                                                                                        |
|               5 | Robot motion control module board                                                        | components Responsible for the control of the main transmission AC servo motor of the robot, including the driver device module                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
|               6 | Robot bus communication HUB board                                                        | Responsible for data interactive communication between robot audio and video processing, internal bus bridges, camera sensors, and other devices                                                                                                                                                                                                                                                                                                                                                                                                                                               |
|               7 | Operation status audible and visual indication alarm                                     | Installed above the robot for installation warning and operation status indication when the robot moves. If the robot fails, a buzzer alarm will be sent through the alarm                                                                                                                                                                                                                                                                                                                                                                                                                     |
|               8 | Programmable Patrol Track Control Unit                                                   | Capable of providing 1024 programmable control command sets to meet various preset position settings and linkage control requirements on site                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|               9 | Mechanical multi-dimensional dynamic mechanism assembly                                  | Including universal bearing base, elastic telescopic steering block, driving shaft, driving bearing, driving double pulley, driven shaft, driven bearing, driven double pulley, and four sets of adjustable current collectors on both sides, to ensure the stability, signal, and power supply smoothness of the robot during movement                                                                                                                                                                                                                                                        |
|              10 | Modular final assembly control cabinet                                                   | Responsible for carrying various control boards of the robot control system (5 control board slots and 2 redundant modular power supply slots), and providing power supply and general I/O activity interfaces to each modular main board, including redundant                                                                                                                                                                                                                                                                                                                                 |
|              11 | Mechanical transmission drive and electrically controlled telescopic rod                 | modular power supply and industrial cooling system Including transmission system, AC servo motor, incremental photoelectric encoder, elastic damping gear train, balanced and stable guide mechanism, electric telescopic rod, and other components; Including phase corrector                                                                                                                                                                                                                                                                                                                 |
|              12 | Prefabricated end of cloud platform                                                      | It can query the address, speed, controlled command, track length, real-time position of the track machine, speed information, limit switch status, preset setting parameters, etc                                                                                                                                                                                                                                                                                                                                                                                                             |
|              13 | Charging pile                                                                            | One charging pile and 500m supporting cable                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
|              14 | Wireless AP                                                                              | Three wireless APs and 500m supporting optical fiber                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
|              15 | Gas detection module and software                                                        | Monitoring the content of carbon monoxide, nitrogen dioxide, and gas, specifically integrated in the robot body                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
|              16 | Temperature and humidity smoke detection module and software                             | Temperature and humidity detection (air temperature and humidity), smoke detection (PM2.5 PM10), specifically integrated in the robot body                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
|              17 | Photosensitive detection                                                                 | Dual wavelength flame detection, specifically integrated into the robot body                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
|              18 | Robot type                                                                               | Intelligent lithium powered non elevating rail robot                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
|              19 | Wireless receiving electrical box                                                        | TCP/IP network digital signal                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|              20 | Special customized parts                                                                 | U-shaped rail connectors, cross shaped components, 9-hole connectors, expansion plates, 6-hole connectors, adjustable connecting rods, and terminal stability kits (quotation does not include special customized parts, which need to be customized according to the actual situation on site)                                                                                                                                                                                                                                                                                                |
|              21 | Main control system                                                                      | Debugging software, calling software interface, database interface, basic control system platform, computer                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
|              22 | Thermal imaging dual view ball machine                                                   | Visible light, thermal integrated image dual view ball machine, used for thermal imaging fire/video monitoring, mounted on the main body of the robot                                                                                                                                                                                                                                                                                                                                                                                                                                          |
|              24 | Thunder vision integrated machine software                                               | Expenses for access, development, integration, and debugging of Thundervision all-in- one computer software with our company                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
|              25 | Alloy aluminum rail                                                                      | Bearing capacity not less than 100kg (including connection and installation accessories), 3m per section, protection grade: IP65                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
|              26 | Road multi-dimensional perception all-in-one machine (Thunder Vision Integrated Machine) | 1. Fixed installation, frequency band 77GHZ, wavelength 4mm, speed measurement range 2km/h-250km/h; 2. All weather environment support, ICR infrared filter type, 3D digital noise reduction; 3. Forward and backward vehicle monitoring and tracking, with a maximum tracking target of 128; 4. Support the identification of new energy license plates, unlicensed vehicles, motor vehicles, non motor vehicles, and pedestrians, and support Beidou/GPS positioning; 5. Traffic accident detection and traffic flow monitoring in tunnels (vehicle density, vehicle spacing, driving speed) |

(5) System management platform

The system management platform can be connected to a dedicated  network,  through  which  the  staff  of  the  superior unit can access the system management platform to achieve intelligent automatic inspection robot control, data query, task management, data export, and other operations. If there is a communication  interruption  or  data  abnormality,  the  robot will send out a communication alarm indication signal, and the system management platform interface will also immediately send out a communication abnormality alarm to facilitate staff to timely detect and handle the abnormality.

The intelligent automatic patrol system management platform  software  is  designed  using  a  B/S  architecture. System  data  can  be  shared  externally  through  the  external interface of the WEB server, and can be remotely controlled, task configured, video accessed, data accessed, and integrated system management for the patrol robot through a dedicated client software/WEB client.

(4) Technical Requirements

① Autonomous charging

The intelligent automatic patrol robot body comes with a battery level detection circuit that can manually set the lower limit of the battery level alarm. Once the robot detects that the battery level is lower than the set value, it can automatically stop the current patrol task, issue an alarm, and automatically run to the charging point for charging.

② Long battery life

The battery carried by the intelligent automatic inspection robot itself is sufficient to support the robot to  work continuously  for  6  hours  without  power  failure,  and  the charging time is not more than 3 hours, to ensure that the robot can work continuously for more than 16 hours online every day.

③ Flexible testing mechanism

The main detection unit consists of modules such as a highdefinition network camera, an infrared thermal imager, and a high-precision  PTZ.  The  PTZ  can  meet  the  continuous rotation of 0~360 °, with a large holding torque, and will not shift due to camera vibration.

## 5.4. Functional design

The  system  functions  include  basic  capability  detection, traffic  incident  monitoring,  emergency  handling,  auxiliary lighting, etc.

(1) Basic detection capability

The intelligent automatic inspection robot system should be equipped with detection equipment such as visible light cameras, infrared thermal imagers, gas acquisition, and sound acquisition,  and  be  able  to  upload  the  captured  video  and sound to the monitoring background.

A. Video monitoring function

The intelligent  inspection  robot  can  achieve  visible  light and infrared video image acquisition functions. The robot can automatically move to a designated position, control the free rotation  of  the  pan-tilt,  capture  high-definition  images  and infrared thermal imaging of various devices in the tunnel, and transmit the collected information to the main control room in real  time  through  a  wireless  LAN.  The  staff  in  the  main control room can judge the tunnel operation status based on the images.

B. Infrared temperature measurement

The intelligent patrol system can achieve the infrared video image  acquisition  function,  control  the  free  rotation  of  the PTZ, take infrared thermal imaging in the smart tunnel, and transmit the collected information to the main control room in real  time  through  the  LAN.  During  the  automatic  patrol process, it automatically discovers temperature overrun nodes and areas and gives a timely warning.

C. Environmental monitoring function

The  intelligent  inspection  robot  is  equipped  with  a  gas detector, which can analyze the air environment in the tunnel at any time and obtain results, while feeding back the results to the staff in the monitoring room. It can also manually set alarm limits, including low and high temperature alarm limits, humidity  alarm  limits,  and  gas  concentration  alarm  limits. Once  the  limit  values  are  exceeded,  an  audible  and  visual alarm will be given immediately to prevent personnel from misjudging the tunnel environment, causing life hazards.

D. Bidirectional voice intercom function

When unconventional problems occur with equipment in the  tunnel  that  cannot be solved by on-site personnel, realtime interaction between on-site personnel and remote experts can  be  achieved  through  the  video  and  voice  devices  of intelligent automatic inspection robots. Experts can guide and supervise on-site personnel, achieve correct and standardized operations, and contribute to on-site problem resolution. At this point, the robot will accompany the on-site staff to work.

(2) Tunnel environmental monitoring

① Gas monitoring

Tongzi ultra long and large span tunnel frequently crosses unfavorable geology such as karst, faults, high ground stress, and coal seams, among which the gas pressure in the gas coal measures formation is 1.9Mpa. Due to the characteristics of tunnel construction in coal measures strata such as high safety hazards, low work efficiency, high difficulty in gas prediction and  waterproof  sealing,  and  the  significant  impact  of  gas content in the air after  the  completion  of  the  tunnel on  the overall  safe  operation  of  the  tunnel,  the  tunnel  inspection robot needs to attach gas monitoring sensors to the corresponding gas and coal measures strata for key monitoring to prevent high gas concentration from generating safety hazards.

② COVI monitoring

The tunnel inspection robot should also be equipped with a carbon  monoxide  (CO)/visibility  (VI)  integrated  detection device (hereinafter referred to as COVI). The COVI detection equipment  is  used  to  conduct  real-time  COVI  detection  of different areas of the tunnel, and the detection data is used to evaluate  the  specific  conditions  of  different  sections  of  the tunnel air, in order to achieve coordinated  work  with ventilation equipment such as fans, so as to maintain good air conditions in the tunnel.

(3)  Rapid  monitoring  of  traffic  incidents  in  ultra  long tunnels

① Rapid Monitoring Technology of Vehicle Flow Characteristics Based on Video Images

Monitor  the  characteristics  of  traffic  flow  in  the  tunnel, such as flow, speed, and density, through video images, and generate real-time data for storage on  the  background platform.  The  inherent  relationship  between  the  frequency and  characteristics  of  accidents  can  be  analyzed  based  on vehicle flow characteristic data.

② Hazardous Vehicle Identification Technology

Based on the external feature recognition technology for hazardous,  flammable,  and  explosive  vehicles,  there  are several  obvious  differences  between  domestic  hazardous transportation vehicles and  ordinary  freight vehicles. a. Hazard signs are installed on the top of the cab; B. Special orange reflective stickers for dangerous goods will be affixed to all parts of the vehicle body; C. There are generally danger signs on the rear of the vehicle. And the vehicle type is also significantly different from ordinary freight vehicles. Writing the  algorithm  into  the  patrol  robot  chip  can  achieve  the identification and detection of dangerous transportation vehicles.

③ Foreign matter detection on tunnel pavement

Through  video  image  algorithms,  foreign  objects  on  the road are detected, analyzed based on the shape and size of the foreign objects, and judged whether they are causing obstacles to the normal passage of vehicles. Due to the fact that some throwing objects do not affect vehicle traffic, their shape and size have a certain impact on the driver, and the driver may cause tunnel accidents due to improper operation. Therefore, such foreign matters must be artificially removed. The tunnel inspection robot is equipped with communication devices and precise positioning devices, which can communicate information with operation management personnel, accurately inform the location of foreign matters on the road surface and the way to handle them. The operation management personnel can also directly and remotely view the  video  camera  information  of  the  inspection  robot  to determine  the  type  of  foreign  matters  on  the  road,  thereby quickly and effectively handling foreign matters on the road.

④ Detection of vehicle parking violations in tunnels

Illegal  parking  of  vehicles  in  tunnels  poses  a  significant safety hazard, with relatively narrow visibility in the tunnel, making  it  difficult  for  drivers  to  distinguish  the  status  of vehicles in front of them in a single dark environment in the tunnel, which may lead to serious traffic accidents. Therefore, the  tunnel  robot  detects  stationary  vehicles  in  the  tunnel through its onboard video monitoring system. If a violation of parking regulations is found, the patrol robot will run to the front  of  the  vehicle  and  warn  the  violation  of  parking regulations  through  its  equipped  audible  and  visual  alarm device.  The  tunnel  robot  is  also  equipped  with  a  voice intercom  remote  broadcast  system,  which  allows  operation management personnel to notify drivers of parked vehicles through remote calls.

⑤ Traffic accident detection

Through the detection and analysis carried out by the video camera,  it  can  quickly  respond  to  traffic  accidents  in  the tunnel, including traffic accidents, parking, retrograde traffic, traffic jams, pedestrians, etc.

⑥ Fire accident detection

Equipped with smoke detectors, temperature detectors, and video thermal imagers, it can quickly detect and accurately locate the occurrence of fires, and alarm through audible and visual alarms. It can be connected to the operating platform through communication equipment to send an alarm.

(3) Emergency handling function

During  the  daily  inspection  process,  when  an  intelligent automatic  inspection  robot  detects  a  traffic  accident  in  a tunnel, it can arrive at the scene as soon as possible, issue an alarm, and upload a real-time location. Detect the concentration of smoke and harmful gases in the tunnel at the same  time,  and  only  when  it  is  safe  and  controllable  can rescue  personnel  enter  the  scene,  greatly  shortening  rescue time and reducing the risk factor.

① Accurate and active fire extinguishing technology The  intelligent  automatic  patrol  robot  is  equipped  with temperature, smoke, and thermal imaging detection devices, and can accurately locate the fire source. For a fire that has just  occurred  but  has  not  spread,  the  intelligent  automatic patrol robot can accurately extinguish the fire through its own positioning device and fire extinguishing device.

② Assistance in rescue technology

For large fires with widespread fire, intelligent automatic inspection  robots  can  timely  alarm  and  notify  operation management personnel, control corresponding variable information  signs  and  traffic  lights.  Quickly  and  orderly arrange the evacuation of personnel and vehicles inside the tunnel  through  audible  and  visual  alarm  devices  and  voice systems.  Real-time  monitoring  of  fire  conditions  through temperature  and  smoke  sensors  moves  outward  as  the  fire expands. Upon arrival, firefighters can provide corresponding temperature data and smoke concentration, locate the nearest safe  rescue  distance  from  the  fire  source,  and  use  infrared sensing equipment to locate the location of the fire source, enabling firefighters to accurately and quickly extinguish the fire during rescue operations

(4) Auxiliary lighting

The  intelligent  automatic  inspection  robot  has  auxiliary lighting function, which can ensure normal operation at night or under low light intensity.

## 5.5. Dynamic design of tunnel inspection robot

The motion module is structurally composed of a power source  and  a  transmission  device.  Its  main  function  is  to provide power for the robot's inspection in the tunnel, while also serving as an executive mechanism for controlling the robot. In this paper, a servo motor is selected as the power source of the robot.

## 5.6. Patrol inspection method

1) Scheduled patrol inspection: patrol according to the set time.

- 2)  Fixed  point  patrol:  The  commonly  used  fixed  point patrol can perform automatic and constant speed patrol based on  the  specified  path  and  the  specified  patrol  target  point. Simply  setting  the  patrol  path  and  starting  the  automatic patrol can enable the robot to automatically complete a patrol.
- 3) Scheduled patrol inspection: Conduct specific inspections  according  to  specific  tasks,  such  as  setting  up robots to perform meter reading tasks, or conducting visual defect detection tasks.

4) Prescribed route inspection: During routine inspections, the inspection route is set in advance. During the inspection process, the robot can automatically and accurately stop and detect  each  patrol  working  position.  After  completing  the specified  actions,  it  can  automatically  advance  to  the  next patrol target point according to the path. No manual control is required.  Complete  the  inspection  operation,  automatically record  and  save  the  collected  data  to  the  management platform, and generate a patrol analysis report on demand.

5) Remote control inspection: real-time remote control of robots through manual  remote control inspection. This application mode is suitable for operation and maintenance personnel  and  management  units  that  need  to  lock  and monitor the status of certain types of equipment, especially when abnormal equipment and environmental conditions are detected  during  autonomous  robot  patrols  and  an  alarm  is given  to the  operation  and  maintenance  personnel,  the operation and maintenance personnel can quickly manipulate the robot to reach the location of abnormal equipment in the first time, view the abnormal equipment in a timely manner, and verify the alarm information, in order to quickly formulate response strategies.

The operation and maintenance personnel have the highest operational  priority  for  the  remote  control  operation  of  the robot. After the system enters the remote control patrol mode, the robot will suspend other tasks that are being executed, and follow manual remote control instructions to achieve functions such as the robot's forward and backward movement at an adjustable speed, the elevator's up and down movement, and the omni-directional rotation of the pan and tilt  table, as well as lens zoom adjustment of the dual view camera. It can ensure that the system reaches the designated location in the first time, obtain status data and visual images of  the  equipment  and  environment,  and  ensure  the  safe operation of the equipment. Autonomous patrol inspection - Operators can flexibly conduct inspections based on the patrol time, cycle, route, target, and type (infrared, visible, partial discharge, etc.)

## 6. Conclusion

Based on Tongzi Tunnel, this paper studies the combined detection  mode  based  on  the  safe  operation  of  ultra-long tunnels,  aiming  at  the  main  safety  issues  in  the  operation process of ultra-long tunnels, based on both tunnel fire and traffic  incidents,  and  develops  a  response  implementation plan; Innovatively transplant mobile detection technology to highway tunnels, use intelligent patrol robots, carry various detection devices and early warning devices based on core detection technology, real-time monitor the tunnel operating environment,  analyze  sensor  detection  data,  predict  tunnel operating conditions in a short time in the future, and achieve safe  operation  of  ultra-long  tunnels.  Based  on  this,  the following conclusions are drawn:

(1) In this paper, video based thermal imaging technology is  used  to  detect  tunnel  fire  accidents,  combining  dual wavelength flame detection and video monitoring methods to achieve open fire and pure smoke detection when a fire occurs in a tunnel. This combined detection method can accurately identify the initial state of the fire and minimize casualties or economic losses caused by the spread of the fire.

(2) The use of traffic incident detection technology based on  lightning  vision  integration  can  effectively  achieve  the monitoring and detection of various types of traffic incidents in tunnels, making up for the shortcomings of high false alarm rates in traditional tunnel traffic incident detection.

(3) Based on this research scheme, using intelligent patrol robots  as  the  carrier  and  carrying  various  types  of  sensing equipment  and  emergency  equipment,  on  the  one  hand,  it compensates for the detection blind spot of fixed monitoring equipment, replaces manual patrol, realizes 24-hour uninterrupted  full  coverage  monitoring  of  tunnel  safety operations,  and  reduces  the  cost  of  manual  patrol;  On  the other hand, equipped with a variety of detection equipment based  on  various  advanced  technologies  to  improve  the accuracy,  timeliness,  and  reliability  of  tunnel  fire,  light environment, and traffic incident detection. At the same time, equipped with emergency equipment, to a certain extent, can replace  manual  timely  handling  of  some  emergencies,  and minimize the losses caused by accidents.

## Acknowledgment

Research and demonstration of key technologies for efficient construction and intelligent operation and maintenance of super long and large span highway tunnels with complex geology + QKH Major Special Document No. [2018] 3011-001

## References

- [1] Du  Zhigang, Yu  Tingyu, Xiang Yiming,  Xu  Wanwan. Research on the optimization of light environment in highway tunnels  based  on  traffic  accident  prevention  [J].  Journal  of Wuhan University of Technology (Traffic Science and Engineering Edition), 2018,42 (5): 715-718.
- [2] Kang Chenglong, Ai Yao. Overview of Research on Highway Traffic  Incident  Detection  [J].  Traffic  Engineering,  2019,  19 (2): 19-22.
- [3] Hu  Yong.  Research  on  Video  Based  Road  Traffic  Incident Detection  Algorithms  [J].  Modern  Information  Technology, 2019,3 (7): 61-63.
- [4] Peng Qizhang. Application of Omnidirectional Tracking Radar in Intelligent Expressway Event Detection [J]. China Transportation Information Technology, 2019, (10): 136-138.
- [5] Baipei, Li Jinping. A Video Based Traffic Accident Detection Method  [J].  Journal  of  Jinan  University  (Natural  Science Edition), 2012,26 (3): 282-286.
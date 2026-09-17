<!-- image -->

Logo

<!-- image -->

Logo

## AUTOMATIC DATA PROCESSING SYSTEM FOR INTEGRATED COST AND SCHEDULE CONTROL OF EXCAVATION WORKS IN NATM TUNNELS

Daegu CHO a , Hunhee CHO a , Daewon KIM b

Received 26 Jan 2012; accepted 07 May 2012

a School of Civil, Environmental and Architectural Engineering, Korea University, Anam-Dong, Sungbuk-Gu, Seoul, S. Korea b Department of PLM Innovation Group, Samsung C&amp;T Corporation Yoksam 2-Dong, Gangnam-Gu, Seoul, S. Korea

Abstract. A  type-based  system  is  widely  used  for  cost  and  schedule  control in  the  NATM  (New  Austrian  Tunnelling Method) tunnel. This study raises several limitations of the type-based system: a broad level of control, a distributed approach to cost and schedule data, ad hoc management, and difficulty in deriving  meaningful data. Integrated cost and schedule control promises a myriad of benefits on both information flow and construction management. Nevertheless, the integrated approach still seems to be a long way from common use in the construction industry because it requires considerable overhead effort to acquire, track, and analyze the integrated data. The objective of this study is to propose a new method to automate the required processes for implementing cost and schedule integration. We propose an operationallevel automatic data processing system for cost and schedule integration. The proposed system consists of a real-time location system for detecting equipment locations, a wireless mesh network for transmitting the location signals to a field office,  and  a  prototype  model  for  transforming  the  signals  to  cost  and  schedule  data.  Technical  feasibility  is  analyzed through a pilot project. The study offers a new approach to facilitating sensor technologies for cost and schedule integration.

Reference to this paper should be made as follows: Cho, D.; Cho, H.; Kim, D. 2013. Automatic data processing system for integrated cost and schedule control of excavation works in NATM tunnels, Journal of Civil Engineering and Management 20(1): 132-141. http://dx.doi.org/10.3846/13923730.2013.801907

Keywords: data integration, NATM, RTLS, wireless mesh network, automation, information technology.

## Introduction

Timely  feedback  on  a  project's  status  enables  project  managers  to  identify  problems  early  and  make  appropriate adjustments that can keep a project on time and within  budget.  Cost  and  schedule  control  have  been  regarded  as  two  major  management  factors  for  successful performance  of  construction  projects.  Because  cost  and

In  the  age  of  limitless  competition,  the  construction  industry has been increasingly challenged to improve work performance. Traditional methods such as organization or process  changes  seem  to  have  reached  their  limits  and their leverage seems to be insignificant. With the incredible  rate  of  advancement  in  information  technology,  IT convergence for the construction industry has been in the spotlight as a new approach to lead the industry from its traditional  labour-intensive  status  to  become  technology or  knowledge  intensive.  While  the  IT  convergence  has been  attractive  to  the  industry,  its  influence  has  been imperceptible compared with other industries. IT convergence  must  not  simply  utilize  some  technology  in  projects,  but  must  optimize  core  technologies  in  the  construction  environment  considering  work  processes,  field characteristics, business strategies, and so on.

schedule control are closely interrelated in terms of sharing data and management process (Jung, Woo 2004), an integrated  approach  also  promises  a  myriad  of  benefits for  information  systems  and  management.  While  extensive research has attempted to provide a systematic method to integrate cost and schedule data, the integrated approach still seems to be a long way off in the construction industry.  Different  levels  of  detail  between  cost  and schedule data structures generate many integrated Control Accounts  (CAs),  which  require  considerable  overhead effort from field managers to acquire, track, and analyze data throughout the integrated data processing. The additional  overhead has generated much resistance to adopting  the  integrated  approach  in  the  industry.  As  a  result, despite much effort, integrated cost and schedule control has  been  considered  as  irritating  work  in  construction fields. While previous effort to integrate cost and schedule  data  have  mostly  focused  on  building  projects  that consist of many elements, operations, and crews, it is not widely  applied  to  a  large  construction  project  such  as  a tunnel, road, or bridge characterized by a relatively small number of information units, horizontally repetitive operations, and construction in open space.

<!-- image -->

Logo

Motivated by these challenges, this  study  hypothesizes  that  an  automatic  data  processing  system  (ADPS) applied to a large construction project should help facilitate  the  integrated  approach  by  reducing  the  number  of CAs and overhead effort in the data processing. The primary objective of this study is to propose a new method to automate the required processes for implementing cost and schedule integration. NATM tunnel projects focusing on excavation works is considered to verify the proposed method.

## 1. Cost and schedule integration

Because cost and schedule information are closely interrelated, it would be ideal for both cost and schedule data to be represented by a single hierarchy and controlled by a single  parameter.  Unfortunately,  the  low-level  items  in  a traditional  bill  of  quantity  (BOQ)  representing  cost  data and the low-level items in a scheduling diagram are in two different  levels  of  an  information  hierarchy  and  there  is considerable mismatch (Perera, Imriyas 2004). The different levels of detail have been regarded as the main difficulty of cost and schedule integration (Hendrickson, Au 1989; Rasdorf,  Abudayyeh  1991;  Jung,  Woo  2004;  Fleming, Koppelman  2005).  Many  researchers  have  attempted  to derive  an  appropriate  integration  model  for  the  industry. Teicholz's CBS to WBS Mapping Model (Teicholz 1987), Hendrickson  and  Au's  Work  Element  Model  (Hendrickson,  Au 1989), Kim's Design Object Model (Kim 1989), and  Rasdorf  and  Abudayyeh's  Work-packaging  Model (Rasdorf, Abudayyeh 1991) are well known. These models have tried to find an integrated control point through distributing  cost  data  into  schedule  data  or  vice  versa  (Cho 2009)  to  remove  mismatches  between  cost  and  schedule data.

As  construction  projects  become  larger  and  more  complex, a great amount of data is generated. Project participants must rapidly understand and leverage these data for efficient project management. Because cost and schedule control  are  the  two  major  functions  determining  a  project's  success  or  failure,  various  document  forms  and software applications are used to acquire, track, and analyze  cost  and  schedule  data.  These  independent  tools might be well customized to represent original data, but there  are  many  redundancies  in  using  different  forms, structures, and perspectives (Rasdorf, Abudayyeh 1991). They  require  considerable  overhead  effort  to  acquire, analyze,  and  manipulate  fundamentally  the  same  data over and over again in the data processing.

An integrated Control Account (CA) is derived from three  information  structures,  Work  Breakdown  Structure (WBS), Cost Breakdown Structure (CBS), and Organization Breakdown Structure (OBS). Thus, the integrated CA is referred to a combination of zone and element from the WBS, corresponding operations from the CBS, and organizations  from  the  OBS  responsible  for  the  operations.  In other words, an integrated CA must encompass all relevant information units such as element, operation, location, and organization to resolve the mismatch. As a result, an integration model requires a large number of CAs, which form a complex data structure. Additional effort to generate CAs

(Deng, Hung 1998) and the overhead costs to control field data (Rasdorf, Abudayyeh 1991; Deng, Hung 1998; Jung, Woo 2004) created resistance to wide adoption of the integrated  approach.  It  is  paradoxical  that  project  managers resist  the  integration  because  of  the  additional  work  required,  while  the  integration  system  was  designed  to  reduce the managers' workload.

Representations  of  cost  and  schedule  control  items and  their  levels  of  detail  vary  according  to  both  project characteristics  including  project  size,  type,  cost,  duration, technical complexity, management level, delivery system, contract type, and management policies (Jung, Woo 2004), and situational characteristics including development stage, delivery method, available resources and constraints, contractual relationship, construction method, developer's experience,  perspective  and  knowledge,  etc.  Considering these  characteristics,  a  single  representative  integration method might not be suitable for all construction projects.

Rasdorf  and  Abudayyeh  (1991)  proposed  an  automatic data acquisition method using bar codes and a relational  database  management  system  to  reduce  the  overhead effort of data acquisition and processing. Jung and Woo (2004)  proposed  a  flexible  WBS  method  to  minimize the number of CAs. On one hand, these approaches improved the practicability of an integration system, but on the other hand, they were still limited to apply to all construction projects.

While  previous  efforts  towards  integration  have usually  focused on building projects, they are rarely applied to large construction projects such as tunnels, roads, railroads, or bridges. These are characterized by relatively small numbers of elements and organizations, horizontally repetitive operations, and construction in open spaces. The  different  characteristics  of  these  large  construction projects might positively impact on the integration method.  In  the  following  sections,  we  propose  a  method  to reduce  the  required  number  of  integrated  CAs  and  the overhead  effort  in  data  processing,  focusing  on  excavation works in NATM tunnel projects.

## 2. Cost and schedule control in an NATM tunnel

The  New  Austrian  Tunnelling  Method  (NATM),  also commonly  referred to as the Sequential Excavation Method  (SEM)  uses  the  inherent  strength  in  the  rock mass to support the roof during excavation. Because this self-supporting  capability  achieves  economy,  flexibility in  uncovered  ground  conditions,  and  dynamic  design variability,  NATM  is  widely  applied  for  underground structures.  NATM  tunnels  are  largely  dependent  upon round  length,  types  of  support,  and  ground  conditions such  as  shear  strength,  deformation,  and  groundwater level.  Excavation  works  accounting  for  more  than  fifty percent  of  the  project  budget  and  consuming  roughly sixty percent of the total project duration are critical management points determining a project's success.

## 2.1. Characteristics of NATM tunnels

Excavation  methods  and  supporting  patterns  are predefined using 'types' in the planning phase.  As ground conditions deteriorate, the type number increases, the  number of  supporting  processes  (such  as  rock  bolts, steel  plates,  and  forepoling)  increases,  and  the  length  of excavation per cycle decreases from 3.5 metres to 1.0 metres.  For  example,  Type-I  is  the  lowest  support type; it is applied in favourable ground conditions, allows full-face  excavation,  and  usually  advances  by  3.5  se  or more per cycle. On the other hand, Type-VI allows only partial  excavation  and  advances  by  1.0 metres  or  less. Type-VI tunnels are excavated in two stages independently.  First,  the  top  half  of  the  tunnel  (or  heading)  is  excavated, and then the bottom half (or bench) is excavated, because  prompt  reinforcements  are  required  to  protect against  unfavourable  ground  conditions.  The  standard types provide a common platform for project participants to  communicate in the field.  A tunnel project  may  have several  drift  patterns  (e.g.  Type-I,  Type-II),  and  more than  six  types  have  been  recommended  to  cope  more flexibly with various ground conditions.

A  standard  type  of  excavation  is  implemented  by cyclic operations such as boring, charging, blasting, mucking,  reinforcing,  and  shotcreting  operations.  Each operation  in  the  repetitive  series  must  usually  be  completed before the subsequent operation can start (Department  of  Transportation  2009).  Twelve-hour  shifts  and two cycles of excavation per day are typical in a portal. Thus,  four  shifts  of  excavation  are  performed  in  a  twoportal tunnel. Because one set of equipment and crews is usually responsible for the four cycles, smooth operational transitions from one portal to the other might be quite important for efficient cost and schedule control.

## 2.2. Type-based cost and schedule control

Table 1 shows a type-based unit costing system that is used in a real tunnel project. These type-based unit costs are derived from the company's own historical database. In the type-based system, cost and schedule control is implemented  by  comparison  between  planned  and  actual  type for a given construction period. For example, Type-VI and Type-V were designated for the first 28 metres of excavation  in  the  plan  in  Figure 1.  However,  only  Type-VI  was actually performed because of unfavourable ground conditions. On  April 4, a project manager  calculates the change's negative impact: the tunnel is 3.2 metres behind schedule and KRW 47 203 200 over budget. Because both cost and schedule control are implemented based on types, it can be regarded as a type-based cost and schedule control system; in short, a type system in the paper.

Fig. 1. An example project management schedule for a tunnel project

<!-- image -->

Engineering drawing

Because of the limitations in investigating precise ground conditions,  excavation  plans  in  the  design  phase  can change  frequently  during  the  project  execution.  Project management  schedules  are  used  widely  to  assess  the change and to compare the current status  with the plan. Figure 1 shows a project management schedule used for underground construction. The big table is divided into a plan  table  and  an  actual  table.  The  plan  table  includes: (1) a station representing the excavation point; (2) a planning  type  denoting  an  excavation  and  support  method; and (3) the total excavation length for the planning type. The actual table includes: (1) an actual start date for the corresponding  station;  (2)  the  implemented  type;  and (3) the total excavation length of the actual type.

Table 1. Type-based unit costs used in Samtan 1 Tunnel

| Standard type   |   Excavation length per cycle (m) |   Unit cost per cycle (wons) |
|-----------------|-----------------------------------|------------------------------|
| TYPE-I          |                               3.5 |                    9,607,500 |
| TYPE-II         |                                 3 |                    8,547,000 |
| TYPE-III        |                                 2 |                    7,342,000 |
| TYPE-IV         |                               1.5 |                    7,726,500 |
| TYPE-V          |                               1.2 |                    8,734,800 |
| TYPE-VI         |                                 1 |                   11,685,000 |
| TYPE-VI-1       |                                 1 |                   11,677,000 |

## 2.3. Limitations of the type-based control system

The  type  system  consists  of  several  cost  items  listed  in BOQ. A cost item can be divided into several operations according  to  equipment  requirements.  Table 2  describes the cost items used in the BOQ and their required operations for the Type-IV top cycle. The type system can be delineated into cost item levels composed of a bundle of operations.

Table 2. Cost items and operations of Type-IV top cycle

| Cost Item in BOQ     | Operation          | Equipment (ea.)                           |   Time (min) |
|----------------------|--------------------|-------------------------------------------|--------------|
| NA1613 Excavation    | Survey & mark      | Charging car (1)                          |           20 |
|                      | Drill              | Drilling jumbo (1)                        |           80 |
|                      | Charge & blast     | Charging car (1)                          |           60 |
|                      | Ventilate          |                                           |           30 |
| NA1920 Muck disposal | Scale              | Backhoe (1) Charging car (1)              |           20 |
| NA1920 Muck disposal | Load & haul        | Backhoe (1) Dump truck (5)                |           90 |
| NA1920 Muck disposal | Clean              | Backhoe (1) Loader(1)                     |           70 |
| NG2111 Steel ribs    | Install steel ribs | Charging car (1)                          |           50 |
| NE1102 Shotcrete     | Cast lining        | Shotcrete machine (1) Ready-mix truck (1) |           80 |
| NE1102 Shotcrete     | Clean              | Loader (1) Dump truck (1)                 |           30 |
| NG1154               | Drill              | Drilling jumbo (1)                        |           20 |
| Rock bolt            | Install rock bolts | Charging car (1)                          |           60 |
| Total                |                    |                                           |          610 |

Three  limitations  of  the  type-based  control  system were identified in our study.  First, the type system does not  allow  project  managers  to  track  individual  performances in particular periods of time. Cost control relies on the level of detail used in the BOQ and schedule control  relies  on  the  productivity  rate  of  an  operation  performed by a crew. Meanwhile, the type system's data are at a too broad level because all operational performances are lumped together. This broad level is rarely appropriate  for  bills  of  quantity  and  detailed  schedule  control. Accordingly,  instead  of  ad  hoc  management  from  the type  system,  a  more  detailed  level  of  control  system  is required for a more systematic project control.

Second,  the  type  system  does  not  support  smooth transitions between operations. As previously mentioned, excavation  works  are  implemented  by  a  series  of  independent  operations,  each  of  which  must  be  completed before  the  next  can  start  (Department  of  Transportation 2009).

- 1) Two  portals :  e.g.  Southbound  and  Northbound Tunnel;

Usually, one set of equipment and crew implements a  two-portal  tunnel.  At  the  operational  level,  a  charging car  is  used  several  times  at  both  tunnel  faces  to  survey and  mark,  charge,  scale,  install  steel  ribs,  and  install rockbolts.  To  complete  two  cycles  within  12  hours,  the one  set  of  equipment  and  crew  must  frequently  move from one portal to the other considering the operational sequence, resources availability, and work space. Because the following factors influence the operational planning, smooth transitions are generally quite complex:

- 2) Eleven types : Type-I, II, III, IV-Top, IV-Bottom, V-Top, V-Bottom, VI-Top, VI-Bottom, VI-1-Top, and VI-1-Bottom;
- 4) Different  quantities according  to  the  applicable type;
- 3) Thirteen operations : surveying and marking, explosive  drilling,  charging  and  blasting,  ventilating, scaling, loading and hauling, muck cleaning, steel  rib  installing,  cast  lining,  floor  cleaning, rockbolt  drilling,  rockbolt  installing,  and  forepoling;
- 5) Inconsistent and ever-changing work conditions : the distance from a tunnel face to a muck pile or a batch plant, access road conditions, equipment efficiency and productivity rate according to excavation  progress,  equipment  failure,  relationships with subcontractors, complaints from neighbouring residents, etc.

Third,  the  type  system  seems  to  be  convenient  to control  a  project,  but  it  requires  considerable  effort  to derive  meaningful  data,  e.g.  feedback  on  a  subcontractor's  performance, productivity rate, equipment efficiency, and effective cycle times of crews. An efficient control  system enables project managers to understand who is going to do what, and how, where, why, and when they are going to do it. Unfortunately, supporting data in the type  system  are  distributed  in  various  documents  and software applications with different forms, structures, and points of view. Although the type system might be quite adequate  to  support  a  broad  level  of  control,  additional effort  is  required  to  manipulate  data  for  deriving  meaningful  feedback  on  project  performance.  Eventually,  the type system triggers inaccuracy, inefficiency, and inconsistency  in  information  flow  and  interrupts  systematic project management.

In the type system, the assembly of operations is unable  to  represent  operational  levels  of  detail,  so  ad  hoc decision-making  relying  on  a  project  manager's  experience, knowledge, and intuition prevails in practice. Thus, a more detailed control system enabling project managers to track current work status should be designed to support the smooth transitions.

So far, we have reviewed several limitations of the current approach to cost and schedule control. Excavation works  are  described  by  several  predefined  supporting types and employ sequential operations at multiple places at  the  same  time.  While  various  field  characteristics should be understood by planners and reflected by constructors in the project execution phase, the type system does not allow project managers to handle the characteristics. These limitations fundamentally originate from the too  broad  level  of  cost  and  schedule  control.  Thus,  an operational-level cost and schedule control system should be considered as a solution to overcome the limitations.

## 3. Information technologies required for integrated cost and schedule control

Based on an analysis of the characteristics of excavation  works,  we  propose  an  automatic  data  processing system (ADPS) that identifies the locations of equipment in tunnels. To accomplish this, the following systems are required:  1) a  real-time  location  system  to  detect  an equipment  location;  2) a  network  system  to  deliver  the location signals from the tunnel face to a field office; and 3) an  information  transformation  system  to  convert  the location signals to cost and schedule data. Based on extensive  reviews  of  currently  available  technologies,  this study  adopts  both  a  real-time  location  system  (RTLS) using a time of arrival (TOA) method to identify the location  of  equipment in tunnels and a Wi-Fi wireless mesh network to deliver signals to a field office.

An NATM tunnel is excavated by repetitive cyclic operations,  as  described  in  Table  2.  Every  operation  is  performed  at  the  tunnel  face  and  by  a  set  of  equipment. Thus, we hypothesize that the operations and their related data can be identified by detecting which equipment is at the tunnel face. For example, a project manager can figure  out  that  a  shotcreting  operation  is  in  progress  if  an information system shows that a shotcrete machine and a ready-mix  concrete  truck  are  located  at  the  tunnel  face. The running time of a piece of equipment can provide the start and end times of the operation: shotcreting.

## 3.1. Real-time location identification system

An active tag system was adopted for tracking locations of equipment in a variety of situations, particularly

Location  identification  technologies  include  the  global positioning system (GPS) using satellites, location-based systems (LBSs) using a mobile base station, and RTLSs using an indoor network (Kim 2011). Because GPS and LBS  are  not  available  inside  tunnels,  an  RTLS  was adopted  in  our  proposed  system  for  identifying  equipment  locations  within  the  tunnel,  while  a  GPS  receiver was used for locations outside the tunnel. RTLS technology is used to monitor the locations of assets, materials, and  people  in  real  time  using  location  tags  and  readers (Sadeghpour 2006). The RTLS transmits real-time location  data  using  readers  from  tags  such  as  passive,  semipassive,  or  active  radio-frequency  identification  (RFID) tags.  The  real-time  location  data  showing  the  routes  of tag movement are transmitted to a network system.

those appropriate to a tunnel's long, linear structure. According to measurement methods, location identification technologies  can  be  divided  by  angle  of  arrival  (AOA), time of arrival (TOA), time difference of arrival (TDOA), and  received  signal  strength  indication  (RSSI).  Among these, TOA was adopted for the proposed system because it allows relatively precise measurement values in a wide range of areas. Figure 2 illustrates a cell-based topology to utilize the TOA algorithm inside a tunnel. The x -  and y -axis  values  representing  the  equipment  location  are calculated by the times of arrival of radio-frequency (RF) signals in a cell composed of four anchor nodes and one mobile node.

Fig. 2. Location identification measurement using TOA algorithm inside tunnel (Kim 2011)

<!-- image -->

Engineering drawing

## 3.2. Wireless mesh network system

Examples  of  network  technologies  include  wireless local  area  networks,  Bluetooth,  ZigBee,  and  Ultra  WideBand. Specifications appropriate to tunnel projects include: a topology appropriate for a long, narrow, linear structure; durability  against  blasting  operations;  transmission  distances as long as possible; low installation cost; and ability to transmit signals in real time. A wireless mesh network (WMN)  was  adopted  as  the  best  solution  to  match  the specifications.  A  WMN is  a  network  system  made  up  of routers, nodes, and gateways organized in a mesh topology connecting all the terminals and relaying signals to users. Advantages of WMNs include an ability to switch routes, allowing  failures  in  nodes,  relatively  low  cost,  and  easy installation. Figure 3 illustrates the overall system architecture of a wireless mesh network installed in a tunnel project.

A  network  system  is  necessary  to  transmit  the  location signals from the RTLS to a field office. Tunnels are usually  remote  from  towns  and  pass  under  mountains,  where installation of all means of communication, including telephone and the Internet, is quite difficult. As a result, communication  problems  are  typical  in  tunnel  projects  and communication is intentionally minimized. However, systematic project control relies greatly on efficient communication  among  project  participants.  A  wireless  network system was adopted to transmit location signals, considering  that  tunnel  projects  include  large,  extensive  construction fields and an unfavourable work environment involving blasting, rockslides, and underground water.

Fig. 3. Wireless mesh network system installed in a tunnel project

<!-- image -->

Flow chart

## 4. Methods to control cost and schedule data from real-time location of equipment

To overcome limitations of the type system, an operationbased  information  system  was  designed  to  measure  cost and  schedule  data.  Figure 4  illustrates  an  example  of  an operational-level schedule, presenting one cycle of excavation works for a two-portal tunnel. The schedule shows that

## 4.1. Operation-based information unit

Type-I for the southbound tunnel and Type-IV-Top for the northbound tunnel were implemented as of 30 April 2010.

Table 3  describes  the  unit  costs  of  one  cycle  of Type-IV-Top. This unit cost is based on the cyclic quantities of  Type-IV-Top and it can be utilized to account for cost  data  in  the  project  budget.  For  example,  when  the 'shotcrete  clean'  operation  is  completed  (Table 2),  the one-cycle  unit  cost  (NE1102;  KRW  1  492.963)  of  the shotcrete  operation  is  added  to  the  project  budget.  The one-cycle  unit  cost  makes  cost  control  possible  at  the operational  level,  because  the  respective  types  are  performed by identical cyclic operations.

Fig. 4. An example of an operation-level schedule for concurrent Type-I and Type-IV-top operations

<!-- image -->

Bar chart

The dotted line in Figure 4 indicates that the load and haul operation in the southbound tunnel and the survey and mark operation in the northbound tunnel were in progress at noon. Based on the southbound tunnel schedule, project managers  coordinate  the  northbound  tunnel  schedule  to eliminate  a  bottleneck  in  operations.  Thus,  the  operationbased schedule not only allows project managers to avoid operational conflicts, but also shows the actual  feasibility of daily scheduling. A smoother transition might be possible depending on how the project manager plans the operational  sequences  and  utilizes  float  time  (for  example,  the prepare  operation  in  Fig. 4).  In  addition,  the  operationbased control system shows the productivity of an operation and the efficiency of equipment usage, the fundamental data of short-term project planning.

Table 3. One-cycle unit cost of Type-IV-Top

| Code    | Operation             | Unit   | Cycle    | Unit cost (Won)   | Unit cost (Won)   | Unit cost (Won)   |   Total cost (wons) |
|---------|-----------------------|--------|----------|-------------------|-------------------|-------------------|---------------------|
|         |                       |        | quantity | Materials         | Labour            | Equip.            |                     |
| NA1613  | Excavation            | m 3    | 99.47    | 5,747             | 878               | 6,239             |           1,279,582 |
| NA1920  | Muck disposal         | m 3    | 105.94   | 1,328             | 649               | 1,051             |             320,786 |
| NX1304  | Labour                | Times  | 1.00     |                   | 1,027,557         |                   |           1,027,557 |
| NG1154  | Rock bolt (L = 4.0 m) | ea.    | 9.50     | 21,396            | 129               | 29,700            |             486,638 |
| NG2111  | Steel rib (50*20*30)  | NR     | 2.33     | 393,580           | 369,186           | 20,739            |           1,825,567 |
| NE 1102 | Shotcrete             | m 3    | 7.87     | 133,703           | 17,404            | 38,596            |           1,492,963 |

## 4.2. Conditions for cost and schedule integration

On the other hand, an integrated CA for excavation works requires a single linear space represented as a station, no specific element, and several cost items consisting of a bundle of operations. A small number of CAs an integrated approach might be easily accomplished. Existence  of  eleven  types  and  on  average  twelve  operations means that  the  integrated  approach  to  excavation  works would require 132 CAs, which must be a relatively small number compared with a building project.

Integrated cost and schedule control can be defined as an effort  to  combine  both  kinds  of  information  in  a  single controllable  account.  As  previously  mentioned,  an  integrated cost and schedule control system requires a great number  of  integrated  CAs,  including  spatial,  elemental, operational, and organizational information units. A single  integrated  item  for  a  building  project  frequently  includes  physical  and  functional  properties  and  sometime requires structural, architectural, and electrical properties with various levels of detail. A building project typically generates  more  than  several  thousand  integrated  CAs. Deng and Hung (1998) mentioned that a large number of CAs requires  an  increase  in  the  labour  force  and  heavy overhead costs.  Consequently, the large number of control items and a complex data structure are the main obstacles to wide adoption of the integrated approach. Although  the  integrated  approach  provides  easy  access  to cost and schedule control for project managers, considerable  effort  may  still  be  required  to  acquire,  track,  and analyze operational data

In  addition,  the  integration  supports  smooth  transitions  and  meaningful  analysis  during  project  execution because an integrated CA is based on the operation level. In summary, the characteristics of tunnel excavations make operational-level cost and schedule integration to be possible with a relatively small number of integrated CAs.

However, despite a small number of CAs, data acquisition, transaction, and analysis in the fields might be far from realistic,  when  considering the large construction  field,  unfavourable  access,  long  distances  from  a  field  office  to jobsites, and limited administrative staff. In this respect, we propose an Automatic Data Processing System (ADPS).

## 4.3. Algorithms to convert location signals to operational-level cost and schedule data

In Section 3, we described a real-time location identification  system to track equipment near a tunnel face and a wireless  mesh network to transmit location signals from the tunnel to a field office. The location signals of equipment are converted into operational-level cost and schedule  data  in  the  proposed  system.  The  following  algorithms are part of the proposed model:

- 2) Respective  operations  are  implemented  by  a specific set of equipment at the tunnel face;
- 1) A series of repetitive operations, each of which must  be  completed  before  the  subsequent  operation can start;
- 3) The running time of an item of equipment can provide the start and end time of an operation;
- 5) A type cost  can  be  represented  by  the  sum  of one cycle of unit costs.
- 4) A cost item used in BOQ can be represented by a bundle of operations;

Figure 5 illustrates a prototype model for the ADPS that we are proposing. The RTLS detects the locations of a shotcrete machine and ready-mix concrete truck at the southbound  tunnel  face  (Station  818  m)  and  the  WMN transmits  the  signals  from  the  RTLS  to  the  field  office. The prototype model automatically realizes that the castlining operation is now in progress and the installing steel rib  operation  has  just  been  completed  from  the  signals that show a charging car is moving back (Fig. 5-A). Then, the one-cycle unit cost of the installing steel rib operation (KRW 1 825 567) described in Table 3 is included in the BOQ in the prototype model (Fig. 5-B). Next, the accumulated unit costs comprise the Type-IV-Top cycle cost (Fig. 5-C) and finally, the type-based cost is included in the project budget (Fig. 5-D). The proposed system thus enables  project  managers  to  access  four  levels  of  detail including the operation, bills  of  quantity,  type,  and  project  budget  level;  to  accomplish  integrated  cost  and schedule control; and to automate all required processes including data acquisition, tracking, and analysis.

## 5. Pilot project

The  practicability  of  the  proposed  ADPS  for  integrated cost and schedule control was tested using a pilot project. The Samtan 1 tunnel is the longest tunnel (2 645 metres in the Samchuk direction and 2 619 metres in the Jeachen direction)  in  the  Samchuk-Jeachen  road  construction  in South Korea.  The NATM tunnelling method and seven standard types were employed in the project. Total duration was 48 months for the two-portal tunnels with twolane roads. Figure 6 illustrates the prototypical longitudinal profile of the Samchuk-Jeachen road construction and shows overall project deliverables of the pilot project.

Fig. 5. A prototype model of the ADPS for integrated cost and schedule control

<!-- image -->

Full page image

Fig. 6. Prototypical longitudinal profile of Samchuk-Jeachen Road construction

<!-- image -->

Geographical map

## 5.1. System application to tunnel fields

Figure 7  illustrates  the  overall  system  application  in  the pilot  project.  The  RTLS  consisted  of  location  anchors (Fig. 7-B)  installed  inside  the  tunnel  and  a  location  tag installed in a sport utility vehicle (Fig. 7-C). Six anchors were installed at 9  metre  width and 30 metre, 50 metre, and 70 metre lengths respectively, as shown in Figure 7, to  minimize  location  errors  according  to  longitudinal changes. The vehicle substituting for construction equipment moved within the rectangular fixed areas (section) and  its  movement  was  measured  by  a  total  station  to check  for  errors  in  the  RTLS.  Anchor  nodes  were  designed  to  transmit  real-time  location  data  30  times  per minute. Figures 7-E and 7-F illustrate the WMN installed inside and outside the tunnel at 100 metre intervals. Table 4 describes system specifications applied in the pilot project.

Fig. 7. Overall system application to the pilot project

<!-- image -->

Photograph

Table 4. System specifications applied in the pilot project

| Applied System       | RTLS                                                               | Location Anchor                                 | GPS                                                         | WMN                                                                                     |
|----------------------|--------------------------------------------------------------------|-------------------------------------------------|-------------------------------------------------------------|-----------------------------------------------------------------------------------------|
| Model                | GNC-TAG-V1                                                         | GNC-An-V1                                       | UIGGUB02-ROO1                                               | RouterStation Pro                                                                       |
| Major Specifications | 2.45 GHz RF Wireless LAN Embedded Linux Cortex A8 (1 GHz) Main CPU | 2.45 GHz RF (ISM Band) Atmega 128L RS-232C JTAG | -160 dBM Sensitivity -160 dBM Tracking System NMEA Protocol | SuperRange 2 Network Inter- face Card AR7100 Network Processing Unit 100-500 m Coverage |

## 5.2. Test results

Several rounds of testing are summarized in the following material. First, signals from the anchors in every section were  detected  to  identify  equipment  locations  precisely, and their errors were minimum 45 centimetres, maximum 315 centimetres, and average 150 centimetres when compared with measurements by a total station. The range of errors  must  be  low  enough  to  identify  equipment  locations in the tunnel and to regard a set of equipment at the tunnel face as an operation. Second, the range of errors is slightly impacted by longitudinal changes. A later test in a  section  of  more  than  100 metres  and  a  test  using  an extended Kalman filter to reduce errors were considered to improve technical and economic feasibility.

Fig. 8. Vehicle movements in the 70 metre section

<!-- image -->

Line chart

Figure 8 shows the pilot test results in the 70 metre section. The dotted line indicates the planned movements and the staggered line shows the actual movements of the vehicle location tag in the narrow-width tunnel and at the unfavourable ground conditions.

## Conclusions

The purpose of cost and schedule control can be defined as  the  optimization  of  the  resources  required  by  tunnel projects:  large  amounts  of  material,  labour,  and  equipment  for  long  periods.  Thus,  cost  and  schedule  control must be realistic and must reflect all the restrictions that are imposed on the project (Department of Transportation 2009). Based on the analysis of characteristics of NATM tunnel excavation works, this study raises several limitations of the type system: the level of control is too broad; cost and schedule data are too distributed; management is ad hoc; and it is difficult to derive a meaningful database. The type system relies on a project manager's experience, knowledge, and intuition, rather than quantitative analysis of field data. This study emphasizes the necessity of operational-level cost and schedule integration and control. While an integrated approach might contribute greatly to the  overall  enhancement  of  project  management  (Jung, Gibson 1999), it requires considerable overhead effort to acquire, track, and analyze data in the project execution phase.  Based  on  the  motivation  that  the  overhead  effort has  been  the  main  cause  of  resistance  to  adopting  the integrated approach, we have proposed an ADPS for cost and schedule integration.

Effect of IT convergence using sensor technologies has been limited in the construction industry. This study introduces novel uses of sensor technologies to facilitate cost  and  schedule  control.  The  proposed  system  can  reduce  the  considerable  overhead  effort  of  implementing cost  and  schedule  integration  through  automating  data processes and reducing the required number of integrated CAs. The integrated approach using sensor technologies thus  offers  project  managers  easy  access  to  operationallevel cost and schedule control, smooth transitions, productivity  analysis,  and  improved  equipment  efficiency.  In  addition,  the  operational-level  database  allows efficient  construction  planning  and  management  considering field characteristics. Technical and economic feasibility studies to install RTLSs and WMNs in construction sites,  extension  of  the  application  range  to  whole  tunnel projects, and quantitative measurements of advantages of the  proposed  system  remain  future  study  areas.  We  expect  that  the  algorithms  proposed  by  the  study  will  become a capstone to an approach to more systematic construction management.

The  proposed  system  is  composed  of  an  RTLS,  a WMN,  and  a  prototype  model  for  integrated  cost  and schedule control. The RTLS has location tags installed in construction  equipment and location anchors calculating the  relative  position  of  a  tag  within  a  section.  From  the signals  transmitted  by  the  WMN,  the  prototype  model identifies equipment locations in tunnels and converts the location  signals  into  integrated  cost  and  schedule  data through the inherent algorithms. Based on the operational level of an integrated Control Account (CA) having cost and schedule values, the prototype model provides various levels of integrated control, i.e. operation, BOQ, type, and project budget level.

## Acknowledgement

## References

This study is part of a research project sponsored by the Korea Institute of Construction and Transportation Technology  Evaluation  and  Planning  (KICTEP)  under  the Grant No. 09CCTI-B052843-01. The support is gratefully acknowledged.

Cho,  D.  G.  2009. Construction  Information  Database  Framework  (CIDF)  for  integrated  cost,  schedule,  and  performance  control :  PhD  Thesis.  University  of  WisconsinMadison, United States.

Department  of  Transportation  (DOT)  2009. Technical  manual for  design  and  construction  of  road  tunnels  -  civil  elements . Report No. FHWA-NHI-10-034. Washington, DC: National Highway Institute, U.S.

Deng, M. Z. M.; Hung, Y. E. 1998. Integrated cost and schedule control:  Hong  Kong  perspective, Project  Management Journal 29(4): 43-49.

Fleming, Q. W.; Koppelman, J. M. 2005. Earned value project management . 3 rd ed. Project Management Institute, P.A.

Jung, Y.; Gibson, G. E. J. 1999. Planning for computer integrated construction, Journal of Computing in Civil Engineering 13(4): 217-225. http://dx.doi.org/10.1061/(ASCE)08873801(1999)13:4(217)

Hendrickson,  C.;  Au,  T.  1989. Project  management  for  construction:  fundamental  concepts  for  owners,  engineers, architects,  and  builders .  Englewood  Cliffs,  NJ:  Prentice Hall.

Jung, Y.; Woo, S. 2004. Flexible work breakdown structure for integrated cost and schedule control, Journal of Construction  Engineering  and  Management 130(5): 616-625. http://dx.doi.org/10.1061/(ASCE)07339364(2004)130:5(616)

Kim, J. J. 1989. An object-oriented database management system  approach  to  improve  construction  project  planning and  control .  PhD  Thesis.  University  of  Illinois,  United States.

Kim, D. W. 2011. Safety management system for a large construction  project  using  real-time  location  system .  PhD Thesis. Korea University, South Korea.

Perera, A.; Imriyas, K. 2004. An integrated construction project cost  information  system  using  MS TM Access  and  MS TM Project, Journal of Construction Management and Economics 22(2): 203-211. http://dx.doi.org/10.1080/0144619042000201402

Sadeghpour, F. 2006. Real time location system for construction site  management, in Proc. of Joint International Conference  on  Computing  and  Decision  Making  in  Civil  and Building Engineering , Montreal, 14-16 June, 2006, 37363741.

Rasdorf,  W.  J.;  Abudayyeh,  O.  Y.  1991.  Cost-  and  schedulecontrol integration: issues and needs, Journal of Construction  Engineering  and  Management 117(3): 486-502. http://dx.doi.org/10.1061/(ASCE)07339364(1991)117:3(486)

Teicholz, P. M. 1987. Current needs for cost control systems, in Ibbs, C. W.; Ashley, D. B. (Eds.). Project controls: needs and solutions, Proc. Specialty Conference , ASCE, 47-57.

Daegu CHO. Research Professor at School of Civil, Environmental, and Architectural Engineering, Korea University, South Korea. He holds a PhD from the University of Wisconsin-Madison, USA. His research has centered around four areas:  construction  management,  information  technology,  database  management,  and  Building  Information  Modelling (BIM). With respect to BIM, he is developing an integrated cost and schedule system appropriate to the intelligent objectoriented modelling.

Daewon KIM. Senior engineer at Samsung Construction and Technology, South Korea. Dr. Kim has extensive research experience, specifically in a location identification system such as GPS, LBS, and RTLS. His main research interests include a safety management system using information and cutting-edge sensor technology.

Hunhee CHO. Associate Professor at School of Civil, Environmental, and Architectural Engineering, Korea University, South Korea. Dr. Cho is working on multiple research projects in South Korea: a conceptual cost estimating system for buildings, an optimal temporary hoist planning system in high-rise building construction, a synchronous hydraulic jack-up system, and more. Fields of research interests include construction automation and robotics, high-rise building construction, and cost control system.
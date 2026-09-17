<!-- image -->

Logo

<!-- image -->

Logo

## COUPLING MODELS OF ROAD TUNNEL TRAFFIC, VENTILATION AND EVACUATION

Blaž LUIN * , Stojan PETELIN

Faculty of Maritime Studies and Transport, University of Ljubljana, Slovenia

Received 2 October 2018; revised 31 July 2019; accepted 6 November 2019; first published online 20 February 2020

Abstract. As road tunnel accidents can result in numerous fatalities and injuries, attention must be paid to accident prevention and management. To address this issue, use of integrated tunnel model for system evaluation and training of road tunnel operators on computer simulator is presented. A unified tunnel model, including traffic, meteorological conditions, ventilation and evacuation that is presented. An overview of simulation models, simulator architecture and challenges during the development are discussed. The integrated tunnel model is used as a core of a simulation system that is capable of reproducing tunnel accidents in real time and it interfaces with Supervisory Control And Data Acquisition (SCADA) interfaces used in real tunnel control centres. It enables operators to acquire experience they could otherwise get only during major accidents or costly exercises. It also provides the possibility for evaluation of tunnel control algorithms and Human Machine Interfaces (HMIs) for efficient operation of all safety systems during upgrades and maintenance. Finally, application of the model for accident analysis and optimization of emergency ventilation control is presented where it was used to identify cause of emergency ventilation malfunction and design fault.

Keywords: road  tunnel,  simulation,  safety,  ventilation,  traffic,  tunnel  fire,  emergency,  visualization,  operator  training, incident management.

## Introduction

Although there are plenty of efforts to increase the level of  safety,  the  tunnels  remain  areas  of  increased  risk  as they are semi-enclosed spaces where explosions, fires and smoke can have more devastating effects than in the open spaces. There is a great deal of focus on tunnel safety after catastrophic road tunnel accidents that have occurred in the past, such as the Mont Blanc, Tauern and Gotthard tunnel fires whose causes were widely analysed and described (Voeltzel, Dix 2004). The Mont Blanc fire in 1999 resulted in 39 fatalities, the Tauern tunnel fire in the same year resulted in 12 fatalities and 42 injured and 60 vehicles collided during the accident. As a result, the EU issued a Directive 2004/54/EC on tunnel safety to prescribe minimum safety requirements for road tunnels that requires mandatory  risk  assessment  for  all  road  tunnels  on  the trans-European road network that are longer than 500 m (EC 2004). A reminder that tunnel safety remains an interesting topic is the Yanhou tunnel fire (China) that occurred in 2014 and resulted in 40 fatalities.

As  prescribed  by  the  directive,  several  risk  assessment  methodologies  evolved.  The  most  widely  used  is the World Road Association (PIARC) and Organisation for  Economic  Co-operation  and  Development (OECD) Quantitative  Risk  Assessment  Model  (QRAM)  (Cassini et al. 2003; Cassini 1998). It assumes many different scenarios of dangerous and non-dangerous goods accidents. When evaluation of risk minimization measures that were not included in the methodology were needed, extensions to the methodology were developed (Petelin et al. 2010). Results from tunnel risk analyses are key data for implementation of risk mitigation measures, which may be also be chosen by consulting expert opinions and multi-criteria analyses (Hashemkhani Zolfani et al. 2013). The results obtained with the above-mentioned methodologies often pointed out importance of prompt accident detection and response in order to minimize consequences. The tunnel operator response in case of emergency is crucial as it is the first who should take actions including informing and

*Corresponding author. E-mail: blaz.luin@fpp.uni-lj.si

coordinating other emergency services. For this reason, risk for tunnel users can vary greatly due to the great variability  of  tunnel  operator  responses and response times (Gandit et al. 2009).

Experience from past accidents showed that the road tunnel operators were often not sufficiently prepared because they never experienced a major emergency event. While minor incidents occur daily, major tunnel accidents such as fires and explosions occur rarely. Some operators might experience such an event once in a career, some never; therefore, lacking sufficient experience they could not handle situation in an optimum way.

To sum up, interactions between traffic and ventilation  control  and  communication  between  tunnel  users and emergency services can be complex and demanding to  understand.  Improper interaction can increase damage and the number of fatalities (Carvel et  al. 2009). For example, if air velocity is too high, more oxygen might help a fire  spread  faster  or  in  the  wrong  direction  -  air might push smoke into tunnel users and emergency services. One way to approach complexity of tunnel control is through proposed automated decision-making system (Alvear et al. 2013).

The problem of efficient tunnel control could also be approached in a similar way as in the aerospace, chemical and nuclear industries - by training on computer simulators. These industries have a long history of standardized equipment testing prior to the commissioning and personnel  training  according  to  the  standards  IEC  TS 62603-1:2014 and IEC 62381:2012. In the standard IEC TS  62603-1:2014,  Factory  Acceptance  Tests  (FAT)  and Site  Acceptance Tests (SAT) it is specified what evaluations must be carried out on Human-Machine Interfaces (HMIs), controllers, terminations, fields and process definitions; provisions for life cycle support, including personnel training are specified, also, a demo unit of a system at the site is suggested.

The aim of this  work  is  to  develop  a  unified  model of a road tunnel traffic, ventilation and evacuation. It can serve as a core of a computer-based simulator, which includes traffic, ventilation and evacuation sub-models that are computed in real time, representing a demo unit for a road tunnel. It could not only be applied for operator training, but also for evaluation of different accident scenarios during the tunnel design and risk analyses. Therefore, an overview of state-of-the-art models that were considered to be incorporated into the simulator will follow in the next sections.

## 1. Approaches to tunnel traffic, ventilation and evacuation modelling

## 1.1. Road traffic microsimulation

Microscopic  models  are  detailed  models  that  simulate individual  vehicles.  Since  the  simulator  requires  implementation  of  visualization,  a  lower  level  of  detail  than microscopic is not sufficient. The microscopic models are comprised of vehicle following and lane-changing models, except in some rare cases where 2D simulation is assumed. Among the most popular are the Fritzsche (1994), Wiedemann (1974) and IDM (Intelligent Driver Model) - Kesting et al. (2007, 2010), Treiber (2013), Gipps (1981) models. It is common among them that speed, acceleration and longitudinal position are continuous variables and lateral position (lane) is a discrete variable. The Fritzsche (1994) and Wiedemann (1974) approaches to modelling represent real driver actions more realistically as they take into consideration physiological limitation of human drivers, especially in terms of ability to sense and react to changes in speed.

Most  of  the  traffic  microsimulation  software  uses  a particular vehicle following model that cannot be changed or  mixed  with  different  models;  for  example,  VISSIM ( http: // vision-traffic.ptvgroup.com )  uses  the  Wiedemann  model,  paramics  uses  Fritzsche  and  AIMSUN ( http: // www.aimsun.com ) uses a modification of the Gipps model (Wiedemann 1974; Fritzsche 1994; Gipps 1981). For  research  purposes  Simulation  of  Urban  MObility (SUMO) tool is  becoming  increasingly  popular  as  it  is open source and allows modifications to be made to any part  of  the  code  (Krajzewicz et  al. 2012). Even without modifications of the code, it provides many configuration options not usually found in other packages such as choice of a vehicle following, lane changing and emissions models and mixing of them in the same simulation scenario.

It  is  common  among all these models that lane is a discrete variable and longitudinal position is a continuous variable. This causes some difficulties during visualization where smooth movements are required for realistic representation. Similar issues are found when using such models in driving simulators, which often use 3D virtual reality interfacing in order to provide realistic visualization for evaluation of driver responses (Wan et al. 2018). Real-time and faster computation is easily achieved using the traffic microsimulation models, where the road network is a single road tunnel with surrounding road sections.

## 1.2. Tunnel ventilation models

There  are  three  basic  approaches  to  simulating  tunnel ventilation: 1D, zone and Computational Fluid Dynamics (CFD) models. 1D models are comprised of continuity, momentum and energy conservation equations. Simplified versions assume stationary conditions and use variations  of  the  Bernoulli  equation  for  flow  estimation.  A notable model of this kind is the IDA Tunnel Ventilation Model (Sahlin 1996; Sahlin, Grozman 2003). Zonal models  assume  zones  of  constant  temperature  and  gas  concentrations. Examples of those models are Consolidated model of Fire growth And Smoke Transport (CFAST) and Pressurized  zOnal  Model  with  Air-diffuser  (POMA)  - (Haghighat et  al. 2001;  Peacock et  al. 2013).  The  zonal models are semi-2D models that consider simplified species transfer equations between the zones. Such approach would appear complicated in case of constantly changing boundary conditions due to moving vehicles.

Since road tunnels are comprised of a large area, detailed simulation would be computationally demanding. Therefore, by sacrificing a certain degree of detail, simplified models such as multi-zone emerged (Suzuki et al. 2003). An advantage of the simplified models is that they take into consideration effects that are specific to the tunnels such as the piston effect that is caused by the vehicles pushing air in the driving direction. The 3D CFD simulations of vehicle fires in bidirectional tunnels yield significant impact of moving vehicles on fire dynamics (Caliendo et al. 2012a, 2012b). The increases of temperature around the fire was observed in the range of 12…29%. Apart from the  air  flow,  tunnel  wall  temperature  has  a  major  effect on air temperature inside the tunnel and wall temperature conduction and radiation models are part of the 1D and multi-layer zone models as well.

There have also been attempts to simulate fires with virtual  reality  techniques,  that  were  not  specifically  targeted at road tunnels and the focus was not on real-time simulations (Xu et al. 2014). Instead, physical simulation of  the  fire  and  air  movement  was  done  in  advance  and the results were used for realistic visualization. The same approach was also applied to the road tunnels, where fire scenarios were simulated in advance with the Fire Dynamics Simulator (FDS) and visualized using the 3D computer graphics (Cha et  al. 2012). Such approach works on scenarios simulated and solved in advance, but does not show immediate impact of operator actions on the situation inside the tunnel.

The  tunnel  simulation  models  serve  as  a  basis  for design  and  evaluation  of  tunnel  ventilation  algorithms, which can be a demanding task even in the case of simple longitudinally ventilated tunnels when appropriate pressure difference at the tunnel cross passages must be maintained. Too low pressure difference will cause smoke to enter the evacuation tube and too high pressure difference will require application of excessive force to open the cross passage door (Luin et al. 2011).

## 1.3. Evacuation models

Evacuation models can be divided into continuity, Cell Automata (CA) and multi-agent models. The continuity models are based on flow equations. CA models assume a mesh of cells that represents possible discrete positions of humans. Cell sizes are usually the size of a standing man and step sizes can be a cell or two, depending on walking speed. Multi agent models usually assume continuous position variables and each evacuating person is moving by the predefined rules or even artificial intelligence (Shi et al. 2009). Agents can have memory to remember and learn from past evacuation attempts.

Several applications of tunnel evacuations modelling have been carried out (Caliendo et  al. 2012a, 2012b; Capote et  al. 2013). The most obvious problem for tunnel evacuation scenarios is that accident position and vehicle distribution is always different in each event. Therefore, initial conditions should be obtained from the traffic and ventilation models. The simulations were carried out using different cell evacuation models with 0.5 m wide square cells and the results were consistent among all the models. Therefore, if  evacuation model is sufficiently tuned, the results should be realistic given the initial conditions are appropriately defined.

An advantage of cell models is also that they are computationally undemanding and are suitable for simulations much faster than real-time, which means many simulation runs can be evaluated for risk assessment and optimization purposes.

## 2. Integrated tunnel model

In real tunnels communication system consist of a physical layer and networking protocols that are used to connect controllers and cameras. In modern tunnels equipment  is  usually  controlled  through  a  ring  fibre  optic ethernet  connection  to  ensure  redundancy.  The  data  is fed to the server-side application; in our example, a data forwarder or a central controller stores states of the entire tunnel equipment by communicating with tunnel equipment Programmable Logic Controllers (PLCs) and supplies the data to subscribers such as Supervisory Control And Data Acquisition  (SCADA) user interface,  remote monitoring systems, data log recorders, etc. The tunnel PLCs are used to control all the tunnel equipment, such as ventilation fans, lighting, traffic signalization (Variable Message Signs - VMS, traffic lights) and environmental sensors (visibility, air quality). It also stores data history in the Structured Query Language (SQL) database that can be  used  for  analysis  of  equipment  malfunction  or  incidents. In Figure 1, an overview of the system is shown.

In the simulator, the tunnel is replaced by a computer model that behaves as a virtual tunnel, capable of simulating physical phenomena, sensors and PLCs. The components are also connected using Ethernet connection and TCP/IP protocol. As opposed to the real tunnels, where sensors are connected directly to controllers that interface them to a data forwarder through TCP/IP protocol, in the simulator a communication module replaces the PLCs and communicates with the data forwarder application (Figure 2).

Key simulator components are the user interface, the communications system and the simulator core. The overview of the architecture is shown in Figure 2. The HMI is  comprised of operator and instructor user interfaces. Operator user interface is an exact replication of a control room workplace with all the screens that are used by the operators: video surveillance system, SCADA display, video detection interface, dangerous goods vehicle detection system, etc. The SCADA system did not need any modifications, as opposed to the video detection and surveillance systems that had to be replaced by simulated modules. The video processors are not needed in the simulator since the data can be obtained directly from the simulation core.

Figure 1. Tunnel control system

<!-- image -->

Flow chart

Figure 2. Simulator architecture

<!-- image -->

Flow chart

## 2.1. Simulator core models

The simulator core is the most vital part of simulator. It is  comprised  of  physical  and  other  phenomena  models that occur in a tunnel during simulated training sessions. These  include  models  of  all  tunnel  equipment.  Among phenomena that are simulated by the simulator core are traffic, ventilation and meteorological conditions models and an evacuation model.

The  core  models  have  been  implemented  in  C++ programming  language  for  performance  reasons,  but simulation  state  exports  may  be  exported  in  MATLAB ( https: // www.mathworks.com ),  SQL  database  or  comma separated value file format. Core models are implemented in different parallel threads that require synchronization of the data.

Data flow of boundary conditions can be seen in the Figure 3. Interconnected models mean that the state of one model is the boundary condition of the other one and vice versa. For example, the ventilation model includes the fire model, which may limit visibility and driveability conditions. On the other hand, moving vehicles in the traffic  model push air in the driving direction, causing the piston effect and influence longitudinal air flows through the tunnel.

Figure 3. Data flow between the models

<!-- image -->

Flow chart

Figure 4. Coordinate system mapping between different simulator components

<!-- image -->

Engineering drawing

In  Figure  4,  mappings  between  different  coordinate systems in each of the models are illustrated. The ventilation model is represented as a topology of pipes inside, which simulation is carried out in 1D, the traffic model is represented as a road network topology, but for visualization purposes vehicle positions are assigned between as a set of 3D arrays of points for each lane. The evacuation model is a 2D mesh of cells. Therefore 3 transformations had to be defined:

- A - between traffic and ventilation model;
- B - between ventilation and evacuation model;
- C - between evacuation and traffic model.

Different coordinate systems of the models also include differently split sections. For example, single traffic section may be divided into two different ventilation sections as it is shown in the Figure 4. This is the consequence of different tunnel cross-sections. For example, a three-lane traffic section may be in circular and perpendicular tunnel tube or even a section with a cross-passage.

## 2.2. Ventilation model

Due to real-time processing requirements, the ventilation model that was used is a 1D ventilation model similar to that described in research by Petelin et al. (2010), except that it was generalized to support multiple branches that represent multi-tube tunnels and cross passages. The road tunnel chosen in the model contains underground road junctions, therefore it was represented as pipe branches and junctions shown in Figure 5.

Figure 5. Ventilation model sections

<!-- image -->

Engineering drawing

The pressures p 1 to p 4 at the junctions 1 to 4 and air velocities v 1 , v 3 and v 4 in branches 1, 3 and 4 are connected using the equations:

<!-- formula-not-decoded -->

where: piston p ∆ is  piston  effect  caused  by  the  vehicles; fans p ∆ is pressure increase due to fans; meteo p ∆ is impact of meteorological conditions; fric p ∆ is friction on the tunnel walls.

When air velocities are calculated from the pressure equations, the species movement (combustion products, exhaust gases, smoke) are calculated using cells of a 1D grid.  The  pressure  drops piston p ∆ , fans p ∆ , meteo p ∆ and fric p ∆ are  all  functions  of  longitudinal  air  velocities v i . Species concentration in i -th cell changes in a single time step dt according to:

<!-- formula-not-decoded -->

where: c i , r i , Vi are  mass  specific  species  concentration, density  and  volume  of i -th  cell; c in , r in , Vin represent concentration, density and volume of inflow from neighbouring cells; Vout is  volume  represents  flow  out  of  the i -th cell.

The time-step during the simulation was limited by:

<!-- formula-not-decoded -->

where: l is section length; v i is air velocity in i -th section.

The 1D model has the shortcoming of not being able to simulate vertical smoke movement, therefore a simplified approach was used in order to mimic smoke stratification behaviour, which is important for the tunnel operators to understand. It was achieved by simulating smoke vertical movement depending on the longitudinal air velocity.

## 2.3. Traffic simulation model integration

Since vehicle following and lane changing models are generally known and are well studied, this section will deal only with problems related to implementation of simulation in the integrated model of a tunnel related to 3D visualization. Most vehicle following models assume space is a continuous variable and it can therefore be visualized smoothly and continuously if at least 20 iterations/s are calculated to achieve smooth perception of the visualization.

To  the  contrary,  a  majority  of  lane  change  models consider lane a discrete variable that either changes instantly or the vehicle remains in a transition state for a certain period of time. In either case, visualization is not smooth if standard models like Fritzsche or MOBIL are used unless intermediate position interpolation is carried out (Fritzsche 1994; Kesting et  al. 2007). Another solution for smooth visualization would be development of a true 2D traffic model, but that would make sense only if drivers often ignore lane markings in the simulated area. In Figure 6 continuous and discrete lane change is shown.

Discrete lane changes are convenient for traffic flow analysis as they are not computationally demanding. On the other hand, they don't provide all the necessary information that is needed for smooth visualization.

The model had to provide 3D visualization, which required interpolation from 1D to 3D space regardless of which type of lane change model was used. This implies the  use  of  a  discrete  model  that  is  less  computationally demanding and very common for simulation of drivervehicle agents.

As can be seen in Figure 7:

<!-- formula-not-decoded -->

represents lane centres, where i is  lane number (starting with 0 on the right) and j is a subsequent point; points at the same index j are  linear and they lie on a line that is perpendicular to the longitudinal road axis; the array of points:

<!-- formula-not-decoded -->

defines road edges starting with the rightmost edge.

After the road geometry is defined, vehicles have to be sorted in order to provide neighbouring vehicle positions for the traffic model. A sorting algorithm is based on sorting distance, defined as maximum length from entry into the road network. Sorting distance is a continuously increasing value increasing from the input into road network and is illustrated in the Figure 8.

Figure 6. Continuous (a) and discrete (b) lane change

<!-- image -->

Bar chart

Figure 7. Definition of lane geometry

<!-- image -->

Engineering drawing

<!-- image -->

Engineering drawing

4

1

3

1

2

Figure 8. Definition of lane geometry

<!-- image -->

Engineering drawing

Figure 9. Adjacent vehicles and distances

After  the  vehicles  are  sorted,  neighbouring  vehicles on adjacent lanes can be determined. Vehicles that are of interest for lane change and vehicle following algorithms are: front-left, front, front-right and rear. Adjacent vehicles are shown in Figure 9.

## 2.4. Visualization of simulation outputs

The simulation results are post-processed and visualized in several ways:

- in operator HMI (SCADA, video-detection interface and video-surveillance 3D display);
- in instructor HMI (tunnel state, reports, time-value plots).

A  video  surveillance  simulation  module  is  a  3D computer graphics display that serves as a substitute for surveillance monitors that are being used by the tunnel operators to acquire information about situations in the tunnel. It renders states of the tunnel model in 3D space; therefore, every simulated object must have 3D coordinates  and  orientations  defined  in  the  simulator  core  itself. The visualization should be refreshed at about 20-30 frames/s in order to achieve a visually pleasant result for the observer.

Each model has its own time step, which may be longer than the maximum allowable time step for visualization and  since  visualization  module  data  is  synchronized  at fixed time-steps, it is necessary to carry out interpolation of object movement, including translation and orientation changes between synchronization time-steps.

In Figure 10, vectors representing object positions are shown, where ( ) x t is the position of an object in the simulator core and ( ) y t is the visualized object. When change in  speed ( ) v t occurred at time 2 T dt ⋅ + ,  the  movement of an object in the visualization continues along its way, but in such a way that visualized and simulated positions are synchronized by the next timestep. This is achieved by calculating object speed as:

<!-- formula-not-decoded -->

Visualization  of  sensor  and  equipment  states  and control of tunnel equipment is achieved using the same SCADA interface as in a real control centre, but is connected to a computer-based simulator instead of to real tunnel controllers. The interface can be seen in Figure 11.

Figure 10. Interpolation of vehicle coordinates for visualization

<!-- image -->

Line chart

Figure 11. Operator SCADA interface

<!-- image -->

Geographical map

It is used to supervise and control ventilation, VMS, traffic lights, illumination, power supplies, firefighting equipment and incident detection.

The third video detection alarm interface that is used to control video surveillance is an exact replication of native interface using and showing notifications and alarms in exactly the same way. The data that is usually provided by the video processors is provided by the simulator core based on the traffic and ventilation simulation outputs:

- speed measurement, standing vehicles, static objects on the road;
- visibility, smoke concentration.

## 2.5. Ventilation model tuning and validation

<!-- image -->

Line chart

The most difficult  part  of  the  unified  model  to  be  calibrated is the ventilation model. It was carried out by comparing the results with the IDA Road Tunnel Ventilation Model (Sahlin, Grozman 2003). Variables observed during the model tuning were: air velocity, air temperature, wall temperature and extinction coefficient (smoke concentration).

Air velocity calculations using the IDA model and the simulator under the same conditions show similar results that can be seen in Table.

Air temperature growth after fire can be observed in the Figure 12. Since air flow direction is from left to right and as the tunnel walls heat, the hot area increases in the direction of the air flow. Tunnel walls are the main source of cooling during the tunnel fire.

A comparison of the air temperature profile obtained with the IDA road tunnel ventilation and with a real-time simulator  is  slightly  different  for  several  reasons  (Figure 13):

Figure 12. Air temperature profile during 50 MW fire

<!-- image -->

Line chart

Figure 13. Air temperature compared to IDA tunnel model

- in the real-time simulator, traffic does not stop immediately, thus influencing the air speed;
- meshing is different;
- in  IDA  ventilation  fans  are  controlled  at  constant speed;  in  the  tunnel  simulator  ventilation  is  controlled according to the tunnel algorithm.

Table. Comparison of simulated longitudinal air speeds during same conditions

|                | Longitudinal air speed [m/s]   | Longitudinal air speed [m/s]   |
|----------------|--------------------------------|--------------------------------|
| Tunnel section | IDA model                      | Simulator                      |
| 3-lane tube    | 5.9                            | 5.94                           |
| 2-lane tube    | 5.5                            | 5.32                           |
| exit ramp      | 4.6                            | 4.69                           |

## 3. Applications of the model

## 3.1. Operator training simulation

The  purpose  of  a  simulator  is  to  replace  the  operator workplace in a control centre with a simulated workplace, providing exactly the same user interface. Therefore, original SCADA interfaces that are being used for operational tunnels were used and connected to the simulator instead of to a real tunnel control network. A view of a simulated and a real workplace can be seen in Figure 14. The only difference is that video surveillance is replaced with a 3D rendering of the situation in the tunnel while maintaining exactly the same camera control interface that supports zooming and rotating.

Operators are supervised by the instructors through a  special  interface  during  training.  The  instructor  user

a)

<!-- image -->

Photograph

b)

Figure 14. Operator workplace (a) and simulator (b)

<!-- image -->

Photograph

interface has the capability to control the simulation variables, define scenarios and supervise the situation in the tunnel during the training. The instructor is able to adjust weather conditions, traffic density, cause traffic incidents or disable systems. In the end the instructor is supposed to determine if the operator's actions were satisfactory.

Assessment of simulation outputs should answer the question of how effective the operator responses were and if  the  rules and procedures are being followed. This can be  evaluated  by  observing  compliance  with  regulations by the instructors or how many road users survive and how many are subjected to danger by observing variables such as road user and vehicle positions, vehicle speeds, air temperature and smoke concentrations. To avoid this problem, a parameter an Immediate Danger for Life and Health (IDLH) area is observed throughout the simulation. In Figure 15, vehicle positions and the IDLH area are shown over 450 s. The vehicles at given distance are shown as colour dots, depending how many vehicles at given distance are there in parallel. After about 60 s the traffic is completely stopped and vehicle position points are at constant positions, forming horizontal lines. Few vehicles are affected by the fire, since most of them stopped in time. If air flow was not in the direction of the traffic, the IDLH area would be covering stopped vehicles, thus resulting in more damage. Therefore, the conditions in the Figure 15 show good response of the tunnel control system.

During the simulator development, the exact geometry of the tunnel was defined with cameras at the same positions as in the real tunnel, so the operators could observe the events through familiar views.

The operators  are  able  to  learn  how  to  read  important parameters in the tunnel and study the interaction of different systems such as ventilation control, traffic and environmental conditions. The interactions between the systems are complex and can result in unsuccessful emergency services intervention or loss of lives if not managed properly.

Figure 15. IDLH area during fire simulation scenario

<!-- image -->

Line chart

Figure 16. Vehicle and positions and fan operation during the incident

<!-- image -->

Engineering drawing

## 3.2. Case study: tunnel control optimization

An example of tunnel control optimization using the integrated tunnel model can be derived from the study of the Trojane tunnel fire accident that occurred in Slovenia in  2010  as  it  exposed  some  weaknesses  of  the  installed tunnel control system (Luin et al. 2011). The Trojane tunnel is a twin-tube motorway tunnel that is situated on the Slovenian A1 motorway, which is part of trans-European road network and represents an important east-west link on the 5-th corridor. The road is subject to heavy traffic with yearly daily average of 37000 vehicles, among which 29% are cargo vehicles.

The  incident  started  after  a  Heavy  Goods  Vehicle (HGV) broke down and stopped inside the tunnel. The incident detection system recorded the incident and automatically lowered speed limit and closed down the incident lane. According to the data that was obtained from the video surveillance system, especially the truck drivers maintained too short headway distance and drove at too high speed. Consequently, several vehicles collided, which resulted in an HGV fire that occurred 570 m from the entry portal. The evacuation of the tunnel users was meant to carry out through the emergency cross passage and the sidewalk of the opposite-direction tube, but during  the  incident  the  ventilation  system  did  not  assure smoke-free evacuation path due to unknown reason at a time, although it was discovered that everything operated according to the design procedure. The smoke that was supposed to be extracted longitudinally, in the direction of the traffic where no tunnel users remained, entered the cross passage and moved into the opposite tube. The situation is shown in the Figure 16.

To  identify  the  cause  of  unexpected  spreading  of smoke and to improve the tunnel ventilation control and incident management, the integrated tunnel model with the simulator was used. In order to replicate the conditions, it was necessary to define vehicle positions as they were observed from the video recordings. As it is shown in the Figure 16, 4 heavy vehicles formed a jam right after the cross passage, which resulted in pressure increase in the incident tube. After simulating the fire event, following relative air pressure that is shown in the Figure 17 was obtained.

Figure 17. Pressure distribution during the incident

<!-- image -->

Line chart

It  is  obvious  that  at  the  distance  of  500  m  from  the entry portal, the pressure in the incident tube was higher than in the empty tube although according to the design strategy it was supposed to assure that the empty tube is pressurized relative to the incident tube. Apparently, the collided heavy vehicles and 4 ventilation fans at the beginning of the tunnel yielded pressure difference of about 6 Pa, which resulted in smoke movement towards the empty tube.

It  was  verified  if  higher  pressure  was predominantly due to the standing vehicles and therefore the simulation was repeated under assumption of the empty tunnel tube. The results are shown in the Figure 18, where the ventilation system still causes similar conditions, except that the pressure difference drops to 4 Pa. This means that even in  an  empty tunnel the designed emergency ventilation control system does not function adequately if the first cross passage is used.

To achieve sufficient pressure difference in case a fire occurs in the first 1000 m of the tunnel, the solution was to switch on only a single pair of fans at the tunnel entrance  thus  obtaining  conditions  in  the  Figure  19.  This way about 2 Pa higher pressure is obtained in the empty tube even though there are heavy vehicles stopped after the cross passage.

The described example shows that the conditions in the tunnel are influenced by a complex set of variables defined by the traffic, ventilation, meteorological conditions and tunnel equipment operation. The integrated model of the road tunnel traffic, ventilation and evacuation provides possibility to study complex scenarios that may occur in the tunnels and improve and optimize control algorithms so they can provide adequate evacuation possibilities during normal operation and during emergency conditions.

Figure 18. Pressure distribution during the incident

<!-- image -->

Line chart

<!-- image -->

Line chart

## Conclusions

The simulator that is based on a real-time tunnel model provides  a  novel  tool  for  evaluation  of  new  equipment and HMI in road tunnels and also for more efficient and comprehensive road tunnel operator training. The simulator training enables the operators to become familiar with the user interface they will encounter at their workplace. However, the most important benefit of simulator training is  increasing preparedness for emergency situations that have the potential to result in a large number of fatalities and material damage. Operators can train critical scenarios on simulators and practice actions that should be taken in case of emergency. This way they gain significant experience they will need in case a major accident occurs and they are the first to take action and properly inform emergency services.

Apart from road tunnel operator training, the model can be used for validation and optimization of tunnel control procedures that should be carried out during the tunnel design. It was shown on a case study of a real accident that the integrated tunnel model is a useful tool to identify causes of tunnel control malfunction and to obtain solutions to the tunnel control problems.

Key distinction of the presented approach from other modelling attempts found in the reviewed literature is the integration of different models and the simplification of the traffic, ventilation and evacuation models in order to build a unified model that is computationally undemanding and can be executed in real time or faster. This way it is possible to evaluate large sets of different scenarios for optimization and risk analysis purposes.

A merged model has some drawbacks, such as that the ventilation model is very simplified and is mostly accurate in 1D. If a true 3D CFD model was used, simulation would be more realistic, but it would be extremely difficult to achieve real time operation, especially merged with traffic and evacuation models that would imply constantly changing geometry and boundary conditions.

Figure 19. Pressure differences between the tubes after optimization of the algorithm

In the future, the model could be improved to be used as  a  risk  analysis  tool  by  executing  multiple  simulation runs in order to estimate damage to the tunnel and fatalities among tunnel users under different scenarios. An attempt for an improved, 3D ventilation model would also be useful in order to improve accuracy as the computer hardware is quickly developing and Graphic Processing Units (GPU) nowadays provide a cost-efficient possibility for parallel computations.

## Acknowledgements

We are expressing gratitude to Urban Džindžinovič for collaboration during 3D visualization development and Savin Gorup from company 'ASIST avtomatizacija sistemov d.o.o.' (Slovenia) for detailed data on tunnel control system communication.

## Funding

This  work  was  supported  by  the  ARRS  under  Grant L2-2324; and DARS, d.d. under Grant 29/20010.

## Author contributions

Blaž  Luin  developed  and  tuned  the  unified  model  and performed adaptation for communication with real tunnel human-machine interfaces.

Stojan Petelin took care of project leadership and supervised the implementation and testing.

## Disclosure statement

The authors have no competing financial, professional, or personal interests from other parties.

## References

Alvear, D.; Abreu, O.; Cuesta, A.; Alonso, V . 2013. Decision support system for emergency management: road tunnels, Tunnelling and Underground Space Technology 34: 13-21.

[https://doi.org/10.1016/j.tust.2012.10.005](https://doi.org/10.1016/j.tust.2012.10.005)

Caliendo, C.; Ciambelli, P.; De Guglielmo, M. L.; Meo, M. G.; Russo, P. 2012a. Numerical simulation of different HGV fire scenarios  in  curved  bi-directional  road  tunnels  and  safety evaluation, Tunnelling and Underground Space Technology 31: 33-50. https://doi.org/10.1016/j.tust.2012.04.004

Caliendo, C.; Ciambelli, P.; De Guglielmo, M. L.; Meo, M. G.; Russo, P. 2012b. Simulation of people evacuation in the event of a road tunnel fire, Procedia - Social and Behavioral Sciences 53: 178-188. https://doi.org/10.1016/j.sbspro.2012.09.871

Capote, J. A.; Alvear, D.; Abreu, O.; Cuesta, A.; Alonso, V . 2013. A real-time stochastic evacuation model for road tunnels, Safety Science 52: 73-80. https://doi.org/10.1016/j.ssci.2012.02.006

Carvel, R.; Rein, G.; Torero, J. L. 2009. Ventilation and suppression systems in road tunnels: some issues regarding their appropriate use in a fire emergency, in 2nd International Tunnel Safety Forum for Road and Rail , 20-22 April 2009, Lyon, France, 375-382.

Cassini, P .; Hall, R.; Pons, P . 2003. Transport of Dangerous Goods through Road Tunnels Quantitative Risk Assessment Model. Version 3.60. Reference Manual . OECD/PIARC/EU (CD-ROM).

Cassini, P . 1998. Road transportation of dangerous goods: quantitative risk assessment and route comparison, Journal of Hazardous Materials 61(1-3): 133-138.

[https://doi.org/10.1016/S0304-3894(98)00117-4](https://doi.org/10.1016/S0304-3894(98)00117-4)

Cha, M.; Han, S.; Lee, J.; Choi, B. 2012. A virtual reality based fire training simulator integrated with fire dynamics data, Fire Safety Journal 50: 12-24.

[https://doi.org/10.1016/j.firesaf.2012.01.004](https://doi.org/10.1016/j.firesaf.2012.01.004)

EC. 2004. Directive 2004 / 54 / EC of the European Parliament and of the Council of 29 April 2004 on Minimum Safety Requirements for Tunnels in the Trans-European Road Network . Available from Internet: http://data.europa.eu/eli/dir/2004/54/oj

Fritzsche, H.-T. 1994. A model for traffic simulation, Traffic Engineering &amp; Control 35(5): 317-321.

Gandit,  M.;  Kouabenan,  D.  R.;  Caroly,  S.  2009.  Road-tunnel fires: risk perception and management strategies among users, Safety Science 47(1): 105-114.

[https://doi.org/10.1016/j.ssci.2008.01.001](https://doi.org/10.1016/j.ssci.2008.01.001)

Gipps, P. G. 1981. A behavioural car-following model for computer simulation, Transportation Research Part B: Methodological 15(2): 105-111.

[https://doi.org/10.1016/0191-2615(81)90037-0](https://doi.org/10.1016/0191-2615(81)90037-0)

Haghighat, F.; Li, Y.; Megri, A. C. 2001. Development and validation of a zonal model - POMA, Building and Environment 36(9): 1039-1047.

[https://doi.org/10.1016/S0360-1323(00)00073-1](https://doi.org/10.1016/S0360-1323(00)00073-1)

Hashemkhani Zolfani, S. H.; Esfahani, M. H.; Bitarafan, M.; Zavadskas,  E.  K.;  Arefi,  S.  L.  2013.  Developing  a  new  hybrid MCDM method for selection of the optimal alternative of mechanical longitudinal ventilation of tunnel pollutants during automobile accidents, Transport 28(1): 89-96.

[https://doi.org/10.3846/16484142.2013.782567](https://doi.org/10.3846/16484142.2013.782567)

IEC 62381:2012. Automation Systems in the Process Industry - Factory Acceptance Test ( FAT ), Site Acceptance Test ( SAT ), and Site Integration Test ( SIT ) .

IEC TS 62603-1:2014. Industrial Process Control Systems - Guideline for Evaluating Process Control Systems - Part 1: Specifications.

Kesting, A.; Treiber, M.; Helbing, D. 2010. Enhanced intelligent driver  model  to  access  the  impact  of  driving  strategies  on traffic capacity, Philosophical Transactions of the Royal Society A: Mathematical , Physical and Engineering Sciences 368: 4585-4605. https://doi.org/10.1098/rsta.2010.0084

Kesting, A.; Treiber, M.; Helbing, D. 2007. General lane-changing model MOBIL for car-following models, Transportation Research Record: Journal of the Transportation Research Board 1999: 86-94. https://doi.org/10.3141/1999-10

Krajzewicz, D.; Erdmann, J.; Behrisch, M.; Bieker, L. 2012. Recent development and applications of SUMO - simulation of urban mobility, International Journal on Advances in Systems and Measurements 5(3-4): 128-138.

Luin, B.; Petelin, S.; Vidmar, P . 2011. Trojane road tunnel operation during emergency conditions, in ISEP 2011: 19th International Symposium on Electronics in Transport , 28-29 March 2011, Ljubljana, Slovenia, 1-4.

Peacock, R. D.; Forney, G. P .; Reneke, P . A. 2013. CFAST - Consolidated Model of Fire Growth and Smoke Transport ( Version 6 ) : Technical  Reference  Guide .  US  Department  of  Commerce, Washington, DC, US. 129 p. https://doi.org/10.6028/NIST. SP.1026r1

Petelin, S.; Luin, B.; Vidmar, P . 2010. Risk analysis methodology for  road  tunnels  and  alternative  routes, Strojniški  vestnik  - Journal of Mechanical Engineering 56(1): 41-51.

Sahlin, P . 1996. Modelling and Simulation Methods for Modular Continuous Systems in Buildings .  Royal Institute of Technology, Stockholm, Sweden. 187 p.

Sahlin, P .; Grozman, P . 2003. IDA simulation environment a tool for Modelica based end-user application deployment, in Proceedings of the 3rd International Modelica Conference 2003 , 3-4 November 2003, Linköping, Sweden, 105-114.

Shi, J.; Ren, A.; Chen, C. 2009. Agent-based evacuation model of large public buildings under fire conditions, Automation in Construction 18(3): 338-347.

[https://doi.org/10.1016/j.autcon.2008.09.009](https://doi.org/10.1016/j.autcon.2008.09.009)

Suzuki, K.; Harada, K.; Tanaka, T. 2003. A multi-layer zone model  for  predicting  fire  behavior  in  a  single  room, Fire  Safety Science 7: 851-862. https://doi.org/10.3801/IAFSS.FSS.7-851

Treiber, M.; Kesting, A. 2013. Traffic Flow Dynamics: Data , Models and Simulation . Springer. 503 p.

[https://doi.org/10.1007/978-3-642-32460-4](https://doi.org/10.1007/978-3-642-32460-4)

Voeltzel, A.; Dix, A. 2004. A comparative analysis of the Mont Blanc, Tauern and Gotthard tunnel fires, Routes / Roads 324: 18-34.

Wan, H.; Du, Z.; Yan, Q.; Chen, X. 2018. Evaluating the effectiveness of speed reduction markings in highway tunnels, Transport 33(3): 647-656.

https://doi.org/10.3846/transport.2018.1574

Wiedemann,  R.  1974. Simulation  des  Straßenverkehrsflusses .  Instituts  für  Verkehrswesen  der  Universität  Karlsruhe, Deutschland. 85 S. (in German).

Xu, Z.; Lu, X. Z.; Guan, H.; Chen, C.; Ren, A. Z. 2014. A virtual reality based fire training simulator with smoke hazard assessment capacity, Advances in Engineering Software 68: 1-8. https://doi.org/10.1016/j.advengsoft.2013.10.004
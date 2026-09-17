<!-- image -->

Logo

Contents lists available at ScienceDirect

## Heliyon

journal homepage: www.heliyon.com

## A new tunnel fi re detection and suppression system based on camera image processing and water mist jet fans

Alireza Sarvari, Sayyed Majid Mazinani *

Department of Electrical Engineering, Imam Reza International University, Mashhad, Iran

## A R T I C L E I N F O

## Keywords:

Mechanical engineering Systems engineering Safety engineering Natural hazards Computer science Fire protection Tunnel fi re Fire fi ghting Fire detection and suppression Image processing Water mist Jet fan

## 1. Introduction

A water mist system is a fi re protection system that controls and suppresses fi re by projecting ultra fi ne droplets onto a target, thereby reducing ambient temperature, replacing oxygen with vapor, and eliminating fi re radiation effects. The droplets are produced by the highpressure pumping of water through a small nozzle. Water mist systems are widely used during fi res in road tunnels. In the past, the use of water systems in such underground passages were prohibited by European and North American standards. For example, Annex D of the Standard for Road Tunnels, Bridges, and Other Limited Access Highways of the National Fire Protection Association (i.e., NFPA 502) rejected the use of water systems in tunnels for reasons such as reduced vision, the possibility of gas explosion due to water spray, and potential steam damage to people. This standard also advised against the installation of sprinkler systems in tunnels, except in those traversed by hazardous heavy vehicles.

These stipulations were reconsidered by road tunnel authorities after the tunnel fi res that occurred between 1995 and 2005 and the consequent fi nancial losses. Attempts to rectify the fl aws of existing water mist

* Corresponding author. E-mail address: smajidmazinani@imamreza.ac.ir (S.M. Mazinani).

## [https://doi.org/10.1016/j.heliyon.2019.e01879](https://doi.org/10.1016/j.heliyon.2019.e01879)

Received 15 September 2018; Received in revised form 26 March 2019; Accepted 29 May 2019

2405-8440/ © 2019 The Authors. Published by Elsevier Ltd. This is an open access article under the CC BY-NC-ND license (http://creativecommons.org/licenses/bync-nd/4.0/).

## A B S T R A C T

Several tunnel fi re detection and fi ghting systems are currently available in the market, each with its own pros and cons. Although no single system is perfect, the water mist system is one of the top-performing conventional tunnel fi re suppression systems available. The problem is that such system is expensive. More affordable equipment with similar performance would be a breakthrough in the fi eld of tunnel safety. Accordingly, this study develop a new water mist system, in which ventilation jet fans are utilized in such a way to achieve economical feasibility. The system features monitoring cameras use to determine fi re coordinates and mist-generating jet fans employed to suppress fi re. The front of the ventilation jet fans is equipped with nozzles, which spray water frontward through the fans, thereby creating mist and propelling it toward the location of a fi re. The mist that shoots out of the fans reduces ambient temperature, fl ushes oxygen, cools the surface of in fl ammable materials, and weakens radiative and convective effects. The simulation of the proposed system shows a low heat release rate, smoke and toxic fumes reduction, tunnel ventilation speed increases, and improved visibility. These improvements enhance tunnel safety and make tunnel conditions during a fi re less threatening to human health. The cost of the system put forward in this work can be further reduced by optimizing the materials that constitute the pipes and fi ttings and removing the fi re fi ghting pumps.

systems followed. Over time, these systems gradually became a cornerstone of tunnel safety. Despite the limitations associated with water mist systems, the installation of such fi re fi ghting equipment in tunnels presents merits, including desirable control over fi re size and spread rate and reliable maintenance of tunnel conditions [1, 2, 3]. In its latest edition, NFPA 502 recommends the use of water mist technology with deluge con fi gurations in Category C and D tunnels [4].

The effective and reliable preservation of breathing conditions in tunnels necessitates the rapid detection of fi re and the implementation of fi re fi ghting measures [5]. With these requirements in mind, we developed a new tunnel fi re detection and suppression system, through which fi re is detected with the help of image processing and controlled in a manner similar to how water mist systems operate but with the added advantage of ventilation jet fans. In the proposed system, an image processing subsystem is fed data by monitoring cameras that identify the occurrence and coordinates of a fi re in a tunnel. Upon fi re detection, the mist required to control the fi re is generated via the pumping of water provided by low-pressure urban water pipelines through a series of nozzles located in front of the ventilation jet fans. The fans operate at higher-than-normal revolutions per minute and thereby produce water droplets with a diameter less than 300 μ m.

<!-- image -->

Logo

<!-- image -->

Icon

The rest of the paper is structured as follows. Section 2 presents a review of standards and studies on fi re detection and fi re fi ghting in tunnels. Section 3 explains the proposed system, its structure, how it detects and locates fi re, how fi re fi ghting procedures are implemented, and how the water mist jet fans suppress fi re. Section 4 is dedicated to the analysis of the system via the Fire Dynamics Simulator (FDS) used with Pyrosim. It also provides comparison tables and the results of the FDS and computational fl uid dynamics analyses, which are necessary to evaluate improvement in fi re fi ghting performance and tunnel safety. Section 5 concludes the paper with a summary of the fi ndings.

## 2. Related work

Upon the occurrence of a fi re, the most important step in limiting its consequences is the timely response of a fi re detection system in alerting people and triggering fi re fi ghting procedures. A study conducted by the Canadian national research council revealed that among the fi re detectors widely used in tunnels, CCTV cameras have one of the best response times under adverse tunnel conditions. They have exhibited a response time of less than 1 minute for large fi res with a rapid spread rate [6]. Because CCTV cameras can reliably monitor a fi re, they can also identify its size, location, and spread rate. These devices are equipped with image processing technology that enables the identi fi cation of the coordinates of a fi re in a tunnel by simply zoning the tunnel and synchronizing the zones with camera images [7, 8, 9].

In recent years, water-based fi re fi ghting systems have undergone major developments; various fi re protection systems for tunnels are currently available, ranging from sprinkler systems that release large water droplets to water mist systems that are based on different technologies [1]. Until 2004, fi re protection authorities were opposed to the use of water-based fi re fi ghting systems in tunnels, arguing that water may facilitate gasoline explosion and that water vapor may hurt people and reduce vision; these factors collectively increase the possibility of additional incidents in a tunnel [10]. With the lessons learned from the tunnel accidents that occurred between 1995 and 2005, further efforts were made to control fi res and their effects. Such efforts involved the use of ventilation jet fans and the retro fi tting of tunnels. These measures, however, were proven insuf fi cient during tests conducted in a Norwegian tunnel; the researchers found that fi re fueled by a bus accident produces about 20 MW of heat a problem that cannot be adequately addressed by the existing fi re protection systems [11]. This de fi ciency prompted the revision of fi re protection standards, which now recommend the use of water spray or water mist fi re fi ghting systems to control and suppress fi res. The effectiveness of this recommendation was con fi rmed in a tunnel in Spain. A water mist system has promising potential for not only controlling fi re but also improving air quality and reducing toxic fumes. As a result, the system became known as an effective suppression system for fi res in tunnels [12, 13, 14].

Analysis of vehicle fi res and testing data shows that heat release rates can reach 20 MW in a few minutes. Based on this data following frame of plausible fi re scenarios could be drawn:

1. A small slow growing passenger car fi re (HRRmax ¼ 0.5 MW)
3. A collision involving two passenger cars (HRRmax ¼ 8 MW)
2. A fast growing passenger car (HRRmax ¼ 4 MW)
4. A fast bus fi re (HRRmax ¼ 30 MW)
5. A HGV fi re (HRRmax ¼ 100 MW)

The main objectives of water mist systems in tunnel are to reduce:

1. The rate of growth of the fi re;
2. The heat release rate of the fi re;
3. The limit size of the fi re;
4. The risk of fi re spread from one vehicle to another.

Building upon existing smoke and fi re suppression systems, we introduce a new water mist system that utilizes ventilation jet fans to achieve an ef fi ciency higher than that of its predecessors. The advantage of the system lies in the changes applied to the functioning of ventilation jet fans that are already installed in a tunnel. This re fi nement renders the system more economic than its counterparts.

## 3. Theory

The proposed system consists of three subsystems, namely, the detection, processing, and fi re fi ghting subsystems. Each subsystem and the principles that underlie its operation are explained in the succeeding sections.

## 3.1. Fire detection

The fi re detection subsystem detects fi res through the processing of images captured by monitoring cameras and liner heat detector that work simultaneously. Once a fi re is detected, its coordinates are determined and sent to the processing subsystem [made of fi eld-programmable gate arrays (FPGAs)], which then directs the fi re fi ghting subsystem to activate local water mist jet fans and accordingly focus a control measure on the exact location zone of the fi re. The segmentation of tunnel space during the fi re detection stage is performed with the help of fi re detection by Video Image Processing cameras (Fig. 1) [2, 3].

As shown in Fig. 1, smoke coordinates are rapidly detected when a fi re is at a considerably small magnitude (i.e., releasing less than 1 MW of heat). At this stage, fi re and smoke can be effectively controlled with a small amount of water and energy, as required by fi re protection standards. The water required for this purpose is provided by a water mist jet fan, which shoots the water toward the desired coordinates.

Fig. 2 presents the algorithm for detecting smoke or fl ame and activating the countermeasure system accordingly. Fire coordinate codes can be attached to fi re alarm signals so that information on fi re location can also be sent to the processing subsystem.

Early fi re detection by Video Image Processing combined with LHD in tunnel can detect fi re less than 1 minutes then the proposed fi re extinguish system actives while the fi re is under 3MW.

## 3.2. Fire data processing

Today, remote control centers that are equipped with intelligent systems and run by expert operators are extensively used in nearly all major cities in the world to improve traf fi c management and transportation performance. In a fi re detection system, detection can be made either by the human operators who monitor tunnels or by a dedicated subsystem that operates on the basis of a predetermined algorithm [6]. The proposed fi re detection and control system comes with a control center that is responsible for the automatic control and management of the system. However, this control center can also be operated and programmed from a distance by human operators in response to unforeseeable events.

Once smoke or fl ame is detected, its characteristics, such as fl ame dimensions, generated smoke, and location coordinates (XYZ), are fed to an FPGA chip, which processes the information to produce commands that must be sent to the components of the water supply system and water mist jet fans. The commands sent to the water supply components include the activation of fi re pumps and the opening of solenoid valves that allow water to fl ow into the nozzles located in front of the jet fans. The proposed system also allows for the advance estimation of the quantity of water required for each jet fan on the basis of type of fi re and fi re dimensions. In the event of a fi re, fl ame and smoke detection cameras identify the site where the fi re has occurred and convert the ascertained location into a coordinate code, which is then sent to the motors that control the direction of the jet fans. The code directs the motors to turn the jet fans toward the fi re. The rotational speed of the jet fans are then adjusted in such a way as to spray water mist toward the exact location of the fi re. The amount of water for suppressing the fi re is controlled by means of solenoid valves. The mechanism that underlies control over water pipes and valves is explained in Section 4. Fig. 3 illustrates the procedure with which fi re data are processed in the proposed water mist system.

Fig. 1. Fire detection and location by image processing.

<!-- image -->

Engineering drawing

Fig. 2. Fire and smoke detection and signaling algorithm.

<!-- image -->

Flow chart

## 3.3. Firefighting

The NFPA standard classi fi es tunnels into fi ve categories according to size [4].

1. Category X: Tunnels with a length shorter than 90 m.
2. Category A: Tunnels with a length equal to or longer than 90 m.
3. Category B: Tunnels with a length equal to or longer than 240 m or tunnels where one segment is located at least 120 m from the nearest safe point.
4. Category C: Tunnels with a length equal to or longer than 300 m.
5. Category D: Tunnels with a length equal to or longer than 1000 m.

According to Clause 7.10.1 of NFPA 502 (2017), Category C and D tunnels must be fi tted with a fi xed fi re fi ghting system. It also states that fi re fi ghting systems for tunnels can be classi fi ed into two categories: fi re control systems and fi re suppression systems. The system put forward in this work corresponds to both these categories. It consists of two sections, namely, the water supply and mist generation sections. The water supply section comprises urban water resources, water pipelines, remotecontrolled solenoid valves, and water spray nozzles installed in front of the jet fans. As stipulated in Clause 10.2 of NFPA 502, the water to be used for suppressing a fi re in a tunnel should be connected to a resource large enough to provide the required volume of water for at least 1 hour. In the mist generation section of the system, ventilation jet fans are used to generate water mist. For this purpose, water is pumped from a resource via pipelines toward the nozzles located in front of the jet fans. Simultaneously, the rotational speed of the jet fans are increased to sharply enhance their exhaust power. In the nozzles, water is combined with air and then propelled toward the fans to generate water mist and concentrate it onto the exact location of a fi re. This action dramatically reduces the temperature and oxygen content of the fi re and thereby suppresses the blaze. Note that this feature also leads to considerable water conservation and cost savings in terms of fi re fi ghting pumps and pipes. Furthermore, the use of a low volume of water causes minimal damage to a tunnel's structure.

Tunnel fi res can be categorized into two classes: Class A fi res, which are caused by in fl ammable solids, and Class B fi res, which are caused by in fl ammable liquids. These fi res can be suppressed through sprinkler systems, deluge water spray systems, water mist systems, and foam systems, each with their own fl aws and merits (Table 1). As indicated in Table 1, a water mist system exhibits the best performance in tunnels and is highly recommended by the majority of today's standards [15, 16].

However, it is far more expensive than conventional water-based systems because it requires extremely high-pressure equipment, such as fi re pumps and steel pipes, and relatively expensive solenoid valves. According to the NFPA 750 standard, there are three classes of water mist systems: high-, medium-, and low-pressure systems. High-pressure water mist systems have an operating pressure of about 100 - 160 bars and transform water completely into mist, resulting in approximately 1700 times higher heat absorption than that achieved with conventional sprinklers. Lowand medium-pressure water mist systems have an operating pressure of less than 35 bars and generally work at pressures of 4 - 12 bars, which is close to the pressure range of conventional sprinklers. In these systems, water is converted completely into powder form and subsequently into ultra fi ne droplets. Compared with ordinary sprinklers, water mist systems have 1.4 times lower water consumption and can suppress fi re 50 times faster because of the greater surface area spanned by released water droplets.

Fig. 3. Procedure for processing fi re data and issuing commands in the proposed system.

<!-- image -->

Flow chart

Table 1 Comparison of water-based fi re fi ghting systems System type.

| Measure of comparison                | System type            | System type               | System type                         | System type   |
|--------------------------------------|------------------------|---------------------------|-------------------------------------|---------------|
|                                      | Sprinkler              | Deluge                    | water mist                          | Foam          |
| Operating pressure Particle diameter | 5 bars millimeters 1 < | 5-12 bars millimeters 1 > | 12-160 bars 300 < microns Good High | 17 bars -     |
| Performance Cost                     | Poor Low               | Medium Medium             |                                     | Excellent -   |

As indicated in Table 1, the best systems for fi re fi ghting in tunnels are water mist and foam systems, but the latter is impractical because of associated high costs. Our approach, therefore, was to improve the water mist system by applying slight modi fi cations to existing ventilation jet fans and transforming them into mist-generation machines capable of producing water particles smaller than 300 μ m. The majority of tunnels are equipped with a system of ventilation jet fans that control and fl ush out smoke, heat, and toxic fumes. In Category D tunnels, the use of emergency ventilation systems is mandatory. The number and capacity of jet fans can be calculated using various methods, but conformity to Clause 11.4 of NFPA 502 requires that the design of tunnel ventilation systems satisfy the release rate requirements for smoke, carbon dioxide, and heat [4]. Correspondingly, we modi fi ed a conventional tunnel fi re detection and suppression system to establish the fi re fi ghting subsystem for controlling fi re parameters and tunnel ventilation. In the subsystem (Fig. 4), jet fans more strongly home in on suppressing smoke and toxic fumes rather than on fl ushing them out of an area. Nevertheless, because of the high operating speed of the jet fans in this subsystem during fi res, the fumes created by fi re suppression and light toxic fumes are still rapidly expelled from a tunnel (Fig. 5).

Fig. 5 is a general diagram of fi re suppression via the proposed water mist system. As indicated in the fi gure, the combined use of water mist with the ventilation system enables improved control over fi re, smoke, and toxic fumes.

## 4. Calculation

This section presents the results of tests performed using the advanced fi re simulation software PyroSim to estimate the performance of the proposed system and improvements in terms of addressing heat, smoke, and vision problems. In essence, PyroSim is a user interface that facilitates working with two applications: the FDS and Smokeview. These applications can simulate the behavior of fi res with extreme precision.

1 Reproduced with permission of NFPA from NFPA 502, Standard for Road Tunnels, Bridges, and Other Limited Access Highways, 2017 edition. Copyright: copyright © 2016, National Fire Protection Association.

Fig. 4. Path of fi re spread in the presence of ventilation [4] 1 .

<!-- image -->

Engineering drawing

Computational Fluid Dynamics (CFD) and Fire Dynamics Simulator (FDS) developed by National Institute of Standards and Technology (NIST), one of the world's largest physics laboratories. Most of studies about tunnel fi re safety system are shown that FDS is a reliable and effective numerical tool for tunnel fi re simulation. For this reason, we use this software as a simulator of the proposed system.

## 4.1. FDS

FDS simulation software has important applications in the fi eld of simulated combustion and fl ue gas movement and fl ame propagation during fi re. We considered FDS as a feasible tool to simulate fi re happen in environment as it works out numerically a collection of the NavierStoker equations for thermally-driven fl ow. Both DNS (Direct Numerical Simulation) and LES (Large Eddy Simulation) models are included. In this investigation, we chose LES model since it is broadly used in the study of fi re induced smoke fl ow behavior. The governing equations for conservation of mass (1), species (2), momentum (3) and of energy (4) are as follows:

Fig. 5. Fire suppression by the jet fans in the proposed water mist system.

<!-- image -->

Engineering drawing

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

There is a collection of parameters consisting the fl uid thermal properties, droplet size distribution and injection features. By using them, the spray speci fi cations are determined at the injection point. FDS spray modeling represents water droplets by using lagrangian particles. Rosin-Rommler and log-normal distributions (5) indicate the droplet size distributions [17].

<!-- formula-not-decoded -->

## 5. Results

PyroSim was used to simulate a 2 - 2 m2 fi re in a 500 m long tunnel with a square 6 - 6 m cross-section over a period of 200 seconds. Simulations were performed in four scenarios. The fi rst scenario involves fi re in the basic tunnel without any ventilation or fi re suppression system. The second features the use of a jet fan system to control smoke. The third scenario was intended to estimate the results of a basic water mist system, and the fourth was designed to evaluated the performance of the proposed water mist jet fan system.

Fire set in Pyrosim simulation is polyurethane. Polyurethane (PUR and PU) is a polymer composed of organic units joined by carbamate (urethane) links, while most polyurethanes are thermosetting polymers that future like class A and class B fi re.

The Standard NF EN2 distinguishes among four classes of fi res depending on the nature of the fuel:

Class A: fi res are solid material fi res, generally producing embers when burning.

Class B: fi res are liquid or lique fi ed.

Class C: fi re are gas fi res.

Class D: fi res are metal fi res.

In the case of tunnels, the most commonly encountered fi re are of class A or B. Given the speci fi cities of tunnel fi res, the most appropriate extinguishing agent seems to be pure water. It is applicable to the fi res likely to occur in tunnels; it is also the most widely used and best known agent.

## 5.1. Scenario 1: basic tunnel

Figs. 6, 7, 8, and 9 show the heat release rate (HRR) and the smoke emission, temperature, and vision contours in transverse and longitudinal cross-sections at a height of 2 m above the tunnel fl oor. The simulation was run at t ¼ 200 seconds.

## 5.2. Scenario 2: tunnel with a jet fan system

In this simulation, a jet fan with an operating speed of 35 m3/s at a 60 m distance from a fi re is used to fl ush smoke and toxic fumes in one direction. Smoke and toxic fumes generated by vehicles during rush hours need to be expelled from the tunnel, and tunnel ventilation systems have no control over the spread of a fi re. Figs. 10, 11, 12, 13, and 14 illustrate the HRR and the smoke emission, temperature, and vision contours in transverse and longitudinal cross-sections at a height of 2 m above the tunnel fl oor. This simulation was run at t ¼ 200 seconds.

Fig. 8. Temperature contour at 2 m above the tunnel fl oor.

<!-- image -->

Line chart

As shown in Figs. 12, 13, and 14, the jet fans can manage only the smoke and toxic fumes produced by vehicles. Once a fi re starts, so much smoke is produced that, in practice, the jet fan system will fail to signi fi cantly contribute to smoke management. Even worse, fans can facilitate the spread of fi re because they infuse fresh air into a location. These problems highlight the need to design tunnel ventilation systems in such a way as to enable jet fans near a fi re to be turned off and an air fl ow velocity of 8 m3/s to be maintained. These features allow the fl ushing out of toxic fumes without spreading fi re. According to the NFPA 502 standard, this scenario is applicable to Category X, A, and B tunnels.

Fig. 9. Vision contour at 2 m above the tunnel fl oor.

<!-- image -->

Bar chart

Fig. 10. Location of the jet fan with an operating speed of 35 m3/s at 60 m from a fi re.

<!-- image -->

Icon

Fig. 11. HRR in the presence of the jet fan.

<!-- image -->

Line chart

Fig. 12. Smoke emission contour in the presence of the jet fan.

<!-- image -->

Line chart

## 5.3. Scenario 3: tunnel with a basic water mist system

The water mist system considered in this simulation has an operating pressure of 80 bars and a nozzle with a K-factor of 4.3

Fig. 13. Temperature contour at 2 m above the tunnel fl oor in the presence of the jet fan.

<!-- image -->

Bar chart

Fig. 14. Vision contour at 2 m above the tunnel fl oor in the presence of the jet fan.

<!-- image -->

Line chart

L/(min. 〖 atm 〗 ^ (1/2)). It produces water particles with a size of 100 μ m. Nozzle activation time was assumed to be 7 seconds after the initiation of a fi re. Fig. 15 shows the location of nozzles in the vicinity of the fi re.

Figs. 16, 17, 18, and 19 illustrate the HRR and the smoke emission, temperature, and vision contours in transverse and longitudinal crosssections at a height of 2 m above the tunnel fl oor. The simulation was run at t ¼ 200 seconds.

The HRR is about 1000 kW, and it takes about 100 seconds for the fi re to be completely extinguished. As depicted in Figs. 17, 18, and 19, although the water mist system exerts a minimal effect on smoke, toxic fumes, and fi eld of vision, it excellently controls and suppresses the fi re and is therefore a desirable choice for fi re fi ghting in the simulated tunnel space.

## 5.4. Scenario 4: tunnel with the proposed system

This scenario involves the proposed system, in which the ventilation jet fans in the tunnel can generate water mist. The water provided by lowpressure urban water pipelines are fed into two nozzles installed in front of the jet fans, which inject the water at the required rate. At the same time, the operating speed of the jet fans is adjusted to propel the water across the desired distance. Fig. 20 presents the location of the nozzles in the PyroSim simulation.

The jet fan has an operating speed of 40 m3/s and is located 29 m away from a fi re. System activation time was assumed to be 20 seconds after the initiation of the fi re. Fig. 21 shows the location of the jet fans in the tunnel.

The HRR obtained from this simulation is plotted in Fig. 22, which indicates that the fi re is completely suppressed after approximately 90 seconds and that the maximum HRR is about 600 kW. As it can be seen, fi re suppression time in this scenario is 10 seconds shorter and the HRR is 400 kW lower than in the third scenario. This reduction in suppression time and HRR can be attributed to the high speed at which water mist is generated by the jet fans. Such generation accelerates the cooling of the surface of in fl ammable materials and the tunnel space.

Fig. 15. Location of the water mist nozzles above a fi re.

<!-- image -->

Engineering drawing

Fig. 16. HRR in the presence of the basic water mist system.

<!-- image -->

Line chart

Fig. 17. Smoke emission contour in the presence of the basic water mist system.

<!-- image -->

Line chart

Fig. 18. Temperature contour at 2 m above the tunnel fl oor in the presence of the basic water mist system.

<!-- image -->

Line chart

Fig. 23 indicates a faster reduction of smoke within the tunnel space in the fourth scenario compared with the third scenario. In the proposed system, smoke reduction is achieved in two ways: (i) smoke suppression through the weighing down of particulates following their combination with high-speed water mist and (ii) fl ushing of light gases through the air circulation above the jet fan water mist system. Given the features of the proposed system, it can also be used to improve air quality in tunnels during rush hours as the system circulates fresh air at a high rate and injects small amounts of water onto a target to facilitate the deposition of fumes and particulates.

Fig. 19. Vision contour at 2 m above the tunnel fl oor in the presence of the basic water mist system.

<!-- image -->

Bar chart

Fig. 20. Location of the nozzles in front of the jet fans.

<!-- image -->

Engineering drawing

Fig. 21. Location of the jet fans in the tunnel.

<!-- image -->

Icon

The contours of temperature and fi eld of vision at a height of 2 m above the tunnel fl oor are presented in Figs. 24 and 25. The proposed system restores tunnel temperature to the normal level within 100 seconds and provides a better fi eld of vision than do the systems in the previous scenarios.

For a better understanding of the performance of the proposed system, a three-dimensional diagram of system performance is presented in Fig. 26.

Fig. 22. HRR in the presence of the proposed system.

<!-- image -->

Line chart

Fig. 23. Smoke emission contour in the presence of the proposed system.

<!-- image -->

Bar chart

Fig. 24. Temperature contour at 2 m above the tunnel fl oor in the presence of the proposed system.

<!-- image -->

Bar chart

## 6. Conclusion

This study developed a new tunnel fi re detection and suppression system based on camera image processing and the use of water mist jet fans. Building upon a conventional water mist system, we proposed the use of ventilation jet fans for mist generation. This method of water mist generation increases the fl ow of fresh air into a tunnel space and improves fi re control and suppression performance. The simulation results showed a 10% shorter fi re suppression time and a 40% lower HRR than those achieved with a conventional water mist system. The results also indicated dramatic improvement in the fi eld of vision.

The result of the simulation was, that the proposed water mist system successfully passed all criteria as required by the noti fi ed testing institutes.

These criteria were:

1. successful prevention of spread of the fi re
2. Providing access to the scene for the fi re brigade to fi nally extinguish the fi re, which was the main problem of the tunnel fi res in the past.
3. Protecting the tunnel structure and prevent the concrete from spalling.

Fig. 25. Vision contour at 2 m above the tunnel fl oor in the presence of the proposed system.

<!-- image -->

Bar chart

Fig. 26. Three-dimensional diagram of the proposed system's performance.

<!-- image -->

Bar chart

The use of the proposed system can result in signi fi cant cost savings with the elimination of a fi re pump setup and the replacement of highpressure pipes and expensive nozzles with low-pressure and inexpensive pipes and fi ttings. The system can also improve normal ventilation during rush hours by infusing mist into a tunnel space for the reduction of toxic fumes and particulates. The proposed system is feasible not only technically but also economically because in Category D tunnels, where the use of ventilation jet fans is mandatory, the system can be implemented through slight modi fi cations in jet fans capacity and structure. This eliminates the need to procurement of separate fans and expensive equipment. Ultimately, the proposed system can easily replace old ventilation and fi re suppression systems and thus constitutes a positive step toward the integration of tunnel safety systems.

## Declarations

## Author contribution statement

Alireza Sarvari &amp; Sayyed Majid Mazinani: Conceived and designed the experiments; Performed the experiments; Analyzed and interpreted the data; Contributed reagents, materials, analysis tools or data; Wrote the paper.

## Funding statement

This research did not receive any speci fi c grant from funding agencies in the public, commercial, or not-for-pro fi t sectors.

## Competing interest statement

The authors declare no con fl ict of interest.

## Additional information

No additional information is available for this paper.

## References

- [1] [MS Aixi Zhou, Ph.D., P.E., Impact of Fixed Fire Fighting Systems on Road Tunnel Resilience, Ventilation, and Other Systems Final report By: Anurag Jha, The University of North Carolina at Charlotte Charlotte, NC, June 2017.](http://refhub.elsevier.com/S2405-8440(18)35692-5/sref1)
- [2] [A. Dix, The Impact of Fixed Fire Fighting Systems on Tunnel Safety - The Burnley Incident in a Current Theoretical Perspective, 2010.](http://refhub.elsevier.com/S2405-8440(18)35692-5/sref2)
- [3] [Directoraat-Generaal Rijkswaterstaat, Ministry of Transport, The Netherlands. Sprinklers in Japanese road tunnels. Final Report, December 2001.](http://refhub.elsevier.com/S2405-8440(18)35692-5/sref3)
- [4] [NFPA 502, Standard for Road Tunnels, Bridges, and Other Limited Access Highways, Annexes B and E, National Fire Protection Association, Quincy, MA, 2017.](http://refhub.elsevier.com/S2405-8440(18)35692-5/sref4)
- [5] [Y.Z. Li, H. Ingason, In fl uence of fi re suppression on combustion products in tunnel fi res, Fire Saf. J. 97 (April 2018) 96 - 110. Elsevier.](http://refhub.elsevier.com/S2405-8440(18)35692-5/sref5)
- [6] [International Road Tunnel Fire Detection Research Project - Phase II Task 2: FullScale Fire Tests in a Laboratory Tunnel for Study of Tunnel Fire Detection Technologies, July 2008.](http://refhub.elsevier.com/S2405-8440(18)35692-5/sref6)
- [7] [Chunyu Yu*, Zhibin Mei, Xi Zhang, The 9th Asia-Oceania Symposium on Fire Science and Technology A Real-Time Video Fire Flame and Smoke Detection Algorithm, 2013.](http://refhub.elsevier.com/S2405-8440(18)35692-5/sref7)
- [8] [Byoung Chul Ko, Kwang-Ho Cheong, Jae-Yeal Nam, Fire Detection Based on Vision Sensor and Support Vector Machines, September 2008.](http://refhub.elsevier.com/S2405-8440(18)35692-5/sref8)
- [9] [Seong G. Kong, Donglin Jin, Shengzhe Li, Hakil Kim, Fast Fire Flame Detection in Surveillance Video Using Logistic Regression and Temporal Smoothing, November 2015.](http://refhub.elsevier.com/S2405-8440(18)35692-5/sref9)
- [10] [NFPA 502, Standard for Road Tunnels, Bridges, and Other Limited Access Highways, Appendix D, National Fire Protection Association, Quincy, MA, 2004.](http://refhub.elsevier.com/S2405-8440(18)35692-5/sref10)
- [11] [PIARC, Fire and Smoke Control in Road Tunnels, World Road Association, 2007.](http://refhub.elsevier.com/S2405-8440(18)35692-5/sref11)
- [12] [R. Carvel, in: A. Beard, R. Carvel (Eds.), The Handbook of Tunnel Fire Safety, Thomas Telford Publishing Company, London, 2004, p. 119, chapter 6.](http://refhub.elsevier.com/S2405-8440(18)35692-5/sref12)
- [13] [S. Kratzmeir, M. Lakkonen, Fixed fi re fi ghting systems in tunnels - integration and compensation, in: A. L € onnermark, H. Ingason (Eds.), Proceedings, Fourth International Symposium on Tunnel Safety and Security, Frankfurt Am Main, Germany, 17 - 19 March, 2010, pp. 283 - 292. SP Sweden.](http://refhub.elsevier.com/S2405-8440(18)35692-5/sref13)
- [14] [J.R. Mawhinney, A critique of claims of smoke scrubbing by water mist, in: Proceedings of the National Fire Protection Research Foundation, Fire Suppression and Detection Research Application Symposium, Tampa, FL, January 23 - 25, 2002.](http://refhub.elsevier.com/S2405-8440(18)35692-5/sref14)
- [15] [PIARC, Fixed Fire Fighting Systems in Road Tunnels: Current Practices and Recommendations, World Road Association, Singapore, 2016, 2016.](http://refhub.elsevier.com/S2405-8440(18)35692-5/sref15)
- [16] [SOLIT, Engineering guidance for a comprehensive evaluation of tunnels with fi xed fi re fi ghting systems, Scienti fi c report of the SOLIT 2 research project, prepared by the, SOLIT 2 consortium, 2012, 2012.](http://refhub.elsevier.com/S2405-8440(18)35692-5/sref16)
- [17] [Qiang Liang, Yangfeng Li, Junmei Li, Hui Xu, Kaiyuan Li, Numerical studies on the smoke control by water mist screens with transverse ventilation in tunnel fi res, Tunn. Undergr. Space Technol. 64 (2017) 177 - 183. ISSN 0886-7798.](http://refhub.elsevier.com/S2405-8440(18)35692-5/sref17)
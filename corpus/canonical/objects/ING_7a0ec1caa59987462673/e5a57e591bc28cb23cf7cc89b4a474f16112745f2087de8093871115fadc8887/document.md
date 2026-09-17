Article

## SHM with Distributed Optical Fiber Sensors (DOFS) of a tunnel lining affected by nearby building construction

## Judit Gómez a , Joan R. Casas a,* and Sergi Villalba b

- a Department of Civil and Environmental Engineering, UPC - BarcelonaTech, c/ Jordi Girona 1 - 3, Barcelona 08034, Spain; joan.ramon.casas@upc.edu
- b Department of Engineering and Construction Projects, UPC - BarcelonaTech, c/ Colom 11, Ed. TR5, Terrassa (Barcelona) 08022, Spain; sergi.villalba@upc.edu
* Corresponding author: joan.ramon.casas@upc.edu

Received: date;

Accepted: date; Published: date

Abstract: This paper addresses the implementation of a Distributed Optical Fiber Sensor system (DOFS) to the TMB L - 9 metro tunnel in Barcelona for Structural Health Monitoring (SHM) purposes as the former could potentially be affected by the construction of a nearby residential building. With the aim of assessing the performance of this newly developed monitoring technology, an in - depth analysis on the collected strain readings is performed from which innovative data post - processing techniques are developed. Finally, the reliability of the installed DOFSs system is studied by means of a comparison with a theoretical model of the site's structural conditions.

Keywords: structural health monitoring; distributed fiber sensing; optical fiber; tunnel monitoring; safety

## 1. Introduction

The built environment comprises a wide range of infrastructure, from buildings, bridges, highways, tunnels, power plants and industrial facilities, to geotechnical and hydraulic structures. They are subjected to multiple events that deteriorate and compromise their structural integrity throughout their service lifetime exposing their future performance to several risks.

In existing infrastructure, some collapses occur due to accidental extraordinary events. These extreme events can involve collisions between the structure and high volume transport at high speed (trucks, ships or even airplanes), unexpectedly strong seismic activity or weather conditions such as wind and rain. All of which being highly unlikely to occur during the structure's service life and, therefore, are normally unaccounted for in the design phase. Many non - accidental failures along the structure service life due to material degradation, change in the boundary conditions and others can be avoided and/or controlled by means of appropriate Structural Health Monitoring (SHM). This is the case for failures or structural degradation that present warning signs long before collapsing, such as deflection, settlement, humidity, superficial erosion, cracks, among many others. In these cases, damage or collapse can be averted by following an appropriate SHM implementation complemented by an maintenance policy. The effectiveness of such monitoring procedures lies in their ability to instantly detect alterations on the structure's performance, warn the involved personnel and follow the damage progress allowing for its control and prevention of further damage. In addition, the maintenance program can be updated and improved based on the results of the monitoring. A faster response allows for better in - depth inspection, evaluation and, finally, determination of the course of action that minimizes the economic, social and environmental impact. For this reason, the contemporary trend in structural management is to supplement intermittent and periodic inspection with automated, continuous and real - time monitoring technologies. This trend is what mainly boosted SHM research during the last decades. According to Housner et al. [1], SHM can be understood as the continuous or regular measurement and analysis of key structural and environmental parameters under operating conditions, for the purpose of warning of abnormal states or accidents at an early stage. Moss and Mathews [2] and Mita [3] identified the cases where structural monitoring may be required:

- Validating modifications to an existing structure.
- Monitoring of structures affected by external works.
- Tracking long - term movement or degradation of materials in critical structures.
- Providing feedback loop to improve future design based on experience.
- Assessing fatigue.
- Checking novel systems of construction and new structural forms.
- Assessing post - earthquake structural integrity.
- Enhancing effectiveness of resources as construction declines and maintenance needs increase.
- Moving towards performance - based design philosophy.

## 1.1. SHM of tunnels

Tunnelling is on the increase around the world not only in terms of work volume but also considering that the demands of modern transport networks require longer and wider tunnels through increasingly difficult ground conditions [4]. Moreover, the increasing awareness of tunnels' sensitivity to seismic activity and their presence under densely populated areas require very high levels of safety. Therefore, SHM for tunnels appears to be particularly important.

Already in 1982, Dunnicliff [5] presented the conventionally required instrumentation for tunnel structural monitoring during construction and operation. Traditionally, safety assessment of tunnels and underground structures, existing or under construction, focuses on ensuring safety regarding two areas: the underground structure itself and its surroundings (mainly controlled through surface monitoring).

On the one hand, tunnel surroundings can experience changes in their geotechnical conditions that appear due to the construction of the tunnel itself (causing settlement or holes at ground level, affections on groundwater drainage, among others) or due to external effects (such as new ground level constructions or excessive rain periods). These effects can be monitored by controlling pore pressure, earth pressure, deformation, superficial settlement, and all the factors characterizing the soil mechanics of the area. For that, a wide range of instrumentation is available: piezometers, observation wells, vibrating - wires, inclinometers, extensometers, single point monuments, heave and strain gauges, among many others.

On the other hand, the tunnel will be subject to stress state variations both when it is being constructed and once completed due to external actions. Monitoring of the structural state of the tunnel usually consists of levelling measurements of particular points of the tunnel or convergence measurements of the contour. This is usually achieved by means of optical or mechanical technologies such as total station surveys or extensometric wires [6]. The former involves laser theodolites that allow for the acquisition of 3D scanned data on tunnel geometry and usually focus on deformation measurement or feature extraction enabling a full characterization of any variation [7]. The latter are invar wires connected to opposite sides of the tunnel section at its internal surface allowing for the measurement of their elongation/compression with a 0.1mm resolution [8,9]. Besides the aforementioned complex sensors, some local tunnel monitoring tools are: extensometers, commonly used to punctually monitor the settlement of structures or displacements between substructures (for example, consecutive concrete lining segments), crackmeters or fissurometers, used to observe the time - related development of cracks (if these are present) and inclinometers used to monitor angular inclinations of the tunnel inner surfaces.

## 1.2. Issues of the conventional SHM technologies

As stated in [10], conventional forms of inspection and monitoring are only as good as their ability to uncover potential issues in a timely manner. Therefore, the conventional SHM technologies present significant drawbacks.

One of the major difficulties with SHM technologies is managing the large volumes of data that the installed sensor scheme generates. Meanwhile, visual inspections and evaluations are obviously insufficient regarding the determination of the infrastructure's structural condition.

Another major drawback is that the mentioned monitoring schemes require, in general, the interruption of the infrastructure's service or the ongoing construction/maintenance works, given their time - consuming installation process, their strict installation requirements and their significant spatial occupancy. Regarding the measurements execution, it is worth noting that some of the conventional technologies to monitor in a global and not local way the tunnel performance (total station surveys and/or laser theodolites) do not involve an automated real - time measuring tool, i.e. most require specific operations/deployments every time a measurement is to be taken.

The last significant drawback is that the majority of sensing tools developed and proven to be reliable so far provide only localized measures specifically where the sensors are deployed. This implies that large amounts of sensors have to be installed in order to provide a global overview of the structure's condition which translates into increasing costs and complex data management. On another note, current sensing techniques that provide global monitoring fail to localize the damaged zone. In conclusion, technological innovations regarding monitoring techniques able to assess both the local and global structural performance are of interest.

## 1.3. Latest innovations in SHM sensors

The use of Fiber Optic Sensors (FOS), Global Positioning Systems (GPS), radars, MicroElectroMechanical Systems (MEMS) and Image Processing Techniques has opened doors to the extraction of structural information that could not be acquired before [11]. Regarding tunnel convergence monitoring in particular, several innovations have arisen in the last years ([12] ,[13]).

The need for technology development and automated structural data treatment to enable continuous and real - time structural monitoring with easy integrity assessment (enabling the conception of 'smart structures', [14]) is what encourages this research. Therefore, this paper focuses on the subject of Distributed Optical Fiber Sensors (DOFS) and studies a real application on a tunnel.

## 2. Optical Fiber Sensors

The first reference to Optical Fiber Sensors (OFS) dates back to the first half of the twentieth century regarding flexible endoscopes and boosting innovation in the medicine field [15]. After that, the development of long distance telecommunications technologies in the eighties allowed for the exponential growth of this technology from which a significant variety of sensing applications started being derived and to which we owe the modern age low - loss optical fibers [16].

Many sensor types can be embedded or attached to the structure, but only those based on fiber technology allow for integrated, quasi - distributed or distributed measurements on or inside the structure and along extensive lengths [17]. Their main characteristics when compared to traditional monitoring instruments are their reduced dimensions that allow for easy integration in structural components, their immunity from electromagnetic influences and corrosion processes which significantly widens their applicability, their ability to form sensor chains using a single fiber allowing for distributed sensing and their rapid data transmission enabling real - time monitoring ([18], [19] ,[20]).

## 2.1. Basics of OFS

The fundamental principle behind OFS is the propagation of light through a medium. This medium, in the case of OFS, is a cable of optical fiber whose main components are the core and the cladding. Figure 1a displays the common structure and shows how the core, with a diameter of 5 - 10 μ m, is embedded in the cladding.

Optical fibers are usually made from silica (SiO2) and they are protected by a polymer - type material coating. The light travelling through the core is usually a monochromatic laser and it is guided through the core thanks to internal reflection. When light is travelling in the optically dense medium that is the core and strikes a boundary at a particular angle (larger than the critical angle of the boundary), the light experiences total internal reflection and is, therefore, confined in the core (see Figure 1b).

Figure 1. Optical fibers a) Typical parts: 1. Core (5 - 10 μ m), 2. Cladding (125 μ m) and 3. Buffer or coating(250 - 900 μ m) and b) Light guiding and total internal refraction in a multi - modal optical fiber (from [21])

<!-- image -->

Engineering drawing

In the previously described process, attenuation is the key property of an optical fiber that affects light transmission. As stated in [16], [20] and [22], when an optical fiber is used for communication applications, attenuation has to be minimized to provide reliable signal transmission or reception. However, when used as a sensor, attenuation has to be exploited to allow for the accurate reproduction of the external perturbations the fiber is exposed to.

## 2.2. Classification of OFS

According to [16] and [23], OFS can be categorized into three different groups: grating - based sensors, interferometric sensors and distributed sensors.

Interferometric fiber sensors use the interference between two light shafts that have propagated through different optical paths of a single fiber or two different fibers [24]. They can be used to measure many parameters including temperature, strain and distributed disturbance [25]. Grating - based sensors rely on periodic changes of refractive index of the fiber, thus being able to encode the measurand into wavelength ([26] and [27]).

Most OFSs, such as Fiber Bragg Grating sensors (FBG) [28] or Fabry - Perot sensors [19], are discrete and can only provide local measurements. Discrete short - gauge sensors provide useful and interesting data regarding local behaviour but might omit important information in structural areas that are not explicitly instrumented (Figure 2).

Figure 2. Spatial distribution detection of cracks with a) point OFS and b) distributed OFS (from [29])

<!-- image -->

Engineering drawing

To understand the global behaviour of a structure by means of discrete sensors, a high number of sensors would have to be installed producing a dense network of monitored points with complex data acquisition and an excessive amount of wiring and measuring devices.

To deal with the mentioned limitations, optical fiber monitoring has been exploited to develop the last group of sensors, the Distributed Optical Fiber Sensors (DOFS), which are the focus of the present work. It is worth noticing that distributed sensing can also be achieved with quasi - distributed FBG sensors centring several FBG sensors at different wavelengths through a technique named Wavelength Division Multiplexing (WDM), and composing a FBG group in the same optical fiber [11]. However, this technique allows for measurement of a finite number of locations along the fiber path, WDM allows for approximately 100 gratings to be multiplexed [16]. This quasi - distributed sensing technique is the most widely used in SHM projects and has been repeatedly applied in civil infrastructure monitoring projects, mostly in concrete bridges [30].

## 2.3. Distributed Optical Fiber Sensors

DOFS have the same advantageous characteristics as the rest of OFS but with the added value of distributed monitoring of strain and temperature variations along the entire length. Additionally, this type of sensors only requires a single cable connection to the reading device [16]. Light scattering is the basis of these sensors. Scattering can be understood as the light interaction with the optical fiber and it occurs when the optical properties of the core are modified at the arrival of the light wave. When an electromagnetic wave is projected into an optical fiber its propagation thorough the core medium interacts with the present particles and it can either generate a second electromagnetic wave (scattering) or return towards the light source (backscattering). The latter is the one used to acquire information regarding changes in the structure.

Minimal fiber modifications can generate different light scattering processes depending on the interaction mechanisms between the propagating light pulse and the optical fiber [22]. The scattered spectral components include Raman, Brillouin and Rayleigh peaks. In Barrias et al [16] a summary can be found of several sensing technologies based on DOFS and including the FBG quasi - distributed technique for comparison.

The first reflectometry technique to emerge and allow for truly distributed and continuous monitoring was the Optical Time - Domain Reflectometer (OTDR). It is a technique that involves the launching of a short optical pulse into a fiber and processing the amount of backscattered light through a photo detector as the light shaft propagates along the fiber [16]. By measuring the variations of intensity of the Rayleigh backscatter, it can obtain the spatial variations experienced by the fiber. This technique is characterized by a low spatial resolution of approximately 1m, which limits its applicability to SHM. Since increasing the spatial resolution implies lowering the pulse width and, consequently, reducing the detected backscatter, a balance needs to be found between spatial resolution and sensing range to optimize the performance of each deployment.

The Brillouin Optical Time Domain Reflectometer (BOTDR) is based on the spontaneous Brillouin scatter while the Brillouin Optical Time Domain Analysis (BOTDA) on the stimulated. An example of application in the monitoring of a tunnel lining is available in [31]. In the frequency domain, also the BOFDA (Brillouin Optical Frequency Domain Analysis) is available for long range applications [32]. Even though Brillouin - based techniques are the most widely used in SHM deployments, their applicability is limited by their low spatial resolution. Recently, the newly developed Pulse - Prepump Brillouin Optical Time Domain Analysis (PPP - BOTDA) sensing technique greatly improved the spatial resolution (10 cm) [33].

The system that answers to the high spatial resolution demands, of millimetre scale, is the Optical Frequency Domain Reflectometry (OFDR). These sensors are based on a tunable laser source (TLS) in which optical frequencies can be tuned linearly in time without any mode hops. A considerable reduction of the backscatter signal is obtained. This requires an increased receiver bandwidth to be detected. It is worth mentioning that the requirements that high spatial resolution implies result in high cost technologies, such as the Optical Backscatter Reflectometer (OBR). The OBR is based on the detection of the spectral shift that the backscatter pattern presents when the fiber is subject to external stimulus, and it can later be used to calculate the strain variations along the fiber. The OBR technique, which is the one used in the presented case study, provides a good balance between cost and efficiency, granting spatial resolutions around 1 mm. at the expense of lower sensing range [34]. Applications of this technique to buried pipelines and concrete culverts are presented in [35 - 37]

## 2.4. DOFS applied in tunnels

In urban environments with dense edification and complex underground networks, it is inevitable for existing and new tunnels to affect or be affected by new underground or ground level constructions. Tunnel monitoring by means of DOFS has been deployed equally in structures during construction works and under operation.

During the construction of the large Crossrail platform tunnel in London, the Royal Mail tunnel was found in the surrounding alterable area being located directly above the soon - to - be constructed tunnel line at Liverpool Street Station [38]. In this case, Brillouin Optical Backscatter Reflectometry (BOTDR) was used. The innovative monitoring technique was complemented by the installation of an Automated Total Station with the aim of comparing their respective readings. The corrected strain readings, after temperature compensation, showed a clear strain profile that matched the conventional displacement measurements of the Total Station and clearly revealed the crown settlement and the tunnel's flexible behaviour as most of the measured strains were recovered after the tunnelling face had advanced away from the measuring point.

Another successful deployment of DOFS was performed in the Shinkansen tunnel [39]. Following a laboratory experiment regarding the monitoring of concrete lining segments by means of DOFS and Electric conductible paint, a field experiment was executed in the mentioned tunnel to assess the performance of such sensors in real world conditions. The experiment took place over approximately three years. The long - term applicability of DOFS using the BOTDR technique was proven, stating in the paper's conclusions that the utilised method had sufficient applicability for damage surveillance of tunnel linings.

The aforementioned SHM deployments involved already constructed tunnels affected or not by external actions with sensors bonded to the inner structural surface. However, structural assessment is also needed during construction, an example of which is presented in [40]. The article analyses real measurements performed on a highway tunnel in Žilina (Slovakia) by means of DOFS within a period of 5 months covering the whole process of building a new tunnel. The soil conditions already indicated that there would be issues related to excavation progress and unstable overburden of the structure and, for that, the construction company required the monitoring of load changes over time. The tunnel was excavated using the New Austrian Tunnelling Method (NATM). The optical fiber was placed on two iron bars of the braced girder of the tunnel, which became a part of the primary lining after being sprayed with concrete. The installed distributed sensors were based on Brillouin scattering (BOTDR).

## 2.5. Summary of DOFS advantages and limitations

After the presentation of diverse laboratory real applications of DOFS, it is clear that they present numerous benefits, making them one of the best options to deploy adequate SHM. Indeed, they could be considered as the latest upgrade of the optical fiber sensing field.

A list summarizing the advantages and limitations of such sensors is presented below. Advantages:

- Reduced dimensions , which ease bonding and embedment on structural elements and improve the reproduction of structural behaviour.
- Easy installation process. All that is required is cleaning the structure's surface and bonding the fiber to it by means of an adhesive.
- Lower installation and maintenance costs than other sensors.
- Accurate readings and high sensitivity.
- Distributed monitoring . They allow for 1 - D continuous monitoring as opposed to local measurements easing the deformation interpretation and the damage pinpointing processes.

- Wide range of applicability to all kind of continuous structural surfaces subject to damage in civil, structural and aerospace engineering.
- Immunity to, and reliability under, electromagnetic influences and aggressive environments. The readings only depend on strain and temperature, and the latter can be adjusted through compensation.
- Rapid data collection and transmission.

## Limitations:

- Cost . They require a high initial investment regarding software, monitoring devices and optical fiber sensors.
- It is a new technology that is still undergoing research , resulting in the absence of standardized guidelines on how to ensure success in every deployment.
- Appearance of anomalies in the DOFS measurements when high gradients of strain are present and depending on the bonding agent used [41].
- Lack of completely reliable DOFS/structural support bonding technique.

## 3. Case study: DOFS installation in concrete lining of L - 9 tunnel

The city of Barcelona has, in recent years, faced several problematic situations regarding underground infrastructure. The fatidic ground collapse in the Carmel neighbourhood in January 2005 due to the TMB metro line L - 5 extension marked a turning point in public infrastructure execution. Since then, all construction works and projects taking place in the metropolitan area of Barcelona are subject to stricter and more exhaustive inspection protocols for which in - depth structural justifications, geological studies and monitoring protocols have to be prepared ensuring safety of the construction site and its surroundings.

The subject of this paper is a building constructed in the Bon Pastor neighbourhood of Barcelona. It is no exception to the aforementioned safety regulations, especially considering that its extension partially covers the TMB L - 9 metro tunnel layout.

## 3.1. Project description

The building under construction is located between Novelles, Tallada and Sant Adrià streets, forming an angle of approximately 60º with the 4 th section of the L9 Metro Sagrera TAV - Gorg tunnel's layout. As can be seen in Figure 3, the South - East corner of the building extends over the tunnel's layout.

Figure 3. Building site location (red), TMB L9 layout and access station Bon Pastor

<!-- image -->

Geographical map

The TMB L - 9 is a 47.8km long (43.71km of which underground) automated (driverless) metro line aimed at connecting the perimetral metropolitan areas of el Prat de LLobregat, l'Hospitalet de Llobregat, Badalona and Santa Coloma de Gramenet to the metro service of Barcelona [42].

The tunnel structure was executed by means of a Tunnel Boring Machine with an Earth Pressure Balanced shield type to ensure operability in soft soil [43] and, as the perforation proceeds the 35cm thick tunnel ring is executed resulting into an 11.60m diameter tunnel that enables the construction of the stations and auxiliary installations in the tunnel itself. Such vast diameter allows for the trains to run at two levels, i.e. one above the other, separated by a supplementary slab (see Figure 4).

The new building, located slightly above the L - 9 tunnel layout is a residential building composed of a basement floor (to be used as parking space), the ground floor and four floors above it rising up to approximately 18.10m above ground level. As can be seen in Figure 4 and Figure 5, the building site's dimensions are approximately 83x20m (1660m 2 ) of which roughly 37m 2 can be found right above the L9 tunnel section covering, at the most critical location, half of the tunnel layout.

An approximate total soil volume of 6500m 3 is removed during the excavation works in order to execute the foundations. The lowest point of the building structure, i.e. lower surface of 80cm thick concrete foundation slab, is at - 3.90m. With the highest point of the underground tunnel being - 18.30m, there is a soil layer approximately 14.40m thick separating the structures.

Figure 4. Schematic cross section of L9 tunnel in relation to the building

<!-- image -->

Engineering drawing

Figure 5. Schematic plan view of L9 tunnel in relation to the building

<!-- image -->

Engineering drawing

The construction site is divided into three areas of execution and the corresponding joint numbers seen in Figure 5 are a reference to the constructive order of the structure. Joint 1, the closest to the tunnel layout, is the most advanced section of the building in terms of constructed surface during the whole project length. The reasons behind the joint construction order are safety - related in an attempt to diminish the possibility of any adverse effects if the deformation and tension tolerancies are exceeded in the underground structure at some point during the construction period.

The 20m long measurement along the tunnel axis in Figure 5 is aimed at determining the possibly affected section of the underground structure, i.e. tunnel length to be monitored and controlled during construction.

The main actions in the design of tunnel linings are the geo - static loads caused by ground - structure interaction, the traffic actions that result from operation within the tunnel or external effects such as nearby traffic or construction works. During construction, the thrust jacking loads imposed by the boring machine and the secondary grouting loads should also be considered. In the present case, the effect of nearby construction was of interest since it produced a change of the stress state on the whole lining in the affected area. The deployment of the DOFS allowed a complete control to be taken of the deformation of the section tunnel, as well as calculation of the development of stresses in the structural elements of the monitored section.

## 3.2. Monitoring set - up and sensor installation

The presented monitoring scheme involves the installation of a DOFS with a 1 cm spatial resolution bonded to the inner structure of the tunnel to reproduce the strains experienced by the tunnel concrete lining due to the unloading / loading processes happening 14.40m above. The geometry of such monitoring scheme is presented in Figure 6.

Figure 6. 3 - D representation of the DOFS monitoring scheme

<!-- image -->

Engineering drawing

In Figure 6, the optical fiber is presented in red and the numerical values around it are a reference to the distance between the indicated point and the beginning of the fiber, i.e. the monitoring device's location. The catalogued discontinuities are presented in orange, refering to points in which the bonding of the fiber to the concrete surface is not guaranteed. This is mainly due to low accessibility. These discontinuities are usually found in corners and joints, under rails and behind pipes, preventing the required attachment to the structure from being executed, thereby compromising the quality and reliability of the readings in that point.

Locating the DOFS forming a perpendicular plane to the tunnel axis and right under the South - East corner of the building, as seen in Figure 7, appears to be the most logical distribution. The reasons behind this are that the critical section, i.e. the one expected to suffer larger effects, is completely monitored and, also, since all measured points belong to the same plane, the strain profile of the structure is easier to interpret.

Figure 7. Plan view of DOFS location with respect to the building site

<!-- image -->

Engineering drawing

The chosen optical fiber length is 50m, which allows for further monitoring length than just the approximately 30m long inner perimeter of the track 2 section. For that, it was decided to bond the fiber in parallel to the tunnel axis along the side that corresponds to the building for the next 8.71m of fiber. Finally, the fiber begins to cover another section and, for the last 8m before the connection to the acquisition device, it remains unbonded (see Figure 6).

## 3.2.1. DOFS installation

In order to ensure the fiber's good performance, it has to be appropriately bonded to the structure. The usual procedure implies a delicate preparation of the concrete surface as described in [22] and [29]. The entire fiber length is temporarily fixed to its position by means of tape dots. This is later covered by a thin layer of epoxy resin that bonds it definitively to the concrete lining (see Figure 8a).

Additional protective measures need to be applied to avoid possible damage. In the case study, duct tape was applied along the whole length of the fiber and additional protective measures were taken regarding the floor and the fiber discontinuities, due to the presence of punctual non - bonded segments in which physical integrity can be easily compromised (see Figure 8b).

<!-- image -->

Photograph

a)

Figure 8. Fiber installation pictures a) bonding of fiber to concrete surface using epoxy resin, b) protection of the fiber in a discontinuity with bubble wrap and duct tape

Figure 9 presents the optical fiber installation overview right next to the guiding orange line; the measuring device can be identified in the box on the right wall of the tunnel. The fiber protective layers are observed as well in the upper surface of the slab and going under the rails.

Figure 9. Tunnel monitored section

<!-- image -->

Engineering drawing

Some detailed pictures of the fiber deployment are presented in Figure 10.

Figure 10. Selection of pictures from the installed DOFS in the tunnel

<!-- image -->

Photograph

1. Initial point of the fiber.
2. Under the rail.
3. Corner: horizontal slab and tunnel ring
4. Tunnel's concrete structure and catenary ~5m above slab (notice clear joints).
5. Tubes and pipes.
6. Corner where the optical fiber changes from transversal monitoring of the vault to longitudinal monitoring of the tunnel.
7. Detail of fiber going through a joint.
8. Top of the 2 nd transversal section.
9. Monitoring equipment.

As can be seen in the figures, several points of the fiber are subject to bonding discontinuities. Since these points are not physically bonded to any surface, the readings performed on them are rather anomalous and should be properly interpreted in the data post - processing.

The long - term performance of the sensor depends not only on the manufacturing process and quality control, but is also greatly affected by an appropriate quality control during deployment and protection measures against environmental conditions and other unexpected factors. In tunnels that are not exposed to aggressive environments, the effect of aging due to environmental attack is not significant for the OBR system. The OBR system, carefully installed, could be a virtually maintenance - free sensor system. Specifically, in the present case, three times the fiber has been inspected without detecting any damage in the fiber or the coating. The system is correctly working after almost 2 years in service.

## 3.3. Construction timeline and monitoring period

The excavation works started in the 8 th October 2018 and in mid - November the ground excavation was finished, starting the construction works in a sequence defined in Figure 11.

Figure 11. Construction time - line

<!-- image -->

Box plot

All works start being executed in the area corresponding to joint 1 (the one located right above the tunnel layout). Given that the excavation is one of the main actions applied to the tunnel, it is interesting to refill that 'void' by constructing firstly over joint 1 to oppose the decompressive action of the excavation. Note as well that there is significantly low construction activity in joints 2 and 3 during the period from 19 th February to 18 th March, which will be reflected in the readings in the form of a reduction in the strain evolution slope.

It is important to mention that the time interval between the execution of construction work, i.e. an action being applied on the soil, and the perception of a response in the strain readings can be quite long. Indeed, we are talking about a 14.4m thick clay soil layer separating the building foundations and the tunnel concrete lining. This translates into a long consolidation period before the load is transferred to the tunnel structure.

The monitoring periods are defined with the aim of covering the main construction periods separately: excavation, foundation, execution of ground floor, first floor, etc. The monitoring intervals are presented below:

- From 4 th October to 7 th October: every 30 minutes.
- From 18 th October to 7 th November: every 6 hours.
- 13 th December: 2 measurements separated by 30 minutes .
- 24 th January: 2 measurements separated by 30 minutes.
- From 21 st February to 25 th March: every 15 minutes.
- From 16 th April to 17 th April: every 30 minutes .
- 17 th May: 5 measurements separated by 10 minutes .

## - From 16 th July to 6 th August: every 30 minutes .

As seen, the monitoring was not continuous due to reading failures resulting from voltage dips and direct disconnection from the electricity grid due to maintenance procedures in the tunnel. Since no wireless connection could be provided at the time (that particular metro line segment does not yet include optical fiber network), physical access is the only remaining option to check the measuring instruments and download the recorded data. However, this alternative is complicated given that the location of the monitoring section is in a metro tunnel. The accessing personnel have to withstand schedule restrictions, making night - time (from 2am to 5am, when the trains are not running) the only available time interval for access. Other factors, like ongoing maintenance operations in the tunnel and access protocols and restrictions established by the metro authority do not facilitate the procedures either.

## 3.4. Data collection: results and discussion

The strains were monitored through a 50m long DOF sensor (bonded to the concrete surface) by means of an OBR ODiSI - A ( O ptical Di stributed S ensor I nterrogator) manufactured by LUNA Technologies [44]. The ODiSI uses swept - wavelength coherent interferometry to measure temperature and strain. The spatial resolution selected for this case study is 10mm and the time interval between measurements depends on the monitoring period (see previous section).

The post - processed data results on strain measurements along the whole length of the fiber with a resolution of 1cm and for every corresponding time are presented in Figure 12.

Figure 12. Graphical representation of results obtained during all monitoring times

<!-- image -->

Engineering drawing

At the beginning of monitoring, the concrete lining segments are under compression. Therefore, all the compressive or tensile effects in the monitoring results represent the variations applied to the initial state. This means that, when the model presents tensile stresses it does not imply that the concrete lining segment is working in tension, but rather that it is being slightly decompressed.

Given that the inner fiber of the tunnel concrete lining is being monitored, it can be expected that when unloaded (excavation) this fiber will experience compression and, when it is loaded, tension. This is because the loading/unloading effect is not a uniform pressure around the whole ring. Therefore, the concrete lining is affected by bending, creating tension in the inner part when the external load is downwards. Therefore, the strain evolution in time will have a negative slope for as long as the soil surrounding the underground structure is transmitting the excavation effects to it. After that, the strain - readings should reach a maximum compressive state and start reproducing the effect of the construction works by adopting a positive slope representing decompression.

Figure 12 may seem ideal in terms of its texture and clarity; however, it is worth mentioning that it is a result of the application of complex data treatment algorithms to the raw strain readings. As stated by Bado et al. [41,45], DOFS are currently prevented from becoming a reliable universal strain - reading method for the following reasons: there is no reliable sensor/structure bonding technique and, also, the appearance of anomalies in the measurements in the form of abnormally high peaks that distort the strain profiles. Because of these limitations, the raw data set presented a significant number of anomalous readings which were mostly identified and analysed.

## 3.4.1 Simplified numerical model

For appropriate visualization of the different effects of the building construction along the tunnel, two simple theoretical 2 - D models are developed with GiD Software [46] based on Finite Element Method (FEM).

The model results of the excavation period are presented in Figure 13a. A positive vertical load of approximately 85kN/m 2 (from assuming an excavation depth of 4.7m and a soil specific weight of 18kN/m 3 ) is applied on the right half of the simulated ground surface replicating the soil removal process. The tunnel cross section is stretched towards the right side (where the building is located). The red/yellow areas represent tensile stresses while the blue/green ones represent compressive stresses (Figure 13b).

<!-- image -->

Engineering drawing

a)

Figure 13. Unloading / excavation model a) general view and b) tunnel view with fiber coordinates

Analysing Figure 13b it can be concluded that the excavation of the building foundation affects the marked areas differently, as explained below.

1. Segment 50 - 40m (concrete slab): The slab works as a diaphragm experiencing compression which is logical given the upwards deformation of the section.
2. Segments 40 - 39m and 24 - 23m (concrete lining close to the slab): The yellow colouring denotes a range of low tensile stresses. However, these segments belong to transitional areas between the tunnel concrete lining and the slab and, consequently, the corresponding strain - readings might behave in particular ways.
3. Segment 33 - 38m : This area is clearly experiencing more tensile stresses than any other, which implies that the corresponding measurements should be the least compressed ones.
4. Segment 32 - 27m : Together with the slab, this area should present measurements that are more compressed than the other areas.
5. Segment 26 - 24m : This section is clearly in tension, but less than segment 3. Therefore, strains between the ones observed in segment 3 and those in segment 4 should be observed along this segment.

Figure 14a presents the theoretical model results due to building construction. Assuming the foundation slab of 0.8m depth, a concrete slab of 0.3m on each floor, approximated dead loads are applied. The effects of the construction on the tunnel lining are detailed in Figure 14b. The tunnel cross section is obliquely flattened, generating the opposite stresses from those observed in the previous model.

Figure 14. Loading model a) general view and b) tunnel view with fiber coordinates

<!-- image -->

Engineering drawing

Having this basic structural analysis in mind, the interpretation of the strain - readings provided by the DOFS will be easier to perform.

## 3.4.2. Experimental results of the section and reference points

The global overview of the post - processed strain measurements is presented in Figure 12. As can be observed, the initial measurements are green corresponding to null or very small strain variations, which is logical given that those correspond to the monitoring period right before the start of the excavation works. Later, the tendency is towards negative strain values, which means compression and is coherent given the nature of the constructive event that is excavation, i.e. unloading of the structure. After reaching a minimum of approximately - 260 με in the most critical location and around February, the strain profile slope is inverted reproducing a decompression process as the negative strains are being reduced in absolute value. At first glance, the measured strain profiles coincide with the theoretical ones obtained in the structural analysis.

A plan view of Figure 12 is presented in Figure 15 and is used to provide a global visualization of the segments that present different structural effects along the 50m fiber.

Figure 15. Plan view of strain evolution at all times and locations

<!-- image -->

Line chart

As can be observed, the five differentiable behaviours in Figure 15 correspond to the fiber lengths covering the five different substructures presented in Figure 6: 0 - 9m (unbonded fiber segment), 9 - 14m (partial sectional monitoring segment), 14 - 23m (longitudinal tunnel segment), 23 - 40m (complete tunnel transversal section segment) and 40 - 50m (upper fiber of the slab).

## 1. 0 - 9m (unbonded segment, Figure 16)

Figure 16. Strain evolution in 0 - 9m segment

<!-- image -->

Other

The unbonded fiber segments do not provide strain measurements per se but reproduce instead the effects of temperature variations on the measurements. Data collected from these segments can be useful in the case of long - term monitoring campaigns where compensation in the strain readings is mandatory due to important temperature variation [47]. In this case, considering that the location of the fiber is a metro tunnel at 14m underground with no affections from the outside weather conditions, it can be concluded that the temperature variations during the monitoring period are negligible.

However, some strain oscillations are observed in the unbonded segment (Figure 16) remaining constant along the 9m length, which induces the thought of actual displacements occurring between locations 0m and 9m. This segment is not bonded to the structure with epoxy resin but it is attached to it with duct tape for protective reasons. Therefore, the readings can end up presenting variations due to minor relative displacements between the extreme points of this segment that can be roughly computed as: 50µ𝜀 ൉ 9𝑚 ൌ 450 ൉ 10 ି଺ 𝑚 ൌ 0.45𝑚𝑚

## 2. 9 - 14m (partial sectional monitoring segment, Figure 17)

Figure 17. Strain evolution in 9 - 14m segment

<!-- image -->

Other

This segment corresponds to the fiber length covering a small portion of a tunnel transversal section. Only the first 3m of the tunnel vault are covered (see Figure 6). It is interesting to see that the covered length shows a similar strain profile as the one observed in the first five meters (23 to 28) of the completely covered half - section (23 - 40m). This can be easily observed by comparing segments 2 and 4 of Figure 15 as facilitated in Figure 18.

Figure 18. Strain readings comparison of segments 2 and 4

<!-- image -->

Engineering drawing

Also, the maximum compressive strains (around - 100 μ strains) are much less than the ones measured in the complete section (23 - 40m segment) as this one is 10m away from the critically loaded section.

## 3. 14 - 23m (longitudinal tunnel segment, Figure 19)

Figure 19. Strain evolution in 14 - 23m segment

<!-- image -->

Line chart

In this 9m long fiber segment, two clearly differentiable processes are happening. Up to fiber length 18.5m a significant compressive process is observed, whereas in the surroundings of fiber length 20m the compression is not so considerable. As can be seen in the tunnel plan view (Figure 20a), this might be because of the presence of several cracks in the first half of this segment weakening it. However, it is important to have in mind that the readings in this segment were particularly affected by anomalous behaviour due to the amount of discontinuities the fiber setup was subject to (mainly joints between the concrete lining segments as seen in Figure 20b).

Figure 20. 14 - 26m segment setup with a) detail of tunnel plan view and b) site pictures of discontinuities

<!-- image -->

Line chart

## 4. 23 - 40m (half - tunnel transversal section segment, Figure 21)

Figure 21. Strain evolution in 23 - 40m segment

<!-- image -->

Other

The readings of this segment should reproduce the observed theoretical behaviour on the tunnel's vault. Since the last reading was executed on the 6 th August, the measurements profile does not get to fully reproduce the deformations caused by the ground level loading. It can be seen, however, how the compression starts diminishing and strains start getting lower (in absolute value) in the middle of the graph (end of January) which means that there is tension in the lower concrete lining fiber and that the effects of the loading works (construction) start compensating the unloading operations (excavation).

## 5. 40 - 50m (slab segment, Figure 22)

Figure 22. Strain evolution in 40 - 50m segment

<!-- image -->

Other

This is clearly the area with the highest compressive strains (darker blue). This behaviour is logical given the upwards stretching of the tunnel cross section. As can be seen, the strain profiles in the last 2.5m of the fiber are significantly affected by peaks, which were not possible to remove during the data post - processing. However, with the punctual nature of the high values and considering that the location of the last segment is a passable area with a surface that is not particularly smooth, the appearance of peaks and distorted profiles can be explained without implying structural damage.

## Representative points

The effect of the different construction works on the tunnel concrete lining can be observed by means of the so - called representative points. Conclusions regarding the structural behaviour of the tunnel lining can be easily extracted and understood from the particular points presented in Figure 23.

Figure 23. Representative points in the tunnel cross section and the theoretical model

<!-- image -->

Engineering drawing

In order to check the accuracy of the strain readings, Figure 24 and Figure 25 have been developed showing the strain evolution of the representative points during the whole monitoring period (from 4 th October 2018 to 6 th August 2019).

It is interesting to present both diagrams to show the difference between the original and post - processed data and to prove that, looking back to the original readings, post - processing is both helpful and necessary. The mean relative error between the raw sensor measurements and the post - processed data is 9.7 με . This value includes all the anomalous readings, without distinguishing their origin: irregular concrete surface and presence of joints and corners where bonding is prevented, noise due to train circulation, data acquisition failure due to maintenance works or power outages, etc. Despite these inconveniences, the mean relative error still presents a relatively small magnitude, which translates into a confirmation of the sensor's high accuracy.

Figure 24. Strain evolution of representative points (Figure 23) from 4th October 2018 to 6th August 2019 (original)

<!-- image -->

Line chart

Figure 25. Strain evolution of representative points (Figure 23) from 4th October 2018 to 6th August 2019 (post - processed)

<!-- image -->

Line chart

The initial measures (between 4 th and 7 th October, before the excavation works started) were conducted with small time intervals between them (30 minutes maximum) and, considering the metro traffic frequency of 10 minutes, it is logical that the point profiles present irregularities in those times, even being representative points specially selected.

Later on, the monitoring period that covers the excavation works (between 7 th October and 9 th November), presents a strong increase of the compressive strains (downwards) clearly reproducing the unloading effects. These effects are observed during the succeeding monitoring episodes on the 13 th December and 24 th January.

The following measures, taken between the 21 st February and 25 th March, already present the compensating effects of construction works, i.e. decompression of the inner surface. The real compression maximum is found close to the 24 th January marking approximately two and a half months between the end of excavation works and their final effects on the tunnel. This aspect points out the previously commented soil consolidation and loads redistribution effects.

The construction works that cause the observed change of tendency start around the end of December with the foundation slab in joint 1, completed on the 20 th December and followed by the one in joint 2, finished by the 10 th January. By the beginning of March, the ground floor slabs of joints 1 and 2 were already executed as well as the walls and pillars of the first floor in joint 1 and the foundation slab in joint 3. Therefore, significant works had been executed preceding the March monitoring period, clearly enough to compensate for the excavation unloading and to start decompressing the lower fiber of the tunnel lining.

At the end of March, a reduction in the strain decompression slope can be appreciated, which, after some thought process regarding the timeline of works, was possible to explain as follows. As mentioned in the construction timeline, the works present at all times advanced development in joint 1 (the one above the tunnel) compared to the other two, with an advantage of 1 floor with respect to joint 2 and two with respect to joint 3. The works in joint 3 started around the end of February, from this it can be deduced that the loading of the further area from the tunnel layout slightly unloaded the soil corresponding to joint 1 by inducing a balanced sort of behaviour between joint 1 and 3, explaining the decompressing profile slope reduction.

The tendency observed after 16 th April and 17 th May monitoring episodes is still of decompression being the zero - axis overcome during the first half of July, meaning that the inner surface of the structure starts being in tension as the theoretical model predicts.

The evolution of each representative point shown in Figure 24 and Figure 25 is as follows:

- Point 45 is in the slab segment and presents the highest compressive state as was expected since the slab is supposed to work in compression during the unloading phase. Later, the

- loading process affects this section as it becomes the most tensioned point, clearly reproducing the tensional state's inversion.
- Point 40 is the second most compressed point, which makes sense given its location in the left - hand side corner, really close to the slab but located on the concrete lining surface, which, according to the model, is supposed to experience high compression as well but slightly less than the slab.
- Point 29 is located close to the keystone of the tunnel slightly to the right. It is the closest point to the application of loads and, since the tunnel section deforms towards the load application area, point 29 presents the second highest compressive state during the unloading phase. After the construction loads reach the tunnel, it becomes one of the most tensioned ones.

As can be seen, points 40 and 29 have similar strain evolutions, in fact, up to the 13 th December, point 29 is more compressed than point 40, which might be explained by the sequential loading of the tunnel, meaning that the loading processes get first to the upper concrete lining and later to the points below.

It is also noticeable that points 23, 25 and 32 present similar tendencies regarding their strain evolution which agrees with the similar colouring these segments present in the models, even while being located in different areas.

- Point 23 is located in the right hand side corner, roughly 50cm above the floor slab.
- Point 25 is located above point 23 and corresponds to a section with slightly higher traction (barely noticeable at determinate times) than 23. Even though it is located in the centre of what could be identified as the first quadrant of the tunnel cross section, the measured traction is not the highest.
- Point 32 is located in the second quadrant of the tunnel cross section really close to the keystone. It represents the beginning of the fiber segment that experiences higher tensile strains.

Finally the, red / dark blue area of the theoretical models is characterized by point 35.

- Point 35 belongs to the least compressed segment between lengths 33 and 38m of the fiber setup. Except for the initial measurements, the strain readings are the lowest in absolute value up to mid - June when the point becomes one of the most compressed.

## 4. Conclusions

The application of DOFS to the monitoring of a tunnel lining affected by nearby construction was presented showing a good performance of this novel technique in the monitoring of strain along the whole affected sections. In fact, the DOFS readings reproduce very accurately the tunnel deformation process. The tendencies observed by the sensors were forecasted by a simple theoretical model. The monitoring of the strain at many points in the critical section allowed us to conclude that the nearby construction only slightly affected the lining stresses and that safety was guaranteed during the whole monitored period.

Even though this paper does not describe the data post - processing in detail, it is important to note that complex algorithms were used to identify and substitute the anomalies that the raw set of data presented mainly due to failure of the fiber - concrete bonding technique, presence of geometrical discontinuities to overcome (corner, joints, etc) or errors produced by the sensor itself. The resulting data set allows for the interpretation of the global behaviour of the structure since it provides a very smooth surface of strain tendencies.

Given the lack of a continuous monitoring tool, i.e. nonstop readings during the whole construction process, the particular effects of each constructive step (for example, the conclusion of each floor), are very hard to appreciate in the strain profiles. Even the concreting works, understood as superficially distributed loads applied in a significantly reduced time interval and considered as the largest loading events, are difficult to observe in the strain profiles of each monitoring point.

However, the monitored segments that behaved differently due to the eccentric loading process matched the predicted distribution of strains.

As discussed, during the analysis, the structural response of the tunnel due to a determinate action at ground level can be monitored logically only after the soil consolidation period. This time interval can involve several months. In the case study, even if the excavation works were concluded around the 10 th December 2018, the unloading effects were still being detected in the readings (reproducing structural compression of the tunnel's inner surface) at the beginning of February 2019.

Despite their advantageous performance and reliability, DOFSs still constitute a recent technology and their reliability and accuracy when applied to real world structures is still under probation since there is still room for improvement and for widening their applicability. In general, standardized guidelines need to be developed to ensure success in every DOFSs deployment regarding fiber bonding to the structure, temperature affections on readings, post - processing of reading anomalies, among other factors. However, real applications, as in the one presented in this paper, show that DOFS are anticipated to have a very important role in Structural Health Management of tunnels in the near future if correctly understood and developed.

## Acknowledgments

We would like to thank COTCA and TMB respectively for providing access to the necessary data regarding the case study and supporting this research. We would also like to thank Ph D student Mattia F. Bado who provided insight that greatly assisted this research during the data post - processing phase. This research did not receive any specific grant from funding agencies in the public, commercial, or not - for - profit sectors.

## References

- [1] G. W. Housner, L. A. Bergman, T. K. Caughey, A. G. Chassiakos, R. O. Claus, S. F. Masri, et al. , 'Structural control: Past, present and future,' Journal of Engineering Mechanics , vol. 123, no. 9, pp. 897971, 1997. Available at: https://doi.org/10.1061/(ASCE)0733 - 9399(1997)123:9(897).
- [2] R. M. Moss and S. L. Matthews, 'In - service structural monitoring a state - of - the - art review,' The Structural Engineer , vol. 73, no. 2, pp. 23-31, 1995. Available at: https://www.istructe.org/journal/volumes/volume - 73 - (published - in - 1995)/issue - 2/in - service - structural - monitoring - a - state - of - the - ar/, accessed: 04 - Feb - 2020.
- [3] A. Mita, 'Emerging needs in Japan for health monitoring technologies in civil and building structures,' in 2nd International Workshop on Strutural Health Monitoring , Stanford University (Stanford, California, USA), Sept. 8 - 10, 1999. Available at: http://www.mita.sd.keio.ac.jp/publications/data/d199901.pdf , accessed: 04 - Feb - 2020.
- [4] K. Loupos, G. Kanellos, M. Bimpas, A. Amditis, O. Bursi, S. Frontistou, et al. , 'Fiber Sensors Based System For Tunnel Linings' Structural Health Monitoring',' in 2nd Conference On Smart Monitoring, Assessment And Rehabilitation Of Civil Structures , Istanbul Technical University (Istanbul, Turkey), Sept. 9 - 11, 2013. Available at: https://data.smar - conferences.org/SMAR\_2013\_Proceedings/html/index.html, accessed: 04 - Feb - 2020.
- [5] J. Dunnicliff, Geotechnical instrumentation for monitoring field performance . Wiley - Interscience, 1988. ISBN: 978 - 0471096146.
- [6] C. B. Barbosa, L. A. Ferreira, F. M. Araújo, L. Gonçalves, C. D. Gama, R. Malva, et al. , 'Fiber Bragg grating system for continuous large - scale monitoring of convergence in Rossio Tunnel,' in 20th International Conference on Optical Fibre Sensors , Heriot - Watt University (Edinburgh, United Kingdom), Oct. 5, 2009, vol. 7503. Available at: https://doi.org/10.1117/12.835420.
- [7] W. Wang, W. Zhao, L. Huang, V. Vimarlund and Z. Wang, 'Applications of terrestrial laser scanning for tunnels: a review,' Journal of Traffic and Transportation Engineering (English Edition) , vol. 1, no. 5, pp. 325-337, 2014. Available at: https://doi.org/10.1016/S2095 - 7564(15)30279 - 8.
- [8] A. Piccolo, Y. Lecieux, D. Leduc, F. Bumbieler, P. Teixeira and J. Zghondi, 'Tunnel convergence analysis by distributed optical fiber strain sensing with means of finite element - inverse analysis method,' in 9th European Workshop on Structural Health Monitoring , Hilton Manchester Deansgate (Manchester, United Kingdom), Jul. 10 - 13, 2018. Available at:

- https://www.ndt.net/search/docs.php3?showForm=off&amp;id=23335, accessed: 04 - Feb - 2020.
- [9] J. Yu, J. R. Standind, R. Vollum and D. Potts, 'Tunneling induced strains and deformations at Central Line,' in Crossrail Project: Infrastructure design and construction , ICE Publishing, 2015, pp. 499-518, ISBN: 978 - 0727760784. Available at: https://www.icevirtuallibrary.com/doi/abs/10.1680/cpid.60784.032, accessed: 09 - Feb - 2020.
- [10] M. Baker, 'Sensors power next - generation Structural Health Monitoring,' GISCafé Blogs . [Online]. Available at: https://www10.giscafe.com/blogs/gissusan/2014/02/21/sensors - power - next - generation - structural - health - monitoring - in - civil - engineering - applications/#, accessed: 09 - Feb - 2020.
- [11] G. Rodríguez Guitiérrez, 'Monitorización de estructuras de hormigón mediante sensores de fibra óptica distribuida,' Ph.D. Thesis, Universitat Politècnica de Catalunya, Departament d'Enginyeria Civil i Ambiental, 2017. Available at: http://hdl.handle.net/2117/112412, accessed: 06 - Feb - 2020.
- [12] S. Maddison, 'Structural Monitoring in Tunnels using a novel Wireless System,' Imperial Engineer , no. 20, pp. 18-20, 2014. Available at: https://www.imperial.ac.uk/media/imperial - college/faculty - of - engineering/public/imperial - engineer/ImperialEngineer20.pdf, accessed: 06 - Feb - 2020.
- [13] F. Ariznavarreta - Fernández, C. González - Palacio, A. Menéndez - Díaz and C. Ordoñez, 'Measurement system with angular encoders for continuous monitoring of tunnel convergence,' Tunnelling and Underground Space Technology , vol. 56, pp. 176-185, 2016. Available at: https://doi.org/10.1016/j.tust.2016.03.014.
- [14] D. Balageas, C. P. Fritzen and A. Güemes, 'Introduction to Structural Health Monitoring,' in Structural Health Monitoring , ISTE, 2006, ch. 1, ISBN: 978 - 0470612071. Available at: https://doi.org/10.1002/9780470612071.ch1.
- [15] E. Udd and W. B. Spillman Jr., Fiber Optic Sensors: An Introduction for Engineers and Scientists , 2nd ed. John Wiley &amp; Sons, 2011. ISBN: 978 - 0470126844.
- [16] A. Barrias, J. R. Casas and S. Villalba, 'A review of distributed optical fiber sensors for civil engineering applications,' Sensors , vol. 16, no. 5, 2016. Available at: https://doi.org/10.3390/s16050748.
- [17] J. M. López - Higuera, L. R. Cobo, A. Q. Incera and A. Cobo, 'Fiber optic sensors in structural health monitoring,' Journal of Lightwave Technology , vol. 29, no. 4, pp. 587-608, 2011. Available at: https://doi.org/10.1109/JLT.2011.2106479.
- [18] J. R. Casas and P. J. S. Cruz, 'Fiber Optic Sensors for Bridge Monitoring,' Journal of Bridge Engineering , vol. 8, no. 6, pp. 362-373, 2003. Available at: https://doi.org/10.1061/(asce)1084 - 0702(2003)8:6(362).
- [19] X. W. Ye, Y. H. Su and J. P. Han, 'Structural health monitoring of civil infrastructure using optical fiber sensing technology: A comprehensive review,' The Scientific World Journal , vol. 2014, 2014. Available at: https://doi.org/10.1155/2014/652329.
- [20] G. Rodriguez, J. R. Casas and S. Villalba, 'SHM by DOFS in civil engineering: a review,' Structural Monitoring and Maintenance , vol. 2, no. 4, pp. 357-382, 2015. Available at: https://doi.org/10.12989/smm.2015.2.4.357.
- [21] FOSCO (Fiber Optics For Sale CO.), 'Optical fiber tutorial: Basic terms.' [Online]. Available at: https://www.fiberoptics4sale.com/blogs/archive - posts/95146054 - optical - fiber - tutorial - optic - fiber - communication - fiber, accessed: 05 - Jun - 2019.
- [22] S. Villalba and J. R. Casas, 'Application of optical fiber distributed sensing to health monitoring of concrete structures,' Mechanical Systems and Signal Processing , vol. 39, no. 1-2, pp. 441-451, 2013. Available at: https://doi.org/10.1016/j.ymssp.2012.01.027.
- [23] H. Guo, G. Xiao, N. Mrad and J. Yao, 'Fiber optic sensors for structural health monitoring of air platforms,' Sensors , vol. 11, no. 4, pp. 3687-3705, 2011. Available at: https://doi.org/10.3390/s110403687.
- [24] B. H. Lee, Y. H. Kim, K. S. Park, J. B. Eom, M. J. Kim, B. S. Rho, et al. , 'Interferometric Fiber Optic Sensors,' Sensors , vol. 12, no. 3, pp. 2467-2486, 2012. Available at: https://doi.org/10.3390/s120302467.
- [25] M. Abolbashari, A. S. Gerges and F. Farahi, 'A combined fiber Bragg grating and interferometric based sensor,' in 20th International Conference on Optical Fibre Sensors , Heriot - Watt University (Edinburgh, United Kingdom), Oct. 5, 2009, vol. 7503. Available at: https://doi.org/10.1117/12.835213.
- [26] S. Michelsen, 'Optical fiber grating based sensors,' Ph.D. thesis, DTU Orbit, Department of Photonics and Engineering, 2003. Available at: https://orbit.dtu.dk/en/publications/optical - fiber - grating - based - sensors, accessed: 06 - Feb - 2020.
- [27] C. E. Campanella, A. Cuccovillo, C. Campanella, A. Yurt and V. M. N. Passaro, 'Fibre Bragg Grating based strain sensors: Review of technology and applications,' Sensors , vol. 18, no. 9, 2018. Available at: https://doi.org/10.3390/s18093115.
- [28] M. D. Todd, G. A. Johnson and S. T. Vohra, 'Deployment of a fiber bragg grating - based measurement system in a structural health monitoring application,' Smart Materials and Structures , vol. 10, no. 3, pp. 534-539, 2001. Available at: https://doi.org/10.1088/0964 - 1726/10/3/316.
- [29] A. Barrias, J. R. Casas and S. Villalba, 'Embedded distributed optical fiber sensors in reinforced

- concrete structures - A case study,' Sensors , vol. 18, no. 4, 2018. Available at: https://doi.org/10.3390/s18040980.
- [30] R. C. Tennyson, A. A. Mufti, S. Rizkalla, G. Tadros and B. Benmokrane, 'Structural health monitoring of innovative bridges in Canada with fiber optic sensors,' Smart Materials and Structures , vol. 10, no. 3, pp. 560-573, 2001. Available at: https://doi.org/10.1088/0964 - 1726/10/3/320.
- [31] L - L - K. Cheung, K. Soga, P.J.Bennett, Y. Kobayashi, B. Amatya and P. Wright, ʺ Optical fibre strain measurement for tunnel lining monitoring ʺ . Proceedings of the Institution of Civil Engineers - Geotechnical Engineering, Vol. 163. no. 3, pp. 119 - 130, 2010. Available at: https://doi.org/10.1680/geng.2010.163.3.119.
- [32] T. Kapa, A. Schreier , K. K.rebber, ʺ 63 km BOFDA for Temperature and Strain Monitoring ʺ , Sensors 2018, 18, 1600. Available at: http://doi.org/10.3390/s18051600
- [33] H. Zhang and Z. Wu, ʺ Performance Evaluation of PPP - BOTDA - Based Distributed Optical Fiber Sensors ʺ . International Journal of Distributed Sensor Networks, vol. 2012, Article ID 414692. Available at: http://doi.org/10.1155/2012/414692
- [34] A. Khadour and J. Waeytens, ʺ Monitoring of concrete structures with optical fiber sensors ʺ In: Eco - efficient Repair and Rehabilitation of Concrete Infrastructures, Chapter 5, Woodhead Publishing, 2018. Available at https://doi.org/10.1016/B978 - 0 - 08 - 102181 - 1.00005 - 8
- [35] B. Simpson, N.A. Hoult and I.D. Moore, ʺ Distributed sensing of circumferential strain using fiber optics during full - scale buried pipe experiments ʺ . Journal of Pipeline Systems Engineering and Practice, vol. 6, no. 4, 04015002, 2015. Available at: https://doi.org/10.1061/(ASCE)PS.1949 - 1204.0000197
- [36] B. Simpson, N.A. Hoult and I.D. Moore, ʺ Rehabilitated reinforced concrete culvert performance under surface loading ʺ . Tunnelling and Underground Space Technology, vol. 69, pp. 52 - 63, 2017. Available at: https://doi.org/10.1016/j.tust.2017.06.007 .
- [37] Y. Liu, N.A. Hoult and I.D. Moore, ʺ Structural Performance of In - Service Corrugated Steel Culvert under Vehicle Loading ʺ . Journal of Bridge Engineering, vol 25, no.3, 04019142, 2019. Available at: https://doi.org/10.1061/(ASCE)BE.1943 - 5592.0001524
- [38] C. Y. Gue, M. Wilcock, M. M. Alhaddad, M. Z. E. B. Elshafie, K. Soga and R. J. Mair, 'The monitoring of an existing cast iron tunnel with distributed fibre optic sensing (DFOS),' Journal of Civil Structural Health Monitoring , vol. 5, pp. 573-586, 2015. Available at: https://doi.org/10.1007/s13349 - 015 - 0109 - 8.
- [39] N. Tachibana, Y. Kojima, T. Nakayama and M. Tanabe, 'Tunnel Monitoring System using Optical Fiber Sensor or Electric Conductible Paint,' in 7th World Congress on Railway Research , Fairmont Queen Elizabeth Hotel (Montréal, Canada), Jun. 4 - 8, 2006. Available at: https://www.sparkrail.org/Lists/Records/DispForm.aspx?ID=11106, accessed: 09 - Feb - 2020.
- [40] M. Fajkus, J. Nedoma, P. Mec, E. Hrubesova, R. Martinek and V. Vasinek, 'Analysis of the highway tunnels monitoring using an optical fiber implemented into primary lining,' Journal of Electrical Engineering , vol. 68, no. 5, pp. 364-370, 2017. Available at: https://doi.org/10.1515/jee - 2017 - 0068
- [41] M.F. Bado, J.R. Casas, and A..Barrias, ʺ Performance of Rayleigh - Based Distributed Optical Fiber Sensors Bonded to Reinforcing Bars in Bending ʺ , Sensors, vol. 18, no. 9, 3125, 2018. Available at: http://doi.org/10.3390/s18093125
- [42] Grup TMB, 'Millores a la xarxa. Metro automàtic. Quines línies són?' [Online]. Available at: https://www.tmb.cat/ca/sobre - tmb/millores - xarxa - transport/metro - automatic/quines - linies - son, accessed: 10 - Jun - 2019.
- [43] D. Vicario Lara, 'Obras de construcción de la Línea 9 del Metro de Barcelona. Tramo 4B. Sagrera - Gorg,' Revista de Obras Públicas (Madrid) , no. 3447, pp. 25-31, 2004. Available at: http://ropdigital.ciccp.es/detalle\_articulo.php?registro=18079&amp;numero\_revista=3447&amp;anio=2004&amp;anio\_ ini=2000&amp;anio\_fin=2009, accessed: 06 - Feb - 2020.
- [44] LUNA Technologies, 'ODiSI - A Optical Distributed Sensor Interrogator (Users Guide).' Available at: http://lunainc.com/wp - content/uploads/2014/05/ODiSI - A - Users - Guidev1.2.pdf, accessed: 04 - May - 2019.
- [45] M. F. Bado, G. Kaklauskas and J. R. Casas, 'Performance of Distributed Optical Fiber Sensors (DOFS) and Digital Image Correlation (DIC) in the monitoring of RC structures,' in 7th International Conference on Euro Asia Civil Engineering Forum , University of Stuttgart, Stuttgart, Germany, Sept. 30 - Oct. 2, 2019, vol. 615. Available at: https://doi.org/10.1088/1757 - 899x/615/1/012101.
- [46] CIMNE (International Center for Numerical Methods), 'GiD. The personal pre and post processor.' Available at: https://www.gidhome.com/, accessed: 06 - Feb - 2020.
- [47] A. Barrias, G. Rodriguez, J. R. Casas and S. Villalba, 'Application of distributed optical fiber sensors for the health monitoring of two real structures in Barcelona,' Structure and Infrastructure Engineering , vol. 14, no. 7, pp. 967-985, 2018. Available at: https://doi.org/10.1080/15732479.2018.1438479.
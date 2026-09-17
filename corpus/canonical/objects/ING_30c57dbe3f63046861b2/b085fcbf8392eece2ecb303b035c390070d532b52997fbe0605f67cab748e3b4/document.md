## ORIGINAL PAPER

## Analysis of Plastic Deformations for Tunnel Support Design in Weak Flysch Rock Mass of a Hydropower Tunnel in Central Albania

Jorge Terron-Almenara 1 · Krishna Kanta Panthi 1

Received: 29 June 2024 / Accepted: 18 March 2025 / Published online: 14 April 2025 © The Author(s) 2025

## Abstract

The prediction and analysis of deformations in tunnels excavated in weak rock mass have been traditionally done with the application of analytical methods. However, these methods are seldom evaluated in terms of their performance. This paper aims to evaluate the performance and limitations of the most commonly used methods for evaluating plastic deformations in tunnels excavated in weak and deformable flysch rock mass. For this purpose, a comparative analysis considering the analytical solutions of Carranza-Torres and Fairhust (Tunn Undergr Space Technol 15(2):187-213, 2000), the Hoek and Marinos (Tunnels Tunnel Int 32(11):34-51, 2000), and Panthi and Shrestha (Rock Mech Rock Eng 51:1823-1838, 2018), together with numerical analyses based on the finite-element method (FEM) was performed. The study is based on the construction of a headrace tunnel in central Albania, excavated in weak and highly deformed flysch rock mass subject to

weak flysch, and suggested that a better characterization of the ground behavior and a more detailed basis for the design of optimal permanent tunnel support can be achieved from the combined, hybrid use of these four approaches. As such, Ribs of Reinforced Shotcrete (RRS) were found functional as permanent tunnel support in sections of weak flysch, where the classical use of analytical approaches would likely have suggested the use of uneconomical cast concrete lining solutions. Based on the results, the study also provides a set of recommendations that can be used to assess plastic deformation and tunnel support in similar weak and complex rock masses of flysch.

## Highlights

- Weak and deformed flysch pose important difficulties for the characterization of rock mass properties and ground behavior.
- Rock mass classifications alone are not sufficient to describe weak flysch rock mass and its deformational behavior.
- Classical analytical and numerical methods used to determine tunnel plastic deformations present limitations if used alone for the study of support design.
- Deformation monitoring, combined with analytical and numerical prediction methods provide a solid basis for the design of permanent rock support.

Keywords

Flysch · Plastic deformation · Weak rock mass · Ground behavior · Deformation monitoring · Tunnel support

## List of Symbols

- Ei  Young's modulus of intact rock
- u1D70E ci  Uniaxial compressive strength of the intact rock
- γ  Unit weight of intact rock
- ν  Poisson`s ratio of intact rock
- mi  Hoek-Brown material constant of intact rock

* Jorge Terron-Almenara jorge.m.terron-almenara@ntnu.no

1 Department of Geosciences, Norwegian University of Science and Technology, Trondheim, Norway

<!-- image -->

Icon

<!-- image -->

Icon

- s  Hoek-Brown material constant of intact rock
- a  Hoek-Brown material constant of intact rock
- Erm  Rock mass deformation modulus

Grm  Shear modulus of rock mass

- u1D70E cm  Strength of rock mass
- p o  In-situ rock stress
- u1D70E v  Vertical stress
- u1D70E h  Minimum principal horizontal stress
- u1D70E H  Maximum principal horizontal stress
- u1D70E 1  Major principal stress
- u1D70E 3  Minimum principal stress
- u1D703 SH  Direction of maximum principal horizontal stress

S XX  In-plane horizontal stress

S ZZ  Out-of-plane horizontal stress

K  Horizontal to vertical stress ratio

KH  Major horizontal stress to vertical stress ratio

Kh  Minor horizontal stress to vertical stress ratio

p i  Internal support pressure in tunnel

p

eq

 Tunnel support pressure at equilibrium

p max  Maximum tunnel support pressure

u r  Tunnel wall displacement

u max  Total wall displacement

u f

 Tunnel wall displacement at the face

u

m

u i

 Tunnel wall displacement at monitoring point

 Tunnel wall displacement at equilibrium

u1D700 IC  Instantaneous tunnel strain

u1D700 FC  Final tunnel strain

u IC  Instantaneous tunnel radial displacement

u FC  Final tunnel radial displacement

L  Distance to the face in the CCM

l  Bolt length

- t  Concrete thickness

Q  Rock mass quality index

R T  Tunnel radius

- ε  Tunnel strain
- z  Tunnel overburden
- D  Tunnel span

## Abbreviations

- BIM  Block in matrix rock

CCM  Convergence confinement method

FEM  Finite-element method

FS  Factor of safety

GRC  Ground reaction curve

GSI  Geological strength index

ISRM  International Society of Rock Mechanics and Rock Engineering

LDP  Longitudinal displacement profile

NFF  Norwegian tunnelling association

NGI  Norwegian geotechnical institute

PLT  Point load test

RQD  Rock quality designation

RRS  Reinforced ribs of shotcrete

<!-- image -->

Icon

- SCC  Support characteristic curve

SDT  Slake durability test

SDI

 Slake durability index

- Sfr

 Fiber reinforced shotcrete

SRF

 Strength reduction factor in the Q-system

## 1  Introduction

The extent of plastic deformation in tunnels is one of the most relevant input parameters for rock support design in weak ground conditions. Plastic deformations around the tunnel periphery are principally the result of the tunnel excavation advance that removes the supporting effect of the face, resulting in a greater loading of the surrounding ground. If the strength of the rock mass around the opening is relatively low compared to the induced stresses acting on it after the excavation, failure of the rock material will take place involving shearing, cracking, bulking, and plastic deformations into the opening (Hoek 1999). Consequently, the installed tunnel support in direct contact or interaction with the excavated tunnel will also deform.

In that sense, the ground support interaction approach has been traditionally employed to investigate the mechanical behavior of the ground during tunnelling, and the interplay with the rock mass and the installed support (Vlachopoulos and Su 2019). Such approach assumes that there is a direct interplay between the induced confinement-or loss of confinement-produced by the excavation and exerted wall-to-wall deformations-or convergence. To address such interaction between plastic deformations, tunnel stability, and design of tunnel support, analytical and numerical approaches are usually employed. In that regard, there have been a significant amount of research covering a wide variety of approaches as noted by Anagnostou and Kovari (1993), Barla (1995, 2001), Fairhust and Carranza-Torres (2002), Oreste (2009), and more recently by Vrakas and Anagnostou (2016), Hedayat and Weems (2019), Lü and Low (2011), Vlachopoulos et al. (2020), Su et al. (2021), and Bobet and Einstein (2024), among other authors.

In rock engineering practice, however, one of the most widely used analysis approaches for the study of plastic deformations, ground interaction, and preliminary designs of tunnel support is the Convergence Confinement Method (CCM), coined by AFTES (1978) but used at least since Fenner  (1938).  This  analytical  approach  is  primarily based on the study of the ground reaction curve (GRC), which describes the relation between radial displacement ( u r ) to the loss of internal pressure ( p i ) as the tunnel face advances. The method has been subject to several updates such as that of Panet (1995, 2001), Carranza-Torres and Fairhust  (2000),  Yu  (2000),  Carranza-Torres  (2004), Vrakas and Anagnostou (2014), and the Longitudinal Displacement Profile (LDP) Vlachopoulos and Diederichs (2009). Additional development of closed analytical solutions has been also done for the simulation of the GRC in different stress-strain behavior types to suit a large variety of geological conditions (Alonso et al. 2003; Vlachopoulos and Su 2019). This includes from elastic-perfectly plastic solutions (Schwartz and Einstein 1980; Panet 1995; Carranza-Torres and Fairhust 2000), to elastic-perfectly brittle (Wang 1996), and strain-softening (Brown et al. 1983; Alonso et al. 2003), involving different failure criterion models with and without associated flow laws.

Other relevant analytical method that is widely used for the prediction of plastic deformations in preliminary studies is the one proposed by Hoek (1999) and Hoek and Marinos (2000). The authors developed a series of dimensionless plots based on Monte Carlo simulations with more than 2000 iterations from which it was found a relationship between tunnel strain ( ε ) and the ratio of rock mass strength ( σ cm ) to in-situ stress ( p o ). Such relationship is further related to a classification of tunnel squeezing potential and suitable support solutions.

More recently, Panthi and Shrestha (2018) have developed a new approach that is based on the analytical solutions of Sulem et al. (1987a, b), monitored data from three tunnel projects subject to plastic deformation in laminated, schistose rock masses from Nepal Himalaya, and correlation. This analytical methodology provides also a tool for the prediction of time-dependent and time-independent (creep) plastic deformations in underground excavations subject to anisotropic far-field stresses and non-circular tunnel excavation geometries (Sect. 4.4).

Numerical modelling methods are also employed very often for the analysis and verification of underground excavations in weak rocks. Indeed, numerical analysis constitutes a valuable part of a design process in complex ground conditions where conventional practices such as empirical and analytical methods can present limitations to capture ground behavior (Vlachopoulos et al. 2020). For tunnel projects in weak rocks, numerical analysis usually involves continuumbased approaches based on the finite-element method (FEM) and elasto-plasticity models, to ultimately derive plastic zones, ground deformations, and loading of support. However, the outcome and the representativity of the results are often very much linked to the reliability and representativity of the input parameters, type of numerical modelling program, the applied failure criterion, the assumed simplifications, and the quality of the simulation.

The above-mentioned approaches have been subject to  study in published literature related to weak ground engineering. For example, in Hoek and Marinos (2000), Marinos and Hoek (2001a, b), Hoek et al. (2005), Goricki et al. (2006), Panthi (2006), Panthi and Nilsen (2007a, b), Marinos (2014), Marinos (2017), and Marinos et al. (2018), where the authors apply or 'test' such methodologies individually on construction sites experiencing plastic deformations in weak rocks. However, the performance of these methods when applied in combination with other methods and in flysch ground conditions, has been studied very seldom. It is essentially the research conducted by Vlachopoulos et al. (2013), Langford et al. (2015) and Iasiello et al. (2021) in which the performance of the CCM is verified with FEM-analyses based on flysch rock mass cases of the Driskos tunnel, Greece and in two tunnels in northern Spain, respectively.

Essentially, the latter tells that there is a general lack of  knowledge about the true performance of analytical approaches when used to assess plastic tunnel deformations. As a result, the application of potential design optimization possibilities using four approaches (hybrid application) in disturbed and weak rock mass of flysch is missing (unknown). Such gap between the current analysis practice and the proposed hybrid procedure in this study can then lead to a poor basis for the assessment of ground behavior and tunnel support design in flysch rocks. In the best cases, such gap may be dealt with conservative designs. In worst-case scenarios, incorrect assessments may end up in undersupported tunnels with associated risk of instabilities in tunnels. Hence, the authors believe that the gap between analysis practices used until present can be significantly improved using hybrid procedure. Considering this fact, this article aims to carry out a comparative assessment of four commonly and widely used approaches for the evaluation of plastic deformations in disturbed and weak rock mass of flysch. The authors investigate the performance and limitations of these approaches with the following two main objectives:

- The study of the potential for design optimization by carrying out a combined, hybrid approach in which the four methodologies are utilized together and verified on site with monitoring deformation records.
- Development of a set of recommendations for the assessment of plastic deformations and support design in weak rocks of flysch.

In the present study, an innovative application that combines the use of four methodologies with deformation monitoring and numerical analysis to assess ground behavior and optimized ground support is proposed. It constitutes a clear advance in relation to the current state-of-the-art in the field of weak ground engineering of flysch rocks. To fulfil these objectives, a 500 m long section of a headrace tunnel in central Albania and excavated through weak flysch subject to plastic deformations was studied with the use of the CCM approach (Carranza-Torres and Fairhust 2000; Hoek and Marinos 2000; Panthi and Shrestha 2018), and FEM analyses in RS2 v.11 (Rocscience 2022). The approach resulted to be innovative, since it provided a more detailed basis for the design of alternative and cost-effective permanent support solutions such as RRS support in weak ground of flysch, where the traditional soft tunnelling practice would have likely resulted in mandatory cast concrete lining in the entire tunnel section in flysch. The comparison of the results together with numerical verification and deformation monitoring have ultimately allowed for the development of a set of recommendations for the assessment of plastic deformations, ground characterization, and tunnel support design applicable to weak rock mass of flysch.

<!-- image -->

Icon

## 2   Description of the Case Study

The study is based on the construction of a headrace tunnel for a hydropower project in central Albania. The headrace tunnel has a horseshoe shape and a diameter of 6.5 m with a cross-sectional area of 37 ­ m 2 . Most part of the 10 km long headrace tunnel was excavated with drill and blast method, which crosses a variety of geological formations that presented rather different engineering geological and rock mechanical conditions. Among other rock mass formations, a 500 m long tunnel section composed of deformed and disturbed sedimentary sequences of flysch rocks of very poor quality and subject to plastic deformation.

The design and construction of the tunnel was principally based on the Scandinavian hard rock tunnelling approach which combines the application of the Q-system for rock mass classification (NGI 2015) with observation and experience. The approach mainly uses permanent rock support consisting of a combination of rock bolts and fiber reinforced shotcrete for fair to good quality rock mass. If the rock mass is  weak  and  presents Q value  below  one,  load-bearing support in the form of RRS is added. As such, both the temporary or initially applied rock support at-or very close to-the advancing face, and the additional support installed behind the face based on the measured/monitored/observed ground behavior-are combined to form the final permanent rock support. This requires that all materials used as tunnel rock support shall be designed and executed to have a permanent function.

Accordingly, the flysch rock masses were mapped and classified at each excavation round, to derive support class and recommendations of rock support recommendations at the tunnel face. Based on a mapped rock mass quality Q ranging around 0.1-1 along the 500 m long tunnel section under study, the initial support consisted of fiber reinforced shotcrete (Sfr) 150 mm, 4 m long radial rock bolts Ø19 mm spaced c/c 1.5 m, and load bearing support in the form of ribs of reinforced shotcrete (RRS) of type Si 30/6 c/c 1.5 m. However, in complex and weak rock mass such as the disturbed flysch, supplementary design approaches based on the principles of weak ground engineering are normally necessary for the adequate characterization and design of tunnel support (Hudson and Harrison 1997). Accordingly, a comprehensive program of site investigations including deformation monitoring, measurement of in-situ stresses, assessment of GSI, laboratory testing of rock, and numerical verification of tunnel stability were performed.

Based on measured tunnel convergences of up to 50 mm (Sect. 3.6) and on the performed stability analyses of the initially applied rock support, it was concluded that additional support was needed in the flysch section. As such, additional RRS arches (RRS Si 30/6) were added behind the face and installed in between existing RRS arches (Fig. 1a, b) with spacing c/c 1.5 m. As a result, the combination of initial and additional support forming the permanent support consisted of Sfr 150 mm, 4 m long radial rock bolts Ø19 mm

<!-- image -->

Engineering drawing

Fig. 1 Schematic illustration of permanent rock support in the studied tunnel section in weak, deformable flysch (not to scale). a Longitudinal section of tunnel showing initial support at the face and final support behind the face. b Tunnel cross section showing permanent, final

<!-- image -->

Logo

support  behind  the  face,  based  on  the  combination  of  initial  +  additional  support. c Detail  of  the  construction  of  a  single  RRS  arch  of type Si 30/6 used in the tunnel project spaced radially c/c 1.5 m and longitudinally c/c 0.75 m, and RRS Si 30/6 spaced c/c 0.75 m. Together with the installation of anchored structural inverts with a thickness of 400 mm and spiling bolts in the roof, the resulting reinforcement and support capacity of that combined RRS-support system was concluded to perform satisfactorily and provide a robust permanent support solution, as so demonstrated in the calculated factors of safety (FS) of support shown in Sect. 5.1.

Despite the use of relatively heavy permanent support that results from the tight spacing of RRS arches, the adopted design solution may be deemed lighter and optimal if compared to current design practices in Alpine countries, where additional concrete lining would have likely been mandatory. The adopted design solution was possible due to comprehensive characterization of the flysch and the involvement-and combination-of different methods to analyze plastic deformations and tunnel stability.

A detail of the basic construction of a single RRS arch of type Si 30/6 used in this tunnel section is shown in Fig. 1c. The design is empirical and based on the recommendations from the Q-system (NGI 2015). As such, 'Si 30/6 c/c 1.5 m' indicates bolted shotcrete arches of 300 mm in thickness, spaced 1.5 m in the tunnel direction, and reinforced with a single layer composed of six steel rebars of diameter Ø = 16 mm. In general, the RRS support provides a significant design and construction flexibility as the RRS configuration can be easily adjusted to the ground behavior and ground load conditions by adjusting the center distance of the RRS arches, the thickness of the arches, and the amount of steel bars in each RRS arch (NFF 2008). The final design was upgraded with the additional rock support by the installation of RRS arches in between existing arches, i.e., shortening the center to center distance of the arches to the half, as shown in Fig. 1b. This addition of rock support was done to achieve smoother, more even surface in the tunnel periphery so that friction head loss caused by undulating surface is minimized.

Fig. 2 Regional geology of Albania, based on the work of Dilek et al. (2007) and Tremblay et al. (2015). a Geodynamic model for the obduction of the Tethys Ocean and evolution of the Dinarides-Hellenides (Balkan Alps). b Simplified geological map of Albania

## 3   Ground Conditions in the Tunnel

## 3.1   Regional Geology

The regional geology in Albania is rather influenced by the tectonic context and the geodynamic evolution of the Dinarides-Hellenides belt as described in Dilek et al.

<!-- image -->

Geographical map

<!-- image -->

Logo

(2007) and Tremblay et al. (2015). Starting from the Middle Jurassic and lasting approximately until the Oligocene, significant compressional events in the E-W and NE-SW directions resulted into continent convergence of the Gondwana and Eurasia plates, locally known as Adria and Pelagonia, respectively (Fig. 2a). This resulted in the closure of the Tethys Ocean, obduction of ocean crust, foreland propagation, crustal shortening associated to piggyback thrusting and detachment, and development of the Balkan Alps.

As such, three main tectonostratigraphic domains can be differentiated in the Dinarides-Hellenides belt in Albania. Starting from the West, the first domain corresponds to folded and thrusted flysch sequences, formed from both, continental and marine sedimentary facies, with varying proportions of fines, coarse material, and carbonates. The rheology of this domain is relatively soft, if compared to the underlying Variscan basement rocks and the overlying ophiolites, facilitating, therefore, the transport and emplacement of the harder ophiolites onto the continent (Fig. 2a). Due to the magnitude of accommodated deformation in the flysch domain, a significant amount of faulting and folding has been printed in the flysch sequences that are embodied in each of the thrust nappes. The second or central domain is represented by ophiolites which are overlying tectonic slices of serpentinites. In addition, a third or Eastern domain is mostly characterized by Triassic-Jurassic platform carbonates overlying Variscan basement.

As illustrated in Fig. 2b, the resulting structural geology of Albania can be characterized by the presence of penetrative thrust faults aligned NNW-SSE, nappes and stratigraphic repetitions, folding with axial planes striking also NNW-SSE direction, tectonic windows, and double verging faults. On the other hand, the other two domains, i.e., the ophiolitic and the Eastern domains show slight folding only, likely occurred before or during obduction (Tremblay et al. 2015). Therefore, it is very likely that most part of deformation and faulting has taken place in the softer flysch sequences facing the Central and Western regions of Albania.

Fig. 3 Geological conditions along the headrace tunnel under study. a Longitudinal profile. Note study area marked with orange color rectangle. b Folded and partially disturbed and thinly laminated siltstonedominant flysch rock mass type VIII with intercalated layers of sandstones at 7 + 317. c Heavily disturbed, sheared, almost chaotic flysch rock mass type X at 7  +  194. d Exposure of bimrock at tunnel face 7  +  484

<!-- image -->

Logo

## 3.2   Geological Layout in the Tunnel

Figure 3a shows a 3 km long headrace tunnel section oriented approximately E-W, crossing through ophiolites, the underlying metamorphic sole composed of serpentinites, and the deformed, faulted flysch sequences. These three geological units are separated by thrust faults. However, it is mainly the flysch domain that is most affected by faults and shear zones. The successive mapping along the tunnel section in flysch revealed that the fault zones and the bedding presented a generalized NNW-SSE strike, with a varying dip angle of 30-60° towards WSW, and a common vergence towards E, indicating a direct influence of the main regional thrusts and structural alignments (Fig. 2b) over the smaller, local scale folded structures in the tunnel.

Since the tunnel section in flysch is aligned W-E, the angle between bedding strike and the tunnel is about 60°. As shown in Fig. 3b, the headrace tunnel alignment is relatively favorable, which has reduced possibilities of structurally controlled failures. On the other hand, the frequently occurrence of faults and shear zones of varying thickness has caused disturbance in the rock mass. Hence, the rock mass in this tunnel section is sheared, crushed, jointed, folded, weathered, which has lowered the mechanical properties of the rock mass. In some sections the flysch has suffered a major remobilization, where the rock mass structure is completely lost. This resulted rock mass to become block-in-matrix rocks (bimrock) as defined in Medley (1994) and illustrated in Fig. 3d.

<!-- image -->

Line chart

Marked with an orange rectangle in Fig. 3a, it is shown the area of study in this article. The selection of this 500 m long section attends to a tunnel section with a larger rock overburden ( z ~  225-285 m) and excavated through rock masses of very poor quality in which the most significative geotechnical challenges were associated to plastic deformations, tunnel portions with slaking rocks, and weak ground, where the traditional design methods of rock support often present limitations to assess ground behavior and adequate tunnel support designs.

## 3.3   Rock Mass Mapping and Geotechnical Behavior

The studied rock mass corresponds to a section of the headrace tunnel located between 7 + 029 and 7 + 531. The headrace tunnel passes through rock mass composed by disturbed and weak siltstone-dominated flysch sequences that present variable proportions of siltstones and strong members represented by intercalated, thin and broken layers of sandstones and some carbonates. The flysch is often folded and intersected by faults and shear zones, leading to a relatively high degree of jointing, disturbance, and weathering.

Two separate classification systems, Q (Barton et al. 1974; NGI 2015) and the adapted version of the GSI for flysch rock mass conditions ­ (GSI flysch ) of Marinos (2017) were used for tunnel mapping. The continuous log of mapped rock mass quality Q and GSI values are plotted in Fig. 4 to show the rock mass quality distribution through the studied section. In general, the mapping has revealed very poor rock mass conditions in the flysch, where Q values ranged between 0.1 and 1, and ­ GSI flysch values between 15 and 35.

The fault and shear zones present a typical thickness of ca. 1-5 m. Moreover, major zones were also encountered, such as the one at tunnel profile 7 + 349, with about 10-15 m in thickness. It should also be noted that the degree of jointing and disturbance in the tunnel sections between the faults were also influenced significantly by the tectonic disturbance, yielding low Q and ­ GSI flysch values as registered in Fig. 4. Hence, the very poor rock mass conditions do not only reflect the weak character of the flysch, but also the tectonic-deformation and faulting-processes that happened to these sedimentary rocks in relation to the geodynamic context and evolution of the Dinarides-Hellenides belt, as described in Sects. 3.1 and 3.2. In other words, the low values of Q and ­ GSI flysch reflect both the weak nature of the dominant flysch rock material-mostly siltstones-the loss of rock mass structure due to shearing, faulting, fracturing, weathering, and folding, which resulted in the weakening of the rock mass strength and potential for plastic deformations.

Figure 4 further shows that there is a good agreement on the variation of Q and ­ GSI flysch values upon change in the rock mass quality along the headrace tunnel chainages. However, it is also observed in two areas that while the ­ GSI flysch can capture small variations of the engineering geological conditions over relatively short tunnel sections, the Q values seem to be insensitive, or at least show smaller variations. These two zones where the performance of ­ GSI flysch is greater than that of the Q to capture variations in the geological conditions are marked with green squares in Fig. 4. There are several reasons that may explain such differences in the performance of both classifications. Some of these are discussed in Palmstrom and Broch (2006), and are related to the high dependence of the RQD and SRF parameters in the overall Q -assessment. In that sense, determination of RQD

Fig. 4 Distribution of Q values and ­ GSI flysch as mapped during construction by the engineering geologist teams at the face, through the weak and disturbed flysch sequence between 7 + 029 and 7 + 531

<!-- image -->

Line chart

<!-- image -->

Icon

in weak, thinly laminated, and deformed sequences of sedimentary rock formations imposes challenges to geologists to visually determine representative RQD values. It is also evident that the alternance of thin (&lt; 10 cm) laminations would damp and flatten the final Q value as observed in the plot, since the standard RQD-measurement practice recommends the use of RQD = 10 in the empirical Q formula whenever the mapped RQD ≤ 10 (NGI 2015). Such recommendation, however, obviates the inherent and beneficial contribution of hard rock members with RQD &lt; 10 on the overall strength and stiffness of the rock mass.

Some challenges were also experienced when attempting to characterize SRF values in flysch rock mass during construction. The SRF parameter in the Q -system depends on the ratio between tangential stress and uniaxial compressive strength of the rock material ( u1D70E ci ). As such, one of the challenges was related to the uncertainty in the estimation of representative values of u1D70E ci due to the weak, broken, layered, and partially slaking nature of flysch rocks. Another important challenge was linked to the practical problem of deriving realistic values of in-situ stresses at the face in the presence of weak, laminated flysch rock mass with embedded and variable proportions of soft and stiff layers, and before the performance of stress measurements. Under these circumstances, best estimates of the SRF parameter were done based on experience, field indicators, and engineering judgement recommendations (NGI 2015).

Therefore, to minimize the challenges associated to the characterization of RQD and SRF parameters in the flysch, ­ GSIflysch was also mapped in parallel with Q so that a more detailed description of the rock mass quality is achieved. A summary of the mapped rock mass conditions considering the approximate proportion of weak and strong rock over the tunnel face, field estimates of the respective strength of the intact rock material ( u1D70E ci ) in the weak and strong rocks, and a description of the rock mass, together with Q and ­ GSI flysch values are presented in Table 1. This information given in Table 1 did not only serve to derive weighted or equivalent strength of the rock mass to be used in analytical and numerical models, but also assisted in the description of the flysch rock mass and the understanding of the expected ground behavior.

The laboratory assessment of intact rock strength of siltstone in Table 1 was rather challenging due to the slaking and weakening nature of the siltstone rocks upon changes in moisture conditions during transport. For this reason, the intact rock strength presented in Table 1 was mainly determined from field estimates done in the tunnel face with geohammer after Brown (1987), and assisted by point load testing (PLT) at the face. The achieved strength values were then compared to characteristic strength values of similar flysch rocks in northern Greece given Marinos (2017). The systematic approach used to field estimates were very helpful to capture the high variability of rock strength in the dominant lithologies of siltstones and sandstones, and to obtain representative, undisturbed estimates of strength. Although this approach did not provide exact values of u1D70E ci , it turned into a valuable methodology for the characterization of rock strength that was later subject to numerical calibration and weighting as suggested in Hoek and Marinos (2000), Marinos et al. (2005) and Marinos (2017).

<!-- image -->

Icon

As mentioned above, the weak and disturbed character together with the heterogeneous composition of the encountered flysch presented challenges for rock mass quality assessment and characterization using the Q-system. With the adapted version of GSI for flysch (Marinos 2017), however, a more comprehensive engineering geological characterization and a better prognose of the ground behavior were made possible. As such, most of the fourteen study sections were geotechnically classified as flysch rock mass class VIII and X. In geological terms, these two classes represent two different degrees of tectonic deformation and disturbance. Yet, the material was characterized by repetitive siltstonerich sequences with alternating and thin intercalations of strong members such as sandstones that have experienced strong deformational and shearing events. As a result, the main rock mass structure such as folding and lamination turned completely disrupted. The presence of disturbed rock mass was later confirmed during symmetrical tunnel wall-to-wall deformation monitoring and registrations. As such, the random orientation of ground heterogeneities such as weakness and shear zones at the scale of the tunnel has shown homogeneous and isotropic character in the flysch rock mass. The latter observation coincides with that of Langford et al. (2015) for similar disturbed flysch materials in the Driskos tunnel.

The described intensity of fractures and disturbance in the flysch rock mass was usually accompanied with a declining quality and strength for class VIII to X rock mass. In addition, there were two mapped tunnel sections, chainages 7 + 423 and 7 + 455, with signs of strong disturbance and remobilization, resulting in a mixture of rock blocks embedded within a finer matrix of remobilized siltstones, as illustrated in Fig. 3d. The latter geological description defines the typical characteristics of a tectonic mélange, also known as bimrock, which in the mentioned two tunnel sections presented a relatively compact character.

To correlate the qualitative description and classification of the mapped flysch to actual geotechnical behavior based on their engineering geological characteristics and the potential failure mechanisms upon tunnelling, the recommendations given in Marinos (2014, 2017) and Marinos et al. (2018) were followed. As such, the behavior of flysch rock mass during tunnelling were mainly assessed on the basis of three main parameters. The rock mass structure, the intact strength of the dominant rock material, and the in-situ stresses. The slaking potential was also considered an important parameter affecting ground behavior as it affects the intact rock strength and the potential for erosion causing tunnel instabilities. Accordingly, a description of the typical rock mass types and a prognose of the ground behavior were done (Fig. 5) to facilitate the assessment of rock support.

Table 1 Summary of mapped rock mass conditions at the studied tunnel sections in flysch between 7 + 029 and 7 + 531

| Section   |    Q |   GSI flysch | GSI flysch class, or ­ BIM a   |   Fraction of weak part (%) |   u1D70E ci b siltstone (MPa) |   u1D70E ci b hard members (MPa) | Rock mass description                                                                                                                                                                                    |
|-----------|------|--------------|--------------------------------|-----------------------------|-------------------------------|----------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 7 + 029   |  0.1 |           25 | X                              |                          90 |                            15 |                               50 | Siltstone dominated rock mass with a high degree of shearing and disturbance. Embedded parts of sheared siltstones                                                                                       |
| 7 + 064   | 0.11 |           25 | X                              |                          80 |                            20 |                               50 | Sheared and disturbed sequence of thin laminated siltstones, clayshales and broken sandstones                                                                                                            |
| 7 + 092   | 0.29 |           25 | X                              |                          60 |                            15 |                               50 | Tectonically disturbed and sheared rock mass composed by bro- ken and partly chaotic blocks inside a weak matrix of strained dark siltstones                                                             |
| 7 + 136   |  0.5 |           35 | VI                             |                          60 |                            15 |                               50 | Stratified and partially disturbed, folded rock mass composed by alternances of persistent siltstone and carbonatic layers                                                                               |
| 7 + 168   | 0.38 |           27 | VIII                           |                          60 |                            10 |                               55 | Deformed and partially sheared rock mass composed of weak and strained siltstones and micritic siltstones                                                                                                |
| 7 + 194   | 0.25 |           25 | X                              |                          70 |                            15 |                               40 | Laminated and strongly disturbed rock mass composed of sheared, clayey siltstones, and embedded broken parts of harder, carbonatic rocks                                                                 |
| 7 + 218   |  0.2 |           25 | X                              |                          50 |                            15 |                               50 | Disturbed, partly chaotic rock mass with nearly disappeared structure, a significant amount of harder and embedded blocks inside a weak matrix, that remind to a typical block-in-matrix (bimrock) mass  |
| 7 + 266   |  0.2 |           35 | VIII                           |                          50 |                            15 |                               50 | Sheared and deformed rock mass composed by broken fragments of weathered and disturbed reddish sandstones embedded in a weak and dark matrix of clayey siltstones                                        |
| 7 + 291   | 0.16 |           30 | VIII                           |                          90 |                            20 |                               40 | Thinly laminated rock mass composed of weak and dark-clayey siltstones with thin carbonatic layers                                                                                                       |
| 7 + 317   |  0.5 |           30 | VIII                           |                          60 |                            25 |                               50 | Disturbed folded and siltstone dominant rock mass with interca- lations of sandstones and limestones                                                                                                     |
| 7 + 342   |  0.1 |           32 | VIII                           |                          70 |                            15 |                               50 | Thinly laminated and partially disturbed rock mass composed of sheared and clayey siltstones, and embedded thin laminations of carbonatic rocks                                                          |
| 7 + 423   | 0.11 |           35 | BIM                            |                          30 |                            15 |                               50 | Sheared rock mass composed by an alternance of disturbed and partly tectonized big sandstone blocks embedded in weak clayey siltstone material                                                           |
| 7 + 455   |  0.2 |           33 | BIM                            |                          50 |                            20 |                               50 | Highly disturbed, partly chaotic rock mass with nearly disap- peared structure, a significant amount of harder and embedded blocks in the rock mass, similar to a typical block-in-matrix (bimrock) mass |
| 7 + 531   | 0.15 |           25 | X                              |                          80 |                            20 |                               50 | Thinly laminated and strongly disturbed rock mass composed of sheared and folded siltstones, and embedded broken parts of harder, carbonatic rocks                                                       |

The ground behavior in flysch rock mass, both class VIII and X, is generally characterized by plastic deformations triggered by a relatively low stiffness and strength of the rock mass in relation to the in-situ stresses acting on it. Provided that the rock mass is rather disturbed, and that there is a generalized absence of dominant structures, the deformations and ground loads should be approximately distributed evenly around the tunnel profile. However, in flysch rock mass VIII, where the bedding or flanks of folds intersect the tunnel excavation (as in the roof of rock mass class VIII in Fig. 3a), some deformation asymmetry and slightly uneven loads may be encountered as a result of pre-defined failure directions at joints. But in general terms, and specially towards flysch type X, the expected behavior is considered almost isotropic and largely controlled by the low strength and high deformability of the dominant lithology ( σ ci of siltstone 15-30 MPa) in relation to the in-situ stresses. As such, the presence of a moderate overburden ( z ~  225-285 m) led medium stress situation in flysch, which limited the extent of plastic deformation. The slaking properties of the siltstone rock can, however, cause additional failure as the rock mass near the tunnel periphery may suffer deterioration and weakening due to cyclic moisture changes.

<!-- image -->

Icon

Fig. 5 Classification  of  ­ GSI flysch ,  description  of  rock  mass  characteristics,  and  interpretation  of  ground  behavior  to  tunnelling  for  the two most representative flysch rock masses studied between 7 + 029

<!-- image -->

Table

Altogether, the mentioned ground behavior suggested the following design and construction implications: (1) short excavation rounds; (2) use of bolt spiling; (3) immediate sealing of the newly exposed excavation faces with shotcrete to minimize slake initiation; (4) dense bolt patterns and shotcrete to reinforce the ground; and (5) construction of load-bearing support consisting of systematic RRS arches to hold both symmetric and uneven ground loads. If compared to the rather stiff solution consisting of steel sets and cast concrete liners mostly used for large convergences and often in weak flysch conditions, RRS support seems to be a more convenient alternative for the expected ground behavior as it offers a more flexible, leaner, and cost-effective solution.

## 3.4   Rock Mass Properties

As derived from the characterization of ground behavior performed in Sect. 3.3 and Fig. 5, the strength and deformability and 7 + 531. Based on the work and ground characterization charts of Marinos (2014, 2017) and Marinos et al. (2018)

<!-- image -->

Logo

properties of the intact rock govern the response of the flysch rock mass to tunnelling. For that reason, a comprehensive site and laboratory investigations were performed to investigate the mechanical properties of the intact rock-both the siltstone and the strong members of sandstone-such as uniaxial compressive strength ( u1D70E ci ) and the Young`s modulus ( Ei ) .

The latter considered rock specimens taken from existing core holes drilled from the ground surface during planning and design stages of the project, rock lump specimens taken from the tunnel face during tunnel construction, and samples from short core holes drilled on the tunnel wall during excavation. It was observed that the slaking-prone siltstone specimens from core holes drilled at the tunnel wall and from the ground surface presented some disturbance as moisture changes were introduced in the rock during both core drilling operations and transport to the laboratory. This experience coincides with that of Hoek et al. (2005) in similar rock mass conditions of flysch, in which some degree of rock deterioration by slaking was usually triggered in weak, fissile flysch rocks in spite of the precautions taken in these cases. As a result, the uniaxial compressive test results of siltstone in the laboratory were only used as an indicator or index of rock strength in relation to the potential deterioration, but not as direct input in our studies and calculations.

The strength of the intact siltstone was determined on the basis of point load testing (PLT) carried out on site, which allowed rapid collection of rock lumps at the tunnel face right after blasting rounds to test the undisturbed, fresh rock according to the ISRM recommendations (1985). PLT in the weak rocks of flysch was in this case a rather versatile testing approach, which offered reliability and a reasonable level of accuracy, as later confirmed during the numerical back-calculations performed in the project. The estimations with PLT were accompanied by systematic estimates of rock strength based on geo-hammer blows and field indicators as suggested in Brown (1987). On the other hand, testing of the sandstone was performed in core specimens retrieved mostly from the mentioned core holes, and tested in the laboratory, allowing for the determination of the Young's modulus and the Poisson ˈ s ratio ( ν ) of the intact rock, as opposed to the siltstones, where these properties had to be based on existing literature in similar flysch rock mass (Marinos (2014, 2017).

In addition to u1D70E ci and Ei , other basic engineering geological input of the intact rock such as the material constant ( mi ) of the generalized Hoek-Brown failure criterion are needed to determine the frictional properties of the rock and rock mass strength (Hoek et al. 2002; Hoek and Corkum 2002; Crowder and Bawden 2004). Since no testing to determine mi in siltstones and sandstones were made in the laboratory, recommended characteristic values from similar flysch conditions by Marinos (2014, 2017) were utilized. A summary of the assessed properties of the intact rocks is presented in Table 2.

The weak rocks of siltstone belonging to the flysch sequences encountered in the study section presented also varying degrees of slaking behavior upon changes in the moisture conditions. As slaking, deterioration of the rock on the outer surface of the tunnel excavation may take place in relation to the normal operation of a headrace tunnel based on normal cycles of emptying and filling for the respective maintenance and production, slake durability test (SDT) according to ISRM (1979) was performed in up to nine samples of siltstone. The results showed a wide variability of Slake Durability Index (SDI), with a minimum of 16.5%, a maximum of 85.8%, and an average of 48.3%. The unit weight of the rock material (γ) was also tested, resulting in 25.2 kN/m 3 for the siltstone and 26.1 kN/m 3 for the sandstone.

Table 2 Assessed properties of intact rock for the main lithologies in the flysch

| Rock type   |   γ (kN/m 3 ) | E i (GPa)   | ν     | σ ci b (MPa)   |   m i a |
|-------------|---------------|-------------|-------|----------------|---------|
| Siltstone   |          25.2 | 15-25 a     | 0.3 a | 15-30          |       7 |
| Sandstone   |          26.1 | 31          | 0.22  | 63-112         |      17 |

## 3.5   In-Situ Rock Stresses

Measurement of in-situ rock stresses were done in the tunnel project. However, the closest measurement was done at chainage 7 + 884, about 400 m distance to the closest tunnel section studied in this manuscript. The measurement results (Table 3) showed relatively high horizontal stresses, and a minimum principal stress represented by the vertical gravitative stress ( u1D70E V ). However, it was found that these measurements had limited usability for the assessment of the in-situ stress state in the tunnel section studied in this article (7  +  029 to 7  +  531) due to significant differences in the tectonic context, topographic conditions, and in the rheology of the rock materials between the measurement location (hard ophiolite) and the study section (weak flysch). As suggested in Stephansson and Zang (2012), supplementary studies should be done to obtain a representative estimation of the in-situ stresses at the given site, in addition to stress measurements. As such, the regional stress context is studied together with numerical simulations to back-calculate a stress state for the studied tunnel sections.

Table 3 Results of in-situ stress measurement with the hydro-fracturing method at 7 + 884

| Location   |   Rock overburden (m) |   u1D70E V (MPa) |   u1D70E H (MPa) |   u1D70E h (MPa) | u1D703 u1D70E H (°)   |
|------------|-----------------------|------------------|------------------|------------------|-----------------------|
| 7 + 884    |                   120 |              3.8 |             13.9 |              7.0 | N134                  |

<!-- image -->

Geographical map

Fig. 6 Word  stress  map  for  Adriatic  region  (Heidbach  et  al.  2018), with directions for maximum  principal  horizontal  stresses,  and approximate location of the tunnel project in central Albania

<!-- image -->

Icon

As observed in the stress map for the Adriatic region in Fig. 6 (Heidbach et al. 2018), the main direction for the maximum principal horizontal stresses ( u1D70E H ) in central Albania and close to the tunnel location is approximately NE-SW. However, the measured direction of u1D70E H at 7  +  884 together with additional stress measurements performed at other locations in the tunnel project suggested a local rotation of u1D70E H to NW-SE direction. Considering that the tunnel section in flysch is aligned N095°, the resulting angle between u1D70E H and the tunnel alignment was ca. 40°, which also means an angle of ca. 50° between u1D70E h and the tunnel direction. This is taken into account by the software utilized for the calibration analysis (RS2 v.11, Rocscience) to calculate the in-plane horizontal stress ( S xx ) and the out-of-plane horizontal stress ( S zz ).

Back-calculation and calibration of the in-situ stress state at the flysch section was then performed on the basis of available deformation measurements from tunnel monitoring sections during construction. For this purpose, the convergence section at 7 + 168 was selected, since it was the one that was placed closest to the face, hence registering most of the deformations behind the face. The vertical stress ( u1D70E V ) was assumed the result of gravitative stress from a rock overburden of 280 m, i.e., 7 MPa. In turn, determination of the horizontal stresses ( u1D70E H )  was based on the semi-empirical expression of Jaky (1944) to estimate the horizontal to vertical stress ratio ( K ) for weak ground, ( K = 1 - sin u1D719 ′ ), followed by numerical verification. The necessary input parameters of the rock mass for the back-calculations were taken from the assessed rock mass properties in Sect. 3.4, and from the application of the Generalized Hoek-Brown (Hoek et al. 2002) criterion to determine the equivalent Mohr-Coulomb strength parameters of the rock mass, cohesion ( c ′ ) and friction angle ( u1D719 ′) in Table 4. Up to four different calibration models were run in the RS2 program, based on several combinations of rock mass strength, stiffness, and K ratios to be able to capture the best fit in relation to possible variations in the rock mass strength and stiffness.

In each of the models, the external boundaries were created by an external geometry of size 60 × 60 m, with the tunnel in its center. The four external boundaries of the boxshaped models were then restrained, and the tunnel excavation geometry placed in the center (Fig. 7). The simulation was carried out for a horseshoe shaped tunnel having a span of 6.5 m. A graded mesh was produced automatically in RS2 with elements formed by six-noded triangles.

To allow for a three-dimensional simulation of tunnel  relaxation  in  relation  to  tunnel  face  advances  with sequential excavation and rock support installation, the core-replacement  method  (Vlachopoulos  and  Diederichs 2009) was employed to determine the displacements occurred at the face ( u f ). By the subtraction of the total displacements of the supported models ( u max ) to the displacements occurred at the face ( u f ), the actual displacements at equilibrium with the support ( u i ) were derived. The latter operation is needed, since RS2 calculates total displacement to solve for equilibrium, but in reality, a fraction of these displacements has taken place before the support installation/activation. By assuming then a symmetric distribution of the tunnel convergence measured at 7 + 168 (32 mm), the measured tunnel radial inward displacement ( u r ) is 16 mm. As such, the calibration model that fits best with both the convergence measurements and with the assessed rock mass properties (Table 4) was model A, i.e., a measured radial displacement of 16 mm contra a calculated wall displacement of 17 mm (Fig. 8a). The resulting stress state for the study section in the flysch was then described by the vertical stress u1D70E v = 0.025 z (where z is the vertical overburden in meters), the ratio of the major horizontal stress to vertical stress K H = 0.5, and the ratio of the minor horizontal stress to vertical stress K h = 0.5.

Fig. 7 Setup of the RS2 model showing restrained outer boundaries, meshing, excavation, and support

<!-- image -->

Engineering drawing

Table 4 Simulations for back-calculation of in-situ stress state at the study section in flysch rocks based on convergence section 7 + 168 (280 m rock overburden)

| Model   |   GSI |   m i a |   u1D70E ci a (MPa) |   E i (GPa) |   E rm b (MPa) |   c ′ (MPa) |   u1D719 ′ (°) |   K |   u1D70E H (MPa) |   u1D70E h (MPa) |   u max c (mm) |   u f d mm) |   u i e (mm) |
|---------|-------|---------|---------------------|-------------|----------------|-------------|----------------|-----|------------------|------------------|----------------|-------------|--------------|
| A       |    27 |       8 |                  28 |          25 |           1618 |         0.5 |             27 | 0.5 |                5 |              3.5 |           81.1 |          64 |           17 |
| B       |    27 |       8 |                  28 |          20 |           1348 |         0.5 |             27 | 0.5 |                5 |              3.5 |            150 |          90 |           60 |
| C       |    27 |       6 |                  25 |          25 |           1618 |        0.43 |             24 | 0.6 |                5 |              4.2 |            215 |          77 |          138 |
| D       |    27 |       6 |                  25 |          20 |           1348 |        0.43 |             24 | 0.6 |                5 |              4.2 |            249 |          88 |          161 |

<!-- image -->

Logo

It should also be noted that the assessment of in-situ stresses presented in Table 4 has been, to a great extent, based on back-calculations. It should, therefore, be highlighted that the employment of back-analyses with numerical  calculations  and  deformation  measurements often involve limitations and assumptions (Walton and Sinha 2022). Although back-calculation provides a rather useful tool to study the response of a rock mass to excavation on the basis of a set of rock mass properties (Sakurai 2017), the simplifications, premises, reading inaccuracies, and assumptions involved in such approach need to still be known for the correct interpretation of results. For this study in flysch rocks, the main assumptions and considerations for the modelling and calibration processes were:

- The utilized constitutive model (generalized HoekBrown) with elastic-perfectly plastic material behavior was assumed to capture the deformational behavior of the weak rock mass of flysch subject to moderate stress levels (ca. 7 MPa of confinement).
- The RS2 calculations performed in computational stages and with the core-replacement method provide a repre-

Fig. 8 Numerical models 'A', 'B', 'C' and 'D' considering different rock mass strength, stiffness and K-ratios for the back-calculation of the in-situ stress state at 7  +  168. The plots show calculated total displacements u max in RS2 in supported tunnel

<!-- image -->

Engineering drawing

<!-- image -->

Logo

sentative simulation of the gradual excavation followed by the sequential installation of rock support.

- The visually mapped proportion of weak rock over strong rock at the tunnel face is sufficiently representative of the actual rock mass conditions at the face and outside the perimeter of the excavation.
- The rock mass is assumed to behave isotropically and can be modelled-or simplified-as a continuum material, based on the weighted assessment of rock mass strength properties, such as u1D70E ci , E i , and m i .
- It is assumed that the type and amount of site investigations have provided sufficient basis as to interpret representative input parameters for the models. Despite of the taken precautions during deformation monitoring, it is similarly assumed that there might have been some inherent uncertainty related to the instrument precision and interpretation of deformation patterns (Sect. 6). This fact was considered while interpreting the results.
- It is assumed that rock mass deformation is the behavior that defines best the response of weak, disturbed flysch and back-calculation based on observed (measured) deformations against calculated results (outputs) give a reliable basis for calibration for the purpose of the study. However, it should be noted that various combinations of input parameters can yield a similar response in the models. To enhance reliability associated to such nonuniqueness in the back-analysis process, all the available rock-mechanical information was utilized to constrain the model as much as possible, as suggested in Sjöberg (2020).

Table 5 Summary of measured wall-to-wall convergence in the flysch tunnel section 7 + 029 to 7  +  531

<!-- image -->

Icon

## 3.6   Measured Tunnel Deformations

As described in Sect. 3.2, the stability and the ground behavior of the studied tunnel sections with disturbed and siltstone-dominated flysch rock mass, are mostly characterized by tunnel deformations. In that sense, rock mass disturbance and heterogeneity led to an increase of rock mass complexity in relation to the high variability in rock mass properties and ground behavior along the tunnel. The latter often involves uncertainty in relation to the selection of input parameters for the design of adequate permanent rock support. In this regard, measurement of tunnel deformation in the flysch section was implemented to allow for the control of tunnel stability over time, to permit the numerical calibration of rock mass properties, and to provide a basis for design verification/optimization based on the application of an observational approach (Peck 1969; Sakurai 1997; Fairhust 2017).

Accordingly, a comprehensive monitoring program with wall-to-wall convergence measurements was implemented in the flysch sections. It consisted of fourteen convergence sections, distributed at about 25-35 m distance from each other along the study tunnel section 7 + 029 to 7 + 531, to cover most possible areas with weak and very poor rock mass of flysch (Table 5). The measurements were done with a digital tape-extensometer of the brand DGSI, presenting a measurement repeatability of ± 0.1 mm. The wall-to-wall convergence measurements in each of the monitoring sections of the tunnel were measured approximately once per day when the monitored section was still under the influence of the tunnel face-i.e., up to a distance of about 2 D (where D is tunnel span). The frequency of these measurements was then reduced progressively as the tunnel face moved away and over time. As such, measurement frequency was about once per week in the first 1-3 months, and twice per month after that. To ensure reliable readings, the instrument was sent for calibration once per year to the supplier, control measurements were done regularly on site over known, fix, distances, and temperature corrections of the measurements performed according to the instrument`s manual. The measurement method involved also the performance of three readings for each measurement. Such approach was done to increase accuracy in the measurements by statistically averaging the three readings in each measurement.

| Chainage   |   GSI | GSI flysch class, or BIM   |   Rock cover (m) |   Tunnel radius ­ R T (m) |   L (m) |   Measured convergence (mm) |   Total monitor- ing time (days) |
|------------|-------|----------------------------|------------------|---------------------------|---------|-----------------------------|----------------------------------|
| 7 + 029    |    25 | X                          |              226 |                      3.25 |       2 |                          34 |                              216 |
| 7 + 064    |    25 | X                          |              238 |                       3.2 |       1 |                          32 |                              255 |
| 7 + 092    |    25 | X                          |              250 |                       3.0 |     2.5 |                          30 |                              132 |
| 7 + 136    |    35 | VI                         |              271 |                       3.0 |     1.5 |                          20 |                              285 |
| 7 + 168    |    27 | VIII                       |              280 |                       3.3 |     0.5 |                          32 |                              266 |
| 7 + 194    |    25 | X                          |              281 |                       3.0 |     3.0 |                          18 |                              306 |
| 7 + 218    |    25 | X                          |              279 |                       2.9 |     2.0 |                          24 |                              181 |
| 7 + 266    |    35 | VIII                       |              277 |                       3.0 |     1.0 |                          12 |                              327 |
| 7 + 291    |    30 | VIII                       |              275 |                       3.0 |     2.0 |                          18 |                              306 |
| 7 + 316    |    30 | VIII                       |              271 |                       3.1 |     2.0 |                          16 |                              210 |
| 7 + 342    |    32 | VIII                       |              279 |                      3.15 |     5.0 |                          16 |                              353 |
| 7 + 423    |    35 | BIM                        |              284 |                      3.25 |     2.0 |                           6 |                              377 |
| 7 + 455    |    33 | BIM                        |              285 |                      2.95 |     2.0 |                           8 |                              382 |
| 7 + 531    |    25 | X                          |              250 |                      3.05 |     3.0 |                          46 |                              382 |

A summary of the total wall-to-wall deformations measured in the flysch section is presented in Table 5. Rock support and the installation of the monitoring sections were installed following the excavation face very closely. The distance at which the monitoring section was installed in relation to the face position is defined as ' L ' in Table 5. The relatively short L -distances allowed for the register of most of the deformations occurring behind the face right after a newly opened excavation round. However, some part of these deformations may have not been registered in the monitoring sections, especially in these with L ≥  5 m.

In addition to Table 5, where the total, final magnitude of wall-to-wall convergence is summarized, a plot of the measured convergences over time is presented in Fig. 9 to assist in the interpretation of the deformational behavior of the flysch. The curves in Fig. 9 show a monitoring period during construction that covers about 1 year. As shown in Fig. 9, the curves clearly represent different behaviors as there exist significant variations of both magnitude and deformation development pattern in spite of a nearly similar rock overburden. To identify or associate the registered ground response to ground conditions, two main parts of the deformation curves should be analyzed and related to geological conditions. As such, a first, steep part close to the face that normally corresponds to the instantaneous deformation that occurs as a direct consequence of the excavation or 'removal' of the rock material from the tunnel face. Such three-dimensional, supportive effect of the face lasts about 8 tunnel radii behind the face (Carranza-Torres and Fairhust 2000) for perfectly elastic-plastic material. The latter agrees well with the performed readings provided that the average tunnel excavation rate was 2-3 m per day, and that the influence of the tunnel face is observed to disappear after ca. 8-10 days (Fig. 9). After the first part of instantaneous deformation, a long-term creep (plastic deformation) takes place over time and stabilizes. As a result of such interpretation, three main groups representing three different deformational responses were evaluated and associated to engineering geological descriptions so that the underlying causes of these differences could be explained:

1. Group 1: The two convergence sections in this group correspond to rock mass that are described as bimrock (BIM) containing relatively large proportions of strong rock embedded in the sheared siltstone, contributing to a stiffer behavior of the rock mass. The latter results in relatively low deformations in spite of the remobilized, apparently weak nature of the bimrock. In this case, the total convergence of the tunnel (considering installed rock support) is lower than 0.15%. As seen in the two deformation curves, a significant part (about 75%) of the total deformation occurs in connection to tunnel excavation (time-independent) close to the face while the rest, approx. 25% is time-dependent deformation that occurs far behind the influence of the face. This suggests that the ground behaves more inelastic in relation to groups 2 and 3, which agrees with the rock mass having relatively

Fig. 9 Measured wall-to-wall convergence (closure) as a function of time between first and final measurements

<!-- image -->

Line chart

<!-- image -->

Logo

higher rock mass strength which is due to the presence of a larger fraction of strong members embedded in the ground mass. Because of the spatial and geomechanical heterogeneity of bimrocks, it could also be the case that strong and relatively thick rockslab would be placed above or around the tunnel without being identified at the face, and bridging, therefore, part of the ground loads.

2. Group 2: The seven convergence sections in this group represent rock mass that are composed of deformed, disturbed, and siltstone-dominant flysch rocks, mostly classified as flysch type VIII (Marinos 2017), and GSI between 25 and 35. The relatively wide range of the mapped and estimated parameters GSI, E rm and E i for the involved tunnel sections in this group essentially reflect the high variability and complexity of deformed flysch rock mass. Such variability affects also on the deformational response to excavation, with measured total deformations ranging from 0.2% to 0.4%. In general, the instantaneous or time-independent deformation that results from the excavation of the tunnel face is ca. 2/3 of the total deformation, which means that about 1/3 of the total deformations is time-dependent deformation. The latter behavior is very much in relation to the conditions defined for flysch rock mass type VIII, where the rock mass is essentially weak due to the disturbance produced in the rock mass structure and the dominant proportion of weak siltstone over of strong sandstone.
3. Group 3: This group corresponds to rock mass described mainly as type X in Marinos (2017). Rock masses of this group consist of highly disturbed siltstone-claystone dominated flysch with clear signs of shearing, disturbance and loss of structure. The rock mass under this group contains &lt; 5 cm thin members or remnants of  sandstone  (Fig.  3c).  However,  the  proportion  of weak and tectonized siltstone prevails largely over the embedded strong rock members, which together with a significant loss of rock mass structure, contributed to a considerable reduction of the rock mass strength. These was visually evident while mapping ­ GSI flysch in this rock mass group, with values ranging between 15 and 25. The lower rock mass strength and stiffness of the flysch rock mass in this group in relation to groups 1 and 2, led, therefore, to measured convergences of about 0.5-0.75% (considering tunnel support). From the study of the convergence curves, it is derived that the time-dependent deformation varies between 25% and 50% of the total deformation, which clearly indicates a higher degree of plastic behavior in rock mass types X in comparison with VIII.

<!-- image -->

Icon

## 4   Analysis Methodology

The analysis methodology is based on a combination of ground investigations, deformation monitoring, and calculations performed with analytical and numerical approaches with the aim to investigate ground behavior and support loading. To do so, a case study based on the construction of a headrace tunnel in weak flysch conditions subject to deformations and with permanent rock support based on RRS arches was used.

Four different approaches were used to study ground behavior and support loading. The aim was to compare the results and enable a study of the performance of each method. As such, four widely accepted and commonly used approaches to evaluate deformations in the field of weak ground engineering were used: the analytical CarranzaTorres and Fairhust (2000), Hoek and Marinos (2000), and Panthi and Shrestha (2018), and the numerical approach based on the two-dimensional finite-element program RS2 v.11 (Rocscience 2022). The four approaches consider rock mass that can be described with the Hoek-Brown failure criterion (Hoek and Brown 1980; Hoek et al. 2002) and assume elasto-plastic model behavior of the rock, which enables comparability of the results obtained.

Although some similarities may be found in the four approaches, their performance to prognose ground behavior, the sensitivity to changes in rock mass conditions at the face, and rock support, can differ from approach to approach. From this perspective, the authors believed that with the combination of these four approaches together with numerical verification and back-calculation towards the available deformation monitoring during construction, it may be possible to compare each other to find possible limitations and investigate potential improvements.

To illustrate the main differences and the ability of each of the four methodologies used in this study to describe and estimate plastic deformations, the authors are elaborated in Fig. 10. The figure illustrates a typical longitudinal displacement profile (LDP) of a tunnel excavated in weak rock mass with deformations occurring ahead and behind the face as a function of the distance to the face. The LDP in Fig. 10 is based on the convergence-confinement method (CCM) of Carranza-Torres and Fairhust (2000) and the work of Vlachopoulos and Diederichs (2009). However, it is updated with the input of Goodman (1989) and Shrestha (2014) to reflect the effect of time-dependent plastic deformations. As such, the updated LDP in Fig. 10 can be divided in three main parts. Deformations ahead of the face as defined by the curve O-F, elastic-plastic time-independent deformations as shown by the curve F-A, and time-dependent plastic deformations (curve A-B).

Fig. 10 Schematic illustration of a typical LDP in weak, overstressed ground, considering time-dependent deformations

<!-- image -->

Line chart

For rock engineering purposes, deformations occurring behind the face (time-independent and time-dependent deformations) are normally of most interest as these are to load the ground support. Time-independent deformation occurs as a direct response to tunnel excavation and ends when either the effect of confinement finishes about 8 × tunnel radiuses ( R T ) behind the face, or when the ground reaches equilibrium with the applied rock support (AFTES 2001). On the other hand, time-dependent deformation (long-term creep) occurs after the face effect has disappeared under constant in-situ rock stress condition.

Among the four methods presented above, only the solutions of Carranza-Torres and Fairhust (2000), Vlachopoulos and Diederichs (2009), and the numerical modelling method are able to simulate tunnel behavior defined by the curves O-F-M-A and O-F-M-A-B, respectively. These two methods can determine the amount of tunnel radial displacements occurred ahead of the face ( u f ) , tunnel wall displacements at a monitoring point ( M ) placed at a distance ( L ) from the face ( u m ) , and the time-independent displacements at equilibrium ( u i ) . With the use of a creep function, the numerical approach could additionally evaluate the total tunnel wall displacements (including time-dependent behavior) at point ( B ) in Fig. 10, represented as ( u max ) . The solutions of Hoek and Marinos (2000), Panthi and Shrestha (2018), however, cannot determine the longitudinal deformation profile (LDP) curve, but rather be used to estimate total deformation ( u max ) including the effect of time-independent deformation and time-dependent creep. It should also be emphasized that while in-situ stresses in the solutions of Carranza-Torres and Fairhust (2000) and Hoek and Marinos (2000) are based on a hydrostatic ( K =  1) and circular tunnel shape condition, the Panthi and Shrestha (2018) and the numerical approaches permit the simulation of anisotropic in-situ stress and noncircular tunnel geometries.

Since the study has considered the use of four different approaches that involves a series of input parameters, analysis steps, calculations, and characteristics, a summary of the overall analysis methodology is presented in Fig. 11. It illustrates the interaction in between each of the analysis steps and methods, the workflow, and the details regarding input variables, together with the objectives, and the main analysis steps. Such sketch should be looked in conjunction with detailed explanations provided for each of the separate approaches given in the successive Sects. 4.1-4.4. As such, separate results from each of these approaches are given in the respective Sects. 5.1-5.4 with separate discussions. Similarly, the final and comparative analysis of the results is given in Sect. 6.

## 4.1   Numerical Analyses in 2D

The development of advanced numerical codes and geotechnical software during the last decades has resulted into powerful numerical simulation programs that permit detailed studies of ground behavior and support performance. For the case of highly disturbed flysch rock mass conditions as studied in this article, the rock mass can be considered-and simulated-as isotropic and equivalent continuum media (Vlachopoulos et al. 2020). In that case, numerical codes based on the finite-element method (FEM) are used, since the ground behavior can be then represented and simulated by such codes.

<!-- image -->

Logo

Fig. 11 General methodology for the analysis of plastic deformations and the study of the performance of the involved approaches in tunnels excavated in weak rock mass of flysch

In this study, the numerical calculations were performed with the FEM modelling software RS2 v.11 of Rocscience, a two-dimensional program that permits stress-strain calculations for geotechnical applications. For the case of weak ground numerical modelling, RS2 allows the simulation of tunnel relaxation deformation as a function of the employed ground properties, the characteristics of the support system, and the simulated in-situ stresses. It similarly allows for any excavation geometry and stress anisotropy, as opposed to classical analytical approaches, such as CCM and Hoek and Marinos (2000), which are based on uniform far-field stress and circular tunnel geometries. At the same time, RS2 can be staged in computation steps, so that the rock support is delayed to the actual distance from the face ' L ' at which the support was in reality installed during construction. Among other details, the numerical approach provides a powerful tool to assess the two main parameters that are under investigation in this study, tunnel deformations and rock support performance.

The deformations are calculated by RS2 by solving the simulation to equilibrium between the ground loads associated  to  plasticized  ground  around  the  tunnel  and  the installed-simulated-capacity of the support system. In Sect. 5.1, the calculated deformation results correspond to wall displacements to enable comparison towards the other three approaches used in the study. As such, deformation symmetry was assumed in the RS2 convergence results at each of the two tunnel walls, and the displacement reported as ( u max , p i &gt; 0 ) .

<!-- image -->

Icon

The analysis of the support loading and performance was done through the assessment of support capacity plots and the study of Factor of Safety (FS). Since the modelled tunnel is not circular, the support is not only subject to compressional, axial thrust loads, but also to shear and moment loading. RS2 allows for the analysis of the stability of shotcrete subject to flexure and shear loads, which obviously gives significant insights into the rock support performance if compared to analytical approaches based on support pressure of circular liner supports. As such, the stability condition that defines the performance of the reinforced shotcrete in RS2 is based on the computation of the acting bending moments ( M ) and shear forces ( V ) in relation to the respective moment of resistance ( M R ) and shear resistance ( V R ) of the support, as defined by Eqs. (1) and (2):

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

where ­ FS c-bending is the factor of safety of the reinforced sprayed concrete to fail in bending, M RC  is the moment resistance of the sprayed concrete, ­ FS c-shear is the factor of safety of the sprayed concrete to fail in shear, and V RC  is the shear resistance of the sprayed concrete.

Table 6 Calibrated and weighted rock mass properties in RS2 for the studied tunnel sections 7+ 029-7 + 531

| Chainage   |   GSI |   Weighted E i (GPa) |   E rm (MPa) |   Weighted u1D70E ci (MPa) |   Weighted m i |   u1D70E cm (MPa) |
|------------|-------|----------------------|--------------|----------------------------|----------------|-------------------|
| 7 + 029    |    25 |                   31 |         1856 |                         28 |             10 |              1.67 |
| 7 + 064    |    25 |                   32 |         1915 |                         29 |              9 |              2.64 |
| 7 + 092    |    25 |                   30 |         1795 |                         30 |             10 |              3.24 |
| 7 + 136    |    35 |                   22 |         2495 |                         30 |              9 |              1.95 |
| 7 + 168    |    27 |                   24 |         1618 |                         28 |              8 |              2.21 |
| 7 + 194    |    25 |                   35 |         2095 |                         35 |             13 |              1.65 |
| 7 + 218    |    25 |                   35 |         2095 |                         30 |             11 |              2.01 |
| 7 + 266    |    35 |                   29 |         3289 |                         29 |             10 |              1.74 |
| 7 + 291    |    30 |                   30 |         2604 |                         30 |              9 |              1.75 |
| 7 + 316    |    30 |                   35 |         2848 |                         35 |             12 |              1.59 |
| 7 + 342    |    32 |                   30 |         2782 |                         28 |             10 |              2.22 |
| 7 + 423    |    35 |                   35 |         3969 |                         40 |             14 |              1.74 |
| 7 + 455    |    33 |                   34 |         3370 |                         35 |             13 |              1.41 |
| 7 + 531    |    25 |                   30 |         1795 |                         29 |             11 |              1.25 |

The generalized Hoek and Brown failure criterion and an elastic-plastic material function were utilized to model the weak rock mass of flysch. The employed input for the rock mass properties in the numerical models are based on the testing results (Table 6), weighting of the properties in relation to the relative fraction of weak over strong rock at the tunnel face (Table 1) according to Hoek and Marinos (2000), Hoek et al. (2005) and Marinos (2017), and model calibration. The back-calculated and calibrated rock mass properties of the studied tunnel sections are presented in Table 6.

In total, 14 numerical models were simulated, one for each of the monitored tunnel sections. The model construction or setup is illustrated in Fig. 7. In each model, analyses of the total radial tunnel displacements at equilibrium with support ( u max , p i &gt; 0 ) and FS for the load bearing (RRS) support under bending and shear, ­ FS c-bending and ­ FS c-shear , respectively, were performed. Modelling of composite support as that of RRS arches composed of steel reinforcement bars and shotcrete (Fig. 1) was conducted with the equivalent section approach. This is a procedure that weights the amount of steel, the dimensions of the RRS arches, and the c/c distance of arches to obtain equivalent beam sections that fit in the unitary (1 m) out of plane slice thickness of RS2. The equivalent section approach to model ribs or arches in geotechnical software has been used in similar studies by authors like Donovan et al. (1984), Carranza-Torres and Diederichs (2009), Chryssanthakis (2015) and Høien and Nilsen (2018), and proven satisfactorily. The properties of the rock support material used in numerical models, including RRS, shotcrete and bolts, are summarized in Table 7.

Table 7 Material properties of rock support modelled for RS2 analyses

| Parameter                                      |   Value |
|------------------------------------------------|---------|
| Thickness of simulated shotcrete layer (m)     |    0.25 |
| Compressive strength of sprayed concrete (MPa) |      35 |
| Young`s modulus of sprayed concrete (GPa)      |      30 |
| Tensile strength of sprayed concrete (MPa)     |       5 |
| RRS steel rebar diameter (m)                   |    0.02 |
| Tensile strength of steel reinforcement (MPa)  |     400 |
| Bolt modulus (GPa)                             |     200 |
| Bolt diameter (mm)                             |      19 |
| Bolt tensile capacity (MN)                     |    0.15 |

Although the numerical simulations constitute a rather detailed approach for determining ground behavior and support loading in weak ground, it should be highlighted that the method is not exempt of limitations and simplifications, some of them described in Sect. 3.5. Some of the challenges when using FEM and equivalent isotropic continuum on the basis of GSI and weighted properties of the rock mass in heterogeneous flysch can be also related to issues for capturing the local effect of beds, folds or any other anisotropy in the rock mass. Other challenges may be derived from the presence of rapid variations of the rock mass structure and/or the proportion of strong/weak rock in the tunnel direction. Other limitations may also be related to the inherent uncertainty related to the measurement, registration and interpretation of field/laboratory data such as rock mass properties forming the basis for the input parameters of the numerical models. In that sense, the integration and involvement of different analysis approaches in the study, the comprehensive study of rock properties performed in the laboratory and in the field, and the systematically monitored deformation data are believed to have contributed positively to the identification of possible deviations in the results and to reduce the level of uncertainty.

## 4.2   Carranza-Torres and Fairhust (2000)

The convergence-confinement method (CCM) of CarranzaTorres and Fairhust (2000) is a standard procedure for the analysis of tunnel wall deformation and ground loads in relation to tunnel excavation in weak rock mass that satisfy the Hoek-Brown failure criterion (Hoek and Brown 1980; Hoek and Corkum 2002; Eberhardt 2012). The approach assumes plane strain conditions, isotropic stress field, and circular tunnel geometries. At least, the following three main elements of the CCM are necessary to carry out analyses with this procedure (Fig. 12): the first component is the GRC, which describes the response of the ground deformation to excavation; the second is the Support Characteristic Curve (SCC) that defines the response of the support and its interaction with the ground; and the third one, the LDP, which relates tunnel wall deformations at successive stages in the analysis to the actual physical location along the tunnel axis (Vlachopoulos and Diederichs 2009) as, for example, locations F (face) and M (installation of support behind the face) in Fig. 12.

To simulate tunnel excavation, the internal pressure in the tunnel ( p i ) is gradually reduced from its initial condition before excavation ( p o = p i ) until a final condition in which the ground finds equilibrium at p i = 0 in an unsupported tunnel. In the case of a supported tunnel, an internal support pressure is applied radially ( p i &gt; 0 ) , and the analytical solution allows for the calculation of radial displacements at which the ground finds equilibrium with the support ( u i, p i &gt;0) at point A in Fig. 12, and at a support pressure at equilibrium ( p eq ) . In this study, analysis of ( u i, p i &gt;0) and evaluation of the displacements occurred at the support activation ( u m ) were done. The latter permitted the study of actual displacements acting on the support, so that comparison of the results towards the other employed approaches was enabled. The conducted study has, in addition to calculations of displacements at equilibrium in supported models, analyzed the support performance. This has been done on the basis of a factor of safety (FS) that is defined as the ratio of maximum support pressure to the support pressure required for equilibrium FS = ( p max ∕ p eq ) .

<!-- image -->

Line chart

Fig. 12 Representation of the three elements of the CCM: GRC, SCC and LDP

<!-- image -->

Icon

The method is obviously not exempt of limitations, some of them shared with the other approaches utilized in this study. As noted by Bobet and Einstein (2024), the approach is basically developed for preliminary analyses of wall displacement and ground support loading, to ultimately assist on support design in the preliminary stages of a project. However, this concept is usually misinterpreted by practitioners, and attempts of detailed designs are sometimes performed using CCM. Another challenge is the consideration of uniform and isostatic in-situ stresses, since anisotropic deformations may then not be captured. Limitations are also related to the determination of representative properties for rock mass of flysch, often composed of laminated, sheared alternations of two or more lithologies with different mechanical properties in an analytical solution that considers isotropic and continuum material models. The final limitation is that the method considers only circular shaped tunnel geometries.

## 4.3   Hoek and Marinos (2000)

Hoek (1999) and Hoek and Marinos (2000) presented a prediction method to estimate the potential for tunnel squeezing. The analytical solution is mainly based on the analysis of tunnel case histories from Taiwan, using closed form analytical solutions for circular tunnels from Duncan Fama (1993) and Carranza-Torres and Fairhust (2000). The authors found that the existing correlation between tunnel strain ( ε ), rock mass strength ( u1D70E cm ) and a hydrostatic stress ( p o ) can be defined by Eq. (3) for unsupported tunnels, and Eq. (4) for supported tunnels considering an internal support pressure p i , in which σ cm is defined by the following equation:

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

where support pressure p i is  determined  following  the approach of Hoek (1999), u1D70E ci is the uniaxial compressive strength of intact rock, and m i the material constant of the intact rock in the Hoek and Brown failure criterion (Hoek et al. 2002).

In this study, tunnel strain has been calculated for each of the monitored tunnel sections. From such calculation, it was then derived tunnel convergence, since the tunnel span is known. By assuming deformation symmetry at both walls, the wall displacement for supported tunnel was analyzed. As for the CCM, the Hoek-Marinos (2000) approach is also based on Hoek and Brown failure criterion for the description and characterization of rock mass. The major limitation of this method is that the analytical solutions presented in Eqs. (3) and (4) are based on circular tunnels subject to hydrostatic stresses ( K =  1) and the tunnel support pressure is simulated radially and evenly. In addition, the method does not permit the direct assessment of support loading and performance. Instead, the results of ground behavior in the form of tunnel strain are normally used as a basis for further interpretations of squeezing potential to ultimately perform correlations towards possible stability problems and design recommendations (Hoek and Marinos 2000).

## 4.4   Panthi and Shrestha (2018)

The solution of Shrestha (2014) and Panthi and Shrestha (2018) is based on the curve fitting models of Sulem et al. (1987a, b), and adjusted to actual rock mass conditions-and measurements-made on very poor, weak rock mass in Himalayan rocks affected by plastic deformations. Based on up to 24 tunnel sections placed in three different tunnel projects subject to squeezing ground, the authors established a correlation to determine instantaneous (time-independent) and final, time-dependent deformations on the basis of rock mass strength and deformability properties, in-situ stresses, and tunnel support pressure, as illustrated in Fig. 13. As shown in the two regression curves, reasonably high coefficients of correlation were obtained, suggesting a good level of correlation and accuracy of the models to predict the outcome of the observed data (tunnel strain) based on the mentioned engineering geological variables. Ultimately, the authors validated the proposed analytical correlation models from the computation and fitting of parameters describing time dependency, stresses and ground properties in the Sulem et al. (1987a, b) solution, to actual deformation monitoring curves from the tunnel. For this purpose, several hundreds of set belonging to the mentioned parameters were randomly generated in a spreadsheet and the best set chosen according to the least sum of square errors (Panthi and Shrestha 2018).

Fig. 13 Correlation of instantaneous and final tunnel strain (%) as a function of rock mass deformability, support pressure and stress state based on the work of Shrestha (2014) and Panthi and Shrestha (2018) in weak rock mass of Himalaya

<!-- image -->

Line chart

On the basis of the obtained correlations, Panthi and Shrestha (2018) derived the respective Eqs. (6) and (7) for the estimation of time-independent (or instantaneous) and time-dependent (or final) tunnel strain, nominated as (ε IC ) and (ε FC ) ,  respectively. As opposed to the classical approaches presented in Sects. 4.2 and 4.3, the proposed analytical equations permit the simulation of anisotropic stresses ( K ≠  1) along with the assessment of time-dependent deformations. The solution provides, therefore, a valuable analytical tool for weak ground engineering, as it introduces the possibility of accounting for non-uniform stresses and time-dependent behavior, two relevant parameters for tunnel stability assessment:

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

where strain ( ε ) represents the tunnel closure in percentage (%), (σ V ) is the vertical, gravitative stress, ( K ) is the ratio of horizontal to vertical stress, ( p i ) is the support pressure, ( G rm ) is the rock mass shear modulus, and ( E rm ) is the deformation modulus of the rock mass. Calculation of G rm is done as suggested by Carranza-Torres and Fairhust (2000) in Eq. (8), while E rm and u1D70E cm calculated from the respective Eqs. (9) and (10) as suggested by Panthi (2006), Hoek and Brown (1997), and Panthi and Shrestha (2018):

<!-- formula-not-decoded -->

<!-- image -->

Icon

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

where E i is the elastic modulus of the intact rock, ( c ) is the cohesion of the rock mass, and ( ϕ ) is the internal friction angle of the rock mass.

From applying this approach in the fourteen tunnel sections of this study, time-independent and time-dependent plastic deformations were evaluated for the supported tunnel. The respective tunnel strain (ε IC ) and (ε FC ) are represented by points A and B in Fig. 10, and converted then to radial inward displacements by assuming deformation symmetry in both tunnel walls. The back-analyzed in-situ stress state in Table 4 was used to derive the actual K -ratio to be used for the application of the Panthi and Shrestha (2018) solution. One of the main limitations of this approach like other two is related to the reduced ability to consider a delayed, sequential activation of rock support. This is because the tunnel support pressure in the analytical solution is applied instantaneously right after the excavation at the face. Another limitation of this solution is the lack of possibilities to make a direct analysis of the support loading and support stability against failure.

Table 8 Results of calculated tunnel wall displacements in RS2 for the tunnel sections 7  +  029-7  +  531

<!-- image -->

Icon

## 5   Analysis Results

## 5.1   Numerical Analyses in 2D

The results of the numerical analyses performed in RS2 are presented in Table 8. Definition of the rock mass properties and in-situ stresses in the models were primarily based on the calibrated rock mass properties and in-situ stresses presented in Tables 4 and 6, respectively. The results present the wall displacements at equilibrium ( u max , p i &gt; 0 ) with a tunnel rock support based on RRS arches as permanent, final rock support as described in Sect. 2. The wall displacements have been calibrated to suit the measured tunnel deformations (Table 5). This served to both calibrate the rock mass properties used in all the models/approaches of this study, and indeed to obtain representative results of support loading.

In general, the level of wall displacements is considered relatively low in relation to the poor and weak ground conditions. One explanation may be the careful excavation sequence with 2-3 m long passes, avoiding unnecessary rock relaxation. Another supplementary explanation may also be the strengthening/stiffening effect of the strong sandstone members on the overall behavior of rock mass. As a consequence, relatively low deformations and limited loading on the support were observed by looking at FS for bending and shear failure. Note that the plotted FS in Table 8 are based on the minimum values registered in the results of the support capacity diagrams. In general, a rather stable support condition is interpreted from the deformation and support loading results presented in Table 8.

| Chainage   |   GSI |   Weighted u1D70E ci (MPa) |   E rm (MPa) |   u1D70E V (MPa) |   ( u i, p i >0) (mm) |   FS c-bending |   FS c-shear |
|------------|-------|----------------------------|--------------|------------------|-----------------------|----------------|--------------|
| 7 + 029    |    25 |                         28 |         1856 |              5.7 |                    17 |              2 |            8 |
| 7 + 064    |    25 |                         29 |         1915 |              6.0 |                    15 |            1.3 |            4 |
| 7 + 092    |    25 |                         30 |         1795 |              6.3 |                    12 |            2.5 |            6 |
| 7 + 136    |    35 |                         30 |         2495 |              6.8 |                    12 |            1.5 |            3 |
| 7 + 168    |    27 |                         28 |         1618 |              7.0 |                    17 |            1.5 |            2 |
| 7 + 194    |    25 |                         35 |         2095 |              7.0 |                    11 |              2 |          3.5 |
| 7 + 218    |    25 |                         30 |         2095 |              7.0 |                    16 |              2 |          3.5 |
| 7 + 266    |    35 |                         29 |         3289 |              6.9 |                     6 |              3 |            4 |
| 7 + 291    |    30 |                         30 |         2604 |              6.9 |                    12 |            1.7 |            4 |
| 7 + 316    |    30 |                         35 |         2848 |              6.8 |                     8 |            2.5 |            6 |
| 7 + 342    |    32 |                         28 |         2782 |              6.8 |                     8 |            2.5 |            6 |
| 7 + 423    |    35 |                         40 |         3969 |              7.1 |                     4 |              2 |            4 |
| 7 + 455    |    33 |                         35 |         3370 |              7.1 |                     7 |              2 |            4 |
| 7 + 531    |    25 |                         29 |         1795 |              6.3 |                    23 |              2 |          3.5 |

Table 9 Summary of tunnel wall displacements determined by Carranza-Torres and Fairhust (2000)

| Chainage   |   E rm (MPa) |   Weighted u1D70E ci (MPa) |   Support pressure ( p i ) (MPa) |   L (m) |   u m (mm) |   ( u i, p i >0) (mm) |   FS of support |
|------------|--------------|----------------------------|----------------------------------|---------|------------|-----------------------|-----------------|
| 7 + 029    |         1856 |                         28 |                              2.0 |       2 |       40.5 |                    51 |             7.3 |
| 7 + 064    |         1915 |                         29 |                              2.0 |       1 |       31.1 |                    46 |             4.9 |
| 7 + 092    |         1795 |                         30 |                              1.6 |     2.5 |       55.6 |                  69.5 |               8 |
| 7 + 136    |         2495 |                         30 |                              1.6 |     1.5 |         26 |                    40 |             4.8 |
| 7 + 168    |         1618 |                         28 |                              1.6 |     0.5 |         47 |                    68 |             2.8 |
| 7 + 194    |         2095 |                         35 |                              1.6 |     3.0 |       48.8 |                  62.2 |             6.4 |
| 7 + 218    |         2095 |                         30 |                              1.6 |     2.0 |         46 |                  64.4 |             5.1 |
| 7 + 266    |         3289 |                         29 |                              1.4 |     1.0 |       15.2 |                    26 |             3.6 |
| 7 + 291    |         2604 |                         30 |                              2.0 |     2.0 |       35.3 |                  53.4 |             6.6 |
| 7 + 316    |         2848 |                         35 |                              1.6 |     2.0 |         19 |                    33 |             6.2 |
| 7 + 342    |         2782 |                         28 |                              2.0 |     5.0 |       49.7 |                  62.9 |               9 |
| 7 + 423    |         3969 |                         40 |                              1.6 |     2.0 |       11.1 |                  20.7 |               7 |
| 7 + 455    |         3370 |                         35 |                              1.6 |     2.0 |         16 |                    27 |             6.4 |
| 7 + 531    |         1795 |                         29 |                              1.4 |     3.0 |       56.9 |                    64 |             6.5 |

## 5.2   Carranza-Torres and Fairhust (2000)

subtracted ( u m ) to ( u i, p i &gt; 0 ) , so that comparison is enabled to, for example, the RS2 results.

Based on the Carranza-Torres and Fairhust (2000) approach, tunnel deformations have been calculated (Table 9). As such, the displacements at support installation ( u m ), and the radial displacement at equilibrium ( u i, p i &gt; 0 ) with supported tunnel were derived. In that regard, it should be highlighted that ( u i, p i &gt; 0 ) corresponds  to  the  total  deformation  at equilibrium with the support, but not to the actual deformations acting and loading on the support. To derive the actual deformation acting on the support, it should then be As shown in Table 9, both the level of calculated displacements with supported tunnel ( u i, p i &gt;0) and the FS are rather sensitive to the rock mass conditions, to the applied support, and to the distance ' L ' at which the support is activated in relation to the face position. As such, tunnel sections presenting stiffer, stronger rock mass or tunnel sections with delayed support (i.e., 7 + 342) usually led to declining levels of displacements and less loads on the rock support.

Based on the results, the Carranza-Torres and Fairhust (2000) approach seems to be a robust application in flysch rock mass. However, some limitations were also identified. The first is related to the circular tunnel geometry, which poses a clear limitation when addressing rock support loading and FS of tunnel support. As a consequence, relatively high values of FS were obtained due to the simulated circular supports taking loads mainly in compression.

Table 10 Summary of calculated tunnel strain ε (%) and u max after Hoek and Marinos (2000)

| Chainage   |   GSI |   p o (MPa) |   Weighted m i |   Weighted u1D70E ci (MPa) |   u1D70E cm (MPa) |   Support pres- sure p i (MPa) |   ε ( p i =0) (%) |   u max ( p i =0) (mm) |   ε ( p i >0) (%) |   u max ( p i >0) (mm) |
|------------|-------|-------------|----------------|----------------------------|-------------------|--------------------------------|-------------------|------------------------|-------------------|------------------------|
| 7 + 029    |    25 |         5.7 |             10 |                         28 |              1.67 |                            2.0 |              2.72 |                     88 |               0.5 |                     16 |
| 7 + 064    |    25 |         6.0 |              9 |                         29 |              2.64 |                            2.0 |              3.17 |                    101 |               0.6 |                     19 |
| 7 + 092    |    25 |         6.3 |             10 |                         30 |              3.24 |                            1.6 |              2.89 |                     87 |              0.87 |                     26 |
| 7 + 136    |    35 |         6.8 |              9 |                         30 |              1.95 |                            1.6 |              1.78 |                     53 |              0.68 |                     20 |
| 7 + 168    |    27 |         7.0 |              8 |                         28 |              2.21 |                            1.6 |              4.61 |                    138 |              1.39 |                     42 |
| 7 + 194    |    25 |         7.0 |             13 |                         35 |              1.65 |                            1.6 |              1.98 |                     59 |              0.76 |                     23 |
| 7 + 218    |    25 |         7.0 |             11 |                         30 |              2.01 |                            1.6 |              3.23 |                     94 |              1.07 |                     31 |
| 7 + 266    |    35 |         6.9 |             10 |                         29 |              1.74 |                            1.4 |              1.80 |                     54 |              0.79 |                     24 |
| 7 + 291    |    30 |         6.9 |              9 |                         30 |              1.75 |                            2.0 |              2.69 |                     81 |              0.69 |                     21 |
| 7 + 317    |    30 |         6.8 |             12 |                         35 |              1.59 |                            1.6 |              1.41 |                     44 |              0.57 |                     18 |
| 7 + 342    |    32 |         6.8 |             10 |                         28 |              2.22 |                            2.0 |              2.29 |                     72 |              0.61 |                     19 |
| 7 + 423    |    35 |         7.1 |             14 |                         40 |              1.74 |                            1.6 |               1.1 |                     23 |              0.36 |                     12 |
| 7 + 455    |    33 |         7.1 |             13 |                         35 |              1.41 |                            1.6 |              1.16 |                     34 |              0.52 |                     15 |
| 7 + 531    |    25 |         6.3 |             11 |                         29 |              1.25 |                            1.4 |              2.77 |                     85 |              0.99 |                     30 |

<!-- image -->

Icon

## 5.3   Hoek and Marinos (2000)

The results from applying the Hoek and Marinos (2000) approach to the fourteen tunnel sections is presented in Table 10. Accordingly, tunnel strain ( ε )  using unsupported  tunnel  ( ε ( p i =0))  and  supported  tunnel  ( ε ( p i &gt;0)) conditions were performed for the tunnel sections under study. In this calculation, the final support that is described in Sect. 2 based on RRS arches in flysch was simulated. To derive tunnel wall displacements ( u max ), deformation symmetry was also considered in this study, on the basis that Hoek-Marinos (2000) approach only gives tunnel strain, that can be related to convergence, provided that the tunnel span is known.

On the other hand, it should also be noted that the level of tunnel strain for the supported tunnel condition is mainly between 0.5% and 1%, and only in one tunnel section the strain goes above 1% (7 + 168). According to Hoek and Marinos (2000), tunnel strain less than 1% can be categorized as minor squeezing problems. This categorization indeed agrees with the preliminary estimation of ground behavior in the assessment of ground failure mechanisms performed in Sect. 3.3 and Fig. 5. On this basis, the Hoek and Marinos (2000) approach proposes design recommendations of potential support solutions for such conditions, consisting mainly of lean arches combined with shotcrete and bolts. The latter agrees well with the design done in the headrace tunnel, where the support was basically formed of RRS arches, a rather flexible solution if compared to the heavy and stiff steel arches that are normally used in squeezing ground.

## 5.4   Panthi and Shrestha (2018)

As observed in Table 10, the application of support pressure p i in  the tunnel has a direct influence on the resulting radial maximum inward displacement ( u max ). However, it should be noted that p i in  the  solution of Hoek and Marinos (2000) is simulated directly upon tunnel excavation, at point F in Fig. 10. Hence, without the effect of a delayed support installed at a distance ' L ' from the face. Such approach may seem conservative as deformation between the face and the support is also accounted in this solution.

The results from applying the Panthi and Shrestha (2018) approach to the 14 tunnel sections is presented in Table 11. Accordingly, tunnel strain ( ε ) using supported tunnel conditions for both the instantaneous (time-independent) and final (time-dependent) were calculated and converted to radial inward displacements by assuming that the tunnel closure is distributed symmetrically in both tunnel walls. In this calculation, the final support that is described in Sect. 2 based on RRS arches as permanent rock support in flysch, was simulated.

As observed in Table 11, the calculated radial displacements  are  rather  dependent  on  the  applicated  support pressure ( p i ) , the in-situ stress conditions and the rock mass properties. This is in line with the previous analytical methods used, Carranza-Torres and Fairhust (2000) and Hoek and Marinos (2000). However, if the methods from Panthi and Shrestha (2018) and the CCM are compared, the latter approach considers the effect of a delayed rock support installation when calculating radial displacement. A delayed support with respect to the tunnel face can lead to missing one part of the instantaneous deformation, as represented by the section F-M in Fig. 10.

Table 11 Summary of calculated plastic deformations after Panthi and Shrestha (2018)

| Chainage   |   E i (MPa) |   u1D70E V (MPa) |   In plane u1D70E h (MPa) |   Weighted u1D70E ci (MPa) |   u1D70E cm (MPa) |   Support press. p i (MPa) |   u IC ( p i > 0) (mm) |   u FC ( p i > 0) (mm) |
|------------|-------------|------------------|---------------------------|----------------------------|-------------------|----------------------------|------------------------|------------------------|
| 7 + 029    |          31 |              5.7 |                       3.5 |                         28 |              1.67 |                        2.0 |                   13.9 |                   26.2 |
| 7 + 064    |          32 |              6.0 |                       3.6 |                         29 |              2.64 |                        2.0 |                   11.8 |                   22.4 |
| 7 + 092    |          30 |              6.3 |                       3.7 |                         30 |              3.24 |                        1.6 |                   12.8 |                   24.3 |
| 7 + 136    |          22 |              6.8 |                       3.9 |                         30 |              1.95 |                        1.6 |                   17.2 |                   32.4 |
| 7 + 168    |          24 |              7.0 |                       4.0 |                         28 |              2.21 |                        1.6 |                   26.6 |                   49.8 |
| 7 + 194    |          35 |              7.0 |                       4.0 |                         35 |              1.65 |                        1.6 |                   15.8 |                   29.8 |
| 7 + 218    |          35 |              7.0 |                       4.0 |                         30 |              2.01 |                        1.6 |                   22.5 |                     21 |
| 7 + 266    |          29 |              6.9 |                       3.9 |                         29 |              1.74 |                        1.4 |                   13.4 |                   25.3 |
| 7 + 291    |          30 |              6.9 |                       3.9 |                         30 |              1.75 |                        2.0 |                   12.6 |                   23.9 |
| 7 + 316    |          35 |              6.8 |                       3.9 |                         35 |              1.59 |                        1.6 |                    9.3 |                     18 |
| 7 + 342    |          30 |              6.8 |                       3.9 |                         28 |              2.22 |                        2.0 |                    7.7 |                   14.8 |
| 7 + 423    |          35 |              7.1 |                       4.0 |                         40 |              1.74 |                        1.6 |                    6.2 |                     12 |
| 7 + 455    |          34 |              7.1 |                       4.0 |                         35 |              1.41 |                        1.6 |                      7 |                   13.4 |
| 7 + 531    |          30 |              6.3 |                       3.7 |                         29 |              1.25 |                        1.4 |                   15.8 |                   29.7 |

<!-- image -->

Icon

Since the Panthi and Shrestha (2018) approach considers instantaneous application of p i at the face, it is important to isolate the support pressure used for instantaneous tunnel strain calculation from the support pressure restraint by the rock support. Hence, to determine the effect of a rock support in the analytical solution of Panthi and Shrestha (2018), an additional analysis was conducted. Such analysis has respected the structure of the analytical formulation used in Panthi and Shrestha (2018) and has consisted of the calculation of tunnel strain at the face ( L =  0) from the application of the CCM approach, and compared the results with the tunnel strain that was measured in the tunnel behind the face at approximately L =  2  ±  1 m. By comparison of the respective trendlines (Fig. 14), it is observed that in weak rock mass experiencing ca. 1% of tunnel strain, the proportion of tunnel strain not registered between the face and the support varies from approximately 25-50%.

## 6   Discussion

The study of the ground behavior and support performance in the headrace tunnel excavated in flysch weak rocks with Q 0.1-1 and ­ GSI flysch 15-35 has enabled the assessment of the performance of four methodologies that are often employed for the study of plastic deformations in tunnels. The study has also permitted the identification of the main advantages and limitations of these approaches when applied to flysch ground conditions of the type VIII and X (Marinos 2014). The latter suggests the involvement of more elaborated approaches to evaluate ground behavior and permanent tunnel rock support design in flysch, based on a rational combination of the presented approaches together with detailed rock mass characterization, deformation monitoring, and advanced numerical modelling.

On the basis of an integrated, hybrid approach, where several methods are utilized, the permanent rock support design in the headrace tunnel consisted of only RRS arches as final support, with the no addition of cast concrete lining solutions. The latter approach permitted the design verification of the leaner and more cost-effective RRS-support solution, if compared to the traditional, mandatory cast concrete lining that is often recommended from the joint use of analytical approaches and the principles of the weak ground engineering.

To illustrate the comparative performance of the four employed approaches of this study, the results in terms of wall displacements along the studied tunnel section have been plotted in Fig. 15. As observed, the calculated displacements are, in general, sensitive to the input parameters in all of the employed approaches, as so denoted by the nearly parallel distribution of curves. On the other hand, it is also noticed a declining performance in the three analytical approaches, when subject to tunnel sections with more disturbance and higher heterogeneity. This was observed from the existing greater match between calculated and measured displacements found at tunnel section 7 + 455 to 7 + 531, which remarkably represents a tunnel section, where less variability and a more homogeneous ground condition were found (Fig. 4). The latter confirms the existing difficulties for determining representative rock mass properties in deformed and heterogeneous flysch presenting variable proportions of strong over weak rock, as also noted by Marinos and Hoek (2001a, b).

Fig. 14 Effect of a delayed installed support on the magnitude of registered tunnel strain based on the work of Panthi and Shrestha (2018)

<!-- image -->

Line chart

<!-- image -->

Logo

Fig. 15 Comparison of calculated and measured tunnel displacements (with rock support) in the study section

<!-- image -->

Line chart

In Fig. 15, it is similarly observed that the greater match between measured and calculated behavior is obtained with the employment of numerical analyses in RS2. In reality, this is a rather logical result, since the back-calculations were performed against actual deformation monitoring, for the necessary calibrations of the rock mass properties in the study. In that sense, it may be argued that the curve for numerical calculations in Fig. 15 does not reflect true performance in comparison with the analytical approaches. In the light of this discussion, it should be then highlighted that such calibration process is done on the basis of deformation measurements that are only available during construction. It follows then that the predictions of ground behavior will be intrinsically dependent on the amount of site investigations done and the available input for ground characterization, and for that reason it is important to understand the premises and limitations of each of utilized approaches.

In looking to predictions done with Hoek and Marinos (2000) in Fig. 15, it seems that the solution has the tendency of over-representing tunnel displacements, as so it does the Panthi and Shrestha (2018) solution for the final deformations ( u FC ) . However, it should be noted that according to Fig. 10, these two solutions predict long-term, time-dependent deformations, a behavior that has not been especially developed in the headrace tunnel under study (Fig. 9). Both of these solutions present also limitations to simulate tunnel supports installed some meters behind the face, which would in theory lead to an over-representation of the calculated wall displacements if compared to the CCM and the RS2 analyses.

<!-- image -->

Icon

If the respective curves for the CCM and the Panthi and Shrestha (2018) for time-independent deformation deformations ( u IC ), are studied, it is observed that the predictions done are rather good in relation to the measured and numerically calculated displacements in Fig. 15. Both, CCM and Panthi and Shrestha (2018) for ( u IC ) apparently follow the changes in the ground conditions. However, it seems that the CCM of Carranza-Torres and Fairhust (2000) tends to over-represent deformations at tunnel sections with increasing overburden, while the Panthi and Shrestha (2018) seems to capture best the effect of changing overburden/in-situ stresses.

Hence, the authors believe that to address ground behavior with the purpose of tunnel stability and predictions of tunnel support performance, study of the support loading should also accompany this type of assessments. Otherwise, predictions of tunnel ground behavior in the form of radial displacements in tunnel wall as presented in Sects. 5.2, 5.3, and 5.4 should be only considered to give an insight into the general behavior to assist during preliminary design work. For this reason, the FS calculated with the CCM approach and RS2 have been plotted in Fig. 16. The FS for CCM defines the failure condition of the support in relation to support pressure in a circular tunnel geometry and under uniform in-situ stresses, whist that of RS2 considers the support stability subject to both flexural and shear loading as a result of an anisotropic stresses and a non-circular tunnel.

The latter poses an important effect in the manner FS is calculated, hence on the type and magnitude of support loading, which is then observed in the form of an overrepresentation of FS for the CCM approach in relation to RS2 (Fig. 16). Such over-representation of FS in the CCM may create a false sensation of stability during design work, therefore, likelihood for undersupported tunnel sections.

Fig. 16 Comparison of calculated FS in CCM and RS2 in the study section

<!-- image -->

Line chart

Table 12 Summary the performance of four different approaches to assess plastic deformations in tunnels excavated in deformed flysch

| Performance                                                    | Carranza-Torres and Fairhust (2000)   | Hoek and Mari- nos (2000)   | Panthi and Shrestha (2018)   | 2-D FEM RS2   |
|----------------------------------------------------------------|---------------------------------------|-----------------------------|------------------------------|---------------|
| Interaction with support pressure p i                          | A                                     | B                           | B                            | A             |
| Evaluation of time-independent deformations                    | A                                     | C                           | A                            | B             |
| Evaluation of creep, time-dependent deformation                | B                                     | A                           | A                            | B             |
| Considers tunnel geometries other than circular                | C                                     | C                           | B                            | A             |
| Considers stress conditions other than hydrostatic             | B                                     | C                           | A                            | A             |
| Considers rock mass medium other than isotropic                | C                                     | C                           | C                            | B             |
| Possibility to delay rock support activation (as per LDP)      | A                                     | C                           | C                            | A             |
| Ground reaction curve is determined                            | A                                     | C                           | C                            | A             |
| Ground support performance and stability (FS) can be evaluated | B                                     | C                           | C                            | A             |

Such likelihood  in  the  headrace  tunnel  under  study  is approximately quantified by the grey area marked between the optimistic FS for the CCM curve and the minimum FS obtained in RS2 for moment loading of RRS support. The latter basically suggests that FS in the CCM should basically be used as an approximation of the support stability condition. However, additional, supplementary methodologies such as elaborated RS2 calculations should be performed in weak ground conditions such as flysch to realize detailed studies of support performance, as suggested in Langford et al. (2015).

On the basis of the performed analyses and the comparative assessment of the results throughout Sect. 5 and Figs. 15 and 16, the authors have developed a matrix which provides a summary of the performance of each of the methods utilized in this study to evaluate plastic deformations (Table 12). It can provide insight into best possible combinations of approaches in relation to the ground conditions and expected ground behavior. In addition, it is principally intended as a supplementary guideline for practitioners for the evaluation of the deformational behavior of weak flysch rocks at any stage of a tunnel project.

## 6.1   Validity of Results

The present study is based on the application of a significant number of numerical analyses and analytical solutions to study the stress-strain behavior of weak, overstressed rock mass. As such, displacements were studied to evaluate ground behavior, and FS to assess the tunnel rock support loading condition. In view of this, the assumed rock mass failure criterion used in both RS2 and in the analytical approaches are well-known approaches for this type of analysis in such ground conditions. In the same context, it is assumed that the input rock mass properties are representative of the ground conditions and that, in consequence, the detail level in the models comply with that of the study purpose. It should be then noted that simplification is normally accepted in rock mechanics modelling as long as the behavior is captured realistically (Starfield and Cundall 1988) as it is the case of this study (Fig. 15).

<!-- image -->

Icon

It should similarly be highlighted that, as mentioned in Sect. 3.5, representativity or uncertainty are believed to have been improved in relation to the comprehensive study performed in this article, including a through site investigation program, deformation monitoring, and advanced back-calculations with numerical analyses. As suggested in TerronAlmenara et al. (2023), the combination and involvement of different investigation and design approaches can contribute to minimize possible deviations and uncertainties in both the calculations and the results, as so observed in the output of the present study.

Although the four analysis approaches utilized are principally built upon the premises of the Hoek-Brown criterion and elastic-plastic material functions for weak ground conditions, it is noteworthy that their level of applicability and compatibility towards weak flysch may not be necessarily equal. As these approaches were developed for varying geological conditions, it is likely that part of the observed mismatch (or match) in the result plots (Figs. 15 and 16) be related to such geological background. Based on the reasonable agreement observed in the results, and on the constitutive models behind each of the utilized methods, it can be said that there are no major conflicts or biases between these methodologies. In that sense, it should also be noted that the basis upon which the Carranza-Torres and Fairhust (2000), Hoek and Marinos (2000), and Panthi and Shrestha (2018) methods rely upon best-fit curves built from data sets that presumably cover distinct geological conditions in the context of weak rock mass. With this in mind, practitioners should be aware about the possible limitations related to the combination of methods. Hence, further application and testing of the proposed hybrid methodology with more case studies in flysch rock mass will definitely enhance the knowledge and reduce biases.

It should be finally noted that the ground behavior and stability conditions established for this headrace tunnel in flysch are the direct consequence of the prevailing characteristics and ground conditions of the project. That is, a horseshoe geometry, a 6.5 m span tunnel excavated in disturbed, nearly isotropic rock mass of flysch type VIII and X, a vertical confinement of ca. 7 MPa, a K -ratio of 0.5, and final support based on RRS arches. The findings and the results presented in this article are, therefore, representative of these conditions, as explained in Sect. 3.5. As a result, the derived design optimizations and proposed recommendations in this study should only be used in other tunnel projects with comparable flysch conditions, and mainly as a design guideline or as a benchmark for research.

<!-- image -->

Logo

## 6.2   Significance of the Findings

In this study, it has been shown that with a more elaborated, combined, hybrid application of analytical methods, numerical analyses, and comprehensive characterization of the ground behavior, optimization of support design can be achieved. Such approach is in line with a hybrid method proposed by Terron-Almenara et al. (2023) for weak rock mass with quality Q &lt;  1 that suggests the involvement of several analysis and design procedures to evaluate ground behavior and adequate, optimal designs of permanent support. The more elaborated work that follows such hybrid procedure obviously requires-a priori-more time and resources to characterize ground properties, apply an observational approach based on deformation monitoring, and to conduct more detailed analyses. However, such initial work would be rapidly compensated by the significant economic savings derived from the reduction of unnecessarily heavy and cost-ineffective support systems such as concrete linings. As a direct consequence of the involvement of approaches such  as  CCM,  FEM,  Hoek-Marinos  (2000),  and  Panthi-Shrestha (2018), weak rock mass other than flysch may also be described-and characterized-with the proposed hybrid approach as the four involved methodologies consider Hoek-Brown failure criterion and elastic-plastic material. In practical terms, this means that the proposed approach may also be applied to other rock mass than flysch as long as the rock mass satisfy the premises of the Hoek-Brown criterion.

Fig. 17 Comparison of rock support consumption for two permanent rock support alternatives, based on two different approaches for tunnel  design  and  construction  in  weak  flysch  rock  mass  of  quality Q 0.1-1 and ­ GSI flysch  15-35

<!-- image -->

Bar chart

To illustrate the potential gain or the benefit of conducting such integrated, more elaborated characterization/analysis work, Fig. 17 has been prepared. The graph shows the rock support consumption related to the construction of 500 m long tunnel section in weak flysch types VIII-X with the two approaches. One approach representing the traditional practice based only on analytical approaches followed by mandatory cast concrete lining. In addition, the other approach based on the involvement of several and more elaborated approaches, and on the integration of the principles of hard rock tunnelling with that of weak ground engineering, to find optimization of permanent tunnel support. As such, the 'traditional practice' alternative considers support material consumption for the temporary support during excavation based on shotcrete, bolts, and lean arches, together with a final, 0.3 m thick steel reinforced full profile cast concrete liner. On the other hand, the 'hybrid' alternative considers an initial support composed of shotcrete, bolts, and RRS arches, supplemented by additional RRS arches that are incorporated into the permanent, final rock support, as illustrated in Fig. 1.

As observed, the utilization of the traditional approach with no incorporation of the temporary support into the final support involves the construction of a reinforced cast concrete lining, which design to cope with the deformations registered in the flysch section, ends up in about 6 ­ m 3 of cast concrete per meter of tunnel (total 2875 ­ m 3 ) and a relatively high amount of steel reinforcement (4410 tons). The latter is about 30 and 4 times greater than the respective consumptions for the hybrid alternative. In turn, the hybrid alternative bases the final support design in shotcrete, bolts and reinforced arches (RRS), which results in a higher consumption of shotcrete and bolts, about 2.3 and 1.8 times higher, respectively. Overall, if these amounts are priced, the relative cost ratio for the respective alternatives 'traditional practice' to 'hybrid approach' results in about 1.25:1. The latter is a conservative figure, since it does not consider the pricing for the formworks necessary in the cast concrete lining solution, nor the saving of equivalent construction time and the intrinsic saving of carbon footprint associated to higher concrete and steel consumptions in the traditional approach.

## 7   Recommendations

The performance and limitations of classical approaches to perform analyses of tunnel deformation and tunnel support stability in weak flysch rock have been studied in Sects. 5 and 6. Based on the results and the arguments explained throughout this article, the following recommendations can be made:

- (1) In tunnel projects subject to weak ground conditions and plastic deformations, the analysis of ground behavior should consider the combination of numerical and analytical approaches with deformation monitoring and a comprehensive ground characterization. This would allow comparison of the results to evaluate whether the results are representative, hence provide a better basis for the design of optimal tunnel supports. In that sense, the utilization of the matrix presented in Table 12 is recommended.
- (2) In disturbed and heterogeneous flysch ground, a comprehensive characterization of the properties of weak and strong members together with their relative proportion over the face should be done. This is important as a detailed weighting of the rock mass properties that are used as input in the analytical and numerical models can be performed. In that sense, several testing and site investigation approaches should be done both at the tunnel face and in the laboratory so that the results are verified and calibrated.
- (3) In weak, disturbed flysch rock mass, the rock mass quality assessment is recommended to be made using at least, two classification systems. The joint use of both, the Q system (Barton et al. 1974; NGI 2015) and ­ GSI flysch  (Marinos 2014, 2017) is recommended to better describe rock mass quality condition and geotechnical behavior. As it concerns the description and characterization of weak flysch compared to other weak rock mass of similar nature, this recommendation may also be applicable to weak ground conditions in general as long as these rock mass satisfy the premises of the Hoek-Brown criterion.
- (4) Whenever possible, it is recommended that any assessment of plastic deformations and tunnel support stability done with the four approaches presented in Sect. 4, are supplemented and verified with systematic deformation monitoring. Measurement and/or a detailed characterization of the in-situ stress state should be performed, since this parameter has a great influence in the magnitude and distribution of stresses around the tunnel, hence on the magnitude, symmetry, and characteristics of the loads affecting the support.
- (5) Although the Hoek-Marinos (2000) approach can give good predictions on the approximate level of expected tunnel deformation in flysch, the use of CCM, and Panthi and Shrestha (2018) solution for instantaneous deformations, and numerical analyses are recommended for the assessment of ground behavior and tunnel support in weak flysch.
- (6) In weak rock mass of flysch type VIII and X, rock mass quality Q 0.1-1, and ­ GSI flysch 15-35, and subject to mild-moderate levels of stress, mild to moderate plastic deformations (tunnel strain around 1%) and slaking

<!-- image -->

Icon

- properties in siltstones may be expected. Under such situation, permanent rock support in the form of shotcrete, bolts and RRS arches should be considered as a functional, valid permanent support alternative to the uneconomical and often mandatory cast-concrete lining solution, as suggested in the results (Sect. 6).
- (7) Further tunnel case records representing weak rock mass subject to plastic deformation should be studied and included as a basis for potential updates and improvements in this hybrid procedure. This may include, among other assessments, parametric analyses and sensitivity studies of rock mass properties and deformation measurements, or probabilistic analyses. Such further work would help to identifying, and likely minimize, uncertainty and limitation issues related to possible errors in readings and interpretations, or issues related to data representativity.

## 8   Conclusions

A study based on an innovative hybrid, combined use of four analysis approaches together with deformation monitoring and elaborated numerical calculations have been employed to assess ground behavior and derive optimal permanent rock support in a tunnel excavated through weak and heterogeneous flysch of type VIII and X. Both the performed analytical and numerical analyses together with the monitored tunnel response during construction have shown that this innovative approach provides an alternative, viable solution, which benefits the use of a more detailed characterization of the ground behavior, hence a better basis for the design of optimal tunnel support in flysch conditions. The application of such approach was possible from the combination of the principles of weak ground engineering with these of the hard rock tunnelling, in which the performance and functionality of RRS arches as permanent support were validated in flysch ground. This permitted a reduction of rock support material consumption and its associated costs. The combined, hybrid approach has similarly allowed to overcome typical challenges in the characterization of ground properties and ground behavior that normally arise in flysch rock mass due to its high variability and heterogeneous character. From the analyses and comparison of the results, the following key findings were revealed:

- (1) The characterization of intact rock properties of flysch rock mass poses challenges due to the high variability in rock properties and the generalized weak character of the rocks involved. Obtaining undisturbed samples for laboratory testing was found complicated as the weak rock specimens of siltstone tend to deteriorate during
2. sample transport and preparation. Field estimates of the intact rock strength ( u1D70E ci ) with PLT and geo-hammer resulted in a valuable approach to determine representative results of fresh, undisturbed strength.
- (2) Face mapping with only one empirical rock mass classification such as the Q -system was observed insufficient to capture the complete ground behavior, describe the rock mass, and give adequate designs of ground support in flysch rock mass. The latter is in line with Iasiello et al. (2021) which postulated that empirical classifications alone present difficulties to address the ground behavior of weak rock mass. It was observed that with the use of supplementary classifications such as the ­ GSIflysch , more detailed assessments of the ground conditions, rock mass strength, and deformational behavior of the ground were obtained.
- (3) Deformation monitoring is an essential component for the assessment of plastic deformations in tunnels excavated in weak rock masses of flysch as these studied in this article. It provides a good basis to zone the tunnel in sections presenting different plastic behaviors and it gives the basis for the necessary numerical verifications and/or calibration of in-situ stresses and rock mass properties.
- (4) Provided the high variability and complexity of the studied flysch rock mass, the assessment and comparison performed on the basis of an integration of four approaches resulted in more detailed predictions of plastic deformations. However, the four studied approaches were also seen to present different levels of performance and limitations when used alone for the study of plastic deformations and tunnel support stability in flysch rock mass.
- (5) In the studied weak rock mass of flysch with Q 0.1-1 or GSI 15-35, analytical solutions that are usually employed alone for the analysis of tunnel convergence were seen to present limitations when these are attempted for detailed analyses or design. The combination of several approaches to determine ground behavior and support performance is a more efficient approach that can provide design optimization. The potential support optimization or saving from using a hybrid approach contra the current, traditional and individual use of analytical methods has been estimated to be about 25% of the total costs considering the characteristics of the studied weak rock mass of flysch.
- (6) The findings show that with such a hybrid approach that combines four analysis methodologies with detailed characterization of the weak ground and deformation monitoring, more detailed assessments of plastic deformation and optimal designs of tunnel rock support are possible. The latter requires, a priori , more elaborated and rigorous investigation and design work.

<!-- image -->

Logo

But as addressed by Langford et al. (2015) for a case in similar flysch conditions, and by Terron-Almenara et al. (2023) for tunnel cases in poor and weak rock mass, a more consistent design basis is obtained as the comparative performance of the employed approaches is then known. A posteriori, such procedure can then result into more optimal and economical designs of tunnel rock support in weak flysch rock mass, as so derived with the use of RRS arches in tunnel sections, where cast-concrete lining had been mandatory with the current design methodology.

Acknowledgements The authors are thankful for the financial support provided by Statkraft for MSc projects developed by three MSc studies on this case project. Some of the geological and engineering geological information were gathered through the supervision of MSc studies by these three MSc fellows.

Funding Open access funding provided by NTNU Norwegian University of Science and Technology (incl St. Olavs Hospital - Trondheim University Hospital). Open access funding was provided by NTNU Norwegian University of Science and Technology (incl St. Olavs Hospital-Trondheim University Hospital). This article has been prepared under a PhD project that is jointly financed by the Norwegian Public Roads Administration (NPRA) and the Norwegian Railway Administration (Bane NOR). The authors also wish to acknowledge the financial support of Sweco Norge AS and the Norwegian Tunneling Association (NFF).

Data availability The datasets generated during this study cannot publicly shared due to commercial reasons.

## Declarations

Conflict of Interest The authors confirm that there are no known conflicts of interest associated with the publication of this article, and that are no financial or non-financial interests that has affected the outcome of this work.

Open Access This article is licensed under a Creative Commons Attribution 4.0 International License, which permits use, sharing, adaptation, distribution and reproduction in any medium or format, as long as you give appropriate credit to the original author(s) and the source, provide a link to the Creative Commons licence, and indicate if changes were made. The images or other third party material in this article are included in the article's Creative Commons licence, unless indicated otherwise in a credit line to the material. If material is not included in the article's Creative Commons licence and your intended use is not permitted by statutory regulation or exceeds the permitted use, you will need to obtain permission directly from the copyright holder. To view a copy of this licence, visit http://creativecommons.org/licenses/by/4.0/.

## References

- AFTES (1978) Analysis of tunnel stability by the convergence-confinement method. Undergr Space 4(4):221-223
- AFTES (2001) Recommendations on the convergence-confinement method
- Alonso E, Alejano LR, Varas F, Fdez-Manin G, Carranza-Torres C (2003) Ground response curves for rock masses exhibiting strain-softening behaviour. Int J Numer Anal Meth Geomech 27:1153-1185
- Anagnostou G, Kovari K (1993) Significant parameters in elastoplastic analysis of underground openings. J Geotech Eng 119(3):401419. https:// doi. org/ 10. 1061/ (ASCE) 0733- 9410(1993) 119: 3(401) ymbas D (ed) Tunnelling mechanics-advances in geotechnical engineering and tunnelling. Eurosummerschool, Innsbruck, pp
- Barla G (1995) Squeezing rocks in tunnels. ISRM News J 2(3):44-49 Barla G (2001) Tunnelling under squeezing rock conditions. In: Kol169-268
- Barton N, Lien R, Lunde J (1974) Engineering classification of rock masses for the design of tunnel support. Rock Mech Rock Eng 6(4):189-236. https:// doi. org/ 10. 1007/ BF012 39496
- Bobet A, Einstein H (2024) Tunnel design methods. CRC Press, Boca Raton
- Brown ET (1987) Rock characterization, testing and monitoringISRM suggested methods. Pergamon Press, Oxford, pp 171-183
- Brown ET, Bray JW, Ladanyi B, Hoek E (1983) Ground response curves for rock tunnels. J Geotech Eng 109(1):15-39
- Carranza-Torres C (2004) Elasto-plastic solution of tunnel problems using the generalized form of the Hoek-Brown failure criterion. Int J Rock Mech Min Sci 41(Supp 1):1-11
- Carranza-Torres C, Diederichs M (2009) Mechanical analysis of circular liners with particular reference to composite supports. For example, liners consisting of shotcrete and steel sets. Tunn Undergr Space Technol 24:506-532
- Carranza-Torres C, Fairhust C (2000) Application of the convergence confinement method of tunnel design to rock-masses that satisfy the Hoek-Brown failure criterion. Tunn Undergr Space Technol 15(2):187-213
- Chryssanthakis P (2015) Behavior of reinforced ribs of shotcrete (RRS) under changing load. In: Proc ISRM 13th int cong rock mech, Montreal, p 16
- Crowder JJ, Bawden WF (2004) Review of post-peak parameters and behaviour of rock masses: current trends and research. Rocknews
- Dilek Y, Furnes H, Shallo M (2007) Suprasubduction zone ophiolite formation along the periphery of Mesozoic Gondwana. Gondwana Res 11:453-475
- Donovan K, Pariseau WE, Cepak M (1984) Finite element approach to cable bolting in steeply dipping VCR stopes. In: Proc geomechanics applications in underground hardrock mining, society of mining engineers, New York, pp 65-90
- Duncan Fama ME (1993) Numerical modelling of yield zones in weak rocks. In: Hudson JA (ed) Comprehensive rock engineering, vol 2. Pergamon Press, Oxford, pp 49-75
- Eberhardt E (2012) The Hoek-Brown failure criterion. Rock Mech Rock Eng 45:981-988. https:// doi. org/ 10. 1007/ s00603- 012- 0276-4
- Fairhust C (2017) The observational approach in Rock engineering. J Hydraul Fract 4(1):36-41
- Fairhust C, Carranza-Torres C (2002) Closing the circle-some comments on design procedures for tunnel supports in rock. In: Labuz JF, Bentler JG (eds) Proc 50th annual geotech conf. University of Minnesota, Minneapolis, pp 21-84
- Fenner R (1938) Undersuchungen zur Erkenntnis des gebirgsdruckes. Gluckauf 74 (In German)
- Goodman RE (1989) Introduction to rock mechanics. John Wiley and Sons, New Jersey, p 412
- Goricki A, Rachaniotis N, Hoek E, Marinos P, Tsotsos S, Schubert W (2006) Support decision criteria for tunnels in fault zones. Felsbau 24(5):51-57
- Hedayat A, Weems J (2019) The elasto-plastic response of deep tunnels with damaged zone and gravity effects. Rock Mech Rock Eng 52:5123-5135. https:// doi. org/ 10. 1007/ s00603- 019- 01834-4

<!-- image -->

Icon

- Heidbach O, Rajabi M, Cui X, Fuchs K, Müller B, Reinecker J, Reiter K, Tingay M, Wenzel F, Xie F, Ziegler F, Zoback M-L, Zoback M (2018) The world stress map database release 2016: crustal stress pattern across scales. Tectonophysics 744:484-498
- Hoek E (1999) Support for very weak rock associated with faults and shear zones. In: Int symp on rock support and reinforcement practice in mining, Kalgoorlie
- Hoek E, Brown ET (1980) Underground excavations in rock. The Institute of Mining and Metallurgy, London
- Hoek E, Brown ET (1997) Practical estimates of rock mass strength. Int J Rock Mech Min Sci Geomech Abstr 34(8):1165-1186
- Hoek E, Carranza-Torres C, Corkum B (2002) Hoek-Brown failure criterion-2002 edition. NARMS-TAC. Toronto
- Hoek E, Corkum B (2002) Hoek-Brown failure criterion-2002 Edition. In: Proc. NARMS-TAC conference, Toronto vol 1, pp 267-273
- Hoek E, Diederichs MS (2006) Empirical estimation of rock mass modulus. Int J Rock Mech Min Sci 43:203-215
- Hoek E, Marinos P (2000) Predicting tunnel squeezing problems in weak and heterogeneous rock masses. Tunnels Tunnel Int 32(11):34-51
- Hoek E, Marinos PG, Marinos VP (2005) Characterization and engineering properties of tectonically undisturbed but lithologically varied sedimentary rock masses. Int J Rock Mech Min Sci 42(2):277-285
- Høien AH, Nilsen B (2018) Analysis of the stabilising effect of ribs of reinforced sprayed concrete (RRS) in the Løren road tunnel. Bull Eng Geol Environ 78(1):1-17. https:// doi. org/ 10. 1007/ s10064- 018- 1238-1
- Hudson JA, Harrison JP (1997) Engineering rock mechanics: an introduction to the principles, 1st edn. Elsevier Science Ltd, Oxford
- Iasiello C, Guerra Torralbo JC, Torrero Fernandez C (2021) Large deformations in deep tunnels excavated in weak rocks: Study on Y-Basque high-speed railway tunnels in northern Spain. Undergr Space 6:636-649
- ISRM (1979) Suggested methods for determining water content, porosity, density, absorption and related properties and swelling and slake-durability index properties. Int J Rock Mech Min Sci 16(2):143-156
- ISRM (1985) Suggested method for determining point load strength. Int J Rock Mech Min Sci Geomech Abstr 22(51):62
- Jaky J (1944) The coefficient of earth pressure at rest. In: Proc 2nd int conf soil mech, vol 1, pp 103-107
- Langford JC, Vlachopoulos N, Diederichs MS (2015) Revisiting support optimization at the Driskos tunnel using a quantitative risk approach. J Rock Mech Geotech Eng 8(2):147-163. https:// doi. org/ 10. 1016/j. jrmge. 2015. 11. 003
- Lü Q, Low BK (2011) Probabilistic analysis of underground rock excavations using response surface method and SORM. Comput Geotech 38(8):1008-1021
- Marinos V (2014) Tunnel behavior and support associated with the weak rock masses of flysch. J Rock Mech Geotechn Eng 6(3):227-239
- Marinos V (2017) A revised, geotechnical classification GSI system for tectonically disturbed heterogeneous rock masses, such as flysch. Bull Eng Geol Environ 19:1-14. https:// doi. org/ 10. 1007/ s10064- 017- 1151-z
- Marinos P, Hoek E (2001a) Estimating the geotechnical properties of heterogeneous rock masses such as flysch. Bull Eng Geol Environ 60:85-92
- Marinos P, Hoek E (2001b) GSI: a geologically friendly tool for rock mass strength estimation. In: Proc. GeoEng 2000 int conf geotech geol eng, Melbourne, Australia. Technomic Publishers, Lancaster, PA, pp 1422-1446
- Marinos V, Goricki A, Malandrakis E (2018) Determining the principles of tunnel support based on the engineering geological behavior type: example of a tunnel in tectonically disturbed
- heterogeneous rock in Serbia. Bull Eng Geol Environ 78:28872902. https:// doi. org/ 10. 1007/ s10064- 018- 1277-7
- Marinos V, Marinos P,  Hoek E (2005) The geological strength index: applications and limitations. Bull Eng Geol Environ 64(1):55-65. https:// doi. org/ 10. 1007/ s10064- 004- 0270-5
- Medley EW (1994) The engineering characterization of Melanges and similar block-in-matrix rocks (Bimrocks). PhD Dissertation, Department of Civil Engineering, University of California at Berkeley
- NFF (2008) Heavy rock support in underground constructions. The principles of Norwegian tunnelling. Handbook no. 5. Norwegian Tunnelling Society, Oslo (in Norwegian)
- NGI (2015) The use of the Q-system: rock mass classification and rock reinforcing. www. ngi. no. Accessed 12 Sept 2024
- Oreste P (2009) The convergence-confinement method: roles and limits in modern geomechanical tunnel design. Am J Appl Sci 6(4):757-771
- Palmstrom A, Broch E (2006) Use and misuse of rock mass classifications systems with particular reference to the Q-system. Tunn Undergr Space Technol 21:575-593
- Panet M (1995) Le calcul des tunnels par la méthod convergence-confinement. Presses de I'ENPC, Paris
- Panet  M  (2001)  Recommendations on the convergence confinement method. Association Francaise des Travaus en Souterrain (AFTES), Paris
- Panthi KK (2006) Analysis of engineering geological uncertainties analysis related to tunnelling in Himalayan rock mass conditions. Doctoral Thesis at NTNU 2006:41, Department of Geology and Mineral Resources Engineering, Norwegian University of Science and Technology, Norway. ISBN 82-471-7826-5
- Panthi KK, Nilsen B (2007a) Predicted versus actual rock mass conditions: a review of four tunnel projects in Nepal Himalaya. Tunn Undergr Space Technol 22(2):173-184
- Panthi KK, Nilsen B (2007b) Uncertainty analysis of tunnel squeezing for two tunnel cases from Nepal Himalaya. Int J Rock Mech Min Sci 44:67-76
- Panthi KK, Shrestha PK (2018) Estimating tunnel strain in the weak and schistose rock mass influenced by stress anisotropy: an evaluation based on three tunnel cases from Nepal. Rock Mech Rock Eng 51:1823-1838. https:// doi. org/ 10. 1007/ s00603- 018- 1448-7
- Peck RB (1969) Advantages and limitations of the observational method in applied soil mechanics. Géotechnique 19(2):171-187
- Rocscience Inc (2022) RS2, v. 11.015 ed. Rocscience Ing, Toronto
- Sakurai S (1997) Lessons learnt from field measurements in tunneling. Tunn Undergr Space Technol 12(4):453-460
- Sakurai S (2017) Back analysis in rock engineering. ISRM book series 4. CRC Press, Boca Raton
- Schwartz CW, Einstein HH (1980) Simplified analysis for groundstructure interaction in tunnelling. The state of the art in rock mechanics. In: Proc 21st U.S. symp rock mech. University of Missouri-Rolla, pp 787-796
- Shrestha PK (2014) Stability of tunnels subject to plastic deformationa contribution based on the cases from Nepal Himalaya. Doctoral thesis at NTNU 2014:305, Norwegian University of Science and Technology. ISBN 978-82-326-0522-4
- Sjöberg J (2020) Solving rock mechanics issues through modelling: then, now, and in the future? In: Proc 2nd int conf undergr min tech, Perth, pp 27-46
- Starfield AM, Cundall PA (1988) Towards a methodology for rock mechanics modelling. Int J Rock Mech Min Sci Geomech Abstr 25(3):99-106
- Stephansson O, Zang A, (2012) ISRM suggested methods for rock stress estimation-part 5: establishing a model for the in situ stress for at a given site. Rock Mech Rock Eng 5:955-969
- Su Y, Su Y, Zhao M, Vlachopoulos N (2021) Tunnel stability analysis in weak rocks using the convergence confinement method.

<!-- image -->

Logo

- Rock Mech Rock Eng 54:559-582. https:// doi. org/ 10. 1007/ s00603- 020- 02304-y
- Sulem J, Panet M, Guenot A (1987a) Closure analysis in deep tunnels. Int J Rock Mech Min Sci Geomech 24(3):145-154
- Sulem J, Panet M, Guenot A (1987b) Analytical solution for time dependent displacements in a circular tunnel. Int J Rock Mech Min Sci Geomech 24(3):155-164
- Terron-Almenara J, Holter KG, Høien AH (2023) A hybrid methodology of rock support design for poor ground conditions in hard rock tunnelling. Rock Mech Rock Eng 56:4061-4088. https:// doi. org/ 10. 1007/ s00603- 023- 03273-8
- Tremblay A, Meshi A, Deschamps T, Goulet F, Goulet N (2015) The Vardar zone as a suture for the Mirdita ophiolites, Albania: constraints from the structural analysis of the Korabi-Pelagonia zone. Tectonics 34:352-375
- Vlachopoulos N, Diederichs MS (2009) Improved longitudinal displacement profiles for convergence confinement analysis of deep tunnels. Rock Mech Rock Eng 42(2):131-146. https:// doi. org/ 10. 1007/ s00603- 009- 0176-4
- Vlachopoulos N, Diederichs MS, Marinos V, Marinos P (2013) Tunnel behavior associated with the weal alpine rock masses of the Driskos twin tunnel system, Egnatia Odos Highway. Can Geotech J 50(1):91-120. https:// doi. org/ 10. 1139/ cgj- 2012- 0025
- Vlachopoulos N, Forbes B, Ioannis V (2020) Tunnelling in weak rock. In: Kanji M, He M, Ribeiro e Sousa L (eds) Soft rock mechanics and engineering. Springer, Berlin, pp 579-621
- Vlachopoulos N, Su Y (2019) Longitudinal Displacement Profiles for Convergence-Confinement Analysis of Excavations: Applicability to Tunnelling, Limitations and Current Advancements. In: Proc 72nd Conf Canadian Geotech Society. Newfoundland, Canada
- Vrakas A, Anagnostou G (2014) A finite strain closed-form solution for the elastoplastic ground response curve in tunnelling. Int J Num Anal Methods Geomech 38(11):1131-1148
- Vrakas A, Anagnostou G (2016) Ground response to tunnel re-profiling under heavily squeezing conditions. Rock Mech Rock Eng 49(7):2753-2762
- Walton G, Sinha S (2022) Challenges associated with back analysis in rock mechanics. J Rock Mech Geotech Eng 14(6):2058-2071
- Wang Y (1996) Ground response of circular tunnel in poorly consolidated rock. J Geotech Eng 122(9):15-39
- Yu HS (2000) Cavity expansion methods in geomechanics. Kluwer Academic Publishers, Dordrecht

Publisher's  Note Springer  Nature  remains  neutral  with  regard  to jurisdictional claims in published maps and institutional affiliations.

<!-- image -->

Icon
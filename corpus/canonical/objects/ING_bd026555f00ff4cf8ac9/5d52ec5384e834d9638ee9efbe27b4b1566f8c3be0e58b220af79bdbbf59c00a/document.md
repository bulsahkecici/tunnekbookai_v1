<!-- image -->

Logo

DOI: 10.5937/SETC25003U

## Analysis of primary NATM support under limited anchor capacity: implications for steel ribs and lattice girders

Milan Uljarević a *, Andrija Rašeta b and Dragan Bojović c

a  CRBC Serbia, Novi Sad, Serbia; umilan89@gmail.com

b University of Novi Sad, Faculty of Technical Science, Civil engineering, Novi Sad, Serbia; araseta@gmail.com

c IMS, Belgrade, Serbia; dragan.bojovic@institutims.rs

Abstract: In the conventional application of the New Austrian Tunneling Method (NATM), the primary tunnel support is designed as a composite system consisting of shotcrete, systematically installed rock bolts, and auxiliary elements such as lattice girders and steel ribs. Official guidelines typically classify steel elements as temporary supports, meant to stabilize the excavation face until the shotcrete and anchoring system become structurally active. However, field experience shows that anchors in weak or heavily fractured ground conditions often fail to mobilize their  full  capacity,  particularly  when  their  embedment  does  not  extend  beyond  the  plasticized  zone  around  the excavation. This paper analyzes the structural behavior of the primary NATM support system in cases where anchors do not perform as  intended.  Using  a  shell-based  numerical  model  with  point  support  representation,  the  study investigates  how  local  ground-structure  interaction  changes  when  anchors  lose  stiffness  and  how  structural responsibility may shift toward steel ribs and lattice girders. Practical site observations are used to illustrate common deviations from design assumptions such as the installation of multiple ribs without proper contact with the rock mass or reliance on rigid steel elements in zones where shotcrete alone could suffice. Special attention is given to the anchorage mechanism, the conditions under which steel ribs begin to act as primary load-bearing components, and the consequences of poor shotcrete encapsulation (e.g., shadow zones). The study emphasizes that the structural contribution  of  steel  elements  in  NATM  should  be  re-evaluated  when  anchors  are  compromised,  and  that  this redefinition must account for ground conditions, construction sequence, and time-dependent concrete performance. The paper proposes practical guidelines for the rational integration of steel supports in NATM lining systems when conventional anchoring is unreliable, aiming to improve both safety and efficiency in tunnel design and execution.

Keywords:

lattice girders; steel ribs; NATM; primary lining; tunnel

## 1. Introduction

The New Austrian Tunneling Method (NATM) is founded on the principle that the surrounding ground mass  should  actively  participate  in  the  overall  load-bearing  system,  with  controlled  deformations ensuring  both  stability  and  economy.  In  its  conventional  application,  the  primary  lining  typically consists of shotcrete, systematically installed rock bolts, and auxiliary elements such as lattice girders or steel ribs. Official guidelines, such as those of the Austrian Society for Geomechanics (2010) and the  U.S.  Department  of  Transportation  Federal  Highway  Administration  (2009),  generally  classify these steel elements as temporary supports intended to stabilize the excavation until the shotcrete and anchoring system becomes fully effective.

However, practical tunneling experience has repeatedly shown that this assumption does not always hold true. In weak or heavily fractured ground, rock bolts often fail to develop their full anchoring capacity, particularly when their embedment remains within the plasticized zone around the excavation (Nilsson  and  Holmgren,  1999).  When  this  occurs,  the  intended  composite  support  mechanism  is compromised, and structural responsibility may shift toward the shotcrete shell and the embedded steel elements.  Representative  cases  include  the  Boggo  Road  Busway  tunnel  in  Brisbane  (Nye  and  Alt,

*Corresponding author: umilan89@gmail.com (M. Uljarević ).

2010), where thick shotcrete and lattice girders were relied upon as both initial and permanent lining due  to  settlement  control  requirements,  and  Collotta  et  al.  (2010)  study  of  steel  ribs  embedded  in shotcrete linings, which demonstrated sustained stress redistribution arising from creep and shrinkage effects. Similar observations have been reported in urban tunneling projects in Central Europe, where insufficient anchor mobilization led to premature reliance on rigid steel ribs for stability.

Despite these findings, the structural contribution of lattice girders and steel ribs in NATM linings remains insufficiently quantified. Current design practice rarely accounts for their long-term stiffness contribution, the effects of poor concrete encapsulation (e.g., shadow zones), or the influence of joint behavior and spacing between elements. This research gap becomes particularly critical in cases where anchors cannot be mobilized, such as when excavation is advanced under pipe umbrellas or in heavily fractured rock masses.

The present study addresses this gap by analyzing the behavior of the NATM primary lining under conditions of limited anchor  capacity. Through  numerical  modeling,  field observations, and comparative  laboratory  testing  of  lattice  girders  and  steel  ribs,  the  study  seeks  to  clarify  the circumstances under which these steel elements transition from temporary stabilizers into structurally relevant components  of the permanent support. By  doing so, it aims to provide practical recommendations for integrating lattice girders and steel ribs into the design of NATM support systems, particularly in weak or fractured ground conditions where conventional anchoring is unreliable.

## 2. General principle of the New Austrian Tunneling Method (NATM)

The  New  Austrian  Tunneling  Method  (NATM)  is  based  on  the  fundamental  concept  that  the surrounding ground is not merely a source of loading but also acts as a structural component of the tunnel support system. This method leverages the self-supporting capacity of the rock or soil mass, aiming to mobilize the ground's strength through controlled deformation and timely installation of support measures (Figure 1 (a) (Chapman et al., 2010) and (b) (Australian Tunnelling Society, 2024)).

Fig. 1. Principle of  NATM ground-structure interaction  (a)  (Chapman  et al.,  2010);  (b)  (Australian  Tunnelling Society, 2024).

<!-- image -->

Engineering drawing

Unlike  traditional  tunneling  methods  that  rely  on  rigid  predesigned  support  systems,  NATM emphasizes  a  flexible,  observational  approach.  Excavation  and  installation  of  support  elements  are continuously adapted to in-situ ground conditions and project-specific requirements. Ground response - primarily measured in the form of displacements of the initial lining is monitored in real time to verify the stability of the opening and to optimize both the excavation sequence and the type and timing of support installation.

Typical NATM support systems consist of (Austrian society of geomechanics, 2010):

Shotcrete, Rock bolts or systematic anchors, with additional elements such as  steel ribs and lattice girders used to provide early structural integrity and to preserve the excavation geometry prior to full shotcrete hardening.

For a long time, especially in the initial period, this procedure encountered resistance. The opponents argued that a tiny layer of shotcrete and anchoring might counteract subsurface pressure. It was most likely because the static analysis of shotcrete and anchors had to be performed in the same way as steel and concrete structures at the time. By activating the load-bearing vault of soil or rock that encloses the underground  opening,  it  becomes  part  of  the  overall  load-bearing  system.  This  single  approach  is essentially based on semi-empirical design, in-situ measurements, and corrections. The development of NATM has substantially enhanced the cost efficiency of tunneling projects and had favorable effects on infrastructure development as well. (Kovačević, 2014).  NATM is based on the concept that the ground around the tunnel not only acts as a load but also as a load-bearing element. The typical support elements in NATM are shotcrete and rock dowels. Steel ribs or lattice girders provide limited early support prior  to the  shotcrete  hardening  and  ensure proper  profile  geometry.    If  ground  conditions require support at or ahead of the excavation face, face dowels, shotcrete, spiles, or pipe canopies are installed. The excavation cross-section is subdivided into the top heading, bench, and invert depending on both ground conditions and logistical requirements (i.e. to facilitate the use of standard plant and machinery). (Austrian society of geomechanics, 2010)

## 3. Lattice girders and Steel Ribs in NATM primary support

Lattice  girders  are  structural  elements  made  of  steel  reinforcing  bars,  interconnected  into  a  threedimensional shape, most commonly triangular to achieve the desired stiffness and geometric stability. They are pre-bent to match the tunnel profile and installed immediately behind the excavation face, before the shotcrete has developed sufficient load-bearing capacity. According to the Technical Manual for Design and Construction of Road Tunnels - Civil Elements (U.S. Department of Transportation), although lattice girders have relatively small cross-sectional areas compared to the thickness of the shotcrete lining and thus do not independently provide substantial bearing capacity, they fulfill several essential  support  functions  (U.S.  Department  of  Transportation  Federal  Highway  Administration, 2009):

Provide immediate support to unstable rock blocks that tend to fall out;

- Offer a precise geometric template for shotcrete application;
- Serve as carriers for welded mesh reinforcement, when used;
- Act as rigid anchors for preliminary support measures such as forepoling.

In the conventional application of the New Austrian Tunneling Method (NATM), lattice girders and steel ribs are typically defined as temporary support elements, intended to provide early stabilization immediately  after  excavation.  According  to  the  Austrian  Society  for  Geomechanics  (ÖGG),  these components serve a short-term role in controlling deformations and ensuring safety until the shotcrete and systematic anchoring are fully activated. 'Steel ribs and lattice girders are considered temporary support  elements  within  the  NATM  framework,  aimed  at  immediate  stabilization  during  early excavation phases.' (based on ÖGG guidelines). This interpretation has been widely adopted in both academic  literature  and  engineering  practice.  Nevertheless,  the  extent  to  which  these  elements contribute  to  the  structural  behavior  of  the  primary  lining  system  remains  an  ongoing  subject  of discussion, particularly in contexts where they are retained in the final lining or assumed to contribute to composite action with the surrounding shotcrete (Austrian Society of geomechanics, 2010).

## 3.1. Opposite attitude

However, several recent studies and design approaches challenge this strict classification. For instance, Nye and Alt (2010) report the use of steel ribs in combination with thick shotcrete layers (up to 350 mm)  as  part  of  a  support  system  classified  as  both  initial  and  permanent  lining,  especially  in geologically sensitive urban tunneling conditions. Similarly, Collotta et al. (2010) present a detailed investigation into the long-term stress redistribution in shotcrete tunnel linings with embedded steel ribs. The study models the ribs as integral parts of the composite lining, highlighting their sustained structural interaction with the surrounding shotcrete due to creep and shrinkage effects and dominant influence in the composite system (Collotta et al., 2010).

These  findings  indicate  that,  under  certain  conditions,  lattice  girders  and  steel  ribs  may  contribute beyond their originally intended temporary function. Nevertheless, the actual structural impact depends on several critical factors: the mechanical connection of rib segments, the manner of their base support (often acting as temporary foundations), the spacing between elements, and the quality of shotcrete placement around the steel frame. These aspects are frequently neglected in simplified models, leading to under or overestimation of the system's stiffness and stability.

## 4. Research background and objectives

This  research  focuses  on  the  application  of  lattice  girders  and  steel  ribs  in  tunnel  construction, particularly  when  using  the  New  Austrian  Tunneling  Method  (NATM).  Although  the  technical literature often defines these elements as temporary support components, in practice it is common to see multiple lattice girders installed in a single excavation step, regardless of the rock stability. There are also frequent cases where these elements are placed at large spacing intervals (as illustrated in Figure 2),  clearly  indicating  that  they  are  not  functioning  as  temporary  supports  but  rather  as  part  of  the shotcrete lining.

A growing concern is the increasing use of steel ribs that are not properly included in structural analyses. Key factors such as staged construction, ground-structure interaction, shotcrete confinement, and the mechanical behavior of rib segment joints are often ignored. These ribs are sometimes modeled as part of the reinforcement within the concrete lining, yet their spacing and influence on the overall loadbearing capacity are rarely evaluated in detail.

The main goal of this research is to reliably determine the actual contribution of lattice girders and steel ribs  to  the  long-term  structural  performance  of the primary tunnel support. The central question is: under what conditions can these elements be considered relevant to the tunnel lining's permanent loadbearing  capacity,  and  how  can  their  role  be  properly  integrated  into  design  analyses  according  to specific geological conditions?

## 4.1. Practical challenges observed on construction sites

In recent years, tunneling practice has increasingly diverged from standard design assumptions. It is becoming common to install multiple lattice girders within a single excavation step, regardless of actual ground stability. In many cases, lattice girders and steel ribs are placed without proper contact or bearing on the  surrounding  rock,  effectively  eliminating  their  intended  structural  function.  Moreover,  these elements are often not included in structural calculations, with important factors such as joint detailing, load  transfer,  and  construction  staging  being  overlooked.  A  critical  issue  is  also  the  frequent discontinuity in the shotcrete lining at the locations of large steel elements, where poor embedding and lack of confinement reduce the composite action and compromise the support system's stiffness.

Fig. 2. (a) Primary support without anchors and propiate temporary foundations; (b) Installing multiple steel ribs in the stable ground with no stiff support on the ground.

<!-- image -->

Photograph

<!-- image -->

Photograph

## 4.2. Configuration examples and setup observations

As part of a broader investigation into the structural role of steel elements in NATM primary lining, several configurations of lattice girders, steel ribs, and conventional reinforcement were prepared and tested  in  order  to  illustrate  typical  integration  approaches  used  in  tunnel  support  systems.  These configurations  were  intended  not  only  to  demonstrate  the  geometric  variability  and  potential implications of steel elements embedded in shotcrete, especially in conditions where anchoring systems underperform or cannot be fully mobilized due to poor ground quality, but also to directly compare their structural efficiency.

Fig. 3. (a) Lattice girder, steel ribs and reinforcement in the moulds; (b) Shotcrete aplication; (c) Labaratory testing.

<!-- image -->

Photograph

Figures 3a, 3b, and 3c show representative stages of the preparation and testing process, including the arrangement of lattice girders and steel ribs in moulds, shotcrete application, and subsequent laboratory testing of full-scale specimens.

<!-- image -->

Photograph

<!-- image -->

Photograph

The  experimental  results  indicated  that  specimens  reinforced  only  with  conventionally  placed reinforcement bars achieved the most favorable performance (Table 1), both in terms of stiffness and ultimate load-bearing capacity. In contrast, configurations with large lattice girders or massive steel ribs  often  exhibited  reduced  composite  action  due  to  incomplete  shotcrete  encapsulation  and  the presence of shadow zones, as confirmed by visual inspection. These outcomes suggest that while lattice girders and ribs can provide immediate stabilization and geometric control during construction, their long-term  contribution  to  the  structural  capacity  of  the  lining  is  limited  compared  to  well-detailed conventional reinforcement.

Table 1. Testing results of concrete beams with different types of reinforcing

| Type heading   | Shape heading              |   Maximum force kN |   Deflection mm | Sample collapse   |
|----------------|----------------------------|--------------------|-----------------|-------------------|
| T70-1          | 1-piece lat. girder        |                196 |            5.72 | Yes               |
| T70-2          | 2-piece lat. girder        |                110 |            4.38 | Yes               |
| T190-1         | 1-piece lat. girder        |                200 |            3.43 | No                |
| T190-2         | 2-piece lat. girder        |                199 |           17.46 | No                |
| HEB140-1       | 1-piece steel rib          |                197 |            4.56 | No                |
| HEB140-2       | 2-piece steel rib          |                120 |           11.93 | Yes               |
| HEA200-1       | 1-piece steel rib          |                196 |            4.44 | No                |
| HEA200-2       | 2-piece steel rib          |                 83 |           11.69 | Yes               |
| RB-1           | reinforcement bars-1-piece |                200 |            3.89 | No                |
| RB-2           | reinforcement bars-overlap |                200 |            3.02 | No                |

## 4.3. Visual inspection

Following  the  preparation  and  casting  of  concrete  specimens  with  integrated  steel  components,  a detailed visual inspection was carried out on cross-sections of the hardened shotcrete. The objective was  to  assess  the  quality  of  concrete  placement  and  the  degree  of  encapsulation  around  the  steel elements.

The inspection revealed that large-profile steel ribs, particularly those with closed geometries or dense configurations, frequently acted as barriers to uniform shotcrete application. In several cross-sections, unfilled zones were observed along the sides and beneath the horizontal flanges of the ribs, indicating incomplete  encapsulation  of  the  steel  elements  by  the  shotcrete.  These  localized  voids,  commonly referred to as shadow zones , compromise the composite behavior of the lining by reducing stiffness and creating potential weak points in the support system.

By contrast, in specimens reinforced only with conventionally placed reinforcement bars, the shotcrete demonstrated excellent continuity and full encapsulation of the reinforcement. The absence of shadow zones resulted in more homogeneous stiffness across the section, which directly translated into higher load-bearing capacity and better overall performance, as confirmed by laboratory testing.

This comparative outcome clearly explains why specimens with conventional reinforcement achieved the best results, while those with lattice girders or heavy steel ribs underperformed due to difficulties in ensuring proper shotcrete confinement and structural integration.

Fig. 4 . (a) Steel rib HEA 200 sample; (b) Reinforcement sample.

<!-- image -->

Photograph

## 5. Numerical modeling of the primary lining concrete shell

To better understand the behavior of the composite tunnel lining system consisting of a reinforced concrete shell supported by anchors, a detailed finite element model was developed using Autodesk Robot Structural Analysis 2025 . The primary lining was represented as a continuous shell structure, simulating the shotcrete layer applied in NATM tunneling. This model was not intended as a direct complement  to  the  experimental  tests  but  rather  served  as  an  independent  tool  for  illustrating  the structural interaction between the concrete shell and the anchoring system.

In the model, anchors were idealized as fixed point supports, assuming full load transfer and no relative displacement with respect to the surrounding ground. This reflects the theoretical condition in which the anchor heads are embedded deeply enough into the surrounding rock mass - beyond the plastic zone to act as effective restraints for the lining. The geometry of the model was simplified and assumed an idealized, smooth concrete shell without surface irregularities such as peaks or depressions. Anchors were modeled as the only fixed support points to the shell structure, simulating full fixity and perfect load transfer.

However, to achieve such an effect in real conditions, it is essential to define the extent of the plasticized zone around the tunnel excavation, particularly in weak or fractured ground. Anchors must be designed with sufficient length to extend beyond this plastic zone (see Figure 5), thus ensuring that the reactive zone into which they transfer load has not lost its mechanical integrity. If anchors are embedded only within the plastified ground, their stiffness and support capacity are significantly reduced, resulting in deformation and loss of control over lining stability.

The deformation field of the shell under uniform ground loading is shown in Figure 5a. The results indicate non-uniform displacement patterns, with pronounced local warping near anchorage points. These  deformation  modes  deviate  significantly  from  the  smooth,  parabolic  curvature  assumed  in simplified arch models, and reveal the complex behavior of reinforced shotcrete linings under localized support.

(

Fig. 5 . (a) Defomed shape of tunnel primary lining with anchors; (b) Bending moments of tunnel primary lining with anchors.

<!-- image -->

Engineering drawing

These  findings  align  with  the  observations  of  Nilsson  and  Holmgren  (1999),  who  emphasized  the influence of anchor placement relative to surface geometry. When bolts are placed in depressions, the system develops high tensile stresses  and  loses  global  stiffness due  to  localized  deconfinement. In contrast, bolts placed on geometric peaks lead to improved load transfer and higher overall capacity. This  effect  is  especially  relevant  in  thinner  linings  where  surface  irregularities  strongly  influence structural performance.

The bending moment distribution over the shell surface, shown in Figure  5b, further reveals stress concentrations around anchorage zones. These peaks result from local stiffening effects introduced by the  concentrated  support,  and  must  be  considered  in  design  to  avoid  punching  failure,  excessive cracking, or deterioration of the lining system over time.

In summary, although the presented numerical model assumes ideal conditions perfect fixity, smooth surface geometry, and no anchorage deformation it provides important insight into stress behavior and the need for realistic representation of ground - lining interaction. For anchors to serve as true structural supports in NATM linings, their design must be based on geotechnical definition of the plasticized zone and  anchorage  beyond  this  zone,  ensuring  proper  load  transfer  and  effective  integration  with  the concrete shell.

Fig. 6 . Determination of plastic zone by Plaxis 2D.

<!-- image -->

Icon

## 5.1. Time-Dependent Behavior of Shotcrete and its Structural Implications

While the numerical model considers the concrete shell as an already stiff structural body supported by fully mobilized anchors, this assumption is only valid if shotcrete reaches sufficient strength within a short time frame. According to EN 14487-1:2005+A1:2007, structural shotcrete must achieve 100% of its design compressive strength within 24 hours when an appropriate accelerator is used.

Figure  7  shows  a  typical  strength  development  curve  of  shotcrete  (C25/30)  with  an  alkali-free accelerator. As can be seen, the concrete reaches approximately 70-80% of its design strength within the first 8-12 hours. This rapid gain in stiffness implies that, unless the installation of steel ribs and anchoring systems is completed in significantly less time, the shotcrete itself begins to act as the primary structural element relatively early in the construction sequence.

Fig. 7 . Compressive strength development of C25/30 shotcrete with alkali-free accelerator over the first 24 hours (adapted from EN 14487-1 and manufacturer data).

<!-- image -->

Line chart

This  finding  is  particularly  relevant  in  cases  where  steel  elements  are  intended  to  serve  only  as temporary supports. If the shotcrete is properly applied and adequately reinforced, it can absorb and redistribute loads efficiently even before full anchor mobilization, reducing the need for rigid steel components in many situations.

## 6. Validation

To validate the findings of the numerical simulations, field monitoring from the Iriški Venac (Serbia) tunnel  was  used,  executed  in  a  zone  of  severely  fractured  siltstones  (alevrolites)  and  claystones, characterized by unfavorable geotechnical conditions and very high deformation rates.

The monitoring results (Figure 8) show that even after the installation of two successive anchor series (6  m and 8 m), the tunnel deformations continued almost linearly and could not be stabilized. The anchors,  although  installed  according  to  design  specifications,  did  not  provide  sufficient  restraint capacity because their embedment remained within the plastified zone of the ground. Consequently, the intended interaction between the shotcrete lining and the anchoring system was not achieved.

Convergence stabilization occurred only after the closure of the invert and the formation of a continuous circular reinforced concrete lining that provided a rigid support ring to the entire tunnel contour. This observation  is  fully  consistent  with  the  numerical  model  assumptions:  once  the  anchors  lose effectiveness in highly fractured ground, structural responsibility shifts to the concrete shell, and overall stability is restored only when a closed ring effect is established.

It is important to emphasize that sufficiently stiff steel ribs or lattice girders, if properly connected into a  closed  circular  frame  either  immediately  after  excavation  or  with  adequately  secured  temporary footings can significantly enhance the load-bearing capacity of the primary support. In such cases, the rigid ring action can be mobilized earlier, reducing deformation rates and providing a more reliable transfer of loads to the surrounding ground. However, when ribs or girders are discontinuous, poorly supported, or left without proper closure, their contribution remains marginal and deformation control relies almost exclusively on the shotcrete shell.

Fig. 8 . Time-Convergence diagram in the tunnel Iriski Venac (testing profile).

<!-- image -->

Line chart

## 7. Conclusion

One of the persistent dilemmas in tunneling engineering concerns the true structural contribution of lattice girders and steel ribs in NATM primary linings. The most recognized international guidelines consistently classify these elements as temporary supports , intended to maintain excavation stability only until the shotcrete lining and anchoring system has become structurally effective.

The Austrian Society for Geomechanics (2010) clearly states: 'The typical support elements in NATM are shotcrete and rock dowels. Steel ribs or lattice girders provide limited early support before the shotcrete hardens and ensure correct profile geometry.'

Similarly, the U.S. Department of Transportation Federal Highway Administration (2009) notes that while lattice girders have small cross-sectional areas relative to the  shotcrete thickness, they fulfill several essential functions:

- providing immediate support to unstable rock blocks prone to falling out,
- offering a precise geometric template for shotcrete application,
- serving as carriers for welded mesh reinforcement, and
- acting as rigid anchors for preliminary measures such as forepoling.

Finally, Wittke et al. (2002) emphasize the time-dependent interaction between steel ribs and shotcrete: 'Immediately after the steel set is installed and covered with shotcrete, when the shotcrete still has a very low Young's modulus, it is mostly the steel set that carries the loads resulting from rock mass pressure.  With  the  hardening  of  the  shotcrete  over  time,  the  strength  and  bearing  capacity  of  the shotcrete membrane increases. Finally, when the shotcrete has fully hardened, the normal stiffness of t he steel sets can be neglected compared to that of the shotcrete membrane.'

These authoritative references consistently underline the temporary role of steel ribs and lattice girders. Moreover, practical evidence often confirms that their presence may even reduce the effective stiffness of the lining at the contact zones, as illustrated in Figure 4a, where massive steel ribs prevent proper shotcrete encapsulation and create shadow zones.

Yet, field experience and monitoring in extremely unfavorable ground conditions demonstrate that this interpretation  is  not  universally  valid.  When  tunneling  advances  through  severely  fractured  or incoherent ground, the installation of sufficiently stiff steel ribs, arranged at short spacing and connected into a closed circular frame, can significantly enhance stability. Under such circumstances, rigid frames provide immediate load-bearing continuity around the excavation contour and may serve as the decisive element preventing excessive deformations until the shotcrete gains sufficient strength.

The contrasting examples shown in Figures 2a and 2b further highlight this ambiguity: in one case multiple ribs are installed in stable ground where they provide no structural benefit, while in another case stiff ribs become essential in controlling deformation in weak rock. Similar contradictory findings can  be  observed  in  many  tunneling  projects  worldwide,  underlining  the  necessity  of  case-specific evaluation rather than universal classification.

This study, therefore, concludes that:

In standard NATM applications and competent ground conditions, lattice girders and steel ribs should be regarded as temporary stabilizers, with negligible long-term contribution once the shotcrete shell has hardened.

In exceptionally poor geological conditions, where anchors cannot mobilize their capacity and shotcrete alone is insufficient, rigid and continuous steel frames may transition into elements of primary structural relevance, particularly when integrated into a closed ring action.

- the decisive factors governing their effectiveness are:
- proper closure of the ring (invert included),
- adequate stiffness and joint continuity, and
- quality of shotcrete encapsulation.

Finally, this research underlines the need for systematic investigation to establish clear thresholds for when lattice girders and steel ribs meaningfully contribute to the structural capacity of the lining. Only through  an  integrated approach  combining  laboratory  testing, numerical  modeling,  and  field observations  can  reliable  criteria  be  developed  for  their  rational  use.  Such  criteria  are  essential  to eliminate  current  uncertainties  in  tunneling  practice  and  to  ensure  reliable  and  economical  NATM designs.

## References

Australian Tunnelling Society, 2024. Tunnel design guideline , (2 nd edition). ISBN 978-1-925627-48-0

- Austrian  Society  of  geomechanics,  2010. NATM - The  Austrian  Practice  of  Conventional  Tunneling,  Austrian society of geomechanics , ISBN 978-3-200-01989-8

Collotta, T., Barbieri G., Mapell, M., 2010. Shotcrete tunnel linings with steel ribs: Stress redistribution dueto creep and shrinkage effects, Taylor &amp; Francis Group, ISBN 978-0-415-47589-1

Chapman, D., Metje, N., Stark, A., 2010. Introduction to tunnel design, Spon press, ISBN 0-203-89515-0

Kovačević , J., 2014., Savremeno građenje u podzemlju , AGM Knjiga, ISBN 978-86-86363-45-9

Nye, E. J., Alt, D., 2010. Shotcrete application on the Boggo Road Busway driven tunnel , Taylor &amp; Francis Group, ISBN 978-0-415-47589-1

U.S.  Department  of  Transportation  Federal  Highway  Administration,  2009.  Technical  Manual  for  Design  and Construction of Road Tunnels - Civil Elements , Publication No. FHWA-NHI-10-034

Nilsson, U., Holmgren, J., 1999. Design of steel fibre reinforced shotcrete linings In Nordic Concrete

Wittke, W., Pierau, B., Erichsen, C., 2002. New Austrian Tunnelling Method (NATM) - Stability Analyses and Design (Geotechnik in Forschung und Praxis, WBI-Print 5). Verlag Glückauf, Essen. ISBN 3-7739-1305-2.
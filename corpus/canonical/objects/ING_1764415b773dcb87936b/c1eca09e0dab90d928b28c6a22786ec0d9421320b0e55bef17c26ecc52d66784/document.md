OPEN

<!-- image -->

Logo

## Three-dimensional simulation analysis of the impact of excavation on non-level crossing tunnels

Mehdi Arash, Alireza Dolatshahi  &amp; Kourosh Shahriar

The rapid growth of underground infrastructure in densely populated urban areas has increased the need for reliable design guidelines concerning the interaction of non-level crossing tunnels. The proximity of these tunnels often leads to complex soil-structure interactions, where excavationinduced stresses and deformations can significantly affect the safety and serviceability of existing tunnels. Despite the significance of this issue, few studies have comprehensively examined the combined impact of intersection angle, vertical spacing, and excavation sequence on the mechanical behavior of tunnels. This research aims to address this gap by performing a systematic threedimensional finite element analysis using Plaxis 3D, focusing on the structural response of the lining and deformation patterns of the surrounding soil. A parametric study was conducted by varying three critical parameters: the intersection angle of the crossing tunnels, the vertical distance between tunnel axes, and the excavation sequence. The results included vertical displacements of the existing tunnel invert and crown, axial forces, bending and torsional moments in the lining, and soil failure indicators such as plastic point development and shear strain contours. Findings revealed that the intersection angle plays a dominant role, with mid-range angles (around 45°) producing the lowest settlements (up to 60% less than at acute angles) and minimizing lining forces. In contrast, near-orthogonal crossings (75°-90°) resulted in the most unfavorable conditions. Vertical spacing was also crucial: an intermediate spacing of 12.5 m resulted in nearly 30% lower settlements compared to 10 m, whereas a larger spacing (15 m) led to higher displacements due to stress redistribution. Additionally, the excavation sequence significantly influenced deformation patterns: shallow-first excavation caused more localized yet higher settlements, whereas deep-first excavation reduced peak displacements by roughly 10-12% but spread them over a broader zone. Overall, these findings emphasize the importance of carefully considering geometric and construction parameters in tunnel design. The results suggest that adopting intermediate intersection angles and moderate vertical spacing offer the best conditions. At the same time, the choice of excavation sequence should strike a balance between peak settlement and the extent of ground disturbance. These insights contribute to the development of safer and more effective design strategies for non-level crossing tunnels in complex urban environments.

Keywords Tunneling, Interaction, Crossing tunnels, Induced stress, Vertical displacement

The  development of the transit system is essential for the growth of large urban centers. Sustainable urban development offers an innovative approach to addressing transportation challenges and the scarcity of surface space by optimizing the use of underground areas. This approach aims to improve transportation efficiency and support optimal urban expansion 1 . As urban regions expand and populations grow, transportation challenges become increasingly  significant.  Therefore,  engineers  are  increasingly  considering  underground  spaces  as  a practical solution to surface area constraints. This strategy seeks to address transportation issues by maximizing the use of underground environments 2 . Subway systems and traffic tunnels are key parts of urban infrastructure. These facilities are crucial in enhancing transportation and movement within cities, enabling people to travel efficiently and smoothly 3 . These elements are fundamental for making urban travel easier and more effective 4 . The process of shield excavation near existing tunnels often causes deformation and changes in stress levels in

Dept. of Mining Engineering, Amirkabir University of Technology, Tehran, Iran.  email: a.dolatshahi77@gmail.com neighboring tunnels 5 . Analyzing these interactions is complex due to the problematic nature of soil-structure relationships 6,7 . Many tunnels are currently being built or planned close to existing metro lines, which can be arranged in various configurations, such as orthogonal, parallel, over-crossing, or under-crossing. The proximity of these structures can cause adverse effects on existing tunnels, including segment deformation, cracking at joint areas, and uneven vertical and longitudinal displacements 5 . When designing and executing tunnel projects that utilize a maintenance system, several key factors require careful consideration. These include the safe load limits for the maintenance system, allowable deformations in the tunnel walls, and the risk of surface subsidence in nearby areas 8 .

To  identify  potential  issues  before  excavation,  numerical  modeling  is  a  method  used.  During  and  after excavation, field observation monitors ground displacement and the forces acting on the tunnels. Researchers have conducted multiple analyses over recent years, demonstrating that the interaction between tunnels and the surrounding ground can significantly impact the troops on the tunnel lining and the extent of surface subsidence. Additionally, the impact of a new tunnel on the maintenance coverage of an existing tunnel is significant when the new tunnel is built next to the existing one 9-14 . The forces on the tunnel lining and the displacement of the soil around the tunnel can be influenced by their relative positions and the timing of their excavation. Furthermore, excavation causes soil compaction in the surrounding area, which alters the interaction between the tunnels. Therefore, reducing soil compaction can improve the interaction between the two tunnels 15-22 .

In  previous  research  on  similar  projects,  Chakri  and  Hasanpour  investigated  the  impact  of  the  Tehran Subway Line 4 tunnel's intersection with the Towhid tunnel on stress distribution, displacements, deformations, and surface subsidence. This article analyzed the effect of increased distance between the double-arched Towhid tunnels  on  the  extent  of  surface  subsidence 23 .  Lai  et  al.  conducted  a  study  on  tunnels  that  do  not  intersect at right angles and exhibit low crossing angles. The behavioral measurements gathered during their research indicated  that  excavating  a  second  tunnel  running  diagonally  beneath  the  primary  tunnel  results  in  both vertical  displacement  and  torsional  deformation 24 .  Liu  conducted  research  on  the  interaction  between  nonlevel  crossing  tunnels  in  Sydney,  with  a  focus  on  the  impact  of  excavation  on  the  existing  tunnel  lining.  To accomplish this, precision instruments were installed 25 . Li et al. researched the effect of the intersection angle of two tunnels in fissured ground. The results indicated an increase in axial tension stress and vertical shear stress in urban tunnels, which was proportional to the rise in the intersection angle. Conversely, the displacement and shear stress of urban tunnels in the horizontal direction increase as the intersection angle decreases. Although variations in the intersection angle of the urban tunnel and ground fissures can have an impact, they cannot significantly reduce the damage sustained by the urban tunnel 26 .  Wang conducted research using numerical and analytical methods to evaluate the effect of excavating parallel tunnels on each other. The study focused on analyzing the dimensions of the tunnels 27 . Afshani et al. researched the impact of excavating parallel tunnels. Notably, this study distinguished itself from others by explicitly focusing on tunnels with an elliptical crossSect 28 . Another notable study in this area is the research conducted by Lin, which investigated the behavior of a tunnel when another tunnel with a low intersection angle passes through it. The study found that reducing the intersection angle between two non-level crossing tunnels results in an increase in asymmetric deformation in the existing tunnel 5 .

Sun et al. conducted shaking table tests in conjunction with numerical analyses to investigate the seismic response of closely spaced intersecting tunnels. Their research primarily focused on the interaction mechanisms between tunnels and the key factors influencing structural behavior under seismic loading, providing insights applicable to seismic design. The results indicated that the crossing angle between tunnels plays a dominant role in the seismic response of the soil-tunnel system. Specifically, ground acceleration, internal forces, and tunnel deformation were found to increase as  the  crossing  angle  enlarged.  Additionally,  other  parameters,  such  as tunnel diameter, burial depth, seismic characteristics, and soil type, have been shown to have significant impacts on the structural response of tunnels 29 . Chen et al. explored the seepage interaction mechanisms between newly constructed  and  existing  tunnels  in  dense  urban  tunnel  engineering  through  model  testing  and  numerical simulations. Their study aimed to clarify the changes in seepage fields and water pressure, providing implications for the design and performance optimization of tunnels. The findings revealed that the overlap of seepage funnels at tunnel intersections leads to notable alterations in the seepage field, resulting in a 20-30% reduction in water pressure  on  tunnel  linings.  Moreover,  the  construction  of  new  tunnels  introduces  additional  seepage  paths, which further decrease water pressure by 10-30%, although it simultaneously causes an asymmetric pressure distribution. Despite reduced inflow in tunnels with small spacing, the overall groundwater discharge was shown to  increase substantially, by up to 53.9% 30 .  Liu  et  al.  proposed  a  simplified  analytical  approach  to  assess  the impacts of above-crossing shield tunneling on existing tunnels. The model's accuracy was validated through comparison with field monitoring data, showing improved agreement over conventional methods such as the Euler-Bernoulli  beam  model.  To  further  explore  tunnel-tunnel  interaction  behavior,  a  parametric  analysis was performed, highlighting the influences of advancing distance, clearance distance, and joint stiffness on the performance of existing tunnels 31 .  Amhar et al. investigated the effects of undercrossing tunnel construction on existing tunnels in soft soil conditions, with a focus on Jakarta Clay. Using a two-step finite element analysis incorporating  the  Hardening  Soil  model,  the  study  first  calibrated  soil  parameters  and  then  evaluated  the structural  response  to  undercrossing  excavation.  The  analysis  revealed  that  excavation  induces  four  distinct stages  of  vertical  displacement  in  the  existing  tunnel,  with  the  most  representative  soil  behavior  captured 32 . Weng et al. examined the influence of constructing a new crossing tunnel on the structural performance of an existing tunnel, with particular emphasis on excavation sequences, clearance, and formation loss. Their analysis revealed a consistent phenomenon of vertical stretching in the existing tunnel, regardless of whether the new tunnel was built above or below it. However, underpass construction was found to induce more pronounced internal forces and deformations compared to overpass construction. Furthermore, variations in clearance were shown to have dual effects. While greater spacing could form load-bearing arches that reduce stress transfer, it simultaneously expanded the extent of collapsed arches and significantly influenced deformation patterns 33 . Zhao et al.  investigated  the  deformation  behavior  of  the  crossing  section  of  two  municipal  road  tunnels  in Hefei City, China, by comparing asymmetric and symmetric construction methods. The results showed that asymmetric  excavation  induced  larger  deformations  in  both  tunnel  structures  and  supporting  piles,  with maximum displacements of 10.57 mm and 6.27 mm at the southern and northern sides, respectively. In contrast, symmetric construction considerably reduced these deformations, with corresponding maximum values of 4.04 mm and 4.13 mm. The findings highlight that symmetric construction is more effective in controlling structural deformations  and  ensuring  tunnel  safety 34 .  Ding  et  al.  proposed  a  simplified  analytical  method  to  evaluate the  deformation  of  existing  tunnels  induced  by  large-diameter  slurry  shield  under-crossing.  The  approach incorporates key construction factors and has been validated against field monitoring data, demonstrating a reliable predictive capacity for engineering applications. The results highlighted the significant influence of the crossing angle on maximum settlement. They provided recommendations for safe clearance values in shield crossing, offering practical guidelines for minimizing risks in tunnel construction 35 .  Dai  et  al.  evaluated  the effects  of  constructing  a  new  railway  tunnel  adjacent  to  an  existing  highway  tunnel,  with  a  focus  on  safetyrelated issues, including displacement and vibration. The results demonstrated that both horizontal and vertical displacements induced by the railway excavation were minimal. Moreover, the vibration velocity generated during blasting remained well below the allowable safety threshold. Overall, the study confirmed that the excavation process posed no significant risk, suggesting that similar highway-railway tunnel crossing projects can be safely and effectively  managed 36 .  Zang  et  al.  investigated  the  effects  of  construction  sequences  on  perpendicularly crossing tunnels using finite element analyses. The study evaluated key responses, including ground surface settlement,  displacement,  and  deformation  of  the  existing  tunnel,  as  well  as  the  bending  moments  induced in the tunnel lining. In addition, the research highlighted the stress-transfer mechanisms in the surrounding soil  caused  by  tunneling  activities,  demonstrating  how  excavation  sequences  play  a  crucial  role  in  shaping soil-structure interaction and ensuring the stability of crossing tunnels 37 .  Fang et al. explored the interaction behavior of interchange tunnels constructed at different crossing angles through numerical simulations. Their findings showed that increasing the crossing angle led to reduced lining stresses but greater vault displacements. In contrast, parallel tunnels exhibited opposite tendencies due to symmetric loading conditions, highlighting the need to consider them separately in design. Based on the analyses, the study recommended adopting a crossing angle greater than 45° and maintaining a tunnel spacing larger than twice the tunnel diameter (2D) to achieve safer and more reliable structural performance 38 .

Multiple  factors,  including  volume  loss,  tunnel  convergence  before  segment  installation,  excavation sequence, intersection angle, and vertical spacing, govern the interaction between non-level crossing tunnels. Previous research has predominantly concentrated on geometric variables such as intersection angle and tunnel spacing, while the influence of excavation priority has been largely overlooked. In this study, a comprehensive three-dimensional finite element analysis is conducted using Plaxis 3D to evaluate tunnel-tunnel interactions. The research explicitly investigates three parameters: the intersection angle, the perpendicular distance between the  tunnels,  and  most  notably,  the  priority  of  excavation  between  shallow  and  deep  tunnels.  The  explicit incorporation of excavation priority constitutes a key novelty of this work, as it has been rarely considered in earlier studies, despite its critical impact on tunnel displacements and lining forces. By integrating this parameter alongside conventional geometric factors, the study provides a more realistic and holistic perspective on the structural response of non-level crossing tunnels.

To  facilitate  a  clearer  understanding  of  the  modeling  framework,  a  flow  chart  has  been  developed  to summarize  the  investigated  scenarios  and  the  associated  parameters.  The  flow  chart  (Fig.  1)  illustrates  the sequential steps of the numerical procedure, including the selection of the intersection angle, vertical distance, and excavation priority. This addition provides a concise visual overview of the parametric study, preceding the detailed comparison of models presented in Table 1.

## Case study region

The Tehran Metro Line 7 extends for approximately 27 km, starting at the Takhti Sport Complex in the eastern part of the city. After advancing nearly 12 km along an east-west alignment, the line changes its orientation at  Navab  Safavi  Highway  and  proceeds  in  a  north-south  direction.  The  line  consists  of  25  stations  in  total, providing a direct connection between eastern Tehran and the northwestern districts. At the junction of Qazvin Street  and  Navab Highway, the project is divided into two segments, east-west and north-south, which are being excavated simultaneously using two Earth Pressure Balance Machines (EPBMs) 39 . In the present study, the analysis, specifically in the region of station S7, has been simulated 40 (see Fig. 2).

The tunnel alignment passes through Quaternary alluvial deposits, which predominantly consist of sand and silt, with occasional layers of clay and sandy silt. Based on detailed geological investigations and complementary field and laboratory tests, the subsurface along the route was classified into six distinct engineering-geological units.  Excavation  was  carried  out  using  an  Earth  Pressure  Balance  Tunnel  Boring  Machine  (EPB-TBM) manufactured by Lovat Co. In this system, the shield and its main components were produced by Lovat, the cutter head by Palmieri Co., and the backup system by SELI Co., which was also responsible for the overall design and assembly of the machine. To ensure precise alignment during tunneling, the TBM was equipped with the TACS guidance system. This system continuously monitored the predefined tunnel route, uploaded before operation, and provided real-time feedback to correct any deviations 41 . Tables 2 and 3provide the soil properties of the target area and tunnel lining, respectively.

Fig. 1 .  Framework of this study.

|                             | Study parameters                              | Study parameters                              | Study parameters                            |
|-----------------------------|-----------------------------------------------|-----------------------------------------------|---------------------------------------------|
| compared parameter          | Intersection angle                            | Vertical distance                             | Excavation priority                         |
| Intersection angle (degree) | 15, 30, 45, 60, 75, 90                        | 90                                            | 90                                          |
| Vertical distance (m)       | 10                                            | 5, 7.5, 10, 12.5, 15                          | 10                                          |
| Excavation priority         | 1 st : Shallow tunnel 2nd : Deep tunnel       | 1 st : Shallow tunnel 2nd : Deep tunnel       | Shallow Then Deep Deep Then Shallow         |
| Reset displacement          | Active after excavation of the shallow tunnel | Active after excavation of the shallow tunnel | Active after excavation of the first tunnel |
| Number of models            | 6                                             | 5                                             | 2                                           |

Table 1 .  Comparison of simulated models.

## Scenarios

To systematically evaluate the influence of different parameters on the interaction between non-level crossing tunnels, three scenarios were considered in this study. Each scenario isolates a specific parameter while keeping the other two constant, thereby enabling a more straightforward interpretation of the individual effects. The investigated scenarios are described as follows:

Scenario 1 - Effect of Vertical Distance:

In this scenario, the vertical distance between the shallow and deep tunnels was varied, while maintaining a constant intersection angle of 90° and a fixed excavation priority (For example, the shallow tunnel was excavated first). Five vertical distances of 5, 7.5, 10, 12.5, and 15 m were analyzed.

Scenario 2 - Effect of Intersection Angle:

This scenario examined the role of the intersection angle while maintaining a constant vertical spacing of 10 m and assigning excavation priority to the shallow tunnel. Six intersection angles of 15°, 30°, 45°, 60°, 75°, and 90° were investigated.

Scenario 3 - Effect of Excavation Priority:

In this scenario, the excavation sequence of the tunnels was varied, while the vertical distance and intersection angle were kept constant at 10 m and 90°, respectively. Two excavation priorities were considered: 1- shallow tunnel excavated first, and 2- deep tunnel excavated first.

This  parametric  framework  provides  a  comprehensive  evaluation  of  how  the  three  key  factors  (vertical spacing, intersection angle, and excavation priority) govern the structural response and interaction of non-level crossing tunnels.

Fig. 2 .  Route plan of Tehran subway line 7.

<!-- image -->

Geographical map

Table 2 .  Geotechnical properties of soil layers 40 .

| Item    | υ     | ψ      | ϕ      | C ref   | γ unsat   | h         | E 50 - ref 2   |   E ur KN/m 2 | E oed 2   |
|---------|-------|--------|--------|---------|-----------|-----------|----------------|---------------|-----------|
|         | -     | degree | degree | KN/m 2  | KN/m 3    | m         | KN/m           |               | KN/m      |
| Layer 1 | 0.3   | 0      | 20     | 10      | 17.5      | 0-1.5     | 15e3           |          15e3 | 45e3      |
| Layer 2 | 0.325 | 3      | 33     | 19.6    | 20.5      | 1.5-15.5  | 49e3           |          49e3 | 147e3     |
| Layer 3 | 0.325 | 5      | 35     | 29.4    | 21.6      | 15.5-30.5 | 98e3           |          98e3 | 294e3     |
| Layer 4 | 0.325 | 5      | 35     | 39.2    | 21.6      | 30.5-45.5 | 147e3          |         147e3 | 441e3     |
| Layer 5 | 0.325 | 6      | 36     | 39.2    | 22.1      | 45.5-75   | 177e3          |         177e3 | 531e3     |

Table 3 .  .General properties of tunnel lining 40 .

| Item    |   υ - |   E KN/m 2 |   γ KN/m 3 | Drained Type   | Material Type   |
|---------|-------|------------|------------|----------------|-----------------|
| Segment |   0.2 |       27e6 |         26 | non-porous     | linear elastic  |

It  is  worth noting that in this study, the displacements were reset to zero after the excavation of the first tunnel. This approach was intentionally adopted to isolate the incremental effect of the second tunnel excavation on the existing tunnel and to enable a direct comparison between different scenarios. Consequently, the absolute cumulative displacements resulting from both tunnels were not evaluated, as such an analysis lies beyond the scope of the present investigation.

## Numerical methodology

This work employs 3D modeling with the finite element software Plaxis 3D to investigate the interaction between non-level crossing tunnels. Plaxis is recognized as a highly robust finite element software capable of analyzing complex geotechnical and structural systems. Thirteen distinct models were utilized to examine all of the desired modes. To minimize the impact of boundary conditions on the output results, the constructed models were standardized to a size of 75 m in each direction. This size was determined through a geometric analysis to ensure that boundary effects on the results are negligible. In contrast, larger model sizes would only increase computational run time without affecting accuracy.

Fig. 3 .  the geometry of one of the simulated models (intersection angle is 60 degree).

<!-- image -->

Engineering drawing

Fig. 4 .  Mesh dependency analysis.

<!-- image -->

Scatter plot

The inner diameter of the tunnel is 6 m, and the thickness of the tunnel lining segments is 30 cm. The tunnel excavation is simulated in stages with a step length of 1.5 m. Initially, 9 m of excavation are performed without  segment  installation,  as  this  portion  remains  under  the  protection  of  the  TBM  shield.  With  each subsequent excavation step, 1.5 m of the tunnel becomes exposed beyond the shield, at which point the tunnel lining segments are applied in the model to maintain stability. This staged excavation process continues until the tunnel is entirely constructed. To realistically simulate the TBM face pressure, a distance of twice the tunnel diameter at each tunnel end is left unexcavated, ensuring that the face pressure is appropriately applied to the mechanized excavation machine. In all models, the groundwater level is set to coincide with the bottom of the model to eliminate the influence of groundwater on the results. Regarding the boundary conditions, the top surface of the model is free in all directions. The lateral surfaces are allowed to move vertically but are restrained in the horizontal direction, preventing horizontal displacement. The bottom surface of the model is fixed in all directions, restricting any movement. Figure 3 depicts the geometry of one of the constructed models, serving as a representative illustration.

The soil in the area of interest exhibits hardening soil behavior and displays elastic properties. Excavation is performed by eliminating soil components inside the tunnel and engaging its lining. The design of the study and analysis utilizes parameters obtained from Tehran's Subway Line 7.

## Mesh dependency analysis

To verify that the numerical results are not sensitive to the discretization, five mesh levels were analyzed. The current mesh comprises 229,558 elements, resulting in a maximum invert settlement of - 1.555 mm (for an intersection angle of 15 degrees). Using identical boundary conditions and material parameters, coarser and finer meshes were tested, and the corresponding settlements were compared. The relative change between the current and fine meshes was within 3-5%, confirming that the adopted mesh provides an adequate balance between accuracy and computational efficiency. The detailed values are illustrated in Fig. 4. Based on these findings, the other models were developed for the medium mesh type. Figure 5 depicts the meshed geometry of the numerical model.

## Simulation results and analysis

This section examines the outputs generated from the simulated models, demonstrating the impact of the three parameters mentioned in the preceding paragraph.

## Excavation priority

Two distinct models were simulated to analyze the impact of excavation priority on tunnel displacement and induced forces on the lining. In both models, the vertical distance between the two tunnels is standardized to 10 m, and their intersection angle is set at 90 degrees. The first model involves initially excavating the shallow tunnel,  and  after  completion,  the  displacement  in  the  model  is  considered  zero  before  excavating  the  deep tunnel. The second model follows a similar process to the first, except that the shallow tunnel is excavated after the deep tunnel. Figure 6 provides a schematic plan view of the simulated tunnels.

Figure  7  displays  the  vertical  displacement  curve  of  the  tunnel  invert,  which  is  depicted  for  half  of  the tunnels due to symmetry. According to Fig. 7, excavating the deep tunnel as the second tunnel results in vertical displacement at the invert of the shallow tunnel. The maximum displacement observed is 1.81 mm. However, when the shallow tunnel is excavated as the second tunnel, an unloading operation occurs, resulting in an uplift in the deep tunnel. This uplift also affects the existing tunnel, resulting in an uplift of 0.73 mm at the invert of the deep tunnel. The uplift intensity, compared to the vertical displacement created in the other model, is lower. Therefore, when a tunnel passes beneath an existing tunnel in the area, its impact should be examined thoroughly, and its behavior must be assessed accordingly.

To analyze the impact of excavation priority on induced forces and bending moments, four points on the tunnel circumference, located at the center of the intersection, were selected. These points include the invert,

Fig. 5 .  meshed geometry.

<!-- image -->

Engineering drawing

7

Fig. 6 .  Schematic plan view of the simulated tunnels.

<!-- image -->

Engineering drawing

Fig. 7 .  Vertical displacement of tunnel invert.

<!-- image -->

Line chart

crown, side A (located on the positive side of the coordinate axis), and side B (located on the negative side of the coordinate axis.

Based on this assumption, when a tunnel passes beneath an underground structure, the support system of the existing structure experiences a more significant amount of induced force and bending moments. When the shallow tunnel is excavated as the second tunnel, the axial force applied to the deep tunnel lining in the invert is reduced by approximately 80%. This percentage decreases to 87%, 70%, and 58% for the crown and sides A and B of the deep tunnel, respectively. It is worth noting that the tunnel crown is the most significantly affected by this excavation method. Moreover, the excavation of the deep tunnel as the second tunnel results in the highest induced bending moment values on the tunnel lining. Specifically, the induced bending moment value for the crown of the shallow tunnel is 59% higher than that of the deep tunnel. This value is 61% for the tunnel invert and 67% and 46% for sides A and B, respectively. Overall, when a tunnel passes beneath an existing tunnel, it imposes more significant stress and force on the existing tunnel compared to when it passes over it.

<!-- image -->

Engineering drawing

Figure 8 compares the distribution of axial forces (n 1 and n 2 )  and torsional moment (m 12 )  in  the  tunnel lining for two excavation sequences: 1- shallow tunnel excavated first followed by the deep tunnel (top row), and 2- deep tunnel excavated first followed by the shallow tunnel (bottom row). Negative values (red) denote compressive forces, whereas positive values (blue) correspond to tensile forces.

When the shallow tunnel is excavated first, the subsequent excavation of the deep tunnel produces significant additional loading on the shallow tunnel lining. The axial forces (n 1 , n 2 ) reveal strong compressive peaks along the invert and crown, with maximum values reaching nearly - 222.6 kN/m, while tensile zones of about + 720.6 kN/m develop at the spring lines. The torsional moment (m 12 ) is moderate in this case, with peak magnitudes of approximately + 621.3 kNm/m, indicating some asymmetric deformation but without severe concentration. This response suggests that the shallow tunnel remains relatively stable when it precedes the deep excavation, though it is subjected to additional compression from the underlying tunnel activity.

In contrast, when the deep tunnel is excavated first, the excavation of the shallow tunnel above it imposes more severe effects on the deep tunnel lining. The axial forces show much sharper distributions, with compressive peaks  up  to  - 284.6  kN/m  (an  increase  of  about  27.85%  compared  with  the  shallow-first  case)  and  tensile values exceeding + 294.7 kN/m. The torsional moment m 12 also intensifies significantly, reaching about + 594.8 kNm/m, which is nearly 4.26% lower than in the shallow-first scenario. The force and moment fields are highly concentrated, reflecting stronger structural demand and greater susceptibility to distortion of the deep tunnel when it is constructed prior to the shallow tunnel.

Overall,  the  results  clearly  demonstrate  that  excavation  priority  plays  a  decisive  role  in  tunnel-tunnel interaction. Two distinct behavioral patterns emerge: 1- Shallow-first excavation: Results in moderate induced forces and moments on the shallow tunnel, with stresses more evenly distributed and torsional effects relatively

<!-- image -->

Engineering drawing

<!-- image -->

Icon

<!-- image -->

Pie chart

<!-- image -->

Engineering drawing

<!-- image -->

Logo

<!-- image -->

Logo

<!-- image -->

Icon

<!-- image -->

Logo

Fig. 8 .  Structural response of tunnel linings under different excavation priorities.

<!-- image -->

Logo

limited. 2- Deep-first excavation: Produces considerably higher compressive and tensile forces, as well as larger torsional moments in the deep tunnel lining, making this scenario structurally more critical.

From a design perspective, these findings highlight that when non-level tunnels intersect, excavating the shallow tunnel first is structurally more favorable, as it reduces the magnitude and concentration of stresses and moments compared with the reverse sequence.

Figure 9 illustrates the vertical displacement contours in the existing tunnel under two excavation priority scenarios: 1- excavation of the shallow tunnel first, followed by the deeper one, and 2- excavation of the deep tunnel first, followed by the shallow one.

In the shallow-first case, the maximum vertical displacement of the section reaches approximately + 3.204 mm (an uplift), while the minimum displacement is close to - 3.976 mm, indicating a clear settlement trend. The deformation  is  concentrated  around  the  tunnel  crown  and  invert,  forming  a  relatively  localized  settlement bowl directly above the deeper tunnel. The displacement distribution along the lining shows that the crown experiences the largest downward movement, while the spring line and invert are less affected. The surrounding soil also shows symmetric settlement patterns, confined to the vicinity of the excavation.

In contrast, in the deep-first case, the maximum vertical displacement in the section rises to about + 4.051 mm, with the minimum displacement close to - 4.723 mm. The deformation zone, however, becomes wider and extends towards the ground surface. Unlike the shallow-first scenario, the displacement is not limited to the crown of the  existing  tunnel  but  propagates  across  the  upper  soil  layers.  The  tunnel  lining  exhibits  a  more uniform distribution of displacements, with smaller variations between the crown, spring line, and invert.

<!-- image -->

Bar chart

Fig. 9 .  Effect of excavation priority on the settlement of the existing tunnel and surrounding ground.

<!-- image -->

Engineering drawing

## Vertical distance

To investigate the impact of the vertical distance between two tunnels on their interaction, five separate models were simulated. In each model, the intersection angle is set at 90 degrees, while the vertical distance between the tunnels varies between 5, 7.5, 10, 12.5, and 15 m. In all models, the shallow tunnel is excavated first, and after excavation, the resulting displacements are reset. Then, the deep tunnel is excavated to assess the impact of the excavation on the existing tunnel. Figure 10 displays the vertical displacement curves of the existing tunnel invert resulting from the excavation of the tunnel beneath it. Due to symmetry, the curve is illustrated in half of the shallow tunnel. Increasing the distance between the two tunnels leads to an expansion of the affected region on the existing tunnel's invert. The impact is so significant that it affects both the beginning and end of the existing tunnel in the simulated models. When the vertical distance between the two tunnels is increased to 15 m, the increase in displacement at the beginning and end of the tunnel is less than 0.2 mm, compared to when the distance is 5 m. The maximum vertical displacement in the existing tunnel is 1.88 mm, which increases as the vertical distance between the two tunnels increases. This increase is approximately 0.15 mm or 8.3%. It is expected that there will be no significant increase in vertical displacement by increasing the distance beyond 15 m since the curves for distances of 7.5, 10, and 12.5 m have nearly identical values at the peak point.

As per Sect. 3.1, the same four points were chosen to study the impact of an increase in the vertical distance between two tunnels on the induced axial force and bending moment.

The results indicate that the selected points on the tunnel invert and crown are experiencing tensile stress, while the points on the sides are experiencing compressive stress. As the vertical distance between the two tunnels increases, the induced forces show an almost constant trend. The most significant change observed is a slight alteration in the induced axial force on the invert tunnel when the vertical distance between the two tunnels reaches 15 m. In contrast, the changes in other locations remain relatively constant, with an average change of approximately 1%. The average change for the tunnel invert and crown is approximately 6.5 KN/m, while for the sides, it is about 25 KN/m.

The results indicate that increasing the vertical distance between two tunnels has an insignificant effect on the distribution of induced bending moments on the tunnel lining. Most changes occur in the tunnel invert, with a decrease of 3.5% observed. The reduction in changes for the crown and sides averages around 2%. The values for induced bending moments are 400 KNm/m for the invert, 650 KNm/m for the crown, and 510 KNm/m for the sides. Like the axial force distribution, the bending moment changes also exhibit a constant trend. In conclusion, the distribution curve of axial force and bending moment shows a slight slope, resembling a horizontal line, as the vertical distance between the two tunnels increases.

Figure 11 presents the distributions of axial forces (n 1 and n 2 ) and torsional bending moment (m 12 ) in the lining of the existing tunnel for different vertical distances between the tunnels (5, 7.5, 10, 12.5, and 15 m), while the intersection angle is kept constant at 90°. Negative values (red) indicate compressive forces, whereas positive values (blue) represent tensile forces.

At the minimum spacing of 5 m, the influence of the underlying tunnel is most significant. The compressive peaks of n 1 and n 2 reach approximately - 111.6 and - 222.3 kN/m, while tensile responses approach + 933.1 and + 925.7 kN/m. The torsional moment m 12 also shows its maximum intensity at this distance, with peak values around + 617.7 kNm/m. The stress and moment fields are highly concentrated near the intersection region, indicating strong structural demand on the lining.

Fig. 10 .  Vertical displacement of tunnel invert.

<!-- image -->

Line chart

Fig. 11 .  Structural response of the tunnel lining under varying vertical distances (at 90° intersection angle).

<!-- image -->

Table

As the distance increases to 7.5 and 10 m, a gradual changing in the intensity of both compressive and tensile forces is observed. For example, at 10 m spacing, the peak compressive force in n 1 reduces by nearly 16.4% compared with the 5 m case, while tensile forces increase by about 2.95%. Similarly, the maximum torsional moment declines to about + 619.3 kNm/m, representing a increase of nearly 0.26% from the minimum spacing. The stress distribution also becomes slightly more uniform, reducing the extent of localized peaks.

At larger distances of 12.5 and 15 m, the interaction between the tunnels becomes less pronounced. The axial forces show relatively stable values, with compressive peaks around - 113.6 and - 112.8 kN/m, which are approximately 1.43% lower than those at 5 m spacing. The tensile responses also decline moderately. The torsional moment m 12 exhibits a decreasing trend, with maximum values near + 620.4 kNm/m at 15 m, corresponding to a increase of about 0.43% relative to the closest spacing.

In  general,  the  results  demonstrate  that  decreasing  vertical  spacing  intensifies  the  structural  demand  on the existing tunnel, producing higher compressive/tensile forces and torsional moments, all localized near the intersection region. Conversely, increasing the vertical distance mitigates these effects, leading to more stable and moderate stress distributions. However, beyond 12.5-15 m, the rate of reduction in forces and moments becomes marginal, indicating that the interaction stabilizes and further spacing provides only limited additional benefit.

Figure 12 presents the distribution of vertical displacement in the existing tunnel for different vertical spacings (H) between the crossing tunnels at a fixed intersection angle of 90°. The results clearly demonstrate that the vertical separation plays a decisive role in the magnitude and spread of settlement. At a spacing of H = 5 m, the maximum settlement of the cross section reaches 3.068 mm, concentrated at the crown and propagating symmetrically into the surrounding soil. Increasing the spacing to H = 7.5 m slightly increases the displacement to 3.163 mm, indicating that modest separation does not significantly mitigate the induced deformation. At H = 10  m,  the  settlement  further  rises  to  3.204  mm,  showing  that  the  impact  of  the  underlying  excavation continues to be directly transferred to the upper tunnel. Interestingly, at H = 12.5 m, the maximum displacement decreases sharply to 2.260 mm, representing a ~ 29.5% reduction compared to H = 10 m. This indicates that beyond a certain  vertical  distance,  the  stress  interaction  between  the  two  tunnels  is  significantly  alleviated, resulting in a more favorable condition for the stability of the existing tunnel. However, when the spacing is further increased to H = 15 m, the settlement increases again to 3.304 mm, which is the largest value among all cases (~ 46.2% higher than H = 12.5 m). This suggests that very large separations may reintroduce instability due to redistribution of stresses and ground arching effects.

From the  perspective  of  deformation  distribution,  smaller  spacings  (H = 5-10  m)  result  in  concentrated settlements directly above the underlying tunnel, while at H = 12.5 m the affected zone becomes narrower and less intense. For H = 15 m, however, the deformation zone elongates upward and regains intensity, indicating a less favorable stress transfer condition. Overall, the findings highlight that an intermediate vertical spacing (around  12.5  m  in  this  case)  provides  the  most  favorable  condition,  minimizing  the  settlement  magnitude and reducing the affected zone. Both smaller and larger separations result in higher displacements and wider influence zones, emphasizing the need for optimized tunnel spacing in design.

## Intersection angle

Six separate models were simulated to investigate the impact of a specific parameter on the interaction between two tunnels. The vertical distance between the tunnels in all models was set to 10 m. In each model, the shallow tunnel was excavated first. After resetting the displacements, the deeper tunnel was excavated to evaluate the effect of the second tunnel excavation on the existing tunnel. For the analysis of this parameter, angles of 15, 30, 45, 60, 75, and 90 degrees were chosen. To examine the impact of this parameter on the existing tunnel, the sinking pattern was analyzed in three parts, namely the tunnel invert, side A, and side B, as mentioned earlier. The simulated tunnels' schematic plan view is shown in Fig. 13.

Figure 14 illustrates the tunnel invert vertical displacement curves in the simulated models. As a result of symmetry, the curve is represented in half of the shallow tunnel. Excavating the second tunnel has the most significant impact on the shallower tunnel when the intersection angle is 15 degrees. This is because, at the lowest intersection angle of 15 degrees, the two tunnels are nearly stacked on each other, resulting in the most significant impact. As a result, noticeable vertical displacement occurs along the entire length of the tunnel. The peak displacement at this intersection angle is 1.5 mm.

As the intersection angle increases from 15 to 45 degrees, the maximum vertical displacement of the existing tunnel invert decreases. Additionally, points located further away from the intersection center are less affected by the excavation of the second tunnel. At an angle of 45 degrees, the displacement at the end of the tunnel (in the simulated model) approaches zero. However, as the intersection angle approaches 90 degrees, the vertical displacement in the center of the intersection increases. At an intersection angle of 90 degrees, the maximum sinking occurs, with a value of 1.8 mm. The vertical displacement of the tunnel invert has a degree of symmetry. This indicates that the sinking at angles (15, 75) and (30, 60) degrees is nearly identical.

The reason for the highest displacement at a 90-degree angle can be attributed to the fact that the affected area is at its minimum, and the intersection part is the only area involved. Thus, all the effects are concentrated in this area, resulting in the most substantial displacement. As the intersection angle decreases, a larger tunnel area is affected, resulting in a decrease in the maximum vertical displacement value. In the case of small angles, the entire length of the tunnel is impacted by the excavation of the second tunnel beneath it. This increases the sinking along the entire length of the tunnel due to the force of gravity and the void created under the first tunnel.

Figures  15  and  16  depict  the  vertical  displacement  on  sides  A  and  B.  Figures  15  and  16  show  that  the displacements on the sides have almost symmetry. Reducing the intersection angle leads to more significant portion of the existing tunnel length being affected by the excavation of the second tunnel, similar to the tunnel invert. Therefore, the vertical displacement at both ends of the simulated tunnel model is considerable due to the more significant portion of the tunnel being impacted. Furthermore, as the intersection angle increases, the peak point of the vertical displacement shifts toward the center of the intersection.

Based on Figs. 15 and 16, the vertical displacement curves on both sides exhibit symmetry. Considering a three-dimensional perspective, it can be concluded that the existing tunnel experienced torsional deformation due to the excavation of the second tunnel from underneath it.

Fig. 12 .  Effect of vertical spacing on the settlement of the existing tunnel and the surrounding ground.

<!-- image -->

Engineering drawing

The investigation of the forces and induced bending moments on the lining of the first tunnel resulting from excavating the second tunnel beneath it revealed that, as in the previous cases, the crown and invert of the tunnel experience tensile stress. In contrast, points on the sides experience compressive stress. The changes in the forces and induced bending moment exhibit an almost constant trend, with minor fluctuations that can be disregarded. Nonetheless, these changes show slight fluctuations with variations in the intersection angle.

The analysis results indicate that the average induced axial force in the tunnel invert and crown is 5 KN/m and 7.5 KN/m, respectively. However, for the sides, this value is 20 KN/m. Additionally, the induced bending moment in the tunnel invert and crown is 800 KNm/m and 400 KNm/m, respectively. In contrast, the sides experience an induced bending moment of 500 KNm/m.

Fig. 13 .  schematic plan view of the simulated tunnels.

<!-- image -->

Engineering drawing

Fig. 14 .  vertical displacement of the tunnel invert.

<!-- image -->

Line chart

Figure 17 illustrates the distributions of axial forces (n 1 and n 2 ) and torsional bending moment (m 12 ) in the lining of the existing tunnel for intersection angles of 15°, 30°, 45°, 60°, 75°, and 90°. Each row corresponds to one intersection angle, while the three columns represent n 1 , n 2 and m 12 , respectively. In these plots, compressive forces are shown in red (negative values) and tensile forces in blue (positive values). At small intersection angles (15°-30°), the induced axial forces are distributed over a wide portion of the tunnel lining. For example, at 15°, the maximum compressive force in n 1 reaches approximately - 98.93 kN/m, while the peak tensile force is  about + 345.7  kN/m.  At  30°,  the  magnitudes  remain  slightly  comparable  (within  ~ 3%  variation),  but  the distribution becomes slightly more localized. The torsional moment (m 12 ) is relatively small in this range, with peak values of + 224.1 kNm/m, indicating a more uniform response. As the intersection angle increases to 45°

Fig. 15 .  Vertical displacement (side A).

<!-- image -->

Line chart

Fig. 16 .  Vertical displacement (side B).

<!-- image -->

Line chart

and 60°, the concentration of forces becomes more evident. At 45°, the compressive peak of n 1 increases to - 111.5 kN/m (about 12.7% higher than at 15°), while tensile values in n 2 reduce slightly, reflecting a redistribution of stresses toward the crown and invert. By 60°, the torsional moment intensifies, with a minimum magnitude of + 190.4 kNm/m. This highlights the growing importance of torsional effects as the crossing angle enlarges.

At large angles (75°-90°), the structural response is strongly concentrated around the intersection region. For n 1 , the compressive peak at 90° reaches about - 111.1 kN/m, which is nearly 12.3% higher than at 15°. Similarly, tensile peaks in n z exceed + 660.9 kN/m, showing an approximate 16.53% reduction relative to the small-angle scenario. The torsional bending moment reaches its moderate value at 90°, with values close to + 631.1 kNm/m, almost three times larger than those observed at 15°. This indicates that perpendicular crossing produces the most critical loading condition, with highly localized but severe structural demands on the lining.

Fig. 17 .  Structural response of the tunnel lining under varying intersection angles.

<!-- image -->

Table

In summary, two distinct behavioral regimes can be identified: 1- Distributed loading regime (small angles, 15°-30°): The induced axial and torsional responses are spread over a large portion of the tunnel circumference, with moderate magnitudes but a wide influence zone. 2- Concentrated loading regime (large angles, 75°-90°): The structural effects are confined to the intersection zone, leading to peak compressive, tensile, and torsional values. From a design perspective, these findings reveal that low-angle crossings require attention to a broader segment of the lining, while orthogonal crossings (90°) demand special reinforcement and monitoring strategies due to the highly concentrated and intensified stresses and moments.

Figure 18 illustrates the distribution of vertical displacement in the existing tunnel cross section for different intersection angles. The results reveal that the magnitude and extent of deformation are strongly dependent on the crossing angle. At 15°, the maximum uplift in section reaches 2.842 mm, which is approximately 145% higher than the value observed at 45°. Increasing the angle to 30° reduces the displacement slightly to 2.610 mm, corresponding to  about  125%  relative  to  the  45°  case.  The  minimum  deformation  occurs  at  45°,  where  the maximum uplift is only 1.159 mm and the minimum settlement is -0.498 mm, providing the most favorable condition. For larger angles, the displacement increases again. At 60°, the uplift rises to 2.344 mm. At 75°, the maximum value reaches 3.273 mm, representing the highest deformation, about + 182% compared with 45°. Similarly, at 90°, the maximum uplift is 3.204 mm, which is + 176% higher than 45°. In terms of deformation distribution, small angles (15° and 30°) cause wider lateral propagation of settlement, affecting a larger portion of the lining. At intermediate angles (45°-60°), the deformation remains localized around the tunnel crown and invert, reducing the impacted area. At larger angles (75°-90°), the vertical displacement zone elongates upward and becomes more intense, indicating a stronger direct transfer of loads from the underpassing tunnel.

Fig. 18 .  Vertical displacement response of the existing tunnel and surrounding ground.

<!-- image -->

Engineering drawing

Table 4 .  General properties for modeling a segment in SAP2000.

| Elasticity Modulus of concrete   |   Poison ratio of concrete | Density of concrete   | Uniaxial compressive strength of concrete   | Elasticity Modulus of rebar   |   Poison ratio of rebar | Density of rebar   |
|----------------------------------|----------------------------|-----------------------|---------------------------------------------|-------------------------------|-------------------------|--------------------|
| 35 GPa                           |                        0.2 | 26 KN/m 3             | 40 MPa                                      | 200 GPa                       |                     0.3 | 76.5 KN/m 3        |

Fig. 19 .  One-meter section of the modeled lining.

<!-- image -->

Engineering drawing

Overall, the analysis highlights that the intersection angle plays a critical role in both the magnitude and the spread of settlement. The results suggest that angles around 45° are most favorable, as they minimize both peak settlement and the affected region, while near-orthogonal crossings produce the most unfavorable conditions for tunnel stability.

## Bending moment-axial force interaction

To evaluate the structural performance of the tunnel during the excavation process, the bending moment-axial force (P-M) interaction diagrams corresponding to the analyzed cases are presented. These interaction diagrams serve as a basis for assessing the stability of the tunnel lining under combined loading conditions. The results are illustrated for the critical excavation scenarios in all three considered cases. It is noted that if the lining maintains stability under the most critical condition of each scenario, its stability in the less severe conditions can also be assured.

The bending moment-axial force (P-M) interaction curve is directly related to the structural characteristics of the tunnel lining. Consequently, it is strongly dependent on the type of construction used for the tunnel lining and requires structural analysis software for its derivation. In this study, SAP2000 was employed to determine the permissible envelope of the tunnel lining capacity. The selected tunnel lining has a thickness of 30 cm and is reinforced with steel bars of diameter d12, as specified in the software's default settings. For every 1.5 m length of  the  lining,  12  reinforcement  bars  are  placed,  positioned  at  the  mid-depth  of  the  section.  The  mechanical properties of the lining are summarized in Table 4, while Fig. 19 illustrates a schematic representative shape of a 3D segment.

Figure 20 presents the permissible envelope curve with a safety factor of 1.2 for the lining considered as the final lining of the modeled tunnels.

Based on the obtained outputs of the induced axial force and bending moment on the tunnel lining in the three considered scenarios, it can be concluded that all the resulting states fall within the permissible bending moment-axial force interaction envelope. Accordingly, the designed lining in this study remains stable under the excavation conditions considered.

Fig. 20 .  Allowable P-M interaction envelope of the tunnel lining.

<!-- image -->

Line chart

## Conclusion

This study employed three-dimensional numerical simulations using Plaxis 3D to investigate the interaction between non-level crossing tunnels under various excavation strategies. A comprehensive parametric analysis was carried out by considering three governing parameters: (i) the intersection angle between the tunnels, (ii) the vertical spacing, and (iii) the excavation sequence. The main findings can be summarized as follows:

- Effect of intersection angle: The intersection angle plays a critical role in both the magnitude and distribution of induced responses in the existing tunnel. At small angles (15°-30°), the settlements are relatively large and extend laterally, affecting a wider portion of the lining. At intermediate angles (around 45°), the vertical displacement and lining forces are minimized, showing up to ~ 60% reduction compared with acute angles. Conversely, large angles (75°-90°) produce the most unfavorable conditions, leading to significant settlements and high axial forces on the tunnel lining.
- Effect of vertical spacing: The vertical distance between the tunnels strongly influences deformation patterns. At small separations (5-10 m), the induced settlements remain high and are directly transferred to the upper tunnel. An optimum condition was observed at a spacing of about 12.5 m, where the maximum settlement decreased by nearly 30% compared to the 10 m case. However, further increasing the distance to 15 m led to renewed growth in settlement, indicating that excessively large spacing may trigger stress redistribution and arching effects.
- Effect of excavation priority: Excavation sequence has a notable effect on the magnitude and spread of displacements. When the shallow tunnel is excavated first, the deeper tunnel excavation induces more localized and intense settlements in the existing tunnel. In contrast, when the deep tunnel is excavated first, the maximum settlement is reduced by about 10-12%, but the deformation zone becomes broader and propagates towards the ground surface.
- Structural response of the lining: The distribution of axial forces and bending/torsional moments along the tunnel lining shows strong dependency on excavation geometry and sequence. Compressive forces typically dominate, but tensile zones also develop under specific conditions, particularly at large crossing angles. The torsional moment (m 12 ) increases with the intersection angle, highlighting potential risks of lining distortion in near-orthogonal crossings.
- Practical implications : The results highlight that an intermediate intersection angle (~ 45°) and a moderate vertical spacing (~ 12.5 m) offer the most favorable conditions, as they minimize both the magnitude of induced deformations and the extent of influence on the existing tunnel. Furthermore, careful consideration of the excavation sequence is essential in design, as shallow-first and deep-first strategies result in different deformation characteristics.
- Future research : Future studies could extend this work by incorporating time-dependent effects such as creep or consolidation, validating results with field monitoring data, and investigating different ground conditions or lining types. Such efforts will further improve the reliability of design recommendations for crossing tunnels in complex urban environments.

## Data availability

The datasets used and/or analysed during the current study available from the corresponding author on reasonable request.

Received: 5 August 2025; Accepted: 16 December 2025

## References

1.  Li, H., Li, X. &amp; Soh, C. K. An integrated strategy for sustainable development of the urban underground: from strategic, economic and societal aspects. Tunn. Undergr. Space Technol. 55 , 67-82 (2016).
2.  Cui, J. &amp; Nelson, J. D. Underground transport: an overview. Tunn. Undergr. Space Technol. 87 , 122-126 (2019).
3.  Lin,  D.,  Zhou, Z., Weng, M., Broere, W . &amp; Cui, J. Metro systems: Construction, operation and impacts. Tunn. Undergr. Space Technol. 143 , 105373 (2024).
4.  Butler, L., Yigitcanlar, T. &amp; Paz, A. Smart urban mobility innovations: A comprehensive review and evaluation. Ieee Access. 8 , 196034-196049 (2020).
5.  Lin, X. T., Chen, R. P ., Wu, H. N. &amp; Cheng, H. Z. Deformation behaviors of existing tunnels caused by shield tunneling undercrossing with oblique angle. Tunn. Undergr. Space Technol. 89 , 78-90 (2019).
6.  Behnen, G., Nevrly, T. &amp; Fischer, O. Soil-structure interaction in tunnel lining analyses. Geotechnik 38 , 96-106 (2015).
7.  Hatzigeorgiou, G. D. &amp; Beskos, D. E. Soil-structure interaction effects on seismic inelastic analysis of 3-D tunnels. Soil  Dyn. Earthq. Eng. 30 , 851-861 (2010).
8.  Wei, M., Song, Y., Wang, X. &amp; Peng, J. Safety diagnosis of TBM for tunnel excavation and its effect on engineering. Neural Comput. Appl. 33 , 997-1005 (2021).
9.  Kawata, T., Ohtsuka, M. &amp; Kobayashi, M. Observational Construction of large-scaled Twin Road Tunnels with Minimum Interval pp. 241-248 (in: Infrastructures Souterraines de Transports, 1993).
10.  Chehade, F. H. &amp; Shahrour, I. Numerical analysis of the interaction between twin-tunnels: influence of the relative position and construction procedure. Tunn. Undergr. Space Technol. 23 , 210-214 (2008).
11.  Shalabi, F. I., Cording, E. J. &amp; Paul, S. L. Sealant behavior of gasketed segmental tunnel lining-Conceptual model. Geomech. Tunn. 9 , 345-355 (2016).
12.  Saitoh, A., Gomi, K. &amp; Shiraishi, T. Influence forecast and field measurement of a tunnel excavation crossing right above existing tunnels, in: International Congress on Tunnelling and Ground Conditions, : pp. 83-90. (1994).
13.  Liu, H. Y., Small, J. C. &amp; Carter, J. P . Full 3D modelling for effects of tunnelling on existing support systems in the Sydney region. Tunn. Undergr. Space Technol. 23 , 399-420 (2008).
14.  Salehi, B., Golshani, A., Rostami, J. &amp; Schneider-Muntau, B. Structural interaction mechanisms in double-shell tunnel linings: influence of slip conditions and shotcrete degradation (Rev. 02). Tunn. Undergr. Space Technol. 166 , 106934 (2025).
15.  Zhu, Y.,  Chen, L.,  Zhang, H., Tu, P .  &amp;  Chen, S.  Quantitative analysis of soil displacement induced by ground loss and shield machine mechanical effect in metro tunnel construction. Appl. Sci. 9 , 3028 (2019).
16.  Wang, H. et al. Effects of construction disturbances on tunnel displacement and the protective role of soil reinforcement in metro tunnels. Sci. Rep. 15 , 19780 (2025).
17.  Zheng, G. et al. A simplified prediction method for evaluating tunnel displacement induced by laterally adjacent excavations. Comput. Geotech. 95 , 119-128 (2018).
18.  Contini,  A.,  Cividini,  A.  &amp;  Gioda,  G.  Numerical  evaluation  of  the  surface  displacements  due  to  soil  grouting  and  to  tunnel excavation. Int. J. Geomech. 7 , 217-226 (2007).
19.  Cheng, C. Y., Dasari, G. R., Chow, Y. K. &amp; Leung, C. F. Finite element analysis of tunnel-soil-pile interaction using displacement controlled model. Tunn. Undergr. Space Technol. 22 , 450-466 (2007).
20.  Zhang, Z., Huang, M. &amp; Wang, W. Evaluation of deformation response for adjacent tunnels due to soil unloading in excavation engineering. Tunn. Undergr. Space Technol. 38 , 244-253 (2013).
21.  Zhang, J. F., Chen, J. J., Wang, J. H. &amp; Zhu, Y. F. Prediction of tunnel displacement induced by adjacent excavation in soft soil. Tunn. Undergr. Space Technol. 36 , 24-33 (2013).
22.  Wang, J. et al. Measurement and analysis of the internal displacement and Spatial effect due to tunnel excavation in hard rock. Tunn. Undergr. Space Technol. 84 , 151-165 (2019).
23.  Chakeri, H., Hasanpour, R., Hindistan, M. A. &amp; Ünver, B. Analysis of interaction between tunnels in soft ground by 3D numerical modeling. Bull. Eng. Geol. Environ. 70 , 439-448 (2011).
24.  Lai, H., Zheng, H., Chen, R., Kang, Z. &amp; Liu, Y. Settlement behaviors of existing tunnel caused by obliquely under-crossing shield tunneling in close proximity with small intersection angle. Tunn. Undergr. Space Technol. 97 , 103258 (2020).
25.  Liu, H. Y., Small, J. C., Carter, J. P . &amp; Williams, D. J. Effects of tunnelling on existing support systems of perpendicularly crossing tunnels. Comput. Geotech. 36 , 880-894 (2009).
26.  Fangtao, L. et al. The effect of intersection angle on the failure mechanism of utility tunnel. Adv. Civil Eng. 2020 , 8864676 (2020).
27.  Wang, H. N., Gao, X., Wu, L. &amp; Jiang, M. J. Analytical study on interaction between existing and new tunnels parallel excavated in semi-infinite viscoelastic ground. Comput. Geotech. 120 , 103385 (2020).
28.  Afshani, A., Akagi, H. &amp; Konishi, S. Close construction effect and lining behavior during tunnel excavation with an elliptical crosssection. Soils Found. 60 , 28-44 (2020).
29.  Sun, F.,  Shi,  L.,  Wang,  J.  &amp;  Wang,  G. Seismic response analysis of close-distance cross tunnels: Shaking table test and numerical parameter analysis 1670-1685 (in: Structures, Elsevier, 2023).
30.  Chen, Z. et al. Seepage interaction mechanism of crossing tunnels and existing tunnels: model test and numerical analysis. Transp. Geotechnics . 46 , 101269 (2024).
31.  Liu,  B.  et  al.  Analytical  solution  for  the  response  of  an  existing  tunnel  induced  by  above-crossing  shield  tunneling. Comput. Geotech. 124 , 103624 (2020).
32.  Yanreginata, M. A. W . &amp; Prakoso, W . A. Numerical Analysis of the Response of Existing Tunnel Structures to Crossing Tunnel Construction in Soft Soil, ASTONJADRO (2024).
33.  Weng,  X.  et  al.  Interactive  effects  of  crossing  tunnel  construction  on  existing  tunnel:  Three-dimensional  centrifugal  test  and numerical analyses. Transp. Geotechnics . 35 , 100789 (2022).
34.  Zhao, C. Y., Yue, R. H., Lin, Y. L., Huang, C. J. &amp; Jiang, X. Investigation on deformation behavior of the crossing section of two municipal road tunnels during construction. Appl. Sci. 12 , 12274 (2022).
35.  Ding, Z., Zhang, M. B., Zhang, X. &amp; Wei, X. J. Theoretical analysis on the deformation of existing tunnel caused by under-crossing of large-diameter slurry shield considering construction factors. Tunn. Undergr. Space Technol. 133 , 104913 (2023).
36.  Xianyao, D., Guobin, W ., Ming, Y. &amp; Yongquan, Z. Safety evaluation of crossing tunnel engineering: A case study. Appl. Sci. 13 , 9459 (2023).
37.  Zang, Y., Gan, P ., Yan, J., Liu, S. &amp; Yan, Z. Effects of construction sequences and volume loss on perpendicularly crossing tunnels. Adv. Civil Eng. 2019 , 6017206 (2019).
38.  Fang, Y., Ni, D., Cai, F., Lu, S. &amp; Weng, Z. 3D numerical investigation of the interaction between interchange tunnels at different angles. Heliyon 10 , e27394. https://doi.org/10.1016/j.heliyon.2024.e27394 (2024).
39.  Chakeri, H., Ozcelik, Y. &amp; Unver, B. Effects of important factors on surface settlement prediction for metro tunnel excavated by EPB. Tunn. Undergr. Space Technol. 36 , 14-23 (2013).
40.  SAHEL Consulting Engineers, Project Line7 Tehran Metro, (2010).
41.  Noori, A. M., Mikaeil, R., Mokhtarian, M., Haghshenas, S. S. &amp; Foroughi, M. Feasibility of intelligent models for prediction of utilization factor of TBM. Geotech. Geol. Eng. 38 , 3125-3143 (2020).

## Author contributions

Mehdi Arash: Writing and editing draft, Conceptualization, Software, InvestigationAlireza Dolatshahi: Writing and reviewing manuscript, Methodology, Formal analysis, InvestigationKourosh Shahriar: Supervision, Writing-reviewing draft, Methodology, Visualization, and Validation.

## Funding

This research received no specific grant from any funding agency in the public, commercial, or not-for-profit sectors.

## Declarations

## Competing interests

The authors declare no competing interests.

## Additional information

Correspondence and requests for materials should be addressed to A.D.

Reprints and permissions information is available at www.nature.com/reprints.

Publisher's note Springer Nature remains neutral with regard to jurisdictional claims in published maps and institutional affiliations.

Open Access This article is licensed under a Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License, which permits any non-commercial use, sharing, distribution and reproduction in any medium or format, as long as you give appropriate credit to the original author(s) and the source, provide a link to the Creative Commons licence, and indicate if you modified the licensed material. You do not have permission under this licence to share adapted material derived from this article or parts of it. The images or other third party material in this article are included in the article's Creative Commons licence, unless indicated otherwise in a credit line to the material. If material is not included in the article's Creative Commons licence and your intended use is not permitted by statutory regulation or exceeds the permitted use, you will need to obtain permission directly from the copyright holder. To view a copy of this licence, visit  h t t p : / / c r e a t i v e c o m m o ns . o r g / l i c e n s e s / b y - n c - n d / 4 . 0/ .

© The Author(s) 2025
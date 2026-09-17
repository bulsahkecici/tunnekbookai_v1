<!-- image -->

Logo

Studia Geotechnica et Mechanica, Vol. XXXV, No. 2, 2013

DOI: 10.2478/sgem-2013-0020

## 3D MODELLING OF TUNNEL EXCAVATION USING PRESSURIZED TUNNEL BORING MACHINE IN OVERCONSOLIDATED SOILS

RAFIK DEMAGH

University of Batna, Civil Engineering Department, Algeria.

FABRICE EMERIAULT

Grenoble-INP, UJF-Grenoble 1, CNRS UMR 5521, 3SR, Grenoble F-38041, France.

FARID HAMMOUD

University of Batna, Civil Engineering Department, Algeria.

Abstract :  The  construction  of  shallow  tunnels  in  urban  areas  requires  a  prior  assessment  of  their effects on the existing structures. In the case of shield tunnel boring machines (TBM), the various construction stages carried out constitute a highly three-dimensional problem of soil/structure interaction and are not easy to represent in a complete numerical simulation. Consequently, the tunnelling-induced soil movements are quite difficult to evaluate. A 3D simulation procedure, using a finite differences code, namely FLAC3D, taking into account, in an explicit manner, the main sources of movements in the soil mass is proposed in this paper. It is illustrated by the particular case of Toulouse Subway Line B for which experimental data are available and where the soil is saturated and highly overconsolidated. A comparison made between the numerical simulation results and the insitu measurements shows that the 3D procedure of simulation proposed is relevant, in particular regarding the adopted representation of the different operations performed by the tunnel boring machine (excavation, confining pressure, shield advancement, installation of the tunnel lining, grouting of the annular void, etc). Furthermore, a parametric study enabled a better understanding of the singular behaviour origin observed on the ground surface and within the solid soil mass, till now not mentioned in the literature.

## 1. INTRODUCTION

During  shield  tunnelling,  soil  movements  induced  by  tunnel  boring  machines (TBM) (deformations  of  surrounding  tunnel  ground  and  surface  settlement)  are  the result  of  a  complex  sequence  of  operations:  excavation,  front  support,  shield  advancement, grouting of the annular void, grout percolation along the shield and grout consolidation. This complexity makes the explicit numerical simulation of the shield tunnelling difficult and at a particular design phase, the movements should be evaluated by accurate numerical modelling.

During the last decade, several 3D phased simulations of tunnel boring processes, generally for soft and saturated soils, have been proposed by various authors [5], [10],

[12]-[15]. On the other hand, only limited information is currently available, regarding ground disturbance associated with shield tunnelling in overconsolidated materials which can be found in [1] and [16].

In spite of the current progress in terms of means and computing time, 3D calculations remain long and numerical problems frequent. In addition, the confrontation with results of observations made in-situ shows that the tunnelling-induced phenomena are not  well  known  yet.  This  is  due  to  the  fact  that  the  shield  passage  induces  a  threedimensional field displacement.

In this paper, an explicit 3D simulation procedure of a tunnel boring process is presented. The latter is applied to an underground construction in overconsolidated soil ( K 0 close to 1.7), namely Toulouse Subway Line B [19]. The confrontation with results of observations made on this construction site shows that the proposed versatile  numerical  procedure  is  able  to  take  into  consideration  all  the  complexity  of the tunnelling-induced movements. The simulations were carried out with the driven shield control parameters recorded during the passage under 'Castera' measurement section,  with  undrained  conditions.  The  simulation  results  are  respectively  confronted with the in-situ data collected on the structure site support. These data include  the  ground  movements  at  the  ground  surface  and  within  the  solid  mass.  In addition, a parametric study has allowed us to partially understand the origin of the atypical ground behaviour observed and which till now has not been mentioned in the literature.

## 2. EXPERIMENTAL SUPPORT

## 2.1. MONITORED SECTION

The tunnel was bored using an EPB's (Earth Pressure Balanced shield) from Herrenknecht TBM. The shield has a diameter D = 7.7 m, a length L = 8.4 m and a half conicity equal to 25 mm. The shield crosses essentially homogenous and overconsolidated argillaceous soils ( K 0 is close to 1.7), characterized by a very low permeability (10 -8 to  10 -9 m/s)  with  strong  undrained shear strength cu equal  to  300  kPa.  In  particular, 'Toulouse molasse' is also characterized by constant Young's modulus in the first 10 m equal to 165 MPa, and beyond increases with depth according to the linear relation E ( z )  = E 0 + z . Δ E with E 0  =  66.1  MPa  and Δ E =  9.9  MN/m 2 /m  (Table  2). Based  on  triaxial  test  results,  this  profile  has  been  validated  by  numerical  backanalysis  on  another  monitoring  section  with  similar  geological  context  but  excavated with the conventional method [19]. In addition, as seen in Fig. 2, the roof of the Toulouse molasse coincides with the water table. At the right of the monitored section, the tunnel axis is at a depth of 16.5 m and under a cover of 12.7 m. The liner  rings  are  constituted  of  six  segments  (including  key  segment)  with  35  cm thickness and 1.40 m length. The geometrical parameters of the tunnel, shield and liner  are  summarized  in  Table  1  and  Fig.  1.  The  'Castera'  section,  for  which  the quality results of in-situ measurements are available, has been retained for confrontation and validation.

Fig. 1. Geometrical notation for the tunnel, shield and liner

<!-- image -->

Engineering drawing

Table 1 Geometrical parameters of the tunnel, shield and liner

| Tunnel   | Tunnel   | Tunnel   | Tunnel   | Tunnel   | Shield   | Shield   | Shield   | Shield   | Liner   | Liner   | Liner    | Liner        |
|----------|----------|----------|----------|----------|----------|----------|----------|----------|---------|---------|----------|--------------|
| H        | D        | C / D    | H w      | Gap      | D ext    | D int    | L        | Δ /2     | Φ ext   | Φ int   | Width cm | Thickness cm |
| m        | m        | -        | m        | cm       | m        | m        | m        | mm       | m       | m       |          |              |
| 16.5     | 7.7      | 1.65     | 4        | 20       | 7.7      | 7.65     | 8.4      | 25       | 7.5     | 6.8     | 140      | 35           |

(Source: [19])

Table 2 Mechanical parameters of the soil

| Layer   | Depth m   |   γ kN/m 3 |   K 0 - |   c u kPa |   ϕ u degrees | E MPa   |   ν - |
|---------|-----------|------------|---------|-----------|---------------|---------|-------|
| Fill    | 0-4       |         20 |     0.5 |         0 |            25 | 25      |  0.30 |
| Molasse | 4-10      |         22 |     1.7 |       300 |             0 | 165     |  0.45 |
| Molasse | >10       |         22 |     1.7 |       300 |             0 | E ( z ) |  0.45 |

(Source: [19])

Figure 2 shows the instrumentation of the monitored section. It is constituted of 3 inclinometers (I1-I3) and 5 multipoint extensometers (E1-E5) with automatic acquisition (one total acquisition every 5 seconds). In addition, during the passage of the TBM, a precision levelling was carried out at the end of each ring excavation.

Fig. 2. Monitored Castera section, (source: [19])

<!-- image -->

Engineering drawing

## 2.2. DRIVEN SHIELD CONTROL PARAMETERS

Figure 3 shows the speed progression of the TBM when it is passing under Castera section [20 m before and 50 m after] the front passage. During the shield tunnelling in this portion, it remains almost constant and equal to 1.33 m/hour, which corresponds to the average time of the installation of one ring which is one hour (the liner rings have a length equal to 1.40 m). This information will be useful later on.

Fig. 3. Advancement speed when shield is passing under Castera section

<!-- image -->

Line chart

The main driven shield control parameters are presented in Fig. 4. Figure 4(a) illustrates the evolution of the confining pressure P conf on the front face (normalized to the initial total vertical stress in the tunnel crown crown 0 V σ ), the ratio crown conf 0 V P σ is roughly

constant and equal to 0.6. Figure 4(b) shows the evolution of the injection pressure P grout into the annular void (gap), measured at the exit of the four grout ports and located on the upper shield tail (Fig. 9), normalized also to crown 0 V σ . On the average, the

ratio crown grout 0 V P σ is  comprised between 0.8 and 1.2 in the range [20 m before and 50 m

after] the front passage (monitored section).

At  the  passage  under  the  Castera  section,  the  average  pressure P grout is  equal  to 0.9 crown 0 V σ .  After  that  it  increases  and  reaches  1.2 crown 0 V σ along  the  first  meters  after exhaust  of  the  shield  tail  to  stabilize  at  the  total  vertical  stress crown 0 V σ .  These  values induce a millimetric heave on the ground surface after injection, as will be mentioned in the following paragraph.

Fig. 4. Evolution of driven shield parameters: (a) front pressure, (b) injection pressure

<!-- image -->

Line chart

## 3. NUMERICAL SIMULATION PROCEDURES

The 3D procedure proposed in Fig. 5 for the simulation of the phased excavation is an attempt to accurately describe all the operations achieved by the TBM and the associated phenomena. It is implemented in the commercial numerical code FLAC3D. Using the TBM operation parameters recorded during the passage under the monitoring section (Figs. 3 and 4), this procedure is repeated throughout the shield progression until a stationary section is reached (stabilization of displacements), [7] and [8]. The grid, 75000 nodes, is composed of eight node brick elements. The boundary conditions are imposed in terms of null displacements in the perpendicular direction to the faces. The extent of the grid, in the longitudinal direction, is conditioned by the position  of  the  stationary  section.  The  vertical  symmetry  makes  it  possible  to  limit  the model size. The soils are modelled in elasto-plasticity with the Mohr-Coulomb yield criterion and a non-associated flow rule requiring few parameters.

A conical shape shield, perfectly rigid (the nodes are fixed according to the method called fixed center, [2]), modelled with thin volumetric elements is installed in a virgin ground  solid  mass  for  which  an  initial  state  of  geostatic  stresses  is  instituted  with a horizontal earth pressure coefficient K 0 .

Fig. 5. A complete phased simulation of TBM excavation process, (source: [8])

<!-- image -->

Engineering drawing

Fig. 6. Used mesh: (a) contour of vertical displacement after complete installation of the shield, (b) arch effect of the displacements at the soil/shield interface

<!-- image -->

Engineering drawing

Figure 6(a) shows the state of the deformation field once the shield is completely installed, afterwards, the procedure illustrated in Fig. 5 can be applied. As far as the shield installation is concerned, it is characterized by the fact that in the absence of grout injection, the volume loss is completely filled. The assumption of a fixed center is verified since the deformations evolve in the same way on the excavation perimeter and the total convergence (in the crown, springline and invert of the tunnel) is uniform and equal to the maximum shield conicity Δ = 25 mm. In addition, these movements are confined in the vicinity of the excavation because of the strong undrained shear strength of Toulouse molasse (Fig. 6a).

The excavation is simulated by the deactivation of soil disk elements. The stability of  the  front  face  is  controlled  by  the  normal  pressure  recorded  on  site.  The  latter  is equal to P front =  0.6 crown 0 V σ and  has  a  gradient  with  the  depth  equal  to  22  kN/m 2 per meter (equal to the weight of the excavated soils). This distribution is interdependent of the  shield  and  progresses  with  it.  This  confining  pressure  profile  must  respect  the  instructions of pressure thresholds recorded on the construction site support (see Fig. 9).

The  shield  passage,  simulated  by  the  annulment  of  the  local  tangential  stresses, clears  a  volume  loss  that  is  immediately  filled  by  the  soil  convergence  (large  displacements  taken  into  consideration,  as  shown  in  Fig.  6(a)).  The  interface  which  is attached  on  the  shield  is  activated  as  soon  as  a  contact  is  established  with  the  surrounding ground; the role of this interface is to block the radial ground convergence and  also  to  allow  the  tangential  convergence  by  transverse  deformation  arch  effect (Fig. 6(b)). The volume loss is partially compensated by the possible migration of the grout towards the front of the shield (there is a great uncertainty regarding the postclosing shape of the ground around the shield). Two techniques are used to simulate this migration; either by a pressure applied over a certain back length of the shield, or by a correction of the shield conicity, fixed in order to reproduce a vertical displacement recorded on the construction site (back-analysis on surface and/or tunnel crown vertical displacement). In [10], this second technique is more relevant.

The liner is simulated by a longitudinal model; it can be modelled either by means of shells or volumetric elements. It is characterized by a weaker Young's modulus in order to take into account the seals between the liner prefabricated rings. The injection of the grout into the annular void (the gap parameter is equal to 20 cm) is controlled both  in  volume  and  pressure.  The  choice  of  the  pressure  diagram  denoted P grout (Fig. 5) is justified by the position of the grout ports, located on the upper part of the tail  shield,  as  illustrated  in  Fig.  9.  The  maximum  injection  pressure  is  fixed  on  the vertical displacement measured at the nearest point to the vertical axis of the tunnel (namely Extensometer E3-1 in Fig. 2). It shows in particular that the pressure really transmitted to the ground remains lower than the average pressure measured at the exit of the grout ports. This difference is due to the pressure loss by friction following the flow of the grout as well as to its impregnation of the surrounding ground [9]. Uncertainty  concerning the behaviour of the grout leads to consideration of two principal phases (liquid and solid phase) intercalated by a transitional one:

- The liquid phase corresponds to the incompressible behaviour of the grout in order to fill the annular void and to transmit the injection pressure to the surrounding ground. This  phase  is  simulated  by  the  application  of P grout and  the  reactivation  of  volumetric elements. A pressure gradient is considered in order to take into account not only the actual weight of the grout but also of the injection specific measures. During this phase, the grout is considered elastic-incompressible [10] and is characterized by a high bulk modulus K associated with a low shear modulus G , 10 2 ≤ K / G ≤ 10 3 , [3] and [4]. This phase lasts as long time as the grout keeps entirely its workability, approximately four hours according to [18], which corresponds in average to the pose of four liner rings.
- The transitional phase corresponds to the grout consolidation (drying grout). During this phase, the behaviour of the grout evolves more or less quickly, according to the type  of  the  grout  used  (active  or  inert).  More  consistent,  the  grout  acquires  a  shear strength associated with a sort of compressibility. This phase is simulated by the annulment of the injection pressure and a progressive reduction in Poisson's ratio [11].
- The solid phase corresponds to the final situation where the grout is at least as rigid as the surrounding ground and transmits the efforts of the ground solid mass to the liner [12]. This phase is characterized by the ratio K / G ≅ 1 [11].

This procedure is repeated throughout the shield progression, until reaching a stationary section after a few tens of excavation steps, as illustrated in Fig. 3 (approximately 40 meters after the passage of the front face, Fig. 9).

Because of the impervious nature of the soils crossed (the permeability coefficient is close to 10 -9 m/s), the simulations are carried out under undrained conditions, taking into  account  the  water  table,  which  corresponds  to  the  short-term  behaviour.  The strength parameters of the molasse adopted in this study are those given by the rapid triaxial compression tests [19].

The 3D simulation results are compared to the in-situ data collected on the construction  site  support.  These  data  include  the  movements  of  the  ground  surface  and inside the ground solid mass, as well as the driven shield control parameters.

## 4. RESULTS

## 4.1. REFERENCE CASE

As shown in Figure 7, the tunnel excavation through the highly overconsolidated materials ( K 0  close to 1.7) induced a surface heaving trough with a maximum displacement of approximately 1 mm. This trough is well simulated both qualitatively (evolution during the progression of TBM) and quantitatively. In addition, the final reversed  half-width  trough  [17],  which  is  equal  to  8  m,  as  well  as  the  settlement zones, seem to be in good agreement with the corresponding in-situ recorded measurements.

Fig. 7. Transverse settlement trough: (a) FLAC3D, (b) measurements

<!-- image -->

Line chart

In Fig. 8, the induced horizontal movements measured on the vertical profile close to the tunnel (deep inclinometer I3, Fig. 2, at one diameter of tunnel axis) agree also quite well. Likewise a good result was obtained in relation to the position of the shield head in the final state. The increase of convergence during the progression of the head shield is also well simulated by the 3D simulation procedure proposed.

Fig. 8. Horizontal convergences: (a) FLAC3D, (b) measurements

<!-- image -->

Line chart

The atypical  behavior  recorded,  that  is  5  mm  horizontal  convergence  associated with  1  mm  heave  on  the  ground  surface,  is  essentially  due  to  the  overconsolidated character of the soil crossed. Nevertheless, a variation law of Young's modulus more suitable than that proposed in Section 2 could still refine the results of convergence displacements for a depth in the rage -5 to -10 m.

Figure 9 illustrates the ability of the procedure to describe the effect of the TBM progression through the longitudinal heaving trough, according to the position of the shield head. It shows the relevance of the choices done for the simulation, in particular, the maximum value of the injection pressure, fixed on the vertical displacement of the depth point on the central extensometer recorded in-situ. The results are less convincing  when  the  values  are  fixed  on  the  horizontal  displacement  recorded  on  the nearest inclinometer [9]. In addition, the choice of the injection pressure distribution is justified by the position of the grout ports at the back of the shield tail. The soil/TBM interaction is thus analysed through Fig. 9.

Fig. 9. Longitudinal settlement trough vs history of horizontal convergence

<!-- image -->

Line chart

The ground is not affected as the shield head gets closer to the monitored section, at least until a distance equivalent to 1 diameter. The front passage results in a small heaving movement on the surface associated with a weak horizontal convergence ( Δ H is  millimetric). The passage of the shield tail is characterized by a strong horizontal convergence  (95%  of  total  convergence)  and  the  conicity  volume  loss  results  in a weak movement of heaving on the surface: this illustrates the K 0 effect on the vertical displacements. Indeed, a subsequent parametric study shows that from K 0 ≥ 1.3 it is not any more the injection that controls the movements of surface heaving but the K 0 effect would be more dominating.

During the phase of the injected grout, the volume loss appears to be stabilized and contrary to what was expected, even with the maximum injection, the effect on displacements (in particular, horizontal convergence on the springline level) is not felt or recorded  by  measurements.  This  is  also  confirmed  by  the  displacement  profile  of Fig. 8 on which we observe a continuous convergence, which confirms once again the state of strong overconsolidation of the 'Toulouse molasse'. On the other hand, part of  the  heaving  observed  in  Fig.  7,  with  a  more  important  slope  (Fig.  9)  can  be  assigned, at least partly, to the injection and not only to convergence due to K 0 effect. It is worth noting for this purpose that the injection pressure adopted in calculations and set on the vertical displacement remains lower than half of the average pressure measured  on  the  4  grout  ports.  In  practice,  it  is  generally  recommended  to  inject  with a threshold of pressure slightly higher than the initial vertical stress at the tunnel key. The difference in pressure can be explained by a load loss by friction following the mortar flow during its impregnation of the surrounding ground.

The  grout  consolidation  is  characterized  by  a  return  of  point Δ H to  its  position after the passage of the shield tail, which shows that the proposed procedure to simulate this phase appears to be relevant. It is further observed that the shifted effect of the injection is felt to a distance of 30 m compared to the monitored section where the maximum heaving is recorded.

At the end of the last phase (stabilization of displacements), a ratio Δ H / Δ V close to 4 is recorded (identical to that recorded on the monitored section, [19]).

## 4.2. PARAMETRIC STUDY

A parametric study aiming to show the sensitivity of the model to the most relevant parameters of the 3D simulation is presented. The response of the model is analysed  through  the  following  displacements: Δ F , Δ H and Δ V ,  representing  the  axial extrusion of the front face, the horizontal displacement of the springline and the vertical displacement on the ground surface, respectively.

Fig. 10. Parametric study: (a) effect of K 0 , (b) effect of Poisson's ratio

<!-- image -->

Line chart

Figure 10(a) shows a regular linear evolution of displacements according to the at rest earth pressure coefficient K 0,  through which it can be seen that for a given diagram of injection pressure, the sensitivity of the three parameters with regard to K 0 is identical. Figure 10(a) shows also a ground surface heaving for K 0 ≥ 1.3, whereas for lower values of K 0 a settlement trough is observed.

Figure 10(b) highlights the displacement sensitivity with respect to Poisson's ratio ν . The relevance of the latter is dictated by important computation times when perfectly incompressible materials ( ν = 0.5) are considered. It mainly shows that the displacements remain more or less the same. This can be explained, on the one hand, by the fact that the incompressibility potential of the model is not completely reached and, on the  other  hand,  by  the  length  insufficiency  of  the  model.  The  choice  of  a  Poisson's ratio value of 0.45 instead of 0.49 decreases the computation times by 3.

Figure 11(a) shows the influence of conicity on displacements. In general, when the  conicity  increases,  the  convergence Δ H increases  while  the  axial  extrusion Δ F decreases. Initially, the ground surface heaving Δ V increases when the conicity value doubles from Δ /2 = 12.5 mm to Δ /2 = 25 mm, then Δ V decreases when the conicity passes  from  25  to  50  mm.  This  can  be  explained  by  the  fact  that  in  the  first  case, ground surface heaving is governed by the convergence Δ H on  the  springline  level, while in the second case, decompression on the springline level being total, the vertical extension of the cover [19] attenuates heaving and thus Δ V decreases.

Figure 11(b) shows logically that the extrusion Δ F decreases when P front increases. It  also  shows  that  the  variation  in  the  range  0.3 crown 0 V σ ≤ P front ≤ 0.9 crown 0 V σ has  little effect on the convergence Δ H and consequently the variation of Δ V remains negligible.

Fig. 11. Parametric study: (a) effect of conicity, (b) effect of confining pressure

<!-- image -->

Line chart

Theoretically, the stability of the front face is ensured even with a null pressure on the  front  face  because  of  the  high  undrained  shear  strength cu which  is  equal  to 300 kPa (numerical analysis of face stability of shallow tunnel [6]); however, simulation carried out without confining pressure ( P front = 0) gave an axial extrusion reported to the excavation diameter about 1%, which value allows the collapse of the front face [6]. This can be explained by the overconsolidated state of the molasse ( K 0 close to 1.7).

On the other hand, for a confining pressure P front =  1.2 crown 0 V σ an  excessive  heaving ( Δ V &gt; 2 mm) is observed, which does not show any sign of stabilization.

In the first three cases of Fig. 12, the injection pressure increases according to the same trend from 0.4 crown 0 V σ to  1.2 crown 0 V σ , Δ H and Δ F decrease  and  increase,  respectively, in small proportions, while the ground surface heaving Δ V increases in an emphasized manner.

This  tendency  highlights  the  direct  influence  of  the  injection  pressure  on  the ground surface heaving. The last two calculations show particularly that heaving remains very sensitive to the applied pressure trend and thus to the position of the grout ports at the end of the shield tail.

Fig. 12. Parametric study, effect of grouting pressure

<!-- image -->

Line chart

## 5. CONCLUSIONS

A 3D simulation procedure was proposed to account for all the different operations carried out during shield tunnelling by an EPB's TBM. The procedure was applied to a real case in order to reproduce, by back-analysis, the movements recorded on construction site and for which the experimental data collected show a singular behaviour, namely, movements of the ground surface heaving associated with continuous horizontal convergence at the springline level. This phenomenon can be allotted partially to the strongly overconsolidated nature of the Toulouse molasse. As far as the coefficient K 0  is  concerned,  the  value  of  1.7  taken  into  consideration  provides  a  good agreement between measured displacements and those evaluated numerically by the 3D simulation procedure proposed.

The  confrontation  of  the  simulation  results  (evolution  of  both  longitudinal  and transverse trough and the inclinometer deformations) with the in-situ measurements of the  construction  site  support,  show  that  the  3D  simulation  procedure  is  relevant,  in particular in the adopted representation for the different operations conducted by the tunnel boring machine.

Qualitatively, the calculations carried out in undrained conditions showed a good agreement of the displacements evaluated numerically and those recorded in-situ. The obtained ground surface longitudinal and transverse troughs as well as the transverse horizontal displacement vertical profiles are in good agreement with the measurements (final  values  and  evolution  during  the  TBM  progression).  In  particular,  the  atypical behaviour of the monitored section was displayed.

Nevertheless, uncertainties related to the injection of the mortar remain; if the migration of the mortar appears well simulated by a correction of the conicity, the different phases of the injection remain still difficult to simulate.

In addition to the K 0 effect, a parametric study is undertaken in order to assess an impact of the shield control parameters, namely the confining pressure, the conicity, the injection pressure into the annular void as well as the position of the grout ports.

An increase in the conicity is likely to change, by a subtle play of horizontal decompression and vertical extension, the displacement amplitude on the surface. The influence of the injection pressure, in particular, on vertical displacements, seems to be in good agreement with the instruction generally allowed on the shield tunnelling construction sites, namely P grout = crown 0 V σ . The confining pressure has no important effect on  vertical  displacements,  at  least  by  respecting  the  instruction  0.3 crown 0 V σ ≤ P front ≤ 0.9 . crown 0 V σ

## REFERENCES

- [1] ATTEWELL P.B., FARMER I.W., Ground disturbance caused by shield tunnelling in a stiff, overconsolidated clay , Elsevier, Engineering Geology, 8, 1974, 361-381.
- [2] BENMEBAREK S., KASTNER R., Modélisation  numérique  des  mouvements  de  terrain  meuble  induits par un tunnelier , Revue Canadienne de Géotechnique, 37, 2000, 1309-1324.
- [3] BEZUIJEN  A.,  TALMON  A.M.,  KAALBERG  F.J.,  PLUGGE  R., Field  measurements  of  grout  pressure during tunnelling of Sophia Rail Tunnel , Tunneling. GeoDelft, 2005, 83-93.
- [4] BEZUIJEN A., TALMON A.M., Proceedings of the Geotechnical Aspects of Underground Construction in soft Ground, Bakker et al. (eds.) Taylor &amp; Francis Group, London, 2006, 187-193.
- [5] BROERE W., BRIKGREVE R.B.J., Phased simulation of a tunnel boring process in soft soil , NUMGE, Mestat (ed.), Presses de l'ENPC/LCPC, Paris, 2002, 529-536.
- [6] DEMAGH R., EMERIAULT F., BENMEBAREK S., Analyse numérique de la stabilité du front de taille d'un tunnel à faible couverture en milieu frottant , Revue Française de Géotechnique, 123, 2008a, 27-35.
- [7] DEMAGH R., EMERIAULT F., KASTNER R., Modélisation  3D  du  creusement  de  tunnel  par  tunnelier à front pressurisé dans les sols surconsolidés , Proceedings des Journées Nationales de Géotechnique et de Géologie de l'Ingénieur (JNGG'08) Nantes, 18-20 juin 2008b, 305-312, (in French).
- [8] DEMAGH R., EMERIAULT E., KASTNER R., Shield tunnelling - Validation of a complete 3D numerical simulation on 3 different case studies . Euro:Tun 2009. Proceedings of the 2nd International Conference on Computational Methods in Tunnelling, Ruhr University Bochum, September 2009a, 77-82.

- [9] DEMAGH R., EMERIAULT F., KASTNER R., Modélisation 3D du creusement de tunnel par tunnelier à front pressurisé - Validation sur 3 cas d'études .  Proceedings of the 17ème Conférence de Mécanique  des  Sols  et  de  Géotechnique  (17ème  ICSMGE),  5-9  Octobre  2009b,  Alexandrie,  Egypte, 77-82, (in French).
- [10] DIAS D., KASTNER R., MAGHAZI M., 3D simulation of slurry shield tunnelling , Proceedings of International Symposium on Geotechnical aspects of underground construction in soft ground, Kusakabe et al. (eds.), Balkema, Rotterdam, 2000, 351-356.
- [11] DIERKENS M., Mesures rhéologiques et modélisation de matériaux en cours de prise ,  Ph.D. thesis, INSA-Lyon, 2005.
- [12] KASPER T., MESCHKE G., A 3D finite element simulation model for TBM tunneling in soft ground , Proceedings of the International Journal for Numerical and Analytical Methods in Geomechanics, 28, 2004, 1441-1460.
- [13] KASPER T., MESCHKE G., On the influence of face pressure, grouting pressure and TBM design in soft ground tunnelling , Tunnelling and Underground Space Technology, 21, 2006, 160-171.
- [14] MROUEH H., SHAHROUR I., Modélisation 3D du creusement de tunnels en site urbain ,  Revue Française de Génie Civil, 3, 1999, 7-23, (in French).
- [15] MROUEH H., SHAHROUR I., A simplified 3D model for tunnel construction using tunnel boring machines , Tunnelling and Underground Space Technology, 23, 2008, 38-45.
- [16] MYRIANTHIS M.L., Ground disturbance associated with shield tunnelling, in overconsolidated stiff clay , Springer-Verlag, Rock Mechanics 7, 1975, 35-65.
- [17] PECK R.B., Deep excavations and tunnelling  in  soft  ground ,  Proceedings  of  the  7th  International Conference on Soil Mechanics and Foundation Engineering, Mexico City, State-of-the-art Volume, 1969, 225-290.
- [18] TALMON A.M., AANEN L., BEZUIGEN A., van der ZON W.H., Grout pressure around a tunnel linning , Tunneling. A Decade of Progress. GeoDelft, 2005, 77-82.
- [19] VANOUDHEUSDEN  E.  et  al., Analysis  of  movements  induced  by  tunnelling  with  an  earth-pressure balance  machine  and  correlation  with  excavating  parameters ,  Proceedings  of  the  Geotechnical Aspects of Underground Construction in Soft Ground, Bakker et al. (eds.), Taylor &amp; Francis Group, London, 2006, 81-86.
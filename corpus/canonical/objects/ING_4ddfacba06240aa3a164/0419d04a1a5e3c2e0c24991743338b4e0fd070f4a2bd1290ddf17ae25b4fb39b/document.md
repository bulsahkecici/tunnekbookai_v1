## 3D-FEM ANALYSIS OF SHIELD TUNNEL CONSTRUCTION WITH GROUND-SPRING MODEL

Pattanasak Chaipanna 1 , *Pornkasem Jongpradist 1

1  Department of Civil Engineering, King Mongkut's University of Technology Thonburi, Thailand;

*Corresponding Author, Received: 15 June 2016, Revised: 15 August 2016, Accepted: 30 November 2016

ABSTRACT: The  shield  tunneling  has  been  extensively  implemented  for  construction  of  underground transportation systems in urban areas. Reports on tunnel segment damage during tunnel construction become increasing. The jack thrust force is the essential cause of damage to the segment. The objective of this article is to present the model which analyzes the behavior of tunnel lining during construction. The model consists of five rings and ten segments for each ring connected together with the shear springs which represent the segment joints and ring joints. The zero thickness interface elements are used to model the segment interface behavior and soil stiffness is represented by mean of ground springs. All relevant construction loads are taken into account in the analysis. The ground spring model is implemented into FEM program ABAQUS to analyze the behavior of segmental lining during construction along straight and curve alignments. The analysis results agree with the measurement data and confirm that the stresses of tunnel segments are governed by jack thrust force.  The  ground-spring  model  has  been  proven  to  be  appropriate  for  analysis  of  behavior  of  the  tunnel segments.

Keywords: 3D FEM, Soil-Tunnel Interaction, Ground spring model, and Tunneling construction

## 1. INTRODUCTION

The shield tunneling technology has been continuously developed with remarkable progress. The segmental lining is popularly used in the shield tunneling. The segments are sequentially erected as tunnel  boring  advances,  which  are  consecutively coupled  with  the  bolts  in  the  longitudinal  and circumferential directions of the tunnel. The packing materials are used between segments with the purpose of load distribution.

During the shield tunnel excavation, the tunnel linings are subjected to the construction loads, such as,  the  jack  thrust,  the  shield  tail  pressure,  the grouting pressure and ground pressure.  Many reports of shield segment damage during construction have been increasingly presented and these indicate the significance of construction load [1], [2]. However, the conventional design of tunnel lining  takes  into  account  only  the  serviceability loads in shield tunneling [3], [4].

Nowadays, analysis of shield tunneling can be achieved by mean of three-dimensional (3D) model [5], [6]. These analyses take into account the steps of  tunnel  construction,  but  the  tunnel  lining  is commonly modeled by means of continuous ring. Katebi et al.,[7] and Blom et al.,[8] model tunnel lining by segmental lining, but the surrounding soil is  characterized  by  elastic  medium  which  is  not rational to represent the actual soil behavior.

Although, it is commonly realized that the effect of the tunnel construction loads on the tunnel lining must  be  taken  into  account  in  the  analysis  and design of shield tunnels, only few research has been carried out to grasp the effect of tunnel construction loads  [5],  [6]-[8].  This  paper  presents  a  threedimensional analysis model to enhance the appreciation  of  tunnel  lining  behavior  due  to  the construction loads. The reference case is referred to Nishin-Shinjuku [9] tunnel which allows the verification of the present analysis method.

## 2. REFERRENCE CASE AND FIELD MEASUREMENT

In  order  to  verify  the  appropriateness  of  the present analysis, the field measured data during the construction  of  Nishin-Shinjuku  tunnel  have  been used  to  validate  the  proposed  model  [9].  The Nishin-Shinjuku tunnel is a part of the Metropolitan Expressway Central Ring Shinjuku Line.

The Nishin-Shinjuku Tunnel comprises of twin tunnels  and  a  total  length  of  600  m.  The  outer diameter of tunnel is 13.0 m, thickness is 0.55 m and segmental width is 1.2 m. For field instrumentation, strain  gauges  were  installed  in  first  three  tunnel rings with 10 positions for each ring The Nishin-Shinjuku Tunnel comprises of twin tunnels  and  a  total  length  of  600  m.  The  outer diameter of tunnel is 13.0 m, thickness is 0.55 m and segmental width is 1.2 m. For field instrumentation, strain  gauges  were  installed  in  first  three  tunnel rings with 10 positions for each ring.

Table 1  Soil properties used in analysis [9]

| Earth layer                             |   Value |
|-----------------------------------------|---------|
| Wet density (kN/m 3 )                   |    18.6 |
| Adhesive force (kN/m 2 )                |    38.0 |
| Internal friction angle (deg)           |    37.0 |
| Subgrade reaction coefficient (MN/m 3 ) |    91.0 |
| N value                                 |      50 |

The tunnel crown is located at the depth of 22 m while  groundwater  table  is  at  13  m  below  the ground  level.  The  tunnel  was  excavated  through very dense gravel and very dense sand.  The geotechnical data are tabulated in Table 1.

## 3. ANALYSIS STRATEGY

This section presents a three-dimensional analysis  for  shield  tunneling,  which  takes  into account the soil and water pressures, the tail void grouting pressure, the  wire brush grease pressure, the  jack  thrust  and  soil-tunnel  interaction.  The analysis is performed by means of FE analysis.

The  tunnel  lining  considered  in  the  analysis includes  five  rings,  each  ring  comprises  of  ten segments, which are staggered alignment along the tunnel  axis.  The  segments  are  coupled  with  the segment joints and ring joints  in  longitudinal  and circumferential directions, respectively. These joints are considered using the shear spring elements. The assembly of tunnel lining is illustrated  in  Fig.1  (a).  The  attribution  of  packer material  is  represented  with  the  interface  element which involves the normal and tangential behaviors.

There  are  various  loads  acting  on  the  tunnel lining, such as, jack thrust, wire brush pressure, tail void  grouting  pressure  and  earth  pressure.  These loads  influence  on  the  performance  of  the  tunnel lining.  For  this  reason,  these  loads  are  taken  into account in the analysis, as seen in Fig.1 (b).

The soil-tunnel interaction is modeled by means of  a  series  of  radial  springs  [10],  the  stiffness  of radial  spring  is  regarded  using  nonlinear  elastic behavior (Fig.2). The stiffness of radial springs are varied  along  the  longitudinal  tunnel,  as  seen  in Fig.1(c).

The Ring1 in the model is only subjected by the jack  thrust  in  longitudinal  direction,  no  any  loads acting on radial direction. The grease is injected into the  gap  between  shield  tail  and  the  extrados  of tunnel lining to prevent the external water flow into the shield. The grease pressure acts on the Ring2. Ring3 is subjected by tail  void  grouting  pressure. The  grout  material  is  filled  the  gap  between  the extrados of tunnel lining and surrounding soil. The constant pressure is kept over the hydrostatic pressure of 90 kPa. Ring4 and Ring5 are subjected to the surrounding ground pressure which comprises the soil pressure and water pressure.

The simulation of shield tunneling is divided in two  categories,  the  shield  tunneling  for  straight forward alignment and the curve forward alignment.  The  hydraulic  jack  pattern  for  both categories are illustrated in Fig.3. The black circles are represented the active jack thrust, in the other hand, the white circles are represented the inactive jack thrust.

(a) Configuration of ring and segment joints

<!-- image -->

Engineering drawing

Fig. 1 Loads distribution and boundary condition of analysis model

<!-- image -->

Bar chart

<!-- image -->

Line chart

<!-- image -->

Engineering drawing

Fig. 2 Modeling of the soil-tunnel interaction

<!-- image -->

Engineering drawing

- (a) Straight alignment          (b) Curve alignment

Fig. 3 Configuration of jack thrust.

## 4. ANALYSIS RESULTS

The  simulation  results  of  Ring1,  Ring2,  and Ring3  are  compared  to  the  field  measurements taken  from literature to validate and calibrate this analysis method.

200

<!-- image -->

Engineering drawing

Fig.4  Comparison  of  bending  moment  (kN-m) between  field  measurement  and  present  analysis (Left side for straight alignment and right for curve alignment). 200

<!-- image -->

Engineering drawing

0

Fig. 5 Computed bending moment distribution (kNm).

<!-- image -->

Line chart

The measured and analysis results from Figs.4 to 7 are traced from centerline of tunnel segments. The measured and computed results are compared by means of plotting the results (bending moment, forces and deformation) in the circumferential direction  against  the  circumferential  angle.  The contour  shedding  of  stress  distribution  are  also depicted as illustrated in Figs.8 to 10.

Fig.4 shows the comparison between the measured  and  computed  circumferential  bending moments  of  the  tunnel  Ring1,  Ring2  and  Ring3. The  left  figures  represent  results  of  simulation during straight alignment, and the right figure is for shield tunneling during curve alignment. The circumferential bending moment occurs slightly in the  Ring1  because  there  is  no  external  force  in circumferential  direction;  only  gravitational  force of the segments themselves exists.  The jack thrusts are in longitudinal direction. The moment becomes increasing in Ring 2 and Ring 3 due to the grease and  grouting  pressures,  respectively.  Comparison between the computed and measured results reveal that the analysis can reproduce the moment distribution in a fair agreement with the measured ones. The difference between the straight and curve alignment can be also reflected.

Fig.5 summarizes the computed circumferential bending moments from all 5 rings. The maximum circumferential bending moment occurs in the Ring 5  as  a  result  of  different  vertical  and  horizontal pressures of surrounding soil. The influence of jack thrust (as straight or  curve  alignment) on  the bending moment is clearly seen as shown in Figs. 5(a) - (b).

Fig. 6 shows the distribution of circumferential force comparing between the measured and computed  values.  The  maximum  circumferential force appears in Ring2. For Ring 1 and Ring 2, it is seen that the computed forces are in good agreement with  the  measured  one,  whereas,  the  computed forces  in  Ring  3  are  larger  than  those  of  the measurement.

Fig.  6  Comparison  of  circumferential  force  (kN) between  field  measurement  and  present  analysis (Left side for straight alignment and right for curve alignment).

<!-- image -->

Engineering drawing

200

0

(a) Straight alignment         (b) Curve alignment Fig. 7 Computed circumferential force (kN).

<!-- image -->

Line chart

From figs.4 and 6, it indicates that the analysis results satisfactorily correspond to the measurement for both bending moment and circumferential force. Fig. 7 depicts the computed circumferential forces from all 5 rings. The maximum circumferential load occurs at the invert of Ring 5. The jack thrust does not only affect the axial load, but also the circumferential load. Furthermore, a circumferential load of Ring5 is affected from the jack thrust too. The distribution of circumferential force  of  Ring  5  of  straight  alignment  (Fig.7  (a)) differ slightly from that of curve alignment (Fig.7 (b)).

The distribution of the circumferential stress is shown in Figs.8 (a) to 8 (b) for straight and curve alignments, respectively. The jack thrust has strong influence on the circumferential stress. The circumferential  stress  mostly  concentrated  on  the front face of Ring1 which is in accordance with the position  of  hydraulic  jacks.  The  circumferential stress decreases in Ring2 and Ring3. The circumferential stress increases again in Ring4 and Ring5  due  to  radial  pressure.  The  eccentric  jack thrust  obviously  shows  the  difference  of  stress intensity between the straight and curve alignment. The jack thrust directly affects to the longitudinal stress, this stress concentrates at the hydraulic jack position on the front face of Ring1. The longitudinal stress  gradually  decreases  in  the  other  rings.  The contour  shading  of  longitudinal  stress  of  straight and  curve  alignments  obviously  differ  as  seen  in Figs.9 (a) to 9 (b).

The computed shear stress distribution in tunnel lining is shown in Figs.10 (a) to 10 (b). Due to the tunnel lining is segmental, the shear stress of adjacent  segments  are  transferred  by  mean  of interface elements and tunnel joints. The maximum shear stress occurs at the position of hydraulic jack.

Fig. 8 Distribution of circumferential Stress (kPa).

<!-- image -->

Engineering drawing

Fig. 9 Distribution of longitudinal stress (kPa).

<!-- image -->

Engineering drawing

<!-- image -->

Engineering drawing

a)  Straight  alignment                                b)  Curve

alignment

Fig. 10 Distribution of shear stress (kPa).

## 5. CONCLUSION

A  three-dimensional  analysis  of  shield  tunnel segments  during  construction  has  been  presented, which  takes  into  account  all  relevant  interactions and loads, i.e., soil and water pressures, the grouting pressure, the jack thrust force and  the grease pressure.  The  conclusions  from  this  study  are  as follows:

- The present analysis satisfactorily correspond to the field measurement of case study.
- The analysis results can reproduce the influence of jack thrust on the tunneling behavior.
- The jack thrust influence on both displacement and structural forces of tunnel lining.
- The  jack thrust is the main  cause of the maximum stress in the segment. Therefore, the internal stress of tunnel lining is governed by the jack thrust.

## 6. REFERENCES

- [1] Sugimoto, M., 'Causes of Shield Segment Damages During Construction', in Proc. Int. Symp. On Underground Excavation and Tunnelling, Bangkok, 2006,Thai, pp.67-74.
- [2] Wu  M.Q.,  'Application  study  on  steel  fiber concrete segment in metro tunnel engineering', Guangdon Building Materials 3, 2004, pp.6-8.
- [3] ITA-WG2, 'Guidelines for the Design of Shield Tunnel  Lining',  Tunnelling  and  Underground Space Technology, Vol.15, No.3, 2000, pp.303331.
- [4] Japanese Society of Civil Engineerings (JSCE), 'Japanese Standard for Shield Tunneling', 3rd ed. 1996, Tokyo, Japan.
- [5] Kasper  T. and Meschke  G.,  'A  3D  finite element simulation model for TBM tunnelling in  soft  ground',  Int.  J.  Numer.  Anal.  Meth. Geomech. 28, 2004, pp.1441-1460.
- [6] Katebi  H.,  Rezaei  A.H.,  Hajialilue-Bonab  M. and Tarifard A.,  'Assessment the influence of ground stratification, tunnel and surface buildings specifications on shield tunnel lining loads (by FEM)', Int. J. Tunn. Undergr. Space Techno. 49, 2015.
- [7] Blom C.B.M., van der Horst E.J. and Jovanovic P.S.,  'Three-dimensional  Structural  Analyses of the Shield-Driven Green Heart Tunnel of the High-Speed Line South', Int. J. Tunn. Undergr. Space Techno. 12, 1999, pp. 217-224
- [8] Mo H.H. and Chen J.S., 'Study on inner force and dislocation of  segments  caused by shield machine attitude', Int. J. Tunn. Undergr. Space Techno. 23, 2008, pp.281-291.
- [9] Tajima M., Kishida M., Fukai N. and Saitou M., 'Study on shield tunnel construction loads using  a  three-dimensional  FEM  model',  in Proc. Tunnel Engineering, JSCE Vol.14, 2004, pp.353-360.
- [10] Chaipanna  P.,  Jonpradist  P.  and  Kalasin  T., '3D  FEA  of  Shield  Segmental  Lining  with Ground  Spring  Model',  in  Proc.  ITA-AITES World Tunnel Congress 2012, pp.114-121.

Copyright  ©  Int.  J.  of  GEOMATE.  All  rights reserved,  including  the  making  of  copies  unless permission is obtained from the copyright proprietors.
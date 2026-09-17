## PREDICTION OF SURFACE SETTLEMENT DUE TO TWIN TUNNEL CONSTRUCTION IN SOFT GROUND OF HANOI METRO LINE 03

* Thai Do Ngoc 1 , Kien Dang Van 1 , Vi Pham Van 1  and Quang Nguyen Van 2

1 Faculty of Civil Engineering, Hanoi University of Mining and Geology, Vietnam;  2 Faculty of Civil Engineering, University of Transport Technology, Vietnam;

*Corresponding Author, Received: 13 Jan. 2022, Revised: 28 Feb. 2022, Accepted: 02 April 2022

ABSTRACT: Construction  of  tunnels  in  the  soft  ground  causes  ground  surface  settlement  in  the  urban conditions, especially for tunnels near the surface. The prediction of ground surface settlement caused by a single tunnel is well established in many documents. However, the ground surface settlement induced by the construction of twin tunnels is not well understood, and methods of predicting ground surface settlement in such projects are currently limited. This paper presents the three-dimensional numerical results using the finite element software (Abaqus) for the prediction of surface settlements caused by twin horizontal tunnels of the Hanoi Metro Line 03 excavated in soft ground. One of the aims of the study is to estimate the effect of the distance between tunnels on the magnitude and shape of the surface settlement trough. The results show that the center-to-center spacing of the tunnels has a significant influence on both the magnitude and the shape of the transverse surface settlement trough. The maximum surface settlement developed over twin tunnels will be reduced with an increase in the tunnels' center-to-center spacing.

Keywords: Twin tunnels, Side-by-side tunnels, Finite element method, Ground settlements

## 1. INTRODUCTION

Twin  tunneling  in  urban  areas  is  growing  in response  to  the  increased  need  for  an  improved transportation system. Many urban twin tunnels are constructed  in  the  soft  ground  at  shallow  depths. Urban  tunnels  are  usually  constructed  as  twinparallel  tunnels.  Twin  tunnels  construction  in  the soft  ground  may  cause  ground  movements  [1]. These  ground  movements,  both  horizontal  and vertical, have been reported by many authors [2-17, 25-27]. These authors have shown several methods to  evaluate  the  settlement  of  the  surface,  such  as analytical,  empirical,  and  finite  element  methods for the prediction of ground movements above twin tunnels. However, the settlements of the surface are dependent on many factors, including soil parameters, tunnel geometry, and types of construction methods.

Terzaghi [4] reported that the result of ground movements above twin tunnels is larger than above the first line tunnel. Peck [5] suggested the result of monitoring data for ground movements above twin tunnels driven in dense sand. The result of ground movements by twin tunnels was greater than that for the  first-line  tunnel.  Moretto  [6]  also  reported  a larger settlement for the second tunnel when twin tunnels were constructed in dense silty sand, overlying  firm  clay.  Cording  and  Hansmire  [7] showed that the surface displacements above twin 6m diameter tunnels at 9m centers constructed at a depth  of  15m  in  silty  sand  and  clay.  The  surface settlements  were  received  an  increased  surface settlement for the second tunnel. Hanya [18] studied surface settlements due to twin tunneling in Japan at  various  depths,  diameters  of  tunnels,  and  soil types.  For  most  cases,  the  increased  settlement found  above  a  second  tunnel,  when  the  second tunnel was constructed, is relatively close to the first tunnel. Akins and Abramson [19] recorded ground settlement  above  twin  tunnels  with  a  diameter  of 6.1m at a center-to-center spacing of 6m constructed at a depth of 15m in residual soil. The results showed that an increase in volume loss was found for the second tunnel.

Numerical  modeling  of  twin  tunnels  has  been conducted  by  many  authors.  Addenbrooke  [12] reported  ground  movements  above  twin  tunnels when conducting non-linear finite element analysis of twin tunnels at 4.8m diameter, a depth of 34m, and  various  spacing.  The  results  showed  that  the center-to-center spacing of the tunnels has a significant effect on the ground surface settlement trough. A study of ground movements by non-linear finite  element  analysis  of  twin  tunnels  at  various depths  and  center-to-center  spacing  in  stiff  clay showed that an increase in volume loss was found for  the  second  tunnel  [20].  Kim  et  al.  provided ground movements above twin tunnels when conducting  finite  element  analyses  of  a  second parallel tunnel at a center-to-center spacing of 0.4D and 1.0D. The most significant ground movements were caused by the construction of a nearer tunnel at  a  spacing  of  0.4D.  The  results  showed  good agreement  with  ground  movements  found  in  the laboratory when conducting tests under gravity in Kaolin clay.

This  study  presented  the  results  of  the  finite element analyses using the Abaqus/Standard threedimensional finite element software to predict ground surface settlements above twin tunnels due to the construction of Hanoi metro line 03. These twin 6.3 m diameter tunnels for side-by-side tunnels at a center-to-center spacing of 15m to 30m and the tunnel crown depth of 20 m [22].

One of the aims of the study is to ascertain the effect of changes to the center-to-center spacing on the magnitude and the shape of the ground surface settlement trough.

## 2. GROUND MOVEMENTS DUE TO TWIN TUNNELING

## 2.1 Superposition Method

New  and O'Reilly proposed a method of calculating  ground  surface  settlement  due  to  the construction  of  twin  tunnels.  The  method  sums together  the  settlement  trough  above  each  tunnel [10], as shown in Eq. (1):

## 2.2 Addenbrooke &amp; Potts Method

Addenbrooke and Potts [13] introduced numerical  results  of  twin  tunnels.  The  authors proposed  a  method  for  adjusting  the  predicted settlement  twin  tunnels.  The  volume  loss  of  the second tunnel is greater than that of the first. The position  of  maximum  settlement  (Smax)  above  the second tunnel is offset from the tunnel axis. Figure1 can be used to evaluate the eccentricity of maximum settlement (Smax) and an increase in volume loss of the second tunnel [13].

## 2.3 Modification Method

Hunt [1] provided a different method for predicting ground movements above twin tunnels. The influence of the changes to soil stiffness on the displacement  profile  above  the  second  tunnel  is directly  related  to  the  amount  of  modification applied [1].

The equation of the modified settlement above a second tunnel is shown in Eq. (2):

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

where:  d  is  the  horizontal  distance  between tunnel centers (m); xA is the lateral distance of the center-line  of  the  first  bored  tunnel  (m);  i  is  the distance from the tunnel centreline to the inflection point.

The subsequent longitudinal displacements horizontal  displacements  can  also  be  found  by summation  and  have  been  reported  by  New  and O'Reilly [10].

<!-- image -->

Line chart

Fig.1 Effect of pillar width on the eccentricity of maximum  settlement  (Smax)  and  an  increase  in volume loss of the second tunnel,  where V is the volume loss  from  the  second  tunnel  construction; Vg is the volume loss of the first (greenfield) tunnel construction [13].

where Smod is the modified settlement (m); Sv is the unmodified settlement above the second tunnel competed by semi-empirical method (m); F is the modification function (m), which can be determined using Eq. (3), [1].

<!-- formula-not-decoded -->

Where Z *  = Z0 - Z (m), Z0 is the depth from the surface  to  tunnel  axis,  Z  is  the  depth  from  the surface to the horizon analysis; A is the multiple of i (m); KA is the value of K in the region of the first tunnel bored; d is the center-to-center spacing of the twin tunnels (m); M is the maximum modification.

## 3. NUMERICAL MODELING

## 3.1. Input Parameters and Numerical Computation Scenarios

Hanoi Metro line 03 starts from "Nhon" station, located in the west of the Hanoi city, passes through "Cau  Giay"  and  then  run  towards  the  east,  "Kim Ma"  and  "Cat  Linh",  until  the  "Hanoi"  terminal station as shown in Fig.2. Project metro line 03 of Hanoi Metro Rail System is the first metro of Hanoi city, Vietnam. The length of line 03 from "Nhon" station  to  "Hanoi"  station  is  12.5  km  long  with  a mixed path  passing  from  surface  to  underground. The elevated part is 8.5 km long from the "Nhon"

station to the "Kim Ma" station using the cut and cover method. The underground part is 4 km long from the "Kim Ma" station to the "Hanoi" station using the mechanized tunneling method [22], [23].

Fig.2 Hanoi metro line 03 "Nhon - Hanoi" station

<!-- image -->

Engineering drawing

Profile  of  Hanoi  metro  line  03  with  twin  6.3  m diameter  tunnels  excavated  side-by-side  and  at  a center-to-center spacing of 15 m to 30 m, the tunnel crown depth of 20 m is shown in Fig.3.

Fig.3 Cross-section profile of the twin tunnels and different soil layers

<!-- image -->

Engineering drawing

According to the investigated geological conditions, the twin tunnels located in the stratum, mainly stiffer clay, sand, or silty sand. The upper soil layers over the twin tunnels are organic, backfill and soft to firm leam clay [24]. The tunnel on the left  is  excavated  first  and  then  followed  by  the tunnel on the right. Parameters of the soil layers are determined as shown in Table 1.

## 3.2. Establish the Numerical Model

The analyses were performed using the Abaqus software version 6.12-3. While the Mohr-Coulomb failure criterion is applied for the soil, the concrete lining is assumed to be elastic.

The case of twin tunnels with 6.3 m diameter, 15.0 m center-to-center spacing (L=15.0 m), and the tunnel  crown  depth  of  C=20.0  m  is  adopted.  A length of 50 m twin tunnels excavation stages was considered in this study. The 3D model was set up with dimensions of 120 m length and 100 m width in the X and Z-direction, respectively, and a height of 100 m in the Y-direction, as shown in Fig.4. The upper model boundary (y = 0.0 m) was set to be free, whereas the vertical and horizontal displacements at the bottom boundary (y = -100.0 m) were fixed.

Fig.4 Boundary conditions of the 3D model

<!-- image -->

Engineering drawing

The tunnel  lining  consists  of  concrete  cast-inplace  rings  characterized  by  a  length  (1.5  m), 300mm thick (Fig.5). The properties of concrete are unit weight (25 kN/m 3 ), Young's Modulus (25 GPa), and Poissons' ratio (0.2).

Table 1  Soil's parameters [24]

| Soil layer   |   Thickness, H (m) |   Density, ρ (k g/m 3 ) | Young's modulus, E (MPa)   |   Poisson's ratio, υ |   Friction angle, φ (0) | Cohesion, c (kPa)   |   Horizontal pressure coefficient, K 0 |
|--------------|--------------------|-------------------------|----------------------------|----------------------|-------------------------|---------------------|----------------------------------------|
| Backfill     |                6.5 |                    1900 | -                          |                  0.3 |                      32 | -                   |                                   0.47 |
| GU3&4        |                5.5 |                    2000 | 8                          |                  0.3 |                      20 | 5                   |                                   0.66 |
| GU1_s1       |                2.5 |                    1850 | 12                         |                  0.3 |                      25 | 10                  |                                   0.58 |
| GU1_s2       |                2.5 |                    1900 | 50                         |                  0.3 |                      25 | 25                  |                                   0.58 |
| GU5a         |               10.5 |                    2000 | 55                         |                  0.3 |                      34 | 25                  |                                   0.44 |
| GU7&8        |               72.5 |                    2100 | 75                         |                 0.25 |                      38 | 25                  |                                   0.36 |

Note: Layer GU3&amp;4 - Organic fat and elastic clays; GU1\_s1 - soft to firm lean clay; GU1\_s2 - Stiffer clay; GU5a - Sand or silty sand; GU7&amp;8 - Coarse sand or gravel [24].

Fig.5 Segment lining twin tunnels

<!-- image -->

Engineering drawing

Fig.6 Segment lining twin tunnels 3D discretized block with soil layers and twin tunnels

<!-- image -->

Engineering drawing

The excavation of the twin tunnels was simulated in  a  step-by-step  procedure. In  the  first step,  boundary conditions and gravity stresses are applied,  and  the  model  is  launched  to  reach  the initial state. In the second step, the tunnel on the left is  excavated  by  deactivating  the  zone  elements inside the tunnel periphery. The concrete lining is then installed on the tunnel boundary. The model is launched to reach a new equilibrium state. After that, the  same  procedure  of  excavating  the  soil  and installing  the  concrete  lining  is  applied  for  the tunnel on the right before reaching the final equilibrium state (Fig. 6).

## 3.3. Results and Discussions

Figs.7  and  8,  respectively,  show  the  vertical displacements after the excavation of the tunnel on the left and the tunnel on the right.

The  maximum  ground  surface  settlement  of 8.25 mm is observed after the excavation of the left tunnel.  The  position  of  maximum  ground  surface settlement is located over the center-line of the left tunnel. The shape of the transverse ground surface settlement  trough  is  in  good  agreement  with  the Gaussian curve.

Fig.7 Vertical displacements after the left tunnel excavation

<!-- image -->

Engineering drawing

Fig.8 Vertical displacements after the right tunnel excavation

<!-- image -->

Engineering drawing

Fig.9 shows  the ground surface settlement trough  induced  by  the  excavation  of  the  first  left tunnel and then the second right tunnel.

Fig.9 Surface settlement trough due to the construction of the left tunnel (1) and twin tunnels (2)

<!-- image -->

Line chart

After the right tunnel excavation, the maximum ground surface settlement of 12.38 mm is reached. The position of maximum ground surface settlement is eccentrically displaced 7.5 m from the center-line of the left tunnel and towards the right tunnel. Fig.10 presents the longitudinal settlement on the ground surface determined after the excavation of the left tunnel and the right tunnel.

Fig.10 Longitudinal settlement trough on the ground surface due to the construction of the left tunnel (1) and twin tunnels (2)

<!-- image -->

Line chart

A length of 50.0 m twin tunnels excavation was considered in this study. As shown in Fig.10, after the left tunnel excavation, the magnitude of ground surface settlement at the tunnel face section is 4.18 mm.  It  is  approximate  50.67  %  compared  to  the maximum  ground  surface  settlement  (8.25  mm). After the right tunnel excavation, the magnitude of ground surface settlement directly above the right tunnel face is 6.26 mm, coinciding with 50.56 % of the  value  of  maximum  ground  surface  settlement (12.38 mm).

The surface settlement will appear in front of the tunnel  face  at  a  distance  of  3-5  times  the  tunnel diameter. The surface settlement reached the maximum value at a distance, behind the tunnel face, of 5-7 times the tunnel diameter.

Fig.11 shows the lateral movements determined at the distance: x = L/2 = 15/2 = 7 m measured from the left tunnel axis (where L is the centre-to-centre spacing, L =15 m).  After the left tunnel excavation, the  maximum  ground  horizontal  movements  of 15.98 mm are seen (Fig.11). After the right tunnel excavation, it equals 4.52 mm.

The changes of center-to-center spacing between tunnels have a significant influence on the ground  surface  settlement.  The  surface  settlement caused by the construction of twin tunnels at centreto-centre  spacings  of  2.5D  (L=15.75  m),  3.0D (L=18.9 m), 3.5D (L=22.05 m), 4.0D (L=25.2 m), 4.5D  (L=28.35  m)  are  shown  in  Fig.12.  The magnitude of the maximum ground surface settlement was found to be 12.2 mm, 10.37 mm, 9.1 mm, 8.47 mm, 8.16 mm, respectively (Fig. 12).

Fig.11 Horizontal movements along the vertical line between two tunnel axes due to the construction of left tunnel (1) and twin tunnels (2)

<!-- image -->

Line chart

Fig.12 Maximum ground surface settlement trough due to the construction of twin tunnels in other cases 2.5D,  3.0D,  3.5D,  4.0D,  and  4.5D  m  center-tocenter spacing

<!-- image -->

Line chart

The results are in agreement with the results of Addenbrooke &amp; Potts [13], Divall et al. [15]  in both terms  of  the  transverse  surface  settlement  trough and the position of maximum settlement.

At  the  small  center-to-center  spacing  of  2.5D (L=15.75  m)  and  3.0D  (18.9  m),  the  position  of maximum settlement is located at the axis between two tunnels when  the center-to-center spacing increases, i.e., 3.5D (L=22.05 m), 4.0D (L=25.2 m) and 4.5D (L=28.35 m), the maximum settlement is observed on the left and right tunnels' axis.

## 4. CONCLUSION

Based on the case study of Hanoi Metro line 03, ground surface settlement due to the construction of Hanoi metro line 03 was presented and analyzed. From the numerical analysis, the following conclusions could be drawn:

After the twin tunnels excavation, the magnitude  of  ground  surface  settlement  directly above the face of the tunnel equals 50.56 % of the maximum ground surface settlement.

Surface settlement began to appear in front of the face of the tunnel and at a distance of 3-5 times the diameter of the tunnel. The location where the maximum surface settlement is  reached  is  behind the  tunnel  face  and  a  distance  of  5-7  times  the diameter of the tunnel.

The  center-to-center spacing  of the tunnels affects  both  the  magnitude  and  the  shape  of  the transverse  ground  surface  settlement  trough.  The maximum  ground  surface  settlement  due  to  the construction of twin tunnels reduces when increasing the center-to-center spacing.

## 5. ACKNOWLEDGMENTS

The  authors  would  like  to  thank  the  Hanoi Metropolitan Railway Management Board (MRB) for  providing  us  with  the  project  data  for  the analysis. This paper was supported by the Vietnam Ministry of Education and Training.

## 6. REFERENCES

- [1] Hunt D.V. L., Predicting the ground movements above twin tunnels constructed in London  Clay.  Ph.D.  Thesis  -  University  of Birmingham. Birmingham, UK, 2005.
- [2] Jim  S.  S.,  Mathew  S.,  Estimation  of  tunneling induced ground settlement using pressure relaxation method. International Journal of Geomate. Vol. 13, Issue 39, 2017,  pp. 132-139.
- [3] Chee M. K., Thanath G., Nurfatin A. A. R. and Hisham, M., Volume loss caused by tunneling in Kenny hill formation. International Journal of Geomate. Vol. 16, Issue 54, 2019,  pp. 164169.
- [4] Terzaghi  K.,  Shield  tunnels  of  the  Chicago subway. Journal of the Boston Society of Civil Engineers, Vol. 29, No.3, 1942, pp. 163-210.
- [5] Peck R. B., Deep excavations and tunneling in soft ground. In: Proceedings of the 7th International  Conference  on  Soil  Mechanics and Foundation Engineering, Mexico, Vol. 3, 1969, pp. 225-290.
- [6] Moretto  O.,  Discussion  on  Deep  excavations and tunneling in soft ground. Proc. 7th Int. Conf. on Soil Mechanics and Foundation Engineering, Mexico City, Vol. 3, 1969, pp. 311-315.
- [7] Cording E. J., Hansmire W. H., Displacement around soft tunnels. In: Proceedings of the 5th Pan American Conference on Soil Mechanics and Foundation Engineering, Session 4, 1975, pp. 571-633.
- [8] Islam  M.  S.,  Iskander  M.,  Twin  tunneling induced ground settlements: A review. Tunneling and Underground Space Technology, Vol. 110, (103614), 2021.
- [9] Attewell  P.  B.,  Yeates  J.,  Selby  A.  R.,  Soil Movements  Induced  by  Tunnelling  and  their Effects on Pipelines and Structures, Glasgow, Blackie, 1986.
- [10] New B. M., O'ReilIy M. P., Tunnelling induced ground movements: Predicting their magnitude and  effects.  Proc.  4th  Int.  Conf.  on  Ground Movements and Structures, Cardiff, 1991, pp. 671-697.
- [11] Hieu N.T., Giao P.H., Phien-wej N., Tunneling induced  ground  settlements  in  the  first  metro line  of  Ho  Chi  Minh  City,  Vietnam.  In:  Duc Long P., Dung N. (eds) Geotechnics for Sustainable Infrastructure Development. Lecture  Notes  in  Civil  Engineering,  Vol.  62. Springer, Singapore, 2020.
- [12] Addenbrooke  T.  I., Numerical  analysis of tunneling  in  stiff  clay.  Ph.D.  thesis,  Imperial College of Science Technology and Medicine. London, UK, 1996.
- [13] Addenbrooke T. I., Potts, D. M., Twin tunnel interaction  -  surface  and  subsurface  effects. International Journal of Geomechanics, Vol. 1,

No.2, 2001, pp. 249-271.

- [14] Chapman  D.  N.,  Ahn,  S.  K.,  Hunt  D.V.  L., Investigating ground movements caused by the construction  of  multiple  tunnels  in  the  soft ground using laboratory model tests. Canadian Geotechnical Journal, Vol. 44, No.6, 2007, pp. 631-643.
- [15] Divall S., Goodey R. J., Taylor R. N., Ground movements  generated  by sequential  Twintunnelling in over-consolidated clay. In: Proceedings  of  Eurofuge  Conference,  Delft, The Netherlands, 2012.
- [16] Le B. T., Nguyen N. T., Divall S., Goodey R., Taylor, R. N., Modified gap method for prediction of TBM  tunneling-induced soil settlement  in  the  sand  -  a  case  study.  In: Proceedings of the Tenth International Symposium on Geotechnical Aspects of Underground  Construction  in  Soft  Ground, 2021, pp. 584-589.
- [17] Dibavar B. H., Ahmadi M. H., Davarpanah S. M.,  3D  Numerical  Investigation  of  Ground Settlements Induced by Construction of Istanbul  Twin  Metro  Tunnels  with  Special Focus on Tunnel Spacing, Periodica Polytechnica Civil Engineering, Vol. 63, No.4, 2019, pp. 1225-1234.
- [18] Hanya T., Ground movements due to construction of the shield-driven tunnel. Proc. 9th Int. Conf. Soil. Mech. and Found. Engng., Tokyo, 1997, pp. 759-90.
- [19] Akins  K.  P.,  Abramson  L.  W.,    Tunnelling  in residual soil and rock. Proc. Rapid. Excavn. and Tunnelling. Conf., Chicago, Vol.1, 1983, pp. 3-24.
- [20] Ottaviano M., Pelli F., Influence of depth and distance between the axes on surface displacements  due  to  the  excavation  of  twin shallow  tunnels.  Proc.  Int.  Symp.  on  Engng. Geol.  and  Underground  Construction.  Lisboa Portugal, Vol. 1, 1983, pp. 247-256.
- [21] Kim  S.  H.,  Burd  H.  J.,  Milligan  G.  W.  E., Interaction  between  closely  spaced  tunnels  in clay.  Proc.  Int.  Symposium  on  Geotechnical Aspects of Underground Construction in Soft Ground  (eds.  R.  J.  Mair  and  R.  N.  Taylor),

London, UK, 1996, pp. 543-548.

- [22] Systra S. A., Technical design statement, input data/volume I. Package: Underground section - Line and Stations, package number: hplmlp/cp03.  Project:  Hanoi  pilot  light  metro  line  03. Hanoi metropolitan railway management board. Hanoi, Vietnam, 2012.
- [23] Systra S. A., Technical design statement design/volume II. Package: underground section  -  Line  and  Stations  package  number: hplmlp/cp-03. Project: Hanoi pilot light metro line 03. Hanoi metropolitan railway management board. Hanoi, Vietnam, 2012.
- [24] Systra S. A., Geotechnical interpretative report underground  section.  Package:  underground section - Line and Stations, package number: hplmlp/cp-03. Design report technical design, Project: Hanoi pilot light metro line 03. Hanoi metropolitan railway management board. Hanoi, Vietnam, 2012.
- [25] Qian F., Qimin T., Dingli Z., Louis N., Y.W., Ground surface settlements due to construction of  closely-spaced  twin  tunnels  with  different geometric arrangements. Tunneling and Underground Space Technology, Vol. 51, 2016, pp. 144-151.
- [26] Behnaz H.D., Mohammad H.A., Seyed M.D., 3D Numerical Investigation of Ground Settlements Induced by Construction of Istanbul  Twin  Metro  Tunnels  with  Special Focus on Tunnel Spacing. Periodica Polytechnica Civil Engineering, Vol. 63, Issue 4, 2019, pp. 1225-1234.
- [27] Ads A., Islam S., Iskander M., Effect of Face Losses and Cover-to-Diameter Ratio on Tunneling  Induced  Settlements  in  Soft  Clay, Using Transparent Soil Models. Geotechnical and Geological Engineering, Vol. 39, 2021, pp. 5529-5547.

Copyright © Int. J. of GEOMATE All rights reserved, including making copies unless permission is obtained from the copyright proprietors.
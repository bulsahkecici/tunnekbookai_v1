Original scientific paper

## SENSITIVITY ANALYSIS OF ROCK MASS PARAMETERS ESTIMATE INFLUENCE ON DECLINE SUPPORT DESIGN USING NATM

## Slavko Torbica 1 , Veljko Lapčević 1 , Wang Gang 2 , Nemanja Đokić 1 , Miodrag Duranović 1

Received:

May 18, 2019

## Abstract:

Capital mine development is often faced with limited geotechnical databases and designers are faced with more or less accurate estimates of missing parameters. GSI classification if often used with numerical modelling and its rounding unit is ±5 as suggested by its creators. In situ stresses are usually estimated in such manner that vertical component is equal to the weight of the rocks above, while horizontal components may vary in wide range, starting with ratio to vertical component of 0.3 and even be several times higher than vertical component.

Influence of estimate error of GSI and horizontal stress is analyzed for the Cukaru Peki location near Bor in Serbia. Zone in the rock mass valued with GSI of 40 at depth 160m is analyzed for the change of GSI value of ±5 and horizontal stress ratio between 0.5-1.5. Change of the unsupported length of decline and shotcrete layer thickness is tracked for different values of input parameters. Finally, best case and worst case scenarios are analyzed with results showing that shotcrete layer thickness could vary in range between 4-33cm, and unsupported lengths between 0.6-2m.

Keywords: Rock mass; Tunneling; NATM; GSI; Stress; Cukaru Peki; Bor;

## 1 INTRODUCTION

Design  of  the  underground  openings  requires  that  crucial  data  about  rock  mass conditions should be determined, such as its strength, deformability and stress conditions that are present. Strength and deformability of the rock masses are commonly determined by classification systems such as Q (Barton et al., 1974), RMR (Bienawski, 1993) or GSI (Hoek, 1994). GSI is commonly used due to its applicability in numerical codes and possibility to determine it by limited database. However, this implies possible errors in determination and consequences that may occur.

1  University of Belgrade - Faculty of Mining and Geology

2 Rakita Exploration d.o.o. Bor, Suvaja Street 185A, 19210 Bor, Serbia Emails:torbica@rgf.bg.ac.rs;veljko.lapcevic@rgf.bg.ac.rs;wang.gang@rakita.net; nemanja.djokic@rgf.rs; miodrag.duranovic@rgf.rs;

Accepted:

June 21, 2019

Stress filed is also one of crucial parameters that influence the stability and design of support for underground openings. Vertical stress component is generally equal to the weight of the above lying rock masses, while horizontal stress components are usually expressed as fraction of the vertical component. Terzaghi and Richart (1952) suggested

method to  determine  horizontal  stress  ratio  by  relation 1  - which  estimates  it  to

around 50% of the vertical stress intensity. Numerous works (Zhang et al., 2012; Torbica and Lapčević, 2016) point out that horizontal stresses may be several times higher than those estimate using only Terzaghi's approach and that previous method is insuficient.

Herein,  sensitivity  analysis  for  the  Cukaru  Peki  near  Bor,  Serbia  site  is  analyzed  by variation  of  the  possible  GSI  and  stress  ratio  values.  Intention  is  to  emphasize  the influence that misjudgment of these parameters can have on advancement of excavation and support design.

## 2 METHODOLOGY

Decline is meant to be excavated down to the depth of almost 600m and along its trajectory passes through several weak zones. One of such weak zones is expected to be passed at the depth of the 160m.  This zone is estimated to be around 120m long and passes through the jointed and weak sandstone layer. Rock mass properties of this zone are shown in Table 1.

Table 1 Initially estimated rock mass properties in the analyzed zone

| Parameter            | Estimated value   |
|----------------------|-------------------|
| Compressive strength | 50 MPa            |
| Young's modulus      | 28 GPa            |
| Poisson's ratio      | 0.3               |
| GSI                  | 37                |

Decline cross section is given in Figure 1 and total cross sectional area is around 25m 2 .

Figure 1 Decline cross section

<!-- image -->

Engineering drawing

Estimated GSI value of 37 (as given by geologist who logged the exploratory cores) is always just estimate and engineers should be aware of possible error of this estimate. Analysis herein is performed for 3 different GSI values of 35, 40 and 45 since these are estimated to be possible margins of error that is easy to made.

Initial  stress  condition  are  not  know  and  therefore  are  estimated  in  such  way  that gravitational component is equal to the weight of above laying rock mass. Horizontal components are changed between 0.5-1.5*gravitational component in order to assess the model sensitivity to the actual stress state in to emphasize its importance. Orientation of the  horizontal  stresses  is  such  that  one  component  is  perpendicular  to  the  decline trajectory meaning that second component is aligned with decline trajectory.

As summary, GSI and stress value estimate error is tested for the impact on support and advancement step of decline development.

Analysis is based on the parameters given in Table 2 and Table 3.

Table 2 Rock mass parameters used in analyses

| Parameters      | GSI     | GSI    | GSI    |
|-----------------|---------|--------|--------|
|                 | 35      | 40     | 45     |
| σ ci (MPa)      | 50      | 50     | 50     |
| E i (MPa)       | 28 000  | 28 000 | 28 000 |
| E m (MPa)       | 3175    | 4470   | 6260   |
| Poisson's ratio | 0.3     | 0.3    | 0.3    |
| m i             | 19      | 19     | 19     |
| m b             | 1.865   | 2.229  | 2.665  |
| s               | 0.00073 | 0.001  | 0.002  |

Table 3 Stress data used in analysis

| Stress components   | k     |    k | k     |
|---------------------|-------|------|-------|
| Stress components   | 0.5   |    1 | 1.5   |
| σ 1 (MPa)           | 4.32* | 4.32 | 6.48  |
| σ 2 (MPa)           | 2.16  | 4.32 | 6.48  |
| σ 3 (MPa)           | 2.16  | 4.32 | 4.32* |

*vertical

## 2.1 FEM model

Methodology  used  herein  is  based  on  the  research  proposed  by  Vlachopoulos  and Diederichs (2009) that made it possible to estimate 3D progression of the underground opening with utilization of 2D FEM models. This method was originally developed for the circular shaper of the tunnels/drifts, however it has been shown to be applicable for other  shapes  of  the  underground  openings.  Main  advantage  of  this  method  is  that  is eliminates complex 3D numerical modeling and reducing time necessary for analysis while providing results reliable enough.

FEM model is created using Phase2 software by Rocscience (2019) and has 20 stages. At the internal boundary of excavation distributed load is applied (Figure 2), where in the first stage this load is equal to the field stress and at every stage it is being decreased for 5% of initial load. In final stage complete distributed load is removed and plain stress strain state is simulated. In this manner progressive excavation is simulated.

Figure 2 Distributed load at excavation boundary

<!-- image -->

Engineering drawing

After model convergence it is necessary to determine radius of plasticization around the underground opening (Figure 3) as well as deformation diagram for point with largest total displacement (Figure 4).

Figure 3 Plastic radius and total displacement in final stage of the model

<!-- image -->

Engineering drawing

Main principle is to determine longest unsupported length of the decline, or, put in other words, distance between supported part of decline and its face. Therefore, in FEM model we are determining the stage before failure of the rock mass occurs as it is illustrated in Figure 4. It is important to mark down the total displacement value in this stage since it is necessary for the next step of the procedure.

Figure 4 Deformation diagram for the point with largest total displacement

<!-- image -->

Line chart

By knowing the ratio between the total displacement in the stage before the failure of the rock  mass  occurs  and  the  maximum  displacement  (Closure  to  maximum  closure  as illustrated in Figure 5) we are using the diagram created by Vlachopoulos and Diederichs (2009) to determine the unsupported length of decline.

Diagram curves (Figure 5) represent the ratio between plastic zone radius and decline radius. For example if we determine following values:

Closure / maximum closure = 0.8

Plastic zone radius / decline radius = 1.5

Then we read from the diagram:

Distance from decline face / decline radius = 1.3 Finally, unsupported length of the decline is:

Distance from decline face = 1.3* decline radius This procedure is repeated for each case.

Figure 5 Diagram by Vlachopoulos and Diederichs (2009)

<!-- image -->

Line chart

Determining the unsupported length of decline is first part of the analysis, second one is to  determine  necessary  support  for  the  decline.  For  simplicity,  only  thickness  of  the shotcrete layer is determined for the required FOS=1.4.

Support design procedure assumes that shotcrete layer is installed in the stage of FEM model before the failure of the rock mass, stage that has been determine in previous analysis. In each case same properties of shotcrete layer are used as shown in Table 4.

Table 4 Shotcrete properties used for the analysis

| Parameter            |           |
|----------------------|-----------|
| Young's modulus      | 30000 MPa |
| Poisson ratio        | 0.15      |
| Compressive strength | 30 MPa    |
| Tensile strength     | 3 MPa     |

## 3 RESULTS

## 3.1 GSI error influence

As it was originally suggested by the Hoek (2007) GSI value should be rounded by increments of 5, meaning that value of GSI=37 that was initially estimated should be 35 or 40. Herein, it is assumed that initial GSI value is 40 and with consideration of the possible estimate error it can spread in span between 35-45. Therefore, there GSI=35, 40 and 45 values are analyzed.

Change of the GSI influences change of the rock mass strength properties for the HoekBrown's  failure  criteria  and  deformation  modulus  (estimated  by  Hoek  and  Diedrich (2006)). Change of these parameters influences support loading as well as size of the plastic zone around underground opening.

All the stress components are equal ( 4.32 v H h MPa    = = = ). Intensity corresponds  to  the  intensity  of  the  gravitational  component  for  the  depth  of  160m assuming that average unit weight is 0.027MN/m 3 .

Analysis results are presented in Figure 6, Figure 7 and Table 5. It is seen that decreasing GSI value determines lower unsupported lengths ranging from 1.4m to 0.6m. Roughly talking  unsupported  length  of  the  decline  is  around  1m  and  it  determines  the advancements and excavation organization. If we compare extreme values, it implies that advance of 1.4m is more than doubled compared with 0.6m, meaning that twice as much time and costs are necessary to develop decline in worse conditions.

Table 5 Analysis results

|                                              |    GSI |    GSI |    GSI |
|----------------------------------------------|--------|--------|--------|
| Parameters                                   |     45 |     40 |     35 |
| Tunnel radius, Rt (m)                        |    2.8 |    2.8 |    2.8 |
| Plastic zone radius, Rp (m)                  |   3.25 |    3.8 |    3.8 |
| Rp / Rt                                      |   1.16 |   1.36 |   1.36 |
| Maximum closure, u max (m)                   | 0.0030 | 0.0064 | 0.0110 |
| Closure in support installation stage, u (m) | 0.0018 | 0.0034 | 0.0047 |
| u / u max                                    |   0.60 |   0.53 |   0.43 |
| Distance from face / tunnel radius           |    0.5 |    0.4 |    0.2 |
| Distance from face                           |    1.4 |    1.1 |    0.6 |

Figure 6 Unsupported length vs GSI change

<!-- image -->

Line chart

Figure 7 illustrates change of the necessary shotcrete thickness for different GSI values. It  is  seen  that  for  the  lowest  GSI  value  of  35  shotcrete  layer  with  the  FOS=1.4  has thickness  of  9cm,  while  in  the  case  of  GSI=45  shotcrete  layer  with  same  FOS  has thickness of 4cm. It is clear that amount of support that is necessary in these cases is enormous. Considering differences in advancements that could be achieved it is obvious that costs may be significantly different.

Figure 7 Shotcrete thickness vs GSI change

<!-- image -->

Bar chart

## 3.2 Horizontal stress influence

Common approach in geomechanical analyses is that horizontal stress is expressed as portion of the gravitational stress component. Horizontal component often estimated by the expression 1  - which estimates horizontal stress between 30-50% of the vertical component depending on actual Poisson's ratio value. However, horizontal stress ratio is know to be higher than this (1-1.5) especially at shallow depths. Zhang et al. (2012) provided useful estimate for the different rock types.

Analysis herein is done for 3 different stress ratios (0.5, 1 and 1.5) with equal minor and major horizontal components. Rock mass parameters are taken for the average GSI value of 40. Results are given in Table 6, Figure 8 and Figure 9.

Table 6 Analysis results

|                                              |      k |      k |      k |
|----------------------------------------------|--------|--------|--------|
| Parameters                                   |    0.5 |      1 |    1.5 |
| Tunnel radius, Rt (m)                        |    2.8 |    2.8 |    2.8 |
| Plastic zone radius, Rp (m)                  |    3.9 |    3.8 |   4.13 |
| Rp / Rt                                      |   1.39 |   1.36 |   1.47 |
| Maximum closure, u max (m)                   | 0.0053 | 0.0064 |  0.010 |
| Closure in support installation stage, u (m) | 0.0034 | 0.0034 | 0.0046 |
| u / u max                                    |   0.64 |   0.53 |   0.46 |
| Distance from face / tunnel radius           |    0.7 |    0.4 |    0.3 |
| Distance from face                           |      2 |    1.1 |    0.8 |

As it  is  seen,  unsupported  length  of  decline  decreases  with  the  increasing  horizontal stresses as it could have been expected. In case when horizontal stress is 50% of the vertical component is possible to achieve advance of 2m before support installation and roof collapse. Unsupported length drops significantly for ratios 1 and 1.5 and is around 1m.

Figure 8 Unsupported length vs stress ratio

<!-- image -->

Line chart

For  the  previously  determined  unsupported  lengths  shotcrete  thickness  is  determined using explained methodology. In the case of highest thickness of the shotcrete layer with the FOS=1.4 is 15 cm while for the case where stress ratio is 1 shotcrete layer is 7cm thick. This illustrates the stress influence on the needed support.

For the case where stress ratio=0.5 shotcrete layer is 10cm thick. This comes from the fact that in this case unsupported length of the underground opening is almost 2 times higher than in previously discussed cases.

Figure 9 Shotcrete thickness vs stress ratio

<!-- image -->

Bar chart

## 3.2 Best- and worst-case scenarios

As it was shown in previous sections, possible estimate errors in stress and GSI values may have high impact on excavation advancing and required support. Intention is to illustrate  range  of  possible  outcomes  and  to  point  out  what  dangers  are  lying  under deterministic  selection  of  analysis  parameters  without  testing  the  sensitivity  of  their influence.

In best-case scenario it is like to assume that rock mass is stronger than estimated and that stresses are low. Therefore, in our case this would mean that rock mass has GSI of 45 and that horizontal stress ratio is 0.5.

For  the  worst-case  scenario  we  would  like  to  assume  that  rock  mass  is  weaker  than initially estimated and that stress ratio is higher. In our case this would mean that GSI value is 35 while horizontal stress ratio is 1.5.

Results presented in Table 7, Figure 10 and Figure 11 show that two cases may differ significantly.  If  most  favorable  conditions  are experienced  unsupported length of the underground opening can be around 2m and shotcrete layer with FOS=1.4 has thickness of 4cm.

On the other side, if lower strength and higher stress are to be present unsupported length of the underground opening is significantly reduced to 0.6m. Shotcrete layer thickness is dramatically increased to 33cm in order to maintain desired FOS.

Table 7 Analysis results

| Parameters                                   |   Worst |   Best |
|----------------------------------------------|---------|--------|
| Tunnel radius, Rt (m)                        |     2.8 |    2.8 |
| Plastic zone radius, Rp (m)                  |     4.7 |   3.75 |
| Rp / Rt                                      |    1.68 |   1.34 |
| Maximum closure, u max (m)                   |   0.015 | 0.0027 |
| Closure in support installation stage, u (m) |  0.0062 | 0.0018 |
| u / u max                                    |    0.41 |   0.67 |
| Distance from face / tunnel radius           |     0.2 |    0.7 |
| Distance from face                           |     0.6 |      2 |

Figure 10 Unsupported length vs stress ratio

<!-- image -->

Bar chart

Figure 11 Shotcrete thickness fro best- and worst-case

<!-- image -->

Bar chart

## 4 CONCLUSION

Analysis  herein  was  undertaken  in  order  to  emphasize  the  importance  of  sensitivity analysis  of  crucial  parameters  for  design  of  the  underground  openings.  Geological strength index is commonly estimated in increments of 5 and therefore its estimation is highly subjective. Range of GSI values ± 5 of the estimated value is possible error that could be made. It is not unusual that horizontal stress components are not treated with care they require, especially in mining applications.

Results show that GSI change influences both unsupported length of decline as well as thickness of the shotcrete layer. With increasing GSI value from 35 to 45 unsupported length increases from 0.6m to 1.4m, while required shotcrete layer thickness ranges from 4cm to 9cm (FOS=1.4) for corresponding lengths. Major reason for these changes comes from the estimate of the deformation modulus of the rock mass that is directly related to GSI.

Stress  change  was  analyzed  by  changing  the  ratio  between  horizontal  and  vertical components from 0.5 to 1.5, while rock mass strength and deformability parameters were kept constant (GSI=40). Unsupported length goes from 2m in case of the ratio of 0.5 to 0.8m in case when stress ratio is 1.5. For case with ratio of 0.5 shotcrete layer thickness is 10cm (FOS=1.4) while in the case of ratio of 1.5 thickness is 15cm. In case where stress ratio is 1 shotcrete layer is 7cm thick, but this comes from the fact that unsupported length is 1.1m and should not be misinterpreted if compared with the case with lowest stress ratio.

In best case where strength of the rock mass is the highest and the stresses are lowest it is shown that unsupported length is around 2m and necessary shotcrete thickness is 4cm. on the other side, in worst possible case unsupported length is 0.6m with shotcrete layer of 33cm.

By comparing best and worst possible cases it is clear that possible estimated errors could lead  in  serious  misjudgments  about  necessary  support  and  advancing  of  excavation. Other implications may include delays and work safety issues, as well as planning of required materials.

## Acknowledgement

Authors  would  like  to  acknowledge  RAKITA  d.o.o.  for  approval  and  availability  of geotechnical database for Cukaru Peki location near Bor.

## REFERENCES

BARTON, N. et al. (1974) Engineering classification of rock masses for the design of tunnel support. Rock mechanics , 6(4), pp.189-236.

BIENIAWSKI, Z.T. (1993) Classification of  rock  masses  for  engineering:  the  RMR system  and  future  trends.  In: Rock  Testing  and  Site  Characterization ,  Pergamon, pp. 553- 573.

HEIDBACH O.  et  al.  (2008)  The  2008  release  of  the  World  Stress  Map.  [Online] Available from: http://www.world-stress-map.org. [Accessed 5/5/2019]

HOEK, E. (1994) Strength of rock and rock masses. ISRM News Journal , pp. 4-16.

HOEK, E. (2007) Practical Rock Engineering . Rocscience Inc.

HOEK, E and DIEDERICHS, M. (2006) Empirical estimates of rock mass modulus. International Journal of Rock Mechanics and Mining Sciences , 43, pp. 203-215

ROCSCIENCE  INC.  (2019)  Phase2  Version  9.0  -  Finite  Element  Analysis  for Excavations and Slopes. Toronto, Ontario, Canada.

TERAGHI,  K.  and  RICHART,  F.E.  (1952)  Stresses  in  Rock  About  Cavities. Géotechnique , 3 (2), pp. 57-90.

TORBICA, S. and LAPČEVIĆ, V. (2016) Model for estimation of stress field in the Earth's crust. Podzemni Radovi , (28), pp. 9-17.

VLACHOPOULOS,  N.  and  DIEDERICHS,  M.S.  (2009)  Improved  Longitudinal Displacement Profiles for Convergence Confinement Analysis of Deep Tunnels. Rock Mechanics and Rock Engineering , 42(2), pp. 131-146.

ZANG, A. et al. (2012) World stress map database as a resource for rock mechanics and rock engineering. Geotechnical and Geological Engineering , 30(3), pp.625-646.
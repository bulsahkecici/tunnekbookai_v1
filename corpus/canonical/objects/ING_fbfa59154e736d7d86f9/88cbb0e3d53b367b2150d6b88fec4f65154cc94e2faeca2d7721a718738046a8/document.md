<!-- image -->

Stamp

## UNIVERSITÀ DEGLI STUDI DI NAPOLI FEDERICO II

Dottorato di Ricerca in INGEGNERIA GEOTECNICA XXIII CICLO Coordinatore Prof. Claudio Mancuso

## Barbara Bitetti

## EFFECTS OF TUNNELLING IN URBAN AREAS

RELATORE Prof. Alessandro Mandolini

## ACKNOWLEDGEMENTS

The result of an experimental work like this Thesis, is not strictly related only to the person who is in charge of presenting it officially. All the merits, hence, have to be shared among various persons which have contributed, even if with different roles and in different ways. The first thank I have to express is in regards of my tutor, Prof. Alessandro Mandolini. Then I would like to thank the Dutch group, in particular, Prof. Frits Van Tol, Wout Broere and Ronald Brinkgreve for their infinite availability both in hosting me in a foreign country and in guiding me wisely within the complex world of numerical analysis. Apart from the academic world, I must thank all the persons and enterprises which allowed me to get my experimental data. In particular, a great 'thank' is in regards of Ing. Mario Carastro,  Geom.  Michele  Merlo  and  Ing.  Michele  Barbato  (Riviera  S.p.A.)  and  Ing.  Andrea Belfiore (Rocksoil S.p.A.).

## CONTENTS

## ACKNOWLEDGEMENTS INTRODUCTION

| INTRODUCTION                                     | INTRODUCTION                                         | INTRODUCTION                                         |   1 |
|--------------------------------------------------|------------------------------------------------------|------------------------------------------------------|-----|
| Chapter 1. BACKGROUND                            | Chapter 1. BACKGROUND                                | Chapter 1. BACKGROUND                                |   3 |
| 1.1.                                             | Introduction                                         | Introduction                                         |   3 |
| 1.2.                                             | Tunnelling-induced soil movements                    | Tunnelling-induced soil movements                    |   3 |
| 1.3.                                             | The prediction of ground movements due to tunnelling | The prediction of ground movements due to tunnelling |   5 |
| 1.3.1.                                           | Empirical methods                                    | Empirical methods                                    |   6 |
| 1.3.1.1.                                         | 1.3.1.1.                                             | Transverse behavior                                  |   6 |
| 1.3.1.2.                                         | 1.3.1.2.                                             | Longitudinal behavior                                |   9 |
| 1.3.1.3.                                         | 1.3.1.3.                                             | Volume loss                                          |  12 |
| 1.3.1.4.                                         | 1.3.1.4.                                             | Trough width parameter                               |  15 |
| 1.3.1.5.                                         | 1.3.1.5.                                             | Subsurface movements                                 |  17 |
| 1.3.2. Numerical analyses of tunnel construction | 1.3.2. Numerical analyses of tunnel construction     | 1.3.2. Numerical analyses of tunnel construction     |  21 |
| 1.3.2.1.                                         | 1.3.2.1.                                             | Two dimensional analyses                             |  22 |
| 1.3.2.2.                                         | 1.3.2.2.                                             | Three dimensional analyses                           |  26 |
| 1.4.                                             | Building damage assessment                           | Building damage assessment                           |  30 |
| 1.4.1.                                           | Definition of structure deformation parameters       | Definition of structure deformation parameters       |  31 |
| 1.4.2.                                           | Evaluation of risk of damage                         | Evaluation of risk of damage                         |  32 |
| 1.4.2.1.                                         | 1.4.2.1.                                             | Preliminary assessment                               |  33 |
| 1.4.2.2.                                         | 1.4.2.2.                                             | Second stage assessment                              |  33 |

12

15

17

21

22

26

30

31

32

33

33

| 1.4.2.3.                                       | Detailed evaluation                                                      |   34 |
|------------------------------------------------|--------------------------------------------------------------------------|------|
| 1.4.3.                                         | Category of damage                                                       |   35 |
| 1.4.4.                                         | Calculation of building strain                                           |   37 |
| Chapter                                        | 2. LINE 6: A 3 KM TUNNEL IN A DENSELY URBANIZED ENVIRONMENT              |   44 |
| 2.1.                                           | Introduction                                                             |   44 |
| 2.2.                                           | LINE 6: the design                                                       |   45 |
| 2.2.1.                                         | Ground conditions                                                        |   48 |
| 2.2.1.1.                                       | Site and laboratory investigations                                       |   50 |
| 2.2.2.                                         | The used excavation technique                                            |   57 |
| 2.2.3.                                         | The monitoring plan                                                      |   59 |
| 2.2.3.1.                                       | Installed monitoring instruments                                         |   63 |
| 2.3.                                           | The empirical methods for prediction of tunnelling induced displacements |   66 |
| Chapter 3. LINE 6: ANALYSIS OF MONITORING DATA | Chapter 3. LINE 6: ANALYSIS OF MONITORING DATA                           |   76 |
| 3.1.                                           | Introduction                                                             |   76 |
| 3.2.                                           | Tunnel excavation                                                        |   76 |
| 3.3.                                           | Field monitoring data                                                    |   81 |
| 3.3.1.                                         | Excavation machine performances                                          |   82 |
| 3.3.2.                                         | Landmarks on the ground surface                                          |   83 |
| 3.3.3.                                         | Landmarks on buildings                                                   |   97 |

97

| Chapter 4.   | Chapter 4.                                                   | THREE-DIMENSIONAL FINITE ELEMENT ANALYSIS                    |   111 |
|--------------|--------------------------------------------------------------|--------------------------------------------------------------|-------|
| 4.1.         | Introduction                                                 | Introduction                                                 |   111 |
| 4.2.         | Plaxis 3D Tunnel: useful informations for Line 6 application | Plaxis 3D Tunnel: useful informations for Line 6 application |   111 |
| 4.2.1.       | The Hardening Soil Model                                     | The Hardening Soil Model                                     |   113 |
| 4.3.         | Three-dimensional analyses of the Line 6 tunnel              | Three-dimensional analyses of the Line 6 tunnel              |   121 |
| 4.3.1.       | The input model                                              | The input model                                              |   121 |
| 4.3.2.       | The effects of soil parameters on surface subsidence         | The effects of soil parameters on surface subsidence         |   124 |
| 4.3.3.       | Parametric analyses on the EPB front and grouting pressures  | Parametric analyses on the EPB front and grouting pressures  |   130 |
| 4.3.4.       | Back-analysis of observed effects of Line 6 tunnelling       | Back-analysis of observed effects of Line 6 tunnelling       |   136 |

## APPENDIX

REFERENCES AND BIBLIOGRAPHY

## INTRODUCTION

The  always  increasing  demand  in  new  transportation  routes  in  urban  area,  in  the  last years, led to the need in increasing the present road transports; by then, the need to use the  underground  environment  for  new  transportation  lines  became  always  more important. New underground lines started to be excavated in many of the largest cities in the  world,  leading  to  a  large  number  of  shallow  and  deep  excavations  in  the  urban environment.

Many tunnels, often located at relatively shallow depth from the ground surface, started to be excavated, inducing not negligible effects on the preexisting buildings. For such a reason, methods directed to the induced tunnelling effects prediction were developed on the basis of empirical data collected all over the years. Despite such empirical methods resulted very useful and reliable for the designing process of a tunnel line, as to predict the  tunnel  induced  displacements  on  the  ground  surface,  they  base  on  very  simplified hypothesis, neglecting important phenomena such as the soil-tunnel-buildings interaction and  considering  in  a  simplified  way  the  excavation  technique  influence.  Indeed  data collected from literature, demonstrated how the improvements in technologies in the last years allowed an important reductions in induced displacements on the ground surface. For  a  such  a  reason  numerical  analysis  of  the  excavation  technique  influence  on tunnelling induced displacements, became always more significant.

Thus, the purpose of this research is to define the importance of excavations technologies, in terms of tunnelling induced effects on the ground surface, inspired by the current construction process of the Line 6 tunnel in Naples. For this purpose, a number of numerical analyses, by means Finite Element codes, were performed as to simulate the tunnel  excavation  process,  and  to  carry  on  a  parametric  study  on  the  technology influence on the induced effects, finally compared to results of a similar parametric study concerning the geotechnical properties of the soils affected by the excavation. Results of such analyses were then used to back-analyze monitoring data collected during the Line 6 tunnelling process.

## 1.1. Introduction

The construction of tunnels in soft ground inevitably leads to ground movements.

Since  most  of  the  excavation  processes  usually  take  place  in  extremely  densely urbanized environment, affecting existing surface or subsurface structures, the determination  of  their  magnitude  plays  an  important  role  in  designing  process  and  in defining the most useful technique to use.

This chapter summarizes methods to estimate tunnel induced ground movements and to assess the resultant damage on buildings.

## 1.2. Tunnelling-induced soil movements

The displacements field (Fig. 1-1) induced by the excavation of tunnel in soft ground, is strongly affected by many phenomena, such as:

-  Face deformations due to stress release, relevant in open-faced tunnels or in EPB or slurry shield excavations when the face pressure is not rightly controlled; they have been strongly reduced by the introduction of the Tunnel Boring Machine;
-  movements  induced  by  shield  in  advancing,  due  to  the  over-cutting,  useful  to reduce  friction  between  shield  and  ground:  they  strongly  depend  by  the  overcutting edge thickness and by any steering problems in maintaining the alignment of the shield;
-  ground  movements  in  between  the  lining  and  the  shield  tail,  reduced  by  using grout  injections  or,  in  case  of  expanded  lining  used,  by  expanding  the  lining  as soon as possible;

## Chapter 1. BACKGROUND

-  lining deflections due  to earth pressure, generally smaller than  the other movements components once the final lining is installed;
-  long term deformations due to consolidation process in clayey soils.

Fig. 1-1. Ground movements induced by tunnel excavations (after Attewell et al., 1986)

<!-- image -->

Engineering drawing

Time  dependency  in  the  mechanical  behavior  of  soil  influences  ground  movements resulting  from  tunnelling,  leading  to  the  classification  of  short,  medium  and  long-term movements.

Short-term movements usually occur at the most the first four days after the excavation in London clay; by reporting short-term settlements over a period of 24 hour before and after  the  passage  of  the  shield,  Macklin  and  Field  (1999)  showed  that  short-term displacements occur almost instantaneously with the advance of tunnel heading, leading to  a  constant  volume  response  of  the  ground  and  to  a  suddenly  new  stress  regime. Because of strains are usually less than 0.1% (a part from very locally to the tunnel), not enough to cause failure or alter the soil structure, the constitutive model for the soil does not change in this phase.

Medium and long-term settlements, caused by alteration of soil properties at constant load, due to such phenomena as creep, ageing and/or consolidation. The timescale over which they occur depends on ground conditions, varying from weeks or months for sand and soft clays, to years for stiff clays.

About the magnitude of short-term compared with long-term tunnel-induced displacements, case histories suggested that for typical site on stiff clay, around 60% of the total settlements occurs in the short term (Simons and Som, 1970; Morton and Au, 1975).

Attewell  and  Selby  (1989)  observed  long-term  settlements  up  to  2.5  times  the  short term, but also that the long-term trough width tended to be wider than the short-term; it implies  the  structures  are  more  able  to  accommodate  long-term  than  short-term settlements, which consequently are the chief issue of engineering problems related to tunnel-induced displacements.

## 1.3. The prediction of ground movements due to tunnelling

Many methods were implemented to quantify tunnelling induced ground movements: from the and analytical methods, to predict displacements in green-field conditions, going through more sophisticated numerical models (e.g. Finite Element Methods), up to the physical models, such as centrifuge tests, reproducing in small scale the in situ situation.

As  for  numerical  analyses  a  sufficiently  accurate  constitutive  model  for  the  soil  is required,  for  the  modelling  technique  (either  laboratory  or  numerical),  the  tunnelling process has to be represented with an acceptable degree of accuracy.

## 1.3.1. Empirical methods

## 1.3.1.1. Transverse behavior

The  current  and  widely  used  empirical  design  methods  for  predicting  ground  surface settlements in response to tunnelling operations, can be dated back to Peck &amp; Schmid (1960); afterwards, Peck 1 (1969) introduced the Normal Gaussian Distribution (Fig. 1-2) as the curve  matching  at  the  most  the  field  data  representing  the  tunnel  induced settlements  on  ground  surface  in  green-field  conditions.  Since  then,  its  mathematical formulation  expressed  by  (1.1)  has  been  accepted  as  it  allows  a  quite  straightaway calculation of vertical displacements in transverse direction; it is given by:

<!-- formula-not-decoded -->

where:

-  Sv,max is the maximum settlement above the tunnel axis;
-  ix is the distance between the inflection point of the curve, where the trough has its  maximum slope,  and  the  central  axis  of  the  tunnel;  it  separates  the sagging from the hogging zone of the curve
-  Sv(x) is the settlement at distance x from the tunnel axis.

1 'Ordinarily the settlements above the tunnel, unless caused by a local disturbance such as a run into the face or stopping above the crown, are more or less symmetrical about the vertical axis of the tunnel. They form a trough like depression with a shape roughly resembling the error function or probability curve' (Peck, 1969)

Fig. 1-2. Transverse settlements trough

<!-- image -->

Line chart

As it represents the probability that the x has  a  value  between - ∞ and +∞, the area below  the  trough  is  by  definition  equal  to  1,  as  a  consequence  the  area  enclosed  by settlements trough is defined by:

<!-- formula-not-decoded -->

Vs  is  the  volume  of  the  settlements  trough  per  unit  length,  strictly  dependent  by  the ground affected by the excavation. In grounds with low permeability, such as stiff-clays, with  initially  undrained  response  to  the  excavation  process,  which  means  not  allowed changing in volume, the volume of settlements trough has to correspond to the excess excavated volume of ground to the theoretical volume of the tunnel. It is usual to define the extra excavated ground as Volume Loss , given by:

<!-- formula-not-decoded -->

where D is the outer tunnel diameter. VL is usually defined as a proportion of theoretical tunnel volume per unit length, expressed as a percentage of it.

Combining  the  (1.2) to  (1.3)  ,  the  transverse  settlements  profile  can  be  expressed  in terms of Volume Loss as:

(1.4)

<!-- formula-not-decoded -->

It shows that for a given tunnel diameter D, the settlements profile only depends by the Volume Loss VL and by the trough width i x , two crucial parameters that need to be defined to know the settlements field induced by tunnelling.

O'Reilly &amp; New (1982) showed that the transverse horizontal surface displacements can be derived from the previous equations, considering their resultants pointing toward the center of the tunnel. They gave the expression to determine them:

<!-- formula-not-decoded -->

Fig. 1-3. Horizontal surface displacements and strains in transverse direction together with settlement trough

<!-- image -->

Line chart

Fig.  1-3  clearly  shows as the maximum horizontal displacements occur at the point of inflections of settlements trough ( x i x  ). By differentiating the horizontal displacements with respect to x, the horizontal strains can be obtained from (1.5) as shown in equation (1.6)

<!-- formula-not-decoded -->

Equation (1.6) leads to compression being defined as negative while a positive value is assigned to tension. Fig. 1-3 shows the development of a compression zone between the two  points  of  inflections i x and i y and  of  a  tensile  zone  outside  them;  the  maximum compression  strain  develops  at 0  x ,  while  the  maximum  tensile  strain  develops  at x i x   3 .

## 1.3.1.2. Longitudinal behaviour

Attewell and Woodmann (1982) showed that even the longitudinal settlement profile can be defined through a cumulative probability curve   y  , given by:

<!-- formula-not-decoded -->

as a consequence the longitudinal profile is described by equation (1.8) while the generic settlement is expressed by (1.9) :

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

The  shape  of  longitudinal  displacements  curve  is  shown  in  Fig.  1-4 . It  indicates  the minimum and maximum values of the longitudinal settlements reached respectively at (ahead the tunnel face) and (behind the tunnel face), while above the tunnel face ( 0  y ) it is /2 ,max v v S S  2 .

For  completely  defining  the  longitudinal  settlement  profile,  it  is  important  to  know about  the  curve  width,  defined  by  the y i value.  Attewell  at  al.  (1986)  compared  the magnitudes if x i and y i for a range of case studies; they observed that usually x i is bigger than y i (the transverse settlements troughs were longer than the longitudinal ones); on the basis of field data coming from the tunnel construction of the Jubilee Line Extension beneath St. James's Park in London, Nyren (1998) observed the same behavior translated into the ratio 1.3 /  y x i i .  However, despite this discrepancy, it is common to consider i i i y x   .

Fig. 1-4. Longitudinal settlement profile after Attewell et al., 1986

<!-- image -->

Line chart

Attewell et al. (1986) assumed that for open face tunnelling, the settlement above the tunnel axis ( 0  x )  is 50% of  the maximum settlement reached behind the tunnel face, while for closed face tunnelling, where  significant face support  is provided, the displacements  ahead  the  tunnel  face  reduce  significantly.  Mair  and  Taylor  (1997) concluded that for closed face tunnelling the settlements above the tunnel axis is 25% - 30% the maximum settlement; this leads to a longitudinal displacements curve translated as shown in Fig. 1-5.

2 Attewell  &amp;  Woodman  (1982) showed  that  above  the  tunnel  face,  for  stiff  clays usually  occurs ,max 0) ( 40% v y v S S  

Fig. 1-5. Longitudinal settlement profile for open face and closed face tunnelling after Mair &amp; Taylor (1997)

<!-- image -->

Line chart

Based on the analyses of tunnel induced displacements in the United Kingdom, Craig &amp; Muir Wood (1978) stated that, for each point of observation, depending on the ground, for open face tunnelling, nearly the 80% - 90% of the settlement is reached when the face is one to two times the tunnel depth.

Tab.1-1. Development of settlement profile (Craig &amp; Muir Wood, 1978)

Observing  the  horizontal  displacements  going  toward  the  center  point  of  the  tunnel face,  Attewell  &amp;  Woodman  (1982)  gave  the  expression  (1.10)    for  determining  the horizontal displacements at the ground surface in the longitudinal direction:

<!-- formula-not-decoded -->

By deriving (1.10) with respect to y, the horizontal strains in longitudinal directions can be obtained; it yields:

<!-- formula-not-decoded -->

which describes tension (positive value) ahead the tunnel face ( 0  y ) and compression behind it ( 0  y ).

Because all the above defined displacements and strains strictly depend by the troughs width parameter i and by the Volume Loss L V , on the next section the attention is going to be focused on them.

## 1.3.1.3. Volume loss

The volume loss is a measure of total disturbance of the ground caused by tunnelling. In undrained conditions it represents the volume of the settlements trough at the surface.

It can be defined as 'the ratio of the difference between the excavated soil (defined by the  outer  tunnel  diameter)  and  the  tunnel  volume,  over  the  tunnel  volume ' ( cfr. Expression (1.3) ).

It is caused by different soil movements due to tunnelling. Attewell (1978) divided the sources of volume loss into four categories:

-  Face loss : radial soil movements toward the unsupported tunnel face
-  Shield  loss :  radial  ground  loss  around  the  tunnel  shield  increased  by  eventual overcutting caused by poor workmanship
-  Ground loss during and subsequent to lining erection : caused by soil movements towards the tunnel, due to the unsupported soil in between the shield and the last erected lining; to prevent it is common practice to grout any voids between soil and lining
-  Ground loss after grouting : due to lining deformations after the grouting, caused by the transfer of the overburden pressure.

Several methods have been proposed to estimate the volume loss.

Attewell (1978) proposed a method to determine the four components of L V based on the  ratio  between  the  rate  of  soil  movements  into  the  excavation  (determined  from laboratory tests) and the rate of tunnel in advance.

Many relations have been proposed to determine L V on the base of the stability factor N. Broms &amp; Bennermark (1967) defined N as:

<!-- formula-not-decoded -->

where v  is the total overburden pressure at tunnel axis, t  is tunnel support pressure (if  present) and u s is  the  undrained shear strength of the clay. As greater is N as more plastic  zones  are  going  to  develop  around  the  tunnel:  for 2  N an  elastic  response  is shown with a stable tunnel face (Lake et al., 1992), for 4 2   N some local plastic zones develop around the tunnel while for 6 4   N plastic  yielding  is  likely  leading  to  face stability when 6  N .

In the past many relations have been suggested relating N with tunnel depth or with ; Mair &amp; Taylor (1993) showed a relation between N and the tunnel depth for unsupported tunnels in London Clay, pointing out a value between 2.5 and 3 for the stability ratio N.

Lake  et  al.  (1992)  showed  a  relation  between  N  and L V summarizing  the  relations proposed by many others authors; they showed that a stability ratio 2  N leads to a L V between 1.5% and 3% (Fig. 1-6).

Fig. 1-6. Relations between N and L V (after Lake et al., 1992)

<!-- image -->

Line chart

Davis et  al.,  (1980)  presented  lower  and  upper  bound  analytical  solutions  for  shallow tunnels with support pressure in cohesive soils. They considered the case of plane-strain unlined circular tunnel (radial ground  movements),  a  plane strain heading (face movements) and circular tunnel heading (the full three-dimensional case). They reached the conclusion that in the examined cases, the stability ratio at collapse varies with depth and even showed how for the three-dimensional case the difference between the lower and  upper  bound  collapse  load  was  the  greatest,  indicating  the  difficulties  in  applying analytical  solutions  for  three-dimensional  problems.  The  Authors  plotted  the  results  in term of NTC against  the  cover  to  diameter  ratio C/D .  Data  from  centrifuge  tests (Mair, 1979)  confirmed  the  solutions  for  a  plane  strain  unlined  circular  heading,  with  best agreement for C/D less than 3, the value defined as a practical transition between shallow and  deep  tunnel,  the  first  characterized  by  a  failure  mechanism  involving  the  ground surface, the latter by a symmetric failure mechanism with a little influence on the surface.

Mair et al. (1981) introduced the Load Factor LF to take account for this effect:

<!-- formula-not-decoded -->

where N is  the  stability  ratio  at  the  working  conditions  and NTC is  the  stability  ratio  at collapse (Fig. 1-7).

Fig. 1-7. Relations between LF and VL determined from centrifuge tests and finite element analyses (after Mair et al., 1981)

<!-- image -->

Line chart

## 1.3.1.4. Trough width parameter

Based on 19 case histories for cohesive grounds and on 16 for coehsionless soils (all in the United Kingdom), O'Reilly &amp; New (1982) showed a linear dependence between the trough width parameter i and  the  tunnel  depth z0 shown in Fig. 1-8, defined by (1.14) and (1.15) and simplified by (1.16) .

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

Fig. 1-8. Correlation between i and the tunnel depth z0 (after O'Reilly &amp; New, 1982)

<!-- image -->

Scatter plot

The Authors pointed that k can vary between 0.7 0.4   k ,  going from stiff to soft clay and concluded that 0.5  k is an appropriate value  for clay, for most design purpose. The same result was later confirmed by Rankin (1988) who presented a similar study based on an enlarged data base, so that (1.16) becomes:

<!-- formula-not-decoded -->

Kimura &amp; Mair (1982) obtained the same results from centrifuge tests and also showed that  K  value  does  not  depend  by  the  tunnel  technique  since is  obtained independently  of  the  degree  of  support  within  the  tunnel.  Later  work  by  others researchers  confirmed  that  usually for  cohesive  soils,  while for cohesionless ground.

## 1.3.1.5. Subsurface movements

Only  the  ground  surface  settlements  have  been  examined  in  the  previous  section. Although  surface  settlements  is  the  most  straight  forward  way  to  describe  ground deformation, it only gives a limited picture of the real mechanism controlling tunnel-soil and if it is the case, tunnel-soil-building interaction.

Mair &amp; Taylor (1993) described vertical and horizontal subsurface ground movements by applying  the  plasticity  solutions  for  the  unloading  of  a  cylindrical  cavity,  showing  their good agreements with collected field data.

The solution they presented shows a linear relation between ground movements ( R S v / or R S h / , where v S and h S are respectively vertical and horizontal movements while R is  the  tunnel  radius)  and  the  distance  from  tunnel  centre  as d R / (where d is  the horizontal or vertical distance from tunnel centre). The Authors focused their attention on vertical displacements above the tunnel centre line and on horizontal movements at tunnel  axis  level.  They  concluded  that  the  Gaussian  curve  to  describe  subsurface settlements  troughs  is  in  good  agreement  with  collected  field  data  which  means  that (1.17) could be straight forward applied by substituting 0 z with where z is the required movements 'depth.

<!-- formula-not-decoded -->

Presenting  field  and  centrifuge  data,  Mair  et  al.  (1993)  also  showed  that  settlements troughs are wider with depth z . Fig. 1-9 shows the relation between 0 / z z and 0 / z i ; it can been seen how the dashed line, representing (1.18) , underestimates i with depth. What better fits the data is the solid line, having equation:

<!-- formula-not-decoded -->

which, substituting becomes:

<!-- formula-not-decoded -->

Fig. 1-9. Variation of trough width parameter i of subsurface settlements troughs with depth z (after Mair et al., 1993)

<!-- image -->

Line chart

Combining equation (1.3) and (1.4) with (1.19) , the maximum settlement of subsurface trough can be expressed as:

<!-- formula-not-decoded -->

It is represented by curve B and C in Fig. 1-9; it represents lower and upper bound for the  range  of  tunnel  depths  ( 0.6 0.1 /   o z R )  and  volume  losses  (1.4%)  of  field  data considered in the graph, and also shows how (1.21) would overpredict subsurface ,max v S settlements troughs. If normalizing ,max v S also against L V , a good agreement is obtained even  with  greenfield  measurements  from  the  Jubilee  Line  Extension  (St.  James's  Park) presented by Nyren (1998), having a much higher L V ( 3.3%  L V ).

Fig. 1-10. Subsurface settlement above tunnel centre line (after Mair et al., 1993)

<!-- image -->

Line chart

A  different  approach  to  estimate  the  trough  width  and  the  maximum  settlement  at surface  was  proposed  by  Heath  &amp;  West  (1996).  They  suggested  using  a  binomial distribution,  instead  of  the  Gaussian  curve,  to  describe  the  settlement  trough.  Their approach yields to:

<!-- formula-not-decoded -->

where 0 i is the trough width at ground surface level. Equation (1.21) leads to a maximum surface  settlement ,max v S proportional  to   1/ 2 0   z z .  Comparing  prediction  of ,max v S obtained from their work with the results given by Mair et al. (1993) it can be seen how the  two  different  approaches  give  the  same  results  for 0.8 0 0   z z while,  close  to  the tunnel,  Heath  &amp;  West  (1996)  solution  predicts  larger  values  of ,max v S ,  being  in  total agreement with field data they collected.

About  the  horizontal  surface  movements,  derived  from  the  vertical  ones,  Mair  et  al. (1993) and Taylor (1995) stated that, in order to achieve a constant volume condition, displacements  vectors  should  point  to  the  point  where  the  line  described  by  (1.17)

intersects the tunnel centre line, located 0.325 0.175 0 z  below the tunnel axis level (Fig. 110).

Fig. 1-11. Distribution of i  for subsurface settlement troughs with depth (a) and focus of vectors of soil movement (after Grant &amp; Taylor, 2000) (b)

<!-- image -->

Engineering drawing

Moreover, New &amp; Bowers (1994) showed how considering the soil particle movement toward a single point at the tunnel axis an overprediction of the soil settlements above the tunnel axis is obtained. They proposed to model the ground loss equally distributed over a horizontal plane at the invert level and showed how this assumption is in good agreement with subsurface field measurements of the Heathrow Express trial tunnel.

Grant &amp; Taylor (2000) proposed different indications about horizontal movements close to the surface, by showing results of a number of centrifuge tests. They showed how their laboratory results were in good agreement with (1.17)  apart from a zone in the vicinity of the tunnel where test data show a narrower subsurface trough and close to the surface were wider troughs were measured. They stated that soil displacements vectors point in the direction of the tangent of the distribution of i represented in Fig. 1-11 \_a ; it follows that  horizontal  displacements  at  the  surface  are  underestimated  by  (1.17)  while  in  the vicinity of the tunnel they are overestimated by the same equation.

Finally the influence of different stiffness soil layers overlying clay in which the tunnel has to be constructed, have been investigated by Hagiwara et al. (1999), by performing a number of centrifuge tests. Comparing the results of their tests with a clay-only case, they showed  that  the  settlement  troughs  become  wider  as  the  stiffness  of  the  top  layer increases; so they demonstrated how the tunnel induced settlement behaviour is affected by the interaction of stiffness of an overlying material with the soil in which the tunnel is constructed.

## 1.3.2. Numerical analyses of tunnel construction

Empirical  methods  are  widely  used  to  predict  tunnelling  induced  displacements  in greenfield conditions, neglecting building-tunnel interaction. As mostly of tunnel excavations for metro system enlargements take place in urbanized areas, new methods have  to  be  developed  and  new  calculation  tools  have  to  be  improved  to  correctly consider buildings presence on the ground. In this regard, numerical modelling provides the  possibility  to  accommodate  the  different  elements  of  interaction  problem  in  one analysis.

This  section  gives  an  overview  of  how  Finite  Element  Analyses  have  been  applied  to predict  tunnel  induced  subsidence  mainly  in  greenfield  conditions  to  demonstrate different approaches to simulate tunnel excavation.

As it can be understood from following pages, despite the tunnel excavation is clearly a 3D problem and three dimensional analyses have to be performed to correctly predict tunnelling  induced  effects,  because  of  limitations  in  computational  power,  2D  analyses are  still  widely  used.  Those  analyses  showed  the  importance  of  considering  the  small strain behaviour of the soil, different values for the lateral coefficient at rest and the soil anisotropy, which could clearly leads to an improvement in settlement prediction.

With the development in using 3D analyses, the influence of all the parameters above has been investigated. The following points were highlighted:

-  about  the  influence  of ,  no  significant  difference  in  the  shape  of  induced transverse settlement troughs has been noticed between 2D and 3D analyses;

-  in  longitudinal  direction  the  steady-state  conditions  should  be  achieved  2D (Desari  et  al.,  1996)  or  5D  (Vermeer  et  al.,  2002)  behind  the  tunnel  face depending on the used soil model and values;
-  the  variety  of  analyzed  problems  demonstrates  the  flexibility  of  numerical simulation: the used tunnelling technique, the initial stress conditions, the soil anisotropy  and  the  mesh  dimension  are  the  observed  parameter  whose influence on the analyses results is not negligible.

## 1.3.2.1. Two-dimensional analyses

Despite  tunnel  excavation  is  clearly  a  3D  problems,  because  of  the  remarkable computational sources required to perform thorough 3D  analyses, tunnel excavation is often  modeled  two  dimensionally.  The  five  methods  described  below  have  been proposed to take account of the stress and strain changes ahead the tunnel face when adopting plane strain analyses.

-  GAP Method ( Rowe at al., 1983 ): it prescribes the final tunnel lining position and size smaller than the initial size of the excavation boundary; hence, soil movements are allowed until  the  soil  closes  the  gap,  defined  by  the  difference  between  the  initial excavation  boundary  and  the  final  tunnel  size.  This  method  can  be  seen  as  a simulation of radial VL along tunnel shield, being the GAP parameter representative of the gap between the cutting head and the tunnel lining. However, as the volume loss  has  a  tunnel  face  component  it  is  difficult  to  define  the  gap  parameter  for different sources of volume loss.
-  Convergence-Confinement  Method ( Panet  &amp;  Guenot,  1982 ):  also  known  as  - method with  defining the proportion of unloading before the final lining is installed. For the remaining radial stress on the lining is .
-  Volume Loss Control Method ( Swoboda, 1979 ): used for modelling tunnel excavation with  the New Austrian  Tunnelling  Method (NATM),  it  lies  in  reducing  soil  stiffness within the tunnel boundary before the tunnel excavation is simulated, thus allowing soil  to  move  towards  it.  Because  the  Volume  Loss  is  suitable  as  design  parameter, when known, it can be directly adopted in this method.

-  Longitudinal-transverse Method ( Finno &amp; Clough, 1985 ): it follows from plane strain analyses  of  both  longitudinal  and  transverse  sections  of  the  tunnel,  leading  to account for stress changes and soil movements ahead the tunnel face. In a transverse section  stress  changes  were  applied  prior  to  tunnel  excavation  to  obtain  soil movements similar to those obtained from longitudinal analyses. Tunnel construction was  then  simulated  adopting  the  GAP  Method.  Rowe  &amp;  Lee  (1992)  compared  the settlements  profiles  from  such  a  plane  strain  approach  with  3D  Finite  Element Analyses results, pointing up a significant overestimation of longitudinal settlements and of the plastic zone extension.

Addenbrooke et al. (1997) used the Volume Loss Method to investigate the effects of pre-yield  soil  models  on  results,  performing  a  number  of  plane  strain  analyses  on  the tunnel  construction  of  the  Jubilee  Line  Extension  beneath  St.  James's  Park  in  London. They used:

1. Linear elastic Model with Young's modulus increasing with depth
2. Non-linear Elastic Model, based on Jardine et al. (1986) formulation, considering shear stiffness varying with deviatoric strain and mean effective stress while the bulk stiffness depends on volumetric strain and mean effective stress.
3. Non-linear  Elastic  Model  with  shear  and  bulk  stiffness  depending  on  deviatoric strain and mean effective stress level, also accounting for loading reversals.

Fig. 1-12 shows how the Authors plotted field data, reported by Standing et al. (1996 ) , together with surface settlements, obtained by using lateral earth pressure coefficient at rest in the clay ( ) within the upper bound of values reported by Hight &amp; Higgins (1995). They demonstrated the necessity of including small strain stiffness into pre-yield model, as  the  predictions  of  the  linear  elastic  model  are  inadequate.  Despite  the  nonlinear  models  responses  are  quite  similar,  their  settlements  troughs  are  too  wide  if compared  with  field  data;  the  maximum  settlement  is  consequently  too  small,  as  the analyses were performed under volume loss control. Too wide settlement troughs in a high -regime  has  been  confirmed  even  by  others  authors,  such  as  Gunn,  1993 who presented results from analyses with applying non-linear pre-yield model (Fig. 113).

The  role  of was  highlighted  by  Gens  (1995)  and  Addenbrooke  (1996);  they  later compared FE predictions for tunnel construction of the Jubilee Line in London for both and with field measurements and demonstrated how the low cases showed  deeper  and  narrower  settlements  troughs,  consequently  closer  to  field  data. Performing axial  symmetric  analyses  the  Authors  showed  a  reduction  in  radial  stresses and increase of the hoop stresses around the tunnel boundary. The change in stresses can be  consequently  represented  in  plane  strain  analyses  as  shown  in  Fig.  1-14.  Analyses adopting such a low zone together with non-linear elasto-plastic soil model, showed an improved settlement profile compared with the global cases. Similar results were  presented  by  others  authors  for  2D  and  3D  analyses  (Guedes  &amp;  Santos  Pereira, 2000; Dolezova, 2002; Lee &amp; Ng, 2002).

Fig. 1-12. Surface settlements troughs obtained from different isotropic models (non-linear elastic, perfectly plastic, after Addenbrooke et al., 1997)

<!-- image -->

Line chart

Fig. 1-13. Surface settlements predictions obtained from different input parameters for a nonlinear elastic perfectly plastic model (after Gunn, 1993)

<!-- image -->

Line chart

Fig. 1-14. Layout of zone of reduced (after Potts &amp; Zdravkovic, 2001)

<!-- image -->

Engineering drawing

In order to improve FE predicted settlement profile, Lee &amp; Rowe (1989) suggested using anisotropic  soil  model.  By  presenting  FE  results  from  Heathrow  Express  trial  tunnel Simpson  et  al.  (1996 I showed  how  that  anisotropy  gives  better  surface  displacements prediction.  Addenbrooke  et  al.  (1997)  introduced  such  anisotropy  in  some  of  their analyses by deriving the soil parameters from the small strain stiffness formulation of the original  isotropic  model,  defining  ratios and .  They  performed  two analyses: the first one using anisotropic ratios observed in field measurements reported by  Burland  &amp;  Kalra  (1986) ,  the  second  one with reduced thus making the caly very soft in shear. Results are shown in Fig. 1-15; it is clear how the first parameters set (AJ4i) does not show remarkable  improvements  in  the  settlement  profile  if  compared  to  the  linear  elastic solution,  while  the  second  set  of  parameters  generates  a  deeper  and  narrower settlement  profile,  closer  to  the  field  measurements,  leading  to  the  conclusion  that unrealistic  soil  stiffness  is  required  to  achieve  better  settlement  predictions  when modelling tunnel excavation in plane strain with .

Fig. 1-15. Surface settlement troughs obtained from different anisotropic soil models (AJ4i and AJ4ii: non-linear elastic, perfectly plastic, after Addenbrooke et al., 1997)

<!-- image -->

Line chart

## 1.3.2.2. Three-dimensional analyses

Following pages describe 3D analyses results performed by many authors with different approach, in order to resume the observed influence of some of the analyzed parameters, including the soil behaviour and the machine parameters.

Three main tunnel excavation methods can be defined to perform FE three dimensional analyses:

-  ' Step-By-Step '  approach  (Katzenbach  &amp;  Breth,  1981):  tunnel  excavation  is modeled by successive removal of tunnel face elements while installing the final lining behind the tunnel face, at distance equal to excavation length;
-  ' Volume Loss Control ' method, as described in Paragraph 1.3.2.1.;
-  ' Detail  Approach '  modelling  the  excavation  machine  main  features,  such  as grouting and slurry pressure.

Katzenbach &amp; Breth (1981) and Desari et al. (1996)  performed  3D  analyses  using  the 'step-by-step' approach of a NATM tunnelling respectively in Frankfurt Clay, with a nonlinear elastic soil model and lateral earth pressure at rest ,  and in London Clay with a non-linear elastic perfectly plastic  soil  model  and .  In  the  first  case  the analyses  settlement  trough  was  in  good  agreement  with  the  field  data,  in  the  latter  it resulted  too  wide  if  compared  with  the  field  measurements.  Desari  et  al.  (1996)  also revealed that the time dependent Young's modulus of the concrete tunnel lining has not great influence on the settlement trough and that the stationary settlement conditions (or  'steady-state'  conditions,  referring  to  Vermeer  et  al.,  2002)  were  established  2 diameters behind the tunnel face.

By  modelling  a  similar  tunnel  construction  as  Desari  et  al.  (1996),  Tang  et  al.  (2000) investigated the excavation length influence on both transverse  and longitudinal settlement profile,  with  two  excavation  lengths  (5  m  and  10  m).  The  London  Clay  was modeled  with  a  transversely  anisotropic  linear-elastic  perfectly plastic constitutive relationship  and  with ,  moreover  the  tunnel  construction  was  modelles  as coupled with a coefficient of permeability for the clay and tunnel advance rate per day. Fig. 1-16 shows for both the excavation  lengths the longitudinal settlement profile; it indicates a steady state of settlement approximately 20 m behind the tunnel face and increasing with the increasing excavation length.

Fig. 1-16. Longitudinal settlement profile obtained for different excavation lengths L exc

<!-- image -->

Line chart

Vermeer et al. (2002) highlighted the importance of the first excavation step in 3D stepby-step  analyses  of  an  8  m  diameter  tunnel,  using  a  linear  elastic  perfectly  plastic  soil model with and (Fig.  1-17).  In  the  first  analysis  an  unsupported excavation  was  performed  in  the  first  step  before  the  final  lining  was  installed;  in  the second one lining was installed  all  over  the  length  of  the  first  excavation  step  prior  to excavation. The Authors concluded that the first excavation step has great influence on the whole analysis and steady-state conditions develop approximately 40 m (5D) behind the tunnel face. As the obtained settlement profiles were in good agreements with the corresponding  plane  strain  analyses,  a fast  settlement  analysis ,  allowing  a  significant reduction in calculations  time,  have  been proposed by the same Authors. It consists in defining  a  two  phases  step-by-step  analysis,  and  using  the  obtained  volume  loss  to perform a final plane strain analysis in order to predict the settlement trough. In the first phase of the 3D step-by-step analysis a complete tunnel is constructed up to a distance over which steady-state conditions can develop, then the lining is installed all over the whole length and displacements are set to zero; afterward the second phase is defined performing  a  single  excavation  step  of  L exc without  lining  installation.  The  latter  phase induces a settlement crater on the surface whose volume loss is used to perform the final 2D analysis using the convergence-confinement method.

Fig. 1-17. Longitudinal settlement profiles for different excavation methods in the first excavation step (after Vermeer et al., 2002)

<!-- image -->

Line chart

In order to reduce the number of steps in a 3D analysis, the excavation technique from plane strain situations were used. Lee &amp; Rowe (1991) performed 3D analyses with the gap method,  of  a diameter  Thunder  Bay  sewer  tunnel  in  Ontario  (Canada),  using  a transverse anisotropic linear perfectly plastic soil model and lateral earth pressure at rest .  The  radial  volume  loss  was  determined  from  the  tunnel  machine  while  the potential  face  loss  was  estimated  from  3D  analysis.  The  tunnel  was  excavated  over  its whole length allowing the full release of axial stress in order to simulate the face loss. The physical gap of the tunnel machine was then applied over the length of the shield, while the total gap (radial and face loss) was applied behind the shield. The lining was installed when the gap was closed. Their prediction were in good agreement with field data and the transverse settlement trough was slightly too wide with a ratio of settlement trough width .

The influence of lateral earth pressure and of soil anisotropy has been investigated in 3D studies by Guedes &amp; Santos Pereira (2000), Dolezalovà (2002), Lee &amp; Ng (2002).

Guedes  &amp;  Santos  Pereira  (2000)  presented  results  from  2D  and  3D  analyses  with and , concluding that 3D simulation does not change the trend of wider settlement trough with increasing ,  as  observed in 2D analyses. The same conclusion was  stated  by  Dolezalovà  (2002)  presenting  2D  and  3D  results  of  the  Mrazovka Exlploratory Gallery near Prague; moreover she did not notice any relationship between the type of analysis (2D or 3D) and .

Lee  &amp;  Ng  (2002)  investigated  both and  soil  anisotropy  (expressed  as ) influence  on  settlement  trough. and , (isotropic  case)  and were  applied  in  their  analyses,  while  the  ratio was  kept  as constant.  They  showed  how  the  transverse  settlement  trough  becomes  deeper  with decreasing  in and/or  increasing in ,  according  to  Addenbrooke  (1996)  and Addenbrooke et al. (1997) 3 .  However Lee &amp; Ng (2002) observed the 3D analyses much more affected by changes in and than the 2D ones, in contrast to what has been obtained by Guedes &amp; Santos Pereira (2000) and Dolezalovà (2002) who did not find great differences between 3D and plane strain analyses.

Finally the tunnel boring machine features influence was investigated by Komiya et al. (1999) and Dias et al. (2000).

Komiya et al. (1999) performed 3D analyses modelling the excavation machine by a rigid body  shield  highly  stiff  and  with  a  self  weight  modeled  by  applied  body  forces.  The advance of the tunnel shield was modeled by applying hydraulic jack forces at the back of the  shield,  so  as  to  reproduce  the  3D  movements  of  the  machine,  accordingly  to  the excavation practice. As they used records of hydraulic jacks forces, their prediction were quite reasonable in reproducing negligible measured displacements.

3 The degree of anistropy is the inverse of the ratio used by Addenbrooke et al. (1997). used by Addenbrooke et al. (1997) is the same as adopted by Lee &amp; Ng (2002). The degrees of anisotropy are thus equivalent while the tunnel geometry changes.

Conversely, Dias et al. (2000) analyzed the construction of a tunnel in Cairo, modelling the shield machine with its conical shape, with the over cut and by applying pressure at the  face  and  at  the  circumferential  tunnel  boundary,  in  order  to  simulate  slurry  and grouting  pressure.  Their  3D  results  overestimated  the  measured  settlements  by  nearly 100%.  Comparing  the  3D  results  with  plane  strain  analyses  ones,  in  which  grouting pressure and the conical shape of the shield were modeled, the Authors observed the 3D analyses exhibiting a narrower trough than the 2D did.

## 1.4. Building damage assessment

Since  tunnelling  excavation  in  soft  ground  causes  ground  movements  as  described  in previous  sections,  in  urban  area  the  ground  subsidence  can  affect  existing  surface  and subsurface structures. As a consequence, predicting tunnel induced deformation of such structures  and  assessing  the  risk  of  damage  is  an  essential  part  for  tunnels  planning, designing and building processes (Mair et al., 1996). As it will be shown in the following pages, even if the damage assessment does not account for building characteristics such as building stiffness, detailed strategies have been developed.

## 1.4.1. Definition of structure deformation parameters

In  order  to  quantify  tunnel  induced  buildings  deformation,  Burland  and  Wroth  (1974) proposed the following widely accepted in-plane parameters (three-dimensional behaviour such as twisting is not included):

-  Settlements : the vertical movement of a point, positive if indicating downwards movements (Fig. 1-18\_ a )
-  Differential or relative settlement ( ) : the difference between two settlements values (Fig. 1-18\_ a )

-  Rotation or slope ( ) : the change in gradient of the straight line defined by two reference points embedded in the structure (Fig. 1-18\_ a )
-  Angular strain ( ) : producing sagging (upward concavity) when positive, hogging (downward concavity) if negative (Fig. 1-18\_ a )
-  Relative deflection ( ) :  the maximum displacement relative to the straight line connecting two reference points with a distance L, indicating sagging deformation if positive (Fig. 1-18\_ b )
-  Deflection ratio (DR) : the quotient of relative deflection and the corresponding length: (Fig. 1-18\_ b )
-  Tilt  ( ) :  the  rigid  body  rotation  of  the  whole  superstructure  or  a  well-defined part of it, difficult to define as the structure normally flexes itself (Fig. 1-18\_ c )
-  Relative  rotation  or  angular  distortion  ( ) :  the  rotation  of  the  straight  line joining two reference points relative to the tilt (Fig. 1-18\_ c )
-  Average horizontal strain ( ) : defined as change in length over the corresponding length L.

To determine the above listed parameters a number of informations, seldom available in engineering practice, are required (Rankine, 1988). However it will be shown that two of  them  are  of  significant  importance  in  defining  the  building  damage,  such  as  the deflection ratio (DR) and the horizontal strain ( ).

Fig. 1-18. Building deformation parameters (a, b, and c) and schematic diagram of three stage approach for damage risk evaluation

<!-- image -->

Flow chart

## 1.4.2. Evaluation of risk of damage

The following pages summarize the ' three stage approach '  widely used to assess the potential building damage for tunnel projects in London (Mair et al., 1996) such as the Jubilee Line Extension, the Channel Tunnel Rail Link and the Cross Rail project. It consists of three stages known as: preliminary assessments , second stage assessment and detailed evaluation .

## 1.4.2.1. Preliminary assessment

The presence of the building is not considered and the greenfield settlement profile is evaluated.

Rankin  (1988)  showed  that  for  buildings  measuring and the risk of damage is negligible, than for such buildings not any more detailed evaluation is carried on; contrariwise in case of exceeding them the second stage assessment has to be  carried  out.  The  above  values  can  be  reduced  with  an  increasing  in  buildings sensitivity.

## 1.4.2.2. Second stage assessment

The building is represented as an elastic beam whose foundation is assumed to follow the settlement profile described by the empirical greenfield trough, not accounting the building's  stiffness.  The  settlement  trough  is  used  to  calculate  the  deflection  ratio  DR (both  for  sagging  and  hogging)  and  the  tensile  strain (both  for  compression  and tension)  in  order  to  define  the  strain  within  the  beam  and  consequently  the  level  of damage,  as  described  in  the  following  sections.  Referring  to  a  number  of  case  studies Frischmann et al. (1994) showed that the building's stiffness interacts with the ground such  that  the  deflection  ratio  and  the  tensile  strain  reduce,  as  a  consequence  Burland (1995) pointed out that the category of damage obtained by the assumptions underlying this stage, is only a possible degree of damage for the structure, usually higher than the real one.

After the required parameters calculation is performed, the relative category of damage is  defined  by  Tab.1-2  and  Tab.1-3.  In  case  of  exceeding  the  second  level  of  damage, corresponding to a damage potentially affecting building serviceability, a more detailed evaluation has to be performed following the next step of the 'three stage approach'.

## 1.4.2.3. Detailed evaluation

Details of the building and of the tunnel construction should be taken into account in this  approach,  including  the  three-dimensional  process  of  tunnel  construction  and  the building  orientation  with  respect  to  the  tunnel  axis.  According  to  Burland  (1995), foundations  design  of  the  building,  its  structural  continuity  and  its  possible  previous movements should also be accounted.

As Fig. 1-19 shows, the soil-structure interaction plays an important role in defining the induced settlement field, since the influence of building's stiffness is likely to reduce the greenfield  displacements.  However  the  same  Fig.  1-19  shows  the  measured  building settlements  significantly  differing  from  the  predicted  ones  according  to  the  effects  of building's  stiffness,  leading  to  a  reduction  both  of  the  slope  and  of  the  maximum settlement compared to the greenfield situation and moreover of the horizontal strain within  the  structure  (Geddes,  1991).  Potts  &amp;  Addenbrooke  (1997)  showed  that  the influence  of  soil-structure  interaction  could  be  incorporated  into  the  second  stage assessment in order to reduce the number of cases for which a detailed evaluation has to be carried out; the suggested procedure will be discuss in following pages.

Because of the conservative assumption of the second stage assessment, Burland (1995) pointed out that the category of damage coming out from this evaluation is usually lower than the one obtained from the previous stages. However for buildings remaining in the third  or  higher  category  of  damage  (Tab.1-2)  after  the  detailed  evaluation,  protective measures have to be considered as necessary.

Fig. 1-19. Tunnel induced building settlement of Maison House, London (after Frischmann et al., 1994)

<!-- image -->

Line chart

## 1.4.3. Category of damage

Burland et al. (1977) distinguished between three criteria when considering the building damage:  visual  appearance,  serviceability  or  function  and  stability.  Since  the  visual damage  is  difficult  to  quantify  as  it  depends  on  subjective  criteria,  they  proposed  a system to identify and classify the level of damage, based on the ease of repair, resumed in Tab.1-2. Such a table was developed for brickwork or stone masonry and the relative degree  of  severity  only  concerns  to  standard  domestic  or  office  buildings;  the  same Authors pointed out that more stringent criteria has to be defined when initial cracks can lead to corrosion, penetration etc.

The  6  categories  of  damage  resumed  in  Tab.1-2  can  be  subdivided  into  the  group  of damage  levels  indicated  in  Tab.1-3  categories  0  up  to  2  correspond  to  aesthetical damage, categories 3 and 4 to serviceability damage and  category 5 to damage affecting the stability of the structure. As mentioned in the previous pages, the division between category 2 and 3 represents an important threshold since Burland (1995) pointed out that damage related to categories 0 to 2 can result from several causes within the structure (such  as  thermal  effects),  however  damage  of  category  3  or  higher  is  frequently associated with ground movements.

Tab.1-2. Classification of visible damage to walls with particular reference to ease of repair of plaster and brickwork masonry (after Burland, 1995)

Tab.1-3. Relation between category of damage and limiting tensile strain (after Boscardin &amp; Cording, 1989 and Burland, 1995)

## 1.4.4. Calculation of building strain

Basing on results of a number of large scale tests on masonry panels and walls, Burland &amp; Wroth (1974) showed that the onset of cracking is usually associated to a well defined value of average tensile strain, defined as critical strain , measured over a length of 1 m  or  more.  It  results  to  be  unrelated  to  the  mode  of  deformation  and  its  values  are for brick works, for conrete. Burland and Wroth (1974) noted that these values are usually larger than the local strain corresponding with tensile failure.

In  1977  Burland  et  al.  replaced  the  notation  of by  the ,  referred  to  as  the limiting  tensile  strain  in  order  to  take  account  of  different  materials  and  serviceability limit states.

Boscardin &amp; Cording (1989) linked values of limiting strains to the categories of damage resumed Tab.1-2, as reported in Tab.1-3.

Burland &amp; Wroth (1974) and Burland (1977) applied the concept of limiting tensile strain to elastic beam theory. In such a way they could demonstrate the mechanism controlling the onset of cracking within a structure.

The elastic beam used in their model is described by a width B and high H. Two possible deformations  can  occur:  bending  deformation  (Fig.  1-20\_ c ), leading  to  a  cracking mechanism caused by direct tensile  strain,  and  shear  deformation,  leading  to  diagonal cracks caused by diagonal tensile strains (Fig. 1-20\_ d ).

Basing on Timoshenko theory for an elastic beam under particular load conditions, for a centrally  loaded  beam  subjected  both  to  shear  and  bending  deformation,  the  total deflection is given by:

<!-- formula-not-decoded -->

where E is Young's modulus, G is the shear modulus and P the point load applied in the middle of the beam. For an isotropic elastic material (assuming ).

The maximum values for the tensile strain within the beam depends by the deformation mode and by the neutral axis position. For neutral axis in the middle of the beam, Burland &amp; Wroth expressed equation (1.23) in terms of deflection ratio ,  maximum extreme fibre strain and maximum diagonal strain as reported below:

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

Fig. 1-20. Cracking of a simple beam in different modes of deformation (after Burland &amp; Wroth, 1974)

<!-- image -->

Engineering drawing

Both the equations are plotted in Fig. 1-21\_ a for ;  it  shows for the diagonal strain being more critical and for B/H increasing above this value, bending becoming the most critical  mode  of  deformation.  Despite  for  the  equations  above  the neutral  axis  was  assumed  to  be  in  the  middle  of  the  beam,  since  foundations  offer significant restraint to their deformations, it can be more realistic to consider the neutral axis at the lower extreme fiber. It leads equations (1.23) and (1.25) changing in (1.26) and (1.27) .

(1.26)

where  is the Poisson's ratio of the beam.

<!-- formula-not-decoded -->

As the neutral axis is assumed to be at the lower extreme fiber, equations (1.26) only applies for hogging deformation mode; indeed, in the case of sagging there are no tensile strains. Equations (1.26) and (1.27) are plotted in Fig. 1-21\_ b . Comparing Fig. 1-21\_ a with Fig. 1-21\_ b it is clear how for a given value of the value of B/H in the second figure is twice that in first one.

Whereas the building weight induced displacements mainly develop in vertical direction leading  to  sagging  and/or  hogging  deformations  (Burland  &amp;  Wroth,  1974  and  Burland, 1977),  the  tunnelling  induced  ground  movements  leads  as  well  to  horizontal  strains. Geddes (1978) highlighted that the horizontal strains can have a significant influence on existing  building.  Boscardin  &amp;  Cording  (1989)  included  them  in  the  above  mentioned framework  by  superimposing  building  strain  due  to  deflection  deformation  with  the horizontal ground strain . The resultant extreme fiber strain and the resultant diagonal tensile strain are respectively given by:

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

Fig. 1-21. Relationship between and for rectangular beamn deflecting due to combined bending and shear: a) neutral axis in the middle, b) neutral axis at the bottom (after Burland &amp; Wroth, 1974)

<!-- image -->

Line chart

By referring to Boscardin &amp; Cording (1989), Geddes (1991) pointed out that the shear strains develop at the structure-ground interface and then that the strain in the structure may differ considerably from the ground strain, as a consequence the approach proposed by Boscardin &amp; Cording (1989) generally overestimates a structure horizontal's strain. The same Authors related the limiting strain to angular distortion and horizontal strain as shown in Fig. 1-21 where a number of case studies subjected to tunnel construction and shallow  mines  are  reported.  Boscardin  &amp;  Cording  (1989)  concluded  that  the  level  of recorded  damage  for  most  cases  fell  within  the  boundaries  by  the  curves  of  limiting strains.

Burland (1995) presented  similar plots for horizontal strain and  deflection ratio, developing  diagrams  showing  the  relationship  between  DR  and for  particular values (Fig. 1-23). Each contour line in the plot represents a value of limiting strain listed in Tab.1-3; for the limiting values of horizontal strain are the same as given in the same table.

Fig. 1-22. Relation of damage to angular distortion and horizontal extension (after Boscardin &amp; Cording, 1989)

<!-- image -->

Line chart

Fig. 1-23. Relation of damage category to deflection ratio and horizontal tensile strain for hogging ( ) (after Burland, 1995)

<!-- image -->

Line chart

## Chapter 2. LINE 6: A 3 KM TUNNEL IN A DENSELY URBANIZED ENVIRONMENT

## 2.1. Introduction

The Neapolitan underground system is actually made of 8 lines linking the Neapolitan suburbs with the city center (Fig.2-1). As described below, this complex urban transport system  has  been  obtained  by  using,  adapting  and  updating  some  of  the  old  existing railway lines connecting some of the Neapolitan areas since the last century.

In  this  section,  after  an  initial  description  of  the  line,  results  from  empirical  methods used to predict the Line 6 tunnelling induced effects, in terms of ground displacements will be presented, together with a possible assessment of the buildings 'damage.

Fig.2-1. Metro of Naples

<!-- image -->

Geographical map

Apart  from  the Cumana ,  the  railway  line  connecting  the  old  town  to  the  Western Flegrea  area,  going  from Montesanto to Pozzuoli ,  working  since  1889,  what  is  actually known as Line 2, opened in 1925, has been the first Neapolitan metro line to be built. It initially was an ordinary railway line, later adapted to a metropolitan line, connecting the Western  suburb  of Bagnoli to  the  Eastern  area  of  the  city  center  in Piazza  Garibaldi (where  the  central  train  station  is  located),  passing  through  what  in  that  period  were considered  the  most  important  places  of  the  city, Fuorigrotta,  Mergellina,  Chiaia  and Montesanto .  The  line  was  named as Line 2 around 1990, after the Line 1 started to be built.

The first part of Line 1 to be realized was the stretch from Vanvitelli to Colli Aminei ,  in the Northern area of the city.

Line  1    actually  consists  of  a  13  km  tunnel  and  14  stations  shafts  ( Dante,  Museo, Materdei, Salvator Rosa, Cilea/Quattro Giornate, Medaglie d'Oro, Vanvitelli, Montedonzelli, Rione Alto, Policlinico, Colli Aminei, Frullone/San Rocco, Chiaiano/(Marianella,  Piscinola/Scampia ),  all  excavated  in  what  is  the  most  urbanized area of Neapolitan environment. Despite the segment connecting Piazza Dante , in the old town, to Piscinola ,  in  the North-Eastern part of the city, is already working, the building process of the Line is still  in  progress;  the  completion  of  the  operations  is  planned  for 2013.  Once the building process will be totally finished, the line will form a circular ring connecting all the strategical parts of the city, the old town ( Toledo, Piazza Dante, Piazza Cavour, Museo, Materdei ), the university area ( Università ), the hospital area ( Policlinico ), the central train station ( Piazza Garibaldi ), the seaport ( Piazza Municipio ) and the airport ( Capodichino )  to  the  Northern  suburbs  of  the  Neapolitan  environment  ( Piscinola, Scampia ).  Moreover thanks to some strategical interchanges with Line 2 (in Museo and Piazza  Garibaldi )  and  Line  6  (in Piazza  Municipio ),  the  mentioned  areas  will  be  easily reached even from the Eastern and the Western parts of the city.

In order to obtain an efficient and well classified Neapolitan metro system, after the Line 1  excavation  process  started,  and  after  the  old  train  line  was  identified  as  Line  2,  the preexisting  Eastern  train  lines  of Circumvesuviana , Circumflgrea and Cumana (working respectively since 1891, 1962 and 1889) have been named as Line 3, Line 4, Line 5 and Line 7.

At the moment, a part of the Southern part of Line 1 (from Piazza Garibaldi to Piazza Dante ) to be accomplished, Line 6 is the last line to be built.

The  building  process  of  the  line  is  actually  in  progress.  Once  completed,  the  line  will connect the University suburb of Fuorigrotta , in the Western area of the City, to the old town ( Piazza Municipio) .

The  design  of  the  line  is  dated  back  to  the  80s  when  the  idea  was  to  create  a ' metrotramvia ',  something  in  between  an  underground  Metro  line  and  a  superficial Tramline, crossing from West to East the Neapolitan territory.

Although the construction process was supposed to be finished within 1990, because of technical and administrative problems it was interrupted and suspended for more than 10 years. The building operations restarted in 2002.

Since January 2007 the first part of the Line, from Fuorigrotta to Mergellina station, is working  while  the  stretch  between Mergellina and Piazza Municipio is  going  to  be finished in the next months. At the moment the last 3 km tunnel excavation is underway.

## 2.2. LINE 6: the design

The  original  design  of  Line  6  counts  about  an  8  km  long  tunnel  going  from Mostra Station in  Fuorigrotta  suburb,  to Piazza  Municipio station  in  the  old  town,  where  the seaport is located. Once completed, Line 6 will count 8 station shafts, up to 45 m depth: Mostra, Augusto, Lala, Mergellina, Arco Mirelli, San Pasquale, Chiaia e Municipio (Fig.2-2).

The beginning part of the line ( Mostra - Mergellina ) has already been realized and it is working  since  2007.  The  excavation  process  of  the  line  restarted  2009  from  Via Piedigrotta, nearby Mergellina station,  where  the  old  TBM  was  stuck  for  more  than  10 years.

Fig.2-2. Line 6 plan

<!-- image -->

Geographical map

According to the design, the tunnel is located beneath Via Piedigrotta and it follows its route in the whole stretch between Mergellina and Piazza Vittoria . It crosses one of the most densely urbanized areas of the city (Riviera di Chiaia), and it has to be excavated in what  is  the  typical  Neapolitan  ground  succession,  made  by Pozzolane (volcanic  loose sand) and Yellow Neapolitan Tuff (YNT).

The tunnel is always located below the groundwater level, mainly crossing the Pozzolone layer. As a matter of fact about 1.2 km (from Mergellina to Piazza Vittoria ) of the 3.3 km missing tunnel of the line, have to be excavated in the Pozzolane ground layer, saving a small 200 m long stretch, between Arco Mirelli and Via S. M. in Portico, where a 10 m YNT cover has been measured; in that area the tunnel is 12 m to 20 m deep. Conversely from Piazza Vittoria up to Piazza Municipio , the tunnel is located up to 44 m deep and crosses the YNT layer, with an extreme 33 m thick YNT cover layer.

An EPB ( Earth Pressure Balance ) machine has been chosen to carry on the tunnel digging operations.

The sandy ground and the high groundwater level led to prefer an EPB machine rather than a Hydroshield TBM. The possibility in applying a face pressure using the excavated material, preserved and constantly checked in the excavation chamber, and the change to straight install the final lining few meters behind the shield, allow to better control the induced displacements and consequently to reduce the effects on preexisting buildings.

Moreover,  because  of  the  opportunity  to  dig  and  simultaneously  assembling  the  final lining,  the  chosen  digging  technique  leads  to  a  shortening  of  the  tunnel  construction process.

The  new  machine  is  an  8.10  m  diameter  EPB.  Because  it  has  to  replace  the  old Hydroshield  TBM  machine  stuck  into  the  ground  at  the  beginning  of  Via  Piedigrotta, nearby Mergellina station, the EPB diameter is smaller than the TBM one, so that it can be easily put into the previously excavated portion of tunnel, after the old TBM have been disassembled and pulled out.

The final lining is made by (8+1) precast concrete segments (0.30 x 1.70 x 1.50) m. The inner  diameter  is  7.20  m  and  the  outer  is  7.85  m,  from  this  it  follows  about  150  mm interspace between the machine and the final lining to be filled. The lining used materials are  an  Rck 45  MPa  concrete  and  a  FeB  44  K  steel  reinforcement.  The  main  material properties are described below.

Tab.2-1. Material properties

| Concrete            | R ck 45 MPa                     |
|---------------------|---------------------------------|
| f ck                | 0.83*R ck = 37.4 MPa            |
| f ctk               | 0.7*0.269*(R ck ) 2/3 = 2.4 MPa |
| E c                 | 5700*(R ck ) 0.5 = 38250 MPa    |
| Steel reinforcement | FeB 44 K                        |
| f yk                | 440 MPa                         |
| E s                 | 210000 MPa                      |

Since  the  tunnel  has  to  be  excavated  in  a  densely  urbanized  area,  the  surrounding buildings defense from the induced tunnel displacements is required; hence many ground reinforcement have been implemented, before the tunnel digging operations started. In detail,  a  number  of  jet  grouting  columns  have  been  realized  sideways  along  Via Piedigrotta, where two micropiles lines were previously realized to protect the preexisting buildings.

Being the tunnel line always below the groundwater level a possible water flow toward the machine is possible when the old shield is removed; hence a number of jet grouting injections from the ground level, together with concrete and chemical columns (from the tunnel to the area below the shield), have been realized in front of and all around the old TBM, so as to prevent excessive displacements  when the machine is removed and the digging  operations  restart.  The  purpose  is  to  obtain  a  less  permeable  and  more  stable ground layer around the machine.

The main jet grouting columns properties are described in the table below.

Tab.2-2. Jet grouting columns properties

| JET GROUTING COLOUMNS            | JET GROUTING COLOUMNS    |
|----------------------------------|--------------------------|
| Diameter                         |  900                    |
| Geometry (triangular grid)       | 0.75 m x 0.75 m x 0.75 m |
| Injecting pressure               | ≥ 40 MPa                 |
| Expected treated soil resistance | ≥ 6 MPa                  |

## 2.2.1. Ground conditions

The  whole  Line  6  route  is  located  in  a  volcanic  area  named  as  ' Distretto  Vulcanico Flegreo-Napoletano ',  including  Naples,  the  islands  Procida  and  Ischia  and  the  NorthWestern area of the Neapolitan bay.

From site investigations campaigns performed all over the years, since the first stretch of the line started to be built, many kind of soils have been identified as Fig.2-8 shows. Because of the similarity in physical and mechanical properties between the upper sandy layers  found  all  along  the  line  track,  it  is  possible  to  consider  the  whole  stratigraphy mainly  affected  by  two  kind  of  soils:  disturbed  and  undisturbed  superficial  loose Piroclastiti deposits and Yellow Neapolitan Tuff (YNT).

The  upper  loose  Piroclastiti  deposit  is  made  by  three  different  stratifications:  the deepest (10 m thick) made by Piroclastiti deposits, the middle one (from 16 m to 18 m thick) made by undisturbed Piroclastiti and the most superficial one (10 m thick) made by Piroclastiti reworked by flood. Because of the Piroclastiti deposits high variability in grain size and lithology a complex groundwater flow takes place and a number of interconnected and overlapping groundwater levels are formed. However the measured piezometric level in that area is varying among 1 and 2 m a.m.s.l.

The Tuff layer has highly variable thickness across the whole tunnel line: 110 m in the Posillipo area, from 60 m to 90 m between Piazza Vittoria and Piazza Plebiscito. Its upper limit  increases  going  from  Mergellina  (15  m  deep)  to  Piazza  Vittoria  (60  m  deep)  and decreases going to Piazza Municipio (15 m deep) (Fig.2-7).

In  between  Mergellina  and  Piazza  dei  Martiri  the  tunnel  is  always  located  in  the Piroclastiti deposit below 11 m up to 16 m thick ground cover, except for a 200 m long stretch straddle Arco Mirelli station. However from Piazza dei Martiri to Piazza Municpio the  tunnel  affects  the  YNT  with  a  33  m  up  to  15  m  thick  ground  cover.  Because  of  a number of geological faults affecting the YNT, its permeability is comparable to the upper sandy layers one ( ).

The  main  physical  and  geotechnical  characteristics  of  soils  affected  by  the  tunnel excavation  have  been  obtained  by  numerous  site  investigations  and  laboratory  tests carried out in between 1990 and 2005.  Tab.2-3 summarizes the number of boreholes and the  tests  performed  all  over  the  years.  Details  of  performed  site  investigations  are reported in the Appendix II .

Tab.2-3. General informations about site and laboratory investigation campaign performed from 1990 up to 2005

| INVESTIGATION CAMPAIGNS   | BOREHOLES                 | CPT   | SPT   | PERMEABILITY TESTS   | LABORATORY TESTS   |
|---------------------------|---------------------------|-------|-------|----------------------|--------------------|
| 1990                      | 45                        | 5     | -     | -                    | On loose soils     |
| 1998 - 2000               | 24                        | 6     | 60    | Lefranc              | On Tuff            |
| 2005                      | 10 (Arco Mirelli Station) | -     | 10    | Lugeon x 2           | -                  |
| 2005                      | 10 (San Pasquale Station) | -     | 10    | Lugeon x 2           | -                  |
| 2005                      | 10 (Chiaia Station)       | -     | 7     | -                    | -                  |

## 2.2.1.1. Site and laboratory investigations

On  the  basis  of  informations  collected  during  the  first  site  investigation  campaign  in 1990,  performed to realize the first Line 6 stretch (Fuorigrotta - Mergellina), a number of further  site  and  laboratory  investigations  were  planned  in  order  to  have  a  global  view about the soil affected by the Mergellina - Municipio tunnel excavation.

Appendix  II reports  informations  about  the  performed  investigations  and  the  results from in situ (CPT, SPT, Lefranc and /or Lugeon permeability tests) and laboratory tests. From the collected informations the main physical and mechanical parameters for each soil layer were extracted (Fig.2-3 - Fig.2-6). Informations from CPT and SPT investigations have been processed using Durgunoglu e Mitchell (1975) and De Mello (1971) relations, while results of laboratory tests have been  depicted in the  Mohr  plane imposing ,  as  figures below show. CPT tests have been used for strain parameters calculation too, by means of empirical correlation:

with as suggested by Meyerhof e Fellenius (1985).

Figures and tables below report the informations obtained for each soil layer and Tab.24 resumes the main physical and mechanical parameters.

| SAND                                | Average value   |
|-------------------------------------|-----------------|
|  [kN/m 3 ]                         | 16              |
|  sat [kN/m 3 ]                     | 18              |
|  ' [kN/m 3 ]                       | 8               |
| k [cm/s]                            | 10 -04  10 -05 |
| Uniaxial compression strength [MPa] | 0               |
| c' [kPa]                            | 37°             |
|  ' [°]                             | 50000           |
| E' [MPa]                            | 0.3             |
|  '                                 | 0.5             |
| k o                                 | 16              |

<!-- image -->

Engineering drawing

Fig.2-3. Sand physical-mechanical properties

<!-- image -->

Line chart

| PIROCLASTITI                        | Average value   |
|-------------------------------------|-----------------|
|  [kN/m 3 ]                         | 14              |
|  sat [kN/m 3 ]                     | 16              |
|  ' [kN/m 3 ]                       | 6               |
| k [cm/s]                            | 10 -04  10 -05 |
| Uniaxial compression strength [MPa] | 0               |
| c' [kPa]                            | 36°             |
|  ' [°]                             | 40000           |
| E' [MPa]                            | 0.3             |
|  '                                 | 0.5             |
| k o                                 | 14              |

Fig.2-4. Piroclastiti physical-mechanical properties

<!-- image -->

Line chart

| CINERITI                            | Average value   |
|-------------------------------------|-----------------|
|  [kN/m 3 ]                         | 14              |
|  sat [kN/m 3 ]                     | 16              |
|  ' [kN/m 3 ]                       | 6               |
| k [cm/s]                            | 10 -04  10 -05 |
| Uniaxial compression strength [MPa] | 0               |
| c' [kPa]                            | 37°             |
|  ' [°]                             | 50000           |
| E' [MPa]                            | 0.3             |
|  '                                 | 0.5             |
| k o                                 |                 |

<!-- image -->

Engineering drawing

Fig.2-5. Cineriti physical-mechanical properties

<!-- image -->

Line chart

| TUFF                                | Average value   |
|-------------------------------------|-----------------|
|  [kN/m 3 ]                         | 14              |
|  sat [kN/m 3 ]                     | 16              |
|  ' [kN/m 3 ]                       | 6               |
| k [cm/s]                            | 10 -4 -10 -5    |
| Uniaxial compression strength [MPa] | 2.5             |
| c' [kPa]                            | 500             |
|  ' [°]                             | 27°             |
| E' [MPa]                            | 1000            |
|  '                                 | 0.3             |
| k o                                 | 0.5             |

Fig.2-6. Tuff physical-mechanical properties

<!-- image -->

Scatter plot

Tab.2-4. Physical an mechanical parameters for each soil layer

| GROUND TYPE   |    [kN/m 3 ] |    [-] |   E [MPa] |    [°] |   c' [MPa] |
|---------------|---------------|---------|-----------|---------|------------|
| SAND          |            16 |     0.3 |        50 |      37 |          0 |
| PIROCLASTITI  |            14 |     0.3 |        40 |      36 |          0 |
| CINERITI      |            14 |     0.3 |        50 |      37 |          0 |
| TUFF (YNT)    |            14 |     0.3 |       100 |      27 |        0.5 |

As previously mentioned, since the loose grounds properties are quite similar to each other,  a  reference  succession  consisting  only  by  loose  grounds  and  Yellow  Neapolitan Tuff, can be defined; the table below summarizes their geotechnical parameters.

Tab.2-5. Physical and mechanical properties for loose soils and Tuff

| GROUND TYPE   |    d [kN/m 3 ] |    [-] |   E [MPa] |    [°] |   c' [MPa] |
|---------------|-----------------|---------|-----------|---------|------------|
| LOOSE SOILS   |              12 |     0.3 |        50 |      35 |          0 |
| TUFF (YNT)    |              14 |     0.3 |       100 |      27 |        0.5 |

Fig.2-7. Schematic stratigraphy

<!-- image -->

Engineering drawing

Fig.2-8. Stratigraphic profile within  Mergellina and Arco Mirelli stations

<!-- image -->

Engineering drawing

## 2.2.2. The used excavation technique

The loose sandy soil and the high groundwater level (-1 m a.m.s.l.), led to choose and EPB machine rather than a TBM, to carry on the tunnel digging operations. As a matter of fact, the operating system of the machine leads to solve many problems related among the others to the supporting face pressure, the presence of water in the machine and the volume loss, to be maintained below 0.5%.

Using an EPB machine not any supporting function is assigned to the cutterhead. The front stability is ensured by the pressure that a plastic ground mixture applies on the ground face.

Once  the  excavation  ground  have  been  loosened,  the  'cake'  (fluid  ground  and smoothing-agents  mixture)  in  front  of  the  machine  falls  through  the  the cutting wheel openings into the excavation chamber; uncontrolled penetrations of the soil in  it are  prevented  thanks  to  the  thrust  cylinders  forces  transmitted  from  the pressure bulkhead onto the soil. A state of equilibrium is reached when the soil in the excavation chamber cannot be compacted any further by the native earth and water  pressure.  Thus  the  face  stability  is  always  guaranteed  only  by  the  thrust cylinders pressure, transferred through the bulkhead on the mixed ground into the excavation  chamber.  Therefore  this  is  only  responsible  for  mixing  the  excavated ground inside and outside the excavation chamber.

The  excavated  material  is  removed  from  the excavation  chamber by  an  auger conveyor. The amount of removed material is controlled by the speed of the auger and  the  cross-section  of  the  opening  of  the  upper  auger  conveyor  driver.  The excavated material is conveyed on some belts to the so called reversible conveyor from which the transportation gantries  in the backup areas are loaded when the conveyor belt is put into reverse.

The lining  segments  of  the  tunnel  are  located  by  means  of  erectors  behind  the pressure  bulkhead  and  then  temporarily  bolted  in  place.  Mortar  is  continuously forced  into  the  remaining  gap  between  the  segments  'outer  side  and  the  soil, through injection openings in the tailskin or openings in the segments.

Fig.2-9. 1) Cutting wheel; 2) Excavation chamber; 3) Pressure bulkhead; 4) Thrust cylinder; 5) Auger conveyor; 6) Erectors; 7) Lining segments

<!-- image -->

Engineering drawing

As  the  tunnel  excavation  occurs  in  sandy  loose  soil,  with  no  any  self-sufficiency ability,  the  used  machine  is  equipped  of  particular  system  to  realize  mortar injections (maximum 4-6 bar) in between the final lining outer line and the soil.

Though a Slurry TBM machine using bentonite should be appropriate for the soil in point, an EPB machine has been preferred for the reasons below:

1. less material to be injected in the excavation chamber and to pull out
2. lower pressure to guarantee the front stability
3. better performance in the loose soil
4. less environmental impact
5. less expensive

Among  the  others,  some  more  reasons  strictly  related  to  the  use  of  bentonite rather that tenso-active products, led to choose the EPB instead of the Slurry TBM:

1. because of the high specific gravity the bentonite could easily penetrate in the grains of the sand, thus a lower shield pressure on the face and higher surface displacements occur
2. to mix the bentonite mud to the ground a large amount of water is required, thus a less safe working environment

3. the bentonite makes the excavated ground fluid for so long to complicate its transport to the landfill
4. using bentonite a more complex and cumbersome system is required.

Concluding, the main properties of the used machine are described below:

Tab.2-6. Excavation machine properties

| EPB                                        | EPB    |
|--------------------------------------------|--------|
| Cutter weal diameter                       | 8.10 m |
| Total length                               | 8.00 m |
| Maximum pressure in the excavation chamber | 3 bar  |
| Maximum thrust cylinder lengthening        | 2.00 m |
| Auger conveyor diameter                    | 900 mm |

## 2.2.3. The monitoring plan

As  the  tunnel  excavation  affects  a  very  urbanized  area,  a  complete  monitoring plan development has been required.

In  order  to  achieve  a  global  view  of  the  tunnelling  induced  effects  in  the surrounding environment, a number of monitoring instruments have been installed on preexisting buildings, into and on the ground surface and inside the final tunnel lining.

Ground and buildings deformations have been constantly controlled by mean of topographic  instruments  installed  into  and  on  the  ground  surface  and  on  the buildings faces overlooking Via Piedigrotta.

To obtain a comprehensive  view  of  the  tunneling induced  effects in the surrounding environment, since the tunnel line always located below the groundwater  level,  some  piezometers  have  been  installed  nearby  the  tunnel operating area as to monitor the induced groundwater variations.

Moreover,  some  strain-gages  have  been  installed  in  some  of  the  tunnel  lining segments to control the induced deformations and the internal stress variations.

According  to  the  monitoring  scheduled  instruments,  three  different  monitoring sections have been defined along the whole tunnel line:

1. topographic sections : with mainly topographic instruments
2. main geotechnical section : with both topographic instruments, inclinometers, piezometers and strain-gages in the tunnel lining
3. secondary  geotechnical  section :  the  same  as  the  previous  one,  with  no monitored tunnel lining segments.

For  each  installed  instrument,  the  frequency  of  the  measurements  is  differently defined  according  to  the  operations  site  in  progress  and  to  the  front  machine position in respect to the measuring section.

In the pages and in the tables below the monitoring sections are fully described together  with  the  scheduled  frequency  for  each  monitoring  instrument  (Tab.2-7Tab.2-11).

## TOPOGRAPHIC SECTIONS

They are made only by topographic instruments such as:

-  n° 7 topographic landmarks on the ground surface orthogonal to the tunnel.

The sections are about 50 m apart and the central landmark has to be installed on the  tunnel  axis.  If  necessary,  n°  5  landmarks  can  be  installed  when  the  section interferes with preexisting structures.

## MAIN GEOTECHNICAL SECTIONS

They  are  made  by  monitoring  instruments  installed  both  in  the  ground  surface surrounding the tunnel and in the tunnel lining segments. The used instruments:

-  n° 7 topographic landmarks on the ground surface orthogonal to the tunnel axis
-  n° 2 inclinometers out of the tunnel excavation area, from 2 to 5 m faraway from the outer tunnel lining, up to 10 m below the invert
-  n° 1 piezometer
-  n° 8 instrumented segments per lining ring

## SECONDARY GEOTECHNICAL SECTIONS

The instruments for this section are the same as the main geotechnical sections' ones except for the lining segments monitoring instruments.

Tab.2-7. Scheduled measurements frequency for the topographic instruments on the ground surface

| WORK IN PROGRESS                                                                                                                    | TUNNEL FACE RESPECT TO THE SECTION                                                                   | MEASURES FREQUENCY   |
|-------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------|----------------------|
|  Zero reading  2 measures/month (until the tunneling operations start)                                                            |  Zero reading  2 measures/month (until the tunneling operations start)                             | SETTING UP           |
|  -5Z0 < TF < -2Z0  -2Z 0 < TF < 2Z 0  2Z 0 < TF < 5Z 0  TF > 5Z 0  3 months after the tunnel face passed the measuring section |  1-2 measures/week  1-2 measures/day  1-2 measures/week  1-2 measures/month  1-2 measures/month | TUNNEL EXCAVATION    |

Tab.2-8. Scheduled measurements frequency for landmarks on buildings

| WORK IN PROGRESS SETTING UP  Zero reading  2 measures/month                                                                       | TUNNEL FACE RESPECT TO THE SECTION tunneling operations start)                             | MEASURES FREQUENCY (until the   |
|-------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------|---------------------------------|
|  -5Z0 < TF < -2Z0  -2Z 0 < TF < 2Z 0  2Z 0 < TF < 5Z 0  TF > 5Z 0  3 months after the tunnel face passed the measuring section |  2 measures/week  2 measures/day  2 measures/week  1 measures/month  1 measures/month | TUNNEL EXCAVATION               |

Tab.2-9. Fig. Scheduled piezometric measurements frequency

| WORK IN PROGRESS  Zero  1                                                                       | TUNNEL FACE RESPECT TO THE SECTION (until the tunneling operations start)                            | MEASURES FREQUENCY reading measures/month   |
|---------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------|---------------------------------------------|
| SETTING UP                                                                                        | SETTING UP                                                                                           | SETTING UP                                  |
|  -5Z0 < TF < -2Z0  -2Z 0 < TF < 2Z 0  2Z 0 < TF < 5Z 0  TF > 5Z 0  until the excavation ends |  1-2 measures/week  1-2 measures/day  1-2 measures/week  1-2 measures/month  1-2 measures/month | TUNNEL EXCAVATION                           |

Tab.2-10. Fig. Scheduled extensometer and inclinometers measurements frequency

| WORK IN PROGRESS SETTING UP                                                                                                         | TUNNEL FACE RESPECT TO THE SECTION tunneling operations start)                                       | MEASURES FREQUENCY the                   |
|-------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------|------------------------------------------|
|  Zero reading  1 measures/month (until                                                                                            |  Zero reading  1 measures/month (until                                                             |  Zero reading  1 measures/month (until |
|  -5Z0 < TF < -2Z0  -2Z 0 < TF < 2Z 0  2Z 0 < TF < 5Z 0  TF > 5Z 0  3 months after the tunnel face passed the measuring section |  1-2 measures/week  1-2 measures/day  1-2 measures/week  1-2 measures/month  1-2 measures/month | TUNNEL EXCAVATION                        |

Tab.2-11. Fig. Scheduled tunnel lining stress measurements frequency

| WORK IN PROGRESS                         | TUNNEL FACE RESPECT TO THE SECTION                                                                                           | MEASURES FREQUENCY                   |
|------------------------------------------|------------------------------------------------------------------------------------------------------------------------------|--------------------------------------|
| SETTING UP                               |  Instruments testing  Zero reading                                                                                         |  Instruments testing  Zero reading |
| AGING OF CONCRETE                        |  1 measure/6 hours  2 measures/day  during the first 20 days  until the concrete aging is finished                       |                                      |
|  1 measure/6 hours  2 measures/day  1 |  for the first 60 m next to the installed ring  until the measured deformation is stabilized  until the line is completed | SEGMENTS INSTALLATION measure/day    |

## 2.2.3.1. Installed monitoring instruments

## LANDMARKS ON THE GROUND SURFACE

N° 45 topographic sections, on average 10 m spaced, were installed on the ground surface along Via Piedigrotta, perpendicular to the tunnel axis. Each section is made at least by 5 landmarks, 5 m spaced, with the central one located at the tunnel axis.

Fig.2-10  show  an  example  of  the  topographic  landmarks  sections  location  along Via Piedigrotta while in Tab.2-12 their exact position is indicated.

Fig.2-10. Fig. Example of installed ground landmarks

<!-- image -->

Engineering drawing

Tab.2-12. Fig. Landmarks on the ground surface

| ID             | Z 0 [m]   |     ID | Z 0 [m]   | ID     | Z 0 [m]   | ID          | Z 0 [m]   | ID     | Z 0 [m]   | ID     | Z 0 [m]   | ID   |   Z 0 [m] |
|----------------|-----------|--------|-----------|--------|-----------|-------------|-----------|--------|-----------|--------|-----------|------|-----------|
| AT01 299.80    | AT06      | 385.90 | AT13      | 443.92 |           | AT19 503.93 | AT26      | 554.47 | AT33      | 623.80 | SP02      |      |    694.00 |
| SP01 316.67    | AT07      | 399.58 | AT14      | 451.31 | AT20      | 511.24      | AT27      | 563.02 | AT34      | 639.35 | AT40      |      |    701.64 |
| AT02 326.50    | AT08      | 407.70 | AT15      | 458.70 | AT21      | 518.83      | AT28      | 578.20 | AT35      | 646.56 | AT41      |      |    708.31 |
| AT03 339.30    | AT09      | 414.93 | AT16      | 466.01 | AT22      | 525.80      | AT29      | 584.98 | AT36      | 654.35 |           | AT42 |    727.71 |
| AT04 355.83    | AT10      | 421.94 | AT17      |        | 473.38    | AT23        | 533.02    | AT30   | 591.69    | AT37   | 668.28    |      |           |
| AT04bis 356.00 | AT11      | 429.19 |           | SC01   | 485.58    | AT24        | 542.09    | AT31   | 608.77    | AT38   | 685.81    |      |           |
| AT05 372.31    | AT12      | 436.44 |           | AT18   | 496.02    | AT25        | 545.67    | AT32   | 616.90    | AT39   | 683.30    |      |           |

## LANDMARKS ON BUILDINGS

To control the preexisting buildings tunneling induced deformations a number of landmarks have been installed on their facades.

29 buildings have been instrumented nearby the tunnel track, along Via Piedigrotta and Riviera di Chiaia.

The monitoring plan provided a landmark each 6/8 m for masonry and landmarks next to the pillars for the concrete buildings, depending on the accessibility of the structure.

In Tab.2-13 below, the monitored buildings together with the number of installed landmarks on them, are resumed.

Tab.2-13. Landmarks on buildings

| Address               |   Building n° |   Number of installed landmarks | Building n°   | Number of installed landmarks   |
|-----------------------|---------------|---------------------------------|---------------|---------------------------------|
| Via Piedigrotta       |             7 |                               5 | 57            | 3                               |
| Via Piedigrotta       |            11 |                              10 | 60            | 10                              |
| Via Piedigrotta       |            16 |                               4 | 63            | 14                              |
| Via Piedigrotta       |            19 |                               6 | 65            | 5                               |
| Via Piedigrotta       |            23 |                               9 | 67            | 3                               |
| Via Piedigrotta       |            30 |                               6 | 93            | 6                               |
| Via Piedigrotta       |            34 |                              12 | 96            | 3                               |
| Via Piedigrotta       |            54 |                               5 | 98            | 3                               |
| Riviera di Chiaia     |            23 |                              10 | 50            | 2                               |
| Riviera di Chiaia     |            33 |                               5 | 53            | 3                               |
| Riviera di Chiaia     |            36 |                               5 | 57            | 2                               |
| Riviera di Chiaia     |            44 |                               4 | 61            | 3                               |
| Riviera di Chiaia     |            48 |                               2 | 66            | 8                               |
| Largo Torretta        |            19 |                               9 | -             | -                               |
| P.za della Repubblica |             2 |                               5 | -             | -                               |
| Via C. Cucca          |             3 |                               5 | -             | -                               |

Fig.2-11. Example of landmarks on buildings

<!-- image -->

Engineering drawing

## 2.3. The  empirical  methods  for  prediction  of tunnelling induced displacements

In this section empirical formula will be used to predict tunnel induced displacements  along  Via  Piedigrotta  and  Riviera di  Chiaia,  where  the  worst combinations  of  factors,  such  as  cover  layer  thickness  and  buildings  to  tunnel distance appear. The analyzed stretch ends in Arco Mirelli station.

As  the  cover  layer  thickness  varies  from  12  m  to  18  m,  empirical  formula  have been applied for 7 different tunnel depths and buildings damage analysis has been carried on for 23 buildings.

As  better  explained  in  the Background section  of  this  work,  transversal  and longitudinal displacements curves result from K and VL, depending by cohesive or cohesionless soils and by the used excavation technique. For the case in question the  chosen  values  for  the  parameters  above  are  respectively  0.30  and  0.5%. Horizontal and vertical displacements in transversal and longitudinal directions are plotted in Fig.2-12 to Fig.2-15 for 12m up to 18 m cover layers thickness; Tab.2-14 resumes obtained results.

Fig.2-12. Transversal section: predicted vertical displacements (K = 0.30 - V L = 0.5%)

<!-- image -->

Line chart

Fig.2-13. Transversal section: predicted horizontal displacements (K = 0.30 - V L = 0.5%)

<!-- image -->

Line chart

Fig.2-14. Longitudinal section: predicted vertical displacements (K = 0.30 - V L = 0.5%)

<!-- image -->

Line chart

Fig.2-15. Longitudinal section: vertical displacements on maximum vertical settlements (K = 0.30 - V L = 0.5%)

<!-- image -->

Line chart

Tab.2-14. Main indications about displacements curves for different cover layers thickness

| K = 0.3 - V L = 0.5%   | K = 0.3 - V L = 0.5%   | K = 0.3 - V L = 0.5%                 | K = 0.3 - V L = 0.5%   | K = 0.3 - V L = 0.5%   | K = 0.3 - V L = 0.5%   |
|------------------------|------------------------|--------------------------------------|------------------------|------------------------|------------------------|
| H [m]                  | Z 0 [m]                | BUILDINGS                            | i [m]                  | w max [mm]             | U x,max [mm]           |
| 18                     | 22                     | RC.50 - RC.53 - RC.57 - RC.61        | 6.6                    | 15.52                  | 2.82                   |
| 17                     | 21                     | RC.40 - RC.48                        | 6.3                    | 16.26                  | 2.95                   |
| 16                     | 20                     | RC.22 - RC.36                        | 6.0                    | 17.07                  | 3.11                   |
| 15                     | 19                     | PG.19 - PG.2 - RC.23                 | 5.7                    | 17.97                  | 3.26                   |
| 14                     | 18                     | PG.11 - PG.7 - PG.93 - PG.96 - PG.98 | 5.4                    | 18.96                  | 3.43                   |
| 13                     | 17                     | PG.23 - PG.65 - PG.67 - PG.16        | 5.1                    | 20.07                  | 3.65                   |
| 12                     | 16                     | PG.63 - PG.30                        | 4.8                    | 21.32                  | 3.87                   |

On the base of calculated displacements, buildings damage analysis has been done to  define  the  level  of  damage  caused  by  predicted  displacements  all  along  the analyzed tunnel stretch. Figures below show results in the damage abacus; in most of  the  cases  buildings  belong  to  the  0  category  of  damage,  with  the  exception  of buildings 93, 96 and 98 along Via Piedigrotta belonging to the 1 st one respectively corresponding  to  the 'Negligible' and 'Very  slight' class  on  the  damage  abacus (after Boscardin &amp; Cording, 1989 and Burland, 1995). Fig.2-18 represents the plan of tunnelling induced damage.

Tab.2-15. Via Piedigrotta, Largo Torretta and Via C. Cucca: analysied buildings and related level of damage

| BUILDINGS       |   BUILDINGS | BUILDINGS   | BUILDINGS   |   L/H |    h |    /L |   CLASS OF DAMAGE (after Boscardin & Cording, and Burland, 1995) | 1989)       |
|-----------------|-------------|-------------|-------------|-------|-------|--------|------------------------------------------------------------------|-------------|
| VIA PIEDIGROTTA |           1 | PG.63       | Masonry     |   1.7 | 0.013 |  0.020 |                                                                0 |             |
| VIA PIEDIGROTTA |           1 | PG.63       | Masonry     |   2.2 | 0.011 |  0.018 |                                                                0 | Negligible  |
| VIA PIEDIGROTTA |           1 | PG.63       | Masonry     |   4.0 | 0.013 |  0.012 |                                                                0 |             |
| VIA PIEDIGROTTA |           2 | PG.30       | Masonry     |   0.8 | 0.013 |  0.023 |                                                                0 | Negligible  |
| VIA PIEDIGROTTA |           3 | PG.23       | Masonry     |   0.5 | 0.029 |  0.022 |                                                                0 | Negligible  |
| VIA PIEDIGROTTA |           3 | PG.23       | Masonry     |   0.9 | 0.016 |  0.022 |                                                                0 | Negligible  |
| VIA PIEDIGROTTA |           3 | PG.23       | Masonry     |   1.2 | 0.011 |  0.019 |                                                                0 | Negligible  |
| VIA PIEDIGROTTA |           4 | PG.65       | Masonry     |   0.9 | 0.026 |  0.022 |                                                                0 | Negligible  |
| VIA PIEDIGROTTA |           5 | PG.67       | Concrete    |   1.4 | 0.026 |  0.014 |                                                                0 | Negligible  |
| VIA PIEDIGROTTA |           6 | PG.16       | Masonry     |   0.4 | 0.025 |  0.020 |                                                                0 | Negligible  |
| VIA PIEDIGROTTA |           6 | PG.16       | Masonry     |   0.7 | 0.026 |  0.023 |                                                                0 | Negligible  |
| VIA PIEDIGROTTA |           6 | PG.16       | Masonry     |   0.8 | 0.026 |  0.022 |                                                                0 | Negligible  |
| VIA PIEDIGROTTA |           7 | PG.11       | Concrete    |   0.3 | 0.033 |  0.017 |                                                                0 | Negligible  |
| VIA PIEDIGROTTA |           8 | PG.7        | Masonry     |   0.7 | 0.037 |  0.014 |                                                                0 | Negligible  |
| VIA PIEDIGROTTA |           9 | PG.93       | Masonry     |   1.0 | 0.045 |  0.022 |                                                                1 | Very slight |
| VIA PIEDIGROTTA |          10 | PG.96       | Masonry     |   1.2 | 0.045 |  0.022 |                                                                1 | Negligible  |
| VIA PIEDIGROTTA |          11 | PG.98       | Masonry     |   1.2 | 0.045 |  0.022 |                                                                1 | Very slight |
| LARGO TORRETTA  |          12 | LT.19       | Masonry     |   1.2 | 0.029 |  0.017 |                                                                0 | Negligible  |
| VIA C. CUCCA    |          13 | CC.3        | Masonry     |   1.4 | 0.013 |  0.020 |                                                                0 | Negligible  |

Tab.2-16. Riviera di Chiaia: analysied buildings and related level of damage

| BUILDINGS   | BUILDINGS   | BUILDINGS   | L/H     |  h         |  /L        |    /L CLASS OF DAMAGE (after Boscardin & Cording, 1989) and Burland, 1995) |  /L CLASS OF DAMAGE (after Boscardin & Cording, 1989) and Burland, 1995)   |
|-------------|-------------|-------------|---------|-------------|-------------|-----------------------------------------------------------------------------|-----------------------------------------------------------------------------|
| 1 4         | RC.23       | Masonry     | 0.7     | 0.031       | 0.014       |                                                                           0 | Negligible                                                                  |
| 3           | RC.33       | Masonry     | 2.3     | 0.015       | 0.020       |                                                                           0 | Negligible                                                                  |
| 3           | RC.33       | Masonry     | 3.5     | 0.015       | 0.018       |                                                                           0 | Negligible                                                                  |
| 3           | RC.33       | Masonry     | 4.0     | 0.015       | 0.017       |                                                                           0 | Negligible                                                                  |
|             | RC.36       | Masonry     | 2.1     | 0.012       | 0.019       |                                                                           0 | Negligible                                                                  |
|             |             | Concrete    | 0.5     | 0.021       | 0.016       |                                                                           0 | Negligible                                                                  |
|             | RC.48       | Concrete    | 0.8 1.1 | 0.023 0.023 | 0.019 0.018 |                                                                           0 | Negligible                                                                  |
| CHIAIA 5    | RC.40-44    | Masonry     | 2.9     | 0.008       | 0.016       |                                                                           0 | Negligible                                                                  |
| CHIAIA 5    | RC.40-44    | Masonry     | 0.0     | 0.008       | 0.026       |                                                                           0 | Negligible                                                                  |
| CHIAIA 5    | RC.40-44    | Masonry     | 0.0     | 0.008       | 0.081       |                                                                           0 | Negligible                                                                  |
| CHIAIA 5    | RC.50       | Masonry     | 2.4     | 0.010       | 0.017       |                                                                           0 | Negligible                                                                  |
| 6           | RC.50       | Masonry     | 2.7     | 0.010       | 0.016       |                                                                           0 | Negligible                                                                  |
| CHIAIA 5    | RC.50       | Masonry     | 3.0     | 0.010       | 0.016       |                                                                           0 | Negligible                                                                  |
| CHIAIA 5    | RC.53       | Masonry     | 2.7     | 0.007       | 0.015       |                                                                           0 | Negligible                                                                  |
| 7           | RC.53       | Masonry     | 3.0     | 0.010       | 0.014       |                                                                           0 | Negligible                                                                  |
| CHIAIA 5    | RC.53       | Masonry     | 3.4     | 0.010       | 0.013       |                                                                           0 | Negligible                                                                  |
| 8           | RC.57       | Masonry     | 0.9     | 0.020       | 0.014       |                                                                           0 | Negligible                                                                  |
| 8           | RC.57       | Masonry     | 1.6     | 0.010       | 0.017       |                                                                           0 | Negligible                                                                  |
| 8           | RC.57       | Masonry     | 1.6     | 0.010       | 0.017       |                                                                           0 | Negligible                                                                  |
| 9           | RC.61       | Masonry     | 2.2     | 0.010       | 0.016       |                                                                           0 | Negligible                                                                  |
| 9           | RC.61       | Masonry     | 2.4     | 0.010       | 0.016       |                                                                           0 | Negligible                                                                  |
| 9           | RC.61       | Masonry     | 2.6     | 0.010       | 0.015       |                                                                           0 | Negligible                                                                  |

Fig.2-16. Damage abacus for concrete buildings (PG.11 and PG.67 along Via Piedigrotta and RC.48 along Riviera di Chiaia)

<!-- image -->

Line chart

<!-- image -->

Line chart

<!-- image -->

Line chart

Fig.2-17. Damage abacus for brick buildings

<!-- image -->

Line chart

Fig.2-18. Damage plan

<!-- image -->

Geographical map

## Chapter 3. LINE 6: ANALYSIS OF MONITORING DATA

## 3.1. Introduction

As  explained  in  Chapter  2,  a  number  of  monitoring  instruments  have  been installed  all  along  the  Line  6  track,  to  control  the  tunnelling  induced  effects (buildings and ground displacements, groundwater variations and lining stresses); it follows that several data, from topographic landmarks on the ground surface and on  preexisting  buildings,  piezometers,  extensometers-inclinometers  and  straingages in the tunnel lining segments, have been collected.

In the following pages the data coming from the installed topographic instruments will  be  discuss  with  the  aim  of  overseeing  the  tunnelling  effects  on  preexisting buildings and consequently their induced level of damage.

## 3.2. Tunnel excavation

Before  the  Line  6  tunnelling  operations  started,  several  yard  operations  took place: the old stuck TBM machine was disassembled and pulled out and the new EPB machine was carried to the yard and then assembled. These operations took about  three  months;  they  started  in  July  2009,  when  the  old  TBM  started  to  be disassembled and finished in September 2009 when the new EPB was assembled.

The  pictures  below  show  the  above  mentioned  operations,  preparatory  to  the tunnel excavation process.

Fig.3-1. Disassembly the old TBM machine

<!-- image -->

Photograph

Fig.3-2. New front with spritz-beton

<!-- image -->

Photograph

Fig.3-3. Carrying and casting the frontal piece of the cutting head

<!-- image -->

Photograph

Fig.3-4. Carrying and casting the cutting weal

<!-- image -->

Photograph

Fig.3-5. Assembled cutting head and cutting wheel

<!-- image -->

Photograph

Once  the  above  mentioned  operations  finished,  on  the  April  7 th ,  2009  the tunnelling operations started from km (0 + 292.90). Basing on the last update on August the 31 st 2010, the machine is at km (0 + 716.13): 423 m of tunnel have been excavated and 250 lining segments have been installed.

The detailed tunnel production day by day is resumed in the Appendix and  it  is represented in Fig.3-6, Fig.3-7 and Fig.3-8.

Fig.3-6. Progressive tunnel production

<!-- image -->

Line chart

Fig.3-7. Tunnel production (a) and tunnel production velocity (b)

<!-- image -->

Bar chart

From the graphs in Fig.3-7 an average of 85 m/month for the excavated tunnel and  of  50  segments/month  for  the  installed  final  lining  can  be  determined,  with respective velocities of 3 m/day and 2 segments/day.

In  terms  of  excavated  distance,  the  best  production  has  been  recorded  in  May, when 132 m of tunnel were excavated and 78 lining segments were installed. On the  opposite  side,  the  worst  production  was  realized  in  June  because  of  several technical problems which slowed down the excavation procedure;  among these a remarkable water inflow from the front observed between May the 31 st and June the  18 th and  the  opening  of  a  hole  on  June  the  28 th in  the  ground  nearby  Largo Torretta,  probably  related  to  the  next  discovery  of  gas  pipes  in  that  area  and immediately filled with 140 mc of grout.

As the graph in Fig.3-6 shows, the tunnel production in July stopped for about 20 days because of the need to repair the roadway and the leakage of mud in the road. Nevertheless since the machine restarted to excavate, the recorded production has been  quite  significant,  as  the  tunnel  velocity  shows  in  Fig.3-7.  However  the  best production  was  in  August  when  of  93  m  of  tunnel  were  excavated  and  55  lining segments were installed with respective velocity of 12 m/day and 7 segments/day.

In Fig.3-8 the detailed tunnel excavation velocity (m/day) is separately represented per month.

Fig.3-8. Excavation velocity: (a) April, (b) May, (c) June, (d) July, (e) August

<!-- image -->

Bar chart

## 3.3. Field monitoring data

In the following pages, collected data from monitoring instruments installed both on the ground surface and on preexisting buildings 'facades will be discuss.

The observed effects in terms of measured displacements are strictly related to the EPB performance (excavation velocity and/or applied pressures and forces); in this  way  the  machine  parameters  have  been  continually  supervised  checking  the applied pressures and torque moment required for the machine advance.

## 3.3.1. Excavation machine performances

Thanks  to  a  number  of  sensors  on  the  EPB  machine,  measurements  of  front pressure  (FP),  grouting  pressure  (GP)  and  torque  moments  (TM)  applied  for advancing with the tunnel excavation were  collected. Tab.3-1 resumes  the measured minimum and maximum values for each parameter while Fig.3-9 shows their trend versus the tunnel advance production. As the figure depicts, the front pressure is linearly increasing with the tunnel advance, whereas both the grouting pressure  and  the  torque  moments  have  a  non  uniform  trend.  For  the  grouting pressure peak values have been recorded between June the 18 th and July the 28 th when electrical problems with the cutterhead and water inflow from the front have been noticed. In the same interval an instantaneous 50% reduction of the torque moments has been measured.

Tab.3-1. Minimum and maximum values for applied front pressure, grouting pressure and torque moments

| EPB parameters         | Minimum value   | Maximum value   |
|------------------------|-----------------|-----------------|
| Front Pressure (FP)    | 110 kPa         | 295 kPa         |
| Grouting Pressure (GP) | 56 kPa          | 574 kPa         |
| Torque Moments (TM)    | 2824 kNm        | 9631 kNm        |

<!-- image -->

Line chart

FP

GP

TM

Fig.3-9. EPB performances: front pressure (FP), grouting pressure (GP) and torque moments (TM)

## 3.3.2. Landmarks on the ground surface

Basing  on  the  monitoring  data  updated  up  to  August  the  31 st ,  45  landmarks sections have been installed on the roadway, above the tunnel track.

Each  section  is  made  by  3  to  5  landmarks  with  the  central  one  installed  at  the tunnel axis. Detailed indications about the identification name, the position and the number  of  landmarks  for  each  monitoring  sections  are  resumed  in  Tab.2-12 (Chapter 2).

In the monitoring plan the landmarks sections are represented together with the tunnel track.

In  Tab.3-2  informations  about  the  zero  and  the  last  reading  of  each  measuring sections are resumed. The table shows that for landmarks sections AT01 to AT30, in the first 300 m from the tunnel starting point, measuring data have been collected for  more  than  one  month;  the  zero  readings  have  been  recorded  between April/May  and  the  last  readings  at  the  end  of  July,  when  330  m  of  tunnel  were excavated  and  the  tunnel  face  was  at  km  (0  +  622.73).  Contrariwise  for  sections AT30 up to AT42 less than one month of recorded measures was observed: zero readings were recorded between the end of July and August and the last measures at the end of August (saving sections AT31 and AT32 for which only few data were collected being the last measures dated at August the 4 th ).

| ID             | ZERO reading   | LAST reading   | ID        | ZERO reading   | LAST reading   | ID        | ZERO reading   | LAST reading   |
|----------------|----------------|----------------|-----------|----------------|----------------|-----------|----------------|----------------|
| AT01 30-Mar-10 | 27-Jul-10      | AT09           | 11-May-10 | 27-Jul-10      | SC01           | 24-May-10 |                | 27-Jul-10      |
| SP01 7-Apr-10  | 27-Jul-10      | AT10           |           | 12-May-10      | 27-Jul-10      | AT18      | 25-May-10      | 27-Jul-10      |
| AT02 9-Apr-10  | 27-Jul-10      | AT11           | 14-May-10 |                | 27-Jul-10      | AT19      | 26-May-10      | 27-Jul-10      |
| AT03 15-Apr-10 | 27-Jul-10      | AT12           |           | 14-May-10      | 27-Jul-10      | AT20      | 26-May-10      | 27-Jul-10      |
| AT04 3-May-10  | 27-Jul-10      | AT13           |           | 17-May-10      | 27-Jul-10      | AT21      | 26-May-10      | 27-Jul-10      |
| AT05 30-Apr-10 | 27-Jul-10      | AT14           |           | 17-May-10      | 27-Jul-10      | AT22      | 31-May-10      | 27-Jul-10      |
| AT06 5-May-10  | 27-Jul-10      | AT15           |           | 19-May-10      | 27-Jul-10      | AT23      | 31-May-10      | 27-Jul-10      |
| AT07 5-May-10  | 27-Jul-10      | AT16           |           | 19-May-10      | 27-Jul-10      | AT24      | 11-Jun-10      | 27-Jul-10      |
| AT08 11-May-10 | 27-Jul-10      | AT17           |           | 19-May-10      | 27-Jul-10      | AT25      | 15-Jun-10      | 27-Jul-10      |

Tab.3-2. Measures zero and last readings

| ID   | ZERO reading        | LAST reading   | ID        | ZERO reading   | LAST reading   |
|------|---------------------|----------------|-----------|----------------|----------------|
| AT26 | 17-Jun-10 28-Jul-10 | AT35           | 30-Jul-10 | 24-Aug-10      |                |
| AT27 | 21-Jun-10           | 29-Jul-10      | AT36      | 2-Aug-10       | 26-Aug-10      |
| AT28 | 21-Jun-10           | 30-Jul-10      | AT37      | 6-Aug-10       | 26-Aug-10      |
| AT29 | 21-Jun-10           | 30-Jul-10      | AT38      | 23-Aug-10      | 27-Aug-10      |
| AT30 | 21-Jun-10           | 2-Aug-10       | AT39      | 23-Aug-10      | 31-Aug-10      |
| AT31 | 28-Jul-10           | 4-Aug-10       | SP01      | 24-Aug-10      | 31-Aug-10      |
| AT32 | 29-Jul-10           | 4-Aug-10       | AT40      | 25-Aug-10      | 31-Aug-10      |
| AT33 | 29-Jul-10           | 23-Aug-10      | AT41      | 27-Aug-10      | 31-Aug-10      |
| AT34 | 29-Jul-10           | 24-Aug-10      | AT42      | 30-Aug-10      | 31-Aug-10      |

Referring  to  the  design  measurements  frequency  for  the  roadway  landmarks,  it has been observed that not for all the landmark sections the scheduled frequency has been respected. In many cases the landmarks readings started just before the tunnel  face  crossed  the  measuring  section,  preventing  to  record  data  when  the tunnel face is at distance 2Z0 before the section (when the recording frequency was supposed to be  equal  to  1-2  measures/day  - cfr .  Tab.  2-7)  and  so  to  completely observe the advancing tunnel effects. In some cases, similar problems in respecting the designed measures frequency have been observed even in the range (2Z0 - 5Z0) of  tunnel-section  distance,  when  1-2  measures/week  have  been  planned  to  be recorded. As matter of fact, after the tunnel passed distance 2Z0 from the sections, for sections AT01 up to AT21 the measures frequency has been respected whereas for AT22 up to AT30 sections not any data was collected. Observing how for the first 24  sections  (AT01  -  AT22)  the  maximum  settlements  have  been  measured  even beyond the distance 2Z0 between the tunnel face and the sections, doubts about the settlements reached their maximum value for sections AT22 to AT30 are then reasonable.

Fig.3-10 and Fig.3-11 show informations about the maximum measured displacements  measured  for  each  section,  the  related  distance  between  the sections  and  the  tunnel  face  location  and  the  time,  as  number  of  days  after  the tunnel underpassed the sections. The same informations are resumed in Tab.3-3.

Looking at the graphs of Fig.3-10, three different zones can be indentified:

-  zone A: sections from AT01 (km 0 + 299.8) to AT09 (km 0 + 414.9)
-  zone B: sections from AT10 (km 0 + 429.2) to AT30 (km 0 + 591.7)
-  zone C: sections from AT31 (km 0 + 608.8) to AT42 (km 0 + 727.7).

Zone  A  includes  sections  from  AT01  to  AT09  installed  along  Via  Piedigrotta between the tunnel starting point and Piazza Eritrea. They measured the maximum settlements, reached at the maximum distance (compared to the other two zones) between the tunnel face and the sections (Fig.3-10\_ b ). All sections measured from 10 mm up to 15 mm settlements saving section AT04 unreasonably measuring 42 mm displacements, sections AT01 and SP01 respectively 6 and 23 m away from the tunnel starting point, which probably did not experience their maximum displacements  since  they  didn't  suffer  the  tunnelling  effects  for  the  whole  2Z0 meters  before  them.  A  part  of  these  three  sections  the  average  displacement  in zone A is about 13 mm while the maximum is 15 mm measured by section AT08 (Fig.3-10\_ a ). As Fig.3-10\_ b and Fig.3-10\_ c show, the maximum displacements have been measured mostly within the first 20 days (except for sections AT01 and AT04 whose  displacements  increased  until  66  and  46  days  after  tunnel  underpassed them)  and  between  50  m  and  100  m  after  the  tunnel  face  crossed  the  sections (saving section AT01 which measured the maximum displacement 236 m after the tunnel underpassed it), farther than distance 2Z0 inside which, basing on the design monitoring plan, the maximum settlement was supposed to be reached.

Zone B including sections from AT10 to AT30 features lower  maximum displacements  (on  average  6  mm)  reached  on  average  13  days  after  the  tunnel underpassed the sections, and shorter distances between the tunnel face and the sections related to the measured maximum displacements (about 38 m, similar to the expected 2Z0).

Zone  C  including  sections  from  AT31  to  AT42,  features  the  smallest  maximum displacements  (on  average  3  mm)  reached  4  days  and  18  m  after  the  tunnel underpassed them. Basing on the last update on August the 31 st when the tunnel face  was  at  km  (0  +  709.00),  it  could  be  reasonable  to  think  that  the  maximum displacements  didn't  have  time  to  totally  develop  for  some  of  those  sections, because  of  the  short  distance  between  some  measuring  sections  and  the  last updated tunnel face location: as matter of fact, the tunnel face on August the 31 st is located not more than 7 m beyond sections SC01, AT40, AT41 and AT42.

Synthesizing, looking at the face locations related to the maximum displacements than the measuring sections locations (Fig.3-10\_ b ),  in  zones  B  and  C,  for  sections AT10 up to AT42, the measured maximum displacements is always reached within 50  m  after  the  tunnel  face  underpassed  the  sections  (on  average  30  m),  saving section AT17 measuring the maximum displacements 112 m away the tunnel face (Fig.3-11\_ a ). Moreover,  looking  at Fig.3-10\_ c it  is  clear  how  the  maximum displacements  are  always  reached  within  30  days  (on  average  10  days)  after  the tunnel face underpassed the sections, saving sections AT01 and AT04 (zone A) and AT17 (zone  B)  whose  displacements  increased  until  66,  46  and  67  days  after  the tunnel  underpassed  them.  The  same  information  is  represented  in  Fig.3-11\_ b showing how in most of the cases the maximum displacements are reached within 20 days after the tunnel passed the sections.

Fig.3-10. Landmarks wmax (a), Landmarks T(wmax) (b), Landmarks Df-s (wmax) (c)

<!-- image -->

Scatter plot

Fig.3-11. Landmarks wmax - Df-s (wmax) (a), Landmarks wmax - T(w max ) (b)

<!-- image -->

Scatter plot

In  Fig.3-10  displacement  measured  by  section  AT24  was  deleted  since  it  can  be easily related to a particular event occurred on June the 28 th when a hole in Largo Torretta appeared. This singular event leads to about 62 mm settlements measured on the ground surface as Tab.3-3 reports and Fig.3-12 shows.

Fig.3-12. Vertical displacements measure by landmarks sections

<!-- image -->

Line chart

| ID          |   w max [mm] |   D f-s (w max ) [m] | T(w max ) [days]   |     ID |   w max [mm] |   D f-s (w max ) [m] | T(w max ) [days]   |     ID |   w max [mm] |   D f-s (w max ) [m] | T(w max ) [days]   |
|-------------|--------------|----------------------|--------------------|--------|--------------|----------------------|--------------------|--------|--------------|----------------------|--------------------|
| -5.60       |          236 |                   66 | AT09               | -13.90 |           82 |                   16 | SC01               | -10.10 |           32 |                   17 | AT01               |
| SP01 -7.00  |           63 |                   13 | AT10               | -10.50 |           36 |                    6 | AT18               |  -6.70 |           35 |                    4 |                    |
| AT02 -10.40 |          106 |                   22 | AT11               |  -2.40 |           29 |                    4 | AT19               |  -5.40 |           39 |                   20 |                    |
| AT03 -12.90 |           93 |                   17 | AT12               |  -5.00 |           30 |                    2 | AT20               |  -3.60 |           31 |                   15 |                    |
| -42.40      |          180 |                   46 | AT13               |  -7.70 |           56 |                   14 | AT21               |  -3.20 |           24 |                   12 | AT04               |
| AT05 -12.60 |           60 |                   10 | AT14               |  -6.70 |           48 |                   13 | AT22               |  -1.60 |           22 |                   13 |                    |
| AT06 -12.50 |           60 |                   12 | AT15               |  -4.60 |           42 |                   13 | AT23               |  -2.10 |           14 |                   10 |                    |
| AT07 -12.60 |           97 |                   18 | AT16               |  -7.70 |           35 |                   13 | AT24               | -62.30 |            6 |                    6 |                    |
| AT08 -14.80 |           50 |                    7 | AT17               | -10.50 |          112 |                   67 | AT25               | -12.20 |           40 |                   28 |                    |

Tab.3-3. Maximum displacements of monitoring sections

| ID         |   w max [mm] |   D f-s (w max ) [m] | T(w max ) [days]   |    ID |   w max [mm] |   D f-s (w max ) [m] | T(w max ) [days]   |
|------------|--------------|----------------------|--------------------|-------|--------------|----------------------|--------------------|
| -8.50      |           55 |                    6 | AT35               | -4.10 |           17 |                    2 | AT26               |
| -2.90      |           46 |                    5 | AT36               | -5.00 |            9 |                    2 | AT27               |
| AT28 -1.20 |           48 |                    4 | AT37               | -1.60 |           33 |                    3 |                    |
| -1.70      |           41 |                    4 | AT38               | -3.10 |           23 |                    3 | AT29               |
| -3.30      |           17 |                    1 | AT39               | -2.50 |           26 |                    7 | AT30               |
| -4.40      |           17 |                    2 | SP02               | -3.40 |           15 |                    3 | AT31               |
| -4.00      |            9 |                    1 | AT40               | -1.20 |            7 |                    6 | AT32               |
| -5.00      |           10 |                    3 | AT41               | -0.80 |           -1 |                    3 | AT33               |
| -4.90      |           24 |                    3 | AT42               | -0.60 |          -19 |                    3 | AT34               |

Graphs  in  Fig.3-13  show  the  transversal  deformed  shapes  obtained  by  ground landmarks measurements concerning the initial reading (referred to the tunnelling starting  operations  on  April  the  7 th ),  the  maximum  settlement  and  last  recorded measure.  Looking  at  the  maximum  measured  settlement,  the  measuring  sections can  be  collected  into  three  main  groups  (Tab.3-4),  together  with  two  different singular special cases (sections AT04 and AT24, measuring remarkable settlement if compared  with  the  others  sections).  Looking  at  the  collected  data  of  face  and grouting pressure the decreasing maximum settlements along Via Piedigrotta, going to  Municpio  Station,  could  be  easily  related  to  the  increasing  applied  pressures (Fig.3-18 and Fig.3-19).

Fig.3-14 and Fig.3-15 show the transversal and longitudinal displacements curves for the three indentified groups whereas Fig.3-17 shows the maximum longitudinal settlements contour.

Tab.3-4. Maximum displacements of monitoring sections

| GROUP          | ID          | ID           | w max [mm]   |
|----------------|-------------|--------------|--------------|
| 1              | AT01 - SP01 | (zone A)     |              |
| 1              | AT12 - AT16 | (zone B)     |              |
| 1              | AT18 - AT19 | (zone B)     | 5 ÷ 8        |
| 1              | AT26        | (zone B)     |              |
| 2              | AT02 -AT10  | (zone A)     |              |
| 2              | AT17        | (zone B)     |              |
| 2              | AT25        | (zone B)     | 8 ÷ 14       |
| 2              | SC01        | (zone B)     |              |
| 3              | AT11        | (zone B)     |              |
| 3              | AT20 - AT23 | (zone B)     | ≤ 5          |
| 3              | AT27 - AT42 | (zone B - C) |              |
| SINGULAR CASES | AT04        | (zone A)     | 42.40        |
| SINGULAR CASES | AT24        | (zone B)     | 62.30        |

<!-- image -->

Line chart

<!-- image -->

Line chart

<!-- image -->

Line chart

<!-- image -->

Line chart

Fig.3-13. Topographic landmarks on the ground surface: measured deformed shapes

<!-- image -->

Box plot

Fig.3-14. Group 1: Transversal (a) and longitudinal (b) displacements curves: w max = 5÷8 m

<!-- image -->

Scatter plot

Fig.3-15. Group 2: Transversal (a)and longitudinal (b) displacements curves: wmax = 8÷14 mm

<!-- image -->

Scatter plot

Fig.3-16. Group 3: Transversal (a)and longitudinal (b) displacements curves: wmax ≤ 5 mm

<!-- image -->

Engineering drawing

Fig.3-17. Ground surface maximum settlements longitudinal contour

<!-- image -->

Line chart

Fig.3-18. Measured front pressure

<!-- image -->

Bar chart

Fig.3-19. Measured grouting pressure

<!-- image -->

Bar chart

Looking at the measured displacements in the longitudinal direction at the tunnel axis, Fig.3-20 shows their trend with the tunnel-section distance. Excluding sections not  reaching  the  maximum  displacements  because  too  close  to  the  tunnel  face (zone C), Fig.3-21 shows the percentage of maximum displacements reached at the tunnel front and at the passage of the shield tail (two times the tunnel depth from the sections). The average values are respectively 22% and 80%, according to the Craig  &amp;  Muir  Wood  (1978)  indications  for  sand  below  the  water  table  (Chapter 1\_Tab.1.1).

Fig.3-20. Settlements trend with the tunnel-section distance

<!-- image -->

Scatter plot

Fig.3-21. Percentage of maximum settlements reached at the tunnel face and 2Z0 away from it

<!-- image -->

Scatter plot

## 3.3.3. Landmarks on buildings

As  described  in  Chapter  2,  29  buildings  to  the  tunnel  track  side  all  along  Via Piedigrotta,  Riviera di Chiaia, Largo Torretta, Piazza Repubblica and Via C. Cucca, have been instrumented with landmarks on their facades.  In the table below the number  of  landmarks  for  each  building  are  related  and  in  the  following  pages, collected monitoring data up the August the 31 st will be discuss.

Tab.3-6 resumes monitored buildings main features (when available) such as brick work or concrete building, length, height, number of floors and foundations depth.

Basing  on  the  last  monitoring  update  on  August  the  31 st ,  Tab.3-7  and  Tab.3-8 relate informations about the zero and the last reading for each building and their maximum measured settlements.

Tab.3-5. Landmarks on buildings

| Address               |   Building n° |   Number of Installed landmarks | Building n°   | Number of Installed landmarks   |
|-----------------------|---------------|---------------------------------|---------------|---------------------------------|
| Via Piedigrotta       |             7 |                               5 | 57            | 3                               |
| Via Piedigrotta       |            11 |                              10 | 60            | 10                              |
| Via Piedigrotta       |            16 |                               4 | 63            | 14                              |
| Via Piedigrotta       |            19 |                               6 | 65            | 5                               |
| Via Piedigrotta       |            23 |                               9 | 67            | 3                               |
| Via Piedigrotta       |            30 |                               6 | 93            | 6                               |
| Via Piedigrotta       |            34 |                              12 | 96            | 3                               |
| Via Piedigrotta       |            54 |                               5 | 98            | 3                               |
| di Chiaia             |            23 |                              10 | 50            | 2                               |
| di Chiaia             |            33 |                               5 | 53            | 3                               |
| di Chiaia             |            36 |                               5 | 57            | 2                               |
| di Chiaia             |            44 |                               4 | 61            | 3                               |
| di Chiaia             |            48 |                               2 | 66            | 8                               |
| Largo Torretta        |            19 |                               9 | -             | -                               |
| P.za della Repubblica |             2 |                               5 | -             | -                               |
| Via C. Cucca          |             3 |                               5 | -             | -                               |

In  Fig.3-22  the  buildings  'maximum  settlements  are  related  to  the  distance between  the  tunnel  face  and  the  building  landmark  measuring  it;  the  maximum measured  displacements  is  about  8  mm  for  building  n°23  in  Riviera  di  Chiaia, reached  when  the  tunnel  was  about  46  m  beyond  it  (Tab.3-7  and  Tab.3-8).  The same  figure  shows  the  maximum  settlements  reached  mostly  within  100  meters between  the  tunnel  face  and  the  buildings,  saving  building  civ.60  along  Via Piedigrotta reaching its maximum displacement 145 m after the tunnel underpassed it. Fig.3-23 and Fig.3-24 show the landmarks displacements with the relative tunnel section  distance  (the  black  line  concerns  the  landmark  measuring  the  maximum settlement for each  building)  and  the  buildings  deformed  shape  when  the maximum displacements was reached, as indicated in Tab.3-7 and Tab.3-8.

Fig.3-25 shows monitored buildings maximum displacements longitudinal contour. The measured settlements are approximately 5 mm, always lower than the ground surface  ones  and  almost  uniform  all  along  the  tunnel  track,  but  with  the  same settlements decrease as shown by landmarks on ground surface, nearness buildings 93, 96, 98, 11 and 7 next to Piazza Eritrea (Fig.3-26).

Tab.3-6. Buildings main features

| BUILDINGS ID      | BUILDINGS ID   | FLOORS [N°]   | MATERIAL   | FOUDATION         | FOUDATION DEPTH [m]   |   LENGTH [m] |   HEIGHT [m] |
|-------------------|----------------|---------------|------------|-------------------|-----------------------|--------------|--------------|
| VIA PIEDIGROTTA   | 34             | 9+2           | Concrete   | Piles             | -7                    |         36.6 |         32.5 |
| VIA PIEDIGROTTA   | 30             | 6             | Masonry    | Masonry           | -5                    |           30 |           25 |
| VIA PIEDIGROTTA   | 23-26          | 5             | Masonry    | Masonry           | -6                    |           43 |           25 |
| VIA PIEDIGROTTA   | 16             | 6             | Masonry    | Masonry           | -2                    |           15 |           25 |
| VIA PIEDIGROTTA   | 11             | 8             | Concrete   | Piles             | -3                    |           38 |           32 |
| VIA PIEDIGROTTA   | 10             | 1             | Masonry    | Masonry           | -                     |            9 |            8 |
| VIA PIEDIGROTTA   | 7              | 2             | Masonry    | Masonry           | -5                    |           20 |         10.5 |
| VIA PIEDIGROTTA   | 19             | 3             | Masonry    | -                 | -                     |           22 |           14 |
| VIA PIEDIGROTTA   | 60             | 3             | Masonry    | Masonry           | -5                    |           16 |           15 |
| VIA PIEDIGROTTA   | 63             | 3             | Masonry    | Masonry           | -                     |           51 |           16 |
| VIA PIEDIGROTTA   | 65             | 4             | Masonry    | Masonry           | -                     |           20 |           15 |
| VIA PIEDIGROTTA   | 67             | 11            | Concrete   | Piles             | -                     |           31 |           37 |
| VIA PIEDIGROTTA   | 90 - 93        | 4             | Masonry    | Masonry           | -2                    |           13 |           19 |
| VIA PIEDIGROTTA   | 96 - 101       | 4             | Masonry    | Arch - Wood Steel | -2                    |           26 |           12 |
| RIVIERA DI CHIAIA | 23             | 4             | Masonry    | Masonry           | -                     |         32.6 |           12 |
| RIVIERA DI CHIAIA | 33             | 3             | Masonry    | Masonry           | -2                    |         27.7 |            9 |
| RIVIERA DI CHIAIA | 36             | 4             | Masonry    | Masonry           | -2                    |           33 |           12 |
| RIVIERA DI CHIAIA | 40 - 44        | 4             | Masonry    | Masonry           | -2                    |         31.5 |           12 |
| RIVIERA DI CHIAIA | 48             | 8             | Concrete   | Piles             | -4                    |         18.8 |           24 |
| RIVIERA DI CHIAIA | 50             | 4             | Masonry    | Masonry           | -5                    |         11.6 |           12 |
| RIVIERA DI CHIAIA | 53             | 5             | Masonry    | Masonry           | -3.5                  |         16.2 |           15 |
| RIVIERA DI CHIAIA | 57             | 5             | Masonry    | Masonry           | -3.5                  |           19 |           15 |
| RIVIERA DI CHIAIA | 61             | 5             | Masonry    | Masonry           | -3.5                  |         18.6 |           15 |
| RIVIERA DI CHIAIA | 66             | 3             | Masonry    | Masonry           | -3.5                  |           50 |            9 |
| P.za REPUBBLICA   | 57             | 5             | Masonry    | Arch - Wood Steel | -3                    |         32.6 |            9 |
| L.go TORRETTA     | 61             | 5             | Masonry    | Masonry           | -3                    |         27.7 |           18 |
| Via C. CUCCA      | 66             | 3             | Masonry    | Masonry           | -                     |          8.8 |            9 |

Tab.3-7. Buildings along Via Piedigrotta: zero and last reading and maximum measured settlements

| ID   | ID             | Zero reading   | Last reading   |   w max [mm] |   D f-s [m] | Date (w max )   |
|------|----------------|----------------|----------------|--------------|-------------|-----------------|
|      | 57             | 30-Mar-10      | 17-May-10      |        -3.80 |        21.6 | 12-apr-10       |
|      | 60             | 30-Mar-10      | 17-May-10      |        -2.90 |       145.3 | 13-mag-10       |
|      | 63             | 30-Mar-10      | 17-May-10      |        -4.80 |       113.9 | 13-mag-10       |
|      | 65             | 30-Mar-10      | 17-May-10      |        -6.60 |        83.6 | 14-mag-10       |
|      | 67             | 30-Mar-10      | 17-May-10      |        -3.90 |        62.7 | 17-mag-10       |
|      | 93             | 30-Mar-10      | 17-May-10      |        -4.90 |        12.9 | 14-mag-10       |
|      | PIEDIGROTTA 96 | 30-Mar-10      | 17-May-10      |        -1.20 |        45.5 | 26-mag-10       |
|      | 98             | 30-Mar-10      | 17-May-10      |        -1.20 |        41.4 | 26-mag-10       |
|      | 34             | 30-Mar-10      | 26-May-10      |        -3.70 |        20.6 | 12-apr-10       |
|      | VIA 30         | 30-Mar-10      | 13-May-10      |        -5.70 |        45.2 | 29-apr-10       |
|      | 23             | 30-Mar-10      | 17-May-10      |        -5.20 |        75.7 | 14-mag-10       |
|      | 16             | 30-Mar-10      | 17-May-10      |        -5.40 |        56.5 | 17-mag-10       |
|      | 11             | 30-Mar-10      | 26-May-10      |        -5.80 |        47.3 | 18-mag-10       |
|      | 7              | 30-Mar-10      | 26-May-10      |        -1.60 |        50.2 | 24-mag-10       |
|      | 19             | 30-Mar-10      | 26-May-10      |        -2.80 |        26.1 | 25-mag-10       |

Tab.3-8. Buildings along Riviera di Chiaia: zero and last reading and maximum measured settlements

| ID                |   ID | Zero reading   | Last reading   |   w max [mm] |   Df-s [m] | Date      |
|-------------------|------|----------------|----------------|--------------|------------|-----------|
| RIVIERA DI CHIAIA |   23 | 19-May-10      | 27-Jul-10      |        -7.70 |      45.60 | 14-Jun-10 |
| RIVIERA DI CHIAIA |   33 | 27-Jul-10      | 26-May-10      |        -4.80 |       31.8 | 28-Jun-10 |
| RIVIERA DI CHIAIA |   36 | 26-May-10      | 26-May-10      |        -5.40 |      36.11 | 28-Jul-10 |
|                   |   44 | 17-Jun-10      | 05-Aug-10      |        -4.60 |       63.5 | 03-Aug-10 |
|                   |   48 | 23-Jul-10      | 31-Aug-10      |        -4.80 |       98.6 | 31-Aug-10 |
|                   |   50 | 29-Jul-10      | 23-Aug-10      |        -3.50 |       35.3 | 06-Aug-10 |
|                   |   53 | 29-Jul-10      | 31-Aug-10      |        -3.60 |       37.1 | 24-Aug-10 |
|                   |   57 | 29-Jul-10      | 31-Aug-10      |        -5.20 |       57.6 | 30-Aug-10 |
|                   |   61 | 06-Aug-10      | 31-Aug-10      |        -2.40 |       15.5 | 27-Aug-10 |
|                   |   66 | 24-Aug-10      | 31-Aug-10      |        -2.80 |       11.8 | 27-Aug-10 |
| P.za REPUBBLICA   |    2 | 25-Aug-10      | 30-Jul-10      |        -2.20 |       54.1 | 25-Aug-10 |
| Via C. CUCCA      |    3 | 17-Jun-10      | 17-May-10      |        -5.30 |       49.6 | 14-Jun-10 |
| Largo TORRETTA    |   19 | 27-Jul-10      | 18-May-10      |        -4.60 |       41.6 | 16-Jun-10 |

<!-- image -->

Scatter plot

-10

Fig.3-22. Via Piedigrotta: maximum buildings settlements

<!-- image -->

Line chart

<!-- image -->

Line chart

<!-- image -->

Line chart

<!-- image -->

Line chart

Fig.3-23. Via Piedigrotta: landmarks measured displacements and buildings deformations related to the maximum measured displacement

<!-- image -->

Scatter plot

<!-- image -->

Scatter plot

<!-- image -->

Scatter plot

Fig.3-24. P.za Repubblica, Via C. Cucca, L.go Torretta and Riviera di Chiaia: landmarks measured displacements and buildings deformations related to the maximum measured displacement

<!-- image -->

Scatter plot

Fig.3-25. Buildings maximum settlements longitudinal contour along Via Piedigrotta and Riviera di Chiaia: sea side (above) and inland side (below)

Fig.3-26. Maximum settlements: longitudinal contours for landmarks on ground surface and on buildings facades

<!-- image -->

Line chart

On the base of the tunnelling induced displacements and on monitoring collected data,  for  each  building  the  damage  analysis  has  been  done  respecting  the  three level  analysis  as  described  in  Chapter  1.  Results  are  summarized  in  Tab.3-9  and Tab.3-10.

After the first level analysis based on calculating the rotation  and the maximum displacements Sv,max, for buildings civ.63 along Via Piedigrotta, buildings civ.3 along Via. C. Cucca and civ.23 along Riviera di Chiaia a more detailed evaluation, based on angular  distortion  L  calculation,  has  been  required.  For  buildings  along  Via Piedigrotta and Riviera di Chiaia, not any more detailed analysis have been needed, being the maximum angular distortion lower than the maximum admissible value (1/500),  whereas  for  buildings  in  Via  C.  Cucca  a  more  advanced  definition  of  the level  of  damage  is  required.  To  carry  on  this  kind  of  analysis  the  horizontal deformations  are  needed;  because  of  the  lack  of  monitoring  data  offering  the horizontal buildings displacements a detailed damage analysis is impossible and on the damage abacus (after Burland, 1995) corresponding to the specific building L/H

value,  only  the  calculation  of  the  limit  horizontal  strain  h for  each  category  of damage, corresponding to the measured deflection ratio  /L is possible (Fig.3-27).

<!-- image -->

Table

Tab.3-9. Via Piedigrotta: buildings damage analysis

| 1 st STEP ANALYSIS   | 1 st STEP ANALYSIS   | 1 st STEP ANALYSIS   | 1 st STEP ANALYSIS   | 1 st STEP ANALYSIS   |
|----------------------|----------------------|----------------------|----------------------|----------------------|
| BUILDING             |  =  /L             |  =  /L             | S v,max [mm]         | S v,max [mm]         |
| 57                   | 0.000701             | no dam               | -3.8                 | < 10 mm              |
| 60vp 1               | 0.000338             | no dam               | -2.9                 | < 10 mm              |
| 60                   | 0.000294             | no dam               | -2.9                 | < 10 mm              |
| 63vp 2               | 0.107407             | >1/500               | -6                   | < 10 mm              |
| 63                   | 0.000327             | no dam               | -6                   | < 10 mm              |
| 65                   | 0.000790             | no dam               | -6.6                 | < 10 mm              |
| PIEDIGROTTA 67       | 0.000237             | no dam               | -3.9                 | < 10 mm              |
| 96                   | 0.000149             | no dam               | -1.2                 | < 10 mm              |
| 98                   | 0.000093             | no dam               | -1.2                 | < 10 mm              |
| VIA 34               | 0.000711             | no dam               | -3.7                 | < 10 mm              |
| 30                   | 0.000954             | no dam               | -5.7                 | < 10 mm              |
| 23                   | 0.000690             | no dam               | -5.2                 | < 10 mm              |
| 16                   | 0.001152             | no dam               | -5.4                 | < 10 mm              |
| 11                   | 0.000681             | no dam               | -5.8                 | < 10 mm              |
| 7                    | 0.000344             | no dam               | -1.9                 | < 10 mm              |

<!-- image -->

Table

Tab.3-10. P.za Repubblica, Via C. Cucca, L.go Torretta and Riviera di Chiaia: building damage analysis

|                   | 1 st STEP ANALYSIS   | 1 st STEP ANALYSIS   | 1 st STEP ANALYSIS   | 1 st STEP ANALYSIS   | 1 st STEP ANALYSIS   | 2 nd STEP ANALYSIS   | 2 nd STEP ANALYSIS   |
|-------------------|----------------------|----------------------|----------------------|----------------------|----------------------|----------------------|----------------------|
| BUILDING          | BUILDING             |  =  /L             |  =  /L             | S v,max [mm]         | S v,max [mm]         |  =  /L             |  =  /L             |
| P.za REPUBBLICA   | 2                    | 0.0002               | no dam               | -2.2                 | < 10 mm              | -                    | -                    |
| Via C. CUCCA      | 3                    | 0.0150               | >1/500               | -5.3                 | < 10 mm              | 0.0150               | >1/500               |
| L.go TORRETTA     | 19                   | 0.0005               | <1/500               | -4.6                 | < 10 mm              | -                    | -                    |
| RIVIERA DI CHIAIA | 23                   | 0.0059               | >1/500               | -7.7                 | < 10 mm              | 0.0002               | <1/500               |
| RIVIERA DI CHIAIA | 33                   | 0.0003               | no dam               | -4.8                 | < 10 mm              | -                    | -                    |
| RIVIERA DI CHIAIA | 36                   | 0.0011               | no dam               | -5.4                 | < 10 mm              | -                    | -                    |
| RIVIERA DI CHIAIA | 44                   | 0.0011               | no dam               | -4.6                 | < 10 mm              | -                    | -                    |
| RIVIERA DI CHIAIA | 48                   | 0.0001               | no dam               | -4.8                 | < 10 mm              | -                    | -                    |
| RIVIERA DI CHIAIA | 50                   | 0.0005               | no dam               | -3.5                 | < 10 mm              | -                    | -                    |
| RIVIERA DI CHIAIA | 53                   | 0.0004               | no dam               | -3.6                 | < 10 mm              | -                    | -                    |
| RIVIERA DI CHIAIA | 57                   | 0.0001               | no dam               | -5.2                 | < 10 mm              | -                    | -                    |
| RIVIERA DI CHIAIA | 61                   | 0.0002               | no dam               | -2.4                 | < 10 mm              | -                    | -                    |
| RIVIERA DI CHIAIA | 66                   | 0.0002               | no dam               | -2.8                 | < 10 mm              | -                    | -                    |

1 60vp and 63vp refer to Vico Piedigrotta side of the buildings

2 Because of the lack of landmarks measurements along the building facade the  calculation is not possible

<!-- image -->

Line chart

h

Fig.3-27. Building civ.3\_Via C.Cucca: category of damage for L/H=1.4 and corresponding  h,lim defining the thresholds between the categories of damage

| Class of damage   | L/H = 1.4   | L/H = 1.4   |
|-------------------|-------------|-------------|
| Class of damage   |  /L [%]   |  h,lim [%] |
| 1                 | 0.0150      | 0.035       |
| 2                 | 0.0150      | 0.060       |
| 3                 | 0.0150      | 0.135       |
| 4                 | 0.0150      | 0.285       |

## Chapter 4. THREE-DIMENSIONAL FINITE ELEMENT ANALYSIS

## 4.1. Introduction

In  order  to  understand  the  tunnelling  induced  effects  of  Line  6,  a  number  of  finite elements  analyses  have  been  performed  by  the  use  of  Plaxis  3D  Tunnel,  especially designed for the analyses of tunnel projects whereas it can be thoroughly used for others geotechnical problems.

Although the limitations of the programs in defining a 'real' 3D geometry (the final 3D model is a consequence of the 2D geometry, extended on defined planes in tunnel axis direction), the used software allows to simulate the real 3D tunnel excavation process by defining different parameters for each calculation step, such as excavation lengths and duration, grouting and front pressure and volume losses.

Advanced  constitutive  models  can  be  implemented  to  simulate  non-linear  and  timedependent soil behaviour and consolidation and safety analyses can be performed too.

In the following pages, details about the software potentialities and the performed 3D analyses will be presented  after a brief discussion on the main  properties  and functionalities of the program, useful for the elaborated analyses.

## 4.2. Plaxis 3D Tunnel: useful informations for Line 6 application

As  briefly  mentioned  in  the  introduction,  the  3D  model  is  a  consequence  of  the  2D geometry  defined  in  a  cross-section  in  the plane  and  copied  in  all  the  planes defined in the z-direction (Fig. 4-1).

Fig. 4-1. Plane section and 3D model (planes and slices)

<!-- image -->

Engineering drawing

In  defining  the  2D  model,  soil  layers,  water  table,  structural  elements,  loads  and boundary conditions have to be specified in order to let the  program generate the 2D mesh,  according  to  the  defined  general  settings  in  regards  to  the  type  of  elements (triangular,  15  nodes  elements  with  6  stress  points  each  -  Fig.  4-3)  and  the  model dimensions (defined by the user in order to prevent the boundary conditions influence on the problem). The 2D mesh is than linearly extended in the z-direction to generate the 3D mesh Fig. 4-2.

<!-- image -->

Table

Fig. 4-2. 2D and 3D mesh

<!-- image -->

Icon

Fig. 4-3. Triangular mesh elements: nodes and stress points

<!-- image -->

Engineering drawing

Before the 3D mesh is generated, material properties have to be defined and so applied to each structural or soil elements. Five soils models are available in the program: Elastic Model, Mohr-Coulomb Model, Hardening Soil Model, Soil Soft Creep Model and Jointed Rock Model .  Except  from  the  Jointed  Rock  Model  used to simulate stratified or jointed rock behaviour, the remaining mentioned soil models can be applied to the soils. Since the Elastic Model, based on the Hook's law of isotropic elasticity is primarily applied for structural elements, the Mohr-Coulomb Model defined by five soil parameters (Young's Modulus ,  Poisson'ratio ,  cohesion ,  friction  angle and  dilatancy  angle ) is considered a good approximation in describing the soil behaviour and the Soft Soil Creep Model is useful in describing time-dependant behaviour of normally consolidate soils, the Hardening Soil Model is the model chosen for Line 6 tunnel affected soils, since it involves compression  hardening  to  simulate  irreversible  compaction  of  soil  under  primary compression and is particularly used for sands and gravels.

When a water table is defined into the model, in order to describe at best the water pressure  influence  on  soil  response, Drained , Undrained or Non-Pouros behaviour  for defined  soil  has  to  be  chosen,  depending  on  the  type  of  soil  (granular  or  cohesive). Because the soils affected by the Line 6 tunnel excavation are essentially granular soils on a Tuff bedrock, Drained behaviour has been set to describe their behaviour. It is especially suitable  when  no  excess  pore  pressure  generate,  for  instance  in  cases  of  dry  or  high permeable soils (sands), low rate of loading and/or for long term behaviour when there is no need to simulate the history of undrained loading or consolidation. The Non-Pouros behaviour  is  indeed  used  for  describing  concrete  or  structural  elements  (i.e.  concrete tunnel lining) often in combination with the Linear Elastic Model .

## 4.2.1. The Hardening Soil Model

The basic idea for the Hardening Soil Model is the hyperbolic relationship between the vertical strain and the deviatoric stress observed in the primary triaxial loading tests (Fig. 4-4). It is related to the decreasing in stiffness and to the plastic strains developing when primary deviatoric loading is applied (Kondner &amp; Zelascko, 1963).

In order to use this soil model, a number of soil parameters have to be defined. Despite some of them are the same as those used in the non-hardening Mohr-Coulomb model, such as and , the below additional parameters for using the model have to be defined:

-  , secant stiffness in standard triaxial test
-  tangent stiffness for primary oedometer loading
-  , power of stress-level dependency of stiffness
-  , unloading/reloading stiffness
-  , secant stiffness in standard triaxial test
-  , Poisson's ratio for unloading-reloading
-  , reference stress for stiffnesses,
-  , value for normal consolidation
-  , failure ratio .

In  the  following  pages,  the  main  equations  describing  the  Hardening  Soil  Model  are reported.

The yield curves obtained by the standard triaxial tests can be described by equation (4.1)  for where is  the  ultimate  deviatoric  stress,  derived  by  Mohr-Coulomb failure  criterion,  involving  the  strenght  parameters and ;  it  is  defined  by  equation (4.2) .

<!-- formula-not-decoded -->

As soon as the failure criterion is satisfied and perfectly plastic yield occurs. The relation  between ,  given  by  equation  (4.3)  ,  and is  expressed  by  the  failure  ratio ,  representing  the  percentage  of  failure  deviatoric  stress reached,  usually automatically set equal to .

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

The stress strain behaviour for primary loading is highly non linear. Instead of using the tangent  stiffness  modulus  for  primary  loading ,  difficult  to  determine,  the  secant Young's modulus is defined. It is expressed by:

<!-- formula-not-decoded -->

where is  the reference stiffness modulus corresponding to a reference stress , and represents the amount of stress dependency of the actual stiffness on the minor principal stress (the effective confining pressure in a triaxial test). is determined from triaxial stress-strain-curve for a 50% mobilization of the maximum shear strength .

Fig. 4-4. Hyperbolic stress-strain relation in primary loading for a standard drained triaxial test

<!-- image -->

Line chart

From experimental data on sandy soils relation has been found (Fig. 4-5), whereas for clay .

For un-reloading stress paths, the stress-dependent stiffness modulus is used. It is expressed by equation (4.5) and defined as the unloading-reloading Young's modulus in a wide  unloading-reloading  cycle  (Fig.  4-7),  corresponding  to  the  reference  pressure .  From  drained  triaxial  tests  relations  between  the  unloading-reloading stiffness modulus and the loading stiffness modulus were found (Fig. 4-8).

<!-- formula-not-decoded -->

Fig. 4-5. vs relationship from experimental data for sandy soils

<!-- image -->

Line chart

Fig. 4-6. Loading and unloading stiffness Young's moduli

<!-- image -->

Line chart

Fig. 4-7. Loading and unloading stiffness moduli

<!-- image -->

Engineering drawing

Fig. 4-8. Relation between and for loose and dense soils from drained triaxial tests

<!-- image -->

Line chart

is even used in defining the shear modulus , as expressed by equation (4.6) and represented in Fig. 4-9.

<!-- formula-not-decoded -->

Fig. 4-9. Shear stiffness modulus

<!-- image -->

Engineering drawing

The  un-reloading  path  is  modeled  as  purely  (non-linear)  elastic  and the elastic component is  calculated  using  equations  (4.5)  and  (4.6)  for  a  constant  value  for  the Poisson's ratio . Relations expressed by formula (4.7) and (4.8)  have been obtained.

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

The yield surfaces for such a model are defined by equations (4.9) and (4.10) depending on plastic shear strain and plastic volumetric strains , and depicted in Fig. 4-10. The approximation in equation (4.10) is accurate since for hard soils plastic volume changes tend to be small when compared with the axial strain.

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

Fig. 4-10. Successive yield loci for various values of the hardening parameter and failure surface

<!-- image -->

Line chart

For given values equations can be plotted in plane by means of yield locus whose shapes depend by values being linear for and slightly curved for lower values. Fig. 4-10 represents yield loci for , typical for hard soils.

Since the Hardening Soil Model involves plastic strains such as and , attention has to  be  focused  on  the  relationship  ( flow  rule )  occourring  between  them,  expressed  by equation:

<!-- formula-not-decoded -->

where is  the  mobilized dilatancy angle given by expression (4.12) depending on the critical state friction angle and on the mobilized friction angle (equation (4.13) .

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

The  above  mentioned  equations  correspond  to  the  stress-dilatancy  theory  by  Rowe (1962)  and  Rowe  (1971),  as  explained  by  Schanz  &amp;  Vermeer  (1996),  based  on  the observed material contraction for small stress ratios  and on the observed dilatancy for high stress ratios . At failure, when equation (4.12) becomes:

<!-- formula-not-decoded -->

hence the critical state angle can be derived from the failure ones and .

## 4.3. Three-dimensional  analyses  of  the  Line  6 tunnel

In this section 3D Finite Elements analyses of Line 6 tunnel performed by means of Plaxis 3D  Tunnel  will  be  discuss.  Description  of  the  geometric  model,  details  on  materials, constitutive model and the kind of analysis performed will be discuss in order to show results of parametric studies on the effects of both soil and machine parameters, and of back-analysis performed on the basis of collected monitoring data. The realized tunnel up to August the 31 st was analyzed and a reference plane section has been chosen along Via Piedigrotta to perform such analyses.

## 4.3.1. The input model

Since Plaxis 3D Tunnel draws the 3D geometry on the basis of the plane-strain section defined  in plane  and  reproduced  all  along  the  tunnel  axis  direction ( cfr. Paragraph 4.2 ), the choice of a representative section along the longitudinal profile of the line has been required.

The analyzed section in the plane is made by 18 m depth tunnel axis and 14 m thick loose soil layer on the Tuff bedrock with 3 m a.m.s.l. groundwater table (Fig. 4-11). As and no buildings have been considered for the 3D analyses, a symmetric section was possible for the analyses, in order to minimize the calculation time strictly depends by the number of elements in the 3D mesh, hence by the model dimensions.

Fig. 4-11. Plane reference section in (x,y) plane for FE analyses

<!-- image -->

Engineering drawing

To prevent the border effects influence on the excavation process, a plane section size was  defined.  The  number  of  planes  in  z-direction  was  fixed  as  to reproduce at best the real excavation process in respect of the real progress of the final lining  and  of  the  tunnel  excavation  day  by  day;  in  such  a  way  an model in z-direction was constructed (Fig. 4-12). The resulted 3D model is then featured by 44268 elements and 122688 nodes.

Fig. 4-12. Plaxis 3D geometric model for the FE analyses

<!-- image -->

Engineering drawing

Since the tunnel excavation affects at the most the upper loose grounds layer, mainly made by sandy soils, ' drained ' analyses were performed in order to not produce excess pore pressure resulting from the tunnel excavation process.

The Hardening Soil Model was used to define the soils'behaviour and the Linear Elastic Model for the structural elements (EPB shield and concrete final lining); 0 resumes both soils and structural elements properties besides the type of elements chosen to simulate the tunnel lining segments ( clusters ) and the EPB shield ( shell ) (Fig. 4-13).

<!-- image -->

Table

<!-- image -->

Table

Tab.4-1. Soil parameters used for the 3D analyses

Fig. 4-13. Structural elements for the EPB shield (' beam ') and the lining segments (' cluster ')

<!-- image -->

Engineering drawing

In  order  to  model  the  soil-tunnel  interaction,  implying  a  reduction  in  soils  strength parameters, the same soils materials have been defined also using the parameter, useful  to  describe  the  interface  and/or  soil  reduction  in  friction  and  adhesion  if  lower than 1. The materials with reduced strength parameters have been applied to that slices where the tunnel was already excavated, the EPB shield was already been and the soiltunnel interface properties were consequently reworked.

## 4.3.2. The  effects  of  soil  parameters  on  surface subsidence

In order to analyze the soils parameters 'influence on the surface subsidence, a number of  FE  analyses  have  been  performed  on  simplified  geometric  model  made  by  a  single loose  soils  layer  (being  the  Tuff  bedrock  at  the  tunnel  invert,  its  effect  on  the  surface displacements can be reasonably considered to be negligible).

The  Hardening  Soil  Model  and  the  'drained'  analysis  were  set  to  describe  the  soil behaviour. For such a constitutive model, apart from the strength parameters and , both the loading and un-reloading Young's modulus are requested.

All  strength  and  stiffness  parameters  (except  from ,  since  analyses  focuse  on  sandy soils),  together  with  un-reloading  on  loading  stiffness  moduli  ratio ,  were varied  within  realistic  ranges  of  values,  as  to  investigate  their  influence  on  tunnelling induced soil behaviour and to indentify that parameters affecting at the most the surface subsidence.

Because of the 'drained' soil behaviour, different  volume  losses  at  the  tunnel  crown and at the ground surface were expected. Though a volume loss controlled analysis would be  possible  (by  setting  an  user  value  in  that  planes  were  a  defined  volume  loss  is required),  in  performed  analyses  cases  not  any  volume  loss  at  the  tunnel  depth  was imposed.  Fig. 4-14\_ a and  Fig.  4-14\_ b show the obtained volume losses and maximum settlements at the tunnel crown related to the loading stiffness modulus while Fig. 4-15\_ a and Fig.  4-15\_ b depict,  for  the  analyzed  section,  the  ratios  between  the  volume  losses and the maximum settlements at the ground surface than at the tunnel crown. A linear relationship can be detected between the volume losses and the maximum settlements ratios  ( and )  and  the  loading  stiffness  modulus,  with  the surface volume loss increasing up to the  volume  loss  at  the  tunnel  crown,  and  the maximum surface settlements being between the crown settlement, depending on ratio.

All  the  results  plotted  in  the  next  pages,  concerning  the  others  'parameters  influence on  the  ground  surface  displacements, refer to the volume loss on the ground surface rather than to the volume loss at the tunnel crown. For more results about the mentioned soil parameters influence on the volume loss at the tunnel depth see Appendix V (Fig. IV-1 up to Fig. IV-6).

Fig. 4-14. Volume loss (a) and maximum settlement (b) at the tunnel crown

<!-- image -->

Scatter plot

Fig. 4-15. Volume loss at the ground surface on volume loss at the tunnel depth (a) and maximum surface settlements on the maximum settlements at the crown (b)

<!-- image -->

Box plot

The range of variations for each soil parameter, together with the reference analyses parameters, are resumed in Tab.4-2, while more details about any specific analysis used parameters together with the obtained numerical results are reported in specific tables in Appendix IV.

Concerning to the stiffness moduli ratio ,  although  3  is  the  Plaxis  default  value and is  a  reliable range for sandy soils, a number of analyses were performed in order to analyze the effects of the un-reloading stiffness modulus increase up to 12 times the loading one. In such a way a kind of  Hardening Soil Small Model is simulated, since increasing in ratio leads the soil behaviour to move towards the small strain field.

Tab.4-2. Soil parameters in the reference analyses and respective ranges of variations for the performed parametric analyses

| SOIL PARAMETERS      | SOIL PARAMETERS   |   REFERENCE VALUES | RANGE OF VARIATION   |
|----------------------|-------------------|--------------------|----------------------|
| REFERENCE ANALYSES   | [kPa]             |                    |                      |
| REFERENCE ANALYSES   | [kPa]             |                    |                      |
| REFERENCE ANALYSES   |                   |                  3 |                      |
| RANGES OF VARIATIONS | [kN/m 3 ]         |                 13 |                      |
| RANGES OF VARIATIONS | [kN/m 3 ]         |                 18 |                      |
| RANGES OF VARIATIONS | [°]               |                 35 |                      |
| RANGES OF VARIATIONS | [°]               |                  0 |                      |

As  widely  described  in  the  first  chapter  of  this  thesis,  results  from  numerical  FE simulations  of  tunnel  excavation  often  show  a  surface  subsidence  curves  too  wide  if compared to collected  monitoring  data.  For  such  a  reason,  in  this  section,  attention  is mainly drawn on the effects of soil parameters on values. Moreover to investigate the advancing effects along the tunnel axis direction, the  output results were  extrapolated and plotted on three planes: 'Plane O' coinciding with the tunnel front plane, 'Plane U' and 'Plane AE'  respectively 1D and 3D from it. Since the observed effects in the three planes are quite similar to each other, the graphs below on and effects, only depict results concerning the tunnel front plane (Plane O); see Appendix IV for results on Plane U and Plane AE ( cfr. Appendix IV - Fig. IV-1).

From the performed analyses, clear relations between and the soil parameters , , , , were  detected.  The  main  results  about  their  effects  on  the  surface subsidence  are  resumed  in  the  following  pages,  although  further  informations  are reported in the Appendix IV (Fig. IV-7, Fig. IV-8, Fig. IV-9) .

Fig.  4-16  shows  the  relations  linking and to  the  subsidence  maximum displacements,  the  volume  loss  and  the  subsidence  width.  The  figures  demonstrate  a significant effect of variations on and , rather than on the width parameter .

Contrarwise a more evident effect on values is played by the stiffness moduli ratio ; as a matter of fact Fig. 4-16\_ c depicts the observed behaviour describing a wider range in the plane  than  in  the  others  cases  (Fig.  4-16\_ a and  Fig.  4-16\_ b ). Actually, focusing the attention on ,  the graphs show reductions in surface subsidence width by increasing the loading stiffness modulus and an opposite effects by raising the ratio; for such a reason the Plaxis default value has been chosen to perform the Line 6 back-analyses. The same informations derived from the just described graphs can be deduced also by dependent curves, as shown in Fig. IV-8 in Appendix IV .

More graphs on the stiffness moduli effects are resumed in Appendix, showing relations in , and planes. Linear  relationships  can  be  highlighted  between  the  observed  parameters  and  the stiffness moduli ratio ( cfr. Appendix IV - Fig. IV-9).

In the same way as described above, in Fig. 4-17 and Fig. 4-18 the effects of variations on and and and of on are depicted (not any particular trend between , and were identified for the analyzed cases, as a consequence not any graph was reported). Increments or reductions in lead to analogous variations in and in (Fig.  4-17 \_a and  Fig.  4-17 \_b ),  contrariwise  not  any  increments  in are  related  to analogous increments in , whereas a 20% reduction leads to a 46% decrease (Fig. 4-17\_ c ).

Tab.4-3  synthesizes  the  obtained  results,  resuming  the  maximum and variations induced by changes in , and .

Tab.4-3. Maximum variations on and induced by maximum variations of , and

| Maximum variations   | Maximum variations            |  w max /w max,rif [%]   |  V L /V L,rif [%]   |  k/k rif [%]   |
|----------------------|-------------------------------|--------------------------|----------------------|-----------------|
|  E/E rif [%]        | (-1/3 - 3) E rif (-67 - 200)% | (+156 -49)%              | (+171 -44)%          | (-2 +10)%       |
|  P/P rif [%]        | (0 - 300)%                    | (0 +15)%                 | (0 +70)%             | (0 +52)%        |
|  /  rif [%]      | ( 20%)                        | (-51 +29)%               | (-73 +32)%           | (-46 +10)%      |

Finally,  Fig.  4-18  depicts  the  effects  of and on  the  subsidence  width:  a  40% reductions in friction angle leads approximately to a 25% linear increase in (the surface subsidence curve becomes wider by reducing the soil friction angle), conversely a nonlinear trend relation is detected in the dependent graphs. Up to not any  effects  on is  identified,  while  for an  instantaneous  15% increase in is observed. The same behaviour is noticed in dependent graphs for and ( cfr. Appendix IV - Fig. IV-10).

Fig. 4-16. Effects of loading stiffness modulus variations on surface subsidence, on tunnel front plane (Plane O): maximum displacements (a) , volume loss (b) and k (c)

<!-- image -->

Line chart

<!-- image -->

Box plot

(c)

Fig. 4-17. Effects of on surface subsidence: maximum displacements (a) , volume loss (b) and k (c)

<!-- image -->

Scatter plot

Fig. 4-18. Effects  of (a) and (b) on subsidence width

## 4.3.3. Parametric  analyses  on  the  EPB  front  and grouting pressures

The EPB operating principle is based on the use of the front pressure (FP), to prevent the tunnel  face  collapse,  the  grouting  pressure  (GP)  to  fill  the  soil-shield  gap  and  of  the hydraulic  jacks  forces  to  ensure  the  machine  advance.  Since  both  the  front  and  the grouting pressures are used to prevent tunnel collapse phenomena as to minimize the volume loss, a parametric study to observe the effects of each pressure on the induced tunnelling  surface  displacements  was  considered  useful,  as  to  define  the  technological parameters importance compared to the soils 'properties ones.

In order to apply to the Line 6 case the results obtained by such a parametric study on the machine pressures, the geometric model described in Section 4.3.1. (Fig. 4-11), made by two soil layer, the upper loose soils layer and the Yellow Neapolitan Tuff bedrock, was used, as to not overlook the pressures 'effects applied even in the underlie portion of the tunnel where the Yellow Neapolitan Tuff is located. The reference properties for both the soils  'layers,  used  in  the  analyses  discussed  in  the  following  pages    are  resumed  in  the table below.

Tab.4-4. Soil parameters for the performed analyses

| SOIL PARAMETERS     | REFERENCE VALUES   | REFERENCE VALUES   |
|---------------------|--------------------|--------------------|
|                     | LOOSE SOILS        | TUFF               |
| [kPa]               |                    |                    |
| [kPa]               |                    |                    |
|                     | 3                  | 3                  |
| VALUES [kN/m 3 ]    | 13                 | 14                 |
| REFERENCE [kN/m 3 ] | 18                 | 19                 |
| c [kPa]             | 0                  | 500                |
| [°]                 | 35                 | 27                 |
| [°]                 | 0                  | 0                  |

A number of analyses were performed keeping as constant the 'input' parameters soil properties, the excavation phases and volume loss 1 at the crown and varying within the ranges resumed in Tab.4-5 the front and the grouting pressures ( cfr. Appendix IV - Tab. IV1). Results will be discussed in the following pages highlighting the single front pressure effects as the grouting pressures ones.

Tab.4-5. Ranges of variations of the machine pressures

| EPB PARAMETERS   | EPB PARAMETERS                                   | RANGE OF VARIATION   |
|------------------|--------------------------------------------------|----------------------|
|                  | Front Pressure (FP) [kPa]                        | (100 - 500)          |
|                  | Grout Pressure (GP) [kPa]                        | (100 - 500)          |
|                  | REFERENCE ANALYSES Hydraulic Jack Pressure [kPa] | (635 - 2255)         |
|                  | GP/FP                                            | (0.2 - 5)            |

For  both  the  front  and  the  grouting  pressures  clear  trends  of  the  maximum  surface settlement  and  the  volume  loss  both  at  tunnel  depth  and  at  the  ground  surface  are evident.

Despite  volume  loss  controlled  analyses  were  performed  by  applying  specific  volume loss at the tunnel depth, the realized volume loss at that location is clearly affected by the applied front pressures (more than by the grouting pressure). Indeed Fig. 4-19\_ a shows the volume loss at the crown referred to the applied pressure at the tunnel face. Despite the imposed volume loss at the crown was always the same (0.1%) the figure reveals how the realized 2 volume loss may exceed such a value for the lower front pressures, as the opposite  can  occur  for  high  pressures.  Such  a  phenomenon  can  be  explained  by  the three-dimensional  effects  related  to  the  tunnelling,  much  more  evident  for  low  front pressures at the tunnel, since the tunnelling induced displacements affect longer distance from the tunnel front because of the higher displacements toward the excavation.

1 A reference  value for the volume loss at the crown was chosen in reference to the parametric study on soil  'properties  effects  described  in Section  5.3.2 .  For  the  design  stiffness  modulus , reliable value  for that volume loss is (Fig. 4-14(a)\_ a ).

2 For  each  calculation  step  the  used  software  provides  the  realized  volume  loss  at  the  tunnel  depth, depending on the relative tunnel-soil stiffness. Such a value represents the final volume loss at the end of each calculation phase, including the effects induced by previous steps.

At the same time Fig. 4-19\_ b shows the pressure influence on volume loss at the surface than the volume at the tunnel depth. Such a ratio can increases up to 4 by raising the front pressure and for the lowest grouting pressure. The same figures finally reveal the front pressure being much more influent than the grouting pressure on the volume loss at the  tunnel  depth,  and  contrariwise  the  grouting  pressure  affecting  much  more  the induced surface behaviour.

Fig. 4-19. Front and grouting pressure effect on the realized volume loss at tunnel depth (a) and on the ratio between the volume loss at the crown and the volume loss at the ground surface (b)

<!-- image -->

Scatter plot

Focusing  the  attention  on  the  pressures  influence  on  the  surface  effects  in  terms  of surface volume loss and maximum settlement, dimensionless and brief graphs are plotted in the next pages, showing the front pressures proportioned to the minimum value of the range  (100  kPa)  related  to  the  relative  surface  settlement  and  volume  loss  ratios.  For specific  graphs  plotting  the  numerical  values  of  such  parameters,  rather  than  their variations, see the Appendix IV .

Fig.  4-20\_ a and  Fig.  4-20\_ b show  the  front  pressure  dependent  results.  A range  of behaviour for both and can be identified, by varying the applied grout pressure. Indeed both the figures show initial reduction for both the and the for increasing front  pressure  up  to  a  specific  value,  than  gradual  increases  with  lower  gradient.  The same behaviour is highlighted in Fig. 4-21 where for each grouting pressure value, both the  settlement  and  volume  loss  variations  are  plotted  in  reference  to  that  value corresponding to the minimum front pressure applied (100 kPa). A reduction up to 30% of the  surface  maximum  settlement  and  up  to  10%  of  the  volume  loss  are  measured  for front pressure increase up to 100% (FP = 200 kPa), after that reductions up to 10% for the settlements and 5% for volume losses are caused by further front pressure increments.

The observed behaviour can be justified by some considerations, resumed below:

-  shear  strength  achievement at the tunnel face for  low front pressures, within the  range  (100  -  130  kPa),  leads  to  local  Mohr-Coulomb  and  Hardening  Soil yielding points ( cfr.  Appendix  IV - Fig. IV-18 and  Fig. IV-19), thus face plasticization and higher settlements
-  for low front pressure the tunnel face plasticization is the predominant effect, leading to high surface settlements and volume losses; raises in such a pressure up to a defined (200 kPa) value, reflect on reduction of both and
-  further  increase  of  the  front  pressure  leads  to  plasticization  of  the  tunnel contour giving rise to new increment in and
-  horizontal  displacements  along  the  tunnel  axis  are  strictly  connected  to  the applied pressure. They go toward the excavated tunnel until the front pressure reaches a sort of 'equilibrium' value (170 kPa) at which no z-axis displacements are detected; when the front pressure exceeds such a value opposite horizontal displacements, up to 20 mm, are measured toward the soil ( cfr. Appendix IV - Fig. IV-15).

A different behaviour is observed in the grouting pressure dependent graphs (Fig. 4-23): linear relationships between the grouting pressure and the relative surface settlements and  volume  losses  are  detected,  showing  25%  in and  30%  in reductions  for grouting pressure increments up to 400%.

Furthermore,  dimensionless  graphs  in  Fig.  4-24  show  the  predominant  effect  of  the front pressure on both the surface maximum settlement and volume loss, up till 200% of pressures  increments,  contrariwise  the  predominant  effect  of  the  grouting  pressure  is pronounced for the highest increment (FP=GP=500 kPa).

Fig. 4-20. Front pressure (FP) effects on maximum surface settlement (a) and on surface volume loss (b): range of values depending on the applied grouting pressure

<!-- image -->

Line chart

Fig. 4-21. Front pressure (FP) effects on maximum surface settlement (a) and on surface volume loss (b): total dimensionless graphs

<!-- image -->

Line chart

Fig. 4-22. Grout pressure (GP) effects on maximum surface settlement (a) and on surface volume loss (b): range of values depending on the applied front pressure

<!-- image -->

Scatter plot

Fig. 4-23. Grout pressure (GP) effects on maximum surface settlement (a) and on surface volume loss (b): dimensionless graphs

<!-- image -->

Scatter plot

Fig. 4-24. Comparison between the grout pressure (GP) and front pressure (FP) effects on maximum surface settlement (a) and surface volume loss (b)

<!-- image -->

Scatter plot

Trying  to  resume  the  informations  collected  up  to  now,  figures  below  represent  the effects of the pressures ratio GP/FP, on and variations. Linear relationships can be identified (Fig. 4-26).

As  Fig.  4-26  show  the  pressures  ratio  influence  on  the  surface  subsidence  is  more pronounced on  the  volume  loss rather  on  the  settlement and  a  sort  of  linear  effect  can  be  detected,  in  a  range  of values defined by the minimum and maximum front pressure values.

Fig. 4-25. Relation between the front than the grouting pressure ratio, the surface settlement (a) and volume loss (b)

<!-- image -->

Scatter plot

<!-- image -->

Line chart

-40%

Fig. 4-26. Influence of the grouting than the front pressure ratio on surface volume loss and maximum settlement

## 4.3.4. Back-analysis  of  observed  effects  of  Line  6 tunnelling

In  order  to  perform  a  back-analysis  of  the  observed  Line  6  tunnelling  effects  the geometric model, the material properties  for the  loose  soil  layer  and  the  Tuff  bedrock described in Section 4.3.1 were used.

In defining the analyses calculation steps, the real construction process was simulated and  the volume  loss or contraction  method was  used.  In  such  a  way,  13  calculation ' Staged construction ' (Tab.4-6) phases have been defined as to reproduce about 100 m tunnel excavation length, respecting the real excavation process.

In  each  phase  the  same  procedure  to  simulate  the  tunnel  construction  process  is repeated by:

-  deactivating  the  soil  clusters  inside  the  tunnel  lining  and  draining  the  water within the EPB shield
-  activating the shell elements representing the EPB shield behind the tunnel face
-  applying the concrete properties to the clusters representing the installed final lining
-  applying the face and the grout pressure to prevent the tunnel collapse, and the forces the hydraulic jack driving the EPB machine exert on the already installed lining (Fig. 4-27)
-  modelling  the  soil-tunnel  interaction  by  assigning  modified  properties,  with reduced  strength  parameters,  to  loose  soils  and  tuff  in  the  slices  where  the tunnel has already been built, by means of parameter
-  defining a tunnel contraction.

Tab.4-6. 13 'staged construction' phases defined for  Plaxis simulation

|      | FRONT    | FRONT              | FINAL LINING   | FINAL LINING       |
|------|----------|--------------------|----------------|--------------------|
| STEP | Plane ID | Plane position [m] | Plane ID       | Plane position [m] |
| 1    | H        | -36.90             | C              | -28.40             |
| 2    | I        | -38.60             | D              | -30.10             |
| 3    | K        | -42.00             | F              | -33.50             |
| 4    | N        | -47.10             | I              | -38.60             |
| 5    | R        | -53.90             | M              | -45.40             |
| 6    | V        | -60.70             | Q              | -52.20             |
| 7    | X        | -64.10             | S              | -55.60             |
| 8    | AB       | -70.90             | W              | -62.40             |
| 9    | AG       | -79.40             | AB             | -70.90             |
| 10   | AH       | -81.10             | AC             | -72.60             |
| 11   | AK       | -86.20             | AF             | -77.70             |
| 12   | AP       | -94.70             | AK             | -86.20             |
| 13   | AS       | -99.80             | AN             | -91.30             |

Fig. 4-27. EPB pressures on the tunnel face (Front Pressure), around the cavity (Grout Pressure) and on the final lining (Jack Pressure)

<!-- image -->

Engineering drawing

Fig. 4-28. Construction stages of a tunnel shield

<!-- image -->

Engineering drawing

For each defined calculation step the gap between the tunnel face and the last installed lining segments was kept equal to the machine length (8.5 m). Except from the first slice next to the last mounted lining segment, where the grout pressure is applied, the EPB shield was installed by activating shell elements all along the slices included in the gap, in order to prevent the tunnel cable collapse. Fig. 4-28 schematically shows the procedure for defining each staged construction phase.

In order to reduce the influence of boundary conditions on the excavation process, 25 m of  tunnel  have  been  excavated  at  the  start  of  the  model  and  the  tunnelling  induced displacements have been set to zero before the first calculation phase of the observed tunnel construction process started. Fig. 4-29 depicts a generic calculation step.

Fig. 4-29. 3D plot of a generic input phase

<!-- image -->

Engineering drawing

Both  the  front  and  grouting  pressure  linearly  increase  with  depth;  starting  from  a reference pressure values at the tunnel crown, a gradient of 14 kPa (the specific weight of the bentonite used for supporting the face) was defined for the front pressure and of 20 kPa (depending on the used mixture for the mortar injections) for the grouting pressure. Contrariwise  the  hydraulic  jacks  pressure  on  the  final  lining  is  not  depth  dependent;  a constant value is defined, related to the applied front pressure.

The  monitoring  data  collected  during  the  tunnel  excavation  have  been  resumed  in Chapter 3 . The landmarks sections on the ground surface have been used to calibrate the model. As discussed in the chapter expressly dedicated to the monitoring data analysis, up to August the 31 st 45 ground landmarks sections were installed along Via Piedigrotta, following  the  tunnel  track;  according  to  the  maximum  measured  settlements,    such sections were collected into the groups resumed in the table below.

Tab.4-7. Landmarks sections on the ground surface grouped according to the maximum measured settlement

| GROUP ID            | GROUP ID     | w max [mm]   |
|---------------------|--------------|--------------|
| AT01 - SP01         | (zone A)     | 5 ÷ 8        |
| 1 AT12 - AT16       | (zone B)     | 5 ÷ 8        |
| AT18 - AT19         | (zone B)     | 5 ÷ 8        |
| AT26                | (zone B)     | 5 ÷ 8        |
| AT02 -AT10          | (zone A)     | 8 ÷ 14       |
| 2 AT17              | (zone B)     | 8 ÷ 14       |
| AT25                | (zone B)     | 8 ÷ 14       |
| SC01                | (zone B)     | 8 ÷ 14       |
| AT11                | (zone B)     | ≤ 5          |
| 3 AT20 - AT23       | (zone B)     | ≤ 5          |
| AT27 - AT42         | (zone B - C) | ≤ 5          |
| SINGULAR CASES AT04 | (zone A)     | 42.40        |
| AT24                | (zone B)     | 62.30        |

As  discussed  in  the  previous  sections,  the  machine  applied  pressures  and  the  volume loss at the tunnel depth have a considerable influence on the tunnelling induced effects on the ground surface, the same goes for the volume loss imposed at tunnel depth.

While  for  the  machine  pressures  the  collected  data,  pointed  out  in  Chapter  3  ( cfr. Section  3.3.1. ),  were  used  as  to  define  the  input  values  for  the  analyses,  not  any monitoring data about the volume loss at the ground surface nor at the tunnel depth is available. Referring to the parametric analyses results discussed in the previous sections, according  to  the  soil  stiffness  parameters  ( cfr.  Section  4.3.2. ),  a  0.1%  volume  loss  was considered an initial reliable value to impose at the tunnel depth. Nevertheless, since the geometric  model  for  the  analyses  did  not  change  (according  to  the  reference  section described in Section 4.3.1.- Fig.  4-11)  and the effects to be reproduced are significantly different from each other, being the soil parameters and the machine pressures known and well defined, different values for the volume loss at the tunnel crown were needed in order to reproduce the different measured subsidence surface. Tab.4-8. resumes the final volume  loss  values  to  reproduce  the  observed  displacements;  the  highest  value  was required to reproduce the Group 1 displacements and the lowest for the Group 3 ones. The obtained subsidence's are plotted in Fig. 4-30. Looking at the maximum settlement, the  analyses  results  are  in  good  agreement  with  the  monitoring  data  in  terms  of maximum settlements reproduced, while a less accurate accordance results regarding the subsidence width, especially for the first group of data (Fig. 4-30\_ a ), showing an abnormal behaviour  if  compared  to  the  remaining  groups  of  sections.  Anyway,  such  a  result confirms the collected indications from literature about the difficulties in reproducing the subsidence width by means of numerical simulations.

Tab.4-8. Input and output parameters for the analyses reproducing the measured landmarks sections displacements

|                                   | GROUP 1 (AT01 - AT07)   | GROUP 2 (AT09 - AT21)   | GROUP 3 (AT27 - AT42)   |
|-----------------------------------|-------------------------|-------------------------|-------------------------|
| Front Pressure [kPa]              | 150                     | 190                     | 240                     |
| Grouting Pressure [kPa]           | 160                     | 150                     | 370                     |
| Hydraulic Jacks Pressure [kPa]    | 877.6                   | 999                     | 1202                    |
| Volume loss at the tunnel depth   | 0.25 %                  | 0.15%                   | 0.10%                   |
| Volume loss at the ground surface | 0.52%                   | 0.34%                   | 0.21%                   |
| Maximum obtained settlements [mm] | -11                     | -6.99                   | -4.53                   |

The  analyses  accuracy  was  confirmed  also  by  comparing  the  obtained  results  to displacements  in longitudinal direction. Fig. 4-31 shows  how  all the settlements longitudinal profiles for the three groups, belong to the range narrowed by monitoring data.

As shown in Fig. 4-32, for the analyzed case, the volume loss at the surface is always twice the volume loss at tunnel depth.

<!-- image -->

Engineering drawing

Fig. 4-30. Transversal subsidence surfaces obtained by the back-analyses for the three groups of sections: Group 1 (a), Group 2 (b) and Group 3 (c)

<!-- image -->

Line chart

Fig. 4-31. Longitudinal displacements obtained by the back-analyses compared to the range defined by the collected monitoring data

<!-- image -->

Line chart

Fig. 4-32. Relation between the volume loss at the tunnel depth and the volume loss at the ground surface

<!-- image -->

Scatter plot

## CONCLUSIONS

Tunnelling in urban areas is of increasing importance over the past few decades. The lack  of  existing  facilities,  considering  the  continuously  increasing  demand  in  transports, asks  for  new  solutions.  In  such  a  way  deep  excavations  (tunnels  and  vertical  shafts) started to spread even more throughout the urban areas, as to realize new underground lines. Because of the high urbanization of the largest cities, where such excavations take place,  the  prediction  and  the  analyses  of  the  induced  effects,  by  means  of  analytical, numerical or sperimental methods, play an even more important role, in order to prevent distortions  and,  in  severe  cases,  damage  to  the  overlying  buildings  and  services.  The conventional design methods to assess the induced deformations on buildings are based on empiricism gained from Greenfield sites. Such methods lead to define the tunnelling induced displacement field in very simple hypothesis roughly accounting of the number of technological factors affecting the induced displacements. However literature data reveal that  the  role  of  the  excavation  technique  is  far  from  negligible.  Indeed,  an  initial distinction between the effects induced by traditional and mechanical tunnelling methods can be defined. Moreover looking at the tunnel excavations realized by means of complex excavation machines, a significant reduction in the induced effects due to the excavation techniques improvement over the years has been revealed. Numerical analyses, by means of Finite Element codes, represent an useful tool to account for the excavation method in the design process, since they enable the whole excavation process. In this context, the objective  of  this  thesis  has  been  to  assess  the  influence  of  technological  factors  on tunnelling induced displacements. This has been done from a numerical point of view by a parametric study aimed to investigate the role played factors. In a second stage of the research, the results have been used to back-analyze at the best the observed behavior, in  terms  of  surface  settlements,  during  the  Line  6  tunnel  excavation  process.  The availability of a huge amount of monitoring data, in terms of ground displacements and machine parameters (over all, front and grouting pressure) allowed to perform several 3D Finite Element Analyses by Plaxis 3D Tunnel.

Looking at the soil parameters influence, main results of the parametric studies can be summarized in the following:

1. as  expected  the  soil  stiffness  mainly  affects  the  volume  loss  and  maximum settlement at the ground surface. Also, it influences the subsidence width in a lesser degree. Nevertheless an increase in the subsidence width is observed for increasing  in  such  a  modulus  (by  increasing  the  stiffness  modulus  the  basin subsidence becomes wider)
2. the  un-reloading  to  loading  stiffness  moduli  ratio  does  not  significantly  affects the ground maximum settlement. An increase in the ratio leads to enlargement of the basin subsidence, thus increasing the volume loss (the higher is the unreloading  stiffness  modulus  with  respect  to  the  loading  one,  the  more  the ground subsidence becomes wider)
3. an  increase  in  the  soil  unit  weight  leads  to  an  increase  in  the  maximum settlement and volume loss, and not in the subsidence width. On the contrary, significant  decrease  in  such  a  parameter  yields  a  shrinkage  of  the  subsidence basin, thus reductions in both the volume loss and the maximum settlement
4. no  clear  relationships  has  been  detected  between  the  friction  angle  and  the dilatancy angle with the volume loss nor with the maximum surface settlement; conversely,  reductions  in  friction  angle  leads  to  a  sort  of  linear  increase  in subsidence width, whereas the dilatancy effect is evident only above a certain value when the subsidence width suddenly increases.

Looking at the pressures effects on the surface volume loss and maximum settlement, the main considerations can be resumed in the ensuing. Clear relationships between such pressures  and  the  induced  surface  volume  loss  and  maximum  settlement  have  been observed.  In  order  to  investigate  the  pressures'influence  also  at  the  tunnel  depth,  the volume  losses  at  that  locations  were  extrapolated,  showing  the  noticeable  influence played  by  low  values  of  the  front  pressures  due  to  a  development  of  an  active  failure mechanism.  On  the  contrary,  with  reference  to  the  grouting  pressure  effects,  results reveal the influence played only on surface volume losses. No effects were detected on the volume loss at the tunnel depth. To this point the main results can be resumed as follows:

1. a  linear  relationship  between  the  grouting  pressure  and  the  effects  on  the ground  surface  can  be  defined,  on  the  opposite  side  a  non-linear  but  clear relation links the front pressure to the same effects

2. the  positive  effect  of  the  front  pressure  on  the  induced  displacements  is evident  up  to  a  certain  value  of  such  a  pressure,  related  to  the  front equilibrium,  after  which  further  increases  leads  to  plasticization  around  the tunnel lining implying later growing in settlements and volume loss
3. the  front  pressure  governs  the  tunnel  front  behaviour  leading  to  active  or passive  failure  mechanism,  thus  strongly  affecting  the  displacements  at  the ground surface
4. the  front  pressure  influence  on  both  the  volume  loss  and  the  maximum settlement at the ground surface, is much more pronounced than the grouting pressure one, up to a certain value, when the observed behaviour changes and the  grouting  pressure  becomes  more  influent  in  reducing  the  tunnelling induced effects
5. looking  at  the  pressures  ratio,  linear  relationships  with  both  the  volume  loss and settlement variations have been detected within a range defined by the minimum and maximum front pressure used.

Due to the large number of influencing factors on the observe behaviour (soil profile, soil properties, constitutive laws, machine parameters, etc.), the back-analysis has been performed necessarily fixing some of the above factors, and changing the others.

For  the  analyses  presented  in  this  thesis,  the  Hardening  Soil  Model  was  used  to numerically simulate the excavation process. The input values of the soil parameters were determined  from  geotechnical  investigation.  The  used  machine  parameters  came  from continuously  monitored  and  recorded  data.  Thus,  the  values  of  volume  loss  at  tunnel depth were defined, and a surface settlement along the tunnel axis was reproduced.

As  general  conclusion,  it  seems  reasonable  to  state  that  the  design  of  tunnel  cannot neglect  (as  usually  done)  technological  factors,  which  have  a  strong  influence  on  the tunnelling induced settlement.

In  other  words,  good  soil  modelling  coupled  with  advances  numerical  analyses,  could give  wrong  results  if  technological  aspects  (grouting  and  front  pressures)  are  not  well considered  at  design  stage  and  not  well  implemented  at  construction  stage.  A  good design is based on a 'right' balance of all above.

## REFERENCES

- Attewell, P. B. (1978). Ground movements caused by tunnelling in soil. Pages 812-
- 948 of: Large ground movements and structures . Pentech Press, London. Attewell,  P.  B.,  Yeates,  J.  and  Selby,  A.  R.  (1986). Soil  movements  induced  by tunnelling and their effects on pipelines and structures . Blackie, Glasgow. Attewell, P.B. and Selby, A.R. (1989). Tunnelling in conpressible soils: Large ground movements  and  structural  implications. Tunnelling  and  Underground  Space Technology, 4 (4) Attewell,  P.  B.    and  Woodman,  J.P.  (1982).  Predicting  the  dynamics  of  ground settlement and its derivatives caused by tunnelling in soil. Ground Engineering, 15 (8), 13-22. Bloodworth  A.  G.  (2002). Three-dimensional  analysis  of  tunnelling  effects  on structures to develop design methods . Thesis (PhD). University of Oxford. Broms,  B.  B.  and  Bennermark,  H.  (1967).  Stability  of  clay  in  vertical  openings. Journal of Soil Mechanics and Foundations, ASCE, 193, 71-94. Davis, E. H., Gunn, M. J., Mair, R. J. and Seneviratne, H. N. (1980). The stability of shallow tunnels and underground openings in choesive material. Géotechnique , 30(4), 397-416. Franzius, J. N. (2003). Behavioue of buildings due to tunnl induced subsidence . Thesis (PhD). Imperial College, University of London. Lake,  L.  M.,  Rankin,  W.  J.  and  Hawley,  J.  (1992). Prediction  and  effects  of  ground movements  caused  by  tunnelling  in  soft  ground  beneath  urban  areas .  CIRIA Funders Report / CP / 5. Macklin, S. R. and Field, G. R. (1999). The response of London clay to full-face TBM tunnelling at West Ham, London. In: Proc. Int. Conf. On Urban Ground Engineering , Hong Kong, 11-12 November 1998. London: Thomas Telford .  Thesis
- Mair,  R.  J.  (1979). Centrifugal  modelling  of  tunnel  construction  in  soft  clay (PhD). University of Cambridge.
- Mair, R. J. and Taylor, R. N. (1993). Prediction of clay behaviour around tunnel using Memorial

plasticity solutions. In: Predictive Soil Mechanics: Proc. Wroth Symposium , Oxford, 27-29 July 1992. London: Thomas Telford, 449-463. Morton, K. and Au, E. (1975). Settlement observation on eight structures in London. In:  Proc. Conf. Settlement of Structures ,  Cambridge, April 1974. London: Pentech Press, 183-203. O'Reilly, M. P. and New, B. (1982). Settlements above tunnels in the United Kingdom - their magnitude and prediction. In. Proc. Int. Symposium Tunnelling '82 , London: 7-11 June. London: Institution of Mining and Metallurgy, 173-181. Nyren, R.  J.  (1998).  Field  measurements  above  twin  tunnels  in  London  clay.  Thesis (PhD). Imperial College, University of London. Peck, R. B. (1969). Deep excavation and tunnelling in soft ground. In: Proc. 7 th ICSMFE, State-of-the-art Volume , Mexico City. Mexico: Sociedad Mexicana de Mecànica de Suelos, 225-290. Peck &amp; Schmid (1960 Simons, N. E. and Som, N. N. (1970). Settlements of structures on clay with particular emphasis on London clay . CIRIA Report 22.

## APPENDIX

i

## APPENDIX II

## SITE AND LABORATORY INVESTIGATIONS

## INVESTIGATION CAMPAIGN 1990

| BOREHOLE   | GROUND LEVEL   | DEPTH   | SAMPLES   | SPT   | GROUNDWATER   | GROUNDWATER   | TUFF   | TUFF         |
|------------|----------------|---------|-----------|-------|---------------|---------------|--------|--------------|
| BOREHOLE   | [m a.m.s.l.]   | [m]     | [N°]      | SPT   | [m a.m.s.l.]  | [m]           | [m]    | [m a.m.s.l.] |
| B52        | 2.3            | 17.00   |           | 5     |               |               |        |              |
| B54        | 2.3            | 30.00   |           | 5     |               |               | 24.20  | -21.90       |
| S176       | 2.28           | 25.50   | 3         | 4     |               |               |        |              |
| B55        | 2.28           | 25.00   | 1         | 3     |               |               |        |              |
| S194       | 2.26           | 36.00   | 1         | 3     |               |               | 31.50  | -29.24       |
| B56        | 2.26           | 31.00   |           | 3     |               |               |        |              |
| B190       | 2.4            | 40.00   | 2         | 4     |               |               | 36.20  | -33.80       |
| S114       | 2.55           | 38.00   | 3         | 4     |               |               | 33.00  | -30.45       |
| B81        | 2.7            | 25.00   | 2         | 5     |               |               |        |              |
| B40        | 3.2            | 25.00   |           |       |               |               |        |              |
| B84        | 3.15           | 25.00   | 1         | 1     |               |               | 9.00   | -5.85        |
| S220       | 3.3            | 20.20   |           | 4     |               | 3.4           | 14.50  | -11.20       |
| B85        | 3.2            | 25.00   | 1         | 3     |               |               | 18.00  | -14.80       |
| S222       | 3.18           | 29.00   |           | 7     |               | 3.4           | 24.00  | -20.82       |
| B86        | 3.2            | 25.00   | 1         | 5     |               |               |        |              |
| S227       |                | 31.00   | 1         | 8     |               | 1.8           |        |              |
| B87        | 3.4            | 25.00   | 1         | 5     |               |               |        |              |
| S196       | 2.3            | 39.50   | 2         | 4     |               |               |        |              |
| S197       | 2.3            | 39.50   |           | 5     |               |               |        |              |
| S198       | 2.3            | 45.00   | 1         | 5     |               |               | 40.20  | -37.90       |
| S199       | 2.3            | 45.00   | 1         | 5     |               |               | 38.50  | -36.20       |
| B88        | 3.4            | 25.00   | 1         | 5     |               |               |        |              |
| B89        | 3.4            | 26.50   | 1         | 5     |               |               |        |              |
| B90        | 3.6            | 25.00   | 2         | 5     |               |               |        |              |
| B91        | 3.7            | 26.00   | 2         | 5     |               |               |        |              |
| S211       | 3.6            | 50.00   |           | 5     |               |               |        |              |
| S208       | 3.6            | 50.00   | 1         | 5     |               |               |        |              |
| S200       | 3.6            | 50.00   |           | 5     |               |               |        |              |
| S210       | 3.6            | 50.00   |           | 5     |               |               |        |              |
| A3         | 3.302          | 7.00    |           |       |               | 2.2           |        |              |
| A1         | 3.329          | 15.50   |           |       |               | 2.5           |        |              |
| S101       | 3.6            |         |           |       |               |               | 36.90  | -33.30       |
| B1         | 3.329          |         |           | 6     |               | 3.3           | 28.50  | -25.17       |
| A4         | 3.518          | 7.00    |           |       |               | 2.6           |        |              |
| S102       | 3.64           |         |           |       |               |               | 25.20  | -21.56       |

Tab.II-1. Site investigation from 1990

| B2      |   3.812 |   25.00 | 5   |   5 |   20.00 |   -16.19 |
|---------|---------|---------|-----|-----|---------|----------|
| B3      |   3.891 |   20.00 |     |   3 |   15.50 |   -11.61 |
| S106    |    5.03 |         |     | 3.6 |   11.90 |    -6.87 |
| A5      |   5.426 |   14.00 |     |   4 |    7.00 |    -1.57 |
| B4      |   4.687 |   12.00 |     | 4.5 |    4.00 |     0.69 |
| A6      |    5.02 |   15.00 |     | 3.8 |    3.00 |     2.02 |
| B5      |   5.349 |   11.00 |     |   3 |    3.00 |     2.35 |
| S103    |    3.66 |   26.00 |     |   3 |   18.40 |   -14.74 |
| S105bis |    6.23 |   40.80 |     | 4.5 |   36.50 |   -30.27 |
| S104    |     3.7 |   20.40 |     | 3.1 |   17.80 |   -14.10 |

Tab.II-2. CPT from the site investigation campaign in 1990

| CPT    |   GROUND LEVEL [m a.m.s.l.] |   DEPTH [m] |
|--------|-----------------------------|-------------|
| CPT 82 |                           3 |       29.20 |
| CPT 83 |                         3.2 |       29.20 |
| CPT 86 |                         3.2 |       25.00 |
| CPT 88 |                         3.4 |       24.20 |
| CPT 90 |                         3.6 |       24.80 |

| BOREHOLE   |   N° |   DEPTH [m] | SOIL         |     W |    [kN/m 3 ] |     S |    S [kN/m 3 ] | K [cm/sec]   | TESTS    |    ' 3 [kPa] |    1 -  3 [kPa] |
|------------|------|-------------|--------------|-------|-----------------|-------|-----------------|--------------|----------|---------------|-------------------|
| S176       |    1 |        7.25 | SAND         | 0.362 |            17.1 | 0.941 |           12.55 |              | TRIAXIAL |            75 |               536 |
|            |      |        7.25 |              |  0.63 |           15.43 | 0.863 |           10.55 |              |          |           150 |               751 |
|            |      |        7.25 |              | 0.389 |           15.53 | 0.908 |           11.89 |              |          |           300 |              1402 |
| S176       |    2 |       16.25 | PIROCLASTITI |  0.38 |           15.94 | 0.943 |           12.27 |              | TRIAXIAL |           150 |               886 |
|            |      |       16.25 |              | 0.382 |           17.05 | 0.958 |           12.23 |              |          |           300 |              1624 |
|            |      |       16.25 |              | 0.384 |           17.88 | 0.963 |           12.34 |              |          |           450 |              2117 |
| S176       |    3 |       22.25 | PIROCLASTITI | 0.302 |           17.83 | 0.943 |            13.7 |              |          |               |                   |
|            |      |       22.25 |              | 0.379 |           16.76 | 0.918 |           12.16 |              | TRIAXIAL |           200 |               909 |
|            |      |       22.25 |              | 0.379 |           16.89 | 0.911 |            12.1 |              |          |           350 |              1476 |
|            |      |       22.25 |              | 0.386 |            16.4 | 0.887 |           11.84 |              |          |           500 |              1851 |
| B55        |    1 |       15.75 | PIROCLASTITI | 0.491 |           16.52 | 0.993 |           11.08 |              |          |               |                   |
| PP55       |    1 |        8.45 | CINERITE     | 0.495 |           16.64 |     1 |           11.13 |              |          |               |                   |
|            |      |        8.45 |              | 0.471 |            16.6 | 0.975 |           11.29 |              | TRIAXIAL |            80 |               367 |
|            |      |        8.45 |              | 0.477 |           16.49 | 0.968 |           11.16 |              |          |           150 |               793 |
|            |      |        8.45 |              | 0.491 |           16.51 | 0.983 |           11.07 |              |          |           300 |              1602 |
| S194       |    1 |        26.3 | PIROCLASTITI | 0.276 |           17.55 |  0.88 |           13.75 |              |          |               |                   |
|            |      |        26.3 |              | 0.288 |           17.38 | 0.878 |           13.49 |              | TRIAXIAL |           200 |              1225 |
|            |      |        26.3 |              | 0.271 |           17.87 |  0.91 |           14.05 |              |          |           300 |              1699 |
|            |      |        26.3 |              |  0.27 |           17.66 | 0.883 |            13.9 |              |          |           400 |              2233 |
| S190       |    1 |         8.7 | CINERITE     | 0.324 |           18.05 |     1 |           13.63 |              |          |               |                   |
|            |      |         8.7 |              | 0.325 |           18.03 |     1 |            13.6 |              | TRIAXIAL |           100 |               404 |

|      |    |    8.7 |              |   0.309 |   18.21 |     1 |   13.9 |          |   200 | 846      | 846      |
|------|----|--------|--------------|---------|---------|-------|--------|----------|-------|----------|----------|
|      |    |    8.7 |              |   0.337 |   17.87 | 0.995 |  13.36 |          |   300 | 1177     | 1177     |
|      |  2 |   23.3 | PIROCLASTITI |   0.468 |   15.81 | 0.902 |  10.77 | TRIAXIAL |   200 | 859      | 859      |
|      |    |   23.3 |              |   0.457 |   16.32 | 0.947 |   11.2 |          |   300 | 1602     | 1602     |
|      |    |   23.3 |              |   0.434 |   16.24 | 0.917 |  11.32 |          |   400 | 1890     | 1890     |
| S114 |  1 |   5.25 | SAND         |   0.299 |   17.45 | 0.791 |  13.44 |          |       |          |          |
|      |  2 |   23.3 | PIROCLASTITI |   0.587 |   14.02 | 0.811 |   8.83 |          |       |          |          |
|      |  3 |  30.45 | PIROCLASTITI |   0.312 |   16.22 | 0.749 |  12.36 |          |       |          |          |
|      |    |  30.45 |              |   0.323 |   16.66 | 0.803 |   12.6 | TRIAXIAL |   300 | 1554     | 1554     |
|      |    |  30.45 |              |   0.362 |   16.47 | 0.833 |  12.89 |          |   400 | 1922     | 1922     |
|      |    |  30.45 |              |   0.371 |   16.79 | 0.874 |  12.25 |          |   500 | 2259     | 2259     |
| B81  |  2 |  20.25 | PIROCLASTITI |   0.561 |   15.41 | 0.936 |   9.87 |          |       |          |          |
|      |    |  20.25 |              |   0.523 |    15.8 |  0.95 |  10.37 | TRIAXIAL |   200 | 876      | 876      |
|      |    |  20.25 |              |   0.536 |   15.76 | 0.955 |  10.27 |          |   350 | 1453     | 1453     |
|      |    |  20.25 |              |   0.756 |   15.02 |     1 |   8.56 |          |   500 | 2044     | 2044     |
| B82  |  2 |   15.3 | PIROCLASTITI |   0.532 |   15.13 | 0.882 |   9.87 |          |       |          |          |
|      |    |        |              |   0.512 |         |       |        |          |       |          |          |
|      |    |   15.3 |              |         |   15.85 | 0.941 |  10.48 | TRIAXIAL |   100 | 492      | 492      |
|      |    |   15.3 |              |   0.562 |   15.64 | 0.955 |  10.02 |          |   250 | 1046     | 1046     |
|      |    |   15.3 |              |   0.489 |   16.04 | 0.942 |  10.77 |          |   400 | 1659     | 1659     |
|      |    |   15.3 |              |   0.631 |   15.62 | 0.997 |   9.58 | TRIAXIAL |   100 | 384      | 384      |
|      |    |   15.3 |              |   0.602 |   15.61 | 0.979 |   9.74 |          |   250 | 842      | 842      |
|      |    |   15.3 |              |   0.604 |   15.71 |  0.99 |   9.79 |          |   400 | 1290     | 1290     |
|      |  3 | 20.225 |              |   0.542 |   16.18 | 0.998 |  10.49 |          |       |          |          |
|      |    | 20.225 | PIROCLASTITI |   0.526 |   15.83 | 0.949 |  10.37 | TRIAXIAL |   200 | 845      | 845      |
|      |    | 20.225 |              |   0.498 |   16.01 | 0.947 |  10.69 |          |   350 | 1237     | 1237     |
|      |    | 20.225 |              |   0.517 |    15.9 |  0.95 |  10.48 |          |       | 500 1868 | 500 1868 |
| B83  |  1 |  15.25 | PIROCLASTITI |   0.292 |   16.32 | 0.762 |  12.63 |          |       |          |          |
|      |    |  15.25 |              |   0.339 |   15.92 | 0.782 |  11.89 | TRIAXIAL |   150 | 699      | 699      |
|      |    |  15.25 |              |   0.288 |   16.01 | 0.726 |  12.43 |          |   300 | 1300     | 1300     |
|      |    |  15.25 |              |   0.331 |   16.05 | 0.786 |  12.06 |          |   450 | 1954     | 1954     |
| B84  |  1 |   6.75 | CINERITE     |   0.378 |   16.72 | 0.866 |  12.13 | 1.6E-03  |       |          |          |
| B85  |  1 |  15.25 | CINERITE     |   0.218 |   19.51 |     1 |  16.02 | TRIAXIAL |   100 | 616      | 616      |
|      |    |  15.25 |              |   0.211 |   19.61 |     1 |   16.2 |          |   250 | 1339     | 1339     |
|      |    |  15.25 |              |   0.235 |   19.25 |     1 |  15.58 |          |       | 400 2273 | 400 2273 |
| B86  |  1 |   14.2 | SAND         |   0.321 |   17.52 | 0.843 |  13.27 | 1.4E-05  |       |          |          |
| B87  |  1 |  11.45 | SAND         |   0.489 |   16.38 | 0.924 |     11 | 7.0E-03  |       |          |          |
| S196 |  1 |  15.75 | SAND         |   0.231 |   19.24 | 0.938 |  15.63 |          |       |          |          |
|      |    |  15.75 |              |    0.23 |   19.49 | 0.967 |  15.85 | TRIAXIAL |   150 | 968      | 968      |
|      |    |  15.75 |              |   0.233 |   19.55 | 0.984 |  15.85 |          |   300 | 1674     | 1674     |
|      |    |  15.75 |              |   0.231 |   19.51 | 0.975 |  15.84 |          |   450 | 2497     | 2497     |
|      |  2 |   23.7 | PIROCLASTITI |   0.361 |   17.43 | 0.956 |  12.81 |          |       |          |          |
|      |    |   23.7 |              |   0.374 |   16.78 |   0.9 |  12.21 | TRIAXIAL |   200 | 686      | 686      |
|      |    |   23.7 |              |   0.366 |   17.14 |  0.93 |  12.55 |          |   300 | 997      | 997      |
|      |    |   23.7 |              |   0.351 |   17.08 | 0.905 |  12.65 |          |   400 |          | 1350     |
| S198 |  1 |  24.75 | PIROCLASTITI |   0.348 |   17.11 | 0.897 |  12.69 |          |       |          |          |
|      |    |  24.75 |              |   0.356 |   17.22 | 0.919 |  12.71 | TRIAXIAL |   200 | 714      | 714      |
|      |    |  24.75 |              |   0.354 |   17.15 | 0.908 |  12.67 |          |   300 | 1003     | 1003     |
|      |    |  24.75 |              |   0.342 |   17.25 | 0.905 |  12.86 |          |       | 400      | 1536     |
| B88  |  1 |   10.2 | SAND         |   0.267 |   18.72 |     1 |  14.78 | 3.7E-05  |       |          |          |

Tab.II-3. Laboratory tests on loose soils from investigation campaign in 1990

| B90   |   1 |   10.3 | SAND         |   0.265 |   19.04 |   0.902 |   15.05 |   3.4E-03 |
|-------|-----|--------|--------------|---------|---------|---------|---------|-----------|
|       |   2 |  20.15 | SAND         |    0.41 |   16.71 |   0.917 |   11.85 |   3.7E-05 |
| B91   |   1 |    5.2 | SAND         |   0.307 |   16.78 |   0.757 |   12.84 |   1.8E-03 |
| S208  |   1 |  25.75 | PIROCLASTITI |   0.335 |   17.32 |   0.927 |   12.97 |           |
|       |     |  25.75 |              |   0.347 |   17.29 |    0.94 |   12.84 |           |
|       |     |  25.75 |              |   0.461 |   16.73 |   0.994 |   11.45 |           |
|       |     |  25.75 |              |   0.449 |   16.77 |   0.989 |   11.58 |           |

## INVESTIGATION CAMPAIGN 1998 - 2000

Tab.II-4. Site investigation between 1998 and 2000

| BOREHOLE   | GROUND LEVEL [m a.m.s.l.]   | DEPTH [m]   | SPT   | GROUNDWATER   | GROUNDWATER   | TUFF   | TUFF         |
|------------|-----------------------------|-------------|-------|---------------|---------------|--------|--------------|
| BOREHOLE   | GROUND LEVEL [m a.m.s.l.]   | DEPTH [m]   | [m    | a.m.s.l.]     | [m]           | [m]    | [m a.m.s.l.] |
| T0         | 22.5                        | 29.8        | 8     | 5.5           | 17            |        |              |
| T1         | 22.3                        | 30          | 8     | 4.8           | 17.5          |        |              |
| T2         | 25                          | 30          | 8     | 5.5           | 19.5          |        |              |
| T3         | 24                          | 30          | 8     | 6             | 18            |        |              |
| P0         | 2.7                         | 31          | 5     | 1.7           | 1             | 30.5   | -27.8        |
| P1         | 2.1                         | 34.5        | 5     | 1             | 1.1           | 30.7   | -28.6        |
| P2         | 2.2                         | 35.5        | 6     | 1.1           | 1.1           | 30.4   | -28.2        |
| P3         | 2.6                         | 35          | 6     | 0.9           | 1.7           |        |              |
| P4         | 2.6                         | 35          | 6     | 0.9           | 1.7           |        |              |
| P5         | 2.6                         | 59          |       | 1.1           | 1.5           | 41.5   | -38.9        |
| F1         | 14.6                        | 40          |       | 0.8           | 13.8          | 5.8    | 8.8          |
| F2         | 14.8                        | 40          |       | 0.9           | 13.9          | 7.8    | 7            |
| F3         | 41.5                        | 60          |       | 1.5           | 40            | 18.9   | 22.6         |
| F4         | 35.2                        | 60          |       | 1.7           | 33.5          | 17.6   | 17.6         |
| F5         | 30.7                        | 40          |       | 1.7           | 29            | 16     | 14.7         |
| F6         | 23.7                        | 30          |       | -1.3          | 25            | 14.2   | 9.5          |
| F7         | 19                          | 40          |       | 4             | 15            | 16     | 3            |
| F8         | 16.3                        | 50          |       | 2.8           | 13.5          | 13.3   | 3            |
| F9         | 21.8                        | 26.5        |       |               |               | 23.5   | -1.7         |
| F10        | 20                          | 19.1        |       |               |               | 13     | 7            |
| F11        | 19.1                        | 18.2        |       |               |               | 14     | 5.1          |
| F12        | 23.5                        | 15.5        |       | 11.8          | 11.7          | 10.2   | 13.3         |
| F13        | 32.2                        | 28.7        |       |               |               | 22.9   | 9.3          |
| F14        | 10.8                        | 12.5        |       |               |               | 8      | 2.8          |

Tab.II-5. CPT from the site investigation campaign between 1998 and 2000

| CPT   | LOCATION     |   GROUND LEVEL [m a.m.s.l.] |   DEPTH [m] |
|-------|--------------|-----------------------------|-------------|
| PP0   | Arco Mirelli |                        2.70 |          32 |
| PP1   | Arco Mirelli |                        2.10 |          32 |
| PP2   | Arco Mirelli |                        2.20 |        25.2 |
| PP3   | San Pasquale |                        2.60 |          35 |
| PP4   | San Pasquale |                        2.60 |          35 |
| PP5   | San Pasquale |                        2.60 |       43.60 |

Tab.II-6. Piezometers from the site investigation campaign between 1998 and 2000

| PIEZOMETER   | LOCATION                             | GROUND LEVEL [m a.m.s.l.]   | DEPTH [m]   | GROUNDWATER LEVEL   | GROUNDWATER LEVEL   |
|--------------|--------------------------------------|-----------------------------|-------------|---------------------|---------------------|
| PIEZOMETER   | LOCATION                             | GROUND LEVEL [m a.m.s.l.]   | DEPTH [m]   | [m a.m.s.l.]        | [m]                 |
| Ma           | Riviera di Chiaia - Via Arco Mirelli | 2.00                        | 29.20       | 0.8                 | 1.20                |
| Mb           | Vico delle fiorentine a Chiaia       | 11.70                       | 40          | 10.30               | 1.40                |
| Mc           | Via Andrea d'Isernia                 | 24.30                       | 40          | 22.30               | 2.00                |
| Sa           | Riviera di Chiaia - Rone Sirignano   | 2.30                        | 40          | 1.28                | 1.02                |
| Sb           | fine Rione Siringano                 | 6.80                        | 20          | 5.35                | 1.45                |
| Sc           | Via Martucci - Gradini dei Nobili    | 17.30                       | 22          | 15.44               | 1.86                |
| Ca           | Riviera di Chiaia - Via Carducci     | 2.30                        | 10          | 1.31                | 0.99                |
| Cb           | Via Carducci - Via Cuoco             | 5.20                        | 14          | 4.18                | 1.02                |
| Cc           | Via Carducci - Via Torelli           | 10.00                       | 50          | 9.04                | 0.96                |
| Cd           | Via Carducci - Via dei Mille         | 17.25                       | 50          | 15.85               | 1.40                |
| Va           | Riviera di Chiaia - via Satriano     | 2.50                        | 57          | 1.94                | 0.56                |
| Vb           | Via Bisignano -Vico Sospiri          | 7.40                        | 30          | 6.32                | 1.08                |
| Vc           | Via Bisignano -via Cavallerizza      | 10.40                       | 30          | 9.38                | 1.02                |

Tab.II-7. Permeability tests (Lefranc) from the site investigation campaign 1998 - 2000

| BOREHOLE   | TESTING STRETCH [m below ground level]   | SOIL         |   K [cm /sec] |
|------------|------------------------------------------|--------------|---------------|
| P1         | 18.50 - 20.00                            | PIROCLASTITI |      2.76E-05 |
| P2         | 10.70 - 11.70                            | SAND         |      1.22E-05 |
| P2         | 14.40 - 16.30                            | PIROCLASTITI |      6.11E-05 |
| P2         | 21.50 - 23.00                            | PIROCLASTITI |      2.16E-05 |
| P3         | 9.00 - 10.00                             | SAND         |      5.81E-05 |
| P3         | 15.00 - 16.50                            | SAND         |      1.03E-04 |
| P3         | 21.50 - 23.00                            | PIROCLASTITI |      6.41E-05 |
| P4         | 9.00 - 10.00                             | SAND         |      8.37E-05 |
| P4         | 14.60 - 16.50                            | SAND         |      4.99E-05 |
| P4         | 21.00 - 22.50                            | PIROCLASTITI |      5.19E-06 |
| P5         | 15.50 - 16.20                            | SAND         |      6.40E-05 |
| P5         | 22.00 - 23.00                            | SAND         |      6.43E-06 |
| P5         | 42.00 - 44.00                            | TUFF         |      2.14E-05 |
| F1         | 13.00 -14.50                             | TUFF         |      1.03E-04 |
| F1         | 19.20 - 21.00                            | TUFF         |      6.46E-05 |
| F2         | 14.00 - 15.50                            | TUFF         |      1.07E-04 |
| F2         | 20.00 - 21.00                            | TUFF         |      2.59E-04 |

Tab.II-8. Laboratory tests on Tuff from investigation campaign in 1998 -2000

| BOREHOLE   |   SAMPLE | DEPTH [m]   |    [kN/m 3 ] |    S [kN/m 3 ] |   UNIAXAL COMPRESSIVE STRENGHT [MPa] |
|------------|----------|-------------|---------------|-----------------|--------------------------------------|
| F6         |        1 | 14.00-14.35 |          1.62 |            1.32 |                                 3.86 |
|            |        2 | 14.35-14.72 |          1.60 |            1.31 |                                 3.96 |
|            |        3 | 15.00-15.39 |          1.70 |            1.38 |                                 4.65 |
|            |        4 | 19.50-19.90 |          1.73 |            1.41 |                                 5.06 |
|            |        5 | 19.90-20.25 |          1.71 |            1.40 |                                 5.89 |
|            |        6 | 21.20-21.50 |          1.69 |            1.39 |                                 7.16 |
|            |        7 | 21.50-21.80 |          1.78 |            1.42 |                                  7.2 |
|            |        8 | 22.00-22.30 |          1.76 |            1.38 |                                 8.99 |
|            |        9 | 22.30-22.70 |          1.73 |            1.43 |                                 8.62 |
|            |       10 | 23.75-23.95 |          1.67 |            1.41 |                                 3.63 |
|            |       11 | 25.65-26.00 |          1.76 |            1.40 |                                 4.55 |
|            |       12 | 28.35-28.70 |          1.71 |            1.38 |                                 2.78 |
|            |       13 | 29.30-30.00 |          1.71 |            1.38 |                                 4.12 |
| F1         |        1 | 10.10-10.50 |          1.71 |            1.39 |                                 5.69 |
|            |        2 | 10.70-11.20 |          1.74 |            1.38 |                                 5.87 |
|            |        3 | 11.40-11.85 |          1.70 |            1.40 |                                 5.11 |
|            |        4 | 14.00-14.50 |          1.70 |            1.41 |                                 5.83 |
|            |        5 | 16.70-17.00 |          1.71 |            1.41 |                                 7.13 |
|            |        6 | 19.32-19.62 |          1.66 |            1.38 |                                 3.71 |
|            |        7 | 22.30-22.70 |          1.68 |            1.40 |                                 4.17 |
|            |        8 | 23.03-23.38 |          1.77 |            1.40 |                                 3.51 |
|            |        9 | 24.00-24.29 |          1.69 |            1.37 |                                 3.24 |
|            |       10 | 25.60-26.00 |          1.72 |            1.40 |                                 2.95 |
|            |       11 | 27.80-28.01 |          1.77 |            1.39 |                                 3.80 |
|            |       12 | 28.75-29.05 |          1.65 |            1.38 |                                 2.78 |
|            |       13 | 31.00-31.65 |          1.70 |            1.38 |                                 4.08 |
|            |       14 | 33.30-33.60 |          1.75 |            1.40 |                                 5.74 |
|            |       15 | 35.50-35.80 |          1.78 |            1.42 |                                 3.23 |
| F2         |        1 | 17.75-18.00 |          1.62 |            1.32 |                                 2.58 |
|            |        2 | 19.00-19.22 |          1.60 |            1.31 |                                 3.17 |
|            |        3 | 23.30-23.60 |          1.56 |            1.36 |                                 1.90 |
|            |        4 | 23.80-24.15 |          1.67 |            1.37 |                                 3.19 |
|            |        5 | 24.15-26.25 |          1.62 |            1.35 |                                 2.46 |
|            |        6 | 26.25-26.55 |          1.79 |            1.38 |                                 4.40 |
|            |        7 | 26.55-26.85 |          1.71 |            1.38 |                                 4.13 |
|            |        8 | 27.00-27.31 |          1.78 |            1.39 |                                 4.59 |
|            |        9 | 29.50-29.81 |          1.77 |            1.39 |                                 5.00 |
|            |       10 | 30.10-30.50 |          1.74 |            1.40 |                                 8.86 |
|            |       11 | 30.80-31.28 |          1.69 |            1.40 |                                 3.03 |
|            |       12 | 32.77-33.20 |          1.71 |            1.35 |                                 1.96 |

## INVESTIGATION CAMPAIGN 2005

Tab.II-9. Arco Mirelli Station: site investigation in 2005

| BOREHOLE   | GROUND LEVEL [m a.m.s.l.]   | DEPTH [m]   | SPT   | GROUNDWATER [m a.m.s.l.]   | TUFF   | TUFF         |
|------------|-----------------------------|-------------|-------|----------------------------|--------|--------------|
| BOREHOLE   | GROUND LEVEL [m a.m.s.l.]   | DEPTH [m]   | SPT   | GROUNDWATER [m a.m.s.l.]   | [m]    | [m a.m.s.l.] |
| S1         | 2.13                        | 45.0        | 10    | 1.2                        | 33.20  | -31.07       |
| S2         | 2.08                        | 40.5        | 8     | 1.2                        | 30.50  | -28.42       |
| SG1        | 2.11                        | 37          | 9     | 1.2                        | 29.20  | -27.09       |
| SG2        | 2.13                        | 37.40       | 8     | 1.2                        | 32.40  | -30.27       |
| SG3        | 2.12                        | 35          | 7     | 1.2                        | 30.90  | -28.78       |
| SG4        | 2.16                        | 35          | 8     | 1.2                        | 30.70  | -28.54       |
| SG5        | 2.41                        | 40          | 9     | 1.2                        | 34.80  | -32.39       |
| SG6        | 2.23                        | 35.80       | 7     | 1.2                        | 30.70  | -28.47       |
| SG7        | 2.04                        | 35          | 8     | 1.2                        | 29.70  | -27.66       |
| SG8        | 2.09                        | 34          | 8     | 1.2                        | 29.30  | -27.21       |

Tab.II-10. San Pasquale Station: site investigation in 2005

| BOREHOLE   | GROUND LEVEL [m a.m.s.l.]   | DEPTH [m]   | SPT   | GROUNDWATER [m a.m.s.l.]   | TUFF   | TUFF         |
|------------|-----------------------------|-------------|-------|----------------------------|--------|--------------|
| BOREHOLE   | GROUND LEVEL [m a.m.s.l.]   | DEPTH [m]   | SPT   | GROUNDWATER [m a.m.s.l.]   | [m]    | [m a.m.s.l.] |
| S1         | 2.23                        | 44.5        | 8     | 1.2                        | 34.2   | -31.97       |
| S2         | 2.06                        | 45          | 9     | 1.2                        | 41     | -38.94       |
| SG1        | 2.27                        | 45          | 9     | 1.2                        | 40.7   | -38.43       |
| SG2        | 2.27                        | 49          | 9     | 1.2                        | 44.5   | -42.23       |
| SG3        | 2.27                        | 52.5        | 9     | 1.2                        | 47.5   | -45.23       |
| SG4        | 2.29                        | 43          | 8     | 1.2                        | 38     | -35.71       |
| SG5        | 2.03                        | 41          | 8     | 1.2                        | 36     | -33.97       |
| SG6        | 2.37                        | 45          |       | 1.2                        | 40     | -37.63       |
| SG7        | 2.29                        | 41.5        | 8     | 1.2                        | 36.5   | -34.21       |
| SG8        | 2.01                        | 50          | 9     | 1.2                        | 45.5   | -43.49       |

Tab.II-11. Chiaia Station: site investigation in 2005

| BOREHOLE   | GROUND LEVEL [m a.m.s.l.]   | DEPTH [m]   | SPT   | GROUNDWATER [m a.m.s.l.]   | TUFF   | TUFF         |
|------------|-----------------------------|-------------|-------|----------------------------|--------|--------------|
| BOREHOLE   | GROUND LEVEL [m a.m.s.l.]   | DEPTH [m]   | SPT   | GROUNDWATER [m a.m.s.l.]   | [m]    | [m a.m.s.l.] |
| S1         |                             |             |       |                            |        |              |
| S1bis      |                             | 35          | 2     |                            | 16     |              |
| S2         |                             | 26          | 6     |                            | 21.5   |              |
| S3         |                             | 15          | 3     |                            |        |              |
| S4         |                             | 15          | 3     |                            |        |              |
| SG1        |                             | 27          | 5     |                            | 22.5   |              |
| SG2        |                             | 22          | 5     |                            | 17.10  |              |

Tab.II-12. Arco Mirelli Station: SPT from the site investigation campaign in 2005

<!-- image -->

Scatter plot

Tab.II-13. Arco Mirelli Station: permeability tests (Lugeon) from the site investigation campaign in 2005

| BOREHOLE   | TESTING STRETCH [m a.m.s.l.]   | SOIL   |   K [cm/sec] |
|------------|--------------------------------|--------|--------------|
| S1         | 33.50-35.50                    | TUFF   |     1.93E-05 |
| S1         | 35.50-37.50                    | TUFF   |     7.87E-06 |
| S1         | 37.80-39.80                    | TUFF   |     8.67E-06 |
| S1         | 40.30-42.30                    | TUFF   |     1.42E-04 |
| S1         | 42.50-44.50                    | TUFF   |     1.23E-04 |
| S2         | 30.50-32.50                    | TUFF   |     3.15E-06 |
| S2         | 32.50-34.50                    | TUFF   |     4.50E-07 |
| S2         | 34.50-36.50                    | TUFF   |     8.84E-07 |
| S2         | 36.50-38.50                    | TUFF   |     1.33E-06 |
| S2         | 38.50-40.50                    | TUFF   |     1.68E-06 |

<!-- image -->

Scatter plot

45

Tab.II-14. San Pasquale Station: SPT from the site investigation campaign in 2005

| BOREHOLE   | TESTING STRETCH [m a.m.s.l.]   | SOIL   |   K [cm /sec] |
|------------|--------------------------------|--------|---------------|
| S1         | 34.00-36.00                    | TUFF   |      1.66E-04 |
| S1         | 36.20-38.20                    | TUFF   |      1.53E-05 |
| S1         | 38.50-40.50                    | TUFF   |      4.38E-05 |
| S1         | 40.30-42.50                    | TUFF   |      4.22E-05 |
| S1         | 42.50-44.50                    | TUFF   |      5.18E-05 |
| S2         | 41.50-43.50                    | TUFF   |      8.40E-05 |
| S2         | 43.50-45.50                    | TUFF   |      2.03E-05 |
| S2         | 45.50-47.50                    | TUFF   |      2.28E-05 |
| S2         | 47.50-49.50                    | TUFF   |      3.86E-05 |

Tab.II-15. San Pasquale Station: permeability tests (Lugeon) from the site investigation campaign in 2005

<!-- image -->

Scatter plot

20

Tab.II-16. Chiaia Station: SPT from the site investigation campaign in 2005

## APPENDIX III

| DATE            |   EXCAVATION [m] | TUNNEL PRODUCTION/ DAY [m]   | TOTAL TUNNEL PRODUCTION [m]   | LINING SEGMENTS [m] N° [m]   |   LINING SEGMENTS/DAY N° TOTAL LINING SEGMENTS [m] |
|-----------------|------------------|------------------------------|-------------------------------|------------------------------|----------------------------------------------------|
| 7-apr-10        |           292.90 | - -                          | 283.65                        | 1                            |                                                  1 |
| 8-apr-10        |           294.60 | 1.70 1.70                    | 283.65                        | 0                            |                                                  1 |
| 9-apr-10        |           296.30 | 1.70 3.40                    | 287.05                        | 2                            |                                                  3 |
| 12-apr-10       |           298.00 | 1.70                         | 5.10 288.75                   | 1                            |                                                  4 |
| 13-apr-10       |           301.40 | 3.40                         | 8.50 292.90                   | 2                            |                                                  6 |
| 14-apr-10       |           303.10 | 1.70                         | 10.20 294.60                  | 1                            |                                                  7 |
| 15-apr-10       |           304.80 | 1.70                         | 11.90 296.30                  | 1                            |                                                  8 |
| 16-apr-10       |           308.20 | 3.40                         | 15.30 299.70                  | 2                            |                                                 10 |
| 19-apr-10       |           313.30 | 5.10                         | 20.40 304.80                  | 3                            |                                                 13 |
| APRIL 20-apr-10 |           320.10 | 6.80                         | 27.20 311.60                  | 4                            |                                                 17 |
| 21-apr-10       |           326.90 | 6.80                         | 34.00 318.40                  | 4                            |                                                 21 |
| 22-apr-10       |           330.30 | 3.40                         | 37.40 321.80                  | 2                            |                                                 23 |
| 23-apr-10       |           330.80 | 0.50                         | 37.90 322.30                  | 0                            |                                                 23 |
| 26-apr-10       |           337.10 | 6.30                         | 44.20 328.60                  | 4                            |                                                 27 |
| 27-apr-10       |           345.60 | 8.50                         | 52.70 337.10                  | 5                            |                                                 32 |
| 28-apr-10       |           352.40 | 6.80                         | 59.50 343.90                  | 4                            |                                                 36 |
| 29-apr-10       |           360.90 | 8.50                         | 68.00 352.40                  | 5                            |                                                 41 |
| 30-apr-10       |           367.70 | 6.80                         | 74.80 359.20                  | 4                            |                                                 45 |
| 30-apr-10       |           367.70 | 0.00                         | 74.80 359.20                  | 0                            |                                                 45 |
| 3-mag-10        |           376.20 | 8.50 83.30                   | 367.70                        | 5                            |                                                 50 |
| 3-mag-10        |           379.60 | 3.40                         | 86.70 371.10                  | 2                            |                                                 52 |
| 4-mag-10        |           383.00 | 3.40                         | 90.10 374.50                  | 2                            |                                                 54 |
| 5-mag-10        |           386.40 | 3.40                         | 93.50 377.90                  | 2                            |                                                 56 |
| 6-mag-10        |           389.80 | 3.40                         | 96.90 381.30                  | 2                            |                                                 58 |
| 7-mag-10        |           391.50 | 1.70                         | 98.60 383.00                  | 1                            |                                                 59 |
| 10-mag-10       |           401.70 | 10.20                        | 108.80 393.20                 | 6                            |                                                 65 |
| 11-mag-10       |           411.90 | 10.20                        | 119.00 403.40                 | 6                            |                                                 71 |
| 12-mag-10       |           418.70 | 6.80                         | 125.80 410.20                 | 4                            |                                                 75 |
| 13-mag-10       |           432.30 | 13.60                        | 139.40 423.80                 | 8                            |                                                 83 |
| 14-mag-10       |           437.40 | 5.10                         | 144.50 428.90                 | 3                            |                                                 86 |
| MAY 17-mag-10   |           445.90 | 8.50                         | 153.00 437.40                 | 5                            |                                                 91 |
| 18-mag-10       |           457.80 | 11.90                        | 164.90 449.30                 | 7                            |                                                 98 |
| 19-mag-10       |           466.30 | 8.50                         | 173.40 457.80                 | 5                            |                                                103 |
| 20-mag-10       |           473.10 | 6.80                         | 180.20 464.60                 | 4                            |                                                107 |
| 21-mag-10       |           478.20 | 5.10                         | 185.30 469.70                 | 3                            |                                                110 |
| 24-mag-10       |           486.70 | 8.50                         | 193.80 478.20                 | 5                            |                                                115 |
| 25-mag-10       |           488.33 | 1.63                         | 195.43 479.83                 | 1                            |                                                116 |
| 26-mag-10       |           496.83 | 8.50                         | 203.93 488.33                 | 5                            |                                                121 |
| 27-mag-10       |           496.83 | 0.00                         | 203.93 488.33                 | 0                            |                                                121 |
| 28-mag-10       |           496.83 | 0.00                         | 203.93 488.33                 | 0                            |                                                121 |
| 31-mag-10       |           499.50 | 2.67                         | 206.60                        | 491.00 2                     |                                                123 |

Tab.III-1. Tunnel excavation process

|                                                                           | DATE                                                                      | EXCAVATION [m]                                                            | TUNNEL PRODUCTION/ DAY [m]                                                | TOTAL TUNNEL PRODUCTION [m]                                               | LINING SEGMENTS [m]                                                       | N° LINING SEGMENTS/DAY [m]                                                | N° TOTAL LINING SEGMENTS [m]                                              |
|---------------------------------------------------------------------------|---------------------------------------------------------------------------|---------------------------------------------------------------------------|---------------------------------------------------------------------------|---------------------------------------------------------------------------|---------------------------------------------------------------------------|---------------------------------------------------------------------------|---------------------------------------------------------------------------|
|                                                                           | 1-giu-10                                                                  | 500.80                                                                    | 1.30                                                                      | 207.90                                                                    | 492.30                                                                    | 1                                                                         | 123                                                                       |
|                                                                           | 3-giu-10                                                                  | 504.20                                                                    | 3.40                                                                      | 211.30                                                                    | 495.70                                                                    | 2                                                                         | 125                                                                       |
|                                                                           | 4-giu-10                                                                  | 508.30                                                                    | 4.10                                                                      | 215.40                                                                    | 499.80                                                                    | 2                                                                         | 128                                                                       |
|                                                                           | 7-giu-10                                                                  | 510.41                                                                    | 2.11                                                                      | 217.51                                                                    | 501.91                                                                    | 1                                                                         | 129                                                                       |
|                                                                           | 8-giu-10                                                                  | 511.80                                                                    | 1.39                                                                      | 218.90                                                                    | 503.30                                                                    | 1                                                                         | 130                                                                       |
|                                                                           | 9-giu-10                                                                  | 513.70                                                                    | 1.90                                                                      | 220.80                                                                    | 505.20                                                                    | 1                                                                         | 131                                                                       |
|                                                                           | 10-giu-10                                                                 | 514.50                                                                    | 0.80                                                                      | 221.60                                                                    | 506.00                                                                    | 0                                                                         | 131                                                                       |
|                                                                           | 11-giu-10                                                                 | 517.23                                                                    | 2.73                                                                      | 224.33                                                                    | 508.73                                                                    | 2                                                                         | 133                                                                       |
|                                                                           | 14-giu-10                                                                 | 521.72                                                                    | 4.49                                                                      | 228.82                                                                    | 513.22                                                                    | 3                                                                         | 136                                                                       |
|                                                                           | 15-giu-10                                                                 | 522.30                                                                    | 0.58                                                                      | 229.40                                                                    | 513.80                                                                    | 0                                                                         | 136                                                                       |
|                                                                           | JUNE 16-giu-10                                                            | 527.40                                                                    | 5.10                                                                      | 234.50                                                                    | 518.90                                                                    | 3                                                                         | 139                                                                       |
|                                                                           | 17-giu-10                                                                 | 530.83                                                                    | 3.43                                                                      | 237.93                                                                    | 522.33                                                                    | 2                                                                         | 141                                                                       |
|                                                                           | 18-giu-10                                                                 | 535.90                                                                    | 5.07                                                                      | 243.00                                                                    | 527.40                                                                    | 3                                                                         | 144                                                                       |
|                                                                           | 21-giu-10                                                                 | 536.02                                                                    | 0.12                                                                      | 243.12                                                                    | 527.52                                                                    | 0                                                                         | 144                                                                       |
|                                                                           | 22-giu-10                                                                 | 539.33                                                                    | 3.31                                                                      | 246.43                                                                    | 530.83                                                                    | 2                                                                         | 146                                                                       |
|                                                                           | 23-giu-10                                                                 | 542.73                                                                    | 3.40                                                                      | 249.83                                                                    | 534.23                                                                    | 2                                                                         | 148                                                                       |
|                                                                           | 24-giu-10                                                                 | 545.50                                                                    | 2.77                                                                      | 252.60                                                                    | 537.00                                                                    | 2                                                                         | 150                                                                       |
|                                                                           | 28-giu-10                                                                 | 547.40                                                                    | 1.90                                                                      | 254.50                                                                    | 538.90                                                                    | 1                                                                         | 151                                                                       |
|                                                                           | 29-giu-10                                                                 | 547.83                                                                    | 0.43                                                                      | 254.93                                                                    | 539.33                                                                    | 0                                                                         | 151                                                                       |
|                                                                           | 30-giu-10                                                                 | 547.83                                                                    | 0.00                                                                      | 254.93                                                                    | 539.33                                                                    | 0                                                                         | 151                                                                       |
| Stop excavation for no ordinary yard operations in the excavation chamber | Stop excavation for no ordinary yard operations in the excavation chamber | Stop excavation for no ordinary yard operations in the excavation chamber | Stop excavation for no ordinary yard operations in the excavation chamber | Stop excavation for no ordinary yard operations in the excavation chamber | Stop excavation for no ordinary yard operations in the excavation chamber | Stop excavation for no ordinary yard operations in the excavation chamber | Stop excavation for no ordinary yard operations in the excavation chamber |
|                                                                           | 19-lug-10                                                                 | 548.80                                                                    | 0.97                                                                      | 255.90                                                                    | 540.30                                                                    | 1                                                                         | 152                                                                       |
|                                                                           | 19-lug-10                                                                 | 549.55                                                                    | 0.75                                                                      | 256.65                                                                    | 541.05                                                                    | 0                                                                         | 152                                                                       |
|                                                                           | 20-lug-10                                                                 | 550.00                                                                    | 0.45                                                                      | 257.10                                                                    | 541.50                                                                    | 0                                                                         | 152                                                                       |
|                                                                           | 21-lug-10                                                                 | 553.90                                                                    | 3.90                                                                      | 261.00                                                                    | 545.40                                                                    | 2                                                                         | 155                                                                       |
|                                                                           | 22-lug-10                                                                 | 555.10                                                                    | 1.20                                                                      | 262.20                                                                    | 546.60                                                                    | 1                                                                         | 155                                                                       |
|                                                                           | JULY 23-lug-10                                                            | 566.50                                                                    | 11.40                                                                     | 273.60                                                                    | 558.00                                                                    | 7                                                                         | 162                                                                       |
|                                                                           | 27-lug-10                                                                 | 585.23                                                                    | 18.73                                                                     | 292.33                                                                    | 576.73                                                                    | 11                                                                        | 173                                                                       |
|                                                                           | 28-lug-10                                                                 | 593.70                                                                    | 8.47                                                                      | 300.80                                                                    | 585.20                                                                    | 5                                                                         | 178                                                                       |
|                                                                           | 29-lug-10                                                                 | 609.00                                                                    | 15.30                                                                     | 316.10                                                                    | 600.50                                                                    | 9                                                                         | 187                                                                       |
|                                                                           | 30-lug-10 2-ago-10                                                        | 622.73 626.04                                                             | 13.73 3.31                                                                | 329.83 333.14                                                             | 614.23 617.54                                                             | 8 2                                                                       | 195 197                                                                   |
|                                                                           | 3-ago-10                                                                  | 634.00                                                                    | 7.96                                                                      | 341.10                                                                    | 625.50                                                                    | 5                                                                         | 202                                                                       |
|                                                                           | 4-ago-10                                                                  | 644.00                                                                    | 10.00                                                                     | 351.10                                                                    | 635.50                                                                    | 6                                                                         | 208                                                                       |
|                                                                           | 5-ago-10                                                                  | 663.50                                                                    | 19.50                                                                     | 370.60                                                                    | 655.00                                                                    | 11                                                                        | 219                                                                       |
|                                                                           | 6-ago-10                                                                  | 663.50                                                                    | 0.00                                                                      | 370.60                                                                    | 655.00                                                                    | 0                                                                         | 219                                                                       |
|                                                                           | Stop exacavation for vacanties                                            | Stop exacavation for vacanties                                            | Stop exacavation for vacanties                                            | Stop exacavation for vacanties                                            | Stop exacavation for vacanties                                            | Stop exacavation for vacanties                                            | Stop exacavation for vacanties                                            |
|                                                                           | AUGUST 23-ago-10                                                          | 668.53                                                                    | 5.03                                                                      | 375.63                                                                    | 660.03                                                                    | 3                                                                         | 222                                                                       |
|                                                                           | 24-ago-10                                                                 | 682.13                                                                    | 13.60                                                                     | 389.23                                                                    | 673.63                                                                    | 8                                                                         | 230                                                                       |
|                                                                           | 25-ago-10                                                                 | 694.03                                                                    | 11.90                                                                     | 401.13                                                                    | 685.53                                                                    | 7                                                                         | 237                                                                       |
|                                                                           | 26-ago-10                                                                 | 724.23                                                                    | 30.20                                                                     | 431.33                                                                    | 715.73                                                                    | 18                                                                        | 255                                                                       |
|                                                                           | 27-ago-10                                                                 | 709.33                                                                    | -14.90                                                                    | 416.43                                                                    | 700.83                                                                    | -9                                                                        | 246                                                                       |
|                                                                           | 30-ago-10                                                                 | 709.33                                                                    | 0.00                                                                      | 416.43                                                                    | 700.83                                                                    | 0                                                                         | 246                                                                       |
|                                                                           | 31-ago-10                                                                 | 716.13                                                                    | 6.80                                                                      | 423.23                                                                    | 707.63                                                                    | 4                                                                         | 250                                                                       |

## APPENDIX IV

## PARAMETRIC ANALYSES ON STIFFNESS MODULI  (E, Eur)  AND THEIR RATIO (P)

| INPUT PARAMTERS   | INPUT PARAMTERS   | INPUT PARAMTERS   | INPUT PARAMTERS   | INPUT PARAMTERS   | INPUT PARAMTERS   | OUTPUT VALUES   | OUTPUT VALUES   | OUTPUT VALUES   | OUTPUT VALUES   | OUTPUT VALUES   | OUTPUT VALUES   | OUTPUT VALUES   | OUTPUT VALUES   | OUTPUT VALUES   | OUTPUT RESULTS RELATED TO   | OUTPUT RESULTS RELATED TO   | OUTPUT RESULTS RELATED TO   | OUTPUT RESULTS RELATED TO   | OUTPUT RESULTS RELATED TO   | OUTPUT RESULTS RELATED TO   | OUTPUT RESULTS RELATED TO   | OUTPUT RESULTS RELATED TO   | OUTPUT RESULTS RELATED TO   | OUTPUT RESULTS RELATED TO   |
|-------------------|-------------------|-------------------|-------------------|-------------------|-------------------|-----------------|-----------------|-----------------|-----------------|-----------------|-----------------|-----------------|-----------------|-----------------|-----------------------------|-----------------------------|-----------------------------|-----------------------------|-----------------------------|-----------------------------|-----------------------------|-----------------------------|-----------------------------|-----------------------------|
| ANLAYSES          | ANLAYSES          |                   | E                 | E ur              | P=E ur /E         | V L             | [%]             |                 |                 | k = i/Z 0       | k = i/Z 0       | w max [mm]      | w max [mm]      |                 |  E/E rif                   |                            | V L /V L,rif [%]            | V L /V L,rif [%]            | V L /V L,rif [%]            | REFERENCE  k/k rif [%]     | ANALYSES                    |  w max /w max,rif [%]      |  w max /w max,rif [%]      |  w max /w max,rif [%]      |
|                   |                   | ID [kN/m          | 2 ]               | [kN/m 2 ]         | [-]               | Plane O         | Plane U         | Plane AE        | Plane O         | Plane U         | Plane AE        | Plane O Plane   | U Plane AE      | [%]             |                             | Plane O                     | Plane U                     | Plane AE                    |                             | Plane O Plane U             | Plane AE                    | Plane O                     | Plane U                     | Plane AE                    |
| 1                 | HS                | E                 | 6.73E+04          | 2.02E+05          | 3                 | 0.08%           | 0.13%           | 0.14%           | 0.52            | 0.52            | 0.52            | -1.82           | -2.92           | -3.05           | 0%                          | 0%                          | 0%                          | 0%                          | 0%                          | 0%                          | 0% 0%                       |                             | 0%                          | 0%                          |
| 2                 | HSE1              | E 1               | 2.24E+04          | 6.73E+04          | 3                 | 0.23%           | 0.35% 0.34%     |                 | 0.54            | 0.53            | 0.53            | -4.76           | -7.47           | -7.34           | -67%                        | 171%                        | 161%                        | 143%                        | 4%                          | 2%                          | 1%                          | 161%                        | 156%                        | 141%                        |
| 3                 | HSE2              | E 3               | 2.02E+05          | 6.06E+05          | 3                 | 0.04%           | 0.07%           | 0.08%           | 0.57            | 0.56            | 0.57            | -0.80           | -1.36           | -1.55           | 200%                        | -52%                        | -50%                        | -44%                        | 8%                          | 8%                          | 10%                         | -56%                        | -54%                        | -49%                        |
| 4                 | HSE3              | E 2               | 3.37E+04          | 1.01E+05          | 3                 | 0.16%           | 0.24% 0.24%     |                 | 0.53            | 0.52            | 0.53            | -3.37           | -5.26           | -5.28           | -50%                        | 86%                         | 82%                         | 74%                         | 1%                          | 1%                          | 0%                          | 85%                         | 80%                         | 73%                         |
| 5                 | HSE4              | E 4               | 1.35E+05          | 4.04E+05          | 3                 | 0.05%           | 0.08%           | 0.09%           | 0.55            | 0.54            | 0.56            | -1.06           | -1.76           | -1.93           | 100%                        | -39%                        | -37%                        | -33%                        | 5%                          | 4% 6%                       |                             | -42%                        | -40%                        | -37%                        |
| 6                 | HS6Eur            | E                 | 6.73E+04          | 4.04E+05          | 6                 | 0.10%           | 0.16%           | 0.20%           | 0.67            | 0.66            | 0.68            | -1.75           | -2.82           | -3.26           | 0%                          | 23%                         | 23%                         | 40%                         | 28%                         | 27% 31%                     |                             | -4%                         | -3%                         | 7%                          |
| 7                 | HSE16Eur          | E 1               | 2.24E+04          | 1.35E+05          | 6                 | 0.23%           | 0.38%           | 0.44% 0.64      |                 | 0.64            | 0.67            | -4.13           | -6.65           | -7.44           | -67%                        | 177%                        | 182%                        | 213%                        | 22%                         | 24% 28%                     |                             | 126%                        | 128%                        | 144%                        |
| 8                 | HSE26Eur          | E 3               | 2.02E+05          | 1.21E+06          | 6                 | 0.05%           | 0.09%           | 0.11%           | 0.70            | 0.69            | 0.68            | -0.87           | -1.48           | -1.91           | 200%                        | -36%                        | -33%                        | -19%                        | 34%                         | 33% 29%                     |                             | -52%                        | -49%                        | -37%                        |
| 9                 | HSE36Eur          | E 2               | 3.37E+04          | 2.02E+05          | 6                 | 0.18%           | 0.28%           | 0.33%           | 0.68            | 0.67            | 0.69            | -2.96           | -4.78           | -5.42           | -50%                        | 110%                        | 110%                        | 135%                        | 29%                         | 28% 32%                     | 63%                         |                             | 64%                         | 78%                         |
| 10                | HSE46Eur          | E 4               | 1.35E+05          | 8.08E+05          | 6                 | 0.07%           | 0.11%           | 0.13%           | 0.69            | 0.68            | 0.70            | -1.09           | -1.83           | -2.18           | 100%                        | -21%                        | -18%                        | -4%                         | 32%                         | 31% 34%                     |                             | -40%                        | -37%                        | -28%                        |
| 11                | HS9Eur            | E                 | 6.73E+04          | 6.06E+05          | 9                 | 0.11%           | 0.18%           | 0.22%           | 0.68            | 0.71            | 0.70            | -1.83           | -2.83           | -3.59           | 0%                          | 30%                         | 33%                         | 58%                         | 29%                         | 37% 34%                     |                             | 0%                          | -3%                         | 18%                         |
| 12                | HSE19Eur          | E 1               | 2.24E+04          | 2.02E+05          | 9                 | 0.25%           | 0.39%           | 0.48%           | 0.71            | 0.70            | 0.73            | -3.95           | -6.38           | -7.38           | -67%                        | 193%                        | 194%                        | 239%                        | 35% 35%                     | 40%                         |                             | 117%                        | 118%                        | 142%                        |
| 13                | HSE29Eur          | E 3               | 2.02E+05          | 1.82E+06          | 9                 | 0.06%           | 0.10% 0.14%     |                 | 0.76            | 0.75            | 0.78            | -0.94           | -1.58           | -1.97           | 200%                        | -25%                        | -22%                        | -4%                         | 46%                         | 44% 50%                     |                             | -49%                        | -46%                        | -36%                        |
| 14                | HSE39Eur          | E 2               | 3.37E+04          | 3.03E+05          | 9                 | 0.17%           | 0.28%           | 0.34%           | 0.71            | 0.70            | 0.73            | -2.80           | -4.54           | -5.33           | -50%                        | 108%                        | 110%                        | 145%                        | 36%                         | 35%                         | 40%                         | 53%                         | 56%                         | 75%                         |
| 15                | HSE49Eur          | E 4               | 1.35E+05          | 1.21E+06          | 9                 | 0.07%           | 0.12% 0.16%     |                 | 0.74            | 0.73            | 0.76            | -1.13           | -1.90           | -2.34           | 100%                        | -13%                        | -8%                         | 12%                         | 41% 40%                     |                             | 46%                         | -38%                        | -35%                        | -23%                        |
| 16                | HSEur             | E                 |                   |                   |                   | 0.12%           | 0.19%           | 0.25%           | 0.77            | 0.76            | 0.79            | -1.75           |                 | -3.52           | 0%                          | 42%                         | 44%                         | 75%                         | 47%                         | 52%                         |                             | -4%                         | -1%                         | 15%                         |
|                   |                   |                   | 6.73E+04          | 8.08E+05          | 12                |                 |                 |                 |                 |                 |                 |                 | -2.88           |                 |                             |                             |                             |                             |                             | 46%                         |                             |                             |                             |                             |
| 17                | HSE1Eur           | E 1               | 2.24E+04          | 2.69E+05          | 12                | 0.27%           | 0.37% 0.52%     | 0.78            |                 | 0.76            | 0.78            | -3.98           | -5.61           | -7.56           | -67%                        | 223%                        | 179% 268%                   |                             | 48%                         | 45% 48%                     |                             | 118%                        | 92%                         | 148%                        |

|   18 | HSE2Eur E 3 2.02E+05   |   2.42E+06 |    | 12    | 0.07%   | 0.12%   |   0.15% |   0.83 |   0.81 |   0.83 |   -1.01 |   -1.70 | -2.10   | 200%   | -12% -10%   |      | 10%   | 58%     | 55%   | 59%   | -45% -42%   | -31%   |
|------|------------------------|------------|----|-------|---------|---------|---------|--------|--------|--------|---------|---------|---------|--------|-------------|------|-------|---------|-------|-------|-------------|--------|
|   19 | HSE3Eur E 2 3.37E+04   |   4.04E+05 | 12 | 0.18% | 0.29%   | 0.36%   |    0.75 |   0.74 |   0.77 |  -2.76 |   -4.47 |   -5.37 | -50%    | 117%   | 118%        | 160% | 44%   | 42% 48% |       | 51%   | 53%         | 76%    |
|   20 | HSE4Eur E 4 1.35E+05   |   1.62E+06 | 12 | 0.08% | 0.14%   | 0.18%   |    0.80 |   0.78 |   0.81 |  -1.18 |   -1.98 |   -2.45 | 100%    | -2%    | 1%          | 25%  | 52%   | 50%     | 55%   | -35%  | -32%        | -20%   |

## SOIL GRAVITY WEIGHT 1

| INPUT PARAMTERS   | INPUT PARAMTERS   | INPUT PARAMTERS   | INPUT PARAMTERS   | OUTPUT VALUES   | OUTPUT VALUES   | OUTPUT VALUES   | OUTPUT VALUES   | OUTPUT VALUES   | OUTPUT VALUES   | OUTPUT VALUES   | OUTPUT VALUES   | OUTPUT VALUES   | OUTPUT RESULTS RELATED TO REFERENCE ANALYSES RESULTS    | OUTPUT RESULTS RELATED TO REFERENCE ANALYSES RESULTS    | OUTPUT RESULTS RELATED TO REFERENCE ANALYSES RESULTS    | OUTPUT RESULTS RELATED TO REFERENCE ANALYSES RESULTS    | OUTPUT RESULTS RELATED TO REFERENCE ANALYSES RESULTS    | OUTPUT RESULTS RELATED TO REFERENCE ANALYSES RESULTS    | OUTPUT RESULTS RELATED TO REFERENCE ANALYSES RESULTS    | OUTPUT RESULTS RELATED TO REFERENCE ANALYSES RESULTS    | OUTPUT RESULTS RELATED TO REFERENCE ANALYSES RESULTS    |
|-------------------|-------------------|-------------------|-------------------|-----------------|-----------------|-----------------|-----------------|-----------------|-----------------|-----------------|-----------------|-----------------|----------------------------------------------------------|----------------------------------------------------------|----------------------------------------------------------|----------------------------------------------------------|----------------------------------------------------------|----------------------------------------------------------|----------------------------------------------------------|----------------------------------------------------------|----------------------------------------------------------|
|                   |                   |  d               |  Sat             | V L [%]         | V L [%]         | k = i/Z         | k = i/Z         | 0               | 0               | w max [mm]      | w max [mm]      |  /  rif      |  V L /V L,rif [%]                                       |  V L /V L,rif [%]                                       |  V L /V L,rif [%]                                       |  k/k rif [%]                                            |  k/k rif [%]                                            |  w max /w max,rif [%]                                   |  w max /w max,rif [%]                                   |  w max /w max,rif [%]                                   |  w max /w max,rif [%]                                   |
| ANLAYSES ID       | ANLAYSES ID       | [kN/m 3 ]         | [kN/m 3 ]         | Plane O         | Plane U         | Plane AE        | Plane O         | Plane U         | Plane AE        | Plane O         | Plane U         | Plane AE        | [%] Plane O                                              | Plane U                                                  | Plane AE                                                 |                                                          | Plane O Plane U                                          | Plane AE                                                 | Plane O                                                  | Plane U                                                  | Plane AE                                                 |
| 1                 | HS                | 16.00             | 21.00             | 0.08%           | 0.13%           | 0.14%           | 0.52            | 0.52            | 0.52            | -1.82           | -2.92           | -3.05 0%        | 0%                                                       | 0%                                                       | 0%                                                       | 0%                                                       | 0%                                                       | 0%                                                       | 0%                                                       | 0%                                                       | 0%                                                       |
| 2                 | HSg1              | 12.80             | 17.80             | 0.04%           | 0.06%           | 0.04%           | 0.41            | 0.38            | 0.28            | -1.19           | -1.78           | -1.51           | -20% -49%                                                | -56%                                                     | -73%                                                     | -22%                                                     | -28%                                                     | -46%                                                     | -35%                                                     | -39%                                                     | -51%                                                     |
| 3                 | HSg2              | 19.20             | 24.20             | 0.10%           | 0.17%           | 0.19%           | 0.52            | 0.52            | 0.54            | -2.25           | -3.63           | -3.94           | 20% 22%                                                  | 25%                                                      | 32%                                                      | -1%                                                      | 0%                                                       | 2%                                                       | 24%                                                      | 24%                                                      | 29%                                                      |
| 4                 | HSg3              | 14.40             | 19.40             | 0.08%           | 0.13%           | 0.13%           | 0.57            | 0.55            | 0.54            | -1.68           | -2.67 -2.72     | -10%            | 1%                                                       | -4%                                                      | -8%                                                      | 10%                                                      | 5%                                                       | 3%                                                       | -8%                                                      | -9%                                                      | -11%                                                     |
| 5                 | HSg4              | 17.60             | 22.60             | 0.09%           | 0.15%           | 0.16%           | 0.52            | 0.53            | 0.53            | -1.99           | -3.17           | -3.39           | 10% 9%                                                   | 10%                                                      | 13%                                                      | 0%                                                       | 1%                                                       | 2%                                                       | 9%                                                       | 9%                                                       | 11%                                                      |

## SOIL FRICTION ANGLE

| INPUT PARAMTERS   | INPUT PARAMTERS   | INPUT PARAMTERS   | OUTPUT VALUES   | OUTPUT VALUES   | OUTPUT VALUES   | OUTPUT VALUES   | OUTPUT VALUES   | OUTPUT VALUES   | OUTPUT VALUES   | OUTPUT VALUES   | OUTPUT VALUES   | OUTPUT RESULTS RELATED TO REFERENCE ANALYSES RESULTS   | OUTPUT RESULTS RELATED TO REFERENCE ANALYSES RESULTS   | OUTPUT RESULTS RELATED TO REFERENCE ANALYSES RESULTS   | OUTPUT RESULTS RELATED TO REFERENCE ANALYSES RESULTS   | OUTPUT RESULTS RELATED TO REFERENCE ANALYSES RESULTS   | OUTPUT RESULTS RELATED TO REFERENCE ANALYSES RESULTS   | OUTPUT RESULTS RELATED TO REFERENCE ANALYSES RESULTS   | OUTPUT RESULTS RELATED TO REFERENCE ANALYSES RESULTS   | OUTPUT RESULTS RELATED TO REFERENCE ANALYSES RESULTS   |
|-------------------|-------------------|-------------------|-----------------|-----------------|-----------------|-----------------|-----------------|-----------------|-----------------|-----------------|-----------------|--------------------------------------------------------|--------------------------------------------------------|--------------------------------------------------------|--------------------------------------------------------|--------------------------------------------------------|--------------------------------------------------------|--------------------------------------------------------|--------------------------------------------------------|--------------------------------------------------------|
|                   |                   |                 | V L [%]         | V L [%]         | k = i/Z 0       | k = i/Z 0       | k = i/Z 0       | w max [mm]      | w max [mm]      | w max [mm]      |  /  rif      |  V L /V L,rif [%]                                     |  V L /V L,rif [%]                                     |  V L /V L,rif [%]                                     |  k/k rif [%]                                          |  k/k rif [%]                                          |  k/k rif [%]                                          |  w max /w max,rif [%]                                 |  w max /w max,rif [%]                                 |  w max /w max,rif [%]                                 |
| ANLAYSES ID       | ANLAYSES ID       | [°]               | Plane O         | Plane U         | Plane AE        | Plane O         | Plane U Plane   | AE Plane        | O               | Plane U         | Plane AE        | [%]                                                    | Plane O                                                | Plane U                                                | Plane AE Plane                                         | O Plane U                                              | Plane AE                                               | Plane O                                                | Plane U                                                | Plane AE                                               |
| 1                 | HS                | 35                | 0.08%           | 0.13%           | 0.14%           | 0.52            | 0.52 0.52       | -1.82           |                 | -2.92           | -3.05           | 0%                                                     | 0%                                                     | 0%                                                     | 0%                                                     | 0% 0%                                                  | 0%                                                     | 0%                                                     | 0%                                                     | 0%                                                     |
| 2                 | HSj1              | 21                | 0.10%           | 0.13%           | 0.12%           | 0.63            | 0.63 0.64       | -1.81           |                 | -2.36           | -2.19           | -40%                                                   | 20%                                                    | -2%                                                    | -13% 21%                                               | 21%                                                    | 22%                                                    | -1%                                                    | -19%                                                   | -28%                                                   |
| 3                 | HSj2              | 28                | 0.10%           | 0.17%           | 0.18%           | 0.61            | 0.60 0.61       |                 | -1.92           | -3.12           | -3.43           | -20%                                                   | 23%                                                    | 24%                                                    | 32% 17%                                                | 16%                                                    | 17%                                                    | 5%                                                     | 7%                                                     | 12%                                                    |
| 4                 | HSj3              | 24.5              | 0.08%           | 0.12%           | 0.12%           | 0.61            | 0.58            | 0.58            | -1.47           | -2.35           | -2.44           | -30%                                                   | -6%                                                    | -10%                                                   | -11% 16%                                               | 12%                                                    | 11%                                                    | -19%                                                   | -20%                                                   | -20%                                                   |
| 5                 | HSj4              | 31.5              | 0.10%           | 0.16%           | 0.18%           | 0.58            | 0.58            | 0.59            | -2.05           | -3.23           | -3.46           | -10%                                                   | 25%                                                    | 22%                                                    | 27% 11%                                                | 11%                                                    | 12%                                                    | 12%                                                    | 11%                                                    | 13%                                                    |

## SOIL DILATANCY ANGLE

| INPUT PARAMTERS   | INPUT PARAMTERS   | OUTPUT VALUES   | OUTPUT VALUES   | OUTPUT VALUES   | OUTPUT VALUES   | OUTPUT VALUES   | OUTPUT VALUES   | OUTPUT VALUES   | OUTPUT VALUES   | OUTPUT VALUES   | OUTPUT VALUES   | OUTPUT RESULTS RELATED TO REFERENCE ANALYSES RESULTS   | OUTPUT RESULTS RELATED TO REFERENCE ANALYSES RESULTS   | OUTPUT RESULTS RELATED TO REFERENCE ANALYSES RESULTS   | OUTPUT RESULTS RELATED TO REFERENCE ANALYSES RESULTS   | OUTPUT RESULTS RELATED TO REFERENCE ANALYSES RESULTS   | OUTPUT RESULTS RELATED TO REFERENCE ANALYSES RESULTS   | OUTPUT RESULTS RELATED TO REFERENCE ANALYSES RESULTS   | OUTPUT RESULTS RELATED TO REFERENCE ANALYSES RESULTS   | OUTPUT RESULTS RELATED TO REFERENCE ANALYSES RESULTS   |
|-------------------|-------------------|-----------------|-----------------|-----------------|-----------------|-----------------|-----------------|-----------------|-----------------|-----------------|-----------------|--------------------------------------------------------|--------------------------------------------------------|--------------------------------------------------------|--------------------------------------------------------|--------------------------------------------------------|--------------------------------------------------------|--------------------------------------------------------|--------------------------------------------------------|--------------------------------------------------------|
|                   |                   |  V L [%]      |  V L [%]      |  V L [%]      | k = i/Z 0       | k = i/Z 0       | k = i/Z 0       | w max [mm]      | w max [mm]      | w max [mm]      |  /  rif      |                                                        |  V L /V L,rif [%]                                     |  V L /V L,rif [%]                                     |  V L /V L,rif [%]                                     |  k/k rif [%]  w                                      |  k/k rif [%]  w                                      |  k/k rif [%]  w                                      | max /w max,rif [%]                                     | max /w max,rif [%]                                     |
| ANLAYSES ID       | ANLAYSES ID       | [°]             | Plane O         | Plane U         | Plane AE        | [%]             | Plane O Plane   | U Plane         | AE              | Plane O         | Plane U         | Plane AE                                               | Plane O                                                | Plane U                                                | Plane AE Plane                                         | O Plane U                                              | Plane AE                                               | Plane O                                                | Plane U                                                | Plane AE                                               |
| 1                 | HS                | 0               | 0.08%           | 0.13%           | 0.14%           | 0.52            | 0.52 0.52       |                 | -1.82           | -2.92           | -3.05           | 0%                                                     | 0%                                                     | 0%                                                     | 0% 0%                                                  | 0%                                                     | 0%                                                     | 0%                                                     | 0%                                                     | 0%                                                     |
| 2                 | HSY10             | 10              | 0.11%           | 0.17%           | 0.18%           | 0.61            | 0.58            | 0.59            | -2.10           | -3.29           | -3.43 29%       |                                                        | 34%                                                    | 25%                                                    | 27% 16%                                                | 11%                                                    | 12%                                                    | 15%                                                    | 13%                                                    | 13%                                                    |
| 3                 | HSY5              | 5               | 0.11%           | 0.17%           | 0.18%           | 0.61            | 0.58            | 0.59            | -2.10           | -3.29           | -3.43 14%       |                                                        | 34%                                                    | 25%                                                    | 26% 16%                                                | 11%                                                    | 12%                                                    | 15%                                                    | 13%                                                    | 13%                                                    |
| 4                 | HSY3              | 3               | 0.08%           | 0.13%           | 0.14%           | 0.52            | 0.52            | 0.52            | -1.82           | -2.92           | -3.05 9%        |                                                        | 0%                                                     | 0% 0%                                                  | 0%                                                     | 0%                                                     | 0%                                                     | 0%                                                     | 0%                                                     | 0%                                                     |
| 5                 | HSY1              | 1               | 0.08%           | 0.13%           | 0.14%           | 0.52            | 0.52            | 0.52            | -1.82           | -2.92           | -3.05 3%        |                                                        | 0% 0%                                                  | 0%                                                     | 0%                                                     | 0%                                                     | 0%                                                     | 0%                                                     | 0%                                                     | 0%                                                     |

## EFFECTS OF SOIL PARAMETERS ON THE VOLUME LOSS AT THE TUNNEL DEPTH (VL,axis)

Fig. IV-1: Effects of on volume loss (a) and maximum settlement (b) at the tunnel depth

<!-- image -->

Line chart

Fig. IV-2: vs surface volume losses (a) and maximum settlements (b) ratios

<!-- image -->

Scatter plot

Fig. IV-3: Effects of on volume loss (a) and maximum settlement (b) at the tunnel depth

<!-- image -->

Scatter plot

Fig. IV-4: vs surface volume losses (a) and maximum settlements (b) ratios

<!-- image -->

Scatter plot

Fig. IV-5: Effects of on volume loss (a) and maximum settlement (b) at the tunnel depth

<!-- image -->

Scatter plot

Fig. IV-6: vs surface volume losses (a) and maximum settlements (b) ratios

<!-- image -->

Scatter plot

## EFFECTS OF SOIL PARAMETERS ON THE SURFACE VOLUME LOSS (VL)

Fig. IV-7: Effects of loading stiffness modulus on along the tunnel axis for constant stiffness moduli ratio (Plane O coinciding with the tunnel front, Plane U and Plane AE respectively 1D and 3D from it)

<!-- image -->

Line chart

Fig. IV-8: Effects of un-reloading stiffness modulus on along the tunnel axis for constant stiffness moduli ratio (Plane O coinciding with the tunnel front, Plane U and Plane AE respectively 1D and 3D from it)

<!-- image -->

Line chart

<!-- image -->

Box plot

Fig. IV-9: Effects of variations up to on , and

<!-- image -->

Line chart

Fig. IV-10: Effects of on and

<!-- image -->

Scatter plot

## PARAMETRIC ANALYSES ON MACHINE PRESSURES EFFECTS

| INPUT VALUES   | INPUT VALUES       | INPUT VALUES   | INPUT VALUES   | INPUT VALUES   | INPUT VALUES   | INPUT VALUES             | INPUT VALUES   |           |             |       | OUTPUT VALUES   | OUTPUT VALUES   | OUTPUT VALUES                     | OUTPUT VALUES         | OUTPUT VALUES    | OUTPUT VALUES         |
|----------------|--------------------|----------------|----------------|----------------|----------------|--------------------------|----------------|-----------|-------------|-------|-----------------|-----------------|-----------------------------------|-----------------------|------------------|-----------------------|
| ANALYSES ID    | ANALYSES ID        | FP             | FP inc         | GP             | GP inc         | HYDRAULIC JACKS PRESSURE | V L,c          | GP/FP w   | max V L     |       |  FP/FP         | FP/FP rif       | RESULTS  V L /V L  w max /w max | ELABORATIONS VL/V L,c | w max /w max,rif | w max /w max,rif (GP) |
|                |                    | [kPa]          | [kPa]          | [kPa]          | [kPa]          | [kPa]                    | [%]            | [-]       | [mm]        | [%]   | [%]             | [-] [%]         | [%]                               | [-]                   | [-]              | [-]                   |
| 1              | PG_HSg1EFP100GP100 | 100            | 14             | 100            | 20             | 635                      | 0.1%           | 1.0       | -7.59       | 0.36% | 0.0             | 1.0 0%          | 0%                                | 3.63                  | 1.00             | 1.00                  |
| 2              | PG_HSg1EFP130GP100 | 130            | 14             | 100            | 20             | 756                      | 0.1%           | 0.8       | -6.29 0.31% | 0.3   | 1.3             | -16%            | -17%                              | 3.06                  | 0.83             | 0.83                  |
| 3              | PG_HSg1EFP170GP100 | 170            | 14             | 100            | 20             | 918                      | 0.1%           | 0.6       | -5.62 0.27% | 0.7   | 1.7             | -25%            | -26%                              | 2.73                  | 0.74             | 0.74                  |
| 4              | PG_HSg1EFP200GP100 | 200            | 14             | 100            | 20             | 1040                     | 0.1%           | 0.5       | -5.50 0.27% | 1.0   | 2.0             | -25%            | -27%                              | 2.70                  | 0.73             | 0.73                  |
| 5              | PG_HSg1EFP300GP100 | 300            | 14             | 100            | 20             | 1445                     | 0.1%           | 0.3       | -5.53 0.27% | 2.0   | 3.0             | -25%            | -27%                              | 2.74                  | 0.73             | 0.73                  |
| 6              | PG_HSg1EFP400GP100 | 400            | 14             | 100            | 20             | 1850                     | 0.1%           | 0.3       | -5.74 0.28% | 3.0   | 4.0             | -22%            | -24%                              | 2.84                  | 0.76             | 0.76                  |
| 7              | PG_HSg1EFP500GP100 | 500            | 14             | 100            | 20             | 2255                     | 0.1%           | 0.2       | -6.13 0.30% | 4.0   | 5.0             | -18%            | -19%                              | 2.96                  | 0.81             | 0.81                  |
| 8              | PG_HSg1EFP100GP130 | 100            | 14             | 130            | 20             | 635                      | 0.1%           | 1.3       | -7.08 0.33% | 0.0   | 1.0             | -9%             | -7%                               | 3.31                  | 0.93             | 1.02                  |
| 9              | PG_HSg1EFP130GP130 | 130            | 14             | 130            | 20             | 756                      | 0.1%           | 1.0       | -5.86 0.29% | 0.3   | 1.3             | -21%            | -23%                              | 2.87                  | 0.77             | 0.84                  |
| 10             | PG_HSg1EFP170GP130 | 170            | 14             | 130            | 20             | 918                      | 0.1%           | 0.8       | -5.21 0.26% | 0.7   | 1.7             | -29%            | -31%                              | 2.58                  | 0.69             | 0.75                  |
| 11             | PG_HSg1EFP200GP130 | 200            | 14             | 130            | 20             | 1040                     | 0.1%           | 0.7 -5.13 | 0.25%       | 1.0   | 2.0             | -30%            | -32%                              | 2.55                  | 0.68             | 0.74                  |
| 12             | PG_HSg1EFP300GP130 | 300            | 14             | 130            | 20             | 1445                     | 0.1%           | 0.4       | -5.15 0.26% | 2.0   | 3.0             | -29%            | -32%                              | 2.58                  | 0.68             | 0.74                  |
| 13             | PG_HSg1EFP400GP130 | 400            | 14             | 130            | 20             | 1850                     | 0.1%           | 0.3       | -5.37 0.27% | 3.0   | 4.0             | -26%            | -29%                              | 2.68                  | 0.71             | 0.77                  |
| 14             | PG_HSg1EFP100GP170 | 100            | 14             | 170            | 20             | 635                      | 0.1%           | 1.7 -6.82 | 0.33%       | 0.0   | 1.0             | -9%             | -10%                              | 3.29                  | 0.90             | 0.98                  |
| 15             | PG_HSg1EFP130GP170 | 130            | 14             | 170            | 20             | 756                      | 0.1%           | 1.3       | -5.92 0.29% | 0.3   | 1.3             | -20%            | -22%                              | 2.89                  | 0.78             | 0.85                  |
| 16             | PG_HSg1EFP170GP170 | 170            | 14             | 170            | 20             | 918                      | 0.1%           | 1.0 -5.07 | 0.25%       | 0.7   | 1.7             | -31%            | -33%                              | 2.49                  | 0.67             | 0.73                  |
| 17             | PG_HSg1EFP200GP170 | 200            | 14             | 170            | 20             | 1040                     | 0.1%           | 0.9       | -4.97 0.25% | 1.0   | 2.0             | -32%            | -34%                              | 2.46                  | 0.66             | 0.71                  |
| 18             | PG_HSg1EFP300GP170 | 300            | 14             | 170            | 20             | 1445                     | 0.1%           | 0.6 -4.97 | 0.25%       | 2.0   | 3.0             | -32%            | -34%                              | 2.48                  | 0.66             | 0.71                  |
| 19             | PG_HSg1EFP400GP170 | 400            | 14             | 170            | 20             | 1850                     | 0.1%           | 0.4       | -5.19 0.26% | 3.0   | 4.0             | -29%            | -32%                              | 2.58                  | 0.68             | 0.75                  |
| 20             | PG_HSg1EFP100GP200 | 100            | 14             | 200            | 20             | 635                      | 0.1%           | 2.0       | -6.96 0.33% | 0.0   | 1.0             | -9%             | -8%                               | 3.30                  | 0.92             | 1.00                  |
| 21             | PG_HSg1EFP130GP200 | 130            | 14             | 200            | 20             | 756                      | 0.1%           | 1.5 -5.65 | 0.27%       | 0.3   | 1.3             | -24%            | -25%                              | 2.75                  | 0.75             | 0.81                  |
| 22             | PG_HSg1EFP170GP200 | 170            | 14             | 200            | 20             | 918                      | 0.1%           | 1.2       | -5.01 0.24% | 0.7   | 1.7             | -33%            | -34%                              | 2.44                  | 0.66             | 0.72                  |
| 23             | PG_HSg1EFP200GP200 | 300            | 14             | 200            | 20             | 1040                     |                | 1.0       | -4.92 0.24% | 2.0   | 3.0             | -33%            | -35% -35%                         | 2.41 2.44             | 0.65 0.65        | 0.71                  |
| 24             | PG_HSg1EFP300GP200 | 200            | 14             | 200            | 20             | 1445                     | 0.1% 0.1%      | 0.7       | -4.93 0.24% | 1.0   | 2.0             | -34%            |                                   |                       |                  | 0.71                  |

Tab.V-1. Performed analyses aimed at the parametric study on machine pressures

| 25                    | PG_HSg1EFP400GP200     |   400 | 14     | 200 20   |   1850 | 0.1%   |   0.5 |   -5.12 | 0.25%   |   3.0 |   4.0 | -30%   | -33%   |   2.52 |   0.67 |   0.74 |
|-----------------------|------------------------|-------|--------|----------|--------|--------|-------|---------|---------|-------|-------|--------|--------|--------|--------|--------|
| 26                    | PG_HSg1EFP500GP200 500 |    14 | 200    | 20       |   2255 | 0.1%   |   0.4 |   -5.43 | 0.26%   |   4.0 |   5.0 | -27%   | -28%   |   2.64 |   0.72 |   0.78 |
| 27                    | PG_HSg1E 200           |    14 | 220    | 20       |   1040 | 0.1%   |   1.1 |   -5.16 | 0.25%   |   1.0 |   2.0 | -31%   | -32%   |   2.52 |   0.68 |   0.00 |
| 28 PG_HSg1EFP100GP300 | 100                    |    14 | 300    | 20       |    635 | 0.1%   |   3.0 |   -6.32 | 0.30%   |   0.0 |   1.0 | -18%   | -17%   |   2.97 |   0.83 |   1.00 |
| 29 PG_HSg1EFP130GP300 | 130                    |    14 | 300    | 20       |    756 | 0.1%   |   2.3 |   -5.37 | 0.25%   |   0.3 |   1.3 | -30%   | -29%   |   2.54 |   0.71 |   0.85 |
| 30                    | PG_HSg1EFP170GP300 170 |    14 | 300    | 20       |    918 | 0.1%   |   1.8 |   -4.77 | 0.23%   |   0.7 |   1.7 | -38%   | -37%   |   2.26 |   0.63 |   0.76 |
| 31                    | PG_HSg1EFP200GP300 200 |    14 | 300    | 20       |   1040 | 0.1%   |   1.5 |   -4.70 | 0.22%   |   1.0 |   2.0 | -38%   | -38%   |   2.24 |   0.62 |   0.74 |
| 32                    | PG_HSg1EFP300GP300 300 |       | 14 300 | 20       |   1445 | 0.1%   |   1.0 |   -4.67 | 0.22%   |   2.0 |   3.0 | -38%   | -39%   |   2.25 |   0.61 |   0.74 |
| 33                    | PG_HSg1EFP400GP300 400 |    14 | 300    | 20       |   1850 | 0.1%   |   0.8 |   -4.82 | 0.23%   |   3.0 |   4.0 | -36%   | -36%   |   2.33 |   0.64 |   0.76 |
| 34                    | PG_HSg1EFP500GP300 500 |    14 | 300    | 20       |   2255 | 0.1%   |   0.6 |   -5.12 | 0.24%   |   4.0 |   5.0 | -33%   | -33%   |   2.43 |   0.67 |   0.81 |
| 35                    | PG_HSg1EFP100GP400 100 |    14 | 400    | 20       |    635 | 0.1%   |   4.0 |   -5.98 | 0.27%   |   0.0 |   1.0 | -25%   | -21%   |   2.72 |   0.79 |   1.00 |
| 36                    | PG_HSg1EFP130GP400 130 |       | 14 400 | 20       |    756 | 0.1%   |   3.1 |   -5.14 | 0.24%   |   0.3 |   1.3 | -35%   | -32%   |   2.37 |   0.68 |   0.86 |
| 37                    | PG_HSg1EFP170GP400 170 |    14 | 400    | 20       |    918 | 0.1%   |   2.4 |   -4.58 | 0.21%   |   0.7 |   1.7 | -42%   | -40%   |   2.11 |   0.60 |   0.77 |
| 38                    | PG_HSg1EFP200GP400 200 |    14 | 400    | 20       |   1040 | 0.1%   |   2.0 |   -4.50 | 0.21%   |   1.0 |   2.0 | -43%   | -41%   |   2.07 |   0.59 |   0.75 |
| 39 PG_HSg1EFP300GP400 | 300                    |    14 | 400    | 20       |   1445 | 0.1%   |   1.3 |   -4.46 | 0.21%   |   2.0 |   3.0 | -42%   | -41%   |   2.09 |   0.59 |   0.75 |
| 40 PG_HSg1EFP400GP400 | 400                    |    14 | 400    | 20       |   1850 | 0.1%   |   1.0 |   -4.57 | 0.21%   |   3.0 |   4.0 | -41%   | -40%   |   2.15 |   0.60 |   0.76 |
| 41 PG_HSg1EFP500GP400 | 500                    |    14 | 400    | 20       |   2255 | 0.1%   |   0.8 |   -4.84 | 0.22%   |   4.0 |   5.0 | -38%   | -36%   |   2.23 |   0.64 |   0.81 |
| 42 PG_HSg1EFP100GP500 | 100                    |    14 | 500    | 20       |    635 | 0.1%   |   5.0 |   -5.69 | 0.25%   |   0.0 |   1.0 | -30%   | -25%   |   2.52 |   0.75 |   1.00 |
| 43 PG_HSg1EFP130GP500 | 130                    |    14 | 500    | 20       |    756 | 0.1%   |   3.8 |   -4.88 | 0.22%   |   0.3 |   1.3 | -41%   | -36%   |   2.15 |   0.64 |   0.86 |
| 44                    | PG_HSg1EFP170GP500 170 |    14 | 500    | 20       |    918 | 0.1%   |   2.9 |   -4.35 | 0.19%   |   0.7 |   1.7 | -47%   | -43%   |   1.91 |   0.57 |   0.77 |
| 45                    | PG_HSg1EFP200GP500 200 |    14 | 500    | 20       |   1040 | 0.1%   |   2.5 |   -4.27 | 0.19%   |   1.0 |   2.0 | -48%   | -44%   |   1.87 |   0.56 |   0.75 |
| 46                    | PG_HSg1EFP300GP500 300 |    14 | 500    | 20       |   1445 | 0.1%   |   1.7 |         |         |   2.0 |   3.0 |        |        |        |        |        |
| 47                    | PG_HSg1EFP400GP500 400 |       | 14     | 500 20   |   1850 | 0.1%   |   1.3 |         |         |   3.0 |   4.0 |        |        |        |        |        |
| 48                    | PG_HSg1EFP500GP500     |   500 | 14     | 500 20   |   2255 | 0.1%   |   1.0 |   -4.63 | 0.21%   |   4.0 |   5.0 | -43%   | -39%   |   2.08 |   0.61 |   0.81 |

Fig. IV-11: Front pressure (FP) effects on maximum surface settlement (a) and on surface volume loss (b)

<!-- image -->

Line chart

Fig. IV-12: Grout pressure (GP) effects on maximum surface settlement (a) and on surface volume loss (b)

<!-- image -->

Line chart

Fig. IV-13: : relative shear stresses for 100 kPa up to 500 kPa front pressures and constant grouting pressure (100 kPa)

<!-- image -->

Engineering drawing

Fig. IV-14: Plastic points for analyses with 100 kPa up to 500 kPa front pressures and constant grouting pressure (100 kPa)

<!-- image -->

Geographical map

Fig. IV-15: Horizontal displacement along tunnel axis (z-axis) for analyses with 100 kPa up to 500 kPa front pressures and constant grouting pressure (100 kPa)

<!-- image -->

Bar chart
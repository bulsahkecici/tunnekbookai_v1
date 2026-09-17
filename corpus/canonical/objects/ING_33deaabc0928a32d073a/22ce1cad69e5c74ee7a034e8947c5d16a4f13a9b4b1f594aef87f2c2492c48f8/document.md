## UNCERTAINTY MODELLING AND LIMIT STATE RELIABILITY OF TUNNEL SUPPORTS UNDER SEISMIC EFFECTS

Mallika S 1 , Srividya. A 2 , Venkatachalam. G 3

1 Research Scholar, Reliability Engineering Group, IIT Bombay, Powai, Mumbai, India, mallika@iitb.ac.in 2 Guest Professor, University College, Haugesund, Norway, asvidya88@gmail.com 3 Emeritus Fellow, Department of Civil Engineering, IIT Bombay, Powai, Mumbai, India, gvee@iitb.ac.in

## Abstract

Underground openings and excavations are increasingly being used for civilian and strategic purposes all over the world. Recent earthquakes  and  resulting  damage  have  brought  into  focus  and  raised  the  awareness  for  aseismic  design  and  construction.  In addition, underground tunnels, particularly, have distinct seismic behaviour due to their complete enclosure in soil or rock and their significant length. Therefore, seismic response of tunnel support systems warrant closer attention. The geological settings in which they  are  placed  are  often  difficult  to  describe  due  to  limited  site  investigation  data  and  vast  spatial  variability.    Therefore,  the parameters which govern the design are many and their variabilities cannot be ignored. A solution to this issue is reliability based analysis  and  design.  These  real  conditions  of  variability  can  only  be  addressed  through  a  reliability  based  design.  The  problem addressed here is one of reliability-based analysis of the support system of an underground tunnel in soil. Issues like the description of the  interaction  between  the  tunnel  lining  and  the  surrounding  medium,  the  type  of  limit  state  that  would  be  appropriate,  the  nonavailability of a closed form performance function and the advantages of response surface method [RSM] are looked into. Both static and seismic environment with random variability in the material properties are studied here. Support seismic response is studied in terms of thrust, moment and shear forces in the lining. Interactive analysis using finite element method [FEM], combined with RSM and Hasofer-Lind reliability concept to assess the performance of the tunnel support, has proven useful under real field situations.

Index Terms: Tunnel, Reliability, Random, Seismic

-----------------------------------------------------------------------***-----------------------------------------------------------------------

## 1. INTRODUCTION

The need today in civil engineering, more than ever before, is toward providing economical designs commensurate with safety.  This  requires  a  careful  consideration  of  variabilities  in loads, geometry and material properties governing the behavior of the given structure. Reliability analysis is best suited for this. While considerable developments have taken place in application  of  reliability  concepts  in  structural  engineering, there is a need for more studies in geotechnical applications.

The importance of reliability  analysis is best illustrated in  the evaluation of slope stability. Several researchers have contributed  to  the  understanding  of  slope  reliability  [1,2,3,4]. The  measure  normally    adopted  for  expressing  safety  is  the factor of safety, which is evaluated from the relative magnitudes of resistance (capacity) and load (demand) as FS = Capaity (C) / Demand (D).  Since capacity and demand cannot be  evaluated  with  certainty,  assuming  a  random  variation,  a ratio of expected values of capacity and demand called Central factor of safety is preferred. However, when material properties exhibit  substantial  variabilities,  the  minimum  factor  of  safety may  not  be  the  correct  measure.  A  better  measure  of  safety, therefore,  is  the  Reliability  Index,  β,  which  accounts  for  the randomness of FS itself. It is defined as the number of standard deviations by which the expected value of FS exceeds a critical or acceptable value. This may be expressed as (Eq.1):

<!-- formula-not-decoded -->

Assuming normal distribution of capacity and demand, another parameter, Probability of failure, is expressed as (Eq.2):

<!-- formula-not-decoded -->

Where, φ (β) is the standard normal probability.

However, the variable values corresponding  to the least value of β would be the most critical [5]. The Hasofer-Lind reliability index βHL is defined as the shortest distance from the origin of the reduced variable space to the limit state function g = 0.

Consider a limit state function g(X1, X2……  Xn)  with uncorrelated Xi variables. The Hasofer-Lind reliability index is determined by the following steps:

1. The reduced variables {Z1, Z2, . . ., Z n } are first determined as (Eq.3):

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

<!-- formula-not-decoded -->

2.  The  limit  state  function  is  then  redefined  in  terms  of  these reduced variables.
3. The reliability index is the shortest distance from the origin in the n-dimensional space of reduced variables to the curve corresponding to the limit state function described by g (Z ,

1

<!-- formula-not-decoded -->

The  Hasofer-Lind  reliability  index  β HL  can  be  expressed  in matrix form as (Eq. 4):

<!-- formula-not-decoded -->

where  x  vector  represents  the  n  random  variables;  µ  is  the vector  of  their  mean  values;  and  C  is  the  corresponding covariance matrix.

The  minimization  of  Eq  (4)  is performed  subject  to the constraint  g(x)  ≤  0  where  the  limit  state  surface  g(x)  =  0 separates  the  n-dimensional  domain  of  random  variables  into two regions: a failure region F represented by g (x) ≤ 0 and a safe region given by g(x) &gt; 0. A schematic of the Hasofer-Lind reliability  estimation  is  given  in  Fig.1,  where  superscript  N represents  normative  values  and  θ  represents  an  angle  as shown.

Fig-1: Schematic of Hasofer-Lind Reliability Index estimation

<!-- image -->

Engineering drawing

Reliability  analysis  has  also  been  done  for  Piles  subjected  to axial and lateral loads [6]. Empirical, analytical and numerical methods are available  for  analysis  and  design  of  tunnels.  The empirical methods such as the geomechanical methods consider rock mass characteristics, which are otherwise very difficult to model.  Authors  of  [7]  have  brought  out  the  significance  of seismic analysis, though the analytical methods, such as those employed by them, generally consider ideal simplified situations.  Numerical  methods  have  come  to  be  employed widely during the past few decades due to their ability to model complex geometry, loading, stress-strain relationships and construction sequences [8, 9]. Apart from the rigourousness of the  method  of  analysis,  consideration  of  material  properties, especially their variabilties, also merits close attention and the present study is an attempt in that direction.

## 2. RESPONSE SURFACE METHODOLOGY

Following  are some  uncertainties surrounding  the seismic analysis of the underground openings.

- Uncertainties in characterizing the seismic event
- Uncertainties in structural and material modeling
- Uncertainties/errors in method of analysis and performance criteria

In the current study, the response of the underground opening under  static  and  seismic  loading  is  analyzed  considering  the ultimate  limit  state  (ULS)  as  the  performance  criterion  and material  properties  as  random  variables  (see  for  example,  Eq. 5). The response surface methodology (RSM) is adopted herein in order to study the response of the tunnel lining considering the effect of the randomness of the ground material parameters. Based  on  the  observed  data  from  the  system,  an  empirical model, which is a polynomial function of the random variables, is  built  using  regression  analysis  of  the  selected  deterministic analysis  results.  This  polynomial,  called  the  response  surface, can  serve  as  a  basis  for  further  simulations  and  hence,  for  a better estimation of the probability of failure (Eq.  6). The true response, y, of a system is given by [10]:

<!-- formula-not-decoded -->

Where i  are the independent variables and ε is the modeling error.  The second-order polynomial approximation of the true response function involving two factors is:

<!-- formula-not-decoded -->

Where  xi  are  called  coded  variables,  which  are  transformed values of the actual variables  i , to the domain of [-1,1] and βij are  called  regression  coefficients.  Fig.  2  shows  the  number  of analyses required and the values of the variables to be used in the case of three factors (a, b and c).

Fig-2: Three level three factor experiment

<!-- image -->

Flow chart

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

## 3. STATEMENT OF PROBLEM

In order to evaluate the effect of uncertainties, a real tunnel and the  earthquake  to  which  it  was  subjected  or  considered.  The case  study  chosen  concerns  a  tunnel  of  6  m  diameter  and overburden depth between 21.0 and 25.3 m [11].

The center of the studied section of the tunnel is approximately 24m deep with a 21 m thick overburden and is embedded in the Shongsan formation which comprises six alternating silty sand and silty clay layers.  A typical cross section of the formations, the alignment of the tunnel and related information are given in (Fig. 3). The material properties of the formation and that of the tunnel lining are listed in Table 1 and Table 2 respectively.

Fig-3: Cross-section of the soil stratification at Shongsan airport tunnel site (Gui and Chien, 2006)

<!-- image -->

Engineering drawing

Table-1: Material properties of the ground medium.\

| Ground properties                  |   Mean values |
|------------------------------------|---------------|
| Bulk unit weight γ (kN/m³)         |            18 |
| Modulus of elasticity E stat (MPa) |            28 |
| Poisson's ratio                   |           0.3 |
| Cohesion c (kN/m 2 )               |            30 |
| Friction angle φ (degrees)         |            31 |
| Modulus of elasticity E dyn (MPa)  |           253 |

Table-2: Tunnel lining parameters (a) a Steel (b) Concrete

| Grade 60 Steel (16 Nos.)             |   Grade 60 Steel (16 Nos.) |
|--------------------------------------|----------------------------|
| Modulus of elasticity of steel (MPa) |                     210000 |
| Poisson's ratio                      |                        0.2 |
| Tensile strength (MPa)               |                        420 |
| Shotcrete Thickness (m)              |                        0.3 |

(a)

| Shotcrete Lining           |       |
|----------------------------|-------|
| Modulus of shotcrete (MPa) | 30500 |
| Poisson's ratio            |   0.2 |
| Tensile strength (MPa)     |  0.36 |
| Compressive strength (MPa) |    42 |

(b)

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

## 4. METHODOLOGY

Interestingly,  when  material  property  variation  is  the  main consideration, reliability analysis requires only a set of deterministic analyses using different combinations of material properties. Hence, the methodology used consists essentially of three steps. In the first step, a series of deterministic analyses is carried out. Since there are three variables (factors), considering  mean  and  ±  standard  deviation,  the  number  of combinations  works out to (3) 3 =  27.  Hence,  27  deterministic analyses are carried out using PLAXIS and thrust, moment and shear are calculated in the lining. Next, using these values and RSM, an equation is built for each of these quantities in terms of  three  variables.  This  serves  as  an  equivalent  alternative function  for  the  unknown  performance  function.  In  the  third step,  the  resulting  equations  are  used  to  arrive  at  the  least reliability index.

Two  cases  as  shown  in  Table  3  have  been  considered.  The objective of choosing the two cases is to identify the  effect of the  random  nature  of  the  material  parameters  (cohesion  c, Elastic  modulus,  E  and  angle  of  internal  friction  φ)  on  the lining performance, under ultimate and serviceability conditions  within  static  as  well  as  seismic  environment.  To perform  the  reliability  analysis  the  material  properties  of  the ground are considered as normally distributed random variables with the mean and Coefficient of Variation (COV) as shown in Table 4. For the chosen COV, there  was no likelihood of the normal variables turning negative. However, for a higher COV, say  more  than  30%,  there  is  a  possibility  of  normal  variables turning  negative.  In  such  cases,  assumption  of  a  lognormal distribution would help. The effect of their randomness on the performance of the tunnel support system is then studied using RSM, where, the response surface  built is evaluated to obtain the  least  reliability  index  β HL through  repeated  iterations  and subsequent convergence.

Table-3: Cases studied

| Case       | ULS                         | SLS         |
|------------|-----------------------------|-------------|
| 1. Static  | Thrust, Moment, Shear force | Deformation |
| 2. Seismic | Thrust, Moment, Shear force | -           |

Table-4: Properties of chosen Normal Random variables.

| Ground properties                  |   Mean values |   COV (%) |
|------------------------------------|---------------|-----------|
| Modulus of elasticity E stat (MPa) |            28 |        13 |
| Modulus of elasticity E dyn (MPa)  |           253 |        13 |
| Cohesion c (kN/m 2 )               |            30 |        30 |
| Friction angle φ (degrees)         |            31 |        10 |

## 4.1 Performance Functions using RSM

Based on the limit states defined for the two cases listed above, the  performance  functions  for  the  thrust,  moment,  shear  force and deformation responses are as follows:

- ·ULS of thrust: Nc/N -1 =0
- ·ULS of moment: Mc/M-1=0
- ·ULS of shear : Qc/Q-1=0
- ·SLS of deformation: yc-y=0

Here,  the  notations  Nc,  Qc,  Mc  correspond  to  the  ultimate capacity of thrust, moment and shear force calculated based on ACI  318-05  [12]  for  the  given  lining  material  properties  as listed  in  Table  5.  The  serviceability  limit  state  is  defined  by limiting the displacement yc of the lining to 5mm.

Table-5: Structural capacity of the tunnel lining

| Thrust capacity Nc (kN/m)   |   7993 |
|-----------------------------|--------|
| Moment capacity Mc (kNm/m)  |    283 |
| Shear capacity Qc (kN/m)    |   3888 |

For  the  seismic  analysis,  the  accelerogram  of  the  earthquake that occurred in November 14, 1986 with a magnitude of 7.8 at a  distance  of  approximately  120km  from  the  airport  and  at  a depth approximately 34m is used. The peak ground acceleration PGA is 0.13g (Fig 4). Fig. 5 shows the FE model used for the dynamic  analysis.  In  order  to  apply  RSM,  27  sample  points were  taken initially as  shown  in  Fig.1.  The  numbers  of experiments were chosen [13] such that the convergence of the order  10 -1 is  attained within  three  to four  iterations.  The selected sample  points are (c i ,φi ,Ei ), (ci+1.2  c , φi ,Ei ), (c i - 0.3  c ,φi ,Ei ), (c i,φi+1.4  φ ,Ei ), (c i ,  φ i -0.3  φ ,Ei ), (c i ,φi,Ei+  E ) and (c i ,φi ,Ei -  E )

Fig-4: Accelerogram of Taiwan Earthquake, November14, 1986 [14] (National Geophysical Data Centre)

<!-- image -->

Line chart

Fig-5: Finite Element model used for seismic analysis

<!-- image -->

Engineering drawing

## 5. RESULTS AND OBSERVATIONS

The  results  are  analyzed  and  discussed  in  terms  of  thrusts, moments, shear and displacements.  The associated reliabilities under appropriate limit states and corresponding critical material property combinations are examined.

Table 6 illustrates the iterations conducted for the RSM used in obtaining  the  reliability  index  for  the  seismic  case.  Table  7 illustrates the minimum reliability obtained for the displacement response.

Table-6: Iterations performed to obtain minimum reliability for (a) thrust, (b) moment and (c) shear response

|         |   Initial values | Iteration # for thrust response   | Iteration # for thrust response   | Iteration # for thrust response   |
|---------|------------------|-----------------------------------|-----------------------------------|-----------------------------------|
|         |                  | 1 st                              | 2 nd                              | 3 rd                              |
| β       |                0 | 1.08                              | 3.60                              | 1.70                              |
| c (kPa) |               30 | 23.63                             | 49.59                             | 48.85                             |
| Φ (deg) |               31 | 33.60                             | 32.95                             | 35.20                             |
| E (MPa) |              253 | 441.75                            | 462.46                            | 368.60                            |

(a)

|         |   Initial values | Iteration # for moment response   | Iteration # for moment response   | Iteration # for moment response   | Iteration # for moment response   |
|---------|------------------|-----------------------------------|-----------------------------------|-----------------------------------|-----------------------------------|
|         |                  | 1 st                              | 2 nd                              | 3 rd                              | 4 th                              |
| β       |                0 | 0.82                              | 3.47                              | 2.84                              | 2.07                              |
| c (kPa) |               30 | 25.20                             | 13.17                             | 2.75                              | 1.42                              |
| Φ (deg) |               31 | 32.95                             | 23.43                             | 25.89                             | 24.53                             |
| E (MPa) |              253 | 425.07                            | 485.84                            | 493.88                            | 569.20                            |

(b)

|         |   Initial values | Iteration # for shear response   | Iteration # for shear response   | Iteration # for shear response   |
|---------|------------------|----------------------------------|----------------------------------|----------------------------------|
|         |                  | 1 st                             | 2 nd                             | 3 rd                             |
| β       |                0 | 0.003                            | 0.56                             | 0.31                             |
| c (kPa) |               30 | 30.00                            | 33.67                            | 33.54                            |
| Φ (deg) |               31 | 31.00                            | 30.04                            | 30.35                            |
| E (MPa) |              253 | 334.32                           | 344.18                           | 331.22                           |

(c)

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

Table-7: Iterations performed to obtain minimum reliability for displacement Response

| Reliability β   |   0 |   0.26 |   4.24 |   0.60 |
|------------------|-----|--------|--------|--------|
| c (kPa)          |  30 |  28.74 |  20.64 |  24.28 |
| Φ (deg)          |  31 |  31.40 |  31.07 |  30.78 |
| E (MPa)          |  28 |  27.35 |  12.64 |  12.55 |

The  minimum  reliability  corresponds  to  the  last  iteration  for each response. The corresponding critical values are also listed alongside.  It  is  also  worth  mentioning  that  the  successive iterations  do  not  result  in  perfect  convergence  for  the  given degree  of  tolerance.  This  could  be  attributed  to  the  sampling points  chosen  and  could  be  refined  further  to  obtain  proper convergence.  The  following  are  the  equations  (  Eq.  7  to  10) derived for the Thrust (N), Moment (M), Shear Force (Q) and deformation of the tunnel lining:

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

A comparison of the static and seismic reliability levels of the lining response is given in Table 9.

Table-9: Comparison of reliability of the static and seismic case for the lining response

|         | Thrust   | Thrust   | Thrust    | Thrust    |
|---------|----------|----------|-----------|-----------|
|         | β        | E (MPa)  | c c (kPa) | φ c (deg) |
| Static  | 1.77     | 2.02     | 34.60     | 23.40     |
| Seismic | 1.70     | 368.56   | 48.80     | 35.20     |

(a)

|         | Moment   | Moment   | Moment    | Moment    |
|---------|----------|----------|-----------|-----------|
|         | β        | E (MPa)  | c c (kPa) | φ c (deg) |
| Static  | 5.77     | 58.60    | 20.02     | 37.10     |
| Seismic | 2.07     | 569.20   | 1.42      | 24.53     |

(b)

|         | Shear   | Shear   | Shear     | Shear     |
|---------|---------|---------|-----------|-----------|
|         | β       | E (MPa) | c c (kPa) | φ c (deg) |
| Static  | 1.30    | 25.51   | 34.93     | 34.74     |
| Seismic | 0.31    | 331.22  | 33.54     | 30.35     |

(c)

## 5.1. Ultimate Limit State (ULS)

The reliability of the lining system is analysed considering the thrust, moment and shear capacity of the lining under Ultimate limit state condition.

From the RSM based reliability analysis results (Tables 6, 7), the  minimum  reliability  is  obtained  for  the  shear  response where  =0.31 indicating a probability of failure (pf) of 37.83% under  seismic  condition.  However  for  the  thrust  and  moment response, where  &gt;1, there is less probability of failure (pf &lt;4%). This indicates that the chosen lining system is reliable against  the  randomness  in  ground  material  properties  for  the thrust  and  moment response.  Table 9 also confirms that shear response  under  seismic  case  is  poorer  compared  to  the  static case.    This  implies  that  strengthening  against  shear  failure would be advisable.

## 5.2 Serviceability Limit State (SLS)

The  displacement  response  indicates  of  0.60  indicating  a probability of failure under serviceability condition as 27.42%.

## CONCLUSIONS

The response surface methodology incorporating the randomness  in  the  material  properties  of  the  ground  and  the subsequent  reliability  based  analysis  of  the  underground  soilsupport  interaction  has  been  found  to  be  useful.  The  study shows:

1. For  the  chosen  lining  system,  the  reliability  decreases under seismic conditions considering the random nature of the ground properties chosen.
2. The reliability of the lining is low for the shear response under seismic case.
3. However  considering  the  total  response  of  the  lining including the thrust, moment and shear for the ULS, the reliability is more than the SLS. Deformation and, hence, SLS is found to be the governing criterion of estimating the  reliability  of  the  support  system  as  it  provides  the least reliability index.
4. Thus, reliability based analysis gives an optimum solution to the design of underground support system.

## ACKNOWLEDGEMENTS

The computational and other support provided by IIT Bombay is gratefully acknowledged.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

## REFERENCES

- [1] Dodagoudar, G. R. and Venkatachalam, G. (2000). 'Reliability  analysis  of  slopes  using  fuzzy  sets  theory', Computers and Geotechnics, Vol. 27, pp. 101-115.
- [2] Venkatachalam, G. (2004). 'Hazard and risk evaluation of  natural  slopes',  Key  Note  Paper  presented  at  ASCE International Conf. Earth &amp;  Space,  2004,  Houston, Texas, USA.
- [3] Venkatachalam, G. (2005). 'Reliability and risk analysis of  slopes  and  application  to  landslides',  28 th Annual Lecture  of  the  Indian  Geotechnical  Society,  delivered during IGC-2005, Ahmedabad.
- [4] Sreedharan, M., Mathada, V.S. and Venkatachalam G.(2006). ' Reliability  analysis  of  rock  slopes  -  case studies', Proc.  Tenth  International  Conf.  on  Structural Engneeringand  Construction  (EASEC  -10), Bangkok, Thailand, August 3-5, 2006, Vol.8, pp. 71-76.
- [5] Hasofer, A.M.  and  Lind,  N.C.  (1974).  'Exact  and invariant second-moment code format', Journal of Engineering  Mechanics,  ASCE,  Vol.  100(1),  pp.  111121.
- [6] Haldar,  S  and  Babu,  G.L.Sivakumar  (2008).  '  LoadResistance factor design of axially loaded pile based on load test results', Jl. Geotech.Geoenv.Eng.,  ASCE, Vol.134, No.8, pp.1106-1117.
- [7] Hashash, Y. M. A., Hook, J. J., Schmidt, B. and  Yao, J. C. (2001). 'Seismic design and analysis of underground structures', Tunnelling and Underground Space Technology, Vol. 16, pp. 247-293.
- [8] Kulhawy,  F.  H.  (1975).  'Stresses  and  displacements around  openings  in  homogeneous  rock',  International Journal  of  Rock  Mechanics  and  Mining  Science  &amp; Geomechanics Abstracts, Vol. 12, pp. 43-57.
- [9] Naik,  A,  V.  (1981).  'Interactive  analysis  of  tunnels  in layered  medium  using  finite  and  infinite  elements', Ph.D. Thesis, 1981, IIT Bombay, India.
- [10] Myers, R.H. and Montgomery, D.C. (1995). 'Response surface  methodology  process  and  product  optimization using  design  experiments',  John  Wiley  &amp;  Sons,  New York.
- [11] Gui,  M.W.  and  Chien,  M.C.  (2006).  'Blast-resistant analysis  for  a  tunnel  passing  beneath  Taipei  Shongsan airport - a parametric study', Geotechnical and Geological Engineering, Vol. 24, pp. 227-248.
- [12] American  Concrete  Institute,  (2005).  'Building  code requirements for structural concrete (ACI 318-05)', ACI Committee 318, Michigan.
- [13] Mollon, G., Dias, D and Soubra, A.H. (2009). 'Probabilistic analysis of circular tunnels in homogeneous soil using response surface methodology', Journal of Geotechnical and Geoenvironmental Engineering, ASCE, Vol 135(9), pp. 1314-1325.
- [14] National Geophysical Data Centre., University of California, Seismograph station, Berkeley, CA  and

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

Institute  of  Earth  Sciences  of  the  Academia  Sinica, Taipei, Taiwan.
## ORIGINAL ARTICLE

## Performance prediction of roadheaders used in coal mines from the needle penetration index and the schmidt hammer value

Masoud Rostami · Sair Kahraman · Behnaz Dibavar · Mustafa Fener

Received: 21 March 2022 / Accepted: 12 December 2023 © The Author(s) 2024

Abstract Coal mine galleries and construction tunnels are commonly excavated using roadheaders. Estimating the performance of roadheaders is crucial for planning  and  cost  estimation  when  planning  tunnel or tunnel projects. The aim of this study is to derive generalized  performance  prediction  models  including Schmidt hammer value, needle penetration index, and  volumetric  joint  count  for  roadheaders  used  in coal mines. The performance measurements of axial and transverse  type  roadheaders  were  carried  out  in six different coal mines. Schmidt hammer tests, needle  penetration  index  tests,  and  of  volumetric  joint count measurements were also performed at the locations  where  the  performance  measurements  were conducted.  The  extensive  data  were  evaluated  using multiple linear and nonlinear regression analysis. The developed  formulas  were  evaluated  using  statistical tests. The Equations that include the Schmidt hammer value or needle penetration index value in addition to cutter head power have been shown to be unreliable. However, the equations that include Schmidt hammer

M. Rostami · B. Dibavar

Institute of Science, Hacettepe University, Ankara, Turkey

S. Kahraman ( * )

Mining Engineering Department, Hacettepe University, Ankara, Turkey

e-mail: sairkahraman@yahoo.com

M. Fener

Geological Engineering Department, Ankara University, Ankara, Turkey

<!-- image -->

Icon

value  or  needle  penetration  index  value  in  addition to cutterhead power and volumetric joint count have been shown to be reliable. This study concludes that the developed reliable equations can be used for the

mines.

## Article highlights

- Performance  prediction  models  were  developed for roadheaders used in coal mines.
- The models include Schmidt hammer, needle penetration index, and volumetric joint count values.
- The developed reliable equations can be used for roadheader performance used in coal mines.

Keywords Roadheaders · Performance prediction · Coal mines

## 1  Introduction

Mechanical  excavation  of  rocks  and  coals  is  widely applied  around  the  world.  Roadheaders  have  been commonly used for the excavation of rocks in tunnel projects and roadway projects in mining since about the1960s. When planning tunnel or roadway projects, assessing  the  performance  of  a  roadheader  is  very important for planning and cost estimation.

Vol.: (0123456789)

<!-- image -->

Logo

Table 1 The performance estimation equations derived by different authors for roadheaders

|   Model number | Model                                                                    | Reference                      | Remarks                                          |
|----------------|--------------------------------------------------------------------------|--------------------------------|--------------------------------------------------|
|              1 | NCR = k P SE                                                             | Rostami et al. (1994)          | -                                                |
|              2 | NCR = 719 σ 1.78 c                                                       | Gehring (1989)                 | 250 kW transverse e type cutterhead              |
|              3 | NCR = 1739 σ 1.13                                                        | Gehring (1989)                 | 230 kW axial type cutterhead                     |
|              4 | c NCR = 0.28 P ( 0.974 ) RMCI RMCI = u1D70E c ( RQD 100 ) 2 ∕ 3          | Bilgin et al. (1990)           | Axial type cutterhead                            |
|              5 | NCR = 27.11 e 0.0023 RPI RPI = PW u1D70E c                               | Copur et al. (1998)            | Transverse type cutterhead, for evaporitic rocks |
|              6 | NCR = 75.7 - 14.3 ln σ c                                                 | Thuro and Plinninger (1999)    | 132 kW transverse e type cutterhead              |
|              7 | NCR = 109.25 σ - 0.72 c NCR = 81.21 SH - 0.78                            | Tumac et al. (2007)            | 90 kW axial type cutterhead                      |
|              8 | NCR = 510588 σ - 2.1779 c                                                | Ocak and Bilgin (2010)         | 300 kW transverse e type cutterhead              |
|              9 | RMBI = e ( σ c ∕σ t ) x ( RQD 100 ) 3 NCR = 30.75 RMBI 0.23              | Ebrahimabadi et al. (2011)     | 82 kW axial type cutterhead                      |
|             10 | NCR = 1.79 u1D70E c + 0.501 u1D6FC + 0.636 RQD - 4.839 u1D70E t - 22.127 | Abdolreza and Yakhchali (2013) | 82 kW axial type cutterhead                      |
|             11 | NCR = - 2.92 I s - 0.79 A w + 22.95                                      | Kahraman and Kahraman (2016)   | 112 kW axial type cutterhead                     |
|             12 | NCR = - 8.58 lnNPI + 55.06                                               | Kahraman et al. (2019)         | 112 kW axial type cutterhead                     |

NCR is net cutting rate ­ (m 3 /h), P is cutterhead power (kW), k is energy transfer coefficient (0.45-0.55), SE is specific energy (kWh/ m 3 ), σ c is compressive strength (MPa), σ t is indirect tensile strength (MPa), RQD is rock quality designation (%), RPI is roadheader penetration index (kWxt/MPa), W is machine weight (ton), SH is Shore hardness, RMBI is rock mass brittleness index, α is the angle between tunnel axis and weakness planes, ­ I s is point load strength (MPa), ­ A w is water absorption ratio (%), and NPI is needle penetration index (N/mm)

Several  researchers  have  recommended  prediction  models  for  roadheader  performance  (Table  1). However,  most  of  them  are  not  generally  applicable  because  they  do  not  take  machine  parameters and  rock  mass  properties  into  account.  Models  1,  4 and 5 listed in Table 1 include machine parameters. Model 1 is theoretical and too general and does not consider rock mass properties. Therefore, its estimation capability is limited. Model 5 proposed by Copur et al. (1998) is based on data obtained only from the excavation of evaporite rocks. It may not be applicable  to  other  rock  types  such  as  coal  measure  rocks. Since it includes cutterhead power and RQD, Model 4 suggested by Bilgin et al. (1990) is the most general formula. However, it includes uniaxial compressive strength that is obtained from tedious and timeconsuming  process.  The  performance  prediction  of roadheaders  will  be  very  useful  using  easy  testing

Vol:. (1234567890)

<!-- image -->

Icon

methods  such  as  Schmidt  hammer  and  needle  penetration tests. These tests can easily be applied in the field. The usability of an experiment on-site is valuable because it gives us the properties of rocks at their natural moisture content and under geological stress.

As  shown  in  Table  1,  Goktan  and  Gunes  (2005) derived an estimation equation for the net cutting rate (NCR)  for  90  kW  axial  type  roadheader,  including the  Schmidt  hammer  value.  Kahraman  et  al.  (2019) derived an estimation equation of NCR for 112 kW axial  type  roadheader,  including  the  needle  penetration  index.  Since  these  models  were  developed  for specific machines and do not contain machine parameters,  they  cannot  be  generalized.  If  a  performance prediction  model  does  not  include  machine  parameters, it can only be used for a specific machine and cannot  be  used  for  machines  with  different  characteristics  such  as  cutterhead  power.  For  this  reason, generalized performance prediction models for roadheaders should be developed. The aim of this study is to derive generalized performance estimation models for roadheaders used in coal mines, including the Schmidt hammer value, the needle penetration index, and the volumetric joint count. The Schmidt hammer and  the  needle  penetration  index  tests  are  selected for the models to be developed since they are simple, cheap, easy to perform, and applicable practically in the  field.  The  Schmidt  hammer  and  the  needle  penetration  index  tests  are  selected  for  the  models  to be  developed  because  they  are  simple,  inexpensive, easy to perform, and practical to use in the field. The highly jointed structure of coal and coal measure rock has a great influence on roadheader performance. For this  reason,  the  joint  structure  of  formation  must  be included in performance models. RQD or volumetric joint  count  can  be  included  in  the  models  regarding joint  structure.  RQD  is  determined  from  drill  cores and  it  is  impossible  to  measure  it  during  roadway excavation.  On  the  other  hand,  the  RQD  values  of coal  and  coal  measure  rocks  are  extremely  low.  For these  reasons,  JV  was  chosen  to  be  included  in  the performance models in this study.

## 2   Field studies

## 2.1   Study areas

Field  studies  were  conducted  in  six  different  coal basin  in  Türkiye:  Soma,  Kınık,  Çayırhan,  Dodurga and  Amasra  coal  fields.  The  Soma  Basin  is  located about  25  km  from  Soma  District  in  Manisa  Province,  100  km  northeast  of  İzmir  and  50  km  from the  Aegean  coast.  It  is  the  neighboring  village  of Eynez to the  southwest.  The  Kınık  Basin  is  located near  Elmadere  Village  in  Kınık  District.  The  mine site  is  located  in  the  Aegean  region,  approximately 150  km  north  of  Izmir  Province  and  approximately 9  km  southeast  of  Kınık  District.  The  Çayırhan Basin is located in Çayırhan Town, Nallıhan District, and  Ankara  Province.  The  basin  is  located  on  the Ankara-Nallıhan  road  and  is  122  km  from  Ankara. The Dodurga Basin is located in  Alpagut  village  of Dodurga  District,  45  km  north  of  Çorum  Province. The Amasra Basin lies within the borders of Bartın Province in northwestern Anatolia.

## 2.2   Performance measurements

The  performance  measurements  of  axial  and  transverse e type roadheaders were carried out in six different  coal  mines  during  roadway  excavation.  The rock  types  covered  in  the  study  include  sandstone, marl, schist, claystone, and coal. The operating times of the roadheaders were noted during excavation, and the excavation volumes were calculated based on the cross-sectional  area  of  roadway  and  advance  length. The NCR values were then calculated by dividing the excavated volume by the operating times.

## 2.3   Schmidt hammer experiments

Several  researchers  have  attempted  to  estimate  the strength of concrete and rock through a Schmidt hammer experiment (Inoue and Omi 1970; Sheorey et al 1984; Haramy and DeMarco 1985; Sachpazis 1990; Kahraman  2001;  Karaman  and  Kesimal  2015,  Teymen 2021,  etc.).  The  Schmidt  hammer  can  be  used in  both  laboratory  and  field  investigations.  Its  field use is common because it is a lightweight and portable device. It has also been used to evaluate the discontinuity planes of rock mass (Young 1978), strata control of mines (Kidybinski 1968), roadheader performance (Poole and Farmer 1978); the performance of  rock  drills  (Howart  et  al.  1986;  Kahraman  1999; Kahraman et al. 2000) and the strength joint surfaces (ISRM 1978).

Before the excavation of each round, the Schmidt hammer (L-type) tests were carried out at the roadway  faces. The  experiments were performed  by applying  a  single  impact  to  ten  different  points  on roadway  faces.  The  average  Schmidt-Hammer  ­ (R L ) values were then calculated for each case.

## 2.4   Needle penetration experiments

The  needle  penetrometer  (Fig. 1) was  originally developed  for  predicting  the  uniaxial  compressive strength (UCS) of soft/very soft rocks. Since then, it has  been  applied  to  predict  the  index  characteristics of  soft  rocks  (Yamaguchi  et  al.  1997;  Ulusay  et  al. 2014;  Erguler  and  Ulusay  2007;  Aydan  et  al.  2008, 2014; Park et al. 2011; etc.). The test is simple and practical,  and  no  sample  preparation  is  required  for the experiment. The experiment can be conducted on

Vol.: (0123456789)

<!-- image -->

Icon

Fig. 1 The needle penetrometer

<!-- image -->

Photograph

the smooth surfaces of small specimens in the laboratory  as  well  as  on  the  faces  of  large  rock  blocks, slopes,  and  tunnels  in  the  field.  After  pushing  the needle of the device into rock surface until it reaches 100 N forces, the penetration distance is read with the help  of  a  presser  on  the  penetration  scale.  For  very soft  rocks,  the  maximum  penetration  distance  of 10  mm  can  be  achieved  before  the  maximum  force is applied. In this case, the experiment is terminated and the force is read using the force scale. The needle penetration index (NPI) is calculated using the equation below (Ulusay et al. 2014):

<!-- formula-not-decoded -->

where NPI is the needle penetration index (N/mm), F is penetration force (N), and D is penetration distance (mm).

The UCS of soft rocks can be predicted using the formula below (Ulusay et al. 2014):

<!-- formula-not-decoded -->

where σ c is the UCS (MPa), and the NPI is the needle penetration index (N/mm).

The UCS of the coals can be estimated from the following equation (Kahraman et al. 2017):

<!-- formula-not-decoded -->

Before the roadheader started excavation, the NPI experiments were conducted at the ten different points of excavation faces (Fig. 2). After computing the NPI values, the average of ten measurements was accepted as the NPI value for the roadway face.

## 2.5   Volumetric joint count

Before  the  roadheaders  started  excavation,  discontinuity  measurements  were  performed  on  the  roadway faces. The joint numbers in each joint set were

Vol:. (1234567890)

<!-- image -->

Icon

Fig. 2 Needle  penetration  experiment  at  gallery  face  composed of claystone

<!-- image -->

Photograph

measured  along  a  scanline  using  a  steel  measuring tape. It was difficult to obtain multiple scanlines underground. However, this was done with the help of mine workers. The corrections for the biases arising from the angle between the scanline and the joint sets were ignored.

The volumetric joint count ­ (J v ) is described as the total  number  of  joints  intersecting  a  unit  volume  of rock mass and can be calculated using the following equation (ISRM 2007):

<!-- formula-not-decoded -->

where ­ J v is the volumetric joint count (joints/m 3 ), N is the number of joints along a scanline, L is the length of the scanline and n is the number of joint sets.

The  ­ J v values  were  calculated  using  Eq.  (4)  for each case. If the roadway face was composed of coal and  rock,  the  ­ J v values  were  calculated  separately, and then the weighted ­ J v value was calculated. Since coal seams have cleat systems, they have too high ­ J v values. Coal measure rocks also have high ­ J v values. Most of the ­ J v values of coal measure rocks calculated in this study are between 50 and 100 joints/m 3 . Measured ­ J v values  of  coal  seams  are  always  higher  than 150 joints/m 3 (Fig. 3). It has been experienced that ­ J v values  above  150  do  not  affect  performance.  Therefore, ­ J v values for coals are accepted as 151 in regression analyses.

Fig. 3 Histogram plot of the ­ J v values

<!-- image -->

Bar chart

## 3   Results and discussions

The summary of NCR, ­ R L , NPI and ­ J v values are given in Tables 2, 3, 4 and 5. The number of data belonging to the ­ R L and the NPI measurements consists of 37 and 35  for  axial  type  roadheaders,  respectively.  For  transverse e type roadheaders, the number of data pertaining to the RL and the NPI measurements consists of 49 and 37, respectively.

Performance  measurements  and  tests  results  were interpreted with the help of multiple regression analysis to derive estimation formulas for NCR. First, cutterhead power, ­ R L , and NPI values were included to the regression  analysis.  Then,  in  addition  to  cutterhead  power, RL, and NPI values, ­ J v values are added to the regression analyses. The developed formulas and the coefficient of correlations are as follows:

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

where NCR is the net cutting rate ­ (m 3 /h), P is cutterhead power (kW), ­ R L is the L-type Schmidt hammer value,  NPI  is  the  needle  penetration  index  (N/mm), and Jv is the volumetric joint count (joint/m 3 ).

Multiple nonlinear regression analyses were also  performed  to  develop  the  estimation  equations for NCR. The double logarithmic method was used here. The formula of the method is as follows (Choi 1978):

Vol.: (0123456789)

<!-- image -->

Logo

| Table 2 Statistical parameters of NCR, ­ R L and ­ J v values for axial type roadheaders  Case 1  Case 2  Case 3  Case 4  75 kW  112 kW  160 kW  200 kW  Statistical parameter  NCR ­ (m  3  /h)  RL  J  v  (Jo-ints/m  3  )  NCR ­ (m  3  /h)  RL  J  v  (Jo-ints/m  3  )  NCR ­ (m  3  /h)  RL  J  v  (Jo-ints/m  3  )  NCR ­ (m  3  /h)  RL  J  v  (Jo-ints/m  3  )  Number of observ.  7  7  7  17  17  17  6  6  6  7  7  7  Minimum  6.4  31.5  117.0  13.5  16.8  53.3  10.1  30.5  55.6  5.5  31.8  8.3  Maximum  9.0  36.8  151.0  41.7  33.4  130.5  16.3  39.8  151.0  6.3  37.8  15.3  Average  7.5  34.0  142.3  21.9  23.8  94.3  13.5  35.0  111.3  5.8  34.6  11.3  Standard deviation  ± 0.9  ± 1.7  ± 1176  ± 7.5  ± 4.3  ± 27.6  ± 2.2  ± 3.4  ± 36.6  ± 0.3  ± 2.2  ± 2.8   |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

Vol:. (1234567890)

<!-- image -->

Icon

<!-- formula-not-decoded -->

where,  Y  is  the  estimated  parameter,  a  is  the  intercept, ­ X 1 , ­ X 2 , ­ X n are the independent parameters, and ­ b1 , ­ b2 , ­ bn are the coefficients of ­ X 1 , ­ X2, ­ X n .

If the logarithm of both sides of Eq. (13) is taken, the equation turns into linear form as follows:

<!-- formula-not-decoded -->

Equation (14) can be expressed as a linear regression function as follows:

<!-- formula-not-decoded -->

Cutterhead  power,  Schmidt  hammer  value,  needle  penetration  index,  and  volumetric  joint  count were included in the multiple nonlinear regression analyses.  The  developed  equations  and  the  coefficient of correlations are as follows:

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

The  correlation  coefficient  values  of  nonlinear equations are very strong and are also greater than those  of  linear  equations.  The  standard  errors  of nonlinear  equations  are  much  lower  than  those  of linear equations as illustrated in Table 6.

The correlation  coefficient  values  of  all  derived formulas  are  strong  or  very  strong.  However,  a good  correlation  coefficient  does  not  always  indicate the validity of a model. Further statistical tests should be done. The accuracy control of the developed formulae was carried out using t- and F-tests, and  the  diagrams  of  measured  and  predicted  NCR values. Parametric tests, such as the t- and F tests, assume that data are normally distributed. If a large data set (&gt; 30) is used, it is assumed to be normally distributed. Because the data sets used in this study are greater than 30, it is assumed the data are normally distributed.

Table 3 Statistical parameters of NCR, NPI, and ­ J v values for axial type roadheaders

| Statistical parameter   | Case 1               | Case 1     | Case 1           | Case 2                | Case 2     | Case 2           |
|-------------------------|----------------------|------------|------------------|-----------------------|------------|------------------|
|                         | 75 kW NCR ­ (m 3 /h) | NPI (N/mm) | Jv (Joints/m 3 ) | 112 kW NCR ­ (m 3 /h) | NPI (N/mm) | Jv (Joints/m 3 ) |
| Number of observ.       | 7                    | 7          | 7                | 28                    | 28         | 28               |
| Minimum                 | 6.4                  | 38.5       | 117.0            | 13.5                  | 4.2        | 75.1             |
| Maximum                 | 9.0                  | 89.7       | 151.0            | 50.4                  | 29.7       | 151.0            |
| Average                 | 7.5                  | 51.0       | 142.3            | 33.9                  | 13.1       | 134.5            |
| Standard deviation      | ± 0.9                | ± 18.1     | ± 1176           | ± 10.6                | ± 6.3      | ± 24.8           |

Table 4 Statistical parameters of NCR, ­ R L and ­ J v values for transverse e type roadheaders

| Statistical parameter   | Case 1         | Case 1   | Case 1           | Case 2         | Case 2   | Case 2           | Case 3         | Case 3   | Case 3           |
|-------------------------|----------------|----------|------------------|----------------|----------|------------------|----------------|----------|------------------|
| Statistical parameter   | 100 kW         | 100 kW   | 100 kW           | 132 kW         | 132 kW   | 132 kW           | 160 kW         | 160 kW   | 160 kW           |
| Statistical parameter   | NCR ­ (m 3 /h) | R L      | Jv (Joints/m 3 ) | NCR ­ (m 3 /h) | R L      | Jv (Joints/m 3 ) | NCR ­ (m 3 /h) | R L      | Jv (Joints/m 3 ) |
| Number of observ.       | 20             | 20       | 20               | 26             | 26       | 26               | 3              | 3        | 3                |
| Minimum                 | 4.0            | 11.7     | 8.3              | 12.0           | 10.0     | 92.9             | 9.9            | 19.8     | 57.3             |
| Maximum                 | 22.3           | 32.0     | 151.0            | 36.0           | 30.4     | 151.0            | 44.8           | 47.0     | 84.5             |
| Average                 | 13.3           | 18.7     | 117.9            | 21.6           | 19.1     | 134.5            | 22.2           | 39.9     | 73.3             |
| Standard deviation      | ± 4.6          | ± 6.0    | ± 54.1           | ± 7.3          | ± 6.3    | ± 23.4           | ± 19.6         | ± 15.7   | ± 14.2           |

Table 5 Statistical parameters of NCR, NPI and ­ J v values for transverse e type roadheaders

| Statistical parameter   | Case 1                | Case 1     | Case 1           | Case 2                | Case 2     | Case 2           |
|-------------------------|-----------------------|------------|------------------|-----------------------|------------|------------------|
|                         | 100 kW NCR ­ (m 3 /h) | NPI (N/mm) | Jv (Joints/m 3 ) | 132 kW NCR ­ (m 3 /h) | NPI (N/mm) | Jv (Joints/m 3 ) |
| Number of observ.       | 17                    | 17         | 17               | 20                    | 20         | 20               |
| Minimum                 | 11.8                  | 6.4        | 54.2             | 12.0                  | 6.2        | 92.9             |
| Maximum                 | 22.3                  | 32.5       | 151.0            | 36.0                  | 40.6       | 151.0            |
| Average                 | 15.1                  | 15.1       | 138.4            | 22.5                  | 16.1       | 132.4            |
| Standard deviation      | ± 2.5                 | ± 7.4      | ± 27.6           | ± 8.0                 | ± 10.0     | ± 23.8           |

The  t-test  can  be  used  to  determine  the  significance of r values. In the test,  calculated  and  tabulated  t-values  are  compared  using  the  null  hypothesis.  If  the  calculated  t-value  is  larger  than  the tabulated  t-value,  the  null  hypothesis  is  rejected. This indicates that r is significant. If the calculated t-value  is  lower  than  the  tabulated  t-value,  the null  hypothesis is not rejected, suggesting that r is insignificant.  As  depicted  in  Table  6,  some  of  the t-values  calculated  for  Eqs.  (5-8)  are  smaller  than the tabulated t-values, indicating some doubt about the  models.  However,  the  calculated  t-values  are larger than the tabulated t-values for Eqs. (9-12 and 16-19), suggesting the models are valid.

Vol.: (0123456789)

<!-- image -->

Icon

| Table 6 The results of t- and F-test   | Equation no   | Independent variable                                       |   Standard error | t-value                     |   Tabu- lated t-value |   F-value |   Tabulated F-value |
|----------------------------------------|---------------|------------------------------------------------------------|------------------|-----------------------------|-----------------------|-----------|---------------------|
|                                        | (5)           | Constant P (kW) R L                                        |             5.47 | 10.42 - 0.14 - 7.06         |                  1.96 |     28.95 |                4.13 |
|                                        | (6)           | Constant P (kW) NPI (N/mm)                                 |             9.18 | - 0.06 1.78 - 2.09          |                  1.96 |     25.37 |                4.08 |
|                                        | (7)           | Constant P (kW) R                                          |                6 | - 1.01 5.96 - 5.1           |                  1.96 |     23.25 |                4.13 |
|                                        | (8)           | L Constant P (kW) NPI (N/mm)                               |              4.4 | - 0.65 5.64 - 6.14          |                  1.96 |     29.96 |                4.08 |
|                                        | (9)           | Constant P (kW) R L J (joint/m 3 )                         |             4.66 | 5.58 2.72 - 8.95 3.72       |                  1.96 |     31.17 |                 3.2 |
|                                        | (10)          | v Constant P (kW) NPI (N/mm) J v (joint/m 3 )              |             6.84 | - 2.39 2.96 - 2.55 6.16     |                  1.96 |     39.34 |                3.27 |
|                                        | (11)          | Constant P (kW) R L 3                                      |             5.72 | - 1.99 6.09 - 4.72          |                  1.96 |     18.89 |                 3.2 |
|                                        | (12)          | J v (joint/m ) Constant P (kW) NPI (N/mm) J v (joint/m 3 ) |             4.17 | 2.36 - 2.01 6.3 - 6.74 2.21 |                  1.96 |     23.87 |                3.27 |
|                                        | (16)          | Constant P (kW) R L 3                                      |              0.1 | 2.13 5.27 - 10.73           |                  1.96 |     69.12 |                 3.2 |
|                                        | (17)          | J v (joint/m ) Constant P (kW) NPI (N/mm) 3                |              0.9 | 7.39 - 6.77 8.54 - 4.08     |                  1.96 |    121.22 |                3.27 |
|                                        | (18)          | J v (joint/m ) Constant P (kW) R L J (joint/m 3 )          |             0.12 | 5.5 - 3.74 5.55 - 4.64 6.25 |                  1.96 |     36.84 |                 3.2 |
|                                        | (19)          | v Constant P (kW) NPI (N/mm) J v (joint/m 3 )              |             0.05 | - 2.27 7.65 - 12.95 2       |                  1.96 |     76.33 |                3.27 |

Vol:. (1234567890)

<!-- image -->

Icon

Fig. 4 The  diagram  of  measured  versus  estimated  NCR  for Eq. (9)

<!-- image -->

Scatter plot

<!-- image -->

Scatter plot

Fig. 6 The  diagram  of  measured  versus  estimated  NCR  for Eq. (11)

<!-- image -->

Scatter plot

Fig. 5 The  diagram  of  measured  versus  estimated  NCR  for Eq. (10)

<!-- image -->

Scatter plot

Variance  analysis  was  performed  to  check  the significance of regressions. It uses F-test to statistically  evaluate  the  equality  of  means.  If  the  calculated  F-value  is  larger  than  the  tabulated  F-value, the  null  hypothesis  is  rejected,  suggesting  there  is an actual relation between dependent and independent variables. As depicted in Table 6, since the calculated F-values of all equations are larger than the tabulated  F-values,  the  null  hypothesis  is  rejected. Therefore, it can be said that all developed formulae are valid according to F-test.

The  scatter  graphs  of  measured  and  estimated NCR values were examined to  check  the  prediction capability  of  the  developed  formulas.  Data  points should  ideally  be  scattered  around  a  1:1  diagonal straight  line  on  the  plot  of  measured  versus  predicted  values.  A  systematic  deviation  from  the  1:1 line  shows  that  greater  errors  tend  to  accompany greater estimations, indicating non-linearity in one or more variables. Because there are some doubts about Eqs. (5-8), the scatter graphs of these equations are not plotted. As illustrated in Figs. 4, 5, 6, and 7, the data points are almost evenly scattered around the 1:1 line,  suggesting  Eqs.  (9-12)  are  valid.  Therefore,  it can be said that Eqs. (9-12) can be reliably used to Vol.: (0123456789)

Fig. 7 The  diagram  of  measured  versus  estimated  NCR  for Eq. (12)

<!-- image -->

Logo

Fig. 8 The  diagram  of  measured  versus  estimated  NCR  for Eq. (16)

<!-- image -->

Scatter plot

<!-- image -->

Scatter plot

Fig. 10 The  diagram  of  measured  versus  estimated  NCR  for Eq. (18)

<!-- image -->

Scatter plot

Fig. 9 The  diagram  of  measured  versus  estimated  NCR  for Eq. (17)

<!-- image -->

Scatter plot

estimate roadheader performances used in coal mines. Figures 8, 9, 10 and 11 show the scatter graphs of the nonlinear equations (Eqs. 16-19). It is seen that the nonlinear equations have higher prediction capability than those of the linear equations.

Since  most  of  the  available  models  were  developed  for  specific  machines  and  do  not  contain machine  parameters,  they  cannot  be  generalized. Models 4 and 5, listed in Table 1, include machine parameters, but the rock parameters they include are

Vol:. (1234567890)

Fig. 11 The  diagram  of  measured  versus  estimated  NCR  for Eq. (19)

<!-- image -->

Icon

direct test methods that are difficult to perform and cannot  be  applied  in  the  field.  The  models  developed  in  this  study  are  generalizable  because  they contain machine parameters. They will also be very useful as they include simple testing methods such as  Schmidt  hammer  and  needle  penetration  tests that  can  be  practically  used  in  the  field.  In  these respects,  the  developed  models  are  more  advantageous than the existing models.

## 4   Conclusions

The extensive data was interpreted  using  multiple regression analysis to  develop  generalized  performance  estimation  formulas  for  both  axial  and transverse  type  roadheaders  used  in  coal  mines. It  was  shown  that  the  equations,  which  included not  only  cutting  head  power  and  volumetric  joint number  but  also  the  Schmidt  hammer  value  or the  needle  penetration  index  value,  were  reliable. However,  the  models  for  axial  type  roadheaders  were  developed  with  cutterhead  power  ranging  from  75  to  200  kW  and  cover  the  NCR  range of 5.5-50.4 ­ m 3 /h. They may not be valid for other values  of  these  parameters.  Similarly,  the  models for  transverse  type  roadheaders  were  derived  with cutterhead power varying from 100 to 160 kW and the NCR ranging from 4.0 to 44.8 ­ m 3 /h. It's possible that they are not valid for other values of these parameters.

It was concluded that the developed reliable equations  could  be  used  to  estimate  the  performance  of roadheaders used in coal mines. The estimation capabilities of the developed nonlinear models are higher than  those  of  the  linear  models.  The  validity  of  the derived  formulas  should  be  checked  for  rocks  other than coal and coal-measure rocks.

Acknowledgements We would like to thank TUBITAK (The Scientific and Technological Research Council of Turkey) for supporting the project (Project No. 217M740). We also thank Park Termik Elektrik San. ve Tic. A.Ş., Hattat Enerji ve Maden Tic. A.Ş., Polyak Eynez Enerji Üretim Madencilik San. ve Tic. A.Ş.,  İmbat  Madencilik  Enerji  Turizm  San.  Tic..A.Ş.,  Demir Export A.Ş., YS Madencilik San. ve Tic. Ltd. Ş. and Kömür İşletmeleri A.Ş. for allowing the field studies.

## Declarations

Competing interests The authors declare that they have no conflict of interest.

Open Access This article is licensed under a Creative Commons  Attribution  4.0  International  License,  which  permits use,  sharing,  adaptation,  distribution  and  reproduction  in  any medium or format, as long as you give appropriate credit to the original  author(s)  and  the  source,  provide  a  link  to  the  Creative Commons licence, and indicate if changes were made. The images or other third party material in this article are included in  the  article's  Creative  Commons  licence,  unless  indicated otherwise  in  a  credit  line  to  the  material.  If  material  is  not included  in  the  article's  Creative  Commons  licence  and  your intended use is not permitted by statutory regulation or exceeds the permitted use, you will need to obtain permission directly from the copyright holder. To view a copy of this licence, visit http:// creat iveco mmons. org/ licen ses/ by/4. 0/.

## References

- Abdolreza  YC,  Yakhchali  SH  (2013)  A  new  model  to  predict  roadheader  performance  using  rock  mass  properties. J Coal Sci Eng 19(1):51-56. https:// doi. org/ 10. 1007/ s12404- 013- 0109-4
- Aydan O, Sato A, Yagi M (2014) The inference of geo-mechanical  properties  of  soft  rocks  and  their  degradation  from needle penetration tests. Rock Mech Rock Eng 47:18671890. https:// doi. org/ 10. 1007/ s00603- 013- 0477-5
- Aydan  O,  Watanabe  S  and  Tokashiki  N  (2008)  The  inference  of  mechanical  properties  of  rocks  from  penetration tests. In: Proc. the 5th Asian rock mechanics symposium (ARMS5), Tehran. pp 213-220
- Bilgin  N,  Seyrek  T,  Erdinc  E,  Shahriar  K  (1990)  Roadheaders  clean  valuable  tips  for  Istanbul  Metro.  Tunn  Tunnell 22:29-32
- Choi SC (1978) Introductory statistics in science. Prentice Hall Inc, New Jersey
- Copur H, Ozdemir L, Rostami J (1998) Roadheader applications in mining and tunneling industries. In: Annual meeting of american society for mining, metallurgy and exploration (SME), Orlando, Florida, March 10-12. pp 98-185
- Ebrahimabadi A, Goshtasbi K, Shahriar K, CheraghiSeifabad M (2011)  A  model  to  predict  the  performance  of  roadheadersbased on rock mass brittleness index. J South Afr Inst Min Metall 111:355-364
- Erguler ZA, Ulusay R (2007) Estimation of uniaxial compressive strength of clay-bearing weak rocks using needle penetration response. In: Proc. 11th congress on international society for rock mechanics, Lisbon, pp 265-268
- Gehring  KH  (1989)  A  cutting  comparison.  Tunn  Tunnell 21:27-30
- Göktan R, Güneş N (2005) A comparative study of Schmidt hammer testing procedures with reference to rock cutting machine  performance  prediction.  Int  J  Rock  Mech  Min Sci 42:466-472. https:// doi. org/ 10. 1016/j. ijrmms. 2004. 12. 002
- Haramy KY, DeMarco MJ (1985) Use of the schmidt hammer for rock and coal testing. In: 26th U.S. symposium on rock mechanics, rapid city, pp 549-555
- Howart  DF,  Adamson  WR,  Berndt  JR  (1986)  Correlation  of model  tunnel  boring  and  drilling  machine  performances with  rock  properties.  Int  J  Rock  Mech  Min  Sci  23:171175. https:// doi. org/ 10. 1016/ 0148- 9062(86) 90344-X
- Inoue M, Omi M (1970) Study on the strength of rocks by the Schmidt hammer test. Proc Rock Mech Jpn 1:177-179
- ISRM  (1978)  Suggested  methods.  Suggested  method  for  the quantitative description of discontinuities in rock masses. Int J Rock Mech Min Sci 15:319-368. https:// doi. org/ 10. 1016/ 0148- 9062(78) 91472-9
- ISRM (2007) The complete ISRM suggested methods for rock characterization,  testing  and  monitoring:  1974-2006.  In: Ulusay R, Hudson JA (eds) Suggested methods prepared by  the  commission  on  testing  methods,  international

Vol.: (0123456789)

- society for rock mechanics. Compilation Arranged by the ISRM Turkish National Group, Ankara, Kozan Ofset
- Kahraman  S  (1999)  Rotary  and  percussive  drilling  prediction using regression analysis. Int J Rock Mech Min Sci 36:981-989. https:// doi. org/ 10. 1016/ S0148- 9062(99) 00050-9
- Kahraman S (2001) Evaluation of simple methods for assessing the uniaxial compressive strength of rock. Int J Rock Mech Min Sci 38:991-994. https:// doi. org/ 10. 1016/ S1365- 1609(01) 00039-9
- Kahraman  E,  Kahraman  S  (2016)  The  performance  prediction  of  roadheaders  from  easy  testing  methods.  Bull Eng  Geol  Envir  75:1585-1596.  https:// doi. org/ 10. 1007/ s10064- 015- 0801-2
- Kahraman S, Balcı C, Yazıcı S, Bilgin N (2000) Prediction of the penetration rate of rotary blast hole drills using a new drillability index. Int J Rock Mech Min Sci 2000(37):729743. https:// doi. org/ 10. 1016/ S1365- 1609(00) 00007-1
- Kahraman S, Aloglu AS, Aydın B, Saygın E (2017) The needle penetration  test  for  predicting  coal  strength.  J  South  Afr Inst  Min  Metall  117:587-591.  https:// doi. org/ 10. 17159/ 2411- 9717/ 2017/ v117n 6a9
- Kahraman S, Aloglu AS, Aydın B, Saygın E (2019) The needle penetration index to estimate the performance of an axial type roadheader used in a coal mine. Geomech Geophys Geo-Energ Geo-Resour 5:37-45. https:// doi. org/ 10. 1007/ s40948- 018- 0097-3
- Karaman K, Kesimal A (2015) Correlation of schmidt rebound hardness with uniaxial compressive strength and P-wave velocity of rock materials. Arab J Sci Eng 40:1897-1906. https:// doi. org/ 10. 1007/ s13369- 014- 1510-z
- Kidybinski A (1968) Rebound number and the quality of mine roof strata. Int J Rock Mech Min Sci 5:283-292. https:// doi. org/ 10. 1016/ 0148- 9062(68) 90001-6
- Ocak  I,  Bilgin  N  (2010)  Comparative  studies  on  the  performance of a roadheader, impact hammer and drilling and blasting method in the excavation of metro station tunnels in  Istanbul.  Tunn  Undergr  Sp  Tech  25:181-187.  https:// doi. org/ 10. 1016/j. tust. 2009. 11. 002
- Park Y, Obara Y, Kan SS (2011) Estimation of uniaxial compressive  strength  of  weak  rocks  using  needle  penetrometer.  In:  Proc.  12th  ISRM international congress on rock mechanics, Beijing, pp. 795-798.

Vol:. (1234567890)

<!-- image -->

Icon

- Poole  RW,  Farmer  IW  (1978)  Geotechnical  factors  affecting tunnelling  machine performance in coal measures rocks. Tunn Tunn 10:27-30
- Rostami J,  Ozdemir  L,  Neil  DM  (1994)  Performance  prediction: a key issue in mechanical hard rock mining. Min Eng 11:1263-1267
- Sachpazis CI (1990) Correlating Schmidt hardness with compressive  strength  and  Young's  modulus  of  carbonate rocks. Bull Int Assoc Eng Geol 42:75-84. https:// doi. org/ 10. 1007/ BF025 92622
- Sheorey  PR,  Barat  D,  Das  MN,  Mukherjee  KP,  Singh  B (1984)  Schmidt  hammer  rebound  data  for  estimation  of large scale in situ coal strength. Int J Rock Mech Min Sci 21:39-42. https:// doi. org/ 10. 1016/ 0148- 9062(84) 90008-1
- Teymen A (2021) Statistical models for estimating the uniaxial compressive  strength  andelastic  modulus  of  rocks  from different hardness test methods. Heliyon 7:e06891. https:// doi. org/ 10. 1016/j. heliy on. 2021. e06891
- Thuro K, Plinninger RJ (1999) Roadheader excavation performance -  geological  and  geotechnical  influences.  In:  The 9th ISRM congress, theme 3: rock dynamics and tectonophysics/rock cutting and drilling, Paris. pp 1241-1244
- Tumac D, Bilgin N, Feridunoglu C, Ergin H (2007) Estimation of  rock  cuttability  from  shore  hardness  and  compressive strength properties. Rock Mech Rock Eng 40(5):477-490. https:// doi. org/ 10. 1007/ s00603- 006- 0108-5
- Ulusay  R,  Aydan  O,  Erguler  ZA,  Ngan-Tillard  DJM,  Seiki T,  Verwaal  W,  Sasaki  Y,  Sato  A  (2014)  ISRM  suggested method  for  the needle penetration test.  Rock Mech  Rock  Eng  47:1073-1085.  https:// doi. org/ 10. 1007/ s00603- 013- 0534-0
- Yamaguchi  Y,  Ogawa  N,  Kawasaki  M,  Nakamura  A  (1997) Evaluation  of  seepage  failure  response  potential  of  dam foundation  with  simplified  tests.  J  Jpn  Soc  Eng  Geol 38(3):130-144
- Young RP (1978) Assessing  rock  discontinuities.  Tunn  Tunn 45-48

Publisher's Note Springer Nature remains neutral with regard to  jurisdictional  claims  in  published  maps  and  institutional affiliations.
<!-- image -->

Logo

## Estimation of rear-end vehicle crash frequencies in urban road tunnels

Author

Meng, Qiang, Qu, Xiaobo

Published

2012

Journal Title

Accident Analysis and Prevention

DOI

[10.1016/j.aap.2012.01.025](http://dx.doi.org/10.1016/j.aap.2012.01.025)

## Rights statement

© 2012 Elsevier. This is the author-manuscript version of this paper. Reproduced in accordance with the copyright policy of the publisher. Please refer to the journal's website for access to the definitive, published version.

## Downloaded from

[http://hdl.handle.net/10072/47097](http://hdl.handle.net/10072/47097)

## Griffith Research Online

[https://research-repository.griffith.edu.au](https://research-repository.griffith.edu.au/)

## Estimation of rear-end vehicle crash frequencies in urban road tunnels

1

Qiang Meng and Xiaobo Qu

Department of Civil and Environmental Engineering, National University of Singapore, Singapore 117576

## ABSTRACT

According to The Handbook of Tunnel Fire Safety , over 90% (55 out of 61 cases) of fires in  road  tunnels  are  caused  by  vehicle  crashes  (especially  rear-end  crashes).  It  is  thus important to develop a proper methodology that is able to estimate the rear-end vehicle crash frequency  in  road  tunnels.  In  this  paper,  we  first  analyze  the  time  to  collision  (TTC)  data collected from two road tunnels of Singapore and conclude that Inverse Gaussian distribution is the best-fitted distribution to the TTC data. An Inverse Gaussian regression model is hence used  to  establish  the  relationship  between  the  TTC  and  its  contributing  factors.  We  then proceeds to introduce a new concept of exposure to traffic conflicts as the mean sojourn time in a given time period that vehicles are exposed to dangerous scenarios, i.e. the TTC is  lower than a predetermined threshold value. A crash frequency estimation method is proposed on the basis of exposure to traffic conflicts, and we find that the rear-end vehicle crash frequency has a proportional linear relationship with the proposed exposure to traffic conflicts .

Keywords :  Rear-end crash frequency; time to collision; Inverse Gaussian regression model; road tunnels

1 Corresponding author, Tel.: +65-65165494; fax +65 6779 1635 E-mail: antielude@gmail.com (Xiaobo Qu); ceemq@nus.edu.sg (Meng Qiang).

## 1. Introduction

Road tunnels are increasingly cost-effective infrastructures which provide underground vehicular passageways for motorists and commuters, especially in densely populated cities like Singapore. With the increasing traffic volume and urban development as well as growing needs for land use in urban areas, constructing road tunnels is becoming one alternative to enhance  the  capacity  and  accessibility  for  road  transport  systems.  However,  fire  disasters occurred  in  a  road  tunnel  would  result  in  catastrophic  consequences  due  to  the  enclosed nature of tunnel systems. For example, in 1999, 39 people lost their lives in a fire disaster that happened  in  the  Mont  Blanc  Tunnel  from  France  to  Italy;  and  another  disaster  in  Tauern Tunnel of Austria resulted in 12 fatalities (PIARC, 2008). These accidents have raised the awareness  among  the  public  as  well  as  the  government  on  both  the  safety  aspect  of  the tunnels and that of the road tunnel users. Thus, quantitative risk assessment (QRA) has been one  of  the  requirements  under  the  European  Union  (EU)  Directive  (2004/54/EC).  In Singapore, QRA for all major urban road tunnels longer than 240 meters is compulsory in accordance with the Project Safety Review (PSR) procedure manual for roads in the country (LTA, 2005).

Several QRA models for road tunnels have been developed, including TuRisMo model of Austria,  TUNPRIM  model  of  the  Netherlands,  Italian  risk  analysis  model,  OECD/PIARC model (PIARC, 2008), and QRAFT model of Singapore (Meng et al, 2011a; Meng et al., 2011b; Qu et al., 2011). All these models acknowledge that the frequency of fire occurred in road tunnels is the most important contributing factor for the risk assessment of road tunnels. The Handbook of Tunnel Fire Safety (Beard and Carvel, 2005) points out that over 90% (55 out  of  61  fire  cases)  of  tunnel  fires  are  caused  by  vehicle  crashes  (especially  the  rear-end crashes).  In  addition,  according  to  crash  statistics  in  Singapore's  road  tunnels,  over  2/3  of crashes are categorized as rear-end crashes 2 . Accordingly, on one hand, rear-end crashes are the major cause for fire in road tunnels; on the other hand, rear-end crashes constitute around 70% out of all the crashes.  It is, therefore, of great importance to develop a methodology that can  estimate  the  rear-end  vehicle  crash  frequency  in  road  tunnels  (the  'rear-end  crash' henceforth are referred to as 'R-E crash' for short).

A number of studies have been conducted to predict/estimate frequency of various types of crashes in highways using crash-frequency data. However, identification of the cause and effect relationship is typical unavailable due to lack of microscopic traffic information (or the detailed  driving  data).  Consequently,  as  pointed  out  by  Lord  and  Mannering  (2010), researchers have framed their analytic approaches to study the factors that affect the number of crashes occurring in some geographical spaces over some specified time periods by using various  types  of  count-data  regression  models  in  accordance  to  some  assumptions.  These models include Poisson regression model (e.g. Miaou and Lum, 1993; Miaou, 1994; Hauer, 2001), Negative binomial/Poisson-Gamma model (e.g. Maycock and Hall, 1984; Malyshkina and  Mannering,  2010a;  Daniels  et  al,  2010),  Zero-inflated  Possion  and  negative  binomial models (e.g. Maiou, 1994; Shankar et al., 1997; Malyshkina and Mannering, 2010b; Lord et al.,  2007),  Conway-Maxwell-Poisson model (e.g. Lord et al., 2008; Lord et al., 2010), and others  (e.g.  Zhang  and  Xie,  2007;  Guo  et  al.,  2010;  Haque  et  al.,  2009).  The  lack  of  the detailed driving data on highways makes those statistical analysis models biased to reflect the fundamental cause and effect relationship. Lord and Mannering (2010) thus highlighted that the entirely new direction of research could potentially open up if the anticipated availability of the detailed driving data and crash data are available.

2 746 out of 1106 crashes (70%) are categorized as rear-end crashes in the CTE road tunnel from 2006 to 2008.

More detailed traffic data are obtainable in road tunnels compared to highways because most of road tunnels are equipped with the closed circuit television (CCTV) cameras and/or an operation control centre (OCC). For example, each of Singapore's road tunnels has been installed  2  to  4  CCTV  cameras  every  200  meters  and  monitored  by  a  twenty-four-hour manned operation control centre (OCC). These CCTV cameras record real time and detailed traffic  information.  In  addition  to  hourly  traffic  volume  and  density,  we  can  precisely measure/estimate  the  time  to  collision  (TTC)  for  two  consecutive  vehicles  moving  in  the same lane of a road tunnel using traffic videos. The TTC is defined as the time that remains until a collision between two vehicles would have occurred if the collision course and speed difference are maintained (Hayward, 1972). The TTC has been one of the well-recognized safety indicators for traffic conflicts on highways (Farah, et al., 2009; Svensson, 1998; Vogel, 2003). Minderhoud and Bovy (2001) further pointed out that the TTC is inversely related to vehicle  crash  frequencies  in  road  sections.  It  is  widely  accepted  as  a  safety  indicator  in highways. A TTC threshold value is usually chosen to distinguish relatively safe situation and dangerous scenarios exposed to traffic conflicts (or critical encounters). It is acknowledged that the TTC threshold should be 2 seconds to 4 seconds (Miderhoud and Bovy, 2001; Vogel, 2003).

The objective of this study is to develop a novel R-E crash frequency estimation method on the basis of TTC distributions. The TTC sample data are collected from the traffic videos of  Singapore's  road  tunnels.  Based  on  the  statistical  analysis,  we  find  that  the  Inverse Gaussian  distribution  is  the  best-fitted  distribution  model  for  the  collected  TTC  data.  The Inverse  Gaussian  regression  model  is  thus  employed  to  establish  the  relationship  between TTC distributions and the corresponding traffic volume. Having had the TTC distributions, a R-E crash frequency estimation method is put up to reflect the relationship between the TTC distributions and the R-E crash frequencies.

The remainder of this paper is organized as follows. In Section 2, the TTC is defined and the  data  collected  from  Singapore's  road  tunnels  are  presented.  In  Section  3,  the  Inverse Gaussian  regression  model  is  built  to  establish  the  relationship  between  TTC  distributions and corresponding traffic volumes. In Section 4, an R-E crash frequency estimation model is developed on the basis of the derived TTC  distributions. Several conjectures and recommendations for further studies are put forward in Section 5. Section 6 concludes this study.

## 2. TTC Data Collection

Assume that there are two consecutive vehicles moving in the same direction on the same lane  of  a  road  tunnel.  Let leader L and follower L be  the  locations  of  the  leading  and  following vehicles at a particular time, respectively. Correspondingly, let leader L  and follower L  denote the speeds  of  the  leading  and  following  vehicles  at  the  particular  time.  According  to  the  TTC definition, namely, the time that remains until a collision between two vehicles would have occurred  if  the  collision  course  and  speed  difference  are  maintained ,  the  TTC  can  be mathematically expressed by

<!-- formula-not-decoded -->

where leader l is the length of the leading vehicle.  Eqn. (1) implies that the TTC is measurable if we have real time traffic information.

To collect the TTC data in a road tunnel, the Kallang/Paya Lebar Expressway (KPE) and the Central Expressway (CTE) in Singapore shown in Figures 1 and 2 are selected. KPE and CTE are two vital infrastructures in Singapore's road system. The first one has a total length of 12 kilometers and 9 kilometers of the expressway (Figure 1) is built underground as a road tunnel,  serving  the  growing  traffic  demand  of  the  north-eastern  sector  of  Singapore.    The second one, a 17-kilometer expressway, links the north and south of Singapore through the Central  Business  District  (CBD).  2.4  kilometers  of  the  expressway  (Figure  2)  are  laid underground and these portions of the CTE form the first road tunnel in Singapore. Both road tunnels are equipped with the 24-hour OOC systems.

Figure 1: General arrangement of KPE road tunnel

<!-- image -->

Engineering drawing

Figure 2: Traffic videos recorded from CTE road tunnel

<!-- image -->

Photograph

We request 42-hour tunnel traffic videos recorded by CCTV of these two tunnels from Land Transport Authority of Singapore, including 14 locations for 3 typical time periods - morning peak hour: 8:00 am to 9:00 am, off-peak hour: 14:00 pm to 15:00 pm, evening peak hour: 19:00 pm to 20:00 pm - in Mar 2011. The TTC data are generated from these traffic videos in different time periods with different traffic conditions. The procedure of measuring a TTC with respect to a particular car-following scenario is summarized as follows. We first measure the length of the leading vehicle ( leader l ) in a car-following scenario. After that, the spot speeds of the vehicles ( follower leader and L L   ) can be estimated by measuring the time taken by the vehicle to cover two lane-markers' distance in the video. Then, the time headway ( h ) between the leading and following vehicles is recorded. According to Vogel (2003), the gap size ( ) leader follower leader L L l - - can be estimated by ( ) follower leader L h l × -  . Finally, the TTC for the car-following scenario could be calculated according to eqn. (1).

In the measurement, we display 30 frames per second to improve the data quality. 867 car following scenarios occurred at various locations are examined, and 421 TTC data (TTC with a finite value) with respect to different traffic volumes are obtained. Statistically, the number of TTC data with a finite value should be equal to that of samples with infinite values. An infinite TTC value indicates that the following vehicle will not be possible catch up with the leading  one,  which  is  an  absolutely  safe  situation.  We  would  focus  on  the  probability distributions of TTC samples with finite values accordingly.

## 3. Inverse Gaussian Distribution for TTC

## 3.1 Statistical analysis for the TTC samples

A data analysis procedure is proposed in order to obtain the best-fitted TTC distributions. Five commonly used distributions are examined in this study: Inverse Gaussian, Exponential, Normal, Triangular, and Lognormal. The maximum likelihood estimation (MLE) technique is employed  to  estimate the parameters  involved  in a distribution. After obtaining the parameters for the five types of distributions, the goodness-of-fit test is conducted to select the  best-fitted  distribution  among  the  given  candidate  distributions.  Kolmogorov-Smirnov (K-S)  test,  a  nonparametric  test,  has  been  widely  applied  to  compare  a  sample  with  a reference probability distribution in transportation studies (e.g. Ibeas et al., 2011; Páez et al., 2011). In this study, the K-S test is also adopted to perform the goodness-of-fit test. The K-S statistic  quantifies a distance between the empirical distribution function of the sample and the cumulative distribution function of the reference distribution. In this study, a distribution with the lowest K-S test statistic is regarded as the best-fitted distribution.

Following the above-mentioned data analysis procedure, we analyze five sets of the TTC data  collected  at  different  locations  with  respect  to  different  traffic  volumes,  as  shown  in Table 1.  Table 2 gives results of the best-fit analysis.

Table 1: TTC data

|            |   Traffic volume (vehs/hour∙lane) |   Number of data |
|------------|-----------------------------------|------------------|
| Location 1 |                               894 |              104 |
| Location 2 |                               963 |               65 |
| Location 3 |                              1127 |               80 |
| Location 4 |                              1374 |               79 |
| Location 5 |                              1672 |               93 |

Table 2: Statistical analysis for the TTC samples

|          | Inverse Gaussian   | Inverse Gaussian   | Lognormal      | Lognormal   | Triangular       | Triangular   | Exponential   | Exponential   | Uniform       | Uniform   |
|----------|--------------------|--------------------|----------------|-------------|------------------|--------------|---------------|---------------|---------------|-----------|
|          | Distributions      | K-S                | Distributions  | K-S         | Distributions    | K-S          | Distributions | K-S           | Distributions | K-S       |
| Location | IG                 | 0.0968 *           | Lognorm        | 0.1198      | Triang           | 0.2385       | Expon         | 0.1814        | Uniform       | 0.3600    |
| 1        | (9.26, 12.21)      |                    | (9.27, 8.28)   |             | (0, 2.30, 31.50) |              | (9.26)        |               | (0, 29.82)    |           |
| Location | IG                 | 0.1003 *           | Lognorm        | 0.1138      | Triang           | 0.2471       | Expon         | 0.1764        | Uniform       | 0.3746    |
| 2        | (9.69, 12.88)      |                    | (9.71, 8.62)   |             | (0, 2.41, 32.80) |              | (9.69)        |               | (0, 31.39)    |           |
| Location | IG                 | 0.1017 *           | Lognorm        | 0.1024      | Triang           | 0.1756       | Expon         | 0.2091        | Uniform       | 0.3807    |
| 3        | (11.20, 14.06)     |                    | (11.53, 9.56)  |             | (0, 2.10, 37.40) |              | (11.20)       |               | (0, 36.84)    |           |
| Location | IG                 | 0.0813 *           | Lognorm        | 0.1097      | Triang           | 0.1768       | Expon         | 0.1408        | Uniform       | 0.3449    |
| 4        | (12.30, 11.01)     |                    | (12.96, 13.86) |             | (0, 1.41, 40.60) |              | (12.30)       |               | (0, 39.55)    |           |
| Location | IG                 | 0.0651 *           | Lognorm        | 0.0781      | Triang           | 0.3199       | Expon         | 0.1934        | Uniform       | 0.4948    |
| 5        | (7.26, 9.24)       |                    | (7.24, 6.45)   |             | (0, 1.65, 29.88) |              | (7.26)        |               | (0, 29.57)    |           |

According to Tables 1 and 2, we can find that

- (1) The  Inverse  Gaussian  distribution  is  the  best-fitted  distribution  for  all  the  five locations 3 .  Figures  3(a)  and  3(b)  depicts  the  histograms  and  empirical  cumulative distribution function (CDF) for data samples with the best-fitted distributions (traffic volume = 963 vehs/hour∙lane).
- (2) Lognormal distribution also performs very well for the five locations (relatively small K-S values). In reality, other samples may suggest that Lognormal distributions are better. The two distributions have similar patterns. Let us take the Location 1 as an example: ( ) ( ) 9.26,12.21 3 0.138 P IG ≤ = and ( ) ( ) Lognorm 9.27,8.28 3 0.139 P ≤ = 4 . Indeed,  the  differences  between  the  two  distributions  are  very  marginal.  In  the following  analysis,  without  loss  of  generality,  we  will  assume  the  samples  follow Inverse Gaussian distributions as suggested in Table 3.

3 Inverse Gaussian Distribution is a two parameter family of continuous probability distributions with support on (0, ∞ ). Its probability density function is given by

<!-- formula-not-decoded -->

where µ &gt;0 is the mean and λ &gt;0 is the shape parameter. The distribution can be viewed as the distribution of first passage time of a Wiener process with an absorbing barrier, i.e., while the Gaussian describes a Brownian Motion's level at a fixed time  (Wiener  process), the inverse  Gaussian  describes  the  distribution of  the  time  the  Brownian Motion  takes  to  reach  a fixed positive level.

4 In this example, the TTC threshold is assumed to be as 3 second. Similar results are obtainable if we assume the threshold is 2 second or 4 second.

Figure 3: The histograms and empirical CDF (traffic volume = 963 vehs/hour∙lane).

<!-- image -->

Line chart

- (3) The TTC data collected at different locations with respect to similar traffic volume generally  follows  the  same  Inverse  Gaussian  distribution  (e.g.  Location  1  and Location 2). In other words, the traffic volume  could  be  considered as the contributing factor for TTC distributions.
- (4) The  TTC  sample  mean  and  its  inverse  both  have  a  parabola  relationship  with  the traffic volume, as shown in Figures 4 and 5. This is because two contributing factors to  TTC,  distance  headway  and  speed  dispersion,  are  both  dependent  of  the  traffic volume.  When  traffic  volume  is  low  (&lt;1000  vehs/hour∙lane),  the  great  speed dispersion  could  result  in  low  TTC  values.  However,  when  traffic  volume  is  high (&gt;1600 vehs/hour∙lane), the small distance headway would lead to low TTC values.

- (5) The  shape  parameters  ( λ )  of  the  best  fitted  Inverse  Gaussian  distributions  with respect to different traffic volumes are within a relatively small range from 9.24 to 14.06.

Figure 4: TTC sample mean - traffic volume relationship

<!-- image -->

Line chart

Figure 5: Inverse of TTC mean - traffic volume relationship

<!-- image -->

Line chart

## 3.2 Estimation of the parameters defining Inverse Gaussian distribution

As  discussed in Section 3.1, both Inverse Gaussian distribution  and  Lognormal distribution fit the data very well. In the following analysis, without loss of generality, we use an Inverse Gaussian regression model to establish the relationship between TTC and traffic volume.  To  formulate  the  inverse  Gaussian  regression  model,  let , 1, , , i y i n =  be n independent  observations  (TTC  samples)  distributed  as ( ) , i IG µ λ ,  in  which  the  inverse  of sample mean has a parabola relationship with traffic volume, namely:

<!-- formula-not-decoded -->

where i x is traffic volume of TTC sample i . Whitmore (1983) derived the pseudo maximum likelihood estimations of β and λ as

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

where Y is  the diagonal matrix with i -th diagonal elements being yi , 1 is the n-vector of all ones  and ( ) 2 1, , T i i X x x = .  They  are  called  the  pseudo  maximum  likelihood  estimations because  the  condition 2 0 1 2 ˆˆˆ 0 i i x x β +β +β &gt; for  all i is  not  guaranteed  to  be  satisfied 5 . According  to  the  collected  421  TTC  data  with  different  traffic  volumes,  the  estimated coefficients are

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

After obtaining the estimated coefficients, the TTC distributions could be determined for different traffic conditions reflected by their traffic volumes. In order to evaluate how well the  Inverse  Gaussian  regression  model  estimates  the  TTC  distributions,  we  compare  the derived  TTC  distributions  with  the  TTC  samples  at  different  traffic  volumes  -  894 vehs/hour∙lane,  963  vehs/hour∙lane,  1,127  vehs/hour∙lane,  1,374  vehs/hour∙lane,  and  1,672 vehs/hour∙lane)  -  by  using  the  hypothesis  test.  The  K-S  test  is  applied  to  conduct  the hypothesis test. The null hypothesis is rejected at level α if

<!-- formula-not-decoded -->

where n is  the  number  of  samples, Dn is  the  K-S  statistic,  and K α is  the  critical  value ( α =0.05 in this study). The results of K-S tests are reported in Table 3.

Table 3: K-S tests

|   Traffic volume (vehs/hour∙lane) |   Number of samples ( n ) | Distributions    |   K-S values ( D n ) |   Critical value ( 0.05 K ) | Test results   |
|-----------------------------------|---------------------------|------------------|----------------------|-----------------------------|----------------|
|                               894 |                       104 | IG(9.02, 12.17)  |               0.0977 |                        1.36 | 1.00<1.36      |
|                               963 |                        65 | IG(10.26, 12.17) |               0.1086 |                        1.36 | 0.88<1.36      |
|                             1,127 |                        80 | IG(12.33, 12.17) |               0.1496 |                        1.36 | 1.34<1.36      |
|                             1,374 |                        79 | IG(12.83, 12.17) |               0.0821 |                        1.36 | 0.73<1.36      |
|                             1,672 |                        93 | IG(7.30, 12.17)  |               0.1026 |                        1.36 | 0.99<1.36      |

Table 3 shows that the regression model performs well. Figures 6(a) and 6(b) depict the CDF  of  the  best  fitted  Inverse  Gaussian  distribution  and  the  CDF  generated  by  Inverse Gaussian regression for a TTC sample (traffic volume = 1,672 vehs/hour∙lane), respectively. As can be seen in the figures,  the  samples  could  be  well  represented  by  either  of  the  two Inverse Gaussian distributions with different parameters.

5 The condition is guaranteed in this study since the traffic volume is with the range from 800 to 1700 vehs/hour∙lane.

Figure 6: Empirical CDF with Inverse Gaussian distributions (traffic volume = 1,672 vehs/hour∙lane)

<!-- image -->

Line chart

## 4. Accident frequency estimation

## 4.1 TTC threshold value and exposure to traffic conflicts

As  mentioned  in  the  introductory  section,  a  TTC  threshold  value  is  usually  chosen  to distinguish relatively safe situation and dangerous scenarios exposed to traffic conflicts (or critical  encounters).  Various  opinions  can  be  found  from  the  literature  as  to  which  value should  be  used  as  the  threshold  value.  Hirst  and  Graham  (1997)  reported  that  a  time-tocollision  measure  of  4  seconds  could  be  used  to  discriminate  between  cases  where  drivers unintentionally find themselves in a dangerous situation from cases where drivers remain in control. Hogema and Janssen (1996) presented a minimum TTC value of 3.5 seconds for nonsupported drivers and 2.6 seconds for supported drivers. It is widely acknowledged that the TTC threshold should be 2 seconds to 4 seconds (Minderhoud and Bovy, 2001; Vogel, 2003).

We define the exposure to traffic conflicts as the mean sojourn time in a given time period (e.g. an hour) that vehicles are exposed to dangerous scenarios (or critical encounters), i.e. the TTCs are lower than a predetermined threshold value τ . Having had the TTC distributions for road tunnel sections (Section 3), the exposure to traffic conflicts in an hour can be quantified by.

<!-- formula-not-decoded -->

where K denote  the  traffic  density; L is  the  length  of  a  road  tunnel  section;  ( 1) K L × - indicates  number  of  gaps  in  the  section; ( ) ( ) 0.5 P TTC x ≤τ × represents  the  probability  of TTC less than the threshold value τ 6 ; x is  the traffic volume of the time period in the road tunnel section. Note that only half of car following scenarios will result in finite TTCs and the other half is considered as absolutely safe situations (infinite TTCs).

## 4.2 Historical Crash-Damage database

Historical Crash-Damage  (HCD)  database of Singapore is used to examine the relationship  between exposure  to  traffic  conflicts and  crash  frequencies.  According  to  the Motor  Claims  Framework  (MCF)  introduced  by  the  General  Insurance  Association  of Singapore (GIA), in the event of a crash in expressways, everyone involved must inform the insurance company within one day using the GIA Motor Accident Report form. In addition, according to Road Traffic Act in Singapore, another report must be made within 24 hours of a crash if an injury has occurred. The HCD database (2006-2008) has all the reported crash records,  by  means  of  either  ways,  occurred  at  Singapore  expressways  from  2006  to  2008, which includes the time of crash, location of crash, crash type (e.g. rear-end, skidded, etc.), vehicle type (e.g. car-car, car-truck, etc.), number of slight injuries, number of serious injuries, and number of fatalities 7 . To sum up, there are 746 rear-end crashes in the CTE road tunnel from 2006 to 2008, causing 0 fatalities, 45 severe injuries, and 458 slight injuries.

6 The infinite TTC samples are considered as absolutely safe situations. The coefficient 0.5 is adequate only in stable traffic conditions;  the  coefficient  would  be  a  little  greater  than  0.5  for  unstable  traffic  flows.  For  simplicity,  the  coefficient  is assumed to be 0.5 in this study.

## 4.3 Relationship between exposure to traffic conflict and crash frequency

2 seconds, 3 seconds, and 4 seconds are considered as the TTC threshold values. From the HCD database we get the crash frequencies in a one-km road tunnel section in CTE road tunnel are 11, 5, 8, 20, 17, and 4 for he time period 7:00 am to 8:00 am, 1:00 pm to 2:00 pm, 5:00 pm to 6:00 pm, 8:00 pm to 9:00 pm, 9:00 am to 10:00 am, and 11:00 pm to 12:00 am from 2006 to 2008,  respectively.  In  the  one-km  tunnel  section,  there  is  a  2.4  meters  wide shoulder and three 3.6 meters traffic lanes in each carriageway with a tunnel structural height of  approximately  6  meters  high.  Both  the  curvature  and  gradient  are  very  gentle  in  this section.

We assume that the traffic volumes in the road tunnel section in a specific time period would  not  have  significant  daily  variations.  In  accordance  with  the  LTA  policy,  only  the latest  two  years  traffic  volume  data  are  obtainable.  Therefore,  the  traffic  volumes  and densities from 2006 to 2008 are not obtainable for this study. The average traffic volumes are estimated  by  LTA  tunnel  operators  on  the  basis  of  the  2010-2011  traffic  volume  and  the summary traffic data in 2006-2008. Accordingly, due to the data unavailability, we just use accurate R-E crash data and estimated average traffic volume to illustrate the methodology in the case study. The estimated traffic volumes, densities, lengths, and number of R-E crashes are summarized in Table 4.

Table 4: Traffic volumes, density, length, and crash records for different time periods

| Time period   | R-E Crash   | Estimated        | Density        | Average   |
|---------------|-------------|------------------|----------------|-----------|
|               | records     | Traffic volume   | (vehs/km∙lane) | Speed     |
|               | (2006-2008) | (vehs/hour∙lane) |                | (km/hour) |

| 7:00am - 8:00am   |   11 |   1600 |   25 |   62 |
|-------------------|------|--------|------|------|
| 1:00pm - 2:00pm   |    5 |   1200 |   16 |   73 |
| 5:00pm - 6:00pm   |    8 |   1400 |   20 |   70 |
| 8:00pm - 9:00pm   |   20 |   1700 |   45 |   39 |
| 9:00pm - 10:00pm  |   17 |   1600 |   50 |   34 |
| 11:00pm - 12:00am |    4 |    900 |   11 |   78 |

According to eqn. (9), the exposure to traffic  conflicts could  be  calculated.  We  further analyze  the  relationship  between exposure  to  traffic  conflicts and  the  crash  frequency  by using the linear regression methods, which is illustrated in Figure 7. The cumulative residual (CURE) method is a well recognized method to examine the goodness of fit of models in transportation  studies  (AASHTO,  2010;  Hauer,  2004;  Hauer  and  Banfo,  1997).  Figure  8 depicts the cumulative residuals for the linear regression models. As can be seen from Figure 8, the linear regression models perform well.

Figure 7: R-E crash count - traffic conflicts relationship with linear fit

<!-- image -->

Line chart

Figure 8: Plot of cumulative residuals against the proposed safety indicator

<!-- image -->

Line chart

The  statistical results for the linear regression models  are reported in Table 5. Surprisingly,  the P -values  of  the  coefficients  with  respect  to  constant  for  the  three  linear regression models are all greater than 0.035. By contrast, the P -values of coefficients with respect to R-E crash frequency are all close to 0. That is to say, the coefficients with respect to intercept are very significant. We further conduct another linear regression model with 0 intercept,  which  is  shown  in  Figure  9.  This  indicates  that  the  crash  rate  may  have  a proportional linear relationship with the proposed exposure to traffic conflicts . The corresponding proportional coefficient is defined as causation factor ( ( ) P t ), which could be considered  as  the  conditional  probability  that  vehicle  crashes  could  not  be  avoided  under dangerous encounters for one hour.

Table 5: statistical results of linear regression models

|    | Constant    | Constant   | Crash frequency   | Crash frequency   |        |
|----|-------------|------------|-------------------|-------------------|--------|
|    | Coefficient | P-value    | Coefficient       | P-value           | R-Sq   |
| 2s | 2.5929      | 0.035      | 0.0111            | 0.000             | 0.9738 |
| 3s | 2.4085      | 0.044      | 0.0037            | 0.000             | 0.9744 |
| 4s | 2.2446      | 0.058      | 0.0022            | 0.000             | 0.9736 |

Figure 9: R-E crash count - traffic conflicts relationship with linear fit (0 intercept)

<!-- image -->

Line chart

## 4.4 Remarks on the crash count - traffic flow relationship

As for the crash count - traffic flow relationship, a series of studies were carried out by several scholars on the basis of the actual data. Chang and Jovanis (1986) proposed a method to  model the relationship between miles travelled and crash count in a time-space domain.

Hauer et al. (1988) developed a model to estimate the safety of a signalized intersection on the  basis  of  the  traffic  flow  and  crash  count.  Miaou  and  Lum  (1993)  compared  four regression models - two conventional linear regression models and two Poisson regression models  -  in  terms  of  their  ability  to  model  the  relationship  among  traffic  flow,  geometry design, and crash count in highways. All the above mentioned studies acknowledged that it was  not  appropriate  to  apply  the  conventional  linear  regression  to  model  crash  count  and traffic  flow.  Figure  10  depicts  the  crash  count  -  traffic  volume  relationship  for  the  present study.  As  can  be  seen  in  the  figure,  neither  of  the  linear  regression  ( R 2 =  0.7323 )  and proportional  regressions  ( R 2 =  0.5339 )  performs  well.  Since  traffic  volume  equals  to  the product of density and speed (Lieu et al., 1999) the densities and speeds for two road sections with the same traffic volume may not be the same (e.g. the two points circled in Figure 9). In reality, the crash frequency is also closed related to the speed and density of a road section (Aarts and van Schagen, 2006). Hence, it is not appropriate to assume the linear relationship between crash count and traffic volume.

Figure 10: Crash count - traffic volume relationship

<!-- image -->

Line chart

Comparatively,  as  can  be  seen  from  Figures  7  and  9,  both  linear  regression  and proportional regression perform well in this study. This is because not only traffic volume but also  density  is  taken  into  account  in  the  proposed  exposure  to  traffic  conflicts.  The  results shows  that,  in  Singapore's  road  tunnels,  the  exposure  to  traffic  conflicts  based  method outperforms the traffic volume based approach.

## 5. Discussions

The  proposed  causation  factor ( ) P t reflects  the  conditional  probability  that  vehicle crashes have occurred when the vehicle are exposed to dangerous scenarios for one hour. The probability  would  be  dependent  on  vehicle  conditions,  drivers'  abilities,  and  the  road geometries. We conjecture that this factor could be a constant for a given road tunnel section in the long run with a given TTC threshold value. The TTC values would generally have a parabola  relationship  with  traffic  volume  because  they  will  be  affected  by  not  only  speed dispersion  but  also  distance  headways.  For  non-interrupt  traffic  flows  with  traffic  volume from  900  vehs/hour∙lane  to  1,700  vehs/hour∙lane,  the  TTC  distributions  may  follow  the Inverse Gaussian distributions (lognormal distributions are also a good approximation) and traffic volume could be considered as the contributing factor to the distribution parameters. It should  be  pointed  out  that  these  perspectives  need  to  be  validated  using  more  actual  data from other expressways and/or urban road tunnels.

The  crash data from  Singapore's  road tunnels shows  that linear or proportional relationship may not be good enough to reflect the relations between crash count and traffic volume. Instead, the linear and proportional relationships perform very well between crash count and exposure to traffic conflicts. This may be because not only traffic volume but also density is taken into consideration in the proposed exposure to traffic conflicts.

Other  than  the  TTC,  the  deceleration  rate  to  avoid  the  crash  (DRAC)  and  the  post encroachment time (PET) have also been considered as good safety indicators to measure the safety level in roads (Meng and Weng, 2011; Cunto and Saccomanno, 2008). Further study may  be  conducted  to  establish  the  relationship  between  crash  frequency  and  the  abovementioned  two  safety  indicators.  The  comparative  analysis  of  these  three  safety  indicators could also be studied accordingly. In addition, the model can also be applied to identify the hotspots  in  the  urban  road  tunnels  and/or  expressways  (Cheng  and  Washington,  2005; Montella, 2010).

## 6. Conclusions

In this study, a novel approach is proposed to estimate the R-E crash frequency in road tunnels. We first conclude that Inverse Gaussian distribution is the best-fitted distribution to the  TTC  data  based  on  the  best-fit  analysis.  Accordingly,  an  Inverse  Gaussian  regression model is applied to establish the relationship between the TTC and the corresponding traffic volume. A new concept of exposure to traffic conflicts is defined as the mean sojourn time in a given time period that vehicles are exposed to dangerous scenarios, i.e. the TTCs are lower than  a  predetermined  threshold  value.  Then,  a  R-E  crash  frequency  estimation  model  is proposed on the basis of the accident records provided by the HCD database for Singapore's road tunnels. We find that the crash frequency has a proportional linear relationship with the proposed exposure to traffic conflicts . Finally, several conjectures and recommendations are proposed.

## Acknowledgments

This study is supported by the innovation fund of Land Transport Authority of Singapore. We  are  really  grateful  to  the  two  anonymous  referees  and  the  editors  whose  comments improved the presentation and the content of the earlier version. Special thanks will also be expressed  to  Ms  Soh  Ling  Tim  from  Land  Transport  Authority  of  Singapore  on  the  data collection for this project.

## References

- Aarts,  L.,  I.,  van  Schagen,  2006.  Driving  speed  and  the  risk  of  road  crashes:  A  review. Accident Analysis and Prevention 38, 215-224.
- AASHTO, 2010. Highway Safety Manual, First Edition.
- Beard, A., Carvel, C., 2005. The handbook of tunnel fire safety. Thomas Telford Publishing. 1 st Jan 2005. London.
- Cheng,  W.,  and  Washington,  S.,  2005.  Experimental  evaluation  of  hotspot  identification methods. Accident Analysis and Prevention. 37: 870-881.
- Cunto, F., and Saccomanno F.F., 2008. Calibration and validation of simulated vehicle safety performance  at  signalized  intersections. Accident  Analysis  and  Prevention .  40,  11711179.
- Daniels, S., Brijs, T., Nuyts, E., Wets, G., 2010. Explaining variation in safety performance of roundabouts. Accident Analysis and Prevention . 42, 393-402.
- Farah, H., Bekhor, S., Polus, A., 2009. Risk evaluation by modeling of passing behavior on two-lane rural highways. Accident Analysis and Prevention . 41, 887-894.
- Guo,  F.,  Wang,  X.,  Abdel-Aty,  M.,  2010.  Modeling  signalized  intersection  safety  with corridor spatial correlations. Accident Analysis and Prevention . 42: 84-92.
- Haque,  M.M.,  Chin,  H.C.,  Huang,  H.,  2010.  Applying  Bayesian  hierarchical  models  to examine motorcycle crashes at signalized intersections. Accident Analysis and Prevention , 42, 203-212.

- Hauer E.,  2004.  Statistical  Road  Safety  Modeling. Transportation  Research  Record ,  1897, 81-87.
- Hauer  E.,  Banfo  J.,  1997.  Two  Tools  for  Finding  What  Function  Links  the  Dependent Variable to Explanatory Variables. Proceedings ICTCT 97 (International Cooperation on Theories and Concepts in Traffic Safety), Lund, Sweden, 1-7.
- Hauer  E.,  Ng  J.C.N.,  Lovell  J.,  1988.  Estimation  of  safety  at  signalized  intersections. Transportation Research Record , 1185, 48-61.
- Hauer,  E.,  2001.  Overdispersion  in  modelling  accidents  on  road  sections  and  in  Empirical Bayes estimation. Accident Analysis and Prevention , 33(6), 799-808.
- Hayward,  J.C.,  1972.  Near  miss  determination  through  use  of  a  scale  of  danger  (traffic records 384). Highway Research Board. Washington, DC.
- Hirst, S., Graham, R., 1997. The format and presentation of collision warnings. In: Noy, N.I. (Ed.), Ergonomics and safety of intelligent driver interfaces.
- Hogema, J.H., Janssen, W.H., 1996. Effects of intelligent cruise control on driving behavior. TNO Human Factors, Soesterberg, The Netherlands, Report TM-1996-C-12.
- Ibeas,  Á.,  Cordera,  R.,  dell'Olio,  L.,  Moura,  J.L.,  2011.  Modelling  demand  in  restricted parking zones. Transportation Research Part A , 45, 485-498.
- Jovanis P.P.,  Chang H.  L.,  1986.  Modeling the  relationship  of  accidents  to  miles  traveled. Transportation Research Record, 1068, 42-51.
- Land Transport Authority (LTA), 2005. Design Safety Submission for KPE [internal report], Singapore.
- Lieu,  H.,  N.,  Gartner,  C.J.,  Messer,  and  A.K.,  Rathi,  1999.  Traffic  flow  theory.  U.S. Department of Transportation. Federal Highway Administration.
- Lord,  D.,  Geedipally,  S.R.,  Guikema,  S.,  2010.  Extension  of  the  application  of  ConwayMaxwell-Poisson models: analyzing traffic crash data exhibiting under  dispersion. Risk Analysis . 30, 1268-1276.
- Lord, D., Guikema, S., Geedipally, S.R., 2008. Application of the Conway-Maxwell-Poisson generalized  linear  model  for  analyzing  motor  vehicle  crashes. Accident  Analysis  and Prevention 40, 1123-1134.
- Lord, D., Mannering, F., 2010. The statistical analysis of crash-frequency data: A review and assessment of methodological alternatives. Transportation research Part A, 44, 291-305.
- Lord, D., Washington, S.P., Ivan JN, 2007. Further notes on the application of zero inflated models in highway safety. Accident Analysis and Prevention . 39, 53-57.

- Malyshkina,  N.,  Mannering,  F.,  2010a.  Empirical  assessment  of  the  impact  of  highway deisgn exceptions on the frequency and severity of vehicle accidents. Accident Analysis and Prevention . 42, 131-139.
- Malyshkina, N., Mannering, F., 2010b. Zero-state Markov switching count-data models: an empirical assessment. Accident Analysis and Prevention . 25, 77-84.
- Maycock,  G.,  Hall,  R.D.,  1984.  Accidents  at  4-Arm  roundabouts.  TRRL  laboratory  report 1120, Transportation and Road Research Laboratory, Crowthorne, UK.
- Meng, Q.,  and  Weng,  J.,  2011  Evaluation  of  rear-end  crash  risk  at  work  zone  using  work zone traffic data. Accident Analysis and Prevention . 43, 1291-1300.
- Meng,  Q.,  Qu,  X.,  Wang,  X.,  Yuanita,  V.,  and  Wong,  S.C.,  2011a.  Quantitative  risk assessment modeling for non-homogeneous urban road tunnels. Risk Analysis ;  31,  382403.
- Meng, Q., Qu, X., Yong, K.T., Wong, Y.K., 2011b. QRA model based risk impact analysis of traffic flow in urban road tunnels. Risk Analysis . DOI: 10.1111/j.1539-6924.2011.01624.x
- Miaou  S.P.,  Lum  H.,  1993.  Modeling  vehicle  accidents  and  highway  geometric  design relationships. Accident Analysis and Prevention 25, 689-709.
- Miaou,  S.P.,  1994.  The  Relationship  between  Truck  Accidents  and  Geometric  Design  of Road  Sections:  Poisson  Versus  Negative  Binomial  Regressions. Accident  analysis  and Prevention . 26, 471-482.
- Minderhoud, M.M., and Bovy, P.H.L., 2001. Extended time-to-collision measures for road traffic safety assessment. Accident Analysis and Prevention . 33, 89-97.
- Montella, A,  2010. A comparative analysis of hotspot identification methods. Accident Analysis and Prevention. 42: 571-581.
- Páez, A., Trépanier, M., Morency, C., 2011. Geodemographic analysis and identification of potential  business  partnerships  enabled  by  transit  smart  cards. Transportation Research Part A , 45, 640-652
- PIARC Technical Committee C3.3 Road tunnel operation, 2008. Risk Analysis for Road Tunnels, May 2008. http://publications.piarc.org/ressources/publications\_files/4/2234,TM2008R02-WEB.pdf. Accessed 19 th May 2011.
- Qu,  X.,  Meng,  Q.,  Yuanita,  V.,  Wong,  Y.K.,  2011.  Design  and  implementation  of  a quantitative  risk  assessment  software  tool  for  Singapore's  road  tunnels. Expert Systems with Applications . 38(11): 13827-13834.

- Shankar, V., Milton, J., Mannering, F.L., 1997. Modeling accident frequency as zero-altered probability processes: an empirical inquiry. Accident Analysis and Prevention .  29,  829837.
- Svensson,  A.,  1998.  A  method  for  analyzing  the  traffic  process  in  a  safety  perspective. Doctoral Dissertation. University of Lund, Lund, Sweden.
- The European Parliament and the council of the European Union. Directive 2004/54/EC of the  European  parliament  and  of  the  council  of  29  April  2004  on  minimum  safety requirements  for  tunnels  in  the  Trans-European  Road  Network.  Official  Journal  of  the European Union. 2004 Apr; L 167/ 39 - 91.
- Vogel,  K.,  2003.  A  comparison  of  headway  and  time  to  collision  as  safety  indicators. Accident Analysis and Prevention . 35, 427-433.
- Whitmore, G.A., 1983. A regression method for censored inverse Gaussian data. Canadian Journal of Statistics . 11, 305-315.
- Zhang, Y., Xie, Y., 2007. Forecasting of short-term freeway volume with v-support vector machines. Transportation Research Record. 2024, 92-99.
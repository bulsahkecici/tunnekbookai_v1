Research Article

## Assessment of rate of penetration of a tunnel boring machine in the longest railway tunnel of Turkey

<!-- image -->

Icon

Candan Gokceoglu 1

Received: 18 October 2021 / Accepted: 29 November 2021

© The Author(s) 2021

OPEN

## Abstract

One of the most important issues in tunnels to be constructed with tunnel boring machines (TBMs) is to predict the excavation time. Excavation time directly affects tunnel costs and feasibility. For this reason, studies on the prediction of TBM performance have always been interesting for tunnel engineers. Therefore, the purpose of the study is to develop models to predict the rate of penetration (ROP) of TBMs. In accordance with the purpose of the study, a new database including 5334 cases is obtained from the longest railway tunnel of Turkey. Each case includes uniaxial compressive strength, Cerchar Abrasivity Index, α angle, weathering degree and water conditions as input or independent variables. Two multiple regression models and two ANN models are developed in the study. The performances of the ANN models are considerably better than those of the multiple regression equations. Before deep tunnel construction in a metamorphic rock medium, the ANN models developed in the study are reliable and can be used. In contrast, the performances of the multiple regression equations are promising, but they predict lower ROP values than the measured ROP values. Consequently, the prediction models for ROP are open to development depending on the new data and new prediction algorithms.

Keywords TBM · Rate of penetration · Bahce-Nurdag tunnel · Metamorphic rock · ANN · Regression model

## 1  Introduction

Approximately four decades ago, Robbins [45] stated 'nothing has been more difficult than evaluating the rock mass characteristics and applying the evaluations to a formula predicting penetration rate'. Despite huge technological developments, the prediction of rock mass characteristics and the rate of penetration of TBMs is still a challenging problem for tunnel engineers. In addition, due to the lack of living space and the increase in population, there has been a construction boom in the underground space to improve the quality of human life [54]. In addition, the growth in the economy has led to enhanced engineering studies that not only result in a significant reduction in transportation time but also aid in developing comfortable transportation choices [37]. In recent decades, mechanized tunnelling techniques, particularly tunnel boring machines (TBMs), have been extensively applied to tunnel construction due to their high excavation rate and low total cost for the excavation of long tunnels [39]. In other words, TBM tunnelling has serious advantages for long tunnels if the geological and geotechnical characterizations of tunnel routes are described correctly and a suitable machine for ground conditions is selected.

A reliable and accurate prediction of the tunnel boring machine (TBM) performance can assist in minimizing the relevant risks of high capital costs and in scheduling tunnelling projects [68, 69]. With respect to TBM drilling

* Candan Gokceoglu, cgokce@hacettepe.edu.tr | 1 Department of Geological Engineering, Hacettepe University, 06800 Beytepe, Ankara, Turkey.

<!-- image -->

Icon

<!-- image -->

Other

<!-- image -->

Logo

<!-- image -->

Logo

Vol.:(0123456789)

in hard rocks, the most important aspect of its operation is the prediction of its rate of penetration (ROP) [49]. However, predicting the tunnel construction duration for long tunnels in complex geological and geotechnical conditions is not an easy task because of high uncertainty. Zhou et al. [68] applied six machine learning methods for the prediction of ROP and found that the comprehensive performance of the particle swarm optimizationextreme gradient boosting hybrid model-is superior to the other five models. Minh et al. [42] used uniaxial compressive strength (UCS), Brazilian tensile strength (BTS), rock brittleness index (BI), the distance between planes of weakness (DPW) and the alpha angle ( α ) between the tunnel axis and the planes of weakness for predicting ROP. Minh et al. [42] suggested that the fuzzy logic as well as other artificial intelligences can also be used as very good alternatives to predict ROP . Jung et al. [28] predicted the ground conditions ahead of the tunnel face regardless of site conditions considering the operational data of the shield TBM acquired during the tunnel excavation stage. Similarly, Zhang et al. [62] predicted the geological conditions using TBM operational data. Armetti et al. [6] assessed TBM performance data employing various intact rock and rock mass properties. Salimi et al. [48] proposed a brief review of the applications of common rock mass classification systems for the performance prediction of TBMs and the development of a new model that is based on the input parameters of the RMR system for the prediction of TBM performance. Farrokh [14] reviewed and compared the results of several mainstream TBM advance rate-estimating models for hard rock TBMs through the evaluation of their predictive abilities, and he used a database of performance parameters for 17 recent tunnel projects. Additionally, several researchers have used various prediction algorithms, such as artificial neural networks [35, 36, 43, 52, 55, 57, 66, 68, 69], fuzzy or neuro-fuzzy inference systems [1, 21], metaheuristic algorithms [70] and multiple regression [12, 15, 17, 20, 22-26, 33, 56, 57], to estimate TBM performance. Jing et al. [27] suggested a TBM advance rate prediction model considering operation factors. As seen from the brief literature summary, the prediction of TBM performance is one of the most important research subjects among tunnel engineers because this problem has not yet been completely solved. Due to the complexity of geological and geotechnical conditions along tunnel routes, the prediction of ROP is difficult. However, depending on the accumulation of well-documented data and advancements in prediction algorithms, more understandable and applicable estimation equations and models have started to be produced.

In Turkey, depending on the development of railway systems, several railway construction projects are ongoing. One of these projects is Bahce-Nurdag (south of Turkey)

twin-tube tunnels, and these tunnels are the longest railway tunnels of Turkey. Excavations started from Nurdag (Gaziantep) with TBM, and one of the tunnels was completed in Bahce (Osmaniye) in 2020. The length of each tube is approximately 10 km. The geological characteristics of the Bahce-Nurdag Railway Tunnels route are extremely complex because the route is located in the active East Anatolian Fault Zone. The most important issue for long tunnels excavated with TBMs in complex geological conditions is the prediction of construction time, and the most important parameter is the rate of penetration (ROP). Consequently, the purpose of the present study is to develop prediction equations and models using the data collected from one of the longest railway tunnels of Turkey (Bahce-Nurdag Railway Tunnel). The length of one tube of the tunnels is approximately 10 km, but the data were collected along 8 km because the other parts of the tunnel were excavated by the NATM method. During the excavation phase, weathering degree and water conditions were observed and measured directly; however, other parameters, such as the Cerchar Abrasivity Index, uniaxial compressive strength and alpha angle, were determined using the borehole and laboratory data. Regression analyses and artificial neural networks were used to analyse the data, and the results were presented and discussed.

## 2   Geological and geotechnical conditions of tunnel route

The Bahce-Nurdag tunnel route is located at the borders of Osmaniye and Gaziantep in southeastern Turkey (Fig. 1). After the completion of the Bahçe-Nurdag tunnels, the length of the railway between Bahçe and Nurdag will decrease from 32 to 15 km. The region has a dense population, and the total population of Gaziantep, Hatay, Osmaniye and Adana, which will directly benefit from this project, is approximately 6.5 million people. In addition, one of Turkey's most important industrial organizations is Iskenderun Iron and Steel Plant located in the region. Great economic benefits will be obtained as a result of transportation of the produced steels and other industrial products by rail. For this reason, Bahçe-Nurdag tunnels have a very high importance in terms of both the travel of local dwellings and the transportation of industrial products.

Fig. 1 Location map of the Bahce-Nurdag tunnels

<!-- image -->

Geographical map

Turkey is located in the Alp-Himalayan earthquake zone, and due to this tectonic feature of Turkey, tunnel construction works have several serious geological and geotechnical problems [7, 8]. The Bahçe-Nurdag tunnels are in the active East Anatolian Fault Zone (EAFZ) (Fig. 2). The EAFZ is one of the most seismically active zones of Turkey because it represents a plate boundary extending over 500 km between the Arabian and Anatolian plates [11]. However, the EAFZ has been relatively quiescent in the last century when compared to historical records and has therefore accumulated significant stresses along its length [44]. In particular, the segment near the project area has a high seismic risk, and the possible magnitude of future earthquakes is predicted to be approximately 7.3 by Nalbant et al. [44]. When considering this seismic risk, the most important factor for the project is duration. If a major earthquake occurs during the construction phase, the damage to the tunnel will be serious. The geological map of the tunnel route and its close vicinity is shown in Fig. 3. Along the tunnel route, various types of metamorphic units, such as metasandstone, quartzite, schist and slate, were encountered (Fig. 4). Some parts of the tunnel route include only units, while some parts are formed by metasandstone-slate or metasandstone-slate-quartzite alternance. The longitudinal cross section of the tunnel is shown in Fig. 4. As shown in Fig. 4, the tunnel has serious groundwater and 50 l/s water inflow was measured, but some parts are occasionally dry. The overburden thickness reaches up to 640 m.

Fig. 2 The  Bahçe-Nurdag  tunnel  location  on  the  seismotectonic map of  the  East  Anatolian  Fault  Zone  (the  map  was    taken  from [44])

<!-- image -->

Geographical map

During the geological and geotechnical investigation phase of the project, a total of 15 geotechnical boreholes were drilled by Fugro Sial Inc. [18]. The depths of these boreholes vary between 40 and 435 m. The average geotechnical data obtained from these boreholes and laboratory tests are summarized in Table 1.

## 3   TBM characteristics and data identification

The customized single-shield TBM (Fig. 5) with a diameter of 8 m was designed with Difficult Ground Solutions (DGS) by Robbins (Robbins Inc., 2020). The TBM has 10 motors, and each motor has 330 kW. These motors produce 14,453 kNm torque. The excavated material is removed from the tunnel with the conveyor belt system (Fig. 6). Along 8 km, 402.000 ­ m 3 metamorphic rock masses were excavated by the TBM (Fig. 5) and transported by the conveyor belt system (Fig. 6).

As mentioned previously, several prediction models have been developed, and various TBMs and intact rock and rock mass parameters have been used. It is obvious that the parameters used in the ROP prediction model should be determined easily and are reliable. One of the commonly used parameters is the α angle. α is expressed as the angle between the TBM axis and the planes; generally, the maximum TBM penetration rate occurs when this angle is approximately 60° [66]. Vergala and Saroglou [53] proposed a new field penetration index for mixed-face ground conditions (MFPI), and they found that increasing weighted rock mass rating, ­ RMR m , resulted in an increase in the mixed-face field penetrating index. However, Salimi et al. [47] mentioned that the boreability of rock decreases with the increase in UCS. Afradi et al. [3] used a comprehensive database including uniaxial compressive strength, Brazilian tensile strength, RQD, cohesion, elasticity modulus, Poisson's ratio, density, joint angle and joint spacing as input parameters for estimating penetration rate. Mahdevari et al. [41] employed uniaxial compressive strength, tensile strength, brittleness index, distance between the plane of weakness, alpha angle and machine parameters when developing the TBM performance model. The parametric study and sensitivity analysis of the common prediction models in relation to input variables indicate that uniaxial compressive strength is the most influential parameter across all models [16]. Similar results on uniaxial compressive strength were obtained by Torabi et al. [51].

Fig. 3 Geological map of the tunnel route and its close vicinity [37]

<!-- image -->

Geographical map

Prediction of the ROP before the excavation phase is important because the main purpose of these models is to estimate the TBM's completion time. For this reason, it  is  the  development of prediction models with the geological-geotechnical parameters affecting the TBM excavation. However, it is also important that the parameters to be used in the prediction model can be obtained from the geological cross section and the boreholes. After the tunnel is completed with TBM, many TBM parameters are obtained. However, it is not possible to know some of these parameters such as thrust, torque and energy consumption [59] before the excavation. Despite this view, some operational parameters such as torque are used for TBM performance estimation as well as geological-geotechnical parameters. Zhao et al. [67] proposed a TBM performance prediction method based on Mixed-face Torque Penetration Index and torque capacity. Consequently, it was preferred to use the parameters obtained before the excavation in the models developed in this study. In other words, after the geological cross section was prepared, the data representing each unit were used as the input parameter using drilling and laboratory data. Consequently, in the present study, α , uniaxial compressive strength (UCS), weathering degree (W), water conditions (WaterInflow) and Cerchar Abrasivity Index (CAI) are used to predict ROP. The statistical summaries of the inputs and the output are given in Table 2. The TBM excavated an 8000 m tunnel, and each parameter was determined at each 1.5 m advancement; hence, the database includes 5334 cases. The ROP values vary between 5.5 and 114.5 mm/min depending on the geological and geotechnical conditions of the tunnel route.

<!-- image -->

Logo

The ' α ' angle is utilized for quantifying the influence of  discontinuity geometry on tunnel boring machine performance, and the following equation is used for the calculation of ' α ' angle [10]:

Fig. 4 Longitudinal cross section of the Bahce-Nurdag Tunnel (section includes the TBM part) (modified after Fugro Sial Inc. [18])

<!-- image -->

Engineering drawing

Table 1 Some average geotechnical parameters of the lithological units (compiled from Fugro Sial Inc. [18])

| Lithological unit          |   RQD (%) |   Uniaxial compressive strength, UCS (MPa) |   Cerchar Abra- sivity Index, CAI |
|----------------------------|-----------|--------------------------------------------|-----------------------------------|
| Metasandstone              |      34.5 |                                       81.2 |                              2.13 |
| Slate                      |      46.2 |                                      122.6 |                              2.60 |
| Quartzite                  |      42.0 |                                      191.4 |                              3.83 |
| Schist                     |       7.0 |                                       10.7 |                              0.20 |
| Slate-metasandstone        |      46.9 |                                      101.9 |                              2.10 |
| Quartzite-schist           |      22.0 |                                      101.0 |                              2.02 |
| Slate-metasandstone-schist |      24.5 |                                       71.5 |                              1.46 |
| Metasandstone-schist       |      21.4 |                                       46.0 |                              1.17 |

Fig. 5 The TBM used in Bahce-Nurdag tunnel

<!-- image -->

Photograph

<!-- image -->

Photograph

Fig. 6 The conveyor belt system of the TBM

<!-- image -->

Logo

Table 2 Statistical summaries of the input and output parameters

|                 |    N |   Range |   Minimum |   Maximum |     Mean |   Std. Deviation |   Variance |
|-----------------|------|---------|-----------|-----------|----------|------------------|------------|
| ROP (mm/min)    | 5334 |  114.50 |      5.50 |    120.00 |  48.8155 |         15.67366 |    245.664 |
| α (degree)      | 5334 |   40.40 |     31.60 |     72.00 |  40.0931 |         12.62861 |    159.482 |
| WatInflow (l/s) | 5334 |   50.00 |      0.00 |     50.00 |   4.0165 |          8.23583 |     67.829 |
| W               | 5334 |    4.00 |      1.00 |      5.00 |   2.0396 |          1.11319 |      1.239 |
| CAI             | 5334 |    3.63 |      0.20 |      3.83 |   2.0457 |          0.76744 |      0.589 |
| UCS (MPa)       | 5334 |  180.70 |     10.70 |    191.40 | 101.7046 |         41.14378 |   1692.811 |

<!-- formula-not-decoded -->

where α f =  dip of discontinuity (degree), α s =  strike of discontinuity (degree), α t =  direction of tunnel (degree).

## 4   Multiple regression analyses

If the dependent variable is controlled for by two or more independent variables, multiple regression analysis is used. In geotechnical practice, multiple regression analyses have been widely used. For example, multiple regression analyses were used to estimate the UCS [19, 58, 60, 71], predict rock mass permeability [30, 32], predict the deformation modulus of rock masses [4, 31] and predict the TBM performance [22, 57]. In this study, a series of simple regression analyses are performed before multiple regression analyses to check the multicollinearity. The coefficients of correlation of the simple regression analyses are summarized in Table 3. The general formula of the correlation coefficient ( r ) is given as follows:

<!-- formula-not-decoded -->

where s x and s y are the sample standard deviations and s xy is the sample covariance.

As seen from Table 2, there is a strong correlation between the CAI and UCS. Similarly, several authors (i.e. [13, 29, 34, 65]) investigated the relation between CAI and UCS and they found meaningful correlations between these two parameters. Hence, it is impossible to use both UCS and CAI in the same model. Among the other parameters, there is either a very weak or no relationship. The relationships between ROP and the independent variables are almost linear. For this reason, linear multiple regression analyses and nonlinear multiple regression analyses were performed using IBM SPSS Statistics package.

Table 3 Coefficient of correlations ( R ) obtained from the simple regression analyses

<!-- image -->

Logo

During the multiple regression analyses, two models are run. The first includes WatInflow, W , α and UCS as independent variables, while the second includes WatInflow, W , α and CAI. For the first model, the coefficients of correlations of cross-correlations between the measured and predicted ROP values are obtained as 0.59 for both nonlinear and linear multiple regressions. For this reason, the linear regression equation (Eq. 1) is preferred, and the cross-correlation graph is shown in Fig. 7a. Additionally, the correlation equation of the second model is given in Eq. (2), and the cross-correlation graph of the second model is shown in Fig. 7b, and the coefficient of correlation for the second model is found to be 0.56.

```
(1) ROP = ( 0.011UCS ) + ( 0.164 a ) - ( 7.2 W ) + ( 0.56WatInflow ) + 53.5 (2) ROP = ( 0.093CAI ) + ( 0.166 a ) - ( 7.3 W ) + ( 0.57WatInflow ) + 54.5
```

where ROP = rate of penetration (mm/min), UCS = uniaxial compressive strength (MPa), α =  alpha angle (degree), WatInflow = water inflow (l/ s ), CAI = Cerchar Abrasivity Index.

The equations obtained from the multiple regression analyses are statistically meaningful; however, the equations for extreme values yield lower values. The model including UCS is slightly better than that including CAI. In general, the equations provide a good prediction of the average values. In addition, both equations are similar because there is a strong relationship between the CAI and UCS.

| Parameters   | ROP    |   WatInflow |    α |    W |   CAI |   UCS |
|--------------|--------|-------------|------|------|-------|-------|
| ROP          | 1      |             |      |      |       |       |
| WatInflow    | 0.22   |           1 |      |      |       |       |
| α            | 0.22   |        0.50 |    1 |      |       |       |
| W            | - 0.43 |        0.29 | 0.21 |    1 |       |       |
| CAI          | 0.13   |        0.09 | 0.00 | 0.32 |     1 |       |
| UCS          | 0.21   |        0.00 | 0.08 | 0.37 |  0.97 |     1 |

Fig. 7 Cross-correlation graphs between predicted and measured ROPs; a model 1 and b model 2

<!-- image -->

Line chart

## 5   Artificial neural networks

Accurately predicting the performance of a tunnel boring machine (TBM) is important for safe and efficient tunnelling, and hence, the application of machine learning algorithms to TBM performance prediction creates several challenges [63]. Similarly, Armaghani et al. [5] applied several optimization techniques for estimating the TBM advance rate in granitic rocks. In addition to traditional methods, some intelligent methods, such as artificial neural networks (ANNs), have been applied to various problems in the tunnel domain in recent years [54]. In the present study, two ANN models are developed using a large database collected over 5 years from 8000 m tunnel excavation. The success of an ANN model depends on the size of the database. In this study, a database including 5334 cases was used during the ANN modelling performed using MATLAB R2020a software. A total of 3734 cases were used in the training stage, 800 cases were used in testing, and 800 cases were used in validation. During the training stage, the Levenberg-Marquardt learning algorithm is employed. Yu and Wilamowski [61] stated that 'the Levenberg-Marquardt algorithm [38, 40] provides a numerical solution to the problem of minimizing a nonlinear function. It is fast and has stable convergence. In the artificial neural networks field, this algorithm is suitable for training small- and medium-sized problems' . The steepest descent method and the Gauss-Newton algorithm are blended by the Levenberg-Marquardt algorithm [61]. The general structures of the ANN models constructed in the study are shown in Fig. 8.

Model 1 completes the learning stage at 142 iterations, while model 2 reaches the minimum SME value at 217 iterations. The cross-correlation between the measured and predicted ROP values for model 1 is shown in Fig. 9. According to the cross-correlation results, the coefficients of correlation of training, testing, validation and all cases for model 1 are 0.84, 0.84, 0.83 and 0.84, respectively. These results show that the model including UCS, water conditions, weathering degree and α angle as input shows a strong prediction capacity. In addition, the coefficients of correlations of the training, testing and validation data are almost the same, which shows that the generalization capacity of the model developed in this study is successful.

Fig. 8 General  structure  of  the  ANN  models  constructed  in  the study

<!-- image -->

Flow chart

The cross-correlation between the measured and predicted ROP values for model 2 is shown in Fig. 10. According to the cross-correlation results, the coefficients of correlation of training, testing, validation and all cases for model 2 are 0.85, 0.83, 0.84 and 0.84, respectively. When compared to model 1, the performance of model 2 is slightly higher than that of model 1; however, both models yield meaningful and promising results.

<!-- image -->

Logo

Fig. 9 Cross-correlations between the predicted (output) and the measured (target) ROP values for model 1

## 6   Results and discussion

One of the essential tasks in the excavation of tunnels with TBMs is the reliable estimation of the performance needed for planning, cost control and other decisionmaking regarding the feasibility of tunnelling projects [2]. However, according to results of the extensive review on the literature performed by Samaei et al. [49], there is no comprehensive agreement on the quantitative or qualitative influence of various variables on the TBM performance assessment, but the degree of accuracy in its prediction has been improved in recent years through using various algorithms such as ANN, support vector machine, fuzzy and neuro-fuzzy. For this reason, reliable prediction models for ROP have been attractive subjects for tunnel engineers. A recent study performed by Bardhan et al. [9] on prediction penetration rate discussed the existing models for prediction of penetration rate. The inputs of the models developed by Bardhan et al. [9] are uniaxial compressive strength, rock quality designation and distance between planes of weakness. In the present study, extensive observations were performed for 5 years to collect the data, and a database containing a large number of cases and based on detailed observations was formed. By using this database, simple and multiple regression analyses and ANN modelling to predict the ROP were performed. It is important to select input parameters that are easy to determine and reliable. In addition, parameters characterizing the geological and geotechnical conditions of the tunnel route and directly affecting the TBM are taken into consideration. In the first stage of the analyses, simple regression analyses are performed. According to the simple regression analysis results, no strong correlation between ROP and the independent parameters was obtained. Additionally, no meaningful correlation among the independent parameters considered in the study was found. However, only a strong correlation between UCS and CAI was obtained. For this reason, UCS and CAI are not used in the same multiple regression and ANN models to eliminate multicollinearity. As a result of this assessment, two different multiple regression analyses are performed. Both nonlinear and linear multiple regression analyses are performed. The coefficients of the correlations are almost the same; hence, linear multiple regression analyses are selected for practical use. The coefficients of correlation of the multiple regression analyses are almost the same but not strong. However, considering the number of cases, multiple regression equations can be used for ROP predictions. In the present study, ANN models were developed to predict ROP. The same parameters as the multiple regression equations are used, and two ANN models are constructed. Both ANN models constructed in the study produced outperforming results. Similarly, Bardhan et al. [9] stated that 'TBM's ROP estimation using theoretical and empirical models gives relatively low accuracy, and hence new methods need to be developed'. In addition, the soft computing algorithms give more successful results than the regression models [2, 9, 35, 50, 57, 65]. Finally, the models developed in the present study can be used to estimate ROP for metamorphic rocks and deep tunnels using easily obtained geological and geotechnical parameters before the excavation phase. Another important result is that UCS

<!-- image -->

Scatter plot

Fig. 10 Cross-correlations between the predicted (output) and the measured (target) ROP values for model 2

<!-- image -->

Scatter plot

and CAI have similar effects on TBM advancement in metamorphic rock media.

## 7   Conclusions

When geological uncertainties are added to this complex system, predicting the performance of a TBM in a long tunnel sometimes becomes extremely difficult. Considering these uncertainties, a database containing a high number of cases is constructed in the study. The data employed in the study are new because one tube of the Bahce-Nurdag tunnels was completed successfully in 2020. Along the tunnel route, various types of metamorphic rocks were encountered, and all assessments performed in the study are valid for metamorphic rocks. In addition, the tunnel is deep, and the overburden reaches 640 m. Consequently, the conclusions obtained from the study can be drawn as follows:

<!-- image -->

Logo

- (a) The reliability of a prediction model depends on the quality and quantity of the data. The database used in the study is formed by careful measurements and observations during tunnel excavation. In this study, 5334 cases were used to construct the prediction models.
- (b) The input or independent parameters should be obtained easily. This is another important issue for an ROP prediction model. For this reason, in the study, UCS, CAI, α angle,  weathering degree and water conditions are selected as inputs or independent variables. These variables directly affect TBM performance because each of the variables has a physical relation with TBM advancement. However, no meaningful relation between ROP and independent variables such as UCS, CAI, α angle, weathering degree and water conditions was found. However, a weak relationship between ROP and weathering degree is obtained, but it is insufficient to use ROP prediction. This result revealed that TBM advancement cannot be explained by a single variable. For this reason, multiple regression and ANN models with multiple inputs are developed.
- (c) The construction of tunnels with linear engineering structures is an extremely complex process. Therefore, it is possible to use highly sophisticated algorithms and a large number of input parameters to estimate the ROP. However, such models are difficult to use in practice. For this reason, attention has been devoted to developing models that are as easy as possible and to using easily obtainable input parameters so that the models developed in this study can be used in other tunnels. However, the models developed in this study have more generalization capacity than the more complex models.
- (d) The developed multiple regression equations have a moderate prediction capacity. However, considering the number of cases and the characteristics of the independent variables, they can be used for preliminary investigation stages. In contrast, both ANN models reveal a high prediction capacity. Before deep tunnel construction in a metamorphic rock medium, the ANN models constructed herein are reliable and can be used.

Consequently, ROP prediction is an important topic, and it is open to development depending on new and reliable data. Depending on the developments in prediction algorithms, more reliable and high-performance models will be developed in the near future. Therefore, studies on TBM performance prediction will continue to increase.

<!-- image -->

Logo

Acknowledgements The author of this article has been the geological-geotechnical consultant of the project since 2014. The author thanks TCDD (General Directorate of Turkish State Railways) and Intekar-Biskon Partnership.

## Declarations

Conflict of interest The author declares that he has no conflict of interest with anyone or any institution.

Open Access This article is licensed under a Creative Commons Attribution 4.0 International License, which permits use, sharing, adaptation, distribution and reproduction in any medium or format, as long as you give appropriate credit to the original author(s) and the source, provide a link to the Creative Commons licence, and indicate if changes were made. The images or other third party material in this article are included in the article's Creative Commons licence, unless indicated otherwise in a credit line to the material. If material is not included in the article's Creative Commons licence and your intended use is not permitted by statutory regulation or exceeds the permitted use, you will need to obtain permission directly from the copyright holder. To view a copy of this licence, visit http:// creat iveco mmons. org/ licen ses/ by/4. 0/.

## References

1. Adoko AC, Yagiz S (2019) Fuzzy inference system-based for TBM field penetration index estimation in rock mass. Geotech Geol Eng 37:1533-1553. https:// doi. org/ 10. 1007/ s10706- 018- 0706-5
2. Adoko AC, Gokceoglu C, Yagiz S (2017) Bayesian prediction of TBM penetration rate in rock mass. Eng Geol 226:245-256. https:// doi. org/ 10. 1016/j. enggeo. 2017. 06. 014
3. Afradi A, Ebrahimabadi A, Hallajian T (2020) Prediction of tunnel boring machine penetration rate using ant colony optimization, bee colony optimization and the particle swarm optimization, case study: Sabzkooh water conveyance tunnel. Min Miner Depos 14(2):75-84. https:// doi. org/ 10. 33271/ minin g14. 02. 075
4. Alemdag S, Gurocak Z, Cevik A, Cabalar AF, Gokceoglu C (2016) Modeling deformation modulus of a stratified sedimentary rock mass using neural network, fuzzy inference and genetic programming. Eng Geol 203:70-82. https:// doi. org/ 10. 1016/j. enggeo. 2015. 12. 002
5. Armaghani DJ, Koopialipoor M, Marto A, Yagiz S (2019) Application of several optimization techniques for estimating TBM advance rate in granitic rocks. J Rock Mech Geotech Eng 11:779789. https:// doi. org/ 10. 1016/j. jrmge. 2019. 01. 002
6. Armetti G, Migliazza MR, Ferrari F, Bertid A, Padovese P (2018) Geological and mechanical rock mass conditions for TBM performance prediction. The case of 'La Maddalena' exploratory tunnel, Chiomonte (Italy). Tunn Undergr Space Technol 77:115-126. https:// doi. org/ 10. 1016/j. tust. 2018. 02. 012
7. Aygar EB (2020) Evaluation of new Austrian tunnelling method applied to Bolu tunnel's weak rocks. J Rock Mech Geotech Eng 12(3):541-556. https:// doi. org/ 10. 1016/j. jrmge. 2019. 12. 011
8. Aygar EB, Gokceoglu C (2020) Problems encountered during a railway tunnel excavation in squeezing and swelling materials and possible engineering measures: a case study from Turkey. Sustainability 12(3):1166. https:// doi. org/ 10. 3390/ su120 31166
9. Bardhan A, Kardani N, GuhaRay A, Burman A, Samui P, Zhang Y (2021) Hybrid ensemble soft computing approach for predicting penetration rate of tunnel boring machine in a rock

- environment. J Rock Mech Geotech Eng. https:// doi. org/ 10. 1016/j. jrmge. 2021. 06. 015
10. Bruland A (1998) Hard rock tunnel boring. Ph.D. thesis, Norwegian University of Science and Technology, Trondheim, Norway
11. Bulut F, Bohnhoff M, Eken T, Janssen C, Kilic T, Dresen G (2012) The East Anatolian Fault Zone: seismotectonic setting and spatiotemporal characteristics of seismicity based on precise earthquake locations. J Geophys Res 117:B07304. https:// doi. org/ 10. 1029/ 2011J B0089 66
12. Delisio A, Zhao J, Einstein H (2013) Analysis and prediction of TBM performance in blocky rock conditions at the Lotschberg Base Tunnel. Tunn Undergr Space Technol 33:131-142
13. Er S, Tugrul A (2016) Estimation of Cerchar Abrasivity Index of granitic rocks in Turkey by geological properties using regression analysis. Bull Eng Geol Environ 75:1325-1339. https:// doi. org/ 10. 1007/ s10064- 016- 0853-y
14. Farrokh E (2020) A study of various models used in the estimation of advance rates for hard rock TBMs. Tunn Undergr Space Technol 97:103219. https:// doi. org/ 10. 1016/j. tust. 2019. 103219
15. Farrokh E, Rostami J, Laughton C (2012) Study of various models for estimation of penetration rate of hard rock TBMs. Tunn Undergr Space Technol 30:110-123
16. Fatemi SA, Ahmadi M, Rostami J (2018) Evaluation of TBM performance prediction models and sensitivity analysis of input parameters. Bull Eng Geol Environ 77:501-513. https:// doi. org/ 10. 1007/ s10064- 016- 0967-2
17. Fattahi H, Moradi A (2017) Risk assessment and estimation of TBM penetration rate using RES-based model. Geotech Geol Eng 35:365-376. https:// doi. org/ 10. 1007/ s10706- 016- 0111-x
18. Fugro Sial Inc. (2014) Nahce-Nurdag Transition Tunnel, Geological and Geotechnical Project Report. Volume 1, P2013.0015, 91p (in Turkish)
19. Gokceoglu C, Zorlu K (2004) A fuzzy model to predict the uniaxial compressive strength and modulus of elasticity of a problematic rock. Eng Appl Artif Intell 17:61-72. https:// doi. org/ 10. 1016/j. engap pai. 2003. 11. 006
20. Gong Q, Zhao J (2009) Development of a rock mass characteristics model for TBM penetration rate prediction. Int J Rock Mech Min Sci 46(1):8-18
21. Grima MA, Bruines PA, Verhoef PNW (2000) Modeling tunnel boring machine performance by neuro-fuzzy methods. Tunn Undergr Space Technol 15(3):259-269
22. Hassanpour J, Rostami J, Khamehchiyan M, Bruland A (2009) Developing new equations for TBM performance prediction in carbonate-argillaceous rocks: a case history of Nowsood water conveyance tunnel. Geomech Geoeng 4(4):287-297
23. Hassanpour J, Rostami J, Khamehchiyan M, Bruland A, Tavakoli H (2010) TBM performance analysis in pyroclastic rocks: a case history of Karaj water conveyance tunnel. Rock Mech Rock Eng 43(4):427-445
24. Hassanpour J, Rostami J, Zhao J (2011) A new hard rock TBM performance prediction model for project planning. Tunn Undergr Space Technol 26(5):595-603
25. Innaurato N, Mancini A, Rondena E, Zaninetti A (1991) Predictioning and effective TBM performances in a rapid excavation of a tunnel in Italy. In: 7th ISRM congress, pp 1127-1132
26. Jamshidi A (2018) Prediction of TBM penetration rate from brittleness indexes using multiple regression analysis. Model Earth  Syst  Environ  4:383-394.  https:// doi. org/ 10. 1007/ s40808- 018- 0432-2
27. Jing L-J, Li J-B, Zhang N, Chen S, Yang C, Cao H-B (2021) A TBM advance rate prediction method considering the effects of operating factors. Tunn Undergr Space Technol 107:103620. https:// doi. org/ 10. 1016/j. tust. 2020. 103620
28. Jung J-H, Chung H, Kwon Y-S, Lee I-M (2019) An ANN to predict ground condition ahead of tunnel face using TBM operational data. KSCE J Civ Eng 23(7):3200-3206. https:// doi. org/ 10. 1007/ s12205- 019- 1460-9
29. Kahraman S, Alber Ö, Fener M, Gunaydin O (2010) The usability of Cerchar Abrasivity Index for the prediction of UCS and E of Misis Fault Breccia: Regression and artificial neural networks analysis. Expert Syst Appl 37:8750-8756
30. Kayabasi A, Gokceoglu C (2019) An assessment on permeability and Grout Take of Limestone: a case study at Mut Dam, Karaman. Turkey Water 11:2649. https:// doi. org/ 10. 3390/ w1112 2649
31. Kayabasi A, Gokceoglu C, Ercanoglu M (2003) Estimating the deformation modulus of rock masses: a comparative study. Int J Rock Mech Min Sci 40(1):55-63. https:// doi. org/ 10. 1016/ S13651609(02) 00112-0
32. Kayabasi A, Yesiloglu-Gultekin N, Gokceoglu C (2015) Use of non-linear prediction tools to assess rock mass permeability using various discontinuity parameters. Eng Geol 185:1-9. https:// doi. org/ 10. 1016/j. enggeo. 2014. 12. 007
33. Khademi Hamidi J, Shahriar K, Rezai B, Rostami J (2010) Performance prediction of hard rock TBM using Rock Mass Rating (RMR) system. Tunn Undergr Space Technol 25(4):333-345
34. Ko TY, Kim TK, Son Y, Jeon S (2016) Effect of geomechanical properties on Cerchar Abrasivity Index (CAI) and its application to TBM tunnelling. Tunn Undergr Space Technol 57:99-111
35. Koopialipoor  M, Tootoonchi  H,  Armaghani  DH,  Mohamad ET, Hedayat A (2019) Application of deep neural networks in predicting the penetration rate of tunnel boring machines. Bull  Eng  Geol  Env  78:6347-6360.  https:// doi. org/ 10. 1007/ s10064- 019- 01538-7
36. Koopialipoor M, Fahimifar A, Ghaleini EN, Momenzadeh M, Armaghani DJ (2020) Development of a new hybrid ANN for solving a geotechnical problem related to tunnel boring machine performance. Eng Comput 36:345-357. https:// doi. org/ 10. 1007/ s00366- 019- 00701-8
37. Komu MP, Guney U, Kilickaya TE, Gokceoglu C (2020) Using 3D numerical analysis for the assessment of tunnel-landslide relationship: Bahce-Nurdag tunnel (South of Turkey). Geotech Geol Eng 2020(38):1237-1254. https:// doi. org/ 10. 1007/ s10706- 019- 01084-9
38. Levenberg K (1944) A method for the solution of certain problems in least squares. Q Appl Math 5:164-168
39. Liu B, Wang R, Guan Z, Li J, Xu Z, Guo X, Wang Y (2019) Improved support vector regression models for predicting rock mass parameters using tunnel boring machine driving data. Tunn Undergr Space Technol 91:102958. https:// doi. org/ 10. 1016/j. tust. 2019. 04. 014
40. Marquardt D (1963) An algorithm for least-squares estimation of nonlinear parameters. SIAM J Appl Math 11(2):431-441
41. Mahdevari S, Shahriar K, Yagiz S, Shirazi MA (2014) A support vector regression model for predicting tunnel boring machine penetration rates. Int J Rock Mech Min Sci 72:214-229
42. Minh VT, Katushin D, Antonov M, Veinthal R (2017) Regression models and fuzzy logic prediction of TBM Penetration Rate. Open Eng 7:60-68
43. Nagrecha K, Fisher L, Mooney M, Rodriguez-Nikl T, Mazari M, Pourhomayoun M (2020) As-encountered prediction of tunnel boring machine performance parameters using recurrent. Neural Netw. https:// doi. org/ 10. 1177/ 03611 98120 934796
44. Nalbant SS, McCloskey J, Steacy S, Barka AA (2002) Stress accumulation and increased seismic risk in eastern Turkey. Earth Planet Sci Lett 195:291-298. https:// doi. org/ 10. 1016/ S0012821X(01) 00592-1

<!-- image -->

Logo

45. Robbins R (1980) Present trends and future directions in tunnelling. In: The Yugoslav symposium on rock mechanics and underground actions, p 11
46. Robbins Inc. (2020) https:// www. thero bbins compa ny. com/ proje cts/ bahce- nurdag/. Accessed on 31 Oct 2020
47. Salimi A, Rostami J, Moormann C, Delisio A (2016) Application of non-linear regression analysis and artificial intelligence algorithms for performance prediction of hard rock TBMs. Tunn Undergr Space Technol 58:236-246
48. Salimi A, Rostami J, Moormann C (2019) Application of rock mass classification systems for performance estimation of rock TBMs using regression tree and artificial intelligence algorithms. Tunn Undergr Space Technol 92:103046. https:// doi. org/ 10. 1016/j. tust. 2019. 103046
49. Samaei M, Ranjbarnia M, Nourani V, Naghadehi MZ (2020) Performance prediction of tunnel boring machine through developing high accuracy equations: a case study in adverse geological condition. Measurement 152:107244. https:// doi. org/ 10. 1016/j. measu rement. 2019. 107244
50. Shahrour I, Zhang W (2021) Use of soft computing techniques for tunnelling optimization of tunnel boring machines. Undergr Space 6(3):233-239
51. Torabi SR, Shirazi H, Hajali H, Monjezi M (2013) Study of the influence  of  geotechnical  parameters  on  the TBM  performance in Tehran-Shomal highway project using ANN and SPSS. Arab J Geosci 6:1215-1227. https:// doi. org/ 10. 1007/ s12517- 011- 0415-3
52. Xu H, Zhou J, Asteris PG, Armaghani DJ, Tahir MM (2019) Supervised machine learning techniques to the prediction of tunnel boring machine penetration rate. Appl Sci 9:3715. https:// doi. org/ 10. 3390/ app91 83715
53. Vergara IM, Saroglou C (2017) Prediction of TBM performance in mixed-face ground conditions. Tunn Undergr Space Technol 69:116-124. https:// doi. org/ 10. 1016/j. tust. 2017. 06. 015
54. Wang X, Lu H, Wei X, Wei G, Bebehani SS, Iseley T (2020) Application of artificial neural network in tunnel engineering: a systematic review. IEEE Access 8:119527-119543. https:// doi. org/ 10. 1109/ ACCESS. 2020. 30049 95
55. Wei M, Wang Z, Wang X, Peng J, Song Y (2020) Prediction of TBM penetration rate based on Monte Carlo-BP neural network. Neural Comput Appl. https:// doi. org/ 10. 1007/ s00521- 020- 04993-6
56. Yagiz S (2008) Utilizing rock mass properties for predicting TBM performance in hard rock condition. Tunn Undergr Space Technol 23(3):326-339
57. Yagiz S, Gokceoglu C, Sezer E, Iplikci S (2009) Application of two nonlinear prediction tools to the estimation of tunnel boring machine performance. Eng Appl Artif Intell 22:808-814
58. Yagiz S, Sezer EA, Gokceoglu C (2012) Artificial neural networks and nonlinear regression techniques to assess the influence of slake durability cycles on the prediction of uniaxial compressive strength and modulus of elasticity for carbonate rocks. Int J Numer Anal Meth Geomech 36(14):1636-1650. https:// doi. org/ 10. 1002/ nag. 1066
59. Yan T, Shen S-L, Zhou A, Lyu H-M (2021) Construction efficiency of shield tunnelling through soft deposit in Tianjin, China. Tunn Undergr Space Technol 112:103917
60. Yesiloglu-Gultekin N, Gokceoglu C, Sezer EA (2013) Prediction of uniaxial compressive strength of granitic rocks by various nonlinear tools and comparison of their performances. Int J Rock Mech Min Sci 62:113-122. https:// doi. org/ 10. 1016/j. ijrmms. 2013. 05. 005
61. Yu H, Wilamowski BM (2011) Levenberg-Marquardt training. In: Intelligent systems, vol 12, pp 1-16. CRC Press
62. Zhang Q, Liu Z, Tan J (2019) Prediction of geological conditions for a tunnel boring machine using big operational data. Autom Constr 100:73-83. https:// doi. org/ 10. 1016/j. autcon. 2018. 12. 022
63. Zhang Q, Hu W, Liu Z, Tan J (2020) TBM performance prediction with Bayesian optimization and automated machine learning. Tunn Undergr Space Technol 103:103493. https:// doi. org/ 10. 1016/j. tust. 2020. 103493
64. Zhang Y, Wei M, Su G, Li Y, Zeng J, Deng X (2020) A novel intelligent method for predicting the penetration rate of the tunnel boring machine in rocks. Math Probl Eng 2020:3268694
65. Zhang S-R, She L, Wang C, Wang Y-J, Cao R-L, Li Y-L, Cao K-L (2021)  Investigation  on  the  relationship  among  the  Cerchar abrasivity index, drilling parameters and physical and mechanical properties of the rock. Tunn Undergr Space Technol 112:103907
66. Zhao ZY, Gong QM, Zhang Y, Zhao J (2007) Prediction model of tunnel boring machine performance by ensemble neural networks. Geomech Geoeng 2(2):123-128
67. Zhao Y, Gong Q, Tian Z, Zhou S, Jiang H (2019) Torque fluctuation analysis and penetration prediction of EPB TBM in rocksoil  interface  mixed  ground. Tunn  Undergr Space Technol 91:103002. https:// doi. org/ 10. 1016/j. tust. 2019. 103002
68. Zhou J, Qiu Y, Armaghani DJ, Zhang W, Lie C, Zhu C, Tarinejad R (2020) Predicting TBM penetration rate in hard rock condition: a comparative study among six XGB-based metaheuristic techniques. Geosci Front. https:// doi. org/ 10. 1016/j. gsf. 2020. 09. 020
69. Zhou J, Bejarbaneh BY, Armaghani DJ, Tahir MM (2020) Predictioning of TBM advance rate in hard rock condition based on artificial neural network and genetic programming techniques. Bull  Eng  Geol  Env  79:2069-2084.  https:// doi. org/ 10. 1007/ s10064- 019- 01626-8
70. Zhou J, Qiu Y, Zhu S, Armaghani DJ, Li C, Nguyen H, Yagiz S (2021) Optimization of support vector machine through the use of metaheuristic algorithms in predictioning TBM advance rate. Eng Appl Artif Intell 97:104015. https:// doi. org/ 10. 1016/j. engap pai. 2020. 104015
71. Zorlu K, Gokceoglu C, Ocakoglu F, Nefeslioglu HA, Acikalin S (2008) Prediction of uniaxial compressive strength of sandstones using petrography-based models. Eng Geol 96:141-158. https:// doi. org/ 10. 1016/j. enggeo. 2007. 10. 009

<!-- image -->

Logo

Publisher's  Note Springer  Nature  remains  neutral  with  regard  to jurisdictional claims in published maps and institutional affiliations.
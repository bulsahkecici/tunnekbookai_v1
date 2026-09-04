---
document_id: "DOC000013"
title: "Estimation_of_Annual_Routine_Maintenance_Cost_for_"
source_file: "Estimation_of_Annual_Routine_Maintenance_Cost_for_.pdf"
source_relative_path: "Leyla Literatür/TunelMaliyet/Estimation_of_Annual_Routine_Maintenance_Cost_for_.pdf"
source_extension: ".pdf"
sha256: "e9bce09c7035ac5c141dea236fcfd694e507faf2ccba90f6e0e21f29b3ecaa4f"
language: null
document_type: "unknown"
organization: null
year: null
authority_level: null
topics: ["maintenance"]
duplicate_group: null
preferred_variant: true
conversion_engine: "docling_full_layout_ocr_colab"
---

<!-- Docling chunk 1/1 -->
<!-- original_page_start: 1 -->
<!-- original_page_end: 14 -->
<!-- citation_rule: original_page = original_page_start + chunk_local_page - 1 -->

## Research Article

## Estimation of Annual Routine Maintenance Cost for Highway Tunnels

## Xuelian Wu , 1 Xiaoli Shi , 1 Yuhuan Li, 2 and Xiaotian Gong 1

1

Xi'an Municipal Engineering Design&amp;Research Institute Co Ltd, Xi'an, Shaanxi, China

School of Highway, Chang'an University, Xi'an, Shaanxi, China 2

Correspondence should be addressed to Xiaoli Shi; glxl@gl.chd.edu.cn

Received 9 September 2022; Revised 25 October 2022; Accepted 28 October 2022; Published 15 November 2022

Academic Editor: Jian Zhang

Copyright © 2022 Xuelian Wu et al. Tis is an open access article distributed under the Creative Commons Attribution License, which permits unrestricted use, distribution, and reproduction in any medium, provided the original work is properly cited.

In highway management, the prediction of the routine maintenance cost of tunnels is an important issue in saving tunnel maintenance costs due to its uncertainty, and the infuencing factors should be carefully selected because too many variables could not be involved in the model. Te complicated relationship between variables may lead to the inconsistency of model coefcients with the actual situation even though the goodness of ft of the model constructed with more variables is higher. Tis paper presents an approach in which quantitative analysis is combined with qualitative analysis to quickly select the independent variables of the tunnel routine maintenance cost (TMC) model. Based on the routine maintenance data collection of nine highway tunnels in Shaanxi province from 2007 to 2016, the independent variables of the models are determined with one-way ANOVA, Pearson correlation, partial correlation, and hierarchical regression. Afterwards, a fxed-efect regression model which can refect the overall regional features is developed. Results show that tunnel age (Age) and tunnel length proportion (PET) have less efect on TMC among the main infuencing factors such as district, Age, annual average daily trafc volume (AADT), truck trafc volume proportion (PTT), PET, and number of ventilation facilities (NVF), while the NVF makes a positive contribution to the TMC. Compared with grouped regression models, the fxed-efect regression model has higher ftting accuracy and a better regression coefcient signifcance. Te quick independent variable selection method can shorten the time of establishing the model and determine the infuencing factors of the research object efectively. Te established model is suitable for forecasting the TMC and budget arrangement. In addition, the elastic analysis results of regression coefcients are helpful to the decision of maintenance strategy and the allocation of maintenance funds.

## 1. Introduction

1.1. Background. Maintenance cost planning is an important aspect of highway infrastructure asset management. Maintenance cost prediction is an important module of the asset management system and the basis for maintenance decisionmaking. Compared with preventive maintenance, rehabilitation, and major maintenance, routine maintenance is characterized by periodicity, repetitiveness, and timeliness [1] which afected the frequency and demand of pavement overhaul. Good pavement condition could lead to the reduced cost of road users as well [2, 3]. Each asset must be treated specially in management as the structural characteristics of each asset are quite diferent with various highway infrastructure assets such as subgrade, pavement, bridge, culvert, tunnel, and trafc safety facilities. Terefore, the management systems of tunnels, bridges, and pavements have been developed separately. Compared with roads and bridges, underground tunnels are more prone to deterioration than aboveground structures due to the aggressive environment of water and soil [4]. Te environment in tunnels is more complicated than other assets in the aspect of the infuence of lighting facilities, fre-fghting facilities, and ventilation facilities installed in tunnels. Terefore, the above mentioned facilities cannot be ignored even if the contents of routine maintenance do not include the maintenance of these facilities. If the lighting conditions are adequate, the routine maintenance efciency will be better and the consumption of labor, materials, and mechanical fuel can be reduced. Ventilation facilities help to keep the tunnel environment clean, which can indirectly afect the TMC. In addition, the length of the tunnel is also a critical factor. Generally speaking, the longer the tunnels are, the greater the installed power (lighting, ventilation, fre-fghting facilities, and control systems) is [4]. Te damage or leakage of tunnel walls has a great infuence on the safety of human life. In this case, the tunnel must be blocked and accessed restrictedly. Consequently, the TMC is unique and important. Special analysis and TMC models are needed.

TMC is a vital part of the tunnel life-cycle cost model which is also the basis of tunnel assets evaluation and longterm maintenance fund forecast. Te TMC can also be applied as a key index to evaluate the maintenance efectiveness of maintenance agencies. Te economic feasibility of infrastructure design and maintenance under variable policies can be assessed by incorporating TMC model results into life-cycle costs [5-7]. With the accumulation of data and update of the cost model, it is more conducive to the decision-making and bidding management for management institutions.

1.2. Literature Review. Several types of highway infrastructure maintenance expenditure prediction are included in the statistical models but relatively few for tunnels. Numerous studies focus on the routine maintenance costs of pavement. Regression analysis is commonly used to establish maintenance cost models. Generally, routine maintenance cost or the routine maintenance volume is set as the dependent variable of the regression model. Te independent variables can be classifed into three categories: (1) pavement performance index [8, 9]; (2) variables that are related to the environment of road, such as natural environment, trafc environment, and road age [1, 10, 11]; and (3) considering both environment and pavement conditions [12, 13], maintenance cost intervals that are proposed in several studies, but without infuencing factors analyzed. For instance, researchers calculated the average routine maintenance cost of a road unit length varied from $285 to $7830 per lane according to the US Highway Economic Demand Analysis System. Ola [14] obtained the criteria of the annual maintenance cost of road, which stated that the cost of a paved two-lane rural main road was from $870/km to $1730/ km, $1682/km to $6743/km for a paved four-lane main road, and from $703/km to $1407/km for two-lane main road without paving.

Research on bridge asset maintenance cost includes the opportunity of bridge preventive maintenance based on cost-beneft analysis [15], the maintenance cost model based on life-cycle cost [16-20], and the maintenance cost model developed in bridge maintenance management systems [16, 21-23]. Te infuencing factors of the maintenance cost of bridges are similar to those of the bridge condition [20, 24-26]. Literature [27] analyzed the infuence of bridge superstructure form, completion time, load grade, bridge length, and other factors on routine maintenance cost of bridges. Other studies [28] considered the infuence of environment, bridge age, maintenance measures, and other factors when evaluating the condition of bridges. Te infuence of environmental factors and trafc factors on bridges was considered in other studies [29-31]. In the research [21], factors such as bridge deck type (steel bridge or concrete bridge), year, road type (interstate highway or other), average daily trafc volume (ADT), width, length, and bridge condition were considered. Te model [6] was established, taking climate factors (including annual average temperature and annual average rainfall), average daily truck trafc (ADTT), bridge condition, total bridge deck area of each state, and the average bridge deck area of each state into account.

Te research of tunnel asset cost involves three key aspects, including TMC prediction [2, 3, 32], the maintenance costs model based on life-cycle cost [33-37], and the maintenance cost model developed in the tunnel maintenance management system [5, 33, 38-40]. Compared to the methods suggested in the literature, many of the case study applications estimated the costs using cost estimation methods based on expert opinion rather than statistical methods [37, 41]. Moretti et al. presented a life-cycle cost analysis by comparing construction, maintenance, and lighting costs needed to manage a highway tunnel. Tey were mainly concerned about the maintenance costs of two diferent kinds of surface pavements which are concrete and asphalt pavement over a 30-year service life. Qing et al. proposed a quantitative approach for selecting efective maintenance strategies for metro tunnels in order to reduce maintenance cost [4]. Al-Chalabi used the parametric method to calculate the costs and estimate the ventilation system's economic lifetime in Stockholm's road tunnels. Cantisani et al. discussed the life-cycle assessment of different road pavements and lighting systems in an Italian road tunnel by examining 19 impact categories.

Many factors result in the degradation of tunnel, such as the carbonation of concrete, corrosion of steel members, creep and shrinkage, alkali-aggregate reaction, fuctuation of underground water, and rheology of soil [4, 42]. For the infuencing factors of the tunnel maintenance costs, Cui [2] studied the tunnel age, tunnel length, tunnel width, and natural trafc volume. Li [32] took the tunnel age, truck ratio, Σ ESAL, and the number of lanes as the infuencing factors.

In general, the research features of highway infrastructure maintenance cost are as follows (1) Highway maintenance cost analysis has regional characteristics, with special location taken as the research object. (2) Most studies focus on the cost of pavement maintenance because it constitutes the largest part of the road maintenance cost, and a few studies focus on the TMC. (3) Most studies on tunnel cost focus on the cost of tunnel structure, lighting, and ventilation system. Te routine maintenance costs have not been taken seriously, such as tunnel cleaning and repair painting. However, low-quality routine maintenance of the tunnel will accelerate the leakage and corrosion of tunnel steel members, leading to structural deterioration and greater property losses. (4) Te TMC is afected by many factors, such as construction quality, maintenance management level, service life, trafc volume, trafc composition, mechanical facilities, electrical facilities, tunnel structure, rainfall, and natural environment. Most of them are selected by qualitative analysis, after which the independent variables are determined.

Tis method may lead to a suitable cost prediction model, but the qualitative selection of infuencing factors does not guarantee sufcient explanatory power for the dependent variable. In addition, choosing the appropriate explanatory variables for a model is always a time-consuming task. Terefore, based on the review of the literature, a method combining quantitative analysis with qualitative analysis is proposed, which can quickly select independent variables in the regression models with strong explanatory ability. Besides, a regression model of TMC is established.

1.3. Objectives and Organization. In this paper, a method is proposed to quickly select the independent variables of the regression model by using widely available panel data and establish the regression models to estimate the annual tunnels expenses. Tis paper also attempts to compare the efcacy of grouped ridge regression and fxed-efect regression. Tese two promising modeling techniques are based on their intuition, explanatory ability, and predictive performance.

Te paper is organized as follows: First, it describes the data sources, then studies boundary conditions, and then discusses the procedures of data collection and adjustment (including adjustments of temporal variations of the expenditure data, data normalized, and outlier detection). Ten the way to choose the independent variables is described. One-way ANOVA, Pearson correlation, partial correlation, and part correlation are used to study the correlation among infuencing factors. A hierarchical regression model is established to study the explanatory ability of each block of variables to the dependent variable. Ten, the independent variables are determined according to the results of hierarchical regression and correlation analysis followed by a discussion on model development. In conclusion, the authors discuss and interpret the results, compare the performance of the grouped ridge regression and fxed-efect model, make an elastic analysis of coefcients [43], and put forward some suggestions for future research work in this feld.

## 2. Data

Te source of the routine maintenance of tunnels data used in this study was provided by Shaanxi Transportation Holding Group (STHG), over the fscal years (FY) 2007-2016 from all of Shaanxi's nine highway contracts. Te data gathered from STHG include the maintenance inventory and its corresponding factors such as costs, tunnel age, initial pile number, tunnel structure (single/double and double arch/nondouble arch), tunnel length, net height, net width, number of lanes, tunnel pavement structure (initial period and present stage), tunnel facilities (ventilation facilities, lighting facilities, and other facilities), tunnel condition index, precipitation, and snowfall. In detail, the routine maintenance inventory of tunnels include the cleaning of ceiling, wall, trafc facilities, drainage facilities, and portal structures; the maintenance of the facade marking, structures, and shading boards; the decoration in the tunnel; and the repaired painting of tunnel structure.

Trough the analysis of the infuencing factors of TMC and the characteristics of the collected routine maintenance data of tunnels, the infuencing factors were selected qualitatively as maintenance management level, climate environment (precipitation and snowfall), tunnel age, trafc factors, and tunnel parameters.

2.1. Setting Service Conditions. Te infuencing factors of maintenance management level and climate environment can be considered by setting service conditions. Te maintenance management level and construction level are afected by many factors, such as the level of the maintenance team and maintenance technique and equipment. Tese factors are often difcult to be quantitatively analyzed, which also have regional characteristics. Consequently, this paper assumes that the maintenance management level of the same manager in the same region is consistent.

According to the management system of STHG, a specifc branch is responsible for the operational management of each highway contract. Meanwhile, the maintenance budget is formulated for each highway. Taking a highway contract section as a specifc analysis object, the maintenance management level of each branch is infuenced by the maintenance policy of the central ofce, and each branch is under the unifed jurisdiction of the central ofce. In this way, there is no need to consider diferent tunnel maintenance management levels of diferent branches.

Shaanxi province is featured by a narrow and long terrain, 870 km from north to south, 200-500 km wide from east to west, including three climate zones. Shaanxi province is usually divided into three districts which are Shanbei (northern Shaanxi), Guanzhong (central Shaanxi), and Shannan (southern Shaanxi). Shanbei experiences a midtemperate climate, located in the Shanbei plateau; Guanzhong is in warm temperate region, located in Guanzhong plain; and Shannan has a north subtropical climate, located in the mountains. In terms of precipitation, the annual value in Shanbei is 400 mm ∼ 600 mm, 500 mm ∼ 700 mm for Guanzhong, and 700 mm ∼ 900 mm for Shannan. Te climate and temperature in the three districts are quite diferent. Te distribution of highway tunnels in the study region is shown in Figure 1.

During the operation of a highway, the tunnel assets are especially afected by climate and environmental factors. In this paper, the temperature diference, precipitation, and altitude are assumed equal in the same district. Tus, these factors can be distributed to district factor variables. In other words, tunnels located in the same climate region are treated as a group of analysis objects. Consequently, the study region was divided into three districts: Shanbei, Guanzhong, and Shannan.

Figure 1: Distributions of highway tunnels in Shaanxi.

<!-- image -->

2.2. Data Adjustment. For data collection, STHG allocated vehicles into mini busses, medium busses, minivans, medium trucks, large trucks, and trailers, and the annual average daily trafc with diferent highway contract sections was provided. Refer to the specifcation for the design of highway asphalt pavement [44], the axle load parameters of the above six vehicle types were determined, and the trafc factors afecting the TMC were also calculated. Te trafc factors included the design AADT, annual average daily truck trafc(AADTT), PTT ( AADTT /AADT × 100% AADTT /AADT × 100%), equivalent single axle load (ESAL), and cumulative equivalent single axle load ( 􏽐 ESAL). Collected tunnel parameters include the number of tunnels (NT) per highway contract, proportion of each length type of tunnel (PET) [45], NVF, and number of lighting facilities (NLF). Te standard equations for calculating the PET (PSLT, PLT, PMLT, and PST) are

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

where PSLT is the proportion of super long tunnels, PLT is the proportion of long tunnels, PMLT is the proportion of medium long tunnels, PSTis the proportion of short tunnels, PMLT is the proportion of medium long tunnels, NSLT is the number of super long tunnels, NLTis the number of long tunnels, NMLT is the number of medium long tunnels, and NST is the number of short tunnels.

After setting the service level, the maintenance management level, climate, and environment were no longer considered, which can be replaced by district variable. Te factors of tunnel age, trafc factor, and tunnel parameter calculated above were divided into time variables, trafc variables, and tunnel parameter variables. Table 1 provides a description of the dependent and independent variables.

2.2.1. Temporal Adjustment of Cost Data. Te dataset contained cost data for highway tunnels between 2007 and 2016, a rather wide temporal span that raised the specter of cost data bias due to infation. Terefore, all monetary amounts were converted to constant Chinese Yuan (CNY). Te variables defned as a monetary expenditure (capital outlay and maintenance) were adjusted for temporal variation using the price index (PI) provided by the Statistical Yearbook of Shaanxi Province [46]. Te standard equation for calculating adjusted monetary value at a given year is given by

<!-- formula-not-decoded -->

where TC 2016 is the equivalent cost in 2016; TCn is the cost in the reference year; and I i is the PI in any year, i .

2.2.2. Normalized Adjustment of Cost Data. Teannual total tunnel routine maintenance investment for each highway is taken as the dependent variable. Since the TMC is afected by the size of the tunnel [6, 47, 48], the standard equation for eliminating the impact of the asset scales on the TMC is given by

<!-- formula-not-decoded -->

where Cit is the TMC of road i for year t (CNY/lane/m); TCit is the TMC of road i for year t (RMB); n ik is the number of lanes of road i for lane k ; the number of tunnel lanes may be diferent in diferent sections of a road, k � 2,4,6; and L ik is the tunnel length of the road i for lane k (m).

Table 1: Dependent and independent variables.

| Variables             |                   | Units                                                                                            | Variable type                                                                                                             |
|-----------------------|-------------------|--------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------|
| Dependent variables   | District Time     | Cost/m/lane in 2016 FY RMB - year year day year day - - - A full set of ventilation facilities A | Continuous Categorical Continuous Continuous Continuous Continuous Continuous Continuous Continuous Continuous Continuous |
| Independent variables | Trafc             |                                                                                                  |                                                                                                                           |
|                       | Tunnel parameters | full set of lighting facilities                                                                  | Continuous                                                                                                                |

2.2.3. Outlier Detection. Tree times standard deviation method was adopted to eliminate outliers [49, 50]. Te Wujing Highway in Shanbei was taken as an example in 2008, 2009, 2010, 2011, 2012, 2013, 2014, and 2015, and TMC were 6.34, 3.16, 6.41, 27.39, 16.6, 23.61, 9.45, and 64.29, respectively. Te cost for 2015 is quite diferent from most data.

It is calculated by

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

where x 2015 should belong to ( -12.80, 39.36), while x2015 =64.29, x2015 is the outlier. Delete the data and take the average value of the others ( x � 13 . 28) to make up the gap.

## 3. Methodology

As previously discussed, the dataset contained 10 years of highway tunnel expenditure data, and the collected data varied across highways (and can thus be described as crosssectional) and varied for given highways over time (the data can also be described as time series). Tis yields a panel dataset by the repeated sampling of the same cross-sectional units over time and is a more powerful subset of pooled data models which were time series models that allowed the cross-sectional units to change over time. Te panel data used in the paper can be further described as unbalanced because some data were missing for certain years. Te cause of missing data was that data cannot be collected in some years due to diferent tunnel opening years. So the unbalanced data were not correlated with the disturbance term, which can be treated as the same as balanced panel data [51]. In the data, the individual number ( N ) was larger than the time ( t ), and the data described was short-panel data due to the minimum t being equal to 2, and the serial correlation between cross-sectional units was not considered. Te regression analysis in the paper was robust estimates and has taken into account the heteroscedasticity [52]. Figure 2 shows the modeling steps for the TMC.

3.1. Correlation Analysis. Regression analysis requires a strong correlation between dependent variables and independent variables, but no correlation is required between independent variables. An independent sample T -test is suitable for two categorical variables, and three or more category variables are tested by one-way ANOVA [53]. In this paper, the district was divided into Shanbei, Guanzhong, and Shannan; hence, the one-way ANOVA was adopted. Pearson correlation analysis is used for continuous variables to verify the correlation between variables [53]. Te standard equation is given by

<!-- formula-not-decoded -->

where ( x , y ) refers to the data objects and N is the total number of attributes.

Correlations between independent variables can lead to disturbances in the relationship between dependent and independent variables. Te partial correlation and part correlation analysis can be applied to exclude interference and verify the relationship between dependent and independent variables. Partial correlation analysis refers to the pure correlation between x 1 and x 2 after excluding the correlation between x 3 and x 1 , x 2 ; the standard equation for calculating the correlation coefcient r 12 , 3 is given by

<!-- formula-not-decoded -->

Part correlation analysis only deals with a certain variable, and its symbols are expressed in two forms. Te r 1 ( 2 , 3 ) represents the part correlation coefcient between x 1 and x 2 ; that is, the correlation after excluding the relationship between x 2 and x 3 . Te r 2 ( 1 , 3 ) represent part correlation coefcients of x 1 and x 2 after the exclusion of correlation of x 1 and x 3 . Te standard equation is given by

<!-- formula-not-decoded -->

3.2. Hierarchical Regression Analysis. It is too arbitrary to rely on the correlation analysis between the dependent variable and the independent variable to choose independent variables. Te relationship between independent variables and some dependent variables is not significant, but qualitative research analysis of this variable is a crucial factor. Infuencing factors have a theoretical hierarchical relationship, which can be divided into district variables, time variables, trafc variables, and tunnel parameter variables. It is necessary to deal with the interpretation of diferent independent variables to dependent variables in diferent blocks. Te biggest characteristic of hierarchical regression is to provide the variation of R 2 ( Δ R 2 ), the variation of F value ( Δ F ), and the variation of P value ( Δ P ). By judging Δ R 2 , Δ F , and Δ P , the increase of explanatory power of the added variables to the original model can be obtained.

Figure 2: Flow chart of the TMC model.

<!-- image -->

A log transformation can alleviate the infuence of heteroskedasticity, autocorrelation, and multicollinearity on the model, especially the infuence of standard deviation, parameter estimator variance, and covariance matrix. Furthermore, it can eliminate or reduce the skewness of the mathematical distribution of variables and narrow the range of values for the variables to bring the model closer to the classical linear model assumptions. Cit , Age, AADT, AADTT, ESAL, 􏽐 ESAL, NT, NVF, and NLF are absolute variables and were logarithmically transformed. PTT and PET (PSLT, PLT, PMLT, and PST) are relative variables that remain in the current state. In Table 1, these infuencing factors are divided into four groups. As the district is a classifed variable, Shanbei is taken as the reference variable, and Guanzhong and Shannan are included in the hierarchical regression. Te sum of the proportion of tunnel length is 1, and only three kinds of tunnel proportion need to be included. Te data showed that there was no extra long tunnel in many highway contracts, and the purpose of reducing multicollinearity cannot be achieved by eliminating the PSLT, so the PST is not included. Te grouping design is shown in Table 2.

Te standard linear form with a log transformation is presented as [43]

<!-- formula-not-decoded -->

where y is equal to ln Cit , x 1 is the district indicator (Guanzhong and Shannan), x 2 is the time indicator (lnAge and ln 􏽐 ESAL), x 3 is the trafc indicator (lnAADT, lnESAL, lnAADTT and PTT), ξ is the normally distributed disturbance term, β 0 is the constant term, and β j is the vector of estimated coefcients.

Te regression coefcient β j indicates the degree of interpretation of the independent variable x j for the dependent variable ln Cit [43]. Te regression coefcient is a nonstandardized statistical parameter with a unit. Although it can refect the extent of infuence of the independent variables on the independent variable, it cannot be used for comparison of variables.

To get the explanatory degree of each independent variable to the dependent variable more intuitively, all variables in (12) can be standardized by calculating their Z-scores. Te intercept term ' β 0 ' disappears, (12) changes to (13), and it can intuitively determine the degree of interpretation of each dependent variable on the dependent variable. B e ta j in (13) is calculated by (14):

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

where s xj is the standard deviation of independent variables x j , and s ln Cit is the standard deviation of dependent variables ln Cit .

Table 2: Te grouping design of hierarchical regression analysis.

| Block one: district indicators   | Block two: time indicators   | Block three: trafc indicators    | Block four: tunnel parameter indicators   |
|----------------------------------|------------------------------|----------------------------------|-------------------------------------------|
| Guanzhong, Shannan               | lnAge, ln 􏽐 ESAL             | lnAADT, lnESAL, lnAADTT, and PTT | lnNT, PSLT, PLT, PMLT, lnNVF, and lnNLF   |

## 3.3. Model Development

3.3.1. Grouped Ridge Regression. Testandard linear form is presented as (15) [43, 54]

<!-- formula-not-decoded -->

where yk is equal to ln Citk ( k � 1,2,3 represent Shanbei, Guanzhong, and Shannan, respectively), x j is the independent variable selected based on the results of correlation analysis and hierarchical regression analysis, β j is the vector of estimated coefcients, β 0 is the constant term, and ξ is the normally distributed disturbance term.

Ridge regression is suitable for the presence of multicollinearity. Its standard linear form is the same as the multivariable linear regression model, but the objective function is diferent. A penalty term is added to the objective function of the ridge regression model, and the standard equation is given by

<!-- formula-not-decoded -->

where the ridge trace map was adopted to determine the λ value [54].

3.3.2. Fixed-Efect Regression. Te panel data were composed of year t and highway contracts i because the length and NT have nothing to do with the year and are completely collinear with highway contract sections. Besides, TMC has obvious regional characteristics, and a fxed-efect regression model of the fxed district can be established. Te standard equation is given by [55, 56]

<!-- formula-not-decoded -->

where yit is equal to ln Cit ; α 0 is the constant term; u k is the district efect ( k � 1, 2, 3 represent Shanbei, Guanzhong and Shannan, respectively); β is the vector of estimated coefcients ( β 1 , β 2 , · · · , β m ) for the number of variables, m ; and x it ′ is the ( x 1 it , x 2 it , · · · , x mit ) ′ , m × 1 transpose vector.

## 4. Model Results and Discussion

## 4.1. Correlation Analysis

4.1.1. One-Way ANOVA. Tree categories of the district were considered. Te P value of the ANOVA F -test reached a statistical signifcance ( P &lt; 0 . 05) and rejected the null hypothesis. It indicatese that TMC is statistically signifcantly diferent in the three districts. Te detailed results of oneway analysis of variance (ANOVA) are presented in Figure 3.

In the fgure, ' a ' is included in the labels of Shaanxi and Guanzhong, indicating that there is no signifcant diference in the mean values in the two districts. ' b ' exists in both Shanbei and Shannan, indicating that there is no signifcant diference in the mean cost between these two districts. Te labels of Guanzhong and Shannan are ' a ' and ' b ,' respectively, which are completely diferent, indicating that the mean cost of Guanzhong and Shannan is signifcantly different at the confdence level of 0.1.

4.1.2. Pearson Correlation Analysis. Pearson correlation analysis was used for continuous variables to verify the correlation between variables [44].

Te results of the correlation analysis between dependent and independent variables are presented in Figure 4. Te dependent variable is signifcantly correlated with Age and VNF and is not statistically signifcantly correlated with ESAL, 􏽐 ESAL, AADT, AADTT, PTT, NT, PSLT, PLT, PMLT, PST, and NLF.

According to the above analysis, only Age and VNF are signifcantly correlated with dependent variables. Te reason for this phenomenon may be that the correlation between the variables is complex. Tere are multiple signifcant correlations between independent variables, which lead to deviation in correlation analysis between the dependent variable and independent variable. Te correlation between independent variables is presented in Figure 5. Red is positive, blue is negative, and the darker the color is, the stronger the correlation is. Te fgure shows that for any independent variable, there are variables associated with it that would cause the interference between variables, causing the correlation analysis result far from truth.

4.1.3. Partial and Part Correlation Analysis. According to Pearson correlation analysis results, the correlation analysis between independent variables and dependent variables should eliminate the variables that are correlated with independent variables frst. Partial and part correlation can be well used to exclude the interference between independent variables and study the correlation between independent variables and dependent variables. Te results of the partial and part correlation analysis are presented in Table 3.

Te correlation between Age and TMC is statistically signifcant both before or after eliminating the AADT, ESAL, 􏽐 ESAL, and PSLT. Te TMC has no statistically signifcant correlation with AADT, PMLT, PST, and VNF, but the signifcance would come out excluding the controlled variables. Te TMC has no statistically signifcant correlation with ESAL, 􏽐 ESAL, AADTT, PTT, NT, PSLT, PLT, and NLF before or after eliminating interference factors.

After partial and part correlation analysis, it is concluded that the strong correlation factors with the TMC are Age, AADT, PET (PSLT, PLT, PMLT, and PST), and VNF. Te routine maintenance of the tunnel mainly involved cleaning and repairing the painting. With the increase of the tunnel age, the structure in the tunnel will be seriously unpainted, and the maintenance cost also increases. Te change of AADThas an impact on the tunnel because AADT is closely related to the probability of trafc accidents and driver behavior, which afects the TMC. Te longer the tunnel is, the higher the possibility of tunnel disease. In addition, ventilation facilities can afect the TMC, which is consistent with the analysis in the introduction.

Figure 4: Correlation coefcients between dependent and independent variables.

<!-- image -->

Figure 5: Correlation coefcients between independent variables.

<!-- image -->

4.2. Hierarchical Regression Analysis. Hierarchical regression analysis was combined with correlation analysis to select the independent variables of the TMC regression model. Te district factors, time factors, and tunnel parameters were taken as important infuencing factors. Tese four factors must be included. Te result of hierarchical regression analysis is given in Table 4 and Figure 6.

Te R 2 shows that the explanatory power of the block 1 model to TMC is 3.1%, the explanatory power of the block 2 model to TMC is 39%, the explanatory power of the block 3 model to TMC is 54.6%, and the explanatory power of the block 4 model to TMC is 76.8%.

Compared with Shanbei, the Beta of Guanzhong is greater than 0, indicating that the cost in Guanzhong is higher than that in Shanbei. Compared with Shanbei, the Beta in Shannan is less than 0, indicating that the cost in Shannan is lower than that in Shanbei. Tey all have no statistical diference. Te conclusion is contrary to the result of one-way ANOVA because the cost gap between the three districts became smaller due to logarithmic transformation.

Te P values of block 2, block 3, and block 4 are all less than 0.0001, indicating that there is a signifcant correlation between cost and variables in area blocks 2, 3, and 4. Te addition of block 2 time factors have efectively improved the explanatory power of the model, where the increment of explanatory power reaches 35.8%. Te addition of block 3 trafc factors has efectively improved the explanatory power of the model, where the increment of explanatory power reaches 15.6%. Te addition of block 4 tunnel parameters has efectively improved the explanatory power of the model, where the increment of explanatory power reaches 22.2%.

Tesize of Beta was used to judge the extent of infuence of the independent variable on the dependent variable. Te Beta of lnAge is greater than that of the ln 􏽐 ESAL of block 2, while the Beta of lnAge is smaller than the ln 􏽐 ESAL in block 3. Te lnAge and ln 􏽐 ESAL variables are of similar importance to the interpretation of the dependent variable that may cause this phenomenon. It is a challenge to compare the infuence extent of time indicators (lnAge and ln 􏽐 ESAL) on the dependent variable. Te same explanation also can be applied to lnAADT and lnESAL of block 3 and block 4. Te rank of trafc indicators infuence extent is lnAADT &amp; lnESAL and AADTT &amp; PTT. Te rank of tunnel parameters infuence extent is NT, NVF, NLF, and PET(PSLT, PLT, PMLT, and PST).

Te Beta T -test of lnAge in block 2, block 3, and block 4 are statistically signifcant, and the lnAge variable has strong explanatory power on the dependent variable. Te Beta T test of ln 􏽐 ESAL in block 2 and block 4 are not statistically signifcant, while that in block 3 are statistically signifcant. Since lnAge and ln 􏽐 ESAL are collinear, only one of them can be chosen. Correlation analysis shows that the correlation between Age and TMC is statistically signifcant, and hierarchical regression analysis cannot judge the importance of the two. Consequently, the lnAge is selected as input of the model as a time indicator.

Table 3: Partial and part correlation analysis.

| Dependent   | Independent       | Independent   | Controlled variable                           | Partial    | Part       |
|-------------|-------------------|---------------|-----------------------------------------------|------------|------------|
|             | Time              | Age           | AADT, ESAL, 􏽐 ESAL, and PSLT                  | 0.415 ∗∗   | 0.382 ∗∗   |
|             | Time              | 􏽐 ESAL        | AADTT, Age, AADT, and ESAL                    | - 0.192    | - 0.163    |
|             | Time              | AADT          | Age, ESAL, 􏽐 ESAL, AADTT, and NT              | 0.410 ∗∗   | 0.348 ∗∗   |
|             | Trafc             | ESAL          | PMLT,Age, AADT, 􏽐 ESAL, and PMLT              | 0.076      | 0.062      |
|             | Trafc             | AADTT         | Age, AADT, ESAL, 􏽐 ESAL, NT, and PMLT         | - 0.043    | - 0.033    |
|             | Trafc             | PTT           | PMLT, PST, and NT                             | - 0.099    | - 0.095    |
| TMC         |                   | NT            | AADTT, AADT, PSLT, PLT, PMLT, PST, and NLF    | - 0.180    | - 0.134    |
| TMC         |                   | PSLT          | Age, PMLT, and VNF                            | - 0.059    | - 0.052    |
| TMC         |                   | PLT           | NT, PLT, and NLF                              | 0.115      | 0.109      |
|             | Tunnel parameters | PMLT          | ESAL, AADTT, PTT, NT, PSLT, PLT, PST, and VNF | - 0.401 ∗∗ | - 0.330 ∗∗ |
|             | Tunnel parameters | PST           | AADTT, NT, PLT, PMLT, and NLF                 | 0.266 ∗    | 0.250 ∗    |
|             | Tunnel parameters | NVF           | PSLT and PMLT                                 | - 0.274 ∗  | - 0.266 ∗  |
|             | Tunnel parameters | NLF           | NT, PLT, and PST                              | - 0.094    | - 0.089    |

Table 4: Te results of hierarchical regression analysis.

| Variables   | Block 1   | Block 1   | Block 1   | Block 2   | Block 2   | Block 2   | Block 3   | Block 3   | Block 3   | Block 4   | Block 4   | Block 4   |
|-------------|-----------|-----------|-----------|-----------|-----------|-----------|-----------|-----------|-----------|-----------|-----------|-----------|
| Variables   | Beta      | t         | P         | Beta      | t         | P         | Beta      | t         | P         | Beta      | t         | P         |
| Guanzhong   | 0.063     | 0.379     | 0.707     | 0.077     | 0.473     | 0.639     | 0.479     | 1.460     | 0.152     | - 8.857   | - 3.976   | 0.000     |
| Shannan     | - 0.135   | - 0.808   | 0.423     | - 0.122   | - 0.796   | 0.430     | 0.318     | 1.248     | 0.219     | 3.067     | 4.088     | 0.000     |
| lnAge       | -         | -         | -         | 0.872     | 4.464     | 0.000     | 1.870     | 5.611     | 0.000     | 0.844     | 2.390     | 0.022     |
| ln 􏽐 ESAL   | -         | -         | -         | - 0.433   | - 1.954   | 0.057     | - 2.665   | - 3.836   | 0.000     | - 1.056   | - 1.520   | 0.137     |
| lnAADT      | -         | -         | -         | -         | -         | -         | 0.752     | 1.145     | 0.259     | 1.737     | 2.547     | 0.015     |
| lnESAL      | -         | -         | -         | -         | -         | -         | 1.436     | 2.413     | 0.020     | 1.265     | 1.820     | 0.077     |
| PTT         | -         | -         | -         | -         | -         | -         | 0.572     | 2.370     | 0.023     | - 1.121   | - 2.047   | 0.048     |
| lnAADTT     | -         | -         | -         | -         | -         | -         | - 0.740   | - 1.050   | 0.300     | - 0.442   | - 0.447   | 0.657     |
| lnNT        | -         | -         | -         | -         | -         | -         | -         | -         | -         | 8.640     | 3.587     | 0.001     |
| PSLT        | -         | -         | -         | -         | -         | -         | -         | -         | -         | - 0.631   | - 2.915   | 0.006     |
| PLT         | -         | -         | -         | -         | -         | -         | -         | -         | -         | - 0.295   | - 0.843   | 0.405     |
| PMLT        | -         | -         | -         | -         | -         | -         | -         | -         | -         | - 6.560   | - 4.696   | 0.000     |
| lnNVF       | -         | -         | -         | -         | -         | -         | -         | -         | -         | - 9.357   | - 4.501   | 0.000     |
| lnNLF       | -         | -         | -         | -         | -         | -         | -         | -         | -         | - 15.099  | - 4.084   | 0.000     |
| R 2         |           | 0.031     |           |           | 0.390     |           |           | 0.546     |           |           | 0.768     |           |
| Adjust R 2  |           | - 0.010   |           |           | 0.335     |           |           | 0.457     |           |           | 0.675     |           |
| F           |           | 0.755     |           |           | 7.181     |           |           | 6.163     |           |           | 8.254     |           |
| P           |           | 0.475     |           |           | 0.000     |           |           | 0.000     |           |           | 0.000     |           |
| Δ R 2       |           | 0.031     |           |           | 0.358     |           |           | 0.156     |           |           | 0.222     |           |
| Δ F         |           | 0.755     |           |           | 13.214    |           |           | 3.529     |           |           | 5.560     |           |
| Δ P         |           | 0.475     |           |           | 0.000     |           |           | 0.015     |           |           | 0.000     |           |

Te Beta T -test of lnESAL and PTT in block 3 are statistically signifcant. In block 4, lnAADT's Beta T -test is statistically signifcant. Correlation analysis shows that the correlation between AADT and TMC is statistically significant, and AADT is statistically signifcantly correlated with ESAL and AADTT, while ESAL and AADTT are not statistically signifcantly correlated with TMC. For this reason, ESAL and AADTT are abandoned, and AADT is retained. Although AADTT is not statistically signifcantly correlated with the dependent variable, it is also not statistically signifcantly correlated with AADT. Te Beta T -test of AADTTis statistically signifcant in block 3 and block 4, so it can be put into the model.

In tunnel parameter indicators, the Beta T -test of NT, PSLT, PMLT, lnNVF, and NLF in block 4 are statistically signifcant, while the Beta T -test of PLT is not statistically signifcant. Correlation analysis shows that the TMC hase no statistically signifcant correlation with NT and NLF variables before or after eliminating interference factors. TMC has no statistically signifcant correlation with PST, but the signifcance would come out excluding the AADTT, NT&amp; PLT, and PMLT &amp; NLF variables. Te PET (PSLT, PLT, PMLT, and PST) and NVF have a statistically signifcant correlation with TMC, while NT has a statistically signifcant correlation with PET and NLF. NT is deleted from the tunnel parameters indicators to eliminate collinear infuence. Te variables such as PET, lnNVF, and lnNLF are selected.

Figure 6: Beta coefcient of the independent variables.

<!-- image -->

In conclusion, the main infuencing factors to the TMC are districts (Shanbei, Guanzhong, and Shannan), Age, AADT, AADTT, PET (PSLT, PLT, PMLT, and PST), and NVF.

4.3. Grouped Ridge Regression. Regression models were established for obtaining the data in districts. Te grouped regression led to fewer data and serious collinearity among variables. Many variables' VIF values were greater than 50, so ridge regression was adopted. Te results of the grouped ridge regression models are presented in Table 5.

Te regression coefcients and models of ridge regression are statistically signifcant, and the R 2 is more than 0.6. Te grouped ridge regression model can well predict the TMC in the three districts, but such grouped regression will lead to over-ftting of data within the group and ignores intergroup information. Te size of variable coefcients in the three districts is quite diferent. For example, the coefcient of AADT is positive in the Shanbei model and Guanzhong model, and it is negative in the Shannan model. Te coefcient of PTT is positive in the Shanbei model and Shannan model, and it is negative in the Guanzhong model. It can be seen that coefcients in the three models of grouped ridge regression cannot well explain the relationship between infuencing factors and the TMC.

4.4. Fixed-Efected Regression. Te data were analyzed by fxed-efect regression. Te district variables Guanzhong VIF was equal to 12.67, Shannan VIF was equal to 12.91, and the others VIF was less than 9. Collinearity between variables was not serious, and the regression results were reliable. Te results of the fxed-efected regression model are presented in Table 6.

Te R 2 of the fxed-efect regression model is 0.477. Te reason for the small R 2 may be that in the correlation analysis, only the Age and NVF are signifcantly correlated with the TMC. Meanwhile, there may be great randomness in routine maintenance of tunnels. Since the model is multidimensional, too large R 2 may be the result of over-ftting.

According to Figure 7, the predicted value has a similar trend to the actual value. Te P value was less than 0.05, indicating that there are variables in the independent variables that can explain the dependent variable. Figure 8 is the coefcient diagram of ridge regression and fxedefect regression. Te PSLT coefcient of Shannan is much smaller than that of other models, and the regression coefcients of the fxed-efect model are similar to those of the Guanzhong model and Shanbei model, indicating that the regression results of fxed-efects are robust. Terefore, the discussion of the model results focused on the fxed-efect model result.

Table 5: Grouped ridge regression.

| Variables   | Shanbei   | Shanbei   | Shanbei   | Guanzhong   | Guanzhong   | Guanzhong   | Shannan   | Shannan   | Shannan   |
|-------------|-----------|-----------|-----------|-------------|-------------|-------------|-----------|-----------|-----------|
|             | β         | t         | P         | β           | t           | P           | β         | t         | P         |
| Constant    | 0.715     | 0.414     | 0.69      | - 30.227    | - 2.168     | 0.053       | 6.686     | 7.33      | 0.000     |
| lnAge       | 0.706     | 2.645     | 0.029     | 0.776       | 2.028       | 0.068       | 0.166     | 0.783     | 0.456     |
| lnAADT      | 0.076     | 0.787     | 0.454     | 1.146       | 2.097       | 0.06        | - 0.306   | - 5.151   | 0.001     |
| PTT         | 0.3       | 0.537     | 0.606     | - 9.951     | - 0.754     | 0.467       | 1.353     | 0.706     | 0.5       |
| PSLT        | 0.11      | 0.167     | 0.871     | 0           | 0           | 0           | - 27.502  | - 8.038   | 0.000     |
| PLT         | - 1.54    | - 2.029   | 0.077     | 1.561       | 1.757       | 0.107       | - 3.844   | - 4.706   | 0.002     |
| PMLT        | 0.476     | 0.374     | 0.718     | 4.023       | 1.757       | 0.107       | - 2.463   | - 4.993   | 0.001     |
| lnNVF       | 0.042     | 0.111     | 0.914     | 5.534       | 1.757       | 0.107       | - 0.284   | - 5.685   | 0.000     |
| R 2         |           | 0.693     |           |             | 0.647       |             |           | 0.894     |           |
| F           |           | 2.575     |           |             | 3.365       |             |           | 9.615     |           |
| P           |           | 0.104     |           |             | 0.039       |             |           | 0.002     |           |

Table 6: Fixed-efect regression model.

Figure 7: Scatter plot of the predicted and actual values.

| Variables   | Beta    | β       | t      | P     |
|-------------|---------|---------|--------|-------|
| lnAge       | 0.685   | 1.222   | 3.60   | 0.001 |
| lnAADT      | - 1.032 | - 0.604 | - 3.33 | 0.002 |
| PTT         | 0.469   | 2.881   | 2.72   | 0.010 |
| PSLT        | 0.128   | 1.972   | 1.14   | 0.259 |
| PLT         | 0.210   | 1.302   | 1.35   | 0.184 |
| PMLT        | - 0.049 | - 0.564 | - 0.22 | 0.826 |
| lnNVF       | - 0.681 | - 1.334 | - 2.81 | 0.008 |
| Constant    | 1       | 8.788   | 3.39   | 0.002 |
| Guanzhong   | 0.896   | 10.944  | 2.53   | 0.016 |
| Shannan     | 0.898   | 11.012  | 2.49   | 0.017 |
| R 2         |         |         | 0.4771 |       |
| F           |         |         | 5.47   |       |
| P           |         |         | 0.0001 |       |

<!-- image -->

Te coefcient of lnAge is positive, indicating that the TMCincreases with the increase of tunnel age. In practice, as the road age increases, the road condition will deteriorate, which causes an increase in cost. Te P value is less than 0.05, indicating that the coefcient of lnAge is statistically signifcant.

Tecoefcient of lnAADTis negative, and the coefcient T -test is statistically signifcant, which is counterintuitive and worth future study. Firstly, in this study, the routine maintenance content of the tunnel does not include tunnel pavement, so the relationship between AADT and TMC is not close. Secondly, at the beginning of the tunnel lifecycle, the trafc volume is low enough, and the tunnel is in good condition. As the trafc volume in the tunnel gradually increases, the TMC remains the same for some time. Besides, there is a large diference in the tunnel age of diferent roads in the original data. For these above reasons, when taking the district as the independent variable comprehensively, the coefcient of lnAADT may be negative. Terefore, the coefcient of lnAADT is not taken as the analysis result of the dependent variable. Te lnAADT is only put into the fxedefect regression model as the control variable.

Figure 8: Regression coefcient of ridge regression and fxed-efect regression.

<!-- image -->

Te coefcient of the PTT is positive, and the T -statistic test is statistically signifcant. With the increase in PTT, the TMC will increase, which is consistent with the practical situations.

Te coefcient of PET in the model is not statistically signifcant by the T -test. Tis may be due to insufcient data. Te proportion distribution of long and short tunnels of diferent highway contracts varies greatly, and some roads have no long tunnel. With many independent variables in the model, it is reasonable that the explanatory ability of variables is insufcient, and the T -test is not statistically signifcant. Te higher the PSLT and PLT are, the higher the TMC is. It is speculated that the longer the tunnel is, the higher the possibility of tunnel disease, and the higher the TMC is. Te proportion coefcient of PMLT is negative. Because the higher the proportion of PMLT is, the lower the PSLT and PLT are, and the lower the TMC is.

Te lnNVF coefcient T -test is statistically signifcant in the model, and the coefcient sign is negative. Te reason may be that ventilation facilities have been installed to help to maintain a clean environment in the tunnel, which indirectly afects the daily maintenance costs of the tunnel.

In the log-log model, the regression coefcient indicates the elasticity of the corresponding variable. According to the regression coefcient, the TMC increases by 1.222% when the Age increases by 1%, while the TMC increases by 2.881% when the PTT increases by 1%. Te TMC increases by 1.972% when the PSLT increases by 1%; the TMC increases by 1.302% when the PLT increases by 1%. However, the TMC decreases by 0.564% when the PMLT increases by 1%, and the TMC decreases by 1.334% when NVF increases by 1%. From the analysis above, the PTT has the greatest impact on the TMC, while Age and PET have the least efect on TMC. Te TMC can be controlled by keeping the balance between these factors.

By comparing the size of Beta, the larger the absolute value of Beta is, the higher the explanatory power of variables to the model is, and the greater the infuence is. Terefore, it can be seen from the regression results that the continuous variables of the TMC model are ranked as Age, NVF, PTT, and PET (PSLT, PLT, PMLT, and PST).

Compared with grouped regression, the fxed-efect regression model contains the infuence of Shanbei, Guanzhong, and Shannan comprehensively although there are signifcant diferences in the TMC among the three districts as well as in landforms. Because the diferences are within a certain range, and the infuencing factors of TMC in the three districts are similar, and the corresponding coeffcient should be similar.

Terefore, the random-intercept and fxed-coefcient model obtained by using this comprehensive regression model can better refect the relationship between the infuencing factors and the TMC.

## 5. Conclusion

Teobjective of this research was to provide an approach in which quantitative analysis was combined with qualitative analysis to quickly select the independent variables of TMC model and estabish a model to estimate the annual highway routine maintenance cost of tunnels. For the analysis, the developed fxed-efect regression model of the fxed district can well explain the relationship between TMC and the infuencing factors of tunnels and then predict the future TMC.

Te main observations that can be drawn from the analysis results are as follows:

- (1) Te method of quickly select independent variables of maintenance cost regression model has a strong explanatory force to the dependent variable, and thus, the established regression model built on the TMC has a relatively good ft.
- (2) Te infuencing factors that can be considered in establishing the TMC model are district, Age, AADT, PTT, PET, and NVF, and PTT has the greatest impact on the TMC, while Age and PET have the least efect on TMC. In addition, the NVF has a positive contribution to the TMC.
- (3) Te highway operation agencies should plan trafc reasonably and control the proportion of heavy vehicles efciently. Apart from this, ventilation

- facilities installed for tunnels with a sufcient budget can efectively save routine maintenance costs.
- (4) Te fxed-efect regression model has higher ftting accuracy and a better regression coefcient signifcance than the grouped regression model because the grouped regression model always losses the information related to each category.
- (5) Since it is hard to compare the diference in TMC of diferent lengths due to insufcient data collection, more detailed classifcation and storage of data are needed for the data collection, which will be helpful for the highway management agencies to make a better plan and save maintenance costs.

## Data Availability

Te data are available upon request to the corresponding author. Data are collected from Shaanxi Transportation Holding Group.

## Conflicts of Interest

Te authors declare that they have no conficts of interest.

## Acknowledgments

Tework was funded by the Natural Science Basic Research Program of Shaanxi Province (No. 2022 JM-307). All contributions are gratefully acknowledged. In particular, Ms. Liu polished the language of this article.

## References

- [1] M. Hagood, Highway Routine Maintenance Cost Estimation for Nevada , University of Nevada, Las Vegas, 2014.
- [2] Q. Cui, M. Y. Dong, X. C. Wang et al., 'Research on evaluation model and evaluation system of highway tunnel maintenance costs,' Tunnelling &amp; Underground Space Technology Incorporating Trenchless Technology Research , vol. 034, no. 001, pp. 104-109, 2017.
- [3] H. Jorgen, Optimization of Operation and Maintenance Activities and Costs for Road Tunnels Based on Experience , 2011.
- [4] Q. Ai, Y. Yuan, S. Mahadevan, and X. Jiang, 'Maintenance strategies optimisation of metro tunnels in soft soil,' Structure and Infrastructure Engineering , vol. 13, no. 8, pp. 1093-1103, 2017.
- [5] D. Alvear, O. Abreu, A. Cuesta, and V. Alonso, 'Decision support system for emergency management: road tunnels,' Tunnelling and Underground Space Technology , vol. 34, pp. 13-21, 2013.
- [6] S. A. Ghahari, M. Volovski, S. Alqadhi, and M. Alinizzi, 'Estimation of annual repair expenditure for interstate highway bridges,' Infrastructure Asset Management , vol. 6, no. 1, pp. 40-47, 2019.
- [7] A. Taggart, L. Tachtsi, M. Lugg, and H. Davies, 'UKRLG framework for highway infrastructure asset management,' Infrastructure Asset Management , vol. 1, no. 1, pp. 10-19, 2014.
- [8] A. I. Al-Mansour and K. C. Sinha, 'Economic Analysis of Efectiveness of Pavement Preventive Maintenance,' Transportation Research Record Journal of the Transportation Research Board , vol. 2672, no. 12, 1994.
- [9] P. Lu and D. Tolliver, 'Multiobjective pavement-preservation decision making with simulated constraint boundary programming,' Journal of Transportation Engineering , vol. 139, no. 9, pp. 880-888, 2013.
- [10] R. Gibby, R. Kitamura, and H. Zhao, 'Evaluation of truck impacts on pavement maintenance costs,' Transportation Research Record Journal of the Transportation Research Board , vol. 1262, pp. 48-56, 1990.
- [11] M. J. Volovski, Econometric Models for Pavement Routine Maintenance Expenditure , Purdue University, West Lafayette, IN, USA, 2011.
- [12] C. L. Wu, Research on Estimation Model of Highway Asphalt Pavement Maintenance Cost Based on Target Maintenance Cycle , Chongqing Jiaotong University, Chongqing, China, 2016.
- [13] Y. Ruan, Research of Maintenance Amount Prediction on the Highway with Intelligent Algorithm , Wuhan Univeristy of Technology, Wuhan, China, 2015.
- [14] S. A. Ola and I. A. Ugiomoh, 'Cost of road maintenance in developing countries,' Journal of Transportation Engineering , vol. 112, no. 4, pp. 440-445, 1986.
- [15] C. X. Zhang and W. Wang, 'Study on the method of determining preventive maintenance time for bridges based on optimal cost efectiveness,' Highways , vol. 4, no. 7, pp. 259262, 2013.
- [16] Y. H. Dong, TeResearch of Bridge Maintenance Management System , Chang'an University, Xi'an, China, 2014.
- [17] G. Barone and D. M. Frangopol, 'Life-cycle maintenance of deteriorating structures by multi-objective optimization involving reliability, risk, availability, hazard and cost,' Structural Safety , vol. 48, pp. 40-50, 2014.
- [18] M. F. Dan, S. Sabatino, and D. You, 'Bridge life-cycle performance and cost: analysis, prediction, optimization and decision making,' Maintenance, Management, Life-Cycle Design and Performance , vol. 12, no. 10, pp. 1239-1257, 2016.
- [19] J. L. Smith, Life-cycle Cost Analysis of Reinforced concrete Bridges Rehabilitated with CFRP , Lexington, KY, USA, 2015.
- [20] D. Kifokeris, J. A. Campos e Matos, Y. Xenidis, and L Bragança, 'Bridge quality appraisal methodology: application in a reinforced concrete overpass roadway bridge,' Journal of Infrastructure Systems , vol. 24, no. 4, Article ID 04018034, 2018.
- [21] T. Hegazy, E. Elbeltagi, and H. El-Behairy, 'Bridge deck management system with integrated life-cycle cost optimization,' Transportation Research Record Journal of the Transportation Research Board , vol. 1866, no. 1, pp. 44-50, 2004.
- [22] Z. J. Song, Research on Information Management of Integrated Construction and Maintenance of Highway Bridge , Southeast University, Zhejiang, China, 2015.
- [23] K. C. Sinha, S. Labi, and B. G. Mccullouch, Updating and Enhancing the Indiana Bridge Management System (IBMS) , Purdue University Press, West Lafayette, 2009.
- [24] C. Zhou, Research on Condition Assessment of Existing Bridges and the Maintenance Managing Method , Zhejiang University, Zhejiang, China, 2008.
- [25] S. Y. Ok, S. Y. Lee, and W. Park, 'Robust multi-objective maintenance planning of deteriorating bridges against uncertainty in performance model,' Advances in Engineering Software , vol. 65, pp. 32-42, 2013.
- [26] F. Biondini and D. M. Frangopol, 'Life-cycle performance of deteriorating structural systems under uncertainty: review,' Journal of Structural Engineering , vol. 142, no. 9, p. F4016001, 2016.

- [27] J. L. Qin, Research on Key Technology to Bridge Maintenance Planning , Beijing University of Civil Engineering and Architecture, Beijing, 2014.
- [28] Z. J. Hu, Study of RC Beam Bridge Condition State Assessment System Based on Al , Tongji University, Shanghai, China, 2006.
- [29] G. Du, M. Saf, L. Pettersson, and R. Karoumi, 'Life cycle assessment as a decision support tool for bridge procurement: environmental impact comparison among fve bridge designs,' International Journal of Life Cycle Assessment , vol. 19, no. 12, pp. 1948-1964, 2014.
- [30] W. S. Han, Y. Zhao, and H. J. Liu, 'Research status and development trend of wind-vehicle-bridge coupled vibration,' China Journal of Highway and Transport , vol. 031, no. 007, pp. 1-23, 2018.
- [31] Z. H. Zong, Z. G. Yang, and Y. F. Xia, 'Vehicle load model of Xinyihe bridge under congestion operation,' China Journal of Highway and Transport , vol. 29, no. 2, p. 8, 2016.
- [32] X. C. Li, Research on Tunnel Maintenance Model and Reasonable Cost , Chang'an University, Xi'an, China, 2015.
- [33] M. Hu, P. P. Liu, and G. Yu, 'Decision support system for tunnel operation and maintenance based on BIM and tunnel whole life cycle information,' Tunnel Construction , vol. 37, no. 4, p. 7, 2017.
- [34] S. Janbaz, M. Shahandashti, M. Najaf, and R. Tavakoli, 'Lifecycle cost study of underground freight transportation systems in Texas,' Journal of Pipeline Systems Engineering and Practice , vol. 9, no. 3, Article ID 05018004, 2018.
- [35] G. T. Kim, K. T. Kim, D. H. Lee, C. H. Han, H. B. Kim, and J. T. Jun, 'Development of a life cycle cost estimate system for structures of light rail transit infrastructure,' Automation in Construction , vol. 19, no. 3, pp. 308-325, 2010.
- [36] Y. Zhang, D. Novick, and A. Hadavi, 'Life-cycle cost analysis of bridges and tunnels,' Construction Research Congress , 2005.
- [37] K. Petroutsatou, A. Maravas, and A. Saramourtsis, 'A life cycle model for estimating road tunnel cost,' Tunnelling and Underground Space Technology , vol. 111, Article ID 103858, 2021.
- [38] W. W. Chu, X. S. Chu, and L. Q. Gao, 'Development and application of BIM based operation and maintenance management system to zizhi tunnel,' Tunnel Constr , vol. 38, no. 10, p. 10, 2018.
- [39] H. Ding, Y. Pan, and S. Cai, 'Development and application of intelligent cloud platform for 'Yunyou' highway tunnel maintenance management,' Highways , vol. 62, no. 11, p. 4, 2017.
- [40] G. English, 'Tunnel operations, maintenance, inspection, and evaluation manual, 2015: practical implications for fre protection and life safety systems,' Transportation Research Record Journal of the Transportation Research Board , vol. 2592, no. 1, pp. 162-168, 2016.
- [41] A. Higham, C. Fortune, and H. James, 'Life cycle costing: evaluating its use in UK practice,' Structural Survey , vol. 33, no. 1, pp. 73-87, 2015.
- [42] J. Wang, A. Koizumi, and H. Tanaka, 'Framework for maintenance management of shield tunnel using structural performance and life cycle cost as indicators,' Structure and Infrastructure Engineering , vol. 13, no. 1, pp. 44-54, 2017.
- [43] J. M. Wooldridge, Introductory Econometrics a Modern Approach , Renmin University of China Press, Beijing, China, 2010.
- [44] M.o.T.o.t.P.s.R.o, Te Specifcation for the Design of Highway Asphalt Pavement , China-Industry standard-transportation CN-JT, China, 2017.
- [45] L. China, Specifcations for Design of Highway Tunnels , People's Communications Publishing House Co., Ltd, Beijing, China, 2018.
- [46] S. P. B. . o. Statistics, Shaanxi Statistical Yearbook , China Statistics Press, Beijing, China, 2020.
- [47] M. Irfan, M. B. Khurshid, A. Ahmed, and S. Labi, 'Scale and condition economies in asset preservation cost functions: case study involving fexible pavement treatments,' Journal of Transportation Engineering , vol. 138, no. 2, pp. 218-228, 2012.
- [48] W. Woldemariam, J. Murillo-Hoyos, and S. Labi, 'Estimating annual maintenance expenditures for infrastructure: artifcial neural network approach,' Journal of Infrastructure Systems , vol. 22, no. 2, 2016.
- [49] T. Chen, Q. Chang, J. Liu, Y. Qi, and M. Liu, 'Temporal and spatial variability of soil available nutrients in arable lands of heyang county in south loess plateau,' Acta Ecologica Sinica , vol. 33, no. 2, pp. 554-564, 2013.
- [50] Y. Jing-han, L. Meng-yun, Z. Jie, Z. Meng-meng, C. Run-shan, and C. Xin-yue, 'Spatial variability of soil nutrients and its afecting factors at small watershed in gully region of the Loess Plateau,' Journal of Natural Resources , vol. 35, no. 3, pp. 743-754, 2020.
- [51] C. Qiang, Advanced Econometrics and Stata Applications , Higher Education Press, Beijing, China, 2014.
- [52] L. H. Zhuo, 'Price elasticity of civil aviation in the context of High-speed rail development: an empirical analysis based on panel data of 449 cities in China,' Price theory and practice , vol. 4, no. 10, pp. 66-70, 2021.
- [53] H. Z. Qiu, Quantitative Research and Statistical Analysis , Chongqing University Press, Chongqing, China, 2013.
- [54] N. Q. Xie and G. L. Jiang, 'Multicollinearity problem in compiling composite indices using repeated trading models: a parametric improvement based solution,' Systems engineering theory and practice , vol. 42, no. 6, pp. 1-17, 2022.
- [55] J. M. Shaver, 'Interpreting interactions in linear fxed-efect regression models: when fxed-efect estimates are no longer within-efects,' Strategy Science , vol. 4, no. 1, pp. 25-40, 2019.
- [56] D. J. Henderson, A. Soberon, and J. M. Rodriguez-Poo, 'Nonparametric multidimensional fxed efects panel data models,' Econometric Reviews , vol. 41, no. 3, pp. 321-358, 2022.

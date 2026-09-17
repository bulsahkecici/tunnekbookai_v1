## OPEN

<!-- image -->

Logo

## A study on risk assessment and system development of tunnel lighting facilities based on XGBoost and Bayesian optimization

Hui Xiao 1 , Weihong Yang 1 , Jiabao Tang 2 &amp; Zhiliu L. Wang 2,3 

Tunnel lighting facilities exhibit significantly increased failure rates and accident risks during long-term operation and maintenance (O&amp;M) due to environmental erosion and equipment aging. Addressing the high latency and resource inefficiency inherent in traditional periodic maintenance models, this study proposes a data-driven dynamic risk assessment methodology for risk assessment and system development of tunnel lighting facilities, with a specific focus on leveraging XGBoost and Bayesian optimization. The research process encompassed several steps: (1) multi-source data fusion for risk factors: integrating 12 critical indicators, including illuminance levels, waterproofing status of electromagnetic contactors, internal tunnel temperature, voltage stability, relative humidity, pole integrity, tunnel wind speed, cumulative operational days of lamps, number of damaged lamps, line corrosion, luminaire damage status, and cumulative operating hours of light sources-to construct multi-dimensional feature engineering. (2) Development of a risk assessment model: utilizing the XGBoost algorithm enhanced by Bayesian Optimization (BO) for automated hyperparameter tuning, effectively capturing nonlinear and temporal features while overcoming the inefficiency of traditional hyperparameter tuning methods. (3) Model validation and lightweight system development: Validated using empirical data from Caoguo Mountain Tunnel, this study innovatively establishes a closedloop workflow integrating 'model training, dynamic assessment, and risk prediction'. An embedded assessment system, developed in PyCharm, implements an optimized three-tier architecture ('data acquisition-algorithmic computation-decision output'). This system achieved a 98.0% failure prediction accuracy on the Caoguo Mountain Tunnel dataset, thereby demonstrating a significant reduction in the operational and maintenance (O&amp;M) risks of lighting facilities. These findings provide scientific theoretical and practical foundations for tunnel infrastructure maintenance.

Keywords Lighting facilities, Risk assessment, XGBoost algorithm, Bayesian optimization, Early warning system

Deterioration in highway tunnel lighting systems-such as lamp aging and circuit failures-severely impairs drivers' visual clarity and decision-making ability. This impairment often precipitates traffic accidents, leading to casualties and property losses. Traditional operation and maintenance (O&amp;M) strategies for lighting facilities predominantly rely on scheduled manual inspections and post-failure repairs, which exhibit inherent limitations: high-latency responses, resource inefficiency, and a failure to proactively identify and mitigate potential risks. Moreover,  these  conventional  approaches  incur  substantial  maintenance  costs.  Consequently,  implementing precise risk assessment for highway tunnel lighting infrastructure is of critical importance.

Artificial intelligence (AI) applications in tunnel lighting systems are increasingly emerging as a focal research area within civil engineering, driving innovations in design, operation, and safety management. For instance, Xu et al. 1 developed a digital workflow for lighting environment design assessment, incorporating a lifecycle framework to support carbon and cost reduction strategies in tunnels-bridging technical optimization with sustainable development goals. Additionally, Lim et al. 2 examined the influence of information delivery systems

1 Central  Research  Institute  of  Building  and Construction Co.,  Ltd.,  MCC Group,  Beijing  100088, China. 2 School of  Civil  Engineering  and  Architecture,  Zhongyuan  University  of Technology,  Zhengzhou  450007,  China. 3 State Key  Laboratory  of  Water  Resource  Protection  and  Utilization  in  Coal  Mining,  Beijing  102211,  China.  email: wzl8925@163.com on illumination intensity and speed limits, shedding light on how intelligent information transmission interacts with lighting performance to shape driving conditions. In parallel, research has advanced our understanding of  the  interplay  between  lighting  facilities  and  driving  safety.  Wang  et  al. 3 conducted field  studies  on  linear visual  guiding  facilities,  aiming  to  enhance  highway  tunnel  safety  through  targeted  improvements  to  visual guidance systems. Another study by Wang et al. 4  delved into the high-dynamic impact mechanism of complex spiral  tunnel  environments on driving behavior, leveraging multi-source data fusion to unpack the intricate relationships between environmental factors and driver responses. Complementing this, Chen et al. 5  performed safety assessment and prediction under diverse tunnel lighting service states, providing a foundation for risk quantification across varying operational scenarios. Shen et al. 6 further contributed by improving the tunnel lighting  environment  using  a  holistic  digital  twin  framework,  integrating  virtual  modeling  with  real-world operation for dynamic optimization. Expanding on technical methodologies, Shen et al. 7 researched a diffuse reflection-based computational lighting model paired with a particle swarm optimization algorithm, offering precision tools for luminance simulation in highway tunnels. Niu et al. 8 developed a multi-parameter intelligent control  method  for  enhancing  lighting  environments  in  long  tunnels,  accounting  for  dynamically  changing luminance differences to adapt to real-time conditions.

Collectively,  these  studies  have  significantly  advanced  the  intelligentization  of  tunnel  lighting,  spanning design  optimization,  safety  management,  and  adaptive  control.  However,  a  critical  and  unresolved  gap remains:  nearly  all  existing  tunnel  lighting-related  research  focuses  on  lighting  environment  optimization, driving  behavior  impact  analysis,  and  intelligent  brightness  control,  while  research  on  the  full-dimensional risk assessment of the lighting infrastructure itself is seriously insufficient. To date, no systematic quantitative evaluation index system covering environmental adaptability, equipment durability, and electrical safety has been formed for tunnel lighting facilities. Moreover, existing risk assessment methods for tunnel facilities-such as Analytic Hierarchy Process, Fuzzy Comprehensive Evaluation, and Fault Tree Analysis-rely excessively on subjective expert experience for weight setting, leading to strong artificial subjectivity and inability to adapt to the multi-factor, strong-coupling risk evolution law of tunnel lighting facilities. Traditional risk management methods under the routine O&amp;M mode (regular inspection, post-failure repair) can only achieve lagging fault disposal, failing to capture the gradual and nonlinear characteristics of lighting facility performance degradation and thus unable to realize forward-looking risk early warning. This gap is rooted in the difficulty of integrating multi-source heterogeneous data (including fundamental operational parameters, environmental factors, and equipment states) and the lack of targeted assessment methods, which imposes stringent requirements on model robustness and comprehensive performance, highlighting the need for a unified framework to address these interconnected challenges.

To  effectively  model  high-dimensional,  nonlinear  risk  interdependencies  while  enhancing  assessment robustness and generalizability, researchers have increasingly adopted advanced ensemble learning techniques, with the XGBoost algorithm standing out. For instance, Emara et al. 9   applied XGBoost to 3D wear mapping in sediment bypass tunnels; Cheng et al. 10  optimized XGBoost for complexity-performance balance to predict pipeline/tunnel  effective  lengths  under  normal  faults;  Yuan  et  al. 11 developed  an  XGBoost-based  fatigue detection model for long tunnel group excavation; Qiao et al. 12 used XGBoost for global sensitivity analysis of shield tunnel-induced ground settlement in karst areas; Bo et al. 13 integrated a PSO variant with XGBoost for tunnel deformation prediction in TBM interference scenarios; Nguyen et al. 14  proposed a hybrid MFO-XGBoost model for rectangular tunnel racking ratio prediction under seismic loads; Lin et al. 15  explored highway carbon emission prediction via an XGBoost-SVR ensemble; Chen et al. 16  studied large-diameter river-crossing tunnel segment uplift using XGBoost; Xia et al. 17 researched shield construction ground settlement prediction with XGBoost;  and  Wang  et  al. 18 designed  an  XGBoost-based  intelligent  decision  system  for  TBM  operational parameters.

These  studies  fully  validate  XGBoost's  strengths  in  handling  complex  data  and  mitigating  overfitting, providing  a  novel  technical  pathway  for  tunnel  lighting  infrastructure  risk  assessment.  However,  a  critical research  gap  persists:  current  civil  engineering  applications  of  XGBoost  focus  primarily  on  tunnel  boring parameter optimization, surrounding rock deformation prediction, ground settlement analysis, and highway construction quality prediction, leaving its potential in tunnel lighting risk assessment completely untapped. There is no complete methodology for algorithm adaptation, hyperparameter optimization, and engineering implementation of XGBoost for the specific scenario of tunnel lighting risk assessment. Furthermore, existing AI algorithms applied in tunnel engineering are not adapted and optimized for the multi-source heterogeneous, high-dimensional, and nonlinear data characteristics of lighting facilities, so their generalization ability and robustness  cannot  meet  the  actual  engineering  requirements  for  precise  risk  assessment.  More  importantly, although the integration  of  Bayesian  optimization  (BO)  and  XGBoost  has  been  widely  used  in  engineering prediction problems, such applications are mostly concentrated in traditional tunnel engineering scenarios (e.g., surrounding rock deformation, construction quality) and adopt a general workflow without targeted design for tunnel lighting scenarios, failing to reflect the uniqueness of lighting risk assessment and the particularity of its data characteristics.

To address the critical research gaps in tunnel lighting facility risk assessment, this study proposes a targeted assessment  framework  with  substantive  scientific,  methodological,  and  practical  advances  beyond  routine predictive modeling and standard BO-XGBoost integration pipelines. From a scientific perspective, we construct a dedicated multi-dimensional risk indicator system covering environmental adaptability, equipment longevity, and  electrical  safety  with  12  quantifiable  indicators,  which  fills  the  gap  of  lacking  professional  quantitative assessment systems for lighting facilities and effectively characterizes the nonlinear coupling of multi-source heterogeneous risk factors-this indicator system is tailored to the operational characteristics of tunnel lighting facilities, differing from the general indicators used in other tunnel engineering prediction scenarios.

From a methodological perspective, we integrate Bayesian optimization and XGBoost with targeted design for the high-dimensional and nonlinear characteristics of lighting operation data, which is the core difference from  the  standard  BO-XGBoost  pipeline.  Specifically,  we  optimize  the  Gaussian  process  kernel  function of  Bayesian optimization to adapt to the dynamic and heterogeneous characteristics of tunnel lighting data, realizing  efficient  global  hyperparameter tuning that is more accurate than traditional empirical tuning and standard BO workflows; meanwhile, we improve the loss function of XGBoost to enhance its ability to identify the coupling risk of lighting equipment and environmental factors, avoiding simple algorithm migration without scenario adaptation. From a practical perspective, we build a complete closed-loop workflow of 'model training, dynamic  assessment,  and  risk  prediction'  and  independently  develop  a  lightweight  intelligent  assessment system, which realizes proactive risk early warning and supports the transformation of tunnel lighting operation and  maintenance  from  passive  repair  to  active  prevention-this  closed-loop  workflow  and  engineeringoriented system development break through the limitation that existing BO-XGBoost applications only stay in  the  theoretical  prediction  stage.  Validation  using  field  data  from  the  Caoguo  Mountain  Tunnel  confirms the feasibility and engineering value of the proposed framework, providing a new technical approach for the intelligent risk management of tunnel lighting infrastructure.

## Improved XGBoost algorithm theoretical model XGBoost algorithm

XGBoost is an enhanced algorithm built on gradient-boosted decision trees, enabling efficient construction of boosted trees through parallel execution. It employs two types of boosted trees: regression trees and classification trees 19 . The optimization of the objective function value forms the core mechanism of XGBoost, as illustrated by the theoretical elaboration of this objective function below.

XGBoost model formula:

<!-- formula-not-decoded -->

Where, ˆ y i is the predicted value of the ith sample, x i is the feature vector of the ith sample, and f k is the decision tree.

XGBoost objective function (loss function):

<!-- formula-not-decoded -->

Where,  Obj  is  the  objective  function,  the  first  term ∑ n i =1 L ( y i , ˆ y i ) is  the  traditional  loss  function,  which measures the model's fit to the data; the second term ∑ K k =1 Ω( f k ) is the regularization term, which is used to control the complexity of the model and prevent overfitting. Ω( f k ) represents the complexity of the kth basis learner.

The objective function after Taylor expansion to the second order:

After  performing  a  second-order  Taylor  expansion  of  the  loss  function,  the  objective  function  can  be expressed as:

<!-- formula-not-decoded -->

Where, Obj ( t ) represents the objective function at the tth iteration. g i represents the first derivative of the loss function at ˆ y ( t - 1) i . h i represents the second derivative of the loss function at y ( t - 1) i . f t represents the tth base learner (decision tree).

Regularization definition of decision tree complexity:

<!-- formula-not-decoded -->

Where, Ω( f ) is the complexity of the decision tree f t , T is the number of leaf nodes in the tree w 2 j , is the weight of the jth leaf node, γ and λ are regularization coefficients used to control the number of leaf nodes and the regularization strength of the leaf node weights.

Formula for solving the optimal leaf node weight:

Given the sample I j set of leaf node j, the optimal leaf node weight w ∗ j can be obtained by solving the following equation:

<!-- formula-not-decoded -->

3

Where, w ∗ j is the optimal weight of leaf node j, I j is the set of all samples assigned to leaf node j, g i is the first-order derivative of the loss function with respect to the current predicted value on sample i, h i is  the  second-order derivative of the loss function with respect to the current predicted value on sample i, λ and is the parameter of the regularization term, which is used to control the complexity of the model and prevent overfitting.

## BO of model hyperparameters

Given  that  the  performance  of  XGBoost  models  in  tunnel  lighting  risk  assessment  critically  depends  on hyperparameter configuration, and considering the limitations of traditional optimization methods-such as inefficient  exploration  of  high-dimensional  spaces  and  excessive  consumption  of  computational  resourcesthis  study  introduces  Bayesian  Optimization  (BO)  for  efficient  hyperparameter  autotuning.  BO  addresses the  challenges  of  model  training  with  large-scale  tunnel  monitoring  datasets  by  constructing  a  probabilistic surrogate  model  of  the  objective  function.  This  surrogate  model  the  black-box  relationship  between hyperparameters and the model's generalization performance, employing an acquisition function to balance exploration  and  exploitation  throughout  the  sequential  optimization  process 20,21 .  The  global  optimization capability  and  uncertainty  quantification  inherent  in  BO  significantly  enhance  the  model's  robustness  and predictive confidence in tunnel lighting risk assessment. This advancement provides a theoretical foundation for the precise identification of complex risk factors. The hyperparameter optimization objective utilizing the Bayesian algorithm is presented in Eq. (6):

<!-- formula-not-decoded -->

Where, θ represents  the  hyperparameter vector of the XGBoost model, i.e., the key parameter combination that  controls  the  performance  of  the  risk  prediction  model;  Θ  represents  the  hyperparameter  search  space; M XGB ( θ ) represents the XGBoost model trained with hyperparameter θ, i.e., the tunnel lighting risk prediction model; ν represents the validation dataset, i.e., historical data on tunnel lighting facilities; L represents the model loss  function; θ ∗ represents  the  optimal  hyperparameter  combination, i.e.,  the  parameter  configuration  that maximizes the accuracy of tunnel risk prediction.

The Gaussian process proxy model is shown in Eqs. (7) and (8):

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

Where, f ( θ ) represents the objective function mapping; GP represents Gaussian process, which is a probabilistic model of  the  unknown  loss  function; m ( θ ) represents  the  mean  function; k ( θ, θ ′ ) represents  the  covariance function; l represents the length scale parameter.

The expected improvement in the collection function is shown in Eqs. (9) and (10):

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

Where, EI represents the expected value function; f min represents the current minimum loss value; E represents the mathematical expectation, i.e., the probability average based on the Gaussian process posterior; θ t represents the hyperparameters evaluated at step t; t represents the number of optimization iterations.

## Building and training the evaluation model Selection and scoring of evaluation indicators

To  construct  a  scientific  and  reasonable  risk  assessment  indicator  system  for  tunnel  lighting  facilities,  an initial candidate pool of 22 indicators was first established by synthesizing relevant national standards, on-site operation and maintenance investigation data of tunnel lighting, existing literature, and two rounds of expert consultation  involving  tunnel  engineering  designers,  on-site  managers,  and  academic  researchers,  covering environmental parameters, electrical safety, structural status, and equipment aging characteristics. A two-step quantitative screening process was then carried out to optimize the indicators: the primary screening eliminated indicators that are difficult to collect in actual engineering or have low sensitivity to risk changes, retaining 17 indicators; the secondary screening adopted Pearson correlation analysis and variance inflation factor (VIF) test to remove indicators with high collinearity and information redundancy, finally determining 12 independent and representative indicators. These 12 indicators fully cover the core dimensions of tunnel lighting risk, without missing key risk factors, which are sufficient to characterize the overall risk state of lighting facilities. The VIF values of the final 12 indicators range from 1.16 to 1.67, far lower than the critical threshold of 10, indicating no  significant  multi-collinearity  between  indicators.  The  detailed  indicator  screening  process,  correlation coefficients, and VIF values are shown in Tables 1 and 2, providing sufficient data support for the rationality and scientificity of the indicator system.

These  twelve  risk  assessment  indicators  are  as  follows:  illuminance,  water  accumulation  status  of electromagnetic  contactors,  tunnel  temperature,  voltage  stability,  relative  humidity,  presence  of  pole  cracks, tunnel wind speed, operational days of luminaires, count of damaged luminaires, line corrosion status, integrity of  luminaire casings, and operational hours of light sources. These indicators collectively encompass critical aspects of lighting system safety, providing a comprehensive characterization of health status and risks.

Table 1 .  Indicator screening process.

| Screening stage              | Treatment                                                       |   Number of indicators |
|------------------------------|-----------------------------------------------------------------|------------------------|
| Initial candidate indicators | Standards, investigation, literature, expert consultation       |                     22 |
| Primary screening            | Remove unmeasurable and low-sensitivity indicators              |                     17 |
| Secondary screening          | Remove high-collinearity indicators by correlation and VIF test |                     12 |

Table 2 .  VIF values of the 12 final indicators.

| Indicator                      |   VIF value |
|--------------------------------|-------------|
| Illuminance                    |        1.42 |
| Contactor water accumulation   |        1.16 |
| Tunnel temperature             |        1.67 |
| Voltage stability              |        1.50 |
| Relative humidity              |        1.61 |
| Pole cracks                    |        1.18 |
| Tunnel wind speed              |        1.22 |
| Operational days of luminaires |        1.36 |
| Count of damaged luminaires    |        1.33 |
| Line corrosion status          |        1.19 |
| Luminaire casing integrity     |        1.21 |
| Light source operational hours |        1.34 |

For continuous indicators including illuminance, tunnel temperature, relative humidity, light source working time, tunnel wind speed, luminaire running time, and number of damaged fixtures, the illuminance thresholds are  primarily  anchored  by JTG/T  D70/2 - 01 - 2014  Specifications  for  Design  of  Highway  Tunnel  Lighting ,  the mandatory industry standard for highway tunnel lighting in China, and CIE 88:2004 Guide for the Lighting of Road Tunnels and Underpasses , the globally authoritative guideline for tunnel lighting issued by the International Commission on Illumination, with the 5-level intervals calibrated to correspond to the compliance with design specifications from Level 1 to Level 5. The thresholds for tunnel temperature and relative humidity are formulated based on JTG H12 - 2015 Technical Specifications for Maintenance of Highway Tunnels , combined with the GB/T 2423 series environmental test standards for electrical and electronic products , and further calibrated using longterm operation data and failure statistics of lighting facilities from the Caoguo Mountain Tunnel and 6 similar highway tunnels, quantifying the correlation between environmental parameters and equipment aging/failure risks. The thresholds for light source working time, luminaire running time, and number of damaged fixtures are based on GB/T 7000.1-2015 Luminaires - Part 1: General Requirements and Tests , combined with the official lifespan  curves  provided by luminaire manufacturers and 3-year maintenance failure records of the project, to  quantify  the  corresponding  relationship  between  equipment  aging  degree  and  loss  risk.  The  tunnel  wind speed threshold is formulated in accordance with the operational safety requirements specified in JTG H12 - 2015 , combined with the tunnel ventilation design specifications, to clarify the impact of different wind speeds on facility safety and maintenance operations.

For binary indicators including whether the electromagnetic contactor is waterlogged, whether the voltage is stable, whether the pole has cracks, whether the line is corroded, and whether the lamp body is damaged, the threshold division is anchored by JTG H12 - 2015 Technical Specifications for Maintenance of Highway Tunnels , GB  50,054 - 2011  Code  for  Design  of  Low  Voltage  Distribution  Systems ,  and GB  50,168 - 2018  Standard  for Construction and Acceptance of Cable Lines in Electrical Installation  Engineering .  The  'normal  (No)'  state  is classified into low loss levels (1-3) as it indicates no immediate fault hazard, while the 'abnormal (Yes)' state is classified into high loss levels (4-5) as it represents direct potential safety hazards such as short circuit and structural damage that may trigger accidents. The voltage stability threshold is strictly formulated in accordance with GB/T 19862 - 2018 Power Quality - General Requirements for Power Quality Monitoring Equipment and GB/T 14549 - 1993  Power  Quality - Harmonics in Public  Supply  Networks ,  clarifying  the  risk  levels  corresponding  to voltage fluctuation and instability.

To further ensure the rationality of the thresholds, we conducted a two-round Delphi expert consultation with 9 senior experts in the fields of highway tunnel design, operation and maintenance, and electrical safety, including 3 professor-level senior engineers, 3 university professors, and 3 technical directors of tunnel operation units. All thresholds were iteratively revised based on expert opinions, and finally verified by retrospective analysis of 3-year operation failure data of the Caoguo Mountain Tunnel, with a matching rate of over 92% between the threshold division and actual fault occurrence, fully proving the scientificity and practicability of the scoring system. We have supplemented the detailed threshold formulation process, standard basis, expert consultation results, and engineering verification data in the revised manuscript, and added a special supplementary table to clarify the corresponding basis for each indicator's threshold, providing sufficient traceable evidence for the rationality of the scoring system (Table 3).

Table 3 .  Details of threshold basis for each indicator in Table 1.

| Indicator type        | Indicator name                | Core basis                                                                                                                                                                                                                                                            |
|-----------------------|-------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Continuous Indicators | Illuminance (lx)              | JTG/T D70/2 - 01 - 2014 Specifications for Design of Highway Tunnel Lighting , CIE 88:2004 Guide for the Lighting of Road Tunnels and Underpasses , statistical data of tunnel traffic accident rate                                                                  |
| Continuous Indicators | Tunnel temperature ( ℃ )      | JTG H12 - 2015 Technical Specifications for Maintenance of Highway Tunnels , GB/T 2423.2-2008 Environmental Testing for Electric and Electronic Products - Part 2: Test Methods - Test B: Dry Heat , measured service life data of lighting equipment                 |
| Continuous Indicators | Relative humidity (RH%)       | JTG H12 - 2015 Technical Specifications for Maintenance of Highway Tunnels , GB/T 2423.3-2016 Environmental Testing for Electric and Electronic Products - Part 2: Test Methods - Test Cab: Damp Heat , Steady State , statistical data of electrical component aging |
| Continuous Indicators | Light source working time (%) | GB/T 7000.1-2015 Luminaires - Part 1: General Requirements and Tests , service life curves provided by luminaire manufacturers , operation and maintenance fault records                                                                                              |
| Continuous Indicators | Tunnel wind speed (m/s)       | JTG H12 - 2015 Technical Specifications for Maintenance of Highway Tunnels , specifications for tunnel ventilation design , requirements for safe operation and maintenance                                                                                           |
| Continuous Indicators | Luminaire operating days (d)  | GB/T 7000.1-2015 Luminaires - Part 1: General Requirements and Tests , service life curves provided by luminaire manufacturers , statistics of operation and maintenance cycles                                                                                       |
| Continuous Indicators | Number of damaged luminaires  | JTG H12 - 2015 Technical Specifications for Maintenance of Highway Tunnels , statistical data of operation and maintenance faults , expert consensus                                                                                                                  |
| Binary Indicators     | Contactor waterlogging status | JTG H12 - 2015 Technical Specifications for Maintenance of Highway Tunnels , GB 50,054 - 2011 Code for Design of Low Voltage Distribution Systems , statistics of tunnel electrical faults                                                                            |
| Binary Indicators     | Voltage stability             | GB/T 19,862 - 2018 Power Quality - General Requirements for Power Quality Monitoring Equipment , GB/T 14,549 - 1993 Power Quality - Harmonics in Public Supply Networks , power distribution safety specifications                                                    |
| Binary Indicators     | Pole cracks                   | JTG H12 - 2015 Technical Specifications for Maintenance of Highway Tunnels , GB 50,168 - 2018 Standard for Construction and Acceptance of Cable Lines in Electrical Installation Engineering , structural safety inspection data                                      |
| Binary Indicators     | Line corrosion                | GB 50,168 - 2018 Standard for Construction and Acceptance of Cable Lines in Electrical Installation Engineering , GB/T 50,217 - 2018 Code for Design of Electric Power Cable Engineering , statistics of cable faults                                                 |
| Binary Indicators     | Luminaire casing damage       | GB/T 7000.1-2015 Luminaires - Part 1: General Requirements and Tests , JTG H12 - 2015 Technical Specifications for Maintenance of Highway Tunnels , operation and maintenance inspection records                                                                      |

Table 4 .  Scoring criteria for tunnel lighting facilities.

| a. Scoring results ①   | a. Scoring results ①             | a. Scoring results ①                                 | a. Scoring results ①          | a. Scoring results ①                 | a. Scoring results ①         | a. Scoring results ①             |
|------------------------|----------------------------------|------------------------------------------------------|-------------------------------|--------------------------------------|------------------------------|----------------------------------|
| Loss value             | Illuminance (lx)                 | Whether the electromagnetic contactor is waterlogged | Tunnel temperature (°C)       | Whether the voltage is stable or not | Relative humidity (RH%)      | Whether the pole has cracks      |
| 1                      | (5,6)                            | No                                                   | (15,19)                       | No                                   | (50,60)                      | No                               |
| 2                      | (4.5,5)                          | No                                                   | (19,23)                       | No                                   | (60,70)                      | No                               |
| 3                      | (4,4.5)                          | Yes                                                  | (23,27)                       | Yes                                  | (70,80)                      | Yes                              |
| 4                      | (3.5,4)                          | Yes                                                  | (27,31)                       | Yes                                  | (80,90)                      | Yes                              |
| 5                      | (3,3.5)                          | Yes                                                  | (31,35)                       | Yes                                  | (90,100)                     | Yes                              |
| b. Scoring results ②   | b. Scoring results ②             | b. Scoring results ②                                 | b. Scoring results ②          | b. Scoring results ②                 | b. Scoring results ②         | b. Scoring results ②             |
| Loss value             | Working time of light source (%) | Tunnel wind speed (m/s)                              | Luminaire running time (days) | Number of damaged fixtures           | Whether the line is corroded | Whether the lamp body is damaged |
| 1                      | (10,20)                          | (4,5.2)                                              | (0,10)                        | (0,1)                                | No                           | No                               |
| 2                      | (20,30)                          | (5.2,6.4)                                            | (10,20)                       | (1,2)                                | No                           | No                               |
| 3                      | (30,40)                          | (6.4,7.6)                                            | (20,30)                       | (2,3)                                | Yes                          | Yes                              |
| 4                      | (40,50)                          | (7.6,8.8)                                            | (30,40)                       | (3,4)                                | Yes                          | Yes                              |
| 5                      | (50,60)                          | (8.8,10)                                             | (40,50)                       | (4,5)                                | Yes                          | Yes                              |

A quantitative scoring framework was implemented for model development, with detailed criteria provided in Table 4.

As shown in Table 5, the 'Loss Value' (Loss Level 1-5) in this study is strictly defined as a comprehensive risk  classification  that  quantifies  the  overall  safety  state  of  tunnel  lighting  facilities,  which  is  determined by  the  coupling  of  the  failure  probability  and  consequence  severity  of  the  facilities,  and  is  closely  linked  to maintenance urgency. Specifically, Level 1 (Low Risk) corresponds to the optimal operation state with extremely low failure probability, no adverse consequences, and only routine inspection required; Levels 2-3 (Medium Risk) represent the sub-healthy and warning states where facility performance deviates from the optimal range, failure probability gradually increases, consequences are mild to limited, and moderate to prompt maintenance is needed to prevent risk escalation; Levels 4-5 (High Risk) correspond to the severe risk and extreme risk states where facility performance is far below the safety threshold, failure probability is extremely high, consequences are  significant  to  catastrophic  (e.g.,  short  circuits,  structural  damage  that  may  lead  to  traffic  accidents),  and emergency maintenance or immediate replacement is imperative.

Table 5 .  Definition and engineering connotation of loss value.

|   Loss level | Definition of risk state   | Corresponding failure probability   | Consequence severity   | Maintenance urgency   | Engineering description                                                                          |
|--------------|----------------------------|-------------------------------------|------------------------|-----------------------|--------------------------------------------------------------------------------------------------|
|            1 | Optimal state              | < 5%                                | No consequence         | Routine inspection    | Fully meets design specifications, no failure risk, only regular maintenance required            |
|            2 | Sub-healthy state          | 5-15%                               | Mild impact            | Moderate maintenance  | Slight performance degradation, low failure risk, targeted inspection needed                     |
|            3 | Warning state              | 15-30%                              | Limited hazard         | Prompt maintenance    | Obvious performance deviation, increasing failure risk, need for scheduled maintenance           |
|            4 | Severe risk state          | 30-50%                              | Significant hazard     | Emergency maintenance | Near-failure state, high failure risk, may cause property loss, urgent repair needed             |
|            5 | Extreme risk state         | > 50%                               | Catastrophic hazard    | Immediate replacement | Severe failure or accident hazard, may lead to traffic accidents, immediate replacement required |

Fig. 1 .  Training data processing.

<!-- image -->

Flow chart

## Processing of training data

In practical applications of XGBoost hyperparameter optimization algorithms, data preprocessing represents a  critical  performance-enhancing  phase 22 .  As  shown  in  Fig.  1,  the  initial  modeling  dataset  integrates  raw tunnel  monitoring  data  (accounting  for  75%)  with  dynamically  generated  supplementary  data  that  reflects the engineering characteristics of the Caoguo Mountain Tunnel. This data fusion strategy addresses gaps in the  completeness  of  risk  probability  distributions  for  lighting  facilities-particularly  the  scarcity  of  data  on extreme operating conditions and edge scenarios-thereby ensuring comprehensive multi-risk coverage for the classification model. Following the assurance of data completeness, enhancing training precision emerged as a paramount priority, given that sample size directly influences predictive accuracy. Leveraging the computational environment of PyCharm Community Edition, this study expanded the original dataset using the 3σ criterion. During  model  training,  randomized  reshuffling  of  the  dataset  was  implemented  through  custom  coding  to enhance training robustness. Finally, 80% of the total dataset was allocated to the training set.

All supplementary data were reviewed and confirmed by senior tunnel operation and maintenance engineers to  ensure  full  consistency  with  real  engineering  characteristics  and  avoid  introducing  unrealistic  bias.  To verify the validity of the data fusion strategy, a controlled experiment was conducted to compare the model performance between the raw monitoring data and the fused dataset. The results indicate that the fused dataset effectively improves the overall prediction accuracy and the prediction accuracy of high-risk samples (Level 4-5), while reducing prediction fluctuation. The detailed statistical parameters for generating supplementary data and the specific model performance comparison results between different datasets are presented in Tables 6 and 7, providing sufficient traceable evidence for the rationality and effectiveness of the data fusion design.

The 3σ criterion specific application includes two standardized steps: first, the 3σ criterion was adopted to identify  and eliminate invalid abnormal outliers in the raw monitoring data, ensuring the basic quality and reliability of the dataset; second, combined with the normality test results of the original data, the 3σ statistical interval  was  used  as  the  reasonable  boundary  for  data  enhancement,  preventing  the  expanded  data  from exceeding the actual engineering operation range. To strictly verify the precondition of the 3σ method, As shown in Tables 8, 9 and 10, before applying the 3σ criterion, the Kolmogorov-Smirnov (K-S) test was conducted on all continuous monitoring indicators, and the results showed that the p values of all indicators were greater than 0.05, which fully validates that the raw data satisfies the normal distribution assumption required for 3σ-based

7

Table 6 .  Statistical parameters for generating supplementary data.

| Indicator                |   Mean of raw data |   Standard deviation | 3σ reasonable interval   | Supplementary data coverage scenario   |
|--------------------------|--------------------|----------------------|--------------------------|----------------------------------------|
| Illuminance (lx)         |               4.72 |                 0.86 | 2.14-7.30                | Ultra-low illuminance (< 3.0 lx)       |
| Relative humidity (%)    |               72.3 |                 12.1 | 36.0-108.6               | High humidity (> 90%)                  |
| Tunnel temperature ( ℃ ) |               25.6 |                  4.2 | 13.0-38.2                | Extreme high/low temperature           |
| Lamp runtime (d)         |                2.1 |                  1.3 | 0-6.0                    | Long-term continuous operation         |
| Number of damaged lamps  |                3.8 |                  2.5 | 0-11.3                   | Large-scale lamp damage                |

Table 7 .  Model performance comparison between raw data and fused data.

| Dataset type                     |   Overall accuracy (%) |   High-risk sample (level 4-5) accuracy (%) | Prediction fluctuation (%)   |
|----------------------------------|------------------------|---------------------------------------------|------------------------------|
| Only raw monitoring data         |                   83.5 |                                        75.2 | ± 2.7                        |
| Fused data (raw + supplementary) |                   91.8 |                                        90.1 | ± 0.9                        |

Table 8 .  Normality test results of raw monitoring indicators (K-S test).

| Indicator                |   p value | Normality test result                      |
|--------------------------|-----------|--------------------------------------------|
| Illuminance (lx)         |     0.126 | Conform to normal distribution ( p > 0.05) |
| Tunnel temperature ( ℃ ) |     0.183 | Conform to normal distribution ( p > 0.05) |
| Relative humidity (%)    |     0.157 | Conform to normal distribution ( p > 0.05) |
| Tunnel wind speed (m/s)  |     0.112 | Conform to normal distribution ( p > 0.05) |
| Lamp runtime (d)         |     0.149 | Conform to normal distribution ( p > 0.05) |

Table 9 .  3σ interval and variable engineering dependence relationship.

| Indicator         | 3σ reasonable interval   | Core engineering dependence relationship          |
|-------------------|--------------------------|---------------------------------------------------|
| Illuminance       | 2.14-7.30 lx             | Negatively correlated with relative humidity      |
| Temperature       | 13.0-38.2 ℃              | Positively correlated with equipment aging rate   |
| Relative humidity | 36.0-108.6%              | Positively correlated with circuit corrosion risk |
| Wind speed        | 0-10.0 m/s               | Negatively correlated with lighting stability     |

Table 10 .  Data consistency test before and after enhancement.

| Dataset                      | Mean value deviation   | Correlation coefficient retention rate   |   Model accuracy change (%) |
|------------------------------|------------------------|------------------------------------------|-----------------------------|
| Raw data                     | -                      | -                                        |                        83.5 |
| Enhanced data (3σ criterion) | < 2.1%                 | 97.8%                                    |                        91.8 |

statistical  expansion.  More  importantly,  in  the  data  enhancement  process,  it  retained  the  real  engineering coupling relationships between variables based on the physical characteristics of tunnel lighting systems (e.g., the negative correlation between illuminance and relative humidity, the positive correlation between temperature and equipment aging rate), ensuring that all expanded samples conform to actual operation laws rather than being generated randomly. Such a constrained generation mechanism guarantees the preservation of real-world variable correlations in the augmented dataset. A consistency test was further performed before and after data enhancement, and the results confirmed that the mean value deviation of the dataset was less than 2.1%, the correlation coefficient retention rate reached 97.8%, and the model accuracy was improved without damaging the authenticity of the original data (Table 10).

## Model training based on the XGBoost algorithm

To facilitate subsequent software development and application, this study implemented XGBoost model training in the PyCharm Community Edition environment. Key model parameters are specified in Table 11. Two critical hyperparameters-maximum tree depth and minimum child weight-were prioritized for optimization. The maximum tree depth governs the model's capacity to capture feature complexity and interaction depth 23 , while the minimum child weight regulates split conservatism to balance the model's expressiveness and resistance to overfitting. A fixed random seed (42) was set for all data splitting, model initialization, and optimization processes to ensure experimental reproducibility.

Table 11 .  Model training parameters.

| Parameters                        | Parameters                |
|-----------------------------------|---------------------------|
| Model type selector               | Maximum depth of the tree |
| Minimum weight sum of child nodes | Feature sampling rate     |
| Loss function objective           | Learning rate             |
| Sample sampling rate              | Sample sampling rate      |

Table 12 .  XGBoost fixed parameters and hyperparameter search range.

| Parameter type            | Parameter name                    | Value/search range                      |
|---------------------------|-----------------------------------|-----------------------------------------|
| Fixed parameters          | Model type selector               | XGBClassifier                           |
| Fixed parameters          | Loss function objective           | Multi: softmax (5-class classification) |
| Fixed parameters          | Learning rate                     | 0.1                                     |
| Fixed parameters          | Feature sampling rate             | 0.8                                     |
| Fixed parameters          | Sample sampling rate              | 0.8                                     |
| Fixed parameters          | Random seed                       | 42                                      |
| Optimized hyperparameters | Maximum depth of the tree         | 3-10                                    |
| Optimized hyperparameters | Minimum weight sum of child nodes | 1-10                                    |
| Optimization settings     | Validation strategy               | 5-fold cross-validation                 |
| Optimization settings     | Early stopping patience           | 10 iterations                           |
| Optimization settings     | Model selection criterion         | Highest cross-validation accuracy       |

Fig. 2 .  Confusion matrix example.

<!-- image -->

Bar chart

As shown in Table 12, the hyperparameter search range was set as: maximum tree depth (3-10), minimum child  weight  (1-10).  5-fold  cross-validation  was  adopted  as  the  optimization  validation  strategy  to  evaluate hyperparameter performance and prevent overfitting. An early stopping criterion was applied: the optimization process  terminated  automatically  when  the  cross-validation  accuracy  did  not  improve  for  10  consecutive iterations. The final optimal hyperparameters were selected based on the highest 5-fold cross-validation accuracy.

Following parameter tuning, model training was executed. A confusion matrix (Fig. 2) was introduced at this stage to evaluate training performance. Analyzing the row and column distributions within the matrix provides explicit insights into predictive accuracy. Within the structure of the confusion matrix, each row corresponds to the true class of instances, while each column represents the predicted class. The value in each cell indicates the total count of samples for that specific classification. As illustrated in Fig. 2, the value 9 at row 1, column 1 indicates that nine samples from true class 1 were correctly predicted as class (1) Conversely, the value 1 at row 1, column 2 signifies that one sample from true class 1 was misclassified as class (2) Row-wise and column-wise accuracy and error rates provide an intuitive visualization of prediction outcomes. In addition to confusion matrix analysis, accuracy metrics were employed to quantitatively evaluate the quality of model construction.

## Development of a risk assessment system for tunnel lighting facilities

To transform the theoretical risk assessment model into an engineering-applicable tool and provide a practical, efficient  platform  for  tunnel  lighting  risk  management,  this  study  developed  an  Intelligent  Risk  Assessment System for  Tunnel  Lighting  Facilities  based  on  the  proposed  BO-XGBoost  model.  The  system  is  developed with lightweight programming frameworks, featuring easy deployment, low operation costs, and user-friendly interaction. It can be directly applied to actual tunnel O&amp;M scenarios, providing strong technical support for the intelligent transformation of lighting facility management.

## System architecture framework

The  architecture  of  the  Bayesian-optimized  XGBoost  risk  assessment  system  for  tunnel  lighting  facilities comprises five layers 24 :  the foundational framework layer, data acquisition layer, data analysis and processing layer, visualization and interaction layer, and application layer, as illustrated in Fig. 3.

As illustrated in the figure above:

1.  Foundational Framework Layer: This layer provides the development environment and supporting dependencies for data processing within the tunnel lighting facility risk assessment system.
2.  Data Acquisition Layer: This layer supplies original multi-source data for subsequent analysis and processing, encompassing real-time operational status data and long-term accumulated degradation data.
3.  Data Analysis &amp; Processing Layer: This layer preprocesses the original multi-source tunnel lighting facility data and utilizes the proposed algorithms and models to provide technical support for the functionalities of the interaction layer.
4.  Visualization &amp; Interaction Layer: This layer offers users comprehensive risk assessment functionalities, visually outputs risk assessment levels, and enables parameter configuration based on practical requirements.
5.  Application Layer: This layer allows users to perform file management and storage configuration for saving assessment results.

## System construction

The system adopts a lightweight three-tier Client-Backend-Database architecture, which realizes the decoupling of  interaction,  computing 25-27 ,  and  data  management  with  high  stability  and  compatibility.  The  system  has excellent engineering-oriented performance: the average risk assessment response time is less than 1 s, meeting the real-time monitoring requirements of tunnel operation; it supports deployment on conventional industrial computers and embedded terminals, with low hardware costs; it can run continuously and stably for a long time, adapting to the all-weather operation characteristics of highway tunnels. The human-computer interaction interface is concise and intuitive (Figs. 4, 5), users can input field operation parameters through a selectionbased mechanism, and one-click risk assessment can be realized after data input.

## Embedded application scheme of the assessment model in the O&amp;M system

This subsection clarifies the one-to-one mapping and tight coupling relationship between the proposed risk assessment model and the subsequent intelligent O&amp;M system, forming a progressive logical link from theoretical model to engineering implementation. The three-tier architecture of the system is completely matched with the core content of the assessment model, with the corresponding relationship as follows:

The data acquisition layer of the system is the data input port of the whole assessment system, which is fully compatible with the 12 core risk indicators constructed in this study. The layer supports data acquisition from tunnel environmental sensors, lighting equipment operation monitoring terminals, and electrical parameter detection devices, as well as manual entry of periodic inspection data. This ensures that the data input of the system is completely consistent with the training data of the assessment model, guaranteeing the reliability of the assessment results.

The algorithm calculation layer is the core functional layer of the system, which is completely embedded with the BO-optimized XGBoost model trained and validated in this study. The layer encapsulates the optimized model parameters, and supports two working modes: (1) real-time dynamic assessment: inputting the real-time operation data of lighting facilities to output the failure risk probability of the equipment within 72 h; (2) batch offline assessment: importing the periodic inspection data of the whole tunnel lighting system to complete the batch risk assessment of all equipment, and generate a risk ranking list.

Fig. 3 .  Architecture of the lighting facility risk assessment system.

<!-- image -->

Flow chart

Fig. 4 .  login screen.

<!-- image -->

Screenshot from computer

Fig. 5 .  System interface.

<!-- image -->

Screenshot from computer

The decision output layer is the result output and application terminal of the system, which strictly follows the risk level classification standard formulated in the model validation process. The layer divides the assessment results into five risk levels. For different risk levels, the layer outputs corresponding decision suggestions: for lowrisk equipment, it gives regular inspection suggestions; for medium and high-risk equipment, it gives priority inspection and maintenance suggestions; for critical risk equipment, it triggers an immediate early warning, and pushes the equipment location, risk factors, and emergency disposal suggestions to the on-site O&amp;M personnel via the system terminal. This layer realizes the closed loop from risk assessment to decision-making disposal, which  is  the  practical  value  realization  of  the  assessment  model.Through  the  above  three-tier  architecture design, the system realizes the full embedding and full-chain application of the proposed risk assessment model.

## Engineering application and verification Project overview

A highway tunnel located in Jinping County, Honghe Prefecture, operates under complex environmental and operational  conditions.  Field  observations  reveal  persistent  high  humidity,  frequent  rainfall,  and  unstable voltage supply within the tunnel. The lighting systems are subjected to extended daily operation, exceeding 12 h of continuous use. Key environmental and operational parameters include voltage fluctuations of ± 15% and ambient humidity levels consistently exceeding 85%. These harsh conditions have led to accelerated degradation of critical components in the lighting systems: LED chips exhibit premature aging, electromagnetic contacts show signs of oxidation and corrosion, and capacitors within the power supply units are observed to bulge-all of which pose significant risks to the reliability and safety of the lighting infrastructure.

Figure 6 shows these cumulative failures have caused tunnel illumination to drop by 30% below the design standards, directly endangering nighttime operational safety. Currently, fault detection relies entirely on manual inspections, leading to significant operational inefficiencies: annual unplanned outages reach 12 incidents, repair responses are delayed with an average resolution time exceeding 24 h, and maintenance costs surpass budget allocations by 35%. Notably, critical risk factors such as real-time equipment status and environmental data lack systematic collection and analysis. This deficiency perpetuates a repetitive 'failure → repair → recurrence of failure' cycle, highlighting the urgent need for a data-driven risk assessment system to break this reactive maintenance pattern.

The  proposed  BO-XGBoost  model  integrates  12  critical  risk  indicators,  encompassing  equipment  status parameters  (e.g.,  illuminance,  waterproofing  performance),  environmental  data  (e.g.,  temperature,  voltage stability), and operational metrics (e.g., daily runtime). Through algorithmic optimization, the model achieves reduced computational complexity while enabling real-time risk prediction and rapid iterative updates. These enhancements collectively  improve  maintenance  efficiency  in  complex  tunnel  environments,  addressing  the limitations of traditional reactive maintenance approaches.

Fig. 6 .  Tunnel lighting aging and circuit short circuits.

<!-- image -->

Photograph

## Quantification of evaluation indicators

The  model  was  trained  using  241  data  groups  collected  in  a  continuous  time  sequence,  which  record  the dynamic changes of tunnel lighting environment and equipment operating status, of which 192 groups (80%) were allocated to the training set and 49 groups (20%) to the test set. Loss risk values were assigned based on expert experience, with partial results of this assignment presented in Table 13.

Which is relatively limited for developing and validating a risk prediction model intended for engineering deployment.  This  limitation  arises  primarily  from  constraints  in  on-site  data  acquisition  of  tunnel  lighting facilities.  To  mitigate  its  impact,  we  adopted  rigorous  strategies  including  stratified  sampling,  5-fold  crossvalidation, and data enhancement within the 3σ interval.

The statistical results show that the sample distribution across risk levels is relatively balanced. Specifically, Risk Level 1 has 76 samples (31.5%), Level 2 has 68 samples (28.2%), Level 3 has 45 samples (18.7%), Level 4 has 32 samples (13.3%), and Level 5 has 20 samples (8.3%). The training set (192 samples) and test set (49 samples) maintain the same risk level distribution through stratified sampling, ensuring the representativeness of both sets.

To verify the dynamic assessment capability of the proposed model, we divided the 241 sequential data groups into six consecutive time periods in accordance with the data collection timeline, and performed incremental model training and validation by sequentially inputting data of each period to simulate the real-time data stream in actual tunnel operation. The incremental dynamic validation results show that the model maintains stable prediction accuracy and low computational latency across different time periods: the prediction accuracy ranges from 89.2% to 92.1%, and the average computational latency is stably maintained between 0.42 s and 0.46 s. The specific indicators of dynamic validation, including the data volume, prediction accuracy, and average latency of each time period, are listed in Table 14.

Table 15 clearly  presents  the  dynamic  validation  indicators  of  the  six  consecutive  time  periods:  the  data volume of each period is between 39 and 41 groups, showing good consistency with the actual monitoring data frequency; the prediction accuracy of each period is maintained above 89%, among which Period 1 achieves the highest accuracy of 92.1%, and even in the later periods, the accuracy remains above 89.2%, reflecting the model's stable performance in continuous data input scenarios; the average latency of each period is between 0.42 s and 0.46 s, with small fluctuations.

## Model training based on the XGBoost algorithm

To  clarify  the  selection  of  the  loss  function  and  the  logical  link  between  model  output  and  discrete  risk classification, this study adopts a 'regression prediction+discrete mapping' framework instead of direct multiclass classification, which is more consistent with the engineering practice of tunnel lighting risk assessment. The loss function reg: squarederror is selected because tunnel lighting risk changes continuously and gradually rather than being rigidly separated into discrete categories; constructing a regression model with this loss function enables  the  model  to  output  a  continuous  risk  score,  which  can  sensitively  capture  subtle  variations  in  risk levels. Based on industry standards, on-site fault statistics, and expert consensus, clear quantitative thresholds are formulated to map the continuous risk score into 5 discrete risk levels (Level 1 to Level 5), balancing the continuity of risk evolution and the interpretability of engineering risk management. The specific mapping rules between continuous risk scores and discrete risk levels are detailed in Table 16.

To  fully  verify  the  advantages  of  the  regression-mapping  strategy  over  direct  multi-class  classification,  a controlled comparative experiment was supplemented under completely identical experimental conditions. The direct classification model (XGBoost with multi: softmax loss function) was constructed, which shares the same model framework, dataset, feature system, and Bayesian hyperparameter optimization strategy as the proposed regression-mapping model. The only difference is that the direct classification model directly outputs discrete risk  level  labels,  while  the  proposed  model  outputs  continuous  risk  scores  and  completes  level  mapping  via standardized thresholds.

Table 13 .  Partial tunnel lighting environment monitoring and equipment operating status variables.

| a. Data ①   | a. Data ①               | a. Data ①             | a. Data ①                | a. Data ①               | a. Data ①               | a. Data ①           | a. Data ①                     |
|-------------|-------------------------|-----------------------|--------------------------|-------------------------|-------------------------|---------------------|-------------------------------|
| Groups      | Illumination (lx)       | Contactor waterlogged | Tunnel temperature ( ℃ ) | Voltage stability       | Relative humidity (RH%) | Cracked light poles | Light source working time (%) |
| 1           | 4.85                    | 1                     | 28.6                     | 0                       | 79.6                    | 0                   | 6.34                          |
| 2           | 5.24                    | 0                     | 21.9                     | 1                       | 51.3                    | 1                   | 8.65                          |
| 3           | 5.12                    | 0                     | 22.2                     | 1                       | 65.4                    | 0                   | 7.87                          |
| 4           | 3.21                    | 1                     | 30.2                     | 0                       | 89.1                    | 1                   | 4.93                          |
| 5           | 4.24                    | 0                     | 20.4                     | 0                       | 50.6                    | 0                   | 8.15                          |
| 6           | 4.53                    | 1                     | 20.1                     | 1                       | 63.2                    | 0                   | 7.88                          |
| 7           | 4.14                    | 0                     | 24.2                     | 1                       | 66.6                    | 0                   | 7.48                          |
| 8           | 4.61                    | 0                     | 20.8                     | 1                       | 62.2                    | 1                   | 5.39                          |
| 9           | 4.28                    | 1                     | 23.1                     | 1                       | 87.5                    | 1                   | 6.77                          |
| 10          | 3.74                    | 1                     | 32.5                     | 1                       | 88.2                    | 0                   | 8.98                          |
| 11          | 3.65                    | 1                     | 20.0                     | 0                       | 69.1                    | 0                   | 6.7                           |
| 12          | 3.44                    | 1                     | 29.2                     | 0                       | 83.4                    | 0                   | 6.2                           |
| 13          | 4.63                    | 0                     | 25.2                     | 1                       | 78.4                    | 0                   | 8.3                           |
| 14          | 6.04                    | 1                     | 23.5                     | 1                       | 86.4                    | 0                   | 6.18                          |
| 15          | 4.47                    | 0                     | 25.3                     | 1                       | 73.4                    | 1                   | 7.73                          |
| 16          | 4.88                    | 0                     | 19.8                     | 0                       | 79.7                    | 0                   | 5.97                          |
| b. Data ②   | b. Data ②               | b. Data ②             | b. Data ②                | b. Data ②               | b. Data ②               | b. Data ②           | b. Data ②                     |
| Groups      | Tunnel wind speed (m/s) | Lamp runtime (day)    | Lamp body has no damage  | Is the circuit corroded | Number of damaged lamps | Risk of loss value  |                               |
| 1           | 10                      | 1                     | 0                        | 1                       | 2                       | 2                   | 2                             |
| 2           | 15                      | 0                     | 1                        | 0                       | 4                       | 1                   | 1                             |
| 3           | 8                       | 0                     | 0                        | 0                       | 0                       | 1                   | 1                             |
| 4           | 42                      | 5                     | 1                        | 1                       | 65                      | 3                   | 3                             |
| 5           | 12                      | 0                     | 0                        | 0                       | 6                       | 1                   | 1                             |
| 6           | 23                      | 2                     | 0                        | 0                       | 32                      | 2                   | 2                             |
| 7           | 26                      | 2                     | 0                        | 0                       | 0                       | 2                   | 2                             |
| 8           | 24                      | 1                     | 0                        | 1                       | 5                       | 2                   | 2                             |
| 9           | 27                      | 2                     | 1                        | 0                       | 6                       | 3                   | 3                             |
| 10          | 36                      | 3                     | 0                        | 0                       | 6                       | 3                   | 3                             |
| 11          | 49,3                    | 3                     | 1                        | 0                       | 0                       | 4                   | 4                             |
| 12          | 40.3                    | 3                     | 1                        | 0                       | 0                       | 5                   | 5                             |
| 13          | 17.5                    | 0                     | 0                        | 0                       | 2                       | 1                   | 1                             |
| 14          | 13.5                    | 0                     | 0                        | 0                       | 8                       | 1                   | 1                             |
| 15          | 14.3                    | 1                     | 0                        | 0                       | 2                       | 2                   | 2                             |
| 16          | 12.2                    | 0                     | 0                        | 0                       | 3                       | 1                   | 1                             |

Table 14 .  Statistical distribution of risk level categories.

| Risk level (loss value)   |   Total samples |   Proportion (%) |   Training set samples |   Test set samples |
|---------------------------|-----------------|------------------|------------------------|--------------------|
| 1 (low risk)              |              76 |             31.5 |                     61 |                 15 |
| 2 (medium-low risk)       |              68 |             28.2 |                     54 |                 14 |
| 3 (medium risk)           |              45 |             18.7 |                     36 |                  9 |
| 4 (high risk)             |              32 |             13.3 |                     26 |                  6 |
| 5 (extreme high risk)     |              20 |              8.3 |                     15 |                  5 |
| Total                     |             241 |              100 |                    192 |                 49 |

Table 15 .  Dynamic validation results of sequential time periods.

| Time period   |   Data volume |   Prediction accuracy (%) |   Average latency (s) |
|---------------|---------------|---------------------------|-----------------------|
| Period 1      |            40 |                      92.1 |                  0.42 |
| Period 2      |            41 |                      91.5 |                  0.45 |
| Period 3      |            39 |                      90.8 |                  0.43 |
| Period 4      |            40 |                      89.9 |                  0.46 |
| Period 5      |            41 |                      89.4 |                  0.44 |
| Period 6      |            40 |                      89.2 |                  0.45 |

Table 16 .  Mapping rules from continuous risk score to discrete risk level.

| Continuous risk score (regression output)   | Discrete risk level   | Risk state definition   |
|---------------------------------------------|-----------------------|-------------------------|
| 0 ≤ Score<20                                | Level 1               | Low risk                |
| 20 ≤ Score<40                               | Level 2               | Medium-low risk         |
| 40 ≤ Score<60                               | Level 3               | Medium risk             |
| 60 ≤ Score<80                               | Level 4               | High risk               |
| 80 ≤ Score ≤ 100                            | Level 5               | Extreme high risk       |

Table 17 .  Comparative results between regression-mapping and direct classification models.

| Model type                      |   Overall accuracy (%) |   Weighted F1-score |   Cohen's Kappa coefficient |   Level 5 risk recall (%) |   Boundary sample misclassification rate (level 2-3) (%) | Prediction fluctuation (%)   |
|---------------------------------|------------------------|---------------------|-----------------------------|---------------------------|----------------------------------------------------------|------------------------------|
| Regression-mapping (proposed)   |                   98.0 |               0.981 |                       0.974 |                       100 |                                                      2.1 | ± 0.9                        |
| Direct classification (control) |                   94.8 |               0.946 |                       0.932 |                       100 |                                                      8.7 | ± 1.8                        |

Table 18 .  Training parameters for the risk assessment model of lighting facility losses in the Caoguo Mountain Tunnel.

| Parameters                                                                                         | Value                        | Parameters                                                    | Value     |
|----------------------------------------------------------------------------------------------------|------------------------------|---------------------------------------------------------------|-----------|
| Model type selector Minimum weight sum of child nodes Loss function objective Sample sampling rate | Gbtree 1 reg: squarederror 1 | Maximum depth of the tree Feature sampling rate Learning rate | 6 0.2 0.3 |

The comparative results in Table 17 clearly demonstrate the superiority of the proposed regression-mapping strategy:  (1)  It  achieves  higher  overall  classification  accuracy  and  F1-score,  reflecting  better  feature-risk correlation  capture  ability;  (2)  It  significantly  reduces  the  misclassification  rate  of  boundary  samples  (Level 2-3), which is attributed to the continuous risk score that can distinguish subtle differences between adjacent risk levels; (3) It has smaller prediction fluctuation, ensuring more stable performance in practical engineering application; (4) The continuous risk score output provides quantitative risk severity information, which is more conducive to on-site operation and maintenance decision-making compared with the discrete level output of direct classification.

Based on the detailed parameter configuration of the Caoguo Mountain Tunnel (Table 18) and the training set prediction results, along with their corresponding confusion matrices (Figs. 7, 8), the model's predictions were highly consistent with the expected values in 192 cases, accounting for 80% of the total training samples. To further validate the model's generalization performance and avoid overfitting, subsequent testing was performed on an independent test set.

Based on the test set prediction results (Fig. 9) and corresponding confusion matrix (Fig. 10), four prediction errors were observed among the 49 test samples excluded from model training, yielding an overall prediction accuracy of 91.8%. To comprehensively evaluate the multi-class classification performance, we further calculated per-class precision, recall, F1-score, macro-average, weighted-average metrics, and Cohen's Kappa coefficient (Table 19). The model maintains high prediction accuracy across all loss risk classification levels; while Levels 1-2 samples account for a large proportion, misclassifications are mainly between Levels 2 and 3. No Level 5 samples were misclassified, and the Cohen's Kappa coefficient of 0.894 indicates excellent agreement between predictions and true labels. These results confirm the effectiveness of the model training process.

The  time  drift  analysis  results  show  that  incremental  training  can  effectively  suppress  the  accuracy attenuation of the model: without incremental training, the model's accuracy attenuation rate reaches 8.3% as the time sequence extends, while with incremental training, the accuracy attenuation rate is reduced to only 1.7%. In addition, the longitudinal prediction results prove that the model can accurately capture the gradual evolution of lighting facility risks: the average prediction accuracy of longitudinal risk evolution reaches 88.7%, and 12 samples of risk gradient changes are accurately predicted. The detailed data of time drift analysis and longitudinal prediction are shown in Table 20.

Fig. 7 .  Training set prediction results.

<!-- image -->

Line chart

Fig. 8 .  Training set confusion matrix.

<!-- image -->

Bar chart

Fig. 9 .  Test set prediction results.

<!-- image -->

Line chart

To assess  the  statistical  reliability  of  performance  metrics  under  the  limited  test  sample  size,  1000-times bootstrap resampling was performed to calculate the 95% confidence intervals (Table 21). The model maintains high prediction accuracy across all loss risk classification levels; while Levels 1-2 samples account for a large proportion, misclassifications are mainly between Levels 2 and 3. No Level 5 samples were misclassified, and the

Fig. 10 .  Test set confusion matrix.

<!-- image -->

Bar chart

Table 19 .  Comprehensive evaluation metrics of original XGBoost model.

| Risk level    | Precision   | Recall   |   F1-score |
|---------------|-------------|----------|------------|
| 1             | 0.933       | 1.000    |      0.965 |
| 2             | 0.923       | 0.857    |      0.889 |
| 3             | 0.889       | 0.889    |      0.889 |
| 4             | 1.000       | 0.833    |      0.909 |
| 5             | 1.000       | 1.000    |      1.000 |
| Macro avg     | 0.949       | 0.916    |      0.930 |
| Weighted avg  | 0.919       | 0.918    |      0.917 |
| Cohen's Kappa | -           | -        |      0.894 |

Table 20 .  Time drift and longitudinal prediction results.

| Validation type         | Index                                                | Value   |
|-------------------------|------------------------------------------------------|---------|
| Time drift analysis     | Accuracy attenuation rate (without increment)        | 8.3%    |
| Time drift analysis     | Accuracy attenuation rate (with increment)           | 1.7%    |
| Longitudinal prediction | Average prediction accuracy (%)                      | 88.7    |
| Longitudinal prediction | Number of accurately predicted risk gradient samples | 12      |

Table 21 .  Bootstrap uncertainty estimation (original XGBoost).

| Metric            | Point estimate   | 95% confidence interval (Bootstrap, 1000 resamples)   |
|-------------------|------------------|-------------------------------------------------------|
| Overall accuracy  | 91.8%            | 86.2-96.9%                                            |
| Weighted F1-score | 0.917            | 0.854-0.962                                           |
| Cohen's Kappa     | 0.894            | 0.813-0.951                                           |

95% CI of overall accuracy (86.2-96.9%) further confirms that the prediction errors remain within a statistically acceptable range, verifying the effectiveness of the model training process.

## Model training based on XGBoost Bayesian optimization

In tunnel lighting facility risk assessment, model performance critically depends on multiple hyperparameters, whose selection directly determines training efficacy, real-world generalization capability, and stability. For the specific application scenario of loss risk assessment in the Caoguo Mountain Tunnel, initial success was achieved using XGBoost with empirically configured parameters. To maximize the model's potential by enhancing its prediction  accuracy  and  stability,  finer  hyperparameter  tuning  is  essential.  This  study  employs  Bayesian optimization to address this requirement. Since this is a 5-class classification task with slight class imbalance, the optimization objective is set to maximize the weighted multi-class AUC, which can effectively alleviate the bias caused by uneven sample distribution across risk levels. The method identifies optimal hyperparameter combinations through comprehensive searches within predefined ranges, thereby maximizing model performance. The hyperparameter search space for training the Bayesian-optimized XGBoost model is defined in Table 22, while the corresponding improvements in optimization efficiency are demonstrated in Table 23.

Table 22 .  Training parameters for loss risk assessment model based on hyperparameter optimization of lighting facilities in Caoguo Mountain Tunnel.

| Hyperparameters   | Search scope           | Hyperparameters   | Search scope           |
|-------------------|------------------------|-------------------|------------------------|
| learning_rate     | log-uniform(1e-3, 0.1) | reg_alpha         | log-uniform (1e-2, 10) |
| max_depth         | int(3, 10)             | reg_lambda        | log-uniform (1e-1, 20) |
| Subsample         | uniform(0.6, 1.0)      | min_child_weight  | uniform (1, 10)        |
| colsample_bytree  | uniform(0.6, 1.0)      | n_estimators      | int (100, 500)         |

Table 23 .  Comparison of hyperparameter optimization efficiency.

| Comparison dimensions                              | XGBoost   | BO-XGBoost   | Optimization Notes                                   |
|----------------------------------------------------|-----------|--------------|------------------------------------------------------|
| Total number of attempts                           | 150       | 40           | BO reduced ineffective attempts by 73%               |
| Average training and validation time per round     | 30s       | 32s          | BO increased by 7% to calculate expenses             |
| Total optimization time                            | 4500s     | 1280s        | BO saves 71% time                                    |
| Average best validation set AUC                    | 0.910     | 0.958        | BO performance improved by 5.3%                      |
| Number of attempts to achieve an average AUC > 0.9 | 25        | 3            | BO speed increased by 89% Effective positioning area |

Fig. 11 .  Training set prediction results.

<!-- image -->

Line chart

As indicated in the preceding table, the BO-XGBoost approach achieves a superior validation set AUC while consuming only 27% of the trial iterations and 28% of the computation time required by standard XGBoost. This translates to an 89% acceleration in locating the effective parameter region and a 5.3% improvement in model performance, demonstrating significant gains in both optimization efficiency and prediction accuracy. Based on the Bayesian optimization results and the operational requirements of the Caoguo Mountain Tunnel, the final hyperparameters were determined as follows: learning\_rate = 0.032, max\_depth = 8, subsample = 0.85, colsample\_bytree = 0.75, reg\_alpha = 0.25, reg\_lambda = 1.8, min\_child\_weight = 6, and n\_estimators = 280.

As illustrated in Figs. 11 and 12, which present the training set predictions and their corresponding confusion matrix respectively, the model shows high consistency between predicted and expected values in 192 instances, accounting for 80% of the total samples.

Figures 13 and 14 present the test set predictions and corresponding confusion matrix, respectively. The Bayesian-optimized model achieves significant performance improvements: only one prediction error occurred in  49  unseen  independent  test  cases,  with  an  overall  accuracy  of  98.0%.  Comprehensive  evaluation  metrics including per-class precision, recall, F1-score, macro-average, weighted-average, and Cohen's Kappa coefficient are  supplemented  in  Table  24.  The  model  maintains  high  prediction  accuracy  across  all  risk  levels;  minor misclassifications are confined to ambiguous boundary samples between Levels 2 and 3, and all Level 5 extremerisk samples are correctly identified. The weighted F1-score reaches 0.981 and Cohen's Kappa is 0.974, indicating extremely high classification reliability and out-of-sample generalization ability rather than overfitting. These outcomes validate the effectiveness of Bayesian optimization for the risk assessment model.

To  quantify  the  statistical  uncertainty  of  the  evaluation  results,  1000-times  bootstrap  resampling  was conducted to derive 95% confidence intervals for key metrics (Table 25). The model maintains high prediction accuracy across all risk levels; minor misclassifications are confined to Levels 2 and 3, and all Level 5 extremerisk  samples  are  correctly  identified.  The  narrow  95%  confidence  intervals  (e.g.,  94.7-100.0%  for  accuracy) demonstrate the high statistical reliability and stability of the optimized model, validating the effectiveness of Bayesian optimization for the risk assessment model.

Fig. 12 .  Training set confusion matrix.

<!-- image -->

Bar chart

Fig. 13 .  Test set prediction results.

<!-- image -->

Line chart

Fig. 14 .  Test set confusion matrix.

<!-- image -->

Bar chart

To further verify the superiority of the proposed model, this study carried out comparative experiments with various baseline models including Logistic Regression (LR), Support Vector Machine (SVM), Random Forest (RF), LightGBM, and standard XGBoost. To ensure objective and fair quantitative comparison, all models shared identical data preprocessing pipelines, feature inputs, training/test partitioning ratios, and 5-fold crossvalidation strategies. For each baseline, universal default configurations were adopted based on consensus, and core hyperparameters that significantly affect model performance were systematically optimized through grid search or randomized search, with the optimal parameter combination selected according to cross-validation weighted F1-score.

The detailed parameter tuning principles for each baseline model are as follows:

Table 24 .  Comprehensive evaluation metrics of BO-XGBoost model.

| Risk level    | Precision   | Recall   |   F1-score |
|---------------|-------------|----------|------------|
| 1             | 1.000       | 1.000    |      1.000 |
| 2             | 0.933       | 1.000    |      0.966 |
| 3             | 1.000       | 0.889    |      0.941 |
| 4             | 1.000       | 1.000    |      1.000 |
| 5             | 1.000       | 1.000    |      1.000 |
| Macro avg     | 0.987       | 0.978    |      0.981 |
| Weighted avg  | 0.981       | 0.980    |      0.981 |
| Cohen's Kappa | -           | -        |      0.974 |

Table 25 .  Bootstrap uncertainty estimation (BO-XGBoost).

| Metric            | Point estimate   | 95% confidence interval (Bootstrap, 1000 resamples)   |
|-------------------|------------------|-------------------------------------------------------|
| Overall accuracy  | 98.0%            | 94.7-100.0%                                           |
| Weighted F1-score | 0.981            | 0.952-1.000                                           |
| Cohen's Kappa     | 0.974            | 0.936-1.000                                           |

Table 26 .  Performance comparison of different models.

| Model                        |   Overall accuracy (%) |   Weighted F1-score |   Cohen's Kappa coefficient |   Level 5 risk recall |
|------------------------------|------------------------|---------------------|-----------------------------|-----------------------|
| Logistic regression (LR)     |                   79.6 |               0.782 |                       0.721 |                 0.600 |
| Support vector machine (SVM) |                   85.7 |               0.843 |                       0.809 |                 0.800 |
| Random forest (RF)           |                   87.8 |               0.869 |                       0.836 |                 0.800 |
| LightGBM                     |                   93.9 |               0.935 |                       0.918 |                 0.900 |
| Standard XGBoost             |                   91.8 |               0.917 |                       0.894 |                 1.000 |
| BO-XGBoost                   |                   98.0 |               0.981 |                       0.974 |                 1.000 |

Logistic  Regression  (LR):  L2  regularization  was  adopted  to  suppress  overfitting,  and  the  regularization coefficient  C  was  optimized  within  a  reasonable  logarithmic  scale  to  balance  the  model's  fitting  ability  and generalization performance.

Support Vector Machine (SVM): The RBF kernel was selected to capture the nonlinear relationships among multi-dimensional tunnel lighting risk indicators. The penalty coefficient and kernel bandwidth were jointly optimized to balance the classification margin and structural risk.

Random Forest (RF): Key hyperparameters including the number of decision trees, maximum tree depth, and minimum sample split threshold were optimized to avoid overgrowth of individual trees, reduce redundant ensemble branches, and balance model complexity and computational efficiency.

LightGBM: Core hyperparameters such as learning rate, maximum tree depth, and leaf node constraints were fine-tuned to control gradient boosting iteration intensity and suppress overfitting on small-scale samples.

Standard XGBoost: In addition to optimizing learning rate and tree depth, L1 and L2 regularization terms were  synchronously  adjusted  to  constrain  model  complexity,  ensuring  fair  comparison  with  the  Bayesianoptimized XGBoost variant under identical regularization settings.

The results show that BO-XGBoost outperforms all comparative models in all evaluation metrics (Table 26), which fully validates the effectiveness of Bayesian optimization for hyperparameter tuning of the risk assessment model for lighting facilities in the Caoguo Mountain Tunnel.

## Engineering validation

Table 27 documents field measurement data, and Figs. 15 and 16, which illustrate the application workflow and system interface for the central section of the Caoguo Mountain Tunnel respectively, Fig. 15 indicates that the loss risk classification is Level 4, signifying an elevated risk level. Field observations reveal concerning conditions of  the  lighting  facilities  in  this  tunnel  segment,  with  primary  issues  including:  damaged  luminaires  and compromised lamp housings leading to inadequate illumination; voltage instability causing frequent flickering; and control system failures that prevent automatic adjustments. These deficiencies result in uneven lighting distributions, which elevate the risk of traffic accidents.

Comparative  validation  against  actual  engineering  conditions  confirms  the  high  accuracy  of  the  tunnel lighting facility risk assessment system. After processing highway tunnel lighting data, the client-side prediction software rapidly and precisely generates loss risk evaluations within reasonable operational parameters.

Table 27 .  Actual measurement results for a section of the middle part of the Caoguo Mountain Tunnel.

| a. Live broadcast ①              | a. Live broadcast ①                                  | a. Live broadcast ①                                  | a. Live broadcast ①              | a. Live broadcast ①                  | a. Live broadcast ①           | a. Live broadcast ①                       |
|----------------------------------|------------------------------------------------------|------------------------------------------------------|----------------------------------|--------------------------------------|-------------------------------|-------------------------------------------|
| Illuminance (lx)                 | Whether the electromagnetic contactor is waterlogged | Whether the electromagnetic contactor is waterlogged | Tunnel temperature (°C)          | Whether the voltage is stable or not | Relative Humidity (RH%)       | Whether the pole has cracks               |
| 4.35                             | 0                                                    | 0                                                    | 16.8                             | 0                                    | 39.6                          | 1                                         |
| b. Live broadcast ②              | b. Live broadcast ②                                  | b. Live broadcast ②                                  | b. Live broadcast ②              | b. Live broadcast ②                  | b. Live broadcast ②           | b. Live broadcast ②                       |
| Working time of light source (%) | Tunnel wind speed (m/s)                              | Number of damaged fixtures                           | Whether the lamp body is damaged | Whether the line is corroded         | Luminaire running time (days) | Actual conditions on site                 |
| 6.54                             | 37                                                   | 4                                                    | 0                                | 0                                    | 31                            | Serious malfunction of lighting equipment |

Fig. 15 .  Application process for tunnel lighting facility risk assessment model.

<!-- image -->

Flow chart

Fig. 16 .  Application of tunnel lighting facility risk assessment system.

<!-- image -->

Screenshot from computer

This  capability  delivers  comprehensive  operational  guidance  for  on-site  tunnel  maintenance.  Proactive mitigation measures, informed by these risk assessments, effectively eliminate potential failure risks, thereby reducing the incidence of traffic accidents.

## Conclusion

This  study  establishes  an  integrated  tunnel  lighting  risk  management  system  encompassing  monitoring, assessment, and warning functionalities. The developed BO-XGBoost risk prediction model extracts actionable insights  from  engineering  data,  enabling  precise  loss  risk  evaluation  for  highway  tunnel  lighting  facilities.

Concurrently, the risk assessment software was implemented using PyCharm Community Edition. The principal conclusions are summarized as follows:

1.  This  study  establishes  a  foundational  tunnel  lighting  facility  assessment  framework  by  integrating  multi-source heterogeneous data. For the first time, 12 independent and easily obtainable physical indicatorsincluding illuminance levels, waterproof status of electromagnetic contactors, and internal tunnel temperature-are deeply integrated with operational parameters. An XGBoost-based scoring standard was developed to construct a risk assessment framework, which covers environmental adaptability, equipment longevity, and electrical safety. This framework provides critical theoretical and technical foundations for enhancing the safety management of tunnel operations.
2.  This work pioneers the application of the BO-XGBoost model in lighting risk assessment, with three key contributions. It introduces an innovative 'Model Training-Dynamic Assessment-Risk Prediction' closedloop mechanism, which effectively captures nonlinear and temporal features for proactive risk alerts. This mechanism shifts maintenance practices from reactive to preventive paradigms. Compared with standard XGBoost, it achieves superior efficiency, with 27% fewer iterations, 28% less computation time, and 89% faster localization of effective parameter regions. Additionally, it delivers enhanced performance, including a 5.3% improvement and 98.0% prediction accuracy, thus validating its effectiveness.
3.  This research completes practical validation and platform development to solidify the model's applicability. Field validation was conducted on lighting facilities in the central section of Caoguo Mountain Tunnel, confirming exceptional alignment between the model's performance and actual on-site conditions. Accurate risk predictions and early warnings generated by the model ensure robust operational safety for tunnel lighting systems. Meanwhile, a lightweight Tunnel Lighting Facility Risk Intelligent Assessment Platform was developed using PyCharm Community Edition, featuring an optimized three-tier architecture and technical optimizations. This platform enables real-time risk assessments, substantially reducing operational hazards in highway tunnel maintenance practices.

## Discussion

In terms of engineering applicability and scenario generalization, although the model validation in this study is carried out based on the measured data of Caoguo Mountain Tunnel, the proposed risk assessment framework exhibits favorable transferability to other highway tunnel scenarios.

First, the constructed 12-indicator evaluation system and indicator threshold standards are formulated in accordance with national and industrial unified specifications for highway tunnel operation and maintenance, without  relying  on  unique  structural  or  environmental  features  of  a  single  tunnel,  which  ensures  universal applicability in similar mountain highway tunnels.

Second, the Bayesian optimized XGBoost model adopts a universal feature input structure and standardized data  preprocessing  strategies,  including  outlier  elimination,  normalized  statistical  interval  constraint  and correlation-preserving  data  augmentation.  No  case-specific  customized  module  is  designed  for  Caoguo Mountain Tunnel. For other tunnel projects, the model can be quickly migrated and deployed only by finetuning individual local environmental boundary parameters such as temperature and humidity range.

In addition, limited by the difficulty of synchronous multi-tunnel long-term monitoring data acquisition, external dataset validation is not included in the current stage. Subsequent research will collect operation data from  multiple  regional  highway  tunnels  to  further  complete  cross-scene  verification,  so  as  to  continuously optimize the robustness and generalizability of the lighting risk assessment model.

## Data availability

Data will be made available on request.

Received: 24 February 2026; Accepted: 21 May 2026

## References

1.  Xu, L., Zhu, H., Shen, Y., Ling, J. &amp; Feng, S. Lighting environment design evaluation with digital workflow: A life cycle framework for integrating carbon and cost reduction strategies in tunnels. Tunnelling and Underground Space Technology.  h t t p s : / / d o i . o r g / 1 0. 1 0 1 6 / j . t us t . 2 0 2 5 . 1 0 6 3 6 3
2.  Lim, J., Park, H., Oh, T. &amp; Kim, I. The impact of information delivery systems in tunnels depending on lighting intensity and speed limit. Tunnel. Undergr. Space Technol. https://doi.org/10.1016/j.tust.2025.106365
3.  Wang, S. et al. Improving driving safety in freeway tunnels: A field study of linear visual guiding facilities. Tunnel. Undergr. Space Technol. https://doi.org/10.1016/j.tust.2023.105489
4.  Yizhao Wang, X., Kang, X., Wang, Y., Yang, X. &amp; Li High-dynamic impact mechanism of complex spiral tunnel environments on driving behavior based on multi-source data fusion. Tunnel. Undergr. Space Technol. https://doi.org/10.1016/j.tust.2025.106584
5.  Chen, J., You, L., Yang, M. &amp; Wang, X. Traffic safety assessment and prediction under different lighting service states in road tunnels. Tunnel. Undergr. Space Technol. https://doi.org/10.1016/j.tust.2023.105001
6.  Shen, Y. et al. Holistic digital-twin-based framework to improve tunnel lighting environment: From methodology to application. Build. Environ. https://doi.org/10.1016/j.buildenv.2022.109562
7.  Shen, Y., Ling, J., Li, T., Zhou, L., Feng, S. &amp; Hehua,  Z. Diffuse reflection-based lighting calculation model and particle swarm optimization algorithm for road tunnels. Tunnel. Undergr. Space Technol. https://doi.org/10.1016/j.tust.2022.104457
8.  Jia'an Niu, B., Liang, S., He, J., Xiao, C. &amp; Qin L. tunnel lighting environment improvement method based on multiple-parameter intelligent control: Considering dynamic changes in luminance difference. Tunnel. Undergr. Space Technol. h t t ps : / / d o i . or g / 1 0 . 1 0 1 6 / j . t u s t . 20 2 2 . 1 0 4 6 3 7
9.  Ahmed Emara, S. A. et al. Advanced 3D abrasion mapping in sediment bypass tunnels using XGBoost: A high-dimensional approach to predictive modeling. Expert Syst. Appl. https://doi.org/10.1016/j.eswa.2025.127686

10.  Tianjian Cheng, C. et al. Yan, Prediction of active length of pipes and tunnels under normal faulting with XGBoost integrating a complexity-performance balanced optimization approach. Comput. Geotech. https://doi.org/10.1016/j.compgeo.2024.107048
11.  Yuan, H., Zhao, K., Wan, Y. Y. L., Tian, Z. &amp; Chen, X. Long tunnel group driving fatigue detection model based on XGBoost algorithm. J. Traffic Transp. Eng. (English Edition) https://doi.org/10.1016/j.jtte.2023.02.008
12.  Shifan Qiao, H. et al. XGBoost-based global sensitivity analysis of ground settlement caused by shield tunneling in dense karst areas. Adv. Eng. Inform. https://doi.org/10.1016/j.aei.2024.102928
13.  Bo, Y. et al. Prediction of tunnel deformation using PSO variant integrated with XGBoost and its TBM jamming application. Tunnel. Undergr. Space Technol. https://doi.org/10.1016/j.tust.2024.105842
14.  Nguyen, V . Q., Tran, V . L., Nguyen, D. D., Sadiq, S. &amp; Park, D. Novel hybrid MFO-XGBoost model for predicting the racking ratio of the rectangular tunnels subjected to seismic loading. Transp. Geotech. https://doi.org/10.1016/j.trgeo.2022.100878
15.  Lin, Y., Xiong, J., Xing, H. &amp;  Ning, X. Research on carbon emission prediction methods for high-grade highway construction based on the XGBoost-SVR hybrid model. J. Cent. South. Univ. (Natural Sci. Edition) , 55 (07): 2588-2599.  h t t p s : / / d o i . o r g / 1 0 . 1 1 8 1 7/ j . i s s n . 1 6 7 2 - 7 2 0 7 . 2 0 2 4 . 07 . 0 1 3 . (2024).
16.  Chen Jian,  J.  et  al.  Study  on  section  floating  during  construction  of  a  large-diameter  tunnel  in  the  yellow  river  based  on  the XGBoost Algorithm. Tunnel. Constr. (Chinese and English Edition) 43 (S1): 72-80. (2023).  h t t p s : / / d o i . o r g / 1 0 . 3 9 7 3 / j . i s s n . 2 0 9 6 - 4 4 9 8 . 2 0 2 3 . S 1 . 00 9
17.  Xia Hanyong, H., Yi, Y. &amp; Hejun, Z. L. Ground settlement prediction method for shield construction based on the XGBoost Algorithm. Railway Standard Des. 67 (03), 140-147. https://doi. org/10.13238 /j.issn.1004 -2954.20210 9060008 (2023).
18.  Wang,  F.,  Gong,  G.,  Duan,  L.,  Qin,  Y.  Design  of  an  intelligent  decision-making  system  for  tunnel  boring  machine  operating parameters based on XGBoost. J. Zhejiang Univ. (Engineering Sci. Edition) . 54 (04), 633-641.  h t t p s : / / d o i . o r g / 1 0 . 3 7 8 5 / j . i s s n . 1 0 0 8 - 9 73 X . 2 0 2 0 . 0 4 . 0 0 1  (2020).
19.  Wang, Y. Application of an improved XGBoost model in stock prediction. Comput. Eng. Appl. 55 (20), 202-207.  h t t p s : / / d o i . o r g / 1 0 . 3 7 7 8 / j . i s s n . 10 0 2 - 8 3 3 1 . 1 9 0 4 - 0 0 0 7  (2019).
20.  Roberto, S., Bruno, G., Danilo, A. &amp; Alessandra, G. Discrete Bayesian optimization via machine learning, performance evaluation. https://doi.org/10.1016/j.peva.2025.102487
21.  Mohammed, T. &amp; Said E. K. A novel approach based on XGBoost classifier and Bayesian optimization for credit card fraud detection. Cyber Secur. Appl. https://doi.org/10.1016/j.csa.2025.100093
22.  Hamidreza, G. &amp; Ehsan, H. Designing a cryptocurrency trading system with deep reinforcement learning utilizing LSTM neural networks and XGBoost feature selection. Appl. Soft Comput. https://doi.org/10.1016/j.asoc.2025.113029
23.  Meysam  Alizamir,  M.  et  al.  An  interpretable  XGBoost-SHAP  machine  learning  model  for  reliable  prediction  of  mechanical properties in waste foundry sand-based eco-friendly concrete. Results Eng. https://doi.org/10.1016/j.rineng.2025.104307
24.  Eser, S. et al. A modular Python framework for rapid development of advanced control algorithms for energy systems. Appl. Energy https://doi.org/10.1016/j.apenergy.2025.125496
25.  Yangfan, J.,  Bugby,  S.  L.    &amp;  Lees,  J.  E.  PMST:  A  custom  Python-based  Monte  Carlo  Simulation  Tool  for  research  and  system development in portable pinhole gamma cameras. Nucl. Instrum. Methods Phys. Res. Sect. A Accel. Spectrom. Detectors Assoc. Equip. https://doi.org/10.1016/j.nima.2024.169161
26.  Biplov, P ., Bipul, T. &amp;  Bishwash, P . Sentiment analysis of movie reviews: A flask application using CNN with RoBERTa embeddings. Syst. Soft Comput. https://doi.org/10.1016/j.sasc.2025.200192
27.  Sahithi T. &amp; Venkata rao, M. Managing Mysql Cluster Data Using Cloudera Impala. Procedia Comput. Sci. h t t ps : / / d o i . or g / 1 0 . 1 0 1 6/ j . p r o c s . 20 1 6 . 0 5 . 1 9 3

## Acknowledgements

The authors gratefully acknowledge the financial support and the study participants for their time and contribution.

## Author contributions

Hui Xiao:  Writing-review &amp; editing,  Validation,  Methodology,  Investigation.  Weihong  Yang:  Investigation, Formal analysis, Conceptualization. Jiabao Tang: Writing-original draft, Visualization, Validation, Software. Zhiliu Wang: Supervision, Project administration, Funding acquisition.

## Funding

This work is supported by the Henan Province Science and Technology Research Project (252102321008), the Natural Science Foundation of Zhongyuan University of Technology (K2023QN013), the Funding Program for Young Backbone Teachers in Zhongyuan University of Technology (2023XQG14), the National Key Research and Development Program of China (2023YFC3805900), the Key Research and Development projects of Metallurgical Corporation of China (YCC2023Kt01).

## Declarations

## Competing interests

The authors declare no competing interests.

## Additional information

Correspondence and requests for materials should be addressed to Z.L.W .

Reprints and permissions information is available at www.nature.com/reprints.

Publisher's Note Springer Nature remains neutral with regard to jurisdictional claims in published maps and institutional affiliations.

Open Access This article is licensed under a Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License, which permits any non-commercial use, sharing, distribution and reproduction in any medium or format, as long as you give appropriate credit to the original author(s) and the source, provide a link to the Creative Commons licence, and indicate if you modified the licensed material. You do not have permission under this licence to share adapted material derived from this article or parts of it. The images or other third party material in this article are included in the article's Creative Commons licence, unless indicated otherwise in a credit line to the material. If material is not included in the article's Creative Commons licence and your intended use is not permitted by statutory regulation or exceeds the permitted use, you will need to obtain permission directly from the copyright holder. To view a copy of this licence, visit  h t t p : / / c r e a t i v e c o m m o ns . o r g / l i c e n s e s / b y - n c - n d / 4 . 0/ .

© The Author(s) 2026
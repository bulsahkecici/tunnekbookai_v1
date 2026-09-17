## DECISION SUPPORT SYSTEM FOR AN INTELLIGENT OPERATOR OF UTILITY TUNNEL BORING MACHINES

PREPRINT

Gabriel Michau ETH Z¨ urich,

Z¨ urich, Switzerland

Olga Fink ETH Z¨ urich, Z¨ urich, Switzerland

08th of January 2021

## ABSTRACT

In tunnel construction projects, delays induce high costs. Thus, tunnel boring machines (TBM) operators aim for fast advance rates, without safety compromise, a difficult mission in uncertain ground environments. Finding the optimal control parameters based on the TBM sensors' measurements remains an open research question with large practical relevance.

In this paper, we propose an intelligent decision support system developed in three steps. First past projects performances are evaluated with an optimality score, taking into account the advance rate and the working pressure safety. Then, a deep learning model learns the mapping between the TBM measurements and this optimality score. Last, in real application, the model provides incremental recommendations to improve the optimality, taking into account the current setting and measurements of the TBM.

The proposed approach is evaluated on real micro-tunnelling project and demonstrates great promises for future projects.

K eywords Decision Support System, Intelligent Operator, Utility Tunnel Boring Machines.

## 1 Introduction

Construction of tunnels has been gaining importance, driven by population growth and urbanization, enabling expansion and enhancement of transportation and underground utility networks. However, tunnelling is subject to large uncertainties of geology and other construction conditions that contribute to the frequently occurring delays and overruns of budgeted costs in such projects. A good management of risks and uncertainties is, therefore, one of the key requirements of large tunnelling projects. Decision support systems (DSS) are one of the primary tools supporting the decision makers.

To assess and reduce tunnelling risks, several DSS have been developed already several decades ago, most of which were addressing general projects risks prior to tunnel construction. One of the widely applied DSS in the tunneling industry is the Decision Aids for Tunnelling (DAT) that were introduced in 1998 Einstein et al. [8] and have since been further developed , integrating several additional features (Einstein [6], Haas and Einstein [9], Min and Einstein [13], Moret and Einstein [16]). The DAT enable quantitative risk estimations in the form of time-cost distributions given geology, resource and construction strategy information.

Other studies (Sousa and Einstein [21], Mooney et al. [14], Zhao et al. [25]) have conducted research on dynamically updating and predicting the geology ahead of the TBM to decrease the main source of uncertainty and to support decision makers during excavation.

Gabriel Rodriguez Garcia ETH Z¨ urich,

Z¨ urich, Switzerland

## Herbert H. Einstein

Massachusetts Institute of Technology, Cambridge, MA 02139-4307, USA

Because of time and budget pressure, the goal of tunnel boring machine (TBM) operators is advancing fast and safely through the tunnel trajectory, achieving high advance rates, while maintaining a high availability of the TBM (since machine breakdowns and unavailability would lead to large delays). advance rates depend on the design, configuration and system state of the TBM but also on the current geological conditions. While TBM have recently been increasingly equipped with numerous sensors to monitor the operation, information on the exact geology is still very scarce and its inference from other measured parameters remains an open research question. Therefore, it cannot be directly integrated in the control. Experienced TBM operators are often able to deduce good control parameter values that enable them to adjust to the geological conditions and achieve good advance rates. However, the level of experience varies among the operators and often, sub-optimal control parameters are used. Finding optimal values for the control parameters based on the information from the TBM system, the operating and the geological conditions remains an open research question with a large practical relevance.

Asimilar challenge as in tunnelling was addressed by Payette et al. [18] with the goal of supporting operator actions in real-time well drilling for the oil and gas industry. The drilling advisory system (DAS) helps operators to avoid drilling dysfunctions acting as performance limiters and helps to achieve higher advance rates while extending drill bit lifetime ([18]). It analyzes data from active control parameters (based on the investigation of drill-off tests) and visually maps optimal parameter settings for the current geologic formation ([19]). However, drill-off tests are, typically, not part of the common practice in tunneling applications. This approach is, therefore, not directly transferable to TBM operation.

Another approach applied for optimizing drilling parameters for oil wells tackles similar challenges as those addressed in the current research study (Chandrasekaran and Govindarajan [3], Self et al. [20], Jiang et al. [10]). In Chandrasekaran and Govindarajan [3], artificial neural networks are applied to predict the advance rate. Heuristic search algorithms (Particle Swarm Optimization or Ant Colony Optimization) are then used to find optimal control parameters in real-time. This approach is different from the one proposed here since it does not consider the scarcity of the data available for training and may require a simulator if abundant data are not available.

To the best of our knowledge, there have been no published studies tackling real-time control parameter optimization with a DSS in the field of tunnel construction risk management. The framework proposed here aims at developing an intelligent decision support system that recommends optimal control parameters in real time to the machine operators (Figure 1). The proposed approach only requires the availability of representative TBM operational data. In addition, a measure of credibility is defined to inform the operator to which extent the model suggestions are supported by training samples under similar conditions. This is particularly relevant in the context where operating regimes exhibit a high variability and where some operating regimes may contain only few measured observations. Furthermore, we define a novel and intuitive measure to quantitatively describe optimality of operation for a micro-tunnelling TBM based on advance rate and working pressure.

## 2 Framework

The proposed framework, as illustrated in Figure 1, consists of three main steps. First, all data sources, including TBM sensor measurements and geological information are pre-processed and cleansed (Fig. 1 - 1). Second, we train a Deep Learning Feed-forward Neural Network on the available historical data to predict the 'optimality score', the measure of the boring efficiency proposed in this work (Fig. 1 - 2.1). Third, the trained model (Fig. 1 - 2.2) can be used during the TBM operation to compute recommendations for control parameters and their credibility in real time (Fig. 1 - 2.3). A dashboard presents these recommendations to the operator (Fig. 1 - 3).

## 3 Related Works

## Decision Aids for Tunnelling (DAT)

Given the significant uncertainties and their effect on tunnelling projects, research on general tunnelling risk assessment and management, in particular for developing DAT systems. has been abundant (Einstein et al. [7], Mikaeil et al. [12], Wang et al. [23]). Existing DAT are advanced tools integrating several features. They have already been in use in large tunnel construction projects for decades, including the Gotthard and L¨ otschberg Basis Tunnels in Switzerland. The DAT are decision support systems that estimate the distribution of possible costs, time and resource requirements, considering a multitude of inputs such as geologic conditions, available resources and construction strategies. They rely on Monte Carlo simulations of a large number of construction cycles, given possible geology profiles. Subsequently, the time to finish the corresponding tunnels with the user-defined strategy and boundary conditions is calculated for each of the excavation cycles ([8]).

Figure 1: Framework Visual representation of the framework, describing how sensor data is leveraged to support TBM operators while drilling. (1) All data sources, including TBM sensor measurements and geological information are pre-processed and cleansed. (2) We train a Deep Learning Feed-forward Neural Network on the available historical data to predict the 'optimality score' (2.1). The trained model (2.2) can be used during the TBM operation to compute recommendations for control parameters and their credibility in real time (2.3). (3) A dashboard presents these recommendations to the operator.

<!-- image -->

Flow chart

Sousa and Einstein [21] developed a related approach to what is proposed in this paper. This approach is based on Bayesian Networks and comprises two models. The first model predicts the ground class (soil, mixed or rock) based on geology sensitive sensor parameters. The second model infers the construction strategy with the lowest risk (open mode or closed mode excavation for Earth Pressure Balance Machines) based on the predicted ground class. The geology prediction model is updated along the trace using information on already excavated tunnel sections to improve the classification accuracy. Compared to the current research study, the DAT and their extensions provide decision support on a higher level, suggesting complete construction strategies. This is in contrast to the problem addressed here, where we aim at providing detailed information on how to adjust control parameters of the TBM in real time. In both cases, the methods require information about geologic ground class profiles.

## Geology Prediction

Geology prediction is an integral part of uncertainty management and has a high influence on real-time decisions. Drilling prior to the start of the project allows one to gather data on the type of geologies that will be met along the trajectory of the tunnel. Depending on the ground condition, it is not always sufficient to gather precise and continuous data on the ground conditions and on the geology changes. A recent study ([17]), where several machine learning algorithms for detecting the changes in geology based on the TBM operational data were developed, highlights the difficulty of detecting geology changes from TBM sensor data. This difficulty arises from the fact that the effects of the geology on the TBM performances are intertwined with the control parameter choices of the operators. The discrimination from TBM sensor data between true geology changes and control parameter changes remains an unsolved problem.

Zhao et al. [25] presented a complete framework for applying a geology type predictor based on TBM operating data consisting of 72 features using a feedforward neural network. In this case study, 88 samples were taken from one single tunnel at 30 meters depth and only operating data recorded in 0.3 m proximity of each sample was considered. This procedure ensures reliable ground truth labels for the approximately 20 geology types, each specified by 7 physicalmechanical indices including natural severity, internal friction angle, deformation modulus, Poisson's ratio etc. 70% of the data is used for training the model, while 30% is used for testing. In this case, the model tries to predict all of the 7 indices. For performance measurement purposes, the averaged mean squared error across all indices are reported, in the best case reaching as low as 0.212. Nonetheless, the large amount of samples taken as well as their detailed description reduces the applicability for other tunnel construction projects due to high costs.

Given the difficulty of extracting precise online information on the geology, we decided in our project to separate the geologies into three broad classes. For each geology class, we train a different model, robust to minor geological variations. In real applications, we expect the operators to be able to know broadly the geological type in which the TBM is currently operated (e.g., soft, weathered or hard materials).

## DSS for Oil Well Drilling

Decision Support Systems have also been studied in closely related fields such as well drilling Payette et al. [18]. With the aim of achieving consistently better drives, a real-time DSS was developed to identify and avoid performance limiters such as bottom-hole assembly whirl, bit balling, stick-slip etc. The proposed framework is an iterative process. One of the core modules of the framework is a learning or calibration phase, in which the operator is encouraged to test different control parameters settings. This procedure enables the system to find optimal regions within the control parameter state-space spanned by the rate of penetration (ROP) and the weight on bit. This approach is not transferable to TBM operation since active parameter exploration is not part of the usual tunnel construction workflow. Similar parameter exploration, particularly for new ground conditions, could be potentially also explored in tunnelling. However, due to the high variability of the ground conditions in long tunnel projects, these explorations would need to be performed in each of the ground conditions, which is not feasible in practical applications.

A similar approach was presented by Chandrasekaran and Govindarajan [3] where deep learning methods and optimization algorithms were applied to generate optimal control parameter recommendations for oil well drilling. More concretely, a feedforward neural network was trained on historical operational data to learn the mapping between the sensor parameters and the rate of penetration. In a second step, recommendations were generated by selecting the control parameters, given by weight on bit, revolutions per minute and flow rate in the pumps, which lead to highest predicted ROP. This selection procedure is based on a heuristic search algorithm, the particle swarm optimization. It requires, therefore, a large number of samples to learn from, to explore the different parameter combinations. It may, therefore, require a simulator if abundant data are not available.

## 4 Essential Concepts and Practices of TBM Operation

To control the TBM during excavation, various control parameters are available to machine operators, making the space of possible setpoint choices very large. The operator's main objective is to achieve safe and efficient operation with the highest possible advance rates. To do so, operators typically adjust the control parameters based on experience and on the expected geology profile. While experienced operators are often able to find a good set of parameters given a certain geology, less experienced operators may, however, operate in sub-optimal conditions. The knowledge of the ground conditions is in any case a centerpiece information for operators to decide on their control actions. In the case study used in this research, operators were only given information on the geology through 13 boreholes drilled over more than half a kilometer, prior to the start of the tunnelling project. Analysis of the project revealed, however, that ground conditions had a high variability and that the samples were not always representative of the real geology profile. Interviews with field experts uncovered that operators decide at the beginning of the excavation phase on the control settings, based on the geology reports from the exploration phase and on their experience. Once the excavation process has started, operators hold their control settings constant as long as possible until it becomes obvious that a sub-optimal state has been reached and that a new control parameter choice is required. Minor parameter adjustments may become necessary to retain the working pressure below the operational limit of the machine. Apart of these adjustments, the operators do, usually, not attempt to optimize the control settings.

TBMs are commonly equipped with dozens to hundreds of sensors to monitor the state of the system, the environmental and operating conditions while drilling. In this study, real operational sensor data from a TBM were categorized disjointedly into three groups: control parameters (CoP), target parameters (TP) and context parameters (CxP). CoPs relate to the parameters which are directly modified by the operator during excavation to control the TBM. TPs are the parameters to optimise (e.g., fastest advance rate, low working pressure). TPs are used to design the optimality function. CxPs represent all remaining sensors capturing essential operating and environmental conditions.

## 5 Methodology

## 5.1 Assumptions

Although the framework, as described in Figure 1, was developed based on the case study from a micro-tunnelling machine, the proposed framework can be extended to any mechanized tunnelling system if the assumptions listed below are fulfilled. For the purpose of clarity, the assumptions are sub-divided by their importance into 'imperative' assumptions, assumptions that have to be fulfilled and 'supplementary' assumptions that are not crucial for the applicability of the framework but contribute to the performance of the framework.

## Imperative Requirements on Data Availability and Quality

Since the proposed DSS framework is a data-driven framework, the availability of a representative dataset capturing the state of the machine and its interaction with the surrounding ground is required. Commonly monitored parameters include advance rate, thrust, feed pump pressure and cutter head torque. Typically, the system parameters are recorded as time series with defined sampling frequencies. We assume that all sensor time series used to generate recommendations are free from measurement errors. In our case study, field experts selected the most important available parameters and analyzed them in terms of noise and general validity. Furthermore, we assume that the training and testing samples were drawn from approximately the same underlying distribution, that is, from similar machines in similar ground conditions. This is an essential condition for the successful application of data-driven algorithms. One of the possibilities how this condition can be fulfilled is if several tunnels are excavated in close proximity. This was so for the considered case study. A further possibility to fulfil this condition is by selecting similar operating conditions from previous tunnelling projects. Furthermore, the models can also be trained on data collected at the beginning of the project and applied to the subsequent operation (assuming that a sufficiently representative dataset can be collected at the beginning of the project). This assumption would for example be violated if the TBM cutter head shapes or ground conditions between training and testing phases differ substantially.

## Supplementary Requirements on Data Availability and Quality

The supplementary requirements are less crucial. However, fulfilling them can increase the performance of the proposed framework and could help with the interpretation of the results.

First, since the geology is the most important feature for setting of the control parameters, we assume that the geology profile of the tunnel is available and has a low uncertainty. The geology profile may be provided either by conducting a detailed site investigation prior to tunnelling or by having geologists analyzing samples of excavated materials at the separation unit after drilling. A further option to provide information on geology may be to develop an accurate geology prediction model. However, this model needs to be either developed on previous tunnelling projects with similar geology profiles or on a portion of the data from the current tunnelling project for which the DSS is developed. In our case study, the available geology profiles were rather imprecise. This is why only data collected in homogeneous sections were used for training and testing.

Second, in order to have a reliable validation reference, the operator control actions (adjustments of CoPs) are assumed to have been recorded and are available for the model development. If this assumption is not satisfied, the control actions can still be reconstructed approximately from the recorded data as introduced in Subsection 6.2.

Third, as to ensure robust training and validation we assume to have a large amount of samples available that capture control parameter changes by the operator since only these can be used for the validation procedure introduced in this study. Nonetheless this is usually hard to get since TBM operators tend to rarely change control parameters.

## 5.2 Rationale for the proposed framework

The proposed framework relies on similar concepts as imitation learning [2]. However, it differs from other works in the literature in two ways. First, we introduce a new optimality score to quantify optimal operations. An optimality function is otherwise hard to identify due to the boundary conditions, the operational constraints and the environmental constraints. Second, our framework is designed to mitigate the inherent scarcity of the training data. This scarcity prevents direct application of imitation learning, since the historic operators' actions are only a very small subset of all possible actions and are likely to be sub-optimal. This scarcity of the training data also challenges the quality of the recommendations and this is why we introduce in addition a credibility score. It enables the decision makers to understand the certainty of the applied algorithm under the specific operating conditions.

From the methodological perspective, the proposed framework has three main steps (steps 2.1-2.3 in Figure 1), comprising the steps of optimality definition (2.1), training the deep neural network to predict the defined optimality score (2.2) and finally, provide recommendations for the adjustments of the control parameters based on the first order derivative with respect to the control parameters (2.3). Finally, a credibility score is provided to support the decision makers on how certain the algorithms' recommendations are.

## 5.3 Optimality Definition (Fig 1 - 2.1)

As discussed above, the goal of the operators is to advance fast and safely through the tunnel trajectory. The operation is, however, constrained by bounds and safety thresholds of the operating parameters. In our case study, if the working pressure (pressure which drives the torque of the cutterhead) exceeds a given safety threshold, the TBM will be shut down automatically, leading to undesired time delays. Based on interviews with tunneling engineers, it appears that the working pressure often changes abruptly, in particular during geological transitions toward harder ground. The operators aim, thus, at maintaining a sufficient margin between the working pressure and the safety threshold to avoid unexpected shut downs. Therefore, we propose to define the optimality function f opt GC as a continuous linear function, first, of the advance rate, with a positive coefficient to reward higher advance rates, and second, of the working pressure, with a negative coefficient to penalise higher working pressure. To model the concept of safety margin, we propose to increase the working pressure coefficients once it exceeds a certain margin bound ( MB ). The aim is to penalise more heavily the working pressure, once it exceeds this margin. Since we advocate for training a different model per ground type, we can actually adapt the optimality scoring function to each ground type, enabling realistic expectations of advance rates given the geology. Formally, we propose to define arbitrarily the optimality function for the i-th ground class as

<!-- formula-not-decoded -->

where

- AR t is the advance rate [mm/min] at time t
- WP t is the working pressure [bar] at time t
- UB is the upper bound of the working pressure (safety threshold before automatic shutdown)
- MB i is the working pressure margin bound [bar] defined as the observed 90th-percentile for the i-th ground class
- MAR i is the observed maximum advance rate within i-th ground class (GC)
- w 1 is the negative penalizing weight on the working pressure, when the working pressure is below the margin bound MB i .
- w 2 is the negative penalizing weight on the working pressure, when the working pressure is above the margin bound MB i . Typically we have w 2 ≫ w 1 .

The values of the hyper-parameters, notably the penalizing weights on the working pressure w 1 and w 2 , can either be decided a priori based on expert knowledge, or tuned a posteriori based on the performance of the model in test conditions.

For the purpose of simplicity, we only consider the advance rate and the working pressure in our definition of the optimality. However, other constraints or parameters could be integrated if deemed relevant by the TBM operator. The proposed methodology can be easily applied to any other optimality definition.

Also, to ease the understanding by the operator, we propose to normalise the optimality score as a value between 0 and 100, where 100 corresponds to highest achieved score observed in historic data.

## 5.4 Training: Learn Mapping from TBM State to Optimality (Fig 1 - 2.2)

In the second part of the framework, a machine learning model is developed and trained to learn the mapping from the control parameters (CoP) and the context parameters (CxP) to the previously defined optimality function f opt GC i . In this step, having historic data with a sufficiently rich representation of the different parameter combinations is crucial for training a model able to accurately predict the optimality given varied CoP and CxP and to provide good recommendations. To perform this regression task, we propose to use a deep feed forward neural network, as it has shown excellent performance in complex and varied regression tasks.(Krizhevsky et al. [11], Szegedy et al. [22]). To select the hyperparameters of the neural network, we follow here standard validation practices such as k-fold cross validation combined with a grid search. The process is detailed in Section 6.5.

## 5.5 Generating Recommendations and Credibility (Fig 1 - 2.3)

In the previous section, we proposed to train a machine learning model which, given current control parameters and context parameters, is able to estimate the optimality score. In this step, we propose to compute the first order derivative of the model's output with respect to the control parameters, that is, to compute which modifications of the control parameters current value lead to an increased optimality score. This allows us to recommend in real-time at each consecutive time step one incremental modification of the control parameters toward higher scores of the optimality.

Since the validity of the recommendation highly depends on the quality of the model and, therefore, on its training dataset and its representativeness, we propose, additionally, to compute a credibility measure to quantify the recommendations' trustworthiness. In this work, we propose to rate the recommendation based on the local performance of the model on similar controlled and context parameters in historic data (the nearest neighbours). For each of the n nearest neighbours, we evaluate the performance of the model with two combined metrics. First, we evaluate the quality of the estimation of the optimality score in the neighbourhood of the current observation to quantify the performance of the learning. To do so, we evaluate the ℓ 2 -norm of the difference between the predicted optimality and the true optimality for the j-th nearest neighbours ( e j 1 ). Second, we evaluate the recommendations of the model with similar points from historic data by comparing the recommendations and the actions taken. That is, for the j-th nearest neighbour and the consecutive observation, we compute the ℓ 2 -norm of the difference between the computed otpimality gradient and the observed optimality difference ( e j 2 ). To combine these metrics, we first normalise them based on typical values observed in the validation set (using the 5-th and 95-th percentile). We then average the two metrics and compute their complement to 1, such that higher values indicate a higher credibility. Formally, we perform the following operations:

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

where clip ( z, 0 , 1) is the clipping function in [0 , 1] . Q i 95 and Q i 5 are the 95-th and 5-th percentiles of the i-th metric on the validation set.

The final credibility of a recommendation, for the k -th sample, is the Gaussian-weighted mean of the trust values T j over its n nearest-neighbours set, N ( k ) . That is:

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

with

To choose the number of neighbours to consider, n , we computed in historic data the average distance to the k-th nearest neighbour as a function of k . We found an abrupt change of slope when 15 neighbours are considered and decided therefore to set n = 15 . The Gaussian kernel width parameter B is chosen as the average standard deviation of the distances to the 15 nearest neighbours.

## 6 Case Study

## 6.1 Project Overview

The rapid increase of renewable energy in the northern part of Germany has led to over capacities, which needed to be reduced by transmitting the excess energy to the southern part of the country. Transmission grids are usually constructed overground and must satisfy many requirements posed by local residents and property owners, which often leads to cumbersome and prolonged procedures. For this reason, the government has decided to support the expansion of the grids underground, making use of the microtunnelling technology to circumvent such problems. One of these projects was completed between 2018 and 2019. The TBM used in this project was designed for pipe jacking. It has a small diameter of about half a meter and is designed for fast and efficient drilling procedures. The TBM was fully equipped with dozens of sensors sampling at 0.1Hz. A total of six micro-tunnels with a length 688 meters each were excavated ([1]).

Table 1: A list of all context parameters

| Context Parameters                                                                                                                                                                                                                                      |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Pressures [bar]                                                                                                                                                                                                                                         |
| Steering cylinder 1 pressure Steering cylinder 2 pressure Steering cylinder 3 pressure Steering cylinder 3 pressure (3-B) Feed line pressure on TBM Feed line pressure on pump Suction line pressure Bentonite pump pressure                            |
| Flow rates [ m 3 /s]                                                                                                                                                                                                                                    |
| Conveyor line flow rate Feed line flow rate Drive line flow rate High pressure nozzle flow rate                                                                                                                                                         |
| Other                                                                                                                                                                                                                                                   |
| High pressure pump rotational speed [rpm] Bentonite pump rotational speed [rpm] Steering cylinder 1 extension [mm] Steering cylinder 2 extension [mm] Steering cylinder 3 extension [mm] Machine oil temperature [celsius] TBM axial rotation [degrees] |

## 6.2 Data Overview and Pre-processing

## Sensor Data

Although 6 micro-tunnels were excavated, an initial analysis of the data led us to restrict the analysis to two of the micro-tunnels. The other micro-tunnel data were left aside in this pilot study since some had missing geological information and other had different data collection systems. Furthermore, based on discussions with domain experts, 26 relevant parameters were selected for the analysis. As described in Section 4, we split the parameters into 3 groups: the 2 operating parameters used to compute the optimality score (advance rate and working pressure), the 5 parameters corresponding to the parameters controlled by the operator (CoP) and 19 context parameters (CxP). The CoP are: the rotational speed of the cutter head (CoP 1 ), often set at its maximum value to achieve full excavation rate; the high pressure water nozzle (CoP 2 ), used to clean the cutting wheel and ensure efficient excavation; the drive line pressure (CoP 3 ), used to control the vacuum created to transport the material rapidly to the separation unit; the jacking frame thrust (CoP 4 ), controlling the load applied at the cutting wheel and the feed pump rotational speed (CoP 5 ), controlling the amount of water/slurry used to extract the material into the excavation chamber. In this case study, the true control actions taken by the operator on the CoP were not directly recorded. Therefore, the above CoP are inferred from closely related sensor measurements. We observed that these related measurements had distinct small and large variations, due respectively to noise and operator actions. External causes, such as sensor noise and ground interactions will lead to small fluctuations of the measurements while operator actions will have larger impact on the sensor values. In fact, when looking at the distribution of these fluctuations, one can observe two modes, one for small fluctuations and one for larger fluctuations, with a drop in-between. This drop can be used as a threshold to recover the operators' actions.

The context parameters, CxP, listed in Table 1, are a combination of pressure-, temperature-, force-, flow rate- and positional parameters captured by sensors installed across the TBM.

## Geology Data

Optimal operational parameters depend on the geology surrounding the TBM. Yet, the geological information is hard to obtain for two reasons: first, predicting the surrounding geology from sensor data remains an open research question, second, studies prior to the start of the project only collect scarce samples and contain many uncertainties. In this project, however, geologists could analyse the excavated material and provide a posteriori the geology profile over the entire tunnel trajectory. Nevertheless, this profile contains some uncertainties since part of the analysed excavated material is dissolved in the slurry. Based on discussions with domain experts, we decided to consider three geological classes, for which uncertainties were deemed low enough by the experts and for which sufficiently long homogeneous sections could be identified. Based on operational data collected in these homogeneous geologic profiles, we trained one independent model for each of the geology classes. In real applications, we expect that the operator is able to know roughly the type of geology in which the TBM is currently operated to choose the right model. The three considered geology classes are:

- GC1: Homogeneous highly weathered schist (soft)
- GC2: Homogeneous moderately weathered schist (firm)
- GC3: Homogeneous slightly weathered schist (hard)

## Data Pre-processing

In order to prepare the dataset for the case study, we performed the following operations on the raw data:

1. Data Cleansing
2. (a) Removal of TBM retraction phases (e.g., for TBM cutting wheel maintenance)
3. (b) Removal of sections in which the tunnel length decreases or is constant, due to anomalous measurements or to actions other than the excavation.
4. (c) Removal of unrealistic/erroneous sections (after validation with a field expert), including sections with unrealistic values for the parameters.
5. (d) Removal of start-up and shut-down transient phases of the TBM ([24]).
2. Smoothing of all parameters with a Gaussian Kernel Smoothing Algorithm with a bandwidth of 30 seconds (3 samples).
3. Standardization of all features (removal of their mean and scaling by their standard deviation)

## 6.3 Optimality Assessment

The parameters determining the proposed optimality function as defined in Section 5.3 are given by

- the slope parameters w 1 = 0 . 8 and w 2 = 3 . 0 ,
- the margin bound on the working pressure for each ground class with 114 bar for GC1, 124 bar for GC2 and 126 bar for GC3.

## 6.4 Baseline Model (Nearest Neighbors)

To evaluate the benefits of our approach, we propose to compare the developed framework to a simpler approach: finding in historic observations points with similar context parameters (CxP) but higher optimality score and using their control parameters (CoP) as recommendation. The idea for this approach is based on the concept that if two observations have similar CxP, but one of the observations has a higher optimality score, the differences can likely be explained by better CoP.

For this baseline, we use a nearest neighbor algorithm (Cover and Hart [5],Chen and Shah [4]). Similarly as described above, we set the numbers of considered neighbours to 15, and propose to recommend for the k -th sample, the Gaussian-weighed average of the CoP of its neighbour set, N ( k ) . Formally this is computed as:

<!-- formula-not-decoded -->

## 6.5 Gradient-Based Recommendations

The neural networks ( cf. Section 5.5) used in this study to learn the relationships between CxP, CoP, and the optimality score were designed in the following way. We performed a grid search on the neural network for the first ground class GC1 with the following parameter ranges: the number of layers (from 2 to 4), the number of neurons (from 30 to 1000 in steps of 10), the dropout rate (from 0 to 0.3 in steps of 0.1) and the learning rate (from 10 - 4 to 10 - 1 in steps of factor 10). We observed that training the network over 200 epochs led to the convergence of the training. Using 10-fold validation, we found that the architecture summarised in Table 2 minimises the ℓ 2 -norm of the difference between the estimated and the ground truth optimality score. This architecture was subsequently used for all neural networks in this work. For illustration purposes, examples of learned versus ground truth optimality scores for each ground class are shown in Figure 2.

Table 2: Hyper-parameters for the applied feed forward neural network

| Parameters of the FNN                                                                                                                       |
|---------------------------------------------------------------------------------------------------------------------------------------------|
| Architecture                                                                                                                                |
| Number of layers : 4 Number of neurons in layer [1-3]: 50 Number of neurons in last layer: 1 Dropout rate: 0.2 Activation function: sigmoid |
| Optimizer                                                                                                                                   |
| Adam Learning rate: 0.01 Decay rate: 0.9 Loss: L2                                                                                           |
| Additional                                                                                                                                  |
| Number of epochs: 200 Batch size: 200                                                                                                       |

Figure 2: Predicted vs. true optimality for (a) GC 1 , (b) GC 2 and (c) GC 3

<!-- image -->

Line chart

## 6.6 Validation Methods

The validation of a recommendation framework in a non-reproducible environment is always challenging if a simulation environment is not available. Indeed, one cannot bore the same tunnel more than once to test different scenarios and the effect of different CoP combinations.

The validation of the proposed framework under real conditions will require that the system is applied in real time to evaluate the operators' actions and to perform a statistical analysis on the overall performance of several operators with and without recommendations (under similar operating conditions).

Since such large-scale experiments are difficult to implement, we propose a surrogate validation method. In our case, only historic data are available for validation and due to the multi-dimensionality of the CoP, different actions might lead to similar effects on the optimality score. A difference between an operator's action and a recommendation cannot be used to invalidate the recommendation. Thus, we propose to evaluate instead the cases where the operators' actions and the recommendations agree. For each CoP, we compute the ratio of cases where the change in optimality score predicted by our model matches the observations. We compute these ratios in two ways. First, we compute this ratio on historic data. This is a reliable indicator but hard to estimate since often, the operator actions and the recommendations do not match. We denote this ratio as 'Synchronised Validation'. Second, to account for the few cases where both the operators' actions and the recommendations match, we propose to find other similar samples in historic data to compare with. Within the samples with similar Context Parameters, identified with the nearest neighbours model, we compare to the sample with the most similar CoP and a different optimality score. We denote this score as 'Contextual Validation'. This second approach also allows us to consider control parameters from other operators during other parts of the project as reference points. Both methods to compute the validation indicators are described in Algorithm 1.

## Algorithm 1 Validation

```
Input: CoP i , CxP i , ∀ i ∈ J 1 .. 5 K 1: V alSV i ← 0 , NumSV i ← 0 ∀ i ∈ J 1 , 5 K 2: V alCV i ← 0 , NumCV i ← 0 ∀ i ∈ J 1 , 5 K 3: for all t timestep available do 4: GC t ← ground class of sample t 5: ̂ CoP t +1 = Recommendation ( CxP t , CoP t , GC t ) 6: for i ∈ J 1 , 5 K do 7: if sign ( ̂ CoP t +1 i ) == sign ( CoP t +1 i ) then 8: NumSV i + = 1 9: if sign ( f opt GC t ( t +1)) == +1 then 10: V alSV i + = 1 11: 12: N t ← 15-closest neighbour set of CxP t 13: t ′ ← Argmin ˆ t ∈N t ‖ ̂ CoP t - CoP ˆ t ‖ 2 14: for i ∈ J 1 , 5 K do 15: if sign ( ̂ CoP t +1 i ) == sign ( CoP t ′ i ) then 16: NumCV i + = 1 17: if sign ( f opt GC t ( t ′ )) == +1 then 18: V alCV i + = 1 19: SV i ← V alSV i /NumSV i ∀ i ∈ J 1 .. 5 K 20: CV i ← V alCV i /NumCV i ∀ i ∈ J 1 .. 5 K 21: SV = Avg i ∈ J 1 , 5 K SV i 22: CV = Avg i ∈ J 1 , 5 K CV i
```

## 7 Results

Both validation scores, for the proposed gradient-based (GB) recommendations and the applied nearest-neighbour baseline (NN) are presented per CoP and per Ground Class in Table 3.

Table 3: Validation Scores: For the two models, Nearest Neighbours (NN) and Gradient-based (GB), the achieved score on the validation set for each control parameter (CoP i in columns), for each geological class (GC i in rows) and for both proposed validation indicators (Synchronized and Contextual). The averages are also reported.

| Synchronized Validation   | Contextual Validation 2 CoP 3 CoP 4 NNGB NNGB NNGB NNGB 62 52 63 61 57 53 48 54 51 53 49 45 42 60 43 58 43 53 51 55 52 57 50 50   |
|---------------------------|-----------------------------------------------------------------------------------------------------------------------------------|

Figure 3: Distributions of the Credibility Scores computed for the three geology ground classes ( GC 1 - GC 3 )

<!-- image -->

Box plot

Figure 4: Gradients over Time for GC1

<!-- image -->

Line chart

Overall, the gradient-based model achieves higher agreement with historic observations, demonstrating the value of the proposed framework.

The 'Contextual Validation' (CV) scores are lower on average compared to the 'Synchronised Validation' (SV). This can have two explanations. First, it can be that some contextual information is not captured by any sensors. This could lead to an hidden discrepancy between neighbouring points. Second, it could also be explained by a lack of sufficiently similar samples in the dataset.

The Synchronised Validation scores in Table 3 are fluctuating less for the NN model than for the GB model: the ranges are 58-63 versus 50-80, 48-63 vs. 50-80 and 52-73 vs. 51-85 for GC 1 , GC 2 and GC 3 respectively. This is expected since the NN model inherently reproduces historic operators actions over all parameters. However, a discussion with the experts validated that the recommendation of the gradient model are very consistent with operators' knowledge on the system. In particular, the gradient model achieves much higher scores for CoP 1 and CoP 4 , which are coincidentally the two parameters for which the model computes the highest gradients as illustrated in Figure 4. The gradient for CoP 1 is mostly positive (the model advises to increase the cutter head rotational speed), which corresponds to the expert feedback that this parameter is the one that operators attempt to maximise. In fact, since thresholds for CoP were not included in the current model, part of the cases where the recommendation and the observations do not agree could be explained by cases where this parameter is already at its maximum setting. In Fig. 4, the gradient for CoP 4 is mostly negative, meaning that the model mostly advises for a decrease of the jacking frame force. This is an interesting insight since higher force should, according to the experts, help with the boring. However, a local change of geology might affect the working pressure in a dangerous way if the jacking frame force is too high. Therefore, the model may be minimising this risk, in particular since we designed our optimality score such as to strongly discourage high working pressure.

For the remaining parameters, CoP 2 has mostly a positive gradient in Fig. 4, that is, the model advises most of the time to increase the nozzle pressure. The experts validated this recommendation since it cleans the head from sticking residuals that lower the excavation capacity. CoP 5 has mostly a negative gradient in Fig. 4, so the model frequently advises to decrease the feed pump that carries the water into the excavation chamber. According to experts, too much water can increase the difficulty of excavation and lead to lower advance rates. Last, the drive line pressure has a very low gradient magnitude on average. Since the drive line controls the transport of the excavation material to the separation unit, experts say that the setting of this parameter mostly depends on the distance between the head of the TBM and the separation unit and is independent of the advance rate and of the working pressure. A gradient close to zero confirms this observation in Figure 4.

These experts' insights, both on the sign and on the magnitude of the gradients confirm the relevance of the recommendations. The magnitude of the gradient can also be interpreted as a measure as to which CoP change would lead to the highest optimality score improvement.

Figure 3 presents the distribution of the computed 'credibility' scores over the three ground classes. GC 1 has the highest median and lowest inter-quartile range which can be explained by a better learning of the optimality function in the neighbourhood of each sample, and by a denser sample distribution. This is in line with the overall best results achieved by both models on GC 1 , in particular for the nearest neighbour baseline.

## 8 Discussion

## 8.1 Data Scarcity

Similarly to any real project, accessing a sufficiently large number of samples for training, validation and testing is of primary importance for the proposed framework. In this project, if the original dataset contained 0.1Hz data for six drives or around 1 million samples. We could only use data from two of the micro-tunnels, that is from 275 000 samples. The other micro-tunnels had large missing gaps, inadequacies within the drilling process or nonavailability of the detailed geology profile. For these two micro-tunnels, after the data pre-processing around 70 000 samples are left, and once we extracted the three homogeneous geologies we are left with around 5 000 samples per section. Last, for the validation set, we could only use samples with control parameter changes (to compare them to the recommendation of the proposed framework). All of these applied constraints for the selection, left only around 2 000 samples per homogeneous geology (around 0.6%). We believe that with more data, the gradient approach will improve further and with the systematization of data collection during operation and with the identification of the most important parameters, the issue of the availability of representative training data should be mitigated in the future.

Figure 5: Frequency of the number of simultaneously adjusted control parameters by the operators over all three ground classes for both selected micro-tunnels.

<!-- image -->

Bar chart

## 8.2 Optimality Definition

In this project, the definition of the optimality score was designed in a simple way to favor high but safe tunnel boring speeds. The proposed function can be tuned to improve the model recommendations. For example, if the model recommendations are too conservative (or respectively not sufficiently conservative) regarding the working pressure, one could lower (resp. increase) the penalizing weights w 1 and w 2 that have a direct effect on the optimality score. More generally, the same framework could be used with much more complex optimality functions. Such more complex optimality functions could include for example financial factors, component degradation or slurry density increase. Before each new each project, the most relevant optimality function for that specific project respecting the needs of the operators can be designed and the model retrained based on historic data.

## 8.3 Unavailable Operator Actions

In this project, we could not access the operator true actions and had to reconstruct them from related measured parameters as explained in Section 6.2. This uncertainty on the true operator actions can propagate to the trained model and to our validation methods. Thereby, it could lower the validation scores. In future projects, we recommend to record operator actions as well as measured parameters to reduce these uncertainties.

## 8.4 Validation Biases

The proposed validation methodology evaluates the recommendations on each parameter independently. This is partly motivated by the gradient approach which computes the partial derivative of the optimality score with respect to each control parameter, that is, assuming that other parameters remain constant. Yet, since the CoP are a multi-dimensional space, their combined actions could be considered together. In practice, we observe that the operators are hardly ever changing the control parameters, and when they do, very few parameters are adjusted at the same time, as illustrated in Figure 5. In 55% of the cases, the operators only adjust one CoP. Without a much larger dataset, it would be highly improbable to find validation points for which the 5 CoP were changed simultaneously in a similar way to the recommendations, given similar CxP. This gap between the model interpretation of the control parameters as a multidimensional space and the observations that only few dimensions are changed at the same time could also explain lower validation computed on historic data.

## 8.5 Credibility Measure

The limitations due to data scarcity and validation bias are captured, to some extend, by the credibility score proposed within this framework. The relatively low observed credibility measures can be linked to the difficulty to find sufficiently representative neighbours for most samples. This lack of relevant neighbours affects the credibility score twice. First, since few data points are available, the model performance in predicting the optimality score will be lower. Second, the credibility score is weighted down by the distance to the neighbours. This score, therefore, plays its role of indicating to which extend the current recommendation is supported by historic data. We expect the overall credibility score to increase as more and more data become available and as the model also learns the optimality score better. Yet, if new conditions are encountered, the credibility will drop, letting the operator know that he or she should proceed with caution.

## 8.6 Computational Complexity

As the amount of available representative data increases, we expect the models to perform better. Yet, this will also affect the computational requirements. The nearest neighbour algorithm complexity at testing time is O ( k log n ) where k is the number of neighbours and n the number of samples [15]. The complexity of the gradient model at testing time is O (1) and is, therefore, expected to scale without any problem to much larger datasets and be more suitable for real-time applications. The credibility measure also relies on the nearest-neighbour algorithm and scales as O ( k log n ) . Yet, as discussed above, we expect that when the dataset becomes sufficiently large, this measure would not be needed anymore. For example, on a normal 3-years old laptop, the Nearest Neighbours model computational time increases from 8.7 to 97.2 seconds when the number of samples increases from 1700 to 5800 in the dataset, while the Gradient-based model's time increases only from 2.60 to 2.85 seconds.

## 9 Conclusion

In this work, we proposed a complete framework for the development of a decision support system for advising TBM operators on how to adjust control parameters in response to rapidly changing conditions. This framework uses the information encoded in sensor data to support the machine operator's control actions directly during the drilling procedure. Thus, it complements existing work to quantify and understand sources of uncertainties and to improve risk management in tunnel construction projects. The proposed framework relies on the definition of an optimality scoring function, which can be designed with expert knowledge as a multi-objective function, such as in our case study, maximising the advance rate while minimising the working pressure. With the defined optimality scoring function, the framework learns from historic data a mapping between environmental conditions, control parameters and the optimality score. It then recommends how to adjust control parameters in order to improve on the optimality score. We proposed in addition a credibility score which analyses the performance of the model on historic data in the neighbourhood of the current conditions. Although the validation of recommendation systems with historic data is challenging, we proposed to evaluate two different matching scores, whose results show consistency between recommendations of the proposed framework and historic data. The recommendations could also be validated and explained by experts, showing high potential for the proposed framework.

Further improvements are to be expected as data will be more and more consistently collected across projects, types of TBM, operators and geological conditions. This could lead to further validation of the framework before its implementation in real conditions. The future development of the framework would greatly benefit from more explorative actions from the operators, which could be encouraged by such recommendation systems. The proposed framework can be implemented in a continuous learning scheme, as data are collected in real time. The natural next step, once a sufficiently robust system will be running and sufficient representative samples are collected, would be to develop the framework further to a reinforcement learning framework. Such approaches are left for future work.

## 10 Acknowledgement

The authors would like to express their gratitude to Herrenknecht AG, Schwanau, Germany, for providing the data and supporting the project with their domain expertise. This work was supported by the Swiss National Science Foundation (SNSF) Grant no. PP00P2-176878.

## References

- [1] Herrenknecht: E-Power Pipe Introduction, 2019. URL https://www.herrenknecht.com/de/ pressematerial-e-power-pipe/ .
- [2] B. D. Argall, S. Chernova, M. Veloso, and B. Browning. A survey of robot learning from demonstration. Robotics and autonomous systems , 57(5):469-483, 2009.
- [3] S. Chandrasekaran and S. K. Govindarajan. Optimization of rate of penetration with real time measurements using machine learning and meta-heuristic algorithm. International Journal of Scientific and Technology Research , 8:1427-1432, 10 2019.
- [4] G. Chen and D. Shah. Explaining the success of nearest neighbor methods in prediction. Foundations and Trends® in Machine Learning , 10:337-588, 01 2018. doi: 10.1561/2200000064.

- [5] T. Cover and P. Hart. Nearest neighbor pattern classification. IEEE Transactions on Information Theory , 13: 21-27, 01 1967.
- [6] H. Einstein. Decision aids for tunneling: Update. Transportation Research Record , 1892:199-207, 01 2004. doi: 10.3141/1892-21.
- [7] H. Einstein, M. A. Kaabi, H. Chan, A. Costa, J.-P. Dudt, C. Haas, C. Indermitte, K. Karam, C. Kollarou, C. Marzer, et al. Risk determination for tunnels and other networked infrastructure. In Geo-Risk 2017 , pages 346-367. 06 2017. doi: 10.1061/9780784480724.032.
- [8] H. H. Einstein, C. Indermitte, J. Sinfield, F. P. Descoeudres, and J. P. Dudt. Decision aids for tunneling. Transportation Research Record , 1998. ISSN 03611981. doi: 10.1061/9780784415139.ch07.
- [9] C. Haas and H. H. Einstein. Updating the decision aids for tunneling. Journal of construction engineering and management , 128(1):40-48, 2002.
- [10] W. Jiang, R. Samuel, et al. Optimization of rate of penetration in a convoluted drilling framework using ant colony optimization. In IADC/SPE Drilling Conference and Exhibition . Society of Petroleum Engineers, 2016. doi: 10.2118/178847-MS.
- [11] A. Krizhevsky, I. Sutskever, and G. E. Hinton. Imagenet classification with deep convolutional neural networks. In F. Pereira, C. J. C. Burges, L. Bottou, and K. Q. Weinberger, editors, Advances in Neural Information Processing Systems 25 , pages 1097-1105. Curran Associates, Inc., 2012. URL http://papers.nips.cc/paper/ 4824-imagenet-classification-with-deep-convolutional-neural-networks.pdf .
- [12] R. Mikaeil, S. Shaffiee Haghshenas, and Z. Sedaghati. Geotechnical risk evaluation of tunneling projects using optimization techniques (case study: the second part of emamzade hashem tunnel). Natural Hazards , 07 2019. doi: 10.1007/s11069-019-03688-z.
- [13] S. Min and H. Einstein. Resource scheduling and planning for tunneling with a new resource model of the decision aids for tunneling (dat). Tunnelling and Underground Space Technology , 51:212-225, 01 2016. doi: 10.1016/j.tust.2015.10.038.
- [14] M. Mooney, B. Walter, J. Steele, D. Cano, G. Davidson, A. Howard, L. Jacobs, R. Pintabona, and B. Zernich. Influence of geological conditions on measured tbm vibration frequency. In Society for Mining, Metallurgy &amp; Exploration , pages 32-41, 2014. ISBN 9780873354004.
- [15] A. Moore. An introductory tutorial on kd-trees. Technical Report Technical Report No. 209, Computer Laboratory, University of Cambridge, Carnegie Mellon University, Pittsburgh, PA, January 1991.
- [16] Y. Moret and H. H. Einstein. Construction cost and duration uncertainty model: application to high-speed rail line project. Journal of Construction Engineering and Management , 142(10):05016010, 2016.
- [17] M. Pawlowsky. Geology change detection in mechanized tunneling using machine learning . Master's thesis, Swiss Federal Institute of Technology, 2019.
- [18] G. S. Payette, D. Pais, B. Spivey, L. Wang, J. R. Bailey, P. Pastusek, M. Owens, et al. Mitigating drilling dysfunction using a drilling advisory system: results from recent field applications. In International Petroleum Technology Conference , pages 1-23. International Petroleum Technology Conference, 2015.
- [19] D. Sanderson, G. Payette, B. Spivey, J. Bailey, R. Kong, and A. Eddy. Field application of a real-time well-site drilling advisory system in the permian basin. In Proceedings of the 5th Unconventional Resources Technology Conference 2017 , 01 2017. doi: 10.15530/urtec-2017-2670861.
- [20] R. Self, A. Atashnezhad, and G. Hareland. Reducing drilling cost by finding optimal operational parameters using particle swarm algorithm. SPE Deepwater Drilling &amp; Completions Conference held in Galveston, Texas, USA, 14-15 September 2016 , 08 2016.
- [21] R. L. Sousa and H. H. Einstein. Risk analysis during tunnel construction using Bayesian Networks: Porto Metro case study. Tunnelling and Underground Space Technology , 2012. ISSN 08867798. doi: 10.1016/j.tust.2011.07. 003.
- [22] C. Szegedy, W. Liu, Y. Jia, P. Sermanet, S. Reed, D. Anguelov, D. Erhan, V. Vanhoucke, and A. Rabinovich. Going deeper with convolutions, 2014.
- [23] F. Wang, H. Li, C. Dong, and L. Ding. Knowledge representation using non-parametric bayesian networks for tunneling risk analysis. Reliability Engineering &amp; System Safety , 191:106529, 06 2019. doi: 10.1016/j.ress. 2019.106529.
- [24] Q. Zhang, Z. Liu, and J. Tan. Prediction of geological conditions for a tunnel boring machine using big operational data. Automation in Construction , 2019. ISSN 09265805. doi: 10.1016/j.autcon.2018.12.022.

- [25] J. Zhao, M. Shi, G. Hu, X. Song, C. Zhang, D. Tao, and W. Wu. A Data-Driven Framework for Tunnel Geological-Type Prediction Based on TBM Operating Data. IEEE Access , 2019. ISSN 21693536. doi: 10.1109/ACCESS.2019.2917756.
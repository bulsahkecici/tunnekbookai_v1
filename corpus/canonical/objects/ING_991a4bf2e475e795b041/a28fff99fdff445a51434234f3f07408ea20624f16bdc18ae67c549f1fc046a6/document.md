<!-- image -->

Logo

Article

## Supervised Machine Learning Techniques to the Prediction of Tunnel Boring Machine Penetration Rate

<!-- image -->

Icon

<!-- image -->

Icon

<!-- image -->

Icon

Hai Xu 1 , Jian Zhou 1 , Panagiotis G. Asteris 2, * , Danial Jahed Armaghani 3, * and Mahmood Md Tahir 4

- 1 School of Resources and Safety Engineering, Central South University, Changsha 410083, China
- 2 Computational Mechanics Laboratory, School of Pedagogical and Technological Education, 14121 Heraklion, Athens, Greece
- 3 Institute of Research and Development, Duy Tan University, Da Nang 550000, Vietnam
- 4 UTMConstruction Research Centre, Institute for Smart Infrastructure and Innovative Construction (ISIIC), School of Civil Engineering, Faculty of Engineering, Universiti Teknologi Malaysia, Johor Bahru 81310, Malaysia
* Correspondence: panagiotisasteris@gmail.com (P.G.A.); danialarmaghani@gmail.com (D.J.A.); Tel.: + 30-210-2896922 (P.G.A.); + 60-196-438320 (D.J.A.)

Received: 14 July 2019; Accepted: 28 August 2019; Published: 6 September 2019

<!-- image -->

Logo

Abstract: Predicting the penetration rate is a complex and challenging task due to the interaction between the tunnel boring machine (TBM) and the rock mass. Many studies highlight the use of empirical and theoretical techniques in predicting TBM performance. However, reliable performance prediction of TBM is of crucial importance to mining and civil projects as it can minimize the risks associated with capital costs. This study presents new applications of supervised machine learning techniques, i.e., k-nearest neighbor (KNN), chi-squared automatic interaction detection (CHAID), support vector machine (SVM), classification and regression trees (CART) and neural network (NN) in predicting the penetration rate (PR) of a TBM. To achieve this aim, an experimental database was set up, based on field observations and laboratory tests for a tunneling project in Malaysia. In the database, uniaxial compressive strength, Brazilian tensile strength, rock quality designation, weathering zone, thrust force, and revolution per minute were utilized as inputs to predict PR of TBM. Then, KNN, CHAID, SVM, CART, and NN predictive models were developed to select the best one. Asimple ranking technique, as well as some performance indices, were calculated for each developed model. According to the obtained results, KNN received the highest-ranking value among all five predictive models and was selected as the best predictive model of this study. It can be concluded that KNN is able to provide high-performance capacity in predicting TBM PR. KNN model identified uniaxial compressive strength (0.2) as the most important and revolution per minutes (0.14) as the least important factor for predicting the TBM penetration rate.

Keywords: tunnel boring machine performance; penetration rate; machine learning technique; predictive model

## 1. Introduction

The prediction of tunnel boring machine (TBM) performance in a specified rock mass condition is a longstanding research area. Suitable prediction of TBM performance parameters, notably the penetration rate (PR) and the advance rate (AR), can reduce the risks related to high capital costs, which are very common for mechanized excavation operations. This is an essential task for planning tunnel projects and selecting suitable construction methods. During the past decades, several empirical techniques have been developed for forecasting the performance parameters of TBM: PR, and AR [1-7].

<!-- image -->

Logo

In the aforementioned models / classifications, the most influential factors of rock mass and material, such as compressive and tensile strengths and joint conditions, as well as of machine specifications, such as average cutter force, and cutter-head torque, were utilized as predictors. A PR model was introduced by Farmer and Glossop [8] based on the tensile strength of the rock and average cutter force. In another study, conducted by Sanio [3], specific energy was predicted using values of uniaxial compressive strength (UCS) of the rock. Ozdemir [9] developed the Colorado School of Mines (CSM) model based on a database comprising of cutter and rock properties to estimate the cutter forces. The CSM model has since been modified several times by Rostami [5], Yagiz and Ozdemir [10], and Yagiz [11], by adding the e ects of rock mass brittleness and rock mass fracture properties. Although these models have several inputs, most of these studies rely on rock properties, such as strength, joint spacing, and brittleness, as inputs into the established techniques [12-16].

Several studies used traditional statistical and linear techniques to predict TBM performance [17,18]. However, these techniques have been criticized, because of their disadvantages in solving highly complex and nonlinear problems. Grima et al. [19] mentioned that statistical models are not always robust enough to accurately describe nonlinear and complex systems. Moreover, their performance capacity is diminished in the presence of outliers and extreme values in the data. Furthermore, Farrokh et al. [20] stated that multiple parameters' models use more project-specific data (compared to simple models), and are more easily applied (compared to computer-aided models). It should be mentioned that the performance capacities of the multiple parameters models are higher than those of simple parameter models. This is due to the use of more related input parameters. Hence, it seems that artificial intelligence (AI) and machine learning (ML) techniques can be the best choice to be applied for prediction of TBM performance using multiple input parameters.

AI and ML techniques (Table 1), such as artificial neural network (ANN), support vector machine (SVM), particle swarm optimization (PSO), and fuzzy inference system (FIS) have been widely used for solving problems in civil engineering and, more specifically, for TBM performance parameters [21-35]. ANN models were developed by Benardos and Kaliampakos [36] and Yagiz et al. [17] to predict TBM PR. Hybrid ANN models of PSO-ANN and imperialist competitive algorithm (ICA)-ANN were developed to approximate PR and AR of TBMs in the study conducted by Armaghani et al. [12] and [37], respectively. Recently, Koopialipoor et al. [13] developed a new model to predict the tunnel boring machine performance based on the group method of data handling. A gene expression programming (GEP) was introduced by Armaghani et al. [38] for estimating PR values obtained from a transfer tunnel in Malaysia.

Table 1. Published research on tunnel boring machine (TBM) performance prediction using related artificial intelligence (AI) and machine learning (ML) techniques.

|                                | Technique   | Parameters                                                            | Parameters   | Datasets / Description           |
|--------------------------------|-------------|-----------------------------------------------------------------------|--------------|----------------------------------|
| Reference                      |             | Input                                                                 | Output       |                                  |
| Alvarez Grima [19]             | ANN         | CFF, Dc, RPM, TF, UCS                                                 | AR, PR       | 640 TBM projects                 |
| Bernardos and Kaliampakos [36] | ANN         | N, overburden, permeability, RMR, rock mass weathering RQD, UCS, WTS, | AR           | Athens metro tunnel              |
| Yagiz [17]                     | ANN         | BI, DPW, UCS, α                                                       | PR           | 151 datasets                     |
| Eftekhari et al. [39]          | ANN         | BTS, CT, Qu, RMR, Rock Type, RQD, Rs TF, UCS                          | PR           | 10 km data excavated in a tunnel |
| Gholamnejad and Tayarani [40]  | ANN         | DPW, RQD, UCS                                                         | PR           | 185 datasets                     |

Table 1. Cont.

| Reference                | Technique        | Parameters                           | Parameters   | Datasets / Description               |
|--------------------------|------------------|--------------------------------------|--------------|--------------------------------------|
|                          |                  | Input                                | Output       |                                      |
| Gholami et al. [41]      | ANN              | Jc, Js, RQD, UCS                     | PR           | 121 tunnel sections                  |
| Salimi and Esmaeili [42] | ANN              | BTS, DPW, PSI, UCS, α                | PR           | 46 sections of a water supply tunnel |
| Torabi et al. [43]       | ANN              | C, UCS, υ , ϕ                        | PR, UI       | 39 sections of a highway project     |
| Shao et al. [44]         | ELM              | BTS, DPW, PSI, UCS, α                | PR           | 153 datasets                         |
| Mahdevari et al. [45]    | SVR              | BI, BTS, CP, CT, DPW, SE, TF, UCS, α | PR           | 150 datasets                         |
| Armaghani et al. [12]    | PSO-ANN, ICA-ANN | BTS, UCS, RMR, RQD, TF, WZ, RPM      | PR           | 1286 datasets                        |
| Armaghani et al. [37]    | PSO-ANN, ICA-ANN | Qu, BTS, UCS, RMR, RQD, TF, WZ, RPM  | AR           | 1286 datasets                        |
| Koopialipoor et al. [46] | FA-ANN           | BTS, UCS, RMR, RQD, TF, WZ, RPM      | PR           | 1200 datasets                        |
| Koopialipoor et al. [47] | DNN              | BTS, UCS, RMR, RQD, TF, WZ, RPM      | PR           | 1286 datasets                        |

While the use of AI techniques has attracted more attention than the use of other techniques, such as ML, in the field of tunneling the main aim of AI is the development of reliable and robust models. On the other hand, ML techniques seek to enhance accuracy, which is desirable for any prediction model. Since the TBM PR is a continuous target variable, the supervised ML techniques, such as SVM, nearest neighbor and decision trees (DTs) should be used for classification and regression of TBM data. Supervised ML approaches are powerful due to their ability to solve problems in science and engineering and obtaining a high accuracy level for prediction purposes, especially when dealing with highly complex and nonlinear problems [48-50].

This study aims to evaluate the use of various ML techniques in predicting the TBM PR. In this study, five ML techniques are developed to predict PR of TBM in hard rock conditions. The proposed models are compared in terms of accuracy and performance, to select the best models among them. This comparison helps decrease future work expended on choosing appropriate techniques / procedures for analysis of TBM and tunneling data. Thus, the importance of input variables to calculate the TBM PR is estimated and assessed using the selected models. This 'importance' calculation can enable a better understanding of the predictive capacity of di erent input parameters.

It is extremely helpful to obtain prior knowledge of the TBM performance in rock excavation projects. This allows for planning construction time and for controlling cost, as well as choosing the excavation method. Several studies noted that predicting the penetration rate is a complex and di cult task because of the interaction between the TBM and rock mass. According to Jamshidi [51], TBMpenetration rate directly influences the advance rate, which represents the total distance excavated by the machine divided by the total time. While there is a high cost associated with tunneling projects and using the TBM, utilizing prediction methods, especially ML techniques for predicting the penetration rate of TBM can significantly reduce the total time and cost of the tunneling projects. On the other hand, more investigations are needed in the field of TBM performance when there are di erent weathering zones in the rock-mass. As stated in several studies [6,52-57], the degree of rock-mass weathering has an enormous impact on rock mass properties as well as TBM performance. Hence, weathering index is used as an important input parameter in this study to predict TBM PR. In the following sections, the background of the applied ML models is described, and then, after developments of ML techniques, the best model among them will be selected for PR prediction.

## 2. Background of Supervised ML Models

## 2.1. K-Nearest Neighbor (KNN)

The k-nearest neighbor (KNN) is a non-parametric approach that was widely applied to statistics in the early 1970s [58,59]. According to Wu et al. [60], KNN is regarded as one of the top 10 algorithms in data mining, due to its simplicity, e ectiveness, and implementation. The KNN-based classification technique can be e ectively applied in several real-world and practical classification tasks in several fields, such as expert and intelligence systems. The KNN finds a group of k samples (e.g., using the distance functions) which are closest to unknown samples in the calibration dataset, constituting the basic theory of KNN. The KNN also determines the label (class) of unknown samples among the k samples through the calculation of the average of the response variables [61,62]. Consequently, k plays a significant role in the performance of the KNN [63].

## 2.2. Support Vector Machine (SVM)

Support vector machines (SVMs) is one of the most widely used algorithms for classification and regression problems [64]. This algorithm can e ectively work with high dimensional and linearly non-separable datasets [48,65]. The basic theory behind the SVM is the statistical learning theory [66]. Kernel functions, such as linear, radial basis function, sigmoid and polynomial, also a ect the SVM performance [67]. According to Hong et al. [65], the main aim of the SVM classifier is to identify an ideal separation hyperplane that can distinguish the two classes. The other advantages of SVM include a reduction in both the error (for training and testing datasets) and model complexity [68].

## 2.3. Neural Network (NN)

The basic structure of an ANN is the artificial neuron, that is, a mathematical model which resembles the behavior of the biological neuron, but with a plethora of activation functions enabling the biological neuron's mainly sigmoid activation function [69]. To be precise, it should be noted that the scientists have decoded only a small amount of the biological neural networks (BNNs) structure, behavior, and functions. Therefore, to be exact, the similarity between biological and artificial neural networks is based mainly on morphological characteristics. Concerning the practical terms, NNs are non-linear statistical data modeling techniques or tools of decision making. The NN can find patterns in data, or unveil relations between inputs (dependent parameters) and output (independent parameter). NNs can be applied to di erent fields, such as function approximation, classification, and data processing. In NNs, the weights denote the connections of the biological neuron. An excitatory connection is reflected by a positive weight, while an inhibitory connection is reflected by a negative value.

## 2.4. Classification and Regression Trees (CART)

Classification and regression trees (CART) is a binary DT which was developed by Breiman et al. [70]. This modeling approach aims to find the best possible split. For various types of variables, the CART categorize values of the input variables from smallest to largest values. To identify the best split point, the technique makes a trial split. For instance, if the call split point is called 'S', then all the cases with value below 'S' go to the left, forming the child node (X &lt; S). Otherwise, instances are sent to the right child node (X &gt; S). The CART seeks to reduce the impurity of the leaf nodes to choose the best data partition. Three potential indices are considered in CART technique for selecting the best data partition: Gini criterion entropy, and Twoing criterion. The CART performance is a ected by the selection of these indices. The best prediction performance can be obtained when the perfect selection of indices has been accomplished.

## 2.5. Chi-Squared Automatic Interaction Detection (CHAID)

Chi-squared automatic interaction detection (CHAID) is a data mining algorithm and DT which was developed by Kass [71]. This algorithm grew a DT by several sequential combinations and splits, based on Chi-square test. The CHAID is a tree-based structure technique, which is a combination of a group rule classifiers. This technique creates a tree structure of the dependent parameters to predict the independent parameter. The ratio of records having the specific value for the target variable to the given values for the independent variables denotes the confidence (accuracy) of the created rules. The CHAID attempts to produce wider and non-binary trees. Besides, it automatically prunes the DT to avoid overfitting.

## 3. Materials and Methods

The present study uses a ranking system to identify the most accurate model to predict PR. The models that are used in this study are KNN, SVM, NN, CART, and CHAID. These supervised techniques were selected because of their e ectiveness to predict the continuous target variables, as well as on account of their wide applicability. The parameters that were used to develop the abovementioned models are presented in Table 2. To develop the models, the authors used IBM SPSS modeler 18. The details of the methods implemented to assess the selected techniques and dataset preparation are presented in the following sub-sections.

Table 2. Parameters of the algorithms used in this study.

| KNN                                                                                                                                                                                                                                                                                                                                     | SVM                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Number of nearest neighbors (k): Minimum 3 and maximum 5 Distance computation: Euclidean metric Prediction for range target: Mean of nearest neighbor values Stopping criteria: Stop when the 10 features have been selected                                                                                                            | Stopping criteria: 1.E-3 Regularization parameter (C): 10 Regression precision (epsilon): 0.1 Kernel type: RBF RBF gamma: 0.1                                                                                                                                                                                                                                                                                                                                        |
| NN                                                                                                                                                                                                                                                                                                                                      | CHAID                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| NNmodel: Multilayer perceptron (MLP) Stopping rules: Use maximum training time (per component model): 15 minutes Combining rule for continuous targets: Mean Number of component models for boosting and / or bagging: 10 Overfit prevention set (%): 30 Missing values in predictors: Delete listwise                                  | Tree growing algorithm: CHAID Maximum tree depth: 5 Minimum records in parent branch (%): 2 Minimum records in child branch (%): 1 Combining rule for continuous targets: Mean Number of component models for boosting and / or bagging: 10 Significance level for splitting: 0.05 Significance level for merging: 0.05 Adjust significance values using Boferroni method Minimum change in expected cell frequencies: 0.001 Maximum iterations for convergence: 100 |
| CART                                                                                                                                                                                                                                                                                                                                    |                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| Maximum tree depth: 5 Prune tree to avoid overfitting: maximum surrogates: 5 Minimum records in parent branch (%): 2 Minimum records in child branch (%): 1 Combining rule for continuous targets: mean Number of component models for boosting and / or bagging: 10 Minimum change in impurity: 0.0001 Over-fit prevention set (%): 30 | Maximum tree depth: 5 Prune tree to avoid overfitting: maximum surrogates: 5 Minimum records in parent branch (%): 2 Minimum records in child branch (%): 1 Combining rule for continuous targets: mean Number of component models for boosting and / or bagging: 10 Minimum change in impurity: 0.0001 Over-fit prevention set (%): 30                                                                                                                              |

## 3.1. Model's Assessment

In this study, four performance indices, namely coe cient of determination ( R 2 ), mean absolute error ( MAE ), root mean square error ( RMSE ), and variance account for ( VAF ), were used to measure the prediction performance and accuracy of the developed models. These indices are widely used to assess the accuracy of the developed models in the related studies as well [72-79]. Furthermore, the recently proposed a 20 - index have been used for the evaluation of models. These indices are computed as follows:

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

where y denotes the measured values, ¯ y and y 0 indicate mean and predicted the values of y, respectively, N denotes the total number of data. Note that, a predictive model with R 2 of 1, VAF of 100%, and RMSE and MAE of zero is defined as a perfect model. The dataset should be divided into two phases (i.e., training and testing) to develop the model and then evaluate the developed model. Thus, in this study, according to suggestions of several studies [21,80-82], 80% of the collected data (or 167 datasets) are randomly selected to train the models and the remaining 20% of the data (or 42 datasets) are used to test and validate the models. The simple ranking technique proposed by Zorlu et al. [83] was used in this research. According to this technique, the total rate of each model is calculated for training and testing dataset, separately. The highest rate value for each performance index is five because we have five models, and the best performance index is assigned the highest rating (5). The total performance rating of each model is then calculated by summing up its total rank of training and total rank of the testing dataset. More information regarding the simple ranking technique can be found in the original study, Zorlu et al. [83].

Furthermore, the following, recently proposed engineering index, the a 20 - index , is proposed for the reliability assessment of the developed AI models:

<!-- formula-not-decoded -->

where M is the number of dataset samples and m 20 is the number of samples with a value of rate experimental value / predicted value between 0.80 and 1.20. Note that for a perfect predictive model, the values of a 20 -index values are expected to be unity. The proposed a 20 - index has the advantage that their value has a physical engineering meaning. It declares the amount of the samples that satisfies predicted values with a deviation of 20% compared to experimental values.

## 3.2. Case Study and Data Preparation

Atunnel project (PSRWT, Pahang-Selangor raw water transfer) with a total length of 44.6 km and a diameter of 5.23 m was planned and constructed in Malaysia. This tunnel aims to transfer water from Pahang state to Selangor state. PSRWT tunnel was excavated in a mountain area of Peninsular Malaysia, where six major faults were observed with an elevation range from 100 to 1200 m. In the field, rock strength is poor in areas of fault intersections and highly to moderately weathered zones were observed along the tunnel. Di erent rock types including shale, coarse-grained granite, and medium-grained granite were observed in various tunnel distances (TDs) of PSRWT tunnel. Regarding construction techniques for the tunnel excavation, there were seven parts, comprising four parts of NATMand three parts of TBM. In PSRWT tunnel project, 11,761 m in the mixed ground, 11,761 m in very hard ground and 11,218 m in the blocky ground were excavated by three TBMs. Construction's of PSRWT tunnel with their maximum overburden are shown in Figure 1. Regarding construction techniques for the tunnel excavation, there were seven parts, comprising four parts of NATM and three parts of TBM. In PSRWT tunnel project, 11,761 m in the mixed ground, 11,761 m in very hard ground and 11,218 m in the blocky ground were excavated by three TBMs. Construction sections of PSRWT tunnel with their maximum overburden are shown in Figure 1.

Figure 1. Seven construction parts of the Pahang-Selangor raw water transfer (PSRWT) tunnel with their maximum overburden. Figure 1. Seven construction parts of the Pahang-Selangor raw water transfer (PSRWT) tunnel with their maximum overburden.

<!-- image -->

Geographical map

There  is  a  need  to  have  a  suitable  database  with  the  most  effective  parameters  of  TBM performance for prediction of TBM PR. The most effective parameters on TBM performance can be identified  by  reviewing  the  previous  related  studies.  Based  on  the  literature,  three  groups  of parameters  are  found  as  the  most  effective  factors  of  TBM  performance,  including  machine characteristics, rock mass, and rock material properties [84]. According to Benardos and Kaliampakos [36],  the  most  important parameters affecting the TBM performance are rock quality designation (RQD), UCS, rock-mass weathering, and rock mass rating (RMR). As some researchers (e.g., [52,53]) have concluded and pointed out, the rock mass weathering can significantly affect the TBM PR. Sapigni et al. [85] found that UCS and RMR can significantly affect the TBM performance. They also noticed that the Brazilian tensile strength (BTS) could be set as an input parameter. Grima et al. [19] found an inverse relationship between PR and UCS. Farrokh et al. [20] showed in their research that factors  such  as  RQD,  the  diameter  of  tunnel,  UCS,  type  of  rock,  disc-cutter  normal  force,  and revolution per minute (RPM) were of the highest influence on PR. Whereas, Mahdevari et al. [45] introduced a different list in this term, including UCS, BTS, intact rock brittleness (BI), cutter head power (CP), cutter-head torque (CT), the distance between the plane of weakness (DPW), and thrust force (TF). An investigation of about 13 km was conducted in the PSRWT tunnel and a database with 209 datasets was prepared. Rock type in the investigated areas was granite covering three weathering zones, i.e., fresh, slightly weathered, and moderately weathered. According to International Society of  Rock  Mechanics (ISRM) [86], a  typical  rock  weathering  profile  is  composed  of  six  weathering grades  namely  fresh,  slightly  weathered,  moderately  weathered,  highly  weathered,  completely weathered, and residual soil. This classification is mainly based on discoloration and decomposition of the rock material. Based on tunnel mapping 34,740 m of PSRWT tunnel which was excavated by TBMs, a total of 12,649 m comprising 5443 m in fresh, 5530 m in slightly weathered, and 1676 m in moderately weathered zones, was observed. In this study, in terms of rock mass properties, many points  in  three  TBMs  were  investigated  and  several  rock  mass  properties,  such  as  type  of  rock, strength, degree of weathering, joint condition (e.g., spacing of discontinuities, alteration, degree of roughness, infilling material), and groundwater condition, were quantified and database established. Furthermore, machine characteristics, such as TF, RPM, PR, AR, boring energy, stroke speed, and cutterhead  torque,  were  recorded  by  TBMs.  For  rock  material  evaluation,  more  than  100  block samples were collected from the face of PSRWT tunnel project and after transferring to the laboratory, several tests, e.g., density, BTS, point load strength, Schmidt hammer, p-wave velocity, and UCS were carried  out  based  on  ISRM  [86].  According  to  several  authors  [54,55,87-92],  the  most  known There is a need to have a suitable database with the most e ective parameters of TBM performance for prediction of TBM PR. The most e ective parameters on TBM performance can be identified by reviewing the previous related studies. Based on the literature, three groups of parameters are found as the most e ective factors of TBM performance, including machine characteristics, rock mass, and rock material properties [84]. According to Benardos and Kaliampakos [36], the most important parameters a ecting the TBM performance are rock quality designation (RQD), UCS, rock-mass weathering, and rock mass rating (RMR). As some researchers (e.g., [52,53]) have concluded and pointed out, the rock mass weathering can significantly a ect the TBM PR. Sapigni et al. [85] found that UCS and RMR can significantly a ect the TBM performance. They also noticed that the Brazilian tensile strength (BTS) could be set as an input parameter. Grima et al. [19] found an inverse relationship between PR and UCS. Farrokh et al. [20] showed in their research that factors such as RQD, the diameter of tunnel, UCS, type of rock, disc-cutter normal force, and revolution per minute (RPM) were of the highest influence on PR. Whereas, Mahdevari et al. [45] introduced a di erent list in this term, including UCS, BTS, intact rock brittleness (BI), cutter head power (CP), cutter-head torque (CT), the distance between the plane of weakness (DPW), and thrust force (TF). An investigation of about 13 km was conducted in the PSRWT tunnel and a database with 209 datasets was prepared. Rock type in the investigated areas was granite covering three weathering zones, i.e., fresh, slightly weathered, and moderately weathered. According to International Society of Rock Mechanics (ISRM) [86], a typical rock weathering profile is composed of six weathering grades namely fresh, slightly weathered, moderately weathered, highly weathered, completely weathered, and residual soil. This classification is mainly based on discoloration and decomposition of the rock material. Based on tunnel mapping 34,740 m of PSRWT tunnel which was excavated by TBMs, a total of 12,649 m comprising 5443 m in fresh, 5530 m in slightly weathered, and 1676 m in moderately weathered zones, was observed. In this study, in terms of rock mass properties, many points in three TBMs were investigated and several rock mass properties, such as type of rock, strength, degree of weathering, joint condition (e.g., spacing of discontinuities, alteration, degree of roughness, infilling material), and groundwater condition, were quantified and database established. Furthermore, machine characteristics, such as TF, RPM, PR, AR, boring energy, stroke speed, and cutterhead torque, were recorded by TBMs. For rock material evaluation, more than 100 block samples were collected from the face of PSRWT tunnel project and after transferring to the laboratory, several tests, e.g., density, BTS, point load strength, Schmidt hammer, p-wave velocity, and UCS were carried out based on ISRM [86]. According to several authors [54,55,87-92], the most known geomechanical tests used to establish the quality state of the rock masses are RQD, Schmidt hammer, UCS, p-wave velocity, etc. A failed sample under Brazilian test conducted in the laboratory is shown in Figure 2. Besides, a conducted UCS test on a sample before and after failure is shown in Figure 3. geomechanical tests used to establish the quality state of the rock masses are RQD, Schmidt hammer, UCS, p-wave velocity, etc. A failed sample under Brazilian test conducted in the laboratory is shown in Figure 2. Besides, a conducted UCS test on a sample before and after failure is shown in Figure 3. Appl. Sci. 2019 , 9 , x FOR PEER REVIEW 8 of 19 geomechanical tests used to establish the quality state of the rock masses are RQD, Schmidt hammer, UCS, p-wave velocity, etc. A failed sample under Brazilian test conducted in the laboratory is shown in Figure 2. Besides, a conducted UCS test on a sample before and after failure is shown in Figure 3.

Figure 2. Failure of a sample collected from the tunnel project (tunnel boring machine (TBM) 1, tunnel distance = 3200 m) under Brazilian test. Figure 2. Failure of a sample collected from the tunnel project (tunnel boring machine (TBM) 1, tunnel distance = 3200 m) under Brazilian test. Figure 2. Failure of a sample collected from the tunnel project (tunnel boring machine (TBM) 1, tunnel distance = 3200 m) under Brazilian test.

<!-- image -->

Photograph

Figure 3. Uniaxial compressive strength (UCS) test conducted on a sample of TBM 2, tunnel distance = 9300 m, ( a ) before failure, ( b ) after failure. Figure 3. Uniaxial compressive strength (UCS) test conducted on a sample of TBM 2, tunnel distance = 9300 m, ( a ) before failure, ( b ) after failure. Figure 3. Uniaxial compressive strength (UCS) test conducted on a sample of TBM 2, tunnel distance = 9300 m, ( a ) before failure, ( b ) after failure.

<!-- image -->

Photograph

In this study, based on the literature review, available field observations, and laboratory tests, six parameters, UCS, BTS, RQD, WZ, TF, and RPM, were selected as model inputs to estimate TBM PR. It is important to mention that RQD was calculated based on the method suggested by Bieniawski [93]. Note that value was assigned to each WZ in the used datasets, i.e., 1, 2, and 3 were assigned to fresh, slightly weathered, and moderately weathered, respectively. Table 3 presents a basic statistical description  of  the  experimental  database  applied  in  the  current  research.  For  more  information regarding the data used in this study, the correlation matrix of input and output variables for all 209 cases is shown in Figure 4. High negative or positive values of the correlation coefficient between the input variables may result in poor efficiency of the methods and a difficulty in construing the effects of  the  expository  variables  on  the  response.  As  can  be  seen  in  Figure  4,  there  are  no  significant In this study, based on the literature review, available field observations, and laboratory tests, six parameters, UCS, BTS, RQD, WZ, TF, and RPM, were selected as model inputs to estimate TBM PR. It is important to mention that RQD was calculated based on the method suggested by Bieniawski [93]. Note that value was assigned to each WZ in the used datasets, i.e., 1, 2, and 3 were assigned to fresh, slightly weathered, and moderately weathered, respectively. Table 3 presents a basic statistical description  of  the  experimental  database  applied  in  the  current  research.  For  more  information regarding the data used in this study, the correlation matrix of input and output variables for all 209 cases is shown in Figure 4. High negative or positive values of the correlation coefficient between the input variables may result in poor efficiency of the methods and a difficulty in construing the effects of  the  expository  variables  on  the  response.  As  can  be  seen  in  Figure  4,  there  are  no  significant In this study, based on the literature review, available field observations, and laboratory tests, six parameters, UCS, BTS, RQD, WZ, TF, and RPM, were selected as model inputs to estimate TBM PR. It is important to mention that RQD was calculated based on the method suggested by Bieniawski [93]. Note that value was assigned to each WZ in the used datasets, i.e., 1, 2, and 3 were assigned to fresh, slightly weathered, and moderately weathered, respectively. Table 3 presents a basic statistical description of the experimental database applied in the current research. For more information regarding the data used in this study, the correlation matrix of input and output variables for all 209 cases is shown in Figure 4. High negative or positive values of the correlation coe cient between the input variables may result in poor e ciency of the methods and a di culty in construing the e ects of the expository variables on the response. As can be seen in Figure 4, there are no significant correlations between the independent input variables. Additionally, a detailed flowchart of this study for the prediction of TBM PR is presented in Figure 5. According to this flowchart, after literature review and site selection, data collection is divided into two sections of laboratory tests and field observation. Therefore, all influential parameters on TBM performance are recorded and considered as model inputs. To predict TBM PR, SVM, KNN, CHAID, NN, and CART are applied and developed. Then, an evaluation will be performed for each model and the best one among them will be selected and introduced as the best predictive model. In the following sections, the modeling process of ML techniques for the PR estimation and their evaluations based on performance indices will be explained. correlations between the independent input variables. Additionally, a detailed flowchart of this study for the prediction of TBM PR is presented in Figure 5. According to this flowchart, after literature review and site selection, data collection is divided into two sections of laboratory tests and field observation. Therefore, all influential parameters on TBM performance are recorded and considered as  model  inputs.  To  predict  TBM  PR,  SVM,  KNN,  CHAID,  NN,  and  CART  are  applied  and developed. Then, an evaluation will be performed for each model and the best one among them will be selected and introduced as the best predictive model. In the following sections, the modeling process of ML techniques for the PR estimation and their evaluations based on performance indices will be explained.

Table 3. Descriptive statistics of the experimental database used in this research. Table 3. Descriptive statistics of the experimental database used in this research.

| Parameter Parameter                                         | Type Type     | Symbol Symbol   | Unit Unit         | Min Min   | Max Max     | Average Average   | St Dev St Dev   |
|-------------------------------------------------------------|---------------|-----------------|-------------------|-----------|-------------|-------------------|-----------------|
| Rock quality designation Rock quality designation           | Input Input   | RQD RQD         | % %               | 10 10     | 95 95       | 53.5 53.5         | 27.7 27.7       |
| Uniaxial compressive strength Uniaxial compressive strength | Input Input   | UCS UCS         | MPa MPa           | 49 49     | 185 185     | 122.7 122.7       | 40.7 40.7       |
| Weathering zone Weathering zone                             | Input Input   | WZ WZ           | - -               | 1 1       | 3 3         | 1.8 1.8           | 0.8 0.8         |
| Brazilian tensile strength Brazilian tensile strength       | Input Input   | BTS BTS         | MPa MPa           | 4.69 4.69 | 15.1 15.1   | 9.6 9.6           | 3.2 3.2         |
| Thrust force per cutter Thrust force per cutter             | Input Input   | TF TF           | kN kN             | 83 83     | 513.5 513.5 | 276.8 276.8       | 133.1 133.1     |
| Revolution per minute Revolution per minute                 | Input Input   | RPM RPM         | rev / min rev/min | 4.5 4.5   | 11.9 11.9   | 8.6 8.6           | 2.4 2.4         |
| Penetration rate Penetration rate                           | Output Output | PR PR           | m / h m/h         | 1.11 1.11 | 3.75 3.75   | 2.4 2.4           | 0.6 0.6         |

Figure 4. Correlation matrix of input and output variables for 209 cases. Figure 4. Correlation matrix of input and output variables for 209 cases.

<!-- image -->

Table

Figure 5. The detailed flowchart of this study in predicting TBM penetration rate (PR). Figure 5. The detailed flowchart of this study in predicting TBM penetration rate (PR).

<!-- image -->

Flow chart

## 4. Results and Discussion 4. Results and Discussion

## 4.1. Assessment of Models 4.1. Assessment of Models

In this study, KNN, SVM, NN, CART, and CHAID models were applied for PR prediction. Each of them has been conducted several times based on their most effective parameters. To evaluate the prediction performance of the mentioned techniques, the established TBM dataset was split into two sections of training and testing. Therefore, 209 cases of the data were separated into 167 and 42 as train and test sections and then the model constructions were conducted to forecast the TBM PR. In this study, KNN, SVM, NN, CART, and CHAID models were applied for PR prediction. Each of them has been conducted several times based on their most e ective parameters. To evaluate the prediction performance of the mentioned techniques, the established TBM dataset was split into two sections of training and testing. Therefore, 209 cases of the data were separated into 167 and 42 as train and test sections and then the model constructions were conducted to forecast the TBM PR.

The values of the performance indices for the proposed KNN, SVM, NN, CART, and CHAID models were calculated and are presented in Table 4. These results are based on testing and training datasets and using the simple ranking technique (as described earlier). Table 4 shows that the KNN model has the highest total rate (25) among the models of the training dataset. For the testing dataset, the NN model has the highest total rate, amounting to a value of 24. The total performance ratings of the models for both training and testing datasets are also indicated in Table 5. According to this table, the KNN model obtained the highest total performance rating, which is 41 (25 for training and 16 for testing).  The  following  sub-section  provides  a  more  detailed  analysis  of  the  KNN  model  for  PR prediction. The values of the performance indices for the proposed KNN, SVM, NN, CART, and CHAID models were calculated and are presented in Table 4. These results are based on testing and training datasets and using the simple ranking technique (as described earlier). Table 4 shows that the KNN model has the highest total rate (25) among the models of the training dataset. For the testing dataset, the NN model has the highest total rate, amounting to a value of 24. The total performance ratings of the models for both training and testing datasets are also indicated in Table 5. According to this table, the KNN model obtained the highest total performance rating, which is 41 (25 for training and

16 for testing). The following sub-section provides a more detailed analysis of the KNN model for PR prediction.

Table 4. The obtained results of performance indices for all predictive models in estimating TBM PR.

| Method   | Stage   |   R 2 |   RMSE |    VAF |   MAE |   a 20 - Index |   R 2 Rank |   RMSE Rank |   VAF Rank |   MAE Rank |   a 20 - Index Rank |   Total Rate |
|----------|---------|-------|--------|--------|-------|----------------|------------|-------------|------------|------------|---------------------|--------------|
| NN       | TS      | 0.924 |  0.180 | 91.735 | 0.137 |          0.944 |          5 |           5 |          5 |          5 |                   4 |           24 |
| NN       | TR      | 0.916 |  0.173 | 91.602 | 0.136 |          0.967 |          1 |           2 |          1 |          1 |                   2 |            7 |
| SVM      | TS      | 0.914 |  0.183 | 91.393 | 0.139 |          0.981 |          4 |           4 |          4 |          4 |                   5 |           21 |
| SVM      | TR      | 0.942 |  0.144 | 94.207 | 0.114 |          0.987 |          3 |           4 |          3 |          2 |                   4 |           16 |
| KNN      | TS      | 0.907 |  0.204 | 89.574 | 0.157 |          0.944 |          3 |           3 |          3 |          3 |                   4 |           16 |
| KNN      | TR      | 0.962 |  0.116 | 96.226 | 0.081 |          0.993 |          5 |           5 |          5 |          5 |                   5 |           25 |
| CART     | TS      | 0.897 |  0.216 | 88.020 | 0.164 |          0.944 |          2 |           2 |          2 |          2 |                   4 |           12 |
| CART     | TR      | 0.944 |  0.144 | 94.265 | 0.104 |          0.993 |          4 |           4 |          4 |          4 |                   5 |           21 |
| CHAID    | TS      | 0.850 |  0.252 | 83.838 | 0.179 |          0.944 |          1 |           1 |          1 |          1 |                   4 |            8 |
| CHAID    | TR      | 0.934 |  0.153 | 93.389 | 0.110 |          0.980 |          2 |           3 |          2 |          3 |                   3 |           13 |

TR: Training, TS: Testing.

Table 5. Total performance ratings.

|                  |   NN |   SVM |   KNN |   CART |   CHAID |
|------------------|------|-------|-------|--------|---------|
| Grand total rank |   31 |    37 |    41 |     33 |      21 |

## 4.2. Result of Selected Models

As mentioned in the previous section, KNN has been selected as the best predictive model of TBM PR. Figures 6 and 7 show the suggested structure of the KNN predictive model in predicting PR of TBM. In the development of the k-NN model, the objective of performing the model was to establish the balance between speed and accuracy. Therefore, the model automatically selected the best number of neighbors, within a small range. In the present study, we used k number between the values 3-5 by implementing a trial-and-error method of the system. Figure 6 presents the predictor space chart of the KNN model. In this figure, the predictor space gave excellent results, using the three input variables of UCS, RQD, and BTS as predictors for predicting the PR. The predictor space chart is an interactive graph of the predictor space and is directly printed out from the software. Any dot can temporarily become a focal record if selected. 'Focal records' are simply points selected in the predictor space chart. If a focal record variable is specified, the points representing the focal records will initially be selected and becomes red. Figure 7 shows the relationship between the predictors and K selection. In the horizontal axis of the chart, the numbers of the nearest neighbor are presented. Sums of square errors are shown in the vertical axis. As shown by the figure, the errors for k = 3, 4, and 5 were determined as 7.41, 7.39, and 7.85, respectively. The results reveal that k = 4 is the best value of the nearest neighbor numbers for the developed k-NN model.

Figure 6. Predictor space chart of k-nearest neighbor (KNN) model.

<!-- image -->

Scatter plot

Figure 6. Predictor space chart of k-nearest neighbor (KNN) model. Figure 6. Predictor space chart of k-nearest neighbor (KNN) model.

<!-- image -->

Line chart

Figure 7. The relationship between the predictors and K selection. Figure 7. The relationship between the predictors and K selection.

Figure 7. The relationship between the predictors and K selection. Predicted PR values by KNN, along with their actual values for training and testing datasets, are displayed in Figure 8. The R 2  between predicted and actual PR in training and testing dataset were 0.962 and 0.907, respectively. Besides, an RMSE of (0.204 and 0.116), a VAF of (89.574% and 96.226%) and an MAE of (0.157 and 0.081) were obtained for testing and training datasets of the best predictive model of this study, respectively. These results show that KNN, as a newly developed model in the field of TBM performance, can provide higher prediction performance compared to other  predictive  models.  It  is  worth  mentioning  that  CHAID  (as  a  tree-based  model)  was  also implemented for the first time in this field with the obtained R 2  values of 0.850 and 0.934, for testing and training datasets, respectively, which showed an enhanced performance of this model in solving Predicted PR values by KNN, along with their actual values for training and testing datasets, are displayed in Figure 8. The R 2  between predicted and actual PR in training and testing dataset were 0.962 and 0.907, respectively. Besides, an RMSE of (0.204 and 0.116), a VAF of (89.574% and 96.226%) and an MAE of (0.157 and 0.081) were obtained for testing and training datasets of the best predictive model of this study, respectively. These results show that KNN, as a newly developed model in the field of TBM performance, can provide higher prediction performance compared to other  predictive  models.  It  is  worth  mentioning  that  CHAID  (as  a  tree-based  model)  was  also implemented for the first time in this field with the obtained R 2  values of 0.850 and 0.934, for testing and training datasets, respectively, which showed an enhanced performance of this model in solving Predicted PR values by KNN, along with their actual values for training and testing datasets, are displayed in Figure 8. The R 2 between predicted and actual PR in training and testing dataset were 0.962 and 0.907, respectively. Besides, an RMSE of (0.204 and 0.116), a VAF of (89.574% and 96.226%) and an MAE of (0.157 and 0.081) were obtained for testing and training datasets of the best predictive model of this study, respectively. These results show that KNN, as a newly developed model in the field of TBM performance, can provide higher prediction performance compared to other predictive models. It is worth mentioning that CHAID (as a tree-based model) was also implemented for the first time in this field with the obtained R 2 values of 0.850 and 0.934, for testing and training datasets, respectively, which showed an enhanced performance of this model in solving TBM performance.

Compared to other published studies related to the same tunnel [12,13,38], this study has a di erent database with a slightly higher prediction performance. For example, in terms of R 2 , values of (0.897 and 0.905) and (0.919 and 0.912) were obtained by PSO-ANN and ICA-ANN techniques, respectively in the study conducted by Armaghani et al. [12]. In another study, Koopialipoor et al. [13] developed the group method of data handling technique to solve TBM PR. They obtained R 2 results of 0.946 and 0.924 for training and testing datasets, respectively. A GEP model was developed by Armaghani et al. [38] to predict TBM PR, with R 2 values of 0.855 and 0.829 for training and testing datasets, respectively. Based on the above discussion, the developed KNN model in this study can provide higher prediction capacity compared to previously published studies. TBM performance. Compared to other published studies related to the same tunnel [12,13,38], this study has a different database with a slightly higher prediction performance. For example, in terms of R 2 , values of (0.897 and 0.905) and (0.919 and 0.912) were obtained by PSO-ANN and ICA-ANN techniques,  respectively  in  the  study  conducted  by  Armaghani  et  al.  [12].  In  another  study, Koopialipoor et al. [13] developed the group method of data handling technique to solve TBM PR. They obtained R 2  results of 0.946 and 0.924 for training and testing datasets, respectively. A GEP model was developed by Armaghani et al. [38] to predict TBM PR, with R 2  values of 0.855 and 0.829 for training and testing datasets, respectively. Based on the above discussion, the developed KNN model  in  this  study  can  provide  higher  prediction  capacity  compared  to  previously  published studies.

Figure 8. Testing and training results of the KNN model in estimating PR. Figure 8. Testing and training results of the KNN model in estimating PR.

<!-- image -->

Scatter plot

In order to understand the influence of each input parameter on PR results, sensitivity analysis has been performed through the developed KNN model. To do this, the importance or weight of each input parameter on system output can be obtained. The importance of the input parameters analyzed by the KNN technique is shown in Table 6. As shown in this table, KNN identified USC as the most important input variable for predicting the PR, while RPM was considered as the least important input variable for predicting the PR. These results are in good agreement with previous investigations in the field of tunneling and underground space technologies [19,94,95]. The results of sensitivity analysis  can  be  used  by  other  researchers  in  further  investigations  to  select  the  most  influential parameters on TBM performance. In order to understand the influence of each input parameter on PR results, sensitivity analysis has been performed through the developed KNN model. To do this, the importance or weight of each input parameter on system output can be obtained. The importance of the input parameters analyzed by the KNN technique is shown in Table 6. As shown in this table, KNN identified USC as the most important input variable for predicting the PR, while RPM was considered as the least important input variable for predicting the PR. These results are in good agreement with previous investigations in the field of tunneling and underground space technologies [19,94,95]. The results of sensitivity analysis can be used by other researchers in further investigations to select the most influential parameters on TBM performance.

Table 6. Importance of input variables in the developed KNN model. Table 6. Importance of input variables in the developed KNN model.

| Input Variable Input Variable   | Importance Importance   |
|---------------------------------|-------------------------|
| RPM RPM                         | 0.14 0.14               |
| WZ WZ                           | 0.15 0.15               |
| BTS BTS                         | 0.16 0.16               |
| RQD RQD                         | 0.17 0.17               |
| TF UCS TF UCS                   | 0.18 0.20 0.18 0.20     |

## 5. Conclusions

The present study evaluated the relative importance (weight) of di erent input variables influencing PR. Initially, di erent supervised ML approaches were compared aiming to identify the most accurate modeling approach. Five supervised ML techniques were selected and evaluated, i.e., KNN, SVM, NN, CART, and CHAID. These modeling approaches were selected because of their ability to handle continuous target variables. A variety of ML techniques were conducted to predict TBM PR using a database comprising of 209 datasets including the most important parameters on TBM PR. Performance of the five mentioned ML techniques was evaluated using a simple ranking technique and some performance indices, i.e., R 2 , RMSE, VAF, and MAE. According to the obtained results, the KNN predictive model was identified as the optimum model. A total ranking value of 32 was obtained by the KNN model, while other techniques obtained ranking values of 25 (NN), 28 (SVM), 24 (CART), and 14 (CHAID). R 2 , RMSE, VAF, and MAE values of (0.907, 0.204, 89.574, and 0.157) and (0.962, 0.116, 96.226, and 0.081) were recorded for the developed KNN, as the selected predictive model of this study. Besides, the results of KNN are enhanced concerning the previously published results in the field of TBM performance prediction. It can be concluded that the KNN predictive model should be applied in similar conditions to examine the capability of this technique in the field of geotechnical engineering. Furthermore, 'importance' (weight) results of the various input variables show that USC and RPM are the most and the least important input variables, respectively, when applying the KNNmodel.

Author Contributions: Conceptualization, D.J.A.; data curation, M.M.T.; formal analysis, J.Z.; supervision, P.G.A.; writing-review &amp; editing, H.X.

Funding: This work is financially supported by the National Foundation of China (No. 41807259) and the Sheng Hua Lie Ying Program of Central South University.

Conflicts of Interest: The authors declare no conflict of interest.

## Abbreviations

| ANNs   | Artificial neural networks                                   |
|--------|--------------------------------------------------------------|
| AR     | Advance rate                                                 |
| DPW    | The distance between planes of weakness                      |
| α      | The angle between plane of weakness and TBM-driven direction |
| RMR    | Rock mass rating                                             |
| GEP    | Gene expression programing                                   |
| CFF    | Core fracture frequency                                      |
| RPM    | Revolution per minutes                                       |
| UI     | Utilization index                                            |
| PSI    | Peak slope index                                             |
| Qu     | Quartz percentage                                            |
| Rs     | Rotational speed of TBM                                      |
| Js     | Joint spacing                                                |
| Jc     | Joint condition                                              |
| C      | Cohesion                                                     |
| ϕ      | Friction angle                                               |
| υ      | Poisson's ratio                                              |
| SE     | Specific energy                                              |
| TF     | Thrust force                                                 |
| CT     | Cutterhead power                                             |
| ELM    | Extreme learning machine                                     |
| N      | Overload factor                                              |
| WTS    | Water table surface                                          |
| DE     | Di erential evolution                                        |

| BNNs    | Biological neural networks                   |
|---------|----------------------------------------------|
| HS-BFGS | Hybrid harmony search                        |
| ICA     | Imperialism competitive algorithm            |
| GWO     | Grey wolf optimizer                          |
| BPNNs   | Back-propagation neural networks             |
| ANFIS   | Adoptive neuro-fuzzy inference system        |
| CART    | classification and regression trees          |
| CHAID   | chi-squared automatic interaction detection  |
| CSM     | Colorado school of mines                     |
| DNNs    | Deep neural networks                         |
| FIS     | Fuzzy inference system                       |
| FA      | Firefly algorithm                            |
| KNN     | k-nearest neighbor                           |
| logsig  | Log-sigmoid transfer function                |
| ML      | machine learning                             |
| PR      | penetration rate                             |
| PSO     | particle swarm optimization                  |
| purelin | Linear transfer function                     |
| SVM     | support vector machine                       |
| tansig  | Hyperbolic tangent Sigmoid transfer function |
| TBM     | Tunnel boring machine                        |
| UCS     | uniaxial compressive strength                |

## References

1. Roxborough, F.F.; Phillips, H.R. Rock excavation by disc cutter. Int. J. Rock Mech. Min. Sci. Geomech. Abstr. 1975 , 12 , 361-366. [CrossRef]
2. Snowdon, R.; Ryley, M.; Temporal, J. A study of disc cutting in selected British rocks. Int. J. Rock Mech. Min. Sci. Geomech. Abstr. 1982 , 19 , 107-121. [CrossRef]
3. Sanio, H. Prediction of the performance of disc cutters in anisotropic rock. Int. J. Rock Mech. Min. Sci. Geomech. Abstr. 1985 , 22 , 153-161. [CrossRef]
4. Sato, K.; Gong, F.; Itakura, K. Prediction of disc cutter performance using a circular rock cutting ring. In Proceedings of the 1st International Mine Mechanization and Automation Symposium, Golden, CO, USA, 10-13 June 1991.
5. Rostami, J. Development of a force Estimation Model for Rock Fragmentation with Disc Cutters through Theoretical Modeling and Physical Measurement of Crushed Zone Pressure. Ph.D. Thesis, Colorado School of Mines, Golden, CO, USA, 1997.
6. Yagiz, S. Utilizing rock mass properties for predicting TBM performance in hard rock condition. Tunn. Undergr. Space Technol. 2008 , 23 , 326-339. [CrossRef]
7. Gong, Q.-M.; Zhao, J. Development of a rock mass characteristics model for TBM penetration rate prediction. Int. J. Rock Mech. Min. Sci. 2009 , 46 , 8-18. [CrossRef]
8. Farmer, I.W.; Glossop, N.H. Mechanics of disc cutter penetration. Tunn. Tunn. 1980 , 12 , 22-25.
9. Ozdemir, L. Development of Theoretical Equations for Predicting Tunnel Boreability. Ph.D. Thesis, Colorado School of Mines, Golden, CO, USA, 1977.
10. Yagiz, S.; Ozdemir, L. Geotechnical parameters influencing the TBM performance in various rocks. In Proceedings of the Program with Abstract, 44th Annual Meeting of Association of Engineering Geologists, Saint Louis, MO, USA, 12-14 June 2001; p. 79.
11. Yagiz, S. Development of Rock Fracture and Brittleness Indices to Quantify the E ects of Rock Mass Features and Toughness in the CSM Model Basic Penetration for Hard Rock Tunneling Machines. Ph.D. Thesis, Colorado School of Mines, Golden, CO, USA, 2002.
12. Armaghani, D.J.; Mohamad, E.T.; Narayanasamy, M.S.; Narita, N.; Yagiz, S. Development of hybrid intelligent models for predicting TBM penetration rate in hard rock condition. Tunn. Undergr. Space Technol. 2017 , 63 , 29-43. [CrossRef]

13. Koopialipoor, M.; Nikouei, S.S.; Marto, A.; Fahimifar, A.; Armaghani, D.J.; Mohamad, E.T. Predicting tunnel boring machine performance through a new model based on the group method of data handling. Bull. Eng. Geol. Environ. 2018 , 78 , 3799-3813. [CrossRef]
14. Yang, H.; Liu, J.; Liu, B. Investigation on the cracking character of jointed rock mass beneath TBM disc cutter. Rock Mech. Rock Eng. 2018 , 51 , 1263-1277. [CrossRef]
15. Yang, H.; Wang, H.; Zhou, X. Analysis on the damage behavior of mixed ground during TBM cutting process. Tunn. Undergr. Space Technol. 2016 , 57 , 55-65. [CrossRef]
16. Yang, H.Q.; Zeng, Y.Y.; Lan, Y.F.; Zhou, X.P. Analysis of the excavation damaged zone around a tunnel accounting for geostress and unloading. Int. J. Rock Mech. Min. Sci. 2014 , 69 , 59-66. [CrossRef]
17. Yagiz, S.; Gokceoglu, C.; Sezer, E.; Iplikci, S. Application of two non-linear prediction tools to the estimation of tunnel boring machine performance. Eng. Appl. Artif. Intell. 2009 , 22 , 808-814. [CrossRef]
18. Hamidi, J.K.; Shahriar, K.; Rezai, B.; Bejari, H. Application of fuzzy set theory to rock engineering classification systems: An illustration of the rock mass excavability index. Rock Mech. Rock Eng. 2010 , 43 , 335-350. [CrossRef]
19. Grima, M.A.; Bruines, P.A.; Verhoef, P.N.W. Modeling tunnel boring machine performance by neuro-fuzzy
8. methods. Tunn. Undergr. Space Technol. 2000 , 15 , 259-269. [CrossRef]
20. Farrokh, E.; Rostami, J.; Laughton, C. Study of various models for estimation of penetration rate of hard rock TBMs. Tunn. Undergr. Space Technol. 2012 , 30 , 110-123. [CrossRef]
21. Chen, H.; Asteris, P.G.; Jahed Armaghani, D.; Gordan, B.; Pham, B.T. Assessing Dynamic Conditions of the Retaining Wall: Developing Two Hybrid Intelligent Models. Appl. Sci. 2019 , 9 , 1042. [CrossRef]
22. Asteris, P.G.; Nikoo, M. Artificial bee colony-based neural network for the prediction of the fundamental period of infilled frame structures. Neural Comput. Appl. 2019 . [CrossRef]
23. Moayedi, H.; Armaghani, D.J. Optimizing an ANN model with ICA for estimating bearing capacity of driven pile in cohesionless soil. Eng. Comput. 2018 , 34 , 347-356. [CrossRef]
24. Yang, H.; Hasanipanah, M.; Tahir, M.M.; Bui, D.T. Intelligent Prediction of Blasting-Induced Ground Vibration Using ANFIS Optimized by GA and PSO. Nat. Resour. Res. 2019 . [CrossRef]
25. Armaghani, D.J.; Hajihassani, M.; Mohamad, E.T.; Marto, A.; Noorani, S.A. Blasting-induced flyrock and ground vibration prediction through an expert artificial neural network based on particle swarm optimization. Arab. J. Geosci. 2014 , 7 , 5383-5396. [CrossRef]
26. Asteris, P.G.; Nozhati, S.; Nikoo, M.; Cavaleri, L.; Nikoo, M. Krill herd algorithm-based neural network in structural seismic reliability evaluation. Mech. Adv. Mater. Struct. 2018 , 26 , 1146-1153. [CrossRef]
27. Asteris, P.G.; Plevris, V. Anisotropic masonry failure criterion using artificial neural networks. Neural Comput. Appl. 2017 , 28 , 2207-2229. [CrossRef]
28. Faradonbeh, R.S.; Armaghani, D.J.; Amnieh, H.B.; Mohamad, E.T. Prediction and minimization of blast-induced flyrock using gene expression programming and firefly algorithm. Neural Comput. Appl. 2016 , 29 , 269-281. [CrossRef]
29. Sarir, P.; Chen, J.; Asteris, P.G.; Armaghani, D.J.; Tahir, M.M. Developing GEP tree-based, neuro-swarm, and whale optimization models for evaluation of bearing capacity of concrete-filled steel tube columns. Eng. Comput. 2019 . [CrossRef]
30. Cavaleri, L.; Chatzarakis, G.E.; Trapani, F.D.; Douvika, M.G.; Roinos, K.; Vaxevanidis, N.M.; Asteris, P.G. Modeling of surface roughness in electro-discharge machining using artificial neural networks. Adv. Mater. Res. 2017 , 6 , 169-184.
31. Zhou, J.; Li, E.; Yang, S.; Wang, M.; Shi, X.; Yao, S.; Mitri, H.S. Slope stability prediction for circular mode failure using gradient boosting machine approach based on an updated database of case histories. Saf. Sci. 2019 , 118 , 505-518. [CrossRef]
32. Guo, H.; Zhou, J.; Koopialipoor, M.; Armaghani, D.J.; Tahir, M.M. Deep neural network and whale optimization algorithm to assess flyrock induced by blasting. Eng. Comput. 2019 . [CrossRef]
33. Mahdiyar, A.; Armaghani, D.J.; Marto, A.; Nilashi, M.; Ismail, S. Rock tensile strength prediction using empirical and soft computing approaches. Bull. Eng. Geol. Environ. 2019 , 78 , 4519-4531. [CrossRef]
34. Zhou, J.; Li, X.; Mitri, H.S. Classification of rockburst in underground projects: comparison of ten supervised learning methods. J. Comput. Civ. Eng. 2016 , 30 , 04016003. [CrossRef]
35. Zhou, J.; Li, X.; Mitri, H.S. Comparative performance of six supervised learning methods for the development of models of hard rock pillar stability prediction. Nat. Hazards 2015 , 79 , 291-316. [CrossRef]

36. Benardos, A.G.; Kaliampakos, D.C. Modelling TBM performance with artificial neural networks. Tunn. Undergr. Space Technol. 2004 , 19 , 597-605. [CrossRef]
37. Armaghani, D.J.; Koopialipoor, M.; Marto, A.; Yagiz, S. Application of several optimization techniques for estimating TBM advance rate in granitic rocks. J. Rock Mech. Geotech. Eng. 2019 , 11 , 779-789. [CrossRef]
38. Armaghani, D.J.; Faradonbeh, R.S.; Momeni, E.; Fahimifar, A.; Tahir, M.M. Performance prediction of tunnel boring machine through developing a gene expression programming equation. Eng. Comput. 2018 , 34 , 129-141. [CrossRef]
39. Eftekhari, M.; Baghbanan, A.; Bayati, M. Predicting penetration rate of a tunnel boring machine using artificial neural network. In Proceedings of the ISRM International Symposium-6th Asian Rock Mechanics Symposium; International Society for Rock Mechanics, New Delhi, India, 23-27 October 2010.
40. Javad, G.; Narges, T. Application of artificial neural networks to the prediction of tunnel boring machine penetration rate. Min. Sci. Technol. 2010 , 20 , 727-733. [CrossRef]
41. Gholami, M.; Shahriar, K.; Sharifzadeh, M.; Hamidi, J.K. A comparison of artificial neural network and multiple regression analysis in TBM performance prediction. In Proceedings of the ISRM Regional Symposium-7th Asian Rock Mechanics Symposium; International Society for Rock Mechanics, Seoul, Korea, 15-19 October 2012.
42. Salimi, A.; Esmaeili, M. Utilising of linear and non-linear prediction tools for evaluation of penetration rate of tunnel boring machine in hard rock condition. Int. J. Min. Miner. Eng. 2013 , 4 , 249-264. [CrossRef]
43. Torabi, S.R.; Shirazi, H.; Hajali, H.; Monjezi, M. Study of the influence of geotechnical parameters on the TBM performance in Tehran-Shomal highway project using ANN and SPSS. Arab. J. Geosci. 2013 , 6 , 1215-1227. [CrossRef]
44. Shao, C.; Li, X.; Su, H. Performance Prediction of Hard Rock TBM Based on Extreme Learning Machine. In Proceedings of the International Conference on Intelligent Robotics and Applications, Busan, Korea, 25-28 September 2013; pp. 409-416.
45. Mahdevari, S.; Shahriar, K.; Yagiz, S.; Shirazi, M.A. A support vector regression model for predicting tunnel boring machine penetration rates. Int. J. Rock Mech. Min. Sci. 2014 , 72 , 214-229. [CrossRef]
46. Koopialipoor, M.; Fahimifar, A.; Ghaleini, E.N.; Momenzadeh, M.; Armaghani, D.J. Development of a new hybrid ANN for solving a geotechnical problem related to tunnel boring machine performance. Eng. Comput. 2019 . [CrossRef]
47. Koopialipoor, M.; Tootoonchi, H.; Jahed Armaghani, D.; Tonnizam Mohamad, E.; Hedayat, A. Application of deep neural networks in predicting the penetration rate of tunnel boring machines. Bull. Eng. Geol. Environ. 2019 . [CrossRef]
48. Hasanipanah, M.; Monjezi, M.; Shahnazar, A.; Armaghani, D.J.; Farazmand, A. Feasibility of indirect determination of blast induced ground vibration based on support vector machine. Measurement 2015 , 75 , 289-297. [CrossRef]
49. Liang, M.; Mohamad, E.T.; Faradonbeh, R.S.; Jahed Armaghani, D.; Ghoraba, S. Rock strength assessment based on regression tree technique. Eng. Comput. 2016 , 32 , 343-354. [CrossRef]
50. Khandelwal, M.; Armaghani, D.J.; Faradonbeh, R.S.; Yellishetty, M.; Majid, M.Z.A.; Monjezi, M. Classification and regression tree technique in estimating peak particle velocity caused by blasting. Eng. Comput. 2017 , 33 , 45-53. [CrossRef]
51. Jamshidi, A. Prediction of TBM penetration rate from brittleness indexes using multiple regression analysis. Model. Earth Syst. Environ. 2018 , 4 , 383-394. [CrossRef]
52. Shijing, W.; Bo, Q.; Zhibo, G. The time and cost prediction of tunnel boring machine in tunnelling. WuhanUniv. J. Nat. Sci. 2006 , 11 , 385-388. [CrossRef]
53. Sundaram, M. The e ects of ground conditions on TBM performance in tunnel excavation-A case history. In Proceedings of the 10th Australia New Zealand conference on Geomechanics, Queensland, Australia, 21-24 October 2007.
54. Ietto, F.; Perri, F.; Cella, F. Weathering characterization for landslides modeling in granitoid rock masses of the Capo Vaticano promontory (Calabria, Italy). Landslides 2018 , 15 , 43-62. [CrossRef]
55. Ietto, F.; Perri, F.; Cella, F. Geotechnical and landslide aspects in weathered granitoid rock masses (Serre Massif, southern Calabria, Italy). Catena 2016 , 145 , 301-315. [CrossRef]
56. Abad, S.V.A.N.K.; Tugrul, A.; Gokceoglu, C.; Armaghani, D.J. Characteristics of weathering zones of granitic rocks in Malaysia for geotechnical engineering design. Eng. Geol. 2016 , 200 , 94-103. [CrossRef]

57. Yang, H.Q.; Li, Z.; Jie, T.Q.; Zhang, Z.Q. E ects of joints on the cutting behavior of disc cutter running on the jointed rock mass. Tunn. Undergr. Space Technol. 2018 , 81 , 112-120. [CrossRef]
58. Duda, R.O.; Hart, P.E.; Stork, D.G. Pattern Classification and Scene Analysis ; Wiley: New York, NY, USA, 1973; Volume 3.
59. Franco-Lopez, H.; Ek, A.R.; Bauer, M.E. Estimation and mapping of forest stand density, volume, and cover type using the k-nearest neighbors method. Remote Sens. Environ. 2001 , 77 , 251-274. [CrossRef]
60. Wu, X.; Kumar, V.; Quinlan, J.R.; Ghosh, J.; Yang, Q.; Motoda, H.; McLachlan, G.J.; Ng, A.; Liu, B.; Philip, S.Y. Top 10 algorithms in data mining. Knowl. Inf. Syst. 2008 , 14 , 1-37. [CrossRef]
61. Akbulut, Y.; Sengur, A.; Guo, Y.; Smarandache, F. NS-k-NN: Neutrosophic set-based k-nearest neighbors classifier. Symmetry 2017 , 9 , 179. [CrossRef]
62. Wei, C.; Huang, J.; Mansaray, L.; Li, Z.; Liu, W.; Han, J. Estimation and mapping of winter oilseed rape LAI from high spatial resolution satellite data based on a hybrid method. Remote Sens. 2017 , 9 , 488. [CrossRef]
63. Qian, Y.; Zhou, W.; Yan, J.; Li, W.; Han, L. Comparing machine learning classifiers for object-based land cover classification using very high resolution imagery. Remote Sens. 2015 , 7 , 153-168. [CrossRef]
64. Vapnik, V.; Vapnik, V. Statistical Learning Theory ; Wiley: New York, NY, USA, 1998; pp. 156-160.
65. Kavzoglu, T.; Sahin, E.K.; Colkesen, I. Landslide susceptibility mapping using GIS-based multi-criteria decision analysis, support vector machines, and logistic regression. Landslides 2014 , 11 , 425-439. [CrossRef]
66. Cortes, C.; Vapnik, V. Support-vector networks. Mach. Learn. 1995 , 20 , 273-297. [CrossRef]
67. Hong, H.; Pradhan, B.; Bui, D.T.; Xu, C.; Youssef, A.M.; Chen, W. Comparison of four kernel functions used in support vector machines for landslide susceptibility mapping: A case study at Suichuan area (China). Geomat. Nat. Hazards Risk 2017 , 8 , 544-569. [CrossRef]
68. Kalantar, B.; Pradhan, B.; Naghibi, S.A.; Motevalli, A.; Mansor, S. Assessment of the e ects of training data selection on the landslide susceptibility mapping: A comparison between support vector machine (SVM), logistic regression (LR) and artificial neural networks (ANN). Geomat. Nat. Hazards Risk 2018 , 9 , 49-69. [CrossRef]
69. Hopfield, J.J. Neural networks and physical systems with emergent collective computational abilities. Proc. Natl. Acad. Sci. USA 1982 , 79 , 2554-2558. [CrossRef]
70. Breiman, L.; Friedman, J.; Olshen, R.; Stone, C. Classification and Regression Trees ; Taylor &amp; Francis Group: New York, NY, USA, 1984; Volume 37, pp. 237-251.
71. Kass, G.V. An exploratory technique for investigating large quantities of categorical data. J. R. Stat. Soc. Ser. C 1980 , 29 , 119-127. [CrossRef]
72. Toghroli, A.; Suhatril, M.; Ibrahim, Z.; Safa, M.; Shariati, M.; Shamshirband, S. Potential of soft computing approach for evaluating the factors a ecting the capacity of steel-concrete composite beam. J. Intell. Manuf. 2018 , 29 , 1793-1801. [CrossRef]
73. Jian, Z.; Shi, X.; Huang, R.; Qiu, X.; Chong, C. Feasibility of stochastic gradient boosting approach for predicting rockburst damage in burst-prone mines. Trans. Nonferrous Met. Soc. China 2016 , 26 , 1938-1945.
74. Zhou, J.; Li, E.; Wang, M.; Chen, X.; Shi, X.; Jiang, L. Feasibility of Stochastic Gradient Boosting Approach for Evaluating Seismic Liquefaction Potential Based on SPT and CPT Case Histories. J. Perform. Constr. Facil. 2019 , 33 , 4019024. [CrossRef]
75. Zhou, J.; Shi, X.; Du, K.; Qiu, X.; Li, X.; Mitri, H.S. Feasibility of random-forest approach for prediction of ground settlements induced by the construction of a shield-driven tunnel. Int. J. Geomech. 2016 , 17 , 4016129. [CrossRef]
76. Asteris, P.; Roussis, P.; Douvika, M. Feed-forward neural network prediction of the mechanical properties of sandcrete materials. Sensors 2017 , 17 , 1344. [CrossRef] [PubMed]
77. Asteris, P.G.; Kolovos, K.G. Self-compacting concrete strength prediction using surrogate models. Neural Comput. Appl. 2019 , 31 , 409-424. [CrossRef]
78. Liao, X.; Khandelwal, M.; Yang, H.; Koopialipoor, M.; Murlidhar, B.R. E ects of a proper feature selection on prediction and optimization of drilling rate using intelligent techniques. Eng. Comput. 2019 . [CrossRef]
79. Koopialipoor, M.; Jahed Armaghani, D.; Haghighi, M.; Ghaleini, E.N. A neuro-genetic predictive model to approximate overbreak induced by drilling and blasting operation in tunnels. Bull. Eng. Geol. Environ. 2019 , 78 , 981-990. [CrossRef]
80. Swingler, K. Applying Neural Networks: A Practical Guide ; Academic Press: New York, NY, USA, 1996; ISBN 0126791708.

81. Looney, C.G. Advances in feedforward neural networks: Demystifying knowledge acquiring black boxes. IEEE Trans. Knowl. Data Eng. 1996 , 8 , 211-226. [CrossRef]
82. Shams, S.; Monjezi, M.; Majd, V.J.; Armaghani, D.J. Application of fuzzy inference system for prediction of rock fragmentation induced by blasting. Arab. J. Geosci. 2015 , 8 , 10819-10832. [CrossRef]
83. Zorlu, K.; Gokceoglu, C.; Ocakoglu, F.; Nefeslioglu, H.A.; Acikalin, S. Prediction of uniaxial compressive strength of sandstones using petrography-based models. Eng. Geol. 2008 , 96 , 141-158. [CrossRef]
84. Bruines, P. Neuro-fuzzy modeling of TBM performance with emphasis on the penetration rate. Mem. Cent. Eng. Geol. Neth. Delft 1998 , 173 , 202.
85. Sapigni, M.; Berti, M.; Bethaz, E.; Busillo, A.; Cardone, G. TBM performance estimation using rock mass classifications. Int. J. Rock Mech. Min. Sci. 2002 , 39 , 771-788. [CrossRef]
86. Ulusay, R.; Hudson, J.A. ISRM (2007) The Complete ISRM Suggested Methods for Rock Characterization, Testing and Monitoring: 1974-2006 ; ISRM Turkish National Group: Ankara, Turkey, 2007; p. 628.
87. Calcaterra, D.; Parise, M. Landslide types and their relationships with weathering in a Calabrian basin, southern Italy. Bull. Eng. Geol. Environ. 2005 , 64 , 193-207. [CrossRef]
88. Jahed Armaghani, D.; Mohd Amin, M.F.; Yagiz, S.; Faradonbeh, R.S.; Abdullah, R.A. Prediction of the uniaxial compressive strength of sandstone using various modeling techniques. Int. J. Rock Mech. Min. Sci. 2016 , 85 , 174-186. [CrossRef]
89. Bejarbaneh, B.Y.; Bejarbaneh, E.Y.; Fahimifar, A.; Armaghani, D.J.; Majid, M.Z.A. Intelligent modelling of sandstone deformation behaviour using fuzzy logic and neural network systems. Bull. Eng. Geol. Environ. 2018 , 77 , 345-361. [CrossRef]
90. Yang, H.Q.; Lan, Y.F.; Lu, L.; Zhou, X.P. A quasi-three-dimensional spring-deformable-block model for runout analysis of rapid landslide motion. Eng. Geol. 2015 , 185 , 20-32. [CrossRef]
91. Zhou, X.P.; Yang, H.Q. Micromechanical modeling of dynamic compressive responses of mesoscopic heterogenous brittle rock. Theor. Appl. Fract. Mech. 2007 , 48 , 1-20. [CrossRef]
92. Yang, H.Q.; Xing, S.G.; Wang, Q.; Li, Z. Model test on the entrainment phenomenon and energy conversion mechanism of flow-like landslides. Eng. Geol. 2018 , 239 , 119-125. [CrossRef]
93. Bieniawski, Z.T. Rock Mechanics Design in Mining and Tunnelling ; A.A. Balkema: Rotterdam, The Netherlands, 1984; ISBN 9061915074.
94. Innaurato, N.; Mancini, A.; Rondena, E.; Zaninetti, A. Forecasting and e ective TBM performances in a rapid excavation of a tunnel in Italy. In Proceedings of the 7th ISRM Congress; International Society for Rock Mechanics and Rock Engineering, Aachen, Germany, 16-20 September 1991.
95. Ribacchi, R.; Fazio, A.L. Influence of rock mass parameters on the performance of a TBM in a gneissic formation (Varzo Tunnel). Rock Mech. Rock Eng. 2005 , 38 , 105-127. [CrossRef]

<!-- image -->

Icon

' 2019 by the authors. Licensee MDPI, Basel, Switzerland. This article is an open access article distributed under the terms and conditions of the Creative Commons Attribution (CC BY) license (http: // creativecommons.org / licenses / by / 4.0 / ).
## Real-time Forecast Models for TBM Load Parameters Based on Machine Learning Methods

Xianjie Gao 1 , Xueguan Song 2 , Maolin Shi 2 , Chao Zhang 3 ∗ , Hongwei Zhang 3

1 Department of Basic Sciences,

Shanxi Agricultural University, Taigu, Shanxi 030801, P.R. China

xjgao@sxau.edu.cn

2 School of Mechanical Engineering,

Dalian University of Technology, Dalian, Liaoning, 116024, P.R. China

sxg@dlut.edu.cn; shl5985336@126.com

3 School of Mathematical Sciences,

Dalian University of Technology, Dalian, Liaoning, 116024, P.R. China

chao.zhang@dlut.edu.cn;

hwzhang@dlut.edu.cn

## Abstract

Because of the fast advance rate and the improved personnel safety, tunnel boring machines (TBMs) have been widely used in a variety of tunnel construction projects. The dynamic modeling of TBM load parameters (including torque, advance rate and thrust) plays an essential part in the design, safe operation and fault prognostics of this complex engineering system. In this paper, based on in-situ TBM operational data, we use the machine-learning (ML) methods to build the real-time forecast models for TBM load parameters, which can instantaneously provide the future values of the TBMload parameters as long as the current data are collected. To decrease the model complexity and improve the generalization, we also apply the least absolute shrinkage and selection (Lasso) method to extract the essential features of the forecast task. The experimental results show that the forecast models based on deep-learning methods, e.g. , recurrent neural network and its variants, outperform the ones based on the shallow-learning methods, e.g. , support vector regression and random forest. Moreover, the Lasso-based feature extraction significantly improves the performance of the resultant models.

Keywords: Tunnel boring machines; feature extraction; real-time forecast; load parameters; machine learning

## 1 Introduction

With the increasing demand of long and deep tunnel construction, the traditional tunneling techniques ( e.g., drilling and blasting) have not satisfied the construction requirement of high efficiency, small environmental damage and low construction risk. Instead, tunnel boring machines (TBMs) have become a primary method in various underground excavation projects ( e.g., mountain tunnel [1], city subway [2] and coal mine [3]) with its predominance of high advance rate, environmental friendliness and security. The widespread use of TBMs benefits from the experiences gained from different conditions and the new technological advances. However, there are still many challenges in the machinery design and the project application of TBMs. For example, under complicated construction conditions, TBMs' excavation process will be faced with high risk caused by an unanticipated presence of water leakage, rock spalling, geological faulting, weak regions, break outs of the tunnel wall and subsidence of work area. To improve TBMs' reliability and reduce unscheduled downtime, some research works have paid attention to TBMs' risk evaluation [4], design and R&amp;D [5], and safety decision [6].

∗ Corresponding author

One main research concern of TBM is to develop a health monitoring and prognostics system that can automatically find out the anomalies and the provides the fault prognostic during the TBM operation [7]. An essential part of such a system is the real-time forecast of TBM load parameters (including torque, advance rate and thrust), which are important indicators to evaluate TBMs' machine health condition by observing whether their forecast values exceed the pre-defined threshold or not [8, 9]. However, due to the complex geological condition, it is still challenging to achieve the accurate real-time forecast of TBM load parameters ( cf. [10, 11, 12, 13, 14, 15, 16]).

In general, the existing methods for forecasting TBM load parameters can be categorized into three kinds:

- (i) Empirical methods aim to developing the empirical equations, which describe the relationship between the geological information and some important operation parameters, e.g., cutter force, thrust and cutter power, to forecast TBM load parameters [17, 18, 19, 20]. In order to improve the forecast accuracy, there have also been some attempts to combine the empirical methods with the cutting experiments ( cf. [21, 22, 23]).
- (ii) Under the assumption that one stratum or different stratums are distributed on the excavation face, rock-soil mechanics methods explore the relationship between the rock-soil mechanics characteristics of the stratums and TBMs' operation state and then provide the estimate of TBM load parameters [24, 25, 26].
- (iii) The numerical simulation methods employ some differential equation models to describe the dynamic variation of TBMs' operation parameters, and then provide the estimate of these parameters with the aid of computer simulation, e.g., the three-dimensional finite element simulation model [27] and the 3D FEM model [28].

However, the practical applications of these methods have the following limitations: 1) we need the considerable specialty knowledge or the participation of relevant professional technicians; 2) the forecast results are lack of generality and cannot be (at least cannot be directly) generalized to other construction conditions; and 3) these methods are unsuitable (at least cannot be directly applied) to the real-time forecast, which requires that the future forecast results should be instantaneously provided as long as the current operational data are collected.

In this paper, we adopt the machine-learning (ML) methods to develop the real-time forecast models for TBM load parameters based on TBM operational data collected from the sensors equipped on a TBM in the construction process. We mainly concern with two kinds of ML models: the deep-learning models including recurrent neural networks (RNN) and its variants ( e.g. long-short term memory network (LSTM) and gated recurrent unit network (GRU)); and the shallow-learning models including support vector regression (SVR), random forest (RF) and feed-forward neural network (FNN). To capture the temporal information encoded in the original data, the input of these models is a length of time series data containing the previous and the current data, and the output is the estimate of the future values of the TBM load parameters including torque, advance rate and thrust.

Although the existing work [29] has discussed the prediction for TBM operational parameters, the models given in [29] can only provide the prediction value of one single operational parameter once a time and thus has a low efficiency in the prediction task of multiple operational parameters. Moreover, the training difficulty of multiple-output models is relatively higher than the single-output models because the former have more undetermined weights. Therefore, we introduce the Lasso method to extract essential features from the original TBM operational data to simplify the model structure and then to improve the training efficiency accordingly. The experimental results support the effectiveness of the ML-based models for the real-time forecast task.

The rest of this paper is organized as follows. In Section 2, we give the necessary preliminaries on the ML methods considered in this paper. In Section 3, we introduce the ML-based models of the real-time forecast of the TBM load parameters. Section 4 presents experimental results and the last section concludes the paper. In the appendix, we list some important features appearing in the in-situ TBM operational data.

## 2 Preliminaries on ML Methods

In this section, we give a brief introduction of the main ML methods used in this paper including FNN, RNN, LSTM, GRU and Lasso. We will show that, because of the existence of loop structure, RNN and its variants can maintain the previous input information for the future forecast, and thus are more suitable to the real-time forecast. The details of SVR and RF are referred to [30].

## 2.1 Feed-forward Neural Networks

Artificial neural networks (ANNs) are the typical representatives of connectionism models. By using the weighted directed lines to connect neurons squashed by non-linear functions, ANNs can accurately approximate arbitrary continuous functions [31]. Because of this strong non-linear mapping capability, ANNs have been widely used in various kinds of AI-related problems [32]. One of the most frequently used ANNs is the feed-forward neural network (FNN) that stacks multiple-layer neurons and the adjacent layers are connected by the unidirectional lines such that the information flow is unidirectional from the input layer to the output layer ( cf. Fig. 1).

Take FNN with one hidden layer as an example. Let V = [ v 1 , v 2 , · · · , v L ] ∈ R J × L be the weight matrix between the output layer and the hidden layer, where v l (1 ≤ l ≤ L ) is the weight vector connecting the hidden layer with the l -th output node. Denote W = [ w 1 , w 2 , · · · , w J ] ∈ R I × J as the weight matrix between the input layer and the hidden layer, where w j (1 ≤ j ≤ J ) is the weight vector connecting the input layer with the j -th hidden node. Let σ : R → R be a sigmoid function. Given an I -dimensional input x = ( x (1) , · · · , x ( I ) ) T ∈ R I , the output y ∈ R L of the FNN can be computed by:

<!-- formula-not-decoded -->

where σ ( · ) is the vector-valued function that is component-wise w.r.t. the scalar-valued function σ ( · ). One popular FNN training algorithm is the stochastic gradient descent method which updates the weights W and V in the following way: given a sample set { ( x t , y t ) } T t =1 , randomly select t from { 1 , 2 , · · · , T } and then

<!-- formula-not-decoded -->

with L k t ( V , W ) = ‖ y k t - ̂ y k t ‖ 2 2 , where η &gt; 0 is a learning rate and ̂ y k t is the network output w.r.t. the input x t at the k -th iteration.

## 2.2 Recurrent Neural Networks

Recurrent neural networks (RNNs) are a class of neural networks that have the loop structures to maintain the previous learning information and then combine it with the current input to generate the future network outputs [33]. In this manner, the output of a RNN contains the information of the current and the previous inputs. This characteristics makes RNNs quite suitable to dynamically modeling the sequential behavior of time series. As shown in Fig. 2, given a current input x t +1 , the current output of the hidden node h t +1 is computed by

<!-- formula-not-decoded -->

where tanh ( · ) is the vector-valued function that is component-wise w.r.t. the scalar-valued function tanh( · ); U is the weight matrix between the current input x t +1 and the current hidden output h t +1 ; and W is the weight matrix between the current hidden output h t +1 and the previous hidden output h t . Then, the fully-connected node gives the following output:

<!-- formula-not-decoded -->

where V is the weight matrix between the current hidden output h t +1 and the current output q t +1 .

RNNs perform well in modeling short sequences, while the training for the long sequences will fail because of vanishing gradients or explosive gradients. The former means that the gradient signal is too small to effectively update weights; and the latter refers to the phenomenon that the magnitude of gradients becomes so large that the training process diverges [34]. To overcome this limitation, some specific gate operations are imposed into RNN's hidden nodes, and then there arise some variants of RNN, e.g., long-short term memory network (LSTM) and gated recurrent unit network (GRU).

## 2.3 Long-short Term Memory Networks

In RNNs, the hidden nodes implement the inner-product operation and then are squashed by a nonlinear activation function. For a long time series data, this simple structure cannot efficiently capture the useful sequential characteristic or eliminate the reductant information. Instead of the inner-product operation, the long-short term memory (LSTM) networks impose three kinds of adaptive and multiplicative gate operations into RNN's hidden nodes including the input gate, the forget gate and the output gate [35]. The input and the output gates respectively control the information flowing in and out; and the forget gate is used to eliminate the redundancy from time series data and meanwhile to maintain the useful information.

In Fig. 3, we display a typical structure of LSTMs' hidden nodes, where i , f and o stand for the input gate, the forget gate and the output gate respectively. Denote c and g as the memory cell and the new memory cell respectively. Given the previous hidden output h t and the current input x t +1 , the forward propagation equations of LSTM are given as follows:

<!-- formula-not-decoded -->

where ⊙ is the Hadamard product, and U [ · ] , W [ · ] stand for the weight matrices for the corresponding gates.

## 2.4 Gated Recurrent Unit Networks

In some problems, the three-gate structure of LSTM's hidden node is likely to cause the overfitting, and thus Cho et al. [36] proposed gated recurrent unit networks (GRUs) , which integrate the input and the forget gates in LSTMs' hidden nodes into one gate ( cf. Fig. 4). Because of the relatively simpler structure, GRUs have a higher training efficiency but also perform better than RNNs and LSTMs in many learning tasks [36]. The forward propagation equations of GRU are given as follows:

<!-- formula-not-decoded -->

where x t +1 , h t +1 , z t +1 and r t +1 are the input, the output, the update gate and the reset gate vectors respectively; and U [ · ] , W [ · ] stand for the weight matrices for the corresponding gates.

## 2.5 Least Absolute Shrinkage and Selection Operator

Given a sample set D = { ( x 1 , y 1 ) , ( x 1 , y 1 ) , . . . , ( x N , y N ) } , where x ∈ R I , y ∈ R , consider the following linear regression model:

<!-- formula-not-decoded -->

where 〈· , ·〉 stands for the inner product, β ∈ R I is the weight vector and β 0 ∈ R is the bias. This model easily leads to overfitting and has a low tolerance for noisy information. To overcome these shortcomings, one way is to add the regularizer into the objective function:

<!-- formula-not-decoded -->

where λ &gt; 0 is the regularization coefficient and Ω( β ) is the regularizer w.r.t. the weight vector β . Especially, when Ω( β ) = ‖ β ‖ 2 2 , the model is called as the ridge regression ( cf. [37]); and when Ω( β ) = ‖ β ‖ 1 , the model is called as the least absolute shrinkage and selection operator (Lasso) ( cf. [38]).

Lasso has become one of the most frequently used feature-extraction methods and has been widely used in many engineering problems ( e.g. [39, 40]). We note that, one common way to use Lasso method for the feature extraction is to remove the features whose Lasso coefficients are close to zero and maintain the rest as the input features for the subsequent learning process.

## 3 Real-time Forecast of TBM Load Parameters

In this section, we present the models of the real-time forecast of TBM load parameters. First, we give the problem setup of the real-time forecast. Then, we discuss two output-modes of the forecast models. Finally, we introduce the Lasso-based feature extraction for TBM operational data.

## 3.1 Real-time Forecast

The real-time forecast requires that models should instantaneously generate the future values of the TBM load parameters during the next period as long as the current operational data are collected.

Therefore, a desired forecast model should be able to dynamically capture the dynamic nature of time series data. One reasonable way to handle this issue is to take a time-continuous sequence from the whole time series as the input of the models.

Given a time series { ( x t , y t ) } ∞ t =1 with x t = ( x (1) t , · · · , x ( I ) t ) T ∈ R I and y t = ( y (1) t , · · · , y ( J ) t ) T ∈ R J , the real-time forecast task aims to find a function f : R I ×··· × R I ︸ ︷︷ ︸ τ → R J such that its output

<!-- formula-not-decoded -->

In practical applications, given a T length of time series data { ( x t , y t ) } T t =1 , we can draw ( T - τ ) sub-sequence ( x t - τ +1 , x t - τ +2 , · · · , x t - 1 , x t ) from it and the length of each sub-sequence is τ . Then, the function f is obtained by minimizing the mean squared error (MSE)

can approximate the actual output y t +1 accurately, where τ &gt; 0 is the window width that controls the length of input sequences. In general, the Euclidean distance ‖ y t - ̂ y t ‖ 2 2 is used to measure the difference between y t and ̂ y t . Especially, if the output vector y t is composed of some specific components of x t , i.e., y t := ( x ( i 1 ) t , · · · , x ( i J ) t ) T ( J &lt; I ), it is the so-called self-forecast problem.

<!-- formula-not-decoded -->

where F is a function class that can be set as a shallow-learning model ( e.g. SVR, RF or FNN) or a deep-learning model ( e.g. RNN, LSTM or GRU).

## 3.2 Output Modes and Lasso-based Feature Extraction

As addressed above, TBM's load refer to three kinds of parameters: torque, advance rate and thrust. Thus, forecasting these parameters can be achieved in two kinds of output modes: single-output and multiple-output. In the single-output mode, the aforementioned f is a scalar function that only generates the estimate of one of the three parameters each time. Because of the relatively simpler model structure, the single-output models have a higher training efficiency than that of multiple-output models. However, three individual models should be built for the three TBM parameters respectively. In contrast, one multiple-output model is enough to simultaneously forecast the three parameters, and thus it has a higher operating efficiency.

One way to improve the performance of multiple-output models is to decrease the model complexity by extracting useful features from TBM operational data. As addressed in Section 2.5, Lasso provides a powerful method for extracting features that are strongly related to learning tasks by observing the magnitude of their Lasso coefficients. In this manner, we select the essential features of the forecast task. The subsequent experimental results show that the Lasso-based feature extraction can significantly improve the performance of the forecast models.

## 4 Numerical Experiments

In this section, we use the in-situ TBM operational data to conduct the numerical experiments for verifying the validity of the proposed models. All experiments were processed by using PyTorch in a computer with Intel ® Core TM i7 CPU at 4 GHz, 64 GB RAM and two NVIDIA GTX 1080 graphics cards.

## 4.1 Data Description

The data set is collected from the sensors equipped on an earth pressure balance shield TBM of the subway tunnel project in Shenzhen, a city of China. The TBM has 500 T total mass and 120 knifes on its cutterhead. The tunnel length is about 2000 m and its diameter is 6 . 3 m . The elevation of ground surface is between 0 . 2 m ∼ 5 . 8 m , and the depth of the tunnel floor from the ground surface is between 11 . 8 m ∼ 25 . 4 m . There are 44 features in the TBM operational data ( cf. Tab. 3).

We choose a 3000 length of time-continuous TBM operational data { x 1 , x 2 , · · · , x 3000 } and then normalize them in the component-wise way:

<!-- formula-not-decoded -->

This sequence is split into two time-continuous sub-sequences: { x 1 , x 2 , · · · , x 2500 } and { x 2501 , x 2502 , · · · , x 3000 } . The former is used to train models, and the latter serves as the test set to examine whether the trained models can accurately forecast the load parameters during next period.

Moreover, we consider two error criterions: the root of MSE (RMSE) ( cf. (3)) and the mean absolute percentage error (MAPE):

<!-- formula-not-decoded -->

where ̂ y ( j ) t and y ( j ) t stand for the prediction and the actual values of the load parameters 'Torque' ( j = 1), 'Advance Rate' ( j = 2) and 'Thrust' ( j = 3).

## 4.2 Experimental Settings

Here, we consider the real-time forecast of TBM load parameters including torque, thrust and advance rate. Note that the three parameters belong to the 44 features of TBM operational data, and thus it is a self-forecast problem. Set the window width τ = 5, i.e., generating the current output needs the previous five inputs.

The following are the specific settings of the aforementioned models in the experiments:

- The kernel function of support vector regression (SVR) is selected as 'RBF' with the parameter ǫ = 0 . 1 and the constant C equals to 1.
- Random forest (RF) is an ensemble of ten decision trees with the maximal depth being 5.
- Feed-forward neural network (FNN) has two hidden layers both of which have 10 nodes, its input layer contains 220 nodes and its output layer has one node (resp. three nodes) corresponding to single-output mode (resp. multiple-output mode) ( cf. Fig. 1). The network is trained by using stochastic gradient descent with learning rate η = 0 . 01 and the maximal training epoch is 100.
- The recurrent neural network (RNN) is composed of an input layer with 44 nodes, one RNN layer with 10 RNN units, a fully-connected layer composed of two layers both of which have 10 hidden nodes and an output layer with one or three nodes. The LSTM (resp. GRU) has the same structure as that of RNN except that the RNN units in the RNN layer are replaced with LSTM (resp. GRU) units ( cf. Fig. 5). These models are trained by using RMSprop [41] with the learning rate η = 0 . 0005 and the maximal training epoch is 30000.

The comparative experiments are conducted in the four kinds of settings: single-output mode with (reps. without) Lasso-based feature extraction (briefly denoted as 's.w.l.' (resp. 's.w/o.l.')) and multiple-output mode with (reps. without) Lasso-based feature extraction (briefly denoted as 'm.w.l.' (resp. 'm.w/o.l.')), respectively. In the s.w/o.l. and m.w/o.l. settings, the inputs of these models are the original operation data that have 44 features. The Lasso-based feature extraction will select the essential features according to their Lasso coefficients whose magnitudes reflects their importance to the forest task. Thus, in the s.w.l. setting, for each one of the three parameters, the input features are extracted from the 44 features by using the Lasso method. Combine its own feature and extracted features, we use Lasso-based single-output SVR, RF, FNN amd RNN-based (RNNs, LSTM and GRU) predictors to real-time forecast. We change the number of input nodes according to the number of extracted features. The number of nodes in the input layer of the predicted torque FNN and RNNbased models are 30 and 6, respectively. The number of nodes in the input layer of the predicted advance rate FNN and RNN-based models are 35 and 7, respectively. The number of nodes in the input layer of the predicted thrust FNN and RNN-based models are 35 and 7, respectively. Comprehensive the features to be predicted and all extracted features. We use multi-output SVR, RF, FNN amd RNN-based (RNNs, LSTM and GRU) predictors. We set the number of nodes in the input layer of FNN and RNN-based models to 90 and 18, respectively. Note that, in the m.w.l. setting, the input features are the integration of the features extracted by the Lasso method implemented for each of the load parameters.

## 4.3 Experimental Results

To exam the validity of the proposed models, we mainly concern with the following issues:

- The performance of these models for the real-time forecast task.
- The performance discrepancy between the single-output mode and the multiple-output mode.
- The effectiveness of the Lasso-based feature extraction.

As shown in Fig. 6 - Fig. 8, the deep-learning models (RNN, LSTM and GRU) outperform the shallow-learning models (SVR, RF and FNN) for the forecast task in most cases, and these deep models can accurately capture the dynamic variation of the three parameters 'Torque', 'Advance Rate' and 'Thrust' during the next period. Especially, in most cases, GRU performs better than RNN and LSTM, which is because the relatively simpler gate structure is enough to afford the forecast task and meanwhile avoids the overfitting.

As listed in Tab. 2, the performance of single-output models is better than that of multiple-output models in most cases because the former has a simpler structure that leads to a higher training efficiency. However, to achieve the forecast of the three parameters, we need to build three single-output models respectively. In contrast, one multiple-output model can simultaneously provide the forecast results of the three TBM parameters and thus has a higher operating efficiency because of a smaller amount of model parameters.

In general, compared with the single-output models, the performance loss of the multiple-output models is due to their complex structures. To overcome this limitation, we use the Lasso-based feature extraction to eliminate the redundant features from the inputs so as to decrease the model complexity. The effectiveness of the Lasso-based feature extraction can be measured by the quantity called 'Performance Gain' (or briefly denoted as 'PERF Gain'):

<!-- formula-not-decoded -->

and

Table 1: Results of Lasso-based Feature Extraction

| Features Coefficient Parameters                     |   Torque |   Advance Rate |   Thrust |
|-----------------------------------------------------|----------|----------------|----------|
| Rotation speed of cutter (r/min)                    |   29.912 |          4.178 |          |
| Cutter power (kw)                                   |   28.871 |                |          |
| Pressure of chamber at top left (bar)               |   -9.126 |                |          |
| Pressure of chamber at bottom right (bar)           |    1.451 |                |          |
| Temperature of oil tank ( ◦ C)                      |    0.813 |                |          |
| Pressure of shield tail seal at left front (bar)    |          |         48.521 |          |
| Rolling angle ( ◦ )                                 |          |        -29.760 |          |
| Propelling pressure (bar)                           |          |          0.075 |          |
| Propelling pressure of C group (bar)                |          |          0.041 |   30.267 |
| Pressure of screw pump (bar)                        |          |          0.023 |          |
| Pressure of shield tail seal at top left back (bar) |          |                |   36.896 |
| Propelling pressure of A group (bar)                |          |                |   29.833 |
| Propelling pressure of B group (bar)                |          |                |   26.638 |
| Propelling pressure of D group (bar)                |          |                |    5.219 |
| Displacement of A group of thrust cylinders (mm)    |          |                |   -0.001 |

<!-- formula-not-decoded -->

where 'RMSE' can also be changed to 'MAPE' accordingly. In Tab. 1, we have listed the three groups of features whose Lasso coefficients have the large magnitude and deem that they are strongly related with the forecast task. Meanwhile, we omit the features with the coefficients close to zero . We find that the essential features of the three TBM operation parameters differ from each other except for two individual features. This fact suggests that the three parameters have difference inherent characteristics. The experimental results given in Tab. 2 point out that the introduction of Lasso-based feature extraction brings a significant performance gain in most cases, and thus support the validity of this method.

Table 2: RMSE (MAPE) of Models for Real-time TBM Multi-parameters Forecast

| Models Results Settings   | s.w/o.l.          | s.w.l.           | PERF Gain (s.w/o.l. vs. s.w.l.)   | m.w/o.l.          | m.w.l.            | PERF Gain (m.w/o.l. vs. m.w.l.)   |
|---------------------------|-------------------|------------------|-----------------------------------|-------------------|-------------------|-----------------------------------|
| SVR                       | 98.204(13.541%)   | 36.510(3.999%)   | 62.882%(70.467%)                  | 98.204(13.541%)   | 66.564(8.976%)    | 32.219%(33.712%)                  |
| RF                        | 94.795(8.471%)    | 30.499(3.221%)   | 67.826%(61.976%)                  | 77.331(7.959%)    | 29.224 ( 2.972% ) | 62.209%(62.659%)                  |
| Torque FNN                | 41.857(5.144%)    | 31.265(2.919%)   | 25.305%(43.254%)                  | 93.226(11.672%)   | 49.240 (6.362%)   | 47.182%(45.493%)                  |
| RNN                       | 40.719(4.555%)    | 28.472( 2.281% ) | 30.077%(49.923%)                  | 61.797(8.229%)    | 56.020(7.283%)    | 9.348%(11.496%)                   |
| GRU                       | 35.476 ( 3.974% ) | 28.112 (2.593%)  | 20.758%(34.751%)                  | 64.407(8.596%)    | 55.912(7.328%)    | 13.190%(14.751%)                  |
| LSTM                      | 38.239(4.266%)    | 29.143(2.821%)   | 23.787%(33.872%)                  | 39.688 ( 4.710% ) | 54.931(7.517%)    | -38.407%(-59.597%)                |
| SVR                       | 3.613(54.953%)    | 2.512(38.643%)   | 30.473%(29.680%)                  | 3.613(54.953%)    | 2.687 (43.608%)   | 25.630%(20.645%)                  |
| Rate RF                   | 2.215( 28.719% )  | 2.149(27.627%)   | 2.980%(3.802%)                    | 2.405( 29.062% )  | 2.404(29.299%)    | 0.042%(-0.815%)                   |
| FNN                       | 2.586(34.065%)    | 1.861(25.646%)   | 28.036%(24.715%)                  | 2.424(29.629%)    | 1.943 (27.001%)   | 19.843%(8.870%)                   |
| Advance RNN               | 2.367(31.959%)    | 1.786( 25.972% ) | 24.546%(18.733%)                  | 2.121 (36.967%)   | 1.971( 28.685% )  | 7.072%(22.404%)                   |
| GRU                       | 2.124 (29.405%)   | 1.749 (28.723%)  | 17.655%(2.319%)                   | 2.173(31.787%)    | 2.137(29.780%)    | 1.657%(6.314%)                    |
| LSTM                      | 2.338(31.997%)    | 1.775(28.111%)   | 24.080%(12.145%)                  | 2.152 (30.102%)   | 2.189(31.483%)    | -1.719%(-4.588%)                  |
| SVR                       | 221.442(4.956%)   | 190.923(4.294%)  | 13.782%(13.358%)                  | 221.442(4.956%)   | 145.007(3.109%)   | 34.517%(37.268%)                  |
| RF                        | 85.340(0.956%)    | 99.354(1.434%)   | -16.421%(-50.000%)                | 110.099 (1.137%)  | 125.190(1.185%)   | -13.707%(-4.222%)                 |
| Thrust FNN                | 132.889(2.854%)   | 65.777 (0.590%)  | 50.502%(79.327%)                  | 83.898(1.262%)    | 76.749(0.928%)    | 8.521%(26.466%)                   |
| RNN                       | 78.607(1.187%)    | 68.987(0.588%)   | 12.238%(50.463%)                  | 83.702 ( 1.232% ) | 82.603(1.101%)    | 1.313%(10.633%)                   |
| GRU                       | 69.903 ( 0.844% ) | 69.119(0.855%)   | 1.122%(-1.303%)                   | 86.797(1.428%)    | 67.414 (0.621%)   | 22.331%(56.513%)                  |
| LSTM                      | 80.748(1.302%)    | 67.223( 0.546% ) | 16.750%(58.065%)                  | 86.724(1.458%)    | 66.159 ( 0.599% ) | 23.713%(58.916%)                  |

## 5 Conclusion

Although TBMs have been widely used in various tunnel construction projects, there still remain some challenges in their machinery design and construction safety. Many research interests are inspired to explore the TBMs' risk evaluation, fault diagnostics and prognostics. One key to these problems is the real-time forecast of the TBM load parameters (including torque, advance rate and thrust), which requires that the forecast models should instantaneously provide the accurate future values of these parameters during the next period as long as the current operational data are collected. There have been many works on the forecast of TBM operational parameters, while it is still challenging to realize a true sense of 'real-time' forecast.

In this paper, we use the ML methods to develop the models for the real-time forecast of the TBM load parameters. In particular, we adopt the shallow-learning models (including SVR, RF and FNN) and the deep-learning models (RNN, LSTM, GRU) as the forecast models, respectively. Different from the non-sequential learning problems which require that models should provide the estimate of the current real value when the current data are collected, the inputs of these real-time forecast models are a length of time series data containing the previous and the current data, and their outputs are the estimate of the future real values of the load parameters. Because of the loop structure, we find that these deep models outperform the shallow models in most case.

Moreover, we consider the forecast task in two kinds of modes: single-output, which allows the models generate the forecast result of one parameter each a time, and multiple-output, which requires that the models should simultaneously provide the forecast results of the three parameters. Although the experimental results show that the single-output models perform better than multiple-output models, three individual single-output models should be develop for the three TBM load parameters. In contrast, one multiple-output model can simultaneously provide the forecast of the three parameters, and thus it has a higher operating efficiency.

In addition, we also use the least absolute shrinkage and selection (Lasso) method to extract essential features of the three parameters according to the magnitude of their Lasso coefficients. Based on the extracted features, we then develop the real-time forecast models for the TBM load parameters. The experimental results show that this manner brings a significant performance gain in most cases. In our future works, we will consider the application of the proposed ML-based models in TBM health monitoring and fault prognostics.

## A Important Features in TBM Operational Data

In the appendix, we list some important features appearing in the in-situ TBM operational data.

Table 3: Some Features in TBM Operation Data [29]

| Parameter (Unit)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | Parameter (Unit)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Temperature of oil tank ( ◦ C) Rotation speed of cutter(r/min) Propelling pressure (bar) Propelling pressure of B group (bar) Propelling pressure of D group (bar) Pressure of articulation system (bar) Pressure of Shield tail seal at right front (bar) Pressure of Shield tail seal at top right back (bar) Pressure of Shield tail seal at bottom left back (bar) Pressure of Shield tail seal at top left front (bar) Pressure of Shield tail seal at top left back (bar) Rolling angle ( ◦ ) Pressure of chamber at top left (bar) Pressure of chamber at bottom right (bar) Temperature of screw conveyor ( ◦ C) Thrust of cutterhead (kN) Torque of cutterhead (kNm) Displacement of B group of thrust cylinders (mm) Displacement of D group of thrust cylinders (mm) Displacement of articulated system at bottom left (mm) Displacement of articulated system at bottom right (mm) Pressure of screw conveyor at front (bar) | Temperature of gear oil ( ◦ C) Cutter power (kw) Propelling pressure of A group (bar) Propelling pressure of C group (bar) Pressure of equipment bridge (bar) Pressure of Shield tail seal at top right front (bar) Pressure of Shield tail seal at bottom left front (bar) Pressure of Shield tail seal at right back (bar) Pressure of Shield tail seal at left front (bar) Pressure of Shield tail seal at left back (bar) Pressure of Shield tail seal at bottom right back (bar) Pressure of screw pump at back (bar) Pressure of chamber at bottom left (bar) Bentonite pressure (bar) Pitch angle ( ◦ ) Advance rate (mm/min) Displacement of A group of thrust cylinders (mm) Displacement of C group of thrust cylinders (mm) Displacement of articulated system at top right (mm) Displacement of articulated system at top left (mm) Bentonite pressure of shield shell (bar) Pressure of screw pump (bar) |

## Acknowledgment

This work is supported by the National Key R&amp;D Program of China (Grant No. 2018YFB1700704 &amp; 2018YFB1702502) and the National Natural Science Foundation of China (Grant No. 11401076 &amp; 61473328).

## References

- [1] Miura, K., 2003. Design and construction of mountain tunnels in japan. Tunn. Undergr. Space Technol. 18 (2-3), 115-126. doi:http://dx.doi.org/10.1016/S0886-7798(03)00038-5 .
- [2] Edalat, K., Vahdatirad, M. J., Ghodrat, H., Firouzian, S., Barari, A., 2010. Choosing tbm for tabriz subway using multi criteria method. J. Civ. Eng. Manag. 16 (4), 531-539. doi:https://doi.org/10.3846/jcem.2010.59 .
- [3] M. Cigla, S. Yagiz, L. Ozdemir., 2001. Application of tunnel boring machines in underground mine development. in: E. ¨ Unal, B. ¨ Unver, E. Tercan (Eds.), Proceeding of the 17th International Mining Congress and Exhibition of Turkey, Ankara, Turkey, pp. 155-164, ISBN:97S-395-417-4. URL http://www.maden.org.tr/resimler/ekler/43857f4a06c8521\_ek.pdf
- [4] Hong, E. S., Lee, I. M., Shin, H. S., Nam, S. W., Kong, J. S., 2009. Quantitative risk evaluation based on event tree analysis technique: application to the design of shield tbm. Tunn. Undergr. Space Technol. 24 (3), 269-277. doi:http://dx.doi.org/10.1016/j.tust.2008.09.004 .
- [5] Cho, S., Ahn, M. Y., Lee, D. W., Park, Y. H., Lee, E. H., Jin, H. G., Lee, C. W., Kim, T. K., Chun, Y. B., Kim, S. K., et al., 2014. Design and r&amp;d progress of korean hccr tbm. Fusion Eng. Des. 89 (7-8), 1137-1143. doi:http://dx.doi.org/10.1016/j.fusengdes.2014.01.032 .

- [6] Wu, X., Liu, H., Zhang, L., Skibniewski, M. J., Deng, Q., Teng, J., 2015. A dynamic bayesian network based approach to safety decision support in tunnel construction. Reliab. Eng. Syst. Saf. 134, 157-168. doi:https://doi.org/10.1016/j.ress.2014.10.021 .
- [7] Kothamasu, R., Huang, S. H., VerDuin, W. H., 2006. System health monitoring and prognostics - a review of current paradigms and practices. Int. J. Adv. Manuf. Technol. 28 (9-10), 1012-1024. doi:http://dx.doi.org/10.1007/s00t70-004-2131-6 .
- [8] Wang, L., Kang, Y., Zhao, X., Zhang, Q., 2015. Disc cutter wear prediction for a hard rock tbm cutterhead based on energy analysis. Tunn. Undergr. Space Technol. 50, 324-333. doi:https://dx.doi.org/10.1016/j.tust.2015.08.003 .
- [9] Talebi, K., Memarian, H., Rostami, J., Gharahbagh, E. A., 2015. Modeling of soil movement in the screw conveyor of the earth pressure balance machines (epbm) using computational fluid dynamics. Tunn. Undergr. Space Technol. 47, 136-142. doi:https://doi.org/10.1016/j.tust.2014.12.008 .
- [10] Javad, G., Narges, T., 2010. Application of artificial neural networks to the prediction of tunnel boring machine penetration rate. Min. Sci. Tech. 20 (5), 727-733. doi:http://dx.doi.org/10.1016/S1674-5264(09)60271-4 .
- [11] Delisio, A., Zhao, J., Einstein, H., 2013. Analysis and prediction of tbm performance in blocky rock conditions at the l¨ otschberg base tunnel. Tunn. Undergr. Space Technol. 33, 131-142. doi:https://doi.org/10.1016/j.tust.2012.06.015 .
- [12] Gong, Q., Zhao, J., 2009. Development of a rock mass characteristics model for tbm penetration rate prediction. Int. J. Rock Mech. Min. Sci. 46 (1), 8-18. doi:https://doi.org/10.1016/j.ijrmms.2008.03.003 .
- [13] Ates, U., Bilgin, N., Copur, H., 2014. Estimating torque, thrust and other design parameters of different type tbms with some criticism to tbms used in turkish tunneling projects. Tunn. Undergr. Space Technol. 40, 46-63. doi:https://doi.org/10.1016/j.tust.2013.09.004 .
- [14] Wang, X., Yuan, Y., Mu, X., Sun, W., Song, X., 2019. Sensitivity of tbm¡ ¯ s performance to structural, control and geological parameters under different prediction models. IEEE Access 7, 19738-19751.
- [15] Shi, M., Sun, W., Zhang, T., Liu, Y., Wang, S., Song, X., 2019. Geology prediction based on operation data of tbm: comparison between deep neural network and soft computing methods. in: The 1st International Conference on Industrial Artificial Intelligence (IAI), pp. 1-5. doi:10.1109/ICIAI.2019.8850794 .
- [16] Zhao, J., Shi, M., Hu, G., Song, X., Zhang, C., Tao, D., Wu, W., 2019. A data-driven framework for tunnel geological-type prediction based on tbm operating data. IEEE Access 7, 66703-66713.
- [17] Krause, H., 1976. Geologische erfahrungen beim einsatz von tunnelvortriebsmaschinen in badenwiirttemberg. Neue Erkenntnisse im Hohlraumbau - Fundierungen im Fels/Latest Findings in the Construction of Underground Excavations - Rock Foundations, Springer, Vienna, 49-60. doi:https://doi.org/10.1007/978-3-7091-8452-3\_3 .
- [18] Yagiz, S., 2017. New equations for predicting the field penetration index of tunnel boring machines in fractured rock mass. Arab. J. Geosci. 10 (2), 33. doi:https://doi.org/10.1007/s12517-016-2811-1 .

- [19] Hamidi, J. K., Shahriar, K., Rezai, B., Rostami, J., 2010. Performance prediction of hard rock tbm using rock mass rating (rmr) system. Tunn. Undergr. Space Technol. 25 (4), 333-345. doi:https://doi.org/10.1016/j.tust.2010.01.008 .
- [20] Hassanpour, J., Rostami, J., Khamehchiyan, M., Bruland, A., Tavakoli, H., 2010. Tbm performance analysis in pyroclastic rocks: a case history of karaj water conveyance tunnel. Rock Mech. Rock Eng. 43 (4), 427-445. doi:https://doi.org/10.1007/s00603-009-0060-2 .
- [21] Gertsch, R., Gertsch, L., Rostami, J., 2007. Disc cutting tests in colorado red granite: Implications for tbm performance prediction. Int. J. Rock Mech. Min. Sci. 44 (2), 238-246. doi:https://doi.org/10.1016/j.ijrmms.2006.07.007 .
- [22] Entacher, M., Lorenz, S., Galler, R., 2014. Tunnel boring machine performance prediction with scaled rock cutting tests. Int. J. Rock Mech. Min. Sci. 70, 450-459. doi:https://doi.org/10.1016/j.ijrmms.2014.04.021 .
- [23] Xue, J., Xia, Y., Ji, Z., Zhou, X., 2009. Soft rock cutting mechanics model of tbm cutter and experimental research. International Conference on Intelligent Robotics and Applications. Springer, Berlin, Heidelberg, 383-391. doi:https://doi.org/10.1007/978-3-642-10817-4\_38 .
- [24] Shi, H., Yang, H., Gong, G., Wang, L., 2011. Determination of the cutterhead torque for epb shield tunneling machine. Autom. Constr. 20 (8), 1087-1095. doi:https://doi.org/10.1016/j.autcon.2011.04.010 .
- [25] Wang, L., Gong, G., Shi, H., Yang, H., 2012. Modeling and analysis of thrust force for epb shield tunneling machine. Autom. Constr. 27, 138-146. doi:https://doi.org/10.1016/j.autcon.2012.02.004 .
- [26] Zhang, Q., Su, C., Qin, Q., Cai, Z., Hou, Z., Kang, Y., 2016. Modeling and prediction for the thrust on epb tbms under different geological conditions by considering mechanical decoupling. Sci. ChinaTechnol. Sci. 59 (9), 1428-1434. doi:https://doi.org/10.1007/s11431-016-6096-0 .
- [27] Kasper, T., Meschke, G., 2006. On the influence of face pressure, grouting pressure and tbm design in soft ground tunnelling. Tunn. Undergr. Space Technol. 21 (2), 160-171. doi:https://doi.org/10.1016/j.tust.2005.06.006 .
- [28] Su, C., Wang, Y., Zhao, H., Su, P., Qu, C., Kang, Y., Huang, T., Cai, Z., Wang, L., 2011. Analysis of mechanical properties of two typical kinds of cutterheads of shield machine. Adv. Sci. Lett. 4 (6-7), 2049-2053. doi:https://doi.org/10.1166/asl.2011.1545 .
- [29] Gao, X., Shi, M., Song, X., Zhang, C., Zhang, H., 2019. Recurrent neural networks for real-time prediction of tbm operating parameters. Autom. Constr. 98, 225-235. doi:https://doi.org/10.1016/j.autcon.2018.11.013 .
- [30] Bishop, C. M., 2006. Pattern recognition and machine learning. Springer. doi:ISBM:978-0-387-31073-2 .
- [31] Cybenko, G., 1989. Approximation by superpositions of a sigmoidal function. Math. Control Signal Syst. 2 (4), 303-314. doi:https://doi.org/10.1007/BF02551274 .
- [32] Jain, A. K., Mao, J., Mohiuddin, K., 1996. Artificial neural networks: A tutorial. Computer 29 (3), 31-44. doi:http://dx.doi.org/10.1109/2.485891 .

- [33] Williams, D., Hinton, G., 1986. Learning representations by back-propagating errors. Nature 323 (6088), 533-538. doi:https://doi.org/10.1038/323533a0 .
- [34] Pascanu, R., Mikolov, T., Bengio, Y., 2013. On the difficulty of training recurrent neural networks. in: S. Dasgupta, D. McAllester (Eds.), Proceedings of the 30th International Conference on Machine Learning, Atlanta, GA, USA , pp. 1310-1318. URL https://arxiv.org/abs/1211.5063
- [35] Hochreiter, S., Schmidhuber, J., 1997. Long short-term memory. Neural Comput. 9 (8), 1735-1780. doi:https://doi.org/10.1162/neco.1997.9.8.1735 .
- [36] Cho, K., Van Merri¨ enboer, B., Gulcehre, C., Bahdanau, D., Bougares, F., Schwenk, H., Bengio, Y., 2014. Learning phrase representations using rnn encoder-decoder for statistical machine translation. arXiv preprint arXiv:1406.1078. URL https://arxiv.org/abs/1406.1078
- [37] Tikhonov, A., Arsenin, V., 1977. Solutions of ill-posed problems. Scripta series in mathematics. V. H. Winston &amp; Sons, Washington, D.C.: John Wiley &amp; Sons, New York. doi:ISBN:9780470991244 .
- [38] Tibshirani, R., 1996. Regression shrinkage and selection via the lasso. J. R. Stat. Soc. Ser. BMethodol. 58 (1), 267-288. doi:http://dx.doi.org/10.1111/j.2517-6161.1996.tb02080.x .
- [39] Lai, Z., Nagarajaiah, S., 2019. Sparse structural system identification method for nonlinear dynamic systems with hysteresis/inelastic behavior. Mech. Syst. Signal Proc. 117, 813-842. doi:https://doi.org/10.1016/j.ymssp.2018.08.033 .
- [40] Bartkowiak, A., Zimroz, R., 2014. Dimensionality reduction via variables selection-linear and nonlinear approaches with application to vibration-based condition monitoring of planetary gearbox. Appl. Acoust. 77, 169-177. doi:http://dx.doi.org/10.1016/j.apacoust.2013.06.017 .
- [41] Tieleman,T., Hinton, G., 2017. Divide the gradient by a running average of its recent magnitude. coursera: Neural networks for machine learning, Technical report, Available online: https://zh. coursera. org/learn/neuralnetworks/lecture/YQHki/rmsprop-divide-the-gradient-by-arunning-average-of-its-recent-magnitude.

Figure 1: Structure of FNN with Two Hidden Layers

<!-- image -->

Flow chart

Figure 2: Structure of Recurrent Neural Networks

<!-- image -->

Engineering drawing

Figure 3: Structure of LSTM's Hidden Node

<!-- image -->

Engineering drawing

Figure 4: Structure of GRU's Hidden Node

<!-- image -->

Engineering drawing

Figure 5: Structure of RNN

<!-- image -->

Engineering drawing

Figure 6: Forecast Results of 'Torque'

<!-- image -->

Line chart

Figure 7: Forecast Results of 'Advance Rate'

<!-- image -->

Line chart

Figure 8: Forecast Results of 'Thrust'

<!-- image -->

Bar chart
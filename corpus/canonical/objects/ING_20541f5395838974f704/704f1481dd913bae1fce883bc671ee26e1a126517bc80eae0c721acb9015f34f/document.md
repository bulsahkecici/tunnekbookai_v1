## AL-iGAN: An Active Learning Framework for Tunnel Geological Reconstruction Based on TBM Operational Data

Hao Wang a , Lixue Liu a , Xueguan Song b , Chao Zhang a, ∗ , Dacheng Tao c

a

School of Mathematical Sciences, Dalian University of Technology, Dalian, 116024, China b School of Mechanical Engineering, Dalian University of Technology, Dalian, 116024, China c JD Explore Academy, JD.COM Inc., 100176, China

## Abstract

In tunnel boring machine (TBM) underground projects, an accurate description of the rock-soil types distributed in the tunnel can decrease the construction risk ( e.g. surface settlement and landslide) and improve the efficiency of construction. In this paper, we propose an active learning framework, called AL-iGAN, for tunnel geological reconstruction based on TBM operational data. This framework contains two main parts: one is the usage of active learning techniques for recommending new drilling locations to label the TBM operational data and then to form new training samples; and the other is an incremental generative adversarial network for geological reconstruction (iGAN-GR), whose weights can be incrementally updated to improve the reconstruction performance by using the new samples. The numerical experiment validate the effectiveness of the proposed framework as well.

Keywords: Tunnel boring machine, generative adversarial network, active learning, geological reconstruction, incremental learning

## 1. Introduction

With the advantage of high advance rate, environmental friendliness and security, tunnel boring machines (TBMs) have taken the place of the traditional tunneling techniques ( e.g. , drilling and blasting) as the primary construction method for various underground excavation projects such as highways [1], railway [2] and water conservancy [3]. However, there are still many challenges in the project applications of TBMs because it is difficult to explore the geological information in the TBM construction tunnel. Especially in some complex geological conditions, such as fracture zones, geological faults, aquifers, karst caves and underground rivers, the TBM excavation process will come with a high risk caused by an unanticipated presence of water leakage, caves and hard rocks, and even the finished TBM tunnel will also be faced with the risk of surface settlement and landslide. For instance, there have arisen two accidents of ground collapse caused by water and sand gushing during TBM construction in Nanjing and Tianjing, two Chinese cites, in 2007 and 2011, respectively. Therefore, an accurate description of the rock-soil types distributed in the TBM construction tunnel can effectively reduce the construction risk and improve the construction efficiency [4].

∗ Corresponding author

Email address: chao.zhang@dlut.edu.cn

(Chao Zhang)

## 1.1. Background and Motivation

The tunnel geological reconstruction is a principal means for exploring the geological information of the entire TBM tunnel. Compared with the geological prediction, which produces the estimation to the geological condition ahead of the tunnel face, the geological reconstruction aims to accurately describe the distribution information of rock-soil types appearing in the entire tunnel. A number of approaches have been developed to understand the geological condition, including the measurement-based methods and the data-based methods. The measurement-based methods adopt the destructive methods ( e.g. drilling and excavating [5, 6]) or the non-destructive methods ( e.g. the electrode equipped on the tunnel face [7] and the ground penetrating radar (GPR) [8]) to directly detect the rock-soil distribution information in a few specific locations along the tunnel alignment. However, it is almost technically impossible to accurately reconstruct the rock-soil distribution throughout the entire tunnel by only using the geological information at the discrete locations ( cf. Fig. 1).

(a) Real rock-soil distribution and discrete sampling locations (marked in red color)

<!-- image -->

Other

- (b) Geological reconstruction result obtained by using interpolation methods based on the discrete geological samples

Figure 1: Geological Reconstruction Based on Discrete Geological Sampling

As addressed above, since the measurement-based methods cannot directly detect the geological condition of the entire tunnel, the reconstruction results are likely to omit some crucial geological information. Instead, a number of different kinds of sensors are equipped on the TBM to collect its real-time operational data during the tunneling process, and the geological information of the entire construction tunnel will be encoded into the collected TBM operational data. The data-based geological reconstruction methods decode the useful features from TBM operational data indexed by the continuous time or displacement points, and then to develop the learning models for estimating the rock-soil distribution of the entire tunnel. The main research concerns on the data-based methods lie in the following three aspects:

- feature extraction - how to extract useful features from the TBM operational data that are indexed by the continuous time or displacement;
- learning model - how to design a reasonable regressor for estimating the thickness of each rock-soil type appearing in the tunnel alignment.
- quantity of data - how to handle the imbalance between the TBM operational data labeled with the geological information and the unlabeled

## TBM operational data;

In view of the sequentiality of TBM operational data, Liu et al. [9] employed the long-short-term-memory networks to capture the sequential characteristics of the training data and then to predict rock-soil types at the tunnel face. Leu and Adi [10] presented a model based on Hidden Markov model and neural network sand predict the probabilistic description of rock-soil types. Zhang et al. [11] utilized hierarchies algorithm to compressed data and adopted support vector classifiers as the learning models for justifying the appearance of some specific rock-soil types (rather than estimating their thickness). Zhao et al. [12] augmented features by using the first-order and the second-order difference information and designed a feed-forward artificial neural network (ANN) with two hidden layers as the predictor, where the second hidden layer has 7 nodes that correspond to 7 kinds of physical-mechanical indexes. Zhang [13] designed the generative adversarial networks for predicting the thicknesses of each rock-soil types based on TBM operational data, where the adversarial training strategy was adopted to exhaustively overcome the negative effects of the rarity of labeled TBM operational data. One main difficulty of these data-based methods lies in the quantity of data. Especially, when the labeled data are very few, these methods are no longer be available. Although one can supplement the labeled data by collecting the geological information at new locations, it is usually expensive and time-consuming to use the geological-condition detection methods ( e.g. drilling or GPR). A compromise way to handle this issue is to recommend new geological-condition detection locations to enrich the labeled operational data based on the training behavior of the reconstruction model developed by using the current labeled and unlabeled data.

## 1.2. Active Learning

In the traditional learning tasks, the samples are passively imposed into the learner in the training phase, and thus this kind of learning processes are also called passive learning. In contrast, the active learning refers to the learning process that the learner can actively explore the informative samples from the sample space and then add them into the subsequent training phase ( cf. Fig. 2). In this manner, the learning models developed by the active learning methods need a smaller size of labeled data than the learning models derived from the passive learning [14]. Taking advantage of this character, the active learning has been widely used in various applications, such as image recognition [15], text classification [16], visual question answering [17], and object detection [18]. Kim et al. [19] proposed a deep active learning approach to effectively reduce the number of training samples in the task of the vision-based monitoring on construction sites. In general, according to the query strategy ( i.e., the means of selecting the candidate data from the data pool), the active learning methods can be sorted into two types:

Figure 2: Pool-based active learning framework

<!-- image -->

Flow chart

- Uncertainty sampling (US) methods - Uncertainty sampling methods consider the model's prediction reliability of the data, and take the data with the largest uncertainty as the data for active learning query. [20, 21, 22]
- Query by committee (QBC) methods - Query by committee methods are similar to ensemble methods in machine learning, voting on data based

on the results predicted by multiple models and querying target data. [23, 24, 25]

## 1.3. Incremental Learning

The goal of incremental learning is to update the previous model to fit newly added samples and meanwhile not to lose the memory of the previous training. In other words, it is expected that the learning model can be updated to fit both the previous and newly added samples, when new samples are available. In the literature, there are three kinds of incremental learning strategies including the architecture-based manner [26], the rehearsal-based manner [27, 28] and the regularization-based manner [29, 30].

- The architecture-based manner equips new neurons into the previouslytrained network when new samples are available, and then, freezing the other weights, use the new samples (sometimes with a part of previous samples) to train the weights associated with these neurons. When there are multi-round newly added samples, this manner will significantly enlarge the size of the network and influence the generalization performance of the final network.
- The rehearsal-based manner selects a part of previous samples and combine them with the newly added samples to form new training samples. This manner could change the distribution of training samples and damage the previous training result of the learning model, which would not fit the previous samples yet.
- The regularization-based manner introduces the regularization terms into the objective function to prevent the learning model from losing the memory of the previous training, when the previously-trained learning models are updated by using the new samples (sometimes, with a part of previous samples).

Compared with the others, the regularization-based method has a high feasibility and is applicable to the incremental learning of many complicated deep learning models.

## 1.4. Overview of Main Results

As addressed above, the main challenge of tunnel geological reconstruction is the lack of labeled samples that can accurately describe the geological condition, especially the sudden changes, of the TBM construction tunnel. Taking advantages of the mechanism of actively acquiring informative samples, we propose an active learning-based framework, called AL-iGAN, for tunnel geological reconstruction to solve this issue ( cf. Fig. 3). The proposed framework contains two parts: one is the usage of active learning methods and the other is a generative adversarial network for incremental learning.

The tunnel geological information is encoded into TBM operational data, collected from the sensors on TBM equipments during the construction phase and a small part of the operational data are labeled with the geological condition by using the drilling method. Unfortunately, the limited size of labeled TBM operational data cannot provide the satisfactory reconstruction results. The active learning methods are used to select the unlabeled operational data that will benefit to the geological reconstruction performance. The drilling method is used again to explore the geological condition at the tunnel locations associated with these unlabeled operational data. Subsequently, the selected operational data will be labeled for a new training phase.

To improve the training efficiency and the reconstruction performance, we also design an incremental generative adversarial network for the geological reconstruction (iGAN-GR), which can be incrementally updated by using the new training samples rather than to be totally retrained. The proposed iGAN-GR is composed of two sub-networks: a generator and a discriminator. The former produces the estimate of the thickness of each rock-soil type appearing in the TBM construction tunnel, and the latter not only justifies whether the input data are the generator outputs or the real training samples but also checks whether the input data are fresh or previous training samples. Since TBM operational data have strong sequentiality and labeled samples are not sufficient, we adopt a positional-encoding attention layer [31] in the generator of iGAN-GR to improve the reconstruction performance. In addition, following the regularization-based manner, we also adopt the elastic weight consolidation (EWC) loss, proposed in [29], as the regularization terms in the generative and the discriminative losses for training iGAN-GR. The numerical experiments support the effectiveness of the proposed framework and show that the active learning methods can effectively find the the most informative operational data that significantly improve the reconstruction performance.

Figure 3: A diagram of active learning for TBM tunnel geological reconstruction. We first develop a reconstruction model by using the training samples composed of the geological information at the previous drilling locations (marked in red color) and the corresponding TBM operational data (marked in red color). If the resultant model performs unsatisfactorily, we further use the active learning method to recommend new drilling locations (marked in blue color) and then form new training samples, composed of the geological information at the previous drilling locations and the corresponding TBM operational data (marked in blue color), to update the previous model.

<!-- image -->

Engineering drawing

The rest of this paper is organized as follows. In Section 3.1, we summarize the query strategies of active learning used in this paper. In Section 2, we introduce the structure and training strategy of iGAN-GR. Section 3 presents the AL-iGAN framework for geological reconstruction. In Section 4, we conduct the numerical experiments to examine the proposed framework and the last section concludes this paper.

## 2. Incremental Generative Adversarial Network for Geological Reconstruction (iGAN-GR)

Generative adversarial networks (GANs), originally proposed in [32], are referred to a body of neural networks that are composed of two subnetworks: a generator and a discriminator, and trained by means of the minimax game between them. In general, the generator is a feedforward neural network (FNN) that implements the data (such as image and time series) generation tasks or the supervised learning tasks (such as classification and regression). The discriminator is also an FNN that roughly has a symmetric network structure of the generator. During the minimax game training, the discriminator will be trained to identify whether the output of generator is a real instance and the generator will be trained to provide a high-quality approximation of the real instance such that the discriminator is unable to identify the output of generator from the real instance. When reaching Nash equilibrium [33], the generator is deemed to fully capture the characteristics of the real-instance distribution. Taking advantages of the minimax game training where the discriminator guides the training of generator, many empirical evidences demonstrate that, given a sample set, the generator of GAN can perform better than an FNN with the same structure, trained by using the stochastic gradient descent (SGD) method [34, 35].

Zhang et al. [13] developed a GAN model, called GAN-GP, for geological prediction. However, this model is unsuitable (at least cannot be directly applied) to the geological reconstruction task considered in this paper. First, the labeled samples are fewer than those in the scenario of geological prediction; and second, there is no incremental learning mechanism in the training strategy of GAN-GP and thus it cannot be incrementally updated by using a limited amount of new labeled samples. To overcome these shortcomings, we designed an incremental generative adversarial network for geological reconstruction (iGAN-GR), whose weights can be incrementally updated by using the new samples recommended in the active learning phase. In Tab. 1, we summarize the main mathematical notations mentioned in this paper.

## 2.1. Structure of iGAN-GR

Similar to the structure of traditional GANs, iGAN-GR is also composed of two sub-networks: a generator and a discriminator ( cf. Fig. 4). Next, we will demonstrate the structure characteristics of iGAN-GR's generator and discriminator, respectively.

The generator of iGAN-GR, denoted as G[ · ], consists of two parts: the feature extraction part and the regression part. The former is a combination of the multi-head self-attention (MSA) module and the position encoding (PE) module in parallel. Different for the ordinary convolution operation that detects the local features from the patches of the input data, the MSA module captures the global features of the input data by mapping them into different subspaces spanned by the weight vectors. Specifically, given an input x ∈ R d x , the output of the MSA is expressed as

Table 1: List of mathematical notations

| Notation                                             | Meaning                                                 | Notation          | Meaning                                                                   |
|------------------------------------------------------|---------------------------------------------------------|-------------------|---------------------------------------------------------------------------|
| d x                                                  | Dimension of input x                                    | w 0 ,p            | The p -th weight of net 0                                                 |
| G[ · ]                                               | iGAN-GR's generator                                     | α 0 ,p            | Change rate of gradient of w p in net 0 ( · )                             |
| y MSA                                                | Output of MSA module                                    | S t               | Training dataset for t -th incremental training stage                     |
| cnt[ · ]                                             | Concatenation of vectors                                | net k t           | Network after the k -th optimization iteration and the t -th sample query |
| d y                                                  | Dimension of output y                                   | L EWC             | Elastic weight consolidation loss                                         |
| L                                                    | Number of heads in MSA module                           | L IS              | Incremental supervised loss                                               |
| h l                                                  | The l -th head in MSA module                            | L ( k ) G ( S t ) | Generative loss after the k -th iteration and t -th sampling query        |
| σ                                                    | Softmax function                                        | L ( k ) D ( S t ) | discriminator loss after the k -th iteration and t -th sampling query     |
| y PE                                                 | Output of PE module                                     | η d               | Learning rate for minimizing L D                                          |
| [ x i ] 2 k                                          | The 2 k -th component of x i                            | η g               | Learning rate for minimizing L G                                          |
| y FE                                                 | Output of the feature extraction part                   | η s               | Learning rate for minimizing L S                                          |
| I                                                    | the size of training samples                            | λ d               | Control factor corresponding to L EWC for discriminator                   |
| D r / g [ · ]                                        | Discriminator output for real or generative instances   | λ g               | Control factor corresponding to L EWC for generator                       |
| D o / f [ · ]                                        | Discriminator output for original or fresh samples      | β d               | Control factor corresponding to L IS for discriminator                    |
| S 0 = { x (0 ,i ) , y (0 ,i ) } I 0 i =1             | Original training samples                               | β g               | Control factor corresponding to L IS for generator                        |
| I t                                                  | Training sample size for the t -th incremental training | W G               | Generator weights                                                         |
| L D                                                  | Discriminative loss                                     | W D               | Discriminator weights                                                     |
| L G                                                  | Generative loss                                         | x add ( t,j )     | the j -th point in S add t                                                |
| L S                                                  | Supervised loss                                         | D ( k )           | Discriminator after the k -th optimization iteration                      |
| ‖·‖ 2                                                | Euclidean norm                                          | G ( k )           | Generator after the k -th optimization iteration                          |
| S add t = { x add ( t,j ) , y add ( t,j ) } J t j =1 | Newly-added training dataset in the t -th sample query  | L ( k ) D         | Discriminative loss after the k -th optimization iteration                |
| τ [ · ]                                              | Indicator function for original or fresh samples        | L ( k ) G         | Generative loss after the k -th optimization iteration                    |
| net 0 ( · )                                          | Pre-existing network for initial training stage         | x ′ EN            | Point queried via entropy sampling                                        |
| P = { x pool m }                                     | Data pool                                               | x ′ VE            | Point queried via vote entropy based on QBC                               |
| x ( t,i )                                            | the i -th point in the t -th sample query               | x query t         | Point selected in the t -th sample query                                  |
| C                                                    | Committee in QBC method                                 | iGAN-GR t         | Network after t -th sampling query                                        |

Figure 4: Structure of iGAN-GR

<!-- image -->

Flow chart

<!-- formula-not-decoded -->

where σ : R → R is the softmax function; cnt[ · ] stands for the concatenation of vectors; L is the number of heads; and W Q l , W K l , W V l , W O are undetermined weights. There is a caveat that the individual usage of MSA module is possible to miss some important local features of the data, especially for the data that have strong sequentiality. Therefore, the PE module, which detects the positional relationship among the different inputs, is employed to collaborate with the MSA module:

<!-- formula-not-decoded -->

with

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

where [ x i ] 2 k (resp. [ x i ] 2 k +1 ) is the 2 k -th (resp. 2 k +1-th) component of the vector x i ∈ R d x and i ∈ { 1 , · · · , I } is the index of the input x i . It is noteworthy that the structure of PE module is fixed and there is no undetermined weight to be trained during the training phase. Moreover, given an input x i ( i ∈ { 1 , 2 , · · · , I } ), the output of the feature extraction part is expressed as:

<!-- formula-not-decoded -->

Then, the regression part is a stack of several fully-connected layers and each node of its output layer signifies the relative thickness of each rock-soil type appearing in the TBM construction tunnel.

The discriminator of iGAN-GR is also a stack of fully-connected layers and usually roughly symmetric with the structure of the regression part of the generator. The input of the discriminator is either a real instance ( i.e., the pair of an input vector and its real geological labels) or a generative instance ( i.e., the pair of an input vector and the corresponding generator output). Different from the traditional GANs, the discriminator of iGAN-GR has two output nodes of 0-1 form, denoted as D r / g [ · ] and D o / f [ · ], respectively. The first one D r / g [ · ] indicates whether the input pair is a real instance, labeled with '1' or a generative instance, labeled with '0'; and the second one D o / f [ · ] indicates whether the input pair is derived from the fresh training data that are recommended by the active learning models, labeled with '1' or from the original or previous training data, labeled with '0'.

Subsequently, we will address the training strategy of iGAN-GR that contains two stages: the initial training stage and the incremental training stage. The former is to initially train iGAN-GR based on the existed samples; and the latter is to incrementally update the weights of iGAN-GR by using the fresh training data that are recommended by the active learning models.

## 2.2. Initial Training Stage of iGAN-GR

Let S 0 := { x (0 ,i ) , y (0 ,i ) } I 0 i =1 ⊂ R d x × R d y be the original training dataset. In the initial training stage, since there are no newly-added training data, we only need to consider the first discriminator output D r / g [ · ]. Then, the discriminative loss is designed as follows:

<!-- formula-not-decoded -->

The minimization of L D ( S 0 ) aims to improve the reconstruction performance of generator and meanwhile to make the discriminator more accurately identify whether its input is a real instance.

On the other hand, the generative loss is defined as:

<!-- formula-not-decoded -->

The minimization of L G ( S 0 ) will make the generator accurately approximate the distribution of training data so as to fake the discriminator.

To enhance the training stability, we also introduce the supervised loss L S ( S 0 ) to balance the training levels of the generator and the discriminator in each iteration:

<!-- formula-not-decoded -->

where ‖·‖ 2 stands for the Euclidean norm. During each iteration of the adversarial training process, we minimize the supervised loss L S to refine the generator weights to prevent the generator to be misguided by the discriminator that is not well trained. These loss functions will be minimized by using minibatch Adam method [36] and the main workflow of iGAN-GR's initial training stage is illustrated in Alg. 1.

## Algorithm 1 Workflow of Initially Training iGAN-GR

Input: S 0 , K , η g , η d , η s ;

Output: generator weights W G , discriminator weights W D ;

- 1: Randomly initialize W G and W D ;
- 2: Minimize the supervised loss L S ( S ) to pre-train the generator and obtain the generator weights W (0) G ;
- 3: for all k = 1 , 2 , · · · , K ; do
- 4: Update W ( k - 1) G by minimizing the supervised loss L S ( S 0 ): W ( k, 1) G = W ( k - 1) G - η s · ∂ L S ( S 0 ) ∂ W ( k - 1) G ;
- 5: Update W ( k, 1) G and W D by minimizing the discriminative loss L D ( S 0 ): W ( k, 2) G = W ( k, 1) G - η d · ∂ L D ( S 0 ) ∂ W ( k, 1) G and W ( k, 1) D = W ( k ) D - η d · ∂ L D ( S 0 ) ∂ W D ;
- 6: Update W ( k, 2) G by minimizing the supervised loss L S ( S 0 ): W ( k, 3) G = W ( k, 2) G - η s · ∂ L S ( S 0 ) ∂ W ( k, 2) G ;
- 7: Update W ( k, 3) G and W ( k, 1) D by minimizing the generative loss L G ( S 0 ): W ( k, 4) G = W ( k, 3) G - η g · ∂ L G ( S 0 ) ∂ W ( k, 3) G and W ( k +1) D = W ( k, 1) D - η g · ∂ L G ( S 0 ) ∂ W ( k, 1) D ;
- 8: Update W ( k, 4) G by minimizing the supervised loss L S ( S 0 ): W ( k +1) G = W ( k, 4) G - η s · ∂ L S ( S 0 ) ∂ W ( k, 4) G ;
- 9: end for
- 2.3. Incremental Training Stage of iGAN-GR

Let S add t := { x add ( t,j ) , y add ( t,j ) } J t j =1 ⊂ R d x × R d y be the newly-added training dataset that are recommended by using the active learning model for the t -th time. Define an indicator function τ [ · ] : R d x × R d y →{ 0 , 1 } as

<!-- formula-not-decoded -->

which signifies whether a training datum ( x , y ) is newly-added.

In the incremental training stage, we adopt the elastic weight consolidation (EWC), a regularization-based incremental learning method proposed in [29], to update the iGAN-GR's weights when the newly-added training data are available. Let net 0 ( · ) : R d x → R d y be a pre-existing network with P weights w 0 , 1 , · · · , w 0 ,P that has been trained by using the original training dataset S 0 := { x (0 ,i ) , y (0 ,i ) } I 0 i =1 , and denote

<!-- formula-not-decoded -->

which recodes the change rate of gradient of the p -th weight w p in the previous process of training net 0 ( · ). A large α 0 ,p means that the weight w 0 ,p will be significantly updated in the training process. Then, combining a part (usually 80%) of the original training dataset S 0 with the newly-added dataset S add 1 to form a new training dataset S 1 := { x (1 ,i ) , y (1 ,i ) } I 1 i =1 ⊂ S 0 ∪ S add 1 , we implement a new process of training net 0 ( · ). Let net ( k ) 1 ( · ) be the network after the k -th iteration and w ( k ) 1 , 1 , · · · , w ( k ) 1 ,P be the newly-updated weights accordingly. The EWC loss of the newly-updated network is expressed as

<!-- formula-not-decoded -->

The minimization of L EWC (net ( k ) 1 ) aims to control the updating amplitude of the weights that sensitive in the training process. In this manner, the previous weights w 0 ,p are used to control the training behavior of the newly-updated network net ( k ) 1 and then to prevent the new network net ( k ) 1 from forgetting the previous training information.

During the new training process, the discriminator is also equipped with an extra output node D o / f [ · ], which indicates whether the input pair is derived from the fresh training dataset S add 1 or from the previous training dataset S 0 . Accordingly, we introduce the incremental supervised (IS) loss:

<!-- formula-not-decoded -->

The minimization of L IS ( S ) aims to make the discriminator distinguish between the fresh data and the previous data and meanwhile the generator can be guided not only to fit the fresh training dataset S add 1 but also to maintain the memory on the previous training dataset S 0 .

Overall, in the incremental training stage, the generative loss after the k -th iteration is expressed as

<!-- formula-not-decoded -->

where G ( k ) stands for the generator after the k -th iteration; and λ g &gt; 0 (resp. β g &gt; 0) is the control factor corresponding to the EWC (resp. IS) loss. Similarly, the discriminative loss for incremental training is given by

<!-- formula-not-decoded -->

where D ( k ) stands for the discriminator after the k -th iteration; and λ d &gt; 0 (resp. β d &gt; 0) is the control factor corresponding to the EWC (resp. IS) loss. In addition, the supervised loss L S ( S ) is also employed to balance the training levels between the generator and the discriminator in each iteration during the incremental learning stage. Both of the two loss functions L ( k ) G ( S ) and L ( k ) D ( S ) are also optimized by using minibatch Adam method and the workflow is illustrated in Alg. 2

## 3. AL-iGAN Framework for Tunnel Geological Reconstruction

In this section, we show the workflow of the proposed AL-iGAN framework for tunnel geological reconstruction. First, we introduce some preliminaries on active learning.

## Algorithm 2 Workflow of Incrementally Training iGAN-GR

<!-- formula-not-decoded -->

Output: generator weights W G , discriminator weights W D ;

- 1: for all k = 1 , 2 , · · · , K ; do
- 2: Update W ( k - 1) G by minimizing the supervised loss L S ( S ): W ( k, 1) G = W ( k - 1) G - η s · ∂ L S ( S ) ∂ W ( k - 1) G ;
- 3: Update W ( k, 1) G and W (0) D by minimizing the discriminative loss L ( k ) D ( S ): W ( k, 2) G = W ( k, 1) G - η d · ∂ L ( k ) D ( S ) ∂ W ( k, 1) G and W ( k, 1) D = W ( k ) D - η d · ∂ L ( k ) D ( S ) ∂ W ( k ) D ;
- 4: Update W ( k, 2) G by minimizing the supervised loss L S ( S ): W ( k, 3) G = W ( k, 2) G - η s · ∂ L S ( S ) ∂ W ( k, 2) G ;
- 5: Update W ( k, 3) G and W ( k, 1) D by minimizing the generative loss L ( k ) G ( S ): W ( k, 4) G = W ( k, 3) G - η g · ∂ L ( k ) G ( S ) ∂ W ( k, 3) G and W ( k +1) D = W ( k, 1) D - η g · ∂ L ( k ) G ( S ) ∂ W ( k, 1) D ;
- 6: Update W ( k, 4) G by minimizing the supervised loss L S ( S ): W ( k +1) G = W ( k, 4) G - η s · ∂ L S ( S ) ∂ W ( k, 4) G ; 7: end for

## 3.1. Query Strategies of Active Learning

Here, we adopt the active learning with pool-based sampling, where the fresh points will be selected from a pool P = { x pool m } of inputs of candidate samples based on a query strategy, and then a human annotator will label these points to form new training samples. The query strategy is the key to active learning, and there are two kinds of the most frequently used query strategies: one is uncertainty sampling, which selects the points making the outputs of the current learning model have the greatest degree of uncertainty [20]; and the other is query-by-committee (QBC), which selects the points according to the voting results of the committee members [23].

## 3.1.1. Entropy-based Uncertainty-sampling (EUS) Strategy

Given a pool P = { x pool m } , let M S ( · ) : R d x → R d y stand for the current learning model that has been trained by using the original samples S 0 := { x (0 ,i ) , y (0 ,i ) } I 0 i =1 . Uncertainty sampling selects a point x ′ ∈ P such that the predicted value [ M S ( x ′ )] j ( j = { 1 , 2 , · · · , d y } ) have the smallest discrepancies, i.e., the learning model M S has the largest uncertainty at the point x ′ . Entropy sampling (ES) [21] chooses the point x ′ EN from the pool P in the way of

<!-- formula-not-decoded -->

Namely, the resultant point x ′ EN should make the distribution of predicted value [ M S ( x ′ )] j is closer to the uniform distribution than the other points in the pool.

## 3.1.2. Query-by-Committee (QBC) Strategy

One main shortcoming of uncertainty-sampling strategy is the computation of predicted value, which usually brings a heavy computational burden. Instead, QBC strategy sets up a committee C = {M 1 , · · · , M C } and the committee members M c are auxiliary learning models trained by using the original training samples. Each committee member votes on the rock-soil type of the maximum predicted value of the candidate input points in the pool P , and the input point with the highest level of disagreement among these voting results will be recommended to form a new training sample. Based on the vote entropy (VE) [24], the point x ′ VE is selected from the pool P in the way of

<!-- formula-not-decoded -->

where V ( j ) stands for the number of voting results that are the j -th label.

Remark 1. We normalized the thicknesses of each rock-soil types, and QBC is designed to be more concerned about the data with multiple rock-soil types which are harder to fit and predict than just one.

## 3.2. Workflow of AL-iGAN Framework

Given an original training dataset S 0 := { x (0 ,i ) , y (0 ,i ) } I 0 i =1 , we first train the iGAN-GR model via the workflow given in Alg. 1 and the resultant network is denoted as iGAN-GR 0 . Then, we adopt the active learning method to select the most informative operational datum x query 1 from the operational data pool P and then to retrieve the location corresponding to the selected data x query 1 in the construction tunnel. The operational data within 0 . 3m around this drilling location are labeled with the present rock-soil types and then gather them to form the newly-added training dataset S add 1 = { x (1 ,j ) , y (1 ,j ) } J 1 j =1 . Next, we randomly take 80% from the original training dataset S 0 and then combine them with the set S add 1 to form a new training dataset S 1 . We use it to incrementally train the network iGAN-GR 0 via the workflow given in Alg. 2. The resultant network is denoted as iGAN-GR 1 and is further used to query anther operational datum x query 2 from the pool P \ { x (1 ,j ) } J 1 j =1 . The combination of a 80% part of S 1 and the set S add 2 derived from x query 2 leads to an other new training dataset S 2 , which will be used to incrementally train the network iGAN-GR 2 .

Repeatedly, denote x query t as the operational datum selected in the t -th sample querying of the active learning method and S add t := { x add ( t,j ) , y add ( t,j ) } J t j =1 ⊂ R d x × R d y as the corresponding newly-added training dataset. Let iGAN-GR t stands for the network after the t -th incremental training based on the training dataset S t composed of a 80% part of S t - 1 and the set S add t . We repeat the aforementioned process of incrementally training based on the active learning method until the terminal condition is satisfied. The workflow of AL-iGAN framework is illustrated in Alg. 3.

## 4. Numerical Experiments

We conduct the numerical experiments to validate the proposed AL-iGAN framework for geological construction based on a real-world TBM operational data that are partially labeled with geological information. In the experiments, we mainly concern with the following issues:

- whether iGAN-GR performs better than the state-of-the-art learning models in the geological reconstruction tasks;
- whether the active learning can effectively improve the reconstruction performance;

## Algorithm 3 Workflow of AL-iGAN framework

Input: S 0 , iGAN-GR 0 , P ;

Output: iGAN-GR model;

- 1: for all t = 1 , 2 , · · · , T ; do
- 2: Used iGAN-GR t - 1 to query the most informative operational datum x query t from P \ {{ x (1 ,j ) } J 1 j =1 ∪ · · · ∪ { x ( t,j ) } J t j =1 } .
- 3: Gather the operational data within 0 . 3m around this drilling location to form the newly-added training dataset S add t .
- 4: Randomly take 80% from S t - 1 and then combine them with the set S add t to form S t .
- 5: Use S t to incrementally train the network iGAN-GR t - 1 via the workflow given in Alg. 2 and get iGAN-GR t .

## 6: end for

- the comparison between different query strategies of active learning.
- the effect of incremental learning in the geological reconstruction tasks.

All experiments are performed on a computer equipped with Intel R i9-10850K CPU at 3.60 GHz × 8, 64GB RAM and two Nvidia R GTX-3080 graphic cards.

## 4.1. Data Preparation

The operational data are collected by sensors on the earth pressure balance shield machine that was operated in an urban subway construction project. The tunnel is about 2000m long with the diameter of 6 . 3 meters and the project route is divided into 1364 ring sections, each of which is about 1 . 5m long. The ground elevation is 0 . 14 ∼ 5 . 86m and the tunnel ground depth is within 11 . 8 ∼ 25 . 4m. There are a total of 4 . 6 million operational data, and each data has d x = 69 attributes corresponding to different operational parameters, such as torque, thrust, tunneling speed and fuel tank temperature.

The geological information is detected by using the drilling method at 88 locations at the ground surface above the construction tunnel. There are 11

rock-soil types appearing in the geological samples. They are signified by using different values of 7 physical and mechanical indicators given in Tab. 6. The thickness of the d y = 11 rock-soil types is set as the geological reconstruction result provided by iGAN-GR's generator.

The operational data within 0 . 3m around a drilling location are labeled with the rock-soil types appearing at the drilling point. We select 60 out of the 88 drilling locations to form the training and testing dataset, and the rest 28 are used to form the data pool for active learning. The 60 drilling locations provide 5186 labeled operational data, which are split into two parts: 3957 of them are used for training and the rest 1229 are used for testing. In the initial training stage, 75% of the training data are used to update the weights and the rest 25% are used for the validation of hyper-parameters.

For each one of the 28 drilling locations, we choose five operational data that lie at one-quarter, midpoint, three-quarter and both ends of the 0.6m-long line segment centering on the drilling location. The resultant 28 × 5 operational data form the data pool P for active learning. As long as an operational datum in P is recommended by the active learning method, we retrieve the drilling location corresponding to the operational datum and set the labeled operational data within 0 . 3m around this drilling location as the newly-added training samples.

## 4.2. Experiment Setting

In the feature-extraction part of iGAN-GR's generator, the MSA module has L = 8 heads, and no trainable weights are set in the PE module. The fully-connected part of iGAN-GR's generator has a 20-7-11 structure and symmetrically, iGAN-GR's discriminator has a structure of 11-7-20-2 fully-connected layers. The activation functions of the input and the hidden nodes of the two sub-networks are set as the ReLU functions. The output nodes of generator are activated by using the softmax function and the two output nodes of discriminator are both activated by using the Sigmoid function, respectively. The hyper-parameters of Adam optimizer for training iGAN-GR are listed in Tab. 2

Given a testing dataset S := { x n , y n } N n =1 , we adopt the mean square error

Table 2: The choices of hyper-parameters in the training of iGAN-GR

| Stage                |   K | η g    | η d    |   η s |   Size | λ d   | λ g   | β d   | β g   |
|----------------------|-----|--------|--------|-------|--------|-------|-------|-------|-------|
| Pre-training         | 200 | -      | -      | 0.005 |     32 | -     | -     | -     | -     |
| Initial training     | 300 | 0.0001 | 0.0005 | 0.001 |     88 | -     | -     | -     | -     |
| Incremental training | 100 | 0.0001 | 0.0005 | 0.001 |     32 | 500   | 500   | 1     | 1     |

1 'K' is the number of training iterations.

2 η g , η d and η s are the learning rates for minimizing the generative loss L G , the discriminator loss L D and the loss L S , respectively.

3 'Size' stands for the size of minibatch in the Adam optimizer.

4 λ d and λ g (resp. β d and β g ) are the control factors corresponding to the EWC (resp. IS) loss, respectively.

(MSE) over five repeated experiments on it as the performance criterion:

<!-- formula-not-decoded -->

where G[ x n ] is the output of the generator w.r.t. the testing input x n . Additionally, we adopt four state-of-the-art regressors as the comparative models including random forest regression (RFR), support vector regression (SVR), Xgboost regressor (XGBR) and GAN-GP [13]. The hyper-parameters of the first three models are determined by using five-fold cross validation and those of GAN-GP follow the relevant suggestion in [13]. For the sake of fairness, after querying samples every time, these comparative models share the same samples that are used to incrementally training iGAN-GR.

We adopt two kinds of active learning methods including the EUS method and the QBC method. Either of the two methods is repeatedly implemented nine times to query candidate operational data from the data pool. We introduce the performance-gain rate γ to measure the influence caused by the active learning methods to the reconstruction performance:

<!-- formula-not-decoded -->

where MSE t stands for the MSE of the reconstruction model after the t -th sample querying of active learning. In the QBC method, the committee models are set as ten iGAN-GRs, each of which is trained via the aforementioned workflow ( cf.

Alg. 3) based on randomly-selecting 80% of the original training data. It is noteworthy that, in the QBC method for each comparative model, the committee models are set as the same models that are trained in the aforementioned way. As a comparison, we also consider the random sampling (RS) method that randomly selects a point from the data pool and the newly-added training data are the labeled operational data associated with its corresponding drilling location.

## 4.3. Experimental Results

Figure 5: Geological reconstruction performance of different models with active learning methods.

<!-- image -->

Line chart

As shown in Fig. 5 and Tab. 3, taking advantages of the specific structure of discriminator and the appropriate incremental training strategy, the proposed iGAN-GR outperforms the other models in the task of geological reconstruction with incremental training samples that are recommended by active learning. The existence of discriminator output D o / f [ · ] makes iGAN-GR prevent from forgetting the previous training results when the newly-added samples are available for incrementally updating the weights of iGAN-GR. In contrast, although GAN-GP has the almost same structure of the proposed iGAN-GR except the discriminator output D o / f [ · ] and is also trained by using the same samples, its reconstruction performance becomes worse when the number of sample query increases. This phenomenon validates iGAN-GR's the specific structure and training strategy for incremental learning. Moreover, the EUS and the QBC active learning methods perform better than the RS method in the incremental training stage of iGAN-GR

Table 3: Averaged reconstruction performance (MSE) of different models with active learning methods

|   T | AL Model   |    SVR |    RFR |   XGBR |   GAN-GP |   iGAN-GR |
|-----|------------|--------|--------|--------|----------|-----------|
|   0 | RS         | 0.0187 | 0.0202 | 0.0191 |   0.0224 |    0.0190 |
|   0 | EUS        | 0.0187 | 0.0205 | 0.0191 |   0.0206 |    0.0189 |
|   0 | QBC        | 0.0187 | 0.0213 | 0.0191 |   0.0190 |    0.0183 |
|   1 | RS         | 0.0181 | 0.0183 | 0.0183 |   0.0183 |    0.0181 |
|   1 | EUS        | 0.0172 | 0.0199 | 0.0186 |   0.0171 |    0.0182 |
|   1 | QBC        | 0.0182 | 0.0185 | 0.0186 |   0.0192 |    0.0168 |
|   2 | RS         | 0.0176 | 0.0168 | 0.0178 |   0.0179 |    0.0159 |
|   2 | EUS        | 0.0161 | 0.0173 | 0.0183 |   0.0194 |    0.0175 |
|   2 | QBC        | 0.0177 | 0.0178 | 0.0161 |   0.0180 |    0.0156 |
|   3 | RS         | 0.0172 | 0.0172 | 0.0192 |   0.0189 |    0.0157 |
|   3 | EUS        | 0.0154 | 0.0179 | 0.0168 |   0.0187 |    0.0165 |
|   3 | QBC        | 0.0165 | 0.0186 | 0.0167 |   0.0164 |    0.0149 |
|   4 | RS         | 0.0169 | 0.0182 | 0.0200 |   0.0175 |    0.0145 |
|   4 | EUS        | 0.0150 | 0.0174 | 0.0165 |   0.0182 |    0.0162 |
|   4 | QBC        | 0.0163 | 0.0181 | 0.0163 |   0.0173 |    0.0142 |
|   5 | RS         | 0.0166 | 0.0188 | 0.0160 |   0.0170 |    0.0145 |
|   5 | EUS        | 0.0147 | 0.0200 | 0.0161 |   0.0149 |    0.0148 |
|   5 | QBC        | 0.0160 | 0.0188 | 0.0167 |   0.0190 |    0.0142 |
|   6 | RS         | 0.0164 | 0.0195 | 0.0165 |   0.0248 |    0.0142 |
|   6 | EUS        | 0.0146 | 0.0207 | 0.0184 |   0.0180 |    0.0126 |
|   6 | QBC        | 0.0158 | 0.0217 | 0.0168 |   0.0210 |    0.0138 |
|   7 | RS         | 0.0160 | 0.0215 | 0.0156 |   0.0195 |    0.0134 |
|   7 | EUS        | 0.0146 | 0.0225 | 0.0177 |   0.0159 |    0.0115 |
|   7 | QBC        | 0.0161 | 0.0234 | 0.0150 |   0.0201 |    0.0131 |
|   8 | RS         | 0.0162 | 0.0250 | 0.0165 |   0.0236 |    0.0118 |
|   8 | EUS        | 0.0148 | 0.0260 | 0.0184 |   0.0165 |    0.0110 |
|   8 | QBC        | 0.0163 | 0.0263 | 0.0158 |   0.0248 |    0.0127 |
|   9 | RS         | 0.0164 | 0.0265 | 0.0164 |   0.0243 |    0.0112 |
|   9 | EUS        | 0.0152 | 0.0285 | 0.0174 |   0.0165 |    0.0101 |
|   9 | QBC        | 0.0167 | 0.0298 | 0.0173 |   0.0209 |    0.0104 |

Table 4: Performance gain γ t of different models after the t -th active learning

| AL    | RS      | RS      | RS      | RS      | RS      | EUS     | EUS     | EUS     | EUS     | EUS     | QBC     | QBC     | QBC     | QBC     | QBC     |
|-------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|
| Model | SVR     | RFR     | XGBR    | GAN-GP  | iGAN-GR | SVR     | RFR     | XGBR    | GAN-GP  | iGAN-GR | SVR     | RFR     | XGBR    | GAN-GP  | iGAN-GR |
| 1     | 0.0321  | 0.0941  | 0.0419  | 0.1830  | 0.0497  | 0.0802  | 0.0293  | 0.0262  | 0.1699  | 0.0395  | 0.0267  | 0.1315  | 0.0262  | -0.0105 | 0.0817  |
| 2     | 0.0276  | 0.0820  | 0.0273  | 0.0219  | 0.1217  | 0.0640  | 0.1307  | 0.0161  | -0.1345 | 0.0376  | 0.0275  | 0.0378  | 0.1344  | 0.0625  | 0.0743  |
| 3     | 0.0227  | -0.0238 | -0.0787 | -0.0559 | 0.0071  | 0.0435  | -0.0347 | 0.0820  | 0.0361  | 0.0546  | 0.0678  | -0.0449 | -0.0373 | 0.0889  | 0.0469  |
| 4     | 0.0174  | -0.0581 | -0.0417 | 0.0741  | 0.0776  | 0.0260  | 0.0279  | 0.0179  | 0.0267  | 0.0213  | 0.0121  | 0.0269  | 0.0240  | -0.0549 | 0.0428  |
| 5     | 0.0178  | -0.0330 | 0.2000  | 0.0286  | 0.0036  | 0.0200  | -0.1494 | 0.0242  | 0.1813  | 0.0820  | 0.0184  | -0.0387 | -0.0245 | -0.0983 | 0.0017  |
| 6     | 0.0120  | -0.0372 | -0.0313 | -0.4588 | 0.0166  | 0.0068  | -0.0350 | -0.1429 | -0.2081 | 0.1521  | 0.0125  | -0.1543 | -0.0060 | -0.1053 | 0.0268  |
| 7     | 0.0244  | -0.1026 | 0.0545  | 0.2137  | 0.0613  | 0.0000  | -0.0870 | 0.0380  | 0.1167  | 0.0845  | -0.0190 | -0.0783 | 0.1071  | 0.0429  | 0.0529  |
| 8     | -0.0125 | -0.1628 | -0.0577 | -0.2103 | 0.1132  | -0.0137 | -0.1556 | -0.0395 | -0.0377 | 0.0430  | -0.0124 | -0.1239 | -0.0533 | -0.2338 | 0.0295  |
| 9     | -0.0123 | -0.0600 | 0.0061  | -0.0297 | 0.0581  | -0.0270 | -0.0962 | 0.0543  | 0.0000  | 0.0858  | -0.0245 | -0.0331 | -0.0949 | 0.1573  | 0.1848  |

Figure 6: Performance gain γ t of different models after querying samples via active learning.

<!-- image -->

Line chart

Moreover, we also examine the performance gain provided by the newly-added training samples recommended by using active learning methods. As shown in Fig. 6 and Tab. 4, after each time of sample querying, the iGAN-GR has a stable and positive performance gain, and in contrast, the performance gains of other models are not always positive and have many fluctuations as the number of times of querying samples increases. This experiment phenomenon also verify the effectiveness of the proposed iGAN-GR.

Because of the complicated network structure, the time cost of training iGAN-GR (and GAN-GP) is higher than the other models, and especially, the QBC active learning methods have a extremely high time cost because there are nine committee members to be trained at each time of querying samples ( cf. Tab. 5). However, the testing time cost of iGAN-GR keeps at a reasonable level, and in contrast, SVR is time-consuming in the testing phase because each testing output is computed by traversing all support vectors ( i.e., training samples).

To sum up, the experiment demonstrates the proposed iGAN-GR with the specific training strategy, which contains two stages: initial training and incremental training, can successfully the task of geological reconstruction, and has a significant superiority to the other models. The EUS and the QBC active learning methods both perform well, but the former has a better feasibility in practice because of its much lower time cost.

Table 5: Time cost of different models with active learning methods

|     | AL                                                 | RS                          | RS                                          | RS                           | RS                                     | EUS                                    | EUS                                                      | EUS                                               | EUS                             | EUS                    | QBC                                   | QBC                                   | QBC                             | QBC                                      | QBC                                       |
|-----|----------------------------------------------------|-----------------------------|---------------------------------------------|------------------------------|----------------------------------------|----------------------------------------|----------------------------------------------------------|---------------------------------------------------|---------------------------------|------------------------|---------------------------------------|---------------------------------------|---------------------------------|------------------------------------------|-------------------------------------------|
| T   | Phase Model                                        | SVR                         | RFR                                         | XGBR                         | GAN-GP                                 | iGAN-GR                                | SVR                                                      | RFR                                               | XGBR                            | GAN-GP                 | iGAN-GR                               | SVR RFR                               | XGBR                            | GAN-GP                                   | iGAN-GR                                   |
| 0   | training (s) testing (s) querying (s)              | 4.0845 1.3948 0.0002        | 68.0003 0.007 0.0000                        | 18.0856 0.0862 0.0002        | 230.0081 0.0018 0.0044                 | 184.8574 0.0014 0.0058                 | 4.1455 1.3791 1.8463                                     | 68.1935 18.1435 0.007 0.0884 0.0708 0.8046        | 211.5 0.0018 0.3183             | 333.943 0.003 0.3912   | 4.026 1.3681 42.0542                  | 71.8587 0.0068 57.6359                | 18.1315 0.0902 156.9674         | 210.0999 0.0018 2741.5014                | 185.9665 0.0016 2409.3793                 |
| 1   | training (s) testing (s) querying (s)              | 3.1443 1.2837 0.0002        | 60.1839 16.2455 0.0066 0.0878 0.0002 0.0002 |                              | 171.6557 0.0024 0.005                  | 154.6756 0.0016 0.0056                 | 2.5316 63.1164 1.2577 1.6298                             | 15.6661 0.0074 0.0906 0.0792 0.7797               | 173.3605 0.0018 0.311           | 274.8515 0.0036 0.3726 | 3.2691 1.3055 36.98                   | 61.9104 0.0066 43.3032                | 15.8286 0.0908 133.2579         | 175.2347 0.0014 2006.1148                | 152.5634 0.0018 2002.8516                 |
| 2 3 | training (s) testing (s) querying (s) training (s) | 2.1391 1.1985 0.0000 1.6088 | 49.7725 0.009 0.0004 42.2052                | 13.8729 0.088 0.0006 11.4274 | 151.3236 0.0032 0.0048 126.4904 0.0032 | 129.1286 0.0014 0.0048 107.6348 0.0014 | 2.2568 1.1936 1.4613 0.0662 1.4284 38.6755 1.0982 0.0068 | 49.2805 13.3573 0.0067 0.0876 0.7476 11.6239 0.09 | 152.8024 0.0014 0.2926 124.1489 | 0.3187 102.3696 0.0014 | 180.1242 0.0026 1.2106 30.6326 2.0797 | 2.8913 46.8407 0.0072 37.5006 38.4342 | 13.4121 0.0898 114.5639 11.3756 | 152.918 0.0012 1738.0138 134.5831 0.0016 | 128.8395 0.0012 1676.7065 118.9602 0.0018 |
| 4   | testing (s) querying (s)                           | 1.0666 0.0002 1.1754        | 0.007 0.0886 0.0001 0.0068                  | 0.0004 9.7389 0.0874         | 0.0036 93.846 0.003 0.0034             | 0.005 0.0014                           | 1.2477 0.063 1.0738 1.0118                               | 0.7125                                            | 0.0014 0.2886 99.4397           | 0.2868 85.08 0.0018    | 24.9794 1.3197 1.0126                 | 1.136 0.0071 29.611 31.8418           | 0.0894 96.9935 9.8546 0.09      | 1462.4156 106.5846 0.0023                | 1539.5195 89.3011 0.0018                  |
|     | training (s) testing (s) querying (s)              | 0.9818 0.0004               | 35.0135 0.0004                              | 0.0002 8.8772                | 75.875                                 | 90.2674 0.0044                         | 31.3401 0.0066 1.0836 0.0619                             | 9.726 0.0908 0.6854                               | 0.0018 0.2759                   | 0.2715                 | 18.469 0.8364                         | 0.0066 23.3716 26.4632                | 83.6602                         | 1227.1505                                | 1164.9315 69.5592                         |
| 5   | training (s) testing (s) querying (s)              | 0.8108 0.8917 0.0002        | 28.3352 0.0068 0.0004                       | 0.0906 0.0000                | 0.0032 0.0036                          | 76.5524 0.0014 0.0044                  | 0.7674 0.9215 0.9537                                     | 29.2835 8.6159 0.007 0.0886 0.0642 0.6467         | 76.4178 0.0016 0.2559           | 71.0697 0.0016 0.2603  | 0.9217 14.8358                        | 0.0072 18.2467                        | 8.9291 0.0888 71.4518           | 79.399 0.0014                            | 0.0016 924.0885                           |
| 6   | training (s) testing (s)                           | 0.6781 0.8391               | 24.0696 0.0068 0.0002                       | 7.5957 0.089 0.0002          | 65.0571 0.0036                         | 65.876 0.0017                          | 22.1098                                                  | 7.2326 0.007 0.0896                               | 69.3814 0.0016                  | 60.5286 0.0016         | 0.6177 0.8418                         | 23.163 0.0068                         | 7.0491 0.088                    | 918.4933 65.6143 0.0014                  | 58.3781                                   |
|     | querying (s)                                       | 0.0004                      | 20.5262                                     | 6.3739 0.0868                | 0.0038 55.3658                         | 0.0042 56.487                          | 0.648 0.8823 0.8741                                      | 0.0581 0.6213 19.6195                             | 0.2475 49.2135                  | 0.2426 51.2222         | 12.3204                               | 15.1267                               | 61.3728                         | 756.9021                                 | 0.0016 765.4794                           |
| 7   | training (s) testing (s) querying (s)              | 0.4915 0.7606 0.0004        | 0.0074 0.0004 0.0004                        |                              | 0.0026 0.0024                          | 0.0012 0.0034                          | 0.4639 0.8021 0.7552                                     | 6.1047 0.0072 0.089 0.0553 0.5894                 | 0.0016 0.2368 43.5528           | 0.0014 0.2348          | 0.4211 0.758 9.8574                   | 18.3329 0.0064 12.3273                | 6.1745 0.0896 52.4706           | 47.3037 0.002 639.6258                   | 49.1769 0.0014 645.2317                   |
| 8   | training (s) testing (s) querying (s)              | 0.3734 0.6923 0.0002        | 17.4084 5.3307 0.0062 0.0886                | 47.7936 0.0028               | 0.003                                  | 48.345 0.0014 0.0032                   | 0.3643 0.7529 0.6634                                     | 18.4755 5.2789 0.007 0.086 0.5623                 | 0.0014 0.2188                   | 44.9365 0.0012 0.2254  | 0.3571 0.7037                         | 15.4815 0.0066                        | 5.3826 0.0894                   | 41.5932 0.0014                           | 40.8628 0.0018 555.6884                   |
|     | training (s) testing (s)                           | 0.2895 0.6241               | 0.0000 0.0008 4.6685                        | 39.2488                      |                                        | 42.5663                                |                                                          | 0.0534                                            |                                 | 39.0722                | 0.271                                 | 8.3672 10.2366                        | 46.2685 4.474                   | 541.9268 37.6931                         | 36.3782                                   |
| 9   |                                                    |                             |                                             |                              |                                        |                                        |                                                          | 4.4172                                            | 38.3525                         |                        |                                       | 13.9656                               |                                 |                                          |                                           |
|     |                                                    |                             |                                             | 0.0032                       |                                        |                                        | 0.2793                                                   | 0.0904                                            |                                 |                        |                                       |                                       |                                 |                                          |                                           |
|     |                                                    |                             | 0.0888                                      |                              |                                        |                                        | 16.5178 0.0074                                           |                                                   | 0.0014                          |                        | 0.6276                                |                                       |                                 |                                          |                                           |
|     |                                                    |                             |                                             |                              |                                        | 0.0018                                 | 0.6455                                                   |                                                   |                                 | 0.0014                 |                                       | 0.0068                                | 0.089                           |                                          |                                           |
|     |                                                    |                             | 16.0201 0.0064 0.0002                       |                              |                                        |                                        |                                                          |                                                   |                                 |                        |                                       |                                       |                                 | 0.0018                                   | 0.0014                                    |
|     | querying (s)                                       |                             |                                             |                              |                                        |                                        |                                                          |                                                   |                                 |                        |                                       |                                       |                                 |                                          |                                           |
|     |                                                    | 0.0000                      | 0.0002                                      | 0.0022                       |                                        | 0.003                                  | 0.5421 0.0534                                            | 0.5304                                            | 0.215                           | 0.2076                 | 7.1891                                | 8.3745                                | 40.658                          | 445.6629                                 | 460.7213                                  |

## 5. Conclusion

In this paper, we propose a framework, called AL-iGAN for TBM tunnel geological reconstruction. This framework contains three aspects: 1) the active learning method for selecting the most informative fresh samples to improve the current model; 2) the iGAN-GR model to estimate the thickness of each kind of rock-soil type at a location of the tunnel based on TBM operational data indexed by continuous displacement; and 3) the training strategy designed for incremental learning.

We adopt the EUS and the QBC active learning methods to select a candidate operational datum from the data pool, and then retrieve the location corresponding to the selected datum. Then, the geological information is obtained by taking a drilling at this location, and then the operational data within 0.3m around the location are labeled with the thickness of the observed rock-soil types to form the newly-added training samples. The numerical experiments show that the two kinds of active learning methods perform comparably, but the time cost of the QBC method is much higher than that of the EUS method. Therefore, the EUC method could be an appropriate choice in practice. It is noteworthy that being not limited to the drilling methods, there have been other ways to detect the geological information at one individual location, for example, seismic ahead prospecting methods [37, 38], electromagnetic ahead prospecting methods [39, 8] and electrical and induced polarization ahead prospecting methods[40, 41].

The structure of iGAN-GR is specifically designed for the incremental learning of the TBM tunnel geological reconstruction based on TBM operational data. In view of the strong sequentiality of these data, we combine the MSA module with the PE module to form the feature-extraction part in the generator of iGAN-GR. We also impose two output nodes D r / g [ · ] and D o / f [ · ] in the discriminator of iGAN-GR: D r / g [ · ] is to identify whether the input instance is a real training sample or the output of generator; and D r / g [ · ] is to justify whether the input instance is one of the original or the newly-added training samples.

The training of iGAN-GR is achieved via two stages: initial training and incremental training. First, we use the original training samples to update the weights of an iGAN-GR ( cf. Alg. 1); and then we use the new training samples, a part of which are the newly-added training samples, to refine the weights of the iGAN-GR for fitting the fresh samples ( cf. Alg. 2). The usage of D r / g [ · ] avoids the previously-trained iGAN-GR to forget the previous memory in the incremental training stage.

The collaboration of the three aspects results in the proposed AL-iGAN framework ( cf. Alg. 3). The experimental results support the effectiveness of the AL-iGAN framework in the task of incremental geological reconstruction and show that 1) iGAN-GR outperforms the other models when only some of original training samples are available; and 2) taking advantages of specific structure and training strategy, iGAN-GR has the best reconstruction accuracy with a positive performance gain after each time of querying samples in active learning. In future works, we will consider the applications of the diffusion models and reinforcement learning in the task of incremental geological reconstruction.

Table 6: Physical and Mechanical Indicators of Different rock-soil types and the number of times that each rock-soil type appears in the drilling samples

| Type       |   Indicator |   Y (kN / m 3 ) FI ( ◦ ) |   EM (MPa) |     P |   SITA |   K (m / d) |   FRB (kPa) |   Number |
|------------|-------------|--------------------------|------------|-------|--------|-------------|-------------|----------|
| 2 ○ 3      |      17.000 |                    4.500 |      4.000 | 0.400 |  0.650 |       0.003 |      10.000 |        7 |
| 4 ○ 2      |      19.000 |                   15.000 |     15.000 | 0.320 |  0.500 |       0.005 |      25.000 |        3 |
| 4 ○ 4      |      18.000 |                    8.000 |      4.500 | 0.420 |  0.700 |       0.005 |      18.000 |        2 |
| 4 ○ 10     |      20.500 |                   32.000 |     25.000 | 0.220 |  0.350 |      20.000 |      55.000 |        9 |
| 7 ○ 2 - 1  |      18.500 |                   20.500 |     18.000 | 0.300 |  0.450 |       0.500 |      22.000 |        9 |
| 7 ○ 2 - 2  |      18.500 |                   22.500 |     20.000 | 0.280 |  0.550 |       0.500 |      28.000 |       36 |
| 9 ○ 1      |      19.500 |                   25.000 |     40.000 | 0.250 |  0.000 |       0.800 |      45.000 |        9 |
| 9 ○ 2 - 1  |      20.500 |                   27.500 |     90.000 | 0.250 |  0.000 |       2.500 |      60.000 |        5 |
| 12 ○ 1     |      19.500 |                   27.000 |     40.000 | 0.250 |  0.000 |       1.000 |      45.000 |        6 |
| 12 ○ 2 - 1 |      20.500 |                   30.000 |     90.000 | 0.250 |  0.000 |       2.500 |      60.000 |        1 |
| 12 ○ 3     |      24.500 |                   55.000 |      10000 | 0.220 |  0.000 |       1.500 |     380.000 |        1 |

## 6. Acknowledgement

This work is supported by the National Key R&amp;D Program of China (No. 2018YFB1702502) and the National Natural Science Foundation of China (No. 62176040 and No. 52075068)

## References

- [1] S.-M. Liao, F.-L. Peng, S.-L. Shen, Analysis of shearing effect on tunnel induced by load transfer along longitudinal direction, Tunnelling and Underground Space Technology 23 (4) (2008) 421-430. doi:https://doi.org/10.1016/j.tust.2007.07.001 .

URL https://www.sciencedirect.com/science/article/pii/ S0886779807000788

- [2] D. Jin, D. Yuan, X. Li, H. Zheng, Analysis of the settlement of an existing tunnel induced by shield tunneling underneath, Tunnelling and Underground Space Technology 81 (2018) 209-220. doi:https://doi.org/10.1016/j.tust.2018.06.035 .

URL https://www.sciencedirect.com/science/article/pii/ S0886779817308064

- [3] S. Yagiz, H. Karahan, Application of various optimization techniques and comparison of their performances for predicting tbm penetration rate in rock mass, International Journal of Rock Mechanics and Mining Sciences 80 (2015) 308-315. doi:https://doi.org/10.1016/j.ijrmms.2015.09.019 .

URL https://www.sciencedirect.com/science/article/pii/ S1365160915300472

- [4] W.-C. Cheng, X.-D. Bai, B. B. Sheil, G. Li, F. Wang, Identifying characteristics of pipejacking parameters to assess geological conditions using optimisation algorithm-based support vector machines, Tunnelling and Underground Space Technology 106 (2020) 103592. doi:https://doi.org/10.1016/j.tust.2020.103592 .

URL https://www.sciencedirect.com/science/article/pii/ S0886779820305460

- [5] J. Chen, X. Li, H. Zhu, Y. Rubin, Geostatistical method for inferring rmr ahead of tunnel face excavation using dynamically exposed geological information, Engineering Geology 228 (2017) 214-223. doi:https://doi.org/10.1016/j.enggeo.2017.08.004 . URL https://www.sciencedirect.com/science/article/pii/ S0013795216308493
- [6] J. Park, K.-H. Lee, B.-K. Kim, H. Choi, I.-M. Lee, Predicting anomalous zone ahead of tunnel face utilizing electrical resistivity: Ii. field

tests, Tunnelling and Underground Space Technology 68 (2017) 1-10. doi:https://doi.org/10.1016/j.tust.2017.05.017 .

URL https://www.sciencedirect.com/science/article/pii/ S0886779816305041

- [7] J. Park, K.-H. Lee, J. Park, H. Choi, I.-M. Lee, Predicting anomalous zone ahead of tunnel face utilizing electrical resistivity: I. algorithm and measuring system development, Tunnelling and Underground Space Technology 60 (2016) 141-150. doi:https://doi.org/10.1016/j.tust.2016.08.007 .
2. URL https://www.sciencedirect.com/science/article/pii/ S0886779815302388
- [8] B. Liu, F. Zhang, S. Li, Y. Li, S. Xu, L. Nie, C. Zhang, Q. Zhang, Forward modelling and imaging of ground-penetrating radar in tunnel ahead geological prospecting, Geophysical Prospecting 66 (4) (2018) 784-797. doi:https://doi.org/10.1111/1365-2478.12613 .
4. URL https://www.earthdoc.org/content/journals/10.1111/ 1365-2478.12613
- [9] Z. Liu, L. Li, X. Fang, W. Qi, J. Shen, H. Zhou, Y. Zhang, Hard-rock tunnel lithology prediction with tbm construction big data using a globalattention-mechanism-based lstm network, Automation in Construction 125 (2021) 103647. doi:https://doi.org/10.1016/j.autcon.2021.103647 . URL https://www.sciencedirect.com/science/article/pii/ S0926580521000984
- [10] S.-S. Leu, T. J. W. Adi, Probabilistic prediction of tunnel geology using a hybrid neural-hmm, Engineering Applications of Artificial Intelligence 24 (4) (2011) 658-665. doi:https: //doi.org/10.1016/j.engappai.2011.02.010 .
7. URL https://www.sciencedirect.com/science/article/pii/ S0952197611000340
- [11] [Q. Zhang, Z. Liu, J. Tan, Prediction of geological conditions for a tunnel](https://www.sciencedirect.com/science/article/pii/S0926580518308628)

boring machine using big operational data, Automation in Construction 100 (2019) 73-83. doi:https://doi.org/10.1016/j.autcon.2018.12.022 .

URL https://www.sciencedirect.com/science/article/pii/ S0926580518308628

- [12] J. Zhao, M. Shi, G. Hu, X. Song, C. Zhang, D. Tao, W. Wu, A data-driven framework for tunnel geological-type prediction based on tbm operating data, IEEE Access 7 (2019) 66703-66713. doi:10.1109/ACCESS.2019.2917756 .
- [13] C. Zhang, M. Liang, X. Song, L. Liu, H. Wang, W. Li, M. Shi, Generative adversarial network for geological prediction based on tbm operational data, Mechanical Systems and Signal Processing 162 (2022) 108035. doi:https://doi.org/10.1016/j.ymssp.2021.108035 . URL https://www.sciencedirect.com/science/article/pii/ S0888327021004271
- [14] P. Ren, Y. Xiao, X. Chang, P. Huang, Z. Li, X. Chen, X. Wang, A survey of deep active learning, CoRR abs/2009.00236 (2020). arXiv:2009.00236 . URL https://arxiv.org/abs/2009.00236
- [15] Y. Gal, R. Islam, Z. Ghahramani, Deep bayesian active learning with image data, in: D. Precup, Y. W. Teh (Eds.), International Conference on Machine Learning, Vol. 70 of Proceedings of Machine Learning Research, PMLR, PMLR, 2017, pp. 1183-1192. URL https://proceedings.mlr.press/v70/gal17a.html
- [16] M. Goudjil, M. Koudil, M. Bedda, N. Ghoggali, A novel active learning method using svm for text classification, International Journal of Automation and Computing 15 (3) (2018) 290-298. URL https://doi.org/10.1007/s11633-015-0912-z
- [17] X. Lin, D. Parikh, Active learning for visual question answering: An empirical study, arXiv preprint arXiv:1711.01732 (2017). URL http://arxiv.org/abs/1711.01732

- [18] Y. Li, B. Fan, W. Zhang, W. Ding, J. Yin, Deep active learning for object detection, Information Sciences 579 (2021) 418-433. doi:https://doi.org/10.1016/j.ins.2021.08.019 .

URL https://www.sciencedirect.com/science/article/pii/ S0020025521008197

- [19] J. Kim, J. Hwang, S. Chi, J. Seo, Towards database-free visionbased monitoring on construction sites: A deep active learning approach, Automation in Construction 120 (2020) 103376. doi:https://doi.org/10.1016/j.autcon.2020.103376 .
2. URL https://www.sciencedirect.com/science/article/pii/ S0926580520309560
- [20] D. D. Lewis, W. A. Gale, A sequential algorithm for training text classifiers, in: Proceedings of the 17th Annual International ACM SIGIR Conference on Research and Development in Information Retrieval, SIGIR '94, SpringerVerlag, Berlin, Heidelberg, 1994, p. 3-12.
- [21] T. Scheffer, C. Decomain, S. Wrobel, Active hidden markov models for information extraction, in: Proceedings of the 4th International Conference on Advances in Intelligent Data Analysis, IDA '01, Springer-Verlag, Berlin, Heidelberg, 2001, p. 309-318.
- [22] C. E. Shannon, A mathematical theory of communication, SIGMOBILE Mob. Comput. Commun. Rev. 5 (1) (2001) 3-55. doi:10.1145/584091. 584093 .

URL

- [https://doi.org/10.1145/584091.584093](https://doi.org/10.1145/584091.584093)
- [23] H. S. Seung, M. Opper, H. Sompolinsky, Query by committee, in: Proceedings of the Fifth Annual Workshop on Computational Learning Theory, COLT '92, Association for Computing Machinery, New York, NY, USA, 1992, p. 287-294. doi:10.1145/130385.130417 . URL https://doi.org/10.1145/130385.130417

- [24] I. Dagan, S. P. Engelson, Committee-based sampling for training probabilistic classifiers, in: Proceedings of the Twelfth International Conference on International Conference on Machine Learning, ICML'95, Morgan Kaufmann Publishers Inc., San Francisco, CA, USA, 1995, p. 150-157.
- [25] A. McCallum, K. Nigam, Employing em and pool-based active learning for text classification, in: Proceedings of the Fifteenth International Conference on Machine Learning, ICML '98, Morgan Kaufmann Publishers Inc., San Francisco, CA, USA, 1998, p. 350-358.
- [26] A. Mallya, S. Lazebnik, Packnet: Adding multiple tasks to a single network by iterative pruning, in: Proceedings of the IEEE conference on Computer Vision and Pattern Recognition, 2018, pp. 7765-7773.
- [27] S.-A. Rebuffi, A. Kolesnikov, G. Sperl, C. H. Lampert, icarl: Incremental classifier and representation learning, in: Proceedings of the IEEE conference on Computer Vision and Pattern Recognition, 2017, pp. 2001-2010.
- [28] M. Masana, X. Liu, B. Twardowski, M. Menta, A. D. Bagdanov, J. van de Weijer, Class-incremental learning: survey and performance evaluation on image classification, arXiv preprint arXiv:2010.15277 (2020).
- [29] J. Kirkpatrick, R. Pascanu, N. Rabinowitz, J. Veness, G. Desjardins, A. A. Rusu, K. Milan, J. Quan, T. Ramalho, A. Grabska-Barwinska, et al., Overcoming catastrophic forgetting in neural networks, Proceedings of the national academy of sciences 114 (13) (2017) 3521-3526. arXiv:https:// www.pnas.org/doi/pdf/10.1073/pnas.1611835114 , doi:10.1073/pnas. 1611835114 .

[URL https://www.pnas.org/doi/abs/10.1073/pnas.1611835114](https://www.pnas.org/doi/abs/10.1073/pnas.1611835114)

- [30] Z. Li, D. Hoiem, Learning without forgetting, IEEE transactions on pattern analysis and machine intelligence 40 (12) (2017) 2935-2947. URL https://arxiv.org/abs/1606.09282v1

- [31] J. Gehring, M. Auli, D. Grangier, D. Yarats, Y. N. Dauphin, Convolutional sequence to sequence learning, in: International conference on machine learning, PMLR, 2017, pp. 1243-1252.
- [32] I. J. Goodfellow, J. Pouget-Abadie, M. Mirza, B. Xu, D. Warde-Farley, S. Ozair, A. Courville, Y. Bengio, Generative adversarial networks, arXiv preprint arXiv:1406.2661 (2014).
- [33] L. J. Ratliff, S. A. Burden, S. S. Sastry, Characterization and computation of local nash equilibria in continuous games, in: 2013 51st Annual Allerton Conference on Communication, Control, and Computing (Allerton), 2013, pp. 917-924. doi:10.1109/Allerton.2013.6736623 .
- [34] L. Liu, X. Song, C. Zhang, D. Tao, Gan-mdf: An enabling method for multi-fidelity data fusion, IEEE Internet of Things Journal (2022).
- [35] C. Zhang, L. Liu, H. Wang, X. Song, D. Tao, Scgan: stacking-based generative adversarial networks for multi-fidelity surrogate modeling, Structural and Multidisciplinary Optimization 65 (6) (2022) 1-16.
- [36] D. P. Kingma, J. Ba, Adam: A method for stochastic optimization, arXiv preprint arXiv:1412.6980 (2014).
- [37] B. Liu, L. Chen, S. Li, X. Xu, L. Liu, J. Song, M. Li, A new 3d observation system designed for a seismic ahead prospecting method in tunneling, Bulletin of Engineering Geology and the Environment 77 (4) (2018) 15471565.
- [38] B. Liu, Q. Guo, Z. Liu, C. Wang, L. Nie, X. Xu, L. Chen, Comprehensive ahead prospecting for hard rock tbm tunneling in complex limestone geology: a case study in jilin, china, Tunnelling and Underground Space Technology 93 (2019) 103045.
- [39] W. Li, J. Wang, X. Guo, H. Li, S. Li, X. Li, A new transient electromagnetic prospecting method in tbm tunnel environment, Journal of Applied Geophysics 196 (2022) 104492.

- [40] A. Belova, Y. Davydenko, D. Gurevich, A. Bashkeev, S. Bukhalov, P. Veeken, Mineral prospecting for copper-molybdene ores in northern kazakhstan using electromagnetic sensing and induced polarization technology (ems-ip), in: 82nd EAGE Annual Conference &amp; Exhibition, Vol. 2021, European Association of Geoscientists &amp; Engineers, 2021, pp. 1-5. doi:https://doi. org/10.3997/2214-4609.202010238 .
- [41] F. A. Alfouzan, A. M. Alotaibi, L. H. Cox, M. S. Zhdanov, Spectral induced polarization survey with distributed array system for mineral exploration: Case study in saudi arabia, Minerals 10 (9) (2020) 769.
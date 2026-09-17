## Defect segmentation: Mapping tunnel lining internal defects with ground penetrating radar data using a convolutional neural network

Senlin Yang c , Zhengfang Wang a , Jing Wang a, ∗ , Anthony G. Cohn d , Jiaqi Zhang a , Peng Jiang c , Lichao Nie b , Qingmei Sui a

a

School of Control Science and Engineering, Shandong University, Jinan, 250061, China. b Geotechnical and Structural Engineering Research Center, Shandong University, Jinan, 250061, China

c School of Qilu Transportation, Shandong University, Jinan, 250061, China d School of Computing, University of Leeds, Leeds, LS29JT, UK

## Abstract

This research proposes a Ground Penetrating Radar (GPR) data processing method for non-destructive detection of tunnel lining internal defects, called defect segmentation . To perform this critical step of automatic tunnel lining detection, the method uses a CNN called Segnet combined with the Lovsz softmax loss function to map the internal defect structure with GPR synthetic data, which improves the accuracy, automation and efficiency of defects detection. The novel method we present overcomes several difficulties of traditional GPR data interpretation as demonstrated by an evaluation on both synthetic and real datas - to verify the method on real data, a test model containing a known defect was designed and built and GPR data was obtained and analyzed.

Keywords: Convolutional Neural Networks (CNNs), Ground Penetrating Radar (GPR), GPR Data Intelligent Recognition, Tunnel Lining Defect

## 1. Introduction

Tunnels are an essential part of traffic and water conservancy projects and, their safe operation has always been a critical engineering issue [1] . Tunnels require maintenance service due to ageing, geological conditions, and natural weathering. During the maintenance process, a variety of defects in the tunnel lining often present themselves. This leads to tunnel instability and can affect tunnel operation safety. Common types of tunnel lining internal defects include cracks, voids, lining-rock separation, water seepage, and other structural defects, which affect the stress and erosion on the tunnel differently [2-4] . Effectively knowing the classification, location, and shape of any lining internal defects provides an essential basis for timely solutions and helps ensures the safety of the tunnel.

∗ Corresponding author

Email addresses: yangsenlin@mail.sdu.edu.cn (Senlin Yang), wangzhengfangsdu@hotmail.com (Zhengfang Wang), wangjingkz@sdu.edu.cn (Jing Wang), A.G.Cohn@leeds.ac.uk (Anthony G. Cohn), 201934530@mail.sdu.edu.cn (Jiaqi Zhang), sdujump@gmail.com (Peng Jiang), llichaonie@163.com (Lichao Nie), qmsui@sdu.edu.cn (Qingmei Sui)

Common detection methods for tunnel lining defects include direct methods for extracting centroid detection, non-destructive testing (NDT) techniques such as infrared thermography, multi-spectral analysis, ultrasonic pulses, and Ground Penetrating Radar (GPR), etc [5, 6] . Among them, GPR has become a preferred method for defect detection in tunnel linings due to its advantages of fast detection speeds, strong penetration ability, convenient use, and carrying ease [7] . Research on tunnel integrity detection using GPR can be traced back to 1994 [8] , and many researchers have studied the performance of GPR [9-11] , which has gradually formed a discipline.

For GPR, tunnel lining internal structures can be deduced, due to different relative dielectric constants, by emitting electromagnetic waves and receiving the reflected signals. These reflected signals are hyperbolic, and they are often interlaced with each other, which makes data interpretation difficult. Commonly used theoretical methods are migration imaging and inversion calculation, which can obtain the relative dielectric constant model. Researchers have conducted comprehensive work on this [12, 13] . In addition, much research exists regarding automatic identification of anomalous objects in GPR data based on the pattern recognition and machine learning methods. Pasolli et al. [14] used Genetic Algorithm and Support Vector Machine (SVM) to perform pattern recognition and classification on pre-processed GPR data and achieved relatively accurate identification. Xie et al. [15] used SVM to extract the void signal from synthetic GPR data, and collected real data through model tests to apply the method. Although 97.74% accuracy was obtained, it is difficult to use their method to accurately obtain the position and shape of the voids. Dou et al. [16] and Zhou et al. [17] respectively proposed a C3 clustering algorithm and an Optimized Stable Clustering Algorithm (OSCA) to extract complex GPR reflection signal characteristics and then fit them to GPR reflection hyperbola parameters.

With the rapid development of artificial intelligence and deep learning in recent years, deep learning algorithms based on Convolutional Neural Networks (CNNs) have provided new solutions for GPR data processing and defect recognition. In the field of image and computer vision, methods such as FCN (Fully Convolutional Network) [18] , U-net [19] , and Segnet [20] have led to better and better achievements and have gradually been applied to autopilot systems and other applications. CNNs have also been introduced in the medical field to perform defect detection and identification [19, 21, 22] . Likewise, in geophysics, there have been many studies to solve the inversion problem using CNNs and related methods [23-25] . For GPR data recognition, Nuaimy et al. [26] effectively combined GPR data processing, pattern recognition, and neural networks to complete high-resolution labelling, imaging, and classification of GPR data as early as 2000. It provided a reference for the application of neural networks in solving the GPR data interpretation problem. Xu et al. [27] used vehicle-borne GPR to detect railway subgrade defects and apply the Faster R-CNN method to identify defect signals in GPR data. Their research effectively obtained the position, classification, and probability of defects in GPR data image. In terms of GPR detection on asphalt pavements, Tong et al. [28] designed a recognition CNN, a location CNN, and a feature extraction CNN, to solve the automatic recognition, location, length measurement, and 3D reconstruction of cracks, respectively.

The research methods reviewed above mainly identified defect signals in GPR data images allowing for accurate classification and positioning. It is necessary to improve the accuracy, automation, and efficiency of GPR data interpretation for tunnel linings internal defects, and to obtain the classification and structures of linings internal.

Inspired by the progress in semantic segmentation in computer vision, we considered the possibility of mapping the tunnel lining internal structure, including the classification, location and shape of the defects, with GPR data. Therefore, this paper proposes an innovative method, using a CNN to complete GPR data processing and obtain pixel-level tunnel lining internal defects information, which we called defect segmentation. In this way, after GPR data is routinely processed and used as input, detailed information on the tunnel lining internal material structure can be obtained, which is more automated and intuitive. Through our method, the efficiency and enforceability of tunnel defect detection can be greatly improved. The main work we report on here includes effective data preparation, selection and analysis of CNNs, and application to real data. The rest of the paper is arranged as follows: In Section 2, we describe the characteristics of our proposed method, and provide designed dielectric constant models and corresponding synthetic GPR data for training of CNNs. Then we design CNNs based on the characteristics of GPR data and introduced the detailed parameters of the CNNs in Section 3. The performance of the proposed CNN is discussed, comparing different CNNs and different defects. Section 4 reports on the results obtained from analyzing synthetic data whilst Section 5 focuses on evaluating performance of the method on real data derived from a test model. Finally, in the conclusion was summarizedwe summarize the contributions of the paper.

## 2. Method description and GPR data preparation

## 2.1. Method description

The aim of this research was to use GPR equipment to collect reflection data from the internal structures of the tunnel lining and then to deduce the internal materials or defects to a complete pixel-by-pixel level defect segmentation. In general, the results of GPR detection are different due to the differing internal materials and defect shapes. For complicated internal structures, they are stacked on top of each other and have similar shapes, which makes it difficult to separate them effectively and give the correct explanation. The defect segmentation task we propose is aimed at this complex problem that may include rebars, surrounding rocks, and multiple defects. Let us denote the relative dielectric constant model inside a tunnel lining can be described as M ; the resulting GPR we denote as D ; D can be segmented to provide a classification, C , of the image data reflecting the elements of the model. Thus we can describe the problem as:

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

where, seg is the mapping from GPR data to defect segmentation, and f represents the process of collecting GPR data for the internal model of the lining, which is shown in Fig. 1.

Figure 1: Defect segmentation method. The numerical model M was designed, and the GPR data D was obtained by modelling. At the same time, according to the model M , the defect segmentation model C was obtained and used as a label for training the CNN. Our defect segmentation method trains the CNN to get the mapping relationship seg and complete the calculation of C from D .

<!-- image -->

Line chart

CNNs based on supervised learning need to train network parameters from many model-data pairs to obtain a network model and complete seg , i.e., the mapping of D to the classification model C . After that, the real data D was only needed to be used as an input to the trained CNNs; the correct defect category, location, and shape can be quickly obtained. This makes the interpretation of radar data simple, automatic and efficient. The workflow is shown in Fig.2.

For classification problems it is worth noting that because the dielectric constant of the same material is within a specific range, it is a many-to-one problem, that is, for the same C , D is not fixed, which is different from the inversion problem.

Table 1: Relative dielectric constant and conductivity properties of different media

| Media            | Relative dielectric constant   | Conductivity S/m   |
|------------------|--------------------------------|--------------------|
| Air              | 1                              | 0                  |
| Water            | 81                             | 0.0005             |
| Rebar            | 300                            | 10ˆ8               |
| Surrounding rock | 6 ∼ 8                          | 0.001              |
| Concrete         | 8 ∼ 10                         | 0.0001             |

## 2.2. Tunnel lining interior materials and defects

Because the training of CNNs relies on a large amount of data, and the structure inside the tunnel lining is difficult to obtain directly, we usually collect models and data based on numerical simulation methods. The prediction result of CNNs depends on the model used to train it, so the practical analysis and selection of tunnel lining materials and the correct design of the tunnel lining models are also the focus of our research.

Common tunnel lining interior materials and defect types include rebars, rock, voids, cracks, lining-rock separation, and water seepage. They can be summarized as five types of media, namely air, water, concrete, surrounding rock, and rebar. Their relative dielectric constants and conductivity ranges, which are modified based on [29], are shown in the Table 1. Among them, water and air are defective media, and they are contained in voids, cracks and lining-rock separations. The interior of the tunnel lining may also contain rebars and rocks, which affects the GPR data and make it more complicated. Dissimilar materials have different effects on GPR due to their different dielectric constants and electrical conductivity, which is also the basis for our defect identification.

The materials and defects in the designed model can be divided into nine types: rebar, concrete, rock, crack, water-bearing crack, void, water-bearing void, lining-rock separation, and water-bearing separation. The lining-rock separation is a defect that appears between the lining and the surrounding rock, and a void is inside the concrete. They cause different hazards, so although they are similar in shape, different types are used here [4, 30] . The crack is a small crack that arises from the uneven forces in the tunnel. It also appears in the concrete and seriously affects the tunnel lining bearing capacity [31] . The above three types are further expanded into six types of defects according to whether they contain water or not. According to these materials and defect types, they are divided into the following categories:

- No defect in tunnel lining;
- A water-free defect in tunnel lining without rebar;
- A water-bearing defect in tunnel lining without rebar;

- A water-free defect in tunnel lining with rebar;
- A water-bearing defect in tunnel lining with rebar.

Based on the categories summarized above, we designed 124,800 sets of tunnel lining relative dielectric constant models, as training models for deep learning algorithms, which covers most cases. The grid size of the model was 70 × 200, and the length and width of each grid were 0.01 m , that is, the model had an actual width of 2 . 0 m and depth of 0 . 7 m . In addition, considering the need to use a Convolutional Perfect Matching Layer (CPML) to reduce false boundary reflections, the model was expanded by ten additional meshes in speculation, and the final model size was 90 × 220.

The excitation end of the GPR emits high-frequency electromagnetic waves, in the form of pulses, and propagates in the medium. In the process of propagation, and due to the difference in electromagnetic characteristics of dissimilar materials (such as air, water), the propagation of the electromagnetic waves is affected, and reflected waves are generated. This reflected signal is then received by the GPR antenna. For the CNN training, the closer the simulated data is to the real GPR data, the stronger the applicability of the network. This paper uses the Finite Difference Time Domain (FDTD) method to calculate the GPR data of the dielectric constant model in Section 4.2. For models of size 90 × 220, a Ricker wavelet with a main frequency of 600 MHz is used, and each model uses 99 sidelines. The sampling time interval is 2.3587 × 10 - 11 , with a total sampling of 800 steps.

## 3. Convolutional Neural Networks

CNNs have become one of the most significant application methods of deep learning due to its wide use in image processing. CNNs can extract features from the input data and then perform tasks such as classification, recognition or prediction. CNNs have been proposed for semantic segmentation. They have achieved impressive results in the natural and medical images field, and they have also been gradually used in the field of geophysics. Among them, CNNs include FCN [18] , U-net [19] and Segnet [20] . In this study, we analyzed the defect segmentation method, introduced Segnet and adopted a new loss function to obtain more accurate results. Finally, hyperparameters were set to update the network parameters reasonably and effectively in the training process.

## 3.1. CNNs for defect segmentation

The method of defect segmentation is similar to the semantic segmentation often handled in CNNs, but it is also more complicated. These are the following features:

- (1) Firstly, as analyzed by Liu et al. [25] , GPR data and dielectric constant models differ in shape, value, and distribution. GPR data is a time series measured at different positions in the horizontal direction, and its size is

timesteps × width , and our target model is a spatial structure with a size of depth × width . There are differences in image processing of detection data between time series and space series. For GPR signals corresponding to different defects, their hyperbola shapes are more similar than natural images. Among them, the shapes of voids and the separations are similar, and their difference lies in their location. The location of the defect needs to be considered, and their differences and features extracted from similar and complex data. In addition, for defects and materials of the same shape, the location and polarity of the reflected signal is affected by different dielectric constants and whether they contain water or not. As shown in Fig. 3 (a) and (b), the dielectric constants of concrete in the two models are different, which leads to differences in their data, as shown in the yellow box, but the fault segmentation results are the same. Comparing Fig. 3 (b) and (c), these show how the water content of the defect affects the signal polarity. This considers not only the shape information but also the amplitude of the signal. That is, both shape and value affect the model. The CNN needs to consider both numerical information and shape characteristics. Given that our present problem is that as a classification task, we suggest that a properly selected CNN is more suitable for our defect segmentation than GPRInvNet which was focused on inversion.

- (2) Normal data and data representing defects are imbalanced in size. As shown in Fig. 3(b), the size of the rebars and cracks are small, but they have a great impact on the GPR data. This size imbalance creates a particular problem for the prediction task, that is, defect segmentation. This is especially true for cracks and rebars, as they are smaller in size and require more accurate segmentation effects. To obtain higher resolution prediction results, an effective loss function must be designed and selected.
- (3) To ensure that all possibilities are included, and to prevent overfitting, a large amount of data and effective measurements are needed for training, and the computational efficiency of the network needs to be taken into account.

Based on the above analysis, we compared Segnet and U-net. It proved that Segnet has the advantages of a simple network structure, fewer parameters, and superior quality results. In addition, Segnet uses max location in upsampling to provide effective information during decoding, which improves the provision of structural information and improved high-frequency data correspondence.

## 3.2. Segnet

The overall structure and idea of Segnet is to use high-dimensional compression data, through convolution and pooling, to obtain high-dimensional features of an image and then up-sampling to complete the regression and segmentation of the image. In the network, the size of the convolution kernel is 3 × 3. To prevent gradient anomalies, Batch Normalization( BN ) is employed and a Rectified Linear Unit ( ReLU ) is used as the activation function in other layers, with the exception of the last layer. For a semantic segmentation problem, the activation function of the last layer is softmax to obtain the probability under each classification to complete the pixel-level segmentation. The innovation of Segnet is that in the decoder process, the low-resolution feature maps are converted to a high-resolution feature map using the upsampling method. This is different from deconvolution in FCN and U-net. Specifically, in the encoder part, features are compressed by pooling, and the index of each pooling is saved, that is, the original maximum position is saved. Then the corresponding pooling index is used in the decoder for non-linear upsampling. In this way, sparse upsampling feature maps can be obtained without learning the weights used in the deconvolution. Badrinarayanan et al. [20] compared Segnet with common CNNs and proved that Segnet is superior to other methods in classification. Since Segnet is used for image semantic segmentation with fewer parameters and better results, our main purpose was to study the defect segmentation of GPR data by Segnet. Its specific structure is as shown in Fig. 4. Segnet has few parameters and, in addition, it maintains high-frequency information integrity and has the advantage of achieving improved results compared to competing methods. In Section 4.2, a comparison between Segnet and U-net proves that Segnet is more suitable for the problem of defect segmentation.

## 3.3. Loss function

In the task of semantic segmentation, the most commonly used loss function is the cross entropy loss function. The activation function of the classification problem is softmax, and the use of the L2 norm loss would seriously affect gradient calculations and network updates. The cross entropy loss function can alleviate the problem of gradient disappearance by the logarithm. The cross entropy loss function is as follows:

<!-- formula-not-decoded -->

where i is the corresponding position of each pixel, and y ∗ i is the predicted probability of the corresponding position and label.

However, although the effect of the cross entropy loss function has been proven in semantic segmentation, the results of the prediction need to be improved. This improvement is especially necessary for smaller objects, because CNNs using the cross entropy loss function often have difficulty predicting them, making it difficult to achieve the requirements for rebars and cracks prediction in our method. Although rebars and cracks are obviously reflected in the input data, the rebars and cracks are usually very small and require high-resolution processing to be effectively classified in the segmentation. To solve this problem, we applied the Lovsz softmax loss function in our CNN. The Lovsz softmax loss function was proposed by Berman in 2018 [32] to optimize Mean Intersection over Union (MIoU), and its superiority on small objects is proven.

<!-- formula-not-decoded -->

where ∆ Jc is the Lovsz extension to ∆ Jc , approximation to the Jaccard index of class c , N is the number of material and defect classes, which is nine in this paper, and m ( c ) is a vector of pixel errors for class c .

Eerapu et al. [33] combined the cross entropy and the Lovsz softmax loss function to achieve better MIoU. In our work, we also use the composite loss function:

<!-- formula-not-decoded -->

The results in Section 4.2 show that the addition of the Lovsz softmax loss improved the quality of the results, especially for cracks.

## 3.4. Network hyperparameters

Suitable network hyperparameters was beneficial to the training results of the network. PyTorch implemented both CNNs and Adam optimizers in this study. The batch size of the Adam optimizer was set to 24, and the initial learning rate was 5 × 10 - 5 . The network was trained for a total of 100 epochs to obtain sufficient parameter updates.

Considering the similarity of GPR data of different materials and defects, it is easy to overfit the network which seriously affects the generalization ability of the network and even causes unreasonable network parameters. Therefore, effectively avoiding the overfitting problem is an important task. For this, we applied both dropout and weight decay. Dropout was proposed by Hinton [34] in 2012 and is proven to effectively reduce overfitting to a specific feature by randomly discarding a few per centage points of the features. The weight decay [35] is used to add a L 2 regularization after the loss function, thereby reducing the complexity of the network coefficients, and improving the effectiveness of data fitting. In this paper, by comparison, the dropout probability was set to 20 % and the weight decay coefficient was 1 × 10 - 4 , which can effectively alleviate the overfitting of the CNN.

## 4. Results and discussion

To effectively train the network, we divided the data set in Section 2.2 into the training, validation, and test set with a ratio of 10:1:1, which were used to train CNNs, verify the ability of the CNNs to save the optimal network parameters, and test the impact of the final network, respectively. Considering the different sizes of input data and output data, we used bicubic interpolation to reshape the input data of 800 × 99 into 256 × 128, and the output of Segnet was 128 × 256 and sized to 90 × 220. We trained three CNN-based networks: Segnet using the cross-entry loss function, Segnet using the cross-entry and the Lovsz maxsoft loss functions, and U-net using the cross-entry and the Lovsz maxsoft loss functions, to compare their effects in the defect segmentation task. To facilitate reference to these three methods, they are named Segnet (1 loss), Segnet(2 loss), and U-net(2 loss), respectively. The loss function curve in the training and validation set is shown in Fig. 5. It can be seen that the result of Segnet(2 loss) is far superior to the comparative methods. As shown in Fig. 5(d), U-net(2 loss) has an overfitting on the validation set, while Segnet(2 loss) does not. In order to quantitatively evaluate the performance of the results of different CNNs and the results of dissimilar materials, a series of indicators were used, such as MPA, MIoU, Precision, and Recall.

## 4.1. Metrics

For a large amount of test set data, it is inconvenient to show each result. Effective evaluation parameters should be used for the statistics of all results, so that the results of different methods and the impact of dissimilar materials can be analyzed. Firstly, for pixel-level classification problems, we used the evaluation metrics commonly employed in semantic segmentation. Mean Pixel Accuracy (MPA), Mean Intersection over Union (MIoU), Frequency Weighted Intersection over Union (FWIoU) were used to evaluate the prediction effect of each model. Secondly, to analyze the effect of our method on each type of material, we also used the Precision, Recall and F-Measure to compare the effects under different types. Moreover, the four types of results with defects were analyzed and the prediction effect of our method in different environments is discussed below.

For MPA, the proportion of correctly classified pixels in each classification was calculated separately, and the average value of all categories was calculated to verify the correctness of the classification. MIoU is the most commonly used standard in classification and semantic segmentation. It calculates the ratio of the intersection and union of the true and predicted values for each category and calculates the average. FWIoU is an improvement on MIoU, which sets weights for each class based on how often it appears. Considering that these three evaluation metrics are very commonly used in semantic segmentation [36] , we used them to evaluate the similarity of each prediction result and ground truth. Precision and recall are, respectively, the correct probability of classifying pixels, and for the probability of correct classification of ground truth, while F-measure is a hybrid metric which is the harmonic mean of precision and recall [37] . They are used to evaluate the results of each type of material and defect prediction.

## 4.2. Comparison of results with U-net and different loss functions

The comparison above of the loss functions has shown the effectiveness of Segnet(2 loss) in tunnel lining defect segmentation. Similarly, we also compares the performance of the three methods on the test set in Table 2, which also demonstrates the performance of Segnet(2 loss). Specifically, we selected four typical model-data pairs, as shown in Fig. 6. In conjunction with Table 3, the effects of each material and defect under each method were analyzed.

Firstly, Segnet(1 loss) achieved acceptable results and had very accurate predictions for rebars, voids, and separations. However, it performed poorly for cracks and had the lowest precision. The recognition of cracks requires high resolution, which is more difficult for segmentation problems. As shown in Fig.6 (b) and (d), it can be seen that this method had a lower prediction accuracy for thinner defects such as cracks. The cross-entropy loss function focuses on the probability of each pixel but is limited to the overall effect, which results in a lower resolution of the result, making it difficult to identify small defects.

|         | Table 2: Results of different methods   | Table 2: Results of different methods   | Table 2: Results of different methods   |
|---------|-----------------------------------------|-----------------------------------------|-----------------------------------------|
| Metrics | Segnet(1 loss)                          | Segnet(2 loss)                          | U-net(2 loss)                           |
| MPA     | 0.91                                    | 0.93                                    | 0.79                                    |
| MIoU    | 0.83                                    | 0.90                                    | 0.75                                    |
| FWIoU   | 0.99                                    | 0.98                                    | 0.96                                    |

Table 3: Results of different methods and different categories

| Metrics   | Methods                  | Linging Matrials   | Linging Matrials   | Linging Matrials   | Defects   | Defects   | Defects    | Water-bearing Defects   | Water-bearing Defects   | Water-bearing Defects   |
|-----------|--------------------------|--------------------|--------------------|--------------------|-----------|-----------|------------|-------------------------|-------------------------|-------------------------|
| Metrics   | Methods                  | Rebar              | Concrete           | Rock               | Crack     | Void      | Separation | Crack                   | Void                    | Separation              |
|           | Segnet(2 loss)           | 0.9664             | 0.9968             | 0.9765             | 0.8157    | 0.9008    | 0.9111     | 0.8833                  | 0.8278                  | 0.8798                  |
|           | Precision Segnet(1 loss) | 0.9312             | 0.9961             | 0.9698             | 0.3108    | 0.8674    | 0.9019     | 0.8754                  | 0.8441                  | 0.8754                  |
|           | U-net(2 loss)            | 0.9543             | 0.9875             | 0.9242             | 0.6324    | 0.8109    | 0.2918     | 0.2619                  | 0.7807                  | 0.2619                  |
|           | Segnet(2 loss)           | 0.9541             | 0.9969             | 0.9777             | 0.8039    | 0.8869    | 0.8960     | 0.8740                  | 0.8303                  | 0.8715                  |
|           | Recall Segnet(1 loss)    | 0.9201             | 0.9928             | 0.9747             | 0.7889    | 0.8635    | 0.8923     | 0.8703                  | 0.8379                  | 0.8703                  |
|           | U-net(2 loss)            | 0.9449             | 0.9861             | 0.9121             | 0.6495    | 0.8001    | 0.193      | 0.1729                  | 0.7629                  | 0.1729                  |
|           | Segnet(2 loss)           | 0.9602             | 0.9968             | 0.9771             | 0.8098    | 0.8938    | 0.9035     | 0.8786                  | 0.8290                  | 0.8756                  |
| F-measure | Segnet(1 loss)           | 0.9256             | 0.9945             | 0.9723             | 0.4459    | 0.8654    | 0.8971     | 0.8728                  | 0.841                   | 0.8728                  |
| F-measure | U-net(2 loss)            | 0.9495             | 0.9868             | 0.9181             | 0.6408    | 0.8054    | 0.2324     | 0.2083                  | 0.7717                  | 0.2083                  |

Secondly, Segnet(2 loss) performed optimally in all materials and defects. It accurately predicted the location and classification of cracks, voids, and separations, and was good for complex data. Good results are obtained for smaller defects, such as cracks and rebars. In general, most of the prediction results are accurate. The presence of reinforcing bars may cause some results to be incorrect, but the probability of errors is very low. This result proves the effectiveness of the Lovsz Softmax loss and our method.

In addition, the effect of U-net(2 loss) was poorer than that of Segnet(1 loss). When multiple defects occurred at different depths in the same location, GPR data was more complicated. The U-net(2 loss) made it difficult to effectively classify the defects, especially separations and cracks with water, as shown in Fig.6. The lack of accurate defect prediction would seriously affect the judgment of the integrity of the tunnel lining. Through analysis, we believe that it is the network structure of U-net that has led to poor results. The characteristic of U-net is that it saves the features of the encoded segments and uses them as feature maps when decoding, which is effective for the task of one-to-one correspondence in image semantic segmentation. However, for our method, GPR data and defect segmentation were not completely corresponding, which caused U-net to introduce incorrect information and obtain poor results.

## 4.3. Results in dissimilar materials

Through the above analysis, we demonstrated the effectiveness of Segnet and the Lovsz softmax loss on defect segmentation and explained the unsuitability of U-net. Segnet also has different performance effects for different types of materials and defects. We divided the defect models into four categories and analyzed them in turn.

Table 4: Results of defection detection without rebars in different types of models

| Class         | Defects   |   Crack |   Void |   Separation |   Crack&Void |   Crack&Separation |   Void&Separation |
|---------------|-----------|---------|--------|--------------|--------------|--------------------|-------------------|
| Water-free    | MPA       |    0.96 |   0.98 |         0.97 |         0.91 |               0.95 |              0.95 |
| Water-free    | MIoU      |    0.93 |   0.96 |         0.95 |         0.86 |               0.91 |              0.92 |
| Water-free    | FWIoU     |    0.99 |   0.99 |         0.99 |         0.99 |               0.99 |              0.99 |
| Water-bearing | MPA       |    0.96 |   0.97 |         0.97 |         0.90 |               0.93 |              0.94 |
| Water-bearing | MIoU      |    0.93 |   0.96 |         0.95 |         0.84 |               0.88 |              0.91 |
| Water-bearing | FWIoU     |    0.99 |   0.99 |         0.99 |         0.98 |               0.98 |              0.99 |

Table 5: Results of defection detection without rebars in different types of model

| Class         | Defects   |   Crack |   Void |   Separation |   Crack&Void |   Crack&Separation |   Void&Separation |
|---------------|-----------|---------|--------|--------------|--------------|--------------------|-------------------|
| Water-free    | MPA       |    0.91 |   0.95 |         0.96 |         0.84 |               0.89 |              0.91 |
| Water-free    | MIoU      |    0.86 |   0.91 |         0.94 |         0.78 |               0.84 |              0.87 |
| Water-free    | FWIoU     |    0.99 |   0.98 |         0.99 |         0.98 |               0.98 |              0.98 |
| Water-bearing | MPA       |    0.91 |   0.94 |         0.96 |         0.83 |               0.89 |              0.90 |
|               | MIoU      |    0.86 |   0.90 |         0.94 |         0.76 |               0.83 |              0.85 |
|               | FWIoU     |    0.98 |   0.98 |         0.99 |         0.97 |               0.97 |              0.98 |

- (1) Water-free defects in the tunnel lining without rebars For defects in the tunnel lining without rebars, because the model is simple, our method obtained accurate classification, location and morphology in various defects, as shown in Fig. 7 and Table 4. Correct predictions at the pixel level are achieved on all models.
- (2) Water-bearing defects in the tunnel lining without rebars Similarly, the water-bearing defect was relatively simple, so the overall effect was satisfactory. It can be seen in Table 4 that crac detection performed less well than other defects especially the model of cracks and voids, which shows that water-bearing defects had an impact on the results. As shown in Fig. 8 (c), especially when the void and crack are in the same horizontal position, the upper defect affects the data below, making it difficult to obtain an accurate shape, but the classification of the defects was accurate.
- (3) Defect in the tunnel lining with rebars The most challenging aspect of this method was that the rebars in the lining would seriously affect the internal defect signals acquisition. Arow of rebars with a small diameter are reflected in GPR data as multiple parallel hyperbolae. They intersect each other, shielding the effective information below. In our results, the effect of rebars on the defect, especially cracks, was severe. As shown in Table 5, the models of cracks and voids under rebars, whether they contain water or not, have a MIoU value below 0.8, which was very rare in our results otherwise. As shown in Fig. 9(c), the length of the crack was also incorrectly predicted, and the interface of the rock was also inaccurate in Fig. 9 (d). For our judgment of defects, correct classification and accurate positioning can meet most of our requirements, so the above problems have little impact on us.

In general, our Segnet with two loss functions achieved excellent defect segmentation results, which was far better than Segnet with one loss function and U-net with two loss functions. In linings containing cracks and rebars, accurate classification and positioning could obtained, which also reflects the high accuracy of our method. Although there were some problems for defect detection under rebars, in most models the correct classification could still be obtained, which provides an effective reference for post-processing. Due to the complexity of the data, some errors are inevitable we believe.

## 5. Experiment on model testing

As a result of our network design and training, we obtained a CNN model which achieved excellent results on synthetic test data. Real data is more complicated than synthetic data, and noise and other disturbances seriously affect the quality of the collected data. In geophysics, because the detection area is usually unknown, many studies use physical model tests to verify the viability and applicability of theoretical methods [15, 38, 39] . To obtain GPR data from a known internal structure and verify the effect in a real environment, we built a test model to simulate the internal defects of a real tunnel lining. Real GPR data was collected, analyzed, and processed. At the same time, the CNN was fine-tuned to fit the real data. Finally, we used the CNN to segment the defects inside the tunnel lining with real data.

## 5.1. Model test building

We designed a model test using a concrete testbed with a size of 4 . 4 m × 2 m × 0 . 7 m to simulate the internal structure of a tunnel lining, as shown in Fig. 10. In the model, we used the materials employed in the lining of an actual tunnel. To simulate a water-bearing void, we used a PVC pipe with a length of 400 mm and a diameter of 120 mm to construct the separation. PVC pipes were filled with water, sealed at both ends and placed in the concrete to simulate a waterbearing void in the lining. As a result of this construction method, we knew the exact materials used and their shape within the model. On the model, we set two sidelines with a distance of 0 . 5 m and a length of 4 . 4 m to obtain reflection information of the embedded defects below the model, of which there is no defect below the X2 sideline. Through the X2 sideline, we could get enough background data under the current model for further experimental analysis and processing. The real GPR data was collected by Impulse Radar 600MHz equipment, with 512 sampling point. The mode of the GPR was set to 'Wheel', and the distance of the traces was chosen as 0.02 m . The GPR data was collected and transmitted to the computer via Wi-Fi, and the data was initially processed.

## 5.2. Data processing

For the actual measured data, referring to previous research [25] , we preprocessed the real GPR data, including static correction, and removed the direct component, background signal, and bandpass filtering. In this way, more effective GPR data could be acquired, which improved the effectiveness of our method. To be more suitable for the real data, we used actual data from measurements of the plain concrete without defects, and randomly added it to the synthetic data as background noise. Because the size of the measured data and the synthesized data were different, we adjusted the measured data by the bicubic difference method and obtained hundreds of sets of background noise.

These actual noise data sets were normalized, fixed to a reasonable range, and randomly added to the synthesized data. The updated synthetic data was used to train and fine-tune the CNN parameters for 40 epochs. In this way, the non-uniformity of the actual medium and the interference noise collected were considered, and the applicability of the CNN was further improved. This also provided a useful reference for real data processing under different operating conditions and environments in the CNNs method.

## 5.3. Result on Real Data

We tested the retrained CNN with the real data on the X1 sidelines. After finishing the retrained CNN and data processing, the internal structure information can be directly obtained, which improves the automation and efficiency of GPR data interpretation. For water-bearing voids, as shown in Fig. 11(a), our method correctly predicted the classification and location of the defect, but the shape of the defect was poorly predicted. In the case of a single defect, our method achieves excellent results, which proves the feasibility of our method. The potential of our method for real data was demonstrated through model building and effective data processing. It was useful to fine-tune the network based on the addition of real background and synthetic data, which may be necessary for the process of applying the CNNs method to real data.

## 6. Conclusion

In this paper, we applied a CNN to create a new method called defect segmentation to resolve the problem of GPR data interpretation and tunnel lining defects detection. The conclusions of this study are as follows:

- (1) There are many differences between the defect segmentation of GPR data and semantic segmentation of natural images, including the dissimilarity of the signals, the morphological differences between the input and output, and the effect of the values on the results, which makes it difficult to apply CNNs to the task of GPR defect segmentation directly.
- (2) The characteristics of Segnet make it more suitable for our method than U-net and we have shown that it achieved more accurate results. Almost all models in a synthetic dataset were correctly classified, and an MPA of 93% and MIoU of 90% have been achieved with the cross entry and Lovsz softmax loss function.
- (3) Due to the effect of the method greatly improving the segmentation accuracy, the Lovsz softmax loss function is worth recommending, especially for crack detection. Segnet combining the cross entropy and the Lovsz softmax loss function improved 7% the MIoU as compared with Segnet, which only uses cross entropy.
- (4) For the CNN method, the complexity of the data also directly led to the accuracy of the prediction results. Both water-bearing defects and rebars had an impact on the segmentation problem. In particular, the presence of rebars and the response of the GPR signal to these, seriously affected the signals of underlying defects and this caused prediction difficulties.

- (5) When applying our proposed CNN to real data, we suggest that the appropriate methodology is to collect background signals of the corresponding environment, combine existing synthetic data sets, and fine-tune the network to achieve better results.

## Acknowledgments

The research was supported by the National Key R &amp; D Program of China (No. 2018YFC0406904), Joint Program of the National Natural Science Foundation of China (No. U1806226), The key project of National Natural Science Foundation of China (No. 51739007), and Shandong Provincial Natural Science Foundation (No.ZR2018MEE052).

## References

- [1] J. Richards, Inspection, maintenance and repair of tunnels: international lessons and practice, Tunnelling and Underground Space Technology 13 (4) (1998) 369-375.
- [2] I. W. group on maintenance, repair of underground structures, Report on the damaging effects of water on tunnels during their working life, Tunnelling and underground space technology 6 (1) (1991) 11-76.
- [3] D. Kolymbas, P. Wagner, Groundwater ingress to tunnels The exact analytical solution, Tunnelling and Underground Space Technology 22 (1) (2007) 23-27.
- [4] M. A. Meguid, H. Dang, The effect of erosion voids on existing tunnel linings, Tunnelling and Underground Space Technology 24 (3) (2009) 278286.
- [5] S. Popovics, J. L. Rose, J. S. Popovics, The behaviour of ultrasonic pulses in concrete, Cement and Concrete Research 20 (2) (1990) 259-270.
- [6] Y. Le Sant, M. Marchand, P. Millan, J. Fontaine, An overview of infrared thermography techniques used in large wind tunnels, Aerospace science and technology 6 (5) (2002) 355-366.
- [7] A. G. Davis, M. K. Lim, C. G. Petersen, Rapid and economical evaluation of concrete tunnel linings with impulse response and impulse radar nondestructive methods, NDT &amp; E International 38 (3) (2005) 181-186.
- [8] P. Holub, T. Dumitrescu, Detection of cavities using electrical parameters and georadar in a water delivery tunnel, Journal of Applied Geophysics 31 (1-4) (1994) 185-195.
- [9] M. Kuloglu, C.-C. Chen, Ground penetrating radar for tunnel detection, in: 2010 IEEE International Geoscience and Remote Sensing Symposium, IEEE, 2010, pp. 4314-4317.

- [10] F. Zhang, X. Xie, H. Huang, Application of ground penetrating radar in grouting evaluation for shield tunnel construction, Tunnelling and Underground Space Technology 25 (2) (2010) 99-107.
- [11] A. M. Alani, F. Tosti, GPR applications in structural detailing of a major tunnel using different frequency antenna systems, Construction and Building Materials 158 (2018) 1111-1122.
- [12] S. Jazayeri, S. Kruse, I. Hasan, N. Yazdani, Reinforced concrete mapping using full-waveform inversion of GPR data, Construction and Building Materials 229 (2019) 117102.
- [13] F. Zhang, B. Liu, L. Liu, J. Wang, C. Lin, L. Yang, Y. Li, Q. Zhang, W. Yang, Application of ground penetrating radar to detect tunnel lining defects based on improved full waveform inversion and reverse time migration, Near Surface Geophysics 17 (2) (2019) 127-139.
- [14] E. Pasolli, F. Melgani, M. Donelli, Automatic analysis of GPR images: A pattern-recognition approach, IEEE Transactions on Geoscience and Remote Sensing 47 (7) (2009) 2206-2217.
- [15] X. Xie, P. Li, H. Qin, L. Liu, D. C. Nobes, GPR identification of voids inside concrete based on the support vector machine algorithm, Journal of Geophysics and Engineering 10 (3) (2013) 034002.
- [16] Q. Dou, L. Wei, D. R. Magee, A. G. Cohn, Real-time hyperbola recognition and fitting in GPR data, IEEE Transactions on Geoscience and Remote Sensing 55 (1) (2016) 51-62.
- [17] X. Zhou, H. Chen, J. Li, An automatic GPR B-scan image interpreting model, IEEE Transactions on Geoscience and Remote Sensing 56 (6) (2018) 3398-3412.
- [18] J. Long, E. Shelhamer, T. Darrell, Fully convolutional networks for semantic segmentation, in: Proceedings of the IEEE conference on computer vision and pattern recognition, 2015, pp. 3431-3440.
- [19] O. Ronneberger, P. Fischer, T. Brox, U-net: Convolutional networks for biomedical image segmentation, in: International Conference on Medical image computing and computer-assisted intervention, Springer, 2015, pp. 234-241.
- [20] V. Badrinarayanan, A. Kendall, R. Cipolla, Segnet: A deep convolutional encoder-decoder architecture for image segmentation, IEEE transactions on pattern analysis and machine intelligence 39 (12) (2017) 2481-2495.
- [21] Y. Xu, T. Mo, Q. Feng, P. Zhong, M. Lai, I. Eric, C. Chang, Deep learning of feature representation with multiple instance learning for medical image analysis, in: 2014 IEEE international conference on acoustics, speech and signal processing (ICASSP), IEEE, 2014, pp. 1626-1630.

- [22] B. Kayalibay, G. Jensen, P. van der Smagt, CNN-based segmentation of medical imaging data, arXiv preprint arXiv:1701.03056.
- [23] S. Li, B. Liu, Y. Ren, Y. Chen, S. Yang, Y. Wang, P. Jiang, Deep-learning inversion of seismic data, IEEE Transactions on Geoscience and Remote Sensing 58 (3) (2020) 2135-2149.
- [24] B. Liu, Q. Guo, S. Li, B. Liu, Y. Ren, Y. Pang, L. Liu, P. Jiang, Deep learning inversion of electrical resistivity data, IEEE Transactions on Geoscience and Remote Sensing (2020) doi: 10.1109/TGRS.2020.2969040.
- [25] B. Liu, Y. Ren, H. Liu, H. Xu, Z. Wang, A. G. Cohn, P. Jiang, GPRInvNet: Deep learning-based ground penetrating radar data inversion for tunnel lining, arXiv preprint arXiv:1912.05759.
- [26] W. Al-Nuaimy, Y. Huang, M. Nakhkash, M. Fang, V. Nguyen, A. Eriksen, Automatic detection of buried utilities and solid objects with GPR using neural networks and pattern recognition, Journal of applied Geophysics 43 (2-4) (2000) 157-165.
- [27] X. Xu, Y. Lei, F. Yang, Railway subgrade defect automatic recognition method based on improved Faster R-CNN, Scientific Programming 2018.
- [28] Z. Tong, J. Gao, H. Zhang, Recognition, location, measurement, and 3D reconstruction of concealed cracks using convolutional neural networks, Construction and Building Materials 146 (2017) 775-787.
- [29] J. L. Davis, A. P. ANNAN, Ground-penetrating radar for high-resolution mapping of soil and rock stratigraphy 1, Geophysical prospecting 37 (5) (1989) 531-551.
- [30] Y. Gao, Y. Jiang, B. Li, Estimation of effect of voids on frequency response of mountain tunnel lining based on microtremor method, Tunnelling and Underground Space Technology 42 (2014) 184-194.
- [31] T. Yu, A. Zhu, Y. Chen, Efficient crack detection method for tunnel lining surface cracks based on infrared images, Journal of Computing in Civil Engineering 31 (3) (2016) 04016067.
- [32] M. Berman, A. Rannen Triki, M. B. Blaschko, The Lov´ asz-Softmax loss: A tractable surrogate for the optimization of the intersection-over-union measure in neural networks, in: Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition, 2018, pp. 4413-4421.
- [33] B. Eerapu, Karuna Kumari Ashwath, S. Lal, F. DellAcqua, A. N. Dhan, Dense refinement residual network for road extraction from aerial imagery data, IEEE Access 7 (2019) 151764-151782.
- [34] G. E. Hinton, N. Srivastava, A. Krizhevsky, I. Sutskever, R. R. Salakhutdinov, Improving neural networks by preventing co-adaptation of feature detectors, arXiv preprint arXiv:1207.0580.

- [35] A. Krogh, J. A. Hertz, A simple weight decay can improve generalization, in: Advances in neural information processing systems, 1992, pp. 950-957.
- [36] A. Garcia-Garcia, S. Orts-Escolano, S. Oprea, V. Villena-Martinez, J. Garcia-Rodriguez, A review on deep learning techniques applied to semantic segmentation, arXiv preprint arXiv:1704.06857.
- [37] D. R. Martin, C. C. Fowlkes, J. Malik, Learning to detect natural image boundaries using local brightness, color, and texture cues, IEEE Transactions on Pattern Analysis &amp; Machine Intelligence (5) (2004) 530-549.
- [38] C. Sivaji, O. Nishizawa, G. Kitagawa, Y. Fukushima, A physical-model study of the statistics of seismic waveform fluctuations in random heterogeneous media, Geophysical Journal International 148 (3) (2002) 575-595.
- [39] B. Liu, Y. Pang, D. Mao, J. Wang, Z. Liu, N. Wang, S. Liu, X. Zhang, A rapid four-dimensional resistivity data inversion method using temporal segmentation, Geophysical Journal International 221 (1) (2020) 586-602.

Figure 2: The workflow of the CNN based segmentation method. Prepared GPR data is input into the CNN, and the predicted result, based on current CNN parameters, is obtained. The difference between the prediction result and the actual model is calculated by the loss function, and the CNN parameters are updated by the gradient. The CNN is trained after multiple iterations. After inputting the GPR data, the CNN parameters can be used to directly obtain the fault segmentation.

<!-- image -->

Flow chart

Figure 3: Effect of dielectric constant on GPR signals.

<!-- image -->

Line chart

Figure 4: The network structure of Segnet.

<!-- image -->

Bar chart

Figure 5: Loss curves of the three CNN methods. (a) and (b) are the curves of the cross entropy loss function (Loss 1) and the Lovsz softmax loss function (Loss 2) on the training set with epoch, respectively. (c) and (d) are the curves of the cross entropy loss function (Loss 1) and the Lovsz softmax loss function (Loss 2) on the validation set with epoch, respectively. In these graphs the red, black and blue lines represent Segnet (1 loss), Segnet(2 loss), U-net(2 loss), respectively.

<!-- image -->

Line chart

Figure 6: Prediction results of three methods on test set data. It contains four sets of data, ground truth, and prediction results of Segnet(1 loss), Segnet(2 loss), and U-net(2 loss).

<!-- image -->

Bar chart

Figure 7: Water-free defects in the tunnel lining without rebar model prediction results. (a) represents the water-free crack and void model without surrounding rock. (b) represents the water-free crack model. (c) represents the water-free crack and separation model. (d) represents the water-free void and separation model. Each color represents the same material as in Fig. 6.

<!-- image -->

Engineering drawing

Figure 8: Water-bearing defects in the tunnel lining without rebar model prediction results. (a) represents the water-bearing crack and void model without surrounding rock. (b) represents the water-bearing cracks model. (c) represents the water-bearing crack and separation model. (d) represents the water-bearing void and separation model. Each color represents the same material as in Fig. 6.

<!-- image -->

Line chart

Figure 9: Water-bearing defects in the tunnel lining without rebar model prediction results. (a) represents the water-free crack and void model with rebars. (b) represents the waterbearing crack and void model with rebars. (c) represents the water-free crack and separation model with rebars. (d) represents the water-bearing void and separation model with rebars. Each color represents the same material as in Fig. 6.

<!-- image -->

Scatter plot

Figure 10: The model we built and GPR for detection.

<!-- image -->

Photograph

Figure 11: Results of the real GPR data. These show measured GPR data, corresponding model, and the model prediction respectively.

<!-- image -->

Engineering drawing
<!-- image -->

Logo

Deposited via The University of Leeds.

White Rose Research Online URL for this paper:

[https://eprints.whiterose.ac.uk/id/eprint/208177/](https://eprints.whiterose.ac.uk/id/eprint/208177/)

Version: Accepted Version

## Article:

Jiang, Y., Wang, L., Zhang, B. et al. (2023) Tunnel lining detection and retrofitting. Automation in Construction, 152. 104881. ISSN: 0926-5805

[https://doi.org/10.1016/j.autcon.2023.104881](https://doi.org/10.1016/j.autcon.2023.104881)

©2023, Elsevier. This manuscript version is made available under the CC-BY-NC-ND 4.0 license http://creativecommons.org/licenses/by-nc-nd/4.0/. This is an author produced version of an article published in Automation in Construction. Uploaded in accordance with the publisher's self-archiving policy.

## Reuse

This article is distributed under the terms of the Creative Commons Attribution-NonCommercial-NoDerivs (CC BY-NC-ND) licence. This licence only allows you to download this work and share it with others as long as you credit the authors, but you can't change the article in any way or use it commercially. More information and the full terms of the licence here: https://creativecommons.org/licenses/

## Takedown

If you consider content in White Rose Research Online to be in breach of UK law, please notify us by emailing eprints@whiterose.ac.uk including the URL of the record and the reason for the withdrawal request.

<!-- image -->

Logo

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

29

30

31

32

## Tunnel lining detection and retrofitting

Yandan Jiang 1 , Lai Wang 1 , Bo Zhang 4 , Xiaowei Dai 2 , Jun Ye 2,3,6 , Bochao Sun 2 , Nianwu Liu 4 , Zhen Wang 5 , Yang Zhao 2,3 1. State Key Laboratory of Industrial Control Technology, College of Control Science and Engineering, Zhejiang University, Hangzhou, China, 310027 2. College of Civil Engineering and Architecture, Zhejiang University, Hangzhou, China, 310058 3. Center for Balance Architecture, Zhejiang University, Hangzhou, China, 310058 4. School of Civil Engineering and Architecture, Zhejiang Sci-Tech University, Hangzhou, China, 310018 5. Department of Civil Engineering, Zhejiang University City College, Hangzhou, China, 310015 6. Centre for Intelligent Infrastructure, University of Strathclyde, Glasgow, UK, G1 1XJ

ABSTRACT: The underground tunnel structure is important and common in transport infrastructures. With the increasing service time, it is crucial to detect the deteriorations in the ageing tunnel linings and make informed retrofitting decisions to ensure their structural safety and extend their service life cycle. This emphasizes the importance of understanding the framework of tunnel lining detection, evaluation, and retrofitting. However, there is no up-to-date review available that covers the entire workflow of tunnel lining detection and retrofitting. This paper provides a comprehensive review of non-destructive  testing  (NDT)  methods,  health  evaluation  methods,  and  retrofitting methods for tunnel linings. The achievements, challenges, and development trends of these methods are illustrated. Specifically, NDT methods for three representative tunnel lining  defects,  including  cracks,  leakage,  and  voids,  are  introduced  and  analyzed  to show the corresponding advantages and disadvantages. Based on the data obtained by the defect detection methods, the procedures for lining health status evaluation are also summarized  to  provide  a  systematic  and  quantitative  evaluation  of  tunnel  linings. Finally, the retrofitting methods and techniques that are suitable for lining structures are reviewed.  This  paper  provides  an  insight  into  the  development  of  structural  health monitoring (SHM) and the maintenance of tunnel linings, offering a systematic guide for understanding the framework of tunnel lining detection and retrofitting.

KEY WORDS: Tunnel lining; Defects; Non-destructive testing; Evaluation; Reinforcement; Retrofitting

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

29

## 1. Introduction

Transportation infrastructure has been developed rapidly during the past decades due to the issues of increased population and traffic congestion [1-3]. Among them, the tunnel structures have become more and more important due to their high construction efficiency and the limited space in urban areas [4]. With the popularity of tunnel structures, the travel efficiency has been significantly improved and transportation costs have been dramatically reduced. In 2019, there were 1615 tunnel projects globally under construction, and 2615 tunnels under planning [5]. China has built over 30,000 km of traffic tunnels and is constructing or planning more than 40,000 km to meet city expansion demands [6]. Japan has built 5,098 km of traffic tunnels, some are over 50 years old but are still in service [7]. However, a significant problem is that many tunnels entered the "maintenance and repair" life cycle [8]. After long-term service, some tunnels exhibit significant health issues, such as lining cracking, water leakage, and voids behind the linings [8,9]. Since the linings are important structural components of the tunnel, accurate detection, periodic monitoring of their status and timely maintenance are crucial to ensure safe operations.

As the service time increases, the structural health of tunnel linings gradually deteriorates due to ageing, long-term loading, and environmental factors [10]. Inadequate maintenance accelerates this process, therefore tunnel structure failures occur frequently [11]. In 2012, over 300 concrete ceiling panels collapsed in the Sasago Tunnel in Japan, resulting in significant damage to the tunnel structure [12]. The collapse of approximately 10 m 2 of tunnel lining in 2020 caused damage to a vehicle and resulted in life loss [13]. These accidents from the failure of tunnel linings caused a threat to the safety of the traffic and human lives. To mitigate these risks, it is increasingly important to  use  structural  health  monitoring  (SHM) data and appropriate damage assessment methods to detect  and  evaluate  the  defects  in  the  linings  and  adopt  effective  means  of  maintenance  and reinforcement on demand to reduce the risk of lining failures [14-16].

Qualitative  and  quantitative  detection  of  tunnel  lining  defects  is  essential  for  subsequent evaluation  and  reinforcement.  With  the  rapid  development  of  non-destructive  testing  (NDT) techniques, a wide range of tunnel lining inspection methods has been developed, including visionbased methods, acoustic techniques, infrared thermography, radar, electrical techniques [17], etc. In recent years, these traditional NDT methods in combination with artificial intelligence and robotics have emerged as a new research focus [18-20]. Previous literature reviews help us to understand 1 the  development  of  the  methodology  in  a  specific  structure,  defect,  or  technique,  including 2 infrastructure inspections [16,19,21,22], targeting at a single type of defect like crack [18], or a 3 single detection method, such as computer vision [10,16,18,19], ground-penetrating radar (GPR) 4 [22], acoustic techniques [23] and robotic techniques [24]. These review papers are summarized and 5 compared  in Appendix  1 .  However,  there  are  no  specific  overviews  of  NDT  techniques  for 6 detecting the various defects in tunnels. With the rapid development of detection technology and 7 the  increasing  demand  for  tunnel  inspection,  it  is  beneficial  to  summarize  the  latest  detection 8 methods to provide a comprehensive review of tunnel inspection. 9

10

11

12

13

14

15

16

17

18

19

20

21

22

Based  on  the  data  obtained  from  tunnel  inspection,  the  health  issues  of  the  tunnel  can  be assessed. The evaluation methods can be qualitative or quantitative according to the characteristics of the defects [25]. Typically, the overall condition evaluation of the tunnel is carried out by Expert Methods [26]. With the in-depth exploration of the ageing mechanism of architectural structures and the development of the detection methodology, new evaluation techniques have been proposed by researchers [24,27]. As more and more evaluation methods are available [28-30], the evaluation framework  for  the  tunnels  is  gradually  forming.  It  includes  three  main  steps:  presentation  of evaluation criteria, selection of evaluation parameters, and derivation of evaluation results. From previous studies, the boundary between detection and evaluation is not always clear [24,27]. There is a lack of reviews sorting the effective methods for structural health assessments of tunnel linings (summarized as Appendix 2 ). Therefore, a review of the structural assessment methods and their classifications  according  to  the  characteristics  of  various  defect  detection  methods  targeting  at tunnel linings is needed.

With the results of tunnel inspection and health assessment, retrofitting decisions can be made. 23 Once the evaluation shows that the conditions of reinforcement are met, timely retrofitting of tunnel 24 linings is crucial to extend the lifespan of tunnels [31]. The tunnel retrofitting has been one of the 25 main research focuses over the last few decades [31-40], as shown in Appendix 3 . Previous studies 26 provided brief  summaries  of  tunnel  strengthening  methods  related  to  the  actual  tunnel  projects. 27 Therefore, the various retrofitting methods, including their rationales, advantages, disadvantages, 28 and future development, have not been specifically reviewed yet. A systematic organization and 29

1

analysis of these details should be conducted.

In conclusion, there is no review available that systematically covers the entire workflow of 2 tunnel  lining  detection,  assessment,  and  retrofitting. As  shield  tunnels  become  more  and  more 3 widely used, there is a need for an up-to-date review and summary that can address these issues. 4 This paper is to provide a comprehensive literature review covering the entire framework of tunnel 5 lining  detection  and  retrofitting,  including  the  detection  techniques  for  different  defects,  the 6 scientific evaluation methods of structural health, and the effective retrofitting methods. The state 7 of  the  art  of  different  techniques/methods  targeting  at  tunnel  lining  detection  and  retrofitting  is 8 presented. The advantages, disadvantages, correlation, and contradiction of different methods are 9 also  compared  and  discussed.  This  review  can  help  researchers  to  have  a  rapid  systematic 10 understanding of the various aspects of tunnel lining detection and retrofitting, and have an idea of 11 the challenges that remain to be overcome. 12

13

14

15

16

17

The review will be structured as follows: Section 2 reviews the classical detection methods of tunnel lining defects and their applications. Section 3 summarizes the existing evaluation methods of tunnel lining conditions. Section 4 presents the available tunnel retrofitting methods and Section 5 concludes the state-of-the-art review, followed by some discussions, challenges and the research to be undertaken in the future.

18

19

20

21

22

23

24

25

26

27

28

## 2. Tunnel lining defects and detection methods

Understanding the different categories of defects in tunnels is critical for exploring effective detection methods. Although classifications of tunnel defects in existing studies differ slightly, they can be divided into several types. The most commonly observed defects of tunnel linings include cracks, leakage, and voids [41-45]. Fig. 1 demonstrates the three types of defects. Although there are some relationships between different defects [13], cracks are the most commonly observed form of tunnel lining damage and attract significant attention from researchers [19]. The voids behind the lining are the main cause of cracks while the leakage often occurs at cracks [13]. These defects can be  identified  and  detected  by  different  techniques  according  to  different  physical  mechanisms. However, the inspection and assessment of these defects are still challenging due to the limited access to the internal space of the tunnel lining structures.

1

2

3

4

5

6

7

- 8

9

10

11

12

13

14

15

16

17

18

19

Fig. 1. Typical tunnel lining defects: (a) cracks and void [13] ; (b) leakage [46] .

<!-- image -->

Photograph

## 2.1 Cracks

Cracks possess a morphological feature with elongated and high-contrast edges and lead to changes in the lining structure. As such, they can be detected through various physical methods, including visual inspection, radar, and acoustic techniques [17].

Conventional visual inspection of tunnel lining cracks relies heavily on manual labor [19]. However, the operator is exposed to the dangerous tunnel environment, including large isolated areas,  low  visibility,  dust,  humidity  or  even  toxic  gases  [24]. Additionally,  the  subjectivity  and inefficiency  of  this  approach  in  obtaining  data  for  structural  evaluation  are  still  issues  to  be addressed in the future.

To achieve more efficient, accurate, and standardized crack inspections, photogrammetric and vision-based methods have been proposed [19]. And currently, vision-based methods are generally considered  to  be  the  most  popular  NDT  methods  in  tunnel  inspections. Fig.  2 shows  a  typical structure of an image acquisition system for tunnel lining, including a group of linear array cameras, a group of laser sources, a control and image acquisition unit, and an industrial personal computer (IPC). These components are usually mounted on a track inspection train for mobile inspections [47].

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

Fig. 2. Typical structure of the image acquisition system.

<!-- image -->

Flow chart

Benefiting from image processing technology, vision-based methods have experienced rapid development over the past decades. Conventional image processing methods for crack detection include threshold techniques, morphological operators, texture analysis, pattern recognition, etc. [10]. Fig. 3 shows a common flowchart of digital image processing for crack detection, including image enhancement, image processing (segmentation and feature extraction), and crack analysis. The results of image processing are used for subsequent qualitative or quantitative analysis. Lei et al. [48] proposed a tunnel lining crack recognition system that employs a series of image processing methods. An effective segmenting method, combining adaptive partitioning, edge detection, and threshold technique, was presented, and the size of cracks was calibrated for precise quantification. Research  results  demonstrated  a  deviation  of  less  than  20%  in  the  measurement  of  crack  sizes between the proposed system and manually measured field tests. Gong et al. [47] used multiple line scan cameras to collect the full images of tunnel lining surfaces and proposed an automatic crack detection  method.  Image  threshold  segmentation  and  edge  threshold  were  used  to  obtain  the morphological and gradient features of the crack, and cracks were extracted using the seed-filling algorithm.  Additionally,  the  proposed  method  can  effectively  eliminate  interference,  such  as pipeline edges and strip marks, through multistage fusion filtering. Wang et al. [49] proposed a method that combined the improved multiscale Retinex (MSR) algorithm for filtering and the eightdirection  Sobel  operator  for  edge  extraction. A  recognition  rate  of  97.5%  was  obtained  and  the

- processing efficiency of the algorithm was relatively high. Considering the impact of image quality, 1
- such as low contrast and uneven illumination, on the effectiveness of crack detection, Yu et al. [50] 2
- used infrared images instead of visible light images. The authors computed the conditional texture 3
- anisotropy of each pixel and obtained the optimum threshold through iteration to extract the cracks. 4
- The proposed method was applied to 50 crack images with different background and illumination 5
- conditions,  resulting  in  better  recognition  effectiveness  than histogram  estimation  and  Otsu 6
- algorithm. The above conventional image processing methods have made significant progress in 7
- improving the crack detection performance of vision-based methods, including recognition rate, 8
- detection  efficiency  and  robustness.  However,  they  share  a  common  limitation,  which  is  the 9
- selection of the optimum threshold for image segmentation. This step can be troublesome and has a 10
- significant impact on the effectiveness of the detection. 11

12

<!-- image -->

Flow chart

13

14

With the development of machine learning (ML) and deep learning (DL), the quality of crack 15 detection has been significantly improved in recent years [18]. Compared to conventional image 16 processing methods, the feature extraction of ML/DL methods is automatically performed during 17 the training process, without the need to determine the optimum threshold. Hsieh and Tsai [18] 18 divided  DL  crack  detection  into  three  task  categories,  classification,  object  detection,  and 19 segmentation, as shown in Fig. 4 . The authors reviewed 68 ML-based crack detection methods and 20 summarized their trends. They observed that the patch-level classification was more popular before 21 2016, but segmentation methods have been rapidly developed after that, providing higher-resolution 22 data and more precise crack detections. They also found that deeper backbone networks in fully 23 convolutional network (FCN) models and skip connections in u-shaped network (U-Net) models 24 had satisfactory performance after evaluating eight crack segmentation models. Xue and Li [51] 25 proposed a fully convolutional network (FCN) for classification and a region proposal network 26

Fig. 3. Flowchart of conventional image processing.

(RPN) and position-sensitive region of interest (RoI) pooling for defects detection. After comparing 1 with AlexNet (ISVRC2012), GoogLeNet (ISVRC2014), and VGG16 (ISVRC2014), their model 2 achieved  a  best-set  accuracy  of  over  95%  at  a  test  time  of  48  ms.  It  also  outperformed  the 3 conventional methods and region-based faster CNN (Faster R-CNN) in terms of detection rate, 4 detection accuracy, and detection efficiency. Ren et al. [52] proposed an end-to-end pixel-wise crack 5 segmentation algorithm based on an improved deep FCN called CrackSegNet, the architecture of 6 which is shown in Fig. 5 . The network combined the advantages of FCN, U-Net, and Pyramid Scene 7 Parsing Network (PSPNet) and was improved based on the characteristics of the crack dataset. 8 Compared to the conventional methods and the FCN, CrackSegNet had a higher detection accuracy. 9 Xu  and Yang  [53]  developed  a  method  combining  geometric  modeling  and  a  crack  detection 10 algorithm. The B-spline surface approximation algorithm was used to construct a three-dimensional 11 tunnel model, and a mask region-based convolutional neural network (Mask R-CNN) was deployed 12 for  crack  segmentation.  Their  method  provided  a  significant  solution  for  intelligent  tunnel 13 monitoring. Zhao et al. [54] presented a method for crack segmentation and quantification, where 14 they utilized a path aggregation network (PANet) model to detect cracks and an A* algorithm in the 15 semantic branch to measure the size of the cracks. In their work, the proposed method had a lower 16 error  rate  than  the  medial  axis  algorithm  in  crack  quantification.  Li  et  al.  [55]  designed  a  data 17 collection system for image acquisition and proposed a multi-layer feature fusion network based on 18 the Faster R-CNN for defect detection. The enhanced network had a good performance in practical 19 field tests, but it did not run in a real-time image processing system. 20

21

22

23

24

Fig. 4. (a) Input image of cracks; (b) classification; (c) object detection; and (d) segmentation [18] .

<!-- image -->

Engineering drawing

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

Fig. 5. Network architecture of CrackSegNet [52] .

<!-- image -->

Bar chart

In previous reviews, Attard et al. [10] explained the image processing techniques for detecting cracks and other defects in detail. Koch et al. [19] presented a summary of defect detection based on computer vision and condition assessment for several types of civil infrastructure, and part of the content described the visual inspection approaches of concrete tunnel cracks. Both of them provided useful insights into the vision-based detection methods of tunnel lining defects. Although visionbased methods are currently the dominant means of tunnel lining inspection, their limitation is clear. Vision-based methods rely on what is visually observed, which means only surface defects and crack size on the surface can be detected and measured, the internal defects and the crack depth information cannot be obtained. Therefore, other detection techniques are needed to provide more comprehensive essential data.

Another technique used for crack detection is GPR. GPR has been widely used in geophysics and related disciplines [20,56]. It uses electromagnetic fields to detect the lossy dielectric materials and obtain the subsurface status by analyzing the characteristics of the reflected echoes, such as travel time, amplitude, phase velocity, and attenuation with frequency [56]. GPR has been used in the detection of tunnel lining defects, including cracks. Fig. 6 (a) illustrates the construction of the GPR device, which consists of antennas for transmitting and receiving electromagnetic waves, a radar control unit with the function of processing GPR data, and other auxiliary structures [57]. Fig. 6  (b) shows  the  basic  principle  of  GPR  for  crack  detection.  When  the  electromagnetic  wave encounters an object with physical properties different from the surrounding medium, then it is scattered from the target and detected by the receiving antenna. A 2D image can be constructed after post-processing. Xiang et al. [58] used GPR in the Damaoshan highway tunnel and obtained results 1 including rebar position, second lining thickness, and probable defects behind the lining. Several 2 probable internal cracks were revealed through the anomalous areas in the GPR data profiles. Fig. 3 7 showed the damage radargrams obtained by GPR, where B and C indicated the features of cracks 4 or fissures. Feng et al. [59] proposed a hybrid algorithm that combines finite-difference time-domain 5 (FDTD) and finite-element time-domain methods for GPR simulation and built numerical models 6 of various defects in the tunnel lining. It is worth noting that GPR is mainly applied to the inspection 7 of internal conditions, with only a few studies exploring its application in surface crack detection, 8 crack  depth  measurement  [60],  and  micro-crack  detection  [61].  Ling  et  al.  [61]  explored  the 9 feasibility of distinguishing the weak reflected signal corresponding to the micro-cracks among the 10 complicated signal by using the orthogonal matching pursuit and the Hilbert transform (OMHT) 11 method. This method could significantly enhance the weak signal and improve the resolution of the 12 GPR image. In terms of detection accuracy and resolution, the GPR is heavily dependent on data 13 interpretation. Besides, the selection of antenna frequency and the design of the antenna are critical 14 to the detection performance as well. Although the work mentioned above provides some useful 15 references, these difficulties remain as an important focus of future research. 16

17

18

19

Fig. 6. (a) The GPR radar GSSI SIR 3000 and (b) principle of GPR [57] .

<!-- image -->

Engineering drawing

1

2

3

Sonic and ultrasonic techniques are effective NDT methods for unilaterally accessible concrete 4 structures  such  as  tunnel  linings  or  thick  concrete  walls  [23,62-69].  There  is  a  category  of 5 techniques,  including  the  impact-echo  technique,  Time-Of-Flight  Diffraction  (TOFD),  impulse 6 response technique, ultrasonic tomography  technique,  and  others. In crack detection, the 7 transmission and diffraction of acoustic waves inside the medium can provide useful information 8 for measuring crack size. The TOFD technique can successfully detect the diffraction of acoustic 9 waves at the edges or tips of defects to obtain the position and size of cracks [62,63]. Fig. 8 shows 10 the measurement principle of TOFD. When an acoustic signal is emitted by the transmitter, the tips 11 of the crack will diffract the ultrasound beam. This diffracted beam can then be detected by the 12 receiver and the arrival time can be accurately measured. The depth and size of the crack can be 13 calculated according to Eq. (1) [62]. 14

15

16

Fig. 8. Principle of TOFD.

<!-- image -->

Engineering drawing

Fig. 7. Damage radargram of left haunch (A and B) and vault profile (C and D) [58] .

<!-- image -->

Engineering drawing

1

2

3 where   is the depth of the upper or lower tip of the crack,   is the velocity of sound, ∆  is the 4 travel time of the ultrasound beam,   is half of the distance between the transmitter and receiver, 5 and ℎ is  the  length  of  the  crack.  Habibpour-Ledari  and  Honarvar  [64]  extended  the  TOFD 6 technique from 2D space to 3D space and developed an active algorithm based on the time-of-flight 7 of the echoes. The proposed algorithm was tested in defect location experiments and achieved a 8 precision of 6.7%, which was lower than the passive algorithm. However, it had fewer limitations 9 on  the  number  of  receivers  than  the  passive  algorithm,  making  it  a  viable  option  for  practical 10 applications.  Moreover,  the  reflection,  transmission,  and  scattering  of  Rayleigh  surface  wave 11 transmission (SWT) across a surface-breaking crack have also been studied [65,66]. Fig. 9 shows 12 the corresponding measurement principle of the SWT test [67]. In the SWT method, two sensors 13 are located on the two sides of the crack, respectively. The depth of the crack can be estimated from 14 the transmission coefficient, which is defined as the spectral amplitude ratio between the transmitted 15 surface waves      and the incident surface waves     in the frequency domain [67]. Angel and 16 Achenbach [65] obtained the curve for the transmission coefficient versus the frequency under the 17 constraint of fixed incidence angle through theoretical derivation. Yew et al. [66] also estimated the 18 relationship between the crack depth and the amplitude of the transmitted surface wave through 19 experimental study. This early work provided an important theoretical basis for subsequent sensor 20 development and signal processing. Since the traditional acoustic techniques for crack inspection 21 require direct contact between the devices and the concrete surface, which is time-consuming and 22 requires  adequate  coupling,  several  non-contact  air-coupled  SWT-based  sensors  have  been 23 developed [68,69]. This type of sensor can also achieve rapid measurement of crack depth. Kee and 24 Zhu [68] used numerical simulations, based on the finite element method (FEM), to investigate the 25 near-scattering of surface waves caused by a surface breaking crack in concrete and compared it 26 with  the  surface  wave  transmission  measured  in  the  far  field.  It  is  showed  that  surface  wave 27 transmission  measurements  in  the  far  field  could  effectively  avoid  near-field  effects.  The 28

<!-- formula-not-decoded -->

measurement results also showed a high degree of consistency with the analytical results. Moreover, 1 both of them verified the curve for the normalized transmission coefficient versus the normalized 2 crack depth proposed by Angel and Achenbach [65]. In addition, a simplified algorithm using only 3 the transmission value at the center frequency was proposed and experimentally verified. A more 4 detailed description of the study on crack detection in concrete structures using SWT-based sensors 5 can be found in the work of Kee et al. [67]. In et al. [69] investigated a fully non-contact ultrasonic 6 sensor using air-coupled transducers and reconstructed the relationship between the transmission 7 coefficient and the normalized notch depth, as shown in Fig. 10 . In the measurement, the elastic 8 waves were generated by the sensors, and mechanical contact was no longer required. These sensors 9 were  of  higher  repeatability,  and  the  experimental  results  showed  satisfactory  consistency 10 agreement  with  the  numerical  simulations.  The  sensors  were  expected  to  be  used  for  mobile 11 continuous monitoring after improving penetration depth and stability. However, in these tests, the 12 sensors were applied to a specimen with a shallow notch instead of a real crack with an irregular 13 shape  and  depth.  To  achieve  non-contact  measurements,  special  ultrasonic  sensors  capable  of 14 generating high-energy excitation signals are often required. Although these works have not been 15 specifically applied to the detection of tunnel lining cracks, they provide a beneficial reference for 16 field inspection, especially when used for the size measurement of cracks. For complex NDT tasks, 17 a combination of these techniques could be a good choice. Non-destructive acoustic techniques for 18 the inspection of concrete structures and their detailed applications and limitations can be found in 19 the work by Schabowicz [23]. The author introduced a method that combined ultrasonic tomography 20 and the impact-echo technique to determine the position of cracks with a detection accuracy of 521 10 mm. 22

23

24

Fig. 9. Principle of SWT test [67] .

<!-- image -->

Engineering drawing

2

3

4

5

6

Fig. 10. The non-contact, air-coupled ultrasonic sensors [69] .

<!-- image -->

Photograph

A more intuitive way to detect a crack is to visualize the crack in terms of images. Tomography

- is one of the best methods to visualize defects [70,71]. It uses the information obtained from the
- projections  calculated  by  the  measurements  of  a  specifically  designed  sensor  array  to  perform 7
- inversion calculations to reconstruct the distribution of the medium inside the object. In addition to 8
- the  previously  mentioned  ultrasonic  tomography,  electrical  tomography  is  another  tomographic 9
- technique that can be potentially applied to the crack detection of tunnel linings. It can present the 10
- electrical  impedance  distribution  inside  the  concrete  structure  through  image  reconstruction 11
- algorithms. Electrical resistance tomography (ERT), electrical capacitance tomography (ECT), and 12
- electromagnetic  tomography  (EMT)  are  three  common  modalities  in  the  electrical  tomography 13
- family. Karhunen et al. [70] used ERT to visualize the position and size of the crack in the cylindrical 14
- concrete specimen. To investigate its performance in realistic single-side inspection scenarios, they 15
- tested  the  feasibility  of  the  above  ERT  system  on  the  planar  surface  of  concrete  [71].  The 16
- photographs of the specimen beam and the reconstruction results are shown in Fig. 11 . The crack in 17
- the beam after the three-point bending test extends to the middle of the specimen and can be seen 18
- in Fig. 11 (b) . Electrical tomography has many advantages such as low cost, high speed, and good 19
- real-time  performance.  However,  electrical  tomography  has  not  yet  been  applied  to  the  field 20
- detection of tunnel lining defects yet because of its low resolution. 21

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

Fig. 11. (a) Photograph of specimen; (b) ERT results [71] .

<!-- image -->

Bar chart

Different inspection methods have their advantages, disadvantages, and scope of applications, which means relying solely on one technique typically leads to limited detection performance. To obtain more information and improve detection accuracy, researchers have made progress in multisensor fusion and the integration of detection methods [20,25,47,48,72]. Mobile vehicles and robots are the carriers of integrated detection methods such as visible light or infrared cameras, radar, laser scanners, and acoustic sensors to achieve automatic tunnel inspection. The image acquisition system on the vehicle consists of cameras and lighting equipment [47,48], which can scan the lining surface at  high  speed  to  reduce  the  impact  on  tunnel  traffic.  Jiang  et  al.  [25]  proposed  a  tunnel  lining inspection  system,  which  integrated  the  lining  scanning  system  including  the  near-infrared  ray illumination and line sensor cameras, lining surface image creation software, and crack extraction software ( Fig. 12 ). The system was able to photograph the lining at a maximum speed of 100 km/h and automatically detect and assess the cracks. Mobile inspection vehicles have a strong carrying capacity and integrate several pieces of equipment, such as line scan cameras, laser scanners, and radars, so they can detect different tunnel defects and have been widely used in field inspection [72]. With  the  development  of  mobile  robot  technology,  completely  unmanned  tunnel  inspection gradually  becomes  a  reality.  The  ROBO-SPECT  European  project  [20]  achieved  an  automated tunnel inspection using the robotic system ( Fig. 13 )  which included the vision system to detect tunnel lining defects, the laser profilers to inspect tunnel structure deformation, and the ultrasonic sensors to measure the size (width and depth) of the cracks after detecting them. The measured results can be used in subsequent damage assessments. In terms of the advantages of robots over detection vehicles, robots are more flexible and have stronger information fusion and communication capabilities.

1

2

3

4

5

6

7

8

In  general,  vision-based  techniques  are  the  most  commonly  used  NDT  methods  for  the detection of tunnel lining surface cracks because of their advantages in data acquisition, efficiency,

- and accuracy. As the direction, location, type, and size of cracks are important parameters of interest 9
- to researchers and engineers, other NDT methods are necessary to provide supplemental source 10
- information, such as subsurface cracks and other quantitative crack information. 11

12

## 2.2 Leakage 13

- Water leakage is a frequent problem that occurs at lining cracks and lining joints, mainly in the 14
- sidewalls, and is greatly influenced by seasonal rainfall [13]. It can damage tunnel lining and affect 15
- the function of the structural components. Similar to crack detection, image processing techniques 16

Fig. 12. The tunnel lining surface photography vehicle components [25] .

<!-- image -->

Flow chart

Fig. 13. The ROBO-SPECT robotic system components [20] .

<!-- image -->

Photograph

can also detect leakage instead of relying on manual visual inspections. The leakage area is typically 1 darker than the background area, with an obvious edge and vertical directionality due to gravity [10]. 2 These visual features make edge detection and threshold segmentation convenient. Huang et al. [73] 3 developed moving tunnel inspection equipment that captured images of the tunnel lining with CCD 4 cameras. The leakage was then recognized by image edge detection and the Otsu algorithm [74], 5 which  was  used  to  calculate  the  optimal  threshold  for  segmenting  the  leakage  area.  However, 6 conventional  image  processing  methods  are  sometimes  not  a  good  choice  in  detecting  leakage 7 because of the interference from surface stains or attachments in the tunnel. 8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

29

Deep learning-based methods are expected to improve the accuracy of detecting leakage and have shown satisfactory performance in recent years [46,51,55,75,76]. In addition to crack detection, the methods proposed by Xue and Li [51] and Li et al. [55] also showed accurate and efficient performance in detecting leakage. In the follow-up work by Huang et al. [75], upgraded image acquisition equipment was developed to acquire tunnel lining images, and a two-stream algorithm using FCN models was applied to segment overlapped regions of crack and leakage. The proposed algorithm achieved error rates of 1.1%, 2.1%, and 1.5%, respectively, in the leakage recognition of several defect images, including leakage-only images, two-defect-nonoverlapping images, and twodefect-overlapping images. Segmenting overlapped defects was highly necessary because leakage always occurred at cracks, and this work made a beneficial attempt. Xue et al. [76] also improved the  performance  of  their  deep  learning-based  model  for  leakage  segmentation  through  data augmentation,  transfer  learning,  and  a  cascade  strategy.  They  obtained  the  leakage  area  by calibrating the relationship between the leakage area pixels and the true leakage areas, followed by estimating the safety status of the tunnel lining. Zhao et al. [46] proposed a method that combined the ResNet-101 and Mask R-CNN to classify and segment defect images. In the integrated progress, the combination of classification and segmentation methods achieved an accuracy of 89.3%. Deep learning-based methods enabled machines to achieve automatic and robust defect detection after acquiring  image  sets  containing  a  large  number  of  lining  defect  images.  They  showed  better performance than conventional image processing methods for single or mixed tunnel lining defects. The  features  were  extracted  automatically  for  follow-up  tasks,  including  classification,  object detection,  and  segmentation.  However,  deep  learning-based  methods  also  have  limitations  and

1

2

3

4

5

6

7

8 where   is the radiation in  /    ,   is the emissivity of the object with a range of 0-1,   is the 9 Stefan Boltzmann constant ( 5.67 × 10               ), and   is the surface temperature in   [77]. 10 The temperature distribution characteristics of different types of water leakage can be seen in Fig. 11 14 . Due to the different types of water leakage, such as spot-leakage type and slot-leakage type, 12 their temperature distribution characteristics are also significantly different. However, overall, they 13 exhibit a temperature distribution where the temperature at the leakage source/centre is lower, which 14 is  due  to  the  higher  ambient  temperature.  It  is  useful  for  identifying  leakage  by  detecting  the 15 difference between the leakage area and the background lining in the infrared radiation temperature 16 field. Infrared thermography includes both passive and active techniques. The former refers to the 17 detection of natural temperature differences, while the latter refers to the detection of temperature 18 differences after active heating, mainly for detecting deep subsurface defects. In practice, a thermal 19 infrared camera can accurately identify a very small temperature difference (approximately 0.05 °C) 20 within the temperature range of -20℃~+150℃ [78]. Most researches on the application of infrared 21 thermography in tunnel leakage detection focused on the passive infrared thermography technique. 22 Conventional image processing techniques, such as edge detection and threshold segmentation, can 23 also be applied to thermal infrared images. Yu et al. [78] proposed a method based on laser scanning 24 and infrared thermal imaging to detect water leakage in tunnels. After the suspected leakage area 25 was detected from the laser intensity data, thermal  infrared  images were  obtained to  verify  the 26 leakage, distinguish the types of leakage, and determine the leakage location and direction. Lu et al. 27 [79] introduced an automatic inspection system for cable tunnel leakage detection based on infrared 28 thermography. Fig.  15 shows  the  inspection  system,  including  a  passive  infrared  thermography 29

problems, such as being regarded as a black-box technique that is difficult to explain physically and relies heavily on large datasets.

The above methods are based on visible light images, whose quality is inevitably affected by the practical complex environment and the confusing background [10]. An effective alternative to the visible light image is the thermal infrared image, which will not be affected by environmental light [50]. Any object with a temperature higher than 0 K will emit thermal radiation. According to the Stefan Boltzmann Law ( Eq. (2) ), the radiation energy is related to the temperature of the object:   =       (2)

- device, an ultrasonic sensor, a visible camera, and a photoelectric encoder. The control PC was 1
- connected to the inspection vehicle via WI-FI to control its movement and image acquisition, which 2
- was then processed and analyzed in real time or offline. As shown in Fig. 16 , the processing of the 3
- thermal  infrared  image  containing  the  leakage  area  went  through  several  steps,  namely  gray 4
- processing,  filtering,  binarization,  and  threshold  segmentation.  Additionally,  the  system  could 5
- accurately calculate the leakage point area and subsequently provide an objective assessment report. 6
- The inspection vehicle, however, was not automatic and instead relied on the connection to the 7
- control  computer,  which  could  lead  to  limitations  in  certain  operating  conditions.  The  passive 8
- infrared thermography method has the advantages of fast data acquisition and high accuracy, which 9
- is sufficient to detect surface leakage on the tunnel lining. However, infrared thermography may be 10
- affected by complex noise, such as thermal reflection from other heat sources [77]. The low signal11
- to-noise ratio (SNR) caused by infrared cameras and environmental factors requires more accurate 12
- and reliable methods for tunnel leakage detection. 13

14

<!-- image -->

Bar chart

15

16

Fig. 14. Temperature distribution of different leakage types [78] .

4

5

6

7

Due to the difference in absorption of infrared laser light between the moist and dry lining, the 8 lower laser intensity indicates the suspected leakage point [78]. Mobile laser scanning (MLS) can 9 be  used  to  achieve  fast  and  high-precision  acquisition  of  tunnel  lining  surface  information,  the 10 threshold-based segmentation is then performed on the laser intensity data to obtain the leakage 11 points. Fig. 17 shows the composition of the MLS system GRP5000 [80]. The MLS vehicle was 12 integrated with a laser scanner, computer, battery, odometer, and other instruments. Considering that 13 the appendages in the tunnel may have the same laser reflectivity as the leakage area, some auxiliary 14 methods were used to remove these interferences. In the aforementioned work of Yu et al. [78], 15 threshold segmentation based on the Otsu method was used to obtain the suspected water leakage 16

Fig. 15. The cable tunnel inspection system with an infrared camera [79] .

<!-- image -->

Engineering drawing

Fig. 16. (a) infrared image of tunnel lining leakage; (b) gray processing; (c) filtering; (d) binarization and threshold segmentation [79] .

<!-- image -->

Photograph

- from  the  laser  intensity  image  of  the  tunnel,  and  the  area  measurement  was  performed  after 1
- confirming the actual water leakage using an infrared camera. Xu et al. [81] used terrestrial laser 2
- scanning (TLS) to obtain the 3D point cloud and laser intensity data. The correction of laser intensity 3
- data eliminated the effects of distance and incident angle. They also considered the impact of the 4
- surface roughness of the tunnel. Similarly, a threshold-based method was applied to segment the 5
- leakage area from the intensity image. Afterward, the appendages were removed based on the 3D 6
- point cloud. The above-mentioned works provide fast, accurate, and robust leakage detection by 7
- combining laser intensity data with other methods and using a threshold algorithm. In recent years, 8
- some applications of deep learning methods in processing laser images have also been carried out 9

10

for leakage detection. Huang et al. [80] used Mask R-CNN to detect water leakage after converting

- the 3D point cloud into a 2D grayscale image, whose gray value of each pixel was derived from the 11
- average laser intensity in the grid. A new triangular mesh method was then proposed to reconstruct 12
- the 3D model of the tunnel lining to show detailed leakage information. Cheng et al. [82] proposed 13
- an improved FCN-based VGG-19 to achieve automatic leakage segmentation in the corrected laser 14
- intensity  images.  This  rapid,  high-precision  and  robust  method  was  not  affected  by  tunnel 15
- attachments,  but  the  quantitative  assessment  of  leakage  was  not  available.  In  summary,  the 16
- significant advantages of laser intensity-based leakage detection are high integration, high precision, 17
- fast tunnel scanning and no dependence on visible light illumination. However, in comparison to 18
- infrared  thermography,  leakage  diagnosis  based  on  laser  scanning  requires  more  complex  data 19
- correction and detection algorithms and may require cooperation with other sensors. 20

21

22

23

24

Fig. 17. The MLS system GRP5000 [80] .

<!-- image -->

Engineering drawing

Apart from the visual characteristics, other traits of the moist concrete, such as electromagnetic

- wave velocity, conductivity, and relative permittivity, have also undergone significant changes with 1
- the existence of leakage [21,83,84]. These characteristics can be used to inspect leakage inside the 2
- lining. Lin et al. [83] proposed an alternative method for detecting tunnel lining leakage using GPR. 3
- The sensitivity of GPR to leakage was demonstrated through forward modeling and back projection 4
- imaging.  Detailed  interpretation  criteria  for  tunnel  lining  defects,  including  water-conducting 5
- fissures, were also established. In addition, the moisture content in the structure could be imaged 6
- through conductivity measurement of the dielectric parameters [21]. Sensing the change in relative 7
- permittivity could also be used for leakage inspection, such as the ECT technique. Voss et al. [84] 8
- investigated the ECT method for monitoring unsaturated moisture flow in cement-based materials. 9
- Three cylindrical specimens with different water-cement mass ratios were used as the experimental 10
- objects, and the ECT reconstructed the relative permittivity distribution, which reflected the inside 11
- moisture ingress, as shown in Fig. 18 . These NDT methods for investigating leakage and moisture 12
- distribution  inside  the  lining  are  valuable  and  promising  in  field  applications.  However,  only 13
- qualitative detection results can be obtained because the resolution of them in leakage detection is 14
- relatively low when compared with vision-based methods. 15

16

17

18

19

20

21

22

23

Fig. 18. ECT experiment: (a) a specimen and a water reservoir, (b) top view of the ECT experimental set-up and (c) ECT reconstructions of three specimens with different watercement mass ratios after 48 hours [84] .

<!-- image -->

Engineering drawing

To  summarize  the  NDT  methods  for  tunnel  leakage  detection,  image  processing  and  deep learning methods based on visible images remain the most common and attractive methods. Infrared and  laser  intensity-based  methods  are  gaining  more  attention  due  to  their  suitability  and

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

29

effectiveness  for  leakage  detection.  However,  their  robustness  needs  improvement,  and  the quantitative results are not precise enough. In addition to image-based methods, penetrating NDT methods, such as radar and electrical tomography, are also used for inspecting internal leakage. Some of these methods are still in the laboratory research stage and have not been applied in the field yet.

## 2.3 Voids

Voids behind tunnel linings are one of the main causes of cracks and leakages [13]. In addition, the lining loses contact with the surrounding rocks due to the existence of voids, resulting in possible structural damage. Therefore, detecting voids and performing timely retrofitting are essential for tunnel structure safety. However, voids are difficult to detect since they are not directly visible on the surface, and vision-based methods are ineffective in detecting them. Therefore, NDT methods with penetrating capabilities provide the possibility for void detection [17].

Investigating the internal state by coring is one of the most common methods in geological surveys [22]. Core samples extracted from tunnel linings allow for direct observation of the internal structure and evaluation of the internal damage. However, coring can only be used at test points, and the full internal status of the object cannot be reflected. Additionally, coring may have negative effects on the structure [85]. Therefore, more efficient, fast, and non-destructive methods have been developed to inspect the internal status of tunnel linings.

GPR is currently the most mature and popular technique for the rapid detection of voids within or  behind  tunnel  linings. Fig.  19 shows  a  typical  GPR  profile.  In  the  tunnel  lining  reinforced concrete cavity model ( Fig. 19 (a) ), two cavities are located at a depth of 0.35m, and a layer of steel mesh is at a depth of 0.1m. The GPR forward profile is effectively imaged in Fig. 19 (b) [85]. The location of the steel mesh and the two cavities can be easily distinguished. In the field of tunnel NDT inspection, air-coupled GPR data is recommended to be collected first, and the area of interest can then be tested in detail by ground-coupled GPR and other in-situ detection methods [22]. Aircoupled GPR, mounted on a rapid detection vehicle, generally operates at a high frequency, resulting in  better  resolution  but  shallow  penetration  depth.  In  the  research  of Alani  and  Tosti  [86],  the differences between the two operating frequencies of GPR were investigated, and their findings suggested the use of multiple operating frequencies to obtain information about targets located at different depths with different shapes, dimensions, and constituent materials. GPR requires complex 1 data interpretation, which has a significant impact on detection accuracy. Therefore, research on 2 detecting  tunnel  lining  voids  primarily  focuses  on  methods  for  data  interpretation,  particularly 3 FDTD techniques [58,59,85,87], and the latest deep learning methods [88,89]. Yu et al. [87] used 4 GPR to investigate the thickness of the grouting layer and the defects in it, where FDTD was applied 5 for data interpretation. In the field measurements, several grouting anomalies, including voids, were 6 successfully detected by analyzing the waveform characteristics of the GPR. The detection results 7 could be used as a reference for subsequent repairs. Lyu et al. [85] applied the reverse-time migration 8 (RTM) algorithm, combined with the FDTD method and the normalized cross-correlation imaging 9 condition, to detect the tunnel lining cavities. The RTM algorithm has been proven to make sense 10 in highlighting the effective signal and suppressing the interference. Qin et al. [88] introduced an 11 automatic detection method based on Mask R-CNN for accurately identifying steel ribs, voids, and 12 initial linings from GPR images. To improve recognition accuracy, the researchers used the FDTD 13 and  deep  convolutional  generative  adversarial  network  (DCGAN)  methods  for  GPR  data 14 augmentation. Liu et al. [89] proposed GPRInvNet, a deep neural network that directly constructs 15 relative  permittivity  maps  from  GPR  B-scan  data.  The  trace-to-trace  encoder  of  GPRInvNet 16 effectively fused information from neighboring GPR traces and automatically extracted key features 17 from the B-Scan data. GPRInvNet performed well in the inversion of defects when applied to real 18 GPR data processing. In the field of engineering applications, Zan et al. [90] developed a high-speed 19 monitoring system equipped with a non-contact air-coupled GPR. The system efficiently worked 20 without interfering with railway operations. The system shown in Fig. 20 consisted of a rail mobile 21 vehicle, air-launched antennas, and matching control and imaging units. For GPR, high resolution 22 implied weak penetration, which meant that selecting the frequency involved making a trade-off 23 between these two contradictory properties. Furthermore, data interpretation posed its own set of 24 challenges.  However,  GPR  is  still  recommended  in  many  retrofitting  manuals  because  of  its 25 maturity and reliability. 26

5

6

7

Another type of radar used in engineering inspection is the transient electromagnetic radar 8 (TER), which is based on the difference in electrical resistivity of materials. The principle of the 9 transient  electromagnetic  method  (TEM)  is  shown  in Fig.  21, where TER  identifies  resistivity 10 information by applying a pulsed current to the transmitting coil (Tx-loop in Fig. 21 ) to create a 11 transient electromagnetic field and receiving the secondary induced electromagnetic field by the 12 receiving  coil  (Rx-coil  in Fig.  21 )  from  the  subsurface  layers  [91]. By  analyzing  the  received 13 electromagnetic field, the electrical resistivity and parameter information of the subsurface can be 14 measured. Ye and Ye [91] developed a TER ( Fig. 22 ) to detect the voids behind tunnel linings and 15

Fig. 19. (a) Schematic map of GPR model, (b) Reverse-time migration profiles of tunnel lining cavity model [85] .

<!-- image -->

Line chart

Fig. 20. Vehicle-mounted GPR system [90] .

<!-- image -->

Photograph

compared the results with GPR. The steep curve and high resistance in TER images revealed the 1 existence of voids. During field testing, TER observed signals of voids that were not found in GPR 2 images, and subsequent drilling tests confirmed their existence. TER is suitable for tunnel inspection 3 fields because of its deeper detection depth and higher sensitivity to low-resistance materials, such 4 as  water,  concrete,  and  rebar. Therefore, TER  can  make up for the deficiencies of GPR and be 5 applied in the engineering inspection field [92]. The combination of TER and GPR can provide new 6 approaches for voids inspection. 7

8

9

10

11

12

13

14

15

16

17

18

Fig. 21. Principle of the TEM [91] .

<!-- image -->

Engineering drawing

Fig. 22. TER system components [91] .

<!-- image -->

Engineering drawing

Acoustic techniques are important for detecting voids behind linings [23,93-98]. Impact-echo, an acoustic NDT method, is a reliable and widely used method for detecting internal defects in concrete. Carino [93] summarized the theory, numerical simulation, experimental verification, and field demonstrations of the impact-echo method. Cao et al. [94] compared several signal analysis approaches used in the impact-echo method for detecting voids behind linings. The experiment showed that the wavelet analysis can provide better energy distribution, and the dynamic stiffness 1 method can determine the location of voids. Acoustic/ultrasonic tomography and impulse response 2 techniques can also detect and locate large air voids [23]. Acoustic tomography, such as elastic wave 3 tomography (acoustic emission tomography), can visualize the wave velocity field distribution of 4 large concrete structures [95,96]. In practical tunnel inspection applications, a portable ultrasonic 5 tomography scanner was used to detect defects behind the linings. White [97] evaluated a phased6 array ultrasonic tomography system ( Fig. 23 ) and carried out a series of experiments on specimens 7 and in the field. The ultrasonic tomography images of the simulated voids in concrete slabs are 8 shown in Fig. 24. The system successfully detected and located air-filled and water-filled voids in 9 the field test. To enhance the penetration and resolution, the synthetic aperture focusing technique 10 (SAFT),  total  focusing  method  (TFM),  and  phased  array  (PA)  technique  have  been  applied  to 11 ultrasonic tomography [98]. However, acoustic-related techniques are still used as a complement to 12 GPR. Ultrasonic tomography devices are used after selecting the suspected defective region by air13 coupled GPR or other methods suitable for rapid detection. 14

15

<!-- image -->

Photograph

16

17

18

19

Fig. 23. (a) The A1040 MIRA system and (b) the transmission/reception of acoustic waves and corresponding echo intensity [97] .

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

Fig. 24. Typical C-scans for simulated defects in concrete slabs: (a) air-filled void, (b) waterfilled void [97] .

<!-- image -->

Engineering drawing

In  addition  to  ultrasonic  tomography,  other  imaging  and  tomography  techniques  have  also shown  potential  for  void  detection.  As  aforementioned,  passive  infrared  thermography  has limitations, such as the requirement for temperature difference and restricted detection depth. In the work of Konishi et al. [99], it was demonstrated that the passive approach had a higher detection rate if the concrete surface temperature was 0.35 ℃ higher than the air temperature in the tunnel. Therefore,  the  temperature condition  must  be  strictly  met  for  tunnel  inspection  using  a  passive approach, making it relatively restricted. Afshani et al. [100] discussed the heat transfer in concrete, tunnel air, and air inside voids, considering the effects of void type (open or closed), void depth, and temperature  differences.  Another  conclusion  was  that  the  temperature  difference  between  the concrete surface and the air in the tunnel of more than 0.35 ℃ was useful for detecting voids of less than 30 mm in depth. Compared with the passive approach, the active approach has more flexible configurations and better detection capabilities, but it requires longer heating and recording times due to the low thermal diffusivities of the materials [101]. Electrical tomography may also have a position in void detection of tunnel linings in the future. It has been used to inspect the internal condition of the concrete. In the experiments by Karhunen et al. [70], the ERT technique was used to reconstruct the conductivity distribution of a concrete specimen with a polyurethane which was simulated as an electrically insulated space. But these experiments in the laboratory were limited in field detection, specifically in strict electrical coupling with the specimen surface, which posed a challenge for rapid detection in the field. In addition, radiography, as a traditional NDT technique, can also be used to detect internal defects in materials. The absorption of radiation depends on the density  and  thickness  of  the  material  [21].  Cui  et  al.  [102]  tested  and  compared  two  X-ray 1 backscatter single-side imaging systems. The image systems were able to detect the defects in the 2 concrete under the cover with high resolution. Due to the fact that tunnel lining can only be accessed 3 from one side, radiography is often employed to assess components rather than massive concrete 4 structures like tunnel lining. Another limitation is the radiation of the rays is a threat to the health of 5 engineers/technicians. The X-rays, gamma rays, and neutron rays have a strong penetrating ability 6 due to their extremely short wavelength, necessitating the use of radiation protection in the field. 7

8

9

10

11

12

13

14

The invisible property of the voids behind the tunnel lining makes them more difficult to be detected. Typically, rapid air-coupled GPR scanning and manual inspection are used to detect voids initially,  followed  by  other  methods  such  as  ground-coupled  GPR,  impact-echo,  ultrasonic tomography, and infrared thermography to collect supplementary information. However, for the newly introduced techniques such as TER, electrical tomography, and radiography, research on this topic  is  still  limited.  Therefore,  further  studies  are  required  to  optimize  the  utilization  of  these methods and devise an appropriate detection scheme for voids inspection.

15

16

17

18

19

20

21

22

23

24

25

26

27

28

29

## 2.4 Summary and outlook

Among the three presented defects, cracks are the most concerning issue when it comes to lining  deterioration,  and  their  detection  methods  attract  the  most  attention.  For  crack  detection, vision-based methods are the most widely used, while other detection methods are used as auxiliary. Similarly,  visible  light-based  detection  is  commonly used  for  identifying leakage. However, the visible light-based method requires even illumination and is susceptible to interference from objects with the same visual characteristics as the targeted defect, such as stains or tunnel attachments. Therefore, two alternative methods based on infrared images and laser intensity images have been proposed for vision-based detection of cracks or leakage. V oids are located behind the tunnel lining, rendering vision-based methods ineffective. GPR, one of the traditional NDT techniques, is actively used in internal defect inspection like void detection due to its relatively strong penetration ability. These methods can be integrated to achieve more comprehensive inspection, including obtaining the type, location, and size information of defects. For in situ measurements, acoustic tomography techniques are also typically used for internal inspection. In addition, other acoustic techniques,

1

2

3

such as TOFD and SWT, have been proposed to achieve quantitative detection of defects. Table 1 provides a detailed summary and comparison of the conventional NDT methods for tunnel lining defects.

Although great progress has been made in the detection methods of tunnel linings over the last 4 few decades, the conventional methods still cannot satisfy the increasing requirements of practical 5 applications. Future work may focus on the following points: 6

1) Different methods can provide different types of defect information, such as location, size, 7 and type, which can be integrated to implement fusion and provide better performance of defect 8 detection. Multi-sensor systems equipped with advanced data fusion algorithms are to be developed 9 to implement the complementarity of different detection methods. 10

2) The development of artificial intelligence has brought a new dawn for smart sensing and 11 intelligent construction. As the current small-scale defect datasets remain a limitation of learning12 based detection methods, the establishment of big datasets will be another focus of future work, 13 either by collecting real-case data with known labels or by developing super-accurate simulation 14 models to generate close-to-reality data. Besides, introducing advanced technology such as expert 15 systems  to  post-process  the  results  of  learning-based  black-box  methods  may  be  beneficial  in 16 making the results more explainable. 17

18

3)  With  the  development  of  robotics,  integrated  mobile  inspection  has  attracted  attention.

19

20

21

22

23

24

25

26

27

28

29

Tunnel inspection is in great demand and with a large workload, especially for large-scale tunnels. That emphasizes the urgent need for real-time mobile tunnel inspection. Therefore, developing highefficiency, intelligent, and robust mobile devices or robots that integrate advanced technologies is also an important point of further research.

1

## Table 1 NDT methods for detecting tunnel linings defects

| Method                   | Targeted defects                                  | Object detected                                                             | Characteristics                                         |                | Advantages                                                                                                 | Disadvantages     | Disadvantages                                                                                                                         |
|--------------------------|---------------------------------------------------|-----------------------------------------------------------------------------|---------------------------------------------------------|----------------|------------------------------------------------------------------------------------------------------------|-------------------|---------------------------------------------------------------------------------------------------------------------------------------|
| Manual visual inspection | Cracks Leakage                                    | Surface conditions                                                          | Surface status; qualitative                             | 1) 2) 3)       | Simple; Good applicability; Low technical requirements;                                                    | 1) 2) 3) 4)       | Inefficient and inaccurate; Subjective and experience-based; Dangerous; Difficult to integrate information;                           |
| Visual inspection        | Cracks [47-55]; Leakage [46,51,55,73,75, 76]      | Visual characteristics of defects                                           | Surface status; qualitative or quantitative             | 1) 2) 3) 4) 1) | Quick; Standardized; Easy to use; System integrated; Quick;                                                | 1) 2) 3) 4) 5) 6) | Not entirely Accurate; Environmental constraints; Require adequate and even illumination; Require device and algorithms; High cost;   |
| Infrared thermography    | Leakage [31,77- 79]; Voids [99,100]               | The temperature difference between defect area and background               | Surface or internal status; qualitative or quantitative | 2) 3)          | Relatively accurate; Less affected by uneven illumination and surface stains or attachments in the tunnel; | 1) 2) 3) 4)       | Complex image processing; Low resolution of infrared images; Influenced by infrared noise; Limited detection depth by passive method; |
| Radar                    | Cracks [58-61]; leakage [83]; voids [58,59,85-91] | Electromagnetic wave velocity; transmission and reflection on the interface | Internal status; qualitative                            | 1) 2) 3) 4)    | Quick; Continuous; Good penetration; Relatively high resolution;                                           | 1) 2)             | Rely on data interpretation; Rely on the selection of antenna frequency and the design of the antenna;                                |
| Laser                    | Leakage [78,80- 82]                               | Laser intensity difference between leakage area and background              | Surface status; qualitative or quantitative             | 1) 2) 3)       | Quick; Accurate; No dependence on visible light illumination;                                              | 1) 2) 3)          | More complex data processing; Easy to be affected by tunnel appendages; High cost;                                                    |

| Acoustic techniques   | Cracks [62-69]; voids [94-98]            | Transmission, reflection, refraction and diffraction of sonic/ultrasonic wave   | Internal status; qualitative or quantitative   | 1) 2)    | Low cost; Tomography possible;                                        | 1) 2) 3) 4)   | Relatively slow; Low penetration depth; Rely on data interpretation; Mostly require good coupling;   |
|-----------------------|------------------------------------------|---------------------------------------------------------------------------------|------------------------------------------------|----------|-----------------------------------------------------------------------|---------------|------------------------------------------------------------------------------------------------------|
| Electrical tomography | Cracks [70,71]; leakage [84]; voids [70] | Electrical impedance distribution                                               | Internal status; qualitative                   | 1) 2) 3) | Low cost; Good real-time performance; Visualization;                  | 1) 2) 3)      | Low penetration depth; Relatively low resolution; Rely on data interpretation;                       |
| Radiography           | Voids [102]                              | Attenuation of rays in concrete                                                 | Internal status; Qualitative                   | 1) 2) 3) | Extremely strong penetration ability; High resolution; Visualization; | 1) 2) 3)      | High cost; Radiation hazard; Radioactive source required;                                            |

1

## 3. Evaluation methods of tunnel lining 2

- Existing tunnels may suffer from a variety of problems over time [103]. These issues may 3
- impair  the  service  of  tunnels  and  cause  deterioration  in  the  performance  of  structures  [104]. 4
- Therefore, it is necessary to assess the serviceability conditions of the tunnel linings. Based on the 5
- results obtained by NDT methods for tunnel lining defects, structural health evaluation of the tunnel 6
- is followed. This section provides an overview of typical evaluation methods and summarizes the 7
- future research that needs to be addressed. 8
- The evaluation process of tunnels is illustrated in Fig. 25. The overall condition of the tunnel 9
- can  be  evaluated  by  considering  its  different  subunits.  Based  on  detection  data  and  evaluation 10
- methods of each subunit, evaluation results can be obtained against evaluation criteria. Routine 11
- maintenance or retrofitting in the future will depend on the final evaluation result. 12
- With the increase of tunnels, the Federal Highway Administration published a manual [105] 13
- that provided useful guidance on the evaluation of operating tunnels to assess aged railway tunnel 14
- linings. Park et al. [44] investigated the evaluation of tunnel defects. Although the evaluation criteria 15
- were based on expert opinion and experience, the evaluation results in their research were objective 16
- because quantitative evaluation methods were used. To reduce the subjectivity in tunnel evaluation, 17
- scientific and rational methods for evaluating the condition of tunnel linings are essential [106]. 18
- Meanwhile, mathematical models and artificial intelligence techniques are gradually developed or 19

introduced to evaluate the condition of tunnels more accurately. Thus, existing evaluation methods 1 can  be  categorized  into  three  types,  including  normative  assessment  method,  evaluation  using 2 mathematical models, and evaluation using artificial intelligence technology. 3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

Fig. 25. Diagram of the evaluation process.

<!-- image -->

Flow chart

## 3.1 Normative assessment method

The  normative  assessment  method  is  primarily  based  on  the  relevant  specifications.  This assessment method takes a wide range of factors into account and a rapid evaluation can be achieved. The normative assessment method can directly and quickly assess the overall condition of a tunnel, as well as the assessment of localised tunnel defects. For example, the general technical situations of road tunnels can be assessed in accordance with the Technical Specifications of Retrofitting for Highway Tunnel [107]. Through this method, the civil structure can be assessed from three aspects: the  electrical  and  mechanical  facilities,  the  civil  engineering  facilities,  and  other  engineering facilities. The level-by-level evaluation of the normative assessment method is summarized in Fig. 26 . The assessment of the civil structure of the tunnel usually starts with a technical condition score according to the following equation:

<!-- formula-not-decoded -->

- where   is  the  weight,   is  the  condition  value  of  the  subunit  and is  the  overall 1

 

    

    

- condition value. Then the civil engineering structures will be categorized according to Table 2 and 2
- Table 3 . In addition, the specification provides separate assessment methods for localised tunnel 3
- defects such as cracks and leakage, with the assessment condition values defined in Table 4 . The 4
- extent of defects can be quantified by condition values in Table 5 and Table 6 . 5

6

<!-- image -->

Flow chart

7

8

9

10

11

12

13

14

15

Fig. 26. Diagram of the level-by-level evaluation in the normative assessment method.

Table 2 Threshold values for the classification of the technical condition of civil structures [107]

| Technical condition rating   | Classification of the technical condition of civil structure   | Classification of the technical condition of civil structure   | Classification of the technical condition of civil structure   | Classification of the technical condition of civil structure   | Classification of the technical condition of civil structure   |
|------------------------------|----------------------------------------------------------------|----------------------------------------------------------------|----------------------------------------------------------------|----------------------------------------------------------------|----------------------------------------------------------------|
|                              | Category 1                                                     | Category 2                                                     | Category 3                                                     | Category 4                                                     | Category 5                                                     |
| JGCI                         | ≥ 85                                                           | ≥ 70 ，＜ 85                                                     | ≥ 55 ，＜ 70                                                     | ≥ 40 ，＜ 55                                                     | ＜ 40                                                           |

Table 3 Classifications of the overall technical status of highway tunnels [107]

| Technical condition rating   | Rating category description   | Rating category description   |
|------------------------------|-------------------------------|-------------------------------|
| category                     | Civil structure               | Electromechanical facilities  |
| Category 1                   | Intact condition              | High integrity rate           |
| Category 2                   | Minor breakage                | Normal integrity rate         |
| Category 3                   | Moderate breakage             | Still operational             |
| Category 4                   | Severe breakage               | Low integrity rate            |
| Category 5                   | Dangerous condition           | --                            |

2

3

4

5

6

Table 4 Definition of condition values [107]

| Condition value   | Evaluation factors      | Evaluation factors   | Evaluation factors                             |
|-------------------|-------------------------|----------------------|------------------------------------------------|
| Condition value   | Degree of defect        | Development trends   | Impact on traffic safety and structural safety |
| 0                 | None or extremely minor | None                 | No impact                                      |
| 1                 | Minor                   | Stable               | No impact yet                                  |
| 2                 | Moderate                | Slow                 | Will impact                                    |
| 3                 | Severe                  | Quick                | Already impacts                                |
| 4                 | Dangerous               | Rapid                | Severe impacts                                 |

Table 5 Evaluation criteria for crack [107]

| Structure   | Crack width b （ b ＞ 3   | mm ） b ≤ 3   | Crack length l （   | m ） l ≤ 5   | Condition value   |
|-------------|-------------------------|--------------|--------------------|-------------|-------------------|
| Structure   |                         |              | l ＞ 5              |             |                   |
| Lining      | √                       |              | √                  |             | 3/4               |
| Lining      | √                       |              |                    | √           | 2/3               |
| Lining      |                         | √            | √                  |             | 2                 |
| Lining      |                         | √            |                    | √           | 2                 |

Table 6 Evaluation criteria for water leakage [107]

| Structure   | Major abnormal conditions   | Degree of leakage   | Degree of leakage   | Degree of leakage   | Degree of leakage   | Whether it affects traffic   | Whether it affects traffic   | Condition value   |
|-------------|-----------------------------|---------------------|---------------------|---------------------|---------------------|------------------------------|------------------------------|-------------------|
| Structure   | Major abnormal conditions   | Ⅰ                   | Ⅱ                   | Ⅲ                   | Ⅳ                   | Yes                          | No                           | Condition value   |
|             |                             | √                   |                     |                     |                     | √                            |                              | 4                 |
|             | Water                       |                     | √                   |                     |                     | √                            |                              | 3                 |
|             | Arch leakage                |                     |                     | √                   |                     | √                            |                              | 2                 |
|             |                             |                     |                     |                     | √                   |                              | √                            | 1                 |
|             | Hanging                     |                     |                     |                     |                     | √                            |                              | 3                 |
|             | ice                         |                     |                     |                     |                     |                              | √                            | 1                 |
|             |                             | √                   |                     |                     |                     | √                            |                              | 3                 |
|             | Water                       |                     | √                   | √                   |                     | √                            |                              | 2                 |
|             | Side leakage                |                     |                     |                     | √                   | √                            | √                            | 2                 |
|             | walls                       |                     |                     |                     |                     | √                            |                              | 1                 |
|             | Hanging                     |                     |                     |                     |                     |                              |                              | 3                 |
|             | ice Sandy                   |                     |                     |                     |                     |                              | √                            | 1                 |
|             | outflow                     |                     |                     |                     |                     | √                            | √                            | 3/4 1             |
|             | Road Ponding                |                     |                     |                     |                     | √                            |                              | 3/4               |
|             | surface                     |                     |                     |                     |                     |                              | √                            | 1                 |
|             | Freezing                    |                     |                     |                     |                     | √                            |                              | 3/4               |
|             |                             |                     |                     |                     |                     |                              | √                            | 1                 |

It is also possible to assess the condition of the tunnel using thresholds for tunnel defects or 1 deformations  in  some  specifications,  such  as  the  threshold  values  for  tunnel  wall  convergence 2 recommended in the Standard for Design of Metro [108] and the allowable value for crack widths 3 recommended  in  the  Standard  for  Design  of  Shield  Tunnel  Engineering  [109].  However,  the 4 inconsistent grading of different defects in the specifications results in the normative assessment 5 method  relying  significantly  on  the  experience  of  the  experts  [26]. To  avoid  mistakes  in  the 6 evaluation results due to human subjectivity, the normative assessment method can be combined 7 with the NDT techniques. For example, Lai et al. [28] applied crack width monitoring technology, 8 concrete  strength  monitoring  technology,  and  electromagnetic  wave  nondestructive  monitoring 9 technology for the evaluation of the overall condition of the tunnel. The detection data obtained 10 from  NDT  techniques,  rather  than  expert  ratings,  make  the  evaluation  results  more  objective. 11 However, incorporating these techniques inevitably increases the cost of the evaluation. 12

13

14

15

16

17

18

19

20

21

22

23

24

where   is the area of concrete, n is the number of branches of the crack,   ( ) is the length of the 25 k th crack,   ( ) is the width of the k th crack,     ( ) is the angle between the normal vector of the k th 26 crack and the i -axis,     ( ) is the angle between the normal vector of the k th crack and the j -axis,   27

## 3.2 Evaluation using mathematical models

Mathematical models can be used to evaluate the health condition of the tunnel [26]. Different detection data, such as sensor readings or imaging data, can be transformed by mathematical models into usable data that can be used to derive evaluation results. Crack is one of the most common defects in existing tunnels [2]. As aforementioned, cracks can easily be detected by NDT methods. As a result, some researchers have chosen to use cracks as a primary indicator when assessing the condition of tunnel linings. Shigeta et al. [110] attempted to quantitatively assess the condition of the tunnel lining by collecting crack information from available tunnels. They proposed a Tunnel lining  Crack  Index  (TCI)  that  took  into  account  the  size  and  distribution  of  the  cracks.  The conceptual diagram of TCI is shown in Fig. 27 . TCI can be calculated based on the crack tensor theory using the following equation:

<!-- formula-not-decoded -->

is a factor related to the width of the crack,   is a factor related to the length of the crack. This 1 evaluation method has been widely used [25]. However, this method did not take into account the 2 complexities that arise when cracks intersected with each other and therefore had limitations [25]. 3 At the same time, the uncertainty in the relationship between TCI and the instability of tunnel lining 4 indicated that this method needs further investigation [29]. 5

6

7

8

9

10

11

12

13

14

15

16

A schematic diagram of the calculation is shown in Fig. 28 . The evaluation results were validated 17 by TCI. The correlation between the fractal dimension D and the TCI is shown in Fig. 29 . The fractal 18 dimension  took  into  account  the  density,  width,  and  distribution  of  the  cracks.  Therefore,  this 19

Fig. 27. The conceptual diagram of TCI [29] .

<!-- image -->

Engineering drawing

The fractal theory could be used to describe the propagation of cracks and the fractal dimension was very effective in characterizing the degree of damage and fragmentation [111,112]. Jiang et al. [25] proposed a Box-Counting method for assessing the health condition of tunnel linings based on fractal dimension theory. The local surface of the lining with cracks was assumed to be an expansion plane in this method. The plane could be divided into equally spaced grids of scale r and the number of  grids  occupied  by  the  cracks  in  the  plane  was N(r) . Then the  fractal  dimension D could  be obtained by the following equation:

<!-- formula-not-decoded -->

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

method was theoretically more reasonable than TCI. However, the fractal dimension possessed the same disadvantages as the TCI evaluation method, such as the high cost of the evaluation process and the inadequacy of the evaluation indicators.

Fig. 28. Schematic diagram of the Box-Counting method. (a) Crack image; (b)   =  ,  ( ) =    ; (c)   =  ,  ( ) =    ; (d)   =  ,  ( ) =    [25] .

<!-- image -->

Line chart

Fig. 29. Correlation between fractal dimension and TCI [25] .

Yuan et al. [113] proposed a comprehensive evaluation framework for tunnels based on the principle of limit state design, in which limit state functions were used. The methodology classified the service state of the tunnel into five levels ( Fig. 30 ). Based on the measured data, a limit state function  was  used  to  determine  the  level  of  service  state  of  the  component.  The  evaluation framework started from the structural components to the individual lining rings, and finally to the overall condition of the tunnel. Fig. 31 shows the assessment framework. Li et al. [26] investigated a  similar  classification  for  the  service  state  of  the  tunnel  but  proposed  a  different mathematical model called the tunnel serviceability index (TSI) formula. The TSI formula is as follows: 1     =            +               +          +        +        +        +                       (6) 2

where       ,            ,       ,     ,     and     are  measurable  variables,       is  the  average 3 relative settlement,            is the average differential settlement,       is the average 4 convergence ratio,     is the total water leakage area,     is the total cracking length and     is the 5 total  spalling  area.     ,     ,     ,     ,     ,     and   are  coefficients  estimated  by  partial  least 6 squares regression and linear transformation. 7

Further research on the TSI was conducted by Lin et al. [114], who compared the assessment 8 results  of  the  TSI  formula  with  those  obtained  from  the  normative  assessment  method.  Their 9 research showed that the TSI method was more conservative. Additionally, Andreotti et al. [115] 10 proposed a cyclic model for longitudinal joints that considers the effect of cyclic loads, and Lin et 11 al. [106] proposed a tunnel structural toughness model that considers multiple disturbances. It was 12 shown that such models could accurately assess the condition of tunnels in earthquake-prone areas. 13 In general, the application of mathematical theory to the condition evaluation of tunnel linings 14 can lead to more accurate results, but high-quality data from the detection methods are required to 15 improve the quality of evaluation results. 16

<!-- image -->

Line chart

Fig. 30. Evolution in service state [113] .

17

18

19

1

2

3

4

5

Fig. 31. Flowchart in assessment [113] .

<!-- image -->

Flow chart

## 3.3 Evaluation using artificial intelligence technology

With the development of artificial intelligence technology, some researchers started to apply it

- to the assessment of tunnel conditions. Zhang et al. [116] proposed a dynamic evaluation method 6
- for  tunnel  performance  in  which  Knowledge  Graph  was  used  to  integrate  data. Although  the 7
- dynamic evaluation model based on Knowledge Graphs was a new evaluation method, it was still 8
- based on the static expert rating method. Zhu et al. [30] proposed a new assessment method via 9
- cloud model-based random forests (CRFs), with the evaluation workflow shown in Fig. 32 . The 10
- method included supervised and semi-supervised machine learning algorithms. The two algorithms 11
- could effectively deal with inconsistent data and limited data respectively. The evaluation method 12
- could be further improved with the incorporation of more accurate and numerous data. In addition, 13
- Rafiei and Adeli [117] proposed an unsupervised learning model for the condition assessment of 14
- large infrastructure systems, which involved machine learning techniques. These approaches can be 15
- a valuable reference for tunnel condition assessment. With the development of automatic detection 16
- technologies as demonstrated in Section 2 , it is becoming easier to quickly obtain data to evaluate 17
- the condition of tunnel linings [118-120]. Artificial intelligence technology has advantages in data 18
- processing. The use of artificial intelligence technology in the condition evaluation of tunnel linings 19

can lead to improved efficiency and accuracy [24]. However, it is difficult to develop a sufficiently 1 large dataset to cover all real-case states of the tunnels during ageing and deterioration, as well as 2 to obtain accurate labels of all the samples in the datasets. 3

4

<!-- image -->

Flow chart

5

6

7

8

Fig. 32. Schematic illustration of the cloud model-based random forests [30] .

## 3.4 Methodology comparisons and perspectives

The normative assessment method evaluates the tunnels in a relatively comprehensive way as

- it takes into account not only the structural performance but also other facilities in the tunnels [107]. 9
- The method also allows for rapid assessment, which is essential in the case of an unexpected event. 10
- However, the method requires the involvement of experts in the assessment. That means the results 11
- obtained  from  the  normative  assessment  method  depend  on  the  experts'  experience,  which  is 12
- inevitably more subjective. When evaluating the condition of tunnel linings, mathematical models 13
- can be applied to different types of damage, but they ignore the correlation between different defects 14
- [26]. Artificial intelligence technology has excellent potential in structural condition evaluation, 15
- especially for data processing and evaluation with the inputs of multiple detection methods. Such 16

17

- evaluation methods usually do not require supervision, especially deep-learning methods, because

18

- they extract the features/information automatically [24]. However,  establishing large and
- comprehensive datasets with accurate labels is still challenging. 19
- In addition to the above three evaluation methods, evaluation can also be conducted based on 20
- numerical simulation software [121] and expert rating methods [26]. A summary of these different 21

- evaluation methods is shown in Table 7 . 1

2

## Table 7 A summary of the different evaluation methods 3

| Evaluation methods                            | Characteristics                  | Advantages                                                                     | Disadvantages                                                                                          |
|-----------------------------------------------|----------------------------------|--------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------|
| Normative assessment method [107-109]         | Qualitative or semi-quantitative | 1) Quick; 2) Economical; 3) high practicality;                                 | 1) Accuracy needs to be improved; 2) Generally relying on experts' experience;                         |
| Mathematical models [25,26,113,115]           | Quantitative                     | Multiple types of indicators can be considered with a high degree of accuracy. | 1) High requirements for evaluation criteria; 2) Complex process of model development and calculation; |
| Artificial Intelligence Technology [30,117]   | Quantitative                     | 1) High precision; 2) Quick;                                                   | 1) Requires sufficient samples; 2) Algorithm changes can lead to biased results;                       |
| Finite element numerical simulation [121-124] | Quantitative                     | 1) Low cost; 2) Good repeatability;                                            | Accuracy in complex environments needs to be improved.                                                 |
| Expert rating methods [31]                    | Qualitative or semi-quantitative | 1) Quick; 2) High practicality;                                                | Evaluation results are subjective.                                                                     |

4

- Future research on tunnel condition evaluation may focus on the following three aspects: 1) 5
- Refine the indicators/models to take into account more components and the correlation between 6
- different  components/defects.  2)  Develop  real-time  assessment  methodology  to  satisfy  mobile 7
- tunnel inspection, and implement assessment while detecting. 3) Build sufficiently large datasets 8
- with  accurate  reference  labels  of  tunnel  states  to  take  full  advantage  of  artificial  intelligence 9
- technology. 10

11

## 4. Tunnel lining retrofitting methods 12

- The  previous  sections summarize  the  types of shield tunnel lining defects and  the 13

corresponding detection and evaluation methods. For various defects, different retrofitting methods 1 can be adopted according to their effects on the performance and safety of the lining. Lining defects 2 that  will  not  affect  the  ultimate  capacity  and  safety  performance  of  the  liner  only  need  normal 3 retrofitting, such as surface damage with inlay repairs [31], as shown in Fig. 33 . Defects that may 4 pose a significant risk to the structural functions of the tunnel require structural modifications of the 5 lining, and this is the focus in this section. For tunnels in service, retrofitting methods can generally 6 be divided into two categories: internal surface retrofitting and grouting retrofitting, depending on 7 the positions of retrofitting operations [9,125]. Therefore, this section will conduct a review on these 8 retrofitting  methods  based  on  the  classification  of  the  inner  surface  retrofitting  method  and  the 9 grouting retrofitting method. 10

11

<!-- image -->

Engineering drawing

12

13

14

15

16

17

18

19

20

21

22

23

Fig. 33. Inlay repairs: (a) adhesives and (b) coating.

## 4.1 Internal surface retrofitting

The mechanism for internal surface retrofitting is typically described as reinforcing the tunnel structures  from  the  lining's  inner  wall.  Depending  on  the  retrofitting  material,  the  conventional internal tunnel retrofitting methods often include bonded steel plates, cover-arch reinforcing, and bonded Fiber-Reinforced Plastic (FRP) [32].

## 4.1.1 Bonded steel plate method

The method using bonded steel plates for tunnel retrofitting was demonstrated by Kiriyama et al. in 2005 [126]. The method works by bonding the steel plates to the defective shield segments using epoxy, which could improve the stiffness and ultimate load carrying capacity of the tunnel structures [127], as shown in Fig. 34 . Thus, the construction procedures were divided into two stages:

steel plate fixation and epoxy resin infusion. The steel plates were attached along the segmental 1 circumferential midline and then joined together using electric welding. Plug bolts were used to 2 connect the steel plate and the adjacent concrete segment, and finally, epoxy was infused between 3 the two materials. The operations of the bonded steel plates could usually be mechanized, so the 4 construction was quick and efficient [128]. Depending on the area of the bonded steel plate, the 5 method was furtherly classified into full-ring and half-ring steel plate reinforcing methods, as shown 6 in Fig. 35 [129]. 7

8

9

10

11

12

13

14

15

16

17

Fig. 34. Bonded steel plate method [127] .

<!-- image -->

Engineering drawing

Fig. 35. Shield tunnel reinforced by steel plate: (a) cross-section; (b) longitudinal section [129] .

Many researchers  have  investigated  the  effectiveness  of  the  bonded  steel  plate  retrofitting method. Chang et al. [130] analyzed the cause of large-scale lateral deformation in shield tunnels and found that the application of the bonded steel plate method could effectively increase tunnel stiffness,  even  though  the deformation was large. To evaluate the load-bearing capacity and the deformation pattern of the reinforced segments, Liu et al. [129] and Bi et al. [131] conducted full1 scale experiments on reinforcing shield tunnels using full and semi-ring inner tensioned steel plates. 2 The results showed that the internal bonded steel method significantly improved the overall stiffness 3 and load-bearing capacity of the shield tunnels. The full-ring strengthening method was found to be 4 more effective than the semi-ring strengthening method. However, the tunnel failure mechanism 5 was  not  provided  in  these  studies.  Additionally,  the  impact  of  existing  deformation  on  the 6 performance of post-reinforced linings was not analyzed. Zhai et al. [132] conducted model tests to 7 assess the influence of various levels of deformation on the performance of steel plate reinforced 8 tunnel linings. However, the physical model was simplified and did not accurately represent the 9 actual prototype. Liu et al. [133] demonstrated the efficacy of steel plate retrofitting through model 10 tests  on  pipe  linings  with  and  without  retrofitting.  Nevertheless,  the  quantitative  damage  to  the 11 bonding surface and segmental joints has not been thoroughly investigated. 12

13

14

15

16

17

18

19

20

21

22

23

24

25

To  investigate  the  structural  performance  and  damage  mechanism  of  shield  tunnel  lining reinforced with steel plates, Liu et al. [134] established a three-dimensional finite element model based on the structural test of tube lining, reinforced with inner bonded steel rings. Through the finite element analysis and parametric study, the mechanical  properties, the deformation characteristics, and the failure modes of tunnel lining reinforced with adhesive steel were discussed. The results  demonstrated  that  the  direct cause  of  the  damage  to  the  lining  structure  after  being reinforced with steel plates was the failure of the epoxy resin bond between the steel plates and the lining. It presented a clear brittle behaviour, and conventional deformation monitoring was unable to provide early warnings. Furthermore, several new retrofitting methods for steel members have been  proposed  by  researchers,  including  bonded  corrugated  steel  [135]  and  bonded  steel  pipe concrete [136]. However, it has been observed the strengthened linings were all damaged at the interface, which significantly reduces the retrofitting effectiveness and efficiency. Therefore, it is important to investigate the bonded condition between the steel plates and the liner.

26

27

28

29

However, the limitations of testing techniques make it challenging to accurately analyze the details  of  the  prototype  during  physical  testing  of  the  model  and  observe  the  detailed  damage phenomena [137]. Numerical simulations have significant advantages over physical tests when it comes  to  studying  detailed  damage  characteristics  of  structures.  These  simulations  offer  good

- repeatability and analytical capabilities [138]. When simulating the mechanical behavior of steel 1
- plate reinforced segment liners, it is crucial to reasonably model the damage behavior at the bonding 2
- surface between the steel plate and the segment liner [139]. Sun et al. [140] utilized cohesive contact 3
- to model the bonding behavior in ABAQUS. The steel plate reinforcement was also incorporated 4
- by  adjusting  its  modulus  of  elasticity  from  a  low  value  to  a  realistic  value.  The  mechanical 5
- performance of the cohesive unit was defined using a damage evolution model based on the traction6
- separation response [141], as depicted in Fig. 36 . 7

8

9

10

11

12

13

14

15

16

17

18

19

- where   ,    and    are  interfacial  stress  data  in  different  directions,   ,    and    are 20

Fig. 36. A model for bond damage evolution based on traction separation response [139] .

<!-- image -->

Engineering drawing

The definition of the parameters in the figure is shown below:   is interfacial stress;   peak is bonding  strength;   is  the  relative  displacement  between  steel  plate  and  lining;     is  relative displacement  value;       is  final  relative  displacement;   is  interface  stiffness;     is  the interfacial fracture energy, which is obtained from the following Eq. (7) based on the B-K criterion [142,143].

The mechanical behavior of cohesive elements is divided into three phases.

1) Well-bonded stage. and remain linear, as shown in Eq. (8) . No bond damage occurs.

 

 

 

<!-- formula-not-decoded -->

- relative  displacement data in different directions,     ,     ,       ,       and       are  the 21 stiffness matrices of the interface. 22
- 2) Bond damage phase. Once the interfacial stress value exceeds peak , bond damage occurs, 23

<!-- formula-not-decoded -->

 

 

 

 

 

- as reflected by the decrease in interfacial stress with the development of relative displacement. 24

 

1

3) Bond failure phase. Once the relative displacement value exceeds ult .

Based on the theory above, Liu et al. [144] developed an analytical solution for predicting 2 interfacial stresses. On this basis, they investigated how the elastic modulus, the thickness of the 3 adhesive  layer,  and  the  thin  plate  affected  the  quality  of  the  inner  surface  bonded  steel  plate 4 reinforcing. However, their study did not take into account the impact of damage to the front section 5 of the reinforcement on the bonding behavior. To address this, Li et al. [139] proposed FEM to 6 accurately simulate the bonding behavior between steel plates and the lining and validated it through 7 detailed physical model tests on tunnels reinforced with steel plates. A series of FEM simulations 8 were conducted for tunnels reinforced under various levels of deformation. The study analyzed the 9 effect of existing structural deformation on the detailed damage mechanisms of the post-reinforced 10 lining under increasing external loads, including the progression of bond damage and the opening 11 and bending stiffness of the joints. 12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

29

30

 

To enhance the bond at the interface, Ren et al. [145] used a large number of chemical anchor bolts  instead  of  structural  adhesive  to  connect  the  lining  to  the  corrugated  steel.  Despite  some slippage at the bonded interface, the shear capacity from the chemical anchor bolts allowed for the deformation and integration of the structure components, resulting in a final increase in the ultimate load-carrying  capacity  by  163%  to  201%.  However,  because  of  the  presence  of  gaps  in  the retrofitting  interface,  the  method  is  ineffective  in  improving  the  waterproof  performance  of  the tunnel compared to structural adhesive bonding. Liu et al. [146] employed fiber-reinforced concrete as an adhesive material to connect the lining to the retrofitting layer using the bonding effect of cement-based  materials,  which  has  the  advantage  of  a  fire-resistance  and  high-temperature resistance. However, the method was restricted to the tensioned region because of the characteristics of the fiber. Therefore, more research is needed to improve the adhesive capacity of the reinforced layer to the lining.

The use of the bonded steel plate method can significantly enhance the overall strength and

rigidity  of  the  lining,  effectively  mitigating  tunnel  deformation  and  resolving  cracking  issues. Additionally, the construction process is straightforward and convenient. However, some challenges need to be addressed [127]:

(1) Higher cost of steel plates and bonding materials.

(2) Increased self-weight of the structure: The addition of steel plates to the structure will add

- extra weight, which may affect its stability and safety, especially in the case of overloading 1 or extreme weather conditions. 2

3

4

5

- (3) Additional anchoring measures: To ensure effective bonding between the steel plates and the strengthened elements, a large number of anchoring measures may be required. This can cause secondary damage to the linings and weaken their overall strength.

6

7

- 8
- (4) A lack of efficient bonding materials: The choice of bonding materials is critical to the success  of  the  retrofitting  method.  The  lack  of  efficient  bonding  materials  that  can withstand high loads and stress can reduce the effectiveness of the retrofitting process.
- 4.1.2 Cover-arch reinforcing 9
- The cover-arch method improves the load-bearing capability of the linings by increasing the 10
- cross-sectional areas of the structure [147], as shown in Fig. 37 . This is achieved by replacing the 11
- damaged lining with a concrete structure that is integrated with the original structure. Depending on 12
- the cover-arch method can be divided into stacked and separated [148]. The stacked arch involves 13
- completely  integrating  the  arch  with  the  original  lining,  while  the  separated  arch  includes  a 14
- waterproof layer set between the arch and the original lining [149]. 15

16

17

18

19

20

To  investigate the effectiveness of stacked  arches  reinforcing, Hakoishi  et  al.  [150] experimentally analyzed the deformation process, investigated the failure modes, and measured the

- ultimate load-carrying capacity of the lining structure after reinforcing the arches in a semi-circular 21
- manner, and they observed an increase of the ultimate load-carrying capacity of the lining. However, 22
- because the experiment was completely unloaded before reinforcing, it differed considerably from 23

Fig. 37. Cover-arch reinforcing [33] .

<!-- image -->

Engineering drawing

the  actual  forces  of  the  lined  arch  reinforced  with  cracks.  Liu  et  al.  [151,152]  used  structural 1 experiments, finite element analysis, and field tests to examine the structural behavior and ultimate 2 capacity of the lining reinforced by the stacked arch. They verified the effectiveness of the stacked 3 arch reinforcement and investigated the structural behavior of stacked arch reinforcement in various 4 cases. A method for calculating the internal force and stiffness of the stacked arch was proposed for 5 better applications. 6

7

8

9

10

11

12

13

Compared to the stacked arch, the separated arch requires an additional drainage system. It is more complex to construct and less efficient to improve the stiffness and load-bearing capacity of the lining but is particularly suitable for strengthening and reinforcing the lining sections with water leakage problems [153]. Yu and Sang [149] used the 'load-structure method' to test the secondary lining structure with a single prefabricated longitudinal crack reinforced by the separated arch and analyzed the mechanical properties, damage modes, and ultimate bearing capacity of the reinforced lining structures. The results proved that the separated arch was very effective for tunnel retrofitting.

14

15

16

17

18

19

20

21

22

23

24

There are also many applications of the cover-arch reinforcement methods, such as the Bayi Tunnel in Chongqing [154], and the method could achieve better reinforcement and guarantee the stability of the tunnel operation. However, the process for the cover-arch method can be complicated and can seriously disrupt traffic. Additionally, the arch structure is typically made of concrete, which is  thick  and  has  a  significant  impact  on  the  tunnel  lining  construction. Therefore,  the  range  of applications of the cover-arch method is still restricted.

## 4.1.3 Bonded FRP method

Another popular method for reinforcing the inner surface of linings is the bonded FRP. FRP is characterized  by  high  strength,  durability,  and  ductility  [155].  The  mechanical  properties  and ductility of the damaged lining can be improved by pasting FRP to the lining with epoxy resin, and the lining will have greater load-carrying potential during the later stages of loading [156].

Many studies  have  been  conducted  to  investigate  the  feasibility  and  effectiveness  of  FRP 25 retrofitting. Wu and Cai [157] investigated the feasibility of fiber-reinforcing tunnels by monitoring 26 the stability of the surrounding rock after reinforcing cracks in the tunnel lining. Ai et al. [158] used 27 FRP to strengthen the tunnel lining and achieved their expected results, indicating that bonded FRP 28 in  the  early  deterioration  stage  could  reduce  retrofitting  costs. Yang  et  al.  [159]  used  the  finite 29

element method to investigate the retrofitting effect of FRP reinforced cracked lining. The results 1 revealed that when the FRP was bonded to the lining surface after the secondary lining cracked, the 2 expansion of tensile cracks could be effectively avoided. Furthermore, Jiang et al. [160] proposed 3 the so-called FRP-PCM method to strengthen degraded tunnel linings and simulated it numerically. 4 The construction procedure of the FRP-PCM method was shown in Fig. 38 [161]. The FRP-PCM 5 method was based on strengthening tunnel linings by FRP grids, embedded in PCM (one of Polymer 6 Cement Mortar). The study evaluated numerical models for various loosening pressures affecting 7 the  tunnel  lining,  taking  into  account  factors  such  as  the  foundation  grade,  extent  of  lining 8 degradation,  and  tunnel  condition.  Based  on  these  evaluations,  the  study  suggested  appropriate 9 conditions  for  implementing  the  FRP-PCM  method  to  effectively  reinforce  the  tunnel  linings. 10 However, it did not consider other unfavorable conditions beyond the loosening pressure. Han et al. 11 [125] examined the reinforcement behavior of the FRP-PCM method on tunnel linings, and they 12 observed that the plastic shear failure on the outer surface could be significantly suppressed and the 13 long-term failure rate of the tunnel lining could also be significantly reduced. Additionally, previous 14 studies all concentrated on enhancing the load-bearing capacity and stiffness of the lining through 15 FRP reinforcement. However, its impact on the cracking behavior of the tunnel lining has not been 16 explored yet. To address this, Liu et al. [162] examined the effect of FRP on controlling lining 17 cracking under inclined pressure using scale tests. They analyzed the mechanism of its action and 18 the influence of the number and arrangement of FRP grid layers on the reinforcement effect. The 19 results demonstrate that as the amount of FRP increases, the ultimate load carrying capacity and 20 structural stiffness of the tunnel lining increases significantly, while the ductility decreases. 21

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

Fig. 38. Application of the FRP-PCM method on tunnel linings: (a) surface treatment; (b) fix the FRP grids; (c) spay the PCM; (d) after the construction [161] .

<!-- image -->

Photograph

Many  researchers  have  also  studied  the  factors  that  affect  the  effectiveness  of  the  FRP retrofitting  method. Li  et  al.  [163]  used  numerical  simulations  to  investigate  the  reinforcing effectiveness of using different lengths and layers of fiber cloth in terms of reinforcement forces and lining damage. Liu and Zhang [164] used numerical simulations to investigate the effect of FRP on tunnel lateral deformation, and they thoroughly analyzed the influence of ground resistance, bonded time, and the number of FRP layers on the retrofitting effectiveness. Liu et al. [165] investigated the use  of  FRP  to  strengthen  longitudinal  joints  in  shield  tunnels  and  compared  the  structural performance  and  damage  morphology  of  reinforced  and  unreinforced  longitudinal  joints. Their research revealed the damage mechanism of FRP-reinforced joints and made an overall evaluation of the efficiency of retrofitting. The results demonstrated that the bonded FRP could improve the corner stiffness of reinforced joints, but the bonded surface of FRP was the weak point of the entire structure. The retrofitting effect was determined by the bonded strength and shear strength of the structural adhesive materials. They also observed that FRP could only be used for the temporary strengthening of longitudinal joints, but not for long-term strengthening.

Compared to the bonded steel method and the cover-arch method, the bonded fiber method has a local reinforcement effect, with simple machinery and construction procedures [155]. However, the FRP fabric has higher requirements for the reinforcing and construction environment, as epoxy is  vulnerable  to  high  temperatures  and  moisture.  The  retrofitting  effectiveness  of  bonded  fiber

- method  is  also  affected  by  existing  deformations,  with  larger  deformations  leading  to  weaker 1
- retrofitting effectiveness [166]. Moreover, due to the flexibility of the fiber, this retrofitting method 2
- is only suitable for the tensile zone, resulting in a local retrofitting effect that does not significantly 3
- improve the overall stiffness of the lining [167]. 4

## 4.2 Grouting retrofitting 5

Previous research has shown that the pressure variation in the surrounding earth or rock is a 6 major cause of damage to tunnel linings [168]. Therefore, in addition to the inner surface of the 7 lining strengthening, it is also important to control the deformation of the lining by grouting the 8 surrounding rock [169]. The reinforcing procedure of the tunnel grouting method is to inject the 9 grouting slurry into the surrounding rock by producing holes, relying on the grouting pressure to 10 spread the slurry into the fissures of the surrounding rock to form a reinforcement zone, as shown 11 in Fig. 39 . This improves the integrity and strength of the rock mass, which in turn reduces the 12 lateral deformation of the tunnel, and solves the problems such as water leakage through the tunnel 13 tubes, large differential settlement, and unstable tunnel deformations [170]. 14

15

<!-- image -->

Engineering drawing

16

17

Researchers  have  investigated  the  effectiveness  of  grouting  reinforcement  using  various 18 methods. The primary methods for investigating grouting retrofitting include field measurements 19 and numerical simulations. The process is usually represented by simulating the volume expansion 20 of predetermined elements that represent the grouted soil. The volume expansion can be achieved 21 through two methods: (1) applying internal pressure or (2) applying volume strain directly to the 22

Fig. 39. The grouting system and working procedure [170] .

unit [171]. Soga et al. [172] described the internal pressure method using the 3D finite difference 1 program FLAC3D. In this numerical procedure, target grids representing grout-treated zones and 2 the  total  volumetric  expansion  rate Δ      of  these  elements  should  be  defined  in  advance.  The 3 parameter Δ      serves as an indicator to judge the terminal of expansion: 4

5

where   inj denotes the volume of grout injected into the soil, and     denotes the initial volume of 6 the same treated soil body. At the beginning of this procedure, the volumetric strain increment Δ    7 of  the  target  element  is  zero.  In  each  iteration,  a  FISH  program  is  used  to  modify  the  stress 8 components     (  =  ,  ,  ) of target elements by adding a small internal pressure     to each of 9 them.  The Δ      increases  as  the  calculation  proceeds.  In  the  volumetric  strain  method,  a  pre10 determined strain is applied directly to the target elements. Based on the above theory, Xue et al. 11 [173]  tested  the  mechanical  strength  of  the  reinforced  tunnel  linings  with  cavities  and  weak 12 surrounding rocks strengthened using the grouting method. The results demonstrated that the use of 13 the slurry reinforcement led to a more uniform distribution of stress within the lining structure and 14 the surrounding rock. A significant improvement in the overall stability of the lining structure was 15 also  achieved.  Zhang  et  al.  [169]  used  lateral  convergence,  joint  opening,  and  grout-induced 16 dislocation changes as indicators to analyze the impact of grouting on the lateral deformation of 17 tunnels. The results demonstrated that grouting could successfully increase the lateral convergence 18 of the tunnel and decrease the joint opening. 19

<!-- formula-not-decoded -->

After determining the reinforcing effect of grouting, evaluating and improving its effectiveness 20 is also an important issue. The horizontal convergence of the tunnel is one of the most commonly 21 used performance indicators in practice for assessing the early effects of reinforcement [174-176]. 22 When using grouting to control convergence in large tunnels, the parameters used are critical to the 23 effectiveness of the treatment. These control parameters include the number of grouting rows, the 24 construction  sequence,  and  the  horizontal  distance  between  the  grouting  rows  and  the  tunnel 25 dimensions, as shown in Fig. 40 [177]. To provide further confirmation of the relevant grouting 26 parameters, Zhang et al. [177] conducted a case study to analyze the effect of grouting on reducing 27 deformations in large tunnels. Recommendations for optimized grouting parameters were provided. 28 However, the study did not discuss the long-term effect of grouting on convergence reduction due 29

to the lack of field data for validation. Future work will be focused on the long-term effects of 1 grouting and the impact of soil swelling, in order to gain a deeper understanding of the effects of 2 grouting. 3

4

5

6

7

8

9

10

11

12

- 13

Fig. 40. Grouting parameters layout [177] .

<!-- image -->

Engineering drawing

Also, many grouting theories have been created, including the seepage grouting theory [178], the  fracture  grouting  theory  [179],  and  the  compaction  theory  [180].  These  theories  reveal  the variation  law  of  grouting  pressure,  grout  flow  rate,  diffusion  radius,  and  grouting  time  in  the grouting process and serve as guides for design and construction.

Some researchers have investigated the behavior of grouting materials. The two primary types of grouting used nowadays are cement slurry and chemical slurry. The inexpensive cement slurry provides excellent longevity, outstanding seepage resistance, and great strength after consolidation.

- However, due to inaccurate control issues and lack of strength, the utilization range of cement slurry 14
- is restricted [181]. The chemical slurry uses grouting materials such as polyurethane and epoxy resin 15

16

with a regulated setting time and good permeability for a variety of applications, although they are

- more expensive [182,183]. 17

18

19

Compared to the internal surface retrofitting methods, grouting can directly seal the fractures in the surrounding rock and fill the cavity to handle lining defects such as water leakage and cavities.

- It  can  also  improve  the  resistance  of  the  surrounding  rocks. As  the  surrounding  rock  pressure 20
- increases, it can effectively reduce the deformation of the lining structure, which can furtherly avoid 21
- the development of other defects. However, determining the ideal grouting volume and pressure is 22
- difficult due to the complexity of the grouting retrofitting process and the numerous influencing 23
- factors. Inappropriate grouting procedures and techniques may be less effective and speed up the 24

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

## progression of the defect [184].

## 4.3 Summary and outlook

In conclusion, a variety of retrofitting techniques have been developed, but these techniques and the reinforcing materials still need further investigation, as shown in Table 8 . Previous studies on reinforcement technology only provide a limited summary of the reinforcement methods used for specific tunnel projects, lacking a comprehensive overview of the development of reinforcement technologies.  Additionally,  there  is  a  lack  of  theoretical  analysis,  application  statement,  and comparison of these methods. With the above review, according to the latest developments and characteristics of the existing tunnel reinforcement methods, the authors believe that further research is needed in the following areas:

- (1) Although the majority of current research focuses on one technology, the combination of different tunnel retrofitting techniques to achieve the overall performance of structures is worth  investigating.  Further  investigation  into  the  coupling  mechanisms  of  various retrofitting technologies can be a good direction.
- (2) The most common failure mode observed for internal surface retrofitting of tunnel linings is interfacial damage. However, the majority of current studies assume that the adhesion between the retrofitting material and the lining is sufficient, thus ignoring the interface damage and failing to reflect the fractural situation. Further research is required on the interface failure mechanism and anchorage control mechanisms for liner internal surface retrofitting.
- (3) The  design  of  lining  retrofitting  is  still  based  on  experience  and  there  is  a  lack  of quantitative design methods. Further exploration is needed to understand the mechanisms and develop corresponding design standards for various retrofitting methods.

Table 8 Comparison of different retrofitting methods

| Retrofitting methods         | Defects solved   | Advantages   | Advantages                                    | Disadvantages   | Disadvantages                   |
|------------------------------|------------------|--------------|-----------------------------------------------|-----------------|---------------------------------|
| Bonded steel plate [126-146] | Deformation      | 1)           | Short construction period;                    | 1)              | Higher cost;                    |
| Bonded steel plate [126-146] | Cracks           | 2)           | Can address the                               | 2)              | Secondary damage to the lining; |
| Bonded steel plate [126-146] |                  |              | overall strength and stiffness of the lining; | 3)              | Fragile bonding interface;      |

| Cover-arch [147- 154]    | Deformation Cracks Leakage       | The most                                                  | effective method 1) 2) 3)        | Complex operation; Long construction period; Tunnel height restrictions;                                        |
|--------------------------|----------------------------------|-----------------------------------------------------------|----------------------------------|-----------------------------------------------------------------------------------------------------------------|
| Bonded FRP [125,155-167] | Deformation Cracks               | 1) Simple 2) Short period;                                | operation; construction 1) 2) 3) | Poor high-temperature resistance; Difficult to use in the wet environment; Only applicable to the tensile area; |
| Grouting [168- 184]      | Deformation Cracks Voids Leakage | Retrofitting of operating tunnels under micro disturbance | 1) 2)                            | Complex operation; May cause secondary damage to the tunnel;                                                    |

1

## 5. Conclusions 2

To ensure the structural safety and extend the service life of the tunnel linings, it is necessary 3 to conduct regular inspections on the structural health and maintenance of tunnels. Modern NDT 4 methods can provide detailed information on tunnel lining defects. The suitability of these methods 5 for representative defects (cracks, leakage, and voids) has been analyzed and summarized. Based 6 on the qualitative or quantitative data, a summary of the procedures for the assessment of tunnel 7 lining  health  states  is  also  provided.  Finally,  different  retrofitting  techniques  corresponding  to 8 various lining defects have also been reviewed. The following conclusions can be made: 9

10

11

12

13

14

15

16

17

18

19

(1)  NDT  methods  should  be  selected  based  on  specific  requirements,  such  as  fast  mobile detection or accurate in-place measurement, and according to the characteristics of the targeted defect. For crack detection, vision-based methods combined with image processing or deep learning are commonly used to obtain the crack information on the surface, while the depth of the crack can be measured by the GPR or acoustic techniques. Leakage can be detected from visible light images, thermal infrared images, and laser intensity images. And radar or sonic/ultrasonic techniques are the most preferred methods of detecting voids behind tunnel linings. On the inspection of the internal state  of  the  defects,  tomography  based  on  acoustic  and  electric  mechanisms,  among  others,  has proven  to  be  a  promising  visualization  method.  For  real-case  applications  with  complex  field conditions,  it  is  recommended  to  use  multiple  sensing  methods  to  conduct  a  comprehensive inspection of tunnel defects. However, attention should also be paid to the contradictory points 1 between different techniques, because they may have limitations in certain conditions or for certain 2 types of defects. In addition, the inconsistent results of different methods may arise from different 3 field conditions, detection resolution, data processing algorithms, measurement errors, and other 4 factors. Therefore, a reasonable fusion strategy of different methods should be developed first to 5 implement complementarity of them and provide accurate and comprehensive results. The future 6 trend of tunnel lining inspection is towards more intelligent and automated systems that integrate 7 multiple sensing techniques and NDT methods. In addition, there is a growing interest in the use of 8 unmanned detection vehicles and robots to perform more complex and dangerous inspection tasks. 9

10

11

12

13

14

15

16

17

18

19

20

(2) Due to the demands of practical applications, the condition evaluation methods of tunnel linings are gradually transferring from qualitative to quantitative analysis. Generally, the methods can be divided into normative assessment method, mathematical model-based evaluation method, and artificial intelligence-based evaluation method. The normative assessment method is relatively comprehensive,  although  the  accuracy  of  the  evaluation  results  could  be  improved  and  manual intervention  is  usually  inevitable.  Mathematical  model-based  evaluation  methods  are  accurate enough  for  a  single  indicator  but  cannot  handle  the  correlation  between  different  evaluation indicators. Artificial intelligence-based evaluation methods have great data processing capabilities and will provide good results if accurate and large databases are available before the evaluation. There is a trend to propose more effective indicators/models and combine the evaluation of tunnel linings with more advanced detection technologies. The condition evaluation of the tunnels will also

21

22

23

24

25

26

27

28

29

become more comprehensive, accurate, and real-time.

(3)  Retrofitting  methods  of  tunnel  lining  defects  can  be  divided  into  lining  inner  surface retrofitting and grouting retrofitting. The three main types of inner surface retrofitting methods are the bonded steel plate method, the cover-arch reinforcing, and the bonded FRP method. To improve the  retrofitting  effectiveness,  the  selected  retrofitting  methods  should  be  based  on  the  health condition, the mechanism of the defect, and the scope of application of the retrofitting method. To satisfy the increasing application demands, the next stage of research will focus on the physical mechanism, the coupling behaviors, and the design method of structural retrofitting.

Although after years of progress in these fields, there is still a gap between the performance of the conventional methods and the application requirements of practical tunnels. There are still some 1 challenges to overcome in the future. More research is needed, especially on the development of 2 integrated and intelligent inspection systems, comprehensive tunnel condition evaluation methods, 3 and effective proven reinforcement techniques with clearer mechanisms. Meanwhile, efforts are also 4 needed to establish effective cooperation mechanisms between detection, evaluation and retrofitting, 5 and finally to develop a comprehensive health monitoring and maintenance system for tunnel linings. 6

7

8

9

10

This paper is an up-to-date and comprehensive review that covers the entire framework of tunnel  lining  detection  and  retrofitting,  which  has  not  been  conducted  before.  It  can  provide systematic guidance and useful reference for understanding the state of the art of tunnel inspection, health evaluation, and retrofitting methods.

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

## Acknowledgement

The  authors  would  like  to  thank  the  financial  supports  from  the  National  Natural  Science Foundation  of  China  (NSFC)  (Grant  Number: 52208215),  the  Natural  Science  Foundation  of Zhejiang Province (Grant Number: LQ22E080008) and The Center for Balance Architecture of Zhejiang University.

## Author Contribution Statement

Yandan Jiang: Writing - review &amp; editing, Writing - original draft, Supervision. Lai Wang: Writing -  review  &amp;  editing,  Methodology,  Investigation.  Bo  Zhang:  Writing  -  review  &amp;  editing, Investigation.  Xiaowei  Dai:  Writing  -  review  &amp;  editing,  Investigation.  Bochao  Sun:  Writing  - review &amp; editing, Investigation. Nianwu Liu: Writing - review &amp; editing. Zhen Wang: Writing - review &amp;  editing. Jun  Ye:  Writing -  review &amp;  editing, Supervision,  Resources, Project Administration, Funding Acquisition, Conceptualization. Yang Zhao: Writing - review &amp; editing, Resources, Project Administration, Funding Acquisition

## References 1

- [1] H.M. Lyu, S.L. Shen, A. Zhou, Z.Y. Yin, Assessment of safety status of shield tunnelling 2

3

using  operational  parameters  with  enhanced  SPA,  Tunnelling  and  Underground  Space

- Technology. 123 (2022) 104428. https://doi.org/10.1016/j.tust.2022.104428. 4
- [2] D. Liu, F. Zhong, H. Huang, J. Zuo, Y. Xue, D. Zhang, Present status and development trend 5
- of diagnosis and treatment of tunnel lining diseases, China Journal of Highway and Transport. 6
- 34 (11) (2021), pp. 178-199 (in Chinese). https://doi.org/10.19721/j.cnki.10017 7372.2021.11.015. 8
- [3] D.  Zhao,  X. Tan,  L.  Jia,  Study  on  investigation  and  analysis  of  existing  railway  tunnel 9 diseases, Applied Mechanics and Materials. 580-583 (2014), pp. 1218-1222. 10
- https://doi.org/10.4028/www.scientific.net/AMM.580-583.1218. 11
- [4] H. Huang, L. Chen, Risk analysis of building structure due to shield tunneling in urban area, 12
- Underground Construction and Ground Movement. (2006), pp. 150-157. 13
- https://doi.org/10.1061/40867(199)17. 14
- [5] ITA-AITES,  Tunnel  Market  Survey  2019.  https://mtry.fi/tunnel-market-survey-2019-ita15

16

17

[6]

aites (Last accessed in February 17th, 2023).

Y. Zhao, P. Li, A statistical analysis of China's traffic tunnel development data, Engineering.

- 4 (1) (2018), pp. 3-5. https://doi.org/10.1016/j.eng.2017.12.011. 18
- [7] H. Mashimo, T. Ishimura, State of the art and future prospect of maintenance and operation 19
- of road tunnel, in: ISARC. Proceedings of the 23rd International Symposium on Automation 20
- and Robotics in Construction, IAARC Publications, 2006, pp. 299-302. 21
- https://doi.org/10.22260/isarc2006/0057 (ISBN 9784990271718). 22
- [8] W. Liu, X. Wu, L. Zhang, Y. Wang, J. Teng, Sensitivity analysis of structural health risk in 23
- operational tunnels, Automation in Construction. 94 (2018), pp. 135-153. 24 https://doi.org/10.1016/j.autcon.2018.06.008. 25
- [9] Z. Huang, H. Fu, W. Chen, J. Zhang, H. Huang, Damage detection and quantitative analysis 26
- of shield tunnel structure,  Automation in Construction. 94 (2018), pp. 303-316. 27
- https://doi.org/10.1016/j.autcon.2018.07.006. 28
- [10] L. Attard, C.J. Debono, G. Valentino, M. Di Castro, Tunnel inspection using 29
- photogrammetric techniques and image processing:  A review, ISPRS Journal of 30
- Photogrammetry and Remote Sensing. 144 (2018), pp. 180-188. 31
- https://doi.org/10.1016/j.isprsjprs.2018.07.010. 32
- [11] Q. Ai, Y. Yuan, S.L. Shen, H. Wang, X. Huang, Investigation on inspection scheduling for 33
- the maintenance of tunnel with different degradation modes, Tunnelling and Underground 34
- Space Technology. 106 (2020) 103589. https://doi.org/10.1016/j.tust.2020.103589. 35
- [12] K.  Elbaz,  J.S.  Shen,  A.  Arulrajah,  S.  Horpibulsuk,  Geohazards  induced  by  anthropic 36
- activities of  geoconstruction:  a  review  of  recent failure cases,  Arabian  Journal  of 37
- Geosciences. 9 (18) (2016), pp. 1-11. https://doi.org/10.1007/s12517-016-2740-z. 38
- [13] C. Liu, D. Zhang, S. Zhang, Characteristics and treatment measures of lining damage: A case 39
- study on a mountain tunnel, Engineering Failure Analysis. 128 (2021) 105595. 40
- https://doi.org/10.1016/j.engfailanal.2021.105595. 41
- [14] W.  Bergeson,  S.L.  Ernst,  Tunnel  Operations,  Maintenance,  Inspection,  and  Evaluation 42
- (TOMIE) Manual, United States. Federal Highway Administration (2015), FHWA-HIF-1543

005. https://rosap.ntl.bts.gov/view/dot/42887 (Last accessed in December 2nd, 2022). 1
- [15] J.M.W.  Brownjohn,  Structural  health  monitoring  of  civil  infrastructure,  Philosophical 2
3. Transactions of the Royal Society A: Mathematical, Physical and Engineering Sciences. 365 3
- (1851) (2007), pp. 589-622. https://doi.org/10.1098/rsta.2006.1925. 4
- [16] D.  Feng,  M.Q.  Feng,  Computer  vision  for  SHM  of  civil  infrastructure:  From  dynamic 5
6. response measurement to damage detection-A review, Engineering Structures. 156 (2018), 6
7. pp. 105-117. https://doi.org/10.1016/j.engstruct.2017.11.018. 7
- [17] C. Balaguer, R. Montero, J.G. Victores, S. Martínez, A. Jardón, Towards fully automated 8
9. tunnel  inspection:  A  survey  and  future  trends,  in:  ISARC.  Proceedings  of  the  31st 9
10. International Symposium on Automation and Robotics in Construction, IAARC Publications, 10
11. 2014, pp. 19-33. https://doi.org/10.22260/isarc2014/0005 (ISBN 978-0-646-59711-9). 11
- [18] Y.A. Hsieh, Y.J. Tsai, Machine learning for crack detection: Review and model performance 12
13. comparison,  Journal  of  Computing  in  Civil  Engineering.  34  (5)  (2020)  04020038. 13
14. https://doi.org/10.1061/(ASCE)CP.1943-5487.0000918. 14
- [19] C. Koch, K. Georgieva, V. Kasireddy, B. Akinci, P. Fieguth, A review on computer vision 15
16. based defect detection and condition assessment of concrete and asphalt civil infrastructure, 16
17. Advanced Engineering Informatics. 29 (2) (2015), pp. 196-210. 17
18. https://doi.org/10.1016/j.aei.2015.01.008. 18
- [20] E.  Menendez,  J.G.  Victores,  R.  Montero,  S.  Martínez,  C.  Balaguer,  Tunnel  structural 19
20. inspection and assessment using an autonomous robotic system, Automation in Construction. 20
21. 87 (2018), pp. 117-126. https://doi.org/10.1016/j.autcon.2017.12.001. 21
- [21] D.M. McCann, M.C. Forde, Review of NDT methods in the assessment of concrete and 22

23

masonry structures, NDT

&amp;

E

International.

34

(2)

(2001), pp.

71-84.

- https://doi.org/10.1016/S0963-8695(00)00032-3. 24
- [22] W.W.L. Lai, X. Dérobert, P. Annan, A review of Ground Penetrating Radar application in 25
- civil engineering: A 30-year journey from Locating and Testing to Imaging and Diagnosis, 26
- NDT &amp; E International. 96 (2018), pp. 58-78. https://doi.org/10.1016/j.ndteint.2017.04.002. 27
- [23] K. Schabowicz, Modern acoustic techniques for testing concrete structures accessible from 28
- one side only, Archives of Civil and Mechanical Engineering. 15 (4) (2015), pp. 1149-1159. 29
- https://doi.org/10.1016/j.acme.2014.10.001. 30
- [24] R. Montero, J.G. Victores, S. Martínez, A. Jardón, C. Balaguer, Past, present and future of 31
- robotic tunnel inspection, Automation in Construction. 59 (2015), pp. 99-112. 32
- https://doi.org/10.1016/j.autcon.2015.02.003. 33
- [25] Y. Jiang, X. Zhang, T. Taniguchi, Quantitative condition inspection and assessment of tunnel 34
- lining, Automation in Construction. 102 (2019), pp. 35

258-269.

- https://doi.org/10.1016/j.autcon.2019.03.001. 36
- [26] X. Li, X. Lin, H. Zhu, X. Wang, Z. Liu, Condition assessment of shield tunnel using a new 37
- indicator: The tunnel serviceability index, Tunnelling and Underground Space Technology. 38
- 67 (2017), pp. 98-106. https://doi.org/10.1016/j.tust.2017.05.007. 39
- [27] M.  Alsharqawi,  T.  Dawood,  S.  Abdelkhalek,  M.  Abouhamad,  T.  Zayed,  Condition 40
- assessment  of  concrete-made  structures  using  ground  penetrating  radar,  Automation  in 41
- Construction. 144 (2022) 104627. https://doi.org/10.1016/j.autcon.2022.104627. 42
- [28] J. Lai, J. Qiu, H. Fan, J. Chen, Z. Hu, Q. Zhang, J. Wang, Structural safety assessment of 43
- existing  multiarch tunnel: a case study, Advances in Materials Science and Engineering. 44

- 2017 (2017). https://doi.org/10.1155/2017/1697041. 1
- [29] X. Wu, Y. Jiang, J. Wang, K. Masaya, T. Taniguchi, T. Yamato, A new health assessment 2
- index of tunnel lining based on the digital inspection of surface cracks, Applied Sciences. 7 3
- (5) (2017) 507. https://doi.org/10.3390/app7050507. 4
- [30] M. Zhu, H. Zhu, F. Guo, X. Chen, J.W. Ju, Tunnel condition assessment via cloud model5
- based random forests and self-training approach, Computer-Aided Civil and Infrastructure 6
- Engineering. 36 (2) (2021), pp. 164-179. https://doi.org/10.1111/mice.12601. 7
- [31] T. Asakura, Y. Kojima, Tunnel maintenance in Japan, Tunnelling and Underground Space 8
- Technology. 18 (2-3) (2003), pp. 161-169. https://doi.org/10.1016/S0886-7798(03)00024-5. 9
- [32] J.A.  Richards,  Inspection,  maintenance  and  repair  of  tunnels:  international  lessons  and 10

11

practice,  Tunnelling  and  Underground  Space  Technology.  13  (4)  (1998),  pp.  369-375.

- https://doi.org/10.1016/s0886-7798(98)00079-0. 12
- [33] F. Ye, N. Qin, X. Liang, A. Ouyang, Z. Qin, E. Su, Analyses of the defects in highway tunnels 13

14

in China, Tunnelling and Underground Space Technology.

107

(2021)

103658.

- https://doi.org/10.1016/j.tust.2020.103658. 15
- [34] L.R. Sousa, R.L. Sousa, C. Silva, V. Freitas, Maintenance methodologies of old railway 16
- tunnels, in: Symposium New Development in Rock Mechanics and Engineering &amp; Sanya 17
- Forum for the Plan of City and City Construction, 2009, pp. 401-406. 18
- https://www.researchgate.net/profile/Luis-Sousa19
- 3/publication/271763635\_Maintenance\_methodologies\_of\_old\_railway\_tunnels (Last 20
- accessed in March 12th, 2023). 21
- [35] T.  Rock,  P.  Arch,  T.  Ireland,  Rehabilitation  and  maintenance  of  road  tunnels-Mersey 22
- Queensway,  in:  IABSE  Symposium  Report,  International  Association  for  Bridge  and 23
- Structural Engineering, 2006, pp. 33-40. https://doi.org/10.2749/222137806796235953. 24
- [36] T. Liu, H. Zhu, Research on defects of arcade tunnel with partial pressure and its treating 25
- measurements,  China  Journal  of  Highway  and  Transport.  18  (4)  (2005),  pp.  72-77  (in 26
- Chinese). https://doi.org/10.19721/j.cnki.1001-7372.2005.04.015. 27
- [37] Y. Luo, J. Chen, Research status and progress of tunnel frost damage, Journal of Traffic and 28
- Transportation Engineering (English Edition). 6 (3) (2019), pp. 297-309. 29
- https://doi.org/10.1016/j.jtte.2018.09.007. 30
- [38] H. Feng, X. Zhang, D. Gou, J. Chun, X. Ou, X. Zhou, Cause investigation of side-wall 31
- cracking in an operational tunnel, Engineering Failure Analysis. 101 (2019), pp. 157-171. 32
- https://doi.org/10.1016/j.engfailanal.2019.02.038. 33
- [39] F.  Ye,  X.  Han,  N.  Qin, A.  Ouyang,  X.  Liang,  C.  Xu,  Damage  management  and  safety 34
- evaluation for operating highway tunnels: a case study of Liupanshan tunnel, Structure and 35
- Infrastructure Engineering. 16 (11) (2020), pp. 1512-1523. 36
- https://doi.org/10.1080/15732479.2020.1713165. 37
- [40] X. Zhang, Y. Jiang, K. Maegawa, Mountain tunnel under earthquake force: A review of 38
- possible  causes  of  damages  and  restoration  methods,  Journal  of  Rock  Mechanics  and 39
- Geotechnical Engineering. 12 (2) (2020), pp. 414-426. 40
- https://doi.org/10.1016/j.jrmge.2019.11.002. 41
- [41] H.  Feng,  X.  Chang, Analysis  of  structural  disasters  in  shield  tunnels  and  measures  and 42
- suggestions for waterproofing, Modern Tunnelling Technology. 53 (6) (2016), pp. 36-43 (in 43
- Chinese). https://doi.org/10.13807/j.cnki.mtt.2016.06.006. 44

- [42] F. Dong, Q. Fang, D. Zhang, H. Xu, Y. Li, X. Niu, Analysis on defects of operational metro 1
2. tunnels in Beijing, China Civil Engineering Journal. 50 (6) (2017), pp. 104-113 (in Chinese). 2
3. https://doi.org/10.15951/j.tmgcxb.2017.06.012. 3
- [43] A. Inokuma, S. Inano, Road tunnels in Japan: deterioration and countermeasures, Tunnelling 4
5. and Underground Space Technology. 11 (3) (1996), pp. 305-309. 5
6. https://doi.org/10.1016/0886-7798(96)00026-0. 6
- [44] S.W. Park, Y.S. Shin, Y .S. Oh, S.R. Ahn, A guideline on condition assessment of existing old 7
8. railway tunnels, Tunnelling and Underground Space Technology. 21 (3-4) (2006), pp. 3298
330. https://doi.org/10.1016/j.tust.2005.12.043. 9
- [45] C. Yuan, S. Li, S. Li, W. Li, Study of defects characteristics and repair methods of old tunnel 10
11. in cold region, Chinese Journal of Rock Mechanics and Engineering. 30 (S1) (2011), pp. 11
12. 3354-3361 (in Chinese). 12
13. https://kns.cnki.net/kcms/detail/detail.aspx?FileName=YSLX2011S1099&amp;DbName=CJFQ 13

14

2011 (Last accessed in March 12th, 2023).

- [46] S. Zhao, M. Shadabfar, D. Zhang, J. Chen, H. Huang, Deep learning-based classification and 15
2. instance segmentation of leakage-area and scaling images of shield tunnel linings, Structural 16
3. Control and Health Monitoring. 28 (6) (2021) e2732. https://doi.org/10.1002/stc.2732. 17
- [47] Q. Gong, L. Zhu, Y. Wang, Z. Yu, Automatic subway tunnel crack detection system based 18

19

on  line  scan  camera,  Structural  Control  and  Health  Monitoring.  28  (8)  (2021)  e2776.

- https://doi.org/10.1002/stc.2776. 20
- [48] M. Lei, L. Liu, C. Shi, Y. Tan, Y . Lin, W. Wang, A novel tunnel-lining crack recognition 21
- system based on digital image technology, Tunnelling and Underground Space Technology. 22
- 108 (2021) 103724. https://doi.org/10.1016/j.tust.2020.103724. 23
- [49] Q. Wang, N. Zhang, K. Jiang, C. Ma, Z. Zhou, C. Dai, Tunnel lining crack recognition based 24
- on  improved  multiscale  retinex  and  sobel  edge  detection,  Mathematical  Problems  in 25
- Engineering. 2021 (2021). https://doi.org/10.1155/2021/9969464. 26
- [50] T. Yu, A. Zhu, Y. Chen, Efficient crack detection method for tunnel lining surface cracks 27
- based  on  infrared  images,  Journal  of  Computing  in  Civil  Engineering.  31  (3)  (2017) 28
04016067. https://doi.org/10.1061/(asce)cp.1943-5487.0000645. 29
- [51] Y. Xue, Y. Li, A fast detection method via region-based fully convolutional neural networks 30
- for shield tunnel lining defects, Computer-Aided Civil and Infrastructure Engineering. 33 (8) 31
- (2018), pp. 638-654. https://doi.org/10.1111/mice.12367. 32
- [52] Y. Ren, J. Huang, Z. Hong, W. Lu, J. Yin, L. Zou, X. Shen, Image-based concrete crack 33
- detection in tunnels using deep fully convolutional networks, Construction and Building 34
- Materials. 234 (2020) 117367. https://doi.org/10.1016/j.conbuildmat.2019.117367. 35
- [53] X. Xu, H. Yang, Vision measurement of tunnel structures with robust modelling and deep 36
- learning algorithms, Sensors. 20 (17) (2020) 4945. https://doi.org/10.3390/s20174945. 37
- [54] S. Zhao, D. Zhang, Y. Xue, M. Zhou, H. Huang, A deep learning-based approach for refined 38
- crack evaluation from shield tunnel lining images, Automation in Construction. 132 (2021) 39
103934. https://doi.org/10.1016/j.autcon.2021.103934. 40
- [55] D. Li, Q. Xie, X. Gong, Z. Yu, J. Xu, Y. Sun, J. Wang, Automatic defect detection of metro 41
- tunnel surfaces using a vision-based inspection system, Advanced Engineering Informatics. 42
- 47 (2021) 101206. https://doi.org/10.1016/j.aei.2020.101206. 43
- [56] A.P.  Annan,  GPR  -  History,  trends,  and  future  developments,  Subsurface  Sensing 44

- Technologies and Applications. 3 (4) (2002), pp. 253-270. 1
- https://doi.org/10.1023/A:1020657129590. 2
- [57] G. Alsharahi, M.F. Bouami, A. Faize, M. Louzazni, A. Khamlichi, M. Atounti, Contribution 3
- of analysis and detection the risks appearing in roads using GPR method: A case study in 4
- Morocco, Ain Shams Engineering Journal. 12 (2) (2021), pp. 1435-1450. 5
- https://doi.org/10.1016/j.asej.2020.10.014. 6
- [58] L. Xiang, H. Zhou, Z. Shu, S. Tan, G. Liang, J. Zhu, GPR evaluation of the Damaoshan 7
- highway tunnel:  A case study, NDT  &amp;  E  International. 59 (2013), pp. 68-76. 8
- https://doi.org/10.1016/j.ndteint.2013.05.004. 9
- [59] D. Feng, X. Wang, B. Zhang, Specific evaluation of tunnel lining multi-defects by all-refined 10
- GPR simulation  method  using  hybrid  algorithm  of  FETD  and  FDTD,  Construction  and 11
- Building Materials. 185 (2018), pp. 220-229. 12
- https://doi.org/10.1016/j.conbuildmat.2018.07.039. 13
- [60] D. Liu, Y. Deng, F. Yang, G. Xu, Nondestructive testing for crack of tunnel lining using GPR, 14

15

Journal of Central  South University of  Technology.

12

(1)

(2005), pp.  120-124.

- https://doi.org/10.1007/s11771-005-0384-3. 16
- [61] T.  Ling,  L.  Zhang,  F.  Huang,  D.  Gu,  B. Yu,  S.  Zhang,  OMHT  method  for  weak  signal 17
- processing of GPR and its application in identification of concrete micro-crack, Journal of 18

19

Central South University. 26 (11) (2019), pp. 3057-3065. https://doi.org/10.1007/s11771-

- 019-4236-y. 20
- [62] M. Moles, L. Robertson, T. Sinclair, Developments in time-of-flight diffraction (TOFD), in: 21
- 18th World Conference on Nondestructive Testing, 2012. 22
- https://www.ndt.net/search/docs.php3?id=12563 (Last accessed in March 14th, 2023). 23
- [63] M. Spies, H. Rieder, A. Dillhöfer, V. Schmitz, W. Müller, Synthetic aperture focusing and 24
- time-of-flight diffraction ultrasonic imaging-past and present, Journal of Nondestructive 25
- Evaluation. 31 (4) (2012), pp. 310-323. https://doi.org/10.1007/s10921-012-0150-z. 26
- [64] A.  Habibpour-Ledari,  F.  Honarvar,  Three  dimensional  characterization  of  defects  by 27
- ultrasonic time-of-flight diffraction (ToFD) technique, Journal of Nondestructive Evaluation. 28
- 37 (1) (2018), pp. 1-11. https://doi.org/10.1007/s10921-018-0465-5. 29
- [65] Y.C. Angel,  J.D. Achenbach,  Reflection  and  transmission  of obliquely  incident Rayleigh 30
- waves by a surface-breaking crack, The Journal of the Acoustical Society of America. 75 (2) 31
- (1984), pp. 313-319. https://doi.org/10.1121/1.390473. 32
- [66] C.H. Yew, K.G. Chen, D.L. Wang, An experimental study of interaction between surface 33
- waves and a surface breaking crack, The Journal of the Acoustical Society of America. 75 34
- (1) (1984), pp. 189-196. https://doi.org/10.1121/1.390393. 35
- [67] S.H.  Kee,  E.  Fernández-Gómez,  J.  Zhu,  Evaluating  surface-breaking  cracks  in  concrete 36
- using air-coupled sensors,  ACI Materials Journal. 108 (5) (2011), pp. 558-565. 37
- https://doi.org/10.14359/51683266. 38
- [68] S.H. Kee, J. Zhu, Using air-coupled sensors to determine the depth of a surface-breaking 39
- crack in concrete, The Journal of the Acoustical Society of America. 127 (3) (2010), pp. 40
- 1279-1287. https://doi.org/10.1121/1.3298431. 41
- [69] C.W.  In,  F.  Schempp,  J.Y .  Kim,  L.J.  Jacobs, A  fully  non-contact,  air-coupled  ultrasonic 42
- measurement of surface breaking cracks in concrete, Journal of Nondestructive Evaluation. 43
- 34 (1) (2015), pp. 1-7. https://doi.org/10.1007/s10921-014-0272-6. 44

- [70] K. Karhunen, A. Seppänen, A. Lehikoinen, P.J.M. Monteiro, J.P. Kaipio, Electrical resistance 1
2. tomography imaging of concrete, Cement and Concrete Research. 40 (1) (2010), pp. 1372
145. https://doi.org/10.1016/j.cemconres.2009.08.023. 3
- [71] K. Karhunen, A. Seppänen, A. Lehikoinen, J. Blunt, J.P. Kaipio, P.J.M. Monteiro, Electrical 4
5. resistance tomography for assessment of cracks in concrete, ACI Materials Journal. 107 (5) 5
6. (2010), pp. 523-531. https://doi.org/10.14359/51663973. 6
- [72] T. Yasuda, H. Yamamoto, M. Enomoto, Y. Nitta, Smart tunnel inspection and assessment 7
8. using mobile inspection vehicle, non-contact radar and AI, in: ISARC. Proceedings of the 8
9. 37th  International  Symposium  on  Automation  and  Robotics  in  Construction,  IAARC 9

10

Publications,  2020,  pp.  1373-1379.  https://doi.org/10.22260/isarc2020/0190  (ISBN  978-

- 952-94-3634-7). 11
- [73] H. Huang, Y. Sun, Y. Xue, F. Wang, Inspection equipment study for subway tunnel defects 12
- by grey-scale image processing, Advanced Engineering Informatics. 32 (2017), pp. 188-201. 13
- https://doi.org/10.1016/j.aei.2017.03.003. 14
- [74] N. Otsu, A threshold selection method from gray-level histograms, IEEE Transactions on 15

16

Systems, Man, and Cybernetics.

9

(1)

(1979), pp.

62-66.

- https://doi.org/10.1109/tsmc.1979.4310076. 17
- [75] H. Huang, Q. Li, D. Zhang, Deep learning based image recognition for crack and leakage 18
- defects of metro shield tunnel, Tunnelling and Underground Space Technology. 77 (2018), 19
- pp. 166-176. https://doi.org/10.1016/j.tust.2018.04.002. 20
- [76] Y. Xue, X. Cai, M. Shadabfar, H. Shao, S. Zhang, Deep learning-based automatic recognition 21
- of water leakage area in shield tunnel lining, Tunnelling and Underground Space Technology. 22
- 104 (2020) 103524. https://doi.org/10.1016/j.tust.2020.103524. 23
- [77] D.  Meng,  S.  Lin,  H.  Azari,  Reducing  thermal  reflections  for  infrared  thermography 24
- applications on tunnel liners with reflective finishes, Transportation Research Record. 2672 25
- (41) (2018), pp. 145-155. https://doi.org/10.1177/0361198118780711. 26
- [78] P. Yu, H. Wu, C. Liu, Z. Xu, Water leakage diagnosis in metro tunnels by intergration of laser 27
- point cloud and infrared thermal imaging, ISPRS-International Archives of the 28
- Photogrammetry, Remote Sensing and Spatial Information Sciences. 42 (2018), pp. 216729
2171. https://doi.org/10.5194/isprs-archives-xlii-3-2167-2018. 30
- [79] Z. Lu, F. Zhu, L. Shi, F. Wang, P. Zeng, J. Hu, X. Liu, Y . Xu, Q. Chen, Automatic seepage 31
- detection in  cable  tunnels  using  infrared  thermography,  Measurement  Science  and 32
- Technology. 30 (11) (2019) 115902. https://doi.org/10.1088/1361-6501/ab30d9. 33
- [80] H. Huang, W. Cheng, M. Zhou, J. Chen, S. Zhao, Towards automated 3D inspection of water 34
- leakages in shield tunnel linings using mobile laser scanning data, Sensors. 20 (22) (2020) 35
6669. https://doi.org/10.3390/s20226669. 36
- [81] T.  Xu,  L.  Xu,  X.  Li,  J.  Yao,  Detection  of  water  leakage  in  underground  tunnels  using 37
- corrected intensity data and 3D point cloud of terrestrial laser scanning, IEEE Access. 6 38
- (2018), pp. 32471-32480. https://doi.org/10.1109/access.2018.2842797. 39
- [82] X. Cheng, X. Hu, K. Tan, L. Wang, L. Yang, Automatic detection of shield tunnel leakages 40
- based on terrestrial mobile LiDAR intensity images using deep learning, IEEE Access. 9 41
- (2021), pp. 55300-55310. https://doi.org/10.1109/ACCESS.2021.3070813. 42
- [83] C. Lin, X. Wang, Y. Li, F. Zhang, Z. Xu, Y. Du, Forward modelling and GPR imaging in 43
- leakage  detection  and  grouting  evaluation  in  tunnel  lining,  KSCE  Journal  of  Civil 44

- Engineering. 24 (2020), pp. 278-294. https://doi.org/10.1007/s12205-020-1530-z. 1
- [84] A. Voss, M. Pour-Ghaz, M. Vauhkonen, A. Seppänen, Electrical capacitance tomography to 2
- monitor  unsaturated  moisture  ingress  in  cement-based  materials,  Cement  and  Concrete 3
- Research. 89 (2016), pp. 158-167. https://doi.org/10.1016/j.cemconres.2016.07.011. 4
- [85] Y. Lyu, H. Wang, J. Gong, GPR detection of tunnel lining cavities and reverse-time migration 5

6

imaging, Applied Geophysics. 17 (1) (2020), pp. 1-7. https://doi.org/10.1007/s11770-019-

- 0831-9. 7
- [86] A.M. Alani,  F.  Tosti,  GPR  applications  in  structural  detailing  of  a  major  tunnel  using 8
- different frequency antenna systems, Construction and Building Materials. 158 (2018), pp. 9
- 1111-1122. https://doi.org/10.1016/j.conbuildmat.2017.09.100. 10
- [87] Q. Yu, H. Zhou, Y. Wang, R. Duan, Quality monitoring of metro grouting behind segment 11
- using ground penetrating radar, Construction and Building Materials. 110 (2016), pp. 18912
200. https://doi.org/10.1016/j.conbuildmat.2015.12.109. 13
- [88] H. Qin, D. Zhang, Y. Tang, Y. Wang, Automatic recognition of tunnel lining elements from 14
- GPR images using deep convolutional  networks with  data  augmentation, Automation  in 15
- Construction. 130 (2021) 103830. https://doi.org/10.1016/j.autcon.2021.103830. 16
- [89] B. Liu, Y . Ren, H. Liu, H. Xu, Z. Wang, A.G. Cohn, P. Jiang, GPRInvNet: Deep learning17
- based  ground-penetrating  radar  data  inversion  for  tunnel  linings,  IEEE  Transactions  on 18

19

Geoscience and Remote Sensing.

59

(10)

(2021), pp.

8305-8325.

- https://doi.org/10.1109/TGRS.2020.3046454. 20
- [90] Y. Zan, Z. Li, G. Su, X. Zhang, An innovative vehicle-mounted GPR technique for fast and 21
- efficient monitoring of tunnel lining structural conditions, Case Studies in Nondestructive 22
- Testing and Evaluation. 6 (2016), pp. 63-69. https://doi.org/10.1016/j.csndt.2016.10.001. 23
- [91] Z. Ye, Y. Ye, Comparison of detection effect of cavities behind shield tunnel segment using 24
- transient electromagnetic radar and ground penetration radar, Geotechnical and Geological 25
- Engineering. 37 (5) (2019), pp. 4391-4403. https://doi.org/10.1007/s10706-019-00916-y. 26
- [92] Z. Ye, C. Zhang, Y. Ye, Principle of a low-frequency transient electromagnetic radar system 27
- and  its  application  in  the  detection  of  underground  pipelines  and  voids,  Tunnelling  and 28
- Underground Space Technology. 122 (2022) 104392. 29
- https://doi.org/10.1016/j.tust.2022.104392. 30
- [93] N.J.  Carino,  The  impact-echo  method:  an  overview,  in:  Structures  2001:  A  Structural 31
- Engineering  Odyssey.  (2001),  pp.  1-18.  https://doi.org/10.1061/40558(2001)15  (ISBN 32
- 9780784405581). 33
- [94] R. Cao, M. Ma, R. Liang, C. Niu, Detecting the void behind the tunnel lining by impact34
- echo methods with different signal analysis approaches, Applied Sciences. 9 (16) (2019) 35
3280. https://doi.org/10.3390/app9163280. 36
- [95] K. Hashimoto,  T. Shiotani, T. Nishida,  T.  Miyagawa,  Application  of elastic-wave 37
- tomography  to  repair  inspection  in  deteriorated  concrete  structures,  Journal  of  Disaster 38
- Research. 12 (3) (2017), pp. 496-505. https://doi.org/10.20965/jdr.2017.p0496. 39
- [96] H.  Wang,  S.H.  Hsieh,  C.H.  Hu,  Y .C.  Tsai,  Tracing  developing  deterioration  zones  in  a 40
- damaged  dam  by  using  elastic  wave  tomography,  in:  IOP  Conference  Series:  Materials 41
- Science and Engineering, IOP Publishing. 615 (1) (2019) 012077. 42
- https://doi.org/10.1088/1757-899x/615/1/012077. 43
- [97] J. White, Ultrasonic tomography for detecting and locating defects in concrete structures, 44

- PhD Thesis, Texas A &amp; M University, 2012. https://core.ac.uk/download/pdf/147229609.pdf 1
- (Last accessed in March 12th, 2023). 2
- [98] C.W. Tseng, Y.F.  Chang,  C.Y.  Wang, Total  focusing  method  or  phased  array  technique: 3
- Which detection technique is better for the ultrasonic nondestructive testing of concrete?, 4
- Journal of Materials in Civil Engineering. 30 (1) (2018) 04017256. 5
- https://doi.org/10.1061/(ASCE)MT.1943-5533.0002118. 6
- [99] S. Konishi, K. Kawakami, M. Taguchi, Inspection method with infrared thermometry for 7
- detect  void  in  subway  tunnel  lining,  Procedia  Engineering.  165  (2016),  pp.  474-483. 8
- https://doi.org/10.1016/j.proeng.2016.11.723. 9
- [100] A. Afshani, K. Kawakami, S. Konishi, H. Akagi, Study of infrared thermal application for 10

11

detecting defects within tunnel lining, Tunnelling and Underground Space Technology. 86

- (2019), pp. 186-197. https://doi.org/10.1016/j.tust.2019.01.013. 12
- [101] P.  Cotič,  D.  Kolarič,  V .B.  Bosiljkov,  V .  Bosiljkov,  Z.  Jagličić,  Determination  of  the 13
- applicability  and  limits  of  void  and  delamination  detection  in  concrete  structures  using 14
- infrared thermography, NDT &amp; E International. 74 (2015), pp. 87-93. 15
- https://doi.org/10.1016/j.ndteint.2015.05.003. 16
- [102] S.  Cui,  J.K.  Nimmagadda,  J.E.  Baciak,  Backscatter  radiography  as  a  non-destructive 17
- examination tool for concrete structures, in: 2017 IEEE Nuclear Science Symposium and 18
- Medical Imaging Conference (NSS/MIC), IEEE, 2017, pp. 1-6. 19

20

https://doi.org/10.1109/nssmic.2017.8532696.

- [103] Y.D. Ye, H.H. Zhu, R.L. Wang, Analysis on the current status of metro operating tunnel 21
2. damage  in  soft  ground  and  its  causes,  Chinese  Journal  of  Underground  Space  and 22

23

Engineering.  3  (1)  (2007), pp.  157-160  (in  Chinese).  https://doi.org/10.3969/j.issn.1673-

- 0836.2007.01.034. 24
- [104] P. Shi, P. Li, Mechanism of soft ground tunnel defect generation and functional degradation, 25
3. Tunnelling and Underground Space Technology. 50 (2015), pp. 334-344. 26
4. https://doi.org/10.1016/j.tust.2015.08.002. 27
- [105] Highway and rail transit tunnel inspection manual, Federal Highway Administration and 28
6. Federal Transit Administration, 2005. https://rosap.ntl.bts.gov/view/dot/40562 (Last 29

30

accessed in February 17th, 2023).

- [106] X.T. Lin, X.S. Chen, D. Su, M. Zhu, K.H. Han, R.P. Chen, Evaluation method for resilience 31
2. of shield tunnel lining considering multiple disturbances and its application, Chinese Journal 32
3. of Geotechnical Engineering. 44 (4) (2022), pp. 591-601 (in Chinese). http://f6z.cn/8iAoD 33
4. (Last accessed in March 15th, 2023). 34
- [107] Technical Specifications of Maintenance for Highway Tunnel JTGH12-2015, Ministry of 35
6. Construction of the People's Republic of China, 2015 (in Chinese). 36
7. https://www.nssi.org.cn/nssi/front/87846803.html (Last accessed in March 12th, 2023). 37
- [108] Code  for  Design  of  Metro  GB50157-2003,  Ministry  of  Construction  of  the  People's 38
9. Republic  of  China,  2003  (in  Chinese).  https://www.nssi.org.cn/nssi/front/6257453.html 39
10. (Last accessed in March 12th, 2023). 40
- [109] Standard for Design of Shield  Tunnel Engineering GB/T51438-2021,  Ministry of 41
12. Construction of the People's Republic of China, 2021 (in Chinese). 42
13. https://www.nssi.org.cn/nssi/front/115026850.html (Last accessed in March 12th, 2023). 43
- [110] Y. Shigeta, T. Tobita, K. Kamemura, M. Shinji, I. Yoshitake, K. Nakagawa, Propose of tunnel 44

- crack index (TCI) as an evaluation method for lining concrete, Doboku Gakkai Ronbunshuu. 1
- 62 (4) (2006), pp. 628-632 (in Japanese). https://doi.org/10.2208/jscejf.62.628. 2
- [111] B. Yu, J. Zhao, K. Fang, Y. Tan, J. Ning, Rock strength evaluation during progressive failure 3
- process based on fractural characterization, Marine Georesources &amp; Geotechnology. 34 (8) 4
- (2016), pp. 759-763. https://doi.org/10.1080/1064119X.2015.1089454. 5
- [112] W. Tian,  N.  Han,  Evaluation  of  damage  in  concrete  suffered  freeze-thaw  cycles  by  CT 6
- technique,  Journal  of  Advanced  Concrete  Technology.  14  (11)  (2016),  pp.  679-690. 7
- https://doi.org/10.3151/jact.14.679. 8
- [113] Y.  Yuan,  Y.  Bai,  J.  Liu,  Assessment  service  state  of  tunnel  structure,  Tunnelling  and 9

10

Underground Space Technology.

27

(1)

(2012), pp.

72-85.

- https://doi.org/10.1016/j.tust.2011.07.002. 11
- [114] X. Lin, W. Ding, X. Li, Y. Xi, Q. Yuan, GIS-Based grid assessment model of shield tunnel 12
- conditions and its application, Modern Tunnelling Technology. 55 (5) (2018), pp. 19-26 (in 13
- Chinese). https://doi.org/10.13807/j.cnki.mtt.2018.05.003. 14
- [115] G. Andreotti, G.M. Calvi, K. Soga, C. Gong, W. Ding, Cyclic model with damage assessment 15
- of  longitudinal  joints  in  segmental  tunnel  linings,  Tunnelling  and  Underground  Space 16
- Technology. 103 (2020) 103472. https://doi.org/10.1016/j.tust.2020.103472. 17
- [116] H. Zhang, X. Wang, Y. Xue, J. Zhu, Service status evaluation of shield tunnel based on 18

19

Knowledge Graph, Modern Tunnelling Technology. 59 (4) (2022), pp. 58-68 (in Chinese).

- https://doi.org/10.13807/j.cnki.mtt.2022.04.007. 20
- [117] M.H. Rafiei, H. Adeli, A novel unsupervised deep learning model for global and local health 21

22

condition  assessment  of  structures,  Engineering  Structures.  156  (2018),  pp.  598-607.

- https://doi.org/10.1016/j.engstruct.2017.10.070. 23
- [118] S.N. Yu, J.H. Jang, C.S. Han, Auto inspection system using a mobile robot for detecting 24
- concrete  cracks  in  a  tunnel,  Automation  in  Construction.  16  (3)  (2007),  pp.  255-261. 25
- https://doi.org/10.1016/j.autcon.2006.05.003. 26
- [119] J.G.  Victores,  S.  Martínez,  A.  Jardón,  C.  Balaguer,  Robot-aided  tunnel  inspection  and 27
- maintenance system by vision and proximity sensor integration, Automation in Construction. 28
- 20 (5) (2011), pp. 629-636. https://doi.org/10.1016/j.autcon.2010.12.005. 29
- [120] X. Chen, G. Liu, Z. Chen, Y . Li, C. Luo, B. Luo, X. Zhang, Automatic detection system with 30
- 3D  scanning  and  robot  technology  for  detecting  surface  dimension  of  the  track  slabs, 31
- Automation in Construction. 142 (2022) 104525. 32
- https://doi.org/10.1016/j.autcon.2022.104525. 33
- [121] C. Yu, W. Ding, Q. Zhang, Research on a calculation method for the damage evaluation of 34
- the existing urban tunnel lining structure, Modern Tunnelling Technology. 55 (5) (2018), pp. 35
- 11-18 (in Chinese). https://doi.org/10.13807/j.cnki.mtt.2018.05.002. 36
- [122] Y.S. Frolov, A.N. Konkov, E.S. Svintsov, Appraisal of highway tunnels construction on the 37
- active railroad tunnel operational reliability in the City of Sochi, Procedia Engineering. 189 38
- (2017), pp. 811-817. https://doi.org/10.1016/j.proeng.2017.05.126. 39
- [123] H.  Cao,  L.  Peng,  M.  Lei,  F.  Chen,  Q.  Tang,  Causes  analysis,  reinforcement  and  repair 40
- technology of segment crack and damage during shield tunnelling process: a case study, 41
- Geotechnical and Geological Engineering. 37 (2019), pp. 765-773. 42
- https://doi.org/10.1007/s10706-018-0648-y. 43
- [124] W.N. Yiu, H.J. Burd, C.M. Martin, Finite-element modelling for the assessment of tunnel44

- induced  damage  to  a  masonry  building,  Géotechnique.  67  (9)  (2017),  pp.  780-794. 1
- https://doi.org/10.1680/jgeot.sip17.P.249. 2
- [125] W. Han, Y. Jiang, N. Li, G. Wang, H. Luan, C. Liu, Failure behavior and reinforcing design 3
- of degraded tunnel linings based on the three-dimensional numerical evaluation, 4
- Engineering Failure Analysis. 129 (2021) 105677. 5
- https://doi.org/10.1016/j.engfailanal.2021.105677. 6
- [126] K. Kiriyama, M. Kakizaki, T. Takabayashi, N. Hirosawa, T. Takeuchi, H. Hajohta, Y. Yano, 7
- K. Imafuku, Structure and construction examples of tunnel reinforcement method using thin 8
- steel panels, Nippon Steel Technical Report. 92 (2005), pp. 45-50 9
- https://www.nipponsteel.com/en/tech/report/nsc/pdf/n9209.pdf  (Last  accessed  in  March 10
- 12th, 2023). 11
- [127] D. Zhang, W. Zhai, H. Huang, D. Chapman, Robust retrofitting design for rehabilitation of 12
- segmental tunnel linings: Using the example of steel plates, Tunnelling and Underground 13
- Space Technology. 83 (2019), pp. 231-242. https://doi.org/10.1016/j.tust.2018.09.016. 14
- [128] C.T. Chang, C.W. Sun, S.W. Duann, R.N. Hwang, Response of a Taipei Rapid Transit System 15
- (TRTS) tunnel to adjacent excavation, Tunnelling and Underground Space Technology. 16 16
- (3) (2001), pp. 151-158. https://doi.org/10.1016/s0886-7798(01)00049-9. 17
- [129] X. Liu, Z. Jiang, Y. Yuan, H.A. Mang, Experimental investigation of the ultimate bearing 18
- capacity of deformed segmental tunnel linings strengthened by epoxy-bonded steel plates, 19

20

Structure and Infrastructure Engineering.

14

(6)

(2018), pp.

685-700.

- https://doi.org/10.1080/15732479.2017.1354892. 21
- [130] C.T. Chang, M.J. Wang, C.T. Chang, C.W. Sun, Repair of displaced shield tunnel of the 22
- Taipei rapid transit system, Tunnelling and Underground Space Technology. 16 (3) (2001), 23
- pp. 167-173. https://doi.org/10.1016/S0886-7798(01)00050-5. 24
- [131] X. Bi, X. Liu, X. Wang, L. Lu, Y. Zhu, Experimental study on the ultimate load-bearing 25
- capacity  of  deformed  segmental  tunnel  linings  strengthened  by  steel  plates,  China  Civil 26

27

Engineering Journal.

47

(11)

(2014), pp.

128-137

(in Chinese).

- https://doi.org/10.15951/j.tmgcxb.2014.11.048. 28
- [132] W. Zhai, D. Chapman, D. Zhang, H. Huang, Experimental study on the effectiveness of 29
- strengthening  over-deformed  segmental  tunnel  lining  by  steel  plates,  Tunnelling  and 30
- Underground Space Technology. 104 (2020) 103530. 31
- https://doi.org/10.1016/j.tust.2020.103530. 32
- [133] X. Liu, H. Lai, Y. Sang, Case study on the model test of staggered-jointed assembling shield 33
- tunnel structure reinforced by bonded steel plates under large deformation, IOP Conference 34
- Series: Earth and Environmental Science. 330 (2) (2019) 022080. 35
- https://doi.org/10.1088/1755-1315/330/2/022080. 36
- [134] T. Liu, H. Huang, R. Xu, X. Yang, Research on load-bearing capacity of metro shield tunnel 37
- lining strengthened by bonded steel plates, China Journal of Highway and Transport. 30 (8) 38
- (2017), pp. 91-99 (in Chinese). https://doi.org/10.19721/j.cnki.1001-7372.2017.08.010. 39
- [135] P. Xu, Y. Wei, Y. Yang, X. Zhou, Application of fabricated corrugated steel plate in subway 40
- tunnel  supporting  structure,  Case  Studies  in  Construction  Materials.  17  (2022)  e01323. 41
- https://doi.org/10.1016/j.cscm.2022.e01323. 42
- [136] D. Liu, J. Zuo, J. Wang, P. Li, K. Duan, D. Zhang, S. Guo, Bending failure mechanism and 43
- strengthening of concrete-filled steel tubular support, Engineering Structures. 198 (2019) 44

109449. https://doi.org/10.1016/j.engstruct.2019.109449. 1
- [137] G.  Wei,  Q.  Wang,  X.  Zhou,  F.  Feng,  X.  Wang,  L.  Zhang,  L.  Liang,  Experiments  and 2
3. numerical simulation of the reinforcement effect of channel-steel-reinforced shield tunnel 3
4. segments  under  unloading  conditions,  European  Journal  of  Environmental  and  Civil 4
5. Engineering. (2023), pp. 1-23. https://doi.org/10.1080/19648189.2023.2177751. 5
- [138] G. Yan, Y. Shen, B. Gao, Q. Zheng, K. Fan, H. Huang, Damage evolution of tunnel lining 6
7. with steel reinforced rubber joints under normal faulting: An experimental and numerical 7
8. investigation, Tunnelling and Underground Space Technology. 97 (2020) 103223. 8
9. https://doi.org/10.1016/j.tust.2019.103223. 9
- [139] Z. Li, X. Liu, H. Lai, Z. Yang, B. Wang, Detailed damage mechanism of deformed shield 10

11

tunnel linings reinforced by steel plates, Engineering Failure Analysis. 143 (2023) 106850.

- https://doi.org/10.1016/j.engfailanal.2022.106850. 12
- [140] Y.  Sun, Y . Yu,  J. Wang, Y . Ye, Q. Tan,  Mechanical properties of linings of shield tunnel 13
- strengthened by steel plates considering interface effects, Chinese Journal of Geotechnical 14
- Engineering. 44 (2) (2022), pp. 343-351 (in Chinese). http://f6z.cn/0MfcL (Last accessed in 15
- March 12th, 2023) 16
- [141]  ABAQUS. Analysis user's manual version (2019). 17
- http://130.149.89.49:2080/v6.14/books/usb/default.htm (Last accessed in March 12th, 2023). 18
- [142] M.L.  Benzeggagh,  M.  Kenane,  Measurement  of  mixed-mode  delamination  fracture 19
- toughness of unidirectional glass/epoxy composites with mixed-mode bending apparatus, 20
- Composites Science and Technology. 56 (4) (1996), pp. 439-449. 21
- https://doi.org/10.1016/0266-3538(96)00005-X. 22
- [143] A. Yin, X. Yang, C. Zhang, G. Zeng, Z. Yang, Three-dimensional heterogeneous fracture 23
- simulation of asphalt mixture under uniaxial tension with cohesive crack model, 24
- Construction and Building Materials. 76 (2015), pp. 103-117. 25
- https://doi.org/10.1016/j.conbuildmat.2014.11.065. 26
- [144] D. Liu, F. Wang, D. Zhang, K. Duan, Interfacial stresses of shield tunnel strengthened by a 27
- thin  plate  at  inner  surface,  Tunnelling  and  Underground  Space  Technology.  91  (2019) 28
103021. https://doi.org/10.1016/j.tust.2019.103021. 29
- [145] T.  Ren,  S.  Liu,  X.  Liu,  Experimental  study  of  bending  capacity  of  shield  tunnel  lining 30
- segment strengthened by corrugated steel, Tunnel Construction. 39 (2) (2019), pp. 317-323 31
- (in Chinese). http://f6z.cn/PMK2B (Last accessed in March 12th, 2023). 32
- [146] D. Liu, H. Huang, Q. Yue, Y. Xue, M. Wang, Behaviour of tunnel lining strengthened by 33
- textile-reinforced concrete, Structure and Infrastructure Engineering. 12 (8) (2016), pp. 96434
976. https://doi.org/10.1080/15732479.2015.1076009. 35
- [147] A.H.  Høien,  B.  Nilsen,  R.  Olsson,  Main  aspects  of  deformation  and  rock  support  in 36
- Norwegian road tunnels, Tunnelling and Underground Space Technology. 86 (2019), pp. 37
- 262-278. https://doi.org/10.1016/j.tust.2019.01.026. 38
- [148] X.  Liu,  W.  Liu,  Y .  Sang,  F.  Kong,  Research  on  failure  mechanism  of  cracked  lining 39
- reinforced with stacked inner lining, Chinese Journal of Rock Mechanics and Engineering. 40
- 34 (S2) (2015) 4244-4251 (in Chinese). https://doi.org/10.13722/j.cnki.jrme.2015.1001. 41
- [149] W.  Yu,  Y.  Sang,  Experimental  study  of  the  deformation  law  of  cracked  tunnel  lining 42
- reinforced by separated cover arch, Modern Tunnelling Technology. 51 (4) (2014) 141-149 43
- (in Chinese). https://doi.org/10.13807/j.cnki.mtt.2014.04.021. 44

- [150] Y. Hakoishi, H. Mashimo, T. Ishimura, S. Morimoto, A experimental study on load-carrying 1
2. capacity of tunnel with the damaged lining reinforced with inner concrete reinforcement 2
3. lining, in: PROCEEDINGS OF TUNNEL ENGINEERING, JSCE, Japan Society of Civil 3
4. Engineers, 2003, pp. 349-354 (in Japanese). https://doi.org/10.11532/journalte1991.13.349. 4
- [151] X. Liu, H. Lai, Y . Sang, Y . Zhang, Study on mechanics damage mechanism of arch surround 5
6. reinforced structure under loose load, in: IOP Conference Series: Earth and Environmental 6
7. Science, IOP Publishing, 2019, p. 022085. https://doi.org/10.1088/1755-1315/330/2/022085. 7
- [152] X.  Liu,  X.  Wang,  B.  He, Y .  Sang,  Model  test  of  cracked  tunnel  lining  reinforced  with 8

9

umbrella  arch  based  on  secondary  loading,  Journal  of  Sichuan  University  (Engineering

10

Science Edition).

47

(3)

(2015), pp.

21-28

(in Chinese).

- https://doi.org/10.15961/j.jsuese.2015.03.004. 11
- [153] Y. Liu, H. Lin, X. Li, Study on the method of reinforcing with compound cover arch in 12
- existing cracked tunnels, Highway. 63 (9) (2018), pp. 289-295 (in Chinese). 13
- http://w0d.cn/qp0e (Last accessed in March 12th, 2023). 14
- [154] F. Wang, Y. Liu, L. Wang, Detection and renovation for hazards in Chongqing Bayi Tunnel, 15
- Technology  of  Highway  and  Transport.  71  (2)  (2008),  pp.  112-116  (in  Chinese). 16
- https://doi.org/10.3969/j.issn.1009-6477.2008.02.031. 17
- [155] I. Laníková, P. Štěpánek, J. Venclovskỳ, Optimization of a tunnel lining reinforced with FRP, 18

19

in:

Key Engineering Materials, Trans Tech Publications,

2016, pp.

148-159.

- https://doi.org/10.4028/www.scientific.net/KEM.691.148. 20
- [156] Z. Wu, Y. Wu, M.F.M. Fahmy, 7 - Reinforcing spalling resistance of concrete structures with 21
- bonded  fiber-reinforced  polymer  composites,  in:  Z.  Wu, Y . Wu,  M.F.M.  Fahmy  (Eds.), 22
- Structures Strengthened with Bonded Composites, Woodhead Publishing, 2020, pp. 48123
524. https://doi.org/10.1016/B978-0-12-821088-8.00007-2 (ISBN 9780128210895). 24
- [157] Q. Wu, Y. Cai, Applying carbon fiber cloths to repair lining cracks in a double arched tunnel, 25

26

Modern Tunnelling Technology.

43

(6)

(2006), pp.

70-75

(in Chinese).

- https://doi.org/10.13807/j.cnki.mtt.2006.06.014. 27
- [158] Q. Ai, Y. Yuan, X. Bi, Acquiring sectional profile of metro tunnels using charge-coupled 28
- device cameras, Structure and Infrastructure Engineering. 12 (9) (2016), pp. 1065-1075. 29
- https://doi.org/10.1080/15732479.2015.1076855. 30
- [159] C. Yang, M. Huang, X. Liu, S. Wang, Effect of lining crack treatment using carbon fiber in 31
- deep buried tunnel, Journal of PLA University of Science and Technology (Natural Science 32
- Edition). 11 (3) (2010), pp. 322-327 (in Chinese). http://f6z.cn/sMsGI (Last accessed in 33
- March 12th, 2023). 34
- [160] Y.  Jiang, X. Wang, B. Li, Y . Higashi, K. Taniguchi, K. Ishida, Estimation of reinforcing 35
- effects  of  FRP-PCM  method  on  degraded  tunnel  linings,  Soils  and  Foundations.  57  (3) 36
- (2017), pp. 327-340. https:// doi.org/10.1016/j.sandf.2017.05.002. 37
- [161] FRP  Grid  Method  Association, Design and construction manual  of the repair  &amp; 38
- reinforcement method for RC structures by FRP grid. http://www.frp-grid.com/01.html (Last 39
- accessed in February 17th, 2023). 40
- [162] D. Liu, Q. Shang, M. Li, J. Zuo, Y. Gao, F. Xu, Cracking behaviour of tunnel lining under 41
- bias  pressure  strengthened  using  FRP  Grid-PCM  method,  Tunnelling  and  Underground 42
- Space Technology. 123 (2022) 104436. https://doi.org/10.1016/j.tust.2022.104436. 43
- [163] Y. Li, M. Wang, H. Xu, Y. Zhang, Numerical analysis of metro tunnel structure reinforced 44

- by fiber cloth material, China Civil Engineering Journal. 47 (8) (2014), pp. 138-144 (in 1
- Chinese). https://doi.org/10.15951/j.tmgcxb.2014.08.042. 2
- [164] Z. Liu, D. Zhang, The mechanism and effects of AFRP reinforcement for a shield tunnel in 3
- soft  soil,  Modern  Tunnelling  Technology.  51  (5)  (2014),  pp.  155-160  (in  Chinese). 4
- https://doi.org/10.13807/j.cnki.mtt.2014.05.024. 5
- [165] X. Liu, C. Zhang, C. Zhang, Z. Jiang, Experimental study on the longitudinal joint in shield 6
- tunnel reinforced with FRP material, Journal of Railway Science and Engineering. 13 (2) 7
- (2016), pp. 316-324 (in Chinese). https://doi.org/10.19713/j.cnki.43-1423/u.2016.02.018. 8
- [166] D.A.  Hensher, Fiber-reinforced-plastic (FRP)  reinforcement for concrete structures: 9

10

properties  and  applications,  in:  Elsevier,  2016.  https://doi.org/10.1016/C2009-0-09136-3

- (ISBN 978-0-444-89689-6). 11
- [167] D.A. Bournas, A. Pavese, W. Tizani, Tensile capacity of FRP anchors in connecting FRP and 12
- TRM sheets to concrete, Engineering Structures. 82 (2015), pp. 72-81. 13
- https://doi.org/10.1016/j.engstruct.2014.10.031. 14
- [168] H.  Huang,  L.  Xiao,  D.  Zhang,  J.  Zhang,  Influence  of  spatial  variability  of  soil Young's 15

16

modulus on tunnel convergence in soft soils, Engineering Geology. 228 (2017), pp. 357-370.

- https://doi.org/10.1016/j.enggeo.2017.09.011. 17
- [169] D. Zhang, W. Zou, J. Yan, Effective control of large transverse deformation of shield tunnels 18
- using grouting in soft deposits, Chinese Journal of Geotechnical Engineering. 36 (12) (2014), 19
- pp. 2203-2212 (in Chinese). https://doi.org/10.11779/CJGE201412007. 20
- [170] T. Zhao, T. Han, G. Wu, Y. Gao, Y. Lu, Effects of grouting in reducing excessive tunnel 21
- lining deformation: Field experiment and numerical modelling using material point method, 22

23

Tunnelling and Underground Space Technology.

116

(2021)

104114.

- https://doi.org/10.1016/j.tust.2021.104114. 24
- [171] H.F. Schweiger, C. Kummerer, R. Otterbein, E. Falk, Numerical modelling of settlement 25
- compensation by means of fracture grouting, Soils and Foundations. 44 (1) (2004), pp. 7126
86. https://doi.org/10.3208/sandf.44.71. 27
- [172] K. Soga, M.D. Bolton, S.K.A. Au, K. Komiya, J.P. Hamelin, A. Van Cotthem, G. Buchet, 28
- J.P.  Michel,  Development  of  compensation  grouting  modelling  and  control  system,  in: 29
- Proceedings  of  the  International  Symposium  on  Geotechnical  Aspects  of  Underground 30
- Construction in Soft Ground, Tokyo, Japan, 1999, pp. 425-430 (in Japanese). 31
- https://cir.nii.ac.jp/crid/1573668924848886784 (Last accessed in March 12th, 2023). 32
- [173] X. Xue, J. Zhang, G. Yao, Y . Gao, Study on mechanical property of highway tunnel lining 33
- grouting reinforcement, Journal of Highway and Transportation Research and Development. 34
- 34 (4) (2017), pp. 93-100. https://doi.org/10.3969/j.issn.1002-0268.2017.04.014. 35
- [174] D. Liu, F. Wang, Q. Hu, H. Huang, J. Zuo, C. Tian, D. Zhang, Structural responses and 36

37

treatments of shield tunnel due to leakage: A case study, Tunnelling and Underground Space

- Technology. 103 (2020) 103471. https://doi.org/10.1016/j.tust.2020.103471. 38
- [175] F. Wang, M. Zhou, D. Zhang, H. Huang, D. Chapman, Random evolution of multiple cracks 39
- and  associated  mechanical  behaviors  of  segmental  tunnel  linings  using  a  multiscale 40
- modeling method, Tunnelling and Underground Space Technology. 90 (2019), pp. 220-230. 41
- https://doi.org/10.1016/j.tust.2019.05.008. 42
- [176] J.  Zhang, K.K. Phoon, D. Zhang, H. Huang, C. Tang, Deep learning-based evaluation of 43
- factor of safety with confidence interval for tunnel deformation in spatially variable soil, 44

- Journal of Rock Mechanics and Geotechnical Engineering. 13 (6) (2021), pp. 1358-1367. 1
- https://doi.org/10.1016/j.jrmge.2021.09.001. 2
- [177] D. Zhang, Z. Liu, R. Wang, D. Zhang, Influence of grouting on rehabilitation of an over3
- deformed operating shield tunnel lining in soft clay, Acta Geotech. 14 (4) (2019), pp. 12274
1247. https://doi.org/10.1007/s11440-018-0696-8. 5
- [178] Z. Yang, X. Niu, K. Hou, Y . Guo, Z. Zhou, F. Chen, Y. Kang, Study on diffusion parameters 6
- of Bingham fluid based on column-hemispherical penetration grouting, Journal of Sichuan 7

8

University  (Engineering  Science  Edition).  47  (S2)  (2015),  pp.  47-53  (in  Chinese).

- https://doi.org/10.15961/j.jsuese.2015.s2.008. 9
- [179] Q.  Zhang,  L.  Zhang,  R.  Liu,  W.  Han,  M.  Zhu,  X.  Li,  D.  Zheng,  X.  Xu,  Laboratory 10
- experimental study of cement-silicate slurry diffusion law of crack grouting with dynamic 11

12

water, Rock and Soil Mechanics.

36

(8)

(2015), pp.

2159-2168

(in Chinese).

- https://doi.org/10.16285/j.rsm.2015.08.005. 13
- [180] J. Zou, L. Li, X. Yang, Z. Wang, C. He, Method of energy analysis for compaction grouting, 14
- Rock and Soil Mechanics. 27 (3) (2006), pp. 475-478 (in Chinese). 15
- https://doi.org/10.16285/j.rsm.2006.03.029. 16
- [181] C. Zhang, J. Fu, J. Yang, X. Ou, X. Ye, Y . Zhang, Formulation and performance of grouting 17
- materials  for  underwater  shield  tunnel  construction  in  karst  ground,  Construction  and 18
- Building Materials. 187 (2018), pp. 327-338. 19
- https://doi.org/10.1016/j.conbuildmat.2018.07.054. 20
- [182] T. Wu, Y. Gao, Y. Zhou, Application of a novel grouting material for prereinforcement of 21
- shield tunnelling adjacent to existing piles in a soft soil area, Tunnelling and Underground 22
- Space Technology. 128 (2022) 104646. https://doi.org/10.1016/j.tust.2022.104646. 23
- [183] S.  Li,  P.  Wang,  C.  Yuan,  J.  Li,  P.  Ma,  B.  Zhi,  H.  Zhou,  Y .  Tian,  Adaptability  of 24
- polyurethane/water  glass  grouting  reinforcement  to  subsea  tunnels,  Construction  and 25
- Building Materials. 311 (2021) 125354. https://doi.org/10.1016/j.conbuildmat.2021.125354. 26
- [184] J.  Liu,  O.  Hamza,  K.S.  Davies-V ollum,  J.  Liu,  Repairing  a  shield  tunnel  damaged  by 27
- secondary grouting, Tunnelling and Underground Space Technology. 80 (2018), pp. 31328
321. https://doi.org/10.1016/j.tust.2018.07.016. 29
- [185] Z. Saleheen, R.R. Krishnamoorthy, A. Nadjai, A review on behavior, material properties and 30
- finite element simulation of concrete tunnel linings under fire, Tunnelling and Underground 31
- Space Technology. 126 (2022) 104534. https://doi.org/10.1016/j.tust.2022.104534. 32
- [186] S. Sony, K. Dunphy, A. Sadhu, M. Capretz, A systematic review of convolutional neural 33
- network-based  structural  condition  assessment  techniques,  Engineering  Structures.  226 34
- (2021) 111347. https://doi.org/10.1016/j.engstruct.2020.111347. 35
- [187] D. Ai, G. Jiang, S.K. Lam, P. He, C. Li, Computer vision framework for crack detection of 36
- civil  infrastructure-A  review,  Engineering  Applications  of  Artificial  Intelligence.  117 37
- (2023) 105478. https://doi.org/10.1016/j.engappai.2022.105478. 38
- [188] T. Hao, C.D.F. Rogers, N. Metje, D.N. Chapman, J.M. Muggleton, K.Y. Foo, P. Wang, S.R. 39
- Pennock, P.R. Atkins, S.G. Swingler, J. Parker, S.B. Costello, M.P.N. Burrow, J.H. Anspach, 40
- R.J. Armitage, A.G.  Cohn,  K.  Goddard,  P.L.  Lewin,  G.  Orlando,  M.A.  Redfern, A.C.D. 41
- Royal, A.J. Saul, Condition assessment of the buried utility service infrastructure, Tunnelling 42
- and Underground Space Technology. 28 (2012), pp. 331-344. 43
- https://doi.org/10.1016/j.tust.2011.10.011. 44

- [189] S. Sajid, L. Chouinard, Impulse response test for condition assessment of concrete: A review, 1
2. Construction and Building Materials. 211 (2019), pp. 317-328. 2 https://doi.org/10.1016/j.conbuildmat.2019.03.174. 3

4

1

Appendix 1 Literature reviews for defect detection methods in infrastructures

| 2 References          |   Year | Subject of investigation               | Method                                                           | Major findings and remarks                                                                                                                                                                                                                                                                                                                                    |
|-----------------------|--------|----------------------------------------|------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Feng and Feng [16]    |   2018 | Civil infrastructure defects           | Computer vision                                                  | The paper presents general principles of the vision sensor systems, introduces the performance evaluation experiments of vision sensors and the application of displacement measurement data for SHM. Vision sensors still need improvements in accuracy, resolution and robustness.                                                                          |
| Koch et al. [19]      |   2015 | Civil infrastructure defects           | Computer vision                                                  | The paper reviews computer vision-based methods for defect detection and condition assessment. In precast concrete tunnels, data collection and location detection of defects are fully automated. Poor lighting conditions, irregularly patterned background and contrast as well as limited data quality and quantity impose the most significant problems. |
| Attard et al. [10]    |   2018 | Tunnel defects                         | Photogrammetric techniques, image processing and computer vision | This review summarizes the state of the art in vision-based automation technologies used in different tunnel inspection procedures and presents a comprehensive review focusing on image-based tunnel inspection.                                                                                                                                             |
| Hsieh and Tsai [18]   |   2020 | Structure cracks                       | Machine Learning                                                 | The author organizes and provides up-to-date information on the research of ML-based crack detection algorithms, and reviews 68 ML-based crack detection papers in detail to identify the current development trend. A performance evaluation system should be established to qualitatively and objectively evaluate crack detection algorithms.              |
| McCann and Forde [21] |   2001 | Concrete and masonry structure defects | NDT methods                                                      | As a highly representative review, it reviews a wide range of NDT techniques applied to bridges and buildings. The author describes five major factors that influence the success of a survey: depth of penetration, vertical and lateral resolution, contrast in physical properties, signal-to-noise ratio and existing information about the structure.    |
| Lai et al. [22]       |   2018 | Civil engineering defects              | GPR                                                              | This paper reviews the latest development of the GPR's primary infrastructure applications. Different types of tunnel linings can be surveyed by GPR, except shotcrete containing steel fibers. The air-coupled GPR can indicate areas of high moisture or low density (high air voids), while ground-                                                        |

| Schabowicz [23]                                                                                                                                                                                                                                                             | 2015 Concrete defects                                                                                                                                                                                                                                                       |                                                                                                                                                                                                                                                                             | structure Acoustic techniques                                                                                                                                                                                                                                               | coupled GPR can possibly detect defects at different cover depths within or just behind the tunnel linings. This paper introduces modern acoustic techniques to detect unilaterally accessible concrete structures. A combination of the impulse response technique and ultrasonic tomography is recommended for identifying and locating zones of concrete macroheterogeneities. A combination of nondestructive techniques using ultrasonic tomography and impact-echo is then recommended to determine the depth of cracks. These methods have been validated in situ.   |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Montero et al. [24]                                                                                                                                                                                                                                                         | 2015                                                                                                                                                                                                                                                                        | Tunnel defects                                                                                                                                                                                                                                                              | Robotic inspection system                                                                                                                                                                                                                                                   | The paper presents the key aspects of tunnel inspection and a survey of the developed robotic tunnel inspection systems to date. It is still very difficult for robots to perform fully automated tunnel inspections. In addition, factors such as communication, data transmission, data quality, and objectivity also need to be considered.                                                                                                                                                                                                                              |
| 1 2 3 4                                                                                                                                                                                                                                                                     | Appendix 2                                                                                                                                                                                                                                                                  | Appendix 2                                                                                                                                                                                                                                                                  | Literature reviews for structural condition assessment methods of tunnel overall                                                                                                                                                                                            | Appendix 2                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| References Year Subjects Major findings and remarks                                                                                                                                                                                                                         | References Year Subjects Major findings and remarks                                                                                                                                                                                                                         | References Year Subjects Major findings and remarks                                                                                                                                                                                                                         | References Year Subjects Major findings and remarks                                                                                                                                                                                                                         | References Year Subjects Major findings and remarks                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| Numerical simulation methods for damage assessment                                                                                                                                                                                                                          | Numerical simulation methods for damage assessment                                                                                                                                                                                                                          | Numerical simulation methods for damage assessment                                                                                                                                                                                                                          | Numerical simulation methods for damage assessment                                                                                                                                                                                                                          | Numerical simulation methods for damage assessment                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| [185] 2022 Evaluation elevated temperatures are shown in this review, which                                                                                                                                                                                                 | [185] 2022 Evaluation elevated temperatures are shown in this review, which                                                                                                                                                                                                 | [185] 2022 Evaluation elevated temperatures are shown in this review, which                                                                                                                                                                                                 | [185] 2022 Evaluation elevated temperatures are shown in this review, which                                                                                                                                                                                                 | [185] 2022 Evaluation elevated temperatures are shown in this review, which                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| Saleheen et al. behaviour and material properties of concrete at is useful for researchers modelling tunnel linings under fire. The article reviews the implementation of convolutional neural networks (CNNs) in structural health monitoring. The authors have provided a | Saleheen et al. behaviour and material properties of concrete at is useful for researchers modelling tunnel linings under fire. The article reviews the implementation of convolutional neural networks (CNNs) in structural health monitoring. The authors have provided a | Saleheen et al. behaviour and material properties of concrete at is useful for researchers modelling tunnel linings under fire. The article reviews the implementation of convolutional neural networks (CNNs) in structural health monitoring. The authors have provided a | Saleheen et al. behaviour and material properties of concrete at is useful for researchers modelling tunnel linings under fire. The article reviews the implementation of convolutional neural networks (CNNs) in structural health monitoring. The authors have provided a | Saleheen et al. behaviour and material properties of concrete at is useful for researchers modelling tunnel linings under fire. The article reviews the implementation of convolutional neural networks (CNNs) in structural health monitoring. The authors have provided a                                                                                                                                                                                                                                                                                                 |
| et al. [186] 2021 Detection and evaluation detailed analysis and discussion of the current state                                                                                                                                                                            | et al. [186] 2021 Detection and evaluation detailed analysis and discussion of the current state                                                                                                                                                                            | et al. [186] 2021 Detection and evaluation detailed analysis and discussion of the current state                                                                                                                                                                            | et al. [186] 2021 Detection and evaluation detailed analysis and discussion of the current state                                                                                                                                                                            | et al. [186] 2021 Detection and evaluation detailed analysis and discussion of the current state                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| and problems of research on structural condition                                                                                                                                                                                                                            | and problems of research on structural condition                                                                                                                                                                                                                            | and problems of research on structural condition                                                                                                                                                                                                                            | and problems of research on structural condition                                                                                                                                                                                                                            | and problems of research on structural condition                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| Sony                                                                                                                                                                                                                                                                        | Sony                                                                                                                                                                                                                                                                        | Sony                                                                                                                                                                                                                                                                        | Sony                                                                                                                                                                                                                                                                        | Sony                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| assessment based on CNNs. The challenges and                                                                                                                                                                                                                                | assessment based on CNNs. The challenges and                                                                                                                                                                                                                                | assessment based on CNNs. The challenges and                                                                                                                                                                                                                                | assessment based on CNNs. The challenges and                                                                                                                                                                                                                                | assessment based on CNNs. The challenges and                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| solutions to structural condition assessment need to be                                                                                                                                                                                                                     | solutions to structural condition assessment need to be                                                                                                                                                                                                                     | solutions to structural condition assessment need to be                                                                                                                                                                                                                     | solutions to structural condition assessment need to be                                                                                                                                                                                                                     | solutions to structural condition assessment need to be                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| studied in depth.                                                                                                                                                                                                                                                           | studied in depth.                                                                                                                                                                                                                                                           | studied in depth.                                                                                                                                                                                                                                                           | studied in depth.                                                                                                                                                                                                                                                           | studied in depth.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| A review of vision-based crack detection and                                                                                                                                                                                                                                | A review of vision-based crack detection and                                                                                                                                                                                                                                | A review of vision-based crack detection and                                                                                                                                                                                                                                | A review of vision-based crack detection and                                                                                                                                                                                                                                | A review of vision-based crack detection and                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| assessment methods. Although the main subject of                                                                                                                                                                                                                            | assessment methods. Although the main subject of                                                                                                                                                                                                                            | assessment methods. Although the main subject of                                                                                                                                                                                                                            | assessment methods. Although the main subject of                                                                                                                                                                                                                            | assessment methods. Although the main subject of                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| Ai et al. [187] 2023 Detection and evaluation                                                                                                                                                                                                                               | Ai et al. [187] 2023 Detection and evaluation                                                                                                                                                                                                                               | Ai et al. [187] 2023 Detection and evaluation                                                                                                                                                                                                                               | Ai et al. [187] 2023 Detection and evaluation                                                                                                                                                                                                                               | Ai et al. [187] 2023 Detection and evaluation                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| this paper is cracks, it is still helpful in assessing the                                                                                                                                                                                                                  | this paper is cracks, it is still helpful in assessing the                                                                                                                                                                                                                  | this paper is cracks, it is still helpful in assessing the                                                                                                                                                                                                                  | this paper is cracks, it is still helpful in assessing the                                                                                                                                                                                                                  | this paper is cracks, it is still helpful in assessing the                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |

| Alsharqawi et al. [27]    | Alsharqawi et al. [27]                                       | 2022                                                         | Detection and evaluation                                     | Detection and evaluation                                                                                                                                                                                                                                                                                                                                                                                                                                                   | This paper describes the current state of knowledge on the use of ground penetrating radar (GPR) to assess concrete structures. Based on the inadequacy of current studies, it is recommended that research directions should be focused on in the future. Further research is expected on data processing and the selection of assessment indicators.                                                                                                                     |
|---------------------------|--------------------------------------------------------------|--------------------------------------------------------------|--------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Hao et al. [188]          | Hao et al. [188]                                             | 2012                                                         | Evaluation                                                   | Evaluation                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | This paper provides an overview of various condition assessment techniques for buried utility services. Challenges remain in resolving the weaknesses of different assessment techniques                                                                                                                                                                                                                                                                                   |
| Sajid and Chouinard [189] | Sajid and Chouinard [189]                                    | 2019                                                         | Detection and evaluation                                     | Detection and evaluation                                                                                                                                                                                                                                                                                                                                                                                                                                                   | The first review of the researches related to the impulse response test. The basic principles and issues faced in impulse response test-based evaluation techniques are summarized. The authors have identified current knowledge gaps and provided recommendations to overcome the issues.                                                                                                                                                                                |
| 1                         | 1                                                            | 1                                                            | 1                                                            | 1                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | 1                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| 2 3 4                     | Appendix 3 Literature reviews for tunnel lining retrofitting | Appendix 3 Literature reviews for tunnel lining retrofitting | Appendix 3 Literature reviews for tunnel lining retrofitting | Appendix 3 Literature reviews for tunnel lining retrofitting                                                                                                                                                                                                                                                                                                                                                                                                               | Appendix 3 Literature reviews for tunnel lining retrofitting                                                                                                                                                                                                                                                                                                                                                                                                               |
| References                | Year                                                         | Year                                                         | Subjects                                                     | Major findings and remarks                                                                                                                                                                                                                                                                                                                                                                                                                                                 | Major findings and remarks                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| Asakura and Kojima [31]   | 2003                                                         | 2003                                                         | Tunnel detection Retrofitting                                | The paper summarizes the inspection and retrofitting methods actually used for railway tunnels in Japan. Moreover, three cases are shown: one of them is the Tukayama tunnel concerning countermeasures against plastic earth pressure and the others are the Fukuoka tunnel and the Rebunhama tunnel concerning an accident caused by spalling of tunnel lining.                                                                                                          | The paper summarizes the inspection and retrofitting methods actually used for railway tunnels in Japan. Moreover, three cases are shown: one of them is the Tukayama tunnel concerning countermeasures against plastic earth pressure and the others are the Fukuoka tunnel and the Rebunhama tunnel concerning an accident caused by spalling of tunnel lining.                                                                                                          |
| Richards [32]             | 1998                                                         | 1998                                                         | Tunnel detection Retrofitting                                | The paper briefly summarizes tunnel detection and retrofitting methods but lacks a detailed description of the development and application of retrofitting methods, including their advantages and disadvantages. The results demonstrate that the design of tunnel structures should take account of new inspection technologies, thereby reducing costs of inspections and disruptions as well as providing for more cost-effective preventative maintenance and repair. | The paper briefly summarizes tunnel detection and retrofitting methods but lacks a detailed description of the development and application of retrofitting methods, including their advantages and disadvantages. The results demonstrate that the design of tunnel structures should take account of new inspection technologies, thereby reducing costs of inspections and disruptions as well as providing for more cost-effective preventative maintenance and repair. |
| Ye et al. [33]            | 2021                                                         | 2021                                                         | Tunnel defects Retrofitting                                  | This paper describes the application of tunnel retrofitting technology in China and examines five characteristics of tunnel defects. In turn, feasible defect prevention and treatment procedures were proposed.                                                                                                                                                                                                                                                           | This paper describes the application of tunnel retrofitting technology in China and examines five characteristics of tunnel defects. In turn, feasible defect prevention and treatment procedures were proposed.                                                                                                                                                                                                                                                           |

| Sousa et al. [34]   |   2009 | Tunnel retrofitting                    | This paper presents a technique for modeling decisions under uncertainty, BN, and their 'extension' to Influence Diagrams. An example applied to the maintenance of tunnels was presented, with the intent of illustrating the advantages and potential of this technique when applied to real problems.                            |
|---------------------|--------|----------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Rock et al. [35]    |   2006 | Tunnel retrofitting Evaluation         | Methods for maintaining, renovating, and improving road tunnels are outlined, including assessments of potential threats and vulnerabilities. The results demonstrate that tunnel cracking is the most damaging condition to the structural performance of a tunnel                                                                 |
| Liu and Zhu [36]    |   2005 | Tunnel defects Retrofitting            | An in-depth analysis of the causes of the defects is conducted for the double-arch tunnel. Appropriate preventive and corrective actions are then proposed to address the issue.                                                                                                                                                    |
| Luo and Chen [37]   |   2019 | Tunnel defects Retrofitting            | An evaluation of the current state and advancement of tunnel damage was conducted, and a thorough analysis of the key measures for preventing and managing frost damage was performed. The results demonstrate that the current theoretical model for tunnel assessment is not very accurate and needs further development.         |
| Feng et al. [38]    |   2019 | Tunnel defects Retrofitting            | The paper presents a case study of the sidewall cracking problem in an existing tunnel and proposes a solution to the problem verified by numerical analysis. The results demonstrate that groundwater has weakened the physical and mechanical properties of the surrounding rock and is the main cause of tunnel wall cracking.   |
| Ye et al. [39]      |   2020 | Tunnel defects Retrofitting Evaluation | The paper investigates the occurrence of tunnel lining defects in the G312 Liupanshan Highway Tunnel in Guyuan City and analyzes the damage characteristics, occurrence mechanisms, and reinforcement methods by combining external and internal causes.                                                                            |
| Zhang et al. [40]   |   2020 | Tunnel defects Retrofitting            | This paper presents the retrofitting methods and the design principles for repairing tunnels damaged by earthquakes, taking the Tawarayama Tunnel as a case study. The results demonstrate that spalling/collapse of liners due to ground vibrations and groundwater leaks have a significant impact on the design of retrofitting. |
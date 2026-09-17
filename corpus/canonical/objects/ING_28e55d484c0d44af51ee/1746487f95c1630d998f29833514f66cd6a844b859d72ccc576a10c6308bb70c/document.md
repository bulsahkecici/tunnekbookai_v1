## Accurate Mapping of Subterranean Structures with Mobile Phones

Martin Rehak 1 , Davide Cucci 1 , Jean-Baptiste Magnin 1 , Christoph Strecha 1

1 PIX4D SA. Route de Renens 24 1008 Prilly, Switzerland (firstname.lastname@PIX4D.com)

Keywords: GSW 2025, iPhone, LiDAR, RTK, GNSS, Surveying, Underground

## Abstract

Accurate mapping of subterranean structures, particularly tunnels, is vital for infrastructure maintenance, safety inspections, and urban planning. Traditional methods such as total stations, LiDAR (Light Detection and Ranging), and Ground-Penetrating Radar (GPR) offer high precision but come with significant financial, logistical, and technical constraints. This paper presents a novel, costeffective approach to underground structure mapping using the Emlid RX RTK (Real-Time Kinematic) GNSS (Global Navigation Satellite System) rover and the PIX4Dcatch mobile application, leveraging the capabilities of modern smartphones. By integrating GNSS RTK signals, photogrammetry algorithms, and the PIX4D AutoTag technology, the proposed method offers an accessible solution for accurate mapping in areas with limited GNSS signal availability. We demonstrate the feasibility of this method in real-world scenarios, highlighting its potential for enhancing productivity, scalability, and accuracy. This study also addresses the challenges of underground environments, such as poor lighting and sensor navigation, and suggests best practices for mobile phonebased mapping. Our results aim to provide a practical, affordable alternative to traditional tunnel mapping techniques, making them more accessible to users with limited photogrammetric knowledge.

## 1. Introduction

Accurate mapping of subterranean structures, particularly tunnels, is crucial for a wide range of applications, including infrastructure maintenance, safety inspections, urban planning, and archaeological exploration. Traditional methods of tunnel mapping, such as using total stations, LiDAR systems, and GPR, though precise, often present significant logistical, financial, and technical challenges. These methods typically require specialized equipment, trained personnel, and substantial time investments, which can be prohibitive for frequent or large-scale surveys.

## 1.1 Current Methods for Tunnel Mapping

In recent years, precise instruments like robotic total stations and distance meters, as well as advanced technologies such as GPR, and SLAM-empowered scanners (Simultaneous Localization and Mapping), have been introduced for underground surveying (Deshpande, 2021). Handheld laser scanners, such as the Leica BLK2GO (Leica Geosystems, 2024) or Faro GeoSLAM ZEB Horizon RT (Faro, 2024), equipped with SLAM technology, provide real-time data acquisition. However, these handheld laser scanners are relatively costly and can suffer from drift if not used with a sufficient number of Ground Control Points (GCPs). Establishing accurate references for georeferencing the data or for accuracy control, in the form of check points, is a time consuming task requiring a total station due to the lack of GNSS signal in tunnels.

This paper presents a novel approach for subterranean structure mapping, leveraging the Emlid REACH RX RTK GNSS rover (Emlid, 2024b) and the PIX4Dcatch app (Pix4D, 2024) on a mobile phone to create precise as-built models. The system is depicted in Fig. 1. This method promises to simplify workflows, improve productivity and scalability, enhance accuracy, and offer significant economic benefits.

Modern smartphones are equipped with high-resolution cameras, sophisticated sensors, and powerful processing capabilities, enabling them to perform tasks that were once reserved for dedicated equipment. This technological advancement has spurred interest in leveraging mobile phones for geospatial data collection and mapping, including in complex environments like tunnels or other subterranean structures. State-of-the-art photogrammetry algorithms allow extending the accuracy from areas with good GNSS signal reception to areas without, as demonstrated in (Strecha et al., 2024a) and (Strecha et al., 2024b).

Figure 1. PIX4Dcatch app on the left, Emlid Reach RX with an iPhone 14 Pro on the right.

<!-- image -->

Photograph

## 1.2 Challenges of Subterranean Mapping

Mapping subsurface areas presents several challenges. One major issue is navigation and sensor orientation, which involves determining the positions and orientations of sensors.

Due to the lack of GNSS signals, navigation systems often rely on dead reckoning. LiDAR sensors require a large number of accurately measured GCPs, while some mapping systems use camera sensors to perform SLAM or visual odometry.

Tunnels and cluttered spaces typically suffer from poor lighting conditions, making photogrammetry and, in particular, Structure From Motion (SFM) processing difficult or impossible. Therefore, active systems such as LiDAR are preferred by professionals for documentation and inspection tasks. It is, in principle, possible to use photogrammetry algorithms for 3D reconstruction in these areas, as demonstrated in several studies, see for example, (Perfetti et al., 2022), (Chapman et al., 2016), (Janiszewski et al., 2022). However, the challenges include poor scene lighting, large variations in scale and contrast, homogeneity of the mapped surfaces, and common sensor orientation issues.

## 1.3 Objectives

In this paper we present an affordable method for accurate mapping of tunnels and other cluttered space with limited access to the GNSS signal. This is achieved by a combination of AutoTags (Strecha et al., 2024b), the Geofusion sensor fusion algorithm (see Sec. 2.4.1 later on), GNSS RTK signals in open-space sections and SFM processing. Indeed, there is lots of tunnels serving to pedestrians for road crossing, areas such as train or metro stations that require regular maintenance and inventory documentation. The accuracy required for this type of work varies by country and industry but often falls within the range of 1 σ = 10 cm (Ali, 2006), (Mattock, 2018). We aim at showing a workflow that can be easily followed by people with limited photogrammetric or surveying knowledge and demonstrate our method on a realistic scenario. Indeed, many regions report a shortage of surveyors, engineers, and general workers, causing project delays and higher costs (HLR, 2023). To improve scalability and cost-effectiveness, it's beneficial to assign certain scanning tasks to general workers rather than hiring surveyors. This approach leverages the existing workforce, reducing costs and integrating mapping tasks into the daily workflow, allowing projects to progress without waiting for surveyor availability. The presented software and hardware equipment is readily available on the market and does not require any further development.

The objectives of this research are twofold: first, to evaluate the accuracy of subterranean maps produced using mobile phones; second, to identify the practical challenges and limitations associated with mobile phone-based mapping in subterranean environments. Through a series of experiments, we aim to validate the absolute and relative accuracy of the 3D reconstruction, the effectiveness of mobile phone-based tunnel mapping and provide a framework for future applications.

By exploring the potential of mobile phones as viable tools for subterranean mapping, this study seeks to contribute to the growing body of knowledge in geospatial science and engineering. It also aims to offer practical insights for professionals in the field, presenting an innovative, cost-effective, and accessible alternative to traditional infrastructure surveying techniques.

## 2. Case Study

This section will cover the selected location, equipment, and data acquisition methodology, followed by a discussion on data processing.

Figure 2. Tunnel in Pr´ everenges. Narrow, dark, high contrast, and big differences in scale make photogrammetric processing very challenging.

<!-- image -->

Photograph

## 2.1 Test site

For this study, a tunnel has been selected to represent a typical structure that requires frequent and regular inspections and maintenance. Located in Pr´ everenges, Switzerland, the tunnel serves as a pedestrian underpass beneath a road connecting Lausanne and Morges. It is approximately 30 mlong and has a diameter of 3 m. The tunnel provides a safe passage for pedestrians and is equipped with lighting to enhance visibility and safety at night, see Fig. 2. However, the limited lighting poses a challenge for photogrammetric data processing, further complicated by its narrow profile.

## 2.2 Equipment used

The mobile mapping system used in this study was an iPhone 14 Pro (Apple, 2024b) with the Emlid Reach RX RTK rover, rigidly attached to the phone via a handle. The GNSS rover provides centimeter-level accuracy through RTK corrections. The PIX4Dcatch mobile application was used to establish interaction between the RTK adapter and the mobile device.

The system was equipped with a custom-built external lighting system to enhance data capture inside tunnels. Although this addition is not necessary in well-lit areas, it improves image quality and the iPhone's tracking capabilities in low-light environments. Its range is somewhat limited, but it still contributes significantly to the overall performance in such

conditions.

The reference points inside of the tunnel were surveyed with the robotic total station Topcon GT-1200/600 (Topcon, 2024). Points outside of the tunnel were measured with long GNSS RTK observations using a tripod and the Emlid Reach RS3 GNSS receiver (Emlid, 2024a). In total, 29 points were surveyed with the accuracy of 1 σ = 1.5 cm in each axis. The measured points were materialized using survey nails in the tarmac and reflective stickers on the tunnel walls, see Fig. 3.

Figure 3. 29 check points (in blue) in the tunnel located in Pr´ everenges, Switzerland.

<!-- image -->

Engineering drawing

PIX4Dcatch was used to capture geospatial data in the field. The collected data, including both images and LiDAR, was then transferred to PIX4Dmatic for desktop processing. In PIX4Dmatic, photogrammetric processing was performed, transforming the input data, images and LiDAR, into a dense point cloud, 3D mesh, Digital Surface Model (DSM), and orthomosaic.

## 2.3 Data Acquisition

To determine the most suitable scanning pattern for the tunnel environment, several capturing techniques were evaluated. These patterns were evaluated based on accuracy, ease of use, and adaptability to the unique geometry of the tunnel.

A total of 10 AutoTag targets were evenly distributed throughout the tunnel. These points play an important role in ensuring accurate mapping with PIX4Dcatch in difficult scenarios. First, the points are detected in real-time by PIX4Dcatch, and this information is integrated with additional data from the phone's sensors and the GNSS RTK receiver, see Sec. 2.4.1 later on. Secondly, each target contains a set of 5 identifiable points. These image observations serve as manual tie-points (MTP's) during post-processing, although in this case they are automatically extracted. Those MTP's significantly improve precision and accuracy while mitigating the creation of double layers or other common artifacts in point clouds or meshes. The key features of AutoTags are the following:

- The AutoTags are detected in real-time during data acquisition, enabling efficient and immediate feedback.
- The 3D position of the AutoTags does not need to be known in advance, simplifying setup.
- Drift compensation is performed automatically on the mobile device, with corrections applied within seconds after data collection is complete.
- The AutoTags are uniquely coded, and can be used to align multiple scans with each other, ensuring consistency and accuracy across different scans or sections of the scanned scene.

Concerning the quality of the GNSS signal, the percentage of images with RTK fix accuracy in each dataset ranged between 10% and 15%.

This approach, combining real-time detection with post-processing capabilities, ensures high-quality data capture in complex environments like tunnels, where maintaining accurate positioning is challenging.

2.3.1 Scanning Patterns Several scanning patterns were evaluated for their effectiveness in capturing the tunnel environment. These patterns were assessed based on the overall model completeness, image quality, and the ability to minimize artifacts during reconstruction. Secondly, the pattern yielding the best results in terms of model completeness was executed four more times on different days, with AutoTags distributed in various locations to test the repeatability of this method.

The following scanning patterns were evaluated:

1. Single direction with straight pattern: The camera moves in one direction, facing forward throughout the scan. This pattern results in the fewest number of images and reduces the likelihood of introducing double-layer artifacts during reconstruction, as the coverage is linear and minimal overlapping occurs. However, it provides minimal or no redundancy.
2. Single direction with spiral pattern: In this approach, the camera is tilted and rotated in a spiral motion while moving in a single direction, ensuring that all sides of the tunnel are captured. This pattern enhances coverage but may increase the number of images and processing time compared to the single direction pattern. Additionally, this pattern is more sensitive to rotational movement, which can lead to image blur if the rotation is not smooth or is too fast.
3. Double direction with straight pattern: The camera moves back and forth through the tunnel, tilted to one side, with an overlapping region created in the center between the two passes. This pattern increases redundancy and provides better coverage, especially for areas that might be missed in a single pass.
4. Double direction with spiral pattern: The camera follows a spiral scanning motion while moving back and forth through the tunnel. This pattern provides the most comprehensive coverage but requires the highest number of images, potentially increasing the chances of over-sampling and prolonging processing time.

## 2.4 Data Processing

Data processing was carried out using PIX4Dmatic desktop software, which offers advanced functionalities for integrating additional points, such as GCPs, check points, and MTPs. The software also allows for extensive customization of the processing workflow, ensuring adaptability to specific project requirements. All processing results can be visualized and further analyzed. For instance, a section cut of the point cloud as generated by the software is depicted in Fig. 4.

The check points were manually marked in the images within PIX4Dmatic, and their accuracy was automatically assessed by the software. It is important to note that these points do not influence the processing in any way. Their image observations

Figure 4. Screen capture of PIX4Dmatic showing the side profile view of the tunnel. Major grid cell: 10 × 10 m, minor grid cell: 1 × 1 m.

<!-- image -->

Photograph

were not used during the SFM. This mapping technique is part of the integrated sensor orientation (Rehak and Skaloud, 2016), and the mapping accuracy is determined solely by the precision of the image geotags.

It is also possible to use some of the check points as GCPs, for example the ones located outside the tunnel, easily measurable with the already employed GNSS rover, together with the AutoTags during the SFM processing. The resulting processing workflow benefits from enhanced accuracy and reliability, reducing potential distortions and ensuring that the final model is as precise as possible, without requiring additional hardware.

2.4.1 Accuracy of Geotags In this section we detail the method of fusing data coming from the GNSS RTK rover and the mobile phone sensors.

The images acquired with PIX4Dcatch are tagged with the estimated position and orientation of the cameras, together with the related uncertainty. These quantities are estimated at the end of the capture by a proprietary sensor fusion algorithm, called Geofusion.

During an outdoor acquisition, PIX4Dcatch records multiple measurement streams:

1. The position fixes from the external GNSS receiver,
2. The position and orientation of the camera provided in real-time by the onboard augmented reality framework. On Apple devices, PIX4Dcatch relies on ARKit (Apple, 2024a).
3. The image coordinates of the corners of the AutoTags detected in real time by PIX4D proprietary detector.

These streams provide partially redundant and indirect information on the camera position and orientation. They may contain errors and/or be unavailable in certain sections of the capture. The first stream provides an estimation of the receiver antenna position (which is offset with respect to the camera by a know lever-arm) with cm-level accuracy (when the ambiguities are fixed) and with respect to a global reference frame. It is not always available, such as indoor, and may contain errors, for instance due to multipath effects. ARKit estimates the position and orientation of the camera relative to the beginning of the capture, also suffering from drift and other artifacts, especially if the visual content of the scene is scarce. In order to meet the tight computational constraints required to ensure real-time operation, ARKit can keep localizing only with respect to a small map and it often fails to re-localize with respect to parts of the scene visited in the past, as it frequently happens in the double direction capturing patterns. PIX4D AutoTags, a fine tuned design of the AprilTag category (Wang and Olson, 2016), provide the missing loop-closure information if appropriately placed along the capture path. They are detected in real-time in order to provide visual feedback to the user and the image coordinates of the tag corners are made available to Geofusion after the capture.

In order to integrate all the aforementioned streams together and estimate the geotags for the images, Geofusion solves a modified bundle adjustment problem, similar to the one presented in (Cucci et al., 2017). The algorithm minimizes the reprojection error of the tag corners as a function of the geotags, also taking into account the two available camera pose priors derived from i) from the GNSS position fixes and ii) the ARKit relative camera poses. The lightweight formulation of the estimation problem allows the algorithm to run in few seconds at worst on the mobile phone. In order to effectively identify and reject measurements outliers, sophisticated stochastic models for all residual terms have been developed to account for heavy tailed distributions and time correlation in the noise terms. These models have been tailored for PIX4Dcatch based on extensive field testing in different real-world conditions.

In Figure 5, it is possible to see an example of the position error of the camera geotags for one of the acquisition considered in the repeatability evaluation, see Sec. 3.2. It is possible to see that Geofusion corrects the substantial drift visible in the original ARKit solution (displayed in green) thanks to the fusion of the additional information coming from the RTK position fixes (outside the tunnel) and AutoTags, achieving dm-level position error on the entire dataset. The uncertainty of the Geofusion position estimate is also displayed in shaded red (one σ bounds). It is possible to see that the uncertainty is higher within the tunnel, as expected, and that the actual error is approximately consistent with the estimated uncertainty. The ground truth trajectory has been obtained in PIX4Dmatic by processing the data using all available check points as GCPs.

The geotags estimated by Geofusion after the capture provide the prior information on camera positions and orientation that is used in postprocessing by the SFM algorithms in PIX4Dmatic.

## 3. Evaluation

## 3.1 Assessing Various Scanning Patterns

This section evaluates the most suitable scanning patterns in terms of point cloud completeness and the presence of artifacts. As described in Sec. 2.3.1, four different scanning patterns were tested. All projects were conducted on the same day, under identical conditions, with the same distribution of AutoTags.

The completeness of the point clouds was visually assessed in Image #

<!-- image -->

Line chart

Figure 5. Position error of the image geotags computed by Geofusion, of the RTK position and of the ARKit solution with respect to the reference for RUN A in Table 1.

<!-- image -->

Photograph

Figure 6. Visual comparison of the fused point clouds (dense point cloud + LiDAR) for the four scanning patterns detailed in Sec. 2.3.1.

PIX4Dmatic by comparing specific regions of the tunnel across different scans. The results indicate that scanning in two directions (back and forth) produced more complete point clouds compared to single-direction scans. This is expected, as certain objects are occluded or not visible when scanned from only one direction. Fig. 6 illustrates these differences.

Although the difference between the oblique and spiral scanning methods was less pronounced, it remains significant. The oblique method provided better coverage of certain tunnel features, such as the floor, while the spiral method was slightly more consistent in reducing occlusions.

The single direction scanning method, particularly the one with a slightly tilted forward-facing camera, is well-suited for mapping the tunnel floor, such as for inspecting the tarmac. However, the tunnel's sides require additional images to achieve adequate coverage. This highlights the importance of selecting a scanning approach based on the project's goals. For instance, if the focus is on visual inspection where the original 2D images provide most of the content, and the point cloud is used mainly for navigation, a simpler scanning method may suffice. On the other hand, if an accurate 3D model is needed for purposes like Building Information Modeling (BIM), a more thorough scanning strategy is required to generate a complete and precise point cloud or mesh.

## 3.2 Assessment of Repeatability

As detailed in Sec. 3.1, the double-direction spiral pattern produced the most complete results, yielding a point cloud without artifacts. The tunnel was then scanned four times on different days with varying AutoTag placements using this pattern. The acquisitions were processed in PIX4Dmatic, and the accuracy of the 3D reconstruction was evaluated using 29 check points. No GCPs were used during the processing. The results are summarized in Tab. 1. It can be seen that the overall accuracy expressed as the Root Mean Square (RMS) error per axis is at cm-level level.

In Figure 7 the 3D norm of the check point errors is displayed for each run separately and as a function of the position of the check point with respect to the tunnel midpoint: within the tunnel, i.e., the area highlighted in grey, the GNSS signals are not available and a higher error could be expected. However, this is not the case and the error remains between 5 and 15 cm even at approximately 20 mfrom the closest available RTK fix. In order to assess the relative accuracy of the 3D reconstruction, the distance between corresponding handrail supports were measured with a tape meter at six different locations along the tunnel. The same points were then manually identified in the images using PIX4Dmatic, see Fig. 8, and the distance estimated by the software was compared with the manual measurements. The results are shown in Fig. 9: the absolute distance error is always lower than 2 . 3 cm, the mean error is sub-millimeter and the error standard deviation, considering all runs and all scales together, The outstanding results presented so far were obtained thanks to the accurate a-priori geotags computed by the Geofusion algorithm and the SFM algorithms available in PIX4Dmatic. In order to confirm the role of Geofusion, a unique feature of PIX4Dcatch, we performed the following ablation experiment: we process all datasets by substituting Geofusion geotags with raw RTK position measurements where ambiguities are fixed, and omitting any a-priori positioning information elsewhere. Note that this workflow is within reach for an advanced practitioner. In Fig. 10, the cumulative distribution of the 3D norm of the check point error is presented for both cases (for the Geofusion case, the figure just provides another view of the same data in Fig. 7). The results obtained with the Geofusion algorithm demonstrate superior performance, as the 3D error values are more concentrated toward lower values. Quantitatively, the 68 % quantile is at 10 cm, and the maximum 3D error is 19 . 4 cm, whereas, using directly the raw RTK position measurements instead of PIX4Dcatch geotags, these values increase to 26 . 7 cm and 59 . 3 cm, respectively.

is 1 . 3 cm. Given that the true distance between the measured features was around 2 m on average, the results indicate a relative accuracy of better than 1 %, which is very interesting in many infrastructure monitoring applications.

| RUN A     | X    | Y    | Z    |
|-----------|------|------|------|
| Mean [cm] | -0.4 | 3.9  | 1.8  |
| Std [cm]  | 3.1  | 4.2  | 4.2  |
| RMS [cm]  | 3.1  | 5.8  | 4.6  |
| RUN B     | X    | Y    | Z    |
| Mean [cm] | -3.9 | -1.9 | -0.9 |
| Std [cm]  | 2.8  | 6.0  | 6.0  |
| RMS [cm]  | 4.6  | 6.3  | 6.1  |
| RUN C     | X    | Y    | Z    |
| Mean [cm] | 2.3  | 4.6  | -3.9 |
| Std [cm]  | 4.2  | 3.5  | 4.8  |
| RMS [cm]  | 4.8  | 5.8  | 6.2  |
| RUN D     | X    | Y    | Z    |
| Mean [cm] | -0.4 | 0.3  | -6.0 |
| Std [cm]  | 3.5  | 5.1  | 3.7  |
| RMS [cm]  | 3.5  | 5.1  | 7.0  |

Table 1. Statistics of the error of the 29 check points for the five projects captured with the 'Double direction with spiral' pattern. No GCPs are used in the SFM.

## 4. Conclusions

This study demonstrates that using mobile phones, in combination with AutoTags, the Geofusion algorithm, and GNSS RTK adapter, provides a highly effective and affordable solution for accurate subterranean mapping. The method was tested in a real-world tunnel environment, producing results with centimeter-level accuracy even in areas with poor or no GNSS signal. Despite the challenging conditions of the tunnel, such as limited lighting, occlusions, and no GNSS signal, this approach successfully produced a complete and precise point cloud, demonstrating its potential for applications like infrastructure maintenance, safety inspections, and urban planning.

The evaluation of different scanning patterns revealed that scanning in two directions, especially with the spiral method, yields the most complete point clouds with minimal artifacts. While the single-direction method is suitable for specific tasks, such as tarmac inspections, more complex tunnel structures benefit from the double direction scanning approach to ensure full coverage. AutoTags played a critical role in maintaining alignment and accuracy, particularly when merging images from different directions.

Figure 7. Norm of the check point errors for each run and as a function of the check point position relative to the tunnel midpoint.

<!-- image -->

Line chart

Figure 8. Estimating the distance between two features marked in multiple images using PIX4Dmatic. A zoom of one of the images is shown in the inset, where the yellow cross identifies the manual click and the green one the reprojection of the estimated 3D point.

<!-- image -->

Photograph

The presented workflow is not only accessible to users with limited photogrammetry or surveying expertise but also reduces logistical and financial burdens compared to traditional methods like LiDAR or SLAM-empowered LiDAR scanners. This makes it a viable alternative for a wide range of tunnel mapping applications. Furthermore, the ease of use and intuitiveness of the solution allow it to be used by non-surveyors, thereby increasing the adoption of this workflow across various levels of the urban planning and construction industries.

Future work should focus on comparing this mobile phone based method with more traditional approaches to better understand its strengths and limitations. Overall, this study paves the way for more accessible and cost-effective mapping solutions in challenging underground settings.

Figure 9. Error with respect to known distances for six pairs of features in the tunnel and for each run. The assumed uncertainty of the manual tape measurements is highlighted in grey.

<!-- image -->

Line chart

Figure 10. Cumulative distribution of the 3D norm of the error for all check points considering the four runs together.

<!-- image -->

Line chart

## References

Ali, H. B., 2006. Standard guideline for underground utility mapping. Available at https: //pejuta.com.my/wp-content/uploads/2015/ 06/Standard-Guidelines-For-UndergroundUtility-Mapping-JUPEM.pdf , Accessed: 2024-10-15.

Apple, 2024a. ARKit - Augmented Reality. Available at https://developer.apple.com/augmented-reality/ arkit , Accessed: 2024-10-15.

Apple, 2024b. iPhone. Available at https://www.apple.com/ iphone , Accessed: 2024-10-16.

Chapman, M., Min, C., Zhang, D., 2016. CONTINUOUS MAPPING OF TUNNEL WALLS IN A GNSS-DENIED ENVIRONMENT. ISPRS - International Archives of the Photogrammetry, Remote Sensing and Spatial Information Sciences , XLI-B3, 481-485.

Cucci, D. A., Rehak, M., Skaloud, J., 2017. Bundle adjustment with raw inertial observations in UAV applications. ISPRS Journal of Photogrammetry and Remote Sensing , 130, 1-12.

Deshpande, S. S., 2021. TUNNEL MODELING USING MOBILE MAPPING LIDAR POINTS. The International Archives of the Photogrammetry, Remote Sensing and Spatial Information Sciences , XLIV-M-3-2021, 23-28. https://isprs-archives.copernicus.org/articles/ XLIV-M-3-2021/23/2021/ .

Emlid, 2024a. Reach RS3. Available at https://emlid.com/ reachrs3 , Accessed: 2024-10-15.

Emlid, 2024b. Reach RX. Available at https://emlid.com/ reachrx , Accessed: 2024-10-15.

Faro, 2024. GeoSLAM ZEB Horizon RT Mobile Scanner. Available at https://www.faro.com/en/Products/ Hardware/GeoSLAM-ZEB-Horizon-RT , Accessed: 202410-15.

HLR, 2023. Mapping our future: Navigating the shortage of land surveyors in illinois. Available at https://www.hlrengineering.com/ navigating-the-shortage-of-professional\ -land-surveyors-in-illinois , Accessed: 2024-10-15.

Janiszewski, M., Torkan, M., Uotinen, L., Rinne, M., 2022. Rapid Photogrammetry with a 360-Degree Camera for Tunnel Mapping. Remote Sensing , 14(21). https://www.mdpi.com/ 2072-4292/14/21/5494 .

Leica Geosystems, 2024. BLK2GO. Available at https://shop.leica-geosystems.com/leica-blk/ blk2go/overview , Accessed: 2024-10-15.

[Mattock, G., 2018. Underground utilities survey guideline. Available at https://www.mainroads.wa. gov.au/technical-commercial/technical-library/ surveying-and-geospatial-services/ underground-utilities-survey-guideline/ , Accessed: 2024-10-15.](https://www.mainroads.wa.gov.au/technical-commercial/technical-library/surveying-and-geospatial-services/underground-utilities-survey-guideline/)

Perfetti, L., Elalailyi, A., Fassi, F., 2022. PORTABLE MULTICAMERA SYSTEM: FROM FAST TUNNEL MAPPING TO SEMI-AUTOMATIC SPACE DECOMPOSITION AND CROSS-SECTION EXTRACTION. The International Archives of the Photogrammetry, Remote Sensing and Spatial Information Sciences , XLIII-B2-2022, 259-266. https://isprs-archives.copernicus.org/articles/ XLIII-B2-2022/259/2022/ .

Pix4D, 2024. PIX4Dcatch. Available at https://www.pix4d. com/product/pix4dcatch , Accessed: 2024-10-15.

Rehak, M., Skaloud, J., 2016. APPLICABILITY OF NEW APPROACHES OF SENSOR ORIENTATION TO MICRO AERIAL VEHICLES. ISPRS Annals of the Photogrammetry, Remote Sensing and Spatial Information Sciences , III-3, 441447. https://isprs-annals.copernicus.org/articles/ III-3/441/2016/ .

Strecha, C., Rehak, M., Cucci, D., 2024a. The accuracy of RTK enabled mobile phones in RTK denied areas. ISPRS Technical Commission IV Symposium 2024 , Perth, AUS.

Strecha, C., Rehak, M., Cucci, D., 2024b. Mobile Phone Based Indoor Mapping. The International Archives of the Photogrammetry, Remote Sensing and Spatial Information Sciences , XLVIII-2-2024, 415-420. https://isprs-archives.copernicus.org/articles/ XLVIII-2-2024/415/2024/ .

[Topcon, 2024. https://mytopcon.topconpositioning. com/na/total-stations/robotic-total-stations/ gt-1200600 .](https://mytopcon.topconpositioning.com/na/total-stations/robotic-total-stations/gt-1200600)

Wang, J., Olson, E., 2016. Apriltag 2: Efficient and robust fiducial detection. 2016 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS) , IEEE, 4193-4198.
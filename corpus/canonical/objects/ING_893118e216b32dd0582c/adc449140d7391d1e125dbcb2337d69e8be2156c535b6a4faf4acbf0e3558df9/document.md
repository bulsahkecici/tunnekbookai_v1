## Research Article

## Analysis of Settlement Induced by Shield Construction of the Metro Passing under Existing Buildings Based on the Finite Difference Method

Rui Wang , 1 Bin Zhang, 2 and You Wang 1

1

School of Civil Engineering, Central South University, 410075 Changsha, China 2 China Railway (Shanghai) Investment Group Co., Ltd., 200126 Shanghai, China

Correspondence should be addressed to You Wang; ywang1920@csu.edu.cn

Received 4 March 2022; Revised 15 April 2022; Accepted 5 May 2022; Published 28 May 2022

Academic Editor: Yang Yu

Copyright © 2022 Rui Wang et al. This is an open access article distributed under the Creative Commons Attribution License, which permits unrestricted use, distribution, and reproduction in any medium, provided the original work is properly cited.

A frequent problem when constructing metro tunnels is the uneven settlement of adjacent buildings, which results in huge economic losses. Due to shields causing the settlement of adjacent buildings, this study took the Nantong Metro Line 1 as the research object. The metro runs from the East Huancheng Road Station to the Nantong Intermediate People ' s Court Station and passes under the old residential area of the Community Sendadi-Huayuan building. Based on the settlement monitoring data, this study analyzed the impact of tunnel shield construction on the foundation settlement of adjacent buildings. The computational analysis of the shield tunnel was performed by numerical simulation, taking into account the upper building load and the construction disturbance to the surrounding rock. Afterward, the study summarized the law behind the settlement. The results show that when the boring machine was tunneling through sandy soil and silt rich in water, its head was prone to twisting due to soil disturbance and the dissipation of pore water, causing instability in the excavation process and eventual ground settlement. In the sandy strata, the relationship between foundation settlement caused by shield construction and time can be approximated as an exponential function in a certain area. The vibrations from shield excavation caused the foundations to vibrate for a short period of time. Therefore, the average settlement of buildings directly above the underpass reached 7 mm/d. Likewise, the tunneling shield caused a 1.5 mm settlement before passing under the building. It caused a peak settlement of 4.0 and 5.1 mm during and after passing under the buildings, respectively. The width of the settlement troughs of approximately 7D formed after the tunnel was excavated. Shield excavation placed the soil at the top of the excavation face in a state of tensile stress, causing tensile and shear damage to the soil and forming a local plastic zone.

## 1. Introduction

The tunnel boring machine is widely used in metro construction because it is safe and quick. More than half of the planned metro miles in China are constructed with this method [1, 2]. Most metros in China pass under busy areas. New metros are usually constrained by the complex surrounding environment and inevitably pass under existing metro tunnels, bridges, underground pipelines, and buildings. Therefore, shield construction must not only meet safety requirements but also ensure the stability of the surrounding buildings.

The impact of metro construction on buildings is mainly manifested in ground settlement caused by strata disturbance during shield excavation [3 - 5]. Most of the engineering practice shows that tunnel excavation disturbs the soil and surrounding rocks and disrupts the original equilibrium. Only after completing the tube lining, the surrounding strata gradually regain equilibrium [6 - 8]. At the end of the 20th century, González and Sagaseta and Yun et al. [9, 10] conducted research on the protection and control of adjacent buildings above shield tunnels and o ff ered recommendations for practical control of buildings in all phases of tunnel construction. Afterward, Wang et al. [11] discussed the theoretical method of applying the law of spatial and temporal e ff ects of settlement to re fl ect surface subsidence below the Wuhan Metro. Based on the method of estimating ground settlement caused by mining, Peck [12, 13] concluded that the shape of ground settlement caused by tunnel construction in the direction perpendicular to the tunnel axis was similar to the normal distribution curve in probability theory. Peck ' s formula for calculating ground settlement is an essential theoretical basis for controlling ground settlement caused by tunnel excavation. In 1987, Sagaseta [14] also proposed a formula for three-dimensional ground settlement caused by tunnel excavation based on the assumption that the strata and isotropy are incompressible. These early theories based on engineering practice and theoretical analysis summarized the ground settlement pattern caused by tunnel construction and provided a rich theoretical framework for future studies to predict the structural response of surrounding buildings in fl uenced by tunneling shield construction.

<!-- image -->

Logo

<!-- image -->

Logo

With the development of computer technology, numerical simulation has become a common means of geotechnical engineering research and has been used in shield tunnel research [15 - 17]. Liu et al. [18] investigated new tunnels passing under existing ones in conjunction with the Winkler ' s foundation model, considering the additional loads caused by tunnel excavation and the weakening e ff ect of the foundation. Likewise, they investigated the loads and deformations of existing tunnels. Kan and Li and Zhang [19, 20] analyzed the settlement pattern of buildings produced by tunnel construction using the fi nite di ff erence method (FDM). Godinho et al. [21 - 23] applied fi nite element calculation procedures combined with neural networks and other methods to investigate the environmental changes caused by tunnel excavation. In addition, they analyzed the changes and proposed corresponding prediction tools. At present, numerous studies have obtained a myriad of results in the research of shield tunnel construction under buildings. However, most of them were focused on new buildings with short time in use, strong integrity, and stability. Studies on shield tunnels passing under old residential areas are relatively rare because the buildings are used for a long time, old, and more sensitive to foundation deformation.

This study took the Nantong Metro Line 1 as the research object because it passes under the old residential area in the Community Sendadi-Huayuan . It conducted on-site settlement monitoring and numerical simulation to fi nd out the settlement law of building foundations above the shield. In addition, it analyzed the distribution of pore pressure in sandy soil with high water content and the distribution characteristics of soil displacement and plastic zones.

## 2. Project Overview

Nantong Metro Line 1 is 39.46 km long, and it will have 28 underground stations. The study section is about 1.504 km long at a depth from 16.5 to 28.0 m. It was constructed along the road using the shield method; however, it passes under some old residential areas.

2.1. Engineering Geology. Nantong is located in the alluvial plain of the lower reaches of the Yangtze River in China. Within this area, the terrain is fl at with elevation ranging from 4.0 to 6.0 m. Nantong Metro Line 1 crosses two types of landforms, namely, the alluvial-marine reticulated and neo-deltaic plains. In particular, the area from the East Huancheng Road to the Intermediate People ' s Court Station belongs to the alluvial-marine reticulated plain. The geological pro fi le of the study area is schematically shown in Figure 1. According to the survey results of the site, the Quaternary strata are over 200m thick, and the soft soil layer is thick, as well. In this study, the soils were divided into fi ve soil units from (1) to (5) and from top to bottom within the survey depth. In addition, the study included three subunits with more complex soil types and di ff erent properties. A water system with high water content in the thick layer of soft soil fl ows along the metro line. This layer of soft soil mainly constitutes powder clay, powder soil, powder fi ne sand, fi ne sand, and medium coarse sand. Among these, the powder fi ne sand is a well permeable stratum. The tunnel in this stratum mainly passes through sandy silt with silty sand, silty sand, sandy silt with silty clay, etc. Additionally, the upper and lower layers of soil also include sandy silt, silty clay with silty soil, and silty sand with silty soil.

2.2. Shield Construction Parameters. The study site is located in Chongchuan District in Nantong City, China. In this study, the Earth Pressure Balance (EPB) shield was used based on shield construction cases in the surrounding areas of Nantong. EPB construction technology is commonly used for excavating layers of soft soil. The constructed lines in Shanghai, Suzhou, Wuxi, Changzhou, and other areas used the EPB shield. Moreover, the tunnels in the mentioned areas pass through powder soil, while the ones in Nantong pass through powder and sandy soils. The speed of shield excavation was 40 ~ 45mm/min (about eight rings per day). When an EPB shield was used, the soil warehouse pressure was continuously adjusted to a reasonable value in the fi rst 100m of the tunnel. The fl uctuation of soil warehouse pressure was also controlled, amounting to less than 0.01 MPa during construction. The shield machine used in the study section was a China Railway Construction EPB shield machine (ZTE6410) with an excavation diameter of 6440mm and a panel box spoke cutter. The main body of the shield is 8.5 m long, while the main body together with the supporting carriage in the back is 84 m long. The shield has a maximum rated torque of 5700kN · m, a breakaway torque of 6300 kN · m, and a rated thrust of 4000 kN. During the construction of the study section, the work face pressure was between 260 and 270 Pa and the push force was between 14,000 and 16,000 kN, with a torque of less than 2500 kN · m. Furthermore, the cutter speed was between 1.0 and 1.2 rpm, the synchronous grouting pressure was between 400 and 500Pa, and the grouting volume was greater than 5.5 m 3 per ring. The amount of grease injected into each ring on the shield ' s end was greater than 35 kg. The longitudinal line of the shield was at 5 ‰ uphill. The width of the lining was 1200mm, with an outer and inner diameter of 6200 and 5500mm, respectively. For each advance of the shield, the

6816, 2022, 1, Downloaded from https://onlinelibrary.wiley.com/doi/10.1155/2022/1206867 by Turkey Cochrane Evidence Aid, Wiley Online Library on [08/09/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License Figure unearthed quantity was 39.2 m 3 in the left and 39.1 m 3 in the right line.

<!-- image -->

Engineering drawing

1: Geological pro fi le of the study area.

## 3. Settlement Observation and Analysis of Building Foundations

3.1. Setting the Points for Monitoring the Foundation Settlement. The line between the East Huancheng Road station and the Intermediate Court station passes below the buildings #3 to #7 and buildings #11 and #12 of the Sendadi Garden District. In the district, the residential buildings are 6-story high and old. The bottom part of the buildings ' foundation was about 11.3 m away from the top of the tunnel. The tunnel construction caused loss and disturbance of soil, which subsequently induced ground settlement. Then, the settlement trough that formed inevitably caused the adjacent buildings to tilt. Based on the construction drawings and the Technical Code for Urban Rail Transit Engineering Monitoring (GB50911-2013) [24], the settlement and the tilt values of the houses along both sides of the line within 50 m had to be monitored during the excavation of the tunnel.

In particular, the average settlement of the foundation and the value of the settlement di ff erence were monitored during excavation. The monitoring points were arranged so that buildings within 50m from the tunnel centerline had them at the corners and on load-bearing structures. A total of 6 monitoring points, No. A to F, were set for each building. The arrangement of monitoring points is shown in Figure 2. Furthermore, the points were monitored 2 times a day, when the work face of the shield tunnel was located 20m before and 50m after passing the building, and once a week, when the heading face was located 50m away after passing the building. The measurement accuracy was ± 0.5 mm. Building monitoring control indicators should include the average settlement (20mm), the average settlement rate (2 mm · d -1 ), and the maximum settlement rate (3mm · d -1 ).

Figure 2: Layout of ground settlement monitoring points in the study area.

<!-- image -->

Engineering drawing

3.2. Results of Foundation Settlement Monitoring. Since the tunnel construction began, a total of seven residential buildings (#3 to #7 and #11 to #12) in the old residential area of Sendadi Garden District have been monitored for settlement for 3 months, that is, from April to July 2020. The tunnel passed under buildings #11, #7, #5, and #3 in sequence on May 4, 2020. The time curve of the settlements was drawn according to the monitoring results in Figure 3.

After analyzing the monitoring data, it was found that the maximum settlement of the seven buildings occurred when the tunneling shield passed the fi rst building (#11). The settlement value reached a maximum of 8.1 mm. When the monitoring was completed, it was found that the settlement of buildings #11, #12, #7, #6, #5, #4, and #3 were 8.42, 7.42, 4.87, 2.79, 7.39, 3.87, and 1.86 mm, respectively. The tilt of each building was calculated based on its geometry, the settlement di ff erences between buildings, and the setup of the monitoring points. The tilt of buildings #11, #12, #7, #6, #5, #4, and #3 was 0.012%, 12 0.026%, 0.017%, 0.010%, 0.026%, 0.013%, and 0.006%, respectively. Moreover, the inclination of each building was less than 0.3% [24], and it was directed towards the metro line. These results indicate that the uneven settlement of the foundations was caused by the excavation of metro tunnel.

The monitoring curves in Figure 3 show that the e ff ect of the shield construction on foundation settlement in the sandy strata can be approximated by fi tting an exponential function over a speci fi c period of time. The ground settlement caused by soil disturbance and the loss of strata caused by excavation gradually stabilized as the shield machine moved away from the monitoring points, and its increment gradually decreased until convergence. The average settlement curve is shown in Figure 4.

Furthermore, the average settlement value increased with time, as shown in Figure 4. Building #11 was the fi rst to settle and stabilize, while buildings #3 and #4 began to settle at the end of June. This happened because the tunneling shield passed under building #11 fi rst and #3 and #4 last. Additionally, no signi fi cant settlement occurred in the foundation of building #4. By the end of monitoring, the average settlement value of building #5 reached 7.09 mm. Figure 5 shows the average settlement rate of each building. According to Figure 5, the settlement rate of most foundations during shield tunneling was lower than the allowable value (2 mm · d -1 ). However, the instantaneous settlement rate of some monitoring points exceeded the maximum control value (3 mm · d -1 ), reaching 7mm · d -1 at buildings #5 and #3. This indicates that the vibration from tunneling caused the foundations to vibrate for a short period, as well.

3.3. Analysis of Foundation Settlement. Shield construction causes ground settlement and disrupts the soil stress fi eld around the surface of the excavation. According to shield machine and ground settlement monitoring data, it was found that the instability of the head was one of the causes of excessive soil disturbance around the tunnel during excavation. The unbalanced pressure distribution at the surface of the excavation was causing the instability of the head. Likewise, the pore water in the soil a ff ected the pressure distribution on the surface of the excavation. Figure 6 shows the types of relative positions of the tunnels in regard to the buildings and the distribution of strata underneath the buildings. The shield machine mainly tunneled through sandy soil and silt mixing sand. The silt mixing sand layer contains diving, while sandy silt mixed with silty clay contains pressurized water. When the shield tunnel encountered silty clay and sandy soil during construction, the pore water in the soil at the front of the shield machine head dissipated quickly. Its shear strength and the frictional resistance on the side of the shield sharply rose, so that the torque of the cutting-head and the total thrust immediately reached their limit, which eventually lead to the torsional instability of the shield head. In addition, quicksand and other phenomena quickly formed in silty clay and sandy soil under hydrodynamic force, which was also one of the reasons for the instability of the excavation. The attitude of the shield machine was adjusted before passing under buildings. Likewise, the shield machine was controlled to advance slowly when passing under buildings. The balance of the excavation face was strictly ensured, and the lining and grouting were reinforced in time after the shield passed under the buildings. Therefore, no signi fi cant settlement occurred in the neighboring buildings, and the di ff erential settlement value did not exceed the limit.

Since the powder and sand soil hold pore water pressure and the burial depth of the head was between 2 and 5 m, the pressure of the soil chamber was adjusted to balance the pressure at the excavation face during tunneling. In addition, quality grouting was ensured by maintaining stable grouting pressure. The initial setting time of the slurry was also strictly controlled in combination with test section monitoring to avoid water seepage, sand gushing, and soil gushing in from the rear of the shield machine. When the shield is excavated to the soft plastic state stratum of silty clay with silty soil, the soft plastic stratum of silty clay and soil has high water content, high compressibility, low strength, and an obvious thixotropic and rheological deformation under dynamic action. It is easy to reduce the strength of this soil, which increases the displacement of the stratum.

As the shield advanced towards the interface of soft and hard soil, the di ff erence in the resistance between the layers of soil caused the soft soil layer to lose too much soil. As a result, the shield lost control in the vertical direction and the head of the shield deviated in the line direction. The instability of the ground also induces uneven settlement of the buildings.

In summary, the loss of strata, disturbance of the surrounding rock, and remodeling or reconsolidation of shear-damaged soils were the main causes of ground and foundation settlement. The tunnel between East Huancheng Road and the Intermediate People ' s Court station is mainly located in the sandy silt mixed with silty clay, which is locally interspersed in silty clay and situated in the silty clay mixed with silty soil. The ground settlement was relatively large when the shield machine passed through the soft and hard soils. The line was reinforced by grouting during shield construction to fi ll the voids between the lining and the surrounding rock, improve grouting quality, e ff ectively control the ground settlement, and reduce the impact of shield construction on neighboring buildings.

## 4. Numerical Simulation of Shield Construction

Combining the investigation and settlement monitoring data, numerical simulation was conducted using FLAC 3D

6816, 2022, 1, Downloaded from https://onlinelibrary.wiley.com/doi/10.1155/2022/1206867 by Turkey Cochrane Evidence Aid, Wiley Online Library on [08/09/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License Figure Figure for the foundation settlement caused by the shield machine passing under buildings #3 to #7 and buildings #11 and #12. The distribution and development pattern of foundation subsidence was summarized to analyze the settlement e ff ect of the tunnel construction on the adjacent foundations. In addition, the settlement laws of the ground surface were summarized and the plastic zones in each stratum analyzed to clarify the degree of disturbance shield tunneling caused and the in fl uence it had on the surrounding environment.

<!-- image -->

Line chart

3: Continued.

Figure 3: Settlement of the buildings of Sendadi Garden District: (a) building #11, (b) building #12, (c) building #7, (d) building #6, (e) building #5, (f) building #4, and (g) building #3.

<!-- image -->

Line chart

<!-- image -->

Line chart

4: Average settlement of foundation of each building.

4.1. Model Building and Parameter Determination. The scope of the calculation model was determined to be within the area of the two-lane tunnel passing through residential buildings #3 to #7 and buildings #11 to #12 in the residential area of the Sendadi Garden District. A ff ected by the construction of tunneling shield, the range of settlement troughs was about 30 m on both sides of the tunnel center [19]. The average spacing between the centers of the two metro tunnels was 18.44 m when crossing the district. This study also considered the distribution width of the foundation of each building within the a ff ected areas. The model was 196m wide, 50m high, and 174 m deep in the longitudinal direction. The tunnel diameter was 6.44 m, while the lining pipes on each section were 1 m long and 0.35 m thick. The height of the model depended on the in fl uence of the excavation on the surrounding rock. A small model can produce the Saint-Venant ' s e ff ect, while a large model can lead to too much mesh and make balancing di ffi cult. In this study, the grid points of both the soil and the lining around the tunnel were encrypted when dividing the grid. The calculation model is shown in Figure 7.

The ' excavation part ' of the model was dug before the excavation. The material parameters of the corresponding soil layers were selected according to their location. Furthermore, the excavation of the model was realized by the intrinsic null model, while the soil layers were described by the Mohr-Coulomb model. The stratigraphy of the study area indicated that the soil contains clayey, chalk, and sand. The Mohr-Coulomb model is commonly used to describe shear damage in soils. In this study, the envelope of the model corresponded to the Mohr-Coulomb strength criterion. When the Mohr-Coulomb model is based on principal stresses σ 1 , σ 2 , and σ 3 and out-of-plane stresses σ zz and used in FLAC 3D , the principal stresses and their directions can be obtained from the stress tensor and its components. The principal strain increment corresponding to the principal stress consists of an elastic and a plastic part:

<!-- formula-not-decoded -->

where Δ e i e and Δ e i p represent the strain increments in the elastic and plastic parts, respectively.

<!-- image -->

Line chart

Figure

5: Average settlement rate of the foundation.

<!-- image -->

Engineering drawing

Figure 6: The type of tunnel underpass in the Sendadi Garden District (unit: m): (a) tunnel underneath #5, (b) tunnel underneath #6, and (c) tunnels under buildings #7 and #11.

The Mohr-Coulomb model is not able to account for the change e ff ects in midmajor stresses when describing the mechanical behavior of sandy and chalky soils. In contrast, the spatially mobilized plane (SMP) criterion better re fl ects the yielding behavior of soft soils. It also considers midprincipal stresses in a large and small principal stress space and Figure constructs a 3D damage surface. However, this can only be achieved in FLAC 3D by means of a customized constitutive model in secondary development.

<!-- image -->

Engineering drawing

7: Computational model for shield tunneling (unit: mm).

Moreover, the tunnel lining was generated by the elastic model. The strength of the concrete was C50, and the elasticity modulus was 34.5 GPa. The properties of each soil layer and the linings are shown in Table 1. The values of each parameter were taken from the geotechnical investigation report of the study area. In addition, the ground surface of the residential area above the metro line was simpli fi ed to a horizontal surface.

When it comes to sandy soils with high water content and permeability, fl uid-solid coupling in the soil must be considered when analyzing the impact of the excavation on the environment [25]. Tunnel excavation causes loss of volume and dissipation of pore water pressure, resulting in the deformation of the soil layer and ultimately a ff ecting the permeability and mechanical properties of the soil. When the FLAC 3D software was used, the seepage module was closed, and only mechanical calculations were conducted. When the mechanical calculations reached balance or a set number of calculation steps, the seepage module was opened and the fl uid-solid coupling calculated. The fl uid fl ow model was set with its head buried 3 m deep based on the soil-water characteristic curve and the results of the undrained triaxial test. The e ff ective stresses of the soil around the tunnel changed as the seepage fi eld changed due to excavation [26]. This paper selected the isotropic fl uid model ' f\_liso ' and set the segmented lining to a nonpermeable group during the calculation.

4.1.1. Boundary Conditions and Calculation Settings. The model sets normal velocity constraints on all surfaces, except the ground one, which was designated as a free boundary. The crustal stress had been balanced before the excavation was calculated. Because the tunnel was buried very deep, only the self-weight stress was considered and not the structural one. In reference to the Load Code for Building Structures (GB50009-2012) [27] and other related studies [20], the load of each building on the ground was simpli fi ed to a vertical uniform load with a value of 105 kPa. After balancing the ground stress, the displacement is also zeroed. In addition, the ground settlement caused by the building load and tunneling was recalculated. During model calculation, every 3m of the excavation site was lined and balanced once. The whole model was completed after 58 calculations of the excavation.

The numerical simulations considered the loss of strata caused by shield construction, simulated the settlement of building and the soil rebalancing after supporting the lining. Simulating the excavation-lining process in the computer was achieved by transforming the constitutive model of solid units from the Mohr-Coulomb to the null and then to the elastic model.

## 4.2. Analysis of Foundation Settlement

4.2.1. Pore Pressure and Distribution of Vertical Displacement. Figure 8 shows the contour of pore pressure when tunnel excavation reached 87 m. Each excavation of the tunnel disturbed the balance of pore pressure in the surrounding soil. As a result, water leaked at the excavation face and seeped into the unsupported areas of the tunnel, ultimately causing more displacement. Figure 8(a) shows the pore pressure contour when the segmental lining was not constructed yet. Due to the excavation, water seeped from the surrounding soil around the inner wall of the tunnel into the tunnel. Therefore, pore pressure in the inner wall of the tunnel was zero. Figure 8(b) shows that pore pressure in the soil recovered and the diving surface restabilized after the completion of the segmental lining. Furthermore, Figure 8(c) shows the longitudinal section of the model. According to the seepage vector in the soil, the water from the soil seeped into the working face, resulting in head di ff erence. Pore pressure at the upper part of the working face was 50 kPa, while that at the lower part was 150 kPa.

Based on the simulation of Nantong Metro Line 1, the vertical displacement contour of the surface of the tunnel at di ff erent stages of tunnel construction is shown in Figures 9 - 10.

6816, 2022, 1, Downloaded from https://onlinelibrary.wiley.com/doi/10.1155/2022/1206867 by Turkey Cochrane Evidence Aid, Wiley Online Library on [08/09/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License Table Figure Figure 9 shows the trace of the ground settlement caused by excavation. The maximum settlement value in the tunnel occurred at the top of the excavation face at di ff erent stages as zero pore pressure did in the seepage fi eld. According to the numerical simulation results, the ground settlement caused by the shield machine before passing under several buildings was about 1.5 mm when 30 m of the tunnel was excavated. However, the value of ground settlement when passing under the buildings was 4.0 mm after excavating

1: The properties of each stratigraphic and tunnel lining.

| Group                       | Group                       |   Thickness (m) |   Weight (kN/m 3 ) |   Shear (MPa) |   Bulk (MPa) | Cohesion (kPa)   | Friction ( ° )   | Porosity   | Permeability coe ffi cient (cm/s)   |
|-----------------------------|-----------------------------|-----------------|--------------------|---------------|--------------|------------------|------------------|------------|-------------------------------------|
| Sandy silt                  | Sandy silt                  |            6.99 |               18.2 |        15.846 |       34.333 | 7.7              | 23.0             | 0.45       | 2.4e-5                              |
| Sandy silt with silty sand  | Sandy silt with silty sand  |            4.48 |               18.5 |        22.596 |       48.958 | 4.7              | 27.8             | 0.37       | 9.8e-3                              |
| Silty sand                  | Silty sand                  |            9.52 |               18.6 |        25.115 |       54.417 | 4.5              | 28.8             | 0.37       | 9.8e-3                              |
| Silty clay with silty soil  | Silty clay with silty soil  |            6.00 |               18.2 |        16.615 |       36.000 | 6.5              | 19.2             | 0.41       | 1.4e-5                              |
| Sandy silty with silty clay | Sandy silty with silty clay |            4.00 |               18.0 |        11.827 |       25.625 | 8.1              | 18.4             | 0.41       | 9.1e-7                              |
| Silty sand with silty soil  | Silty sand with silty soil  |            9.00 |               18.6 |        23.115 |       50.083 | 3.5              | 27.3             | 0.4        | 3.6e-4                              |
| Silty clay with silty soil  | Silty clay with silty soil  |           10.01 |               18.0 |        11.827 |       25.625 | 8.1              | 18.4             | 0.4        | 3.6e-6                              |
| Tunnel lining               | C50                         |            0.35 |               25.0 |       14781.5 |      17267.3 | -                | -                | -          | -                                   |

<!-- image -->

Engineering drawing

8: Contours of pore pressure distribution when excavated to 87 m (unit: Pa).

87m. After passing under the buildings and excavating 174m, the value was 5.1 mm. Figure 8 shows the settlement trough and displacement of the upper soil layer after tunneling. The impact area of lateral ground settlement was about 24.5 m on both sides of the tunnel.

Figure 11 shows the distribution of plastic zones in di ff erent excavation stages of the tunnel. Due to the disturbance of the original soil layer and the reduction of pore pressure at the top of the excavation face, the soil at the top of the

6816, 2022, 1, Downloaded from https://onlinelibrary.wiley.com/doi/10.1155/2022/1206867 by Turkey Cochrane Evidence Aid, Wiley Online Library on [08/09/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License Figure excavation face and the top of the tunnel was susceptible to subsidence, causing tensile stress in this part of the soil. As a result, tensile-shear damage occurred, and local plastic zones formed in the soil. In contrast, the bottom of the excavation face maintained high pore pressure. According to the e ff ective stress principle, the stress in this part of the soil was relatively low and no plastic zones formed. Due to timely lining after the excavation, the plastic zone around the tunnel regained equilibrium after tensile-shear damage. It transformed into a shear strain zone after the completion of the lining. When the tunnel excavation was completed and the lining fi nished, the tensile and shear stress zones disappeared and only a layer of the shear strain zone remained. The lining support restabilized the soil around the tunnel while also converging the ground settlement.

<!-- image -->

Engineering drawing

9: Tunnel vertical displacement contour at di ff erent shield tunneling stages (unit: m).

<!-- image -->

Line chart

Figure 10: Contour of vertical displacement of stratigraphic crosssection (unit: m).

4.2.2. Settlement Analysis. The dissipation of pore water pressure and the loss of volume in the soil layer eventually caused ground settlement, after which a settlement trough formed. Figure 12 shows the settlement trough curve based on the site monitoring data of the south side of building #4. The settlement curve of this section shows that the width of the settlement trough was about 7D on both sides of the metro (D is the diameter of the tunnel excavation). The numerical simulation results showed that the maximum settlement of this section was 5.3 mm, while the settlement of the same section during site monitoring was 6.7 mm. However, the settlement distribution of both was consistent, which indicates that the numerical simulation results were valid. The reason for the errors between the two can be attributed to the fact that the values of the material parameters and the intrinsic model were di ffi cult to fully restore. Likewise, the ground settlement was a ff ected by a variety of complex factors, but only the excavation of the tunnel was considered in the numerical simulation process, so the calculated results were smaller than the fi eld monitoring data.

Before calculating the model excavation, monitoring points were set up at the four corners and the center of the long side of buildings #3 to #7 and buildings #11 and #12 to monitor the settlement of their foundations. The location of each measurement point is shown in Figure 13. After the excavation, the upper soil layer settled downward during the excavation. However, the layer gradually stabilized and regained equilibrium after lining the shield tunnel. The monitoring curve of the foundation settlement of the seven main residential buildings in the Sendadi Garden District is shown in Figure 14.

The metro line slant passed under the residential neighborhood. The tunnels passed fi rst underneath buildings #11 and #12. Building #7 was juxtaposed with building #11. Because building #12 was adjacent to tunnel and the tunnel did not pass directly under its foundation, the settlement of its foundation was small, and it recovered after tunnel lining was fi nished. Similarly, building #4 was less a ff ected by the construction because the tunnel did not pass under it directly. According to Figure 14(a), points A and B of Figure Numerical simulation results Figure building #11 nearest to the tunnel were a ff ected by its construction. However, the other points of building #11 were farther away from the tunnel and consequently less a ff ected by the settlement. Therefore, the di ff erent results of the monitoring points revealed di ff erential settlement. Similarly, monitoring points D and E of building #7, B of building #6, C, D, E, and F of building #5, and A, B, and C of building #3 were all close to the tunnel, so they were a ff ected by the construction of the tunnel and su ff ered signi fi cant settlement unlike other points.

(a) Excavation 174 m

<!-- image -->

Photograph

(b) Excavation 87 m

<!-- image -->

Engineering drawing

(c) Excavation 30 m

<!-- image -->

Photograph

11: The plastic zone of tunnel surrounding rock in di ff erent stages.

<!-- image -->

Line chart

12: Surface settlement trough.

<!-- image -->

Engineering drawing

Figure

13: Layout of ground settlement monitoring points.

Macroscopic analysis of the monitoring curve in Figure 14 revealed that the foundation settlement of all buildings caused by tunnel construction was less than 4mm. The settlement value of building #5 was the largest, i.e., 3.6 mm. With the completion of the tunnel lining, the ground settlement in the upper part of the tunnel gradually stabilized and even recovered, but some of the monitoring points on the foundations directly above the tunnel signi fi - cantly fl uctuated in settlement values. The settlement values

6816, 2022, 1, Downloaded from https://onlinelibrary.wiley.com/doi/10.1155/2022/1206867 by Turkey Cochrane Evidence Aid, Wiley Online Library on [08/09/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License Figure of neighboring foundations during shield crossing were signi fi cantly greater than those registered by other monitoring points on the foundation of the same building.

<!-- image -->

Line chart

14: Continued.

Figure 14: Settlement curves of the foundation: (a) building #11, (b) building #12, (c) building #7, (d) building #6, (e) building #5, (f) building #4, and (g) building #3.

<!-- image -->

Line chart

## 5. Construction Proposals

Based on the actual construction of Nantong Metro Line 1, the settlement monitoring results, and numerical simulation calculations, the following recommendations are given for the di ff erent relative positions of the building and the tunnel when shield construction is passing under the neighboring buildings. Before passing under the buildings, the attitude of the shield machine should be adjusted. Then, the propulsion speed and the time and amount of correction should be reduced when passing under the buildings. The total push force should be controlled and disturbance in the surrounding soil avoided. The shield machine should also pass under the buildings no more than once. After passing under the buildings, shield tail grouting should be strictly controlled because it can reduce later settlement.

Furthermore, cutterhead should be inspected and replaced before passing under dense buildings. The discharge speed should be strictly controlled and adjusted in time according to the amount of soil lost during excavation. Similarly, grouting should be completed in time and its pressure controlled strictly. The grouting volume on each section of lining should be more than 6m 3 . Grouting pressure should be more than 200 kPa.

The parameter control scheme during excavation can be determined by referring to the initial 100 m test section of the excavation and monitoring results. The speci fi c construction parameters can be referred to as follows. The average advancement speed is controlled at 40 ~ 45mm/min and the shield advances about 8 rings per day. The speed is more reasonable, so that the daily progress can be controlled at 8 ~ 12 rings. The pressure in the soil chamber is greater than 200kPa to better balance the pressure at the excavation face, while the recommended value can be between 260 and

270kPa. Thrust can be controlled between 14000 and 16000kN, with torque less than 2500 kN · m. Cutter speed can be controlled at 1.0 ~ 1.2 r/min. The grouting pressure is controlled at 400 to 500 kPa, and the grouting volume is guaranteed to be not less than 5.5 m 3 per ring in reality.

## 6. Conclusions

- (1) When the shield tunnel was digging in sandy soil and silt, pore water in the soil in front of the cutter dissipated faster and its shear strength rose quickly. The frictional resistance at the side of the shield also rose quickly, so that the torque and total thrust of the cutter of the shield reached their limit, leading to an unstable shield machine
- (2) The vibrations caused by the shield in a short period of time resulted in the rapid settlement of the buildings. The average settlement rate for buildings directly above the shield reached 7 mm/d. The shield caused a maximum of 1.5 mm of settlement before it passed under the buildings. However, the peak settlement during and after the passage was 4.0 and 5.1 mm, respectively. The settlement troughs formed during tunnel excavation had a width of approximately 7D on one side
- (3) The excavation reduced the pore pressure at the top of the excavation face. This part of the soil was a ff ected by tensile stress, causing the soil to su ff er tensile-shear damage. In that soil, a local plastic zone formed, which eventually became a relatively large deformation. In contrast, the bottom of the excavation face still maintained large pore pressure. Based on the e ff ective stress principle, this part of the soil su ff ered small stress, so no plastic zone was formed
- (4) When shield construction was carried out in sand with high water content, the settlement of the

6816, 2022, 1, Downloaded from https://onlinelibrary.wiley.com/doi/10.1155/2022/1206867 by Turkey Cochrane Evidence Aid, Wiley Online Library on [08/09/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License adjacent buildings caused by the shield decreased with time according to the exponential law. When the shield passed under these buildings, their settlement eventually stabilized as the shield moved away

## Data Availability

The data used to support the fi ndings of this study are included within the article.

## Conflicts of Interest

The authors declare that there are no fi nancial and personal relationships with other people or organizations that can inappropriately in fl uence our work and there is no professional or other personal interest of any nature or kind in any product, service, and/or company that could be construed as in fl uencing the position presented in, or the review of, the manuscript entitled ' Analysis of Settlement Induced by Shield Construction of the Metro Passing under Existing Buildings Based on the Finite Di ff erence Method. '

## Authors ' Contributions

Rui Wang was responsible for the data curation, writing of the original draft, software, and visualization. Bin Zhang was responsible for the conceptualization, methodology, project administration, supervision, and investigation and wrote, reviewed, and edited the manuscript. You Wang was responsible for the resources, investigation, and project administration and wrote, reviewed, and edited the manuscript.

## Acknowledgments

This work was supported by the NNSFC (National Natural Science Foundation of China) through project Grant Nos. 51778633 and 51308552 and 2020 Science and Technology Research and Development Plan Guiding Subjects of China Railway Corporation through project Grant Nos. 41 and 243.

## References

- [1] Y. Cai, C. P. Zhang, and B. Min, ' Analysis of ground deformation and failure induced by shallow tunneling with cavity in the overlying strata, ' Journal of the China Railway Society , vol. 41, no. 9, pp. 118 - 127, 2019.
- [2] K. Cui and W. Lin, ' Muck problems in subway shield tunneling in sandy cobble stratum, ' Polish Maritime Research , vol. 23, no. s1, pp. 175 - 179, 2016.
- [3] K. L. Chen, H. N. Wu, W. C. Cheng, Z. Zhang, and J. Chen, ' Geological characteristics of strata in Chongqing, China, and mitigation of the environmental impacts of tunnelinginduced geo-hazards, ' Environmental Earth Sciences , vol. 76, no. 1, p. 10, 2017.
- [4] C. C. Torres and C. Fairhurst, ' Application of the convergence-con fi nement method of tunnel design to rock masses that satisfy the Hoek-Brown failure criterion, ' Tunnelling and Underground Space Technology , vol. 15, no. 2, pp. 187 - 213, 2000.
- [5] A. R. Selby, ' Tunnelling in soils-ground movements, and damage to buildings in Workington, UK, ' Geotechnical &amp; Geological Engineering , vol. 17, no. 3-4, pp. 351 - 371, 1999.
- [6] Y. Z. Xiang, H. L. Liu, W. G. Zhang, J. Chu, D. Zhou, and Y. Xiao, ' Application of transparent soil model test and DEM simulation in study of tunnel failure mechanism, ' Tunnelling and Underground Space Technology , vol. 74, pp. 178 - 184, 2018.
- [7] J. H. Shin, I. K. Lee, Y. H. Lee, and H. S. Shin, ' Lessons from serial tunnel collapses during construction of the Seoul subway line 5, ' Tunnelling and underground space technology , vol. 21, no. 3-4, pp. 296-297, 2006.
- [8] Y. Jiang, H. Yoneda, and Y. Tanabashi, ' Theoretical estimation of loosening pressure on tunnels in soft rocks, ' Tunnelling and Underground Space Technology , vol. 16, no. 2, pp. 99 - 105, 2001.
- [9] C. González and C. Sagaseta, ' Patterns of soil deformations around tunnels. application to the extension of Madrid Metro, ' Application to the extension of Madrid Metro , vol. 28, no. 6-7, pp. 445 - 468, 2001.
- [10] B. Yun, Z. H. Yang, and Z. W. Jiang, ' Key protection techniques adopted and analysis of in fl uence on adjacent buildings due to the bund tunnel construction, ' Tunnelling and Underground Space Technology , vol. 41, no. 1, pp. 24 - 34, 2014.
- [11] Z. D. Wang, L. M. Jiang, and Y. Rao, ' Estimation of ground settlement induced by shield tunnel excavation based on the time-space relationship, ' Journal of Civil and Environmental Engineering , vol. 41, no. 1, pp. 62 - 69, 2019.
- [12] R. B. Peck, ' Deep excavations and tunneling in soft ground, ' in 7th International Conference on Soil Mechanics and Foundation Engineering, Mexico City, Mexico, State-of-the-Art , 1969Mexico City.
- [13] P. B. Attewell, ' Ground movements caused by tunnelling in soil, ' in Conference on Large Ground Movements and Structures , pp. 812 - 948, London, 1978.
- [14] C. Sagaseta, ' Analysis of undrained soil deformation due to ground loss, ' Geotechnique , vol. 37, no. 3, pp. 301 - 320, 1987.
- [15] R. P. Chen, F. Y. Meng, Y. H. Ye, and Y. Liu, ' Numerical simulation of the uplift behavior of shield tunnel during construction stage, ' Soils and Foundations , vol. 58, no. 2, pp. 370 - 381, 2018.
- [16] Z. Wang, G. Li, A. Wang, and K. Pan, ' Numerical simulation study of stratum subsidence induced by sand leakage in tunnel lining based on particle fl ow software, ' Geotechnical and Geological Engineering , vol. 38, no. 4, pp. 3955 - 3965, 2020.
- [17] X. T. Wu and Z. W. Liu, ' Numerical simulation of ground settlement caused by over-lapping tunnel shield construction and measures of stratum reinforcement, ' Journal of Physics: Conference Series , vol. 1176, no. 5, p. 052070, 2019.
- [18] X. Liu, Q. Fang, D. Zhang, and Z. Wang, ' Behaviour of existing tunnel due to new tunnel construction below, ' Computers and Geotechnics , vol. 110, pp. 71 - 81, 2019.
- [19] C. Kan and J. J. Li, ' Study on the in fl uence of small clear distance tunnel with multiple arches on the foundation of adjugate high-rise buildings, ' Railway Construction Technology , vol. 293, no. 2, pp. 77 - 81+102, 2018.
- [20] S. L. Zhang, Impact Analysis of Earth Pressure Balance Shield Tunnel Construction on Existing Buildings in Beijing Metro , China University of Geosciences, China, 2010, (in chinese).

- [21] L. Godinho, P. Amado-Mendes, A. Pereira, and D. Soares Jr., ' A coupled MFS-FEM model for 2-D dynamic soil-structure interaction in the frequency domain, ' Computers &amp; Structures , vol. 129, pp. 74 - 85, 2013.
- [22] Z. Xiang, G. Swoboda, and Z. Cen, ' Identi fi cation of damage parameters for jointed rock, ' Computers &amp; Structures , vol. 80, no. 16-17, pp. 1429 - 1440, 2002.
- [23] A. Zhang and Z. Ling, ' RBF neural networks for the prediction of building interference e ff ects, ' Computers &amp; Structures , vol. 82, no. 27, pp. 2333 - 2339, 2004.
- [24] Ministry of housing and urban-rural development and P. R. China, Technical Code for Urban Rail Transit Engineering Monitoring (GB50911-2013) , China Building Industry Press, Beijing, 2013.
- [25] X. L. Lu, Y. C. Zhou, M. S. Huang, and F. Li, ' Computation of the minimum limit support pressure for the shield tunnel face stability under seepage condition, ' International Journal of Civil Engineering , vol. 15, no. 6, pp. 849 - 863, 2017.
- [26] Y. T. Zhang, ' Analysis of seepage fi eld of highway tunnel excavation by fi nite di ff erence method, ' Applied Mechanics and Materials , vol. 638-640, pp. 798 - 803, 2014.
- [27] Ministry of construction of the People's Republic of China and P. R. China, Load Code for Building Structures (GB500092012) , China Building Industry Press, Beijing, 2012.

6816, 2022, 1, Downloaded from https://onlinelibrary.wiley.com/doi/10.1155/2022/1206867 by Turkey Cochrane Evidence Aid, Wiley Online Library on [08/09/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License
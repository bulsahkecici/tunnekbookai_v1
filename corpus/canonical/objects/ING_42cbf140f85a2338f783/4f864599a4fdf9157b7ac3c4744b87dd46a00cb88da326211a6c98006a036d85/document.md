## OPEN

<!-- image -->

Logo

## Numerical analysis of mechanical response in bridge and pile foundations due to shield cutting of residual piles

Yongbo Li 1 , Zhiqiang Wu 2 &amp; Wenchao Zhang 2,3 

During shield tunneling, interactions with existing structures, such as pile foundations and bridges, are frequently encountered, leading to a growing implementation of shield cutting techniques. This study utilizes a metro tunnel project crossing under a ring expressway bridge in a city in Northeast China to develop a refined three-dimensional finite difference method (FDM) model. The 3D FDM model investigates the mechanical responses of existing pile foundations and the bridge structure due to shield cutting through residual pile foundations. The proposed numerical model is validated against field monitoring data. The simulation results show that the primary mechanical response of the existing pile foundations to shield tunneling is horizontal deformation, which decreases with increasing distance from the tunnel axis. In zones containing residual piles, tunnel crown settlement exhibits a wavy pattern, with lower settlement values compared to areas without residual piles. In contrast, bridge structure deformation remains minimal, with final deformation values below standard values. To comprehensively evaluate the effects of shield cutting through residual piles, the study quantitatively examines stratum disturbances using the ground loss ratio as an indicator. Results reveal that ground loss ratios surrounding residual pile foundations exceed 0.5%, reflecting a substantial influence. A parametric analysis underscores the critical role of ground loss ratios in influencing both bridge structure deformation and tunnel settlement.

Keywords EPB shield machine, Bridge piles, FLAC 3D , Ground loss ratio, Numerical simulation

Shield tunneling is one of the most fundamental excavation methods for urban rail transit tunnels 1-3 .  With the  increasing  density  of  urban  rail  transit  networks  in  China,  shield  tunneling  often  encounters  reinforced concrete structures, such as pile foundations and diaphragm walls. According to incomplete statistics, in more than 10 cities including Beijing, Shanghai, Suzhou, over 20 subway lines have encountered reinforced concrete pile  foundations  during  construction 4 .  Using  shield  tunneling  to  directly  cut  through  pile  foundations  can reduce costs and shorten construction periods. However, the disturbance caused by shield tunneling may induce responses in existing structures, affecting their normal use. Therefore, it is necessary to conduct deformation analysis and safety assessment of existing structures caused by shield tunneling through pile foundations.

Currently, scholars have conducted relevant studies on shield tunneling through pile foundations, utilizing methods  such  as  model  test,  theoretical  calculation,  on-site  monitoring,  and  numerical  simulation.  The experimental study, based on different accelerations, can be divided into 1 g mode test and centrifuge test. He et al. 5 used a self-developed miniature shield machine to conduct a series of 1 g model tests to investigate the mechanical response of shield tunneling through pile groups in clay. Test results show that shield tunneling induces both longitudinal and transverse additional bending moments on the pile groups, while the impact decreases  as  the  pile-tunnel  space  increases.  Guo  et  al. 6 used  model  tests  to  study  the  displacement  and internal force response of piles caused by shield tunneling in the sub-clay obtaining similar results to He et al. 5 Conventional gravity model tests reduce the size of pile foundations and cannot simulate the real mechanical response  of  pile  foundations.  The  centrifuge  is  a  powerful  tool  that  increases  the  gravitational  acceleration applied to the system while reducing the size, thereby restoring its true response. Ng et al. 7 conducted a series of centrifuge tests to simulate the influence of piggyback twin tunnelling excavation on pile groups and found two different load transfer mechanisms between the pile and soil. Song &amp; Marshall 8 used centrifuge tests to study the

1 Jiangsu  College  of  Engineering  and  Technology,  Nantong  226007,  China. 2 Department  of  Architecture  and Engineering, Nantong Vocational University, Nantong 226007, China.  3 Jiangsu Shipping College, Nantong 226010, China.  email: anwei1256@126.com impact mechanism of tunnel excavation on pile load redistribution. Test results were applied to demonstrate two important mechanisms affecting pile load distribution during tunnel volume loss.

As for theoretical solutions, the most widely applied computational approach is the two-step method. The first step involves calculating the stratum response caused by shield tunneling, then obtaining the mechanical response of the pile foundation by considering the pile-soil interaction. Based on the Winkler model, Huang et al. 9 derived the vertical and horizontal displacement of adjacent bridge piles caused by shield tunneling, considering the impact of stable groundwater effect and fluid-soil interaction on the response of pile foundation. Although the Winkler model is clearly defined and widely used, it neglects the continuity of the soil foundation and cannot account for the influence of shearing displacements of foundation. Zhang et al. 10 used the Pasternak's foundation model to establish a simplified solution reflecting the influence of shearing displacements of foundation on tunnel-pile interaction, and verified it through the existing centrifuge test 11 and field test 12 . Subsequently, with the use of a similar method, Zhang et al. 13 established a theoretical model for predicting the pile deformation controlled by the disturbance of the passive displacement and found that the significant influence of the ground loss ratio, the diameter of the pile, and the tunnel-pile space on the deformation of the pile foundation. The above models assume the soil layer is homogeneous and cannot account for the impact of differences in soil parameters on pile foundation response. Based on homogenization theory and two-stage method, Cao et al. 14 derived the horizontal displacement and bending moment of the pile foundation in layered stratums. Results of parameter analyses also emphasize the significant influence of the ground loss ratio and geometric parameters of the pile foundation. Recently, Cao et al. 3 investigated the response characteristics of the pile foundation based on the Pasternak foundation beam theory. The calculation results indicate that the cumulative effect of ground deformation resulting from shield tunneling is crucial for analyzing the response of the pile foundation. With continuous  improvements,  these  theoretical  solutions  provide  more  realistic  results  of  the  response  of  pile foundations, while also emphasizing the important impact of the ground loss ratio.

Field tests are the most useful method to reflect the mechanical response of pile foundations, which have been extensively reported by many scholars. Xu et al. 15 introduced a case study of a shield tunnel of Shanghai Metro Line 10 passing through a group of pile foundations. The pile underpinning technology was adopted to maintain the safety of the existing bridge structure, and numerical simulations were conducted to study the load transfer mechanism of the bridge structure. Wang et al. 1 reported a more complex case of shield tunneling cutting pile foundations in Hangzhou Metro Line 2, where the feasibility of the reinforcement scheme was verified through analysis  of  field  monitoring  data.  Although  the  field  measurement  can  provide  real  responses  on-site,  it  is sometimes necessary to combine numerical simulations to analyze the effects of different geological conditions and construction parameters on the mechanical response of the pile foundation. Based on the project of China's Shenzhen Metro Line 10 crossing through the bridge pile foundation of highway, Li et al. 2 employed the finite difference method (FDM) software FLAC 3D  to finely simulate the process of pile foundation underpinning and shield tunneling. Calculation results emphasize the influence of ground loss on the deformation of bridge pile foundations. For the upper-soft and lower-hard composite strata, Lv et al. 16 established a finite element method (FEM) model to study the mechanical response of existing bridge pile foundations caused by shield tunneling. Simulation results show that hard-rock height ratio has a significant impact on the deformation and internal forces of the single pile. Recently, Du et al. 17 conducted a refined FEM simulation of the shield tunneling through pile foundations of an overpass bridge on Chengdu Metro Line 27, considering the coupling effect of seepage stress. Protective measures and reinforcement schemes were proposed based on the deformation modes and stress characteristics of pile foundations.

The literature review reveals that existing research predominantly emphasizes the mechanical response of pile foundations and existing structures. However, there is a notable research gap regarding the influence of variations in the ground loss ratio on structural mechanical responses. In tunnel engineering, the ground loss refers  to  the  difference  between  the  volume  of  soil  excavated  and  the  volume  of  the  completed  tunnel.  The ground loss ratio η is defined as the ratio of the volume of difference per meter to the volume of the completed tunnel. η is  instrumental  not  only  in  predicting  ground  settlement  caused  by  tunnel  excavation  but  also  in assessing the environmental implications of shield tunneling 18-20 .  Typically, a ground loss ratio of η &lt;  0.5% is considered to indicate negligible impact on the surrounding soil strata during tunnel construction. However, for strata intersected by shield tunneling, the ground loss can become significant due to the combined influences of pre-existing ground stresses and the cutting of pile foundations. Consequently, it is imperative to evaluate the effects of shield machine cutting of residual piles on the surrounding soil strata with a focus on the ground loss ratio as a critical metric.

In this paper, the shield tunneling project under a highway as part of a subway extension line in a northeastern city in China is introduced as a case. Finite difference method (FDM) software, FLAC 3D , is employed to conduct a refined simulation of the process of the shield tunnel cutting residual bridge piles and side-crossing present bridge piles. This study evaluates the deformation behavior and internal forces within the pile foundations and bridge structures, analyzing their response under these conditions. Furthermore, the structural safety of the bridges is assessed with a focus on ground loss ratio as a critical parameter.

## Project overview

This  undercrossing  bridge  project  is  part  of  the  extension  of  Metro  Line  1  in  a  northeastern  city  in  China. The plan view and over-crossing section view of the twin tunnels and bridge piles are shown in Figs. 1 and 2, respectively. The twin tunnels are driven by an earth chamber pressure (EPB) shield machine with an excavation diameter of 6.47 m. The outer diameter, inner diameter and ring width of the tunnel lining are 6.2 m, 5.5 m, 1.2 m, respectively. The horizontal distance between the axes of the left line and right line is 14.0 m. The depth of the tunnel crown is 11.0-19.2 m. A typical geological profile of the over-crossing section is also shown in Fig. 2. The profile shows that the twin tunnels are mainly located in the round gravel layer. The physical and mechanical parameters of soils obtained by the site investigation are shown in Table 1. The bridge being undercrossed is part of a reconstruction and expansion project of a ring expressway. The total length of the bridge is 105.2 m, and the hole span combination is 5 × 20 m. The bridge adopts the bored pile foundation. The length and diameter of bored piles are 26.5 m, 1.2 m, respectively. In the process of tunnel excavation, the EPB shield machine on the left and right lines will cross through the bridge piles at angles of 50° and 51°, with the minimum distances 2.2 m and 4.4 m, respectively.

Fig. 1 .  Plan view of the undercrossing project.

<!-- image -->

Engineering drawing

During the expansion of the highway, only the upper bridge structure was removed, while the pile foundations were left intact. Through on-site exploration, a total of 12 residual piles were discovered, with 6 on each of the north and south sides, as shown in Fig. 3. The residual pile is buried to a depth of 21.7 -22.1 m and has a diameter of 0.95 -1.08 m. The relative position of the residual pile and tunnel is shown in Fig. 1. It can be found that residual piles are all distributed within the excavation range of the tunnel, meaning that the EPB shield machine will directly cut through all residual piles. Due to the lack of detailed material of the strength and integrity of residual piles, there is a significant safety risk during shield tunneling.

Due to the presence of residual piles, the shield cutting of pile foundations has a significant impact on the existing  structures.  In  this  project,  the  real-time  monitoring  of  surface  settlement  and  tunnel  settlement  is conducted, and the monitoring layout plan is also shown in Fig. 1. The monitoring points in the shield crossing area are arranged with encryption. It should be noted that for ease of illustration, only monitoring points of surface settlement in the bridge area are presented. For each monitoring section of tunnel lining, five reflecting

3

Fig. 2 .  Over-crossing section view of the undercrossing project.

<!-- image -->

Engineering drawing

Table 1 .  Physical property parameters of main soil layers. Note: γ is the unit weight; E s is the constrained modulus; ν is the Poisson's ratio; φ , c are the friction angle and cohesion obtained from the direct shear test; '*' represents the hypothetical friction angle considering the cohesion of the rock.

| Soil layers                     |   γ (kN/m 3 ) |   E s (MPa) |    υ | φ (°)   | c (kPa)   |
|---------------------------------|---------------|-------------|------|---------|-----------|
| ① Miscellaneous fill            |            18 |        5.56 | 0.37 | 15.0    | 0         |
| ③ 4 Gravel sand                 |            19 |        32.0 | 0.26 | 33      | 0         |
| ③ 5 Round gravel                |            19 |        34.0 | 0.21 | 38      | 0         |
| ④ 5 Round gravel                |            18 |        35.0 | 0.20 | 38      | 0         |
| ⑤ 4 Gravel sand                 |            19 |        38.0 | 0.26 | 35      | 0         |
| ⑨ 1 Fully Weathered Granit      |            20 |        45.0 | 0.29 | 14.8    | 35.5      |
| ⑨ 2 Intensely weathered granite |            21 |        50.0 | 0.21 | 40*     | \         |

prisms are installed at different locations, with one installed at the tunnel crown, two on the spring-line of the tunnel, and two on the rail bed.

## Refined numerical model Description of the numerical model

To analyze the impact of shield machine directly cutting residual bridge piles and side-crossing present bridge piles during the tunnel excavation, a refined three-dimensional (3D) numerical model is established using the commercial 3D finite difference code FLAC 3D . Considering the influence of boundary effects, the dimensions of the model are set to x × y × z : 200 m×100 m×40 m, where the y -direction is the driving direction of the shield machine, and the z -direction is the vertical direction. The model has total of 1,124,518 elements and 498,760 nodes. The vertical boundaries on both sides of the model constrain horizontal displacement, and the bottom boundary constrains both horizontal and vertical degrees of freedom. The outer contour of the model is shown in Fig. 4, and the relative position between the residual bridge pile and tunnel is shown in Fig. 5.

## Simulation scheme

## (1) Some assumptions of numerical simulation .

Shield  tunneling  construction  is  a  complex  process,  and  fully  replicating  the  shield  tunneling  process  is extremely challenging. Therefore, some certain simplifications are made:

- a. Considering shield tunneling construction is typically a dynamic process, the advancement of the shield machine is simplified into a segmented static analysis. Three rings are taken as one calculation step for tunneling.
- b. The complex structure of the shield machine is simplified as a rigid body, with details such as the cutterhead and screw conveyor omitted, focusing only on the interaction between the shield body and soils.
- c. Since the twin tunnels are mainly located in the round gravel layer, fluid-solid coupling calculations are not considered.
- d. Residual piles are considered as cylindrical bodies with material integrity for ease of analysis.
- e. The overlying load on the bridge is represented by an average load of 0.2 MPa.

Fig. 3 .  Exploration site of residual piles.

<!-- image -->

Geographical map

<!-- image -->

Geographical map

Fig. 4 .  Outer contour of the model.

<!-- image -->

Engineering drawing

Fig. 5 .  Relative position between residual bridge piles and the tunnel.

<!-- image -->

Engineering drawing

## (2) Construction load .

During shield tunneling, in addition to the applied thrust load, the construction loads are primarily generated by the interaction between the shield machine and stratum, including the frictional force between the shield body and stratum, as well as between the cutterhead and stratum. Considering the drag-reducing effect of the mud, the friction force between the shield body and stratum is neglected. The circumferential friction force generated by the cutter head cutting the soil ahead causes the disturbance to the surrounding stratum. Simultaneously, the support pressure applied on the excavation face compresses the soil ahead, resulting in uplift and settlement deformation of the surrounding stratum. Cao et al. 21 derived the expression for the cutter head friction force and applied it to the 3D refined simulation of shield tunneling, as shown in Eq. 1:

<!-- formula-not-decoded -->

where K is the coefficient of earth pressure at rest, K =  1-sin φ , φ is the internal friction angle; γ is the unit weight of the soil; z is the depth of the calculation point; µ c is the friction coefficient between the cutter head and the soil. Since the shield machine is mainly driven in the gravel layer, µ c =  0.5 21 .

The FISH program embedded in FLAC 3D  is used to extract the z coordinate of the excavation face nodes and calculate the circumferential friction force according to Eq. 1. The friction force is perpendicular to the direction of the line connecting each node to the center of the excavation face, as shown in Fig. 6a. The simulation method for the thrust force is similar to that for the circumferential friction force, with its value being the horizontal atrest earth pressure plus 20 kPa, as shown in Fig. 6b.

Since it is challenging to completely replicate the detailed process of shield tunneling cutting pile foundations, certain  simplifications  are  made  in  this  FDM  model.  Considering  the  worst-case  scenario,  the  maximum thrust and torque are used as the construction loads for the calculation. The shield machine cutter head has an excavation diameter of 6.47 m, with a maximum thrust of 42,500 kN and a maximum torque of 6500 kN m. The corresponding thrust and circumferential shear force are calculated as:

<!-- formula-not-decoded -->

Fig. 6 .  Diagram of applied construction load.

<!-- image -->

Engineering drawing

<!-- formula-not-decoded -->

where P max and τ max represent  the  maximum thrust and shear force per unit area acting on the cutterhead, respectively; F max and T max represent the maximum thrust and torque during shield tunneling, respectively.

## (3) Interaction between soils and structures .

To simulate the interaction between soils and structures during shield tunneling, interface elements are added into three positions: soil &amp; pile, soil &amp; shield body and soil &amp; lining, as presented in Fig. 7. For the stiffness of interface elements, a good rule provided by FLAC 3D  5.0 manual 22 is employed: the normal stiffness k n and shear stiffness k s are equal to ten times the equivalent stiffness of the stiffest neighboring zone:

<!-- formula-not-decoded -->

where K is the bulk modulus, K = E /3(1-2 υ ); G is the shear modulus, G = E /2(1 + υ ); Δ z min is the minimum size of the connecting area in the normal direction of the interface.

For  the  strength  parameters  of  the  pile-soil  interface  elements,  Chen  &amp;  Xu 23 suggested  using  0.5  to  0.8 times the parameters of the surrounding soil when experimental data is not available. In this shield tunneling undercrossing project, the pile foundation is mainly located at round gravel and gravel sand layer, with cohesion c =  0. Therefore, only the friction angle is set, taking the average of the suggested range, which is 0.65 times the parameters of the surrounding soil. For the interface elements between the soil &amp; shield body and soil &amp; tunnel lining,  according  to  the  recommendations proposed by Pellet-Beaucour &amp; Kastner 24 ,  the  friction  coefficient of the pipe-soil interface is taken as 1/3 to 1. Considering the drag-reducing effect of the mud, the strength parameters of the interface elements are taken as the lower limit of the recommended range, which is 1/3. The interface elements parameters are listed in Table 2.

## Simulation parameters of structures

In the presented model, the soil, bridge, pile foundation are simulated using solid elements, while the shield body and tunnel linings are simulated using shell elements. The soil element is modelled using the Mohr-Coulomb model, with parameters shown in Table 1. The pile foundation is modelled with elastic model. Considering

7

Fig. 7 .  Interface elements between the soil and structure.

<!-- image -->

Bar chart

Table 2 .  Parameters of interface elements.

| Positions          |   k n (MPa) |   k s (MPa) |   φ (°) |   c (kPa) |
|--------------------|-------------|-------------|---------|-----------|
| Soil & pile        |         389 |         389 |    22.8 |         0 |
| Soil & shield body |         259 |         259 |    11.7 |         0 |
| Soil & lining      |         259 |         259 |    11.7 |         0 |

Table 3 .  Simulation parameters of structures.

| Structures            | Types of elements   | Constitutive model   | D/m   |   γ/kN·m - 3 |   E/GPa |    υ |
|-----------------------|---------------------|----------------------|-------|--------------|---------|------|
| Lining                | Shell               | -                    | 6.2   |           25 |    32.5 | 0.35 |
| Bridge                | Solid               | Elastic              | -     |           25 |      30 |  0.2 |
| Present bridge piles  | Solid               | Elastic              | 1.2   |           25 |      30 |  0.2 |
| Residual bridge piles | Solid               | Elastic              | 1.0   |           25 |      24 |  0.2 |

the reinforcement effect of the steel within the pile foundation and the tunnel lining on the overall structure, the parameter values for the pile foundation and tunnel ling ( E , υ ) are set between those of concrete and steel. Additionally, due to the reduction in stiffness of the residual pile over time, a reduction factor of 0.8 is applied to the elastic modulus. The simulation parameters of structures are shown in Table 3.

## Results and analyses Ground surface settlement

Figure  8  shows  the  numerical  simulation  results  of  surface  settlement  directly  beneath  the  bridge  and  the monitoring data. By comparison, the peak value in the numerical simulation is smaller, indicating that the results are more conservative. This may be related to certain assumptions in the numerical model, particularly the simplifications regarding the uniform thrust and shear force applied on the excavation face. Overall, the surface settlement distributions predicted by numerical simulation are consistent with monitoring data, and the numerical simulation results are reasonable.

In addition, it can be found that the ground settlement caused by the excavation of left line follows a Gaussian distribution along the tunnel axis, with a maximum value of 3.8 mm. The ground settlement gradually increases during  the  excavation  of  right  line,  but  it  no  longer  completely  conforms  to  a  Gaussian  distribution.  The maximum settlement shifts from the axis of the left line to the axis of the right line, reaching about 7.0 mm. It is worth noting that after shield tunneling, a significant decrease occurs in the settlement trough at the center of the twin tunnels. This is primarily due to the increasing distance between the advancing shield machine and the No. 5 pile foundation near the tunnel axis, which results in diminished ground disturbance. Consequently, the pile-soil interface friction decreases, leading to a reduction in surface settlement.

Fig. 8 .  Distribution of the ground surface settlement right under the bridge.

<!-- image -->

Line chart

## Deformation of the pile foundations

The deformation of the present pile foundation after shield tunneling is shown in Fig. 9. It can be found that the pile foundation deformation caused is not significant, and the maximum horizontal deformation and vertical deformation are 3.8 mm and 1.1 mm respectively, which all occur in pile foundation No. 5 pile closest to the tunnel axis. Since the shield machine crosses laterally rather than directly cutting the present bridge pile, the horizontal deformation is greater than the vertical deformation.

To  further  analyze  the  deformation  of  the  present  pile  foundations,  Fig.  10  compares  the  maximum deformation of all pile foundations (No. 1 to No. 8) caused by shield tunneling. It can be clearly seen that both the vertical and horizontal deformation decrease with increasing distance from the tunnel axis, indicating that the disturbance effect of excavation weakens with distance. The vertical deformation of No. 1 and No. 8 piles located on the left and right sides of the bridge are only about 0.1 mm, which can be ignored. In addition, the statistical results in Fig. 10 show that the horizontal deformation is greater than the vertical deformation, indicating that the mechanical response around the present pile foundations is mainly the variation of horizontal stress.

As  illustrated  in  Fig.  10,  the  impact  of  shield  tunneling  on  the  present  bridge  pile  No.  5  is  significantly greater than that of other present piles. Figure 11 shows the time history curve of the horizontal and vertical deformation of pile No. 5 with shield tunneling. It is obvious that the horizontal deformation of pile foundation is significantly larger than the vertical deformation, which is consistent with the findings in Fig. 10. The main reason is that the shield machine passes through pile foundation laterally, and the horizontal stress response is greater than that of vertical stress. For horizontal deformation, there are two regions with higher growth rates, both located before the shield cutting the residual pile. This indicates that the deformation of the present bridge pile has already occurred significantly before the cutting of residual piles, which is caused by the accumulation effect of the stratum disturbance. Thus, reinforcement measures should be done in advance to avoid excessive deformation of the pile foundation.

The deformation of the residual pile foundation after shield tunneling is shown in Fig. 12. Compared with Fig. 9, it can be seen that the vertical deformation of the residual pile foundation is significantly greater than that of the present pile foundation, with a maximum value of 9.1 mm. The main reason is that the pile foundation within the tunnel excavation range is cut by the cutterhead, causing the upper part of the residual pile to lose part of its bearing capacity and deform downward under the combined effect of its own weight and ground loss. Meanwhile, as the original stress state is disrupted, the soil at the tunnel bottom rebounds, causing upward displacement of the lower residual pile. Furthermore, by comparing Fig. 12(a) and (b), it can be found that the horizontal deformation of the residual bridge pile is less than the vertical deformation, which is contrary to the deformation pattern of the present pile foundation. This indicates that the mechanical response around the residual pile foundation caused by the shield cutting is mainly the variation of vertical stress.

Fig. 9 .  Deformation of present bridge piles.

<!-- image -->

Bar chart

To  investigate  the  stress  variation  of  the  residual  bridge  piles,  Fig.  13  compares  the  distribution  of  the maximum principal stress before and after cutting. In Fig. 13a, the distribution of maximum principal stress appears continuous, showing no significant difference between the cut and residual sections. However, Fig. 13b reveals a notable stress concentration at the bottom of the upper residual pile following the cutting process, indicating  a  high  risk  of  failure  at  the  cutting  location.  Consequently,  it  is  essential  to  adjust  construction parameters to mitigate potential damage arising from the cutting of the residual pile foundation.

## Tunnel crown settlement

Figure 14 shows the distribution of the tunnel crown settlement after shield tunneling. By comparison, it can be found that the distribution characteristic of the left line is similar to that of right line. In the area without residual bridge piles, the tunnel crown settlement shows a uniform distribution from 10 mm to 15 mm. However, the tunnel crown settlement presents a wave shape within the area with residual bridge piles. The settlement of the tunnel lining in contact with the residual piles is obviously smaller than that of the non-contact tunnel lining. This is mainly related to the deformation mode of residual piles discussed in 'Deformation of the pile foundations' . The stress release of the surrounding stratum caused by shield tunneling leads to the downward movement of the upper residual pile and upward movement of the lower residual pile, which restrains the deformation of the tunnel. Furthermore, Fig. 14 presents a comparison between the monitoring tunnel crown settlement and the corresponding numerical simulation results. The close alignment between the two validates the accuracy and rationality of the numerical model developed in this study.

Fig. 10 .  Distribution of the maximum deformation of present bridge piles.

<!-- image -->

Line chart

To provide a more detailed analysis of the effects of shield tunneling cutting through residual pile foundations on the tunnel, Fig. 15 presents the settlement contour of the tunnel crown in areas interacting with the residual piles, demonstrating noticeable uneven settlement. In the numerical model, the residual pile is idealized as a regular cylinder, whereas field measurements reveal its actual shape to be irregular, complicating the assessment of its structural integrity. Thus, particular focus must be placed on reinforcing the surrounding stratum of the tunnel during the cutting of residual piles.

## Deformation of the bridge structure

During shield tunneling, by extracting the maximum settlement of the bridge surface corresponding to each excavation step, the history curve of the maximum settlement of the bridge surface is obtained. As shown in Fig. 16, during the excavation of the left line, the settlement of the bridge surface gradually increases as the distance between the excavation face and the residual pile foundation decreases. After the shield machine cuts through the residual pile foundation, the bridge surface settlement slightly rebounds. By comparison, it is found that the settlement of the bridge surface caused by the excavation of the right line is relatively smaller than that of the left line, with a final settlement of approximately 1.6 mm. Overall, the cutting of the residual bridge piles by the shield machine has little impact on the deformation of the bridge structure. The main reason is that the above-ground part of the original bridge has been completely demolished, and the bridge structure is no longer mainly supported by the residual pile foundation. Thus, the variation of stress in the residual pile foundation has minimal impact on the existing bridge structure.

According to the " Specifications for Design of Foundation of Highway Bridges and Culverts' (JTG 3363 - 2019) in China, the differential settlement between adjacent piers (excluding settlement during construction) should not cause an additional longitudinal slope (angular change) greater than 2‰ on the bridge surface, which means that the differential settlement should not exceed 20 mm. As illustrated in Fig. 16, the final settlement of the bridge surface is much smaller than the specified value, indicating the safety of the bridge structure is guaranteed.

Fig. 11 .  Time history curve of the maximum deformation of present bridge pile No. 5.

<!-- image -->

Line chart

Fig. 12 .  Deformation of residual bridge piles.

<!-- image -->

Bar chart

## Quantitatively evaluation of the effect of shield machine cutting residual piles

According to the definition of the ground loss ratio 18 , if the ground loss volume per meter V loss and the excavation diameter D are known, the ground loss ratio η can be calculated by

<!-- formula-not-decoded -->

Fig. 13 .  Distribution of the maximum principal stress of residual bridge piles.

<!-- image -->

Bar chart

Fig. 14 .  Tunnel crown settlement.

<!-- image -->

Line chart

Existing theoretical approaches to calculating the ground loss ratio, denoted as η , impose specific assumptions on the deformation profile following tunnel excavation. Moreover, back-analysis and empirical methods, which depend heavily on monitoring data, are often subject to inherent uncertainties. To address these limitations, this study introduces an innovative approach for determining η using the FISH language integrated within FLAC3D. As illustrated in Fig. 17, the proposed calculation framework, demonstrated with a representative tunnel lining cross-section, is outlined below:

Step 1 Extracting the three-dimensional coordinates of each node i (1 ≤ i ≤  12) on the cross-section before shield tunneling ( x i \_ pos, y i \_ pos, z i \_ pos ) ;

Step 2 Performing excavation calculations and complete stress release, then extracting deformation data for each node ( x i \_ dis, y i \_ dis, z i \_ dis ) ;

Step  3 the  results  of  Step  1  and  Step  2  to  obtain  the  coordinates  of  each  node  after  shield  tunneling ( x ′ i \_ pos, y ′ i \_ pos, z ′ i \_ pos ) ;

Fig. 15 .  Tunnel crown settlement within the residual pile area.

<!-- image -->

Engineering drawing

Fig. 16 .  Variation of the maximum settlement of the bridge surface.

<!-- image -->

Line chart

Fig. 17 .  Calculation of ground loss ratio in FLAC 3D

<!-- image -->

Engineering drawing

Step 4 Importing the coordinates of each node on the cross-section before and after shield tunneling into MATLAB, then calculating the area enclosed by each node and the volume of difference per meter. Substituting the above results into Eq. 5 to calculate the ground loss ratio of each lining.

There are 12 residual piles in this undercrossing bridge project. In the direction of the shield tunneling, the residual piles on the south and north sides are numbered S1-S6 and N1-N6, respectively. Taking N1 and S1 as examples, as shown in Fig. 18, it is clear that the significant elliptical deformation has occurred in the surrounding stratum after shield tunneling. This is the result of the combined effects of the original ground stress and cutting pile foundations. The maximum vertical displacement is approximately 12.5 mm. Using the FISH program to extract the 3D coordinates of each node on the tunnel lining before and after shield tunneling, the ground loss volume per meter can be obtained: 0.2 m 3 /m and 0.27 m 3 /m. Subsequently, the ground loss ratios of the stratum around N1 and S1 are calculated based on Eq. 5: 0.62% and 0.83%. It can also be seen from Fig. 18 that the ovality of the stratum around S1 is greater than N1, and the corresponding ground loss ratio is also greater.

Because of the existence of the residual pile foundation, tunnel excavation and shield cutting pile foundation will produce greater influence on the surrounding stratum. Thus, the ground loss ratios η around the residual pile foundation are emphatically considered. Figure 19 summarizes the ground loss ratio of the stratum around

Fig. 18 .  Vertical displacement of the stratum around residual piles N1 and S1.

<!-- image -->

Engineering drawing

12 residual piles. It can be found that η mainly ranges from 0.6 to 1%. The average value of η for residual pile on the north and south are 0.88% and 0.92%, exceeding 0.5%. This indicates that the tunnel excavation and shield cutting pile foundation have a non-negligible impact on the surrounding stratum. By comparison, the distribution of η on the south and north sides are similar, with the south side being slightly larger than the north side. The main reason is that the shield tunneling first crossed the north side piles, resulting in the accumulated disturbance in the stratum of around residual piles on the south side.

To quantitatively assess the impact of shield tunneling on the bridge structure and tunnel, Fig. 20 compares the deformation of the bridge structure and tunnel under different ground loss ratios η based on the calculation method of the ground loss ratio proposed in this paper, including the maximum settlement of present bridge piles, bridge surface and tunnel crown. It can be clearly seen that all of them increases linearly with the rising η , indicating the significant influence of ground loss ratio. By comparison, the tunnel crown settlement is the most sensitive to the variation of η , and the value is also the largest. Notably, since the present pile foundation is  closer  to  the  tunnel,  the  disturbance  caused  by  shield  tunneling  is  greater,  resulting  in  greater  settlement. Furthermore, Fig. 20 shows that when η &lt;  2%, the maximum settlement of the bridge surface is smaller than 10 mm, which is half of the allowable value mentioned in 'Deformation of the bridge structure' . This indicates that the disturbance caused by shield tunneling is within the permissible limits specified by the regulations.

## Discussions on the limitations of the proposed model

While the numerical simulation results presented in 'Results and analyses' provide a generally accurate prediction of ground surface settlement and bridge deformation, some discrepancies are observed when compared with the monitoring data. These discrepancies can be attributed to various factors, given the model's inclusion of complex elements such as soil behavior, the shield tunneling machine, and pile foundations. Furthermore, by comparing with the current research, we still identified some areas that need improvement in the future. The following discussion addresses areas where the model requires refinement, with a focus on enhancing its realworld application and generalizability:

## (1) Simulation scheme .

In  the  proposed  model,  the  interaction  between  the  cutterhead  and  the  soil  is  simplified  as  uniformly distributed shear force, which significantly underestimates the disturbance caused by the cutterhead rotation. In reality, both the cutterhead rotation and shield tunneling are dynamic processes, where the shear stress in the surrounding soil is fully mobilized during the rotation of the cutterhead, leading to greater disturbance. Future research can focus on a more refined simulation of the movement of cutterhead, taking into account factors such as rotational speed and opening ratio. Furthermore, the thrust applied to the excavation face is also simplified to  be  uniform. The earth chamber pressure monitored in actual projects is nonlinear rather than uniformly distributed 25 , which is another aspect that requires improvement in the model.

Fig. 19 .  Distribution of the ground loss ratio of residual piles.

<!-- image -->

Bar chart

## (2) Simulation parameters .

One of the main focuses of this study is the interaction between the soil and the structure, which is simulated using interface elements. Existing research 26 demonstrates that the strength parameters strength parameters ( c , φ ) of the interface have a greater impact on the calculation results than the stiffness parameters ( k n , k s ). In this paper, the strength parameters are obtained by reducing the parameters of the surrounding soil. Although this approach facilitates computation and analysis, it lacks experimental data support. Therefore, future research should conduct laboratory tests on the pile-soil interface and determine the reduction factors based on the characteristics of the stratum for specific projects.

## Conclusions

In  this  paper,  a  refined  3D  FDM  model  is  established  to  analyze  the  impact  of  cutting  residual  bridge  piles and side-crossing present bridge piles on the bridge structure. The impact is quantitatively evaluated from the perspective of ground loss ratio based on the simulation results. The main conclusions are as follows:

- 1) The ground surface settlement directly beneath the bridge follows a Gaussian distribution along the tunnel axis after the left tunnel excavation, with a peak value of approximately 3.8 mm. After the excavation of the right tunnel, the settlement trough shifts toward the center of the twin tunnels, with a peak value of about 7.0 mm. Due to the influence of present pile foundations between the twin tunnels, a noticeable decrease occurs at the center of the settlement trough.
- 2) The structural response of the present pile foundation is mainly characterized by horizontal deformation, which decreases with increasing distance from the tunnel axis, with a maximum horizontal deformation of 3.8 mm. The cumulative effects of stratum disturbance lead to the significant deformation in the existing

Fig. 20 .  Influence of the ground loss ratio on the maximum settlement on present bridge piles, bridge surface and tunnel crown.

<!-- image -->

Line chart

piles prior to the shield machine reaching the residual piles. In contrast, the deformation of the residual piles is primarily horizontal, exhibiting stress concentration at the base of the upper residual piles, with a maximum deformation of approximately 9.1 mm.

- 3) In areas without residual piles, the settlement of the tunnel crown is uniform, ranging from 10 to 15 mm. Conversely, the settlement of the tunnel in contact with the residual piles is smaller, causing a wavy deformation of the tunnel. The impact of cutting residual bridge piles on the deformation of the bridge structure is minimal, with a final bridge surface settlement of 1.6 mm. The maximum differential settlement between adjacent piers is also much smaller than the standard value.
- 4) A new calculation method for the ground loss ratio is proposed, providing a quantitative assessment of the impact of shield tunneling cutting residual piles on the surrounding stratum. Simulation results indicate that the ground loss ratio around residual piles ranges from 0.6 to 1%, suggesting a non-negligible impact. Results of parametric analyses demonstrate that the maximum settlement of the existing piles, bridge surface, and tunnel exhibit a linear correlation with the ground loss ratio, with the settlement of the tunnel crown displaying the most pronounced variation.

## Data availability

The datasets used and analyzed during the current study are available from the corresponding author on reasonable request.

Received: 6 August 2024; Accepted: 1 April 2025

## References

1.  Wang, Z. et al. Field measurement analysis of the influence of double shield tunnel construction on reinforced Bridge. Tunn. Undergr. Space Technol. 81 , 252-264 (2018).
2.  Li, Z., Chen, Z. Q., Wang, L., Zeng, Z. K. &amp; Gu, D. M. Numerical simulation and analysis of the pile underpinning technology used in shield tunnel crossings on Bridge pile foundations. Undergr. Space . 6 (4), 396-408 (2021).
3.  Cao, K. et al. Calculation method for the response changes of existing Bridge piles caused by side penetration of shield tunnels considering construction factors and cumulative impact of excavation. Comput. Geotech. 172 , 106472 (2024).
4.  Jia, P ., Sun, Z. Y ., Zhao, W . &amp; Song, L. M. Overview on research of shield cutting pile foundation. Tunn. Constr. 43 (10), 1637-1656 (2023).
5.  He, S. Y. et al. Pile group response induced by adjacent shield tunnelling in clay: scale model test and numerical simulation. Tunn. Undergr. Space Technol. 120 , 104039 (2022).
6.  Guo, X., Li, Z. T., Zhang, X. L. &amp; Pu, M. J. Model test study on a shield tunnel adjacent to pile in the sub-clay of a coastal area. Appl. Sci. 12 (15), 7718 (2022).
7.  Ng, C. W . W ., Hong, Y. &amp; Soomro, M. A. Effects of piggyback twin tunnelling on a pile group: 3D centrifuge tests and numerical modelling. Géotechnique 65 (1), 38-51 (2015).
8.  Song, G. Y. &amp; Marshall, A. M. Centrifuge study on the influence of tunnel excavation on piles in sand. J. Geotech. GeoEnviron. Eng. 146 (12), 04020129 (2020).
9.  Huang, K. et al. Influence of water-rich tunnel by shield tunneling on existing Bridge pile foundation in layered soils. J. Cent. South. Univ. 28 (8), 2574-2588 (2021).
10.  Zhang, Z. G., Huang, M. S., Xu, C., Jiang, Y. J. &amp; Wang, W . D. Simplified solution for tunnel-soil-pile interaction in Pasternak's foundation model. Tunn. Undergr. Space Technol. 78 , 146-158 (2018).
11.  Loganathan, N., Poulos, H. G. &amp; Stewart, D. P . Centrifuge model testing of tunnelling-induced ground and pile deformation. Géotechnique 50 (3), 283-294 (2000).
12.  Lee, R. G., Turner, A. J. &amp; Whitworth, L. J. Deformation caused by tunnelling beneath a piled structure. In Proceedings of the XIII International Conference ICSMFE , New Delhi . pp. 873-878 (1994).
13.  Zhang, Z. G. et al. Analytical prediction for tunnel-soil-pile interaction mechanics based on Kerr foundation model. KSCE J. Civ. Eng. 23 , 2756-2771 (2019).
14.  Cao, L. Q. et al. Horizontal mechanical responses of single pile due to urban tunnelling in multi-layered soils. Comput. Geotech. 135 , 104164 (2021).
15.  Xu, Q. W . et al. A case history of shield tunnel crossing through group pile foundation of a road Bridge with pile underpinning technologies in Shanghai. Tunn. Undergr. Space Technol. 45 , 20-33 (2015).
16.  Lv, J. B. et al. Mechanical responses of slurry shield underpassing existing Bridge piles in upper-soft and lower-hard composite strata. Buildings 12 (7), 1000 (2022).
17.  Du, Y. P ., Zhang, P . &amp; Zhang, J. B. Mechanical response and control measures of pile foundations under close-range shield tunneling in water - rich sandy pebble strata. Advances in Civil Engineering . 1 , 4364716 (2024).
18.  Peck, R. B. Deep excavation and tunneling in soft ground state of the art report. In Proc, 7th Int. Conf. on soil Mechanics and Foundation Engineering , Mexico city . pp. 225-290 (1969).
19.  Chen, R. P . et al. Deformation and stress characteristics of existing twin tunnels induced by close-distance EPBS under-crossing. Tunn. Undergr. Space Technol. 82 , 468-481 (2018).
20.  Jin, D. L., Yuan, D. J., Li, X. G. &amp; Zheng, H. T. An in-tunnel grouting protection method for excavating twin tunnels beneath an existing tunnel. Tunn. Undergr. Space Technol. 71 , 27-35 (2018).
21.  Cao, Y., Lin, X. Y. &amp; Lin, Z. L. Refined numerical simulation of shallow shield construction in soft soil stratum. Adv. Eng. Sci. 54 (3), 149-158 (2022).
22.  ITASCA. Fast Lagrangian analysis of continua, ITASCA Consulting Group, Inc. Minneapolis. (2003).
23.  Chen, Y. &amp; Xu, D. P . FLAC/FLAC3D Fundamentals and Engineering Examples (China Water &amp; Power, 2009).
24.  Pellet-Beaucour, A. L. &amp; Kastner, R. Experimental and analytical study of friction forces during microtunneling operations. Tunn. Undergr. Space Technol. 17 (1), 83-97 (2002).
25.  Bezuijen, A., Talmon, A. M., Joustra, J. F. W . &amp; Grote, B. Pressure gradients and muck properties at the face of an EPB. Tunnelling. A Decade of Progress . GeoDelft 1995-2005, 43 (2006).
26.  Qiu, R. C. &amp; AI, J. S. FLAC3D-based study on sensitivity of pile-soil interface parameters by static load test of single pile. Subgrade Eng. 02 , 164-169 (2019).

## Acknowledgements

We acknowledge the reviewers and editors for their valuable advice on improving the quality of this paper. Financial support for this work is provided by Jiangsu Province Construction System Science and Technology Project (2023ZD045), Nantong Natural Science Foundation and Social Livelihood Science and Technology Plan Project (MSZ2023108), Basic Science (Natural Science) Research Projects in Higher Education Institutions in Jiangsu Province (23KJD170002, 23KJD440001), Open Project of Intelligent Urban Rail Engineering Research Center of Jiangsu Province (SDGC2412). This support is gratefully appreciated.

## Author contributions

Yongbo Li: Conceptualization, Methodology, Software, Writing &amp; editing; Zhiqiang Wu: Methodology, Software, Review &amp; editing; Wenchao Zhang: Supervision, Review &amp; editing.

## Declarations

## Competing interests

The authors declare no competing interests.

## Additional information

Correspondence and requests for materials should be addressed to W .Z.

Reprints and permissions information is available at www.nature.com/reprints.

Publisher's note Springer Nature remains neutral with regard to jurisdictional claims in published maps and institutional affiliations.

Open Access This article is licensed under a Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License, which permits any non-commercial use, sharing, distribution and reproduction in any medium or format, as long as you give appropriate credit to the original author(s) and the source, provide a link to the Creative Commons licence, and indicate if you modified the licensed material. You do not have permission under this licence to share adapted material derived from this article or parts of it. The images or other third party material in this article are included in the article's Creative Commons licence, unless indicated otherwise in a credit line to the material. If material is not included in the article's Creative Commons licence and your intended use is not permitted by statutory regulation or exceeds the permitted use, you will need to obtain permission directly from the copyright holder. To view a copy of this licence, visit  h t t p : / / c r e a t i v e c o m m o ns . o r g / l i c e n s e s / b y - n c - n d / 4 . 0/ .

© The Author(s) 2025
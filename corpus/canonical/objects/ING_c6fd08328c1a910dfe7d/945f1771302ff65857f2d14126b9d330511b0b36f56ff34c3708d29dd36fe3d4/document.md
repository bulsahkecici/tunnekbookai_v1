## OPEN

<!-- image -->

Logo

## Numerical simulation method for double shield TBMs crossing weak zones

Zhiwen Wang 1,2 , Meng Wei 1,2  ,  Yang Liu 1,2 ,  Yushi Liu 1,2 , Xinyu Tan 1,2 &amp; Xin Tong 1,2

Deformation and collapse of the surrounding rock, leading to machine jamming, are critical factors hindering the safe and efficient operation of Double Shield Tunnel Boring Machines (DS TBMs). Machine jamming can be categorized into shield jamming and cutterhead jamming, each influenced by various factors. Numerical simulation effectively quantifies the impact of these factors. This paper examines the calculation methods for thrust resistance and cutterhead torque in DS TBMs and proposes a numerical simulation method that accounts for their tunneling process. A finite difference model of DS TBM excavation in rock with weak zones was developed in FLAC3D, incorporating interactions between the surrounding rock, TBM cutterhead, and shield. A Python program was created to extract stress data from individual shield and cutterhead elements, allowing for a precise quantitative assessment of potential jamming. The proposed numerical simulation method was validated for its accuracy and applicability through the analysis of a shield jamming incident at the K10 + 242 section of the DXL tunnel.

Keywords Deep Buried Tunnel, Double Shield TBM, Weak Zone, TBM Jamming, Numerical Simulation

Numerous engineering experiences have demonstrated that TBM construction in deep, high-stress tunnels is among the most efficient methods available 1-8 .  However, due to the complexity of TBM operations and the unpredictability of geological conditions, TBMs often encounter jamming incidents when passing through weak zones like fault fracture zones, joint fissure zones, and weak interlayers. These incidents significantly impact construction safety and progress 9-12 .  Theoretically, excessive resistance on the cutterhead, shield, and related equipment has been identified as the primary cause of TBM jamming incidents 13-15 . Xu et al. 16, through the analysis  of  121  TBM  jamming  incidents,  concluded  that  TBM  jamming  is  primarily  caused  by  cutterhead and shield blockages due to rock collapse, large deformations, and creep. Therefore, studying the interaction between the TBM shield, cutterhead, surrounding rock, and adverse geological bodies can effectively reduce the occurrence of TBM jamming incidents 17,18 .

The core of TBM jamming risk analysis is to examine the interaction mechanisms between surrounding rock and TBM components, such as the cutterhead and shield 19 . This analysis mainly involves three methods: empirical analysis, theoretical analysis, and numerical analysis. The empirical analysis method relies mainly on actual engineering experience, using specific rock deformation indicators and charts to qualitatively analyze TBM jamming, indirectly assessing jamming risk. For instance, Aydan et al. 20 , drawing on experience from a tunnel project in Japan, proposed evaluating tunnel squeezing risk using the ratio of intact rock strength to the pressure of the overlying surrounding rock. Ramoni et al. 21 used the N2 relationship chart method to analyze the impact of TBM downtime and advance rate on jamming risk. The theoretical analysis method mainly relies on elastoplastic mechanics theory to analytically solve the stress-strain state of tunnel surrounding rock. For instance, Wu et al. 22 , based on the plane strain axial symmetry assumption and plastic increment theory, theoretically derived the equilibrium and compatibility equations for the surrounding rock of a circular tunnel. Finally, using the fourth-order Runge-Kutta method, they obtained a semi-analytical solution. Carranza-Torres et al. 23 and Lee et al. 24 discussed the application of the convergence-confinement method in tunnel design, assuming rock masses follow the Hoek-Brown failure criterion. They proposed an evaluation method for squeezing deformation based on this approach. Zhang et al. 25 focused on time-dependent deformation of strata and derived a calculation model  for  jamming  in  squeezing  conditions.  Given  the  numerous  factors  influencing  TBM  jamming,  both empirical and theoretical analysis methods consider only a limited number of factors, which results in certain limitations. In recent years, numerical simulation methods have become essential tools for analyzing geotechnical

1 State  Key  Laboratory  of  Geohazard  Prevention  and  Geoenvironment  Protection  (Chengdu  University  of Technology),  Chengdu  610059,  China. 2 Sichuan  Complex  Geology  TBM  Intelligent  Excavation  and  Disaster Prevention Engineering Technology Research Center, Chengdu 610059, China.  email: 3463715071@qq.com engineering challenges. Hou et al. 19 simulated the time-dependent deformation characteristics of surrounding rock using a creep model based on internal variable thermodynamics, successfully replicating the interaction between the surrounding rock and the shield. Hasanpour et al. 26 , Manuel et al. 27 , Dipaloke et al. 28 , and Chen et al. 29  all proposed TBM tunneling analysis models under adverse geological conditions using FLAC3D software. They studied the impact of excavation methods, over-excavation amounts, and various strata on TBM jamming, using  strata  convergence  displacement  as  an  indicator.  However,  existing  numerical  simulation  studies  on TBM jamming mainly focus on strata  displacement,  homogeneous  surrounding  rock,  and  shield  jamming. Limited research exists on TBM tunnels in surrounding rock with weak zones, particularly regarding combined cutterhead and shield jamming.

Fig.1 .  Longitudinal cross-section schematic of the tunnel.

<!-- image -->

Line chart

Table 1 .  Parameters of the tunnel surrounding rock.

| Rock Mass Grade   | Elastic Modulus/GPa   | Poisson's Ratio   | Density/(kg·m 3 )   | Shear Strength/MPa   | Compressive strength /MPa   | Tensile strength/MPa   |
|-------------------|-----------------------|-------------------|---------------------|----------------------|-----------------------------|------------------------|
| III               | 5 ~ 8                 | 0.30              | 2.68 ~ 2.77         | 0.65 ~ 0.70          | 45 ~ 60                     | 4.38 ~ 4.89            |
| IV                | 2 ~ 5                 | 0.30 ~ 0.35       | 2.65 ~ 2.70         | 0.45 ~ 0.65          | 30 ~ 45                     | 3.41 ~ 4.38            |
| V                 | < 2                   | > 0.35            | 2.60 ~ 2.65         | < 0.45               | < 15                        | < 3.41                 |

This study, set against the backdrop of a highway tunnel project in Tibet (DXL tunnel), employs the finite difference  method  to  conduct  a  three-dimensional  numerical  simulation  of  the  mechanical  response  of  the surrounding rock and the forces on the cutterhead and shield of the DS TBM as it advances through weak zones. The research results enhance understanding of the interaction mechanisms between the DS TBM and surrounding rock, providing a theoretical foundation for developing construction plans and disaster management strategies during TBM advancement through weak zones.

## Project overview and jamming incidents Project overview

The DXL tunnel is a part of a rural highway in Tibet, functioning as a 4,789-m-long, bidirectional traffic tunnel. As shown in Fig. 1, the tunnel traverses a massive mountain, with strata belonging to the Duoxionglara Formation (Pt2-3d) of the Himalayan stratigraphic zone. The tunnel's maximum depth is approximately 820 m. The tunnel's surrounding rock is primarily composed of granitic gneiss, featuring well-developed gneissic foliation. According to the Bieniawski RMR classification system, the surrounding rock is predominantly classified as Grade III, with some sections classified as Grade IV and occasional sections as Grade V 30,31 . According to geological surveys, the physical and mechanical parameters of the rock mass in the tunnel construction area are presented in Table 1.

The middle section of the tunnel, from segment K8 + 849.5 to K13 + 382, was excavated using a DS TBM. The DS TBM excavated a tunnel with a diameter of 9.13 m, supported by 35 cm thick prefabricated reinforced concrete segments. The parameters of the DS TBM used for the construction of the DXL tunnel are presented in Table 2.

As  illustrated  in  Fig.  2,  the  maximum  monthly  tunneling  progress,  achieved  in  July  2017,  was  565  m. Excluding stoppages in January and February 2017 due to TBM jamming and extreme adverse weather, the average monthly progress of the tunnel boring machine was 355 m.

In-situ stress tests using the hydraulic fracturing method in deep boreholes estimated that the maximum horizontal stress component at the tunnel center is approximately 30 MPa, and the maximum vertical stress component is around 21.63 MPa. The ratio of vertical to horizontal stress is approximately 7:10.

## Introduction to TBM jamming incidents

Between  August  and  October  2016,  the  DS  TBM  encountered  four  jamming  incidents  at  tunnel  sections K10 + 145, K10 + 209, K10 + 242, and K10 + 253. The most severe jamming occurred at section K10 + 242 (with a vertical depth of 600 to 680 m) as the TBM traversed a weak zone. This study uses this incident as its research focus.

Table 2 .  Parameters of the DS TBM Used in the Construction of the DXL Tunnel.

| Standard excavation diameter   | 9.83 m   | Maximum excavation diameter        | 10.13 m   |
|--------------------------------|----------|------------------------------------|-----------|
| Rated torque                   | 3550kN·m | Maximum torque                     | 4508kN·m  |
| Total machine weight           | 1800 t   | Total weight of the back-up system | 1100t     |
| Maximum thrust                 | 6.1575MN | Number of TBM Disc Cutters         | 53        |
| Average Cutter Spacing         | 85.85 mm | Disc Cutter Radius                 | 120.65 mm |
| Disc Cutter Blade Width        | 20 mm    | Disc Cutter Penetration            | 7.6 mm    |

Fig. 2 .  Monthly Progress of DS TBM Tunneling.

<!-- image -->

Bar chart

Fig. 3 .  Geophysical survey results from the ISP test along the sections K10 + 168 ~ K10 + 268. ( a ), Top view; ( b ), Left vie. Note: In the top view, the amplitude ranges from - 0.25 (blue) ~ 0.25 (red), with no threshold; in the left view, the threshold ranges from - 0.045(blue).

<!-- image -->

Engineering drawing

As the TBM advanced to section K10 + 168, the ISP method was employed to investigate the surrounding rock up to 100 m ahead of the tunnel face. According to the investigation results (Fig. 3), potential weak zones with fractured rock masses were identified near sections K10 + 189 to K10 + 208, K10 + 239 to K10 + 242, and K10 + 251 to K10 + 254.

As the TBM advanced to section K10 + 168, the Integrated Seismic Prediction (ISP) method was employed to investigate the surrounding rock up to 100 m ahead of the tunnel face. In this test, the seismic wave parameters were V R =  2320  m/s  and  V S =  2500  m/s.  According  to  the  investigation  results  (Fig.  3),  potential  weak  zones with fractured rock masses were identified near sections K10 + 189 to K10 + 208, K10 + 239 to K10 + 242, and K10 + 251 to K10 + 254.

When the TBM advanced to section K10 + 242, it became jammed. Despite switching from a low to a highpressure system, which reached the machine's design limits, the TBM was still unable to advance. From within the telescopic shield, staff observed a large accumulation of rock debris on top of the TBM. The surrounding rock on both sides was intact but severely compressed against the shield, as illustrated in Fig. 4 (a-c). After clearing the surrounding rock, the monitoring team discovered a significant collapse from the 12 o' clock to 2 o' clock position on the right side of the TBM main unit (from the cutter face to the support shoe shield), resulting in a cavity approximately 6 m high and 12 m long, as shown in Fig. 4 (d).

A weak zone near tunnel section K10 + 242 was the site of a jamming incident. Additionally, other tunnel sections where jamming incidents occurred also contained problematic geological formations. For example, at K10 + 145, multiple fracture-developed compression zones were discovered; at K10 + 209, although the rock integrity was generally better, it was located in a transition zone where rock quality changed from poor to good. Preliminary analysis suggests that the jamming was caused by collapses of surrounding rock in weak zones due to tunnel advancement and convergence deformation of the surrounding rock caused by high geostress.

## Development of a numerical Model for DS TBM tunneling Numerical simulation approach

The mesh of the numerical simulation model used in this study is illustrated in Fig. 5. To minimize boundary effects, the lateral simulation range of the model was set to at least 15 times the tunnel diameter, and the longitudinal range was set to at least 10 times the tunnel diameter 32 . The dimensions of the model are 150 m × 150 m × 150 m. Additionally, the mesh within a 15 m radius around the tunnel excavation area was refined. Based on the actual conditions at the K10 + 242 tunnel segment, the width of the weak zone in the model was set to 5 m, angled at 60° to the tunnel axis.

Fig. 4 .  TBM jamming situation at the tunnel section K10 + 242. ( a ), Surrounding rock conditions at the top of the TBM; ( b ), Conditions of the surrounding rock on the left side of the telescopic shield; ( c ), Conditions of the surrounding rock on the right side of the telescopic shield; ( d ), Schematic diagram of the DS TBM jamming).

<!-- image -->

Engineering drawing

Fig. 5 .  Schematic diagram of the numerical calculation model.

<!-- image -->

Engineering drawing

Table 3 .  Mechanical Parameters and Geometric Dimensions of the Main Components of the DS TBM.

| TBM Component   | Material Properties   | Diameter/m   | Length/m   | Thickness/m   |   Density/(kg·m -3 ) | Equivalent Density/(kg·m -3 )   |   Elastic Modulus/GPa |   Poisson's Ratio |
|-----------------|-----------------------|--------------|------------|---------------|----------------------|---------------------------------|-----------------------|-------------------|
| Cutterhead      | Steel                 | 9.13         | 1          | -             |                 7600 | 56,986.77                       |                   200 |               0.3 |
| Front Shield    | Steel                 | 9.04         | 6          | 0.05          |                 7600 | 56,986.77                       |                   200 |               0.3 |
| Rear Shield     | Steel                 | 8.94         | 0.20       | 0.04          |                 7600 | 56,986.77                       |                   200 |               0.3 |
| Lining Segment  | C35 Concrete          | 8.80         | 2.0        | 0.35          |                 2390 | -                               |                  31.5 |              0.25 |
| Backfill Layer  | Pea Gravel            | -            | -          | -             |                 2200 | -                               |                   1.0 |               0.3 |

In the model, the surrounding rock is treated as an isotropic continuous medium, utilizing an ideal elastoplastic  model and the Mohr-Coulomb yield criterion. The physical and mechanical parameters of the weak zone and the adjacent rock masses are assigned values corresponding to Grade V and Grade III surrounding rock, respectively. The model simulates the main components of the DS TBM, including the cutterhead, front shield, rear shield, segmental lining, and gravel backfill grouting layer. Since directly simulating the rotary cutti ng process of the TBM cutterhead against the tunnel face is challenging, a liner structural element is used for a simplified representation of the cutterhead front end, while cshell elements simulate the cutterhead periphery. The front and rear shields are also modeled with cshell elements, while the segmental lining and backfill grouting layer are modeled with solid elements. The mechanical parameters and geometric dimensions of the main TBM components are presented in Table 3. Additionally, to simulate the self-weight of the TBM, the equivalent density method is employed, converting the TBM's total weight into an equivalent density based on the total weight and volume of each component 33 .

Since the model needs to simulate the interaction between the surrounding rock and the TBM cutterhead and shield, and to extract stress data from each element, the large deformation mode is not activated during calculations. Considering the convergence deformation of the surrounding rock after excavation, a reserved excavation  gap  is  typically  provided  in  TBM  design  and  construction.  In  the  absence  of  large  deformation mode, the existence of the excavation gap prevents direct contact between the surrounding rock and the TBM shield. Therefore, we use solid elements (hereinafter referred to as 'gap elements') to simulate the excavation gap.  The  gap  elements  are  modeled as elastic  with  a  very  low  deformation  modulus, used to transfer forces between the deformed surrounding rock and the shield structure. Its initial thickness is the same as the reserved excavation gap thickness in the tunnel design and construction, and it is divided into multiple layers of mesh. Due to the rigidity of the shield structure, when the surrounding rock undergoes convergence deformation, the compression from the surrounding rock and the restraint from the shield structure gradually compress the gap elements, generating small elastic reactions, with the surrounding rock deforming almost freely during this process. As the surrounding rock continues to deform, approaching or reaching the reserved excavation amount, the gap elements are compressed to a very thin state, at which point the reaction force of the gap elements increases on both sides, indicating that compression occurs between the surrounding rock and the shield.As the surrounding rock deforms further, the shield structure experiences significant elastic deformation under the compressive forces, leading to cases where the deformation of the surrounding rock in the shield zone exceeds the gap thickness in the calculation results. At this point, the stress values of the shield and other components are extracted to assess whether TBM jamming has occurred. Additionally, the initial geostress field in the project area, obtained from geological surveys and inversion calculations, is presented in Table 4.

Table 4 .  Initial In-Situ Stress of the Surrounding Rock.

| σx/MPa   | σy/MPa   | σz/MPa   | σxy/MPa    | σyz/MPa    | σxz/MPa    |
|----------|----------|----------|------------|------------|------------|
| - 28.5   | - 20.6   | - 17.8   | - 8.96E-16 | - 1.41E-31 | - 2.31E-15 |

Table 5 .  Relative convergence values of surrounding rock as specified in the 'Technical Specification for Highway Tunnel Construction' .

|                 | Depth/m    | Depth/m   | Depth/m   |
|-----------------|------------|-----------|-----------|
| Rock Mass Grade | < 50       | 50 ~ 300  | > 300     |
| III             | 0.1 ~ 0.3  | 0.5 ~ 0.5 | 0.4 ~ 1.2 |
| IV              | 0.15 ~ 0.5 | 0.4 ~ 1.2 | 0.8 ~ 2.0 |
| V               | 0.2 ~ 0.8  | 0.6 ~ 1.6 | 1.0 ~ 3.0 |

In order to differentiate between tunnel surrounding rock convergence and collapse, this study adopts the relative convergence value of surrounding rock as specified in the "Technical Specification for Highway Tunnel Construction" (JTG F60-2009) of China as the criterion for assessing surrounding rock stability. The specific standards are shown in Table 5. The relative convergence value of surrounding rock refers to the ratio of the tunnel crown settlement displacement (in centimeters) to the tunnel width (in meters). For brittle rock, the smaller values in the table are applied, while for plastic rock, the larger values are used. Based on this, a tunnel crown  settlement  displacement  of  273.9  mm  is  used  as  the  threshold  for  distinguishing  surrounding  rock collapse in this study.

## Calculation of Forces on TBM components by surrounding rock

TBM advancement resistance

The resistance encountered by the TBM during rock-breaking advancement primarily includes the cutterhead frontal resistance ( F 1 ) , the frictional resistance of the shield sliding ( F 2 ) , and the resistance from dragging the back-up system F 3 . Therefore, the formula for calculating the TBM thrust resistance F is as follows:

<!-- formula-not-decoded -->

The frontal resistance of the cutterhead primarily includes the normal rock-breaking resistance of the disc cutters ( F 11 ) and the axial thrust required to maintain stability of the cutter face and continue forward excavation ( F 12 ) . The sliding friction of the shield body mainly arises from the pressure exerted by the surrounding rock on the shield shell and the friction generated by the self-weight of the shield. The traction resistance of the rear support equipment primarily results from the force required to drag the rear support units.

(I) Calculation of F 11 .

The normal component of the rolling cutter rock-breaking resistance primarily refers to the thrust required for the rolling cutters to penetrate the rock, which is the sum of the rolling thrusts of each cutter on the TBM cutterhead:

<!-- formula-not-decoded -->

where F v represents the vertical force exerted on each rolling cutter during the rock-breaking process; and t represents the number of single-edged rolling cutters installed on the cutterhead.

As noted above, the key to determining the normal rock-breaking resistance of TBM disc cutters is accurately calculating the vertical forces experienced by each cutter during the rock-breaking process, which is directly reflected in the force analysis of a single cutter's rock-breaking effort. Numerous theoretical and experimental studies  have  been  conducted by scholars both domestically and internationally on the forces acting on disc cutters,  leading  to  the  development  of  various  predictive  models  for  cutter  forces 34-37 .  Among  the  many predictive models for cutter forces, this paper adopts the Rostami prediction formula to calculate the normal rock-breaking resistance of TBM disc cutters. The calculation formula is as follows:

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

where T represents the disc cutter blade width; r represents the disc cutter radius; ∅ represents the cutterrock contact angle; P r represents the pressure directly under the cutter; φ represents the cutter tip pressure distribution coefficient, which decreases as the cutter tip width increases ( φ = - 0 . 2 ∼ 0 . 2 ); C represents a dimensionless constant, usually taken as 2.12; S represents the disc cutter spacing; σ c represents the uniaxial compressive strength of the rock, with a value taken as the maximum uniaxial compressive strength of the surrounding rock, which is 60 MPa ; and σ t represents the uniaxial tensile strength of the rock, with a value taken as the maximum uniaxial tensile strength of the surrounding rock, which is 4.89 MPa.

## (II) Calculation of F 12

During the simulation process, the normal force on the TBM cutterhead can be indirectly obtained by reading the forces on the liner structural elements that simulate the cutterhead on the tunnel face, as shown in Eq. (5).

<!-- formula-not-decoded -->

where n i represents the number of the triangular liner structural element; m represents the total number of liner structural elements in the cutterhead model facing the tunnel face; f n i represents the average normal stress of the corresponding element (MPa); and A i represents the area of the liner structural element (m 2 ).

## (III) Calculation of F 2

The sliding friction of the shield body can be indirectly determined from the normal stress on the outer surface of the shield, as shown in Eq. (6):

<!-- formula-not-decoded -->

where µ 1 represents the friction coefficient between the surrounding rock and the shield in relative motion; k represents the total number of shell structural elements in the shield model; f m i represents the normal stress of the corresponding element (MPa); and S i represents the area of the shell structural element (m 2 ).

During the continuous tunneling process of the TBM, the dynamic friction coefficient between the surrounding rock and the shield typically ranges from 0.3 to 0.5, while the static friction coefficient for restarting the TBM after a stop generally ranges from 0.3 to 0.45 21,38 . In this paper, the value of µ 1 is taken as 0.35.

(IV) Calculation of F 3

<!-- formula-not-decoded -->

where µ 2 represents the friction coefficient between the back-up system and the invert support structure surface, taken as µ 2 = 0 . 2 based  on  Ates  et  al.'s  research 6 ; W 1 represents  the  weight  of  the  back-up  system;  and α represents the angle between the tunnel axis and the horizontal direction.

Based on the engineering geological conditions and TBM cutter parameters, F 11 = 7070 kN , F 3 = 2200 kN are calculated. F 12 and F 2 need to be determined through numerical simulation.

## Calculation of TBM cutterhead torque

During TBM construction, numerous factors influence the cutterhead torque, and various methods have been proposed by scholars to calculate it 39-41 .  It  is  generally accepted that the total torque ( T ) acting on the TBM cutterhead consists of five main components: the rolling resistance torque generated by the disc cutters during rock breaking ( T 1 ); the resistance torque caused by the rotation of broken rock debris with the cutterhead ( T 2 ); the torque required to overcome the cutterhead's self-weight ( T 3 ); the frictional torque generated by interaction between the cutterhead periphery and the rock during rotation ( T 4 ); and the torque produced by the cutterhead bearings and other devices ( T 5 ). Some scholars have pointed out that among the factors influencing cutterhead torque, the components T 1 , T 2 , T 3 , and T 4 dominate the total torque T, while the component T 5 accounts for only 2% of the total torque and can be neglected 6,39-41 .Therefore, the total cutterhead torque is calculated as follows in this paper:

<!-- image -->

Other

<!-- formula-not-decoded -->

7

(I) Calculation of T 1

<!-- formula-not-decoded -->

where F R represents the rolling resistance of a single disc cutter; t i represents the distance of the i -th disc cutter from the cutterhead axis; and t represents the number of disc cutters.

According to the Rostami prediction formula, the calculation for F R is as follows:

<!-- formula-not-decoded -->

Where ∅ represents the disc cutter's contact angle with the rock; P r represents the pressure directly beneath the disc cutter; G represents the width of the disc cutter blade; and φ represents the rock fragmentation angle, generally taken as 135° to 160°.

(II) Calculation of T 2

<!-- formula-not-decoded -->

where q represents the unit weight of rock debris; δ represents the cutterhead opening ratio; R represents the radius of the cutterhead; and h represents the disc cutter penetration rate.

(III) Calculation of T 3

<!-- formula-not-decoded -->

Where W 2 represents the self-weight of the cutterhead.

(IV) Calculation of T 4

<!-- formula-not-decoded -->

where d represents axial width of the cutterhead; θ p represents the circumferential coordinate of a point on the cutterhead; P 1 and P 2 represent the vertical and horizontal pressures on the cutterhead, respectively.

To  simplify  the  calculation  process,  by  combining  the  stratum  lateral  pressure  coefficient  with  the  TBM cutterhead perimeter area, the calculation formula for T 4 is as follows:

<!-- formula-not-decoded -->

where K 0 represents the lateral pressure coefficient, taken as 1.5; S i represents the area of each shell structural unit (m 2 ); j represents the total number of shell structural units in the cutterhead perimeter model; and f m j represents the normal stress of the shell element on the cutterhead perimeter model (MPa).

Based on the engineering geological conditions and relevant parameters of the TBM disc cutters, the torque values for the cutterhead are as follows: T 1 = 1816 kN · m , T 2 = 66 . 2 kN · m , T 3 = 83 kN · m . The torque T 4 needs to be determined through numerical simulation.

## Assessing the jammed condition of a TBM

(I) Shield Jamming

During TBM excavation, if the total thrust resistance exceeds the rated thrust ( F 0 ), the TBM shield becomes jammed, resulting in a machine stoppage. Therefore, the conditions for assessing TBM shield jamming are as follows:

<!-- formula-not-decoded -->

(II) Cutterhead jamming.

During the TBM tunneling process, if the total torque of the TBM exceeds the maximum torque ( T 0 ) of the cutterhead, the TBM cutterhead jams, causing a machine stall. Therefore, the condition for determining the jammed cutterhead state of the TBM is as follows:

<!-- formula-not-decoded -->

## Analysis of actual working condition simulation results Analysis of mechanical response and deformation of surrounding rock

This paper analyzes the middle section of the TBM's front shield during key stages: when the TBM has not yet entered, has just started to enter, is fully within, is beginning to exit, and has exited and moved away from the weak zone (corresponding to excavation steps 50, 67, 82, 92, and 113, respectively). The LDP curve refers to the longitudinal displacement profile of the surrounding rock.

As illustrated in Fig. 6a, c, and d, prior to entering the weak zone (excavation step 50), the stress field and plastic zone around the TBM tail shield section show a symmetric distribution. At this stage, the plastic zone in the surrounding rock primarily appears in front of the tunnel face and along both sides of the tunnel axis. The plastic zone ahead of the tunnel face extends to a maximum depth of 5.40 m. The maximum stress near the tunnel reaches 25.80 MPa, concentrated at the tunnel crown and the junction between the weak zone and the surrounding rock. The settlement deformation of the surrounding rock arch within the TBM shield area increases with distance from the tunnel face, ranging from 31.21 mm to 49.80 mm, as shown in Fig. 6b. Analysis of  the  longitudinal  displacement  profile  of  the  surrounding  rock  indicates  that  in  certain  areas  of  the  TBM front shield zone, the surrounding rock deformation exceeds the allowable deformation limit. This indicates that compression is occurring at this stage between the tunnel arch's surrounding rock and the TBM shield.

Fig. 6 .  Excavation Step 50. ( a ), The first principal stress at the front shield cross-section (unit: Pa); ( b ), LDP curve of the surrounding rock at the vault; ( c ), Plastic zone at the front shield cross-section; ( d ), Plastic zone in the longitudinal section (The red dashed line represents the boundary between the surrounding rock and the weak zone.)).

<!-- image -->

Line chart

As illustrated in Fig. 7a, when the TBM's cutterhead begins to enter the faulted zone (excavation step 67), the stress  field  of  the  surrounding  rock  exhibits  a  symmetrical  distribution.  Due  to  the  oblique  intersection between the weak zone and the tunnel, a low-stress area exists above the tunnel, and the stress distribution is uneven on the upper and lower sides of the tunnel face. The maximum rock pressure around the tunnel reaches 26.68 MPa, concentrated on both sides of the tunnel. As illustrated in Figs. 7c and d, during this excavation step, the tunnel's plastic zone mainly forms near the interface between the intact surrounding rock and the weak zone, with a depth of approximately 10 m. This is mainly due to the influence of tunnel excavation unloading and the weak boundary of the weak zone, resulting in a significant drop in principal stress and the transition to a plastic state. The plastic zone of the rock mass at the tunnel face is mainly concentrated below the tunnel axis, with a maximum depth of 6.0 to 6.3 m. Additionally, the plastic zone at the interface between the intact surrounding rock and the weak zone above the tunnel face begins to develop. Figure 7b shows that the settlement deformation of the surrounding rock crown within the TBM shield zone increases with distance from the tunnel face, ranging from 44.54 mm to 58.46 mm. This indicates that the surrounding rock in the crown area of the tunnel is exerting pressure on the TBM shield. Additionally, more rock blocks near the tunnel face experience shear failure than tensile failure. This phenomenon can be explained as follows: Prior to tunnel excavation, the horizontal stress in the rock exceeded the vertical stress. As a result, after excavation and stress redistribution, stress concentration occurs mainly in the horizontal direction, increasing the likelihood of shear failure. This effect occurs regardless of the horizontal stress coefficient. In circular tunnels, the release of confinement due to excavation leads to an increase in deviatoric stress, thereby primarily contributing to rock mass shear failure.

Figure 8a, c, and d reveal that when the TBM fully entered the weak zone at excavation step 82, no significant stress concentration areas were observed in the surrounding rock. Due to the reduced strength of the surrounding rock, the plastic zone of the tunnel at this stage expanded significantly, reaching a maximum depth of 10.50 m. Within the shield range, the depth of the plastic zone in the surrounding rock at the tunnel crown reached 8.70 m, while at the tunnel invert, it reached 13.30 m, showing a significant increase compared to excavation step  67.  According  to  Fig.  8b,  the  settlement  deformation  of  the  surrounding  rock  arch  in  the  TBM  shield zone within the weak zone ranges from 153.32 to 339.25 mm, significantly exceeding the planned excavation deformation. This suggests significant compression of the shield structure in this area, posing a risk of TBM jamming. Furthermore, it can be observed that the deformation of the surrounding rock at the tunnel crown within the TBM shield area exceeds 273.9 mm, indicating that collapse of the surrounding rock in the weak zone has occurred at this stage. Outside the shield area, the deformation of the intact surrounding rock near the weak zone increased compared to that further away, with a maximum displacement of 164.04 mm. This phenomenon can be explained as follows: during tunnel excavation, the original in-situ stress state is disturbed, leading to a redistribution of stress within the surrounding rock. Particularly near the weak zone, due to its inherent low strength and high deformation characteristics, the adjacent intact rock must bear additional loads, resulting in stress  concentration. This stress concentration induces additional deformation within the surrounding rock. Moreover, differences in mechanical properties between the weak zone and the adjacent intact rock significantly affect deformation patterns. The high compressibility and low shear strength of the weak zone lead to significant compressive and shear deformations under stress, which, through stress transfer mechanisms in the rock, further impact the adjacent intact rock 42 . Additionally, in the latter part of the LDP curve, tunnel deformation decreases. This is primarily because the actual weak zone width is relatively small, and by this stage, parts of the TBM have reached the intact rock zone.

Fig. 7 .  Excavation Step 67. ( a ), The first principal stress at the front shield cross-section (unit: Pa); ( b ), LDP curve of the surrounding rock at the vault; ( c ), Plastic zone at the front shield cross-section; d, Plastic zone in the longitudinal section (The red dashed line represents the boundary between the surrounding rock and the weak zone).

<!-- image -->

Engineering drawing

Fig. 8 .  Excavation Step 82. ( a ), The first principal stress at the front shield cross-section (unit: Pa); ( b ), LDP curve of the surrounding rock at the vault; ( c ), Plastic zone at the front shield cross-section; d, Plastic zone in the longitudinal section (The red dashed line represents the boundary between the surrounding rock and the weak zone).

<!-- image -->

Engineering drawing

Figure 9a illustrates that when the TBM cutterhead starts to emerge from the faulted zone (excavation step 92), the maximum stress in the surrounding rock occurs at the sides of the tunnel arch, reaching 25.67 MPa. Figure 9c and d reveal that the internal plastic zone of the surrounding rock is mainly concentrated in the weak zone and near the tunnel face. The rock at the interface between the intact rock and the weak zone enters a plastic state due to a reduction in lateral principal stress caused by tunnel excavation. At this stage, the settlement deformation of the tunnel crown in the intact rock section within the TBM shield area ranges from 27.03 mm to 198.93 mm, as indicated in Fig. 9b. In contrast, the maximum settlement deformation of the crown in the portion of the shield still within the weak zone reaches 341.25 mm (indicating that the surrounding rock in the weak zone is still collapsing at this stage). This also indicates that as the TBM gradually moves from the weak zone into the intact rock zone, the surrounding rock continues to exert deformation pressure on the shield. However, this deformation pressure is gradually decreasing.

Fig. 9 .  Excavation Step 92. ( a ), The first principal stress at the front shield cross-section (unit: Pa); ( b ), LDP curve of the surrounding rock at the vault; ( c ), Plastic zone at the front shield cross-section; d, Plastic zone in the longitudinal section (The red dashed line represents the boundary between the surrounding rock and the weak zone).

<!-- image -->

Engineering drawing

As shown in Fig. 10, when the TBM cutterhead has completely emerged from and moved away from the faulted zone (excavation step 113), the stress field in the surrounding rock gradually returns to a distribution similar to that before entering the weak zone. The surrounding rock continues to exert pressure on the TBM shield, and the settlement of the tunnel crown outside the shield area continues to increase with distance from the tunnel face. The plastic zone in the surrounding rock is mainly concentrated within and near the weak zone, indicating that the settlement of the tunnel crown and the development of the plastic zone are still influenced by the weak zone.

It  should  be  noted  that,  to  simplify  the  simulation,  the  time-dependent  deformation  effects  of  the surrounding rock were not considered in either the selection of the rock constitutive model or the excavation process simulation. However, faulted and fractured rock typically exhibits significant rheological properties. In such poor-quality rock sections, tunnel support measures are enhanced, TBM advancement speeds are reduced, and the surrounding rock exerts greater contact pressure on the shield. Therefore, future detailed simulations should incorporate factors such as the time-dependent deformation characteristics of the surrounding rock and variations in TBM advancement rates across different rock sections.

## Analysis of Structural Loads on the TBM

The  analysis  in  Sect.  4.1  revealed  that  the  surrounding  rock  consistently  contacts  the  shield  body  during TBM advancement. To determine whether a TBM jamming incident has occurred under these conditions, it is necessary to analyze the forces acting on the TBM cutterhead and shield structure. Figure 11 presents the variations in the forces acting on the cutterhead and shield structure during DS TBM advancement.

Figure 11a illustrates that in the intact rock zone, the normal force on the TBM cutterhead ranges from 19.84 to 22.65 MN. Once the TBM enters the weak zone, the normal force on the cutterhead rapidly increases, peaking at 34.89 MN, which is still below the TBM's maximum thrust capacity of 61.575 MN. According to Fig. 11b, the cutterhead torque surpasses the TBM's rated torque in the middle of the weak zone, peaking at 3940.80 kN·m. This occurs because, after the TBM head enters the weak zone, a significant amount of loose rock is compressed under excavation disturbance and tightly surrounds the cutterhead.. When the palm face exerts pressure on the cutterhead, the TBM rapidly increases the normal force on the cutterhead to maintain rock face stability. Simultaneously, the torque required to rotate and cut with the cutterhead also increases rapidly, exceeding the TBM's rated torque but not surpassing the maximum torque. This indicates that there is no risk of the cutterhead jamming during the tunnel excavation process.

Fig. 10 .  Excavation Step 113. ( a ), The first principal stress at the front shield cross-section (unit: Pa); ( b ), LDP curve of the surrounding rock at the vault; ( c ), Plastic zone at the front shield cross-section; d, Plastic zone in the longitudinal section (The red dashed line represents the boundary between the surrounding rock and the weak zone).

<!-- image -->

Engineering drawing

As shown in Fig. 11c, the TBM shield frictional resistance also increases significantly once the TBM cutting head enters the weak zone, peaking at 25.85 MN, which remains below the TBM's maximum thrust capacity. This increase is primarily due to deformation and collapse within the weak zone, which exert additional pressure on the TBM shield, leading to a continuous rise in frictional resistance. It is important to note that the variation in shield frictional resistance differs from that of TBM torque and tunnel face thrust. Specifically, the frictional resistance exhibits a trend of increasing and then decreasing before 21 m, likely due to boundary effects in the numerical simulation.

The total thrust required by the TBM is derived from Eq. (1), as illustrated in Fig. 11d. Excluding boundary effects from the numerical simulation, the thrust required for excavation increases rapidly once the TBM enters the weak zone, reaching a maximum of 68.97 MN, which exceeds the TBM's maximum thrust capacity of 61.575 MN. This indicates that the TBM shield became jammed between excavation steps 82 and 92. Based on the analysis in Sect. 4.1, during excavation steps 82 to 92, collapse occurred in the weak zone, indicating that the results of the numerical simulation are consistent with the actual engineering incident, further validating the accuracy of the numerical simulation method.

In the TBM shield area, the deformation of the surrounding rock is influenced by the spatial constraints imposed by the unexcavated rock face, increasing as the distance from the tunnel face grows. On one hand, the DS TBM features a closed shield structure with a large contact area with the surrounding rock, resulting in significant frictional resistance between the shield and the rock. On the other hand, the relatively long shield of  the  DS  TBM means that the rock mass receives support for a longer period, and as time progresses, the deformation and displacement of the rock increase. This results in more extensive contact between the rock and the shield, leading to increased frictional resistance. The increase in frictional resistance between the shield and the surrounding rock raises the risk of the shield jamming in fragmented rock sections.

Fig. 11 .  Variation of Structural Loads on the TBM with Tunnel Face Advancement Distance. ( a ), Variation in Cutterhead Normal Force; ( b ), Variation in Cutterhead Torque; ( c ), Variation in Shield Frictional Resistance; ( d ), Variation in Total Thrust Required by the TBM).

<!-- image -->

Line chart

In summary, as the TBM approaches the boundary between a weak zone and intact surrounding rock, ground stress concentration occurs, leading to increased shield pressure and cutterhead stress. This results in higher shield friction resistance and increased cutterhead normal force and torque even before entering the weak zone. In practical engineering, the closer the TBM gets to the weak zone boundary, the more fractured the surrounding rock tends to be, leading to greater TBM cutter penetration and increased machine torque. Consequently, the increase in normal stress on the cutterhead and rock-breaking torque can serve as early warning indicators of approaching a weak zone, allowing engineers to combine this information with geological survey data to better identify faulted and fractured zone boundaries.

## Conclusion

The presence of weak zones in deep tunnels is one of the primary causes of TBM jamming. However, limited numerical simulation research has been conducted on the rock-machine interaction of DS TBMs crossing these weak zones. This study used the finite difference method to simulate the excavation of DS TBMs in deeply buried weak rock formations. The forces on the TBM shield and cutterhead were theoretically calculated, and a finite difference model was developed in FLAC3D to simulate the DS TBM's excavation through these weak zones. A Python program was then used to extract stress information from each element of the shield and cutterhead, enabling accurate predictions of whether the DS TBM would jam.

This numerical simulation method was applied to the shield jamming incident in the K10 + 242 section of the DXL tunnel. The simulation results indicate that the method is both reasonable and applicable. However, factors such as TBM advance rate, tunnel over-excavation, and the characteristics of the weak zone were not considered in this study. Therefore, future research should address these aspects.

## Data availability

The datasets used and/or analyzed during the current study available from the corresponding author on reasonable request.

Received: 3 September 2024; Accepted: 7 January 2025

## References

1.  Liu, Q. S. et al. Application and development of hard rock TBM and its prospect in China. Tunn. Undergr. Space Technol. 57 , 33-46. https://doi.org/10.1016/j.tust.2016.01.034 (2016).
2.  Huang, X., Liu, Q. S., Shi, K., Pan, Y. C. &amp; Liu, J. P . Application and prospect of hard rock TBM for deep roadway construction in coal mines. Tunn. Undergr. Space Technol. 73 , 105-126. https://doi.org/10.1016/j.tust.2017.12.010 (2018).
3.  Zhang, Y. et al. Failure characteristics and development mechanism of fault rockburst in a deep TBM tunnel: a case study. Acta. Geotech. 18 , 5575-5596. https://doi.org/10.1007/s11440-023-01883-8 (2023).
4.  Han,  X.,  Liang,  X.  M.,  Y e,  F .,  Wang,  X.  &amp;  Chen,  Z.  M.  Statistics  and  construction  methods  for  deep  TBM  tunnels  with  high geostress: A case study of Qinling Tunnel in Hanjiang-Weihe River Diversion Project. Eng. Fall. Anal. 138 , 106301.  h t t p s : / / d o i . o r g / 1 0 . 1 0 1 6 / j . e n g f a i l a n a l . 20 2 2 . 1 0 6 3 0 1  (2022).
5.  Deng, H. S., Fu, H. L., Shi, Y., Zhaog, Y. Y. &amp; Hou, W . Z. Countermeasures against large deformation of deep-buried soft rock tunnels in areas with high geostress: A case study. Tunn. Undergr. Space Technol. 119 , 104238. https://doi.org/10.1016/j.tust.2021.104238 (2022).
6.  Ates, U., Bilgin, N. &amp; Copur, H. Estimating torque, thrust and other design parameters of different type TBMs with some criticism to TBMs used in Turkish tunneling projects. Tunn. Undergr. Space Technol. 40 , 46-63. https://doi.org/10.1016/j.tust.2013.09.004 (2014).
7.  Zhang, Z. X., Wang, S. F., Huang, X. &amp; Kwok, C. Y. TBM-block interaction during TBM tunneling in rock masses: block classification and identification. Int. J. Geomech. 17 , E4016001. https://doi.org/10.1061/(ASCE)GM.1943-5622.0000640 (2017).
8.  Koopialipoor, M. et al. Predicting tunnel boring machine performance through a mew model based on the group method of data handling. Bull. Eng. Geol. Environ. 78 , 3799-3813. https://doi.org/10.1007/s10064-018-1349-8 (2019).
9.  Cui, G. Y. &amp; Ke, X. Rescue technology of the jamming accident for the double-shield TBM in complex geological conditions: A case study. Alex. Eng. J. 79 , 374-389. https://doi.org/10.1016/j.aej.2023.08.032 (2023).
10.  Hasanpour, R., Rostami, J. &amp; Ünver, B. 3D finite difference model for simulation of double shield TBM tunneling in squeezing grounds. Tunn. Undergr. Space Technol. 40 , 109-126. https://doi.org/10.1016/j.tust.2013.09.012 (2014).
11.  Hasanpour, R. &amp; Rostami, J. Impact of Advance Rate on Entrapment Risk of a Double-Shielded TBM in Squeezing Ground. Rock Mech. Rock. Eng. 48 , 1115-1130. https://doi.org/10.1007/s00603-014-0645-2 (2015).
12.  Abdollahi, M. S., Najafi, M., Bafghi, A. Y. &amp; Marji, M. F. A 3D numerical model to determine suitable reinforcement strategies for passing TBM through a fault zone, a case study\_ Safaroud water transmission tunnel. Iran. Tunn. Undergr. Space Technol. 88 , 186-199. https://doi.org/10.1016/j.tust.2019.03.008 (2019).
13.  Lin, P ., Yu, T. F ., Xu, Z. H., Shao, R. Q. &amp; Wang, W . Y . Geochemical, mineralogical, and microstructural characteristics of fault rocks and their impact on TBM jamming: a case study. Bull. Eng. Geol. Environ. 81 ,  64.  https://doi.org/10.1007/s10064-021-02548-0 (2022).
14.  Ramoni, M. &amp; Anagnostou, G. Tunnel boring machines under squeezing conditions. Tunn. Undergr. Space Technol. 25 , 139-157. https://doi.org/10.1016/j.tust.2009.10.003 (2010).
15.  Smith, J. V . Assessing the ability of rock masses to support block breakage at the TBM cutter face. Tunn. Undergr. Space Technol. 57 , 91-98. https://doi.org/10.1016/j.tust.2016.01.012 (2016).
16.  Xu, Z. H. et al. Hard-rock TBM jamming subject to adverse geological conditions: Influencing factor, hazard mode and a case study of Gaoligongshan Tunnel. Tunn. Undergr. Space Technol. 108 , 103683. https://doi.org/10.1016/j.tust.2020.103683 (2021).
17.  Dash,  B.,  Murthy,  V .  M.  S.  R.  &amp;  Chattopadhyaya,  S.  Design  Aspects  Governing  Disc  Cutters  and  Cutterheads  of  Hard  Rock TBM-A Review. Mining Metall Explor. 41 , 219-237. https://doi.org/10.1007/s42461-024-00923-5 (2024).
18.  Hasanpour, R. Advance numerical simulation of tunneling by using a double shield TBM. Comput. Geotech. 57 , 37-52.  h t t p s : / / d o i . o r g/ 1 0 . 1 0 1 6 / j . c o m p g e o . 2 0 1 4 . 0 1 . 0 0 2  (2014).
19.  Hou, S. K. &amp; Liu, Y. R. Numerical simulations of double-shield BMtunneling for analyzing shieldjamming control factors. Journal of Tsinghua University (Science and Technology). 61 , 809-817.https://doi.org/10.16511/j.cnki.qhdxxb.2021.26.013 (2021).
20.  Aydan, Ö., Akagi, T. &amp; Kawamoto, T. The squeezing potential of rock around tunnels: Theory and prediction with examples taken from Japan. Rock Mech. Rock. Eng. 29 , 125-143. https://doi.org/10.1007/BF01032650 (1996).
21.  Ramoni,  M.  &amp;  Anagnostou,  G.  The  Interaction  Between  Shield,  Ground  and  Tunnel  Support  in  TBM  Tunnelling  Through Squeezing Ground. Rock Mech. Rock. Eng. 44 , 37-61. https://doi.org/10.1007/s00603-010-0103-8 (2011).
22.  Wu, X. Z., Jiang, Y. J., Guan, Z. C. &amp; Gong, B. Influence of confining pressure-dependent Young's modulus on the convergence of underground excavation. Tunn. Undergr. Space Technol. 83 , 135-144. https://doi.org/10.1016/j.tust.2018.09.030 (2019).
23.  Carranza-Torres, C. &amp; Fairhurst, C. Application of the Convergence-Confinement Method of Tunnel Design to Rock Masses That Satisfy the Hoek-Brown Failure Criterion. Tunn. Undergr. Space Technol. 15 , 187-213.  h t t p s : / / d o i . o r g / 1 0 . 1 0 1 6 / S 0 8 8 6 - 7 7 9 8 ( 0 0 ) 0 0 0 46 - 8  (2000).
24.  Lee, Y. L., Ma, C. H. &amp; Lee, C. M. An Improved Incremental Procedure for the Ground Reaction Based on Hoek-Brown Failure Criterion  in  the  Tunnel  Convergence-Confinement  Method. Mathematics. 11 ,  3389.  https://doi.org/10.3390/math11153389 (2023).
25.  Zhang,  J.  Z.  &amp;  Zhou,  X.  P .  Time-dependent  jamming  mechanism  for  Single-Shield  TBM  tunneling  in  squeezing  rock. Tunn. Undergr. Space Technol. 69 , 209-222. https://doi.org/10.1016/j.tust.2017.06.020 (2017).
26.  Hasanpour, R., Schmitt, J., Ozcelik, Y. &amp; Rostami, J. Examining the effect of adverse geological conditions on jamming of a single shielded TBM in Uluabat tunnel using numerical modeling. J Rock Mech. Geotech. 9 , 1112-1122.  h t t p s : / / d o i . o r g / 1 0 . 1 0 1 6 / j . j r m g e . 20 1 7 . 0 5 . 0 1 0  (2017).
27.  de la Fuente, M., Sulem, J., Taherzadeh, R. &amp; Subrin, D. Tunneling in Squeezing Ground: Effect of the Excavation Method. Rock Mech. Rock. Eng. 53 , 601-623. https://doi.org/10.1007/s00603-019-01931-4 (2020).
28.  Majumder, D., Viladkar, M. N. &amp; Singh, M. Numerical Modelling of Tunnels Excavated in Squeezing Ground Condition: A Case Study. Arab. J. Sci. Eng. 48 , 4657-4673. https://doi.org/10.1007/s13369-022-07098-5 (2023).
29.  Chen, J. L., Yang, S. Q., Du, L. K., Wen, S. &amp; Zhang, J. Y. Three-dimensional numerical simulation on interaction between doubleshieldTBM and surrounding rock mass in composite ground. Chin. J. Rock Mech. Eng. 35 , 511-523.  h t t p s : / / d o i . o r g / 1 0 . 1 3 7 2 2 / j . c n ki . j r m e . 2 0 1 5 . 0 6 9 3  (2016).

30.  Feng, W . Study on the in-situ stress characteristics and thestability of surrounding rock by double shield TBM excavation of the duoxiongla tunnel in tibet. (Southwest Jiaotong University Master, 2018).
31.  Wang, T. Study on the interaction mechanism between double shield TBM tunneling and surrounding rocks in douxiongla a mountain of tibet. (Southwest Jiaotong University Master, 2018).
32.  Li, C. Y. et al. double-shield TBM tunnel based on advance borehole monitoring and inversion analysis. Tunn. Undergr. Space Technol. 103 , 103513. https://doi.org/10.1016/j.tust.2020.103513 (2020).
33.  Wen, S., Yang, S. Q., Dong, Z. F. &amp; Zhao, L. M. TBM jamming mechanism and control measures in deep buried tunnels. Chin. J. Rock Mech. Eng. 37 , 1271-1277 (2015).
34.  Sun, J. D. et al. A new prediction model for disc cutter wear based on Cerchar Abrasivity Index. Wear h t t ps : / / d o i . or g / 1 0 . 1 0 1 6 / j . we a r . 2 0 2 3 . 20 4 9 2 7  (2023).
35.  Wang, L. H., Li, H. P ., Zhao, X. J. &amp; Zhang, Q. Development of a prediction model for the wear evolution of disc cutters on rock TBM cutterhead. Tunn. Undergr. Space Technol. 67 , 147-157. https://doi.org/10.1016/j.tust.2017.05.003 (2017).
36.  Yan, C. Z., Wang, T., Zheng, Y. C., Zheng, H. &amp; Ali, S. Insights into the Effect of Water Content on Mudstone Fragmentation and Cutter Force during TBM Cutter Indentation via the Combined Finite-Discrete Element Method. Rock Mech. Rock. Eng. 57 , 2877-2912. https://doi.org/10.1007/s00603-023-03700-w (2024).
37.  Zhou, G. H. et al. Study on rock-breaking efficiency evaluation of TBM disc cutters based on Rostami prediction equations. Front. Earth Sci. https://doi.org/10.3389/feart.2023.1178127 (2023).
38.  Erharter, G. H., Goliasch, R. &amp; Marcher, T. On the Effect of Shield Friction in Hard Rock TBM Excavation. Rock Mech. Rock. Eng. 56 , 3077-3092. https://doi.org/10.1007/s00603-022-03211-0 (2023).
39.  Zhou, X. P . &amp; Zhai, S. F. Estimation of the cutterhead torque for earth pressure balance TBM under mixed-face conditions. Tunn. Undergr. Space Technol. 74 , 217-229. https://doi.org/10.1016/j.tust.2018.01.025 (2018).
40.  Shi, H., Yang, H. Y., Gong, G. F. &amp; Wang, L. T. Determination of the cutterhead torque for EPB shield tunneling machine. Automat. Constr. 20 , 1087-1095. https://doi.org/10.1016/j.autcon.2011.04.010 (2011).
41.  Yang, Z. Y. et al. Characteristics of conditioned sand for EPB shield and its influence on cutterhead torque. Acta. Geotech. 17 , 5813-5828. https://doi.org/10.1007/s11440-022-01666-7 (2022).
42.  Li, X. et al. Deformation characteristics and damage evolution analysis of weak interlayer zone in fractured underground cavern. Tunn. Undergr. Space Technol. https://doi.org/10.1016/j.tust.2024.105686 (2024).

## Acknowledgements

We would like to express our heartfelt thanks to those who contributed to the review of this article and to the editors.

## Author contributions

Z. W. W. wrote the main manuscript text. M. W . provided ideas, funding for the research. Y. L., Y. S. L., X. Y. T. &amp; X. T. They participated in numerical simulation experiments and numerical analysis. All authors reviewed the manuscript.

## Funding

This research was supported by the National Key R&amp;D Project (Grant No. 2021YFB2300801) and the National Natural Science Foundation of China (Grant No. 42072342).

## Declarations

## Competing interests

The authors declare no competing interests.

## Additional information

Correspondence and requests for materials should be addressed to M.W .

Reprints and permissions information is available at www.nature.com/reprints.

Publisher's note Springer Nature remains neutral with regard to jurisdictional claims in published maps and institutional affiliations.

Open Access This article is licensed under a Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License, which permits any non-commercial use, sharing, distribution and reproduction in any medium or format, as long as you give appropriate credit to the original author(s) and the source, provide a link to the Creative Commons licence, and indicate if you modified the licensed material. You do not have permission under this licence to share adapted material derived from this article or parts of it. The images or other third party material in this article are included in the article's Creative Commons licence, unless indicated otherwise in a credit line to the material. If material is not included in the article's Creative Commons licence and your intended use is not permitted by statutory regulation or exceeds the permitted use, you will need to obtain permission directly from the copyright holder. To view a copy of this licence, visit  h t t p : / / c r e a t i v e c o m m o ns . o r g / l i c e n s e s / b y - n c - n d / 4 . 0/ .

© The Author(s) 2025
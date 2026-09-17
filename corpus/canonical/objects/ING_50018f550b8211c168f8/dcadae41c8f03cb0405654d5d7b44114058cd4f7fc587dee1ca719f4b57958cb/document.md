## EPB-TBM tunnel under internal pressure: Assessment of serviceability

N.A. Labanda &amp; A.O. Sfriso

SRK Consulting, Argentina

## D. Tsingas &amp; R. Aradas

Jacobs, Argentina

## M. Martini

Salini-Impregilo S.p.A., Italy

ABSTRACT: The Mantanza-Riachuelo basin recovery is one of the most ambitious environmental projects under construction in Argentina. In this context, the sanitary bureau of the metropolitan area of Buenos Aires (AySA) is building a sewage collection network to transport the waste water of the population in the southern area of the city, composed by almost fi ve million people. The most complex tunnel in this big project is named Lot 3 , an outfall EPB-TBM tunnel starting at a shaft located at the Rio de la Plata margin and running under the river 12 km to a discharge area.

The tunnel runs through soft clay belonging to the post-pampeano formation and dense sands of the Puelchese formation. In operation, it will be pressurized by a pumping station which will produce a piezometer head that, in the fi rst 2000 m, might be eventually higher than the confining pressure around the tunnel.

This paper presents the numerical analysis of the structural forces acting on the tunnel rings using a riskoriented approach that considers the stochastic nature of materials, stratigraphy and tunnel-ground inter­ action. The compression of the lining is evaluated and compared with field measurements in order to predict the structural forces and the risk of the rings going into tension beyond the structural capacity of the system.

## 1 INTRODUCTION

The Matanza-Riachuelo river fl ows along the ripar­ ian lands between the City and the Province of Buenos Aires (Argentina). It is a water stream 64 km long that fl ows into the Rio de la Plata . The river is heavily contaminated with industrial and residential wastewater discharged from both mar­ gins with limited -if any- pre-discharge water treat­ ment process.

The Matanza-Riachuelo basin recovery project is an ambitious plan to manage the wastewater from the left margin of the Rio de la Plata through a sewerage interceptor tunnel, a treatment plant and a discharge tunnel into the Rio de la Plata . The project is divided into several contracts. One of them, named Lot 3 , holds the outfall tunnel, an EPB-TBM tunnel running 35 meters below the riverbed of the Rio de la Plata . A global scheme of the outfall, which is the sub­ ject of this paper, is presented in Figure 1. The tunnel has an internal diameter of 4.3 m and a total length of 12 km, including a 1.5 km

diffusor zone with 34 standpipe risers, 28 m long, that daylight in the riverbed. It is being driven through soft clays of the Postpampeano formation and dense sands from the Puelchense formation. Water flows by gravity from a pumping station onshore built into the access shaft. Figure 2 shows the longitudinal elevation of the tunnel proposed in pre-feasibility stage.

The tunnel will be subjected to a maximum internal pressure of 550 kPa and an external water pressure from 330 to 420 kPa, resulting in a net outwards pressure 130 to 220 kPa. Further infor­ mation about the tunnel and its design can be found in Aradas et al. (2019). EPB-TBMs employ muck to balance water and soil pressure at the tunnel face. By managing the excavation param­ eters i.e., screw conveyor speed, advance rate, thrust force, face support pressure, etc., the ground relaxation and, consequently, structural forces in the lining can be somewhat controlled. This aspect, usually not of high interest, is important in the case of segmental pressurized tunnels working at high internal pressure.

Figure 1. Location of Matanza-Riachuelo outfall (Buenos Aires, Argentina). The thin red line is the border between the city of buenos aires and the province of buenos aires. The Riachuelo river is along the south border.

<!-- image -->

Geographical map

A common feature found when reviewing case histories of pressurized tunnels in soft ground is the recommendation to neglect the contribution of the external ground confinement as a safety redun­ dancy. This hypothesis, despite being conservative from the perspective of confinement, produces an unrealistic estimate of the deformation of the lining ring and therefore of the resulting bending moments. On the other hand, the adoption of a nonzero effective external ground pressure is challenging as it is largely dependent on the TBMsoil interaction during excavation and on the long­ term creep behavior of the soil.

An assessment of the compression induced in the segmental rings by ground pressure via sto­ chastic numerical models and calibrated using back-analysis after field measurements is pre­ sented in this paper. Two rings are studied in this proposal: N  237 and N  497, embedded in soft clays and dense sands, respectively.

## 2 CONSTITUTIVE MODELING FOR SOIL AND LINING CONCRETE

f The tunnel was designed in pre-feasibility stage to be driven through dense sands, as shown in Figure 2, where yellow layers represent the Puelchense forma­ tion. However, fi eld conditions departed from this assumption in several places. For instance, highplasticity clays belonging to the Paranaense forma­ tion were detected in the conveyor belt (Figure 3) betwen chainages PK 0+294 to PK 0+586. Ring N  237 placed at PK 0+316 and consequently, embedded in clay, and Ring N  497 placed at PK 0 +681, embedded in dense sand, were instrumented with strain gauges whose results allow for evaluating the compression load of the tunnel lining in two dif­ erent grounds.

t The Hardening soil small (HSsmall) constitu­ ive model was used to simulate the mechanical behavior of soils and calibrated by in situ and lab tests and local experience. Statistical variabil­ ity of the friction angle was estimated using the 6-sigma method. A correlation between the com­ pression index Cc and the liquid limit ω L for Postpampeano clays was fi rst reported by (Sfriso 1997) with a COV ¼ 0 : 30, and was later updated by(Ledesma 2008) as presented in Figure 4, with a COV ¼ 0 : 12. Swelling index Cs , relevant for the estimation of the interaction forces, correlates with Cc by:

Figure 3. High-plasticity clay detected in the TBM ' s con­ veyor belt.

<!-- image -->

Photograph

Figure 2. Matanza-Riachuelo outfall: longitudinal elevation of the tunnel proposed in pre-feasibility stage.

<!-- image -->

Engineering drawing

Figure 4. Compression index Cc versus liquid limit for the post-pampeano formation.

<!-- image -->

Scatter plot

HSsmall requires the definition of elastic and hardE ref E ref ening parameters E ref , and G ref , among oed , ur 50 0 other parameters. They were computed as

being l ur the Poisson modulus, K 0 the at rest earth pressure coefficient, pref the reference pressure and e 0 the initial void ratio.

Uncertainties in the properties of the clay where the ring N  237 is placed were dealt with by consid­ ering a stochastic approach to bracket the prediction of the structural forces acting on the lining. The parameters employed are presented in Table 1, where some properties are defined using probability distributions that will be described in the next sec­ tion. A deterministic set of parameters were used for dense sand because its influence is negligible for the ring under analysis.

The structural stiffness of the lining was reduced to account for the segment joints using the MuirWood expression (Muir Wood 1975)

Table 1. Constitutive models and parameters used.

|           | Unit             | Soft clay                                       | Sandy soils                                |
|-----------|------------------|-------------------------------------------------|--------------------------------------------|
| Model     | - - kN =  kPa  | HSsmall Undrained (A) 16.0 P.D. 0 0 P.D. 3 10 - | HSsmall Drained 20.5 32 0 0 200 4 10 - 120 |
| Drainage  |                  |                                                 |                                            |
| γ         | 3 m              |                                                 |                                            |
| ¢ 0       |                  |                                                 |                                            |
| c 0       |                  |                                                 |                                            |
| ψ         |                  |                                                 |                                            |
| G ref 0   | MPa              |                                                 |                                            |
| γ 0 : 7   | -                |                                                 |                                            |
| E ref ur  | MPa              | P.D.                                            |                                            |
| E ref 50  | MPa              | P.D.                                            | 40                                         |
| E ref oed | MPa              | P.D.                                            | 40                                         |
| m         | -                | 1.0                                             | 0.5                                        |
| l ur      | -                | 0.20                                            | 0.20                                       |
| OCR       | -                | 1.00                                            | 1.00                                       |
| K nc 0    | -                | 0 1 - sin ¢                                     | 0 1 - sin ¢                                |
| R inter   | -                | 0.90                                            | 0.70                                       |
| k         | 10 - 6 m/s       | 0.005                                           | 1.00                                       |

where I red is the reduced moment of inertia, I real is the real moment of inertia and n is the number of lining segments in each ring.

## 3 STATISTICAL CHARACTERIZATION

## 3.1 Soil parameters

The proposed risk analysis requires that the variability of soil parameters be defined together with the bound­ aries presented in Equation (4). A statistical character­ ization for the effective friction angle ¢ 0 and the compression index Cc is presented in Figure 5. Prob­ ability distributions were obtained using the experi­ mental data shown in Figure 4 and classical correlations for the friction angle. Considering values a ± σ a for parameters Cc , ¢ 0 and boundary multipliers in Equations (1) and (4), 2 4 ¼ 16 permutations can be performed to reproduce drained triaxial tests, where a is the mean value and σ a is the standard deviation of the considered parameter. Results are presented in Figure 6 and compared with three experimental tests for this project. Good fi tting is obtained for consolida­ tion mean pressures of p ¼ 50 kPa , p ¼ 100 kPa and p ¼ 200 kPa .

## 3.2 Lining segment concrete

The Young ' s modulus of concrete is required to com­ pute stresses and forces out of microstrains measured by the monitoring system. A histogram of 480 simple compression tests, a normal probability function and a cumulative probability function are shown in Figure 7. In order to compute the concrete stiffness at low strains Eci , the following expression is used (CEB­ FIP 1993)

Figure 5. Probability distribution for friction angle and compressibility index of the Postpampeano formation.

<!-- image -->

Line chart

<!-- image -->

Line chart

Figure 6. Drained triaxial test, comparisons between laboratory tests and HSsmall simulations.

<!-- image -->

Line chart

with Eco ¼ 21500 MPa , fcmo ¼ 10 MPa and fcm unconfined compression resistance of the sample.

Considering a mean value fcm ¼ 59 : 6 MPa and a standard deviation σ fcm ¼ 4 : 94 MPa , deformations measured by strain gauges can be translated into structural forces.

## 3.3 Water level in the river

Variable water level in the river is one of the key contributors to uncertainty of the compression forces acting on the tunnel lining, making its statistical characterization a critical aspect of the analysis. The Argentine Naval Hydrographic Service provided the time-history evolution of the river over the last few years. Taking the data corresponding to the first semester of 2018, where the rings under analysis were installed, a normal probability function is fi tted and presented in Figure 8, and compared with fi eld measurements. A mean elevation 0 : 945 m and a standard deviation 0 : 547 m were considered in the analyses.

Figure 7. Histogram of unconfined compression test results for 480 samples of lining concrete. Probability distribution and cumulative distribution.

<!-- image -->

Line chart

Figure 8. Water level in the Rio de la Plata . Probability dis­ tribution and cumulative distribution.

## 4 NUMERICAL RESULTS AND COMPARISON WITH FIELD MEASUREMENTS

## 4.1 Ground relaxation estimate by 3D modeling in ring N  237

A three dimensional model of the excavation was developed to estimate the ground relaxation induced by the TBM drive in ring N  237. The TBM shield was simulated considering a face contraction cref ¼ 0 : 4% and a tail-to-face contraction increment cinc ; axial ¼ 0 : 03571%/ m . A grout pressure equal to the total fi eld stress plus 0.5 bar was applied in the TBMs tail. The face pressure was calibrated with data provided by the sensors in the TBM, imposing a normal surface load equal to the measured value presented in Figure 9. The 3D model is presented in Figure 10. Due to the high computational effort required by this kind of simulations, mean values for all materials were used and a single model is ana­ lyzed. The excavation sequence was repeated until a reasonably stabilized zone was obtained.

Settlements in the tunnel crown and effective verti­ cal stresses in the stabilized section are plotted in Figure 11. The mean value for settlement is close to 30 mm, while the effective vertical stress is around 145 kPa. These values were used to fi t a ground relax­ ation factor in the two dimensional models presented in the next section.

## 4.2 Structural forces in ring N  237

In order to evaluate the risk of tension forces being developed in the ring, a 2D model was developed and the influence of uncertainties in input data in Equations (1) and (4), river water level and concrete quality were studied.

Figure 9. Sensor data from the TBM face.

<!-- image -->

Line chart

Figure 10. 3D model of settlements after excavation.

<!-- image -->

Engineering drawing

The numerical model and construction stages are summarized in Figure 12. The excavation sequence was simulated in 2D by partial stress relaxation using the β -method, i.e. applying E Mstage ¼ 1 - β 5 1. Grout pressure in TBMs tail was simulated as a distributed load, the (impervious) lining was activated and consolidation until 99 % dissipation of excess pore pressure -the expected condition by the time the tunnel starts operatingwas allowed for. In operation, an internal head of 15.5 m, 14.0 to 15.1 meters above the river level was applied. 2 5 ¼ 32 models were gener­ ated by performing all permutations of data presented in Table 2.

Figure 12. 2D model of ring N  237. (a) Excavation using E M stage 5 1 (b) grout pressure (c) Activation of lining and consolidation (d) Internal pressure in operation.

<!-- image -->

Engineering drawing

Table 2. Parameter ranges used to compute ground relax­ ation curves.

|                  | Unit   |   Lower bound |   Upper Bound |
|------------------|--------|---------------|---------------|
| C c              | -      |         0.367 |         0.497 |
| C s (eq. 1)      | -      |           0.1 |           0.2 |
| E ref 50 (eq. 4) | -      |          1.25 |          1.90 |
| ¢ 0              |       |            24 |            26 |
| River Elevation  | m      |         0.398 |         1.492 |

Figure 11. Settlements of tunnel crown and effective vertical stress in stabilized section.

<!-- image -->

Line chart

Figure 13 shows the obtained ground relaxation curves and both displacement and effective vertical stress measured in the tunnel crown, plotted in terms of E M stage . The purpose of these curves is to obtain, in a 2D model, a stress state similar to the stabilized sec­ tion of a 3D model.

By getting into the graph with the mean crown dis­ placement obtained in the 3D model, and intersecting curves corresponding to the 2D crown displacement (in blue), a range of E M stage values were obtained. The range of effective contact stresses obtained rea­ sonably contains the mean value obtained in the 3D model. Values adopted for the analysis are E M stage ¼ ½ 0 : 35 ; 0 : 40 ; 0 : 45 ; 0 : 50 ; 0 : 55 ; 0 : 60 ] . Tables 2 and 3 show values employed to calculate structural forces in the lining. Together with the E M stage values, a set of 6 x 2 6 ¼ 384 numerical models were obtained.

Figure 14 plots translation and ovalization compo­ nents of the tunnel lining obtained with all permuta­ tions, during construction. The model shows that, for low relaxation values, a little rebound of the tunnel is observed and an ovalization pattern where the vertical stress is larger than the horizontal stress is obtained. While the ground relaxation increases, a tunnel settle­ ment and an invertion in the tunnel ovalization is obtained. Figure 15 shows the obtained structural forces for all models in the construction stage, compar­ ing those with fi eld data measured in ring N  237 using strain gauges. The actual concrete stiffness was used to translate deformations into forces, as indicated with markers for the mean value and lines for the standard deviation band.

Figure 13. Ground relaxation curves for 2 5 32 permuta­ tions in soil parameters and river water level. ¼ Ring N  237.

<!-- image -->

Line chart

Table 3. Concrete parameters used in permutations to compute structural forces.

|      | Unit   |   Lower bound |   Upper Bound |
|------|--------|---------------|---------------|
| f cm | MPa    |          54.6 |          64.5 |

Figure 14. Translation and ovalization of ring N  237 during construction.

<!-- image -->

Engineering drawing

Figure 15. Structural forces of ring N  237 in construction stage and comparison with fi eld measurements.

<!-- image -->

Line chart

It can be seen that the proposed procedure prodcues a good fitting with field data for both bending moments and normal forces. For low E M stage values, hihger normal forces and lower bending moments are obtained, being the last in agreement with the ovalization pattern. If E M stage is higher, normal forces decrease and bending moments increase. Figure 16 shows a comparison of the mobilized shear stress τ mob for a 2D model and a stabilized section of the 3D model. For sake of simplicity, a single represen­ tative 2D model is shown but similar stress patterns are obtained in all permutations. It is interesting to see that the mobilized shear, a measure of the tunnel arch­ ing effect, is similar in both cases. After ensuring the validation of the proposed methodology, a study of the tunnel lining in operation was performed and the risk of tension forces being developed was analyzed.

Figure 16. Comparison of τ mob between the 2D model and a stabilized section of the 3D model.

<!-- image -->

Bar chart

## 4.3 Structural forces in operation in ring N  237

Lining forces in operation in ring N  237 are evalu­ ated in this section. Figure 17 shows the translation and ovalization for the tunnel under internal pres­ sure. Results are similar than those obtained for the construction stage, with a small increment in tunnel settlements due to the waste water weight. Ovaliza­ tion remains almost equal by virtue of the hydro­ static not generating higher deformations compared with the construction stage. Figure 18 plots the structural forces for all considered permutations. Results show that bending moments and shear forces are almost the same than during construction. Normal compression forces, however, decrease dra­ matically from values - 1900 ± 100 kN before the internal pressure to - 200 ± 150 kN in service. Des­ pite this fact, even for high relaxation values i.e. E M stage ¼ 0 : 60, lining is still under compression, and tension in connecting bolts is avoided.

Figure 17. Translation and ovalization of ring N  237 in normal operation stage.

<!-- image -->

Engineering drawing

Figure 18. Structural forces of ring N  237 in normal operation.

<!-- image -->

Line chart

## 4.4 Structural forces in ring N  497

Structural forces and deformations in the most adverse chainage of the tunnel, represented by ring N  497, is presented in this section.

The procedure for the back analysis used in this case is different than the used in the previous case, avoiding 3D calculations and fixing the ground relaxation by means of E M stage and field measurements. The simulation procedure is the same than in the previous case. Soil proper­ ties for the soft clay and overlying materials were defined using the mean values presented in previous sections, while parameters for dense sand were considered to be permuted using bounds presented in Table 4.

A two dimensional base model considering the stratigraphy corresponding to chainage PK 0 +681 is presented in Figure 19. The construction procedure is the same than in the previous case.

The effective friction angle ¢ 0 was defined as the sum of the constant volume friction angle ¢ cv ¼ 30  and the dilatancy angle ψ presented above.

Ground relaxation curves for current stratig­ raphy are shown in Figure 20. Displacement are considerably lower than those observed for soft clays in Figure 13. Also, a lower ground mobil­ ization is required to achieve the same confine­ ment pressure on the lining. Concrete parameters presented in Table 3, together with relaxations E M stage ¼ ½ 0 : 35 ; 0 : 45 ; 0 : 55 ] , produce 192 sets of paramteres that were employed to do the stochastic analysis. Results are expressed in terms of bending moments, normal and shear forces during construction, and are shown together with fi eld measurements for ring N  497 in Figure 21. Good fitting is found between numerical and experimental results in bending moments, while predictions in normal forces tend to underestimate the compression forces in the lining. Tunnel translation and ovalization during construction are plotted in Figure 22, where vertical displacements are negligible while ovalization tends to increase with ground relaxation.

Table 4. Parameters used to compute ground relaxation curves in dense sands.

|                 | Unit   |   Lower bound |   Upper Bound |
|-----------------|--------|---------------|---------------|
| ψ               |       |           8.0 |          10.0 |
| E ref 50        | [kPa]  |         82000 |         98000 |
| E ref ur        | [kPa]  |        200000 |        240000 |
| G ref 0         | [kPa]  |        280000 |        400000 |
| River Elevation | m      |         0.398 |         1.492 |

Figure 19. 2D base model for ring N  497. (a) Excavaction with E M stage (b) grout pressure application (c) Lining construction (d) Tunnel under internal pressure in normal operation.

<!-- image -->

Screenshot from computer

Figure 20. Ground relaxation curves for 2 5 32 permuta­ tions in soil parameters and river water level. ¼ Ring N  497.

<!-- image -->

Line chart

Figure 21. Structural forces of ring N  497 in construction stage and comparisons with fi eld measurements.

<!-- image -->

Line chart

Figure 22. Translation and ovalization of ring N  497 during construction.

<!-- image -->

Line chart

## 4.5 Structural forces in operation, ring N  497

Using the calibrated numerical model, an assess­ ment of serviceability in operation (under internal pressure) is presented in this section.

Bending moments, normal and shear forces in the lining are presented in Figure 23, while translation and ovalization are shown in Figure 24.

Similar to ring N  237, internal pressure in the tunnel does not change much the bending moments, shear forces and lining deformations. However, normal forces were affected, being the internal pressure produced by the waste water transportation similar or even higher than the ground and water pressure applied in the tunnel lining. In this aspect, the behavior is different than the section embedded in clay; dense sands produce less pre-compression in the lining, thus increasing the probability to experience tensile forces in the joint bolts.

Figure 23. Structural forces of ring N  497 in operation.

<!-- image -->

Line chart

Figure 24. Translation and ovalization of ring N  497 in operation.

<!-- image -->

Engineering drawing

## 5 CONCLUSIONS

Pressurized TBM tunnels are traditionally designed neglecting the pre-compression induced by the soil-structure interaction, largely due to the uncertainties involved in their estimation. Despite enormous progress in the monitoring equipments and technology, and also in the numerical model­ ing tools available, it is still a challenging task to estimate a lower-bound contact pressure induced in the tunnel lining, reliable enough for being employed in the joint bolt design.

A procedure for the risk assessment and the computation of the probability to have tension forces in the tunnel lining during the operation were presented and discussed in this paper.

The stochastic nature of some relevant parameters was acknowledged, and the calibration of probability density distributions was done based on experience, published data and usual correlations for selected crit­ ical parameters. In the same way, a statistical analysis of the river level and the properties of the concrete used to manufacture lining segments was detailed and used in the simulations. A fi rst stage, consisting in a convergence analysis using 3D simulations of the excavation sequence was briefly discussed, and mean values for vertical crown displacement and effective stress were shown and used to define an equivalent ground relaxation for the 2D models.

After defining a reasonable range for E M stage , a set of 6 x 2 6 ¼ 384 permutations were used in the 2D numerical model to estimate a range for the struc­ tural loads. A comparison with results obtained by the strain gauges during the tunnel construction in two rings was presented, showing a good agreement between the predictions and fi eld measurements. Using this validation, the structural forces in service were estimated, concluding that the probability to support tension forces in this stage are negilgible for rings embedded in soft clay, while it increases for rings embedded in dense sands if the ground relaxation is not properly controlled.

## ACKNOWLEDGMENTS

The authors would like to acknowledge the Argentine Naval Hydrographic Service (www. hidro.gov.ar) for providing the water level timehistory of the Rio de la Plata and Salini­ Impregilo-Chediak for permission to publish the data contained in this paper.

## REFERENCES

- Aradas, R., D. Tsingas, &amp; M. Martini (2019). The design of a segmentally lined tunnel for a large sewer outfall. lote 3 - emisario planta riachuelo, argentina. In World Tunnel Congress 2019, Naples - Italy . International Tunnel Asociation.
- CEB-FIP (1993). MODEL CODE 1990 . Thomas Telford Publishing.
- Ledesma, O. (2008). Calibración del Cam Clay para suelos del post-pampeano . Buenos Aires, Argentina: Tesis de grado de Ingeniería Civil - Universidad de Buenos Aires.
- Muir Wood, A. (1975). The circular tunnel in elastic ground. Géotechnique 25 (1), 115 - 127.
- Sfriso, A. (1997). Formación post-pampeano: predicción de su comportamiento mecánico. CLICJ - Caracas, Vene­ zuela , 1 - 10.
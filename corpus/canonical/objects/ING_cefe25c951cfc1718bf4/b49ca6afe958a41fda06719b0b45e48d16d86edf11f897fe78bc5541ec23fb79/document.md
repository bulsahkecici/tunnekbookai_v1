## ORIGINAL PAPER

## Distributed fiber optic shape sensing along shotcrete tunnel linings: Methodology, field applications, and monitoring results

<!-- image -->

Icon

Christoph M. Monsberger 1 · Werner Lienhart 1

Received: 30 July 2020 / Revised: 3 November 2020 / Accepted: 24 November 2020 / Published online: 27 January 2021 © The Author(s) 2021

## Abstract

Deformation monitoring and structural reliability assessment are key components in modern conventional tunneling. The state-of-the-art monitoring design is usually based on displacement measurements of geodetic targets using total stations paired with pointwise geotechnical sensors inside the tunnel lining. In recent years, distributed fiber optic sensing (DFOS) has become more popular in tunneling applications. DFOS measurements basically deliver internal strain and temperature distributions, but no direct relation to the tunnel shape's behavior. This paper introduces a novel sensing and evaluation concept, which combines DFOS strain measurements and geodetic displacement readings for distributed shape assessment along curved structures, such as tunnel cross-sections. The designed system was implemented into shotcrete tunnel crosssections as well as shaft linings and enables the determination of displacement profiles with high spatial resolution in the range of centimeters. Evaluations of continuous monitoring campaigns over several weeks as well as epoch-wise measurements performed by different DFOS sensing units in combination with stochastic analysis demonstrate the high potential of the developed approach and its capability to extend traditional monitoring methods in tunneling.

Keywords Distributed fiber optic sensors · Shape sensing · Shotcrete tunnel lining · Displacement sensing · Field applications · Tunneling

## 1  Introduction

The design of excavation and supporting methods in modern tunneling is usually based on geotechnical monitoring and reliable data interpretation to enable an assessment of the structural integrity and, finally, to guarantee a safe construction and operation. State-of-the-art monitoring approaches utilize displacement measurements of geodetic targets at the inner surface of the tunnel using total stations [22, 24, 25], which are however time-consuming and always require a line of sight between the instrument and the measured object. Therefore, the measurements might interfere with the regular tunnel construction work, involve risks for the surveying team, and can cause construction delays every time they are performed. Electrical sensors, e.g., vibrating wire sensors [23] or extensometers [2], may be installed in addition to

* Christoph M. Monsberger christoph.monsberger@tugraz.at

1 Institute of Engineering Geodesy and Measurement Systems, Graz University of Technology, Steyrergasse 30, 8010 Graz, Austria

3D monitoring targets inside the shotcrete lining to provide continuous in situ measurements. Nevertheless, the number of sensors inside the lining is limited due to practical reasons as each electrical sensor needs its own connecting cable to the data logger, and hence, information can only be obtained at particular locations of the lining.

Distributed fiber optic sensors (DFOS) are advantageous as the cable itself acts as the sensitive element and distributed measurements can be performed along the entire sensing fiber. Only one lead-in cable is necessary to realize a large number of monitoring points, that which significantly reduces the installation effort to gather strain values in the tunnel lining with a high spatial resolution. The DFOS utilization might be, however, limited, if major impairments with huge crack widths become prevalent along the lining or yielding elements are used to control large deformations. Although the sensing cable installation procedure is critical due to the harsh tunnel environment, DFOS have already been successfully implemented inside shotcrete tunnel linings. These existing installations are mainly focused on investigations of mechanical stress as a result of creepage, shrinkage, and/or rock pressure [9, 19, 28], as well as

<!-- image -->

Logo

123

<!-- image -->

Icon

convergence analysis [4, 10], but do not deliver concepts for fully distributed shape analysis along the lining. This paper introduces a distributed fiber optic shape sensing and evaluation approach, which utilizes DFOS strain measurements along different sensing layers in combination with pointwise displacement readings for fully distributed shape assessment along curved structures, such as tunnels. The developed system was implemented into shotcrete tunnel cross-sections as well as shaft linings at a railway tunnel currently under construction and extends conventional geodetic readings, which are carried out anyhow. The installations were interrogated by different DFOS sensing units based on Rayleigh and Brillouin scattering, whose basic characteristics are described in the following (sect. 2). Moreover, the designed shape sensing algorithm and its capabilities by means of stochastic analysis (sect. 3) are presented. Results of continuous monitoring campaigns and evaluations of epoch-wise follow-up measurements are shown and different evaluation setups are discussed (sect. 4). Finally, the outcomes are concluded and an outlook on future research aspects is given (sect. 5).

## 2   Distributed fiber optic monitoring system and practical aspects

Distributed fiber optic sensing systems use natural scattering of optical signals during the forward propagation along the sensing fiber. Small parts of these intensity losses are backscattering effects, whose spectral characteristics carry information about geometrical, physical, or chemical quantities. Backscattering effects can be basically divided into linear (Rayleigh) and non-linear (Raman and Brillouin) scattering. Raman-based systems are only sensitive to temperature, whereas Rayleigh as well as Brillouin instruments are sensitive to both, strain and temperature changes [8]. Their capabilities regarding spatial resolution and measurement accuracy are however significantly different, which is why, the applications presented in this paper were partially interrogated by two different sensing units to assess potential impacts of the DFOS characteristics on the shape sensing approach.

The used Rayleigh backscattering system OBR 4600 [14] from Luna Innovations Inc. enables distributed strain sensing with high spatial resolution of some millimeters, a measurement precision in the range of 1 μ m/m, and a measurement frequency of about 0.1 Hz. The usual sensing range is limited to 70 m, but can be extended up to 2 km using specially developed software components. This, however, results in limitations of the feasible measurement resolution of 4.1 μ m/m using a spatial resolution of 3 cm according to the manufacturer. These specifications can be confirmed by IGMS (Institute of Engineering Geodesy and Measurement Systems at Graz University of Technology) experiences in practical environment.

<!-- image -->

Logo

Unlike Rayleigh sensing units, Brillouin interrogators provide measurements over tens of kilometers, though with limitations in the measurement capabilities and, typically, significantly longer measurement times of several minutes. Based on the BOFDA (Brillouin Optical Frequency Domain Analysis) technique, the fTB 5020 from FibrisTerre GmbH (Germany) allows monitoring over 25 km with a spatial resolution of 0.5 m [5]. Under geotechnical conditions, a measurement precision between 2 and 10 μ m/m can be usually achieved depending on the sensing network.

In addition to the interrogation unit itself, the reliability and robustness of the DFOS cable are highly relevant to guarantee the integrity of the optical sensing fiber in harsh tunnel environment. Different manufactures offer such cables especially developed for strain monitoring in geotechnical applications, e.g., [26]. These can protect the optical fiber by a metal tube or even by a special steel armoring. The cables show good resistance against mechanical impacts and their suitability could be proven by various successful installations at different construction sites, e.g., [13, 16, 28]. The outer surface of selected cables is also structured to provide a solid connection with the surrounding shotcrete material. Since Rayleigh and Brillouin systems are strain and temperature sensitive, appropriate temperature compensation is important in practical applications. For that reason, specially designed temperature sensing cables [27] or sensing cables in loose tubes are typically installed parallel to the strain sensing cable to numerically correct the temperature impact.

The temperature-corrected raw measurement quantity (i.e., wavelength, frequency, or intensity) must be finally converted into strain. The parameters of the sensor characteristic curve often vary depending on the cable type as well as different batches of the same cable in some cases. Cable calibration is therefore essential to achieve accurate sensing results. IGMS developed a unique calibration facility [29] which enables highly precise, fully automatic calibration of strain sensors with lengths of up to 30 m under stable laboratory conditions. Individual calibrations are carried out prior to field applications to provide reliable conversion parameters for the used cable. Further information on the design of different strain sensing cables from Solifos AG and corresponding strain calibration results are presented in [17].

## 3   Shape sensing algorithm

## 3.1   Functional model

DFOS systems deliver distributed strain (and temperature) profiles along the longitudinal axis of the installed sensing fiber.

Multidimensional information can however also be captured if two or more fibers are parallelly aligned along the structure. This setup enables the determination of curvature profiles in case of bending orthogonal to the DFOS sensing direction.

It is known from elastic bending theory (e.g., [15]) that the deflection w at one specific sensing element s along an object can be described by

<!-- formula-not-decoded -->

where M is the bending moment, E the modulus of elasticity, and I y the moment of inertia at the observed position. The deflection w can also be expressed by the segment's curvature u1D705 and, therefore, by the bending radius R . The relation of the bending radius and the measured strain along the outer layer u1D716 out and the inner layer u1D716 in in combination with the distance between the fibers d enables a direct curvature acquisition from the DFOS measurements:

<!-- formula-not-decoded -->

Beside influencing shear stresses, the concrete object might also be affected by longitudinal stresses due to shrinkage, creepage, or temperature-induced expansion. These effects are taken into account by the longitudinal strain, which is equal to the mean strain value of both sensing layers u1D716 :

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

To obtain displacements orthogonal to the sensing direction, the distributed curvature values can be numerically double-integrated based on the difference equation method, as already introduced by [21]. The relation between the curvature u1D705 at the i -th position along an object and the deflection value w is described by

<!-- formula-not-decoded -->

where h is  the distance between the sensing points and, therefore, equal to the spatial resolution of the DFOS system. The linear functional model is given by

<!-- image -->

Flow chart

<!-- formula-not-decoded -->

where u1D6F4 u1D705 u1D705 describes the stochastic of the observations. A least-square adjustment based on the Gauß-Markov model can be finally used to derive the estimated deflection values ̂ w :

<!-- formula-not-decoded -->

The absolute position and orientation of the object is however unknown. The normal equation matrix N has therefore a rank deficiency of 2 and cannot be inverted without further information. For linear structures in geotechnics, this boundary-value problem is commonly solved using the cantilever beam approximation, where the starting point (i.e., the bottom point) and its orientation is assumed to be fixed.

For curved structures like tunnel linings, two sensing cables may be installed in circumferential direction, but with different distances to the center, see Fig. 1a. This results in slightly different sensing segment lengths d ( s ) along the outer and inner layer, which can be taken into account by the installation radii of the different layers [18]. Nevertheless, the values resulting from Eq. 2 only represent the curvature change due to shear stresses acting on the single sensing segment, i.e., stresses orthogonal to the tangent to the lining. Considering the curved initial geometry, the curvature impact within the two-dimensional coordinate system can be rewritten and expressed by:

<!-- image -->

Engineering drawing

Fig. 1 Shape sensing principle: a Schematic representation of crosssection profile; b detail of one single sensing segment along the lining

<!-- image -->

Logo

<!-- formula-not-decoded -->

where u1D711 is the orientation of the sensing segment relative to horizontal coordinate axis x (Fig. 1b). This geometry parameter can be initially retrieved from the planning model. The numerical integration process is performed individually for each coordinate direction. In contrast to the cantilever approximation, the boundary-value problem can be solved by extending the functional model with additional observations, e.g., pointwise displacements of geodetic targets ( u1D6E5 x TS , u1D6E5 y TS ) recorded by total stations at the jth position of the fiber optic installation along the lining:

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

The number of geodetic points is basically variable, but must be at least 2 to solve the boundary-value problem. Using more than two supporting points provides an estimation with redundancy, which enables an assessment of the correctness of the functional and the stochastical model.

<!-- image -->

Logo

The derived curvature values u1D705 x i and u1D705 y i are always related to the geometry of the lining. The workflow can hence be understood as an iterative approach, see Fig. 2, where the lining's geometry ( u1D711 ) is continuously updated. This evaluation procedure is performed as long as the total sum of squares (TSS) of the coordinate differences between the current and the previous iteration is decreasing. The coordinates in both directions can be finally determined by adding the estimated differential supplements u1D6E5 x i and u1D6E5 y i to the initial model shape.

## 3.2   Stochastic analysis

It is obvious that measurements from different sensing technologies are recorded with different stochastics. Appropriate weighting of the different observation types is therefore essential to guarantee the suitability of the estimation model.

Geodetic measurements in tunneling are usually performed with modern total stations with a distance measurement precision of 1 mm for prisms or 3 mm for bi-reflex targets and a standard deviation of 1' (= 0.3 mgon) for angle readings [12]. These specifications typically result in standard deviations between 1 and 5 mm for displacements in both coordinate directions depending on the target type as well as the measurement configuration.

The curvature values are represented by a combination of different measurement quantities, i.e., the DFOS strain measurement u1D716 , the distance between the fibers d and the orientation of the sensing segment u1D711 (cf. Eq. 2 and 9). Their standard deviation in both coordinate directions can be derived using variance propagation:

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

Fig. 2 Basic  determination  workflow  of  the  designed  DFOS  shape sensing approach

<!-- image -->

Flow chart

According to the manufactures of the used sensing units (see Sect. 2), the DFOS strain readings can be performed with a standard deviation between 2 and 10 μ m/m. The distance between the fibers is basically determined by the planning model, which, however, does not exactly represent the actual installation in most cases due to practical reasons on-site. To analyze typical variations between model and realization, the positions of the DFOS cables at one selected construction site were captured by reflectorless total station measurements before the respective shotcrete layer was applied (see Fig. 3a). From the interpolated cable routes along both installation layers, the DFOS cable spacing can be continuously derived in circumferential direction. The resulting profile (Fig. 3b) along the lining depicts deviations to the mean value of up to 10 cm. Although the mean value itself is basically in accordance with the planning model ( d model = 17 cm), these variations with a standard deviation of 4.1 cm must be considered as an essential part of the combined curvature's measurement uncertainty.

Analogous to the cable spacing, the initial geometry of the lining is also retrieved from the planning model. Laser scans may be carried out after the shotcrete lining is constructed to investigate the excavation accuracy (Fig. 3c). The orientation angles of the differential sensing segments in circumferential direction derived from the model and the laser scan of the observed cross-section are shown in Fig. 3d. This comparison delivers variations with a standard deviation of 3.41 ◦ , which should be also incorporated for thorough variance propagation.

The appropriate combination of all affecting measurement quantities enables a simulation of the achievable standard deviation of the resulting displacement profiles in both coordinate directions, see Fig. 4. The analysis was done using different measurement uncertainties for the geodetic displacement observations as well as different specifications for the DFOS strain readings according to Sect. 2. The results show that the standard deviation basically increases from the tunnel crown to the side walls. This seems logical, since the integration process is less well-controlled at the

Fig. 3 Stochastic analysis of constructed cross-section: a DFOS cables along inner and outer shotcrete layers from total station measurements; b derived  distance  between  installed  sensing  cable  layers in  circumferential  direction; c laser  scan  of  excavation  compared  to

<!-- image -->

Line chart

planning model and positions of geodetic targets ( T 1 - T 5 ); (d) orientation of single segments in circumferential direction derived from laser scan and planning model

<!-- image -->

Logo

123

Fig. 4 Standard deviation of resulting displacement profiles in lateral direction (solid) and height (dotted)

<!-- image -->

Line chart

outside due to the setup of supporting points (c.f. locations of total station targets in Fig. 3). While the geodetic readings have major influence, different DFOS instrument capabilities depict only a small effect on the precision of the resulting displacement profiles. This is why, strain profiles measured by Brillouin sensing units, typically with lower measurement precision, but significantly longer sensing range, may be also appropriate to determine capable displacement distributions. The standard deviation is similar for both coordinate directions with small deviations in the central area. It is obvious that particular orientations tend the curvature value to 0 (e.g., approx. 90 ◦ for u1D705 x ). The curvature uncertainties of these positions have significantly lower influence on the estimation, which, therefore, provides a better result in x-direction at the tunnel crown area.

## 4   Field applications and monitoring results

As part of the European TEN-T Network Corridor, the Semmering Base Tunnel (SBT) is one of the main railway infrastructure projects currently under construction in Europe. The original 150-year-old railway track crosses the mountain ridge with small curvature radii and large height gradients and, therefore, the train speed is low. The two tunnel tubes, with a total length of 27.3 km each, will be part of a highspeed rail connection, which will reduce the traveling time between Austria's capital Vienna and the second largest city Graz by about 30% in the future. The optimized track routing through the tunnel additionally enables significantly better capabilities for rail goods traffic.

As discussed in [6], the geological conditions along the tunnel track are challenging and most parts are being excavated by conventional tunneling based on the New Austrian Tunneling Method (NATM). This requires extended monitoring of the tunnel construction itself as well as of critical infrastructure nearby. DFOS monitoring systems were installed by IGMS at each construction lot (Fig. 5) to assess the structural integrity of individual construction parts and, finally, to increase the work safety on-site. These installations include monitoring of conventional tunnel cross-sections [19, 28] and shaft linings [13] (SBT 1.1), reinforced earth structures [20] (SBT 2.1) as well as pipelines [11] (SBT 3.1).

## 4.1   Conventional tunnel cross-sections

The outbreak in conventional tunneling based on the NATM is performed in different, well-defined sequences, which enables the rock to support itself. Both instrumented crosssections presented in this publication were constructed in two steps: first, the upper part of the tunnel (so-called top/ heading) was excavated and supported with two shotcrete layers. DFOS sensing cables were installed in different configurations along the supporting wire meshes of both layers using cable ties. Their routing was retrieved by reflectorless total station measurements before the shotcrete was applied, which guarantees an exact spatial allocation of the cables within the cross-section for data analysis (Fig. 6a). In practice, this may also be an appropriate solution for future installations performed by workers on-site without IGMS support, since these measurements can be carried out by the surveyor on-site. About 5 days later, the lower part (so-called bench/invert) was removed and the lining ring was closed. Wagner et al. (2020) give detailed information on the DFOS concept and installation inside the tunnel [28].

<!-- image -->

Engineering drawing

Fig. 5 Semmering Base Tunnel: project overview and IGMS monitoring sites (based on [6])

<!-- image -->

Logo

DFOS monitoring was started immediately after the installation and was continuously performed over several weeks, while the further tunnel excavation continued. The first instrumented cross-section was interrogated by a Rayleigh sensing unit, which can provide a spatial resolution of 3 cm over measurement ranges up to 2 km (cf. Sect. 2). Figure 6b shows the strain profiles along both DFOS cables about 5 days after the installation. Both layers basically depict negative strain due to the interacting rock pressure as well as shrinkage and creepage effects. Differences between the layers at the tunnel shoulders and the side walls indicate bending along the lining, which is confirmed by the derived curvature changes (Fig. 6c). The observed behavior seems logical, since the bench/invert section was excavated and supported about 5 days after the installation of the top/heading. The entire top/heading section therefore moves downwards before the support and the lining is bent due to the resistance of the bench/invert.

Distributed displacements along the cross-section can be determined by combining the DFOS curvature profiles with displacement readings of five geodetic targets using the algorithm presented in Sect. 3. The derived displacement profile in Fig. 6d shows good agreement to the pointwise geodetic observation, even if this behavior is partly implied by the correlation within the sensing algorithm. The correctness of the functional as well as the stochastical model is however additionally confirmed by the estimation's redundancy, which delivers an a-posteriori variance factor ̂ 𝜎 2 of about 1.06.

The DFOS displacement profile can be estimated for each geodetic measurement epoch (usually once a day) to analyze typical deviations between the different sensing techniques over time. Figure 7 depicts the coordinate residuals at the supporting point locations over the first 24 days of continuous monitoring. The first measurement of both sensing techniques exactly at the same time is only available about 12 h after the initial DFOS measurement, which is why the displayed curves are referenced to this second geodetic epoch after construction. The results present deviations of about ±3 mm in x-direction and ±4 mm in y-direction. These are

Fig. 6 Distributed displacement sensing along instrumented shotcrete tunnel cross-section: a installation  overview  captured  by  laser  scan; b measured  strain  profiles  along  inner  (green)  and  outer  (yellow) shotcrete  layer; c derived  curvature  values; d displacement  curves derived from DFOS profiles and pointwise geodetic measurements

<!-- image -->

Flow chart

<!-- image -->

Logo

123

Fig. 7 Coordinate residuals at supporting point locations over first 24 days of continuous monitoring

<!-- image -->

Line chart

in accordance with the 3u1D70E range of the theoretical analysis (cf. Fig. 4) and confirm the capabilities of the designed approach.

The continuous construction process in conventional tunneling requires fixed installation equipment (air ventilation system, electricity supply, etc.) and heavy tunnel machinery, which can restrict the field of view to geodetic targets. Consequently, some monitoring points of selected cross-sections may be partially unavailable for displacement measurements by total stations. The DFOS-based estimation can be performed using only a selected number of supporting points (min. 2) to overcome these limitations and to provide displacements along the entire top/heading section.

The estimated displacement profiles of different setups (utilized supporting points, respectively, marked in red) are shown in Fig. 8. Estimations with uniformly distributed supporting points (Fig. 8, top-left and top-right) depict a very good agreement with residuals smaller than 3 mm to the reference profile (dotted red line), which represent the estimation result with all supporting points (cf. Fig. 6d). Unilateral configurations with three geodetic points (Fig. 8, bottom-left) might be the most common limitation in tunneling. Even with this non-uniform supporting arrangement, the DFOS approach can deliver displacement profiles with maximum deviations of about

Fig. 8 Displacement profile estimation with different supporting point setups (used supporting points marked in color) (color figure online)

<!-- image -->

Engineering drawing

<!-- image -->

Logo

3.5 mm to the geodetic readings. This can be advantageous, especially if one side is blocked by tunnel infrastructure over longer periods.

Limitations of the DFOS-based estimation become visible if only two supporting points at one tunnel side are used (Fig. 8, bottom-right). Using this configuration, uncertainties of the curvature profiles might lead to a progressive error propagation starting from the supporting points, which finally result in large deviations at the opposite tunnel side.

Geodetic monitoring in conventional tunneling involves significant risks for the surveying team on-site. Since the instrument is often positioned in the middle of the tunnel axis to obtain an optimal measurement setup, surveyors must always be attentive not to be overlooked by workers driving heavy tunnel machinery. Tragically, disastrous working accidents cannot be ruled out completely [1]. For that reason, every monitoring system which may reduce the physical human presence inside the tunnel is a real benefit.

It is obvious that the DFOS approach also requires displacement readings to solve the boundary-value problem of the double integration. However, if geodetic readings are not available over longer periods of time, the displacements at the supporting point locations may be estimated from the recorded DFOS strain values. The approximated strain-displacement relation can be defined linearly by a minimum of two arbitrary measurement epochs i and j to predict the displacement value at kth epoch

<!-- formula-not-decoded -->

where u1D716 represents the mean strain at the geodetic target position. Using more than two measurement epochs might optimize the prediction, but requires more presence of the surveyor inside the tunnel.

For concept proofing, the displacements at the instrumented cross-section after 175 h were predicted from the readings about 12 and 36 h after the installation to support the DFOS-based estimation. The results in Fig. 9a demonstrate that the prediction method can provide displacement profiles with maximum deviations of about 5 mm to the exact solution. The prediction was subsequently performed for all DFOS epochs of the continuous monitoring campaign (Fig. 9b) to analyze the method's long-term suitability. The supporting points over the first 175 h are derived from the geodetic readings on the first and second day after construction (indicated with I in Fig. 9b). After this point in time, the bench/invert of the cross-section was already excavated, supported as well as refilled, which essentially changes the deformation behavior. For that reason, the prediction model is updated with two displacement observations for all following monitoring epochs, see II in Fig. 9b. The comparison between the DFOS-based estimations and the geodetic readings basically depict good agreement for all target positions with a mean deviation of about 1.2 mm in x-direction and 0.9 mm in y-direction over the entire monitoring period. The

Fig. 9 Displacement profile estimation based on supporting point prediction: a cross-sectional displacement profile; (b) displacement values at supporting point locations derived from DFOS curvature pro-

<!-- image -->

Line chart

files  over  35  days  of  continuous  monitoring  compared  to  pointwise geodetic measurements

<!-- image -->

Logo

123

maximum deviation of about 5 mm can be observed at the left-sided targets shortly before the update of the supporting points about 175 h after installation. The displacement profile of this epoch is already displayed in Fig. 9a, which, therefore, represents the estimation with the highest deviations to geodetic observations. Although this displacement accuracy might be insufficient for high-precise geotechnical monitoring applications, the resulting information certainly allows general conclusions on the deformation behavior with significantly lower presence of the surveyor inside the tunnel, in this example, 4 instead of 35 daily monitoring epochs. Moreover, distributed displacement profiles can also be determined for DFOS epochs without simultaneous geodetic measurements, which further extends the capabilities of the DFOS-based approach.

Even if the used Rayleigh sensing unit provides strain profiles with high spatial resolution, the sensing range is restricted with a maximum of 2 km. Especially in tunneling applications, sensing over longer distances can be advantageous to monitor numerous cross-sections using only one interrogation unit, which is placed at a protected place, preferably outside the tunnel. Brillouin sensing systems usually enable measurements over tens of kilometers, but are limited in the spatial resolution and the measurement precision. To evaluate potential effects on the crosssectional strain and subsequently derived displacement profiles, the DFOS system was installed within another cross-section at the same construction lot and continuous measurements were performed using a BOFDA sensing unit (see Sect. 2). Further information on the installation as well as strain and temperature monitoring results may be found in [3].

The derived displacement curve of one selected epoch about 82 h after the installation is shown in Fig. 10a. The estimation was supported by seven geodetic targets along the cross-section. Their displacements are in accordance with the shape derived from the BOFDA measurements, whose estimation redundancy delivers an a-posteriori variance factor ̂ 𝜎 2 of about 1.33. This also confirms the correctness of the statistical model at a significance level of 95%.

Analogous to Fig. 7, the DFOS displacement profiles can be estimated at each geodetic measurement epoch to analyze the typical variations between the different sensing approaches. The coordinate residuals at all seven geodetic target positions over the first 15 days of continuous monitoring are displayed in Fig. 10b. The different curves were referenced to the second geodetic epoch about 10 h after installation, where simultaneous results of both technologies are available for the first time. The derived deviations are within a range of about ±5 mm in both coordinate directions, except for the right-bottom target, and comparable to Rayleigh sensing results. The higher number of supporting points could, however, also be used for data snooping to detect and eliminate potential outliers in the curvature profiles or the supporting point displacements. This would potentially further optimize the estimation result.

Fig. 10 Displacement profile estimation from BOFDA measurements: a cross-sectional displacement profile; b coordinate residuals at supporting point locations over first 15 days of continuous monitoring

<!-- image -->

Engineering drawing

<!-- image -->

Logo

## 4.2   Tunnel shaft linings

Intermediate headings with shaft constructions are widely used in modern conventional tunneling to shorten construction times. The SBT project includes shafts at three construction lots with depths of up to 400 m [6]. As shown in Fig. 11a, the Göstritz intermediate access as part of the SBT 1.1 (Fig. 5) requires a complex construction system. Two horizontal access tunnels with a total length of more than 1 km each were built with a massive cavern at the end, which subsequently enabled the construction of two vertical shafts with a total depth of approximately 240 m to reach the planned altitude of the future railway line.

Exploration drillings revealed very challenging geological conditions for the shaft constructions, which is why an extended monitoring program was set up to detect any degradation of the structural stability of the linings. Conventional geodetic measurements of shaft walls using total stations are very difficult because of very steep, almost vertical sightings as well as water intrusion at the shaft floor. Furthermore, the shaft construction must always be completely paused during the time-consuming measurements, which, therefore, delay the construction process as a whole. After completion of the shaft construction itself and the installation of corresponding infrastructure, geodetic measurements additionally become almost impossible due to the limited field of view.

To  overcome  these  limitations,  DFOS  cables  were embedded into five selected shaft cross-sections based on the geological conditions to measure distributed strain and temperature profiles in circumferential direction of the shotcrete linings. An instrumentation along both shotcrete layers also enables an assessment of potential curvature changes. The cable routing was recorded by total station measurements before shotcreting to ensure the exact position along the lining. These measurements as well as the installation itself were challenging due to small working space inside the shaft as well as permanent water intrusion (Fig. 11b). The sensing cables of all cross-sections were guided from waterproof connection boxes at the cross-section locations to an instrument box at the shaft head, from where measurements can be carried out without any interference of the regular construction.

Contrary to partial excavations in conventional tunneling, the continuous construction of tunnel shaft linings enables an installation along the entire cross-section at the same time and can provide a closed ring system along both sensing layers. Based on this configuration, the boundary-value problem of the DFOS-based estimation can be solved by assuming that the displacement value and its gradient at the starting point must be equivalent to the last integration position by extending the functional model with constraints instead of pointwise displacement readings (cf. Eq. 10 to 14). These constraints can be realized in various ways, e.g., by pseudo-observations:

<!-- formula-not-decoded -->

The extension allows an estimation of relative displacement profiles along the shaft lining free of external observations. ⎣ ⎦ ⎣ ⎦

<!-- formula-not-decoded -->

<!-- image -->

Engineering drawing

Fig. 11 Tunnel shaft lining monitoring at Göstritz access point: a schematic representation of construction site (based on [7]) and DFOS monitoring setup; b vertical view down the shaft during sensor installation [13]

<!-- image -->

Logo

Although  rigid-body  motions  of  the  linings  remain unknown, this procedure can be very valuable to obtain the shaft's deformation behavior without any interruption of the shaft construction.

The initial measurement of the instrumented shaft linings was taken immediately after the installation using the BOFDA interrogator. Up to now, follow-up monitoring has been conducted epoch-wise on request of the geotechnical engineer on-site. Relative displacement profiles may be derived for each monitoring epoch based on the DFOS strain measurements, which are detailedly introduced in [13].

The evaluated profiles of two monitoring epochs along one selected cross-section (shaft 02, 228 m) are shown in Fig. 12a. These present only small displacements within a range of about ±13 mm for both epochs, but allow conclusions on the cross-sectional deformation behavior and its progress: the first measurement already displays a squeezed shape orientated to the right-bottom side with small magnitude, which has significantly further developed about 171 days after installation.

To verify the DFOS-based approach (blue), the deformation shape can also be approximated by an ellipse based on the geodetic displacements measured by total station (red). The individual profiles of both technologies must however be reduced by their respective mean value, since the DFOS approach depicts only relative deformation within the lining. The orientation of the geodetic ellipse represents the deformation process well, which confirms the above concluded assumption, although the estimation shows lower deformation magnitudes. Numerical deviations between the sensing techniques at the geodetic target positions are within a range of some millimeters (Fig. 12b) and, therefore, only slightly lower than the total deformation amount. The differences generally increase over time, which might be related to the increasing sighting steepness due to the further shaft sinking process. This usually results in higher measurement uncertainties for geodetic monitoring. The DFOS-based approach can therefore be a valuable substitute to capture the relative deformations profiles along shaft linings without physical access of the surveyor or delays of the construction process.

## 5   Conclusion

This paper introduced an innovative shape sensing and evaluation approach, which enables fully distributed shape assessment along curved structures, such as tunnel crosssections, based on distributed fiber optic sensing combined with geodetic displacement readings. The designed system was installed inside conventional tunnel cross-sections as well as shaft linings and interrogated by different DFOS sensing units based on Rayleigh and Brillouin scattering. The special setup of the used sensing cable in combination with appropriate installation techniques can enable successful installations with survival rates of more than 95%, even in the harsh tunnel environment.

The sensing concept is related to the double integration of distributed curvature values derived from DFOS strain measurements along two layers in well-known arrangement along the structure. Stochastic analysis could show that the curvature's measurement uncertainty is not only related to the DFOS strain measurements, but also to the distance between the fibers and the accuracy of the geotechnical planing model. The standard deviation of the estimated displacement profile also strongly depends on the geodetic measurement precision.

<!-- image -->

Line chart

Fig. 12 Shaft monitoring results (s02-228m): a cross-sectional displacement profiles estimated from fiber optic sensing (bright/blue) and displacement ellipse derived from geodetic measurements (dark/red); b coordinate residuals at geodetic target locations (color figure online)

<!-- image -->

Logo

Evaluations of continuous monitoring of tunnel crosssections demonstrate that the distributed displacement shape can be assessed without any gaps along the entire top/heading section. The results depict maximum deviations of about 4 mm to displacements measured by total stations at the geodetic target position, which confirms the stochastic analysis. Additionally, the deformation behavior might be also captured by laser scanning in future applications to independently verify the derived displacement shape. The DFOS-based approach is also capable to predict supporting information based on the measured strain values. It could be shown that the displacement profiles can be determined with mean deviations of about 1 mm in both coordinate directions at the supporting point locations by using only 4 instead of 35 geodetic measurement epochs. This significantly reduces the surveyor's physical presence inside the tunnel.

The closed ring system along tunnel shaft linings enables an estimation of relative displacement profiles, even without external observations. The resulting shape allows conclusions on the deformation behavior of the instrumented shaft cross-section, whose deformation progress and orientation could be verified by evaluations of an ellipse estimated from pointwise geodetic displacements. The deformation behavior along the instrumented crosssections is mostly homogeneous and the deformation's magnitude is small, especially at the tunnel shafts. Longterm monitoring of the installations is currently being performed to detect and quantify potential structural integrity anomalies. The outcomes will further prove the suitability of the designed shape sensing approach and will also give information on the long-term behavior of the DFOS tunnel installations.

Acknowledgements The authors thank the Austrian Federal Railways (ÖBB-INFRA), namely Johannes Fleckl-Ernst, Michaela HaberlerWeber, Frank Klais, Tobias Schachinger, Petra Wolf, as well as Gerhard Gobiet (SBT project leader) for the opportunity to realize various DFOS monitoring applications at the Semmering Base Tunnel project. We also would like to acknowledge all other project partners, especially the geotechnical surveying team ARGE GTM SBT1.1 (VSP Stolitzka &amp; Partner Ziviltechniker GmbH and DI Dr. Karl Strobl) and the Institute of Rock Mechanics and Tunnelling of Graz University of Technology (Michael Henzinger, Alexander Kluckner, Wulf Schubert, Lukas Wagner). Last, but not least, special thanks to the IGMS team members (Peter Bauer, Fabian Buchmayer, Dietmar Denkmaier, Slaven Kalenjuk, and Madeleine Winkler) for their valuable efforts during the sensor installations.

Funding Open  Access  funding  provided  by  Graz  University  of Technology.

## Compliance with ethical standards

Conflict of interest The authors declare that they have no conflict of interest.

Open Access This article is licensed under a Creative Commons Attribution 4.0 International License, which permits use, sharing, adaptation, distribution and reproduction in any medium or format, as long as you give appropriate credit to the original author(s) and the source, provide a link to the Creative Commons licence, and indicate if changes were made. The images or other third party material in this article are included in the article's Creative Commons licence, unless indicated otherwise in a credit line to the material. If material is not included in the article's Creative Commons licence and your intended use is not permitted by statutory regulation or exceeds the permitted use, you will need to obtain permission directly from the copyright holder. To view a copy of this licence, visit http://creat iveco mmons .org/licen ses/by/4.0/.

## References

1. [Austria Press Agency (APA): Unfall beim Bau des SemmeringBasistunnels (2020) https ://www.derst andar d.at/story /20001 17801 971/toedl icher -arbei tsunf all-beim-bau-des-semme ring-basis tunne ls. Accessed 14 Jul 2020](https://www.derstandard.at/story/2000117801971/toedlicher-arbeitsunfall-beim-bau-des-semmering-basistunnels)
2. Barla G (2009) Innovative tunneling construction method to cope with squeezing at the saint martin la porte access adit (lyon-turin base tunnel). In: Proceedings of ISRM Regional SymposiumEUROCK 2009 (keynote lecture).  International Society for Rock Mechanics and Rock Engineering,  pp 15-24
3. Buchmayer F, Monsberger CM. Lienhart W (2019) Benefits of strain and temperature monitoring of conventional tunnel cross sections using distributed fibre optic sensors. In: 4th joint international symposium on deformation monitoring (JISDM), p 7
4. De Battista N, Elshafie M, Soga K, Williamson M, Hazelden G, Hsu Y (2015) Strain monitoring using embedded distributed fibre optic sensors in a sprayed concrete tunnel lining during the excavation of cross-passages. In: 7th International conference on structural health monitoring of intelligent infrastructure (SHMII7). International Society for Structural Health Monitoring of Intelligent Infrastructure, p 10
5. fibrisTerre Systems GmbH: fTB 5020, Fiber-optic sensing system for distributed strain and temperature monitoring. Berlin, Germany (2020) https ://www.fibri sterr e.de/files /fibri sTerr e\_flyer .pdf. Accessed 9 Jun 2020
6. Gobiet G, Nipitsch G, Wagner OK (2017) The semmering base tunnel-special challenges in construction. Geomech Tunnel 10(3):291-297. https ://doi.org/10.1002/geot.20170 0008
7. Gobiet G, Wagner OK (2013) The new semmering base tunnel project. Geomech Tunnel 6(5):551-558. https ://doi.org/10.1002/ geot.20130 0041
8. Hartog A (2017) An introduction to distributed optical fibre sensors. CRC Press, Taylor &amp; Francis Group, UK. https ://doi. org/10.1201/97813 15119 014
9. Henzinger  MR,  Schachinger  T,  Lienhart  W,  Buchmayer  F, Weilinger W, Stefaner R, Haberler-Weber M, Haller EM, Steiner M, Schubert W (2018) Fibre-optic supported measurement methods for monitoring rock pressure. Geomech Tunnel 11(3):251263. https ://doi.org/10.1002/geot.20180 0015

<!-- image -->

Logo

123

10. Kechavarzi C, Soga K, de Battista N, Pelecanos L, Elshafie MZEB, Mair RJ (2016) Distributed fibre optic strain sensing for monitoring civil infrastructure. ICE Publishing, UK. https ://doi. org/10.1680/dfoss mci.60555
11. Klais F, Wolf P, Lienhart W (2017) The Grautschenhof contractconstruction of an intermediate access under complex local conditions. Geomech Tunnel 10(6):686-693. https ://doi.org/10.1002/ geot.20170 0052
12. Leica Geosystems (2015) AG: Leica TS15 User Manual. Version 6.0, Heerbrugg, Switzerland
13. Lienhart W, Buchmayer F, Klug F, Monsberger CM (2019) Distributed fiber optic sensing on a large tunnel construction site: increased safety, more efficient construction and basis for condition-based maintenance. In: International conference on smart infrastructure and construction 2019 (ICSIC), pp. 595-604. https ://doi.org/10.1680/icsic .64669 .595
14. Luna Technologies Inc.: OBR 4600 Optical Backscatter Reflectometer, Datasheet. Roanoke, VA, USA (2019) https ://lunai nc.com/wp-conte nt/uploa ds/2012/11/LUNA-Data-Sheet -OBR4600-V2.pdf. Accessed 4 Apr 2019
15. Mang H, Hofstetter G (2018) Festigkeitslehre. Springer Vieweg, Berlin. https ://doi.org/10.1007/978-3-662-57564 -2
16. Monsberger C, Lienhart W, Hayden M (2020) Distributed fiber optic sensing along driven ductile piles: design, sensor installation and monitoring benefits. J Civ Struct Health Monitor 10(4):627637. https ://doi.org/10.1007/s1334 9-020-00406 -3
17. Monsberger C, Woschitz H, Lienhart W, Račanský V, Hayden M (2017) Performance assessment of geotechnical structural elements using distributed fiber optic sensing. In: SPIE 10168, sensors and smart structures technologies for civil, mechanical, and aerospace systems. International Society for Optics and Photonics, pp 101680Z, 1-12
18. Monsberger CM, Lienhart W, Kluckner A, Schubert W (2019) Insitu assessment of distributed strain and curvature characteristics in shotcrete tunnel linings based on fiber optic strain sensing. In: ISRM 14th International Congress on Rock Mechanics. International Society for Rock Mechanics and Rock Engineering, p 8
19. Monsberger CM, Lienhart W, Moritz B (2018) In-situ assessment of strain behaviour inside tunnel linings using distributed fibre optic sensors. Geomech Tunnel 11(6):701-709. https ://doi. org/10.1002/geot.20180 0050

<!-- image -->

Logo

123

20. Moser F, Lienhart W, Woschitz H, Schuller H (2016) Longterm monitoring of reinforced earth structures using distributed fiber optic sensing. J Civ Struct Health Monitor 6(3):321-327. https :// doi.org/10.1007/s1334 9-016-0172-9
21. Pei  HF,  Yin  JH,  Jin  W  (2013)  Development  of  novel  optical fiber sensors for measuring tilts and displacements of geotechnical structures. Meas Sci Technol 24(9):10. https ://doi. org/10.1088/0957-0233/24/9/09520 2
22. Rabensteiner K (1996) Advanced tunnel surveying and monitoring. Felsbau 14(2):98-102
23. Rastogi VK (2008) Instrumentation and monitoring of underground structures and metro railway tunnels. In: 34th AITES-ITA world tunnel congress. International Tunnelling and Underground Space Association
24. Schubert W, Moritz B (eds) (2014) Handbook-geotechnical monitoring in conventional tunnelling. OeGG-Austrian Society for Geomechanics, Salzburg, Austria
25. Schubert W, Steindorfer A, Button EA (2002) Displacement monitoring in tunnels-an overview. Felsbau 20(2):7-15
26. Solifos AG: BRUsens DSS 7.2mm V3 grip 3\_50\_2\_002. Windisch, Switzerland (2019) http://solif os.nubos ys.com/filea dmin/ syncfiles/media /Solif os\_SE-01-03\_3-50-2-002\_en.pdf. Accessed 22 Jan 2020
27. Solifos AG: BRUsens DTS STL PA 3\_50\_1\_001. Windisch, Switzerland (2019) http://solif os.nubos ys.com/filea dmin/syncf iles/media /Solif os\_SE-01-01\_3-50-1-001\_en.pdf. Accessed 22 Jan 2020
28. Wagner L, Kluckner A, Monsberger CM, Wolf P, Prall K, Schubert W, Lienhart W (2020) Direct and distributed strain measurements inside a shotcrete lining: concept and realisation. Rock Mech Rock Eng 53:641-652. https ://doi.org/10.1007/s0060 3-01901923 -4
29. Woschitz H, Klug F, Lienhart W (2015) Design and calibration of a fiber-optic monitoring system for the determination of segment joint movements inside a hydro power dam. J Lightwave Technol 33(12):2652-2657. https ://doi.org/10.1109/JLT.2014.23701 02

Publisher's  Note Springer  Nature  remains  neutral  with  regard  to jurisdictional claims in published maps and institutional affiliations.
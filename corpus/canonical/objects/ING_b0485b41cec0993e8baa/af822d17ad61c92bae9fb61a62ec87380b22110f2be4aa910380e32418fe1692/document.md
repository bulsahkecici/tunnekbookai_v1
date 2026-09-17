## INFLUENCE OF THE TUNNEL SHAPE ON SHOTCRETE LINING STRESSES

Fabrizio Barpi 1 and Daniele Peila 2

Post print (i.e. final draft post-refereeing) version of an article published on Computer-Aided Civil and Infrastructure Engineering . Beyond the journal formatting, please note that there could be minor changes from this document to the final published version. The final published version is accessible from here: 10.1111/j.1467-8667.2011.00728.x This document has made accessible through PORTO, the Open Access Repository of Politecnico di Torino ( http://porto.polito.it ), in compliance with the Publisher's copyright policy as reported in the SHERPAROMEO website: http://www.sherpa.ac.uk/romeo/issn/1093-9687/

March 27, 2012

1 Assistant Professor; Department of Structural and Geotechnical Engineering , Politecnico di Torino, Corso Duca degli Abruzzi 24, 10129 Torino, Italy. Tel: +39 011 5644886, Fax: +39 011 5644899, e-mail: fabrizio.barpi@polito.it . Corresponding author.

2 Professor; Department of Land, Environment and Geo-Engineering , Politecnico di Torino, Corso Duca degli Abruzzi 24, 10129 Torino, Italy. Tel: +39 011 5647607, Fax: +39 011 5647699, e-mail: daniele.peila@polito.it

Abstract Tunnel excavation is frequently carried out in rock masses by the drill and blast method and the final shape of the tunnel boundary can be irregular due to overbreaks. In order to investigate the effects of overbreaks a study of the effect of tunnel boundary irregularity has been carried out. This is done developing a computational tool able to take into account fuzzy variables (i.e., thickness of the beams of the bedded spring approach used for the model). The obtained results show that irregularity effects should be considered when a shotcrete lining is used as the final tunnel lining (for the case where the tunneling procedure does not permit a smooth surface to be obtained). This is crucial to obtain a durable lining.

## 1 INTRODUCTION

Tunnel excavation in rock masses is frequently carried out by the drill and blast method. The final shape of the tunnel boundary can have an irregular surface due to overbreaks, that gives a final cross-section larger than the theoretical one due to irregular detachment of rock portions. Thomas (2009) has highlighted that 'variation in shape and thickness are not normally considered in design calculation' while Hoek &amp; Brown (1980); Stelzer &amp; Golser (2002); Son &amp; Cording (2007) and Borio &amp; Peila (2009) have highlighted that the irregular shape of a tunnel excavation boundary induces stress concentrations in the shotcrete lining, that could result in cracking and sometimes in local collapses. Stelzer &amp; Golser (2002) examined both with small scale models and with the back analysis using numerical models the effect of the variation of the profile of a shotcrete lining that are found in drill and blast tunnels and have highlighted that the imperfection could reduce the structural capacity of the lining of more than 50% and that the irregular lining tends to deform more than an homogeneous one (ICE (1996); Thomas (2009)). Since the use of shotcrete as the final lining is becoming more frequent in tunneling, and the presence of cracks can affect the durability and impermeability of the structure, with consequent relevant problems of refurbishments, the correct evaluation of the stresses acting in shotcrete linings taking into accounts its real shape is of primary importance.

Even though the consequences of this irregularity are well known, as discussed by the previously presented authors, tunnel linings are usually designed under the assumption of a smooth tunnel surface and therefore considering a lining with constant thickness. This assumption can underestimate the real stresses in the lining.

In order to investigate these situation with indications for the designers of these special cases, and to provide a simple procedure and design tool, a study on the effect of tunnel boundary irregularity, based on a fuzzy model, has been carried out using a simple, but well known and widely used, design method such as the bedded-beam spring model. The advantage of the proposed methodology is that it prevents to simulate the irregularities with complex mesh as requested by numerical models (usually Finite Element Method or Finite Difference Method) that is numerically complex and difficult, furthermore it permits to better take into account the natural irregularities due to rock mass fabric.

The design of the tunnel lining (both the first and the final phase) requires the designer to use computational tools that are able to evaluate the underground and surface displacements, and the plasticized zones around the void, but also the forecast stresses acting inside the lining, to produce a structural design (thickness, type and properties of the materials, concrete reinforcement such as steel bars, steel or plastic fibers). The British Tunnelling Society (BTS (2004)) clearly states that the most important goal of a tunnel design is to provide the designer with an understanding of the mechanism of behaviour during tunnelling, including the possibility of risks and where they could occur, and a basis for producing a robust and safe design and, finally, a basis for interpreting the monitoring results. Because of the uncertainties concerning the properties of the ground and the induced loads on the lining, it is important to highlight that there is not a single analysis method that can be used for all tunnels, and very often the precision of the available analytical and numerical tools is much greater than the reliability and the accuracy of the data obtained from site investigations and rock mass characterization. Therefore, designers are obliged to undertake sensitivity analysis of the ground-support interaction model in order to understand the influence of the input parameters.

The most frequently used lining design methods in tunneling practice are (AFTES (1976); USACE (1997); BTS (2004)):

- empirical methods, which are usually developed by using different rock mass classification methods;

- analytical solutions, which are usually developed using:

-

continuum analytical models (Muir Wood (1975)),

-

-

-

the convergence-confinement method (Hoek &amp; Brown (1980); Brown et al. (1983); Panet (1995)),

limit equilibrium methods, which are used to evaluate the stability of rock blocks around a tunnel boundary and the stability of the tunnel face in soils (Hoek &amp; Brown (1980); Goodman &amp; Shi (1985)),

bedded-beam-spring models (USACE (1997); Oreste (2007)) where the tunnel lining is modelled as a series of beams connected to each other and to the ground, by radial and tangential springs that simulate the ground support interaction,

- two and three-dimensional numerical analyses, which can be carried out using the finite element or the finite difference method with the ability to model complex geometrical, geological and geotechnical structures.

The bedded-beam-spring model (also known as the hyperstatic reaction method) presents some disadvantages, such as the difficulties involved in the correct evaluation of the spring stiffness and load to be applied to the lining, which has to be evaluated independently from the deformation of the system using, e.g., dead load approaches or rock mass classifications. Despite these drawbacks, this approach is widely applied in design practice thanks to its ease of use, and the possibility of obtaining a quick and simple evaluation of the actions inside the structural elements by varying the acting loads, and thus carrying out sensitivity analyses, in a simple and effective way.

Tunnel designers should always take into account that any calculation could be affected by many errors in modelling that could lead to poor predictions (Kalamaras (1996); Stelzer &amp; Golser (2002); BTS (2004); Peila (2009)) such as the theoretical geometry of the problem, which can be different from the reality induced by the construction method. For this reason, the present research analyses the tunnel boundary geometry after excavation and its influence on a ground-lining system and on the stresses inside the lining. The study of the soil-tunnel interaction is performed by introducing a predetermined degree of variation ( fuzziness ) into the geometrical parameters of the model. Given a certain degree of uncertainty in the parameters, the fuzzy set theory (Zadeh (1968) and Zadeh (1988)) makes it possible to evaluate the uncertainty in the results, thereby avoiding the difficulties associated with stochastic analysis, since this method does not require any knowledge of the probability distribution functions. Here it is assumed that model parameters are affected by a certain degree of uncertainty (defined by the so-called membership functions ) and the computational results are calculated by solving the fuzzy equations, thus quantitatively estimating the influence of a given change in the model parameters.

## 2 REASONS FOR OVERBREAKS

The level of overbreak as a result of irregularity of a tunnel wall and roof, excavated by the drill and blast method, depends on (Mancini et al. (1993); Ibarra et al. (1996); Schmitz (2003); Mancini &amp; Pelizza (1977); Singh &amp; Xavier (2005); Wahlstrom (1973)):

- the geological conditions of the rock mass (i.e., strength, joint pattern orientation and spacing);
- the quality of drilling of the blasting hole pattern (particularly at the periphery of the tunnel);

- the adequacy of the used blasting scheme, the distance between the peripheral charges and round length, the distance between the installation position of the lining and the tunnel face;
- the scaling activity;
- the workmanship ability (that depends on the ability of the drilling shift to carry out a correct drilling pattern thus to minimizing the risk that some incorrectly directed peripheral bore-hole could create the over profiling).

Furthermore, since the final support has a pre-defined thickness, and because removing an underbreak is more expensive than filling it, contractors usually tend to allow a large safety margin in the blasting design, thus considering larger overbreaks than those actually encountered. Concerning the thickness of overbreaks, Schmitz (2003) gave the following ranges: 0.05 ÷ 0.10 m of overbreak in a compact stable rock mass with few joints or a fractured rock mass with small joint spacing; 0.15 ÷ 0.30 m in fractured, unstable rock masses prone to caving and 0.5 m in a compact stable rock mass with large joint spacing.

The influence of the geological factors on overbreaks is mainly linked to the joint pattern and its geometry: the key blocks, after the excavation, trying to find a new free surface and they detach towards the new void, leading to the detachment of new rock elements (Goodman &amp; Shi (1985)). This effect is less important when the main joints are orientated almost orthogonal to the tunnel axis, opposite to the case when the joints are parallel to the tunnel advancement direction. The worst condition could happen when sub-horizontal joints or rock bedding planes and sub-vertical joints are present. Figure 1 (a) shows the effect of inclined joints patterns with reference to the tunnel axis with risk of instability of rock slabs on the left side and the detachments of blocks sliding on the joints. Figure 1 (b) shows the gravitational detachments of blocks from the roof and the buckling of rock slabs on the tunnel side. All these detachments produces overbreaks in the final tunnel cross section. Figure 1 (c) shows the wedge generated by rock joints on the roof and Figure 1 (d) shows an example of rock detachments from the tunnel face in real cases.

Key block design analysis can be used to evaluate the geometry of these detachments, taking into account the local joint patterns and the length of the blast round (Figures 2, 3, and 4).

The drilling accuracy, the type and quantity of the charge in the holes and the blast round pattern are the key-factors controlling the size of overbreaks. The larger the blast round and the specific charge (quantity of explosives/blasted volume), the greater the probability of inducing a detachment and, consequently, pathological overbreaks. It is worth noting that the design of the peripheral charges is of great importance for a reduction in the overbreaks (Mancini &amp; Cardu (2001); Wyllie &amp; Mah (2004)).

The above discussion clearly shows how the final shape of the tunnel boundary is inevitably irregular in a real tunnel and therefore, when a shotcrete lining is used as the only lining, the real shape of the tunnel periphery should be considered.

Referring the example of Figure 5 where many cracks in the shotcrete lining (that is the final lining of a water conveyance tunnel) where induced by the presence of large irregularities of the tunnel boundary due both to the rock mass structure and to the excavation of niches necessary to install the electrical and pumping devices used during the construction. In this example the need of this refurbishment was discovered few months after the construction and after the preliminary water circulation tests performed to examine the power plant machinery behaviour. Rock bolts were necessary to refurbish the shotcrete lining, that was originally reinforced with wire mesh only. This intervention is not technically complex but, since the damaged zones where distributed along the 14 km long tunnel, it was necessary to set up a special moving job site (with some problem of electricity and water suppling). For carrying out this refurbishment the power plant was stopped for about one month with very high induced costs due to the loss of electrical production. The present example clearly highlight that in some special cases the problem of tunnel irregularity cannot be disregarded and therefore the proposed methodology can be of interest for technical engineers.

## 3 A SHORT INTRODUCTION ON FUZZY LOGIC

Fuzzy logic was introduced in an attempt to formalize approximate knowledge and approximate reasoning (see, for instance, Zadeh (1968) and Zadeh (1988)). It is a superset of conventional Boolean logic extended to handle the concept of partial truth (i.e., truth values between 'completely true' and 'completely false'). Fuzzy logic recognizes more than true and false values: propositions can be represented with degrees of truthfulness and falsehood. This logic can be employed to cope with complex systems, that are controlled by human experts, systems that use human observations as input and systems that are naturally vague (behavioral or social sciences).

Some applications of fuzzy logic can be found, in hydrology by Schulz &amp; Huwe (1997), in structural optimization and rehabilitation by Sarma &amp; Adeli (2000 a ), Sarma &amp; Adeli (2000 b ), Sarma &amp; Adeli (2002) and Tagherouit et al. (2011), in structural system identification by Samant &amp; Adeli (2001), Adeli &amp; Jiang (2006) and Bianchini &amp; Bandini (2010) and for risk assessment by Sadeghi et al. (2010).

It is important to point out that precision is expensive and that it should be applied only to the extent necessary in a given problem. The fuzzy theory, designed to work with imprecise data, can handle problems of this kind, where only approximate knowledge is available.

It must be noticed that there are many similarities between fuzzy theory and probability theory; for example, both of them express uncertainty and have their values in the [0 , 1] range. From a mathematical point of view, fuzzy values are commonly misunderstood to be probabilities, or fuzzy logic is interpreted as some new way of handling probabilities. This is not true: a minimum requirement of probabilities is additivity , that is that they must add together to one, or the integral of their density curves must be one, that does not hold in general with membership grades. Semantically, the distinction between fuzzy logic and probability theory is related to the difference between the notions of probability and a degree of membership. Probability statements are about the likelihoods of outcomes: an event either occurs or does not. With fuzziness, it is not possible to say unequivocally whether an event occurred or not, but it is possible to model the extent to which an event occurred.

## 4 THE COMPUTATIONAL MODEL

## 4.1 Introduction

A computational model has been developed in order to couple the bedded-spring model with a fuzzy set analysis tool, i.e., to take into account the imprecision in the data as outline below. This model is able to take into account a generic number of imprecise parameters and to solve the correspondent fuzzy equations. It is a general model that is not restricted to make imprecise the thickness of the beams only (as described below) but it is able to deal with the imprecision of any model parameter. It performs the proper calculations (solution of the fuzzy equations) and output the membership function of the chosen parameters.

## 4.2 The bedded-beam spring model

The bedded-beam spring model describes the tunnel lining as a series of beams connected at their nodes to a series of radial and tangential springs that are designed to model the ground reactions (Figure 6).

The loads acting on the lining are evaluated by an empirical formulation taking into account the material properties of the rock mass (usually through rock mass classifications) and the discontinuity directions. The structural elements (i.e., beams) are usually modelled with a linear elastic analysis; their stiffness is based on the thickness and elastic modulus of the constituting material. The stiffnesses K n and K t of the springs (Figure 7) are usually evaluated from the rock mass data using very simple relationships as proposed in the literature that are derived from Winkler theory (DAUB (2005); AFTES (1976); USACE (1997)). Oreste (2007) has recently proposed a more refined formulation with a hyperbolic constitutive relationship but, for the present work, it was preferred to use a simpler formulation due to the difficulty of determining these parameters from the in-situ investigation and, therefore, affected by the related uncertainties.

This approach even if very simple is still widely used in tunnelling design also because it permits a quick and speed parametric calculation and, for example, is suggested by DAUB (2005) for the design of the shield in a mechanized tunnel.

## 4.3 Application of fuzzy set analysis to soil-tunnel interaction

The influence of the uncertainty or imprecision that affects some parameters of a beddedbeam spring model is therefore assessed through a fuzzy approach : thickness t of a number of beams of the lining is considered to be fuzzy, i.e., associated with a certain degree of uncertainty, as defined through the appropriate membership functions µ . Such functions represent the level of confidence (or imprecision) of a variable; a typical shape can be triangular (as in the present research), trapezoidal, Gaussian or bell-shaped.

Compared to stochastic analysis, this approach is a simpler and more intuitive way to allow for the uncertainty in some parameters, since it does not call for the determination of probability distribution functions.

As shown above, the determination of the membership functions plays an essential role. This aspect is very important for practical applications: some of the common methods used to build membership functions are listed below:

- subjective evaluation and elicitation or expert statements given by an expert on the subject,
- converted probabilities obtained from histograms or other probability diagrams,
- physical measures (often difficult),
- learning and adaptation.

Given a value of the membership function, it is possible to obtain a closed interval within which the variable of interest lies. The projections of the α -cut (i.e., the cut through the membership function at height α ) on the axis of the variable define the left and right boundaries of this interval. For instance, the α -cut=0.5 in Figure 10 defines interval 0.204 m to 0.256 m for t (beam group number 1). As a result, the variables of interest (output of the model), for instance, displacements u ( θ ), v ( θ ), ϕ ( θ ) and internal forces N ( θ ), M ( θ ) and T ( θ ) are now expressed by fuzzy numbers ( θ is represented in Figure 6). The same applies to any other output of the model, i.e., stresses in the boundary elements or in the structural elements. This means that all the output of the model are associated with a certain membership function which can be determined by finding their minimum and maximum value for each t of the n fuzzy beam group belonging to the given interval which correspond to a certain (given) value of the α -level.

The solution is found by minimizing and maximizing the fuzzy variables and calculating any parameters of interest for each level of α . The range of variation of the fuzzy variables represents their level of imprecision, due to the imprecision in the input data. The determination of the membership functions of displacements, i.e., their level of imprecision, is achieved by repeating the calculation for different α 's. This problem can be viewed as an optimization problem , as explained in Dubois &amp; Prade (1980).

Compared to a sensitivity analysis, the method presented here makes it possible to take into account an entire set of imprecise parameters and to determine the level of imprecision in the results. A different level of imprecision in the data is obtained by a change in the membership functions.

## 5 CALCULATION EXAMPLE

## 5.1 Tunnel description

In order to explain the proposed methodology, a calculation based on the data measured a road tunnel excavated by drill and blast in flysch in the North of Italy, has been developed. The rock mass is a chaotic mixing of argillite, sandstone and siltstone. The argillite and the siltstone are in thin layers (from 30 mm to 250 mm thick) very fractured and sometimes twisted while the sandstone layers are well stratified with a thickness of the strata ranging between 50 mm to 300 mm. No water was observed in the tunnel. The used blast round is a standard one with a 'V open' cut. The maximum depth of the tunnel is at about 300 m. This tunnel was used as an example even if the final lining is a casted in place concrete lining since the data of the overbreaks were available and therefore this is a good example for the application of the proposed design procedure. The geometry of the tunnel used in the model is summarized in Figure 8 while Table 1 summarizes the mechanical parameters of the model. The chosen calculation geometry is based on the interpolation of the real data measured with a topographical systematic measurement in the tunnel and shown in Figure 9 (the measured overbreak area for each section in this example ranges between 4% to 11% if the design cross section). The designer, in this specific case, should take into account that due to the irregular joint distribution the shotcrete lining can be irregular and this situation can be easily taken into account with the proposed methodology. The applied loads used in this simulation were evaluated using the Terzaghi formulation of the computation of the vertical dead load with a drained cohesion of 0.13 MPa and a drained friction angle of 23 ◦ . The obtained loads are q v =0.37 MPa and q h =0.5 × q v =0.185 MPa. The thickness of the lining has been determined by a homogeneizing procedure (Oreste (2007), Hoek et al. (2008)) of a conventional tunnel lining made of shotcrete (0.22 m thick) and steel ribs (two IPN180 ribs placed side by side with a distance of 1 m).

The stiffnesses K n and K t of the bedded-spring elements (Figure 6) were chosen to be equal to K n = 8 × 10 9 Pa/m and K t = 2 . 6 × 10 9 Pa/m using the calculation scheme proposed by USACE (1997). To avoid introducing any further uncertainties, the springs were designed to remain in the elastic range by raising the plasticization level.

## 5.2 Calculation with fuzzy thickness

The parameters of interests, which are considered to be imprecise, are the thicknesses t of eight groups of beams used to model the lining (Figure 8); the output parameters used to evaluate the response of the model are the displacements u , v and ϕ of node 35 (near the top of the crown, x =0.4297 m, y =5.7339 m) and the normal force, bending moment and shear for element 15 (at the base of the crown). The number of the beam groups, equal to eight, has been chosen on the basis of the real detachment monitored in the real case presented in Figure 9. The chosen point is 35 and the related element 15 are not most stressed but are chosen with reference to their relevant position in the geometry of the tunnel (close to the top of the heading) and used as an example to show the effect of the imprecision. Since all the results are presented, it is possible for the designers to accurately design the lining, taking into account the most critical conditions.

## 6 DISCUSSION OF THE RESULTS

As mentioned above, parameters t of eight groups of beams are considered to be fuzzy and, hence, associated with given membership functions, with a triangular symmetrical shape with respect to the reference values . These fuzzy distributions are presented in Figure 10.

The results of the model, in terms of displacements u and v of node number 35, are shown in Figures 11, 12, while the results, in terms of internal forces N , M and T of element 15, are shown in Figures 13, 14 and 15.

Each diagram shows the value obtained for different α -cuts and makes it possible to investigate the effects of parameter imprecision and to identify the parameters with the most adverse influence on the response. It is important to highlight that α -cut=1 means a constant thickness of the lining.

For instance, in Figure 12 for α -cut=0 (that allows to maximize the imprecision), the v displacement range is - 1 . 05 × 10 - 2 m to - 9 . 25 × 10 - 3 m, i.e., a range - 6 . 0% to +7 . 4% with respect to the reference value - 9 . 85 × 10 - 3 m. This range corresponds to a maximum range - 22 . 5% to +22 . 5% (beam group number 1, Figure 10) for the fuzzy input data related to the same value of α -cut=0. It should be noted that, despite the linear membership functions in Figure 10, the resulting membership function is non linear.

Furthermore, it can be noticed that the imprecision in the data results in a much larger imprecision in the value of the displacement u than in v , as shown in Figures 11 and 12. It can also be noticed that for the largest imprecision of thickness t of the lining (that correspond to α -cut=0) and that spans from -22.5% to +22.5%, we obtain the following imprecision of the results:

- horizontal displacement u of node 35: -414.8% ÷ +419.0%;
- vertical displacement v of node 35: -6.0% ÷ +7.4%;
- normal force N of beam 15: -6.2% ÷ +4.3%;
- bending moment M of beam 15: -71.7% ÷ +82.1%;
- shear force T of beam 15: -23.6% ÷ +32.2%.

If taking as a reference element 23, that is the element with the maximum bending moment, the following imprecision is obtained: normal force N -8.5% ÷ +4.9%, bending moment M -78.1% ÷ +52.0%, shear force T -69.8% ÷ +24.7%.

It is clear that, for a given element, the imprecision on the thickness of some elements along the tunnel is reflected in a large imprecision for horizontal displacement u and bending moment M of the chosen beam. Figures 16, 17 and 18 show the normal force, bending moment and shear force, as function of θ for α =0 and α =1; both show the influence of imprecision in the data on the internal forces in the lining. For a different choice of displacements or choice of the beam to evaluate the results, the imprecision can differ. The same applies in a different number or position of the fuzzy beams are considered.

The presented results show the importance of a proper evaluation of the imprecision in the model parameters and of quantitatively evaluating how this imprecision is reflected on the results. It is clear that the presented analysis is an essential tool that can be included in the design of linings in order to avoid the underestimation of the real effects of the ground irregularity on the lining itself, particularly when the long-term life of a shotcrete lining has to be considered, so that the development of cracks that can negatively affect the durability of the lining is avoided. The study of the influence of thickness irregularity by Son &amp; Cording (2007) shows similar order of magnitude in the results.

Finally, the interaction diagrams for shotcrete and steel are shown in Figures 19, 20, 21 and 22 according to the procedure outlined in Hoek et al. (2008) and Carranza-Torres &amp; Diederichs (2009) (the material properties are listed in Table 1). The diagrams for steel present two domains: the larger is based on the Galileo criterion while the smaller is based on the Tresca criterion. By using a safety factor equal 1.5, some points for shotcrete fall outside the diagrams, which means a bending failure (Figure 19). This results clearly shows that if the average thickness would have been considered, a wrong design could have been obtained since the designed lining would have been too small and cracks and damages could have been occurred.

It is clear the contribution of the proposed methodology: the effect of the imprecision make it possible to find the most adverse combination of parameter that, in some cases, could give a wrong design.

## 7 CONCLUSIONS

The present research deals with importance of thickness irregularities of the shotcrete lining on the stresses acting within the lining and how it can critically affect the final stability of the whole structure. It is useful to point out that designers normally think that a large thickness of the lining (even irregular) due to overbreaks are on the safety side. This can be a mistake since, as shown in the paper, a large thickness can mean large stresses in the lining that can crack the lining itself thus reducing its durability.

Since overbreaks are unavoidable when the drill and blast method is used, the shape of the lining is not regular, as is usually considered in conventional design procedures. The fuzzy approach , applied to a widely used computational bedded-beam spring model, makes it possible to take into account a degree of imprecision in the model parameters and to evaluate it quantitatively . A numerical parametric fuzzy analysis has shown that when the irregularity of the rock boundary increases, there is also an increase in the acting compression stresses, while the stresses reduce at the intrados till traction appears, and this traction can be critical for the occurrence of cracks in the lining.

The results of the analysis show that irregularity effects cannot be disregarded when a shotcrete lining is going to be applied as the final tunnel lining when the tunneling procedure does not permit a smooth surface to be obtained, particularly if a durable lining has to be created.

It is worth noting that more refined approach for the shotcrete lining modelling can be considered in order to take into account phenomena like creep, shrinkage and hydration beaviour, see for instance, Barpi &amp; Valente (2003), Hellmich &amp; Mang (2005) and Scheiner &amp; Hellmich (2009). It is not the purpose of the present research to investigate such aspects but he proposed methodology could have been applied to a more complex constitutive model. The authors are aware of the simplification introduced modelling the behavior of the shotcrete but they are assumptions commonly used in tunnelling design (see, for instance, Hoek et al. (2008)). The loads applied to the structure by the rock mass were treated in a deterministic way, as usually done in practice, but a parametric analysis can be easily done if the rock shows irregular or variable mechanical properties. The proposed calculation approach has been conceived to be quick and simple to be applied for parametric studies.

## References

- Adeli, H. &amp; Jiang, X. (2006), 'Dynamic fuzzy wavelet neural network model for structural system identification', Journal of Structural Engineering (ASCE) 132 (1), 102-111.
- AFTES (1976), Association Fran¸ caise des Tunnels et de l'Espace Souterrain , Consideration on the usual method of tunnel lining design. Tunnels &amp; Ouvrages Souterrains, 14, mars/avril.
- Barpi, F. &amp; Valente, S. (2003), 'Creep and fracture in concrete: A fractional order rate approach', Engineering Fracture Mechanics 70 (5), 611-623. Elsevier Science Ltd. (Great Britain).
- Bianchini, A. &amp; Bandini, P. (2010), 'Prediction of pavement performance through neurofuzzy reasoning', Computer-Aided Civil and Infrastructure Engineering 25 (1), 39-54. Wiley-Blackwell.
- Borio, L. &amp; Peila, D. (2009), 'How tunnel boundary irregularities can influence the stresses in a shotcrete lining', Geoingegneria Ambientale e Mineraria XLVI(2) , 45-52.
- Brown, E., Bray, J., Ladanyi, B. &amp; Hoek, E. (1983), 'Ground response curve for rock tunnels', Journal of Geotechnical Engineering (109), 15-39. ASCE.
- BTS (2004), British Tunnelling Society , Tunnel Lining Design Guide. Thomas Telford (London).
- Carranza-Torres, C. &amp; Diederichs, M. (2009), 'Mechanical analysis of circular liners with particular reference to composite supports. For example, liners consisting of shotcrete and steel sets', (24), 506-532. Elsevier Science Ltd. (Great Britain).
- CETU (1998), Centre d'Etudes des Tunnels , Dossier Pilote des Tunnels: g´ eologiehydrog´ eologie-g´ eotecnique. Bron (France).
- DAUB (2005), 'Recommendation for static analysis of shield tunnelling machines', Tunnel (7), 44-58. German Commitee for Underground Construction.
- Dubois, D. &amp; Prade, H. (1980), Fuzzy Sets and Systems: Theory and Application , Academic Press, San Diego.
- Goodman, R. &amp; Shi, G. (1985), Block Theory and its Application to Rock Engineering , Prentice-Hall, New York.
- Hellmich, C. &amp; Mang, H. (2005), 'Shotcrete elasticity revisited in the framework of continuum micromechanics: From submicron to meter level', Journal of Materials in Civil Engineering 17 (3), 246-256.
- Hoek, E. &amp; Brown, T. (1980), Underground Excavation in Rock , The Institution of Mining and Metallurgy, London.
- Hoek, E., Carranza-Torres, C., Diederichs, M. &amp; Corkum, B. (2008), 'The 2008 Kersten Lecture. Integration of geothecnical and structural design in tunnelling', pp. 1-53. 56 th Annual Geotechnical Engineering Conference, Minneapolis (USA).
- Ibarra, J., Maerz, N. &amp; Franklin, J. (1996), 'Overbreak and underbreak in underground openings. Part 2. Causes and implications', Geotechnical and Geological Engineering 14(4) , 325-340. Springer.

- ICE (1996), Institution of Civil Engineers , Sprayed concrete lining (NATM) for tunnels in soft ground. Thomas Telford (London).
- Kalamaras, G. (1996), A probabilistic approach to rock engineering design: application to tunnelling , Milestones in Rock Engineering: Bieniawski Jubilee Collection, Balkema, Rotterdam, pp. 113-135.
- Lunardi, P. (1979), 'Applications de la m´ ecanique des roches aux tunnels autoroutiers. Example de Tunnel de Frejus (cˆ ote Italia) e du Gran Sasso', Revue Fran¸ caise de G´ eotechnique (12).
- Mancini, R. &amp; Cardu, M. (2001), Scavi in Roccia. Gli Esplosivi , Hevelius Edizioni, Benevento (Italy).
- Mancini, R., Cardu, M., Fornaro, M. &amp; Innaurato, N. (1993), Consideration on the profile accuracy attainable in tunnel excavation by drilling and blasting, in 'Proceedings of the conference Option for Tunnelling', Vol. 1, Amsterdam, pp. 741-748.
- Mancini, R. &amp; Pelizza, S. (1977), 'Previsione dei consumi di esplosivo e di lavoro di perforazione nello scavo di gallerie', Lavori con Esplosivo pp. 91-102. Italesplosivi, Bergamo (Italy).
- Muir Wood, A. (1975), 'The circular tunnel in elastic ground', Geotechnique (25(1)), 115127. Thomas Telford (London).
- Oreste, P. (2007), 'A numerical approach to the hyperstatic reaction method for the dimensioning of tunnel supports', Tunnelling and Underground Space Technology 22(2) , 185205. Elsevier Science Ltd. (Great Britain).
- Panet, M. (1995), Le Calcul des Tunnels par la M´ ethode Convergence-Confinement , Presses de l' ´ Ecole Nationale des Ponts et Chauss´ ees, Paris (France).
- Peila, D. (2009), 'Indagini preliminari nella costruzione di gallerie: analisi della letteratura tecnica', Geoingegneria Ambientale e Mineraria XLVI(3) , 37-59.
- Sadeghi, N., Fayek, A. &amp; Pedrycz, W. (2010), 'Fuzzy Monte Carlo simulation and risk assessment in construction', Computer-Aided Civil and Infrastructure Engineering 25 (4), 238-252. Wiley-Blackwell.
- Samant, A. &amp; Adeli, H. (2001), 'Enhancing neural network incident detection algorithms using wavelets', Computer-Aided Civil and Infrastructure Engineering 16 (4), 239-245. Wiley-Blackwell.
- Sarma, K. &amp; Adeli, H. (2000 a ), 'Fuzzy discrete multicriteria cost optimization of steel structures', Journal of Structural Engineering (ASCE) 126 (11), 1339-1347.
- Sarma, K. &amp; Adeli, H. (2000 b ), 'Fuzzy genetic algorithm for optimization of steel structure', Journal of Structural Engineering (ASCE) 126 (5), 596-604.
- Sarma, K. &amp; Adeli, H. (2002), 'Life-cycle cost optimization of steel structures', International Journal of Numerical Methods in Engineering 55 (12), 1451-1462.
- Scheiner, S. &amp; Hellmich, C. (2009), 'Continuum microviscoelasticity model for aging basic creep of early-age concrete', Journal of Engineering Mechanics (ASCE) 135 (4), 307323.
- Schmitz, R. (2003), 'Line infrastructure and the role of engineering geology in analysing overbreak', Ingeokring Newsletter 10(2) , 31-41.

- Schulz, K. &amp; Huwe, B. (1997), 'Water flow modeling in the unsaturated zone with imprecise parameters using a fuzzy approach', Journal of Hydrology 201 , 211-229.
- Singh, P. &amp; Xavier, P. (2005), 'Causes, impact and control of overbreak in underground excavations', Tunnelling and Underground Space Technology 20(1) , 63-71. Elsevier Science Ltd. (Great Britain).
- Son, M. &amp; Cording, E. (2007), 'Ground-lining interaction in rock tunnelling', Tunnelling and Underground Space Technology 22 , 1-9. Elsevier Science Ltd. (Great Britain).
- Stelzer, G. &amp; Golser, J. (2002), Untersuchung zu geometrischen imperfektionen von spritzbetonschalen - Ergebnisse aus modellversuchen und numerischen betrechnungen, in W. Kusterle, ed., 'Proceedings of the Spritzbeton-Technologie 2002 Conference, Alpbach, January 31-February 2, 2002'.
- Tagherouit, W., Bengassem, J. &amp; Bennis, S. (2011), 'A fuzzy expert system for prioritizing rehabilitation sewer networks', Computer-Aided Civil and Infrastructure Engineering 26 (2), 146-152. Wiley-Blackwell.
- Thomas, A. (2009), Sprayed Concrete Lined Tunnels: An Introduction , Taylor and Francis, New York.
- USACE (1997), US Army Corps of Engineering , Tunnels and shafts in rock. Engineering Manual 1110-2-2901, Washington (USA).
- Wahlstrom, E. (1973), Tunnelling in Rock , Development of Geotechnical Engineering 3, Elsevier (The Netherland).
- Wyllie, D. &amp; Mah, C. (2004), Rock Slope Engineering , Spoon Press, New York.
- Zadeh, L. (1968), 'Fuzzy algorithms', Information and Control 12 , 94-102.
- Zadeh, L. (1988), 'Fuzzy logic', Institute of Electrical and Electronic Engineers Computer 1 (14), 83-93.

Table 1. Material properties for shotcrete (0.22 m thick) and steel (two IPN180 ribs placed side by side).

| Material   |   Elastic modulus GPa |   Poisson ratio - |   Tensile strength MPa |   Compressive strength MPa |
|------------|-----------------------|-------------------|------------------------|----------------------------|
| Shotcrete  |                    10 |              0.15 |                    0.5 |                         10 |
| Steel      |                   210 |              0.25 |                    355 |                        355 |

Fig. 1. Top: example of overbreaks induced by local rock collapses for different joint pattern orientations (CETU (1998)). Bottom: examples of the real overbreaks due to local rock collapses as measured during the excavation of the Frejus tunnel (Lunardi (1979)).

<!-- image -->

Engineering drawing

Fig. 2. Schematic example of the geometry of a shotcrete lining when there is an irregular geometry of the tunnel boundary.

<!-- image -->

Engineering drawing

Fig. 3. Photograph of large overbreaks induced by joints discontinuities around a road tunnel. The steel rib indicates the theoretical tunnel boundary (courtesy Prof. S. Pelizza).

<!-- image -->

Photograph

Fig. 4. Example of usual irregularity of the boundary for a road tunnel excavated by drill and blast in black calcareous shists (courtesy Prof. S. Pelizza).

<!-- image -->

Photograph

Fig. 5. Cracks in the shotcrete lining (design average thickness of 20 cm) of a water conveyance tunnel. The rock bolts were later installed to control and stabilize the lining. The cracks were induced by the presence of large irregularities of the tunnel boundary (photograph archive Prof. D. Peila).

<!-- image -->

Photograph

Fig. 6. Layout of the model, horizontal q h and vertical q v loads and node numbers ( R =5.75 m).

<!-- image -->

Engineering drawing

Fig. 7. Constitutive relationship of the springs that represents the soil reaction in the bedded-spring model ( p n and p t represent the normal and tangential load, δ n and δ t the normal and tangential displacement and K n and K t the normal and tangential stiffness).

<!-- image -->

Line chart

Fig. 8. Cross section of the tunnel studied (dimensions in m). The eight group of fuzzy beams are represented with different thickness (group 1 to group 8 from right to left).

<!-- image -->

Line chart

Fig. 9. Example of the real shape of the extrados after excavation by drill and blast in a flysch (used as the basis for the development of the computational example).

<!-- image -->

Engineering drawing

Fig. 10. Membership functions for thickness t of beams group 1-8.

<!-- image -->

Line chart

Fig. 11. Membership functions for horizontal displacement u of node 35.

<!-- image -->

Line chart

Fig. 12. Membership functions for vertical displacement v of node 35.

<!-- image -->

Line chart

Fig. 13. Membership functions for normal force N (element 15).

<!-- image -->

Line chart

Fig. 14. Membership functions for bending moment M (element 15).

<!-- image -->

Line chart

Fig. 15. Membership functions for shear force T (element 15).

<!-- image -->

Line chart

Fig. 16. Normal force in the lining for α =0 and α =1.

<!-- image -->

Line chart

Fig. 17. Bending moment in the lining for α =0 and α =1.

<!-- image -->

Line chart

Fig. 18. Shear force in the lining for α =0 and α =1.

<!-- image -->

Line chart

Fig. 19. Bending moment M vs. normal force N for shotcrete.

<!-- image -->

Line chart

Fig. 20. Bending moment M vs. normal force N for steel ribs.

<!-- image -->

Scatter plot

Fig. 21. Shear force T vs. normal force N for shotcrete.

<!-- image -->

Line chart

Fig. 22. Shear force T vs. normal force N for steel ribs.

<!-- image -->

Line chart
<!-- image -->

Logo

## Optimal selection of a metro tunnel excavation method using AHP and TOPSIS: a case study of Tehran metro OPEN

Amirhossein Rostami 1  , Hamid Chakeri 2 , Kurosh Shahriar 3 &amp; Hamid Mousapour 2

Urban tunnel construction often faces challenges due to weak ground conditions or shallow overburden, making effective stabilization of surrounding soil critical. Selecting an appropriate excavation method is essential for controlling ground subsidence and convergence, which are key considerations in tunnel design, especially in densely populated areas. Excavation-induced ground movements can propagate upward, potentially causing surface subsidence and structural damage. Therefore, a systematic decision-making framework is indispensable during the design phase. This study presents a comprehensive model for selecting the optimal excavation method for Phase 4 of Tehran Metro Line 3. The model evaluates a wide range of criteria, including technical, financial, managerial, social, and geo-mechanical factors. Seven candidate alternatives were considered: Open Shield (full face) method, Slurry method, NATM (New Austrian Tunneling Method), fore-poling, twintunnel excavation with TBM, EPB (Earth Pressure Balance) Shield method, and Open Trench method. The Analytical Hierarchy Process (AHP) was applied to derive criteria weights, and the Technique for Order Preference by Similarity to Ideal Solution (TOPSIS) was employed to rank alternatives. Both methods consistently identified Alternative E as the most suitable excavation method. The proposed framework provides a robust and systematic approach that can be applied to future metro tunneling projects, ensuring informed decision-making under complex technical and environmental constraints.

Keywords Excavation method, Multi-criteria decision-making, AHP, TOPSIS, Tehran metro tunnel

Urban tunnels are often excavated at shallow depths due to weak ground conditions, traffic limitations, and logistical  challenges.  Minimizing  ground  displacement  is  therefore  a  fundamental  design  objective.  Initial lining and excavation methods-including steel beams, lattice girders, precast segments, and reinforcementsstabilize the tunnel both during and after excavation, ensuring structural integrity. In some cases, the initial lining functions as both temporary and permanent support, whereas in others, additional reinforcements such as cast-in-place concrete are required.

Predicting cutter wear and clogging in mechanized tunneling is crucial for ensuring both efficiency and safety during excavation. Excessive tool wear can lead to frequent stoppages, higher maintenance costs, and unexpected project delays, while clogging caused by soil adhesion may reduce cutting performance and endanger the stability of the excavation face. By anticipating these phenomena, engineers can optimize tool replacement schedules, minimize downtime, and improve the overall reliability of tunnel boring operations 1-6 .

Numerical methods provide a powerful approach for predicting cutter wear in mechanized excavation by simulating the complex interactions between the cutting tools, rock or soil conditions, and machine operational parameters.  Using  techniques  such  as  finite  element  modeling,  discrete  element  methods,  and  coupled simulations, engineers can estimate stress distribution, contact forces, and material removal rates that directly influence wear. These predictive models not only enhance the accuracy of wear forecasts but also support the design of more durable cutting tools and the selection of optimal tunneling strategies 7 .

Resilience  of  underground  infrastructure  has  increasingly  been  recognized  as  a  critical  performance objective, particularly in dense urban environments where excavation-induced risks directly influence service continuity and safety. The selection of an appropriate excavation method contributes to the resilience of metro systems by reducing disruption to surface structures and ensuring rapid recovery in case of unexpected events.

1 Department  of  Mining  Engineering,  South Tehran  Branch,  Islamic Azad University, Tehran,  Iran. 2 Department of  Mining  Engineering,  Sahand  University  of Technology, Tabriz,  Iran. 3 Department  of  Mining  and  Metallurgy Engineering, Amir Kabir University of Technology, Tehran, Iran.  email: arostami80@gmail.com Recent studies have emphasized the importance of incorporating resilience considerations into underground construction planning 8 .

Since multiple technical and non-technical factors influence the selection of excavation methods, relying on a single perspective is insufficient. Expert judgment combined with systematic decision-making is required. Multi-Attribute Decision-Making (MADM), a subset of Multi-Criteria Decision-Making (MCDM), provides a structured framework for weighting criteria and ranking alternatives 9-14 .

MADM methods have been widely applied in mining and geotechnical engineering. For example, Tan et al. (2022) applied AHP to optimize environmental reclamation of open-pit mines, while Mahmut (2008) designed excavation methods for coal mines using AHP 15,16 . Similarly, Bangian et al. (2012 ) employed MADM to support post-mining land-use decisions 16 .

In the following of this research, we provide a brief yet structured synopsis of prior studies in this field, outlining their aims, methodologies, and principal findings to position our work within the existing literature.

Nezarat  et  al.  (2015)  conducted  a  risk  assessment  study  for  mechanized  tunneling  projects,  focusing  on uncertainty in foundation conditions that can affect safety and project economy. Using expert input and geological data, they identified eight categories of risks and evaluated them through the Fuzzy Analytical Hierarchy Process (FAHP). The case study of the Golab Tunnel in Iran revealed that squeezing and face instability posed the highest risks, while gas emissions and clay clogging were the least significant 17 .

Wu  et  al.  (2020)  use  3D  simulations  to  test  how  construction  sequence,  support-closure  timing,  and reinforcement settings affect metro-tunnel stability, then rank options with an FAHP-grey correlation-TOPSIS model using deformation and stress indicators. They show that higher relative-closeness scores mean greater stability, and the top-ranked parameter set-applied at Beijing Metro Line 17 reduced risk and offers a practical recipe for similar projects 12 .

Baloyi and Meyer (2020) explored the application of multi-criteria decision-making (MCDM) methods to improve the mining method selection (MMS) process, which traditionally lacked comprehensive and unbiased evaluation. They compared ten MCDM techniques-including TOPSIS, PROMETHEE, TODIM, and VIKORthrough case studies and statistical analyses to identify the most effective methods for coal mining. The results showed  that  PROMETHEE,  TOPSIS,  and  TODIM  were  the  most  suitable  tools  for  MMS,  leading  to  the development of a systematic, case-based MMS model for future decision support in mining 18 .

Genger et al. (2021) create a GIS-based MCDM framework (AHP/ANP + TOPSIS) to rank street corridors for multi-purpose utility tunnels. By layering criteria like utility density, traffic, and expected excavations, they generate suitability maps and show that modeling criterion dependencies (ANP) improves location decisions over simpler weighting 19 .

Zhu et al. (2021) conducted a systematic literature review and bibliometric analysis of 530 studies published between 2000 and 2019 to explore the application of multiple-criteria decision-making (MCDM) methods in the construction industry. They classified the research into seven main application areas and analyzed the evolution, trends, and thematic focus of methods such as AHP and TOPSIS. Their findings highlighted key challengesincluding  robustness,  applicability,  and  scale  issues-and  suggested  future  directions  for  improving  MCDM approaches in construction decision-making 20 .

Li et al. (2022) developed a comprehensive risk evaluation model for slurry balancing shield tunneling based on system engineering principles and the 'human-machine-material-method-environment' framework. They modified the analytic hierarchy process (AHP) and integrated it with fuzzy synthetic evaluation to quantitatively assess safety risks throughout the construction process. Using a case study, they validated the model's effectiveness and proposed management, economic, and technical measures to mitigate identified risks 21 .

Zhang and Chen (2022) proposed a hybrid soft computing method combining the cloud model and TOPSIS to address uncertainty in multi-criteria decision-making (MCDM) problems. They applied the model to tunnel excavation method selection using 16 evaluation criteria and Monte Carlo simulations to assess uncertainty and sensitivity.  The  study  found  that  the  shield  tunnel  boring  machine  (TBM)  was  the  optimal  choice,  and highlighted how increasing uncertainty (Entropy) leads to greater inconsistency in decision outcomes 22 .

Yang et al. (2023) developed a comprehensive evaluation model for tunnel drilling and blasting ergonomics using the game theory-based G2-EW-TOPSIS method. The model integrates 11 indicators across efficiency, duration,  and  synergy  factors,  assigning  combined  subjective-objective  weights  through  Nash  equilibrium optimization. Applying the method to the Shangtianling Tunnel project, they found it effectively identified key factors influencing excavation ergonomics and provided reliable performance ratings 23 .

Kong and Zhang (2024) propose a practical framework to assess water-inrush risk during tunnel construction by  combining  fuzzy  AHP  for  criterion  weighting  with  an  interval  form  of  TOPSIS  (FAHP-I-TOPSIS)  that outputs risk intervals instead of single-point scores, capturing on-site uncertainty; applied to the Shijingshan Tunnel case, the model highlights structural discontinuities (cracks, fault zones) as dominant drivers of high risk and shows greater robustness than classic TOPSIS and VIKOR, aligning well with field evidence and providing clearer guidance for targeted grouting, drainage, and monitoring 24 .

Zhang et al. (2024) propose a compact MCDM framework for tunnel blasting under existing buildings: they weight a three-level, 15-indicator system with LFPP and evaluate scheme 'rationality' using FAHP to identify the most influential parameters. Applied to the No. 3 Tunnel on Georgia's E60 Highway, their optimized scheme aligned better with field monitoring than traditional methods, improving blasting effectiveness while reducing vibration impacts 25 .

Jia et al. (2024) develop a real-time heat-stress assessment and early-warning approach for semi-enclosed, high-temperature tunnels by collecting on-site environmental (air, globe, and wet-bulb temperatures, humidity, wind) and physiological (skin temperature, heart rate) data and fusing them with an integrated-weight TOPSIS model to create the TSIcw (Thermal Stress Index-combined weighting). They find air temperature, relative humidity, and dry-bulb temperature are the dominant drivers; TSIcw tracks well with WBGT (Wet-Bulb Globe Temperature) and offers practical risk bands-high (0-0.58), moderate (0.58-0.83), and low (0.83-1)-to guide timely worker protection 26 .

Table 1 .  Summary of research methods.

| Research method                                                                                | Research method                                                                                |
|------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------|
| Introducing effective alternatives and criteria for selecting a metro tunnel excavation method | Introducing effective alternatives and criteria for selecting a metro tunnel excavation method |
| Selecting best alternative by AHP method                                                       | Selecting best alternative by TOPSIS method                                                    |
| Introducing the best criteria selected by AHP and TOPSIS                                       | Introducing the best criteria selected by AHP and TOPSIS                                       |
| Numerical analysis of selected case study.                                                     | Numerical analysis of selected case study.                                                     |

Table 2 .  Hierarchy for optimum excavation method selection.

| Level 1: Goal        | Excavation method selection   | Excavation method selection   | Excavation method selection   | Excavation method selection   | Excavation method selection   | Excavation method selection   | Excavation method selection   |
|----------------------|-------------------------------|-------------------------------|-------------------------------|-------------------------------|-------------------------------|-------------------------------|-------------------------------|
| Level 2: Criteria    | c 1                           | c 2                           | …                             | …                             | …                             | …                             | c 31                          |
| Level 3: Alternative | A                             | B                             | C                             | D                             | E                             | F                             | G                             |

Table 3 .  Saaty's preference scale for pairwise comparison 29 .

| Oral judgments          | Numeral value   |
|-------------------------|-----------------|
| Extremely preferred     | 9               |
| Very strongly preferred | 7               |
| Strongly preferred      | 5               |
| Moderately preferred    | 3               |
| Equally preferred       | 1               |
| Intermediate preferred  | 2, 4, 6 and 8   |

In  this  study,  AHP  was  used  to  derive  weights  for  selection  criteria  through  pairwise  comparisons,  and TOPSIS was applied to rank tunnel support alternatives. Expert choice (2010) software was used for AHP , while MADM Selection software supported TOPSIS 27 . The combined application of these methods enhances reliability and ensures robust decision-making. A summary of the research methodology is presented in Table 1.

## Multi-criteria decision-making techniques and decision tree

MCDM methods are particularly useful when multiple, and often conflicting, criteria affect decision-making. In this study, AHP was first applied to generate criterion weights, followed by TOPSIS for final evaluation. The decision tree, Table 2 illustrates the hierarchical structure, with the overall goal at the top, criteria at the second level, and alternatives at the third.

To justify the criteria system, the 31 items (C1-C31) were derived through a structured, multi-step process embedded in the AHP-TOPSIS workflow. First, an initial long-list of decision criteria was compiled from a scoping  review  of  peer-reviewed  studies  and  relevant  tunneling/metro  standards.  Second,  semi-structured consultations with domain experts (geotechnical engineering, construction management, and metro operations) were conducted to contextualize items and ensure measurability. Third, a two-round Delphi exercise was used to  refine  wording,  merge  overlaps,  and  remove  items  considered  ambiguous  or  non-actionable.  Fourth,  the surviving items were mapped to five dimensions (technical, geomechanical, economic, executive, and social) and labeled as benefit or cost criteria to align with the TOPSIS ideal/anti-ideal formulation. Finally, screening retained criteria meeting pre-specified thresholds for relevance (median ≥ 4 on a 5-point scale) and feasibility (median ≥ 3), while highly redundant items (inter-item r &gt;  0.80) were excluded.

## Analytical hierarchy process (AHP)

AHP, developed by Saaty (2022), is one of the most widely used MCDM methods. The procedure involves the following steps 28 :

1. Hierarchy Construction: Define the overall goal, criteria, and alternatives.
2. Decision-Making Matrix: Construct pairwise comparison matrices based on Saaty's nine-point scale (Table 3).
3. Pairwise comparisons: Compare criteria to determine relative importance (Eq. 1):

<!-- formula-not-decoded -->

Where, the element a ij is interpreted as the degree of preference of i attribute over j attribute and vice versa.

4. Normalization: Normalize the comparison matrices so that column sums equal one (Eq. 2):

<!-- formula-not-decoded -->

5. Relative Weights: Compute the average of row values to obtain relative weights.
6. Overall Weights: Multiply relative weights by higher-level weights to form the global weighting vector (Eq. 3):

<!-- formula-not-decoded -->

Where w i is the weight of the i attribute.

7. Consistency  Check:  Calculate  the  consistency  ratio  (CR),  which  must  be  below  0.10  for  reliable  results (Eq. 4):

<!-- formula-not-decoded -->

Where λ max is the highest eigen value of the pair-wise comparison matrix.

For group decision-making, expert judgments are aggregated using the geometric mean 29 . Weighted averages may be applied if expert opinions differ in importance. In these cases, as Eq. 5, geometrical average of different expert opinions ( x ′ ij ) should be calculated as the basic matrix (2).

<!-- formula-not-decoded -->

In this Equation L is the identification number of a decision maker, K is the number of decision makers and (i, j) are the comparative criteria or alternatives. Also, if the opinions of decision makers have different effects, we can evaluate weight expert opinions ( w l ) according to Eq. 6.

<!-- formula-not-decoded -->

To ensure compatibility of the basic couple comparison matrix, the opinions and comparisons should be similar; otherwise, probability of incompatibility of matrix increases.

## Technique for order preference by similarity to ideal solution (TOPSIS)

TOPSIS, developed by Hwang and Yoon (1981 ) , identifies the alternative closest to the positive ideal solution (PIS) and farthest from the negative ideal solution (NIS) 30 . The main steps include:

1. Weighted normalized matrix: Normalize the decision matrix and apply criterion weights. based on Eq. 7 below, in the TOPSIS algorithm the inputs are in the form of a weighted normalized matrix v ij . This matrix is the outcome of multiplication of the normalized matrix R ij (Eq. 2), in the diagonal matrix of total weighting of criteria, w i (Eq. 3).

<!-- formula-not-decoded -->

4

2. Ideal solutions: (Determine PIS and NIS) Determine positive (best) and negative (worst) solutions. Using weighted normalized matrix in which the criteria are specified, Positive-Ideal Solution A ∗ , and Negative-Ideal Solution A - , are determined by Eq. 8 and Eq. 9 respectively.

<!-- formula-not-decoded -->

Where 'I' is associated with benefit criteria, and I ′ ′ is associated with cost criteria.

<!-- formula-not-decoded -->

It should be noted that, in this formulation, the positive and negative ideal solutions are not manually selected based on expert opinion; instead, they are automatically determined from the extrema of the normalized decision matrix (best performance for benefit criteria and worst performance for cost criteria). Subjective influence is thus limited to the weighting stage.

3. Distance Measures: Compute the Euclidean distance of each alternative from PIS and NIS. The Euclidean distance of each alternative from positive ideal d + i and negative ideal d - i are calculated through Eq. 10 and Eq. 11, respectively.

<!-- formula-not-decoded -->

4. Relative closeness: Calculate the relative closeness of each alternative to PIS. The relative closeness CL ∗ i calculated by Eq. 12.

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

Since d - j ≥0 and d + j ≥0, then clearly CL ∗ i ∈ [0, 1].

5. Ranking: Rank alternatives; the one with the highest closeness value is preferred. All alternatives are ranked based on the amounts of CL ∗ i and the alternative which has the maximum CL ∗ i is  considered the most appropriate alternative.

Robustness  of  the  rankings  to  weight  uncertainty  was  examined  using  both  deterministic  and  probabilistic perturbations embedded in the AHP-TOPSIS workflow. First, an OAT (one at a time) analysis was performed by varying each criterion weight by ± 10-20% with proportional re-normalization; TOPSIS closeness values and ranks were recalculated after each perturbation, and the maximum rank shift per alternative was recorded. Second, a probabilistic experiment was conducted by sampling MMM weight vectors from a Dirichlet distribution Dir ( K w ) centered on the baseline AHP weights. For each draw, the ideal/anti-ideal solutions, distances ( d + i , d - i ), and closeness ( C i ) were recomputed to obtain ranks. Stability was summarized by the probability of each alternative being ranked first and top-2, the rank-switching rate, and Spearman's ρ relative to the baseline.

## Options and criteria for choosing a subway excavation method

Subway tunnels reduce urban congestion and improve transportation efficiency. However, variable overburden and  urban  constraints  necessitate  careful  selection  of  excavation  methods.  For  Tehran  Metro  Line  3,  Phase 4  (between  Hemat  Bridge  and  Sayad-Shirazi),  ten  support  alternatives  were  evaluated  based  on  economic, executive, social, technical, and geo-mechanical criteria. Tables 4, 5, 6, 7, 8 and 9 present the alternatives and the evaluation criteria.

This study applied AHP under the assumption of independence among criteria, which is consistent with pre-construction  decision-making  where  baseline  conditions  are  considered.  Although  certain  criteria  may exhibit  conceptual  relationships  (e.g.,  subsidence  and  effects  on  surface  structures),  expert-based  screening and refinement were employed to minimize overlap and avoid double-counting. The stability of the ranking underweight uncertainty indicates that any residual inter-dependencies are unlikely to affect the final selection. Future extensions could incorporate ANP or network-based models to explicitly account for interrelationships when more detailed information becomes available during construction.

Table 4 .  Alternatives for Tehran subway excavation method, line 3, phase 4.

| A   | Slurry method                              |
|-----|--------------------------------------------|
| B   | Open Trench method                         |
| C   | fore-poling method                         |
| D   | Open Shield (full face) method             |
| E   | NATM (New Austrian Tunnelling Method)      |
| F   | EPB (Earth Pressure Balance) Shield method |
| G   | Twin tunnel excavation with the TBM method |

Table 5 .  Economic elements for Tehran subway excavation method, line 3, phase 4.

| c 1   | Investment costs       |
|-------|------------------------|
| c 2   | Operational costs      |
| c 3   | Costs of contingencies |

Table 6 .  Executive elements for Tehran subway excavation method, line 3, phase 4.

| c 4   | Availability of skilled workforce                                                                  |
|-------|----------------------------------------------------------------------------------------------------|
| c 5   | Availability of necessary machinery and equipment                                                  |
| c 6   | Necessary flexibility of the method for methodological changes in order to deal with contingencies |
| c 7   | Necessity of using foreign experts                                                                 |
| c 8   | Subsidence                                                                                         |

Table 7 .  Social elements for Tehran subway excavation method, line 3, phase 4.

| c 9   | Job creation                                             |
|-------|----------------------------------------------------------|
| c 10  | Government support                                       |
| c 11  | Compatibility with geological conditions of the location |

Table 8 .  Technical elements for Tehran subway excavation method, line 3, phase 4.

| c 12   | The effect of the opening                                                |
|--------|--------------------------------------------------------------------------|
| c 13   | Order of advancement                                                     |
| c 14   | The influence of earthquake on excavation method                         |
| c 15   | Applicability of the selected excavation method                          |
| c 16   | The ability of the excavation method in shallow overburden conditions    |
| c 17   | Support toughness and its relation to hardness of the earth              |
| c 18   | Time of installing final lining                                          |
| c 19   | The thickness of final lining                                            |
| c 20   | Using mesh to increase resistance                                        |
| c 21   | The existence and the effects of surface structures on excavation method |
| c 22   | Change of layer materials around and in the tunnel                       |

## AHP application

Using  Saaty's  scale,  pairwise  comparison  matrices  were  generated,  normalized,  and  weighted.  The  overall criterion weights are shown in Fig. 1, and the normalized results are provided in Table 10.

The lowest weights are associated with C3, C7, and C16 (0.0020), indicating their relatively limited influence compared with the dominant criteria in the excavation method selection process.

Finally, the overall AHP score of each alternative is obtained by combining the criterion weights with their local priorities using Eq. 13, and the resulting rankings are summarized in Table 11.

Table 9 .  Geo-mechanical features of the place for Tehran subway excavation method, line 3, phase 4.

| c 23   | Chosen                      |
|--------|-----------------------------|
| c 24   | Friction angle              |
| c 25   | Elastic module              |
| c 26   | Tensile strength            |
| c 27   | Compressive strength        |
| c 28   | Poisson ratio               |
| c 29   | Sheering resistance         |
| c 30   | The thickness of overburden |
| c 31   | The effects of water table  |

Fig. 1 .  Vector of the weights of the applied criteria to select the best excavation method alternative.

<!-- image -->

Bar chart

Table 10 .  Normalized matrix and weights of criteria.

| Alternatives Criteria   | A     | B     | C     | D     | E     | F     | G     | Weight   |
|-------------------------|-------|-------|-------|-------|-------|-------|-------|----------|
| c 1                     | 0.088 | 0.040 | 0.062 | 0.154 | 0.268 | 0.261 | 0.068 | 0.006    |
| c 2                     | 0.128 | 0.074 | 0.136 | 0.143 | 0.164 | 0.197 | 0.023 | 0.010    |
| …                       | …     | …     | …     | …     | …     | …     | …     | …        |
| c 30                    | 0.111 | 0.067 | 0.067 | 0.140 | 0.282 | 0.202 | 0.054 | 0.052    |
| c 31                    | 0.101 | 0.062 | 0.079 | 0.142 | 0.256 | 0.205 | 0.048 | 0.024    |

<!-- formula-not-decoded -->

Where a ij shows the relative importance of alternative 'i' for C j criterion and W j , shows the importance of criterion C j .

The pairwise comparison matrices were completed by an expert panel assembled based on domain relevance and  professional  experience.  The  panel  consisted  of  eight  specialists  from  geotechnical  engineering,  tunnel construction management, and metro operations, each with more than 10 years of experience in underground construction projects. A conflict-of-interest check was conducted to confirm that none of the experts were directly engaged in contractor selection or financial decision-making for the studied project. Individual judgments were aggregated using the geometric mean to obtain the final comparison matrices.

7

Table 11 .  Weights and ranking of alternatives (AHP method).

| Alternative s   |   weights |   Rankings |
|-----------------|-----------|------------|
| A               |     0.105 |          4 |
| B               |     0.068 |          7 |
| C               |     0.080 |          5 |
| D               |     0.128 |          3 |
| E               |     0.225 |          1 |
| F               |     0.174 |          2 |
| G               |     0.071 |          6 |

Fig. 2 .  Final ranking of alternatives for excavation method by AHP method.

<!-- image -->

Bar chart

The evaluation framework follows a single-level AHP hierarchy, and thus a single 31 × 31 pairwise comparison matrix was constructed to derive the final criteria weights. The consistency ratio was CR = 0.07, confirming acceptable judgment consistency.

In addition, the alternatives and the weights of criteria must be normalized based on Eq. 14 and Eq. 15.

<!-- formula-not-decoded -->

Based on the AHP analysis, Alternative E ranked highest, followed by D and F (Fig. 2).

<!-- formula-not-decoded -->

To incorporate objective weighting and assess the influence of alternative weighting schemes, the CRITIC method (Criteria Importance Through Intercriteria Correlation) was additionally applied. In this procedure, weights are determined based on the contrast intensity (represented by the standard deviation of each criterion) and the conflict among criteria (represented by the correlation structure of the normalized decision matrix). The computed CRITIC weights were then substituted into the TOPSIS formulation to obtain an alternative ranking, and deviations from the baseline AHP-based ranking were recorded.

## TOPSIS application

The weighted normalized matrix was calculated (Table 12), and the positive and negative ideal solutions were determined (Table 13). Relative closeness values and final rankings are summarized in Table 14.

Consistent  with  the  AHP  results,  the  TOPSIS  method  also  ranked  Alternative  E  as  the  optimal  choice, followed by F and D (Fig. 3). Figure 4 further illustrates the joint application of AHP and TOPSIS in selecting the most suitable tunnel excavation method.

When CRITIC-derived objective weights were used, the top-ranked alternative remained unchanged, and only minor rank shifts were observed for lower-ranked options, indicating consistent selection performance across subjective and objective weighting schemes.

Although the ideal solutions in TOPSIS are mathematically derived, subjective judgment in the weighting stage may still affect prioritization; hybrid schemes combining subjective and objective weighting can further reduce such influence.

Table 12 .  Weighted normalized matrix of excavation method alternatives.

| Alternatives Criteria   | A        | B        | C        | D        | E        | F        | G        |
|-------------------------|----------|----------|----------|----------|----------|----------|----------|
| c 1                     | 0.000528 | 0.000240 | 0.000372 | 0.000924 | 0.001608 | 0.001566 | 0.000408 |
| …                       | …        | …        | …        | …        | …        | …        | …        |
| c 30                    | 0.005772 | 0.003484 | 0.003484 | 0.007280 | 0.014664 | 0.010504 | 0.002808 |
| c 31                    | 0.002424 | 0.001488 | 0.001896 | 0.003408 | 0.006144 | 0.004920 | 0.001152 |

Table 13 .  Positive and negative ideal solutions for selecting a excavation method alternative.

| Criteria   | Positive ideal solution   | Negative ideal solution   |
|------------|---------------------------|---------------------------|
| c 1        | 0.001608                  | 0.000084                  |
| …          | …                         | …                         |
| …          | …                         | …                         |
| c 30       | 0.009471                  | 0.000594                  |
| c 31       | 0.014144                  | 0.001040                  |

Table 14 .  Relative closeness to positive and negative ideal solutions and the final ranking of tunnel excavation method alternatives.

| Alternative   |   Distance from positive ideal |   Distance from negative ideal |   Relative closeness to ideal solutions |   Ranking |
|---------------|--------------------------------|--------------------------------|-----------------------------------------|-----------|
| A             |                      0.0267777 |                      0.0140543 |                               0.3441977 |         4 |
| B             |                      0.0330497 |                      0.0104121 |                               0.2395698 |         7 |
| C             |                      0.0311902 |                      0.0111021 |                               0.2625089 |         6 |
| D             |                      0.0225808 |                      0.0185265 |                               0.4506864 |         3 |
| E             |                      0.0114027 |                      0.0363374 |                               0.7611506 |         1 |
| F             |                      0.0164936 |                      0.0272655 |                               0.6230811 |         2 |
| G             |                      0.0328976 |                      0.0169288 |                               0.3397548 |         5 |

Fig. 3 .  Final ranking of tunnel excavation method alternatives by TOPSIS method.

<!-- image -->

Bar chart

Fig. 4 .  Tunnel cross-section considering common seasons and excavation stages.

<!-- image -->

Flow chart

Table 15 .  Analytical items at 5 different sections of the station.

|   Analysis number | Cases section   |   Overburden (m) |   Groundwater level (m) | Dynamic loads (m)   |
|-------------------|-----------------|------------------|-------------------------|---------------------|
|                 1 | A               |                3 |                      30 | 0.6                 |
|                 2 | A               |                3 |                      30 | -                   |
|                 3 | B               |                2 |                      34 | 0.6                 |
|                 4 | B               |                2 |                      34 | -                   |
|                 5 | C               |                1 |                    38.5 | 0.6                 |
|                 6 | C               |                1 |                    38.5 | -                   |
|                 7 | D               |              0.5 |                      42 | 0.6                 |
|                 8 | D               |              0.5 |                      42 | -                   |
|                 9 | E               |                0 |                      47 | 0.6                 |
|                10 | E               |                0 |                      47 | -                   |

## Numerical modelling

The alignment of Tehran Metro Line 3 extends diagonally from Qale Morghi in the southwest to Ghaem Boulevard in the northeast. The northern extension spans from Shariati-Beheshti intersection to Ghaem Boulevard, with a significant portion passing beneath Sayad Shirazi Highway 9 . A water canal and other urban utilities also run parallel to the project alignment, requiring careful selection of construction methods to minimize disruption.

The construction process was analyzed using the finite ellement method (FEM) in two dimensions with PLAXIS software. The main objective was to evaluate tunnel stability  after  construction  rather  than  during excavation (Table 15). Only Section A was modeled step by step, considering groundwater levels, overburden conditions, and dynamic loads.

Dynamic loading was defined using an elastic response spectrum consistent with Iranian seismic design provisions for high-seismicity regions. An upper-bound horizontal peak ground acceleration (PGA) of 0.6 g was adopted to represent a severe shaking scenario for the Tehran area, accounting for near-fault effects and epistemic uncertainty in ground-motion characteristics, rather than a single code-prescribed value for a specific return period 31 .

Initial pore-pressure conditions were established using a phreatic level corresponding to the groundwater table reported in Table 15. A steady-state seepage analysis was performed prior to mechanical excavation stages to ensure hydrostatic pore-pressure equilibrium and consistent effective stress initialization across the model domain.

Table 16 .  Soil information surrounding the tunnel.

| Parameter                    | Sign    | Layer L1     | Layer L2     | Unit   |
|------------------------------|---------|--------------|--------------|--------|
| Material model               | Model   | Mohr Coulomb | Mohr Coulomb | -      |
| Type of material behavior    | Type    | Drained      | Drained      | -      |
| Unsaturated specific gravity | γ unsat | 21           | 21           | kN/m 3 |
| Saturated specific gravity   | γ sat   | 22.4         | 22.4         | kN/m 3 |
| Vertical permeability        | K y     | 0.086        | 0.086        | m/day  |
| Horizontal permeability      | K x     | 0.086        | 0.086        | m/day  |
| Young's modulus              | E ref   | 113,800      | 250,300      | kN/m 2 |
| Poisson's ratio              | υ       | 0.35         | 0.35         | -      |
| Cohesion                     | c ref   | 7            | 7            | kN/m 2 |
| Friction angle               | φ       | 40           | 40           | -      |
| Dilation angle               | ψ       | 10           | 10           | -      |
| Resistance reduction factor  | R inter | -            | 0.45         | -      |

Table 17 .  Lattice girder information for guard structure.

| Parameter                 | Sign          | T100         | T140         | T170         | Unit      |
|---------------------------|---------------|--------------|--------------|--------------|-----------|
| Type of material behavior | Material type | Elastic      | Elastic      | Elastic      | -         |
| Normal hardness           | EA            | 23.88 × 10 6 | 43.33 × 10 6 | 40.59 × 10 6 | kN/m      |
| Flexural stiffness        | EI            | 497.4 × 10 3 | 1365 × 10 3  | 2.44 × 10 6  | kN/m 2 /m |
| Equivalent thickness      | d             | 0.25         | 0.7          | 0.85         | m         |
| Weight                    | w             | 25           | 25           | 25           | kN/m/m    |
| Poisson's ratio           | υ             | 0.18         | 0.18         | 0.18         | -         |

Table 18 .  Main lattice girder information for guard structure.

| Parameter                 | Sign          | T100         | T140          | T170          | Unit      |
|---------------------------|---------------|--------------|---------------|---------------|-----------|
| Type of material behavior | Material type | Elastic      | Elastic       | Elastic       | -         |
| Normal hardness           | EA            | 47.75 × 10 6 | 71.63 × 10 6  | 16.71 × 10 6  | kN/m      |
| Flexural stiffness        | EI            | 3.979 × 10 6 | 0.1343 × 10 6 | 0.1706 × 10 6 | kN/m 2 /m |
| Equivalent thickness      | d             | 1            | 0.15          | 0.35          | m         |
| Weight                    | w             | 25           | 25            | 25            | kN/m/m    |
| Poisson's ratio           | υ             | 0.18         | 0.18          | 0.18          | -         |

## Creating the tunnel geometry

Based on the maps provided, the tunnel's geometry was accurately represented in the software environment using its coordinates. The distance of the model boundaries from the tunnel was approximately determined using the Kirsch relationship. According to this relationship, the lateral boundaries are set at 10 times the average tunnel radius from its center. Thus, the model dimensions are 80 m in the x-direction (on both sides of the tunnel) and 60 m in the -y direction (below the tunnel). For the analyses, the Mohr-Coulomb constitutive model was employed to represent the material behavior 13 . The Mohr-Coulomb model, one of the most common behavioral models in soil mechanics, is fully elastic and characterized by five main parameters.

## Information on materials used

Information regarding the surrounding soil was defined in the model according to Table 16. Lattice girders were modeled based on the data in Table 17 and 18, and the tunnel lining concrete adopted parameters from Table 19.

## Cross-section loading process

After applying the interfaces between the materials, the tunnel cross-section is depicted in Fig. 5 . This figure also illustrates the sections excavated during each phase.

With a specific weight of water set to 10 kN/m³, a water table with a height of 30 m above the ground surface at Section A was applied to the model to establish initial conditions. In all eight phases, intermediate calculations and displacements from previous phases were considered, and all undrained behaviors were accounted for. The loading type for the phases is structurally staged, the calculation type is plastic, and the maximum number of stages is 250.

Table 19 .  Tunnel lining concrete information.

| Parameter                    | Sign    | Concrete       | Unit   |
|------------------------------|---------|----------------|--------|
| Material model               | Model   | Linear elastic | -      |
| Type of material behavior    | Type    | No porosity    | -      |
| Unsaturated specific gravity | γ unsat | 25             | kN/m 3 |
| Young's modulus              | E ref   | 23,420,000     | kN/m 2 |
| Poisson's ratio              | υ       | 0.18           | -      |
| Cohesion                     | c ref   | 7              | kN/m 2 |

Fig. 5 .  Tunnel excavation phases.

<!-- image -->

Engineering drawing

## Excavation stages

The excavation was carried out in eight distinct phases, as shown in Fig. 6.

- Phase 1: In this phase, Sect. 1 of the excavation was completed, and the surrounding lattices were installed. The maximum displacement at the end of this phase measured 11.37 mm at the gallery floor.
- Phase 2: Sect. 2 of the excavation was completed, and its surrounding lattices were installed. The excavation and lattice installation in this phase were performed similarly to Phase 1. The maximum displacement at the end of this phase was 11.18 mm at the floor of gallery number 1.
- Phase 3: After removing the lattice from the floor of gallery number 1, Sect. 3 was excavated, and the surrounding lattices were installed, followed by concrete pouring. The maximum displacement at the end of this phase was 11.05 mm at the floor of gallery 2 mm.
- Phase 4: Sect. 4 was excavated, and its surrounding lattices were installed. The maximum displacement at the end of this phase was 35.54 mm at the tunnel ceiling level.
- Phase 5: Sect. 5 was excavated, and concrete was poured along the tunnel ceiling. The maximum displacement at the end of this phase was 35.37 mm at the tunnel ceiling.
- Phase 6: Sect. 6 was excavated, and its floor lattice was installed. The maximum displacement at the end of this phase was 36.36 mm at the tunnel ceiling.
- Phase 7: Sect. 7 was excavated, the surrounding lattices were removed, and concrete was poured. At the end of this phase, the upper part of the tunnel was completed. The maximum displacement at the end of this phase was 37.37 mm at the tunnel ceiling.
- Phase 8: The lower part of the tunnel was excavated, and the surrounding lattices were installed, followed by concrete pouring. The maximum displacement at the end of this phase was 37.01 mm at the ceiling.

## Numerical modeling results and their analysis

As observed in Fig. 7, the maximum displacement of 37.01 mm occurred at the tunnel ceiling. Notably, most of the displacement concentrated in the upper part of the tunnel, with minimal displacement in the lower floor. This pattern suggests that the majority of the applied pressure acts on the upper part of the tunnel. Displacement contours were generated based on nodal displacement results from the finite-element analysis. The maximum displacement value indicated in the figures corresponds to the maximum nodal magnitude and lies within the displayed contour scale range.

Table 20 presents the values obtained across 10 loading cases after the final analysis stage, following the installation of permanent and temporary supports. The analysis stages for the other nine analyses were identical to this one. To draw conclusions, compare, and assess the effect of each factor, the final parameter values for each of the 10 analysis cases are summarized in Table 20. The predicted displacements in Cases 9 and 10 differ by less than 1 mm, despite a 5 m change in groundwater level. This limited variation can be attributed to the relatively deep position of the tunnel and the fact that both groundwater levels remain sufficiently below the ground surface, such that the resulting change in pore pressure at tunnel depth is modest. Consequently, the effective stress state and deformation pattern are only slightly affected within this range of water-table variation, which explains the nearly flat displacement response reported in Table 20.

Fig. 6 .  Final displacement at the end of the numerical analysis of section A by 2D PLAXIS software.

<!-- image -->

Engineering drawing

Fig. 7 .  Comparison of tunnel behavior under dynamic and static loading conditions.

<!-- image -->

Engineering drawing

Table 20 .  Values obtained in 10 loading cases after the final stage of analysis (after installation of permanent and temporary supports).

|   Parameter |   Maximum displacement (m × 10 - 3 ) |   Maximum effective stress (kN/m 2 × 10 3 ) |   Maximum displacement of walls (m × 10 - 3 ) |   Maximum shear force (kN/m × 10 3 ) |   Maximum bending moment (kN/m/m) |
|-------------|--------------------------------------|---------------------------------------------|-----------------------------------------------|--------------------------------------|-----------------------------------|
|           1 |                                37.01 |                                       -1.87 |                                         38.73 |                                -2.16 |                              1060 |
|           2 |                                36.33 |                                       -1.86 |                                            38 |                                -2.12 |                              1040 |
|           3 |                                34.99 |                                       -1.84 |                                         36.63 |                                -2.10 |                              1030 |
|           4 |                                34.37 |                                       -1.83 |                                         35.97 |                                -2.05 |                              1010 |
|           5 |                                32.76 |                                       -1.82 |                                         34.33 |                                -2.02 |                               991 |
|           6 |                                32.08 |                                       -1.80 |                                         33.60 |                                -1.98 |                               984 |
|           7 |                                31.88 |                                       -1.80 |                                         33.41 |                                -1.98 |                               971 |
|           8 |                                31.23 |                                       -1.79 |                                         32.73 |                                -1.95 |                               970 |
|           9 |                                30.72 |                                       -1.77 |                                         32.18 |                                -1.92 |                               958 |
|          10 |                                30.71 |                                       -1.77 |                                         32.18 |                                -1.92 |                               958 |

Mesh sensitivity  was  examined  by  refining  the  elements  around  the  tunnel  and  comparing  the  resulting maximum displacements with those from the original mesh; only minor differences were observed, indicating that the reported deformations are not governed by mesh dependency.

To compare the tunnel's behavior under dynamic and static loading conditions, comparative diagrams for each parameter were utilized (Fig. 8). It was observed that, generally, as long as water is present around the tunnel, the dynamic values of the parameters are greater than the static displacement. Once the water leaves the  tunnel  section,  the  difference  between  the  parameters  becomes  almost  negligible,  clearly  indicating  the significant effect of water presence on this parameter. The slope of these parameters also changes proportionally with  the  overburden.  In  these  diagrams,  it  should  be  noted  that  parameters  with  a  constant  slope  indicate their insensitivity to the overburden change factor but their dependence on changes in subsurface water. The maximum bending moment exhibits a moderate increase with overburden depth. A linear regression fitted to the numerical values indicates a noticeable but not highly pronounced dependency, supporting a moderate level of responsiveness under the examined conditions. Regression lines and R² coefficients are shown for all subplots in Fig. 8.

<!-- image -->

Line chart

<!-- image -->

Line chart

<!-- image -->

Line chart

<!-- image -->

Line chart

<!-- image -->

Line chart

Fig. 8 .  Selection of the optimal excavation method (Alternative E) for the metro tunnel using AHP and TOPSIS.

<!-- image -->

Line chart

Based on the graph of overburden changes (assuming Section E as the origin) and groundwater changes along the station in Fig. 8A, the following observations were made:

- In Fig. 8B, generally, when water is present around the tunnel, the dynamic displacement is 0.7 mm greater than the static displacement. After the water exits the tunnel section, the difference between the displacements becomes almost zero, highlighting the effect of water on this parameter. The slope of this parameter also changes proportionally with the overburden. The ratio of dynamic load to static load in the section decreases, consequently reducing the displacement effect related to the dynamic load.
- In Fig. 8C, the dynamic effective stress values are consistently greater than the static stress. With a uniform increase in the depth of the water table and a uniform decrease in the overburden load, the effective stress increases. This phenomenon occurs because, despite water exiting through the pores, the decreasing overburden allows for a greater influence of the effective water pressure on the structure. The increase in the slope of the stress increase can be attributed to the overburden value approaching zero.
- In Fig. 8D, the tunnel wall displacement in the dynamic state is greater than in the static state. The increased slope of the stress reduction at the beginning of the graph can be attributed to the high overburden in these sections.
- In Fig. 7E, the dynamic shear stress exhibits higher values than the static shear stress. As the water table depth increases, the difference in shear stresses decreases. The steep slope of the parameters at the beginning of the graph indicates the significant effect of the overburden on the stresses.
- In Fig. 8F, the change in overburden is identified as the most crucial factor influencing the values of the bending moment. The steep slope of the parameters at the beginning of the graph signifies the pronounced effect of the overburden on the bending moments.

It is acknowledged that the criteria weights used in this study were derived under pre-construction conditions and treated as static values throughout the evaluation. In practice, criterion prioritization may change due to evolving geological  conditions,  newly  identified  hazards,  or  unexpected  operational  constraints  during  excavation. Dynamic weighting approaches such as stage-based re-weighting, adaptive risk-driven updates, or scenariodriven  weighting  schemes  could  therefore  be  integrated  to  better  capture  real-time  variations  in  excavation challenges.  Such  extensions  would  improve  decision  responsiveness  while  maintaining  methodological consistency with the proposed AHP-TOPSIS framework.

It is also recognized that key geological parameters (e.g., friction angle, cohesion, and elastic modulus) are subject  to  inherent  uncertainties  arising  from  spatial  variability  and  limitations  of  subsurface  investigation. Although  crisp  AHP-TOPSIS  was  adopted  to  support  pre-construction  decision-making  using  baseline estimates, future research could integrate fuzzy AHP or interval TOPSIS formulations to explicitly propagate such uncertainties into the weighting and ranking processes, thereby improving robustness under uncertain geological environments.

## Conclusion

This  study  proposed  a  systematic  framework  for  selecting  tunnel  excavation  methods,  applied  to  Tehran Metro Line 3, Phase 4. Based on 31 evaluation criteria and 7 alternatives, both the AHP and TOPSIS methods consistently identified Alternative E as the optimal solution.

- AHP results: E (0.225) ranked highest, followed by F (0.174) and D (0.128).
- TOPSIS results: E (0.761) ranked highest, followed by F (0.623) and D (0.450).

When CRITIC-derived objective weights were used, the top-ranked alternative remained unchanged, and only minor rank shifts were observed for lower-ranked options, indicating consistent selection performance across subjective and objective weighting schemes.

The consistency between the AHP and TOPSIS outcomes confirms the robustness of the findings. Alternative E  demonstrated  clear  superiority,  providing  decision-makers  with  confidence  in  its  implementation.  Minor variations in the ranking of other alternatives can be attributed to methodological differences between the two algorithms.

Numerical modeling further indicated that the tunnel remains stable across all soil sections when lattice girders  are  used  for  temporary  support  and  concrete  for  permanent  support.  For  the  analyzed  station Sect. (19.8 m height, 17.5 m width, 22 m soil cover above the crown, 3 m overburden, and 33 m groundwater depth), the maximum displacement was estimated at 37 mm under dynamic loading.

Groundwater presence consistently produced a distinct difference between static and dynamic responses, except for bending moment. As groundwater depth increased beyond the station boundary, parameter values converged, underscoring its significant influence. Dynamic loads consistently yielded larger values than static loads.

Groundwater  exerted  a  greater  influence  than  overburden  where  slopes  were  constant,  while  bending moment was  less  affected  due  to  its  stronger  dependence  on  tunnel-induced  displacements.  The  predicted surface settlement of 20 mm indicates a moderate and manageable level of deformation under the analyzed conditions. This interpretation should be considered in reference to applicable design limits and future field monitoring where available.

Overall, dynamic loads had a stronger impact on effective stress, total stress, bending moment, and wall displacement. The comparative analyses using PLAXIS 2D confirmed that the proposed decision-making model is both accurate and practically applicable to the project site.

## Data availability

Data that support the findings of this study are available from the corresponding author upon reasonable request.

Received: 6 October 2025; Accepted: 24 December 2025

## References

1.  Chakeri,  H.,  Maleki,  A.,  Shakeri,  H.,  Darbor,  M.  &amp;  Mousapour,  H.  Laboratory  and  numerical  investigation  of  cutting  tool performance using a new small-scale linear cutting machine. Sci. Rep. 15 (1), 22337. https://doi.org/10.1038/s41598-025-08401-8 (2025).
2.  Khodaei, S., Khoshzaher, E., Chakeri, H. &amp; Darmarani, S. M. Laboratory investigation of the performance of two-component Grout behind the segment in sandy soils below the water table level. Rudarsko-geološko-naftni Zbornik . 40 (4), 157-169.  h t t p s : / / d oi . o r g / 1 0 . 17 7 9 4 / r g n . 2 0 2 5 . 4 . 1 2  (2025).
3.  Maleki, A., Chakeri, H., Shakeri, H., Khoshzaher, E. &amp; Darbor, M. Experimental study of effects of mechanical properties of rocks on wear of cutting tools using a new Small-Scale linear cutting machine. J. Min. Environ. 16 (5), 1809-1826.  h t t p s : / / d o i . o r g / 1 0 . 2 2 04 4 / j m e . 2 0 2 5 . 1 5 0 3 3 . 2 8 6 8  (2025).
4.  Khoshzaher, E., Khodaei, S. &amp; Chakeri, H. Laboratory investigation of the effect of sodium silicate and bentonite on the mechanical properties of the Grout behind the segment in mechanized excavation. Rudarsko-geološko-naftni Zbornik . 39 (2), 63-74.  h t t p s : / / d oi . o r g / 1 0 . 17 7 9 4 / r g n . 2 0 2 4 . 2 . 5  (2024).
5.  Mousapour, H., Chakeri, H., Darbor, M. &amp; Hekmatnejad, A. Evaluating the wear of cutting tools using a tunnel boring machine laboratory simulator. Min. Mineral. Deposits . 17 (2), 28-34. https://doi.org/10.33271/mining17.02.028 (2023).
6.  Rostami, A., Chakeri, H., Shahriar, K. &amp; Seifabad, M. C. Subsidence prediction for twin tunnels using genetic algorithms-case study: Isfahan, Iran. Rudarsko-geološko-naftni Zbornik . 40 (4), 57-76. https://doi.org/10.17794/rgn.2025.4.5 (2025).
7.  Azad,  H.,  Chakeri,  H.  &amp;  Shakeri,  H.  Assessment  of  Ground  Surface  Settlement  and  Excavation  Volume  Loss  in  Mechanized Tunneling Using Field Data and Numerical Modelling: A Case Study of Tabriz Metro Line 2. Journal of Mining and Environment. https://doi.org/10.22044/jme.2025.16120.3113 (2025a).
8.  Huang, Z. K., Zeng, N. C., Zhang, D. M., Argyroudis, S. &amp; Mitoulis, S. A. Resilience Models for tunnels recovery after earthquakes. Engineering https://doi.org/10.1016/j.eng.2025.06.028 (2025).
9.  Rostami, A. H. Subway Excavation method Selection by Multi-Criteria Decision Making Method-Case study: Tehran Subway Line 3 Phase 4 M.Sc. Unpublished, M.Sc. Thesis in Mining Engineering. Research and Science Branch, Faculty of Mining Engineering, Islamic Azad University. (2011).
10.  Haghshenas, S. S. et al. Selection of an appropriate tunnel boring machine using TOPSIS-FDAHP method (Case study: line 7 of Tehran Subway, East-West Section). Electron. J. Geotech. Eng. 22 , 4047-4062 (2017).
11.  Hassan, B. A. et al. Selection of a subway excavation method using AHP and TOPSIS. Geosciences 29 (116), 121-124.  h t t p s : / / d o i . o r g / 1 0 . 2 2 0 7 1 / g s j . 2 0 1 9 . 9 9 0 8 8 . 1 2 6 5  (2020).
12.  Wu, B. et al. A case study on the construction optimization decision scheme of urban subway tunnel based on the TOPSIS method. KSCE J. Civ. Eng. 24 (11), 3488-3500. https://doi.org/10.1007/s12205-020-1290-9 (2020).
13.  Koohathongsumrit, N. &amp; Chankham, W. Risk analysis of underground tunnel construction with tunnel boring machine by using fault tree analysis and fuzzy analytic hierarchy process. Safety 10 (3), 68. https://doi.org/10.3390/safety10030068 (2024).
14.  Tan, Z. et al. Research on the tunnel boring machine selection decision-making model based on the fuzzy evaluation method. Appl. Sci. 12 (21), 10802. https://doi.org/10.3390/app122110802 (2022).
15.  Mahmut Yavuz The optimum support design selection by using AHP method for the main haulage road in WLC Tuncbilek colliery. Tunn. Undergr. Space Technol. 23 , 111-119. https://doi.org/10.21203/rs.3.rs-7793264/v1 (2008).
16.  Bangian, A. H., Ataei, M., Sayadi, A. &amp; Gholinejad, A. Optimizing post-mining land use for pit area in open-pit mining using fuzzy decision-making method. International J. Environ. Sci. And Technol. 9 (4), 613-628. https://doi.org/10.1007/s13762-012-0047-5 (2012).
17.  Nezarat, H., Sereshki, F. &amp; Ataei, M. Ranking of geological risks in mechanized tunneling by using fuzzy analytical hierarchy process (FAHP). Tunn. Undergr. Space Technol. 50 , 358-364. https://doi.org/10.1016/j.tust.2015.07.019 (2015).
18.  Baloyi, V . D. &amp; Meyer, L. D. The development of a mining method selection model through a detailed assessment of multi-criteria decision methods. Results Eng. 8 , 100172. https://doi.org/10.1016/j.rineng.2020.100172 (2020).
19.  Genger, T. K., Luo, Y. &amp; Hammad, A. Multi-criteria Spatial analysis for location selection of multi-purpose utility tunnels. Tunn. Undergr. Space Technol. 115 , 104073. https://doi.org/10.1016/j.tust.2021.104073 (2021).
20.  Zhu, X., Meng, X. &amp; Zhang, M. Application of multiple criteria decision making methods in construction: A systematic literature review. J. Civil Eng. Manage. 27 (6), 372-403. https://doi.org/10.3846/jcem.2021.15260 (2021).
21.  Li, K. et al. AHP-FSE-Based risk assessment and mitigation for slurry balancing shield tunnel construction. J.  Environ. Public. Health . 2022 (1), 1666950. https://doi.org/10.1155/2022/1666950 (2022).
22.  Zhang,  L.  &amp;  Chen,  W .  Multi-criteria  group  decision-making  with  cloud  model  and  TOPSIS  for  alternative  selection  under uncertainty. Soft. Comput. 26 (22), 12509-12529. https://doi.org/10.1007/s00500-022-07189-3 (2022).
23.  Yang, C. et al. Evaluation of excavation ergonomics of drill and blast method based on game theory G2-EW-TOPSIS model. Appl. Sci. 13 (12), 7205. https://doi.org/10.3390/app13127205 (2023).
24.  Kong, H. Q. &amp; Zhang, N. Risk assessment of water inrush accident during tunnel construction based on FAHP-I-TOPSIS. J. Clean. Prod. 449 , 141744. https://doi.org/10.1016/j.jclepro.2024.141744 (2024).
25.  Zhang, Y., Zhang, Y., Song, Z. &amp; Pan, H. A LFPP-FAHP based evaluation model of blasting scheme for tunnel undercrossing existing buildings. Tunn. Undergr. Space Technol. 153 , 105937. https://doi.org/10.1016/j.tust.2024.105937 (2024).
26.  Jia,  C.  et  al.  Real-Time  assessment study of individual thermal stress in high-temperature tunnel based on integrated weightTOPSIS model. Tunn. Undergr. Space Technol. 162 , 106614. https://doi.org/10.1016/j.tust.2025.106614 (2025).
27.  Expert choice, I. Expert choice software, version 11.1.328. (01/03/10) www.expertchoice.com (2010).
28.  Saaty, T. L. The Analytic Hierarchy Process . 83-98. (Springer, 2022).
29.  Daisuke Maeda, T., Namatame, Yamaguchi, T. For Group Decision Making With Opinion Modifying Process. Bali 7th ISAHP Indonesia, 305-314. https://doi.org/10.13033/isahp.y2003.004 (2003).
30.  Hwang, C. L. &amp; Yoon, K. P . Multiple attribute decision making. In Methods and Application (Springer, 1981).  h t t p s : / / d o i . o r g / 1 0 . 1 0 07 / 9 7 8 - 3 - 6 4 2 - 4 8 3 1 8 - 9 .
31.  Building and Housing Research Center (BHRC). Iranian Code of Practice for Seismic Resistant Design of Buildings: Standard No. 2800 3rd edn (BHRC, 2007).

## Author contributions

Conceptualization, A.R., H.Ch.; Methodology, A.R., H.Ch.; Software, H.Ch., K.SH.; Validation, K.SH.; Formal analysis, A.R., H.Ch., K.SH.; Investigation, K.SH., H.M.; Resources, K.SH., H.M.; Data curation, K.SH.; Writing-original draft preparation, A.R., H.M.; Writing-review and editing, A.R., H.M.; Visualization, A.R., H.M.;

Supervision, A.R., H.Ch.; Project administration, A.R., H.Ch.; Funding acquisition, No funding. All authors have read and agreed to the published version of the manuscript.

## Declarations

## Competing interests

The authors declare no competing interests.

## Additional information

Correspondence and requests for materials should be addressed to A.R.

Reprints and permissions information is available at www.nature.com/reprints.

Publisher's note Springer Nature remains neutral with regard to jurisdictional claims in published maps and institutional affiliations.

Open Access This article is licensed under a Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License, which permits any non-commercial use, sharing, distribution and reproduction in any medium or format, as long as you give appropriate credit to the original author(s) and the source, provide a link to the Creative Commons licence, and indicate if you modified the licensed material. You do not have permission under this licence to share adapted material derived from this article or parts of it. The images or other third party material in this article are included in the article's Creative Commons licence, unless indicated otherwise in a credit line to the material. If material is not included in the article's Creative Commons licence and your intended use is not permitted by statutory regulation or exceeds the permitted use, you will need to obtain permission directly from the copyright holder. To view a copy of this licence, visit  h t t p : / / c r e a t i v e c o m m o ns . o r g / l i c e n s e s / b y - n c - n d / 4 . 0/ .

© The Author(s) 2025
<!-- image -->

Logo

Article

## ATheoretical Study on the Resilience Evaluation Method of Operational Road Tunnel Systems

Chongbang Xu 1 , Hongchuan Hu 1, * and Hao Wang 2

- 1 Research Institute of Highway Ministry of Transport, Beijing 100088, China
- 2 Shanxi Xixian New Area Urban Construction Investment Group Co., Ltd., Xi'an 712000, China
* Correspondence: 222210036@seu.edu.cn

Abstract: Road tunnel operation will suffer from a lot of uncertain external disturbances, which will greatly affect the operational safety of road tunnels and even block traffic. Focusing on road tunnel operation safety and disaster-resistant ability, the concept of resilience is introduced to provide a scientific and effective basis for road tunnel operation and emergency management. In this paper, the concept of tunnel system resilience was proposed based on the concept of system resilience. A theoretical analysis model of road tunnel resilience was built to describe the change in road tunnel system function over time due to external disturbances (e.g., fires, traffic accidents, floods, earthquakes). Five fundamental attributes of road tunnel system resilience were proposed to describe the resilience level. A resilience evaluation method for road tunnels was proposed based on the functional network. The vulnerable links of road tunnels subjected to external disturbances can be analyzed using this method. This study will provide important references for the resilience evaluation method of road tunnels and risk mitigation strategies.

Keywords: road tunnel system; resilience; resilience evaluation model; resilience evaluation method

## 1. Introduction

The 2022 China statistical bulletin on the development of the transport industry [1] shows that China has built 24,850 road tunnels. In particular, the emergence of numerous subaqueous tunnels has led to more attention on the operation security of road tunnels in China [2]. The factors affecting road tunnel operation safety can be divided into external disturbance events and system self-functional status. For external disturbance events, transport infrastructures are facing a sudden increase in the frequency and intensity of extreme climate due to the change in global climate in the 21st century. Excessive vehicles beyond the design consideration will greatly affect the traffic capability of road tunnels and increase operational security risks. The technical condition of long-term operating road tunnels is generally at a low level due to the occurrence of numerous structural diseases and low operational management capability. These tunnels exhibit poor resistance and recovery when facing the effects of external disturbance events. So, it is necessary to grasp the functional state of road tunnels and improve their operational ability to deal with external disturbances.

The emergence of the concept of system resilience provides a new perspective for systems engineering to cope with external disturbances. The aim of this study was to build a theoretical evaluation framework for road tunnel resilience. The basic concept of road operating tunnel resilience will be discussed in detail, and an evaluation model will be proposed to describe the functional change in road tunnels that are subjected to external disturbances. Finally, one method based on functional networks will be established to evaluate the resilience of road tunnels. It is expected to analyze the critical function nodes and paths that affect road tunnel function under external disturbance conditions.

<!-- image -->

Logo

Citation: Xu, C.; Hu, H.; Wang, H. A Theoretical Study on the Resilience Evaluation Method of Operational Road Tunnel Systems. Appl. Sci. 2023 , 13 , 13279. https://doi.org/ 10.3390/app132413279

Academic Editors: Eugene J. Obrien and Giuseppe Lacidogna

Received: 28 April 2023 Revised: 8 October 2023 Accepted: 28 November 2023 Published: 15 December 2023

<!-- image -->

Icon

Copyright: © 2023 by the authors. Licensee MDPI, Basel, Switzerland. This article is an open access article distributed under the terms and conditions of the Creative Commons Attribution (CC BY) license (https:// creativecommons.org/licenses/by/ 4.0/).

<!-- image -->

Logo

## 2. Literature Review

Over the past few years, resilience has become a focal topic for transport infrastructure systems. As an important transportation infrastructure, road tunnels have been studied in depth by a large number of scholars.

Valletta et al. [3] presented a detailed analysis and summary of the Port Authority of New York and New Jersey's pilot program for resilience management methodologies, which was applied to the Holland tunnel and the Port Authority Bus Terminal to evaluate their resilience to Superstorm Sandy-like flood hazards. The purpose of the pilot program was to solve the problem of resource allocation of critical infrastructure assets.

Alderson et al. [4] used the defend-attacker-defender model to research the operational resilience of regional transportation systems. They utilized the major highway roads, bridges, and tunnels of the San Francisco Bay area as nodes to build a transportation network. This network was used to investigate the resilience to worst-case losses.

Wang et al. [5] proposed the concept of surrounding rock resilience of subway tunnels to effectively deal with the problem of instability of surrounding rock structures. They summarized the influencing factors of surrounding rock resilience of subway tunnels, including design, construction, and surrounding rock attributes, formed a surrounding rock resilience evaluation model with eight representative factors as the main evaluation indexes, and proposed an evaluation method of surrounding rock resilience of subway tunnels based on the Euclidean distance method.

Zhang et al. [6] proposed the concepts of emergency resilience and the resilience ring by analyzing tunnel fire cases combined with existing resilience theories. They made a detailed analysis of the linkage operation mechanism of each tunnel subsystem during the whole process of fire occurrence and provided new ideas for tunnel disaster prevention and mitigation.

Khetwal S et al. [7] believed that tunnel resilience had a great impact on the traffic efficiency of the road network. They proposed an ideal data collection framework to calculate the functional level value of road tunnels and then used data analysis to seek the relationship between tunnel design, operation, and tunnel resilience.

Wei et al. [8] put forward the concept of tunnel construction safety resilience. Taking resistance, adaptability, and resilience as the main aspects of construction resilience evaluation and fully considering the tunnel structure, geological conditions, emergency management, and other factors, they built a construction resilience evaluation model with nine representative factors as the main evaluation indexes. Based on the ideal fuzzy matterelement evaluation method, they proposed the weight of a specific evaluation index and the resilience grade of tunnel construction safety.

Zhao et al. [9] built a resilience evaluation index system for tunnel construction emergency management, including 26 indexes. Using the order relation analysis method and the entropy weight method, the index weight was determined using the weighted average method, which effectively reduced the subjectivity of the evaluation.

Zheng et al. [10] divided the engineering structure resilience design into four levels: single safety factor design, reliability design, robustness design, and restorability design. They summarized and analyzed the research progress in geotechnical and underground engineering fields in the above four levels. This research provides a reference for the resilience design theory and framework construction of geotechnical and underground engineering.

Chen et al. [11] proposed the idea of constructing an intelligent shield tunnel construction system based on the resilience theory to realize the intelligent shield tunnel construction in a resilient city. Their main idea was to use the resilience of materials and structure, combined with advanced intelligent technology, in order to realize the intelligent construction of the shield tunnel in a resilient city.

Lin et al. [12] established the tunnel structure resilience analysis model under multiple disturbances, proposed the tunnel structure resilience evaluation index under different typical working conditions, combined with the structural safety control index value given in relevant specifications, and constructed the tunnel structure resilience classification standard.

Caliendo et al. [13] developed a computational fluid dynamics model to analyze user safety and resilience simultaneously. The relationship between the resilience index and the expected value of risk under different scenarios was studied to serve as a reference in the choice of the most appropriate strategy for the recovery of the system function.

Caliendo et al. [14] assessed the resilience of a twin-tube motorway tunnel in the event of a traffic accident or a fire occurring within a tube using simulation. They conducted a simulation analysis of various traffic disruption scenarios and proposed several measures to improve the recovery efficiency of tunnel functions.

To sum up, numerous existing research studies on tunnel resilience focus on operating road tunnels. The main application scenarios mainly include fire and traffic accidents. There are also some studies about tunnel design, construction, and structure in China. The concept of resilience describes the ability of the system to respond to external disturbances. The external disturbances faced by the tunnel include, but are not limited to, fire and traffic accidents. The existing research cannot reflect the randomness of the influence of various external disturbances. So, it is necessary to build a theoretical evaluation framework including various external disturbances that road tunnels are subjected to.

## 3. Basic Concept of Road Tunnel Resilience

## 3.1. Resilience

The concept of resilience first appeared in the field of engineering [15]. Similar to the concept of elasticity, it is used to describe the ability of a single structural member or a certain material to deform and return to the initial state under external force conditions [16]. Since then, the concept of resilience has been introduced into ecology [17], sociology [18], psychology [19], and many other fields. Gradually, it formed a set of independent concept systems, which were used to describe the ability of complex systems to decline and restore to their original functional state or maintain a certain functional level when subjected to external disturbances. After half a century of evolution, the concept of resilience has experienced three stages of development [15]: engineering resilience, ecological resilience, and social-ecological resilience. Its connotation has been gradually enriched and improved, and it has formed four R basic resilience characteristics [20]: robustness, rapidity, redundancy, and resourcefulness. The meaning of the resilience attributes is shown in Table 1.

Table 1. The table of resilience 4R basic attributes.

| Basic Attributes of Resilience   | Interpretation                                                                                                                                                                                                                                                                                                                                                                       |
|----------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Robustness                       | Strength or the ability of elements, systems, and other units of analysis to withstand a given level of stress or demand without suffering degradation or loss of function.                                                                                                                                                                                                          |
| Rapidity                         | The capacity to meet priorities and achieve goals in a timely manner in order to contain losses and avoid future disruption.                                                                                                                                                                                                                                                         |
| Redundancy                       | The extent to which elements, systems, or other units of analysis exist that are substitutable, i.e., capable of satisfying functional requirements in the event of disruption, degradation, or loss of functionality. The capacity to identify problems, establish priorities, and mobilize resources when conditions exist that threaten to disrupt some element, system, or other |
| Resourcefulness                  | unit of analysis; resourcefulness can be further conceptualized as consisting of the ability to apply material (i.e., monetary, physical, technological, and informational) and human resources to meet established priorities and achieve goals.                                                                                                                                    |

The concept of resilience mainly describes the process of the system resisting external disturbances and recovering. Four main elements can be extracted in this process:

- (1) External disturbances.
- (2) System function.

4 of 13 The concept of resilience mainly describes the process of the system resisting external disturbances and recovering. Four main elements can be extracted in this process:

- (1) External disturbances.
- (2) System function.
- (4) Recovery ability. (4) Recovery ability.
- (3) Resistant ability. (3) Resistant ability.

In the conceptual system of resilience, 'system' and 'external disturbance' are two main elements in the process. Among them, 'system' is the main carrier to withstand 'external disturbance'. The appearance of 'external disturbances' will affect the 'system function' and reduce the operating level of the system. 'Resistance' and 'recovery' are the coping abilities of the system after suffering 'external disturbance'. The relationship between the four elements can be described as shown in Figure 1. In the conceptual system of resilience, 'system' and 'external disturbance' are two main elements in the process. Among them, 'system' is the main carrier to withstand 'external disturbance'. The appearance of 'external disturbances' will affect the 'system function' and reduce the operating level of the system. 'Resistance' and 'recovery' are the coping abilities of the system after suffering 'external disturbance'. The relationship between the four elements can be described as shown in Figure 1.

Figure 1. The relationship diagram of resilience concept keyword. Figure 1. The relationship diagram of resilience concept keyword.

<!-- image -->

Flow chart

## 3.2. Road Tunnel System Resilience 3.2. Road Tunnel System Resilience

Based on the concept of resilience, road tunnel system resilience can be defined as the ability of a road tunnel system to resist the influence it is subjected to by external dis - turbances, maintain a certain level of operation, and restore to normal quickly. In this def - inition, four key points need to be discussed: Based on the concept of resilience, road tunnel system resilience can be defined as the ability of a road tunnel system to resist the influence it is subjected to by external disturbances, maintain a certain level of operation, and restore to normal quickly. In this definition, four key points need to be discussed:

- (1) What is the function of a road tunnel system? (1) What is the function of a road tunnel system?
- (3) What are the external disturbances faced by road tunnel systems? (3) What are the external disturbances faced by road tunnel systems?
- (2) What is a road tunnel system? (2) What is a road tunnel system?
- (4) What is the research content of road tunnel resilience? (4) What is the research content of road tunnel resilience?

Secondly, the realization of the basic functions of road tunnels not only depends on the existing basic structure and facilities but also on various operating systems, manage - ment mechanisms, and resource allocation to ensure the safe operation of road tunnels. Secondly, the realization of the basic functions of road tunnels not only depends on the existing basic structure and facilities but also on various operating systems, management mechanisms, and resource allocation to ensure the safe operation of road tunnels. So, the road tunnel system can be divided into two systems: the road tunnel infrastructure system and the road tunnel auxiliary function system. The compositions of the two systems are shown in Figure 2.

Firstly, as a transportation infrastructure, the most basic function of a road tunnel system is to achieve safe, unobstructed, and comfortable transportation. So, the core of the road tunnel system resilience concept will be considered the degree of influence of exter - nal disturbances on the traffic capacity of a road tunnel. Firstly, as a transportation infrastructure, the most basic function of a road tunnel system is to achieve safe, unobstructed, and comfortable transportation. So, the core of the road tunnel system resilience concept will be considered the degree of influence of external disturbances on the traffic capacity of a road tunnel.

Appl. Sci. 2023 , 13 , 13279

5 of 13 So, the road tunnel system can be divided into two systems: the road tunnel infrastructure system and the road tunnel auxiliary function system. The compositions of the two sys - tems are shown in Figure 2. So, the road tunnel system can be divided into two systems: the road tunnel infrastructure system and the road tunnel auxiliary function system. The compositions of the two sys - tems are shown in Figure 2.

Figure 2. Classification diagram of a road tunnel system. Figure 2. Classification diagram of a road tunnel system. Figure 2. Classification diagram of a road tunnel system.

<!-- image -->

Flow chart

Thirdly, 'external disturbance' in the concept system of resilience refer to the uncer - tain events that will have a great impact on the system. For the road tunnel system, 'ex - ternal disturbance' should be the potential major risk events during road tunnel opera - tion. These risk events are mainly characterized using suddenness, uncertainty, linkage, and coupling, which will greatly affect the structural safety and traffic capacity of the road tunnel. So, the 'external disturbances' to road tunnels can be divided into natural disaster events and emergency events, as shown in Figure 3. Thirdly, 'external disturbance' in the concept system of resilience refer to the uncertain events that will have a great impact on the system. For the road tunnel system, 'external disturbance' should be the potential major risk events during road tunnel operation. These risk events are mainly characterized using suddenness, uncertainty, linkage, and coupling, which will greatly affect the structural safety and traffic capacity of the road tunnel. So, the 'external disturbances' to road tunnels can be divided into natural disaster events and emergency events, as shown in Figure 3. Thirdly, 'external disturbance' in the concept system of resilience refer to the uncer - tain events that will have a great impact on the system. For the road tunnel system, 'ex - ternal disturbance' should be the potential major risk events during road tunnel opera - tion. These risk events are mainly characterized using suddenness, uncertainty, linkage, and coupling, which will greatly affect the structural safety and traffic capacity of the road tunnel. So, the 'external disturbances' to road tunnels can be divided into natural disaster events and emergency events, as shown in Figure 3.

Figure 3. Classification diagram of 'external disturbance' in the road tunnel. Figure 3. Classification diagram of 'external disturbance' in the road tunnel. Figure 3. Classification diagram of 'external disturbance' in the road tunnel.

<!-- image -->

Flow chart

Finally, according to the concept of road tunnel resilience, the process of a road tunnel

coping with external disturbances can be divided into three stages:

- (1) Functional decline stage.
- (2) Low functional operating stage.

Finally, according to the concept of road tunnel resilience, the process of a road tun - nel coping with external disturbances can be divided into three stages:

- (1) Functional decline stage.
- (2) Low functional operating stage.
- (3) Functional recovery
4. stage.

These three stages mainly describe three aspects of the resilience of road tunnels:

- (3) Functional recovery stage. (1) Degree of function loss of the road tunnel.
2. These three stages mainly describe three aspects of the resilience of road tunnels: (2) Level of low functional operating of the road tunnel.
- (1) Degree of function loss of the road tunnel. (3) Degree of function recovery of the road tunnel.
- (2) Level of low functional operating of the road tunnel. (3) Degree of function recovery of the road tunnel. Among them, the infrastructure system is the most important structural component and facility of road tunnels, as well as the main carrier to deal with 'external disturbance'.

Among them, the infrastructure system is the most important structural component and facility of road tunnels, as well as the main carrier to deal with 'external disturbance'. The auxiliary functional system is the key link to ensure the normal operation of the road The auxiliary functional system is the key link to ensure the normal operation of the road tunnel system, improve disaster prevention ability, and improve functional recovery abil - ity.

tunnel system, improve disaster prevention ability, and improve functional recovery ability. Based on the above analysis of the concept of road tunnel resilience, combined with the concept of the public safety triangle [20], a road tunnel resilience triangle was proposed to specifically describe the relationship between external disturbances, the road tunnel infrastructure system, and the road tunnel auxiliary function system, as shown in Figure 4. Based on the above analysis of the concept of road tunnel resilience, combined with the concept of the public safety triangle [20], a road tunnel resilience triangle was pro - posed to specifically describe the relationship between external disturbances, the road tunnel infrastructure system, and the road tunnel auxiliary function system, as shown in Figure 4.

Figure 4. Road tunnel resilience triangle. Figure 4. Road tunnel resilience triangle.

<!-- image -->

Flow chart

The road tunnel resilience triangle mainly includes the following basic content: The road tunnel resilience triangle mainly includes the following basic content:

- (1) The infrastructure system is affected by external disturbances and absorbs their influence. (1) The infrastructure system is affected by external disturbances and absorbs their influence.
- (2) According to the state of the road tunnel infrastructure system, the road tunnel auxiliary function system should be adjusted in time to ensure the normal oper - ation of the highway tunnel. The auxiliary function system should be adapted for (2) According to the state of the road tunnel infrastructure system, the road tunnel auxiliary function system should be adjusted in time to ensure the normal operation of the highway tunnel. The auxiliary function system should be adapted for the infrastructure system.
3. the infrastructure system. (3) The occurrence of external disturbances will be fed back to the tunnel auxiliary
- (3) The occurrence of external disturbances will be fed back to the tunnel auxiliary function system to trigger an effective response mechanism to achieve the pur - pose of disaster prevention. The tunnel's resistant ability and recovery ability function system to trigger an effective response mechanism to achieve the purpose of disaster prevention. The tunnel's resistant ability and recovery ability will be improved to make the system more resilient via learning and summarizing.
5. will be improved to make the system more resilient via learning and summariz - ing. 3.3. Evaluation Range of Road Tunnel Resilience

3.3. Evaluation Range of Road Tunnel Resilience The concept of resilience is relative to external disturbances. The resilience level of the road tunnel is an intrinsic attribute. This intrinsic attribute can only be motivated when the system is subjected to relatively severe external disturbances. So, the resilience evalu - ation will lose practical significance when the road tunnel is in the area of low external The concept of resilience is relative to external disturbances. The resilience level of the road tunnel is an intrinsic attribute. This intrinsic attribute can only be motivated when the system is subjected to relatively severe external disturbances. So, the resilience evaluation will lose practical significance when the road tunnel is in the area of low external disturbance risk. Of course, this also needs to take into account the importance of the road tunnel itself. Therefore, the resilience evaluation of road tunnels should be targeted at major and important road tunnels, submarine tunnels, tunnel groups, and tunnels in areas with a high risk of external disturbances.

## 4. Theoretical Analysis Model of Road Tunnel Resilience

## 4.1. Introduction of the Model

Based on the concept of resilience, it can be seen that the essence of resilience is a comprehensive ability to resist external disturbances, reflected using system function changes major and important road tunnels, submarine tunnels, tunnel groups, and tunnels in areas with a high risk of external disturbances.

## 4. Theoretical Analysis Model of Road Tunnel Resilience

## 4.1. Introduction of the Model

over time. Therefore, the change in system function over time is used to quantitatively describe the resilience value. Based on the concept of resilience, it can be seen that the essence of resilience is a comprehensive ability to resist external disturbances, reflected using system function changes over time. Therefore, the change in system function over time is used to quanti - tatively describe the resilience value.

Referring to the conceptual model of seismic resilience proposed by Bruneau et al. [21], a theoretical model of road tunnel resilience was proposed, combined with the characteristics of the road tunnel as shown in Figure 5. In order to quantify the resilience of the road tunnel, the following hypotheses are proposed: Referring to the conceptual model of seismic resilience proposed by Bruneau et al. [21], a theoretical model of road tunnel resilience was proposed, combined with the char - acteristics of the road tunnel as shown in Figure 5. In order to quantify the resilience of the road tunnel, the following hypotheses are proposed:

- (1) Before and after the road tunnel system is affected by external disturbances, the change in system function level value is not considered. (1) Before and after the road tunnel system is affected by external disturbances, the change in system function level value is not considered.
- (2) The functional change in the road tunnel system caused by external disturbances is linear. (2) The functional change in the road tunnel system caused by external disturbances is linear.

<!-- image -->

Line chart

Figure 5. Resilience theoretical model of a road tunnel system, where Fbefore is the value of the system function level of the road tunnel before the influence of external disturbance. Fafter is the value of the system function level of the road tunnel after the influence of external disturbances. Frecover is the value of the system function level of the road tunnel after road tunnel system restoration. Fmin is the lowest level of system function when the basic traffic capacity of the road tunnel is satisfied. Δ F is the disaster loss value of the road tunnel system. t 1 is the moment when the road tunnel system suffers from a natural disaster or emergency event. t 2 is the moment when the function of the road tunnel system declines to the lowest value. t 3 is the moment when the function of the road tunnel system begins to recover. t 4 is the moment when the function of the road tunnel system is restored to its normal state. Figure 5. Resilience theoretical model of a road tunnel system, where F before is the value of the system function level of the road tunnel before the influence of external disturbance. F after is the value of the system function level of the road tunnel after the influence of external disturbances. Frecover is the value of the system function level of the road tunnel after road tunnel system restoration. Fmin is the lowest level of system function when the basic traffic capacity of the road tunnel is satisfied. D F is the disaster loss value of the road tunnel system. t1 is the moment when the road tunnel system suffers from a natural disaster or emergency event. t2 is the moment when the function of the road tunnel system declines to the lowest value. t3 is the moment when the function of the road tunnel system begins to recover. t4 is the moment when the function of the road tunnel system is restored to its normal state.

In the theoretical analysis model of road tunnels, the road tunnel system operates at a constant functional level before and after being affected by external disturbances. The three stages of road tunnel resilience proposed in Chapter 2.2 are the AE, EF, and FB seg - ments, as shown in Figure 5. In the AE segment, Δ F is used to describe the degree of dam - age to the system function or the severity of external disturbances. In the EF segment, the response time of the road tunnel system can be described using t 3 - t 2 . It is used to reflect the soundness of the system's response mechanism to external disturbances. Under the In the theoretical analysis model of road tunnels, the road tunnel system operates at a constant functional level before and after being affected by external disturbances. The three stages of road tunnel resilience proposed in Section 3.2 are the AE, EF, and FB segments, as shown in Figure 5. In the AE segment, D F is used to describe the degree of damage to the system function or the severity of external disturbances. In the EF segment, the response time of the road tunnel system can be described using t3 - t 2 . It is used to reflect the soundness of the system's response mechanism to external disturbances. Under the sound emergency response mechanism, the road tunnel system can quickly start an effective emergency decision-making scheme and prevent secondary damage to the system's function. In the FB segment, the recovery time of the road tunnel system function is described using t4 - t3 . In addition, resilience should be an ability of the system within a certain functional state. If the system function exceeds a certain limit, the system can be considered to enter a 'plastic stage' called resilience failure state. Under this state, the road tunnel system should have the following three characteristics:

- (1) The road tunnel system function is basically lost.

Appl. Sci. 2023 , 13 , 13279

functional state. If the system function exceeds a certain limit, the system can be consid - ered to enter a 'plastic stage' called resilience failure state. Under this state, the road tun - nel system should have the following three characteristics:

- (1) The road tunnel system function is basically lost.
- (2) The road tunnel system function is difficult to recover in a short time.
- (3) The cost of road tunnel system function restoration is high.

(2) The road tunnel system function is difficult to recover in a short time. (3) The cost of road tunnel system function restoration is high. For the road tunnel system, Pmin is defined as the system resilience limit, which is For the road tunnel system, Pmin is defined as the system resilience limit, which is used to describe the system function level value when the road tunnel system maintains the most basic traffic capacity.

used to describe the system function level value when the road tunnel system maintains the most basic traffic capacity. From the perspective of resilience, the road tunnel system can predict and forewarn the external disturbance so that it can deal with the influence in advance. The threat of external disturbances to the road tunnel system function will be greatly reduced, and the road tunnel system will show better resilience. Therefore, the road tunnel system function From the perspective of resilience, the road tunnel system can predict and forewarn the external disturbance so that it can deal with the influence in advance. The threat of external disturbances to the road tunnel system function will be greatly reduced, and the road tunnel system will show better resilience. Therefore, the road tunnel system function will exhibit the following characteristics, as shown in Figure 6:

- will exhibit the following characteristics, as shown in Figure 6: (1) Slower decline speed.
- (1) Slower decline speed. (2) Lower disaster damage value.
- (3) Zero response. (3) Zero response.
- (2) Lower disaster damage value.
- (4) Faster recovery speed. (4) Faster recovery speed.

Figure 6. Ideal resilience curve of the road tunnel system, where Δ t is the disaster loss lag time. Figure 6. Ideal resilience curve of the road tunnel system, where D t is the disaster loss lag time.

<!-- image -->

Line chart

## 4.2. Basic Properties of Road Tunnel Resilience 4.2. Basic Properties of Road Tunnel Resilience

Combined with the theoretical analysis model of road tunnel resilience, the resilience level can be described using three aspects: Combined with the theoretical analysis model of road tunnel resilience, the resilience level can be described using three aspects:

- (1) The influence degree of the road tunnel system subjected to external disturbances. (2) The ability of the road tunnel system to respond to external disturbances.
- (1) The influence degree of the road tunnel system subjected to external disturbances.
- (2) The ability of the road tunnel system to respond to external disturbances. (3) Road tunnel system function recovery level.
- (3) Road tunnel system function recovery level. Based on the 4R attributes of resilience, five resilience attributes of road tunnels were

Based on the 4R attributes of resilience, five resilience attributes of road tunnels were proposed to describe the resilience level, as shown in Table 2. proposed to describe the resilience level, as shown in Table 2. Resistibility and responsiveness are used to describe the ability of road tunnel systems to respond to external disturbances. A higher resilience level indicates greater resistance to external disturbances and shorter response times. Adaptability is used to describe the influence degree of the road tunnel system subjected to external disturbances. A higher resilience level indicates a lower impact when subjected to external disturbances. Recuperability and robustness are used to describe the system function recovery level. A higher resilience level indicates shorter recovery times and higher post-disaster functional levels.

8 of 13

Table 2. The table of basic attributes of road tunnel resilience.

| Basic Attributes of Road Tunnel Resilience   | Interpretation                                                                                    |
|----------------------------------------------|---------------------------------------------------------------------------------------------------|
| Resistibility                                | The ability of the road tunnel system to cope with 'external disturbance'                         |
| Adaptability                                 | The ability of the road tunnel system to adapt to 'external disturbance'                          |
| Responsiveness                               | The ability of the road tunnel system to respond to 'external disturbance'                        |
| Recuperability                               | The ability of the road tunnel system function to recover quickly                                 |
| Robustness                                   | The ability of the road tunnel system to recover stability after suffering 'external disturbance' |

## 5. Resilience Evaluation Method of Road Tunnel

## 5.1. Evaluation Method and Indexes

The existing resilience evaluation methods mainly include the index system method and the network analysis method. The index system method is mainly applied to the resilience evaluation of a single system. In the study of urban resilience evaluation, ARUP [22] has developed a framework for assessing urban resilience. The resilience assessment framework mainly divides the indicators into four dimensions: health and wellbeing, economy and society, infrastructure and ecosystem, and leadership and strategy. On this basis, 52 primary indexes and 156 secondary indexes were constructed to evaluate urban resilience. The establishment of the index system can comprehensively analyze the influencing factors of resilience. Zhong [23] constructed the resilience evaluation index system for road tunnel construction. In this index system, the absorptivity resistance, adaptive learning ability, and recovery ability are taken as the first-level evaluation index. The second-level index is the specific system used to realize the above functions; however, in the absence of a large amount of supporting data, index weights and scores tend to be too subjective.

The network analysis method is mainly applied to the resilience evaluation of road networks. Taking the road network in East China as the research object, Sheng [24] established the network topology model using counties and cities as nodes. The key nodes and key sections in the network are identified using computer simulation to evaluate the risk of the road network. The network established in this method is nondirective between nodes. This network analysis method is suitable for systems with multiple explicit nodes. The road tunnel system cannot construct such a nondirective network.

The resilience evaluation method of road tunnels should be oriented to actual needs. If the evaluation only obtains a specific resilience value of highway tunnels, it can only have a general understanding of the resilience state of road tunnels. It cannot identify the pain points and weak links of the system in the prevention process of external disturbances. Such resilience evaluation methods lack practical utility; therefore, the resilience evaluation of road tunnels needs to analyze the critical path in the process of resisting external disturbances in detail, to point out the key nodes and important paths of the system.

In order to meet the needs of the evaluation, a resilience evaluation method of road tunnel systems was constructed by combining the index system method with the network analysis. The five basic attributes of road tunnel resilience proposed in Section 3.2 were taken as primary evaluation indexes. A formula for calculating the subitem resilience value of road tunnels was proposed as follows:

<!-- formula-not-decoded -->

where Ri is the value of road tunnel resilience for a single external disturbance, Rr is the resistibility value, Ra is the adaptability value, Rs is the responsiveness value, Rc is the recuperability value, Rb is the robustness capability value, w r is the resistibility weight, w a Appl. Sci. 2023 , 13 , 13279 10 of 13 resistibility value, Ra is the adaptability value, Rs is the responsiveness value, Rc is the recuperability value, Rb is the robustness capability value, ɷ r is the resistibility weight, ɷ a is the adaptability weight, ɷ s is the responsiveness weight, ɷ c is the recuperability weight, and ɷ b is the robustness weight.

is the adaptability weight, w s is the responsiveness weight, w c is the recuperability weight, and w b is the robustness weight. Each road tunnel subsystem proposed in Section 3.2 is numbered and taken as a node to construct the functional network of the road tunnel system, as shown in Figure 7. In this functional network, directed arrows are used to express the transmission direction of system functions. The resilience index value is obtained by analyzing the system function network. Finally, the key nodes and paths affecting the resilience of the road tunnel can be Each road tunnel subsystem proposed in Section 3.2 is numbered and taken as a node to construct the functional network of the road tunnel system, as shown in Figure 7. In this functional network, directed arrows are used to express the transmission direction of system functions. The resilience index value is obtained by analyzing the system function network. Finally, the key nodes and paths affecting the resilience of the road tunnel can be analyzed in this network.

analyzed in this network.

Figure 7. Functional network diagram of the road tunnel system, where I is the infrastructure system of the road tunnel, and A is the auxiliary function system of the road tunnel. of the road tunnel, and A is the auxiliary function system of the road tunnel.

<!-- image -->

Flow chart

Figure 7. Functional network diagram of the road tunnel system, where I is the infrastructure system 5.2. Overall Resilience of Road Tunnels

5.2. Overall Resilience of Road Tunnels The types, severity, and frequency of external disturbances suffered by different road tunnels are quite different. So, the resilience evaluation of road tunnels should not

The types, severity, and frequency of external disturbances suffered by different road tunnels are quite different. So, the resilience evaluation of road tunnels should not only consider the common requirements but also focus on the differences in operating envi - ronments faced by different road tunnels. Therefore, the overall resilience value should be reflected using the resilience value of the road tunnel in response to different external disturbances, as shown in Figure 8. Furthermore, the following formulas for calculating the road tunnel resilience considering different operating environments are proposed. The weight of external disturbances is determined using the type of external disturbance. It is used to describe the difference in the operating environment faced by road tunnels so that the resilience evaluation is more suitable to the actual situation. only consider the common requirements but also focus on the differences in operating environments faced by different road tunnels. Therefore, the overall resilience value should be reflected using the resilience value of the road tunnel in response to different external disturbances, as shown in Figure 8. Furthermore, the following formulas for calculating the road tunnel resilience considering different operating environments are proposed. The weight of external disturbances is determined using the type of external disturbance. It is used to describe the difference in the operating environment faced by road tunnels so that the resilience evaluation is more suitable to the actual situation. ⎧ ⎪ ⎪ ⎨ ⎪ ⎪ ⎩ R = n i = 1 w i Ri n i = 1 w i = 1

where R is the overall road tunnel resilience value, and w i is the resilience weight value of the road tunnel in response to different external disturbances.

<!-- image -->

Engineering drawing

11 of 13 where R is the overall road tunnel resilience value, and ɷ i is the resilience weight value of the road tunnel in response to different external disturbances.

Figure 8. Resilience evaluation diagram of road tunnel considering different operating environ - ments. Figure 8. Resilience evaluation diagram of road tunnel considering different operating environments.

<!-- image -->

Flow chart

## 6. Conclusions

6. Conclusions This paper provides a summary of the existing research on the resilience of road tun - nels. We analyze the basic elements of resilience. It can be divided into four keywords: system function, external disturbances, resistant ability, and recovery ability. The relation - ship between the four basic elements is described in this paper, and we propose the basic concept of road tunnel system resilience. Based on this concept, we propose the tunnel function system composition and the classification of external disturbances faced by road tunnels. The road tunnel resilience triangle is proposed to describe the relationship be - tween road tunnel systems and external disturbances emphatically. The theoretical anal - ysis model of road tunnel resilience is built to describe the change in road tunnel system function over time due to external disturbances. The ideal resilience curve of road tunnel systems can be used to exhibit a high resilience level, which includes slow speed of func - tional damage, low functional damage, zero response, and fast speed of functional recov - ery. Five basic properties of road tunnel resilience are proposed to describe the resilience level. Furthermore, we propose a resilience evaluation method for road tunnels based on the functional network. This method can show the functional transfer direction through the functional nodes. We can analyze the important functional nodes and paths to find This paper provides a summary of the existing research on the resilience of road tunnels. We analyze the basic elements of resilience. It can be divided into four keywords: system function, external disturbances, resistant ability, and recovery ability. The relationship between the four basic elements is described in this paper, and we propose the basic concept of road tunnel system resilience. Based on this concept, we propose the tunnel function system composition and the classification of external disturbances faced by road tunnels. The road tunnel resilience triangle is proposed to describe the relationship between road tunnel systems and external disturbances emphatically. The theoretical analysis model of road tunnel resilience is built to describe the change in road tunnel system function over time due to external disturbances. The ideal resilience curve of road tunnel systems can be used to exhibit a high resilience level, which includes slow speed of functional damage, low functional damage, zero response, and fast speed of functional recovery. Five basic properties of road tunnel resilience are proposed to describe the resilience level. Furthermore, we propose a resilience evaluation method for road tunnels based on the functional network. This method can show the functional transfer direction through the functional nodes. We can analyze the important functional nodes and paths to find vulnerable links that road tunnel systems are subjected to by external disturbances. Based on the vulnerable links, it can provide a theoretical foundation for capital allocation plans and risk mitigation strategies.

Author Contributions: Conceptualization, C.X. and H.H.; methodology, C.X. and H.H.; software, H.H.; validation, C.X., H.H. and H.W.; formal analysis, H.H.; investigation, H.W.; resources, H.W.; data curation, H.H. and H.W.; writing-original draft preparation, C.X. and H.H.; writing-review and editing, H.H.; visualization, C.X.; supervision, C.X.; project administration, C.X.; funding acquisition, C.X. All authors have read and agreed to the published version of the manuscript.

## References

1. China's Ministry of Transport. Statistical Bulletin on Development of Transport Industry in 2022 ; China Communications News: Beijing, China, 2023.
2. Editorial Department of China Journal of Highway and Transport. A review of academic research on traffic tunnel engineering in China · 2022. China J. Highw. Transp. 2022 , 35 , 1-40.
3. Valletta, M.; Hapij, A.W.; Ettouney, M.M.; Abboud, N.N. Development of the Resilience Management Tool: A Pilot Program at the Port Authority of New York and New Jersey. In Proceedings of the AEI Conference on Birth and Life of the Integrated Building, Milwaukee, WI, USA, 24-27 March 2015; pp. 342-356.
4. Alderson, D.; Brown, G.; Carlyle, W.M.; Wood, R.K. Assessing and Improving the Operational Resilience of a large Highway Infrastructure System to Worst-Case Losses. Transp. Sci. 2017 , 52 , 1012-1034. [CrossRef]
5. Wang, J.; Zhao, F.; He, X.; Wang, B. Resilience Evaluation of Subway Tunnel Surrounding Rock Based on Euclidean Distance. Railw. Stand. Des. 2019 , 63 , 106-111.
6. Zhang, Y.; Yan, Z.; Zhu, H. Study on Emergency Resilience of Tunnel System Based on Dynamic Interaction. Mod. Tunn. Technol. 2019 , 56 , 9-14.
7. Khetwal, S.; Pei, S.; Gutierrez, M. A Data-Driven Approach for Direct Assessment and Analysis of Traffic Tunnel Resilience. In Information Technology in Geo-Engineering ; Springer International Publishing: Cham, Switzerland, 2022; pp. 168-177.
8. Wei, Q.; Liu, J.; Wang, J.; Wang, P. Tunnel Construction Safety Toughness Evaluation Based on Ideal Fuzzy Matter-element. China Saf. Sci. J. 2021 , 31 , 62-68.
9. Zhao, Y.; Ma, W.; Weng, H. Resilience Evaluation of Tunnel Construction Emergency System. J. Civ. Eng. Manag. 2021 , 38 , 167-172.
10. Zheng, G.; Cheng, X.; Zhou, H.; Zhang, T.; Yu, X.; Diao, Y.; Wang, R.; Yi, F.; Zhang, W.; Guo, W. Evaluation and Control of Structural Resilience in Geotechnical and Underground Engineering. China Civ. Eng. J. 2022 , 55 , 1-38.
11. Chen, X.; Yu, Y.; Bao, X.; Cui, H.; Xia, C.; Zhou, H.; Zhu, M. Intelligent Construction of Shield Tunnel Based on Toughness Theory. Mod. Tunn. Technol. 2022 , 59 , 14-28.
12. Lin, X.; Chen, X.; Su, D.; Zhu, M.; Han, K.; Chen, R. A Resilience Evaluation Method for Shield Tunnel Structure Considering Multiple Disturbances and Its Application. Chin. J. Geotech. Eng. 2022 , 44 , 591-601.
13. Caliendo, C.; Genovese, G.; Russo, I. A Simultaneous Analysis of the User Safety and Resilience of a Twin-Tube Road Tunnel. Appl. Sci. 2022 , 12 , 3357. [CrossRef]
14. Caliendo, C.; Russo, I.; Genovese, G. Resilience Assessment of a Twin-Tube Motorway Tunnel in the Event of a Traffic Accident or Fire in a Tube. Appl. Sci. 2022 , 12 , 513. [CrossRef]
15. Shao, Y.; Xu, J. Understanding Urban resilience: A Conceptual Analysis Based on Integrated International Literature Review. Urban Plan. Int. 2015 , 30 , 48-54.
16. Gordon, J.E. Structures ; Penguin Books: Harmondsworth, UK, 1978.
17. Holling, C.S. Resilience and stability of ecological systems. Annu. Rev. Ecol. Syst. 1973 , 4 , 1-23. [CrossRef]
18. Wildavsky, A. Searching for Safety ; Routledge: New York, NY, USA, 1988.
19. Horne, J.F.; Orr, J.E. Assessing behaviors that create resilient organisations. Employ. Relat. Today 1997 , 24 , 29-39.
20. Fan, W.; Liu, Y.; Weng, W. 'Triangle' framework and '4+1' methodology of public safety Technology. Sci. Technol. Rev. 2009 , 27 , 3.
21. Bruneau, M.; Chang, S.E.; Eguchi, R.T.; Lee, G.C.; O'Rourke, T.D.; Reinhorn, A.M.; Shinozuka, M.; Tierney, K.; Wallace, W.A.; von Winterfeldt, D. A framework to quantitatively assess and enhance the seismic resilience of communities. Earthq. Spectra 2003 , 19 , 733-752. [CrossRef]
22. Arup. City Resilience Index: Understanding and Measuring City Resilience ; The Rochefeller Foundation, Arup International Development: London, UK, 2016.

Funding: This research was funded by the pilot tasks for building a strong transportation country of Research Institute of Highway Ministry of Transport: QG2021-1-3-3).

Institutional Review Board Statement: Not applicable.

Informed Consent Statement: Not applicable.

Data Availability Statement: The relevant data are all included in the paper.

Conflicts of Interest: Author Chongbang Xu was employed by the company Research Institute of Highway Ministry of Transport. The remaining authors declare that the research was conducted in the absence of any commercial or financial relationships that could be construed as a potential conflict of interest.

23. Zhong, S. Study on Toughness Evaluation of Highway Tunnel Construction System ; Chongqing Jiaotong University: Chongqing, China, 2021.
24. Sheng, H. An Approach to Analysis and Evaluation of Highway Network Structural Properties for Risk Assessment and Emergency Management ; Beijing Jiaotong University: Beijing, China, 2012.

Disclaimer/Publisher's Note: The statements, opinions and data contained in all publications are solely those of the individual author(s) and contributor(s) and not of MDPI and/or the editor(s). MDPI and/or the editor(s) disclaim responsibility for any injury to people or property resulting from any ideas, methods, instructions or products referred to in the content.
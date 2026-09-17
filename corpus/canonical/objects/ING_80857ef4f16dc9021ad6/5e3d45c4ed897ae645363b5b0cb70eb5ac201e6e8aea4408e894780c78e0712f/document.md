<!-- image -->

Logo

## Abstract

Road tunnel ventilation system is of high non-linearity and uncertainty, and its exact mathematical model is acquired with very difficulty. In order to effectively control road tunnel ventilation system, a combined grey prediction fuzzy control (CGPFC) law is proposed in the paper. The output of this kind of combined controller is formed by combining outputs of the grey prediction fuzzy controller (GPFC) and the traditional fuzzy control law. The grey predictor is realized by discrete GM(1,1) and it is used to predict the system outputs on line in rolling mode. The simulation and experiment for this new fuzzy control law to be applied in road tunnel ventilation system are conducted. The simulation and the practical application show that the effect of this method is better and it also cost less energy compared to the traditional fuzzy control method.

All Rights Reserved © 2015 Universidad Nacional Autónoma de México, Centro de Ciencias Aplicadas y Desarrollo Tecnológico. This is an open access item distributed under the Creative Commons CC License BY-NC-ND 4.0.

Keywords: Grey prediction; Fuzzy control; Tunnel; Compound control; Ventilation system

## 1. Introduction

Road tunnel is a half closed space, and pollutants exhausted from passing vehicles are ejected out with difficulty. Pollutants such as CO, SOx, NOx, seriously threaten peoples' health and affect driving safety in road tunnels. In order to exhaust air pollutants and pump the fresh air into the tunnel, most of tunnels are equipped with mechanical ventilation systems that consume vast electrical energy, especially in large and long tunnels. The ventilation system of road tunnel should keep the visibility index on required level and the pollutants under certain margins meanwhile consuming least electrical power. But to achieve this goal is extremely difficult because of random and chaos factors that existed in the ventilation system of road tunnel. The pollutants are randomly ejected in the tunnel by numerous stochastically passing vehicles. The great attention has been paid on the control for ventilation system of tunnel system.

In order to improve the ventilation efficiency and saving energy, several ventilation control methods have been put forward. Chen (1998) and Karakas (2003) firstly used the fuzzy controller to operate jet fans and to provide a good approach to combine manual operation experiences into automatic ventilation control systems. Chu (2008) used the genetic algorithm to design a fuzzy controller and improved the energy efficiency. Bogdan (2008) added model predictor in the control system to amend the fuzzy controller outputs, accelerated the response speed of the ventilation, and reduced the energy consumptions. Zhang and Jin (2004) proposed the fuzzy-neural network control method, in which the neural network was used to model mathematical model of ventilation for forecasting pollutants. Cha (2006) adopted neural network to predict pollutants in the feed forward ventilation control system.

*Corresponding author.

E-mail address: yhli@buaa.edu.cn (Y. Li).

From the above researches, we can see that fuzzy control method is available in road tunnel ventilation control system. Combining prediction control with the fuzzy controller can further improve the response speed of the ventilation and decrease electrical costs. But in previous ventilation control systems, the forecast methods are often complex, and increase the difficulty of system establishment in practical applications. The grey system theory developed by Deng (1982, 1989, 2002) provides a framework for predicting system responses, and it is easily embedded into control systems. The grey prediction has been successfully utilized in many fields. For example, grey prediction is used to forecast stock prices (Wang, 2002) and Lorenz chaotic system (Zhang, 2004). Lee (2006, 2007) applied grey model to estimate air quality in traffic tunnel, and achieved considerable prediction accuracy. Chen and Li (2010) established the discrete grey model to predict pollutants in road tunnels, and acquired high prediction accuracy. Combined the grey predic-

Disponible en www.sciencedirect.com

## Journal of Applied Research and Technology

Journal of Applied Research and Technology 13 (2015) 313-320

Original

## Combined grey prediction fuzzy control law with application to road tunnel ventilation system

Yunhua Li a,b, *, Lina Ling b , Jiantao Chen b

a School of Mechanical Engineering, North China University of Water Resources and Electric Power, Zhengzhou, China

b School of Automation Science and Engineering, Beihang University, Beijing, China

Received 19 April 2014; accepted 18 August 2014

<!-- image -->

Logo

www.jart.ccadet.unam.mx

tion with fuzzy control (GPFC) algorithm has been successfully implemented in several application. Huang and Huang (1996) proposed the integration of fuzzy and grey modeling methods for plant control. Luo and Chen (2000) integrated grey predictor with fuzzy control for motion control of the tracker. Lian (2005) designed the grey prediction fuzzy controller for constant cutting force in turning and its control performance is better than one of the traditional fuzzy controller. Hernandez-Rosales (2005) developed a discrete PI controller for DC gear motor. Using the microcontroller, Giménez (2014) developed a control system for a Raman Spectrometer. Using the dynamic nonlinear feedback, Lopez Perez and Aguilar-Lopez (2014) studied temperature control of continuous stirred reactor with complex behavior. The road tunnel ventilation has typical grey characteristics, so the grey prediction and fuzzy control scheme should also be suitable for the control of the road ventilation operation.

The rest of the paper is organized as follows. In the next section, the control process of longitudinal ventilation system in road tunnel is introduced and analyzed. In section 3, the structures of GPFC and CGPFC are proposed and their design procedures are discussed. Section 4 is simulation results and efficiency comparisons among traditional fuzzy control, GPFC and GPCFC. Finally, main conclusions are summarized in Section 5.

## 2. Longitudinal ventilation control process in road tunnel

Longitudinal ventilation system in road tunnel is widely used in the transportation road. The longitudinal ventilation is implemented with a system of jet fans, which is intermittently settled at the ceiling above the roadway or is housed in the central ventilation buildings, as shown in Figure 1.

The plant discussed here is a two-way single lane tunnel. The polluted air contaminated by exhausts from passing vehicles is mainly drawn out using jet fans. The jet fan can boost the air flow speed in the tunnel, and let the fresh air absorbed into tunnel in the entrance and pollutant air blew out in the exit. When the pollutant concentrations in the road tunnel air are higher the more jet fans should be started for increasing the air flow speed and exhausting the contaminated air; when the pollutant concentrations are lower, the more jet fans should be shut down for saving energy. The operation of ventilation control system is to start or shutdown the jet fans according to changes of the pollutant concentrations to satisfy ventilation and saving energy to objectives. The pollutants concentrations always fluctuate with varieties of many variants values, such as air flow speed in road tunnel, traffic volume, pollutant emission rates of each vehicle, air temperature, and natural wind speed, etc. It is difficult to establish an exact mathematical model for describing the relationship between pollutant concentrations and many variants. Therefore intelligent control method is always applied to control the operation of jet fans.

Fig. 1. Longitudinal ventilation system in one-dimensional road tunnel.

<!-- image -->

Engineering drawing

## 3. Design of GPFC and CGPFC

## 3.1. Grey prediction fuzzy controller

The composition of the proposed grey prediction and fuzzy controller for the road tunnel ventilation is showed in Figure 2. It consists of a fuzzy controller, a grey predictor, a smooth filter, two P controllers (two quantizer factors) and jet fans controller.

In Figure 2, Rpc is the reference input, and it often is the constant value for the road tunnel ventilation control; is the current output of the pollutant concentrations in the exit section of road tunnel in the k -th control period; is the one-step forward predicted value of the system output; is the difference between and the current reference input; and is the difference between the predict value and the reference value. Both of and are the inputs of fuzzy controller. The N represents the number of the opened jet fans in the k -th control period and it is the output value of the fuzzy controller. The F represents the forces caused by jet fans to push the air moving in the road tunnel, and it is the inner variant of the road tunnel ventilation process. The smooth filter here is to filter noises from the measured signal for improving the predict precision.

The jet fans controller firstly roughly estimates N , here using to note the round result of N , and then chooses of jet fans number whose total running time are shorter and start them. Because the starting of many jet fans at same time may be shatter the electrical power supply networks, so the number of the starting jet fans should be limited. In this study, according to our practical project environment, the number of the starting jet fans in a 10 minutes period is limited to 4.

## 3.2. Grey predictor

Grey predictor is designed based on grey system theory. In the grey system theory, the output of a process is treated as time series values in the 'grey' value within a certain range. The grey prediction is carried out based on accumulated generating operation (AGO) technology and grey model-GM( n,m ) where n denotes the order of the ordinary differential equation and m denotes the number of grey variables. GM(1,1) of GM( n,m ) has been widely successfully used and proved effective and accurate in many fields. Based on GM(1,1), Xie and Liu developed a discrete form of GM(1,1), abbreviated as DGM(1,1). DGM(1,1) is more accurate than GM(1,1) under some conditions and is reasonable to be applied in many discrete control systems (Xie &amp; Liu, 2005). In fact, most of plant control systems are discrete control systems based on industrial computers, e.g., the road tunnel ventilation control system, so here using DGM(1,1) implements the prediction.

<!-- formula-not-decoded -->

Fig. 2. Block diagram of the grey prediction fuzzy control for road tunnel ventilation system.

<!-- image -->

Engineering drawing

The grey prediction employs the data generation method to obtain a regular generating sequence from the past and present known data of the pollutant concentrations in order to predict future data. In this study, four sample points continuously substituted with new detected data are used for prediction (Wang, 2002). These four sample points are collected in a so-called moving short-team data set. The form of moving short-team data set is utilized to forecast the next unknown datum using DGM(1,1). Likewise, the prediction operation repeats for each control period.

The recursion prediction process is as follows (Kayacan, Ulutas &amp; Kaynak, 2010): Let us define a moving data set and is  the  original  sample data at time , ; m denotes the width of the data window in the k -th control period, generally, ; the script k represents the k -th control period, and n denotes the number of control periods. The AGO series of the moving data set is defined as and it can be expressed as

<!-- formula-not-decoded -->

Unlike GM(1,1), DGM(1,1) directly changed the ordinary differential equation to the difference equation, and obtained the following first-order difference equation:

<!-- formula-not-decoded -->

where is  the  forecast  value  of  k-th  AGO  series, is parameter vector, and are dynamic coefficients which are determined in each cycle by least square technique as follows:

<!-- formula-not-decoded -->

According to (2), we can forwardly predict one step to acquire , considering the definition of the AGO series, so that the forecast value can be calculated as:

<!-- formula-not-decoded -->

where is the prediction value at time , and is also the output result of the current prediction cycle. To predict means to obtain at , it is very useful to overcome the great inertia influence. The same prediction process is performed in each control period excluding the three periods in the initialization process.

## 3.3. Fuzzy controller

Fuzzy controller has been successfully applied in the road tunnel ventilations. Generally, a fuzzy controller is a fuzzy logic system with m inputs and n outputs. In our system, the fuzzy controller is a multiple input and single output fuzzy logic system with m = 2 and n = 1, such that the inputs are and and the output is N, illustrated in Figure 2. The fuzzy system consists of three parts, i.e. fuzzification, inference and defuzzification. The fuzzification converts the inputs ( and ) into fuzzy sets, the inference uses fuzzy inference rules from a fuzzy rule-base in order to produce fuzzy conclusions, and the defuzzification converts these fuzzy conclusions into the output ( N ).

## 3.3.1. Fuzzification

Here, the ventilation of Qinling No. 3 tunnel is chosen as the study object and only the CO concentration as the control objective (Chu, 2008). Its allowable CO concentration is 100 ppm and it has 22 jet fans settled at the ceiling above the roadway. So, the region of the input is scaled within [-1 2], the region of the input is scaled within [-2 2], and the region of the output N is within [0 22].

We use , and N to represent real input variables and output variable, and map them into fuzzy sets. According to practical operation experiences, the inputs and are mapped to 7 sets separately noted by NB, NM, NS, Z, PS, PM and PB and their membership functions are showed in Figues 3 and 4. The output of N is mapped into 5 fuzzy sets, i.e. NB, NS, Z, PS, PB, and the membership functions of N are shown in Figure 5.

Fig. 3. Member functions of e(k) .

<!-- image -->

Line chart

Fig. 4. Member functions of ec(k) .

<!-- image -->

Line chart

Fig. 5. Member functions of N .

<!-- image -->

Line chart

## 3.3.2. Fuzzy inference

From the membership functions showed in Figures 3 and 4, the fuzzy values of the inputs can be obtained. Then the control output is induced by the fuzzy inference rules. Table 1 shows the fuzzy inference rules. There are total of 49 fuzzy rules. For example, the rules R1 and R2 are expressed as -R1: If is NB and is NB, then N is NB; and -R2: If is NM and is NB, then N is NB.

The 'Max-Min operation rule' proposed by Mamdani is used in order to infer the fuzzy control outputs. And the outputs of the fuzzy inference rules R1 and R2 are derived as:

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

where is a logical operator, i.e., , and ( or )  is the value of the membership function when the real value of the input is (or ), is the membership function values of the fuzzy controller output N. The final inference result is induced as:

<!-- formula-not-decoded -->

where is a logical operator, i.e., .

## 3.3.3. Defuzzification

It is obvious that RuleOut(N) belongs to a fuzzy set and it can't be directly used as the number of jet fans. Therefore, RuleOut(N) should be transformed into a real value. Here, the 'Center of Weight' method is chosen to defuzzify the RuleOut(N), and the formula is as follows:

<!-- formula-not-decoded -->

Figure 6 depicts the response of the fuzzy controller.

| Table 1 Fuzzy inference rules.   | Table 1 Fuzzy inference rules.   | Table 1 Fuzzy inference rules.   | Table 1 Fuzzy inference rules.   | Table 1 Fuzzy inference rules.   | Table 1 Fuzzy inference rules.   | Table 1 Fuzzy inference rules.   | Table 1 Fuzzy inference rules.   |
|----------------------------------|----------------------------------|----------------------------------|----------------------------------|----------------------------------|----------------------------------|----------------------------------|----------------------------------|
|                                  | NB                               | NM                               | NS                               | Z                                | PS                               | PM                               | PB                               |
| NB                               | NB                               | NB                               | NB                               | NB                               | NS                               | Z                                | PS                               |
| NM                               | NB                               | NB                               | NM                               | NM                               | NS                               | PS                               | PS                               |
| NS                               | NB                               | NM                               | NS                               | NS                               | Z                                | PM                               | PS                               |
| Z                                | NM                               | NS                               | Z                                | Z                                | PS                               | PM                               | PM                               |
| PS                               | NS                               | Z                                | Z                                | PS                               | PM                               | PM                               | PB                               |
| PM                               | Z                                | PS                               | PS                               | PM                               | PM                               | PB                               | PB                               |
| PB                               | PS                               | PM                               | PM                               | PB                               | PB                               | PB                               | PB                               |

Fig. 6. The response of fuzzy controller.

<!-- image -->

Other

## 3.4. Combined grey prediction fuzzy controller

The main characteristic of the feed-forward type road tunnel ventilation control is the added prediction part. In this paper, the grey prediction controller is used as feed-forward predictor to predict the outputs of the ventilation system, and the control system shown as in Figure 2 can also be called as grey-fuzzy control system. Grey-fuzzy control system is characterized by the rapid response speed and good control ability, which has been applied in some progress control and the system which has the request for with high prediction precision.

The grey prediction control is one of the main features of the grey-fuzzy control system, and the predicting quality of the predictor has a great effect on the control performance of the overall system. However, the disadvantage of the GPFC is that, when the fluctuation of the output is a little larger, a relatively large errors might occur for the prediction of the peak or crest with the grey prediction method, and this phenomenon can lead to the relatively wider fluctuation of the output of the whole system, while this problem does not exist in the traditional fuzzy control systems.

Thus, by combining the two kinds of fuzzy control methodologies,  raising  merits  and  restraining  weaknesses,  the performance of the control system will be increased. Here, a combined control system to be called the combined grey prediction fuzzy control (CGPFC for short) is proposed, and the structure of the CGPFC system can been seen in Figure 7, where k 1 and k 2 are combination coefficients, they must satisfy the following condition as:

<!-- formula-not-decoded -->

Usually, the k 1 and k 2 are both set as 0.5, which can be adjusted based on the precision of the prediction. The meanings of other parameters in Figure 7 are same as ones of the former two kinds of control laws: GPFC and fuzzy control.

In the CGPFC, the outputs of the two fuzzy controllers are linearly integrated by the combination coefficients, and this integration can decrease the fluctuation of the system output. In addition, the grey predictor can make a better prediction for the change trends of the output signals than the separated fuzzy control or GPFC.

Fig. 7. The block diagram of response of fuzzy controller used in tunnel ventilation system.

<!-- image -->

Engineering drawing

## 4. Simulation results and analyses

## 4.1. Plant description and parameters selection

Based on the simplified mathematic models to be established by Chen and Li (2011), and the calculation method recommended by the 'Specifications for Design of Ventilation and Lighting of Highway Tunnel' and the latest research results, the simulation models for the road tunnel ventilation system are developed. The parameters of the tunnel structures are acquired from that of Qinling No. 3 tunnel in Xi'an-Hanzhong highway of China, and the relevant parameters are listed in Table 2. Vertical ventilation is adopted in China's Qinling No. 3 tunnel, and the selected jet fan is SDS112T-4P-22, shown in Figure 8. The performance parameters are listed in Table 3.

Table 2 The main parameters of the road tunnel ventilation simulation models.

| Parameters                                         | Value           |
|----------------------------------------------------|-----------------|
| Tunnel length (L)                                  | 5000 m          |
| Tunnel cross-sectional area (A)                    | 70 m 2          |
| Tunnel hydraulic diameter (Dh)                     | 8.5 m           |
| Tunnel inlet loss coefficient e1                   | 0.6             |
| Tunnel wall friction coefficient e2                | 0.02            |
| Proportion of the large vehicle r1                 | 0.3             |
| Front projection area of large vehicle Acl         | 5.37 m 2        |
| Front projection area of small vehicle Acl         | 2.13 m 2        |
| Air resistance coefficient of large vehicle e3     | 1               |
| Air resistance coefficient of small vehicle e4     | 0.5             |
| Tunnel design speed V                              | 80 km/h         |
| The outlet air velocity of jet fan Vj              | 30 m/s          |
| The outlet cross-sectional area of jet fan Aj      | 1 m 2           |
| The friction coefficient of jet fan                | 0.7             |
| The static pressure difference of tunnel outlet ΔP | 20 Pa           |
| The average value of each car's CO emission        | 30 g/km·per car |

Fig. 8. Installed SDS112T-4P-22 jet fans in tunnel.

<!-- image -->

Photograph

Table 3 Specifications of jet fan SDS112T-4P-22.

| Rotational speed    | 1470 r/min   | Flow        | 27.3 m 3 /s   |
|---------------------|--------------|-------------|---------------|
| Outlet air velocity | 27.7 m/s     | Motor power | 22 kW         |
| Axial thrust        | 825 N        | Noise       | 70 dB(A)      |

## 4.2. Setting of transportation flow

In order to compare the control performance of the traditional fuzzy control, GPFC and CGPFC, three kinds of transportation flow conditions of normal (case 1), dense transportation (case 2) and scattered transportation (case 3) have been set here. Based on the test and the observed data, the simulation for three control laws was conducted according to the three transportation flows.

For the first normal case 1, the average transportation flow is approximately 500 cars/h, and the high valves occur during 8:00 to 10:00 AM or 1:00 to 3:00 PM regularly. For the second dense transportation case 2, the average transportation flow is about 750 cars/h, and the high valves often occur on the holidays or caused by some special things such as earthquake relief. For the third scattered transportation case 3, the average transportation flow is about 200 cars/h, and most of the high valves are appeared during 1:00 to 4:00 AM.

## 4.3. Different control performance of the three transportation flow

## 4.3.1. Case of the first type of transportation flow

The selected data of the first transportation flow for 8 h are shown in Figure 9.

Fig. 9. Data of the first transportation flow.

<!-- image -->

Line chart

The simulation results of the three control methods are expressed in the Figures 10 and 11.

As is shown in Figure 10, for the first case, all the three methods can control the CO concentrations blow 80 ppm. However, the overall fluctuation of the CO concentrations is a little larger with the pure fuzzy control method and that changes gently approaching to 80 ppm better with the CGPFC, and the GPFC results in some instabilities and some points exceeding the standards.

According to the Figure 11, the switching frequency of the jet fans is lower when the methods of GPFC and CGPFC are used, compared with the pure fuzzy control, and the change of the working fans number is gently as well.

By calculating the open times of the fans (that is the sum of working fans numbers during every control period), some results can be got as the follow. The total times of fan open is 590 when fuzzy control method is chosen; and that is 518 with GPFC, 72 less compared with the former method, and 12.2% of the power is saved; and that is 525 with CGPFC, 65 less compared with the fuzzy control, and 11% of the power is saved.

## 4.3.2. Case of the second type of transportation flow

The selected data of the second transportation flow for 8 h are shown in Figure 12.

The simulation results of the three control methods are expressed in the Figures 13 and 14.

As is shown in Figure 13, for the second case, all the three methods can control the CO concentrations blow 80 ppm which change gently. It can be seen from Figure 14, most of the jet fans are working in the second condition. By calculating the open times of the fans (that is the sum of working fans numbers during every control period), we can get that the number of working fans is 721 for the three control methods.

Fig. 10. The variation of CO concentrations at the tunnel opening for the first case.

<!-- image -->

Line chart

Fig. 11. The number of working jet fans for case 1.

<!-- image -->

Line chart

## 4.3.3. Case of the third type of transportation flow

The selected data of the third transportation flow for 8 h are shown in Figure 15.

The simulation results of the three control methods are expressed in the Figures 16 and 17.

As shown in Figure 16, for the third case, all the three methods can control the CO concentrations blow 80 ppm generally. However, the change fluctuation is smaller when the CGPFC is used compared with the other two control methods.

According to the Figure 17, the switching frequency of the jet fans and the number of working fans are about the same with the three control methods. By calculating the open times of the fans (that is the sum of working fans numbers during every control period), we can get that the total open times of the fans is 133 with the pure fuzzy control; and that is 132 with the GPFC, 1 time less than the former method, and about 0.7% of the power is saved; and that is 130 with the CGPFC, 3 times less than the pure fuzzy control, and about 2.1% of the power is saved.

Fig. 12. Data of the second transportation flow.

<!-- image -->

Line chart

Fig. 13. The variation of CO concentrations at the tunnel opening for case 2.

<!-- image -->

Line chart

Fig. 14. The number of working jet fans for the second case.

<!-- image -->

Line chart

## 5. Conclusions

In this paper, the characteristics analysis of the gas motion in the road tunnel with vertical ventilation system is carried out. Based on the existing road tunnel fuzzy control methods, a fuzzy control system with the grey prediction fuzzy control model for the vertical ventilation control of the road tunnel is established. A GPFC system and a combined system for the road tunnel are studied, respectively. The grey prediction and fuzzy control structure is established through adding grey prediction part into the traditional fuzzy control system for the road tunnel ventilation. In this control structure, the fuzzy controller deduces the values of control variable based on the system current output and one-step forward prediction output of the system forecasted by the grey predictor. The grey predictor can continuously predict and update the future outputs using current and past outputs of the system based on grey theory.

Fig. 15. Data of the third transportation flow.

<!-- image -->

Line chart

Fig. 16. The variation of CO concentrations at the tunnel opening for the third case.

<!-- image -->

Line chart

Fig. 17. The number of working jet fans for the third case.

<!-- image -->

Bar chart

Taken the Qinling No. 3 tunnel of the western Han dynasty of China as the example, some simulations and comparisons are made for the three ventilation control methods. The analysis results show that the GPFC and the CGPFC make better performance in the aspect of power saving than the traditional fuzzy control, and the CGPFC has a better stability than the GPFC. The fuzzy controller with the grey prediction in the paper not only can be applied in the road tunnel ventilation system, but also can be used in other industrial control projects where the grey prediction method performs well.

## Acknowledgements

This work was supported by the National Key Basic Research Program of China under Grant No. 2014CB046400 and the National Natural Science Foundation of China under Grant No. 51475019, and their financial support is much appreciated.

## References

- Bogdan, S. (2008). Model predictive and fuzzy control of a road tunnel ventilation system. Transportation Research Part C. 16, 574-592.

Chen, P.H. (1998). Application of fuzzy control to a road tunnel ventilation system. Fuzzy Sets Systems, 100, 9-28.

Cha, C.H. (2006). Control of the road tunnel CO density by a feed-forward algorithm. Tunn. Undergr. Space Technol., 21, 298.

Chu, B. (2008). GA-based fuzzy controller design for tunnel ventilation systems. Autom. Constr., 17, 130-136.

Chen, J.T., &amp; Li, Y.H. (2010). Grey difference model to forecast air pollution in road tunnel. J. Grey Syst., 13, 97-104.

Chen, J.T., &amp; Li, Y.H. (2011). Short-period forecasting algorithm for air pollution concentration in road tunnel with longitudinal ventilation. Journal of Beijing University of Aeronautics and Astronautics, 37, 114-118.

Deng, J.L. (1982). Control problems of grey systems. Systems and Control Letters, 1, 288-294.

Deng, J.L. (1989). Introduction to grey system theory. The Journal of Grey System, 1, 1-24.

Deng, J.L. (2002). Grey prediction and grey decision. Wuhan, China: Huazhong University of Science and Technology Press.

Giménez, A.J. (2014). Control system development for a Raman spectrometer using microcontroller. Journal of Applied Research and Technology, 12, 139-144.

Huang, Y.P., &amp; Huang, C.C. (1996). The integration and application of fuzzy and grey modeling methods. Fuzzy Sets Syst., 78, 107-119.

Hernandez-Rosales, C. (2005). A standard microcontroller based discretetime PI for controlling the motion of a DC gear motor. Journal of Applied Research and Technology, 1, 44-52.

Karakas, E. (2003). The control of highway tunnel ventilation using fuzzy logic. Eng Appl Artif Intell., 16, 717-721.

Kayacan, E., Ulutas, B., &amp; Kaynak, O. (2010). Grey system theory-based models in time series prediction. Expert Systems with Applications, 37, 1784-1789.

Lee, C.C. (2006). Estimating air quality in a traffic tunnel using a forecasting combination model. Environ Monit Assess, 112, 327-345.

Lee, C.C. (2007). Modified grey model for estimating traffic tunnel air quality. Environ Monit Assess, 132, 351-364.

Lian, R.J. (2005). A grey prediction fuzzy controller for constant cutting force in turning. Int. J. Mach. Tools Manuf., 45, 1046-1056.

Luo, R.C., &amp; Chen, T.M. (2000). Autonomous mobile target tracking system based on grey-fuzzy control algorithm. IEEE Trans. Ind. Electron., 47, 720-931.

Lopez Perez, P.A., &amp; Aguilar-Lopez, R. (2009). Dynamic nonlinear feedback for temperature control of continuous stirred reactor with complex behavior. Journal of Applied Research and Technology, 7, 202-217.

Wang, Y.F. (2002). Predicting stock price using fuzzy grey prediction system. Expert Systems with Applications, 22, 33-38.

Xie, N.M., &amp; Liu, S.F. (2005). Discrete GM(1,1) and mechanism of grey forecasting model. Systems Engineering Theory and Practice, 1, 93-99.

Zhang, Y.S., &amp; Jin, W.D. (2004). A road tunnel longitudinal ventilation control system based on fuzzy-neural network. Proceedings of the 5th Word Congress on Intelligent Control and Automation, 4, 3570-3574.

Zhang, Y.G. (2009). GM(1,1) grey prediction of Lorenz chaotic system. Chaos, Solitons and Fractals, 42, 1003-1009.
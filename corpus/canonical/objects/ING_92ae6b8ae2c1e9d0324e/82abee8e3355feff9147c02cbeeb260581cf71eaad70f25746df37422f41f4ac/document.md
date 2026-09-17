<!-- image -->

Music

Periodica Polytechnica Civil Engineering, 63(2), pp. 352-361, 2019

## Potentialities of a Highway Alignment Optimization Method in an I-BIM Environment

Nicola Bongiorno 1 , Gaetano Bosurgi 1 , Federico Carbone 1 , Orazio Pellegrino 1 , Giuseppe Sollazzo 1*

- 1 	 Department of Engineering, University of Messina

Vill. S. Agata, C.da di Dio, 98166 Messina, Italy

*  Corresponding author, e-mail: gsollazzo@unime.it

Received: 12 March 2018, Accepted: 30 January 2019, Published online: 12 March 2019

## Abstract

The BIM (Building Information Modeling) approach potential in the civil engineering field opened novel scenarios in the design idea concept, from planning to executive and constructive phases. The related advantages are numerous and not only limited to a realtime interaction among the involved subjects, that can actually operate in an optimized 3D shared environment. Owing to the sharing information philosophy and to the features of various " smart objects " combined in the project, this innovation reduces potential errors and increases the effectiveness of the design solution in terms of both functionality and cost. Despite these advantages, the highway alignment design problem remains very complicated and not easy to solve without appropriate supporting tools. In recent years, several efforts have been spent in defining highway optimization procedures for helping designers in the selection of an optimal solution in compliance with numerous different constraints. Introducing these procedures in a BIM environment may represent a crucial step in the improvement of the highway design procedures, exploiting the full representation and modelling potential of the approach. In this paper, the authors present the advantages of a 3D highway alignment optimization algorithm, based on the Particle Swarm Optimization method, and its possible implementation in a BIM platform. A proper I-BIM environment can exploit the potential of the alignment optimization algorithms, simplifying the analysis of the different solutions, the final representation and the eventual manual modifications.

## Keywords

I-BIM, alignment optimization, artificial intelligence, smart design, highway project

## 1 Introduction

The road alignment design problem is traditionally a very complicated task in infrastructure engineering, due to the several and heterogeneous skills required to the engineers for the analysis. Moreover, a significant amount of time is required for finding an acceptable and proper solution. The complications are generally due to the different aspects and issues  involved  in  the  design  which  define  very  import - ant  constraints  (economical,  environmental,  geometrical, social, etc.) and strictly condition the road alignment.

Since  traditional  approaches  are  too  slow  and  errorprone,  in  recent  years  many  efforts  have  been  made  for developing novel tools and algorithms that can actually support the designers in these delicate tasks. These algorithms - nowadays generally based on Artificial Intelligence (AI) techniques - may analyze and compare thousands and thousands of different solutions, to optimize the alignment and select the best road corridor. These algorithms are also able to define the most appropriate highway geometric character - istics that can minimize costs (not only for construction, but also  management and external costs) and reduce eventual critical situations [1]. Among the various solutions, the most interesting  algorithms  relied  on  the  Genetic  Algorithms (GA) approaches [1-8] or the Swarm Intelligence (SI) meth - ods [9-12] and provided significant and effective results. In general,  all  the  alignment  optimization  approaches  aim  to simplify the design phase by helping the engineers in the road-planning  task  for  reducing  errors  and  inaccuracies, minimizing costs and execution times.

Similar  aims  regard  another  excellent  innovation  that has been interesting the civil engineering field in the last years,  causing  the  so-called  BIM  (Building  Information Modeling) revolution. The BIM is a novel and useful way of thinking, handling, representing, and analyzing the design of any construction object in civil engineering [13]. It rep - resents a shared 3D environment, in which all the subjects involved in the project can operate in parallel, offering their contributions in real-time and simplifying the knowledge sharing [14]. This approach can significantly reduce errors and inaccuracies in the project and increase the efficiency of  the  work-group,  since  the  members  can  immediately update  and  share  all  the  information.  Furthermore,  the entire project is based on a 3D realistic representation of the construction, by means of several specific "smart objects" representing the core element of the BIM environment [15]. These  provide  not  only  an  easy-to-understand  3D  reproduction  of  the  single  elements  and  their  interaction,  but also all the relevant related information that can influence and condition the different project phases (from planning to construction), stored in a complete and large relational database. By analyzing and processing this large amount of data, the most advanced BIM tools can offer support and forecasts in all these phases, simplifying the cost and time estimates and also the working operation organization and scheduling [16, 17]. Then, it is easy to understand that, considering the particular needs of a complex highway design, this kind of solution is strategical and very productive.

In truth, despite the great progress reached in the struc - tural field, the I-BIM (Infrastructure-BIM) tools and envi - ronments  are  nor  adequate  and  developed  enough  for  an exhaustive and significant contribution in the project design and management phases [18]. However, the attention on the topic is high and the progress is continuous and quick.

In this paper, the authors analyze the advantages that can be determined by the implementation of the most modern and efficient alignment optimization procedures in a com - plete and detailed I-BIM environment. As deeply discussed in  the  following  sections,  this  integration  can  exploit  the full potential of both the innovations, since the BIM rela - tional database can directly provide all the needed information for the alignment examination. Moreover, the final sug - gested solutions can be easily represented in 3D in a realistic frame, in which the designers can also easily compare and eventually modify them. In the following sections, first use - ful  notices  regarding  the  BIM  and  I-BIM  approaches  are provided. Then, the authors present a brief literature review on  the  main  highway  alignment  optimization  algorithms and provide general guidelines for the problem modelling. Finally,  the  advantages  of  practically  implementing  these algorithms in I-BIM environments are analyzed and criti - cally discussed.

## 2 BIM and I-BIM

The  BIM  technologies  have  been  introduced  at  the  end of  last  century  in  the  civil  engineering  field.  BIM  can - not only represent a software solution or a specific tech - nical  procedure.  On  the  contrary,  it  defines  a  change  in the  way  of  thinking,  a  novel  approach  to  design,  modelling,  and  management  of  every  civil  engineering  construction [13]. The BIM technologies - made possible by the recent software progress and the modern microprocessor performance [19] - rely on some essential and simple principles, shown in Fig. 1. All these aspects improve the project accuracy and reliability and increase project team efficiency and construction quality, providing advantages for all the involved subjects.

BIM  adoption  in  the  building  design  has  been  rela - tively quick and effective. Even if the approach is in continuous evolution  and  the available solutions are not completely exhaustive, designers and technicians have generally  moved  from  CAD-based  design  approaches  to  the BIM  methodologies.  This  is  essentially  due  to  the  great advantages  produced  by  the  BIM  adoption,  as  it  can  not only actually  reduce  and,  maybe,  avoid  design  inadequacies  or  mistakes  and,  thus,  the  number  of  legal  disputes, but also the time spent for every modification or correction. The BIM produces an overall optimization of the project, since it does not offer advantages to the planning and design phases only, but it can incorporate all design information for  organizing  and  optimizing  all  the  stage  of  the  building lifecycle [20]. Consequently, it is common, nowadays,

Fig. 1 BIM principles

<!-- image -->

Flow chart

|

Fig. 2 BIM dimensions

<!-- image -->

Flow chart

to increase the number of construction representative dimensions from the traditional 3D (for a spatial representation) up to n dimensions [21]. For simplicity, we can list the first 8Ds (Fig. 2), considering:

adaptable  for  I-BIM  projects,  but  attempts  have  been already made for improving this standard or producing new formats strictly related to road modelling [26-29].

- a time model (4 th dimension, for construction activity visualization and analysis);
- a cost model (5 th dimension, for budget analysis and control);
- an  energy  model  (6 th dimension,  for  evaluation  of energy consumptions);
- a  facility  management  model  (7 th dimension,  for management and maintenance organization for the entire life-cycle);
- a safety model (8 th dimension, for checking operators' risks and preventing critical hazardous scenarios).

This  evolution,  relied  on  the  "smart-object"  information included in the BIM relational database, simplifies a complete management of the building, from design, to construction, to the future actual management. Then, it produces significant economical savings and reduces inaccu - racies and critical situations [22]. In detail, for each object, the database contains information regarding all the main internal and external aspects, such as width, height, material, weight, interaction with other objects, etc. This information is collected and stored in specific file formats, of which the IFC (Industry Foundation Classes, developed by  buildingSMART;  [23])  represents  the  current  reference standard for general BIM objects.

However, despite these encouraging innovations, there has not been a parallel and complete development for these solutions  in  the  infrastructure  field.  Concerning  BIM  for infrastructures, the related standardization process and the available solutions are not fully adequate for reliable practical applications [24, 25]. For instance, due to the intrin - sic  differences  in  the  models,  IFC  format  is  not  directly However,  I-BIM  solutions  can  be  generally  used  for realizing the conceptual BIM model of a road infrastruc - ture in a realistic 3D territorial context. In a 'user-friendly' environment, the operator can design the entire alignment by  defining  and  combining  simple  smart  objects,  repre - senting all a complete road section. Each object is actually represented in the 3D model, considering in real-time its interaction with the existing territorial conditions and with the other road elements. At the same time, the operator  can  adjust  and  design  the  vertical  alignment  of  the road by means of simple selections on the object reference points. Model dynamism and flexibility offer many advan - tages in a complex project management, as any modifica - tion in the horizontal alignment, the vertical profile, or the road cross section immediately affect the other representations. Further, I-BIM solutions are strategical for optimiz - ing  collaborations  among  various  groups  of  specialized operators that can in parallel operate on different aspects of the infrastructure (alignment, walls, bridges, hydraulic systems, etc.) in the existing 3D shared model.

Finally, as previously said, each object is not a simple representation of the realistic element in the 3D scenario, but it consists in a list of features that guarantee an exhaustive understanding of the object characteristics, role, interactions, and influence on the external context. This infor - mation,  stored  in  a  relational  database,  can  be  used  for performing any kind of further analysis on the project, in order  to  evidence  inaccuracies  or  optimize  the  design  of specific parts of the construction. Moreover, similarly deep analyses  can  be  performed  for  forecasting  organization and scheduling of the working activities, cost trends, and any kind of further simulations. Naturally, the simulation outcomes can be used for evaluating the efficiency of the project  from  different  point  of  view  and  optimizing  the activity scheduling [30, 31]. As another example, geometrical and topography data can be combined with pluviometry  estimates  for  evaluating  the  road  hydraulic  vulnerability. Further, traffic-simulator tools can also process the road geometry, for checking the influence of the designed road in the infrastructure network. Naturally, implementing these models in the I-BIM tools can improve the method efficiency and reduce the operational times and effort, sim - plifying and optimizing the final solutions.

## 3 Highway alignment optimization problem

Since 1970, many researchers focused on how to simplify and support engineers in the highway alignment definition. After many preliminary attempts by means of several traditional analytical techniques [32-34], the main results have been obtained using AI techniques (in particular, using GA and one SI approach, i.e. the PSO method - Particle Swarm Optimization method). Both GA and PSO represent itera - tive evolutionary approaches and start from some random initial  solutions  that,  after  each  cycle,  are  improved  and corrected to minimize specific cost functions and observe several  constraints.  Their  main  differences  concern  the analytical methods adopted for modifying and optimizing the various solutions. Since GAs consider an evolutionary theory - derived from Darwin's theory on genetic evolution - in which only the best ones survive and reproduce after each cycle, the solutions of each cycle are rearrangements and combinations of the previous ones. The PSO, on the contrary, moves in the search space the different solutions, as it derives from the observation of flocks of birds moving in the space and searching for food.

In  detail,  the  SI  was  introduced  by  Kennedy  and Eberhart [35] and is based on the social interaction typi - cal of particular simple groups of animals that, without a leader and through simple and coordinated behaviors, can perform very complex global tasks. Even if the individuals do not have a real collective awareness, the group is able to achieve exceptional goals.

The hypothesis  of  the  PSO  is  that  each  bird  (particle) does not know the real food position, but only its distance from it; then, it modifies its speed, step by step, and thus its  position,  in  order  to  minimize  this  distance.  Similarly, each  particle  symbolizes  a  possible  solution,  moving  in the space of the solutions, searching for global optimum. Each  particle  changes  its  position  according  to  its  own experience and by imitating other particle movements and

|

experience. The position is evaluated through a specific fit - ness  (or  cost)  function  to  be  maximized  (or  minimized). The  equations  to  calculate  the  position  and  the  speed  of each particle after each iteration depends on some stochastic parameters and the best positions achieved both by the swarm and the generic particle. The methodology can be very  efficient  also  in  terms  of  computational  costs,  espe - cially compared to GA. However, since GA and PSO show different advantages, various papers [10, 36-38] proposed hybrid methods for assuring a more extensive exploration of  the  searching  space  (typical  of  GA)  and  guaranteeing higher  calculation  speed  and  model  convergence  (PSO).

Considering  the  alignment  optimization  problem,  it concerns the choice of an optimum backtracking 3D highway alignment linking two known points in the 3D space in compliance with the various considered constraints. In this context, the optimum solution is the one minimizing the  total  costs,  defined  through  a  proper  cost  function. The position of the vertices defining the alignment may represent the independent variable; then, in a 3D space, each  solution  is  represented  by  3 np independent  variables, where np is  the  number of the internal vertices of the alignment preliminarily fixed.

A  well-defined  and  accurate  Digital  Terrain  Model (DTM) can reproduce the region topography (Fig. 3). In the study region, it is possible to evidence some areas characterized by various constraints (economic, historical, environmental, etc.). In traditional approaches, this characterization may be handled by means of rectangular grids (Fig. 4) easily adaptable to all conditions or through GIS (Geographic Information  Systems)  regions.  Area  information  should include different kind of details related to the actual economical (natural or historical) value of the area, to the soil conditions, and to the environmental hazard (such as seismic, hydraulic, and geo-morphological hazard).

Fig. 3 Example of a DTM representation [12]

<!-- image -->

Other

Fig. 4 Example of grid for zone condition and cost assignment [12]

<!-- image -->

Bar chart

For clarity, the optimization algorithm is divided into various  steps,  as  shown  in  the  flowchart  represented  in Fig. 5. The initial solutions are very essential to solve the problem properly and, in general, there are various alternatives for choosing them. Even if the easier method is a random definition of the several initial solutions for favor - ing a whole exploration of the study area, other methods can avoid loops and critical solutions and, thus, increase the method efficiency [3, 11]. Regarding the vertical align - ment, the algorithm chooses the z coordinate of each vertex. Since an appropriate DTM query provides the ground elevation for each vertex, the algorithm slightly modifies these values, in order not only to maintain as close as possible the road and the ground elevations, but also to define a smooth and correct vertical profile, in compliance with the adopted road standards. Generally, the vertices of the horizontal path can be selected as vertices of the vertical profile also, but the designers can define different criteria according to the project characteristics.

Concerning the radius design for vertical and horizontal alignments, determining random radius values within a given range is a feasible approach, but the values must be checked to assure alignment continuity and avoid intersections between following curves. It is also preferable to main - tain also a certain minimum straight segment (according to the  specific  national  road  standards). The  algorithm obvi - ously can include in the design traditional transition curves (such  as  clothoids),  but  innovative  solutions  can  be  also adopted for increasing users' comfort [12]. Special penalty functions will charge additional costs to improper solutions, in which the difference between following radii is too high or the radius values exceed the Road Standard boundaries.

In general, the cost function to be minimized is the key element of the optimization procedure (Eq. 1). In this case, the total cost of each solution, C T ,  is  the  sum of the real cost, C , and various penalties, P , useful to discard incorrect alignments by increasing the related cost in proportion to the related violation.

<!-- formula-not-decoded -->

where C len is  the  length-dependent  costs, C loc the  location-dependent costs, C E the earthwork costs, P Rmin the minimum radius of circular curves penalty, P R the ratio of following circular curves radii penalty, P ret the minimum and maximum tangent segment length penalty, P G the maximum grade penalty, P Rv the minimum radius of parabolic curves penalty, P dz the  maximum height (depth) of fill (cut) sec - tions penalty, and P E the environmental penalty.

Obviously, the cost function may be adapted to the specific project needs, adding different contributions. Finally, the introduction of particular operators (stochastic or corrective), derived from the GA theory and easily adaptable to the actual project issues, guarantees a rapid convergence and a larger exploration of the search space. The iterative approach reduces the total cost cycle-by-cycle, producing a final solution in compliance with the fixed constraints, by minimizing the cost function (Fig. 6).

## 4 Why implement alignment optimization tools in I-BIM environments?

As discussed,  the  adoption  of  reliable  methodologies  for optimizing highway alignments and supporting operators in the decisional planning phases are significant to improve the road design. On the other side, the I-BIM environment

Fig. 5 Optimization algorithm

<!-- image -->

Flow chart

Fig. 6 Cost function minimization [11]

<!-- image -->

Line chart

(despite its current minimalism and technical limits) may offer numerous advantages in terms of operational simplicity,  interoperability,  quick  modification,  and  exhaustive knowledge of the entire construction ensemble (including the  several  objects  of  the  construction,  the  external  constraints, the territorial scenario, etc.). The consequent step of combining these solutions is crucial and, according to the authors, can improve the planning approaches exploiting potentialities of both the novel methodologies.

The BIM environment seems to be the most appropriate one for developing optimization tools as those described in section  3  (only  for  example,  some  representative  scenarios are developed for test in a specific I-BIM environment, Autodesk ® Infraworks ® ).  First,  the  realistic  and  accurate terrain representation (Fig. 7) can improve the grid or GIS representation generally adopted in the highway optimization algorithms.

The I-BIM flexibility can simplify the analysis of par - allel solutions and the realistic 3D representation (Fig. 8) can  immediately  evidence  the  differences  between  the best  solutions  proposed  by  the  algorithm.  The  operator, by simple clicks on the relevant points of the alignment, is  also  able  to  improve  and  modify  alignment  vertices, changing the smart objects according to different design needs (Fig. 9).

Furthermore,  the  I-BIM  relational  database  can  rep - resent  a  complete  and  exhaustive  source  of  information for evaluating, in detail and with great accuracy, the different  contributions  of  the  cost  function.  Right-of-way costs and soil conditions can be assigned properly to each square meter of the study area, guaranteeing an accurate and reliable evaluation of the external costs. Moreover, the high-resolution  representation  of  the  territorial  morphology can be processed, in combination with other relevant information on seismic and hydraulic exposure, to estimate with great accuracy the environmental risks for each particular alignment.

Fig. 7 Terrain representation in a BIM environment

<!-- image -->

Photograph

Fig. 8 Road alignment representation in a BIM environment

<!-- image -->

Photograph

Fig. 9 Road object information in a BIM environment

<!-- image -->

Screenshot from computer

Fig. 10 Road visualization in a BIM environment

<!-- image -->

Photograph

The I-BIM project dynamism allows the designers to evaluate impact of alignment modifications on all the other related  aspects:  for  example,  this  can  immediately  show how shifting an horizontal vertex and the related curve, for  avoiding  a  particular  area,  may  modify  the  vertical alignment and the earth-work distribution in real-time.

Another  key  aspect  to  not  forget  is  the  possibility to define the project by means of different Levels of Development (LoD; also called Levels of Definition; [39-41]). They are used to classify the progression level of the informational model and affect the measure of the representation  detail  level  for  the  3D  objects.  In  other  words,  their representation  complexity  decreases  as  the  objects  leave the point of view and, consequently, the closer the object, the higher the representation detail (not only in rendering terms, but also in a BIM-related semantic context). In this context, the optimization core may work using low LoD, reducing calculation complexity and increasing rendering efficiency  for  graphical  and  geometric  aspects;  then,  the final optimum alignments can be improved and transformed in objects with higher LoD, for the final highway analyses.

Considering the other road-related civil works (bridges, walls, etc.) the advantages are very remarkable. First, by processing the differences between road and ground elevation, it is possible to include these elements in the cost functions, as a function of the involved heights and lengths. However,  their  representation  and  preliminary  calculation  in  I-BIM  environments  is  simplified  and  very  real - istic (Fig. 10), improving the following tasks of structural calculation  and  design  optimization.  The  main  bridges features (pile number, beam lengths, eventual deep geotechnical supporting structures) can be parametrized and, in parallel, both properly represented in the 3D frame and economically evaluate in the global project. Similarly, also the road pavement can be included accurately in the optimization procedure, considering specific smart objects for its single elements.

Finally, the other project dimensions defined in section 2 may offer another relevant contribution to the alignment optimization. The mole of information (regarding the various aspects previously discussed) stored in the relational database can be extended to the optimization procedure, adding novel terms to the cost function to define a more reliable solution from all the points of view. Then, the road alignment can be optimized through productive considerations regarding construction-area organization and management, workers' safety needs, resource availability and distribution, and construction activity scheduling. If prop - erly tuned, all these aspects can significantly increase the project reliability, the final solution quality, and the eco - nomic margins for all the involved stake-holders.

## 5 Conclusions

In this paper, considering the highway alignment design complexity and the recent development of efficient BIM solutions, the authors have discussed the possible advantages produced by including the most advanced highway alignment optimization algorithms in an I-BIM environ - ment. This combination is expected to increase the quality of the optimization process - and thus the solution - due to  a  more  realistic  representation  of  the  ground  and  the related constraints. Moreover, it also simplifies the repre - sentation of several optimal solutions, easily comparable and manually modifiable by the designer by simple oper - ations on the BIM smart objects. Moreover, the BIM phi - losophy and architecture can simplify the introduction of working-related  problems,  for  defining  objective  func - tions that consider also construction and operational problems.  Since  the  attention  on  I-BIM  has  been  increasing recently, these tools will be developed and improved substantially in the next years; then, the authors believe it is essential to immediately implement these algorithms, for their efficient symbiotic development and practical utiliza - tion. Finally, the authors believe that the BIM philosophy should be extended also to the maintenance management process,  by  defining  a  novel  way  for  representing  road survey  results  and  possible  interventions  as  BIM  smart objects, for a simpler and more immediate representation of the pavement condition and for increasing productivity and reliability of maintenance management.

## Acknowledgement

This  paper  is  independent  of  Autodesk,  Inc.,  and  is  not authorized by, endorsed by, sponsored by, affiliated with, or otherwise approved  by Autodesk, Inc. Autodesk, Infraworks  are  registered  trademarks  or  trademarks  of Autodesk, Inc., and/or its subsidiaries and/or affiliates in the USA and/or other countries.

## References

- [1] Jong, J-C., Jha, M. K., Schonfeld, P. "Preliminary Highway Design with Genetic Algorithms and Geographic Information Systems", Computer-Aided Civil and Infrastructure Engineering, 15(4), pp. 261-271, 2000.

[https://doi.org/10.1111/0885-9507.00190](https://doi.org/10.1111/0885-9507.00190)

- [2] Jong, J-C., Schonfeld, P. "Cost Functions for Optimizing Highway Alignments",  Transportation Research Record: Journal of the Transportation Research Board, 1659(1), pp. 58-67, 1999. https://doi.org/10.3141/1659-08
- [3] Jong, J-C., Schonfeld, P. "An evolutionary model for simultaneously optimizing three-dimensional highway alignments", Transportation Research, Part B: Methodological, 37(2), pp. 107-128, 2003. https://doi.org/10.1016/S0191-2615(01)00047-9
- [4] Jha, M., Schonfeld, P. "Integrating Genetic Algorithms and Geographic Information System to Optimize Highway Alignments", Transportation Research Record, 1719(1), pp. 233-240, 2000. https://doi.org/10.3141/1719-31
- [5] Jha,  M.  K.,  Schonfeld,  P.  "A  highway  alignment  optimization model  using  geographic  information  systems",  Transportation Research, Part A: Policy and Practice, 38(6), pp. 455-481, 2004. https://doi.org/10.1016/j.tra.2004.04.001
- [6] Kim, E., Jha, M. K., Schonfeld, P., Kim, H. S. "Highway Alignment Optimization  Incorporating  Bridges  and  Tunnels",  Journal  of Transportation Engineering, 133(2), pp. 71-81, 2007. https://doi.org/10.1061/(ASCE)0733-947X(2007)133:2(71)
- [7] Maji, A., Jha, M. K. "Multi-objective Highway Alignment Optimization  using  a  Genetic  Algorithm",  Journal  of  Advanced Transportation, 43(4), pp. 481-504, 2009. https://doi.org/10.1002/atr.5670430405
- [8] Kang, M-W., Jha, M. K., Schonfeld, P. "Applicability of highway alignment optimization models", Transportation Research, Part C: Emerging Technologies, 21(1), pp. 257-286, 2012. https://doi.org/10.1016/j.trc.2011.09.006
- [9] Angulo, E., Castillo, E., Garcia-Ròdenas, R., Sànchez-Vizcaìno, J. "Determining Highway Corridors", Journal of Transportation Engineering, 138(5), pp. 557-570, 2012. https://doi.org/10.1061/(ASCE)TE.1943-5436.0000361
- [10] Shafahi, Y., Bagherian, M. "A customized Particle Swarm Method to  solve  highway  alignment  optimization  problem",  ComputerAided Civil and Infrastructure Engineering, 28(1), pp. 52-67, 2013. https://doi.org/10.1111/j.1467-8667.2012.00769.x

- [11] Bosurgi, G., Pellegrino, O., Sollazzo, G. "A PSO Highway Alignment Optimization Algorithm Considering Also Environ-mental Constraints",  Advances  in  Transportation  Studies,  31,  pp.  63-80, 2013. [online]  Available at: https://www.researchgate.net/publication/ 286482741\_A\_PSO\_highway\_alignment\_optimization\_algorithm\_ considering\_environmental\_constraints [Accessed: 05.03.2019]
- [12] Bosurgi,  G.,  Pellegrino,  O.,  Sollazzo,  G.  "A  PSO  algorithm  for designing 3D highway alignments adopting polynomial solutions", presented at Transport Infrastructure and Systems: Proceedings of the AIIT International Congress on Transport Infrastructure and Systems, Rome, Italy, April 10-12, 2017. https://doi.org/10.1201/9781315281896-52
- [13] Bryde,  D.,  Broquetas,  M.,  Volm,  J.  M.  "The  project  benefits  of Building Information Modelling (BIM)", International Journal of Project Management, 31(7), pp. 971-980, 2013. https://doi.org/10.1016/j.ijproman.2012.12.001
- [14] Autodesk "Building Information Modeling", 2002. [online] Available at: http://www.laiserin.com/features/bim/autodesk\_bim.pdf
- [15] Chen,  Sz-Y.,  Lok,  K.,  Jeng,  T.  "Smart  BIM  object  for  design intelligence",  In:  Living  Systems  and  Micro-Utopias:  Towards Continuous  Designing,  Proceedings  of  the  21st  International Conference of the Association for Computer-Aided Architectural Design Research in Asia CAADRIA, Hong Kong, China, 2016. [online]  Available  at: http://papers.cumincad.org/data/works/att/ caadria2016\_457.pdf [Accessed: 05.03.2019]
- [16] Hergunsel, M. F. "Benefits of Building Information Modeling for Construction  Managers  and  BIM  based  scheduling",  MA  Thesis, Worcester Polytechnic Institute, 2011. [online] Available at: https:// web.wpi.edu/Pubs/ETD/Available/etd-042011-135239/unrestricted/ MHergunsel\_Thesis\_BIM.pdf [Accessed: 05.03.2019]
- [17] Shou, W., Wang, J., Wang, X., Chong, H. Y. "A comparative review of Building Information Modeling Implementation in Building and Infrastructures  Industries",  Archives  of  Computational  Methods in Engineering, 22(2), pp. 291-308, 2015. https://doi.org/10.1007/s11831-014-9125-9
- [18] Dell'Acqua, G. "I-BIM Infrastructure-Building Information Modeling: Stato dell'Arte," Le Strade, 1521, 2016. (in Italian)
- [19] Abanda, F.  H.,  Kamsu-Foguem,  B.,  Tah,  J.  H.  M.  "BIM  -  New rules of measurement ontology for construction cost estimation", Engineering Science and Technology, and International Journal, 20(2), pp. 443-459, 2017. https://doi.org/10.1016/j.jestch.2017.01.007
- [20] Marshall-Ponting, A., Lee, A., Wu, S., Aouad, G., Abott, C. et al. "Developing a vision of nD-enabled construction", Construct I.T. Centre  of  Excellence,  University  of  Salford,  Manchester,  Great Britain,  Construct  IT  Report,  2003.  Available  at  https://www. researchgate.net/publication/262910963\_Developing\_a\_vision\_ of\_nD-enabled\_construction [Accessed: 05.03.2019]
- [21] Lee, A., Wu, S., Marshall-Pointing, A. J., Aouad, G., Cooper, R., Tah, J. H. M., Abbott, C., Barrett, P. S. "nD modelling road map: A  vision  for  nD-Enabled  construction",  University  of  Salford, Manchester, Great Britain,  2005. [online] Available  at: http://usir. salford.ac.uk/35972/ [Accessed: 05.03.2019]
- [22] Li,  J.,  Hou,  L.,  Wang,  X.,  Wang,  J.,  Guo,  J.,  Zhang,  S.,  Jiao,  Y. "A  project-based  quantification  of  BIM  benefits",  International Journal of Advanced Robotic Systems, 11(8), 2014. https://doi.org/10.5772/58448
- [23] Liebich,  T.,  Adachi,  Y .,  Forester,  J.,  Hyvarinen,  J.,  Richter,  S., Chipman,  T.,  Weise,  M.,  Wix,  J.  "Industry  Foundation  Classes IFC2xEdition4 Release Candidate 1", BuildingSMART, 2010. [online] Available at: http://www.buildingsmart-tech.org/ifc/IFC2x4/ rc1/html/ [Accessed: 05.03.2019]
- [24] Yabuki, N. "Issues and implementation methods for BIM in the civil infrastructure  domain",  presented  at  Proceedings  of  the  1st  International  Conference  on  Sustainable  Urbanization  (ICSU),  Hong Kong, China, Dec. 15-17, 2010. [online] Available at: http://www. jacic.or.jp/acit/ICSU\_Yabuki\_Presentation.pdf [Accessed: 05.03.2019]
- [25] O'Brien, W. J., Gau, P., Schmeits, C., Goyat, J., Khwaja, N. "Benefits of Three- and Four-Dimensional Computer-Aided Design Model Applications  for Review  of  Constructability",  Transportation Research Record: Journal of the Transportation Research Board, 2268(1), pp. 18-25, 2012.

[https://doi.org/10.3141/2268-03](https://doi.org/10.3141/2268-03)

- [26] Lee, S-H., Kim, B-G. "IFC extension for road structures and digi - tal modelling", Procedia Engineering, 14, pp. 1037-1042, 2011. https://doi.org/10.1016/j.proeng.2011.07.130
- [27] Yabuki, N., Lebeque, E., Gual, J., Shitani, T., Li, Z. "International Collaboration  for  Developing  the  Bridge  Product  Model  "IFCBridge", presented at Proceedings of the International Conference on  Computing  and  Decision  Making  in  Civil  and  Building Engineering,  Montréal, Canada,  14-16,  June, 2006. [online] Available  at: http://itc.scix.net/data/works/att/w78-2006-tf289.pdf [Accessed: 05.03.2019]
- [28] Amann, J., Borrmann, A., Hegemann, F., Jubierre, J., Flurl, M., Koch, C., König, M. "A Refined Product Model for Shield Tunnels Based on a Generalized Approach for Alignment Representation", In:  Proceedings of the ICCBEI 2013, Tokyo, Japan, 2013. pp. 449456. Available at http://www.iccbei.com/AGCEI/ICCBEI2013/ ICCBEI\_2013\_Proceedings\_Web.pdf [Accessed: 05.03.2019]
- [29] Amann, J.,  Singer,  D.,  Borrmann,  A.  "Extension  of  the  upcoming IFC alignment standards with cross sections for road design", presented  at  Proceedings  of  the  ICCBEI  2015,  Tokyo,  Japan, 22-24, April, 2015. Available at https://publications.cms.bgu.tum. de/2015\_Amann\_CrossSections.pdf [Accessed: 05.03.2019]
- [30] Bosurgi,  G.,  Carbone,  F.,  Pellegrino,  O.,  Sollazzo,  G.  "Time Reduction  for  Completion  of  a  Civil  Engineering  Construction Using  Fuzzy  Clustering  Techniques",  Periodica  Polytechnica Transportation Engineering, 45(1), pp. 25-34, 2017. https://doi.org/10.3311/PPtr.9810
- [31] Bosurgi, G., Pellegrino, O., Sollazzo, G. "Project Duration Evaluated Using Affine Arithmetic", Periodica Polytechnica Civil Engineering, 61(3), pp. 412-420, 2017. https://doi.org/10.3311/PPci.8972
- [32] Nicholson, A., Elms, D., Eilliman, A. "A variational approach to optimal route location", Highway Engineers, 23, pp. 22-25, 1976.
- [33] Chew, E. P., Goh, C. J., Fwa, T. F. "Simultaneous optimization of horizontal and vertical alignments for highways", Transportation Research Part B: Methodological, 23(5), pp. 315-329, 1989. https://doi.org/10.1016/0191-2615(89)90008-8
- [34] Cheng,  J-F.,  Lee,  Y.  "Model  for  Three-Dimensional  Highway Alignment", Journal of Transportation Engineering, 132(12), pp. 913-920, 2006. https://doi.org/10.1061/(ASCE)0733-947X(2006)132:12(913)

- [35] Kennedy,  J.,  Eberhart,  R.  "Particle  Swarm  Optimization",  In: Proceedings  of  ICNN'95  -  International  Conference  on  Neural Networks, Perth, WA, Australia, 27 November - 1 December, 1995. https://doi.org/10.1109/ICNN.1995.488968
- [36] Eberharth, R. C., Shi, Y. "Comparison between Genetic Algorithms and Particle Swarm Optimization", In: 7th International Conference, EP98 San Diego, California, USA, 1998, pp. 611-616. https://doi.org/10.1007/BFb0040812
- [37] Thangaraj, R., Pant, M., Abraham, A., Bouvry, P. "Particle swarm optimization:  Hybridization  pespectives  and  experimental  illustrations",  Applied  Mathematics  and  Computations,  217(12),  pp. 5208-5226, 2001.

[https://doi.org/10.1016/j.amc.2010.12.053](https://doi.org/10.1016/j.amc.2010.12.053)

- [38] Juang, C-F. "A hybrid of Genetic Algoritghm and Particle Swarm Optimization for Recurrent Network Design", IEEE Transactions on systems, man and cybernetics - Part B: Cybernetics, 34(2), pp.
2. [997-1006, 2004. https://doi.org/10.1109/TSMCB.2003.818557](https://doi.org/10.1109/TSMCB.2003.818557)
- [39] Gröger, G., Plümer, L. "CityGML interoperable semantic 3D city models", ISPRS Journal of Photogrammetry and Remote Sensing, 71, pp. 12-33, 2012.

[https://doi.org/10.1016/j.isprsjprs.2012.04.004](https://doi.org/10.1016/j.isprsjprs.2012.04.004)

- [40] BIM Forum, "Level of development specification, Version 2013", Association General Contractors, Arlington, Virginia, USA, 2013. [online] Available at: https://bimforum.org/wp-contentuploads/2013/ 08/2013-LOD-Specification.pdf [Accessed: 05.03.2019]
- [41] Cheng, J. C. P., Lu, Q., Deng, Y. "Analytical review and evaluation of  civil  information modeling", Automation in Construction, 67, pp. 31-47, 2016. https://doi.org/10.1016/j.autcon.2016.02.006
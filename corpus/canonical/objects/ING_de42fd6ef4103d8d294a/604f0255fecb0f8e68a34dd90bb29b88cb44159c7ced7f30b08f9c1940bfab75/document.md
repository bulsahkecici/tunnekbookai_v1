## Applications of Particle Swarm Optimization in Geotechnical Engineering:  A Comprehensive Review

M. Hajihassani 1 , D. Jahed Armaghani 2 *, R. Kalatehjari 3

## Abstract

Particle swarm optimization (PSO) is an evolutionary computation approach to solve nonlinear global optimization problems. The PSO idea was made based on simulation of a simplified social system, the graceful but unpredictable choreography of birds flock. This system is initialized with a population of random solutions that are updated during iterations. Over the last few years, PSO has been extensively applied  in  various  geotechnical  engineering  aspects  such  as  slope  stability  analysis,  pile  and foundation  engineering,  rock  and  soil  mechanics,  and  tunneling  and  underground  space  design.  A review  on  the  literature  shows  that  PSO  has  utilized  more  widely  in  geotechnical  engineering compared  with  other  civil  engineering  disciplines.  This  is  due  to  comprehensive  uncertainty  and complexity of problems in geotechnical engineering which can be solved by using the PSO abilities in solving the complex and multi-dimensional problems. This paper is aimed to review the applications of PSO in geotechnical engineering to provide insights into the PSO mechanism for civil engineers.

Keywords: Particle swarm optimization, Civil Engineering, Geotechnical Engineering.

1  Department of Geotechnics and Transportation, Faculty of Civil Engineering, Universiti Teknologi Malaysia, 81310 UTM Skudai, Johor, Malaysia. Email: mohsen\_hajihassani@yahoo.com.

2 * Department of Civil and Environmental Engineering, Amirkabir University of Technology, 15914, Tehran, Iran. Email: danialarmaghani@gmail.com. Tel.: +98 911 1574644 ( Corresponding Author ).

3

Built Environment Engineering Department, Auckland University of Technology, Auckland, New Zealand,

r.kalatehjari@aut.ac.nz

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

29

30

31

32

33

34

35

36

37

38

39

40

41

42

43

44

45

46

47

48

49

50

51

52

53

54

55

56

57

58

59

60

61

62

63

64

65

## 1. Introduction

Swarm  intelligence  (SI)  is  the  collective  behaviour  of  decentralized  systems  composed  of  many individuals that coordinate their activities using self-organization (Cui and Gao, 2012). SI systems are inspired  from  biological  systems  which  are  usually  consisted  of  a  population  of  simple  agents interacting locally with one another and globally with their environment. The ant colonies (Dréo and Siarry, 2002; Dorigo and Blum, 2005), bird flocking (Antoniou et al. ,  2009; Antoniou et al. ,  2013), bee colonies (Karaboga and Basturk, 2007; Karaboga and Basturk, 2008) and fish schooling (Li and Qian, 2003; Neshat et  al. ,  2013) are some example of natural SI systems. Based on these systems, several  optimization  algorithms  such  as  ant  colony,  artificial  bee  colony,  and  PSO  have  been developed. PSO is a powerful population-based computational method that is able to solve a problem by  using  a  population  of  candidate  solutions.  To  improve  a  candidate  solution,  PSO  iteratively relocates the candidates in a search space by employing simple mathematical equations. Compared to other  optimization  algorithms,  PSO  has  many  advantages  such  as  easy  realized,  fast  convergent, promising performance on nonlinear function optimization (Chen et al. , 2011).

Ever since the PSO algorithm has been introduced by Kennedy and Eberhart (Kennedy and Eberhart, 1995; Eberhart and Kennedy, 1995), it has successfully applied in various fields of civil engineering. This  popularity  is  due  to  the  comprehensible  performance  of  PSO  as  well  as  simplicity  of  its operation. Many scholars applied PSO to solve their problems in the fields of structural (Gholizadeh and  Salajegheh  2009;  Poitras et  al., 2011;  Mashhadban et  al. ,  2016),  environmental  (Wan,  2013; Hajihassani et  al. ,  2015; Najafzadeh and Tafarojnoruz, 2016), hydrological (Kuok et  al. ,  2010) and geotechnical  (Sadoghi  Yazdi et  al .,  2011;  Kalatehjari et  al. ,  2014;    Jahed  Armaghani et  al. ,  2014) engineering. The literature reveals that PSO has been applied frequently in geotechnical engineering, in comparison to the other fields of civil engineering. This is mainly because of the uncertain behavior of  rock  and  soil  as  the  main  materials  in  geotechnical  engineering,  in  contrast  with  the  other  civil engineering materials such as concrete and steel. As a powerful optimization technique, PSO has been extensively applied in different geotechnical engineering aspects such as slope stability analysis, pile and foundation engineering, rock and soil mechanics, and tunneling and underground space design.

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

29

30

31

32

33

34

35

36

37

38

39

40

41

42

43

44

45

46

47

48

49

50

51

52

53

54

55

56

57

58

59

60

61

62

63

64

65

In addition to the aforementioned applications, PSO is also used as a learning algorithm in artificial neural networks (ANNs) that are widely used in geotechnical engineering (Jahed Armaghani et  al. , 2014,  Hajihassani et  al .,  2014).  Backpropagation  (BP)  is  the  most  well-known  learning  algorithm which is frequently used as the training algorithm in ANNs. However, BP is a local search learning algorithm  and  therefore  the  optimum  search  process  of  ANNs  might  fail  and  return  unsatisfied solution (Liou et al. , 2009). On the other hand, PSO as a robust global search algorithm, is a suitable alternative to modify weight and bias of ANNs for getting higher performance prediction. Hence, a combination PSO-ANN algorithm receives advantages of  both PSO and ANN to solve/optimize the problems in which PSO searches for global minimum and ANN uses the global minimum to find the best result.

Despite the superiorities of PSO in solving the complex problems, it is occasionally faced with some limitations  such  as  premature  and  divergence  phenomena  (Neshat,  2013).  Consequently,  some modifications have been suggested to avoid these limitations and enhance the PSO capabilities (e.g. introducing  inertia  weight  (Shi  and  Eberhart,  1998),  constriction  factor    (Eberhart  and  Shi,  2000), crossover operation (Lovbjerg et al. , 2001), self-adaptation (Lü et al. , 2006; Zhang et al. , 2013), and logistic dynamic weight (Ni and Deng, 2013)).The modified PSO techniques were reported to perform with reasonable convergence capability.

## 2. Overview of Particle Swarm Optimization

Kennedy and Eberhart (1995) developed PSO as a stimulation of birds swarm. Swarm is a group of individuals  with  defined  rules  for  individual  behaviors  and  communications.  The  ability  of  each individual  to  deal  with  the  previous  experiences  of  the  swarm  is  called  swarm  intelligence.  This capability  guides  the  swarm  toward  its  optimum  goal.  PSO  is  a  population-based  search  technique where a population of particles starts their journey in a space with respect to the current best position (Hossain  and  El-Shafie,  2014).  Reynolds  (1987)  described  three  simple  rules  for  the  behavior  of individuals inside a swarm which were used as one of the basic concepts of PSO by Kennedy and

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

29

30

31

32

33

34

35

36

37

38

39

40

41

42

43

44

45

46

47

48

49

50

51

52

53

54

55

56

57

58

59

60

61

62

63

64

65

Eberhart  (1995).  Although  these  simple  rules  model  the  behavior  of  individuals,  their  combination produces a complicated behavior for the swarm:

- i. Individuals avoid collision with others
- ii. Individuals go toward the goal of swarm
- iii. Individuals go to the center of swarm

The process of decision making related to individuals is other basic concept of PSO. Each individual of the swarm makes decision based on the following two factors:

- i. the own experiences of individual that is its best results so far
- ii. the  experiences  of  other  individuals  in  the  swarm  that  is  the  best  results  in  the  whole swarm

Fig.  1  illustrates  the  standard  flowchart  of  PSO.  At  the  starting  step  of  the  original  PSO  a  certain number of individuals, called particles, are distributed in the search space by using a random pattern (Kennedy  and  Eberhart,  1995;  Cheng et  al. ,  2007).  Each  particle  is  a  representative  of  a  feasible solution. Fig. 2 shows the schematic structure of a particle in PSO involving three divided parts as its current  position,  best  position,  and  velocity.  The  current  position,  best  position,  and  velocity  of particles  record  respectively  the  current  coordinates,  best  coordinates,  and  velocity  vectors  of  a particle  in  D-dimensional  space,  where  D  starts  from  one  (Kalatehjari,  2013).  Consequently,  for  a particle in D-dimensional space, a 3D-dimensional particle is desirable.

The aim of PSO is to meet the termination criteria which are defined as the criteria for terminating the iterative  search  process.  To  select  an  appropriate  termination  criterion,  it  should  be  noted  that  the termination condition  does not cause a prematurely converge  and  it  should protect against oversampling  of  the  fitness  (Engelbrecht,  2007).  The  following  termination  criteria  are  frequently used in PSO:

- i. Termination when the maximum number of iterations is exceeded
- ii. Termination  when  an  satisfactory  solution  is  found  based  on  the  condition  of  each problem
- iii. Termination when no improvement is achieved over a certain number of iterations

These criteria are applied to ensure that PSO is able to converge on a feasible solution. In fact, PSO tries to make the objective function as minimum or maximum depend to the problem to be solved.  To lead  the  swarm  toward  this  aim,  the  fitness  value  of  each  particle  is  determined  by  evaluating  its current position by the objective function. After evaluation the fitness of all particles, Eq. 1 (velocity equation) is used to calculate the velocity of particles based on their best position and the position of the best particle in the swarm. Using Eq. 2, particle positions can be updated according to their current positions and velocities. This iterative process continues until reaching the termination criteria. Eqs. 1 and 2 are as follow:

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

where, vn(i-1) is  the  velocity  of  n th particle  in  past  iteration  and  v n(i) is  the  velocity  of  n th particle  in current iteration. The vectors of random numbers of n th particle are presented by u(0, ϑ 1) and u(0, ϑ 2 ), bpn(i) is the best position of n th particle so far, bgn(i) is the position of the best particle of the swarm so far, and xn(i-1) and xn(i) are the position of n th particle respectively in the current and the next iterations.

Three components of velocity equation are respectively the initial, cognitive, and social parts. Two specifications of searching, explorations and exploitation, depend on the velocity of particles that is controlled by the values of ϑ 1 and ϑ 2. Consequently, these values control the searching behaviour of PSO. It is usual to set ϑ 1= ϑ 2=2 in early search. A greater value of ϑ 1  provides faster convergence, while increase in ϑ 2 helps to discover new solutions in the search space. Since the velocity of particles may increase surprisingly by changing the mentioned coefficients, a limiting bound of velocity as [vmax, vmax] was attached to the original PSO. The value of vmax is called constriction coefficient. Poli et al.  (2007)  advised  to  select  the  constriction  coefficient  carefully,  since  it  influenced  the  balance  of exploration and exploitation. By introducing  as the inertia weight of particles, the original formula of  velocity  was  edited  by  Shi  and  Eberhart  (1998)  to  minimize/reduce  the  role  of  constriction coefficient as presented in Eq. 3. However, Clerc and Kennedy (2002) showed that using the inertia weights  of  greater  than  one  interrupts  the  converge  process  of  PSO.  They  proposed  Eq.  4  by introducing  as  the  constant  multiplier  in  to  prevent  the  explosion  of  the  swarm,  guaranteed  the converge process, and almost eliminated the effects of constriction coefficient.

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

In  PSO,  all  members  of  the  population  stay  alive  and  move  along  the  process  of  optimization. Therefore, it can guarantee to save all feasible solutions (Kennedy and Eberhart, 1995). Moreover, PSO works with real variables, operates simple, and needs slight tune-up studies to make convergence and searching in balance (Clerc and Kennedy, 2002). These features have equipped PSO with simple implementation  and  fast  convergence  to  the  optimal  solution  which  are  the  main  reasons  of  its popularity (Windisch et al. , 2007).

With  the  aim  of  improving  the  PSO  performance,  many  attempts  have  been  made  to  incorporate obtained knowledge  from  other evolutionary computation approaches through adapting  PSO parameters. By employing the Gaussian noise, Miranda and Fonseca (2002) proposed self-adapting PSO. In this technique, the variance of distributions is evolved using selection. Lovjberg et al. (2001) utilized  a  sort  of  breeding  to  recombine  solutions.  In  their  technique,  by  performing  weighted averaged  of  PSO  parameters,  the  position  and  velocity  of  the  selected  pairs  of  particles  were recalculated. PSO and GA algorithms were combined by Robinson et al. (2002) through switching one of them to another one after several iterations. The best results were obtained by switching of the PSO to GA. Ciuprina et al. (2002) proposed intelligence PSO based on the combination of PSO with

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

29

30

31

32

33

34

35

36

37

38

39

40

41

42

43

44

45

46

47

48

49

50

51

52

53

54

55

56

57

58

59

60

61

62

63

64

65

Tabu search method. The successful performance was obtained for solving the difficult multimodal problems.

PSO  has  been  greatly  effective  to  solve/approximate  a  huge  range  of  problematic  optimization problems  in  the  civil  engineering  arena  such  as  construction  litigation,  design  optimization  of water/wastewater  distribution  networks,  traffic  control,  structural  design,  parameter  calibration  of hydrological  models,  river  stage  prediction,  transportation  network  design,  geotechnical  model calibration, slope stability analysis, and pavement engineering. Consequently, the application of PSO has  increased  surprisingly  in  recent  years.  Table  1  presents  a  comparison  between  PSO  and  three other well-known metaheuristic methods.

## 3. PSO Applications in Geotechnical Engineering

Complexity of analysis of geotechnical behavior is due to multivariable dependencies of soil and rock responses. Most of the materials that geotechnical engineers deals with show uncertain behavior in consequence  of the complex  formation  of these materials. Therefore, in some  geotechnical engineering problems, the objective function is non-convex and discontinuous. Consequently, simple optimization  techniques  may  have  difficulties  in  finding  the  global  optimum  solution  due  to  get trapped  in  local  solutions.  To  overcome  this  limitation,  using  a  powerful  optimization  method  to obtain the global optimum solution is of interest. Accordingly, as a powerful optimization technique, PSO  has  entered  in  the  field  of  geotechnical  engineering  to  solve  its  problems.  In  the  following sections, a review of the PSO applications in geotechnical engineering is presented.

## 3.1. Slope Stability Analysis

The application of PSO in slope stability analysis is mainly within the framework of limit equilibrium method  for  soil  slopes  (Kalatehjari  and  Ali,  2013).  This  context  involves  two  major  steps  as calculating the factor of safety of possible slip surfaces and determining the critical slip surface with the minimum factor of safety. PSO is mainly used to the second step, since the shape and location of the critical slip surface is generally unknown in soil slopes (Bolton et al ., 2003).

PSO  can  be  applied  to  two-dimensional  (2D)  or  three-dimensional  (3D)  slope  stability  problems (Kalatehjari, 2013). In 2D analyzes, a search engine can be applied to the problem to determine the shape of the critical slip surface in a pre-defined section of the slope. The common shapes of the slip surface  in  2D  analyzes  are  circular,  ellipse,  spiral,  and  polygonal  or  arbitrary  (Chen et  al. ,  2006; Kalatehjari  et  al.,  2014).  In  contrast,  3D  analyzes  assume  space  shapes  of  slip  surfaces  such  as spherical, ellipsoidal, and Non-Uniform Rational B-Splines (Li et al. , 2008; Kalatehjari et al. , 2012; Taha et al. , 2012).

Fig.  3  shows  the  general  flowchart  of  PSO  to  determine  the  critical  slip  surface  in  slope  stability analysis. The initial PSO parameters were set in order to start optimization procedure. After that, a number of  particles  equal  to  swarm  size  are  generated  by  using  a  random  pattern  over  the  search space. The personal best particles for the first swarm are identical to particles themselves; because no other swarm exists yet to make a comparison. The velocity of all particles at the starting point is set to zero, because the particles are just created without any movement. After setting up the initial values, the first particle is converted to a slip surface. If this slip surface has an acceptable intersection with the slope, it is qualified. Otherwise, the slip surface is disqualified. A pre-defined value of fitness is given  to  disqualify  slip  surfaces  as  the  minimum  fitness.  This  value  is  obtained  by  setting  the maximum allowed value of FOS. In parallel, the value of FOS together with the unique direction of sliding are calculated for qualified slip surfaces. Then, the corresponding fitness values of particles are  calculated  by  fitness  function  of  PSO.  This  process  is  repeated  for  all  particles  of  the  swarm (Kalatehjari, 2013).

The global best particle is defined as the one with the greatest fitness value in a swarm. The current position of particles that improved their fitness value is recorded as their new personal best positions, while  the  previous  best  position  is  retained  for  other  particles.  Through  an  iterative  process, subsequent swarms are generated by updating the velocity and position of particles. The optimization process  is  finished  when  the  particles  of  a  swarm  satisfy  the  termination  criteria.  Eventually,  the position of the last global best particle represents the critical slip surface of the slope.

Kalatehjari et  al .  (2012  and  2014),  Taha et  al .  (2012),  and  Wang et  al .  (2013)  used  PSO  in  2D analysis to determine the location of critical slip surface with circular shape. They proved the ability of  PSO  in  determining  the  critical  slip  surface  by  re  analysing  three  numerical  examples  from  the literature and actual slope stability problem. Moreover, Zhou et al . (2012) proposed an arbitrary shape of 2D slip surface defined by seven control points with arbitrary horizontal spacing to determine the general shape and location of the critical slip surface. They benefited the global feature of PSO to avoid  local  minima  and  verified  their  approach  by  evaluating  two  examples  for  simple  slope  and complex slope.

Li et al . (2005) applied a modified PSO to determine the critical slip surface of slope. Their proposed method, discontinuous flying PSO, was created by relating the position and velocity update of particle to their fitness value. They found an average improvement of 6% and faster convergence in the results of their method compared with the original PSO. Li et al . (2010) introduced a mutation PSO to solve the search of critical slip surface in complex soil slopes. They concluded that their proposed method can locate the true critical slip surface.

Chen et al. (2006) adopted PSO to determine the 2D non-circular critical slip surface of slope. They listed the benefits of PSO as providing a good balance between global search and local refinement, solving  the  local  minima  problem,  great  efficiency,  and  easily  incorporating  with  both  limit equilibriums  and  finite  element  methods.  Zhao et  al .  (2008)  applied  an  updated  PSO  method  to determine the 2D non-circular critical slip surface of non-homogeneous slope. They found that faster convergence rate and better precession are the superior abilities of PSO.

Kang et  al .  (2006)  and  Wen-Tao  (2009)  respectively  developed  the  combined  method  of  PSO  by adding  support  method  machines  and  least  square  vector  machines  methods  to  evaluate  the  2D stability  of  rock  slopes.  They  concluded  that  fast  speed  of  problem  solving,  more  accurately estimation of slope stability, and global optimization are the advantages of this technique.

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

29

30

31

32

33

34

35

36

37

38

39

40

41

42

43

44

45

46

47

48

49

50

51

52

53

54

55

56

57

58

59

60

61

62

63

64

65

Li et al . (2008 and 2009), Wang et al . (2010), Li and Chu (2011), and Cheng et al . (2011) applied a coupled  optimization  method  of  PSO/harmony  search  to  solve  the  nonlinear  function  of  factor  of safety in slope stability problem. The feasibility and applicability of this technique was supported by evaluating practical engineering problems and re-evaluating bench mark problems from literature. In addition,  Khajehzadeh  et  al.  (2010  and  2011)  used  a  same  combined  optimization  method  of PSO/harmony search to analyse the reliability of earth slope in 2D. They obtained lower values of reliability and factor of safety in comparison with the standard PSO and other methods by employing their new method in previous studies. Xu et al . (2011) developed an optimization method based on the Projection Pursuit (PP), PSO, and the Logistic Curve Function (LCF) to evaluate the 2D problem of slope stability. PSO was used to optimize the PP function and the parameters of LCF. They verified the feasibility and affectivity of their proposed model in practice by evaluating a case study.

Li et al . (2012) proposed a modified PSO in cooperation with finite element limit equilibrium method (FELEM) to determine the location and shape of non-circular critical slip surface in 2D geotechnical problems. Based  on  the slope geometry and stress distribution, they established the stress compatibility  constraints  together  with  the  geometrical  and  kinematical  compatibility  constraints. These extra features were used to guarantee the realistic shape of the critical slip surface. They went through several numerical examples to prove the affectivity and efficiency of their approach in routine geotechnical practices.

Although PSO has successfully contributed in determining the 2D critical slip surface, it is absent in 3D slope stability analysis. In fact, only a few researchers published their results in determining the critical  slip  surface  in  3D  slope  stability  problems  and  none  of  them  applied  PSO.  Yamagami  and Jiang  (1997)  applied  Dynamic  Programming  with  Random  Number  Generator, Jiang et  al .  (2003), Mowen (2004),  and  Mowen  et  al . (2011)  used  Monte  Carlo  method,  Cheng et  al .  (2005)  utilized Simulated Annealing, and Toufigh et al. (2006) applied Gradient methods to determine the critical slip  surface  in  3D  slopes  stability  problems.  The  shortage  of  studies  in  this  area  is  caused  by  the potential  difficulties  in  performing  a  successful  search  within  a  complicated  3D  slope  stability problem.  The  problem  of  determining  the  3D  critical  slip  surface  needs  a  fast  and  precise  global

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

29

30

31

32

33

34

35

36

37

38

39

40

41

42

43

44

45

46

47

48

49

50

51

52

53

54

55

56

57

58

59

60

61

62

63

64

65

optimization technique to work integrated with the complicated 3D equations of FOS and slip surface respectively  as  its  objective  function  and  particle  generator  (Kalatehjari,  2013).  Based  in  the successful  performance  of  PSO  in  2D  slope  stability  analysis  as  well  as  other  problems  of geotechnical engineering, it is  believed  that  PSO can  be  a competent  candidate  in the study  of  3D critical slip surface.

## 3.2. Pile and Foundation Design

In General, the application of PSO in pile and foundation design is mainly in predicting the behavior of axially loaded piles and ultimate bearing capacity of foundations. In addition, PSO has been used to estimate the secant pile construction time.

A  hybrid  PSO-BP  model  was  developed  by  Ismail  and  Jeng  (2012)  to  predict  the  relationship  of load/settlement in a  single  pile. They  considered  pile  settlement  as  a  non-linear  function  of related parameters as follow:

<!-- formula-not-decoded -->

in which, S, P, ks, Ep, D and L are pile settlement, pile load, soil stiffness, pile modulus, pile diameter and pile length, respectively. A database of 92 static pile loading tests on concrete piles was used to conduct the modeling. The results of their study show high values of correlation coefficient between predicted settlements obtained by PSO-ANN model and measured settlements obtained by static load tests.

In the field of geotechnical engineering, construction time is a critical factor for control the cost and planning in construction projects. Regarding this, Chen et al . (2009) compared the construction time of a secant pile wall using two  optimization methods  including  self-organizing  map  based optimization (SOMO) and PSO. A database consists of 207 primary and secondary bored piles for a secant pile wall was used in this study. The results of the study revealed that the total saved time for the  SOMO and PSO was 27.21 and 23.79 h respectively. They concluded that the SOMO method yields better construction compared to the PSO method.

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

29

30

31

32

33

34

35

36

37

38

39

40

41

42

43

44

45

46

47

48

49

50

51

52

53

54

55

56

57

58

59

60

61

62

63

64

65

A research on the load-deformation behaviour of axially loaded piles was conducted by Ismail et al . (2013). They utilized a hybrid PSO-BP model for predicting behavior of single piles embedded in soil medium  and  subjected  to  an  axial  load.  The  data  of  full  scale  static  load  tests  of  115  piles  were considered to train and validate the network. Subsequently, the PSO-BP algorithm was used to solve the soil-structure interaction problem, including a difficult mechanism of load transfer from the pile to the supporting geologic medium. Pile load, soil stiffness, pile modulus, pile diameter, and pile length were used as inputs whereas pile load-deformation was considered as output. For evaluation purpose, they compared the results the proposed model with BP and PSO models as well as the PSO-BP model developed by Zhang et  al .  (2007).  Finally,  they  found  that  the  proposed  PSO-BP  hybrid technique simulates  the  load-deformation  curve  of  axially  loaded  piles  more  accurately  compared  to  other models.

Zhao and Yin (2010) utilized a Chaotic PSO (CPSO) and support vector machine (SVM) method for ultimate  bearing  capacity  prediction  of  shallow  foundation.  CPSO  is  a  more  superior  algorithm  in comparison  to  simple  PSO  in  terms  of  searching  quality,  efficiency  and  robustness  on  initial conditions. Fig. 4 shows the algorithm of CPSO-SVM proposed by Zhao and Yin (2010) to determine the ultimate bearing capacity of shallow foundations. They utilized footing width (B), footing depth (D),  footing  geometry  (L/B),  unit  weight  of  sand  (γd)  and  angle  of  shearing  resistance  (θ)  as  input parameters, whereas the ultimate bearing capacity (qu) was used as the single output variable. The results  revealed  that  the  CPSO-SVM  model  predicts  the  ultimate  bearing  capacity  of  shallow foundation with high degree of accuracy.

Evaluation  of  pile  capacity  and  control  of  pile  driving  are  significant  issues  in  pile  installation process. In this way, Cheng et al. (2012) developed a modified model based on hybrid of harmony search (HS) and PSO for selection of parameters related to the maximum axial load. The purpose of selecting  parameters  was  to  minimize  difference  between  the  calculated  axial  load  values  obtained from formula and the measured axial load values obtained from the pile driving analyzer (PDA) tests. From the conclusion part of this study it can be found that the proposed coupling model is effective over a wide range of problems and also this model can be applied in different fields of engineering.

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

29

30

31

32

33

34

35

36

37

38

39

40

41

42

43

44

45

46

47

48

49

50

51

52

53

54

55

56

57

58

59

60

61

62

63

64

65

## 3.3. Rock Mechanics

The  application  of  PSO  in  rock  mechanics  included  but  not  limited  to  determining  the  roughness profiles of rocks, back analysis of geomechanical parameters, identifying the structure of rocks, and recognizing the structure of altered rocks.

A new method based on hybrid PSO algorithm and multi-layer perceptron (MLP) neural network was developed  by  Babanouri et  al .  (2013)  to  estimate  fractal  dimension  of  roughness  profiles  (D)  and standard  deviation  (σ)  of  rock.  It  is  worth  noting  that  determination  of  D  is  still  a  problem  in geotechnical  engineering  due  to  attributed  different  values  of  the  fractal  dimension.  There  are  two kinds  of  errors  for  prediction  of  fractal  dimension;  stochastic  and  systematic.  Modelling  of  these errors  is  difficult  because  of  the  complexity  relationship  between  the  fractal  dimension  and  the measurable variables. A huge number of fractional Brownian including 39900 profiles was generated and  their  statistical  features  were  extracted.  They  examined  this  model  for  10  standard  profiles  of roughness  and  concluded  that  the  proposed  estimator  gives  an  error  15  times  smaller  than  the roughness-length method. The results show that the fractal dimension does not necessarily increase with increasing roughness.

Zhao  and  Yin  (2009)  proposed  a  new  intelligent  displacement  back  analysis  method  based  on  the combination  of  support  vector  machine,  PSO,  and  numerical  analysis.  A  non-linear  relationship between displacement and geomechanical parameters of rock mass was described by SVM. They used PSO to increase the generalization performance of searching process in the SVM model. A series of numerical analyses (using FLAC2D) was conducted to produce the required datasets for training and testing  steps.  Fig.  5  shows  the  process  of  recognizing  the  rock  mass  parameters  using  the  back analysis based on the proposed method. The results revealed that the proposed technique increases the efficiency and precision of back analysis of geomechanical parameters.

A hybrid genetic programming with modified PSO algorithm was proposed by Feng et al . (2006) to identify the structure of visco-elastic models of rocks. In this study, genetic programming was utilized to explore the structure of the model and the modified PSO was used to investigate coefficients in the

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

29

30

31

32

33

34

35

36

37

38

39

40

41

42

43

44

45

46

47

48

49

50

51

52

53

54

55

56

57

58

59

60

61

62

63

64

65

provisional  model.  They  concluded  that  if  the  evolving  factors  and  number  of  generation  are appropriately set, the fitness method can be found with a global optimum solution.

Zhan and Wu (2009) recognized the hyper-spectral altered rock using an improved algorithm based on PSO and neural network. The point was mentioned in their paper that PSO can be improved into two parts;  reinforcing  the  particles  diversity  and  avoiding  the  prematurity  of  particle  swarm.  Field survey of altered rock spectral data was used to investigate samples of illite, chlorite, gypsum and kaolinite for using in the network. To show the ability of the improved PSO-BP model, the network was also modelled using BP algorithm. The results indicated that the BP algorithm easily falls into the local minima whereas the proposed PSO-BP method can be effectively applied to identify the altered rocks.

## 3.4. Soil Mechanics

PSO have successfully encountered with some problems in soil mechanics such as determination of soil erosion characteristics, behavior of unsaturated soil, soil-structure interaction, and soil parameters.

Yunkai et al . (2010) predicted soil erosion characteristics in small watersheds using a combination of SVM and  PSO.  In  fact,  they  introduced  the  application  of  PSO  for  automatic  selection  of  SVM parameters  and  presented  a  model  by  linking  PSO  and  SVM  for  small  sample  data  analysis.  The predicting model in this study was based on the monitoring data of sand production. According to the results, the proposed model can simulate successfully the erosion characteristics in small watersheds with low degree of average error (3.85%).

Zhang et al. (2009 and 2013) utilized a hybrid moving boundary PSO (HMPSO) method to minimize the difference between measured (field data) and computed values on the cavity pressure-cavity strain curve  in  unsaturated  soil.  They  used  the  HMPSO  algorithm  to  select  parameter  values  in  the Barcelona Basic Model (BBM) which is one of the best known constitutive models for unsaturated soils. Field data  were  obtained  from  Suction  Monitored  Pressuremeter tests,  which  employ

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

29

30

31

32

33

34

35

36

37

38

39

40

41

42

43

44

45

46

47

48

49

50

51

52

53

54

55

56

57

58

59

60

61

62

63

64

65

tensiometers to measure suction. The computed cavity pressure-cavity strain curve was obtained using finite element model of an unsaturated soil. In their study, an HMPSO algorithm was used to identify model  parameters  of  field  Pressuremeter  tests.  The  combination  of  field  Pressuremeter  tests,  finite element results  and the  HMPSO algorithm introduces a practical technique to determine parameter values for geotechnical modelling in unsaturated soils.

Fontan et  al .  (2011)  used  PSO  algorithm  and  finite  element  (FE)  method  to  develop  an  inverse identification  process.  The  objective  here  was  to  recognize  the  equivalent  structure  stiffness  that mimics soil-structure interaction problem. For this purpose, experimental tests and FE analysis were conducted  to  validate  methodology  and  to  show  the  role  of  the  input  data  (displacement)  on  the identification  quality.  In  this  study,  a  general  frame  based  on  different  combination  tools  (inverse analysis, FE and PSO techniques) was developed to solve the problem. PSO was utilized for treatment of  the  mechanical  properties  recognition.  They  concluded  that  the  combination  of  aforementioned methods is able to investigate the parameters related to inverse problem.

Sadoghi Yazdi et al. (2012) calibrated the soil parameters using the linear elastic-hardening plastic constitutive  model  and  the  Drucker-Prager  yield  criterion  by  the  combination  of  the  neuro-fuzzy (ANFIS) and PSO model. For providing nonlinear relationship between the deviatoric stress and axial strain (σd-ԑ) resulted from a consolidated drained triaxial test on sand samples, an ANFIS model was used in this  study.  According  to  Fig.  6,  PSO  was  utilized  to  determine  soil  model  parameters.  For verification of the accuracy and applicability of the proposed technique, a series of data obtained from different confining pressures was modelled using the proposed model. The outcome showed a close match with the same order of accuracy.

## 3.5. Tunneling and Underground Space Design

Since tunneling deals with many uncertainties, the conventional empirical and analytical methods face with some difficulties in tunnel designing. Based on the applicability of PSO in funding the optimum solution, its applications have been developed in different aspects of tunnel design such as prediction

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

29

30

31

32

33

34

35

36

37

38

39

40

41

42

43

44

45

46

47

48

49

50

51

52

53

54

55

56

57

58

59

60

61

62

63

64

65

of  tunneling-induced ground movements and building damage,  determining the rock displacements around  a  tunnel,  finding  the  optimized  supporting  system  parameters,  and  obtaining  the  optimized performance of tunnel boring machines (TBM).

Hajihassani  (2013)  developed  hybrid  PSO-based  ANN  model  to  predict  three  dimensional  ground movements  induced  by  tunneling.  For  that  reason,  an  extensive  database  consisting  of  measured settlements, geotechnical parameters and tunneling parameters were collected From Karaj Tunnel in Iran.  In  order  to  assess  the  ability  and  accuracy  of  the  proposed  model,  the  predicted  ground movements using proposed model were compared with the measured settlements. In addition, for a particular point, ground movements were obtained using FE analysis and the results were compared with the proposed model. He indicated that the proposed model is able to eliminate the limitations of the current methods and is an applicable tool to predict three-dimensional tunneling-induced ground movements with high degree of accuracy.

A  research  has  been  conducted  by  Xing et  al .  (2010)  to  study  the  adaptive  control  of  tunnel excavation  in  rock.  Focusing  on  the  uncertainty  of  underground  engineering,  they  introduced  PSO application to recognize rock mechanical  parameters and obtaining the  optimum  supporting parameters. Using the in-situ monitoring displacements, they obtained rock mechanics parameters and subsequently optimized anchor parameters using these parameters. Furthermore, they investigated the process  of  combining  PSO  with  3D  fast  Lagrange  numerical  method  and  applied  this  method  to Dalian Gezhenpu tunnel in China. They resulted that the PSO arithmetic can be easily realized and the proposed method provides a new way to inform construction design. Annan and Zhiwu (2011) also used  an  improved  PSO  to  optimize  the  anchor  and  spay  layer  parameters  in  rock  tunneling.  They applied the presented method in metro tunnel of Dalian City in China with satisfied results. A similar study on the rock displacements around a tunnel was conducted by Jiang et al . (2011). They employed a combination of PSO and SVM to identify the nonlinear relationship between tunnel parameters and displacements around a tunnel. For this purpose, they used numerical analysis to produce training and testing  samples.  Afterwards,  they  utilized  SVM  to  determine  the  nonlinear  relationship  between

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

29

30

31

32

33

34

35

36

37

38

39

40

41

42

43

44

45

46

47

48

49

50

51

52

53

54

55

56

57

58

59

60

61

62

63

64

65

parameters and displacements. The parameters of SVM were determined using PSO algorithm and the results were validated with a case study.

Performance prediction of hard rock TBM is a complex and essential task in mechanized excavation which may reduce the risks related to high capital costs. Yagiz and Karahan (2011) employed PSO algorithm to predict the performance of TBM using a database consisting of intact rock parameters, rock mass properties and field machine performance data. They generated seven different PSO models employing the variety of datasets with various percentages of rock type and concluded that the PSO is applicable to predict TBM penetration rate precisely.

In  addition  to  abovementioned  application,  PSO  algorithm  was  employed  to  increase  the  ANN applicability  in  modeling  the  trench  layer  location  around  a  pipeline.  In  this  respect,  Janalizadeh Choobbasti et al . (2014) utilized an integrated PSO-ANN model to determine the optimum locations of a trench layer around a pipeline. The local radial basis function differential quadrature (LRBF-DQ) method was used in their study to obtain the pore pressure and the obtained data were utilized to train the  ANN.  Finally,  PSO  was  used  to  determine  the  best  location  of  trench  later.  The  results demonstrated  the  minimum  liquefaction  is  happened  when  the  trench  layer  is  placed  beneath  the pipeline.

## 3.6. Other Applications

In  addition  to  aforementioned  applications,  PSO  algorithm  has  been  employed  in  optimization problems of varies geotechnical engineering  fields. Hajihassani et al.  (2014) employed PSO as the training  algorithm  of  ANN  to  predict  environmental  impacts  of  blasting  operation,  including  the flyrock and ground vibration. The PSO was used in their study as optimization algorithm to achieve the  best  weights  and  biases  for  applying  in  ANN.  Collected  datasets  from  blasting  operations including the most influential parameters on flyrock distance and ground vibration were considered in their study. The proposed models presented satisfactory results to predict flyrock distance and ground vibration with a high degree of precision.

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

29

30

31

32

33

34

35

36

37

38

39

40

41

42

43

44

45

46

47

48

49

50

51

52

53

54

55

56

57

58

59

60

61

62

63

64

65

To minimize maintenance-related, Xu and Zeng (2010) utilized PSO algorithm to solve a dynamic equipment allocation problem (DEAP) through the operation of a concrete-faced rock-fill dam. As an important maximization factor in construction throughput, the uncertainties associated with equipment failures were considered in a mathematical model. Their model was confined by initial and constraint conditions. Afterwards, PSO algorithm was implemented to find the optimum solution of the DEAP. The Shuibuya Hydropower Project was utilized to investigate the applicability and efficiency of the propose  method.  The  results  demonstrated  that  the  proposed  optimization  model  is  applicable  and efficient in solving the DEAP with uncertainties.

Based on PSO algorithm, a decision support system was proposed by Wang et al . (2011) to reduce the disequilibrium  degree  of  filling  intensity  in  rock-fill  dams.  They  analyzed  the  main  affecting parameters on substage-zoning filling design and proposed an optimization model based on analyses. Based upon this, a decision support system for the substage-zoning  filling design of rock-fill dams was developed. They employed the proposed model in a hydropower project and demonstrated the applicability of the proposed model in various types of rock-fill dams.

## 4. Conclusions

Complex and not well-understood problems are the common obstacles in geotechnical engineering. In this regard, finding the optimum  solution is difficult and even impossible in some  cases. Consequently, PSO has been extensively used in geotechnical engineering as a powerful optimization technique to find the optimum solution. Simplicity of the operations and reasonability of the results have paved the way to use PSO in various fields of geotechnical engineering such as slope stability analysis, pile and foundation engineering, rock and soil mechanics, and tunneling and underground space design.

In PSO algorithm, each individual learns not only from its own experience, but also from the others, especially  from  the  best  particle.  Therefore,  PSO  presents  some  advantages  over  conventional optimization techniques by using simultaneous combination of particles cooperation and competition.

Despite the  advantages  of  PSO  in  solving  the  complex  engineering  problems,  it  should  be  applied with  caution  in  consequence  of  the  fact  that  divergence  phenomenon  happens  occasionally  in  its optimization  process.  In  addition,  local  solutions  may  trap  PSO  by  setting  inappropriate  initial parameters in which depend on the condition of each problem. Consequently, the application of PSO should  be  always  with  caution  and  conducting  sensitivity  analysis  on  initial  parameters  to  avoid returning disappointing results.

## References

- Annan,  J.,  and  Zhiwu,  W.  (2011).  'Optimizing  Supporting  Parameters  of  Metro  Tunnel  Based  on Improved Particle Swarm Optimization Arithmetic.' Procedia Engineering, Vol. 15, pp. 48574861, DOI: 10.1016/j.proeng.2011.08.906.
- Antoniou,  P.,  Pitsillides,  A.,  Blackwell,  T.,  and  Engelbrecht,  A.  (2009).  'Employing  the  flocking behavior of birds for controlling congestion in autonomous decentralized networks' 2009 IEEE Congress on Evolutionary Computation, pp. 1753-1761.
- Antoniou,  P.,  Pitsillides,  A.,  Blackwell,  T.,  Engelbrecht,  A.,  and  Michael,  L.  (2013).  'Congestion control in wireless sensor networks based on bird flocking behavior.: Computer Networks , Vol. 57, No. 5, pp. 1167-1191, DOI: 10.1016/j.comnet.2012.12.008.
- Babanouri,  N.,  Nasab,  S.  K.,  and  Sarafrazi,  S.  (2013).  'A  hybrid  particle  swarm  optimization  and multi-layer  perceptron  algorithm  for  bivariate  fractal  analysis  of  rock  fractures  roughness.' International  Journal  of  Rock  Mechanics  and  Mining  Sciences,  Vol.  60,  pp.  66-74,  DOI: 10.1016/j.ijrmms.2012.12.028.
- Bolton,  H.,  Heymann,  G.,  and  Groenwold,  A.  (2003).  'Global  search  for  critical  failure  surface  in slope stability analysis.' Engineering Optimization, Vol. 35, No. 1, pp. 51-65.
- Chen, D., Zhao, C., and Zhang, H. (2011). 'An improved cooperative particle swarm optimization and its  application'.  Neural  Computing  and  Applications,  Vol.  20,  No.  2,  pp.  171-182,  DOI: 10.1007/s00521-010-0503-4.
- Chen, J.H., Yang, L.R., and Su, M.C. (2009). 'Comparison of SOM-based optimization and particle swarm optimization for minimizing the construction time of a secant pile wall.' Automation in Construction, Vol. 18, No. 6, pp. 844-848, DOI: 10.1016/j.autcon.2009.03.008.
- Chen, Y., Wei, X., and Li, Y. (2006). 'Locating non-circular critical slip surfaces by particle swarm optimization algorithm.' Chinese Journal of Rock Mechanics and Engineering, Vol. 25, No. 7, pp. 1443-1449.
- Cheng, Y.M., Li, D. Z., Li, L., Sun, Y. J., Baker, R., and Yang, Y. (2011). 'Limit equilibrium method based on an approximate lower bound method with a variable factor of safety that can consider

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

29

30

31

32

33

34

35

36

37

38

39

40

41

42

43

44

45

46

47

48

49

50

51

52

53

54

55

56

57

58

59

60

61

62

63

64

65

residual strength.' Computers and Geotechnics, Vol. 38, No. 5, pp. 623-637, DOI: 10.1016/j.compgeo.2011.02.010.

- Cheng, Y.M., Li, L., and Chi, S.C. (2007). 'Performance studies on six heuristic global optimization methods in the location of critical slip surface.' Computers and Geotechnics, Vol. 34, No. 6, pp. 462-484, DOI: 10.1016/j.compgeo.2007.01.004.
- Cheng, Y.M., Li, L., Sun, Y.J., and Au, S. K. (2012). 'A coupled particle swarm and harmony search optimization  algorithm  for  difficult  geotechnical  problems.'  Structural  and  Multidisciplinary Optimization, Vol. 45, No. 4, pp. 489-501, DOI: 10.1007/s00158-011-0694-z.
- Cheng, Y.M., Liu, H.T., Wei, W.B., and Au, S.K. (2005). 'Location of critical three-dimensional nonspherical  failure  surface  by  NURBS  functions  and  ellipsoid  with  applications  to  highway slopes.' Computers and Geotechnics, Vol. 32, No. 6, pp. 387-399, DOI: 10.1016/j.compgeo.2005.07.004.
- Choobbasti, A.J., Tavakoli, H., and Kutanaei, S.S. (2014). 'Modeling and optimization of a trench layer location around a pipeline using artificial neural networks and particle  swarm optimization  algorithm.' Tunnelling  and  Underground  Space  Technology, Vol.  40,  pp.  192202, DOI: 10.1016/j.tust.2013.10.003.
- Ciuprina, G., Ioan, D., and Munteanu, I. (2002). 'Use of intelligent particle swarm optimization in electromagnetics.' IEEE Transactions on Magnetics, Vol. 38, No. 1037-1040.
- Clerc,  M.,  and  Kennedy,  J.  (2002).  'The  particle  swarm-explosion,  stability,  and  convergence  in  a multidimensional  complex  space.' IEEE  transactions  on  Evolutionary  Computation, Vol.  6, No. 1, pp. 58-73.
- Cui, Z., and Gao, X. (2012). 'Theory and applications of swarm intelligence.' Neural Computing &amp; Applications, Vol. 21, No. 2, pp. 205-206, DOI: 10.1007/s00521-011-0523-8.
- Dorigo, M., and Blum, C. (2005). 'Ant colony optimization theory: A survey.' Theoretical computer science, Vol. 344, No. 2, pp. 243-278, DOI:10.1016/j.tcs.2005.05.020.
- Eberhart, R.C, and Kennedy, J. (1995). 'A new optimizer using particle swarm theory.' Proceeding of the  Sixth  International  Symposium  on  Micro  Machine  and  Human  Science,  IEEE,  Nagoya, Japan, pp. 39-43.
- Eberhart,  R.C.,  and  Shi,  Y.  (2000).  'Comparing  inertia  weights  and  constriction  factors  in  particle swarm optimization.' Proceeding of Congress Evolutionary Computation, NJ:IEEE Press, pp. 84-88.
- Engelbrecht, A.P. (2007). 'Computational intelligence: an introduction.' John Wiley &amp; Sons.
- Feng,  X.T.,  Chen,  B.R.,  Yang,  C.,  Zhou,  H.,  and  Ding,  X.  (2006).  'Identification  of  visco-elastic models  for  rocks  using  genetic  programming  coupled  with  the  modified  particle  swarm optimization algorithm.' International Journal of Rock Mechanics and Mining Sciences, Vol. 43, No. 5, pp. 789-801, DOI: 10.1016/j.ijrmms.2005.12.010.

- Fontan, M., Ndiaye, A., Breysse, D., Bos, F., and Fernandez, C. (2011). 'Soil-structure interaction: Parameters identification using particle swarm optimization. Computers &amp; Structures, Vol. 89, No. 17, pp. 1602-1614, DOI: 10.1016/j.compstruc.2011.05.002.
- Gholizadeh, S.,  and  Salajegheh,  E.  (2009).  "Optimal  design  of  structures  subjected  to  time  history loading  by  swarm  intelligence  and  an  advanced  metamodel."  Computer  Methods  in  Applied Mechanics and Engineering, Vol. 198, No. 37, pp. 2936-2949, DOI: 10.1016/j.cma.2009.04.010.
- Hajihassani,  M.  (2013).  'Tunneling-Induced  Ground  Movement  and  Building  Damage  Prediction Using Hybrid Artificial Neural Networks.' PhD diss., Universiti Teknologi Malaysia.
- Hajihassani, M., Jahed Armaghani, D., Monjezi, M., Mohamad, E.T., and Marto, A. (2015). 'Blastinduced  air  and  ground  vibration  prediction:  a  particle  swarm  optimization-based  artificial neural network approach.' Environmental Earth Sciences, Vol. 74, No. 4, pp. 2799-2817, DOI: 10.1007/s12665-015-4274-1.
- Hajihassani,  M.,  Jahed    Armaghani,  D.,  Sohaei,  H.,  Mohamad,  E.T.,  and  Marto,  A.  (2014). 'Prediction of airblast-overpressure induced by blasting using a hybrid artificial neural network and particle swarm optimization.' Applied Acoustics, Vol. 80, pp.57-67, DOI: 10.1016/j.apacoust.2014.01.005.
- Hossain,  M.S.,  and  El-Shafie,  A.  (2014).  'Evolutionary  techniques  versus  swarm  intelligences: application  in  reservoir  release  optimization.' Neural  Computing  and  Applications, Vol.  24, No. 7, pp. 1583-1594, DOI: 10.1007/s00521-013-1389-8.
- Ismail, A., and Jeng, D.S. (2012). 'Empirical Method for Settlement Prediction of Single Piles Using Higher Order Neural Network and Particle Swarm Optimization.' In Geo Congress 2012, State of the Art and Practice in Geotechnical Engineering, pp. 285-294.
- Ismail, A., Jeng, D. S., and Zhang, L. L. (2013). 'An optimised product-unit neural network with a novel PSO-BP hybrid training algorithm: Applications to load-deformation analysis of axially loaded  piles.'  Engineering  applications  of  artificial  intelligence,  Vol.  26,  No.  10,  pp.  23052314, DOI: 10.1016/j.engappai.2013.04.007.
- Jahed  Armaghani,  D.,  Hajihassani,  M.,  Mohamad,  E.T.,  Marto,  A.,  and  Noorani,  S.A.  (2014). 'Blasting-induced flyrock and  ground  vibration  prediction  through  an  expert  artificial  neural network based on particle swarm optimization.' Arabian Journal of Geosciences, Vol. 7, No. 12, pp. 5383-5396, DOI: 10.1007/s12517-013-1174-0.
- Jahed Armaghani, D., Hajihassani M, Yazdani Bejarbaneh B, Marto A, and Tonnizam Mohamad, E. (2014).  'Indirect  measure  of  shale  shear  strength  parameters  by  means  of  rock  index  tests through  an  optimized  artificial  neural  network.'  Measurement,  Vol.  55,  pp.  487-498,  doi: 10.1016/j.measurement.2014.06.001.
- Jiang, A.N., Wang, S.Y., and Tang, S.L. (2011). 'Feedback analysis of tunnel construction using a hybrid arithmetic based on Support Vector Machine and Particle Swarm

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

29

30

31

32

33

34

35

36

37

38

39

40

41

42

43

44

45

46

47

48

49

50

51

52

53

54

55

56

57

58

59

60

61

62

63

64

65

Optimisation.' Automation in Construction, Vol. 20, No. 4, pp. 482-489, DOI: 10.1016/j.autcon.2010.11.016.

- Jiang, J.C., Yamagami, T., Baker, R. (2003). 'Three-Dimensional Slope Stability Analysis Based on Nonlinear Failure  Envelope.'  Chinese Journal of  Rock  Mechanics  Engineering,  Vol.  22,  pp. 1017-1023.
- Kalatehjari.  R.  (2013).  'An  improvised  three-dimensional  slope  stability  analysis  based  on  limit equilibrium  method  by  using  particle  swarm  optimization.'  PhD  Dissertation,  Universiti Teknologi Malaysia.
- Kalatehjari, R., and Ali, N. (2013). 'A review of three-dimensional slope stability analyses based on limit  equilibrium  method.' Electronic Journal of Geotechnical Engineering, Vol. 18, pp. 119134.
- Kalatehjari, R., Ali, N., Hajihassani, M., and Kholghi Fard, M. (2012). 'The application of particle swarm  optimization  in  slope  stability  analysis  of  homogeneous  soil  slopes.'  International Review on Modelling and Simulations, Vol. 5, No. 1, pp. 458-465.
- Kalatehjari,  R.,  Ali,  N.,  Kholghifard,  M.,  and  Hajihassani,  M.  (2014).  'The  effects  of  method  of generating  circular  slip  surfaces  on  determining  the  critical  slip  surface  by  particle  swarm optimization.' Arabian Journal of Geosciences, Vol. 7, No. 4, pp. 1529-1539, 10.1007/s12517013-0922-5.
- Kang, F., Li, J.J., Hu, J. (2006). 'Combined forecasting model for slope stability based on support vector  machines  with  particle  swarm  optimization.'  Rock  and  Soil  Mechanics,  Vol.  27,  pp. 648-652.
- Karaboga,  D.,  and  Basturk,  B.  (2008).  'On  the  performance  of  artificial  bee  colony  (ABC) algorithm.' Applied soft computing. Vol. 8, No. 1, pp. 687-697, DOI: 10.1016/j.asoc.2007.05.007.
- Karaboga, D., and Basturk, B. (2007). 'A powerful and efficient algorithm for  numerical  function optimization: artificial bee colony (ABC) algorithm.' Journal of global optimization. Vol. 39, pp. 459-471.
- Kennedy,  J.,  and  Eberhart,  R.  (1995).  'Particle  swarm  optimization.'  Proceeding  of  the  IEEE International Conference on Neural Networks, Perth, Australia, pp. 1942-1948.
- Khajehzadeh, M., El-Shafie, A., and Taha, M. R. (2010). 'Modified particle swarm optimization for probabilistic  slope  stability  analysis.' International  Journal  of  Physical  Sciences, Vol.  5,  No. 15, pp. 2248-2258.
- Khajehzadeh, M., Taha, M. R., and El-Shafie, A. (2011). 'Reliability analysis of earth slopes using hybrid chaotic particle swarm optimization.' Journal of Central South University of Technology, Vol. 18, No. 5, pp.1626-1637, DOI: 10.1007/s11771-011-0882-4.
- Kitagawa,  S.,  Takenaka,  M.,  and  Fukuyama,  Y.  (2004).  'Recent  optimization  techniques  and applications to customer solutions.' Fuji Electric Journal, Vol. 77, No. 2, pp. 137-141.

- Kuok,  K.K.,  Harun,  S.,  and  Shamsuddin,  S.M.  (2010).  'Particle  swarm  optimization  feedforward neural  network  for  modeling  runoff.'  International  Journal  of  Environmental  Science  &amp; Technology, Vol. 7, No. 1, pp. 67-78, DOI: 10.1007/BF03326118.
- Li,  H.,  Zhong, H., Yan, Z., and Zhang, X. (2012). 'Particle swarm optimization algorithm coupled with  finite  element  limit  equilibrium  method  for  geotechnical  practices.'  Math  Prob  Eng, Article number 498690.
- Li,  L.,  Chi,  S.C.,  and  Lin,  G.  (2005).  'Improved  complex  method  based  on  particle  swarm optimization  algorithm  and  its  application  to  slope  stability  analysis.'  Rock  AND  Soil Mechanics Vol. 26, No. 9, p. 1393.
- Li,  L.,  Chi,  S.C.,  and  Zheng,  Y.M.  (2008).  'Three-dimensional  slope  stability  analysis  based  on ellipsoidal  sliding  body  and  simplified JANBU method.' Rock and Soil Mechanics, Vol. 29, No. 9, pp. 2439-2445.
- Li,  L.,  and  Chu,  X.  S.  (2011).  'An  improved  particle  swarm  optimization  algorithm  with  harmony strategy for the location of critical slip surface of slopes.' China Ocean Engineering, Vol. 25, pp.357-364, DOI: 10.1007/s13344-011-0030-9.
- Li,  L.,  Yu,  G.,  Chu,  X.,  and  Lu,  S.  (2009).  'The  harmony  search  algorithm  in  combination  with particle swarm optimization and its application in the slope stability analysis.' Proceeding of the International Conference on Computational Intelligence and Security, Beijing, China, pp. 133-136.
- Li,  L.,  Yu,  G.M.,  Chen,  Z.Y.,  and  Chu,  X.S.  (2010).  'Discontinuous  flying  particle  swarm optimization algorithm and its application to slope stability analysis.' Journal of Central South University of Technology, Vol. 17, pp. 852-856, DOI: 10.1007/s11771-010-0566-5.
- Li, X.L., and Qian, J.X. (2003). 'Studies on Artificial Fish Swarm Optimization Algorithm based on Decomposition and Coordination Techniques.' Journal of Circuits and Systems, Vol. 1, pp. 1-6.
- Liou, S.W., Wang, C.M., and Huang, Y.F. (2009). 'Integrative Discovery of Multifaceted Sequence Patterns  by  Frame-Relayed  Search  and  Hybrid  PSO-ANN.'  Journal  of  Universal  Computer Science, vol. 15, No. 4, pp. 742-764.
- Lovbjerg,  M.,  Rasmussen,  T.K.,  and  Krink,  T.  (2001).  'Hybrid  particle  swarm  optimizer  with breeding and subpopulations.' Proceeding of the third Genetic and Evolutionary Computation Conference, San Francisco, pp. 469-476.
- Lü,  Z.S.,  Hou,  Z.R.,  and  Du,  J.  (2006).  'Particle  swarm  optimization  with  adaptive  mutation.' Frontiers of Electrical and Electronic Engineering in China, Vol. 1, No. 1, pp. 99-104, DOI: 10.1007/s11460-005-0021-9.
- Mashhadban,  H.,  Kutanaei,  S.S.,  and  Sayarinejad,  M.A.  (2016).  'Prediction  and  modeling  of mechanical  properties  in  fiber  reinforced  self-compacting  concrete  using  particle  swarm optimization  algorithm  and  artificial  neural  network.'  Construction  and  Building  Materials, Vol. 119, pp. 277-287, DOI: 10.1016/j.conbuildmat.2016.05.034.

- Miranda,  V.,  and  Fonseca,  N.  (2002).  'New  evolutionary  particle  swarm  algorithm  applied  to voltage/var control.' 14th Power Systems Computation Conference, pp. 1-6.
- Mowen, X., Zengfu,  W.,  Xiangyu,  L.,  and  Bo,  X.  (2011).  'Three-dimensional  critical  slip  surface locating  and  slope  stability  assessment  for  lava  lobe  of  Unzen  volcano.'  Journal  of  Rock Mechanics and Geotechnical Engineering, Vol. 3, No. 1, pp. 82-89, DOI: 10.3724/SP.J.1235.2011.00082.
- Mowen, X. J. E. (2004). 'A Simple Monte Carlo Method for Locating the Three - dimensional Critical Slip Surface of a Slope.' Acta Geologica Sinica (English Edition), Vol. 78, No. 6, pp. 12581266.
- Najafzadeh,  M.,  and  Tafarojnoruz,  A.  (2016).  'Evaluation  of  neuro-fuzzy  GMDH-based  particle swarm  optimization  to  predict  longitudinal  dispersion  coefficient  in  rivers.'  Environmental Earth Sciences, Vol. 75, No. 2, pp. 1-12, DOI: 10.1007/s12665-015-4877-6.
- Neshat,  M.  (2013).  'FAIPSO:  fuzzy  adaptive  informed  particle  swarm  optimization.'  Neural Computing and Applications, Vol. 23, No. 1, pp. 95-116, DOI: 10.1007/s00521-012-1256-z.
- Neshat,  M.,  Sepidnam,  G.,  and  Sargolzaei,  M.  (2013).  'Swallow  swarm  optimization  algorithm:  a new method to optimization'. Neural Computing and Applications. Vol. 23, No. 2, pp. 429454, DOI: 10.1007/s00521-012-0939-9.
- Ni, Q., Deng, J. (2013). 'A New Logistic Dynamic Particle Swarm Optimization Algorithm Based on Random Topology.' The Scientific World Journal. DOI: 10.1155/2013/409167.
- Poitras,  G.,  Lefrançois,  G.,  and  G.  Cormier.  (2011).  "Optimization  of  steel  floor  systems  using particle  swarm  optimization."  Journal  of  Constructional  Steel  Research,  Vol.  67,  No.  8,  pp. 1225-1231, DOI: 10.1016/j.jcsr.2011.02.016.
- Poli, R., Kennedy, J., and Blackwell, T. (2007). 'Particle swarm optimization.' Swarm intelligence, Vol. 1, No. 1, pp. 33-57, DOI: 10.1007/s11721-007-0002-0.
- Reynolds,  C.W.  (1987).  'Flocks,  herds  and  schools:  A  distributed  behavioral  model.'  ACM SIGGRAPH computer graphics, Vol. 21, No. 4, pp.25-34.
- Robinson, J., Sinton, S., and Rahmat-Samii, Y. (2002). 'Particle swarm, genetic algorithm, and their hybrids:  optimization  of  a  profiled  corrugated  horn  antenna.'  2002  IEEE  Antennas  and Propagation Society International Symposium, pp. 314-317.
- Sadoghi Yazdi, J., Kalantary, F., and Sadoghi Yazdi, H. (2011). 'Calibration of soil model parameters using particle swarm optimization.' International Journal of Geomechanics, Vol. 12, No. 3, pp. 229-238, DOI: 10.1061/(ASCE)GM.1943-5622.0000142.
- Shi, Y., and Eberhart, R.C. (1998). 'A Modified Particle Swarm Optimizer.' Proceeding of the IEEE International Conference of Evolutionary Computation, Piscataway, pp. 69-73.
- Taha, M.R., Khajehzadeh, M., and El-Shafie, A. (2012). 'Application of particle swarm optimization in evaluating the reliability of soil slope stability analysis.' Sains Malaysia, Vol. 41, No. 7, pp. 847-854.

- Toufigh, M.M., Ahangarasr, A., and Ouria, A. (2006). 'Using non-linear programming techniques in determination  of  the  most  probable  slip  surface  in  3D  slopes.' World  Academy  of  Science, Engineering and Technology, Vol. 17, No. 5, pp. 30-35.
- Wan,  S.  (2013).  'Entropy-based  particle  swarm  optimization  with  clustering  analysis  on  landslide susceptibility  mapping.'  Environmental earth sciences,  Vol. 68,  No. 5,  pp.  1349-1366,  DOI: 10.1007/s12665-012-1832-7.
- Wang, G., Li, H., and Chu, X. (2010). 'Slope stability analysis based on harmony search method and particle  swarm  optimization  method.'  Journal  of  Liaoning  Technical  University  (Natural Science Edition), Vol. 29, pp. 208-211.
- Wang, L., Zeng, J., and Xu, L. (2011). 'A decision support system for substage-zoning filling design of  rock-fill  dams  based  on  particle  swarm  optimization.'  Information  Technology  and Management, Vol. 12, No. 2, pp. 111-119, DOI: 10.1007/s10799-011-0092-7.
- Wang, S.N., Shi, C., Zhang, Y.L., Chen, K.H. (2013). 'Numerical limit equilibrium analysis method of slope stability based on particle swarm optimization.' Appl Mech Mater, Vol. 353, pp. 247251, DOI: 10.4028/www.scientific.net/AMM.353-356.247
- Wen-Tao, M.A. (2009). 'Evaluation of rock slope stability based on PSO and LSSVM.' Rock and Soil Mechanics, Vol. 30, No. 3, pp. 845-848.
- Windisch,  A.,  Wappler,  S.,  and  Wegener,  J.  (2007).  'Applying  particle  swarm  optimization  to software testing.' Proceeding of 9 th Annual  Conference  on Genetic and Evolutionary Computations, London, UK, pp. 1121-1128.
- Xing, J., Jiang, A., and Qiu, J. (2010). 'Studying the adaptive control of tunnel excavation based on numerical simulation and particle swarm optimization.' ICCTP 2010: Integrated Transportation Systems-Green Intelligent Reliable, pp. 3117-3125.
- Xu, F., Xu, W. Y., Liu, Z.  B.,  and  Liu, K. (2011). 'Slope  stability  evaluation  based  on  PSO-PP.' Chinese Journal of Geotechnical Engineering, Vol. 33, No. 11, pp. 1708-1715.
- Xu,  J.,  and  Zeng,  Z.  (2010).  'Applying  optimal  control  model  to  dynamic  equipment  allocation problem: case study of concrete-faced rockfill dam construction project.' Journal of Construction Engineering and Management, Vol. 137, No. 7, pp. 536-550, DOI: 10.1061/(ASCE)CO.1943-7862.0000325.
- Yagiz,  S.,  and  Karahan,  H.  (2011).  'Prediction  of  hard  rock  TBM  penetration  rate  using  particle swarm optimization.' International Journal of Rock Mechanics and Mining Sciences, Vol. 48, No. 3, pp. 427-433, DOI: 10.1016/j.ijrmms.2011.02.013.
- Yamagami, T., and Jiang J.C. (1997). 'A Search for the Critical Slip Surface in Three-dimensional Slope Stability analysis.' Soils and Foundations, Vol. 37, pp. 1-16, DOI: 10.3208/sandf.37.3\_1.
- Yunkai, L., Yingjie, T., Zhiyun, O., Lingyan, W., Tingwu, X., Peiling, Y., and Huanxun, Z. (2010). 'Analysis of soil erosion characteristics in small watersheds with particle swarm optimization, support vector machine, and artificial neuronal networks.' Environmental Earth Sciences, Vol. 60, No. 7, pp. 1559-1568, DOI: 10.1007/s12665-009-0292-1.

- Zhan,  Y.,  and  Wu,  Y.  (2009).  'Recognition  of  Altered  Rock  Based  on  Improved  Particle  Swarm Neural Network.' International Symposium on Neural Networks, Springer Berlin Heidelberg, pp. 149-155.
- Zhang, J.R., Zhang, J., Lok, T.M., and Lyu, M.R. (2007). 'A  hybrid particle swarm optimizationback-propagation  algorithm  for  feedforward  neural  network  training.' Applied  Mathematics and Computation, Vol. 185, No. 2, pp. 1026-1037, DOI: 10.1016/j.amc.2006.07.025.
- Zhang,  Y.,  Gallipoli,  D.,  and  Augarde,  C.  (2013).  'Parameter  identification  for  elasto-plastic modelling  of  unsaturated  soils  from  pressuremeter  tests  by  parallel  modified  particle  swarm optimization.' Computers and Geotechnics, vol. 48, pp. 293-303, DOI: 10.1016/j.compgeo.2012.08.004.
- Zhang, Y., Gallipoli, D., and Augarde, C. (2009). 'Parallel hybrid particle swarm optimization and applications in geotechnical engineering.' Advances in Computation and Intelligence, Springer Berlin Heidelberg, pp. 466-475.
- Zhang,  Y.,  Xiong,  X.,  and  Zhang,  Q.  (2013).  'An  improved  self-adaptive  PSO  algorithm  with detection function for multimodal function optimization problems.' Mathematical Problems in Engineering, DOI: 10.1155/2013/716952.
- Zhao, H.B., and Yin, S. (2010). 'A CPSO-SVM model for ultimate bearing capacity determination.' Marine  Georesources  and  Geotechnology, Vol.  28,  No.  1,  pp.  64-75,  DOI: 10.1080/10641190903359076.
- Zhao,  H.B.,  and  Yin,  S.  (2009).  'Geomechanical  parameters  identification  by  particle  swarm optimization and support vector machine.' Applied Mathematical Modelling, Vol. 33, No. 10, pp. 3997-4012, DOI: 10.1016/j.apm.2009.01.011.
- Zhao, H.B.,  Zou, Z.S., and Ru, Z.L. (2008). 'Chaotic particle swarm optimization for non-circular critical slip surface identification in slope stability analysis.' Proceedings of the International Young  Scholars'  Symposium  on  Rock  Mechanics  -  Boundaries  of  Rock  Mechanics  Recent Advances and Challenges for the 21st Century, Beijing, China, pp. 585-588.
- Zhou, Y.W., Cai, X.J., and Chen, J.B. (2012). 'A new method of simulating arbitrary slip surface in soil slope.' Applied Mechanics and Materials, Vol. 204, pp. 350-353.

## List of Table

Table1 Comparison of metaheuristic methods (Kitagawa et al. , 2004)

## List of Figures

- Fig. 1 Standard flowchart of PSO (Kalatehjari, 2013)
- Fig. 2 Schematic structure of a particle in PSO (Kalatehjari, 2013)
- Fig. 3 Flowchart of PSO to determine the critical slip surface in slope stability analysis (Kalatehjari, 2013)
- Fig. 4 The flowchart of CPSO-SVM to determine the ultimate bearing capacity (Zhao and Yin, 2010)
- Fig. 5 Intelligent displacement back analysis based on PSO and SVM (Zhao and Yin, 2009)

Fig. 6 Combination of PSO and ANFIS techniques for calibration of soil model parameters (Sadoghi Yazdi et al., 2012)

<!-- image -->

Flow chart

<!-- image -->

Flow chart

<!-- image -->

Flow chart

<!-- image -->

Flow chart

<!-- image -->

Flow chart

<!-- image -->

Flow chart

Table1 Comparison of metaheuristic methods (Kitagawa et al. , 2004)

| Methods                                                                                               | GA 1                                                                               | SA 2                                                                                                        | TS 3                                                                                                                                                                                | PSO            |
|-------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------|
| 1970s                                                                                                 | 1983                                                                               | 1989                                                                                                        | 1995                                                                                                                                                                                | Advent         |
| Combinatorial optimization problem                                                                    | Combinatorial optimization problem                                                 | Combinatorial optimization problem                                                                          | Continues optimization problem, Mixed-integer nonlinear optimization                                                                                                                | Target problem |
| Discrete variable                                                                                     | Discrete variable                                                                  | Discrete variable                                                                                           | Discrete variable, Continuous variable                                                                                                                                              | State variable |
| Multi-point                                                                                           | Single point                                                                       | Single                                                                                                      | point Multi-point                                                                                                                                                                   | Search points  |
| Medium                                                                                                | Long                                                                               | Short                                                                                                       | Short                                                                                                                                                                               | Run time       |
| In recent years, application efficacy for multi-objective optimization problems has been under review | A good quality solution can be obtained, but it will require a long amount of time | Good quality solution can be obtained for combinational problems in a shorter amount of time than GA and SA | Good quality solutions can be obtained within a short amount of time for mixed-integer nonlinear optimization problems, for solutions difficult to obtain with conventional methods | Features       |

1 Genetic Algorithm,  2 Simulated Annealing,  3 Tabu Search
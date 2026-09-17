DOI ： 10.11779/CJGE201906005

## 基于非线性 M-C 准则的深埋土质隧道三维塌落破坏 上限分析

于  丽 1，2 ，吕  城 1，2 ，王明年 *1，2

(1. 西南交通大学土木工程学院，四川 成都 610031；2. 西南交通大学交通隧道工程教育部重点实验室，四川 成都 610031)

摘 要 ：围岩条件较差时，深埋土质隧道在隧道开挖过程中容易发生塌方，准确预测深埋土质隧道塌方土体的范围极 其重要，目前能预测深埋土质隧道塌落范围的理论研究不够成熟。为了提前预测土质隧道围岩顶部塌落体的范围，基 于非线性 Mohr-Coulomb 准则和极限分析上限法，推导出深埋土质隧道在三维破坏机制下塌落体的上限表达式，得到 了深埋土质隧道塌落体范围的精确解。通过数值软件 Matlab 绘制出了塌落体的三维形状，研究了各参数对深埋隧道塌 落体形状的影响，并与既有研究进行对比分析，研究结果表明：土体中各参数、隧道顶部圆弧的半径和支护力对深埋 土质隧道塌落体的范围影响比较大；基于非线性 Mohr-Coulomb 准则下深埋土质隧道塌落体的上限分析可以求解出有、 无支护力条件下塌落体的高度和宽度，求解合理、可靠，并能给出防止深埋土质隧道塌方发生的支护力大小，可为隧 道工程设计提供理论依据。

关键词 ：非线性破坏准则；上限分析；三维破坏机制；土质隧道；塌落体

中图分类号： U459 文献标识码： A 文章编号： 1000 - 4548(2019)06 - 1023 - 08

作者简介 ： 于 丽 (1978 - ) ， 女， 辽宁大连人， 副教授， 博士， 主要从事隧道及地下工程研究。 E-mail ： 22643123@qq.com 。

## Three-dimensional upper bound limit analysis of deep soil tunnels based on nonlinear Mohr-Coulomb criterion

YU Li 1, 2 , LÜ Cheng 1, 2 , WANG Ming-nian 1, 2

(1. School of Civil Engineering, Southwest Jiaotong University, Chengdu 610031, China; 2. Key Laboratory of Traffic Tunnel

Engineering, Ministry of Education, Southwest Jiaotong University, Chengdu 610031, China)

Abstract :  When  the  surrounding  rock  conditions  are  poor,  the  buried  earth  tunnel  is  prone  to  collapse  during  the  tunnel excavation process. It is extremely important to accurately predict the extent of the collapsed soil in the deep buried soil tunnel. The theoretical study to predict the collapse range of the deep-buried soil tunnel is not mature enough. In order to predict the extent of the collapse of the surrounding rock of the soil tunnel in advance, based on the nonlinear Mohr-Coulomb criterion and the limit analysis upper bound method, the upper limit expression for the collapse block of the deep-buried soil tunnel under the three-dimensional  failure  mechanism  is  derived,  and the exact  solution to  the extent  of  the  tunnel  collapse is  obtained.  The three-dimensional shape of the collapsed body is drawn by the numerical software Matlab. The influences of various parameters on  the  shape  of  the  buried  tunnel  collapse  are  studied  and  compared  with  the  existing  researches.  The  results  show  that  the parameters in the soil, the radius of the top arc of the tunnel and the supporting pressure have a great influence on the range of the  collapse  block.  Based  on  the  nonlinear  Mohr-Coulomb  criterion,  the  upper  bound  analysis  of  the  buried  earth  tunnel collapse  block  can  solve  the  height  and  width  of  the  collapsed  body  with  and  without  support  force,  and  the  solution  is reasonable and reliable. The proposed method can also give the support force to prevent the collapse of deep-buried soil tunnels, which can provide a theoretical basis for the engineering design of tunnels.

Key words : nonlinear failure criterion; upper bound analysis; three-dimensional failure mechanism; soil tunnel; collapse block

## 0  引    言

随着经济建设的需要，不可避免地修建了大量的 土质隧道，深埋土质隧道围岩条件较差时容易发生土 体塌方。对于土质隧道的破坏模式主要分为 4 种 [1] ：

───────

①局部掉块；②塌穿型破坏；③散体结构崩溃破坏； ④规整的塌落拱破坏。对于深埋土质隧道一般是发生 塌落拱破坏，目前国内外对于深埋隧道土质塌方机制 的理论研究尚不够成熟。扈世民等 [1] 结合现场调研， 通过离散元软件 PFC 2D 模拟了黄土隧道围岩破坏的演 变过程， 得到了深埋隧道稳态塌落拱的形状。 Atkinson 等 [2] 通过极限分析上、下限定理和模型试验研究了无 黏性土质隧道的稳定性，基于一系列模型试验中隧道 围岩的变形特征，构建了无黏性土质隧道的楔形破坏 机制，圆形隧道顶部围岩形成了一个向下滑落的楔形 塌落体，但构建的上限破坏机制过于简单尚不能得到 最优意义的上限解； Mollon 等 [3] 利用空间离散技术建 立了隧道开挖面的三维破坏机制，该破坏机制能够精 确地反映实际工程中隧道的破坏情况，但空间离散技 术过于复杂难以实现。 Fraldi 等 [4-5] 基于 Hoek-Brown 破坏准则构建了一种曲线形破坏机制，通过理论分析 得到了各种断面形式的隧道顶部围岩上限意义下的塌 落面方程，得到了上限意义下的深埋隧道塌落范围， 黄阜 [6] 在 Fraldi 等 [4-5] 研究的基础上构建了圆形和矩形 隧道三维破坏机制研究了深浅埋隧道的塌方，没有考 虑支护力对塌落体的影响，且 Hoek-Brown 破坏准则 发展时间不长，参数在现实中难以确定。 Hoek-Brown 破坏准则适用于岩质基础隧道而不适用于土质隧道， 对于土质隧道只有选择合理的破坏准则才能得到更好 的精确解。

根据工程实际和大量的试验证明，岩土材料的破 坏包络线并不是简单的线性，大多数破坏包络线是非 线性的，线性只是其中的一种。 Zhang [7] 首次将幂函数 非线性破坏准则引入进行岩土工程相关问题的分析， 此后基于非线性破坏准则的应用成为工程问题研究的 热点。 Maksimovicm [8] 、 Li [9] 、 Jiang 等 [10] 做了很多的 研究。 Hoek-Brown 破坏准则适合于岩石基础的工程 问题，对于岩土材料更适合用非线性 Mohr-Coulomb 破坏准则研究相关的工程问题。本文将采用非线性 Mohr-Coulomb 准则基于上限法分析深埋土质隧道的 三维破坏机制， 研究不同参数对深埋隧道塌方的影响， 得到上限意义下深埋隧道塌方宽度和高度的精确解及 防止深埋土质隧道顶部围岩发生塌方的支护力的大 小；将得到的塌落体的高度、宽度与 Fraldi 等 [4-5] 的研 究进行对比，验证了基于上限分析的非线性 Mohr-Coulomb 准则下深埋土质隧道三维塌落机制的 合理性。

## 1  极限分析上限定理简介

根据极限分析上限定理可表述为 [11] ：在任意的运 动许可的塑性应变率场 * ij   和速度场 * i v 中，荷载 Fi 和

2019

Yi 都大于或等于真实的极限荷载，且由虚功率方程确 定：

<!-- formula-not-decoded -->

式中， A 为塑性区， Yi 为作用在研究对象的体力， Fi 为作用在研究对象上的面力， ij  为运动许可速度场中 的应力。

根据极限分析定理的应用条件，对研究的土体材 料和速度场作如下假设 [12] ：①土体材料没有应变软 化、应变硬化特性，即为理想的塑性；②屈服面呈凸 形，塑性应变率可以通过流动法则由屈服函数导出； ③机动速度场中的塌落体是刚性体，忽略极限荷载下 产生的几何变形，可采用虚功原理；④整个机构服从 刚塑性理论，即不发生机构内部几何变形。

## 2  深埋土质隧道塌落面上限分析

## 2.1  非线性 Mohr-Coulomb 准则

非线性 Mohr-Coulomb 准则是用来描述岩土屈服 材料屈服时主应力和切应力之间的非线性关系，由于 其表达形式简单，物理意义明确，被广泛应用在各类 岩土工程问题中 [13-15] 。非线性 Mohr-Coulomb 准则的 表达式如下：

<!-- formula-not-decoded -->

式中 n  ， n  为正应力和剪应力； C 0 为初始黏聚力； t  为轴向拉应力； m 为非线性系数，上述参数均可由 三轴实验得出，当 m =1 时为线性 Mohr-Coulomb 准则 见下式：

<!-- formula-not-decoded -->

材料服从相关流动法则，即塑性势面与屈服面重 合，因此塑性势函数为  ：

<!-- formula-not-decoded -->

根据流动法则，塑性应变增量与塑性势函数的应 力梯度成正比：

<!-- formula-not-decoded -->

式中，  是塑性乘数。

## 2.2  深埋土质隧道三维破坏机制

参考 Fraldi 等 [4-5] 和 Yang 等 [16] 的研究，构建深埋 土质隧道三维破坏机制如图 1 所示，隧道断面几何参 数根据银西高铁驿马一号隧道设计图选取，图 1 中塌

落体的高度为 h ，宽度的一半为 L ， v 为塌落体在机动 速度场中的速率，假设塌落体边界线速度间断线的方 程为 f ( x ) ，从而在 XOZ 面上形成了一个二维拱形塌落 面；然后令曲线 f ( x ) 在空间上绕 Z 轴旋转一周，得到 了一个关于 Z 轴对称的三维塌落体，这个塌落体和它 周围的岩体构成了深埋隧道的三维机动速度场。为了 分析拱形结构对隧道顶部围岩塌落范围的影响，由于 球体的拱形结构与圆柱体形隧道的拱形结构基本一 致，本文将深埋土质隧道顶部围岩的圆柱体简化成球 体进行计算 [6] 。

图1 深埋土质隧道顶部围岩塌落体三维破坏模式图

<!-- image -->

Engineering drawing

Fig. 1 Three-dimensional failure mode of surrounding rock mass collapse at top of deep-buried soil tunnel

由图 1 可知， cot ( ) f x    ，所以可以得到：

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

将式（ 6 ）代入式（ 8 ） ，式（ 8 ）代入式（ 9 ）可 得

<!-- formula-not-decoded -->

式中，  为塌落体和围岩间分离的厚度， v 为机动速 度场中的速率。将式（ 5 ）代入式（ 10 ）可得

<!-- formula-not-decoded -->

## 2.3  基于非线性 Mohr-Coulomb 准则下深埋土质隧道 能耗计算

根据相关联流动法则，塑性势面与屈服面一致且 塑性应变增量与塑性势的应力梯度成正比 [6] 。由极限 分析上限定理可以得到，三维塌落体外表面上任意一

## 点的耗散功率表达式为

n n n n ( ) D          



<!-- formula-not-decoded -->

而塌落体侧面的面积 S 可以按照旋转体侧面积 的计算公式得到：

<!-- formula-not-decoded -->

于是将式（ 12 ）沿着整个塌落体侧面积分可以得 到塌落体表面上由切向应力和法向应力产生的耗散功 率：

<!-- formula-not-decoded -->

曲线 f ( x ) 绕 Z 轴旋转的旋转体被球体截得的空间 几何体的体积可由下式计算：

<!-- formula-not-decoded -->

式中， R 为隧道顶部的圆弧半径， L 为塌落体的底面 半径。因此，重力在塌落体上做功而产生的功率为

<!-- formula-not-decoded -->

式中，  为土体的重度。

隧道围岩顶部支护力

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

为了求出极限状态下构成塌落体的曲面方程的 解析表达式，这里用耗散功率和外力功率之差构建了 一个包含曲线 f ( x ) 方程的目标函数  [16] ：

<!-- formula-not-decoded -->

   将 P D 和 P  的表达式代入式（ 18 ）可得

<!-- formula-not-decoded -->

式中，   ( ), ( ), f x f x x  

<!-- formula-not-decoded -->

  ( ), ( ), f x f x x  



<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

从式（ 19 ）中可以看出，  的极值完全由 ψ 决定， ψ 中的自变量 f ( x ) 本身也是一个函数，且 ψ 是一个泛 函，因此可以根据变分法原理 [17] 求出泛函 ψ 对应的欧 拉方程，将泛函的极值问题转化成求解欧拉方程在满 足边界条件下的定解问题 [16] 。泛函 ψ 对应的欧拉方程 为

<!-- formula-not-decoded -->

将式（ 20 ）代入式（ 21 ）中可以求得 ψ 对应的欧 拉方程：

<!-- formula-not-decoded -->

可以看出，式（ 22 ）是一个常系数非齐次二阶线 性微分方程，可以采用解析方法求其解析解。令

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

采用换元法对其进行降阶处理，令 ( ) f x  = p ，那 么 ( ) f x   =d p/ d x ，则式（ 24 ）变为

<!-- formula-not-decoded -->

式（ 25 ）是一个伯努利方程，这里假设 1 1 m y p   并代入上式得到了一个非齐次的一阶线性微分方程：

<!-- formula-not-decoded -->

显然，由一阶线性微分方程的通解求解可知：

<!-- formula-not-decoded -->

式中， c 为积分常数。由于   1 1 ( ) m y f x    ，可以解出 ( ) f x  的表达式：

<!-- formula-not-decoded -->

从图 1 中可以看出，当 x =0 时， ( ) f x  =0 。因此， 上式中的常数 c =0 ，又结合式（ 26 ） ，则可得到

2019

<!-- formula-not-decoded -->

则图 1 中 XOZ 平面上速度间断曲线 f ( x ) 的解析表 达式可以由式（ 29 ）积分得到

<!-- formula-not-decoded -->

式中， h 是三维塌落体的高度。根据上限定理，令塌 落面上的耗散功率等于外力功率（即 P D= P  + Pc + Pq ） 时得

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

通过 Matlab 软件求出式（ 31 ）中的 L 值，然后 代入式（ 32 ）中得到 h ，再将 h 代入式（ 30 ）中得到 f ( x ) 的表达式， 最后绕 Z 轴旋转得到的旋转曲面方程见 式（ 33 ） ，塌落体的形状可利用数值软件 Matlab 根据 下式绘制出：

<!-- formula-not-decoded -->

## 2.4  影响参数分析

本文方法应用时需要确定隧道围岩顶部圆弧的 半径 R 、非线性系数 m 、初始黏聚力 C 0 、轴向拉应力 t  、土体重度  及支护力 q 。为了明确不同参数对深 埋土质隧道围岩顶部塌落体形状的影响，需要控制单 一参数变化。

首先分析土体物理力学参数对塌落体的影响，令 隧道上部圆弧半径为 R =7.35 m ，非线性系数 m =1 ～ 3 ， 初始黏聚力 C 0=10 ～ 100 kPa ，轴向拉应力 t  =10 ～ 60 kPa ，重度  =15 ～ 23 kN/m 3 ，支护力 q =0 kPa ，塌落体 形状随非线性系数 m 的变化规律如图 2 （ a ）～（ d ） 所示，塌落体的宽度随非线性系数 m 的变化规律如图 3 （ a ）～（ d ）所示。

分析隧道上部圆弧半径 R 对塌落体的影响，令隧 道上部圆弧半径为 R =3 ～ 10 m ，非线性系数 m =1.2 ，初 始黏聚力 C 0=25 kPa ，轴向拉应力 t  =60 kPa ，重度  = 17 kN/m 3 ，支护力 q =0 kPa ，塌落体形状随隧道上部圆 弧半径 R 的变化规律如图 2 （ e ）所示，塌落体的宽度 随隧道上部圆弧半径 R 的变化规律如图 3 （ e ）所示。

<!-- image -->

Line chart

2019

图3 不同参数对三维塌落体宽度的影响规律

<!-- image -->

Line chart

Fig. 3 Effects of different parameters on width of three-dimensional slump

分析隧道支护力 q 对塌落体的影响，令隧道上部 圆弧半径为 R =7.35 m ，非线性系数 m =1.2 ，初始黏聚 力 C 0=25  kPa ，轴向拉应力 t  =60  kPa ，重度  =17 kN/m 3 ，支护力 q =0 ～ 60 kPa ，塌落体形状随隧道支护 力 q 的变化规律如图 2 （ f ）所示，塌落体的宽度随隧 道支护力 q 的变化规律如图 3 （ f ）所示。

从图 3 中可以看出，在保持其它参数不变的情况 下，深埋土质隧道塌落体的高度随着非线性系数 m 、 重度  和支护力 q 的增大而减小，随初始黏聚力 C 0 、 隧道围岩顶部圆弧的半径 R 和轴向拉应力 t  的增大 而增大；非线性系数 m =1 时，塌落体顶部为锥形，深 埋土质隧道围岩顶部的塌方往往呈稳定的'塌落拱' ， 可见 m =1 时不符合工程实际情况，而非线性系数 m 越大塌落体顶部越圆滑更符合工程的实际情况。

从图 3 中可以看出，塌落体宽度随非线性系数 m 的变化规律不同于塌落体高度，塌落体宽度随着非线 性系数 m 的增大先增大后减小；塌落体宽度随着轴向 拉应力 t  和初始黏聚力 C 0 的增大而增大，且增大的 速度越来越小； 塌落体宽度随着重度  的增大而减小； 塌落体的宽度随着隧道顶部围岩圆弧半径 R 的增大而 增大，说明隧道开挖尺寸越大围岩顶部发生塌落的风 险越大。塌落体的宽度随着支护力的增大而减小，当 支护力大于 60 kPa 时塌落体宽度近似为 0 ，可见此时 支护力为 60 kPa 时能够防止深埋隧道围岩顶部塌方事 故的发生。

## 3  计算方法验证

为了进一步检验非线性 Mohr-Coulomb 准则下深 埋土质隧道塌落机制上限分析的合理性，取 m =1 即将 非 线 性 Mohr-Coulomb 准 则 转 换 为 线 性 Mohr-Coulomb 准则， m =1 时按照上述方法进行推导 同样可以得到线性 Mohr-Coulomb 准则下的塌落体相 关计算公式。

线性 Mohr-Coulomb 准则下 XOZ 平面上速度间 断曲线 f ( x ) 的解析表达式为

<!-- formula-not-decoded -->

式中， h 是三维塌落体的高度。根据上限定理，令塌 落面上的耗散功率等于外力功率（即 P D= P  + Pc + Pq ） 时得

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

Fraldi 等 [4-5] 构建了隧道围岩顶部为圆形的二维 破坏机制，基于非线性 Hoek-Brown 破坏准则得到了 塌方的高度和宽度计算公式：

<!-- formula-not-decoded -->

式中， c  为岩体的单轴抗压强度， t  为岩体拉伸强度， 令 B =1 ， tan A   ， t / tan c    [4] ，式（ 38 ）可以用 线性 Mohr-Coulomb 准则来表示：

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

由于 Fraldi 等 [4-5] 的研究没有考虑支护力的作用， 下面比较两种计算方法在无支护力作用下不同参数下 结果，当计算参数黏聚力 c =10 ～ 80  kPa ，重度  =16 kN/m 3 ，隧道顶部圆弧半径 R =7.35  m ，内摩擦角 φ = 30 °，计算结果随黏聚力 c 变化关系如图 4 （ a ）所示。

当计算参数黏聚力 c =30 kPa ，重度  =16 kN/m 3 ， 隧道顶部圆弧半径 R =7.35  m ，内摩擦角 φ =10 °～ 40 °，计算结果随黏聚力变化关系如图 4 （ b ）所示。

当计算参数黏聚力 c =30 kPa ，内摩擦角 φ =30 °， 重度  =22  kN/m 3 ，隧道顶部圆弧半径 R =7.35  m ，计 算结果随黏聚力变化关系如图 4 （ c ）所示。

当计算参数黏聚力 c =30 kPa ，内摩擦角 φ =30 °， 重度  =16 kN/m 3 ，隧道顶部圆弧半径 R =3 ～ 9 m ，计 算结果随黏聚力变化关系如图 4 （ d ）所示。

<!-- image -->

Line chart

图4 不同参数变化下计算结果对比

<!-- image -->

Line chart

Fig. 4 Comparison of calculated results under change of different parameters

从图 4 可知：本文方法计算得到的塌落体的宽度 和高度解随不同参数变化的规律和 Fraldi 等 [4-5] 的解随 不同参数变化的规律是一致的，塌落体的宽度和高度 随着内摩擦角和重度的增大而增大，随着黏聚力和隧 道顶部圆弧半径的增大而减小，且本文方法的宽度和 高度解均大于 Fraldi 等 [4-5] 的解，根据计算结果本文方 法的解比 Fraldi 等 [4-5] 的解增大的百分比为 10.0% ～ 30.8% ，可见本文方法的解是更加安全的，基于三维 破坏机制进行的隧道支护结构设计能够有效减小隧道 顶部塌方发生的概率。 Fraldi 等 [4-5] 的只能应用于岩质 基础的隧道， 且 Hoek-Brown 破坏准则发展时间不长， 相关参数在现实中难以确定，本文方法中应用的非线 性 Mohr-Coulomb 破坏准则的参数在实际工程中容易 获取，为预测深埋土质隧道围岩顶部塌方范围提供了 理论依据。

## 4  结    论

本文基于非线性 Mohr-Coulomb 准则，采用三维 破坏机制对深埋土质隧道的塌落体进行上限分析，研 究了单一参数变化对塌落体形状的影响，得到了如下 结论：

（ 1 ） 基于非线性 Mohr-Coulomb 准则和上限分析 构建了深埋土质隧道的三维破坏机制，通过理论推导 得到深埋隧道顶部围岩三维塌落面的表达式，利用数 值软件 Matlab 绘制出深埋隧道塌落面的三维图形， 本 文方法可得到有无支护力条件下塌落体的高度、宽度 及防止深埋隧道塌方发生的支护力数值。

（ 2 ）在保持其它参数不变的情况下，深埋土质隧 道塌落体的高度随着非线性系数 m 、重度  和支护力 q 的增大而减小，随初始黏聚力 C 0 、轴向拉应力 t  和 围岩顶部圆弧半径 R 的增大而增大。

（ 3 ） 深埋土质隧道塌落体的宽度随着非线性系数 m 的增大先增大后减小；随着轴向拉应力 t  和初始黏

聚力 C 0 的增大而增大，且增大的速度越来越小；塌落 体宽度与重度  的增大而减小；塌落体宽度随着隧道 顶部围岩圆弧半径 R 的增大而增大；随支护力 q 的增 大而减小， 当支护力足够大时可防止塌方事故的发生。

（ 4 ）将本文方法中非线性系数 m =1 时的上限解 和 Fraldi 等的研究进行比较，两种方法的塌落体高度 及宽度随参数的变化规律一致，证明本文的上限解法 正确的、有效的，本文方法的上限解比 Fraldi  and Guarracino 的上限解增大 10% 以上，本文方法预测塌 方范围更安全。

## 参考文献：

- [1] 扈世民 , 张顶立 . 大断面黄土隧道破坏模式离散元分析 [J]. 北京交通大学学报 ,  2013, 37 (4):  13 - 18.  (HU  Shi-min, ZHANG  Ding-li. DEM  analysis of failure modes of surrounding rock for large-section loess tunnel[J]. Journal of Beijing Jiaotong University, 2013, 37 (4): 13 - 18. (in Chinese))
- [2] ATKINSON J H, POTTS D M. Stability of a shallow circular tunnel  in  cohesionless  soil[J].  Géotechnique,  1977, 27 (2): 203 - 215.
- [3] MOLLON G, DIAS D, SOUBRA A H. Face stability analysis of  circular tunnels driven by a pressurized shield[J]. Journal of  Geotechnical  and  Geoenvironmental  Engineering,2010, 136 (1): 215 - 229.
- [4]  FRALDI  M,  GUARRACINO  F.  Limit  analysis  of  collapse mechanisms in cavities and tunnels according to the Hoek-Brown failure criterion[J].International Journal of Rock Mechanics and Mining Sciences, 2009, 46 (4): 665 - 673.
- [5]  FRALDI  M,  GUARRACINO  F.  Analytical  solutions  for collapse mechanisms in tunnels with arbitrary cross sections[J].  International  Journal  of  Solids  and  Structures, 2010, 47 (2): 216 - 223.
- [6] 黄 阜 . 隧道围岩塌落机理与锚杆支护结构的上限分析研 究 [D]. 长沙 : 中南大学 ,  2012.  (HUANG  Fu.  Upper  bound analysis  of  collapsing  mechanism  of  surrounding  rock  and rockbolt supporting structures for  tunnels[D].  Changsha: Central South University, 2012. (in Chinese))
- [7]  ZHANG  X  J,  CHEN  W  F.  Stability  analysis  of  slopes  with general nonlinear failure criterion[J]. International Journal for Numerical and Analytical Methods in Geomechanics, 1987, 11 (1): 33 - 50.
- [8] MAKSIMOVICM. A family of nonlinear failure envelopes for

2019

non-cemented soils and rock discontinuities[J]. The Electronic Journal of Geotechnical Engineering, 1996(1): 1 - 62.

- [9] LI  X.  Finite element  analysis  of  slope  stability  using  a nonlinear  failure  criterion[J].  Computers  and  Geotechnics, 2007, 34 (3): 127 - 146.
- [10]  JIANG  J  C,  BAKER  R,  YAMAGAMI  T.  The  effect  of strength envelope nonlinearity on slope stability computations[J]. Canadian Geotechnical Journal, 2003, 40 (2): 308 - 325.
- [11] 杨 峰 , 阳军生 . 浅埋隧道围岩压力确定的极限分析方法 [J]. 工程力学 ,  2008(7):  179 - 184.  (YANG  Feng,  YANG Jun-sheng. Limit analysis method for determination of earth pressure on shallow tunnel[J]. Engineering Mechanics, 2008(7): 179 - 184. (in Chinese))
- [12] 黄 阜 , 杨小礼 , 黄 戡 , 等 . 考虑孔隙水压力效应和非 线性破坏准则的浅埋地下洞室支护力上限分析 [J]. 岩土工 程学报 ,  2011, 33 (12):  1903 - 1909.  (HUANG  Fu,  YANG Xiao-li,  HUANG  Kan,  et  al.  Upper  bound  solutions  of supporting  pressure  of  shallow  cavities  subjected  to  pore water pressure based on nonlinear failure criterion[J]. Chinese  Journal  of  Geotechnical  Engineering,  2011, 33 (12): 1903 - 1909. (in Chinese))
- [13]  JIANG  J  C,  BAKER  R,  YAMAGAMI  T.  The  effect  of strength envelope nonlinearity on slope stability computations[J]. Canadian Geotechnical Journal, 2003, 40 (2): 308 - 325.
- [14]  ZHANG X J, CHEN W F. Stability analysis of slopes with general nonlinear failure criterion[J]. International Journal for Numerical and Analytical Methods in Geomechanics, 1987, 11 (1): 33 - 50.
- [15]  YANG  X  L,  YIN  J  H.  Estimation  of  seismic  passive  earth pressures with nonlinear failure criterion[J]. Engineering Structures, 2006, 28 (3): 342 - 348.
- [16] YANG X L, HUANG F. Three-dimensional failure mechanism  of  a  rectangular  cavity  in  a  Hoek-Brown  rock medium[J]. International Journal of Rock  Mechanics  &amp; Mining Sciences, 2013, 61 (10): 189 - 195.
- [17] 樊 涛 . 非线性非保守系统弹性力学拟变分原理研究 [D]. 哈尔滨 : 哈尔滨工程大学 , 2007. (FAN Tao. Research on the quasi-variational principles in nonlinear  non-conservative elasticity[D].  Harbin:  Harbin  Engineering  University,  2007. (in Chinese))
## 하이브리드 섬유보강 쉴드터널 라이닝의 온도의존적 열전도도 추정

An Estimation of the Temperature-dependent Thermal Conductivity for Hybrid-fiber Reinforced Shield Tunnel Lining

이 창 수 1)

김 용 혁 2)*

Lee, Chang Soo Kim, Yong Hyok

## Abstract

This  study  presents  estimation  method  of  temperature-dependent  thermal  conductivity  by  using  solution  of  inverse heat  conduction  problem.  Time  and  depth  temperature  distribution  data  from  full-scale  fire  test  were  used  for  estimating temperature-dependent  thermal  conductivity  on  hybrid-fiber  reinforced  shield  tunnel  lining.  At  short  heating  time, estimated  thermal  conductivity  sharply  decreased  within  100℃.  On  the  other  hand,  it  reflected  thermal  properties  of concrete  and  effect  of  steel  fiber  at  heating  time  of  measured  maximum  heating  temperature.  Thus  arbitrary  time  should be  determined  to  estimate  temperature-dependent  thermal  conductivity  in  time  zone  of  measured  maximum  heating temperature. Estimated temperature-dependent thermal conductivity is similar to results of other study.

Keywords : Hybrid-fiber  reinforced  shield  tunnel  lining,  Inverse  heat  conduction  problem,  Temperature-dependent  thermal conductivity

## 1. 서 론

터널 내에서의 화재는 터널 내부의 온도를 단시간에 고 온으로 상승시켜 구조물의 손상을 유발한다. 특히 구조체 역할을 하는 쉴드터널 라이닝의 경우에는 화재에 의해 더 욱 심각한 피해가 발생할 수 있다. 콘크리트는 온도에 따 라 물리 ⋅ 화학적 변화가 발생하기 때문에 화재에 의한 콘 크리트의 손상정도를 판단하기 위해서는 구조물 내의 수 열온도를 예측하는 것이 중요하다.

콘크리트의 수열온도는 다양한 기기분석에 의해 예측 이 가능하지만 정확한 수열온도를 파악하는 데는 한계가 있다(김인수, 2002; 장수호 등, 2006). 따라서 콘크리트 의 수열온도를 파악하기 위해서는 기기분석에 의한 평가 와 더불어 콘크리트의 열전도 특성을 반영한 해석적 방법 에 의한 온도분포 예측이 병행되어야 할 필요가 있다.

콘크리트 내부의 온도변화를 예측하기 위한 열전도 해 석에서 콘크리트의 열전도도는 중요한 변수로 작용한다. 상온에서의 콘크리트 열전도도는 1.4~3.6W/m ℃ 의 범위

1) 정회원 , 서울시립대학교 토목공학과 교수

2) 정회원 , 서울시립대학교 토목공학과 박사수료 , 교신저자

에 있다. 그러나 온도가 증가함에 따라 콘크리트 내부에 존재하는 자유수 및 공극수의 증발에 의해 콘크리트의 열 전도도는 급격히 감소한다. 즉 온도변화가 작은 일반적인 조건에서는 온도에 의한 영향을 무시할 수 있지만 화재에 의해 고온에 노출된 콘크리트의 경우에는 열전도도의 온 도의존적 특성은 상당히 중요한 사항이다. 따라서 열전도 해석 시 정확한 온도분포 예측을 위해서는 이러한 콘크리 트의  온도의존적  열전도  특성을  정확히  반영해야  한다 (Cerny et al., 2000; Kodur et al., 2008; Kodur and Khaliq, 2011; Toman and Cerny, 2001).

콘크리트의 열전도도는 정상상태(steady state) 및 비 정상  상태(transient  state)에서의  실험을  통해  측정할 수 있으며, 콘크리트 열전도도의 온도의존성을 고려하기 위해서는 원하는 온도구간에 대해 각각의 온도별 열전도 도를 구해야 한다. 일반적으로 정상상태 측정방법은 온도 상승에 따른 콘크리트의 열전도 특성 변화를 반영하기에 는 적합하지 않아 비정상 상태에서의 측정방법인 비정상 열선법 등이 주로 사용된다(Shin et al., 2002). 하지만

* Corresponding author : anjelmo@uos.ac.kr  02-2210-2271

' 본 논문에 대한 토의를 2012 년 8 월 31 일까지 학회로 보내주시면 2012 년 9 월호에 토론결과를 게재하겠습니다 .

이러한 측정 방법들은 온도에 따른 열전도도를 산출하기 위해서 많은 시간이 소요되며 고온에서 콘크리트의 열전도 도를 측정하기 때문에 장비의 제약도 많이 따른다(Cerny and Rovnanikova, 2002).

이에 본 연구에서는 콘크리트 구조물의 내화성능을 평 가하기 위해 수행되고 있는 화재실험에서 측정된 온도 데 이터를 활용하여 콘크리트의 온도에 따른 열전도도를 간 편하게 추정할 수 있는 방법론을 제안하고자 한다. 이를 위해 콘크리트의 온도의존적 열전도도에 대한 열전도 역 문제(inverse  heat  conduction  problem)의  해를  구하 고,  이를  이창수(2011)의  연구에서  측정된  하이브리드 쉴드터널 라이닝의 시간 및 깊이별 온도분포 결과에 적용 하여 하이브리드 쉴드터널 라이닝의 온도에 따른 열전도 도를 추정하였다.

## 2. 온도의존적 열전도도에 대한 열전도 역문제

콘크리트의 1차원 열전도 방정식은 식 (1)과 같은 비 선형 편미분 방정식으로 정의된다.

<!-- formula-not-decoded -->

여기서,  는 열확산계수(m 2 /s),  는 콘크리트 내부온 도( ℃ ),  는 깊이(m),  는 시간(s)이다.

식 (1)의 열전도 지배방정식을 온도에 대한 상미분 방 정식으로 변환하기 위해 식 (2)의 Boltzmann 변수를 적 용하면 식 (1)의 좌변과 우변은 식 (3), 식 (4)와 같이 정리할 수 있다.

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

따라서 식 (3)과 (4)를 식 (1)에 대입하여 정리하면 식 (5)와 같은 온도에 대한 상미분 방정식을 얻을 수 있다.

<!-- formula-not-decoded -->

한편 온도  는 시간 및 깊이에 대한 온도함수  

를 의미하며 이는 화재실험에서 측정된 데이터를 통해 충 분히 알 수 있다. 이러한 화재실험 데이터를 기초로 식 (5)에 대한 열전도 역문제를 풀게 되면 온도에 따른 열확 산계수인    를 결정할 수 있다. 이에 대한 초기 조건 및 경계조건은 Dirichlet 경계조건인 식 (6)과 같다.

<!-- formula-not-decoded -->

임의의 시간  의 시점에서 대상이 되는 콘크리트 내부의 임 의 온도   에 대한 열확산계수는 식 (5)에서 BoltzmannMatano method를 적용하면 식 (7)과 같이 온도  부터 임의 온도   의 구간에 대한 적분형태의 방정식으로 정리 된다(Glicksman, 2000; Cerny and Rovnanikova, 2002).

<!-- formula-not-decoded -->

식 (7)에서 온도  일 때    는 0에 가까워지므로 식 (7)은 식 (8)과 같이 나타낼 수 있다.

<!-- formula-not-decoded -->

따라서 임의 시간  에서 임의 온도   에 대한 열확산 계수는 식 (9)와 같이 구할 수 있다.

<!-- formula-not-decoded -->

식 (9)는 온도에 따른 열확산계수를 나타내며 콘크리 트의 비열과 밀도를 알고 있다면 온도의존적 열전도도는 식 (10)과 같이 계산할 수 있다.

<!-- formula-not-decoded -->

여기서,    는  임의  온도   에서의 열전도도(W/ m ℃ ),  는 밀도(kg/m 3 ),  는 비열(J/kg ℃ )이다.

이상과 같이 비정상 편미분 열전도 방정식의 역문제에 대한 해를 Boltzmann-Matano method를 이용하여 구 하였다. 따라서 화재시험에 의해 측정된 시간 및 깊이별 온도분포를 측정할 수 있다면 상기와 같은 과정에 의해

온도의존적 열전도도를 추정할 수 있을 것이다.

## 3. 온도의존적 열전도도 추정

## 3.1 하이브리드 섬유보강 쉴드터널 라이닝의 시간 및 깊이별 온도분포

이창수(2011)는 실물모형 화재실험을 통해 일반 쉴드 터널 라이닝과 하이브리드 섬유보강 쉴드터널 라이닝의 내화성능을 비교 ⋅ 평가하였다. 그 중 하이브리드 섬유보 강 쉴드터널 라이닝의 시간 및 깊이별 온도분포를 측정한 결과는 Fig. 1과 같다. 실물모형 내화시험에서 측정된 온도 데이터는 시험체 깊이별(25mm, 50mm, 75mm, 100mm, 250mm)로 매설된 총 32개의 온도게이지 중 시험체 제 작 및 화재시험 중 손상되지 않은 온도게이지의 데이터를 바탕으로 같은 깊이의 온도데이터를 평균한 결과이다.

Fig.  1의 결과에서 실험시간 20분 경에 깊이 100mm 의 위치에서 다소 높은 온도가 나타나고 있다. 이러한 원 인으로는 데이터의 측정 과정에서 발생한 온도게이지와 데이터 로거 간의 노이즈에 의한 영향이며, 온도변화에 의한 하이브리드 섬유보강 쉴드터널 라이닝의 물리 ⋅ 화 학적 변화와는 무관하다. 또한 임의 시간에 대한 깊이별 온도분포 함수는 실험 데이터의 회귀분석을 통해 결정되 기 때문에 100mm 깊이에서 나타난 데이터의 오차는 회 귀분석 과정에서 큰 영향을 미치지는 않는다.

깊이 25mm 위치에서의 최대온도는 가열 후 67분이 경과한 시점으로 370.3 ℃ 까지 상승하였다. 깊이 250mm 위치에서는 실험시간 50분부터 온도가 서서히 상승하기 시작하여 실험시간 60분 이후부터 온도 상승폭이 커지는 것으로 나타났다. 각각의 깊이별 최대온도 결과는 Table 1과 같다.

Fig.  1  Time-Temperature  Curve  for  Hybrid  Fiber  Reinforced Concrete Shield Tunnel Lining

<!-- image -->

Line chart

Table 1 Maximum temperatures with depth

|   Depth(mm) |   Max. Temperature(℃) |
|-------------|-----------------------|
|          25 |                 370.3 |
|          50 |                 255.5 |
|          75 |                 223.2 |
|         100 |                 169.0 |
|         250 |                  70.9 |

## 3.2 임의 시간에 대한 깊이별 온도분포

임의 시간에서의 온도에 따른 열전도도는 식 (10)에 의해 추정할 수 있으며, 이를 위해서는 먼저 임의 시간  에서의 깊이별 온도분포를 결정해야 한다. 따라서 실물모 형 화재실험에서 측정된 시간 및 깊이별 온도분포 데이터 를 기초로 각각의 실험시간에 대한 깊이별 온도를 회귀분 석하여 깊이별 온도분포 함수   를 산정하였다.

실험시간에 대한 깊이별 온도분포는 식 (11)과 같은 지수함수의 형태로 나타낼 수 있다.

<!-- formula-not-decoded -->

여기서,  는 깊이(mm)이며,  ,  ,  는 회귀계수이다. 각각의  실험시간에서  깊이별  온도분포를  회귀분석한 결과는 Table 2와 같다. 회귀분석 결과 결정계수(R 2 )가 대부분 0.99 이상의 값으로 나타나 실물모형 화재실험에 서 측정된 깊이별 온도분포 결과를 매우 유사하게 표현하 고 있음을 알 수 있다.

Fig. 2는 Table 2의 회귀분석 결과와 실물모형 화재실 험에서 측정된 깊이별 온도를 나타내는 것으로 실험시간 40분까지는 깊이 25mm 위치에서만 온도가 급격히 상승 하여 깊이 25~50mm 사이의 온도 차이는 최대 164 ℃ 까 지  발생하였다. 하지만 깊이 50mm 이후의 위치에서는 온도차이가 가열시간 5분에서 최대 0.5 ℃ ,  실험시간 40

Table 2 Results of regression analysis

|   Time(min.) | Depth-Temperature Function       |    R 2 |
|--------------|----------------------------------|--------|
|            5 |   exp    | 0.9999 |
|           10 |   exp    | 0.9999 |
|           20 |   exp    | 0.9969 |
|           30 |   exp    | 0.9911 |
|           40 |   exp    | 0.9897 |
|           50 |   exp    | 0.9899 |
|           60 |   exp    | 0.9907 |
|           67 |   exp    | 0.9925 |

Fig. 2 Results of full-scale fire test and regression analysis

<!-- image -->

Line chart

분에서는 최대 24 ℃ 로 온도 차이가 크게 발생하지 않았 다. 이러한 결과는 하이브리드 섬유보강 쉴드터널 라이닝 의 가열면 부근에서만 열전도가 일어나고 있음을 의미한 다. 한편 가열시간 50분 이후부터는 깊이 50~250mm 위 치에서도 온도가 상승하고 있어 하이브리드 섬유보강 쉴 드터널 라이닝의 전체에 걸쳐 열전도가 진행되고 있는 것 으로 판단된다. 이러한 실험시간에 따른 깊이별 온도분포 특성은 온도의존적 열전도도를 추정하는 데 영향을 줄 수 있다. 즉 실험시간 40분까지는 깊이 25~50mm 사이에서 만 큰 온도차이가 발생하기 때문에 열전도도가 낮게 추정 될 수 있으나, 50mm 이후에서는 온도변화가 작기 때문 에 상대적으로 높은 열전도도가 계산될 수 있다. 따라서 온도의존적 열전도도를 추정하기 위해서는 콘크리트 전 체에 충분한 열전도가 이루어지는 실험시간대를 결정하 는 것이 중요하다.

## 3.3 실험시간의 영향

실험시간에 대한 깊이별 온도분포 함수를 회귀분석한 결과, 온도의존적 열전도도를 추정함에 있어 임의의 실험 시간이 열전도도의 계산결과에 영향을 줄 수 있다는 것을 예상할 수 있었다. 이를 검토하기 위해 실험시간별로 하 이브리드 쉴드터널 라이닝의 온도의존적 열전도도를 추 정한 결과는 Fig. 3 및 4와 같다. 콘크리트의 깊이별 내부 온도 분포 형태가 깊이 250mm로 갈수록 온도 차이가 작 아지기 때문에 식 (10)의 적분항도 0에 가까워진다. 이에 상온에  가까운  온도영역에서는  열전도도가  급격히  0에 근접하는 결과를 보인다. 하지만 이러한 결과는 실물모형 화재실험 시 상온(26 ℃ )을 기준으로 약 30 ℃ 의 온도차 이내에서 급격히 감소하는 것으로 온도에 따른 콘크리트 의 열전도도를 추정하는 데 있어 고려할 필요가 없는 값 들로 판단된다(Cerny et al., 2000).

Fig. 3은 실험시간 5분, 10분, 20분, 30분 및 40분에

Fig. 3 Estimated thermal conductivity of hybrid-reinforced shield tunnel lining within 40minutes of heating time

<!-- image -->

Line chart

<!-- image -->

Scatter plot

Fig. 4 Estimated thermal conductivity of hybrid-reinforced shield tunnel lining within 67minutes of heating time

서의 온도에 따른 하이브리드 섬유보강 쉴드터널 라이닝 의 열전도도를 추정한 결과이다. 깊이 50mm 이상의 온 도 변화가 거의 없는 위치에 해당되는 수열온도 100 ℃' 이하에서는 최대 열전도도가 8.0W/m ℃ 로 매우 큰 반면 수열온도 100 ℃' 이상에서는 열전도도가 0.8W/m ℃' 이하 로 낮은 값을 보이고 있다. 즉 상온에 가까운 영역에서의 열전도도는 과다하게 추정되어지며 가열면에 가까운 위 치인 수열온도 100 ℃' 이상에서는 급격히 감소하는 경향 을  보인다.  따라서  실험시간이 짧은 시점에서는 가열면 부근에서만 열전도가 일어나기 때문에 온도변화에 따른 콘크리트의 열전도 특성을 제대로 반영하지 못해 콘크리 트의 열전도도에 큰 편차가 발생할 수 있다.

Fig. 4는 실험시간 50, 60분 및 깊이 25mm에서 최대 온도가 측정된 실험시간 67분에 대한 하이브리드 섬유보 강 쉴드터널 라이닝의 열전도도를 추정한 결과이다. 수열 온도 100 ℃' 이하에서 급격하게 감소한 Fig. 3의 결과와 는 달리 실험시간 50분 이후의 시점에서는 상온에서 약 400 ℃ 의 수열온도 범위에서 열전도도가 감소하고 있으 며,  수열온도 400 ℃' 이후에는 열전도도의 변화가 크지 않는 것으로 추정되었다. 깊이 250mm 위치에서 온도가 상승하기 시작한 시점인 실험시간 50분의 경우에는 Fig. 3의 결과에서처럼 상온 영역에서 열전도도가 급격히 감 소하는 경향이 나타나고 있으나 최대온도가 측정된 67분 에 가까울수록 상온 영역에서의 이러한 경향은 추정되지 않는다.

온도에 따른 콘크리트의 열전도도 변화는 콘크리트 내 에 존재하는 수분 변화에 기인한다. 수열온도가 상승함에 따라 콘크리트 내에 존재하는 자유수 및 공극수가 증발하 여 수열온도 400 ℃ 까지는 콘크리트의 열전도도가 감소 하며, 400~500 ℃ 에서는 물리적 흡착수가 해리되는 결과

열전도도가 큰 변화를 보이지 않는다. 이후 500 ℃' 이상 에서는 다시 열전도도가 완만히 감소한다. 이러한 경향은 기존의 연구 결과에서도 유사하게 보고되고 있다(Bazant and Kaplan, 1996; Kodur and Khaliq, 2011; Takeuchi et al., 1993).

또한 하이브리드 섬유에 포함되어 있는 강섬유는 수열 온도 400 ℃' 이상의 온도에서 발생하는 콘크리트 내의 미 세균열을 억제하여 콘크리트의 열전도도 감소를 완화시 킨다(Kodur and Sultan, 2003). 열전도가 깊이 250mm 까지 진행되기 시작하는 실험시간 50분 이후의 시점에서 는 상기와 같은 온도에 따른 콘크리트의 특성변화 및 강 섬유의 효과를 반영하고 있는 것으로 판단된다. 따라서 온도의존적 열전도도의 추정 방법을 적용하기 위해서는 실험시간의 결정이 중요하며, 최적의 결과를 추정하기 위 해서는 가열면 부근에서의 수열온도가 최대가 되는 시점 을 기준으로 결정해야 될 것이다.

## 3.4 온도에 따른 열전도도 추정 결과

콘크리트의 종류 및 섬유혼입 유무에 따른 콘크리트의 온 도의존적 열전도도 예측모델은 Fig. 5와 같이 여러 연구자 들에 의해 제시되었다(ASCE, 1998; Eurocode2, 2004; Kodur and Sultan, 2003; Kodur et al., 2008; Kodur and Khaliq, 2011; Lie and Kodur, 1996; Shin et al., 2002).  ASCE의 예측모델은 보통강도 콘크리트에 대한 모델이며 Eurocode2에서 제시하고 있는 모델은 콘크리 트의  구분없이  상한값과  하한값으로만  정의하고  있다. Lie  and  Kodur(1996)와  Kodur  and  Sultan(2003)의 예측모델은 강섬유를 혼입한 콘크리트를 사용하였으나 강 도의 차이가 있으며, Kodur 등(2011)은 설계강도 80MPa

Fig.  5  Thermal  conductivity  of  concrete  to  be  predicted  by different models`

<!-- image -->

Line chart

<!-- image -->

Line chart

Fig.  7  Decreasing  trend  of  therm al  conductivity  for  varied  fiber reinforced concrete

<!-- image -->

Line chart

Fig.  6  Comparison  of  this  study  and  other  studies  for  therm al conductivity

<!-- image -->

Scatter plot

의 고강도 하이브리드 섬유보강 콘크리트에 대해 온도의 존적 열전도도 예측모델을 제시하고 있다.

콘크리트의 열전도도는 콘크리트의 배합비, 사용골재 및 함수량 등과 열전도도 측정을 위한 시험방법, 시험조 건, 시험체 크기 및 사용장비 등에 따라 상이한 결과가 나 타난다(김국한 등, 2001; Kim et al., 2003; Schneider, 1988). 따라서 본 연구에서 제안한 온도의존적 열전도도 추정방법의 적용성을 검토하기 위해서는 실물모형 화재 실험에서 사용된 하이브리드 섬유보강 쉴드터널 라이닝 에 대해 추가적인 온도별 열전도도 실험을 수행하여 비교 해야 한다. 하지만 고온영역에서의 콘크리트 열전도도를 측정하기 위한 장비의 제약으로 인해 본 연구에서는 기존 의 연구결과를 바탕으로 비교를 하였다.

Fig. 6은 최대 수열온도가 측정된 시점인 실험시간 67 분에서의 추정된 열전도도를 기존의 연구결과와 비교한 것이다. 음영으로 표시된 부분은 Fig. 5와 같이 기존 연구 자들이 제시한 온도에 따른 열전도도값의 범위를 나타낸

Fig.  8  Comparison  between  estimated  thermal  conductivity  and other study for hybrid-fiber reinforced concrete

다. 본 연구에서 추정된 온도의존적 열전도도는 기존 연 구결과의 범위에서 크게 벗어나지 않는 것으로 나타났다. 또한 섬유혼입 콘크리트에 대해 온도의존적 예측모델을 제 시한 기존의 연구결과(Kodur and Sultan, 2003; Kodur and Khaliq, 2011; Lie and Kodur, 1996)와 본 연구에 서 추정된 결과는 온도 증가에 따른 열전도도의 감소 경 향이 유사하게 나타나고 있다(Fig. 7).

Fig. 8은 실물모형 화재실험에 적용된 하이브리드 섬유 보강 쉴드터널 라이닝(설계강도 40MPa)과 유사한 배합 을 사용한 김흥열 등(2010)의 연구결과와 본 연구에서 추정한 열전도도를 비교한 결과이다. 김흥열 등(2010)은 설계강도 40MPa의 하이브리드 섬유보강 콘크리트 기둥 에 대해 내화실험을 수행하고 특정 온도에 대한 콘크리트 의  열전도도를  측정하였다.  Fig.  8에서  보면  수열온도 400 ℃ 에서  본  연구에서  추정된  열전도도가  김흥열  등 (2010)의 연구결과 보다 0.47W/m ℃ 가 낮은 열전도도 를 보이고 있다. 이는 실물모형 화재실험에서 사용된 하

이브리드 섬유의 강섬유 혼입량이 20kg/m 3 인데 비해 김 흥열 등(2010)의 연구에서 사용된 하이브리드 섬유의 강 섬유 혼입량은 40kg/m 3 으로 강섬유 혼입량의 차이에 의 한 영향으로 사료된다. 즉, 콘크리트에 비해 매우 큰 열전 도도를 갖는 강섬유로 인해 콘크리트 열전도도는 다소 증 가될 수 있으며, 고온에서 발생되는 미세균열의 제어효과 도 강섬유의 혼입량에 영향을 받기 때문에 나타나는 결과 이다(Lie and Kodur, 1996).

이상과 같이 열전도 역문제를 통해 추정한 하이브리드 섬유보강 쉴드터널 라이닝의 온도의존적 열전도도는 기 존의 연구 결과와 비교하여 유사하게 추정되었다. 따라서 본 연구에서 제안한 콘크리트의 온도의존적 열전도도 추 정방법은 추가적인 열전도도 실험을 수행하지 않아도 화 재실험에서 측정된 시간 및 깊이별 온도분포 결과를 기초 로 실험에 사용된 콘크리트의 온도에 따른 열전도도 예측 이 가능할 것으로 사료된다. 본 연구에서 사용한 시간 및 깊이별 온도분포는 실물모형에 대한 대규모 화재실험으 로 측정된 데이터로 소규모의 실내실험에 비해 환경적 요 인에 영향을 받을 수 있다. 추후 외부 영향인자가 제어된 조건에서의 화재실험 및 열전도도 특성변화에 관한 연구 가 수행된다면 제안한 온도의존적 열전도도 추정방법의 적용성 및 신뢰성 향상을 기대할 수 있다. 본 연구의 결과 는 콘크리트 구조물의 온도의존적 열전도 특성을 평가하 기 위한 기초적 자료로 활용될 수 있을 것이다.

## 4. 결 론

본 연구에서는 실물모형 화재실험에서 측정한 시간 및 깊이별 온도 데이터를 기초로 회귀분석을 통해 실험시간 에 대한 깊이별 온도분포 함수를 결정하고, 열전도에 대 한 역문제의 해를 이용하여 하이브리드 섬유보강 쉴드터 널 라이닝의 온도의존적 열전도도를 추정하였다. 이를 통 해 도출된 결론은 다음과 같다.

- (1) 화재실험을 통해 측정된 시간 및 깊이별 온도 데이 터를 기반으로 Boltzmann-matano method를 이 용한 열전도 역문제의 해를 통해 온도에 따른 콘크 리트 열전도도의 추정이 가능하다.
- (2) 추정된  온도의존적  열전도도는  실험시간이  짧은 시점에서는 상온 영역에서 열전도도의 급격한 감 소가 나타나는 것으로 추정되었으나, 깊이 25mm
3. 위치의 최대온도가 측정된 실험시간대에서는 온도 에 따른 콘크리트의 특성변화 및 강섬유 혼입 효과 를 반영하고 있다.
- (3) 이에 제안한 온도의존적 열전도도 추정방법을 적 용하기 위해서는 적절한 실험시간대의 결정이 중 요하며 본 연구에서는 가열면 부근에서 최대온도 가 측정된 시점을 기준으로 추정할 것을 제안한다.
- (4) 온도의존적 열전도도의 추정결과, 기존 연구자들의 콘크리트 종류별 온도에 따른 열전도도 측정값의 범위에 들어오며, 유사배합을 사용한 기존연구 결 과와 비교하였을 때 비슷한 결과를 나타내고 있다.
- (5) 내화성능 평가를 위한 화재실험 시 시간 및 깊이별 온도분포를 측정한다면, 별도의 열전도도 측정실 험을 수행하지 않아도 본 연구에서 제안하는 추정 방법을 이용하여 콘크리트의 온도의존적 열전도도 를 간편하게 추정할 수 있을 것이다.

## 참고문헌

1. 김국한, 전상은, 방기성, 김진근, 콘크리트의 열전도율에 관한 실험적  연구 ,  한국콘크리트학회논문집,  제13권  4호,  2001, pp.305-313.
2. 김인수, 국내외 콘크리트 구조물의 화재피해 사례분석 ,  콘크 리트학회지, 제14권 2호, 2002, pp.10-16.
3. 김흥열,  김형준,  전현규,  염광수, 표준화재  재하조건  Fiber Cocktail을  혼입한  고강도  콘크리트  기둥의  전열 특성  및 화 재 거동에 관한 연구 ,  한국콘크리트학회논문집, 제22권 1호, 2010, pp.29-39.
4. 원종필,  최민정,  이수진,  이상우, 도시철도  터널구조체의  내 화안정성 평가를 위한 표준시간-온도곡선 적용 ,  구조물진단 학회지, vol. 14, No. 3, 2010, pp.118-122.
5. 이창수, 콘크리트 쉴드 터널 라이닝의 내화성능 평가 ,  한국 방재학회논문집, 제11권 5호, 2011, pp.105-113.
6. 장수호, 윤태국, 최순욱, 배규진, 화재로 인한 터널 구조물의 피 해와 대책 ,  한국지반공학회지, vol. 22, No. 3, 2006, pp.7-19.
7. ASCE,  Structural  Fire  Protection,  Manual  No.78,  ASCE Committee  on  Fire  Protection,  Structural  Division,  American Society of Civil Engineers, New York, 1992.
8. Bazant,  Z.  P.,  Kaplan,  M.  F.,  Concrete  at  temperatures. material  properties  and  mathematical  models,  Longman, Essex, England, 1996.
9. Cerny, R., Madera, J., Podebradska, J., Toman, J., Drchalova,  J.,  Klecka,  T.,  Jurek,  K.,  Rovnanikova,  P., The effect of compressive stress on thermal and hygric properties  of  Portland  cement  mortar  in  wide  temperature and  moisture  ranges ,  Cement  and  Concrete  Research 30, 2000, pp.1267-1276.
10. Cerny, R., Rovnanikova, P., Transport processes in concrete, Spon Press, London, 2002.
11. Eurocode  2,  Design  of  concrete  structures,  Part  1-2: General  rules-Structural  fire  design,  BS  EN  1992-1-2:

2004, 2004.

12. Glicksman,  M.  E.,  Diffusion  in  Solids:  Field  Theory, Solid-State Principles  and  Applications,  Wiley,  New  York, 2000.
13. Kim,  K.  H.,  Jeon,  S.  E.,  Kim,  J.  K.,  Yang,  S.  C., An experimental  study  on  thermal  conductivity  of  concrete , Cement and Concrete Research 33, 2003, pp.363-371.
14. Kodur,  V.  K.  R.,  Dwaikat,  M.  M.  S.,  Dwaikat,  M.  B., High temperature properties of concrete for fire resistance modelling  of  structures ,  ACI  Mater.  J.,  105(5),  2008, pp.517-527.
15. Kodur,  V.  K.  R.,  Khaliq,  W., Effect  of  Temperature  on Thermal Properties of Different Types of High-Strength Concrete , Journal of Materials in Civil Engineering, ASCE, 2011, pp.793-801.
16. Kodur,  V.  K.  R.,  Sultan,  M.  A., Effect  of  Temperature on Thermal Properties of High-Strength Concrete , Journal  of  Materials  in  Civil  Engineering,  ASCE,  2003, pp.101-107.
17. Lie,  T.  T.,  Kodur,  V.  K.  R., Thermal  and  mechanical properties  of  steel-fibre-reinforced  concrete  at  elevated temperatures ,  Canadian  Journal  of  Civil  Engineering,
7. vol.  23,  1996,  pp.511-517.
18. Schneider,  U., Concrete  at  high  temperatures-a  general review ,  Fire  Safety  Journal,  vol.  13,  1988,  pp.55-68.
19. Shin,  K.  Y.,  Kim,  S.  B.,  Kim,  J.  H.,  Chung,  M.,  Jung,  P. S., Thermo-physical properties and transient heat transfer  of  concrete  at  elevated  temperatures ,  Nuclear Engineering and Design 212, 2002, pp.233-241.
20. Takeuchi,  M.,  Hiramoto,  M.,  Kumagai,  N.,  Yamazaki,  N., Kodaira, A., Sugiyama, K., Material properties of concrete and  steel  bars  at  elevated  temperatures ,  Proceedings of  Structural  Mechanics  in  Reactor  Technology(SMiRT 12), 1993, pp.133-138.
21. Toman,  J.,  Cerny,  R., Thermal  Conductivity  of  High Performance Concrete in Wide Temperature and Moisture Ranges ,  Acta Polytechnica, vol. 41, No. 1, 2001, pp.8-10.

(접수일자 : 2012년 3월 12일)

(수정일자 : 2012년 6월  4일)

(심사완료일자 : 2012년 6월  8일)

## 요 지

본 연구는 콘크리트의 열전도 역문제의 해를 통해 온도의존적 열전도도를 추정하는 방법을 제안하였다. 온도의존적 열전도도의 추정은 실물모형 화재실험에서 측정된 하이브리드 섬유보강 쉴드터널 라이닝의 시간 및 깊이별 온도분포 데이터를 이용하였다. 추정된 온도의존적 열전도도는 실험시간이 짧은 시점에서는 상온 영역에서 열전도도의 급격한 감소가 나타나는 것으로 추정되었 다.  반면  깊이  25mm  위치에서 최대온도가 측정된 실험시간대에서는 온도에 따른 콘크리트의 특성변화 및 강섬유 혼입 효과를 반영하고 있다. 따라서 온도의존적 열전도도 추정 시 가열면 부근에서 최대온도가 측정된 시점을 기준으로 실험시간을 결정해야 한다. 추정된 열전도도는 유사배합을 사용한 기존연구와 유사한 결과를 나타내고 있다.

핵심 용어 : 하이브리드 섬유보강 쉴드터널 라이닝, 열전도 역문제, 온도의존적 열전도도
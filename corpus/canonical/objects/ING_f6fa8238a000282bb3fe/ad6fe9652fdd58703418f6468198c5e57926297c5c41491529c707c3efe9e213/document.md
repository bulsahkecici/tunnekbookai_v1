## 지식기반 개념을 이용한 해저터널의 NATM 터널의 라이닝 설계

신춘원 1 ㆍ우승주 2 ㆍ유충식 3 *

1 비회원 , 성균관대학교 글로벌건설엔지니어링학과 석사과정

2 비회원 , 성균관대학교 글로벌건설엔지니어링학과 석사

3

정회원 , 성균관대학교 토목공학과 교수

## A knowledge-based study on design of NATM lining for subsea tunnels

Chunwon Sin 1

2 , Chungsik Yoo 3 *

1 Graduate  Student,  Dept.  of  Global  Construction  Engineering,  Sungkyunkwan  University

2 Master,  Dept.  of  Global  Construction  Engineering,  Sungkyunkwan  University

3 Professor,  Dept.  of  Civil  and  Environmental  Engineering,  Sungkyunkwan  University

ABSTRACT: This paper concerns a study of a knowledge-based NATM tunnel lining design for subsea tunnels. Concept for tunnel automation designing system, the development of Artificial Neural Network based technology of the tunnel design system, the learning process and verification of the technology forecasting member forces were described. The design system is the series of process which can predict segmental lining member forces by ANN(artificial neural network system), analyze suitable section for the designated ground, construction and tunnel conditions using a FEM(finite element analysis). The lining member forces are predicted based on the ANN quickly and it helps designers determine its segmental lining dimension easily.

Keywords:

NATM lining, ANN, Subsea tunnels

초 록: 이 논문에서는 해저터널의 특수성을 고려한 NATM 터널의 라이닝의 설계에 대한 내용을 다루었다. 해저터널 자동화 설계 시스템 개발의 요소기술인 인공신경망(Artificial Neural Network) 기반의 터널 설계 시스템에 대한 개념, 학습과정 및 검증과정과 예측된 부재력을 통한 최적 단면 설계에 대한 내용을 기술하였다. 부재력 평가가 정확하게 구현 가능한 인공신경망을 개발하기 위해서 다양한 설계 조건과 각 조건에 따른 해석 모델을 이용한 유한요소해석을 수행하여 단면 설계에 필요한 최대부재력의 학습DB를 구축하고 인공신경망을 통해 일반화하였다. 인공신경망을 이용해 산정된 부재력은 해저 터널의 라이닝 설계 시스템에 적용시켜 빠르고 쉽게 해저터널의 라이닝 설계에 적용이 가능하도록 하였다.

주요어:

NATM 라이닝, 인공신경망, 해저터널

## 1. 서 론

## 1.1 연구 배경 및 목적

토목 공학 기술이 발전함에 따라 초장대 교량 , 터널 등의 시공 및 설계 사례가 늘고 있으며 , 글로벌화로

*Corresponding  author: Chungsik  Yoo

E-mail:  csyoo@skku.edu

Received February  23,  2016; Revised March  10,  2016;

Accepted

March  11,  2016

인한 물리적 ․ 지리적 장애물을 극복하고자 최신 토목 기술들이 적용되고 있는 추세이다 .  Park  et  al.  (2007) 의 해저터널의 조사 및 설계 기술 동향에 따르면 최근 전 세계적으로 교통 수단의 발달과 더불어 해협 등과 같은 지리적 장애물에 대한 극복 수단으로 해상 교량 이나 해저 터널의 수요가 늘고 있으며 이에 대한 타당 성 검토 및 설계 ․ 시공 등의 사례가 늘고 있다 . 이에 부합한 터널 기술의 발달은 해저 터널과 같은 특수 조건에서의 설계 ․ 시공을 가능하게 하고 있으며 실제

로 터키나 일본 , 영국 등의 선진국에서는 해저 터널을 시공 혹은 운용 중에 있다 . 또한 Shin  (2011) 의 해저터 널건설을 위한 주요 기술적과제와 Yoo  and  Choi (2014) 의 인공신경망 기반의 TBM 터널 세그먼트 라 이닝 부재력 평가 등 우리나라에서도 한중 해저 터널 , 한일 해저 터널 등에 대한 타당성 연구가 활발히 진행 되고 있으며 이와 같은 해저 터널에 대한 지속적인 관심과 연구 결과는 추후 제주도 , 중국 및 일본으로의 해저 터널을 통한 육로 연결을 현실로 이루어낼 것으 로 판단된다 . 해저터널은 계획 수립시 장대화 ․ 대단면 화되는 조건으로 인해 여러 가지 터널 시공법 중 건넘 선 구간과 같은 확폭 구간은 기존의 NATM (New austrian  tunnelling  method) 공법을 적용하고 본선구 간은 TBM  (Tunnel  Boring  Machine) 터널로 계획 및 시공되는 것이 일반화되고 있다 .

해저터널에 있어서 공사비의 대부분을 차지하고 있는 것은 지보재로 사용되는 세그먼트 라이닝이며 이에 대한 최적 설계를 빠르게 수행할 수 있다면 투입 인력  및  수반되는  노력을  최소화하여  해저터널 NATM 라이닝의 경제적인 설계 ․ 시공을 가능하게 할 것으로 판단된다 . 유로 코드에서 라이닝 설계 시 설계자는 라이닝에 적용되는 하중들에 대해서 안전측 으로 두께 , 철근배근 등을 결정하고 있다 (European Committee  for  Standardization,  2004). 해저터널의 설계과정에서 설계자는 그 굴착 공법에 따라 목적물 의 지반 조건 , 시공 조건 및 터널 조건을 토대로 이에 적합한 라이닝의 단면과 철근량 등을 경험적인 방법 에 의해 산정한 후 수치해석이나 이론해 등을 이용하 여 부재력을 산출하고 이 부재력에 대한 단면 검토를 수행하여 설계에 대한 적합 여부를 판단하게 된다 (Terzaghi,  1943). 이때 수치해석을 통해 부재력을 산 출하는 방법은 대상구간의 복잡한 지질특성 및 시공 조건을 반영하여야 한다 . 그러나 터널이 해저 조건에 있고 장대화 ․ 대단면화 되는 경우 실제 현장 데이터를 입수하는데 한계가 있고 다량의 지반정보 및 설계정 보를 분석해야하므로 실제적인 해석에 있어서 시간과

비용의 제약을 초래한다 .  Yoo  et  al.  (2005,  2008) 은 IT 기반의 터널 설계를 위한 연구를 수행하였다 . 이러 한 문제를 개선하고 효율적인 터널설계를 수행하기 위하여 해저터널의 굴착 공법에 따른 라이닝 설계의 공통적인 부분을 단순화하고 적정한 단면 DB 를 선정 하여 최적 단면을 설계할 수 있게 함으로써 설계자가 시간과 비용을 절약할 수 있도록 하며 각 공법에 따른 라이닝의 설계를 자동화함으로써 설계자가 쉽고 정확 하게 터널 라이닝의 단면을 결정하도록 하는 로직을 정립하는 데 목적을 두고 있다 . 이러한 지식기반 개념 을 이용한 연구는 Yang and Zhang (1997, 1998) 을 참고하였고 Beale  et  al.  (2013) 과 Garson  (1991) 의 연구를 통해 인공신경망의 정확도를 높이고 예측값과 결과값의 오차범위를 검증하였다 .

## 1.2 연구 내용 및 범위

본 연구에서는 ANN (Artificial  Neural  Network, 인공신경망 ) 을 기반으로 하여 해저터널의 설계 ․ 시공 에 큰 영향을 미치는 라이닝 설계에 대한 로직을 수립 하고 , 설계 인자인 최대부재력에 대해서 정확도 높은 예측 시스템을 구축하는 기초연구를 수행하였다 . 해 저터널에 대한 지반조건 , 시공조건 및 터널조건에 따 른 현장 자료를 통해 부재력을 정확히 예측하여 사용 자가 별도의 수치해석 없이 부재력을 평가하고 라이 닝 설계에 있어서 그 단면을 설계할 수 있도록 하였다 . 이러한 ANN 기반의 부재력 예측 시스템 구축을 위한 이 논문의 연구 내용 및 범위는 다음과 같다 .

## 1.2.1 해저터널 NATM 2 차 라이닝의 해석 DB 구축

해저터널에 있어서 TBM 공법의 적용이 어려운 구난역이나 확폭이 필요한 건넘선 구간의 경우 일부 NATM 공법이 적용될 필요성이 있다 . 이러한 현장 자료를 분석하여 일반화하고 일정 수준의 설계 조건 을 케이스화하여 각 케이스에 대해서 수치해석을 통 한 구조해석을 실시하여 2 차 라이닝 설계에 필요한

최대부재력을 산출하는 것을 목적으로 ANN 을 구축 하였다 . 이 연구는 본선에 대한 TBM 세그먼트 라이닝 의 설계와 연계하여 해저터널 계획시 전체 구간에 대한 터널 라이닝 설계를 일관된 방법으로 시행할 수 있도록 하는 연구가 된다 .

## 1.2.2 라이닝 단면검토 로직의 정립

터널 라이닝 설계에 있어서 원형이나 마제형으로 구성되어 있는 터널 라이닝의 횡단 단면 설계를 위해 단주설계로 단순화하고 이 결과는 실제 원형 설계에 비해 안정적인 설계가 가능하다 .  NATM 에 대한 라이 닝 설계시 정확히 예측된 부재력을 바탕으로 각각의 굴착 공법에 따른 라이닝 설계 로직을 수립하여 경제 적인 라이닝 단면 설계가 가능하도록 연구하였다 . 본 연구에서는 NATM 터널의 라이닝 부재력을 정 확히 예측할 수 있는 ANN 엔진을 구축하고 엔진에 적용되는 입력값이 출력값의 부재력에 미치는 영향 정도를 RSE (Relative Strength  Effect) 와 RI  (Relative Importance) 를 통해 다각적으로 분석하고자 하였다 . 결론적으로 예측된 부재력을 통해 시공성을 고려하여 미리 선정한 단면 DB 를 구축하고 , 단주설계법을 적용 한 구조검토를 통해 설계자가 특정의 해저터널 설계 조건에 있어서 가장 경제적인 단면을 설계하고 그 결과를 쉽게 알 수 있도록 하는데 효과적인 개념을 제시하고자 하였다 . 이와 더불어 본 실제 그 타당성 연구가 진행되고 있는 해남 - 제주간 해저터널의 설계 에 적용하여 실제 해저 터널 설계 ․ 시공 단계에서 단면 의 부재력 산정 및 안정성을 검토하였다 . 검증된 정확 도 높은 부재력 예측과 실제 단면 설계법을 통하여 추후 연구될 해저터널에 대한 BIM 프로그램 등과 연동되어 해저 터널 설계시 사용자가 별도의 구조해 석 없이 원하는 위치의 설계조건을 토대로 경제적인 단면을 정확하고 신속하게 도출할 수 있도록 하는데 효과적으로 적용될 수 있을 것으로 연구하였다 .

## 2. NATM 2차 라이닝의 설계

## 2.1 Winkler 모델을 이용한 2차 라이닝 모델링

해저터널에 있어서 장대 TBM 터널이 주로 고려되 지만 일정 기준 간격의 구난역 설치가 불가피하고 , 구난역 구간의 경우 건넘선 등의 확폭 구간이 존재하 여 일부 구간의 NATM 시공이 불가피하다 . 따라서 NATM 2 차 라이닝에 대해서도 해저 터널의 특수성을 감안한 설계가 필요하다 .  NATM 터널의 라이닝 설계 는 있어서 이완하중의 개념에 의거해서 작용하는 토 압을 추정하고 주변 지반이 일반 구조물과 같이 이완 토압을 지지하도록 설계하고 터널 굴착에 따라 주변 지반의 응력의 재분배에 의해 그 자체로 안정되도록 지보공을 구조 검토한다 . 단면형상이 일정하고 사업 량이 많은 철도터널이나 도로터널에서는 표준설계를 암반등급마다 설정하고 이를 적용하는 경우가 많다 . 단 , 피복두께가 얇은 암반 , 막 장 안정이 곤란 하다고 생 각되는 암반 , 산사 태 지역 , 단 층 파쇄 대에 대해서는 별도의 지보 패턴 을 검토하는 것이 바 람 직하다 . 이와 는 별도로 유한요소법에 의해 해석을 실시하는 경우가 있는데 , 유한요소해석 (Finite  Element  Method,  FEM) 은 터널주변 암반을 작은 요소로 분할하고 그 절 점 에 작용하는 외 력으로부터 변위를 구하고 이 변위로부터 각 요소의 변형 률 , 응력을 산출하는 기법이다 . 대개는 숏크 리트나 록 볼 트 같은 1 차 지보재가 기능 상실시 2 차 지보재로서 터널 대 작용하중에 저 항 하는 개념으 로 2 차 라이닝을 설계한다 . 터널 라이닝 설계시 주로 수정 Terzaghi 암반 이완하중을 적용하여 과업구간의 지반에 적합한 2 차 라이닝의 단면과 철근배근을 결정 하며 단면 구조해석을 위해 수치해석을 실시한다 . 수 정 Terzaghi 암반 이완하중은 적용식 및 사용계수에 따라 다르게 적용되며 과다설계의 경향이 있어 최근 에는 GLI (Ground-Lining Interaction) 모델 을 이용하 여 하중을 산정한다 . 본 연구에서는 NATM 시공이 적용되는 해저터널의 고토피고의 특성을 고려하여

안전측으로 고려하고 토피고에 독 립적으로 계산될 수 있도록 이완하중고에 암반단위중량을 곱 해서 적용 하는 이완하중을 작용 토압으로 고려 했 다 .

## 2.1.1 암반 및 지보의 모델화

터널 굴착시 암반은 특히 터널의 막 장 주변부에서 3 차원적으로 거동하지만 수치해석은 일반적으로 2 차 원에서 수행한다 . 따라서 평면변형 률 모델 을 적용하 며 터널 종 단방향의 해석시에는 주변암반의 탄 성계수 나 굴착에 상당하는 외 력 또는 굴착부분의 탄 성계수 를 변화시키는 방법으로 유사 3 차원 해석을 실시하는 것이 일반적이다 .

## 2.1.2 2 차 라이닝의 모델화

2 차 라이닝은 일반적으로 터널의 변형이 수 렴 된 후 시공되므로 막 장으로부터 떨 어진 위치에서 시공한 다고 가정하면 해석상 응력이 발 생 하지 않 는다 . 그러나 피복두께가 얇거나 상재하중 또는 장기적인 토압 ․ 수 압을 추정해서 해석하며 ,  1 차 지보재가 항 복 했 다는

가정하에 안전측으로 해석을 실시한다 . 이 경우 라이 닝을 다각형의 2 차원 보 요소로 모델 화하고 암반을 용수철로 취 급하며 해석시에는 지반용수철의 방향 및 크 기 , 부 호 에 주의해야 한다 . 이때 라이닝을 직선인 보 요소로 모델링 함에 따라 발 생 되는 오차를 줄 이기 위해 두 요소의 연결각은 5° 를 초과하지 않 도록 하며 라이닝은 측 벽 하부 까 지 모델링 한 후 하부 경계조건 은 힌 지로 수직변위와 수평변위를 구속하였다 .

## 2.1.3 해저터널에서의 설계

해저터널의 NATM 2 차 라이닝 설계에서는 해면 아 래 깊 게 터널을 구축할 경우 터널 내의 용수를 전 영역에 허 용하지 않 으면 라이닝에 큰 수압이 작용하 게 되며 , 복공의 두께가 두 꺼워 지는 문제가 발 생 한다 . 따라서 터널 주변에 주입영역을 설정하고 , 암반의 투 수계수를 낮 게 하여 터널 내 용수량을 감소시키고 작용 수압이 굴착에 의한 이완영역 바 깥쪽까 지만 작 용하도록 해야 한다 . 주입영역의 바 깥쪽 에 작용하는 수압은 주로 주입영역 자체의 개량된 지반으로 지지

<!-- image -->

Engineering drawing

c.  Application  of  Loads d.  Result  of  Beam  Forec

Fig.  1. Flow  of  structural  analysis  modeling

하고 , 암반과 수압의 복합작용 외 력은 터널 내의 1 차 지보재와 2 차 라이닝이 지지하도록 하여 주입 영역을 통과해 터널 내부로 들어오는 용수는 라이닝 배면을 통해 터널 내부로 배출시 켜 라이닝에 작용하는 수압 을 저감시 켜 야 한다 .

## 2.2 지반 및 작용하중 산정

일반적으로 철근 콘크 리트로 구성되는 NATM 터 널의 2 차 라이닝은 구조해석과 단면설계의 순서로 이루어지며 , 작용하중이 구조물에 일으키는 응력과 변형을 구조해석으로부터 구하고 부재단면의 안전을 검토하여 주어진 하중작용에 대해 적합한 단면을 결 정하는 절차로 이루어진다 . 특히 NATM 공법에서 지보재는 주변 원지반과 영구복합구조체로 보고 설계 한다 .

NATM 에서 2 차 라이닝의 단면력을 구하기 위해 수행하는 모델링 은 대개 범용 유한요소해석을 이용하 고 , 터널 2 차 라이닝을 스프 링 이 연속적으로 분 포 하는 Winkler 모 형으로 치 환 하고 , 이러한 스프 링 에 둘 러 싸 여 단순지지되는 2 차 라이닝에 이완하중과 잔류 수압 이 사다리 꼴 등분 포 하중으로 작용하는 것으로 모 사한 다 .  Winkler 스프 링 모델 에서는 터널과 지반의 상 호 작 용을 독 립된 스프 링 으로 치 환 하여 터널 2 차 라이닝을 보로 모델링 한다 .  Winkler 스프 링 모델 의 적절한 적용 을 위해 터널 2 차 라이닝의 곡 선은 모델 의 가정을 충족 할 수 있고 , 스프 링 의 불연속인 배치를 피하기 위해 0.25  m ～ 0.5  m 의 길 이를 같은 미소보로 구성하 고 각 절 점 은 1  m 이격된 가상의 고정 점 과 계산된 지반반력 스프 링 계수를 통해 압축만 작용하는 탄 성연 결이 되도록 한다 .  Winkler 스프 링 모델 에서의 가정은 다음과 같다 .

- 각각의 스프 링 은 독 립적이다 .
- 터널 2 차 라이닝의 전단 변형은 없다 .
- 주변지반의 변형 추이는 1 차원적으로 전달된다 .

## 2.2.1 이완토압과 잔류수압

자중의 경우 콘크 리트 라이닝 설계시 외 력으로 적 용하며 대개 프로그램내에서 자동으로 고려된다 . 토 압은 2 차 라이닝에 직각으로 작용하는 이완하중으로 발 파 이완 하중값을 고려하며 터널경계선에서 제어발 파 를 실시하는 경우 발 파 공으로부터 약 0.5  m 떨 어진 곳까 지 발 파 에 의한 동적 손 상을 받 는 것으로 확인되 었 고 ( Lim ,  1997) 발 파 에 의한 암반 손 상시의 발 파 진동 주 파 수 영역은 약 800  Hz 정도이며 , 이를 근거로 발 파 로 인한 이완영역을 평면변형율 요소를 사용한 2 차원 해석을 실시하여 수치해석적으로 검토시 발 파 하중 입력후 초기에는 소성영역이 점 차로 증가하는 양 상을 보이다가 0.6 초 정도이후부터는 거의 일정한 패턴 의 소성영역이 나타나며 그 크 기는 대 략 천 단부에서 50 cm 정도로 발 생 된다 . 따라서 암반 등급 4 등급 이상의 경우 0.5  m 의 이완하중고를 적용한다 . 작용하는 토압 은 이완하중고 두께의 주변지반의 단위중량을 곱 하여 모델링 한다 .

<!-- formula-not-decoded -->

여기서 ,   :

천 장부 이완토압 (kPa)

  :

이완하중고 (m)

잔류 수압의 경우 배수 층 이 제 기능을 발 휘 하지 못 할 경우를 고려하여 해석에 적용하며 수치해석 결과 부직 포 의 폐색 으로 인한 장래 2 차 라이닝에 예상되는 잔류 수압은 암반 4 등급 이상의 경우 터널 높이의 1/3, 암반 5 등급 이하의 경우 터널 높이의 1/2 을 적용 했 다 . 단면설계시 적용하중의 조합이나 형 태 에 따라 최대단 면력의 크 기나 발 생 위치가 달라지며 , 이 논문에서는 Fig.  2 에서 케이스 7 의 경우가 단면두께에 가장 큰 영향을 미치는 모멘 트가 가장 크 기 때문에 안전측으 로 가장 불리한 형 태 인 케이스 7 의 형 태 를 적용 했 다 . 암반 이완 하중은 수평토압을 터널 높이에 따라 차등 적용하고 , 수평 토압을 균 등하게 적용하여 수치해석

Fig.  2. Load  combination  of  NATM  lining  analysis

<!-- image -->

Engineering drawing

에 적용되는 형 태 이다 . 잔류 수압의 작용 형 태 는 침 투 해석에 의한 형 태 이며 측면 배수기능이 원활한 경우 를 나타 낸 다 .

## 2.2.2 스프링 계수 산정

경계조건에 사용되는 스프 링 계수는 주변지반의 변형 특성을 고려한 Wolfer 이론식을 Table  1 과 같이 사용 했 다 .

Table  1. Theory  of  coefficient  of  subgrade  reaction

| Classification   | Content                                                                                                                                                                        |
|------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Theory           |          ∙            : Coefficient of subgrade reaction  : Modulus of deformation  : Poisson`s ratio  : Radius of the lining  : Length of member |

Table  2. Application  of  temperature  load

| Classification                                                 | Application   | Content                                                                                                                                                                                   |
|----------------------------------------------------------------|---------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Seasonal Temperature Load                                      | ± 15°C        | • Thermal expansion coefficient of concrete α : 1.0 × 10 - 5 • Converted to - 15°C thermal loads •ε : Concrete drying shrinkage (15 × 10 -5 ) Δ t =  α ε =  ×  ×  = - 15°C |
| Load temperature difference between inside and outside surface | ±             | 5°C                                                                                                                                                                                       |
| Drying Shrinkage                                               | -             | 15°C                                                                                                                                                                                      |

## 2.2.3 기타 온도 하중

NATM 터널의 2 차 라이닝 설계에서의 경우 건조수 축 및 온 도하중을 고려하며 터널 종 방향으로 신축이 음을 설치하여 건조수축 및 온 도변화의 영향을 최소 화하도록 계획하여 시공함으로써 그 영향은 무 시하고 횡단면상의 건조수축 및 온 도변화에 의한 영향만을 고려하여  범용  유한요소  프로그램  내의 System temperature 기능을 적용하고 내 ․ 외 면 온 도차 하중은 Temperature gradient 기능으로 고려한다 . 본 연구에 서 적용하는 온 도하중은 Table  2 에 나타 냈 다 .

## 2.2.4 설계시 주요 고려사항

이전에 언 급한 하중 외 에 균열 에 대한 사용성을 검토해야 하며 , 공용성 측면에서도 라이닝의 역할을 고려해야 한다 . 다음 Table  3 에 2 차 라이닝 설계시 고려사 항 에 대해 나타 냈 고 ,  Table  4 에 주요 고려사 항 을 나타 냈 다 .

Table  3. Role  of  reinforced  concrete  secondary  lining

| Classification   | Content                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
|------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Performance      | • Less leakage of water and Favorable of watertightness • Inspection and Improvement of repair effectiveness                                                                                                                                                                                                                                                                                                                                                                                                            |
| Strength         | • Providing binding required for stability of tunnel during construction of the concrete lining without convergence to the deformation of the tunnel • Support the external forces when situation(construction defects) occurred during construction • Improve the safety of the structure uncertain factors considered uncertainty factors(Uneven ground, quality degradation of support, depression of primary support) • Increase the durability against deterioration of the supports and change of external forces |

Table  4. Consideration  of  the  secondary  lining  design

| Classification                          | Classification                          | Content                                                                                                                                                                                                                  |
|-----------------------------------------|-----------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Cross section form and Application Load | Cross section form and Application Load | • Consider a tunnel clearance limit and allowance • Secure usability and durability when depressed the primary supports                                                                                                  |
| Design                                  | Stability Check                         | • Application of blasting relaxed load • Consider change of temperature and drying shrinkage                                                                                                                             |
| Design                                  | Prevention Cracks                       | • Reinforcement of small diameter rebar at appropriate intervals • Secure the position of reinforced joints and thickness of cover concrete • Compliance the reinforcement standards(Check spacing of reinforced rebars) |

## 2.3 2차 라이닝 설계 흐름

일반적으로 콘크 리트 구조물의 설계는 구조해석과 단면설계의 순으로 진행되며 작용되는 하중이 구조물 에 일으키는 응력과 변형을 구조해석으로부터 구하고 부재단면의 안전을 검토하여 주어진 하중작용에 대해

적합한 단면을 결정하는 절차로 진행된다 .  Fig.  3 에 2 차 라이닝의 설계 흐름 도를 나타 냈 다 .

Fig.  3 의 흐름 도를 따라 2 차 라이닝 단면계획에 의해 선정한 대표단면과 지반조건을 고려하여 계산한 네 가지 적용하중을 이용하여 NATM 라이닝을 모델 링 하고 구조해석을 수행하였다 . 사용된 유한 요소 프

Fig.  3. Flow  of  NATM  secondary  lining  design

<!-- image -->

Flow chart

로그램은 Midas civil  2012+(Midas,  2012) 이며 터널 을 빔 요소로 고려하는 빔 스프 링 모델 을 적용하였다 . 대표단면의 2 차 라이닝 단면도를 빔 스프 링 의 왜곡 된 거동을 피하기 위해 0.25 ～ 0.5  m 가 되도록 절 점 을 분할하여 모델링 후 2.2 장에서 설 명 한 산정이론식을 따라 계산하여 스프 링 계수를 Elastic  Link 로 적용한 다 .  2 차라이닝에 작용하는 하중은 이완하중으로 계산 한 토압과 잔류 수압으로 계산한 수압을 각각 적용하 였다 . 자중은 프로그램 자체적으로 적용되도록 하고 , 온 도하중은 건조수축 , 내 외 면 온 도차 하중 , 계절별 온 도하중을 적용하여 유한요소해석을 위한 준비를 마 친 다 . 해석 결과 중 Beam Force 를 선 택 하여 최대부재력 ( 모멘 트 , 축력 , 전단력 , 사용 모멘 트 ) 을 추출한다 .

## 3. ANN 기반의 해저터널 NATM의 라이닝 단면력 산정 및 최적 설계

## 3.1 ANN 기본 배경

인간이 가지고 있는 신체 기능의 대부분은 신경세 포 (Neuron) 들의 유기적 결합체인 신경망에 의해 통제 된다 . 신경망의 중추인 뇌 에 대한 그 동안의 연구 결과는 뇌 의 복잡한 구조적인 특 징 과 신 호처 리 체계 를 연구하여 고난도의 실제 문제들을 단순화하여 해 결하는 연산기법을 개발하는 방식으로 발전되어 왔 다 . ANN 은 이러한 생 물학적 신경망에 모티브 를 두고 발전되어 왔 으며 복잡한 실 생 활의 문제를 그래프 형 태 와 수학적인 알고리 즘 형 태 로 모델링 할 수 있게 되 었 다 .  ANN 은 생 물학적 뉴런 을 모델링 한 유 닛 들과 그 유 닛 들 사이의 가중치 연결들로 구성되며 각 ANN

Fig.  4. Neural  Network

<!-- image -->

Flow chart

모델 에 따라 다 양 한 구조와 독창 적인 학 습 규칙 을 얻 는다 .  ANN 은 은 닉 마 디 라 불리우는 독 특한 구성요 소에 의해 일반적인 통계론과는 다른 차원의 방법이 며 은 닉 마 디 는 인간의 신경세 포 를 모 형화한 것으로 써 , 각 은 닉 마 디 는 입력변수들의 결합을 수신하여 목 표변수에 전달한다 .

## 3.2 ANN의 구조

ANN 에는 여러 가지 다 양 한 모 형이 있다 .  MLP (Multiplayer  Perceptron, 다 층 인식자 ) 신경망 ,  RBF (Radial  Basis  Function, 원형기준함수 ) 신경망 ,  EBF (Elliptical  Basis  Function, 타원형기준함수 ) 신경망의 세가지가 있으며 가장 널리 사용되는 모 형은 MLP 신경망이다 .  MLP 신경망은 입력 층 , 은 닉 마 디 로 구성 된 은 닉층 그리고 출력 층 으로 구성된 전방향 신경망 이다 .

- 입력 층 : 각 입력변수에 대응되는 마 디 들로 구성되어 있다 . 명 목형 (norminal) 변수에 대해서는 각 수준에 대응하는 입력마 디 를 가진다 .
- 은 닉층 : 여러 개의 은 닉 마 디 로 구성되어 있다 . 각 은 닉 마 디 는 입력 층 으로부터 전달되는 변수값들을 비선형함수 (Nonlinear  function) 로 처 리하여 출력 층 또는 다른 은 닉층 에 전달한다 .
- 출력 층 : 목표변수 (Target) 에 대응하는 마 디 들을 갖 는다 . 여러 개의 목표변수 또는 세 개 이상의 수준을 갖 을 경우 여러 개의 출력마 디 가 존재한다 .

## 3.3 ANN의 특징

ANN 은 단순한 기능을 가진 무 수히 많은 신경세 포 또는 처 리소자들이 병렬 연결된 연산구조로 되어 있 다 . 각 신경세 포 는 다른 신경세 포 들과 완전히 독 립적 이며 자신들과 연결된 연결 강 도를 통해 직 접 전달되 는 정보에만 의존하며 다른 정보들과는 무 관하다 . 이 로인해 병렬처 리가 가능하고 연산속도가 빠르다 . 또

한 무 수히 많은 연결 강 도를 가지고 있어 정보의 분산 표현  및 처 리가  가능하다 . 또 , 중복성이 크 므로 fault-tolerant 할 뿐 아니 라 일부 정보로부터 전체를 얻 을 수 있는 연산기 억 (Associative  memory) 특성을 갖 는다 .  ANN 은 학 습 이나 훈련 을 통해 연결 강 도를 조정함으로써 새 로운 정보를 추가하거나 변경할 수 있는 적응 특성도 함께 가지고 있다 .

ANN 은 주어진 문제의 입력 패턴 과 출력 패턴 의 예 를 충 분히 많이 생 성하여 이들의 관계를 추출하며 , 병렬 구조를 가지고 많은 양 의 데이터를 사용하여 학 습 한다 . 이와 같은 특 징 으로 인해 ANN 은 신경 회 로 컴퓨 터로 조직되어 패턴 인식 , 음성인식 , 음성합성 , 자 동 번 역 , 최적화 , 적응제어 , 수치해석 등 많은 분야에 응용되고 있다 .

## 3.4 NATM 공법 적용 구간 모델링 DB 구축 및 설계 ANN 엔진 적용

Fig.  5 는 일반적인 NATM 라이닝의 설계 흐름 과 ANN 엔진을 적용하여 간 편 화된 설계 흐름 을 비교할 수 있도록 제시된 그 림 이다 . 설계조건에 Input  Data 만 확보한다면 하중산정과 구조해석에 소요되는 시간 을 줄 이고 설계자가 간 편 하게 설계단면을 확보할 수

있다 . 구조해석을 대체한 ANN 엔진에서 출력된 최대 부재력의 정확도가 예비설계단면을 선정할 때 가장 중요한 요소 임 을 고려하여 모델링 DB 와 ANN 엔진 구축에 있어서 정확도를 높이는데 중 점 을 두 었 다 .

## 3.4.1 ANN 엔진 구축 과정

Fig.  6 은 NATM 2 차 라이닝 최적 설계를 ANN 엔진을 구축하는 과정에 대한 이해를 돕 기 위한 구축 순서도이다 . 먼저 지반 조건 , 라이닝 제원 , 부재력 등 다 양 한 설계 조건을 고려한 구조해석 case 를 선정 하며 이때 ANN 엔진의 사용성과 정확도를 높이기 위하여 최대최소범위 및 case 간의 다 양 성을 갖 추도록 하였다 . 본 연구에서는 총 80 개의 case 를 선정하였고 선정한 case 의 구조해석을 수행하여 ANN 엔진의 DB 를 구축하였다 . 여기에서 출력 Parameter 인 최대부재 력과 연관성이 깊 다고 판단되는 입력 Parameter 를 검토하여 각각 정 규 화한 후 Matlab 을 활용하여 ANN 엔진을 구축하였는데 이에 대한 자세한 내용은 3.5.3 절에서 다루 었 다 . 구축한 ANN 엔진은 RSE 와 RI 값을 계산하고 임 의의 Validation  Set 으로 검증하여 완성하 였다 . 완성된 ANN 엔진을 통해 출력된 Output 값은 역정 규 화하여 예측한 최대부재력을 산출하는데 활용 할 수 있게 된다 .

Fig.  5. Comparison  of  the  flow  of  NATM  secondary  lining  design  after  applying  the  ANN

<!-- image -->

Flow chart

Fig.  6. Flow  of  building  an  ANN

<!-- image -->

Flow chart

값 중 지반 조건은 해저터널 연구단의 서 울 대학교 연구실적을 참고하여 대표 지반 물성값을 설계 조건 에 따라 Table  6 과 같이 암반 1 등급 ～ 5 등급의 5 가지로 구분하였고 , 추후 연구를 위해 지반조건 확장은 가능 하도록 하였다 . 이는 해저터널에서 NATM 공법을

## 3.4.2 해석 단면 선정

ANN 구성을 위하여 총 80 개의 선정된 설계 조건에 대해 최대 모멘 트 , 최대축력 , 최대전단력 , 최대사용 모 멘 트를 구조해석하고 DB 를 구축하였다 .  ANN 구축에 사용된 입력변수의 범위는 Table  5 에 나타 냈 다 . 입력

Table  5. The  range  of  input  value  considered  for  ANN

| Classification   |   Breadth (m) |   Height (m) |   Lining thickness ( m ) |   Ground Type |
|------------------|---------------|--------------|--------------------------|---------------|
| Max              |          21.2 |        14.45 |                      0.5 |             5 |
| Min              |           9.8 |         8.75 |                      0.2 |             1 |

Table  6. Input  value  for  FEM  analysis

| Ground Type   |     (kN/m 3 ) |     (MPa) |     |    (kPa) |    (  ) |
|---------------|-----------------|-------------|-------|-----------|-----------|
| Rock I        |            26.8 |       35000 |  0.20 |      6000 |        45 |
| Rock II       |            25.7 |       22000 |  0.22 |      2000 |        40 |
| Rock III      |            24.7 |        8000 |  0.24 |       700 |        38 |
| Rock IV       |            23.2 |        1500 |  0.27 |       200 |        27 |
| Rock V        |            21.4 |         400 |  0.30 |        50 |        21 |

Table  7. Load  combination  factor

| Description   | Description   |   Dead Load |   Relaxed Rock Load |   Residual Water Pressure | + Temperature Load   | - Temperature Load   | Drying Shrinkage   |
|---------------|---------------|-------------|---------------------|---------------------------|----------------------|----------------------|--------------------|
| Strength      | C1            |         0.9 |                 0.9 |                       1.6 | -                    | -                    | -                  |
| Strength      | C2            |         1.2 |                 1.6 |                       1.6 | 1.2                  | -                    | -                  |
| Strength      | C3            |         1.2 |                 1.6 |                       1.6 | -                    | 1.2                  | 1.2                |
|               | U1            |         1.0 |                 1.0 |                       1.0 | -                    | -                    | -                  |
|               | Usability U2  |         1.0 |                 1.0 |                       1.0 | 1.0                  | -                    | -                  |
|               | U3            |         1.0 |                 1.0 |                       1.0 | -                    | 1.0                  | 1.0                |

<!-- image -->

Engineering drawing

- a.  Starting  point  (B*H=9800*8750)
- b.  The  widening  A  (B*H=13600*10650)
- c.  The  widening  B  (B*H=17400*12550)

<!-- image -->

Engineering drawing

<!-- image -->

Engineering drawing

Fig.  7. Cross-sectional  drawing  of  NATM  lining  (Unit  :  mm)

<!-- image -->

Engineering drawing

적용하는 구간의 특성 때문인 것으로 , 해저터널의 경 우 구난역이나 환 기시설에 존재하는 확폭구간 즉 TBM 공법의 적용이 불가능한 지역에 한해 국부적으 로 NATM 공법을 적용하기 때문이다 . 해저터널에서 구난역이나 환 기시설 등 확폭구간이 필요한 지 점 은 주로 섬 이나 인공 섬 등 지반 조건이 비교적 양호 한 구간에 해당된다 . 수치해석시 적용한 하중조합은 Table  7 에 나타 냈 다 .  Fig.  7 은 구조해석에 사용한 대표 단면 4 가지에 대한 그 림 을 나타 냈 다 .

## 3.4.3 학습 DB 구축

NATM 2 차 라이닝의 ANN 은 설계 정보를 바탕으

로 하는 터널 폭 , 터널 높이 , 라이닝 두께 및 지반등급 의 4 개 입력값을 정 규 화하여 입력하고 단면 검토를 위한 최대 모멘 트 , 최대 축력 . 최대 전단력 및 최대 사용 모멘 트를 예측함에 있어서 각각의 ANN 을 구성 한다 . 보다 정확한 설계는 터널 라이닝을 천 장부 , 어 깨 부 , 측 벽 부로 구분하여 각 부위에 대한 최대 모멘 트부 와 최대 축력부의 모멘 트 , 축력 및 전단력을 판단하여 각 부위 별로 철근배근을 달리할 수 있으나 본 연구에 서는 단순화된 최대 부재력을 고려하여 정확도를 높 이고자 하였다 .

Fig.  8 에서와 같이 각 해석 조건을 고려하여 이완하 중과 잔류 수압을 정한 후 터널 주변 지반의 등급에

Fig.  8. FEM  analyzing  flow  for  NATM  secondary  lining

<!-- image -->

Flow chart

Table  8. Input  and  Output  parameters

| Input Parameter   | Breadth          |
|-------------------|------------------|
| Input Parameter   | Height           |
| Input Parameter   | Lining thickness |
| Input Parameter   | Ground type      |

| Output    | Max Moment       |
|-----------|------------------|
| Output    | Max Axial Force  |
| Parameter | Max Shear Force  |
| Parameter | Max Using Moment |

따른 지반 반력 계수를 계산하고 수치해석을 수행하 여 단면검토를 위한 NATM 2 차 라이닝의 최대부재력 을 산정하였고 , 산정된 부재력은 ANN 구축시 학 습 DB 로 사용하였다 . 해저터널의 특성을 고려하여 구난 역 혹은 환 기시설에 해당하는 80 개의 학 습 조건을 고 려한 해석 케이스를 선정하였다 . 다음 Table  8 에는 NATM 2 차 라이닝 최대부재력 ANN 구축시 적용되 는 입력값과 출력값을 나타 냈 다 .

## 3.4.4 NATM ANN 구축

ANN. 엔진 구축시 은 닉층 의 수는 1 ～ 10 범위 내에 서 사용되는데 10 에 가 까울 수록 구축된 DB 의 인자에 대해서만 정확한 값을 출력한다 . 본 연구에서는 적합 한 NATM ANN 모델 구축에 사용할 내적인자 수를 결정하기 위해 TBM 세그먼트 라이닝 ANN 구축시 ANN 의 예측치에 대한 RMSE 값의 비교를 수행하였 고 은 닉층 의 뉴런 수는 2 개 , 모멘텀 은 0.8, 학 습률 은

Table  9. Maximum  and  Minimum  sectional  forces  by  ANN

| Classification              |   Maximum value |   Minimum value |
|-----------------------------|-----------------|-----------------|
| Max Moment (   ⋅ )       |           575.8 |            20.8 |
| Max Axial Force (   )     |          4907.8 |           629.1 |
| Max Shear Force (   )     |           260.4 |            27.8 |
| Max Using Moment (   ⋅ ) |           372.1 |            15.5 |

Table  10. Result  of  building  an  ANN

| Classification              |     (Coefficient of determination) |   RMSE (Root Mean Square Error) |   MAE (Mean Absolute Error) |
|-----------------------------|--------------------------------------|---------------------------------|-----------------------------|
| Max Moment (   ⋅ )       |                               0.9770 |                            12.2 |                         8.4 |
| Max Axial Force (   )     |                               0.9614 |                           166.3 |                        13.8 |
| Max Shear Force (   )     |                               0.9880 |                             5.4 |                         4.0 |
| Max Using Moment (   ⋅ ) |                               0.9009 |                            88.3 |                        66.8 |

0.2 를 사용하였다 . 구축한 DB 를 활용하여 학 습 을 수 행한 ANN 은 Input  layer 에 4 개의 입력 뉴런 ,  1 개의 Hidden layer 에 2 개의 은 닉뉴런 ,  Output  layer 에 1 개의 출력 뉴런 으로 구성 했 다 .

먼저 설정된 DB 출력값의 최대 ․ 최소값을 Table 9 에 나타 냈 다 .  Table  10 에서는 결정계수 (   ), 평 균 제 곱 근오차 (RMSE), 평 균 절대오차 (MAE) 등 세 가지 통계변수를 이용해 ANN 의 학 습 평가 결과를 보여주 는데 각 부재력의 최대최소값을 고려하였을 때 오차 범위가 크 지 않 다고 판단된다 .  NATM ANN 의 구축 결과는 다음 Fig.  9 에 나타 냈 다 . 이 학 습 평가 결과는 최대 모멘 트 , 최대축력 , 최대전단력 및 최대사용 모멘 트에 대한 학 습 결과 결정계수 (   ) 가 각각 0.9770, 0.9614,  0.9880,  0.9009 로 나타나 각 최대 부재력에 대한 ANN 예측 값과 학 습 에 사용된 값은 높은 상관관 계를 보여준다 .

Fig.  9. Comparison  of  computed  versus  predicted  values  for  training

<!-- image -->

Scatter plot

## 3.4.5 NATM ANN 민감도 분석

구축된 NATM ANN 에 대해서 TBM 세그먼트에서 와 같은 방법으로 RSE (Relative Strength Effect) 와 RI  (Relative  Importance) 를 분석하였다 .  Fig.  10 에서 는 각 부재력에 대한 RSE 를 나타 냈 고 , 실제 값을 Table  11 에 표시 했 다 .

Table  11 에 나타난 바와 같이 전단력을 제 외 한 경우 터널내측 폭에 가장 큰 영향을 받 는 것으로 검토되 었 다 . 터널 내측 높이에 대해서 최대축력과 모멘 트 , 최대사용 모멘 트는 ( - ) 의 부 호 로 영향 받 는 것으로 나타 났 다 .

추가적으로 RSE 와 마 찬 가지로 각 최대부재력에 대한 구축된 ANN 의 RI 를 검토하여 Fig.  11 에 RI 를

Table  11. RSE  of  Maximum  member  forces

| Classification   | Breadth   | Height   |   Thickness | Ground Type   |
|------------------|-----------|----------|-------------|---------------|
| Max Moment       | 1.000     | - 0.952  |       0.153 | 0.107         |
| Max Axial Force  | 0.731     | - 0.658  |       0.139 | 0.358         |
| Max Shear Force  | - 0.223   | 0.727    |       0.674 | - 0.032       |
| Max Using Moment | 1.000     | - 0.987  |       0.025 | 0.085         |

나타 냈 다 .  RI 는 RSE 와는 다른 방식으로 분석하는 입력값의 결과값에 대한 민 감도 지표로써 RI 분석 결과 지반등급이 모든 최대부재력에 미치는 영향이 큰 것으로 나타 났 으며 라이닝 두께가 가장 적은 것으 로 나타 났 다 . 이는 RSE 의 결과와도 다소 일치하는 것으로 터널이 위치하게 되는 지역의 지반 상 태 가 NATM 2 차 라이닝의 단면 설계에 큰 영향을 미치는 것으로 판단된다 . 또한 향후에는 지반 조건에 대한 분 류 를 통해 다 양 한 지반 조건 중 어 떤 요소가 단면 설계에 큰 영향을 미치는지 연구해보는 것도 좋 을 것으로 사료된다 .

<!-- image -->

Line chart

a.  Max  Moment d.  Max  Using  Moment

<!-- image -->

Line chart

c.  Max  Shear  Force

<!-- image -->

Line chart

b.  Max  Axial  Force

<!-- image -->

Line chart

<!-- image -->

Bar chart

<!-- image -->

Bar chart

a.  Max  Moment b.  Max  Axial  Force

c.  Max  Shear  Force

<!-- image -->

Bar chart

d.  Max  Using  Moment

<!-- image -->

Bar chart

Fig.  10. RSE

Fig.  11. RI

## 3.4.6 NATM ANN 부재력 예측 결과 검증

이 절에서는 NATM ANN 을 이용한 부재력 산정 시스템의 효율을 제고하고 정확도를 검증하기 위해 4 개 케이스를 Validation  set 으로 설정하고 이를 Table 12 에 나타내고 부재력 검증을 수행하여 그 결과를 Table  13 에 나타 냈 다 . 선정된 케이스에서 ANN 의 부 재력 평 균 예측 오차는 최대 모멘 트는 4.6%, 최대축력 은 4.9%, 최대전단력 5.1%, 최대사용 모멘 트 7.4% 로 나타나 실제 예측 수준이 거의 차이가 없음을 알 수 있 었 다 . 최대사용 모멘 트의 경우 일부 경우에 있어서 15% 의 오차 수준을 보이는 것이 있지만 , 최대사용 모 멘 트는 계수하중의 최대 모멘 트보다 크 기가 작고 단 면의 선정에는 고려되지 않 는 요소이며 또한 오차의 절대값 자체가 작은 경우로 실제 단면 설계에는 영향 을 미치지 않았 다 .

Table  12. Input  values  for  ANN  verification

|   Classification |   Breadth (m) |   Height (m) |   Lining thickness (m) |   Ground type |
|------------------|---------------|--------------|------------------------|---------------|
|                1 |          13.6 |        10.65 |                    0.5 |             5 |
|                2 |          17.4 |        12.55 |                    0.5 |             3 |
|                3 |          21.2 |        14.45 |                    0.4 |             2 |
|                4 |          21.2 |        14.45 |                    0.5 |             5 |

Table  13. Maximum  sectional  forces  by  ANN  and  FEM  analysis  for  verification

| Classification         | Classification         | Max Moment (kN·m)   | Max Axial (kN)   | Max Shear (kN)   | Max Use Moment (kN·m)   |
|------------------------|------------------------|---------------------|------------------|------------------|-------------------------|
|                        | FEM                    | 229.1               | 2194.9           | 170.1            | 165.3                   |
|                        | 1 ANN                  | 235.8               | 2371.2           | 164.7            | 190.9                   |
|                        | ERR                    | 3%                  | 8%               | - 3%             | 15%                     |
|                        | FEM                    | 130.0               | 2078.7           | 60.6             | 96.5                    |
|                        | 2 ANN                  | 123.4               | 1866.2           | 56.6             | 92.0                    |
|                        | ERR                    | - 5%                | - 10%            | - 7%             | - 5%                    |
|                        | FEM                    | 100.3               | 1750.1           | 61.9             | 73.5                    |
|                        | 3 ANN                  | 96.2                | 1736.8           | 57.7             | 71.9                    |
|                        | ERR                    | - 4%                | - 1%             | - 7%             | - 2%                    |
|                        | FEM                    | 575.8               | 4907.8           | 260.4            | 372.1                   |
|                        | 4 ANN                  | 539.3               | 4931.8           | 250.3            | 344.8                   |
|                        | ERR                    | - 6%                | 0%               | - 4%             | - 7%                    |
| Average absolute error | Average absolute error | 4.6 %               | 4.9 %            | 5.1 %            | 7.4 %                   |

## 3.5 NATM 2차 라이닝의 설계

NATM 의 2 차 라이닝의 설계는 콘크 리트 구조기준 (2012) 설계법에 따라 하중조합하여 3.5.1 절의 Table 18 과 같은 하중조합을 사용하며 이완하중과 잔류 수압 을 고려한 배수터널로 가정하여 설계하였다 .  NATM 공법 적용 구간은 구난역이나 환 기 시설에 적용되므 로 대부분 섬 에 위치해 있고 토피고가 해저 구간보다 크 고 , 주변 지반이 양호 하여 육상 시공 조건과 비 슷 한 것으로 간주할 수 있기 때문이다 . 최초 무 근 적용성을 검토하여 단면력이 허 용응력 내에 존재하는 경우 무 근 콘크 리트로 설계하며 , 이 외 의 경우 적절한 철근배 근을 계획하였다 . 철근의 피복두께 , 최소간격 , 배력철 근은 설계조건에 맞 는 배근을 고려하며 콘크 리트 구 조기준 (2012) 에 따 랐 다 . 철근배근 가정 후에는 계수

하중에 대하여 천 장부 , 어 깨 부 , 측 벽 부에 대한 구조검 토를 각각 실시하고 사용 모멘 트에 의한 사용성 검토 를 수행하여 가정단면의 적정성 여부를 판단한다 . 사용 성 검토는 구조물 또는 부재가 사용기간 중 기능과 성능을 유지하기 위하여 외 력에 대하여 안전해야 하므 로 사용 하중하에서 사용성 및 내구성을 검토해야 한다 . NATM 의 2 차 라이닝의 설계는 무 근안정성 검토 후 철근보 강 이 필요하다고 판단되면 단면을 가정하고 강 도설계법으로 안정성을 검토 했 다 . 콘크 리트 라이닝 에 철근을 보 강 하지 않 고 무 근으로 설계하기 위해서 는 휨 응력 (      ±    ) 과 전단응력이 콘크 리트의 허 용응력보다 작거나 같 아 야 하며 이에 따른 콘크 리 트의 허 용응력은 Table  14 에 나타 냈 다 . 여기서 사용되 는 강 도감소계수는 무 근 콘크 리트의 휨모멘 트 , 압축 력 , 전단력에 해당되는 0.55 를 사용 했 다 .

강 도설계는 부재의 파괴 상 태 또는 파괴 에 가 까 운 상 태 를 기초로 하는데 이 런 상 태 에 가 까 이 있는 부재 의 강 도를 극한 강 도라 하며 , 기 설 명 된 TBM 세그먼트 라이닝의 설계법과 동일하다 . 강 도검토시 가정단면의 철근에 대해 철근 중심간격과 배력 철근의 설계기준 을 검토해야 한다 . 사용성 검토는 인장철근의 간격 제한으로 균열 을  제어하도록 콘크 리트  구조기준 (2012) 에 개정되 었 다 .

Table  14.

Check  allowable  stress  of  concrete

| Classification                       | Check allowable stress of concrete   |
|--------------------------------------|--------------------------------------|
| Allowable bending compressive stress |              ≤         |
| Allowable bending tensile stress     |           ≤      |
| Allowable bending shear stress       |                       |



## 4. 결론 및 향후 연구 계획

이 논문에서는 해저터널에서 적용되는 NATM 터 널의 라이닝 최적설계 시스템에 관한 내용을 다루 었 다 . 최적설계를 위해 관 련 선행 연구에서 그 적용성이 확인된 바 있는 ANN 을 도입하여 시공 조건 , 지반 조건 및 터널 조건 입력값을 바탕으로 별도의 응용프 로그램 해석 없이 부재력을 정확히 예측하여 단면검 토에 적용될 수 있도록 하였고 , 기 구축된 단면에 대한 구조검토와 그 결과에 따른 라이닝의 최적 단면 선정 로직을 포 함하여 해저터널의 제한된 조건에 대 해 각 굴착 공법에 따른 라이닝의 설계가 가능하도록 하였다 . 구축된 인공신경망은 설계자가 쉽게 터널 라 이닝 설계에 접 근할 수 있을 것으로 기대된다 . 일반적 으로 터널 라이닝의 유한요소해석은 모델링 과 해석에 상당히 많은 시간이 소요되기 때문에 이 논문에서 구축된 ANN 은 사용자에게 시간적 ․ 공간적 제한을 상당부분 해소해 주어 경제적인 라이닝 설계를 가능 하게 할 수 있을 것이라 판단된다 . 또한 향후 해저터널 의 BIM 개발 등의 추가 연구에 있어서 특정 구간의 라이닝 설계와 연동할 수 있을 것으로 기대되며 Input parameter 에 대한 추가적인 연구를 통해 단면의 설계 에 가장 영향이 큰 요소인 지반 조건을 세분화하고 더 정 밀 한 ANN 엔진을 구축하는 연구를 수행할 예정 이다 . 연구의 구체적인 내용은 다음과 같다 .

1. 해저터널의 설계 ․ 시공에 있어서 장대화 됨 에 따라 환 기 및 방재 측면에서 구난역의 필요성이 규 정되 어 있다 . 이에 구난역에서의 시공은 TBM 공법만으 로는 시공성을 확보하기 어 렵 기 때문에 일부 구간 의 NATM 터널이 계획되는 실정이고 ,  NATM 터널 의 개 략 적이 2 차 라이닝 설계를 위한 ANN 을 구축 하였다 . 해저터널의 설계에 있어서 NATM 터널 라이닝의 설계시 추가의 수치해석 없이 정확도 높 은 부재력을 얻 을 수 있어 사용자가 쉽게 적용할 수 있도록 하였다 .

2. ANN 으로 정확히 예측된 최대부재력을 바탕으로 시 공성이 확보된 단면의 DB 를 구축하고 각 단면의 구조 검토를 통하여 해당 단면의 적정성을 평가하였다 .
3. ANN 에 대한 검증 결과 상용유한요소해석 프로그 램을 이용한 부재력 결과와 90% 이상 일치하는 것으로 검증되어 장대화 및 대단면화 된 해저 터널 의 해석 및 설계에 효과가 극대화 될 것으로 기대되 며 , 본 연구로 구축된 ANN 을 통해 가상 터널의 시공조건을 고려한 터널의 라이닝 부재력 평가 및 단면 설계를 가능하도록 하였다 .

본 연구를 통해 해저터널 가상설계에 대한 BIM 과 연동시 켜 추가적인 구조해석이 없이 정확도 높은 ANN 의 예측 부재력을 통해 설계가 가능한 프로그램 의 장 점 을 극대화시키고 , 설계자가 최적화된 세그먼 트 라이닝 단면에 대해 간 편 하고 경제적인 설계가 가능할 것으로 판단된다 . 또한 추후에는 본 연구를 더 욱 발전시 켜 ANN 엔진의 부재력 산출 정확도를 높인다면 추가적인 구조해석 없이 최적단면설계를 가능하게 할 수 있을 것으로 고려된다 .

## 감사의 글

본 연구는 국토교통부 - 국토교통과학기술진 흥 원 - 국 토교통기술연구개발사업 (2013 년 이후 )[52-B991] 의 지원으로 수행되 었 으며 , 이에 깊 은 감사를 드립 니 다 .

## References

1. Beale, M.H., Hagan, M.T., Demuth, H.B. (2013), Neural Network Toolbox User's Guide, Mathwork Inc.
2. European Committee for Standardization, (2004). 'Eurocode 2: design of concrete structures - part 1-1:  general  rules  and  rules  for  buildings'.
3. Garson, G.D. (1991), 'Interpreting neural-network connection  weights',  AI  Expert,  Vol.  6,  No.  7, pp.  47-51.
4. Lim, S.B. (1997), 'Evaluation of dynamic damage adjacent  to  a  blasthole  in  tunnel  excavations', Kyunghee  Univ.  PhD  dissertation.
5. Midas users manual version 2012+ (2012), MIDAS IT  Co.,  Ltd.
6. Ministry  of  Land,  Transport  and  Maritime  Affairs (2012), 'Standard concrete construction specification 2012'.
7. Park, E.S.,  Shin,  H.S.,  Hong,  E.S.  (2007),  'Trends of  investigation  and  design  for  subsea  tunnels', KSCE  Tunnel Committee Special Conference 27th  Dec.  pp.  29-41.
8. Shin,  H.S.  (2011),  'Technology aspects of subsea tunnels',  Proceedings  of  the  Korean  Society  for Rock  Mechanics  Conference  2011.9,  pp.  35-43.
9. Terzaghi, K. (1943), 'Theoretical soil mechanics', J.  Wiley  &amp;  Sons,  New  York.
10. Yoo, C.S., Choi, J.H.  (2014), 'Prediction  of  TBM tunnel segment lining forces using ANN technique', Journal  of  Korean  Tunnelling  and  Underground Space  Association,  Vol.  16,  No.  1,  pp.  13-24.
11. Yoo, C.S., Kim, S.B., Yoo, K.H. (2008), Development  of  IT-based  tunnel  design  system,  Journal of  Korean  Tunnelling  and  Underground  Space Association,  Vol.  10,  No.  2,  pp.  153-166.
12. Yoo, C.S., Kim, J.M., Kim, J.H. (2005), Application of  Information  Technology  in  Tunnel  Design -  A case  study,  Journal  of  Korean  Tunnelling  and Underground  Space  Association  pp.  105-116.
13. Yang,  Y., Zhang, Q. (1997), 'A  hierarchical analysis for rock engineering using artificial neural networks', Rock  Mechanics and  Rock Engineering,  Vol.  30,  Issue  4,  pp.  207-222.
14. Yang,  Y.,  Zhang,  Q.  (1998),  'The  application  of neural networks to rock engineering system (RES)', Rock  Mechanics  and  Mining  Sciences,  Vol.  35, Issue  6,  pp.  727-745.
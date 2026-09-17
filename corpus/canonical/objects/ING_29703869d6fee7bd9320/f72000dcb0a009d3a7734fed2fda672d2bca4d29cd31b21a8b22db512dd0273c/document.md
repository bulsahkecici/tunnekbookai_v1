## Comparación de tres metodologías de análisis sísmico de túnel NATM en suelos finos de Santiago

Comparison of  three  methodologies  of  seismic  analyses  of  NATM  tunnel  in  fine  soils  of Santiago

Fecha de entrega: 19 de diciembre 2014 Fecha de aceptación: 7 de abril 2015

## David Solans, Cristian Hormazábal, Benjamin Rojas y Roberto León

ARCADIS  Chile,  Antonio  Varas  621,  Providencia,  Santiago,  Chile,  david.solans@arcadis.cl,  cristian.hormazabal@arcadis.cl, benjamin.rojas@arcadis.cl, roberto.leon@arcadis.cl

El análisis sísmico sobre revestimientos de túneles se ha desarrollado tradicionalmente con modelos simplificados, mediante  expresiones  analíticas  para  geometrías  sencillas  y mediante  softwares  de  análisis  estructural  que  no  incluyen el  historial  de  tensiones  del  suelo  debido  a  las  secuencias constructivas  y distancia al frente  de  excavación,  lo  cual tiende a sobrestimar los esfuerzos en el revestimiento de túneles. Sin embargo, los avances en el desarrollo de software de  modelos  de  elementos  o  diferencias  finitas  han  propiciado nuevas  herramientas  que  permiten  solucionar  las  dificultades planteadas,  así  como  evaluar  la  respuesta  sísmica  mediante historiales de aceleraciones. Este artículo compara la respuesta sísmica de un túnel excavado de acuerdo al método NATM en suelo  fino  de  Santiago  mediante  el  método  de  distorsión  de suelo aplicado en un software de análisis estructural y a través de  un  software  de  diferencias  finitas  para  interacción  suelo  - estructura. Adicionalmente, para el último modelo se aplica un historial de aceleraciones. Los resultados de estos análisis son comparados en términos de diseño estructural de acuerdo a la experiencia chilena.

Palabras  clave:  túneles,  NATM,  modelamiento  numérico  3D, análisis sísmico

## Introducción

Los análisis sísmicos de túneles han sido tradicionalmente abordados mediante expresiones analíticas para geometrías sencillas que no incluyen las secuencias constructivas ni historiales de esfuerzos (Wang, 1993; Penzien y Wu, 1998; Penzien, 2000). Últimamente, algunos softwares de análisis geotécnico han entregado herramientas para la resolución de problemas complejos, permitiendo incorporar las variaciones en los historiales de tensiones,  métodos constructivos,  secuencias  de  excavación  y  solicitaciones sísmicas a través de registros de aceleraciones.

Seismic design of tunnels is often based on simplified models through analytical expressions for elemental geometries  and  structural  softwares  which  not include soil stress path due to construction stages and  the  distance  of  the  front  of  the  excavation, resulting  in  overestimating  the  tunnels  stresses. However,  the  development  of  finite  differences  or finite  elements  software  has  provided  new  tools that  solve  these  problems  and  allow  evaluating the seismic response through seismic records. This article  compares  the  seismic  response  of  NATM tunnels in soft soil of Santiago through the seismic distortion  method  of  soil  applied  in  a  structural analysis  software  and  a  finite  difference  software for  soil  -  structure  interaction.  Additionally,  a seismic record is applied to the last case. The results of these analyses are compared in terms of seismic response of soils and structural design according to current Chilean practice.

Keywords:  tunnels,  NATM,  numerical  modelling 3D, seismic analysis

Este artículo presenta un estudio comparativo de 3 métodos de  análisis  sísmico  para  un  túnel  NATM  construido en  suelos  finos  del  noroeste  de  Santiago.  Se  describe  la metodología, consideraciones particulares y los parámetros empleados en cada caso. Se indican las complejidades y los tiempos computacionales requeridos para el desarrollo de cada metodología. Finalmente, se presenta un análisis comparativo de los resultados obtenidos: esfuerzos sísmicos en revestimiento del túnel y cálculo de espesor de revestimiento.

## Geometría  del  túnel  y  propiedades  del suelo de fundación

La geometría del túnel se muestra en la Figura 1. La secuencia  constructiva  considera  3  secciones  principales: side drift I, sección central, side drift II y 9 subsecciones que se enumeran en la misma figura. La metodología utilizada es acorde a los principios del método NATM (New Austrian Tunnelling Method) y simula las secuencias de excavación en tres etapas constructivas: bóveda, banco y contrabóveda; con desfase entre etapas y la aplicación de revestimiento estructural. Entre cada frente de avance de sidedrift , hay un desfase de 10 m, así también de la pared central. El nivel de riel del túnel se encuentra a una profundidad de 22 m del nivel de terreno y la clave del túnel se encuentra a 16 m de profundidad. La sección del túnel abarca un área aproximada de 190 m 2 .

Figura  1:  a)  Geometría  (dimensiones  en  cm)  y  b)  secuencia constructiva del túnel

<!-- image -->

Engineering drawing

Se  considera  un  túnel  construido  en  el  sector  de  suelos finos del noroeste de Santiago, al cual se le han asignado las  propiedades  geotécnicas  presentadas  en  la  Tabla  1. El  módulo  de  deformación  ha  sido  considerado  lineal aumentando en profundidad, también se han considerado distintos valores de cohesión y coeficiente de empuje en reposo in situ K 0 para dos distintos estratos de suelo.

Tabla 1: Propiedades de los materiales (ARCADIS, 2014)

| Propiedades                              | Valor               |
|------------------------------------------|---------------------|
| Densidad natural γ t , kN/m 3            | 18.5                |
| Ángulo de fricción φ, °                  | 31                  |
| Cohesión c , kPa                         | 30 para Z < 12 m    |
| Cohesión c , kPa                         | 50 para Z > 12 m    |
| Compresión no confinada q u , kPa        | 20 - 40             |
| Módulo de deformación E , MPa            | 20 + 2.75 Z         |
| Razón de Poisson ν                       | 0.3                 |
| K 0                                      | 0.65 para Z < 12 m  |
| K 0                                      | 0.45 para Z > 12 m  |
| Coef. de balasto horizontal K h , kN/m 3 | 0.53E( Z )/ B       |
| Coef. de balasto vertical K v , kN/m 3   | 0.53E( D f + B )/ B |

- Z : profundidad medida desde la superfície en m
- Df : profundidad sello fundación en m, B : dimensión menor de estructura en m

## Solicitación sísmica

Con el fin de simular la solicitación sísmica, se utilizan dos procedimientos: desangulación sísmica y análisis dinámico con  registro de aceleraciones. Para la  desangulación sísmica, la metodología empleada se basa en las recomendaciones del Manual de Carreteras (2014), que se sustentan en la propuesta de Kuesel (1969) para el diseño sísmico del metro de San Francisco. En este estudio se ha considerado una desangulación θ s de 1.1·10 -3 rad, obtenida de los valores tabulados en el Manual de Carreteras (2014) para un rango de compresión no confinada q u entre 20 y 40 kPa, para zona sísmica con a o = 0.4g.

El  análisis  dinámico  se  basó  en  uno  de  los  registros  de aceleraciones  del  terremoto  de  Chile,  ocurrido  el  27  de Febrero  del  2010,  que  tuvo  una  magnitud  momento M w de 8.8. El sismo fue subductivo tipo thrust con epicentro marítimo frente a la localidad de Cobquecura, Región del Bío Bío  (Saragoni  y  Ruíz,  2012).  El  registro  de  aceleraciones fue  obtenido  de  la  Red  Nacional  de Acelerógrafos  de  la Universidad  de  Chile  (RENADIC).  Corresponde  a  un registro de superficie con componente horizontal, obtenido en una estación ubicada en Maipú,  sobre depósitos de  ceniza  volcánica  denominados  comúnmente  como 'Pumicita'. Las principales características del registro de aceleraciones se indican en la Tabla 2.

Tabla 2: Principales características sísmicas registro aceleraciones terremoto 2010, estación Maipú (Saragoni y Ruíz, 2012)

| Características sísmicas                 |   Valor |
|------------------------------------------|---------|
| Aceleración máxima en campo libre PGA, g |    0.54 |
| Intensidad de Arias I a , g s            |    0.58 |
| Potencial Destructivo P d , cm s         |    6.07 |

La  Figura  2  presenta  las  componentes  de  aceleraciones, velocidades  y  desplazamientos  del  registro  utilizado.  El registro  ha  sido  sometido  a  corrección  de  línea  de  base. La Figura 3 presenta los espectros de Fourier y pseudoaceleración para un amortiguamiento del 5%.

Figura 2: Registros de aceleración, velocidad y desplazamiento en función del tiempo. Sismo 27F2010, estación Maipú

<!-- image -->

Line chart

Figura 3: Espectro de Fourier y espectro de respuesta de aceleraciones (5% de amortiguamiento)

<!-- image -->

Line chart

Para obtener el registro de aceleraciones en profundidad requerido para el análisis dinámico, se utilizó el procedimiento propuesto por Mejia y Dawson (2006) para aplicación del sismo en la base del modelo. En este caso se  escaló  el  registro  de  superficie  a  la  profundidad  del modelo, ajustando la respuesta en superficie en términos de PGA y espectro de aceleraciones.

## Modelación numérica

Se  han  llevado  a  cabo  tres  análisis  numéricos  mediante distintas  metodologías.  El  primer  análisis  corresponde  a una modelación mediante el software de elementos finitos para análisis estructural SAP2000 (caso I). El segundo y el tercer análisis (caso II y III) se han efectuado mediante el software de diferencias finitas para interacción suelo - estructura FLAC 3D versión 5.0. Las características principales de los distintos análisis se presentan en la Tabla 3.

Tabla 3: Principales características casos analizados

| Caso   | Tipo de análisis                                                   | Solici- tación sísmica      | Secuencia construc- tiva   | Soft- ware   | Com- pleji- dad   |
|--------|--------------------------------------------------------------------|-----------------------------|----------------------------|--------------|-------------------|
| I      | Modelo de Winkler interacción suelo - estructura mediante resortes | Desan- gulación sísmica     | No incluida                | SAP 2000     | Media             |
| II     | Modelo de diferencias finitas                                      | Desan- gulación sísmica     | Incluida                   | FLAC 3D      | Alta              |
| III    | Modelo de diferencias finitas                                      | Registro de acelera- ciones | Incluida                   | FLAC 3D      | Muy alta          |

Para el caso I se adoptaron las siguientes consideraciones:

- Empuje horizontal en reposo, calculado con el coeficiente de empuje en reposo in situ. Este empuje se aplica comprimiendo los resortes.
- Los coeficientes de balasto incluyen el módulo de deformación del suelo amplificado 3 veces para el caso sísmico.
- Carga vertical equivalente al 60% del peso de la columna de suelo. Esta reducción del peso de la columna de suelo se asocia al efecto de arco, y fue estimada por los autores  en  base  a  las  dimensiones  del  área  a  excavar, profundidad del túnel y desplazamientos verticales en la clave del túnel en comparación con los otros análisis.
- Esta metodología no incorpora la secuencia constructiva del túnel.

- La modelación no incorpora el efecto de excavación con la distancia al frente.
- El desplazamiento por desangulación sísmica se impone en la base de los resortes. Se desactivan los resortes traccionados.
- Los elementos estructurales se han modelado como elementos viga o frame .

La geometría modelada se presenta en la Figura 4.

Figura 4: Geometría modelo SAP2000. Caso I

<!-- image -->

Engineering drawing

La modelación numérica de los casos II y III se ha llevado a cabo mediante el software de diferencias finitas FLAC3D versión  5.0.  Para  estas  simulaciones  se  consideraron  los bordes del modelo con restricción de desplazamiento horizontal (X e Y) y la base del modelo con restricción de desplazamiento en todas las direcciones (X, Y y Z). La Figura 5  presenta  la  geometría,  malla  y  secuencia  constructiva. El modelo cuenta con una profundidad de cota de riel de 22 m desde la superficie, un sobreancho desde los bordes del túnel de 100 m (≈ 5 veces ancho túnel) a fin de reducir el  efecto de los bordes en la respuesta del túnel. Para el análisis  dinámico,  se  han  utilizado  elementos  absorbentes en los bordes ( free - field condition ) a fin de evitar la reflexión de ondas. El revestimiento fue modelado como elemento estructural del tipo Shell que considera un comportamiento tensión - deformación lineal elástico. No se ha considerado interfaz entre suelo y estructura. La altura de  los  elementos  se  limitó  de  acuerdo  a  las  recomendaciones de Kuhlemeyer y Lysmer (1973) para evitar filtrar frecuencias de interés para el análisis dinámico (caso III). Considerando valores de V s del orden de 200 m/s (incrementándose en profundidad), se obtienen elementos de altura en torno a 3.0 m.

<!-- image -->

Engineering drawing

Figura  5:  a)  Secuencia  contructiva  y  b)  geometría  Modelo Flac3D. Casos II y III

<!-- image -->

Engineering drawing

Se utilizó la ley constitutiva Cap - Yield (CY Soil ) (ITASCA,  2011)  que  se  encuentra  implementada  en  FLAC 3D.  CY Soil corresponde  a  un  modelo  constitutivo  del tipo  plástico  y  está  caracterizado  por  el  criterio  de  falla Mohr  -  Coulomb.  El  modelo  presenta,  entre  otras,  las siguientes particularidades: la rigidez depende del estado tensional,  genera  deformaciones  plásticas  en  cargas  desviatorias  primarias,  genera  deformaciones  plásticas  en compresión isotrópica primaria y considera trayectorias de descarga-recarga elásticas. El modelo constitutivo CY Soil establece relaciones del tipo hiperbólico para el módulo de corte G , y para el módulo volumétrico K , en función de la presión media efectiva p ',  quedando establecidas por las siguientes expresiones:

donde G e ref es  el  módulo  de  corte  elástico  de  referencia en  kPa  para  una  tensión  de  referencia p ref , K iso ref es  el módulo  volumétrico  elástico  de  referencia  en  kPa  para una  tensión p ref , p '  es  la  tensión  efectiva  media  en  kPa y m es  una  constante.  Los  parámetros  del  modelo  se han  ajustado  en  base  a  las  propiedades  de  resistencia  al corte, coeficiente de empuje en reposo y la variación del módulo  de  deformación  en  profundidad.  Cabe  destacar que  el  modelo  constitutivo Cap  Yield ha  sido  utilizado exitosamente  en  la  modelación  en  obras  de  metro  de Roma  y  sus  resultados  han  sido  verificados  de  forma satisfactoria  con  datos  de  monitoreo  (Lucarelli,  2011).

Tabla 4: Parámetros geotécnicos para el modelo Cap Yield en suelos finos

| Propiedades                                             | Valor               |
|---------------------------------------------------------|---------------------|
| Densidad natural γ n , kN/m 3                           | 18.5                |
| Angulo de fricción ϕ°                                   | 31                  |
| Cohesión c , kPa                                        | 30 para Z < 12 m    |
| Cohesión c , kPa                                        | 50 para Z > 12 m    |
| Módulo de corte elástico de referencia G e ref , MPa    | 65.4, para Z < 12 m |
| Módulo de corte elástico de referencia G e ref , MPa    | 84.6 para Z > 12 m  |
| Módulo volumétrico elástico de referencia K e ref , MPa | 57.2 para Z < 12 m  |
| Módulo volumétrico elástico de referencia K e ref , MPa | 74 para Z > 12 m    |
| Potencia m                                              | 0.7, para Z < 12 m  |
| Potencia m                                              | 1.0, para Z > 12 m  |
| Presión de referencia p ref , kPa                       | 100                 |
| Coeficiente de Poisson ν                                | 0.3                 |
| Razón de falla R f                                      | 0.9                 |
| Factor de calibración β                                 | 0.25                |

Dentro de las consideraciones del análisis dinámico (caso III),  el  modelo  constitutivo  utilizado  considera  el  efecto de descarga-recarga con una amplificación del módulo de deformación de 3 veces el valor estático. Adicionalmente, se ha considerado una razón de amortiguamiento del tipo Rayleigh de 4% en torno a la frecuencia fundamental del sismo de 2 Hz.

Los tiempos computacionales de ejecución de los casos II y III, para la condición sísmica, resultan muy distintos. El caso II corresponde a una etapa adicional de 1 a 2 horas de ejecución, mientras que el caso III demora cerca de 8 a 10 días.

## Resultados

En  la  Figura  6  se  presentan  los  resultados  de  esfuerzos resultantes  sobre  revestimientos  de  túnel,  para  el  Caso  I y Caso II. Los resultados del Caso III se presentan en la Figura 7. Si bien los esfuerzos de los Casos I y II difieren en  magnitud,  presentan  una  distribución  similar  en  la estructura. El Caso III resulta difícil de comparar con los otros, dado que el análisis genera un historial de esfuerzos en  el  tiempo.  En  la  Tabla  5,  se  presentan  los  rangos  de esfuerzos obtenidos para cada análisis efectuado.

Tabla 5: Rango de esfuerzos túnel distintos análisis

| Caso   | Esfuerzo normal, kN/m   | Esfuerzo de corte, kN/m   | Esfuerzo de momento, kN/m   |
|--------|-------------------------|---------------------------|-----------------------------|
| I      | -1300 a -1650           | -300 a 100                | -300 a 800                  |
| II     | -2000 a -3200           | -150 a 150                | -400 a 400                  |
| III    | -1000 a -2500           | -250 a 50                 | -400 a 500                  |

Como criterio de comparación de resultados, se considera el espesor de revestimiento diseñado en base a los estados tensionales  resultantes.  No  se  considera  el  cálculo  de cuantías de acero para el análisis comparativo, dado que estas cantidades son determinadas fundamentalmente por  los  esfuerzos  generados  en  etapas  de  construcción. Para el diseño de los espesores del túnel, se desarrollaron diagramas de interacción de esfuerzo axial versus corte del elemento  estructural,  mediante  el  código  de  diseño ACI 318-08  (2008).  Los  esfuerzos  internos  del  revestimiento del túnel fueron amplificados en un 20% de acuerdo a la práctica  habitual  chilena  en  este  tipo  de  proyectos.  Los diagramas de interacción se presentan en la Figura 8 para cada uno de los casos, con los espesores resultantes. En la Tabla 6 se indican los espesores obtenidos para cada caso de análisis.

Tabla 6: Resultados de espesores del análisis estructural del túnel

| Caso   |   Espesor revestimiento túnel, cm |
|--------|-----------------------------------|
| I      |                                75 |
| II     |                                70 |
| III    |                                60 |

Los resultados del caso III conducen a los menores espesores, sin embargo se asocia a un evento sísmico particular, por lo que al aplicar otros sismos la respuesta pudiese variar.

## Conclusiones

Se realiza el análisis sísmico de un túnel construido con el  método  NATM en suelos finos. El análisis  se  efectúa mediante 3 métodos distintos, con objeto de comparar los espesores de revestimiento determinados a partir de sus resultados. Para el Caso I se adopta un modelo cinemático (Manual de Carreteras, 2014). Análisis estructural representando  interacción  suelo-estructura  mediante  resortes. Solicitación sísmica impuesta mediante distorsión angular. Software SAP 2000. Para el Caso II se usa un modelo de diferencias finitas. Solicitación sísmica impuesta mediante distorsión angular. Software FLAC 3D. Y para el Caso III también se usa un modelo de diferencias finitas, pero la solicitación sísmica es determinada por un análisis dinámico con historial de aceleraciones. Software FLAC 3D.

Figura 6: Esfuerzo sísmicos resultantes a) Sap2000 (caso I) y b) FLAC3D desangulación (caso II)

<!-- image -->

Pie chart

Figura 7: Puntos de control y esfuerzo sísmicos resultantes Flac3D para análisis dinámico (Caso III)

<!-- image -->

Line chart

Figura 8: Diagramas interacción corte versus axial. Casos I, II y III

<!-- image -->

Line chart

En relación a la  complejidad  y  tiempos  de  ejecución  de cada método, se concluye lo siguiente:

Para el Caso I, la elaboración del modelo resulta más rápida  que  en  los  otros  casos  y  no  se  simula  la  secuencia constructiva. El tiempo computacional que requiere no es significativo.

Para el Caso II, la elaboración del modelo requiere más tiempo  que  en  el  Caso  I  y  debe  simularse  la  secuencia constructiva. El tiempo computacional de la etapa estática es  de  3  días  y  para  la  desangulación  sísmica,  el  tiempo adicional no es significativo.

Para el Caso III, los tiempos requeridos para la elaboración del modelo y simulación de la secuencia constructiva son los mismos que en el Caso II. El análisis dinámico requiere un tiempo computacional de unos 10 días más que el Caso II.

Los  espesores  determinados  en  base  a  los  resultados  de los distintos casos presentan diferencias que no superan el 25%. El Caso I conduce al mayor espesor, mientras que el espesor más reducido se deduce en el Caso III. Los espesores determinados en base a análisis con desangulación sísmica no difieren significativamente de aquellos obtenidos mediante un análisis dinámico. Este resultado sugiere que la desangulación sísmica �s es  de 1.1·10 -3 rad, es un valor aproximado que resulta aplicable para el diseño de túneles en suelos finos del noroeste de Santiago.

## Agradecimientos

Los  autores  agradecen  a  las  disciplinas  de  Geotecnia  y Túneles de ARCADIS Chile por el tiempo y recursos computacionales para la elaboración del presente artículo.

## Referencias

ACI (2008). Requisitos de Reglamento para Concreto Estructural (ACI 318S-08) y Comentario, American Concrete Institute, USA

ARCADIS (2014). Base de datos de diversas unidades de suelos. Sección de Geotecnia.

ITASCA  (2011).  FLAC3D:  Theory  and  Background.  ITASCA Consulting Group Inc.

Kuesel, T. (1969). Earthquake design criteria for subways. Journal of Structural Division 95 , Nº ST6, 1213-1231

Kuhlemeyer,  R.  and  Lysmer,  J.  (1973).  Finite  element  method accuracy for wave propagation problemas. Journal of Soil Mechanics and Foundations Division 99 (SM5), 421-427

Lucarelli, A., Guiducci, G., Furlani, G. and Sorge, R. (2011). CapYield model with cohesion, back analysis of real excavations. 2nd International FLAC/DEM Symposium, Melbourn Australia Manual de Carreteras (2014). Instrucciones y criterios de diseño. Vol. N° 3. Dirección de Vialidad. Ministerio de Obras Públicas Mejia, L.H. and Dawson, E.M. (2006). Earthquake deconvolution for  FLAC.  4th  International  FLAC  Symposium  on  Numerical Modelling in Geomechanics.

Penzien, J. and Wu, C.L (1998). Stresses in linings of bored tunnels. Earthquake Engineering Structural Dynamics 27 (3), 283-300

Penzien, J. (2000). Seismically induced racking of tunnel linings. Earthquake Engineering Structural Dynamics 29 (5), 683-691

Saragoni, R. y Ruíz, S. (2012). Implicaciones y nuevos desafíos de diseño sísmico de los acelerogramas del terremoto del 2010. En: Mw = 8.8. Terremoto en Chile, 27 de febrero 2010. Departamento de Ingeniería Civil, Universidad de Chile. Editora Maval, 127-146

Wang, J.N. (1993). Seismic design of tunnels. Parsons Brickerhoff, Quade &amp; Douglas, Inc. Monograph 7
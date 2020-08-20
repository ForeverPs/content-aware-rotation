# Content-Aware-Rotation
* Reproduction of Kaiming He's Paper [**Content-Aware Rotation**](http://kaiminghe.com/publications/iccv13car.pdf) on ICCV 2013.<br>
---
#### Contents

1. [Dependency](#Dependency)
1. [Formula Derivation](#formula-derivation)
1. [Usage](#Usage)
1. [Results](#Results)
1. [References](#References)
---

#### Dependency
###### &emsp;Python&ensp;3.6 or newer<br>
###### &emsp;pillow == 5.1.0<br>
###### &emsp;numpy == 1.14.5<br>
###### &emsp;opencv == 4.2.0<br>
###### &emsp;matplotlib == 2.2.2<br>
###### &emsp;tensorflow == 1.10.0<br>

#### Formula Derivation
* ![](http://latex.codecogs.com/svg.latex?\\E_R(\theta)})<br>
$E_R(\theta)=\sum_{m}\delta_m(\theta_m-\Delta )^2+\sum_{m}(\theta_m-\theta_{m+1})^2$<br>
suppose that : \theta_{m+1}=P@\theta, then we have : <br>
![eq3](https://github.com/ForeverPs/content-aware-rotation/blob/master/eq/eq3.jpg)


#### References
##### Author&ensp;:&ensp;Kaiming He, Huiwen Chang, Jian Sun<br>
* ###### &ensp;[Content-Aware Rotation----ICCV 2013](http://kaiminghe.com/publications/iccv13car.pdf)<br>

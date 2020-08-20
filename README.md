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
* E_R(\theta)
E_R(\theta)=\sum_{m}\delta_m(\theta_m-\Delta )^2+\sum_{m}\delta_m(\theta_m-\theta_{m+1})^2

#### References
##### Author&ensp;:&ensp;Kaiming He, Huiwen Chang, Jian Sun<br>
* ###### &ensp;[Content-Aware Rotation----ICCV 2013](http://kaiminghe.com/publications/iccv13car.pdf)<br>

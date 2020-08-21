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
* Rotation Manipulation ![eq1](https://github.com/ForeverPs/content-aware-rotation/blob/master/eq/eq1.jpg) <br>
![eq2](https://github.com/ForeverPs/content-aware-rotation/blob/master/eq/eq2.jpg)
suppose that : ![eq3](https://github.com/ForeverPs/content-aware-rotation/blob/master/eq/eq3.jpg), then we have : ![eq4](https://github.com/ForeverPs/content-aware-rotation/blob/master/eq/eq4.jpg)
further, we can get the derivative : ![eq5](https://github.com/ForeverPs/content-aware-rotation/blob/master/eq/eq5.jpg) <br>

* Line Preservation ![eq6](https://github.com/ForeverPs/content-aware-rotation/blob/master/eq/eq6.jpg) <br>
![eq7](https://github.com/ForeverPs/content-aware-rotation/blob/master/eq/eq7.jpg)
suppose that : ![eq8](https://github.com/ForeverPs/content-aware-rotation/blob/master/eq/eq8.jpg), then we have : ![eq9](https://github.com/ForeverPs/content-aware-rotation/blob/master/eq/eq9.jpg)
further, we can get the derivative : ![eq10](https://github.com/ForeverPs/content-aware-rotation/blob/master/eq/eq10.jpg) <br>

* Shape Preservation ![eq11](https://github.com/ForeverPs/content-aware-rotation/blob/master/eq/eq11.jpg) <br>
![eq12](https://github.com/ForeverPs/content-aware-rotation/blob/master/eq/eq12.jpg)
suppose that : ![eq13](https://github.com/ForeverPs/content-aware-rotation/blob/master/eq/eq13.jpg), then we have : ![eq14](https://github.com/ForeverPs/content-aware-rotation/blob/master/eq/eq14.jpg)
further, we can get the derivative : ![eq15](https://github.com/ForeverPs/content-aware-rotation/blob/master/eq/eq15.jpg) <br>

* Boundary Preservation ![eq16](https://github.com/ForeverPs/content-aware-rotation/blob/master/eq/eq16.jpg) <br>
![eq17](https://github.com/ForeverPs/content-aware-rotation/blob/master/eq/eq17.jpg)
further, we can get the derivative : ![eq18](https://github.com/ForeverPs/content-aware-rotation/blob/master/eq/eq18.jpg) <br>

* Optimization
* Step 1 : Fix θ solve for V <br>
Sparse Linear System : ![eq19](https://github.com/ForeverPs/content-aware-rotation/blob/master/eq/eq19.jpg)
V is the minimum point of total energy above, thus, let : <br>
![eq20](https://github.com/ForeverPs/content-aware-rotation/blob/master/eq/eq20.jpg)<br>
we can get the solution for V. <br>
* Step 2 : Fix V solve for θ <br>





#### References
##### Author&ensp;:&ensp;Kaiming He, Huiwen Chang, Jian Sun<br>
* ###### &ensp;[Content-Aware Rotation----ICCV 2013](http://kaiminghe.com/publications/iccv13car.pdf)<br>

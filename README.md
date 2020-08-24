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
* Rotation Manipulation ![eq1](https://github.com/ForeverPs/content-aware-rotation/blob/master/eq/eq1.jpg =0.8x)<br>
![eq2](https://github.com/ForeverPs/content-aware-rotation/blob/master/eq/eq2.jpg)<br>
suppose that : ![eq3](https://github.com/ForeverPs/content-aware-rotation/blob/master/eq/eq3.jpg),<br>
then we have : ![eq4](https://github.com/ForeverPs/content-aware-rotation/blob/master/eq/eq4.jpg)<br>
further, we can get the derivative : ![eq5](https://github.com/ForeverPs/content-aware-rotation/blob/master/eq/eq5.jpg)<br>

* Line Preservation ![eq6](https://github.com/ForeverPs/content-aware-rotation/blob/master/eq/eq6.jpg)<br>
![eq7](https://github.com/ForeverPs/content-aware-rotation/blob/master/eq/eq7.jpg)<br>
suppose that : ![eq8](https://github.com/ForeverPs/content-aware-rotation/blob/master/eq/eq8.jpg),<br>
then we have : ![eq9](https://github.com/ForeverPs/content-aware-rotation/blob/master/eq/eq9.jpg)<br>
further, we can get the derivative : ![eq10](https://github.com/ForeverPs/content-aware-rotation/blob/master/eq/eq10.jpg)<br>

* Shape Preservation ![eq11](https://github.com/ForeverPs/content-aware-rotation/blob/master/eq/eq11.jpg)<br>
![eq12](https://github.com/ForeverPs/content-aware-rotation/blob/master/eq/eq12.jpg)<br>
suppose that : ![eq13](https://github.com/ForeverPs/content-aware-rotation/blob/master/eq/eq13.jpg),<br>
then we have : ![eq14](https://github.com/ForeverPs/content-aware-rotation/blob/master/eq/eq14.jpg)<br>
further, we can get the derivative : ![eq15](https://github.com/ForeverPs/content-aware-rotation/blob/master/eq/eq15.jpg)<br>

* Boundary Preservation ![eq16](https://github.com/ForeverPs/content-aware-rotation/blob/master/eq/eq16.jpg)<br>
![eq17](https://github.com/ForeverPs/content-aware-rotation/blob/master/eq/eq17.jpg)<br>
further, we can get the derivative : ![eq18](https://github.com/ForeverPs/content-aware-rotation/blob/master/eq/eq18.jpg)<br>

* Optimization
* Step 1 : Fix θ solve for V <br>
Sparse Linear System : ![eq19](https://github.com/ForeverPs/content-aware-rotation/blob/master/eq/eq19.jpg)<br>
V is the minimum point of total energy above, thus, let : <br>
![eq20](https://github.com/ForeverPs/content-aware-rotation/blob/master/eq/eq20.jpg)<br>
we can get the solution for V. <br>
* Step 2 : Fix V solve for θ <br>
**Part 1** : Fix Φ, update θ<br>
![eq21](https://github.com/ForeverPs/content-aware-rotation/blob/master/eq/eq21.jpg)<br>
suppose that : ![eq22](https://github.com/ForeverPs/content-aware-rotation/blob/master/eq/eq22.jpg)<br>
we have : ![eq23](https://github.com/ForeverPs/content-aware-rotation/blob/master/eq/eq23.jpg)<br>
let : ![eq24](https://github.com/ForeverPs/content-aware-rotation/blob/master/eq/eq24.jpg)<br>
by solving a sparse linear system, we can get the solution of θ : <br>
![eq25](https://github.com/ForeverPs/content-aware-rotation/blob/master/eq/eq25.jpg)<br>
**Part 2** : Fix θ, update Φ<br>
![eq26](https://github.com/ForeverPs/content-aware-rotation/blob/master/eq/eq26.jpg)<br>
the solution of Φ can be easily approximately reached by enumeration based on iteration methods(increase β gradually).<br>

#### Usage
* How to Use : download the whole project and run **main.py**
* folder ep : images which are used for formula derivation and some results.
* folder image : images which are used in original paper.
* folder lsd : line segment detection algorithm in python version.
* warp_mesh.py : image warping method realized by embedded function in tensorflow.

#### Results
* [**The Leaning Tower of Pisa  5.5°**](https://github.com/ForeverPs/content-aware-rotation/blob/master/image/image7.jpg)<br>
<img src= https://github.com/ForeverPs/content-aware-rotation/blob/master/eq/pisa_tower.jpg /><br><br>

* [**Palace Tower  -6.1°**](https://github.com/ForeverPs/content-aware-rotation/blob/master/image/image2.png)<br>
<img src= https://github.com/ForeverPs/content-aware-rotation/blob/master/eq/palace_tower.jpg /><br><br>

* [**House Building  -5.8°**](https://github.com/ForeverPs/content-aware-rotation/blob/master/image/image1.png)<br>
<img src= https://github.com/ForeverPs/content-aware-rotation/blob/master/eq/house.jpg /><br><br>

* [**The Oriental Pearl Tower  1.8°**](https://github.com/ForeverPs/content-aware-rotation/blob/master/image/image8.jpg)<br>
<img src= https://github.com/ForeverPs/content-aware-rotation/blob/master/eq/shanghai.jpg /><br><br>


#### References
##### Author&ensp;:&ensp;Kaiming He, Huiwen Chang, Jian Sun<br>
* ###### &ensp;[Content-Aware Rotation----ICCV 2013](http://kaiminghe.com/publications/iccv13car.pdf)<br>
##### Matlab Version<br>
* ###### &ensp;[iRotate](https://github.com/yuchien302/iRotate)<br>

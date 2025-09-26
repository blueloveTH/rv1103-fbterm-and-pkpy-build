【这是一个简陋的地图】
【虽然说这个游戏只是分享一下♥ 的一个想法，但还是设定一个游戏目标吧】
【目标：出门】
-> map ->
-> move
== setting ==
VAR locationx=0
VAR locationy=0
VAR line= ""
== map ==

{locationx :
-  0:~ line="墙—♥ —〇—〇—〇—〇—〇—〇—墙"
-  1:~ line="墙—〇—♥ —〇—〇—〇—〇—〇—墙"
-  2:~ line="墙—〇—〇—♥ —〇—〇—〇—〇—墙"
-  3:~ line="墙—〇—〇—〇—♥ —〇—〇—〇—墙"
-  4:~ line="墙—〇—〇—〇—〇—♥ —〇—〇—墙"
-  5:~ line="墙—〇—〇—〇—〇—〇—♥ —〇—墙"
-  6:~ line="墙—〇—〇—〇—〇—〇—〇—♥ —墙"
}

```
.
.
.
.
.
.
.
.
.

墙—墙—墙—墙—墙—墙—墙—墙—墙
{locationy == 0 : {line}}
墙—〇—〇—〇—〇—〇—〇—〇—墙
{locationy == 1 : {line}}
墙—〇—〇—〇—〇—〇—〇—〇—墙
{locationy == 2 : {line}}
墙—〇—〇—〇—〇—〇—〇—〇—墙
{locationy == 3 : {line}}
墙—〇—〇—〇—〇—〇—〇—〇—墙
{locationy == 4 : {line}}
墙—〇—〇—〇—〇—〇—〇—〇—墙
{locationy == 5 : {line}}
墙—〇—〇—〇—〇—〇—〇—〇—墙
{locationy == 6 : {line}}
墙—墙—墙—墙—门—墙—墙—墙—墙
```
->->
== move ==
+ {locationy >=1 } 上
~ locationy=locationy-1
+ {locationy <=5 } 下
~ locationy=locationy+1
+ {locationx >=1 } 左
~ locationx=locationx-1
+ {locationx <=5 } 右
~ locationx=locationx+1
+ {locationx == 3 and locationy==6 } 推门而出
你成功出门了
-> END
- -> map -> move
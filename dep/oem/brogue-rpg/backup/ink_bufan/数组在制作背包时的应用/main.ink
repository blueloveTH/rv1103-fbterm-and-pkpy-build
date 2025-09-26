
INCLUDE gyc.ink
INCLUDE array.ink

VAR zb1= 0
VAR zb2= 0
VAR zb3= 0
VAR zb4= 0
VAR x=0
// 名字，攻击，附加，附加值，装备栏位置
~ zb1=array4(0,0,0,0)
~ zb2=array4(1,1,1,1)
~ zb3=array4(1,2,1,2)
~ zb4=array4(2,3,2,3)
//由于array一次最多只能有4个元素，因此后面尧再加元素需要用到push或者connect
~ push(zb1,1)
~ push(zb2,2)
~ push(zb3,3)
~ push(zb4,4)

-> a
//装备栏中装备名字显示器
== function equipment_name(i) ==
{
  - get(i,0) ==0:
  ~ return "[空]"
  - get(i,0) ==1:
  ~ return "[匕首]"
  - get(i,0) ==2:
  ~ return "[短剑]"
  - get(i,0) ==3:
  ~ return "[短杖]"
  - get(i,0) ==4:
  ~ return "[火枪]"
}

//背包父界面
== check_packet ==
```
༄༅༄༅༄༅༄༅༄༅ 背 包 ༄༅༄༅༄༅༄༅༄༅༄༅
装备栏1:。。。{equipment_name(zb1)}
装备栏2:。。。{equipment_name(zb2)}
装备栏3:。。。{equipment_name(zb3)}
装备栏4:。。。{equipment_name(zb4)}
༄༅༄༅༄༅༄༅༄༅༄༅༄༅༄༅༄༅༄༅༄༅༄༅༄༅
```
//用来查看某装备栏中某件物品的属性的一个选项
+ [༄༅༄༅༄༅༄༅༄༅ 装备1 ༄༅༄༅༄༅༄༅༄༅]
~ x=zb1
+ [༄༅༄༅༄༅༄༅༄༅ 装备2 ༄༅༄༅༄༅༄༅༄༅]
~ x=zb2
+ [༄༅༄༅༄༅༄༅༄༅ 装备3 ༄༅༄༅༄༅༄༅༄༅]
~ x=zb3
+ [༄༅༄༅༄༅༄༅༄༅ 装备4 ༄༅༄༅༄༅༄༅༄༅]
~ x=zb4
- -> check_pack_equipment ->
- ->->

//某装备栏中物品属性显示器，背包子界面
== check_pack_equipment ==
```
༄༅༄༅༄༅༄༅༄༅ 装备{get(x,4)} ༄༅༄༅༄༅༄༅༄༅
名称: 。。。。{equipment_name(x)}
攻击加成: 。。{get(x,1)}
防御加成: 。。{get(x,2)}
附加效果: 。。{get(x,3)}:{get(x,3)}
༄༅༄༅༄༅༄༅༄༅༄༅༄༅༄༅༄༅༄༅༄༅༄༅
```
+[【返回】]
->->

== a ==
-> check_packet ->
+ 打开背包
-> a
+ 关闭背包
-> END



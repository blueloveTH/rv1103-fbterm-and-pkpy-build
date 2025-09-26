【这是一个投掷小游戏】
【每一次投掷，标靶位置都不会变，除非投中】
【你需要做的是，像一台投石机一样，设定投掷速度和角度】
【系统会自动判断落点位置，若距离篮框在一定范围内，视作成功】

VAR sin1= 0.01745240644
VAR cos1= 0.99984769516

VAR sinans= 0
VAR cosans= 1

VAR rotation= 0
VAR set =0

VAR speed= 0
VAR A= 0
VAR location= 0
VAR target= 0


~ target= RANDOM(5,1000)
-> start
== start ==
【目标位置：{target} m】
-> set_rotation
== set_rotation ==
~ set=0
【设置仰角：
-> s ->
~ set = A
{set<=0 or set>=90:
  【角度超出范围！】
  ~ set=0
  ~ A=0
  -> set_rotation
}
【仰角：{set}°】

-> set_speed
== set_speed ==
~ speed=0
~ A = 0
【设置速度：
-> s ->
~ speed = A
~ A = 0
【速度：{speed}m/s】

+ 投掷！
-> caculate1




== s ==

+[0]
~ A=A*10+0
{A}
-> s
+[1]
~ A=A*10+1
{A}
-> s
+[2]
~ A=A*10+2
{A}
-> s
+[3]
~ A=A*10+3
{A}
-> s
+[4]
~ A=A*10+4
{A}
-> s
+[5]
~ A=A*10+5
{A}
-> s
+[6]
~ A=A*10+6
{A}
-> s
+[7]
~ A=A*10+7
{A}
-> s
+[8]
~ A=A*10+8
{A}
-> s
+[9]
~ A=A*10+9
{A}
-> s
+ 清空！
~ A=0
-> s
+ 确定！
->->


== caculate1 ==
-> initialization
== initialization ==
~ sinans= 0
~ cosans= 1
~ rotation= 0

-> caculate2
== caculate2 ==
{rotation != set :
  ~ add()
  -> caculate2
}
~ double()
~ loc()
-> judge
== judge ==
{location<= target+5 and location >= target-5:
  -> true1
  -else:
  -> false1
}
== true1 ==
-> word ->
~ target= RANDOM(5,1000)
-> start
== false1 ==
-> word ->
-> start
== word ==
【仰角：{set}°】
【速度：{speed}m/s】
【目标位置：{target}m】
【你的位置：{INT(location)}m】
【误差：{INT(location-target)}m】
{location<= target+5 and location >= target-5:
  【成功！】
  【目标位置变更】
  -else:
  【失败】
  【重新开始吧】
}
->->
== function add() ==
~ sinans= sinans*cos1+cosans*sin1
~ cosans= cosans*cos1-sinans*sin1
~ rotation= rotation+1

== function loc() ==
~ location = speed*speed*sinans/10

== function double() ==
~ sinans=2*sinans*cosans
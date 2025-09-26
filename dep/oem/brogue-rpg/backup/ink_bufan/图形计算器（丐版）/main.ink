VAR initial_x=0
VAR step_x=0
VAR initial_y=0
VAR offset_x = 0
VAR offset_y=0

VAR y1=0
VAR y2=0
VAR y3=0
VAR y4=0
VAR y5=0
VAR y6=0
VAR y7=0
VAR y8=0

VAR initial_line=""
VAR line1=""
VAR line2=""
VAR line3=""
VAR line4=""
VAR line5=""
VAR line6=""
VAR line7=""
VAR line8=""

-> set

== function line() ==
{
  - initial_y>0*step_x and initial_y<=1*step_x:
~    initial_line= "◇ — — — — — — — —"
  - initial_y>1*step_x and initial_y<=2*step_x:
~  initial_line= "— ◇ — — — — — — —"
  - initial_y>2*step_x and initial_y<=3*step_x:
~  initial_line= "— — ◇ — — — — — —"
  - initial_y>3*step_x and initial_y<=4*step_x:
~  initial_line= "— — — ◇ — — — — —"
  - initial_y>4*step_x and initial_y<=5*step_x:
~  initial_line= "— — — — ◇ — — — —"
  - initial_y>5*step_x and initial_y<=6*step_x:
~  initial_line= "— — — — — ◇ — — —"
  - initial_y>6*step_x and initial_y<=7*step_x:
~  initial_line= "— — — — — — ◇ — —"
  - initial_y>7*step_x and initial_y<=8*step_x:
~  initial_line= "— — — — — — — ◇ —"
  - initial_y>8*step_x and initial_y<=9*step_x:
~  initial_line= "— — — — — — — — ◇"
- else:
~  initial_line= "— — — — — — — — -"
}

{
  - y1>0*step_x and y1<=1*step_x:
~  line1="◇ — — — — — — — —"
  - y1>1*step_x and y1<=2*step_x:
~   line1="— ◇ — — — — — — —"
  - y1>2*step_x and y1<=3*step_x:
~  line1="— — ◇ — — — — — —"
  - y1>3*step_x and y1<=4*step_x:
~  line1="— — — ◇ — — — — —"
  - y1>4*step_x and y1<=5*step_x:
~  line1="— — — — ◇ — — — —"
  - y1>5*step_x and y1<=6*step_x:
~  line1="— — — — — ◇ — — —"
  - y1>6*step_x and y1<=7*step_x:
~  line1="— — — — — — ◇ — —"
  - y1>7*step_x and y1<=8*step_x:
~  line1="— — — — — — — ◇ —"
  - y1>8*step_x and y1<=9*step_x:
~  line1="— — — — — — — — ◇"
- else:
~  line1= "— — — — — — — — -"
}

{
  - y2>0*step_x and y2<=1*step_x:
~  line2="◇ — — — — — — — —"
  - y2>1*step_x and y2<=2*step_x:
~  line2="— ◇ — — — — — — —"
  - y2>2*step_x and y2<=3*step_x:
~  line2="— — ◇ — — — — — —"
  - y2>3*step_x and y2<=4*step_x:
~  line3="— — — ◇ — — — — —"
  - y2>4*step_x and y2<=5*step_x:
~  line2="— — — — ◇ — — — —"
  - y2>5*step_x and y2<=6*step_x:
~  line2="— — — — — ◇ — — —"
  - y2>6*step_x and y2<=7*step_x:
~  line2="— — — — — — ◇ — —"
  - y2>7*step_x and y2<=8*step_x:
~  line2="— — — — — — — ◇ —"
  - y2>8*step_x and y2<=9*step_x:
~  line2="— — — — — — — — ◇"
- else:
~  line2= "— — — — — — — — -"
}

{
  - y3>0*step_x and y3<=1*step_x:
~  line3="◇ — — — — — — — —"
  - y3>1*step_x and y3<=2*step_x:
~  line3="— ◇ — — — — — — —"
  - y3>2*step_x and y3<=3*step_x:
~  line3="— — ◇ — — — — — —"
  - y3>3*step_x and y3<=4*step_x:
~  line3="— — — ◇ — — — — —"
  - y3>4*step_x and y3<=5*step_x:
~  line3="— — — — ◇ — — — —"
  - y3>5*step_x and y3<=6*step_x:
~  line3="— — — — — ◇ — — —"
  - y3>6*step_x and y3<=7*step_x:
~  line3="— — — — — — ◇ — —"
  - y3>7*step_x and y3<=8*step_x:
~  line3="— — — — — — — ◇ —"
  - y3>8*step_x and y3<=9*step_x:
~  line3="— — — — — — — — ◇"
- else:
~  line3= "— — — — — — — — -"
}

{
  - y4>0*step_x and y4<=1*step_x:
~  line4="◇ — — — — — — — —"
  - y4>1*step_x and y4<=2*step_x:
~  line4="— ◇ — — — — — — —"
  - y4>2*step_x and y4<=3*step_x:
~  line4="— — ◇ — — — — — —"
  - y4>3*step_x and y4<=4*step_x:
~  line4="— — — ◇ — — — — —"
  - y4>4*step_x and y4<=5*step_x:
~  line4="— — — — ◇ — — — —"
  - y4>5*step_x and y4<=6*step_x:
~  line4="— — — — — ◇ — — —"
  - y4>6*step_x and y4<=7*step_x:
~  line4="— — — — — — ◇ — —"
  - y4>7*step_x and y4<=8*step_x:
~  line4="— — — — — — — ◇ —"
  - y4>8*step_x and y4<=9*step_x:
~  line4="— — — — — — — — ◇"
- else:
~  line4= "— — — — — — — — -"
}

{
  - y5>0*step_x and y5<=1*step_x:
~  line5="◇ — — — — — — — —"
  - y5>1*step_x and y5<=2*step_x:
~  line5="— ◇ — — — — — — —"
  - y5>2*step_x and y5<=3*step_x:
~  line5="— — ◇ — — — — — —"
  - y5>3*step_x and y5<=4*step_x:
~  line5="— — — ◇ — — — — —"
  - y5>4*step_x and y5<=5*step_x:
~  line5="— — — — ◇ — — — —"
  - y5>5*step_x and y5<=6*step_x:
~  line5="— — — — — ◇ — — —"
  - y5>6*step_x and y5<=7*step_x:
~  line5="— — — — — — ◇ — —"
  - y5>7*step_x and y5<=8*step_x:
~  line5="— — — — — — — ◇ —"
  - y5>8*step_x and y5<=9*step_x:
~  line5="— — — — — — — — ◇"
- else:
~  line5= "— — — — — — — — -"
}

{
  - y6>0*step_x and y6<=1*step_x:
~  line6="◇ — — — — — — — —"
  - y6>1*step_x and y6<=2*step_x:
~  line6="— ◇ — — — — — — —"
  - y6>2*step_x and y6<=3*step_x:
~  line6="— — ◇ — — — — — —"
  - y6>3*step_x and y6<=4*step_x:
~  line6="— — — ◇ — — — — —"
  - y6>4*step_x and y6<=5*step_x:
~  line6="— — — — ◇ — — — —"
  - y6>5*step_x and y6<=6*step_x:
~  line6="— — — — — ◇ — — —"
  - y6>6*step_x and y6<=7*step_x:
~  line6="— — — — — — ◇ — —"
  - y6>7*step_x and y6<=8*step_x:
~  line6="— — — — — — — ◇ —"
  - y6>8*step_x and y6<=9*step_x:
~  line6="— — — — — — — — ◇"
- else:
~  line6= "— — — — — — — — -"
}

{
  - y7>0*step_x and y7<=1*step_x:
~  line7="◇ — — — — — — — —"
  - y7>1*step_x and y7<=2*step_x:
~  line7="— ◇ — — — — — — —"
  - y7>2*step_x and y7<=3*step_x:
~  line7="— — ◇ — — — — — —"
  - y7>3*step_x and y7<=4*step_x:
~  line7="— — — ◇ — — — — —"
  - y7>4*step_x and y7<=5*step_x:
~  line7="— — — — ◇ — — — —"
  - y7>5*step_x and y7<=6*step_x:
~  line7="— — — — — ◇ — — —"
  - y7>6*step_x and y7<=7*step_x:
~  line7="— — — — — — ◇ — —"
  - y7>7*step_x and y7<=8*step_x:
~  line7="— — — — — — — ◇ —"
  - y7>8*step_x and y7<=9*step_x:
~  line7="— — — — — — — — ◇"
- else:
~  line7= "— — — — — — — — -"
}

{
  - y8>0*step_x and y8<=1*step_x:
~  line8="◇ — — — — — — — —"
  - y8>1*step_x and y8<=2*step_x:
~  line8="— ◇ — — — — — — —"
  - y8>2*step_x and y8<=3*step_x:
~  line8="— — ◇ — — — — — —"
  - y8>3*step_x and y8<=4*step_x:
~  line8="— — — ◇ — — — — —"
  - y8>4*step_x and y8<=5*step_x:
~  line8="— — — — ◇ — — — —"
  - y8>5*step_x and y8<=6*step_x:
~  line8="— — — — — ◇ — — —"
  - y8>6*step_x and y8<=7*step_x:
~  line8="— — — — — — ◇ — —"
  - y8>7*step_x and y8<=8*step_x:
~  line8="— — — — — — — ◇ —"
  - y8>8*step_x and y8<=9*step_x:
~  line8="— — — — — — — — ◇"
- else:
~  line8= "— — — — — — — — -"
}



== function f(x) ==
~ return (  (x*x)  )
//       ^^^^^^^^^^^^^^^^^^^^^^^^
//在这个括号里输入函数表达式

== function y() ==
~ initial_y= f(initial_x)-offset_y
~ y1= f(initial_x+step_x)-offset_y
~ y2= f(initial_x+2*step_x)-offset_y
~ y3= f(initial_x+3*step_x)-offset_y
~ y4= f(initial_x+4*step_x)-offset_y
~ y5= f(initial_x+5*step_x)-offset_y
~ y6= f(initial_x+6*step_x)-offset_y
~ y7= f(initial_x+7*step_x)-offset_y
~ y8= f(initial_x+8*step_x)-offset_y


== set ==
~ initial_x= 0.01
~ step_x=1.01
~ offset_y = 0.01
-> operation
== operation ==
+ 左移1单位—>{initial_x-1}
~ initial_x=initial_x-1
+ 右移1单位—>{initial_x+1}
~ initial_x=initial_x+1
+ 上移1单位—>{offset_y+1}
~ offset_y=offset_y+1
+ 下移1单位—>{offset_y-1}
~ offset_y=offset_y-1
+ 缩小1倍
~ step_x=step_x*2
+ 放大1倍
~ step_x=step_x/2
+ 显示图像
-> start ->
- -> operation


-> start
== start ==
~ y()
~ line()
```
步长：{step_x}
x:{initial_x}～{initial_x+step_x*9}
y:{offset_y}～{step_x*9+offset_y}

{initial_line}
{line1}
{line2}
{line3}
{line4}
{line5}
{line6}
{line7}
{line8}
```
->->

-> END

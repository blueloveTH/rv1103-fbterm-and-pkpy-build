INCLUDE gyc.ink
INCLUDE array.ink
点击按钮，看看你的内存什么时候会爆炸吧
VAR a=0
VAR b=0
VAR log=9
[创建元素]VAR t=0
~ a=range(0,100)
-> a1
== a1 ==
+ 【添加{log*100}个元素】
~ add_array(0)

现在是{t}个元素
-> a1
== function add_array(x) ==
{x==log:
  ~ t=t+log*100
  ~ log=log*10
  -else:
~ b=concat(a,array())
~ return add_array(x+1)
}
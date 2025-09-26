INCLUDE gyc.ink
INCLUDE array.ink

INCLUDE 1.ink


//说明书：

//1:  你需要在main.ink文件的靠上位置输入
//    INCLUDE 1.ink

//2:  你需要复制整个1.ink文件的文本，然后到你自己的游戏中新建一个1.ink文件黏贴进去，当然，文件名随意，只要include的文件名和它相同就可以

//3:  在使用时，创建一个用于存储玩家输入信息的变量，而后输入以下代码，尖括号部分需要你按照提示输入

//    ~ back_array = array(<变量>)
//    ->get_num(back_num,<最小值>,<最大值>)
//    ~ <变量> = get(back_array,0)



//以下是一个例子
-> init
== init ==
VAR x = 0
//创建一个变量x用于存储玩家输入的数字

~ x = array(0)
-> get_num(x,0,9999) ->
~ x = get(x,0)
//按提示输入这三行代码


玩家输入了：{x}

-> END

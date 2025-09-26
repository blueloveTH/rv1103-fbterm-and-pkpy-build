
== get_num(back_array,min_num,max_num) ==
~ set(back_array,0,0)
-> choose_num(back_array,min_num,max_num,0) ->
->->
== choose_num(back_array,min_num,max_num,choosen_num) ==

~ temp flag = 0
{ get(back_array,0)*10+choosen_num >= min_num && get(back_array,0)*10+choosen_num <= max_num :
~ set(back_array,0,get(back_array,0)*10+choosen_num)
~ flag = 1
- else :
~ flag = 0
}
+ {flag == 1}
        [确认输入--{get(back_array,0)}]
+ {flag ==0}
        [错误--“{get(back_array,0)*10+choosen_num}”超出范围]
-> choose_num(back_array,min_num,max_num,choosen_num)->



+ [清空]
~ set(back_array,0,0)
-> choose_num(back_array,min_num,max_num,0)->

+ [0]
-> choose_num(back_array,min_num,max_num,0)->
+ [1]
-> choose_num(back_array,min_num,max_num,1)->
+ [2]
-> choose_num(back_array,min_num,max_num,2)->
+ [3]
-> choose_num(back_array,min_num,max_num,3)->
+ [4]
-> choose_num(back_array,min_num,max_num,4)->
+ [5]
-> choose_num(back_array,min_num,max_num,5)->
+ [6]
-> choose_num(back_array,min_num,max_num,6)->
+ [7]
-> choose_num(back_array,min_num,max_num,7)->
+ [8]
-> choose_num(back_array,min_num,max_num,8)->
+ [9]
-> choose_num(back_array,min_num,max_num,9)->

-
->->
//既然每次选择，都会多加一层choose_num隧道，那为什么这里只要一个->->就够了呢？ 原因是，每次隧道结束，都会回到原处，这就意味着，当故事流第一次进入choose_num时，故事流会不断重复得进入choose_num去选择选项，而不是走最后的-，直到玩家选择了确认输入时，故事流才会走到-，到这一步后，故事流便通过->->回到上一层choose_num的隧道出口，而巧妙的是，该层出口的下一句正好就是该层的-，于是故事流便又回到了上上层choose_num。。。（我真是个天才doge）

= progress(back_array,min_num,max_num,choosen_num)
{
    - get(back_array,0)+choosen_num>=min_num && get(back_array,0)+choosen_num<=max_num :
~ set(back_array,0,get(back_array,0)*10+choosen_num)
}
->->
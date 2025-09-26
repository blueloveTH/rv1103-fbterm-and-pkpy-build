INCLUDE gyc.ink
INCLUDE array.ink
INCLUDE news_queue.ink

VAR month = 1
VAR date = 10
VAR time = 0
VAR emo = 50
VAR buff = 100

VAR homework_num = 0
VAR time_need = 0
VAR rate_add = 0
VAR emo_add = 0

VAR entertain_time_need = 0
VAR emo_remove = 0

~ homework_num = array(0,0,0,0,0)
~ time_need = array(1,2,2,3,5)
~ rate_add = array(2,4,5,10,25)
~ emo_add = array(5,10,10,20,60)

~ entertain_time_need = array(1,2,5,8,10)
~ emo_remove = array(-5,-12,-35,-60,-85)

-> main

== main ==
-> introduce


== introduce ==
版本：1.3

介绍：
现在是寒假（1月20日），你需要在一个月的时间內完成所有的作业，每个作业都会增加emo值，而娱乐可以降低。

当emo值满，你将不得不进行为期3天的休息。

每一天，你都拥有10个可分配时段完成作业或者进行娱乐，请合理安排时间。

注意：你需要在2月20日前完成所有的作业

（这是第一版，平衡性也许不太好。）

+ [开始游戏]
-> cycle_1

== cycle_1 ==
~ temp select_news = 0
+ [-------------------------------------------]
~ select_news = 1
+ {news_num>0}[{news_queue.get(0)}]
~ select_news = 1
+ {news_num>1}[{news_queue.get(1)}]
~ select_news = 1
+ {news_num>2}[{news_queue.get(2)}]
~ select_news = 1
+ [--------------------------------------]
-> cycle_1
+ [时间：{month}月{date}日 时段: {time}/10]
-> cycle_1
+ [emo值: {emo}%  学习效率：{buff}%]
-> cycle_1
+ [睡觉（进入下一天）]
-> sleep ->
-> cycle_1
+ [--------------------------------------]
-> cycle_1
+ [娱乐]
-> entertain ->
+ [写作业]
-> homework ->
+ [--------------------------------------]
-> cycle_1
- 
{
  - select_news == 1:
    -> cycle_1
}
-> cycle_1

== entertain ==
~ temp select_news = 0
+ [-------------------------------------------]
~ select_news = 1
+ {news_num>0}[{news_queue.get(0)}]
~ select_news = 1
+ {news_num>1}[{news_queue.get(1)}]
~ select_news = 1
+ {news_num>2}[{news_queue.get(2)}]
~ select_news = 1
+ [--------------------------------------]
+ [时间：{month}月{date}日 时段: {time}/10]
-> entertain
+ [emo值: {emo}%  学习效率：{buff}%]
-> entertain
+ [睡觉（进入下一天）]
-> sleep ->
-> entertain
+ [--------------------------------------]
-> entertain
+ [娱乐1  emo {emo_remove.get(0)}%]
-> do_entertainment(0) -> entertain
+ [娱乐2  emo {emo_remove.get(1)}%]
-> do_entertainment(1) -> entertain
+ [娱乐3  emo {emo_remove.get(2)}%]
-> do_entertainment(2) -> entertain
+ [娱乐4  emo {emo_remove.get(3)}%]
-> do_entertainment(3) -> entertain
+ [娱乐5  emo {emo_remove.get(4)}%]
-> do_entertainment(4) -> entertain
+ [--------------------------------------]
-> entertain
+ [写作业]
-> homework
- 
{
  - select_news == 1:
    ->entertain
}
->entertain

== homework ==
~ temp select_news = 0
+ [-------------------------------------------]
~ select_news = 1
+ {news_num>0}[{news_queue.get(0)}]
~ select_news = 1
+ {news_num>1}[{news_queue.get(1)}]
~ select_news = 1
+ {news_num>2}[{news_queue.get(2)}]
~ select_news = 1
+ [--------------------------------------]
+ [时间：{month}月{date}日 时段: {time}/10]
-> homework
+ [emo值: {emo}%  学习效率：{buff}%]
-> homework
+ [睡觉（进入下一天）]
-> sleep ->
-> homework
+ [--------------------------------------]
-> homework
+ [娱乐]
-> entertain 

+ [--------------------------------------]
-> homework
+ [作业1  进度：{homework_num.get(0)}%]
-> do_homework(0) ->
+ [作业2  进度：{homework_num.get(1)}%]
-> do_homework(1) ->
+ [作业3  进度：{homework_num.get(2)}%]
-> do_homework(2) ->
+ [作业4  进度：{homework_num.get(3)}%]
-> do_homework(3) ->
+ [作业5  进度：{homework_num.get(4)}%]
-> do_homework(4) ->
-
-> homework

== do_entertainment(pos) ==
{
  - time + entertain_time_need.get(pos) > 10:
    ~ news_queue_push(news_queue, "你没有时间娱乐了，赶紧睡觉吧")
    ->->
}
-> add_emo(emo_remove.get(pos)) ->
-> add_time(entertain_time_need.get(pos)) ->
~ news_queue_push(news_queue, "正在进行娱乐{pos+1}，emo{emo_remove.get(pos)}%，时间消耗{entertain_time_need.get(pos)}")
->->

== do_homework(pos) ==
{
  - homework_num.get(pos) >= 100:
~ news_queue_push(news_queue, "作业{pos+1}做完了")
->->
  - else:
  {
    - time + time_need.get(pos) > 10:
      ~ news_queue_push(news_queue, "你没有时间写这个作业了，换一个作业或者睡觉吧")
      ->->
  }
}
-> add_emo(emo_add.get(pos)) ->
-> add_time(time_need.get(pos)) ->
-> add_homework_num(pos) ->
~ news_queue_push(news_queue, "正在写作业{pos+1}，emo+{emo_add.get(pos)}%, 时间消耗{time_need.get(pos)}，完成进度{INT(rate_add.get(pos)*0.01*buff)}")
->->

== sleep ==
~ time = 0
~ emo = emo - emo/5
~ news_queue_push(news_queue, "你睡了一觉，emo值降低到{emo}%，学习效率变更至{-emo+150}")
~ buff = -emo+150
-> add_date ->
{
  - homework_num.get(0) == 100 && homework_num.get(1) == 100 && homework_num.get(2) == 100 && homework_num.get(3) == 100 && homework_num.get(4) == 100:
    -> win
}
->->

== add_emo(x) ==
~ emo = emo + x
{
  - emo >= 100:
    ~ news_queue_push(news_queue, "你的emo值爆表了！")
    ~ news_queue_push(news_queue, "3天过后，你的emo值回到了80%")
    ~ emo = 80
    -> add_date ->
    -> add_date ->
    -> add_date ->
    ->->
}
{
  - emo <= 0:
    ~ emo = 0
}
->->

== add_time(x) ==
~ time = time + x
{
  - time > 10:
    ~ time = time - x
    ~ news_queue_push(news_queue, "你没有时间写这个作业了，换一个作业或者睡觉吧")
    ->->
}
->->

== add_date ==
~ date = date + 1
{
  - date >= 31:
    ~ month = month +1
    ~ date = date - 30
  - else:
    {
      - month == 2 && date >= 20:
      -> gameover
    }
}
~ news_queue_push(news_queue, "时间：{month}月{date}日")

->->

== add_homework_num(pos) ==
~ homework_num.set(pos, homework_num.get(pos) + INT(rate_add.get(pos)*0.01*buff))
{
  - homework_num.get(pos) > 100:
    ~ homework_num.set(pos, 100)
    ~ news_queue_push(news_queue, "这一门作业已经完成了")
    ~ time = time - time_need.get(pos)
}
->->

== gameover ==
现在是2月20日，而你并没有完成所有的作业
-> END

== win ==
恭喜你完成了所有的作业
-> END
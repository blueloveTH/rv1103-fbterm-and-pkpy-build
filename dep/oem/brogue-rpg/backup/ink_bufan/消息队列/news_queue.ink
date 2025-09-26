VAR news_queue = 0
VAR news_num = 10

~ news_queue = array()
~ init_news_queue(news_queue,news_num)

== list_queue ==
~ temp select_news = 0
+ [-------------------消息----------------------]
~ select_news = 1
+ {news_num>0}[{news_queue.get(0)}]
~ select_news = 1
+ {news_num>1}[{news_queue.get(1)}]
~ select_news = 1
+ {news_num>2}[{news_queue.get(2)}]
~ select_news = 1
+ {news_num>3}[{news_queue.get(3)}]
~ select_news = 1
+ {news_num>4}[{news_queue.get(4)}]
~ select_news = 1
+ {news_num>5}[{news_queue.get(5)}]
~ select_news = 1
+ {news_num>6}[{news_queue.get(6)}]
~ select_news = 1
+ {news_num>7}[{news_queue.get(7)}]
~ select_news = 1
+ {news_num>8}[{news_queue.get(8)}]
~ select_news = 1
+ {news_num>9}[{news_queue.get(9)}]
~ select_news = 1
+ [-------------------------------------------]
~ select_news = 1
+ [加一条信息]
~ news_queue_push(news_queue,str(POW(RANDOM(2,10),RANDOM(0,10))))
+ [清空]
~ news_queue_clear(news_queue)
- 
{
  - select_news == 1:
    ->list_queue
}
->list_queue

== function init_news_queue(queue,num) ==
{
  - num > 0:
    ~ queue.push("")
    ~ init_news_queue(queue,num-1)
}

== function news_queue_clear(queue) ==
~ queue.clear_arr()
~ init_news_queue(queue,news_num)

== function news_queue_push(queue, news) ==
~ queue.push(news)
~ queue.del_arr(0)

== function del_arr(a_array, pos) ==
//删除pos位置元素的函数
~ temp a_piece = a_array.slice(0,pos)
~ temp b_piece = a_array.slice(pos+1,len(a_array))
~ a_array.clear_arr()
~ a_piece.concat_to_arr(a_array)
~ b_piece.concat_to_arr(a_array)

== function concat_to_arr(template_array, aim_array) ==
//将一个数组拼接到到另一个数组的函数
~ concat_to_arr_while_1(template_array, aim_array, 0)

== function concat_to_arr_while_1(template_array, aim_array, i)==
{
  - i!=len(template_array):
  ~ aim_array.push(0)
  ~ aim_array.set(len(aim_array)-1, template_array.get(i))
  ~ concat_to_arr_while_1(template_array, aim_array, i+1)
}

== function clear_arr(a_array) ==
//一个通用的清空函数，可以将传入数组变成一个空数组
{
  - len(a_array)!=0:
  ~ a_array.pop()
  ~ clear_arr(a_array)
}


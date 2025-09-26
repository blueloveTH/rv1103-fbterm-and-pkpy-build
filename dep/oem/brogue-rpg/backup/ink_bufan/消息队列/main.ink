INCLUDE gyc.ink
INCLUDE array.ink
INCLUDE news_queue.ink
-> init

== init ==
~ news_queue_clear(news_queue)
{str(news_queue)}
-> list_queue

-> END


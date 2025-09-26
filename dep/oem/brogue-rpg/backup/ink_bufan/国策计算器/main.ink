INCLUDE gyc.ink
INCLUDE array.ink
INCLUDE amount.ink
-> start
== start ==
+ [数据]
-> information ->
+ 前进一年
~ time = time+1

-> information ->
- -> start
== information ==
```
>>>>>>>>>>>>>>>>>>>
时间：{time}年
人口：{population}({pop_rate-pop_rate_dec}%倍/年)
GDP： {GDP}/年
税率：{tax_rate}
资金: {money}({m_rate-m_rate_dec}%/年)
国土: {land}/{max_land}({land_rate}%)
知识水平：{education}({edu_speed}/年)
总科技点：{science_point}({sp_speed}/年)
掌控力：{control_power}
民众支持率: ({satisfaction}%)
军力: {army_power}
士兵数量：{army}
行政点：{policy_point}   科技点：{science_point}
.
粮食作物：{resources1}({r1_speed}/年)   工业作物：{resources2}({r2_speed}/年)
矿物：{resources3}({r3_speed}/年)   环境：{resources4}%({r4_speed}%/年)
.
产品1：{production1}({pro1_speed}/年)   产品2：{production2}({pro2_speed}/年)
产品3：{production3}({pro3_speed}/年)   产品4：{production4}({pro4_speed}/年)
产品5：{production5}({pro5_speed}/年)   产品6：{production6}({pro6_speed}/年)
产品7：{production7}({pro7_speed}/年)   产品8：{production8}({pro8_speed}/年)
```
->->
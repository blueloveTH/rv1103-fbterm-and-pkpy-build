INCLUDE gyc.ink
INCLUDE array.ink
//a，b种子
VAR ablood = 60.0
VAR bblood = 60.0
VAR aattack = 60
VAR battack = 60
VAR anum = 20
VAR bnum = 10
//防御树
VAR tattack = 60
VAR tnum = 3
VAR t = "b"
//被攻击树
VAR aimtreeblood = 600
VAR aimtreenum = 1
VAR aimtreerecover = 10
VAR aimtree = "b"
//无关
VAR anum1 = 0
VAR bnum1 = 0

//轮
VAR k = 6

```
开始
a:{anum}
b:{bnum}
被攻击树血量：{aimtreeblood}
```

-> init

== init ==
~ k = k+1
~ anum1 = zer((ablood*anum-battack/10*bnum)/ablood)
~ bnum1 = zer((bblood*bnum-aattack/10*anum)/bblood)

{t == "a":
~ bnum1 = zer((bblood*bnum1-tattack/2*tnum)/bblood)
-else:
{t=="b":
~ anum1 = zer((ablood*anum1-tattack/2*tnum)/bblood)
}
}


{aimtree == "a" :
~ aimtreeblood = aimtreeblood - bnum1*battack/10/aimtreenum + aimtreerecover
-else:
{aimtree=="b":
~ aimtreeblood = aimtreeblood - anum1*aattack/10/aimtreenum + aimtreerecover
}
}

~ anum = anum1
~ bnum = bnum1
```
第{k}游戏刻
a:{INT(anum)}
b:{INT(bnum)}
被攻击树血量：{INT(aimtreeblood)}
```
-> init


== function zer(x) ==
{x<=0:
~ return 0
-else:
~ return x
}


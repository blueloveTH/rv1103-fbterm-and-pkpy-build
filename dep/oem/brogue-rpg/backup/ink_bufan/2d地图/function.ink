== function TranslateObj(x) ==
{
 - x == 0: ~ return "⬛️"
 - x == 1: ~ return "🔥"
 - x == 2: ~ return "🗡"
 - x == 3: ~ return "🏚"
}
== function ShowMapLine(line) ==
~ temp W = 0
~ W = map(slice(world,11*line,11+11*line),->TranslateObj)
~ return "{get(W,0)}{get(W,1)}{get(W,2)}{get(W,3)}{get(W,4)}{get(W,5)}{get(W,6)}{get(W,7)}{get(W,8)}{get(W,9)}{get(W,10)}"

== function World2dSet(x,y,n) ==
~ set(world,11*y+x,n)

== function Entity2dSetline(line,x,y,n) ==
~ set(entity,3*line+0,x)
~ set(entity,3*line+1,y)
~ set(entity,3*line+2,n)
== function Entity2dget(x,y) ==
~ return get(entity,3*y+x)

== function LoadEntity(y) ==
{
 - y < m*(MaxPosition-MinPosition):
  {
   - (Entity2dget(0,y)-dx+5)+(Entity2dget(1,y)-dy+5)*11 <= 120 and (Entity2dget(0,y)-dx+5)+(Entity2dget(1,y)-dy+5)*11 >= 0 and (Entity2dget(0,y)-dx+5) <= 10 and (Entity2dget(0,y)-dx+5) >= 0:
  ~ World2dSet(Entity2dget(0,y)-dx+5,Entity2dget(1,y)-dy+5,Entity2dget(2,y))
  ~ y = y + 1
  ~ LoadEntity(y)
   - else :
  ~ y = y + 1
  ~ LoadEntity(y)
  }
 - else :
  ~ return 1
}


== function RN(X,Z,n,i) ==
~ X = RANDOM(MinPosition,MaxPosition)
{
 - contains(Z,X) == false :
  ~ push(Z,X)
  {
   - i >= n-1 :
    ~ return Z
   - else :
    ~ return RN(X,Z,n,i+1)
  }
 - else :
  ~ return RN(X,Z,n,i)
}
== function RandomNumberX(n) ==
~ temp X = 0
~ temp Z = 0
~ temp i = 0
~ Z = array()
~ return RN(X,Z,n,i)
== function RandomNumberY(Y,i) ==
{
 - i >= (MaxPosition-MinPosition)-1 :
  ~ return Y
 - else :
  ~ Y = concat(Y,RandomNumberX(m))
  ~ return RandomNumberY(Y,i+1)
}



== function RP(X,Y,kind,i,o,n) ==
{
 - i < (MaxPosition-MinPosition) :
  {
   - o < n - 1 :
    ~ Entity2dSetline((i*n+o),get(X,(i)),get(Y,i*n+o),kind)
    
    ~ return RP(X,Y,kind,i,o+1,n)
   - else :
    ~ return RP(X,Y,kind,i+1,0,n) 
  }
 - else:
~ return 
}

== function RandomPosition(kind,i) ==
~ temp X = 0
~ X = range(MinPosition,MaxPosition)
~ temp Y = 0
~ Y = array()
~ Y = RandomNumberX(m)
~ Y = RandomNumberY(Y,0)
~ RP(X,Y,kind,i,0,m)




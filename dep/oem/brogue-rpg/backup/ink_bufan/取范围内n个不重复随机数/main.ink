INCLUDE gyc.ink
INCLUDE array.ink
-> v
== function RN(min,max,X,Z,n,i) ==
~ X = RANDOM(min,max)
{
 - contains(Z,X) == false :
  ~ push(Z,X)
  {
   - i >= n :
    ~ return Z
   - else :
    ~ return RN(min,max,X,Z,n,i+1)
  }
 - else :
  ~ return RN(min,max,X,Z,n,i+1)
}
== function RandomNumber(min,max,n) ==
~ temp X = 0
~ temp Z = 0
~ temp i = 0
~ Z = array()
~ return RN(min,max,X,Z,n,i)

== v ==
{str(RandomNumber(0,400,6))}
-> DONE




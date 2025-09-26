INCLUDE gyc.ink
INCLUDE array.ink
INCLUDE amount.ink
INCLUDE fn.ink
INCLUDE sentence.ink
INCLUDE tabletop.ink
.

== function _init() ==
~ temp1 = array()
~ temp2 = array()
~ temp3 = ""
~ i = 0
~ u = 0
~ _chess = 0
~ _just_x = 0
~ _just_y = 0

~ _chessboard= concat(range(0,length*width,1),zeros(length*width*(height-1)+3))
//第一层：表示位置
//第二层：0格子 1紫子 2白子
== function _draw() ==
~ temp1 = array()
......五子棋......//当调整宽度时，此处文本也需要调整
{draw_chessboard()}
{ _chess == 0 :
    { __player__:
       -0:
        我方落子
        ~ allow = 1
       -else :
        对方落子
        
    }
 - else :
    { _chess mod 2 :
      - __player__:
       我方落子
       ~ allow = 1
      - else :
       对方落子
    }
}

== function _on_tap(q) ==
~ qq = q
{ allow == 1:

~ temp x = q-width

{ coordinate_get_chessboard(x mod width,INT(x/width),1) :
  -0:
  ~ _just_x = x mod width
  ~ _just_y = INT(x/width)
  ~ coordinate_set_chessboard(_just_x,_just_y,1,_chess mod 2 + 1)
  ~ refresh()
  ~ _chess = _chess + 1
  ~ allow = 0
}
~ sync()
~ refresh()

}

#!/usr/bin/wish
catch { unset universe neighbours new_universe}
global zeile spalte  universe new_universe neighbours
proc readUniverse { } {
  global filename universe
   set filename [ tk_getOpenFile  -filetypes {{Txt .txt} {All *}} ]
   set f [ open $filename r]
   catch {unset universe }
   .life.universe itemconfigure cell -fill white -width 1
    while { [ gets $f line] >= 0 } {
         incr universe($line)
        .life.universe itemconfigure $line -fill red -width 3
     }
   close $f
}

proc saveUniverse { } {
global filename  universe
set filename [ tk_getSaveFile -initialfile live.txt -filetypes {{Txt .txt} {All *}} ]
set f [ open $filename w]
foreach label [ array names universe ] { puts $f $label }
close $f
}

proc draw_life_board args {
global zeile spalte
catch {destroy .life }
toplevel .life

menu .life.mbar
.life configure  -menu .life.mbar
.life.mbar add cascade -label Datei -menu .life.mbar.datei -underline 0
menu .life.mbar.datei
.life.mbar.datei add command -label Öffnen... -command { readUniverse }
.life.mbar.datei add command -label Speichern... -command { saveUniverse }
.life.mbar.datei add separator
.life.mbar.datei add command -label Beende -command { exit }


canvas .life.universe -height 820 -width 780
pack .life.universe
set stager 1
for {set zeile 0} {$zeile<40} {incr zeile } {
  set stager [expr -1*$stager]
  puts $stager
  for {set spalte 0} {$spalte<40} {incr spalte } {
        set koy [ expr round(($spalte+($stager+1.)/4.0)*10.0)  ]
        set kox [ expr $zeile*10 ]
               set tag "xy:$kox:$koy"
        puts $tag
       set circle  [ .life.universe create oval [ expr ($spalte*20+20+($stager*5))] [expr ($zeile*20*sqrt(3.0)/2+20)] \
                    [ expr ($spalte*20+40+($stager*5))] [expr ($zeile*20*sqrt(3.0)/2+40)] -fill white -tags "$tag cell" ]
       .life.universe bind $circle <ButtonPress-1> " toggleCell $tag"
    } }

 button .life.singlestep -text Step -command { set goon 0 ; go }
 button .life.start -text Start  -command { set goon 1 ; go }
 button .life.stop -text  Stop  -command { set goon 0 }
 button .life.clear -text Lösche \
     -command { global goon; set goon 0; \
      .life.universe itemconfigure \
      cell -fill white -width 1; catch { unset universe }}
 scale  .life.speed -length 4cm -width 0.25cm -variable speed -orient horizontal -from 1 -to 100
 pack .life.singlestep .life.start .life.stop .life.clear -side left
 pack .life.speed -side right

}

proc toggleCell cell {
     global universe
     set lebt [ info exists universe($cell) ]
     if { $lebt  } {
       .life.universe itemconfigure $cell -fill white -width 1
        unset universe($cell)
 #       puts "unset"
        } else  {
      .life.universe itemconfigure $cell -fill red -width 5
       incr universe($cell)
 #      puts "Set"
     }
 #    puts [ array names universe ]
      calculateNeighbours
}
puts "toggleCell"

set neighbour_color { #00000 #f0f080 #f0f000 #f08000 #F00000 #800080 #000080 }
proc calculateNeighbours {} {
global universe neighbours neighbour_color
catch { unset neighbours }
foreach label [ array names universe ] {
 lassign [ split  $label ":"] dummy x y
 incrNeighbour $x [ expr $y+10 ]
 incrNeighbour $x [ expr $y-10 ]
 incrNeighbour [ expr $x-10 ] [ expr $y-5 ]
 incrNeighbour [ expr $x-10 ] [ expr $y+5 ]
 incrNeighbour [ expr $x+10 ] [ expr $y-5 ]
 incrNeighbour [ expr $x+10 ] [ expr $y+5 ]
 }
  .life.universe itemconfigure cell -fill white
  foreach label [ array names neighbours ] {
       .life.universe itemconfigure $label -fill [ lindex $neighbour_color $neighbours($label) ]
   }

}
puts "calculateNeighbours"

proc incrNeighbour { x y } {
 global neighbours
 set x [ expr ($x%400) ]
 set y [ expr ($y%400) ]

 if { ($x>=0) && ($x<400) && ($y>=0) && ($y<400) } {
  set tag "xy:$x:$y"
  incr neighbours($tag)
 }
}

puts "incrNeighbour"

proc nextUniverse {} {
  global universe neighbours neighbour_color
  foreach label [ array names neighbours ] {
  if [ info exists universe($label)]  {
      if {($neighbours($label)>1) && ($neighbours($label)<3)} {
         incr new_universe($label)
      }
  } else {
         if {($neighbours($label)>1) && ($neighbours($label)<3)} {
          incr new_universe($label)
          }
  }
  }
  catch { unset universe }
  .life.universe itemconfigure cell  -width 1
  foreach label [ array names new_universe ] {
     incr universe($label)
     .life.universe itemconfigure $label  -width 9 -fill black
  }
   .life.universe itemconfigure cell -fill white
   foreach label [ array names neighbours ] {
       .life.universe itemconfigure $label -fill [ lindex $neighbour_color $neighbours($label) ]
  }
}

global goon
set goon 1
proc stepUniverse {} {
 calculateNeighbours
 nextUniverse
 calculateNeighbours
}

global color

proc go {} {
stepUniverse
global goon speed
if { $goon != 0} { after  [ expr round(2000./$speed) ] go }
}

proc stop {} { global goon; set goon 0 }

draw_life_board;



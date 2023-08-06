1 {a(1..3)}.
a(2) :- a(3). 
a(3) :- a(2).

{ extra(1..5) } :- a(1).

_heuristic(a(1..3),false,1).

object(a;b).

{ thing(a) ; thing(b) }.

_heuristic(thing(X), true, 1) :- object(X).

#show _heuristic/3.
#show thing/1.

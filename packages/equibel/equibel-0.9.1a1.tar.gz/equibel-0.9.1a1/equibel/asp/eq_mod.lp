edge(X,Y) :- edge(Y,X).

subformula(N,S) :- formula(N,S).
subformula(N,S) :- subformula(N, and(S,_)).
subformula(N,S) :- subformula(N, and(_,S)).
subformula(N,S) :- subformula(N, or(S,_)).
subformula(N,S) :- subformula(N, or(_,S)).
subformula(N,S) :- subformula(N, implies(S,_)).
subformula(N,S) :- subformula(N, implies(_,S)).
subformula(N,S) :- subformula(N, iff(S,_)).
subformula(N,S) :- subformula(N, iff(_,S)).
subformula(N,S) :- subformula(N, neg(S)).

compound_prop(N,F) :- F = and(A,B), subformula(N,F), subformula(N,A), subformula(N,B).
compound_prop(N,F) :- F = or(A,B), subformula(N,F), subformula(N,A), subformula(N,B).
compound_prop(N,F) :- F = implies(A,B), subformula(N,F), subformula(N,A), subformula(N,B).
compound_prop(N,F) :- F = iff(A,B),	subformula(N,F), subformula(N,A), subformula(N,B).
compound_prop(N,F) :- F = neg(A), subformula(N,F), subformula(N,A).

atom(N,P) :- subformula(N,P), not compound_prop(N,P).
atom(P)   :- atom(_,P).

satisfied(N,P) :- set(N,P,1,t), atom(N,P).
satisfied(N,neg(P)) :- set(N,P,0,t), atom(N,P).
satisfied(N,F) :- F = and(A,B), satisfied(N,A), satisfied(N,B), subformula(N,F), subformula(N,A), subformula(N,B).
satisfied(N,F) :- F = or(A,B),  satisfied(N,A), subformula(N,F), subformula(N,A), subformula(N,B).
satisfied(N,F) :- F = or(A,B),  satisfied(N,B), subformula(N,F), subformula(N,A), subformula(N,B).
satisfied(N,F) :- F = implies(A,B),  not satisfied(N,A), subformula(N,F), subformula(N,A), subformula(N,B).
satisfied(N,F) :- F = implies(A,B),      satisfied(N,B), subformula(N,F), subformula(N,A), subformula(N,B).
satisfied(N,F) :- F = iff(A,B),          satisfied(N,A), satisfied(N,B), subformula(N,F), subformula(N,A), subformula(N,B).
satisfied(N,F) :- F = iff(A,B),      not satisfied(N,A), not satisfied(N,B), subformula(N,F), subformula(N,A), subformula(N,B).
satisfied(N,F) :- F = neg(A),        not satisfied(N,A), subformula(N,F), subformula(N,A).


{ set(P,X,Y,e) : atom(P), edge(X,Y), X < Y }.

1 { set(N,P,1,t) ; set(N,P,0,t) } 1 :- atom(P), node(N).

:- set(P,X,Y,e), edge(X,Y), set(X,P,V,t), set(Y,P,W,t), V != W.
:- formula(N,F), not satisfied(N,F).

eq(P,X,Y) :- set(P,X,Y,e).
tv(N,P,V) :- set(N,P,V,t).

_heuristic(set(P,X,Y,e), true, 1) :- atom(P), edge(X,Y), X < Y.
_heuristic(set(N,P,0,t), init, 2) :- node(N), atom(P).
_heuristic(set(N,P,1,t), init, 2) :- node(N), atom(P).

#show _heuristic/3.
#show eq/3.
#show set/4.
#show tv/3.

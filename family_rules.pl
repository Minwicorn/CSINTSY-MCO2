:- dynamic parent/2.
:- dynamic male/1.
:- dynamic female/1.
:- dynamic sibling/2.
:- dynamic brother/2.
:- dynamic sister/2.
:- dynamic grandfather/2.
:- dynamic grandmother/2.
:- dynamic uncle/2.
:- dynamic aunt/2.
:- dynamic child/2.
:- dynamic daughter/2.
:- dynamic son/2.
:- dynamic grandparent/2.
:- dynamic related/2.
:- dynamic older/2.
:- dynamic younger/2.

% General Relation Rule: Two people are related if any familial relationship exists
related(X, Y) :- parent(X, Y).
related(X, Y) :- parent(Y, X).
related(X, Y) :- sibling(X, Y).
related(X, Y) :- grandparent(X, Y).
related(X, Y) :- grandparent(Y, X).
related(X, Y) :- uncle(X, Y).
related(X, Y) :- uncle(Y, X).
related(X, Y) :- aunt(X, Y).
related(X, Y) :- aunt(Y, X).
related(X, Y) :- cousin(X, Y).

% Makes related work
assert_related(X, Y) :-
    (related(X, Y) -> true; assertz(related(X, Y))),
    (related(Y, X) -> true; assertz(related(Y, X))). 

initialize_related :-
    forall((parent(X, Y); sibling(X, Y); grandparent(X, Y); uncle(X, Y); aunt(X, Y); cousin(X, Y); ancestor(X, Y)),
           assert_related(X, Y)).

% Older Rule: Same rule as related, but only works for if someone predates another person
older(X, Y) :- parent(X, Y).
older(X, Y) :- grandparent(X, Y).
older(X, Y) :- uncle(X, Y).
older(X, Y) :- aunt(X, Y).

younger(X, Y) :- older(Y,X).

% Makes older work
assert_older(X, Y) :-
    (older(X, Y) -> true; assertz(older(X, Y))).

% Parent and Gender-based Relations
father(X, Y) :- parent(X, Y), male(X).
mother(X, Y) :- parent(X, Y), female(X).

% Sibling inference
sibling(X, Y) :- parent(Z, X), parent(Z, Y), X \= Y.
sibling(Y, X) :- parent(Z, Y), parent(Z, X), Y \= X.


% Grandparent relationships
grandparent(X, Y) :- parent(X, Z), parent(Z, Y).
grandfather(X, Y) :- grandparent(X, Y), male(X).
grandmother(X, Y) :- grandparent(X, Y), female(X).

% Uncle and Aunt Relations
uncle(X, Y) :- sibling(X, Z), parent(Z, Y), male(X).
aunt(X, Y) :- sibling(X, Z), parent(Z, Y), female(X).

% Child, Daughter, and Son Relationships
child(X, Y) :- parent(Y, X).
daughter(X, Y) :- parent(Y, X), female(X).
son(X, Y) :- parent(Y, X), male(X).

% Extended Family Relations
cousin(X, Y) :- parent(A, X), parent(C, Y), sibling(A, C).
nephew(X, Y) :- sibling(Y, Z), male(X), parent(Z, X).
niece(X, Y) :- sibling(Y, Z), female(X), parent(Z, X).

% Gender Consistency
cannot_be_both_male_and_female(X) :- male(X), female(X), !.
cannot_be_both_male_and_female(X) :- not(male(X)), not(female(X)), !.

% Prevent cyclic relationships or invalid parent assignments
:- parent(X, Y), parent(Y, X).
:- sibling(X, Y), parent(X, Y).

:- initialize_related.

% Facts for Testing
parent(john, mary).
parent(john, mama).
parent(john, maddie).
parent(kiel, john).
parent(kiel, karen).
parent(kiel, bob).
sibling(bob, john).
sibling(bob, karen).

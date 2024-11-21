% Parent and Gender-based Relations
father(X, Y) :- parent(X, Y), male(X).
mother(X, Y) :- parent(X, Y), female(X).
sibling(X, Y) :- parent(Z, X), parent(Z, Y), X \= Y.
grandparent(X, Y) :- parent(X, Z), parent(Z, Y).
grandfather(X, Y) :- grandparent(X, Y), male(X).
grandmother(X, Y) :- grandparent(X, Y), female(X).
uncle(X, Y) :- sibling(X, Z), parent(Z, Y), male(X).
aunt(X, Y) :- sibling(X, Z), parent(Z, Y), female(X).
daughter(X, Y) :- parent(Y, X), female(X).
son(X, Y) :- parent(Y, X), male(X).

% Extended Family Relations
cousin(X, Y) :- sibling(A, B), sibling(C, D), parent(A, X), parent(C, Y).
nephew(X, Y) :- sibling(Y, Z), male(X), parent(Z, X).
niece(X, Y) :- sibling(Y, Z), female(X), parent(Z, X).

% Handling Ancestors and Descendants
ancestor(X, Y) :- parent(X, Y).
ancestor(X, Y) :- parent(X, Z), ancestor(Z, Y).
descendant(X, Y) :- parent(Y, X).
descendant(X, Y) :- parent(Y, Z), descendant(Z, X).

% Gender Consistency
cannot_be_both_male_and_female(X) :- male(X), female(X), !.
cannot_be_both_male_and_female(X) :- not(male(X)), not(female(X)), !.

% Ensuring Parent and Sibling Consistency
parent(X, Y) :- male(X), !. % Optional: Handle general parent relationship
parent(X, Y) :- female(X), !. % Optional: Handle general parent relationship


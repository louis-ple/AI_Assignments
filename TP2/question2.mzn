include "globals.mzn"; 

int: n = 5;
% the given results
array[1..4] of int: res = [1,2,5,7];

% number of points for each player
array[1..n] of var 0..3*n: x;

% (i, j) is the result of player i against player j
array[1..n, 1..n] of var {0,1,3}: matches;
%--------------------------------------------------------------


%contrainte scores totaux
constraint forall(i in index_set(res))(sum(j in 1..5)(matches[i,j])=res[i]);

%contrainte jouer contre sois meme
constraint forall(i in index_set(res))(matches[i,i]=0);

%contrainte partie nulle
constraint forall(i in index_set(res))(forall(j in 1..5) (if matches[i,j] = 1 then matches[j,i] =1 else true endif));

%contrainte partie gagnee-perdu
constraint forall(i in index_set(res))(forall(j in 1..5 where j !=i) (if matches[i,j] = 0 then matches[j,i] =3 else true endif));

%constraint pour determiner les scores
constraint forall(i in index_set(x))(sum(j in 1..5)(matches[i,j])=x[i]);


%--------------------------------------------------------------

output 
[
  "Scores\n"
]
++
[
  show(x)
]
++	
[
  "\nMatches\n"
]
++
[ show(matches[i,j]) ++ 
         if j == n then "\n" else " " endif |
         i in 1..n, j in 1..n
]
;
% Frédérique Roy (1894397) et Louis Plessis (1933334)

include "globals.mzn"; 

int: n; % num rows and columns

int: L = 1; % Lamp
int: P = 2; % Plant

% 1 for a lamp, 2 for a plant and 0 for nothing 
array[1..n,1..n] of 0..2: garden;

% number of plants by row/col
array[1..n] of int: rows;
array[1..n] of int: cols;

% decision variables : position des plantes
array[1..n,1..n] of var 0..P: x;
%--------------------------------------------------------------
array[1..3] of -1..1:a = [-1, 0, 1];

% C1: nb plantes fixe par ligne
%constraint alldifferent_except_0([grid[i,j] | i,j in NUM]);
include "among.mzn";

constraint forall(i in index_set(rows))(count_eq( [x[i,j] | j in index_set(cols)], P, rows[i]));

% C2: nb plantes fixe par colonne
constraint forall(j in index_set(cols))(count_eq( [x[i,j] | i in index_set(rows)], P, cols[j]));


% C3: Les plantes ne doivent pas se toucher horizontalement, verticalement ni en diagonale.

constraint forall(i in index_set(rows))(forall(j in index_set(cols))(forall(a_i in -1..1)(forall(a_j in -1..1)(if x[i, j]=P /\ not(a_j = 0 /\ a_i = 0) /\ i+a_i > 0 /\ i+a_i <= length(rows) /\ j+a_j > 0 /\ j+a_j <= length(cols) then x[i+a_i, j+a_j]=0 else true endif )) ));


% C4: Chaque plante doit être directement à côté d’une lampe solaire (horizontalement ou verticalement).

set of int: L_set = L..L;
set of int: P_set = P..P;

function array[1..4] of var int: case_autour(var int: i, var int: j, var int :n, array[1..n,1..n] of var int: x) = [ if i-1>0 then x[i-1,j] else 0 endif, if i+1<=n then x[i+1,j] else 0 endif, if j-1 > 0 then x[i,j-1] else 0 endif, if j+1<=n then x[i,j+1] else 0 endif];

constraint forall(i in index_set(rows))(forall(j in index_set(cols))( if x[i, j]=P then among( case_autour(i, j, n, garden), L_set)>=1 else true endif));

% C5: Chaque lampe doit être directement à côté d’au moins une plante (horizontalement ou verticalement).

constraint forall(i in index_set(rows))(forall(j in index_set(cols))( if garden[i, j]=L then among( case_autour(i, j, n, x), P_set)>=1 else true endif));

% C6: Les plantes ne peuvent pas être la ou il y a des lampes


constraint forall(i in index_set(rows))(forall(j in index_set(cols))(if garden[i, j]= L then x[i, j]!=P else true endif));

%--------------------------------------------------------------


output 
[
 if j = 1 then "\n" ++ show(rows[i]) ++ " " else " " endif ++
   if fix(x[i,j]) = L then "L" elseif fix(x[i,j]) = P then "P" else "_" endif
| i,j in 1..n
] ++ ["\n  "] ++ [show(cols[i]) ++ " " | i in 1..n];

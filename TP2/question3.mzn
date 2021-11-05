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

% C1: nb plantes fixe par ligne
%constraint alldifferent_except_0([grid[i,j] | i,j in NUM]);
include "among.mzn";
constraint forall(i in index_set(rows))(count_eq( [x[i,j] | j in index_set(cols)], P, rows[i]));

% C2: nb plantes fixe par colonne
constraint forall(j in index_set(cols))(count_eq( [x[i,j] | i in index_set(rows)], P, cols[j]));


% C3: Les plantes ne doivent pas se toucher horizontalement, verticalement ni en diagonale.

% C4: Chaque plante doit être directement à côté d’une lampe solaire (horizontalement ou verticalement).

% C5: Chaque lampe doit être directement à côté d’au moins une plante (horizontalement ou verticalement).

% C6: Les plantes ne peuvent pas être la ou il y a des lampes

%--------------------------------------------------------------


output 
[
 if j = 1 then "\n" ++ show(rows[i]) ++ " " else " " endif ++
   if fix(x[i,j]) = L then "L" elseif fix(x[i,j]) = P then "P" else "_" endif
| i,j in 1..n
] ++ ["\n  "] ++ [show(cols[i]) ++ " " | i in 1..n];

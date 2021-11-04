include "globals.mzn"; 
include "alldifferent.mzn";

int: r; % number of rows 
int: c; % number of columns
array[1..r] of int: rowinsects; % total of insects by row
array[1..c] of int: colinsects; % total of insects by col
array[1..r, 1..c] of 0..r*c: knownpositions;  % known number of insects, 0 appears when unknown



array[1..r, 1..c] of var 1..r*c: x; % the final garden grid (decision variable)
%--------------------------------------------------------------

%contrainte pour chaque colonne
% sum(la structure de laquelle je tire mes elements )(ce que j'aditionne atteint avec i)
set of int: columns = 1..c;
set of int: rows = 1..r;

%sum d'une colonne
constraint forall(i in index_set(columns))(sum(j in rows)(x[j,i])=colinsects[i]);

%contrainte pour chaque row
constraint forall(i in index_set(rows))(sum(j in columns)(x[i,j])=rowinsects[i]);

%contrainte known number
constraint forall (i in index_set(rows), j in index_set(columns)  
where knownpositions[i, j] != 0) (x[i,j] = knownpositions[i,j]);


%contrainte pas le mm nb d'insect dans une row ou colonme
%constraint alldifferent(order);

solve satisfy;

%----------------------------------------------------------------
output [
  "["
]
++
[
  if j = 1 then "\n" else "," endif ++
    if fix(x[i,j]) < 10 then "  " else " "  endif ++
    show(x[i,j]) ++
  if j = c then 
    ", f(" ++ show(rowinsects[i]) ++ "),"
  else 
    ""
  endif
  | i in 1..r, j in 1..c
] 
++
["\n"]++
[
  "f(" ++ show(colinsects[j]) ++ "),"
  | j in 1..c
]

++ ["]\n"]
;
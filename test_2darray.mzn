
int: r = 2; % number of rows 
int: c = 3; % number of columns
array[1..r] of int: rowinsects = [9,12]; % total of insects by row
array[1..c] of int: colinsects = [9, 7, 5]; % total of insects by col
array[1..r, 1..c] of 0..r*c: knownpositions = array2d(1..r, 1..c, 
   [
     0, 0, 3,
     0, 6, 0
   ]);  % known number of insects, 0 appears when unknown

array[1..r, 1..c] of var 1..r*c: x; % the final garden grid (decision variable)
%array[1..r] of var 1..r: x; % the final garden grid (decision variable)
array[1..r, 1..c] of var 1..r*c: temp; % the final garden grid (decision variable)

%----------------------------------------------------------------
set of int: columns = 1..c;
set of int: rows = 1..r;

%sum d'une colonne
constraint forall(i in index_set(columns))(sum(j in rows)(x[j,i])=colinsects[i]);

%constraint forall(i in columns)((sum(j in rows)(x[i,j]))=colinsects[i]);


%contrainte pour chaque row
constraint forall(i in index_set(rows))(sum(j in columns)(x[i,j])=rowinsects[i]);

%constraint forall(j in rows)((sum(i in columns)(x[i,j]))=rowinsects[j]);
%if table[i,j]!=0 then key2[k]=j else true endif

%constraint forall (i in rows, j in columns) (x[i,j] > 1);
%constraint forall(i in index_set(x) where i < j)(x[i] <= x[j]);

%contrainte pas le mm nb d'insect dans une row ou colonme
%constraint alldifferent(order);
include "alldifferent.mzn";

constraint forall(i in index_set(rows))(alldifferent(j in columns)(x[i,j]));
             
constraint forall(j in index_set(columns))(alldifferent(i in rows)(x[i,j]));

%contrainte known nb insect
constraint forall (i in index_set(rows), j in index_set(columns)  
where knownpositions[i, j] != 0) (x[i,j] = knownpositions[i,j]);

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
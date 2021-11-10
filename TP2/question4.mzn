include "globals.mzn";

int: n_nurse; % Number of nurses
int: n_week; % Number of weeks in our horizon
int: n_day; % Number of days in our horizon (7 * n_week). Monday is the first day of the week
int: n_work_period; % Number of work period. It equals 4 (MATIN, SOIREE, NUIT, REPOS)

% Indexing the work periods
int: MATIN = 1;
int: SOIREE = 2;
int: NUIT = 3;
int: REPOS = 4;

int: dur_work_period; % Duration of the work periods (6h)

array[1..n_day,1..n_work_period] of int: demande_min; % Number of nurses required for each day and each work period (= 0 for REPOS)
array[1..n_nurse,1..n_day,1..n_work_period] of int: preference; % Work preference for each nurse

% Decision variables
array[1..n_nurse,1..n_day,1..n_work_period] of var 0..1: x; % work period [MATIN, SOIREE, NUIT, REPOS]
var int: sum_preference;
%--------------------------------------------------------------

% C1 : La demande minimale journalière doit être satisfaite pour chaque période (matin, soiree, nuit).

constraint forall(d in 1..n_day)(forall(w in 1..n_work_period)( sum(n in 1..n_nurse)(x[n, d, w])>=demande_min[d, w]));

% C2 : Une infirmière ne peut travailler que sur une seule période par jour.
%constraint forall(n in 1..n_nurse)(forall(d in 1..n_day)( sum(w in 1..n_work_period)(x[n, d, w])=1));
include "among.mzn";
constraint forall(d in 1..n_day)(forall(n in 1..n_nurse)( among( [x[n, d, w] |w in 1..n_work_period], 1..1 ) = 1));



% C3 : Une infirmière ne peut travailler qu’au maximum 36 heures dans la semaine (du lundi au dimanche).
%% par semaine!!!! pb
%constraint forall(n in 1..n_nurse)( sum(w in 1..n_work_period, d in 1..n_day)(x[n, d, w])<=(36/dur_work_period));


% C4 :  Une infirmière doit travailler au minimum 4 jours dans la semaine.

constraint forall(n in 1..n_nurse)( sum(d in 1..n_day)(x[n, d, 4])<=3);


% C5 :  Une infirmière travaillant de nuit le jour j est obligatoirement en repos le jour j +1.
constraint forall(n in 1..n_nurse)(forall(d in 1..n_day)(forall(w in 1..n_work_period)( if w = 3 /\ x[n, d, w] = 1 /\ d< n_day then x[n, d+1, 4] = 1 endif )));


% C6:  Une infirmière ne peut pas avoir un jour de travail isolé (on interdit la séquence suivante : repos - travail - repos).
constraint forall(n in 1..n_nurse)(forall(d in 1..n_day)(forall(w in 1..n_work_period)( if w != 4 /\ x[n, d, w] = 1 /\ d< n_day /\ d> 1 then (x[n, d+1, 4] != 1 \/ x[n, d-1, 4] != 1) endif ))); 

% C7:  Une infirmière ne peut pas travailler plus de 3 jours consécutifs.

%constraint forall(n in 1..n_nurse)(forall(d in 1..n_day)(forall(w in 1..n_work_period)( if w != 4 /\ x[n, d, w] = 1 /\ d< n_day /\ d> 1 then (x[n, d+1, 4] != 1 \/ x[n, d-1, 4] != 1) endif ))); 


% M1: maximiser la somme des préférences


%--------------------------------------------------------------

output
[
  "total: " ++ show(sum_preference) ++ "\n" ++
  "solution:\n\t    "
]
++
["Day \(j)\t" | j in 1..n_day]
++ 
[ 
  if j = 1 then "\n NURSE \(i): " else "\t" endif ++
    if fix(x[i,j,4]) == 1 then "--" elseif fix(x[i,j,3]) == 1  then "NUIT" elseif fix(x[i,j,2]) == 1  then "SOIREE" elseif fix(x[i,j,1]) == 1 then "MATIN" else "NONE" endif
  | i in 1..n_nurse, j in 1..n_day
];


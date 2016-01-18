echo '#!/bin/bash'
for sub in s1 s2 s3 s4
do
    for act in a1 a2 a3 na1 na2 na3
    do
        for config in {0..103}
        do
        echo 'results/robot-experiments/biorob/'$1'/09-09-2015_'$sub'_'$act'_'$config'.dat'
            if [ ! -e 'results/robot-experiments/biorob/'$1'/09-09-2015_'$sub'_'$act'_'$config'.dat' ]
                then
                 echo 'results/robot-experiments/biorob/'$1'/09-09-2015_'$sub'_'$act'_'$config'.dat'
#                echo qsub pbs/$1-$sub-$act-$config.pbs
            fi
        done
    done
done

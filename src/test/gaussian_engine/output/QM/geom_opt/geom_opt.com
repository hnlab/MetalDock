%mem=4GB
%chk=geom_opt.chk
%nprocshared=32
#P B3LYP/Def2SVP ! ASE formatted method and basis
pop(Hirshfeld)
SCRF(Solvent=Water)
EmpiricalDispersion(GD3BJ)
opt(tight)
IOP(6/7=3)

Gaussian input prepared by ASE

0 1
H                 2.8888100000        2.2556800000       -1.3352300000
C                 1.9781300000        1.7220100000       -1.0952500000
C                 1.9659700000        0.3398500000       -1.0175400000
C                 0.7933300000        2.4038000000       -0.8763900000
H                 2.8609300000       -0.2383600000       -1.2063900000
C                 0.7891000000       -0.3172500000       -0.6791700000
H                 0.7484500000        3.4821400000       -0.9543100000
C                -0.3609400000        1.6950100000       -0.5658200000
C                 0.6444800000       -1.7475500000       -0.5311000000
N                -0.3531400000        0.3538400000       -0.4350300000
C                -1.6793300000        2.2717500000       -0.4265200000
C                 1.5861300000       -2.7237100000       -0.8399600000
N                -0.5543000000       -2.0867700000       -0.0327500000
Ru               -2.0863700000       -0.6646400000        0.1885600000
C                -2.0249700000        3.6147700000       -0.5421600000
N                -2.6229200000        1.3427200000       -0.2204300000
H                 2.5450700000       -2.4275600000       -1.2452900000
C                 1.2874200000       -4.0604400000       -0.6265600000
C                -0.8385000000       -3.3698400000        0.1981100000
O                -2.6862100000       -2.3529600000        1.0774900000
O                -4.0411600000       -0.5406300000        0.2697600000
S                -1.6329700000       -0.0079300000        2.3631600000
H                -1.2482900000        4.3530000000       -0.6943300000
C                -3.3564400000        3.9922500000       -0.4670400000
C                -3.9032900000        1.6982700000       -0.1488500000
H                 2.0115600000       -4.8291800000       -0.8654800000
C                 0.0526900000       -4.3888900000       -0.0849400000
C                -2.1734300000       -3.5185400000        0.8860100000
C                -4.7838800000        0.4966700000        0.0816200000
C                -0.2910000000       -0.9114700000        3.1233200000
C                -3.0768800000       -0.2841600000        3.3785600000
O                -1.2978900000        1.4120800000        2.3704200000
H                 0.6079600000       -0.7292400000        2.5420200000
H                -0.5513800000       -1.9650800000        3.1330700000
H                -0.1821400000       -0.5198500000        4.1319100000
H                -3.8601000000        0.3786700000        3.0226300000
H                -3.3667400000       -1.3259900000        3.2736800000
H                -2.8016900000       -0.0460100000        4.4028200000
H                -3.6366000000        5.0347300000       -0.5518100000
C                -4.3201300000        3.0099300000       -0.2852800000
H                -0.2374200000       -5.4098300000        0.1306500000
O                -2.6299800000       -4.5732700000        1.2463800000
O                -5.9869800000        0.5269200000        0.0784500000
H                -5.3786700000        3.2319600000       -0.2328900000



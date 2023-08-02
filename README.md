```python
from IPython.display import display
from pathlib import Path
from ff_epl.optimisation import optimise
```

# The problem: select a set of players for a fantasy football team such that we maximise the number of points based on an adjusted historical average.

Let $x$ be a vector of players to be selected - our decision variables - with each player indexed by an identification number within set $P$. Let four boolean vectors $g$, $d$, $m$ and $f$ define whether each players is a goalkeeper, defender, midfielder and forward, respectively. Let $c$ and $w$ be the cost and optimisation weight of each player.

Although we're selecting the 11 outfield players we still need to adjust the our budget to ensure we can select bench players; for now, let's assume we can take the cheapest players for each position to sit on the bench. As such, introduce four slack variables to capture the amount of bench players we need for each position; $B^{g}$, $B^{d}$, $B^{m}$, and $B^{f}$. We also need the minimum cost of players for each of these positions, $C^{g}$, $C^{d}$, $C^{m}$, and $C^{f}$. Let $q$ contain the set of position indices, $Q=\{g,d,m,f\}$.

We cannot select more than three players from each team; we will use a boolean vector, $t$, for each team, $t*$, in the EPL where $t \in EPL$ (e.g. $T^{ARS}$ ).

We also don't want to select any players that are injured at the start of the season.

All contraints noted above are outlined inline below.

# Model

$maximise$

$w^{T} x$

$subject \ to$

$\sum\limits_{p=0}^{P}x_{p} = 11$  (select 11 outfield players)

$\sum\limits_{p=0}^{P}x_{p}g_{p} = 1$  (select 1 goalkeeper)

$\sum\limits_{p=0}^{P}x_{p}d_{p} \geq 3$, $\sum\limits_{p=0}^{P}x_{p}d_{p} \leq 5$   (select three to five defenders)

$\sum\limits_{p=0}^{P}x_{p}m_{p} \leq 5$  (select no more than five midfielders)

$\sum\limits_{p=0}^{P}x_{p}f_{p} \geq 1$  (select at least one forward)


$\sum\limits_{p=0}^{P}x_{p}g_{p} + B^{g} = 2$  (capture amount of bench goalkeepers required)

$\sum\limits_{p=0}^{P}x_{p}d_{p} + B^{d} = 5$ (capture amount of bench defenders required)

$\sum\limits_{p=0}^{P}x_{p}m_{p} + B^{m} = 5$ (capture amount of bench midfielders required)

$\sum\limits_{p=0}^{P}x_{p}f_{p} + B^{f} = 3$ (capture amount of bench forwards required)

$\sum\limits_{p=0}^{P}x_{p}c_{p} + \sum\limits_{q=0}^{Q} B^q C^q \leq 100$ (total cost of the team including bench must be less than 100)

$\sum\limits_{p=0}^{P}x_{p}t_{p}^{t*} \leq 3 \quad \forall t* \in EPL$ (select no more than three players from each club)


```python
df = optimise.fetch_data(Path("data/player_points.csv"))  # Output from notebooks/metric_research.ipynb
decision_vars, mdl = optimise.generate_model(df, optimisation_metric="points_bias_recent_avg")
optimise.lpsolve(model=mdl, logs=True)

mdl.writeLP("FantasyFootball.lp")

# Get solution vector
SV = [bool(int(x.value())) for x in decision_vars]
```

    Welcome to the CBC MILP Solver 
    Version: 2.10.3 
    Build Date: Dec 15 2019 
    
    command line - /home/ehutchinson/projects/fantasy-football-epl/.venv/lib/python3.11/site-packages/pulp/solverdir/cbc/linux/64/cbc /tmp/3aa322f737be4316ac764ac5bcdbb982-pulp.mps max timeMode elapsed branch printingOptions all solution /tmp/3aa322f737be4316ac764ac5bcdbb982-pulp.sol (default strategy 1)
    At line 2 NAME          MODEL
    At line 3 ROWS
    At line 35 COLUMNS
    At line 2933 RHS
    At line 2964 BOUNDS
    At line 3316 ENDATA
    Problem MODEL has 30 rows, 351 columns and 1866 elements
    Coin0008I MODEL read with 0 errors
    Option for timeMode changed from cpu to elapsed
    Continuous objective value is 1799.8 - 0.00 seconds
    Cgl0004I processed model has 23 rows, 335 columns (335 integer (335 of which binary)) and 1268 elements
    Cbc0038I Initial state - 2 integers unsatisfied sum - 0.666667
    Cbc0038I Solution found of -1773.57
    Cbc0038I Before mini branch and bound, 333 integers at bound fixed and 0 continuous
    Cbc0038I Full problem 23 rows 335 columns, reduced to 0 rows 0 columns
    Cbc0038I Mini branch and bound did not improve solution (0.00 seconds)
    Cbc0038I Round again with cutoff of -1776.19
    Cbc0038I Reduced cost fixing fixed 279 variables on major pass 2
    Cbc0038I Pass   1: suminf.    0.06667 (2) obj. -1776.19 iterations 4
    Cbc0038I Pass   2: suminf.    0.66667 (2) obj. -1787.21 iterations 3
    Cbc0038I Pass   3: suminf.    0.44092 (2) obj. -1776.19 iterations 3
    Cbc0038I Pass   4: suminf.    0.71356 (3) obj. -1776.19 iterations 3
    Cbc0038I Pass   5: suminf.    0.44092 (2) obj. -1776.19 iterations 4
    Cbc0038I Pass   6: suminf.    0.82547 (4) obj. -1776.19 iterations 4
    Cbc0038I Pass   7: suminf.    0.82547 (4) obj. -1776.19 iterations 0
    Cbc0038I Pass   8: suminf.    1.16515 (4) obj. -1776.19 iterations 3
    Cbc0038I Pass   9: suminf.    0.64908 (4) obj. -1776.19 iterations 3
    Cbc0038I Pass  10: suminf.    0.06667 (2) obj. -1776.19 iterations 4
    Cbc0038I Pass  11: suminf.    0.66667 (2) obj. -1787.21 iterations 4
    Cbc0038I Pass  12: suminf.    0.44092 (2) obj. -1776.19 iterations 4
    Cbc0038I Pass  13: suminf.    0.88148 (3) obj. -1776.19 iterations 3
    Cbc0038I Pass  14: suminf.    0.88148 (3) obj. -1776.19 iterations 1
    Cbc0038I Pass  15: suminf.    0.75000 (2) obj. -1779.9 iterations 7
    Cbc0038I Pass  16: suminf.    0.60403 (3) obj. -1776.19 iterations 4
    Cbc0038I Pass  17: suminf.    0.06667 (2) obj. -1776.19 iterations 5
    Cbc0038I Pass  18: suminf.    0.06667 (2) obj. -1776.19 iterations 0
    Cbc0038I Pass  19: suminf.    0.66667 (2) obj. -1787.21 iterations 5
    Cbc0038I Pass  20: suminf.    0.44092 (2) obj. -1776.19 iterations 4
    Cbc0038I Pass  21: suminf.    0.73090 (4) obj. -1776.19 iterations 9
    Cbc0038I Pass  22: suminf.    0.43820 (3) obj. -1776.19 iterations 3
    Cbc0038I Pass  23: suminf.    0.75000 (2) obj. -1781.41 iterations 9
    Cbc0038I Pass  24: suminf.    0.04126 (2) obj. -1776.19 iterations 5
    Cbc0038I Pass  25: suminf.    0.54415 (3) obj. -1776.19 iterations 6
    Cbc0038I Pass  26: suminf.    0.50554 (3) obj. -1776.19 iterations 4
    Cbc0038I Pass  27: suminf.    0.56807 (4) obj. -1776.19 iterations 8
    Cbc0038I Pass  28: suminf.    0.44162 (3) obj. -1776.19 iterations 4
    Cbc0038I Pass  29: suminf.    0.06658 (2) obj. -1776.19 iterations 10
    Cbc0038I Pass  30: suminf.    0.04126 (2) obj. -1776.19 iterations 3
    Cbc0038I Rounding solution of -1785.23 is better than previous of -1773.57
    
    Cbc0038I Before mini branch and bound, 316 integers at bound fixed and 0 continuous
    Cbc0038I Full problem 23 rows 335 columns, reduced to 5 rows 12 columns
    Cbc0038I Mini branch and bound improved solution from -1785.23 to -1790.23 (0.01 seconds)
    Cbc0038I Round again with cutoff of -1792.15
    Cbc0038I Reduced cost fixing fixed 322 variables on major pass 3
    Cbc0038I Pass  30: suminf.    0.47214 (2) obj. -1792.15 iterations 0
    Cbc0038I Pass  31: suminf.    0.66667 (2) obj. -1796.43 iterations 2
    Cbc0038I Pass  32: suminf.    0.56444 (2) obj. -1792.15 iterations 1
    Cbc0038I Pass  33: suminf.    0.68264 (3) obj. -1792.15 iterations 3
    Cbc0038I Pass  34: suminf.    0.25000 (2) obj. -1795 iterations 4
    Cbc0038I Pass  35: suminf.    0.04863 (2) obj. -1792.15 iterations 2
    Cbc0038I Pass  36: suminf.    0.68264 (3) obj. -1792.15 iterations 2
    Cbc0038I Pass  37: suminf.    0.68264 (3) obj. -1792.15 iterations 0
    Cbc0038I Pass  38: suminf.    0.80653 (3) obj. -1792.15 iterations 3
    Cbc0038I Pass  39: suminf.    0.56444 (2) obj. -1792.15 iterations 2
    Cbc0038I Pass  40: suminf.    0.66667 (2) obj. -1796.43 iterations 1
    Cbc0038I Pass  41: suminf.    1.42968 (4) obj. -1792.15 iterations 1
    Cbc0038I Pass  42: suminf.    1.42968 (4) obj. -1792.15 iterations 0
    Cbc0038I Pass  43: suminf.    0.44588 (2) obj. -1792.15 iterations 4
    Cbc0038I Pass  44: suminf.    0.44588 (2) obj. -1792.15 iterations 0
    Cbc0038I Pass  45: suminf.    0.63980 (3) obj. -1792.15 iterations 2
    Cbc0038I Pass  46: suminf.    0.63980 (3) obj. -1792.15 iterations 0
    Cbc0038I Pass  47: suminf.    0.72727 (2) obj. -1794.14 iterations 3
    Cbc0038I Pass  48: suminf.    1.00000 (3) obj. -1792.15 iterations 2
    Cbc0038I Pass  49: suminf.    0.51592 (2) obj. -1792.15 iterations 2
    Cbc0038I Pass  50: suminf.    0.31967 (2) obj. -1792.15 iterations 1
    Cbc0038I Pass  51: suminf.    0.75069 (3) obj. -1792.15 iterations 2
    Cbc0038I Pass  52: suminf.    0.75069 (3) obj. -1792.15 iterations 0
    Cbc0038I Pass  53: suminf.    0.60000 (2) obj. -1794.2 iterations 3
    Cbc0038I Pass  54: suminf.    0.51787 (2) obj. -1792.15 iterations 3
    Cbc0038I Pass  55: suminf.    0.51787 (2) obj. -1792.15 iterations 0
    Cbc0038I Pass  56: suminf.    0.77377 (3) obj. -1792.15 iterations 2
    Cbc0038I Pass  57: suminf.    0.51787 (2) obj. -1792.15 iterations 1
    Cbc0038I Pass  58: suminf.    0.31967 (2) obj. -1792.15 iterations 4
    Cbc0038I Pass  59: suminf.    0.31967 (2) obj. -1792.15 iterations 2
    Cbc0038I No solution found this major pass
    Cbc0038I Before mini branch and bound, 327 integers at bound fixed and 0 continuous
    Cbc0038I Full problem 23 rows 335 columns, reduced to 3 rows 6 columns
    Cbc0038I Mini branch and bound did not improve solution (0.01 seconds)
    Cbc0038I After 0.01 seconds - Feasibility pump exiting with objective of -1790.23 - took 0.01 seconds
    Cbc0012I Integer solution of -1790.234 found by feasibility pump after 0 iterations and 0 nodes (0.01 seconds)
    Cbc0038I Full problem 23 rows 335 columns, reduced to 0 rows 0 columns
    Cbc0006I The LP relaxation is infeasible or too expensive
    Cbc0013I At root node, 0 cuts changed objective from -1793.8906 to -1793.8906 in 1 passes
    Cbc0014I Cut generator 0 (Probing) - 1 row cuts average 0.0 elements, 4 column cuts (4 active)  in 0.000 seconds - new frequency is 1
    Cbc0014I Cut generator 1 (Gomory) - 0 row cuts average 0.0 elements, 0 column cuts (0 active)  in 0.000 seconds - new frequency is -100
    Cbc0014I Cut generator 2 (Knapsack) - 0 row cuts average 0.0 elements, 0 column cuts (0 active)  in 0.000 seconds - new frequency is -100
    Cbc0014I Cut generator 3 (Clique) - 0 row cuts average 0.0 elements, 0 column cuts (0 active)  in 0.000 seconds - new frequency is -100
    Cbc0014I Cut generator 4 (MixedIntegerRounding2) - 0 row cuts average 0.0 elements, 0 column cuts (0 active)  in 0.000 seconds - new frequency is -100
    Cbc0014I Cut generator 5 (FlowCover) - 0 row cuts average 0.0 elements, 0 column cuts (0 active)  in 0.000 seconds - new frequency is -100
    Cbc0014I Cut generator 6 (TwoMirCuts) - 0 row cuts average 0.0 elements, 0 column cuts (0 active)  in 0.000 seconds - new frequency is -100
    Cbc0014I Cut generator 7 (ZeroHalf) - 0 row cuts average 0.0 elements, 0 column cuts (0 active)  in 0.000 seconds - new frequency is -100
    Cbc0001I Search completed - best objective -1790.2340492842, took 3 iterations and 0 nodes (0.01 seconds)
    Cbc0035I Maximum depth 0, 324 variables fixed on reduced cost
    Cuts at root node changed objective from -1799.8 to -1793.89
    Probing was tried 1 times and created 5 cuts of which 0 were active after adding rounds of cuts (0.000 seconds)
    Gomory was tried 0 times and created 0 cuts of which 0 were active after adding rounds of cuts (0.000 seconds)
    Knapsack was tried 0 times and created 0 cuts of which 0 were active after adding rounds of cuts (0.000 seconds)
    Clique was tried 0 times and created 0 cuts of which 0 were active after adding rounds of cuts (0.000 seconds)
    MixedIntegerRounding2 was tried 0 times and created 0 cuts of which 0 were active after adding rounds of cuts (0.000 seconds)
    FlowCover was tried 0 times and created 0 cuts of which 0 were active after adding rounds of cuts (0.000 seconds)
    TwoMirCuts was tried 0 times and created 0 cuts of which 0 were active after adding rounds of cuts (0.000 seconds)
    ZeroHalf was tried 0 times and created 0 cuts of which 0 were active after adding rounds of cuts (0.000 seconds)
    
    Result - Optimal solution found
    
    Objective value:                1790.23404928
    Enumerated nodes:               0
    Total iterations:               3
    Time (CPU seconds):             0.02
    Time (Wallclock seconds):       0.02
    
    Option for printingOptions changed from normal to all
    Total time (CPU seconds):       0.02   (Wallclock seconds):       0.02
    



```python
print(f'Team cost: ${df[SV]["now_cost"].sum(): .2f}')
display(df.loc[SV, ["id", "position", "name", "first_name", "second_name", "now_cost"]])
```

    Team cost: $ 82.50



<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>position</th>
      <th>name</th>
      <th>first_name</th>
      <th>second_name</th>
      <th>now_cost</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>31</th>
      <td>569</td>
      <td>GKP</td>
      <td>Wolves</td>
      <td>José</td>
      <td>Malheiro de Sá</td>
      <td>5.0</td>
    </tr>
    <tr>
      <th>53</th>
      <td>5</td>
      <td>DEF</td>
      <td>Arsenal</td>
      <td>Gabriel</td>
      <td>dos Santos Magalhães</td>
      <td>5.0</td>
    </tr>
    <tr>
      <th>87</th>
      <td>189</td>
      <td>DEF</td>
      <td>Chelsea</td>
      <td>César</td>
      <td>Azpilicueta</td>
      <td>4.5</td>
    </tr>
    <tr>
      <th>105</th>
      <td>290</td>
      <td>DEF</td>
      <td>Liverpool</td>
      <td>Trent</td>
      <td>Alexander-Arnold</td>
      <td>8.0</td>
    </tr>
    <tr>
      <th>110</th>
      <td>307</td>
      <td>DEF</td>
      <td>Liverpool</td>
      <td>Andrew</td>
      <td>Robertson</td>
      <td>6.5</td>
    </tr>
    <tr>
      <th>168</th>
      <td>373</td>
      <td>MID</td>
      <td>Man Utd</td>
      <td>Bruno</td>
      <td>Borges Fernandes</td>
      <td>8.5</td>
    </tr>
    <tr>
      <th>182</th>
      <td>14</td>
      <td>MID</td>
      <td>Arsenal</td>
      <td>Martin</td>
      <td>Ødegaard</td>
      <td>8.5</td>
    </tr>
    <tr>
      <th>211</th>
      <td>516</td>
      <td>MID</td>
      <td>Spurs</td>
      <td>Son</td>
      <td>Heung-min</td>
      <td>9.0</td>
    </tr>
    <tr>
      <th>229</th>
      <td>216</td>
      <td>MID</td>
      <td>Chelsea</td>
      <td>Raheem</td>
      <td>Sterling</td>
      <td>7.0</td>
    </tr>
    <tr>
      <th>247</th>
      <td>308</td>
      <td>MID</td>
      <td>Liverpool</td>
      <td>Mohamed</td>
      <td>Salah</td>
      <td>12.5</td>
    </tr>
    <tr>
      <th>323</th>
      <td>60</td>
      <td>FWD</td>
      <td>Aston Villa</td>
      <td>Ollie</td>
      <td>Watkins</td>
      <td>8.0</td>
    </tr>
  </tbody>
</table>
</div>


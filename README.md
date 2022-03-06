<div class="cell code" data-execution_count="1">

``` python
import numpy as np
import pandas as pd
import pulp as p
import optimise
```

</div>

<div class="cell markdown">

# The problem: select a set of players for a fantasy football team such that we maximise the number of points based on an adjusted historical average.

Let \(x\) be a vector of players to be selected - our decision variables
- with each player indexed by an identification number within set \(P\).
Let four boolean vectors \(g\), \(d\), \(m\) and \(f\) define whether
each players is a goalkeeper, defender, midfielder and forward,
respectively. Let \(c\) and \(w\) be the cost and optimisation weight of
each player.

Although we're selecting the 11 outfield players we still need to adjust
the our budget to ensure we can select bench players; for now, let's
assume we can take the cheapest players for each position to sit on the
bench. As such, introduce four slack variables to capture the amount of
bench players we need for each position; \(B^{g}\), \(B^{d}\),
\(B^{m}\), and \(B^{f}\). We also need the minimum cost of players for
each of these positions, \(C^{g}\), \(C^{d}\), \(C^{m}\), and \(C^{f}\).
Let \(q\) contain the set of position indices, \(Q=\{g,d,m,f\}\).

We cannot select more than three players from each team; we will use a
boolean vector, \(t\), for each team, \(t*\), in the EPL where
\(t \in EPL\) (e.g. \(T^{ARS}\) ).

We also don't want to select any players that are injured at the start
of the season.

All contraints noted above are outlined inline below.

# Model

\(maximise\)

\(w^{T} x\)

\(subject \ to\)

\(\sum\limits_{p=0}^{P}x_{p} = 11\) (select 11 outfield players)

\(\sum\limits_{p=0}^{P}x_{p}g_{p} = 1\) (select 1 goalkeeper)

\(\sum\limits_{p=0}^{P}x_{p}d_{p} \geq 3\),
\(\sum\limits_{p=0}^{P}x_{p}d_{p} \leq 5\) (select three to five
defenders)

\(\sum\limits_{p=0}^{P}x_{p}m_{p} \leq 5\) (select no more than five
midfielders)

\(\sum\limits_{p=0}^{P}x_{p}f_{p} \geq 1\) (select at least one forward)

\(\sum\limits_{p=0}^{P}x_{p}g_{p} + B^{g} = 2\) (capture amount of bench
goalkeepers required)

\(\sum\limits_{p=0}^{P}x_{p}d_{p} + B^{d} = 5\) (capture amount of bench
defenders required)

\(\sum\limits_{p=0}^{P}x_{p}m_{p} + B^{m} = 5\) (capture amount of bench
midfielders required)

\(\sum\limits_{p=0}^{P}x_{p}f_{p} + B^{f} = 3\) (capture amount of bench
forwards required)

\(\sum\limits_{p=0}^{P}x_{p}c_{p} + \sum\limits_{q=0}^{Q} B^q C^q \leq 100\)
(total cost of the team including bench must be less than 100)

\(\sum\limits_{p=0}^{P}x_{p}t_{p}^{t*} \leq 3 \quad \forall t* \in EPL\)
(select no more than three players from each club)

</div>

<div class="cell code" data-execution_count="2">

``` python
df = optimise.fetch_data(r'data/player_points.csv')
decision_vars, mdl = optimise.generate_model(df)
mdl.writeLP('FantasyFootball.lp')  # Output human readable LP file
mdl.solve()
# Get solution vector
SV = [bool(int(x.value())) for x in decision_vars]
```

</div>

<div class="cell code" data-execution_count="3">

``` python
print(f'Team cost: ${df[SV]["now_cost"].sum(): .2f}')
df[SV]
```

<div class="output stream stdout">

    Team cost: $ 84.10

</div>

<div class="output execute_result" data-execution_count="3">

``` 
      id         first_name        second_name  now_cost         name club  \
4    199              Illan            Meslier       4.8        Leeds  LEE   
105  168              Lucas              Digne       5.1  Aston Villa  AVL   
155  418           Vladimir             Coufal       4.7     West Ham  WHU   
186  262       Rúben Santos    Gato Alves Dias       6.2     Man City  MCI   
216  277       Bruno Miguel   Borges Fernandes      11.6      Man Utd  MUN   
227  188             Stuart             Dallas       4.9        Leeds  LEE   
234  267               Jack           Harrison       5.5        Leeds  LEE   
324  233            Mohamed              Salah      13.2    Liverpool  LIV   
412  699          Christian            Eriksen       5.5    Brentford  BRE   
415  579  Cristiano Ronaldo  dos Santos Aveiro      12.3      Man Utd  MUN   
444  205              Jamie              Vardy      10.3    Leicester  LEI   

    position  total_points  weighted_points  injured  
4        GKP    154.000000       308.000000        0  
105      DEF    132.666667       174.777778        0  
155      DEF    128.000000       256.000000        0  
186      DEF    142.000000       284.000000        0  
216      MID    180.500000       281.333333        0  
227      MID    171.000000       342.000000        0  
234      MID    160.000000       320.000000        0  
324      MID    205.800000       252.106667        0  
412      MID    156.857143       178.076531        0  
415      FWD    244.333333       323.666667        0  
444      FWD    178.000000       204.510204        0  
```

</div>

</div>

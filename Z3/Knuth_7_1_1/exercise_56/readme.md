# Exercise 56 from TAOCP "7.1.1 Boolean Basics", solving it using Z3.

Page41 from fasc0b.ps or http://www.cs.utsa.edu/~wagner/knuth/fasc0b.pdf

![screenshot](https://raw.githubusercontent.com/DennisYurichev/random_notes/master/Z3/Knuth_7_1_1/exercise_56/fasc0b_page41.png)

For exists/forall/forall:

```python
(assert
        (exists ((x Bool)) (forall ((y Bool)) (forall ((z Bool))
                (and
                        (or x y)
                        (or (not x) z)
                        (or y (not z))
                )))
        )
)
(check-sat)
```

All the rest: https://github.com/DennisYurichev/random_notes/tree/master/Z3/Knuth_7_1_1/exercise_56

Results:

```
z3 -smt2 KnuthAAA.smt
z3 -smt2 KnuthAAE.smt
z3 -smt2 KnuthAEA.smt
z3 -smt2 KnuthAEE.smt
z3 -smt2 KnuthEAA.smt
z3 -smt2 KnuthEAE.smt
z3 -smt2 KnuthEEA.smt
z3 -smt2 KnuthEEE.smt

...

unsat
unsat
unsat
sat
unsat
unsat
sat
sat
```


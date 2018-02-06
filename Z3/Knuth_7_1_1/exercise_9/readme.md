# Exercise 9 from TAOCP "7.1.1 Boolean Basics", solving it using Z3.

Page 34 from fasc0b.ps or http://www.cs.utsa.edu/~wagner/knuth/fasc0b.pdf

![screenshot](https://raw.githubusercontent.com/DennisYurichev/random_notes/master/Z3/Knuth_7_1_1/exercise_9/fasc0b_page34.png)

For (a):

```
(assert
        (forall ((x Bool) (y Bool) (z Bool))
                (=
                        (or (xor x y) z)
                        (xor (or x z) (or y z))
                )
        )
)
(check-sat)
```

For (b):

```
(assert
        (forall ((x Bool) (y Bool) (z Bool) (w Bool))
                (=
                        (or (xor w x y) z)
                        (xor (or w z) (or x z) (or y z))
                )
        )
)
(check-sat)
```

For (c):

```
(assert
        (forall ((x Bool) (y Bool) (z Bool))
                (=
                        (or (xor x y) (xor y z))
                        (or (xor x z) (xor y z))
                )
        )
)
(check-sat)
```

Results:

```
% z3 -smt2 Knuth_a.smt
unsat
% z3 -smt2 Knuth_b.smt
sat
% z3 -smt2 Knuth_c.smt
sat
```


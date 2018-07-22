# Vietnamese puzzle

Can you fill 1..9 numbers in squares?

![puzzle](puzzle.png)

See also:
http://abc7.com/education/can-you-solve-this-third-grade-math-problem/732268/
https://gizmodo.com/there-are-other-possible-solutions-but-the-first-one-i-1705742922

This is a simple equation. It's not specified if the numbers must be distinct, however, I tried distinct ones, and there are 2672 unique solutions.

Some of:

```
3 4 8 7 6 2 1 9 5
9 8 3 2 4 7 6 1 5
3 1 9 8 6 7 5 4 2
3 4 8 2 7 9 1 6 5
2 4 8 3 7 9 1 6 5
7 6 2 8 3 4 9 1 5
7 6 2 8 3 4 1 9 5
6 8 4 2 5 9 1 7 3
6 8 4 2 5 9 7 1 3
5 1 4 2 7 9 3 6 8
5 1 8 2 7 9 3 6 4
4 1 8 2 6 7 5 9 3
9 3 6 8 4 1 7 5 2

...

```

The problem is easy enough to be solved my [toy-level MK85 SMT solver](https://github.com/DennisYurichev/MK85).


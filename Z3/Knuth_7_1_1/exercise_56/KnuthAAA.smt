(assert
	(forall ((x Bool)) (forall ((y Bool)) (forall ((z Bool))
		(and
			(or x y)
			(or (not x) z)
			(or y (not z))
		)))
	)
)
(check-sat)


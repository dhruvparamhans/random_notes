(set-logic QF_BV)
(set-info :smt-lib-version 2.0)

(declare-fun E () (_ BitVec 2))
(declare-fun F () (_ BitVec 2))
(declare-fun G () (_ BitVec 2))
(declare-fun H () (_ BitVec 2))

; apples = 0
; bananas = 1
; cherries = 2
; dates = 3

; children's preferences:

(assert
	(or
		(= E (_ bv2 2))
		(= E (_ bv3 2))
	)
)

(assert
	(or
		(= F (_ bv0 2))
		(= F (_ bv2 2))
	)
)

(assert
	(or
		(= G (_ bv1 2))
		(= G (_ bv2 2))
	)
)

(assert
	(or
		(= H (_ bv0 2))
		(= H (_ bv2 2))
		(= H (_ bv3 2))
	)
)

; each child must get a food of one type:

(assert (distinct E F G H))

; enumerate all possible solutions:

(get-all-models)

;(model
;        (define-fun E () (_ BitVec 2) (_ bv2 2)) ; 0x2
;        (define-fun F () (_ BitVec 2) (_ bv0 2)) ; 0x0
;        (define-fun G () (_ BitVec 2) (_ bv1 2)) ; 0x1
;        (define-fun H () (_ BitVec 2) (_ bv3 2)) ; 0x3
;)
;(model
;        (define-fun E () (_ BitVec 2) (_ bv3 2)) ; 0x3
;        (define-fun F () (_ BitVec 2) (_ bv2 2)) ; 0x2
;        (define-fun G () (_ BitVec 2) (_ bv1 2)) ; 0x1
;        (define-fun H () (_ BitVec 2) (_ bv0 2)) ; 0x0
;)
;(model
;        (define-fun E () (_ BitVec 2) (_ bv3 2)) ; 0x3
;        (define-fun F () (_ BitVec 2) (_ bv0 2)) ; 0x0
;        (define-fun G () (_ BitVec 2) (_ bv1 2)) ; 0x1
;        (define-fun H () (_ BitVec 2) (_ bv2 2)) ; 0x2
;)
;Model count: 3


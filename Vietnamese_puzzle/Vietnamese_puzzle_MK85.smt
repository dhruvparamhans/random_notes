(set-logic QF_BV)
(set-info :smt-lib-version 2.0)

(declare-fun a () (_ BitVec 16))
(declare-fun b () (_ BitVec 16))
(declare-fun c () (_ BitVec 16))
(declare-fun d () (_ BitVec 16))
(declare-fun e () (_ BitVec 16))
(declare-fun f () (_ BitVec 16))
(declare-fun g () (_ BitVec 16))
(declare-fun h () (_ BitVec 16))
(declare-fun i () (_ BitVec 16))

(assert (and (bvuge a #x0001) (bvule a #x0009)))
(assert (and (bvuge b #x0001) (bvule b #x0009)))
(assert (and (bvuge c #x0001) (bvule c #x0009)))
(assert (and (bvuge d #x0001) (bvule d #x0009)))
(assert (and (bvuge e #x0001) (bvule e #x0009)))
(assert (and (bvuge f #x0001) (bvule f #x0009)))
(assert (and (bvuge g #x0001) (bvule g #x0009)))
(assert (and (bvuge h #x0001) (bvule h #x0009)))
(assert (and (bvuge i #x0001) (bvule i #x0009)))

(assert (distinct a b c d e f g h i))

; a + 13*b/c + d + 12*e - f - 11 + g*h/i - 10 == 66

(assert (=
	(bvsub
		(bvadd
			(bvsub
				(bvsub 
					(bvadd
						a
						(bvudiv	(bvmul (_ bv13 16) b) c)
						d
						(bvmul (_ bv12 16) e))
					f)
				(_ bv11 16))
			(bvudiv (bvmul g h) i))
		(_ bv10 16))
	(_ bv66 16)))

;(check-sat)
;(get-model)
(count-models)
;(get-all-models)


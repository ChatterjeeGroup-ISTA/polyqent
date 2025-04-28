(declare-const x Real)

(assert (forall ((y Real)) (=> (> x 0) (>= (+ x y) y) ) ))
(check-sat)
(get-model)
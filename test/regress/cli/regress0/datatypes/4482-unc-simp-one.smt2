(set-logic ALL)
(set-info :status unsat)
(declare-fun a () Tuple)
(assert (distinct a tuple))
(check-sat)
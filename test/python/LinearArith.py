#!/usr/bin/env python

###
# \file LinearArith.py
# \verbatim
# Top contributors (to current version):
# Andrew V. Jones
# This file is part of the CVC4 project.
# Copyright (c) 2009-2019 by the authors listed in the file AUTHORS
# in the top-level source directory) and their institutional affiliations.
# All rights reserved.  See the file COPYING in the top-level source
# directory for licensing information.\endverbatim
###
# \brief Linear arithmetic example
###
# Linear arithmetic example
###

import CVC4


class LinearArith(object):
    def __init__(self):
        self.em = CVC4.ExprManager()
        self.smt = CVC4.SmtEngine(self.em)

    def main(self):
        self.smt.setLogic("QF_LIRA")

        real = self.em.realType()
        integer = self.em.integerType()

        # Variables
        x = self.em.mkVar("x", integer)
        y = self.em.mkVar("y", real)

        # Constants
        three = self.em.mkConst(CVC4.Rational(3))
        neg2 = self.em.mkConst(CVC4.Rational(-2))
        two_thirds = self.em.mkConst(CVC4.Rational(2, 3))

        # Terms
        three_y = self.em.mkExpr(CVC4.MULT, three, y)
        diff = self.em.mkExpr(CVC4.MINUS, y, x)

        # Formulas
        x_geq_3y = self.em.mkExpr(CVC4.GEQ, x, three_y)
        x_leq_y = self.em.mkExpr(CVC4.LEQ, x, y)
        neg2_lt_x = self.em.mkExpr(CVC4.LT, neg2, x)

        assumptions = self.em.mkExpr(CVC4.AND, x_geq_3y, x_leq_y, neg2_lt_x)
        self.smt.assertFormula(assumptions)
        self.smt.push()
        diff_leq_two_thirds = self.em.mkExpr(CVC4.LEQ, diff, two_thirds)

        assert CVC4.Result.VALID == \
            self.smt.query(diff_leq_two_thirds).isValid()

        self.smt.pop()

        self.smt.push()
        diff_is_two_thirds = self.em.mkExpr(CVC4.EQUAL, diff, two_thirds)
        self.smt.assertFormula(diff_is_two_thirds)

        true = self.em.mkBoolConst(True)
        assert CVC4.Result.SAT == self.smt.checkSat(true).isSat()

        self.smt.pop()


if __name__ == '__main__':
    LinearArith().main()

# EOF

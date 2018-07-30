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
# \brief A simple demonstration of the linear arithmetic capabilities of CVC4
#
# A simple demonstration of the linear arithmetic solving capabilities and
# the push pop of CVC4. This also gives an example option.
###
# LinearArith example
###

import CVC4


class LinearArith(object):
    def __init__(self):
        self.em = CVC4.ExprManager()
        self.smt = CVC4.SmtEngine(self.em)

    def main(self):
        self.smt.setLogic("QF_LIRA") # Set the logic

        # Prove that if given x (Integer) and y (Real) then
        # the maximum value of y - x is 2/3

        # Types
        real = self.em.realType()
        integer = self.em.integerType()

        # Variables
        x = self.em.mkVar("x", integer)
        y = self.em.mkVar("y", real)

        # Constants
        three = self.em.mkConst(CVC4.Rational(3))
        neg2 = self.em.mkConst(CVC4.Rational(-2))
        two_thirds = self.em.mkConst(CVC4.Rational(2,3))

        # Terms
        three_y = self.em.mkExpr(CVC4.MULT, three, y)
        diff = self.em.mkExpr(CVC4.MINUS, y, x)

        # Formulas
        x_geq_3y = self.em.mkExpr(CVC4.GEQ, x, three_y)
        x_leq_y = self.em.mkExpr(CVC4.LEQ, x, y)
        neg2_lt_x = self.em.mkExpr(CVC4.LT, neg2, x)

        assumptions = self.em.mkExpr(CVC4.AND, x_geq_3y, x_leq_y, neg2_lt_x)

        print("Given the assumptions " + assumptions.toString())
        self.smt.assertFormula(assumptions)


        self.smt.push()
        diff_leq_two_thirds = self.em.mkExpr(CVC4.LEQ, diff, two_thirds)
        print("Prove that " + diff_leq_two_thirds.toString() + " with CVC4.")
        print("CVC4 should report VALID.")
        print("Result from CVC4 is: " + self.smt.query(diff_leq_two_thirds).toString())
        self.smt.pop()

        print()

        self.smt.push()
        diff_is_two_thirds = self.em.mkExpr(CVC4.EQUAL, diff, two_thirds)
        self.smt.assertFormula(diff_is_two_thirds)
        print("Show that the asserts are consistent with ")
        print(diff_is_two_thirds.toString() + " with CVC4.")
        print("CVC4 should report SAT.")
        print("Result from CVC4 is: " + self.smt.checkSat(self.em.mkBoolConst(True)).toString())
        self.smt.pop()

        print("Thus the maximum value of (y - x) is 2/3.")


if __name__ == '__main__':
    LinearArith().main()


# EOF

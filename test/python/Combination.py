#!/usr/bin/env python

###
# \file Combination.py
# \verbatim
# Top contributors (to current version):
# Andrew V. Jones
# This file is part of the CVC4 project.
# Copyright (c) 2009-2019 by the authors listed in the file AUTHORS
# in the top-level source directory) and their institutional affiliations.
# All rights reserved.  See the file COPYING in the top-level source
# directory for licensing information.\endverbatim
###
# \brief Combination example
###
# Combination example
###

import CVC4


class Combination(object):
    def __init__(self):
        self.em = CVC4.ExprManager()
        self.smt = CVC4.SmtEngine(self.em)

    def main(self):
        self.smt.setOption("tlimit", CVC4.SExpr(100))
        # Produce Models
        self.smt.setOption("produce-models", CVC4.SExpr("true"))
        # output-language
        self.smt.setOption("output-language", CVC4.SExpr("cvc4"))
        # Disable dagifying the output
        self.smt.setOption("default-dag-thresh", CVC4.SExpr(0))
        self.smt.setLogic("QF_UFLIRA")

        # Sorts
        u = self.em.mkSort("u")
        integer = self.em.integerType()
        booleanType = self.em.booleanType()
        uToInt = self.em.mkFunctionType(u, integer)
        intPred = self.em.mkFunctionType(integer, booleanType)

        # Variables
        x = self.em.mkVar("x", u)
        y = self.em.mkVar("y", u)

        # Functions
        f = self.em.mkVar("f", uToInt)
        p = self.em.mkVar("p", intPred)

        # Constants
        zero = self.em.mkConst(CVC4.Rational(0))
        one = self.em.mkConst(CVC4.Rational(1))

        # Terms
        f_x = self.em.mkExpr(CVC4.APPLY_UF, f, x)
        f_y = self.em.mkExpr(CVC4.APPLY_UF, f, y)
        add = self.em.mkExpr(CVC4.PLUS, f_x, f_y)
        p_0 = self.em.mkExpr(CVC4.APPLY_UF, p, zero)
        p_f_y = self.em.mkExpr(CVC4.APPLY_UF, p, f_y)

        # Construct the assumptions
        assumptions = self.em.mkExpr(CVC4.AND,
                                     self.em.mkExpr(
                                         CVC4.LEQ, zero, f_x),  # 0 <= f(x)
                                     self.em.mkExpr(
                                         CVC4.LEQ, zero, f_y),  # 0 <= f(y)
                                     # f(x) + f(y) <= 1
                                     self.em.mkExpr(CVC4.LEQ, add, one),
                                     p_0.notExpr(),                  # not p(0)
                                     p_f_y)                         # p(f(y))

        self.smt.assertFormula(assumptions)

        assert CVC4.Result.VALID == self.smt.query(
            self.em.mkExpr(CVC4.DISTINCT, x, y)).isValid()

        true = self.em.mkBoolConst(True)
        assert CVC4.Result.SAT == self.smt.checkSat(true).isSat()


if __name__ == '__main__':
    Combination().main()


# EOF

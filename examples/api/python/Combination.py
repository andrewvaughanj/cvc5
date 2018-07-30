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
# \brief A simple demonstration of the capabilities of CVC4
#
# A simple demonstration of how to use uninterpreted functions, combining this
# with arithmetic, and extracting a model at the end of a satisfiable query.
# The model is displayed using getValue().
###
# Combination example
###

import CVC4


class Combination(object):
    def __init__(self):
        self.em = CVC4.ExprManager()
        self.smt = CVC4.SmtEngine(self.em)

    def _prefixPrintGetValue(self, e, level):
        for i in range(0, level):
            print("-", end="")

        print("smt.getValue({e:s}) -> {val:s}".format(e=e.toString(), val=self.smt.getValue(e).toString()))

        if e.hasOperator():
            self._prefixPrintGetValue(e.getOperator(), level + 1)

        for i in range(0, e.getNumChildren()):
            curr = e.getChild(i)
            self._prefixPrintGetValue(curr, level + 1)

    def main(self):
        self.smt.setOption("tlimit", CVC4.SExpr(100))
        self.smt.setOption("produce-models", CVC4.SExpr(True)) # Produce Models
        self.smt.setOption("output-language", CVC4.SExpr("cvc4")) # output-language
        self.smt.setOption("default-dag-thresh", CVC4.SExpr(0)) # Disable dagifying the output
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
        sum = self.em.mkExpr(CVC4.PLUS, f_x, f_y)
        p_0 = self.em.mkExpr(CVC4.APPLY_UF, p, zero)
        p_f_y = self.em.mkExpr(CVC4.APPLY_UF, p, f_y)

        # Construct the assumptions
        assumptions = self.em.mkExpr(CVC4.AND,
                    self.em.mkExpr(CVC4.LEQ, zero, f_x), # 0 <= f(x)
                    self.em.mkExpr(CVC4.LEQ, zero, f_y), # 0 <= f(y)
                    self.em.mkExpr(CVC4.LEQ, sum, one),  # f(x) + f(y) <= 1
                    p_0.notExpr(),                  # not p(0)
                    p_f_y)                          # p(f(y))
        self.smt.assertFormula(assumptions)

        print("Given the following assumptions:")
        print(assumptions.toString())
        print("Prove x /= y is valid. " +
                           "CVC4 says: " + self.smt.query(self.em.mkExpr(CVC4.DISTINCT, x, y)).toString() +
                           ".")


        print("Now we call checksat on a trivial query to show that")
        print("the assumptions are satisfiable: " +
                           self.smt.checkSat(self.em.mkBoolConst(True)).toString() + ".")

        print("Finally, after a SAT call, we recursively call self.smt.getValue(...) on " +
                           "all of the assumptions to see what the satisfying model looks like.")
        self._prefixPrintGetValue(assumptions, 0)


if __name__ == '__main__':
    Combination().main()


# EOF

#!/usr/bin/env python

###
# \file Strings.py
# \verbatim
# Top contributors (to current version):
# Andrew V. Jones
# This file is part of the CVC4 project.
# Copyright (c) 2009-2019 by the authors listed in the file AUTHORS
# in the top-level source directory) and their institutional affiliations.
# All rights reserved.  See the file COPYING in the top-level source
# directory for licensing information.\endverbatim
###
# \brief Reasoning about strings with CVC4 via Python API.
#
# A simple demonstration of reasoning about strings with CVC4 via Python API.
###
# Strings example
###

import CVC4


class Strings(object):
    def __init__(self):
        self.em = CVC4.ExprManager()
        self.smt = CVC4.SmtEngine(self.em)

    def main(self):
        # Set the logic
        self.smt.setLogic("S")

        # Produce models
        self.smt.setOption("produce-models", CVC4.SExpr(True))
        # The option strings-exp is needed
        self.smt.setOption("strings-exp", CVC4.SExpr(True))
            # output-language
        self.smt.setOption("output-language", CVC4.SExpr("smt2"))

        # String type
        string = self.em.stringType()

        # String constants
        ab  = self.em.mkConst(CVC4.CVC4String("ab"))
        abc = self.em.mkConst(CVC4.CVC4String("abc"))
        # Variables
        x = self.em.mkVar("x", string)
        y = self.em.mkVar("y", string)
        z = self.em.mkVar("z", string)

        # String concatenation: x.ab.y
        lhs = self.em.mkExpr(CVC4.STRING_CONCAT, x, ab, y)
        # String concatenation: abc.z
        rhs = self.em.mkExpr(CVC4.STRING_CONCAT, abc, z)
        # x.ab.y = abc.z
        formula1 = self.em.mkExpr(CVC4.EQUAL, lhs, rhs)

        # Length of y: |y|
        leny = self.em.mkExpr(CVC4.STRING_LENGTH, y)
        # |y| >= 0
        formula2 = self.em.mkExpr(CVC4.GEQ, leny, self.em.mkConst(CVC4.Rational(0)))

        # Regular expression: (ab[c-e]*f)|g|h
        r = self.em.mkExpr(CVC4.REGEXP_UNION,
          self.em.mkExpr(CVC4.REGEXP_CONCAT,
            self.em.mkExpr(CVC4.STRING_TO_REGEXP, self.em.mkConst(CVC4.CVC4String("ab"))),
            self.em.mkExpr(CVC4.REGEXP_STAR,
              self.em.mkExpr(CVC4.REGEXP_RANGE, self.em.mkConst(CVC4.CVC4String("c")), self.em.mkConst(CVC4.CVC4String("e")))),
            self.em.mkExpr(CVC4.STRING_TO_REGEXP, self.em.mkConst(CVC4.CVC4String("f")))),
          self.em.mkExpr(CVC4.STRING_TO_REGEXP, self.em.mkConst(CVC4.CVC4String("g"))),
          self.em.mkExpr(CVC4.STRING_TO_REGEXP, self.em.mkConst(CVC4.CVC4String("h"))))

        # String variables
        s1 = self.em.mkVar("s1", string)
        s2 = self.em.mkVar("s2", string)
        # String concatenation: s1.s2
        s = self.em.mkExpr(CVC4.STRING_CONCAT, s1, s2)

        # s1.s2 in (ab[c-e]*f)|g|h
        formula3 = self.em.mkExpr(CVC4.STRING_IN_REGEXP, s, r)

            # Make a query
        q = self.em.mkExpr(CVC4.AND,
          formula1,
          formula2,
          formula3)

        # check sat
        result = self.smt.checkSat(q)
        print("CVC4 reports: " + q.toString() + " is " + result.toString() + ".")

        print("  x  = " + self.smt.getValue(x).toString())
        print("  s1.s2 = " + self.smt.getValue(s).toString())


if __name__ == '__main__':
    Strings().main()


# EOF

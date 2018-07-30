#!/usr/bin/env python

###
# \file FloatingPointArith.py
# \verbatim
# Top contributors (to current version):
# Andrew V. Jones
# This file is part of the CVC4 project.
# Copyright (c) 2009-2019 by the authors listed in the file AUTHORS
# in the top-level source directory) and their institutional affiliations.
# All rights reserved.  See the file COPYING in the top-level source
# directory for licensing information.\endverbatim
###
# \brief An example of solving floating-point problems with CVC4's Java API
#
# This example shows how to check whether CVC4 was built with floating-point
# support, how to create floating-point types, variables and expressions, and
# how to create rounding mode constants by solving toy problems. The example
# also shows making special values (such as NaN and +oo) and converting an
# IEEE 754-2008 bit-vector to a floating-point number.
###
# FloatingPointArith example
###

import CVC4
import sys


class FloatingPointArith(object):
    def __init__(self):
        self.em = CVC4.ExprManager()
        self.smt = CVC4.SmtEngine(self.em)

    def main(self):
        # Test whether CVC4 was built with floating-point support
        if not CVC4.Configuration.isBuiltWithSymFPU():
          print("CVC4 was built without floating-point support.")
          print("Configure with --symfpu and rebuild CVC4 to run")
          print("this example.")
          sys.exit(77)

        # Enable the model production
        self.smt.setOption("produce-models", CVC4.SExpr(True))

        # Make single precision floating-point variables
        fpt32 = self.em.mkFloatingPointType(8, 24)
        a = self.em.mkVar("a", fpt32)
        b = self.em.mkVar("b", fpt32)
        c = self.em.mkVar("c", fpt32)
        d = self.em.mkVar("d", fpt32)
        e = self.em.mkVar("e", fpt32)

        # Assert that floating-point addition is not associative:
        # (a + (b + c)) != ((a + b) + c)
        rm = self.em.mkConst(CVC4.roundNearestTiesToEven)
        lhs = self.em.mkExpr(CVC4.FLOATINGPOINT_PLUS,
            rm,
            a,
            self.em.mkExpr(CVC4.FLOATINGPOINT_PLUS, rm, b, c))
        rhs = self.em.mkExpr(CVC4.FLOATINGPOINT_PLUS,
            rm,
            self.em.mkExpr(CVC4.FLOATINGPOINT_PLUS, rm, a, b),
            c)
        self.smt.assertFormula(self.em.mkExpr(CVC4.NOT, self.em.mkExpr(CVC4.EQUAL, a, b)))

        r = self.smt.checkSat() # result is sat
        assert r.isSat() == CVC4.Result.SAT

        print("a = " + self.smt.getValue(a).toString())
        print("b = " + self.smt.getValue(b).toString())
        print("c = " + self.smt.getValue(c).toString())

        # Now, let's restrict `a` to be either NaN or positive infinity
        fps32 = CVC4.FloatingPointSize(8, 24)
        nan = self.em.mkConst(CVC4.FloatingPoint.makeNaN(fps32))
        inf = self.em.mkConst(CVC4.FloatingPoint.makeInf(fps32, True))
        self.smt.assertFormula(self.em.mkExpr(
            CVC4.OR, self.em.mkExpr(CVC4.EQUAL, a, inf), self.em.mkExpr(CVC4.EQUAL, a, nan)))

        r = self.smt.checkSat() # result is sat
        assert r.isSat() == CVC4.Result.SAT

        print("a = " + self.smt.getValue(a).toString())
        print("b = " + self.smt.getValue(b).toString())
        print("c = " + self.smt.getValue(c).toString())

        # And now for something completely different. Let's try to find a (normal)
        # floating-point number that rounds to different integer values for
        # different rounding modes.
        rtp = self.em.mkConst(CVC4.roundTowardPositive)
        rtn = self.em.mkConst(CVC4.roundTowardNegative)
        op = self.em.mkConst(CVC4.FloatingPointToSBV(16)) # (_ fp.to_sbv 16)
        lhs = self.em.mkExpr(op, rtp, d)
        rhs = self.em.mkExpr(op, rtn, d)
        self.smt.assertFormula(self.em.mkExpr(CVC4.FLOATINGPOINT_ISN, d))
        self.smt.assertFormula(self.em.mkExpr(CVC4.NOT, self.em.mkExpr(CVC4.EQUAL, lhs, rhs)))

        r = self.smt.checkSat() # result is sat
        assert r.isSat() == Result.Sat.SAT

        # Convert the result to a rational and print it
        val = self.smt.getValue(d)
        realVal = val.getConstFloatingPoint().convertToRationalTotal(CVC4.Rational(0))
        print("d = " + val.toString() + " = " + realVal.toString())
        print("((_ fp.to_sbv 16) RTP d) = " + self.smt.getValue(lhs).toString())
        print("((_ fp.to_sbv 16) RTN d) = " + self.smt.getValue(rhs).toString())

        # For our final trick, let's try to find a floating-point number between
        # positive zero and the smallest positive floating-point number
        zero = self.em.mkConst(FloatingPoint.makeZero(fps32, True))
        smallest = self.em.mkConst(CVC4.FloatingPoint(8, 24, CVC4.BitVector(32, 0b001)))
        self.smt.assertFormula(self.em.mkExpr(CVC4.AND,
            self.em.mkExpr(CVC4.FLOATINGPOINT_LT, zero, e),
            self.em.mkExpr(CVC4.FLOATINGPOINT_LT, e, smallest)))

        r = self.smt.checkSat() # result is unsat
        assert r.isSat() == Result.Sat.UNSAT


if __name__ == '__main__':
    FloatingPointArith().main()


# EOF

#!/usr/bin/env python

###
# \file BitVectors.py
# \verbatim
# Top contributors (to current version):
# Andrew V. Jones
# This file is part of the CVC4 project.
# Copyright (c) 2009-2019 by the authors listed in the file AUTHORS
# in the top-level source directory) and their institutional affiliations.
# All rights reserved.  See the file COPYING in the top-level source
# directory for licensing information.\endverbatim
###
# \brief BitVectors example
###
# BitVectors example
###

import CVC4


class BitVectors(object):
    def __init__(self):
        self.em = CVC4.ExprManager()
        self.smt = CVC4.SmtEngine(self.em)

    def main(self):
        self.smt.setLogic("QF_BV")  # Set the logic

        # The following example has been adapted from the book A Hacker's Delight by
        # Henry S. Warren.
        #
        # Given a variable x that can only have two values, a or b. We want to
        # assign to x a value other than the current one. The straightforward code
        # to do that is:
        #
        # (0) if (x == a ) x = b
        #    else x = a
        #
        # Two more efficient yet equivalent methods are:
        #
        # (1) x = a (+) b (+) x
        #
        # (2) x = a + b - x
        #
        # We will use CVC4 to prove that the three pieces of code above are all
        # equivalent by encoding the problem in the bit-vector theory.

        # Creating a bit-vector type of width 32
        bitvector32 = self.em.mkBitVectorType(32)

        # Variables
        x = self.em.mkVar("x", bitvector32)
        a = self.em.mkVar("a", bitvector32)
        b = self.em.mkVar("b", bitvector32)

        # First encode the assumption that x must be equal to a or b
        x_eq_a = self.em.mkExpr(CVC4.EQUAL, x, a)
        x_eq_b = self.em.mkExpr(CVC4.EQUAL, x, b)
        assumption = self.em.mkExpr(CVC4.OR, x_eq_a, x_eq_b)

        # Assert the assumption
        self.smt.assertFormula(assumption)

        # Introduce a variable for the value of x after assignment.
        # x after executing code (0)
        new_x = self.em.mkVar("new_x", bitvector32)
        # x after executing code (1) or (2)
        new_x_ = self.em.mkVar("new_x_", bitvector32)

        # Encoding code (0)
        # new_x = x == a ? b : a
        ite = self.em.mkExpr(CVC4.ITE, x_eq_a, b, a)
        assignment0 = self.em.mkExpr(CVC4.EQUAL, new_x, ite)

        # Assert the encoding of code (0)
        self.smt.assertFormula(assignment0)
        self.smt.push()

        # Encoding code (1)
        # new_x_ = a xor b xor x
        a_xor_b_xor_x = self.em.mkExpr(CVC4.BITVECTOR_XOR, a, b, x)
        assignment1 = self.em.mkExpr(CVC4.EQUAL, new_x_, a_xor_b_xor_x)

        # Assert encoding to CVC4 in current context
        self.smt.assertFormula(assignment1)
        new_x_eq_new_x_ = self.em.mkExpr(CVC4.EQUAL, new_x, new_x_)

        expect = CVC4.Result.VALID
        actual = self.smt.query(new_x_eq_new_x_).isValid()
        assert expect == actual
        self.smt.pop()

        # Encoding code (2)
        # new_x_ = a + b - x
        a_plus_b = self.em.mkExpr(CVC4.BITVECTOR_PLUS, a, b)
        a_plus_b_minus_x = self.em.mkExpr(CVC4.BITVECTOR_SUB, a_plus_b, x)
        assignment2 = self.em.mkExpr(CVC4.EQUAL, new_x_, a_plus_b_minus_x)

        # Assert encoding to CVC4 in current context
        self.smt.assertFormula(assignment2)

        expect = CVC4.Result.VALID
        actual = self.smt.query(new_x_eq_new_x_).isValid()
        assert expect == actual


if __name__ == '__main__':
    BitVectors().main()


# EOF

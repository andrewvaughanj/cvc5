#!/usr/bin/env python

###
# \file BitVectorsAndArrays.py
# \verbatim
# Top contributors (to current version):
# Andrew V. Jones
# This file is part of the CVC4 project.
# Copyright (c) 2009-2019 by the authors listed in the file AUTHORS
# in the top-level source directory) and their institutional affiliations.
# All rights reserved.  See the file COPYING in the top-level source
# directory for licensing information.\endverbatim
###
# \brief BitVectorsAndArrays example
###
# BitVectorsAndArrays example
###

import CVC4
import math


class BitVectorsAndArrays(object):
    def __init__(self):
        self.em = CVC4.ExprManager()
        self.smt = CVC4.SmtEngine(self.em)

    def main(self):
        # Produce Models
        self.smt.setOption("produce-models", CVC4.SExpr("true"))
        # output-language
        self.smt.setOption("output-language", CVC4.SExpr("smtlib"))
        self.smt.setLogic("QF_AUFBV")                              # Set the logic

        # Consider the following code (where size is some previously defined constant):
        #
        #   Assert (current_array[0] > 0)
        #   for (unsigned i = 1 i < k ++i) {
        #     current_array[i] = 2 * current_array[i - 1]
        #     Assert (current_array[i-1] < current_array[i])
        #   }
        #
        # We want to check whether the assertion in the body of the for loop holds
        # throughout the loop.

        # Setting up the problem parameters
        k = 4                # number of unrollings (should be a power of 2)
        index_size = int(math.log(k, 2))  # size of the index

        # Types
        elementType = self.em.mkBitVectorType(32)
        indexType = self.em.mkBitVectorType(index_size)
        arrayType = self.em.mkArrayType(indexType, elementType)

        # Variables
        current_array = self.em.mkVar("current_array", arrayType)

        # Making a bit-vector constant
        zero = self.em.mkConst(CVC4.BitVector(index_size, 0))

        # Asserting that current_array[0] > 0
        current_array0 = self.em.mkExpr(CVC4.SELECT, current_array, zero)
        current_array0_gt_0 = self.em.mkExpr(
            CVC4.BITVECTOR_SGT, current_array0, self.em.mkConst(
                CVC4.BitVector(32, 0)))
        self.smt.assertFormula(current_array0_gt_0)

        # Building the assertions in the loop unrolling
        index = self.em.mkConst(CVC4.BitVector(index_size, 0))
        old_current = self.em.mkExpr(CVC4.SELECT, current_array, index)
        two = self.em.mkConst(CVC4.BitVector(32, 2))

        assertions = CVC4.vectorExpr()
        for i in range(1, k):
            index = self.em.mkConst(
                CVC4.BitVector(index_size, CVC4.Integer(i)))
            new_current = self.em.mkExpr(CVC4.BITVECTOR_MULT, two, old_current)
            # current[i] = 2 * current[i-1]
            current_array = self.em.mkExpr(
                CVC4.STORE, current_array, index, new_current)
            # current[i-1] < current [i]
            current_slt_new_current = self.em.mkExpr(
                CVC4.BITVECTOR_SLT, old_current, new_current)
            assertions.append(current_slt_new_current)

            old_current = self.em.mkExpr(CVC4.SELECT, current_array, index)

        query = self.em.mkExpr(CVC4.NOT, self.em.mkExpr(CVC4.AND, assertions))
        self.smt.assertFormula(query)

        expect = CVC4.Result.SAT
        actual = self.smt.checkSat(self.em.mkBoolConst(True)).isSat()
        assert expect == actual


if __name__ == '__main__':
    BitVectorsAndArrays().main()


# EOF

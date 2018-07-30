#!/usr/bin/env python

###
# \file Datatypes.py
# \verbatim
# Top contributors (to current version):
# Andrew V. Jones
# This file is part of the CVC4 project.
# Copyright (c) 2009-2019 by the authors listed in the file AUTHORS
# in the top-level source directory) and their institutional affiliations.
# All rights reserved.  See the file COPYING in the top-level source
# directory for licensing information.\endverbatim
###
# \brief An example of using inductive datatypes in CVC4 (Python version)
#
# An example of using inductive datatypes in CVC4 (Python version).
###
# Datatypes example
###

import CVC4


class Datatypes(object):
    def __init__(self):
        self.em = CVC4.ExprManager()
        self.smt = CVC4.SmtEngine(self.em)

    def main(self):
        # This example builds a simple "cons list" of integers, with
        # two constructors, "cons" and "nil."

        # Building a datatype consists of two steps.  First, the datatype
        # is specified.  Second, it is "resolved"---at which point function
        # symbols are assigned to its constructors, selectors, and testers.

        consListSpec = CVC4.Datatype("list") # give the datatype a name
        cons = CVC4.DatatypeConstructor("cons")
        cons.addArg("head", self.em.integerType())
        cons.addArg("tail", CVC4.DatatypeSelfType()) # a list
        consListSpec.addConstructor(cons)
        nil = CVC4.DatatypeConstructor("nil")
        consListSpec.addConstructor(nil)

        print("spec is:")
        print(str(consListSpec))

        # Keep in mind that "Datatype" is the specification class for
        # datatypes---"Datatype" is not itself a CVC4 Type.  Now that
        # our Datatype is fully specified, we can get a Type for it.
        # This step resolves the "SelfType" reference and creates
        # symbols for all the constructors, etc.

        consListType = self.em.mkDatatypeType(consListSpec)

        # Now our old "consListSpec" is useless--the relevant information
        # has been copied out, so we can throw that spec away.  We can get
        # the complete spec for the datatype from the DatatypeType, and
        # this Datatype object has constructor symbols (and others) filled in.

        consList = consListType.getDatatype()

        # e = cons 0 nil
        #
        # Here, consList.get("cons") gives you the DatatypeConstructor
        # (just as consList["cons"] does in C++).  To get the constructor
        # symbol for application, use .getConstructor("cons"), which is
        # equivalent to consList.get("cons").getConstructor().  Note that
        # "nil" is a constructor too, so it needs to be applied with
        # APPLY_CONSTRUCTOR, even though it has no arguments.
        e = self.em.mkExpr(CVC4.APPLY_CONSTRUCTOR,
                           consList.getConstructor("cons"),
                           self.em.mkConst(CVC4.Rational(0)),
                           self.em.mkExpr(CVC4.APPLY_CONSTRUCTOR,
                                     consList.getConstructor("nil")))

        print("e is " + e.toString())
        print("type of cons is " +
                           consList.getConstructor("cons").getType().toString())
        print("type of nil is " +
                           consList.getConstructor("nil").getType().toString())

        # e2 = head(cons 0 nil), and of course this can be evaluated
        #
        # Here we first get the DatatypeConstructor for cons (with
        # consList.get("cons") in order to get the "head" selector
        # symbol to apply.
        e2 = self.em.mkExpr(CVC4.APPLY_SELECTOR,
                            consList.get("cons").getSelector("head"),
                            e)

        print("e2 is " + e2.toString())
        print("simplify(e2) is " + self.smt.simplify(e2).toString())
        print()

        # You can also iterate over a Datatype to get all its constructors,
        # and over a DatatypeConstructor to get all its "args" (selectors)
        for i in range(0, consList.getNumConstructors()):
            ctor = consList.get(i)
            print("ctor:" + ctor.getName())
            for j in range(0, ctor.getNumArgs()):
                arg = ctor.get(j)
                print("   arg:" + arg.getName())

if __name__ == '__main__':
    Datatypes().main()


# EOF

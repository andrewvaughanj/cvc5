#!/usr/bin/env python

###
# \file HelloWorld.py
# \verbatim
# Top contributors (to current version):
# Andrew V. Jones
# This file is part of the CVC4 project.
# Copyright (c) 2009-2019 by the authors listed in the file AUTHORS
# in the top-level source directory) and their institutional affiliations.
# All rights reserved.  See the file COPYING in the top-level source
# directory for licensing information.\endverbatim
###
# \brief A very simple CVC4 example
###
# A very simple CVC4 tutorial example.
###

import CVC4


class HelloWorld(object):
    def __init__(self):
        self.em = CVC4.ExprManager()
        self.smt = CVC4.SmtEngine(self.em)

    def main(self):
        helloworld = self.em.mkVar("Hello World!", self.em.booleanType())
        expected = CVC4.Result.INVALID
        actual = self.smt.query(helloworld).isValid()
        assert expected == actual


if __name__ == '__main__':
    HelloWorld().main()

# EOF

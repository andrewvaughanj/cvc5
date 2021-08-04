/******************************************************************************
 * Top contributors (to current version):
 *   Mathias Preiner, Gereon Kremer, Haniel Barbosa
 *
 * This file is part of the cvc5 project.
 *
 * Copyright (c) 2009-2021 by the authors listed in the file AUTHORS
 * in the top-level source directory and their institutional affiliations.
 * All rights reserved.  See the file COPYING in the top-level source
 * directory for licensing information.
 * ****************************************************************************
 *
 * Bit-blast solver that sends bit-blast lemmas directly to the internal
 * MiniSat.
 */

#include "theory/bv/bv_solver_bitblast_internal.h"

#include "proof/conv_proof_generator.h"
#include "theory/bv/theory_bv.h"
#include "theory/bv/theory_bv_utils.h"
#include "theory/theory_model.h"

namespace cvc5 {
namespace theory {
namespace bv {

/* -------------------------------------------------------------------------- */

namespace {

bool isBVAtom(TNode n)
{
  return (n.getKind() == kind::EQUAL && n[0].getType().isBitVector())
         || n.getKind() == kind::BITVECTOR_ULT
         || n.getKind() == kind::BITVECTOR_ULE
         || n.getKind() == kind::BITVECTOR_SLT
         || n.getKind() == kind::BITVECTOR_SLE;
}

/* Traverse Boolean nodes and collect BV atoms. */
void collectBVAtoms(TNode n, std::unordered_set<Node>& atoms)
{
  std::vector<TNode> visit;
  std::unordered_set<TNode> visited;

  visit.push_back(n);

  do
  {
    TNode cur = visit.back();
    visit.pop_back();

    if (visited.find(cur) != visited.end() || !cur.getType().isBoolean())
      continue;

    visited.insert(cur);
    if (isBVAtom(cur))
    {
      atoms.insert(cur);
      continue;
    }

    visit.insert(visit.end(), cur.begin(), cur.end());
  } while (!visit.empty());
}

}  // namespace

BVSolverBitblastInternal::BVSolverBitblastInternal(
    TheoryState* s, TheoryInferenceManager& inferMgr, ProofNodeManager* pnm)
    : BVSolver(*s, inferMgr),
      d_pnm(pnm),
      d_bitblaster(new BBProof(s, pnm, false))
{
}

void BVSolverBitblastInternal::addBBLemma(TNode fact)
{
  if (!d_bitblaster->hasBBAtom(fact))
  {
    d_bitblaster->bbAtom(fact);
  }
  NodeManager* nm = NodeManager::currentNM();

  Node atom_bb = d_bitblaster->getStoredBBAtom(fact);
  Node lemma = nm->mkNode(kind::EQUAL, fact, atom_bb);

  if (d_pnm == nullptr)
  {
    d_im.lemma(lemma, InferenceId::BV_BITBLAST_INTERNAL_BITBLAST_LEMMA);
  }
  else
  {
    TrustNode tlem =
        TrustNode::mkTrustLemma(lemma, d_bitblaster->getProofGenerator());
    d_im.trustedLemma(tlem, InferenceId::BV_BITBLAST_INTERNAL_BITBLAST_LEMMA);
  }
}

bool BVSolverBitblastInternal::preNotifyFact(
    TNode atom, bool pol, TNode fact, bool isPrereg, bool isInternal)
{
  if (fact.getKind() == kind::NOT)
  {
    fact = fact[0];
  }

  if (isBVAtom(fact))
  {
    addBBLemma(fact);
  }
  else if (fact.getKind() == kind::BITVECTOR_EAGER_ATOM)
  {
    TNode n = fact[0];

    NodeManager* nm = NodeManager::currentNM();
    Node lemma = nm->mkNode(kind::EQUAL, fact, n);

    if (d_pnm == nullptr)
    {
      d_im.lemma(lemma, InferenceId::BV_BITBLAST_INTERNAL_EAGER_LEMMA);
    }
    else
    {
      d_bitblaster->getProofGenerator()->addRewriteStep(
          fact, n, PfRule::BV_EAGER_ATOM, {}, {fact});
      TrustNode tlem =
          TrustNode::mkTrustLemma(lemma, d_bitblaster->getProofGenerator());
      d_im.trustedLemma(tlem, InferenceId::BV_BITBLAST_INTERNAL_EAGER_LEMMA);
    }

    std::unordered_set<Node> bv_atoms;
    collectBVAtoms(n, bv_atoms);
    for (const Node& nn : bv_atoms)
    {
      addBBLemma(nn);
    }
  }

  return false;  // Return false to enable equality engine reasoning in Theory.
}

TrustNode BVSolverBitblastInternal::explain(TNode n)
{
  Debug("bv-bitblast-internal") << "explain called on " << n << std::endl;
  return d_im.explainLit(n);
}

bool BVSolverBitblastInternal::collectModelValues(TheoryModel* m,
                                                  const std::set<Node>& termSet)
{
  return d_bitblaster->collectModelValues(m, termSet);
}

Node BVSolverBitblastInternal::getValue(TNode node, bool initialize)
{
  if (node.isConst())
  {
    return node;
  }

  if (!d_bitblaster->hasBBTerm(node))
  {
    return initialize ? utils::mkConst(utils::getSize(node), 0u) : Node();
  }

  Valuation& val = d_state.getValuation();

  std::vector<Node> bits;
  d_bitblaster->getBBTerm(node, bits);
  Integer value(0), one(1), zero(0), bit;
  for (size_t i = 0, size = bits.size(), j = size - 1; i < size; ++i, --j)
  {
    bool satValue;
    if (val.hasSatValue(bits[j], satValue))
    {
      bit = satValue ? one : zero;
    }
    else
    {
      if (!initialize) return Node();
      bit = zero;
    }
    value = value * 2 + bit;
  }
  return utils::mkConst(bits.size(), value);
}

BVProofRuleChecker* BVSolverBitblastInternal::getProofChecker()
{
  return &d_checker;
}

}  // namespace bv
}  // namespace theory
}  // namespace cvc5
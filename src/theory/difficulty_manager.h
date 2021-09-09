/******************************************************************************
 * Top contributors (to current version):
 *   Andrew Reynolds
 *
 * This file is part of the cvc5 project.
 *
 * Copyright (c) 2009-2021 by the authors listed in the file AUTHORS
 * in the top-level source directory and their institutional affiliations.
 * All rights reserved.  See the file COPYING in the top-level source
 * directory for licensing information.
 * ****************************************************************************
 *
 * Relevance manager.
 */

#include "cvc5_private.h"

#ifndef CVC5__THEORY__DIFFICULTY_MANAGER__H
#define CVC5__THEORY__DIFFICULTY_MANAGER__H

#include "context/cdhashmap.h"
#include "context/cdlist.h"
#include "expr/node.h"
#include "theory/valuation.h"

namespace cvc5 {
namespace theory {

class TheoryModel;

/**
 * Difficulty manager, which tracks an estimate of the difficulty of each
 * preprocessed assertion during solving.
 */
class DifficultyManager
{
  typedef context::CDList<Node> NodeList;
  typedef context::CDHashMap<Node, uint64_t> NodeUIntMap;

 public:
  DifficultyManager(context::Context* c, Valuation val);
  /**
   * Get difficulty map, which populates dmap mapping preprocessed assertions
   * to a difficulty measure (a constant integer).
   */
  void getDifficultyMap(std::map<Node, Node>& dmap);
  /**
   * Notify lemma, for difficulty measurements. This increments the difficulty
   * of assertions that share literals with that lemma if the difficulty mode
   * is LEMMA_LITERAL. In particular, for each literal lit in the lemma lem, we
   * increment the difficulty of the assertion res[lit], which corresponds to
   * the assertion that was the reason why the literal is relevant in the
   * current context.
   *
   * @param rse Mapping from literals to the preprocessed assertion that was
   * the reason why that literal was relevant in the current context
   * @param lem The lemma
   */
  void notifyLemma(const std::map<TNode, TNode>& rse, Node lem);
  /**
   * Notify that `m` is a (candidate) model. This increments the difficulty
   * of assertions that are not satisfied by that model.
   *
   * @param input The list of preprocessed assertions
   * @param m The candidate model.
   */
  void notifyCandidateModel(const NodeList& input, TheoryModel* m);

 private:
  /** Increment difficulty on assertion a */
  void incrementDifficulty(TNode a, uint64_t amount = 1);
  /** The valuation object, used to query current value of theory literals */
  Valuation d_val;
  /**
   * User-context dependent mapping from input assertions to difficulty measure
   */
  NodeUIntMap d_dfmap;
};

}  // namespace theory
}  // namespace cvc5

#endif /* CVC5__THEORY__DIFFICULTY_MANAGER__H */
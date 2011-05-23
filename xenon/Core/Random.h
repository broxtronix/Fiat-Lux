#ifndef __PE_CORE_RANDOM_H__
#define __PE_CORE_RANDOM_H__

#include <boost/random/linear_congruential.hpp>

namespace pe {

  class RandomGenerator {
    boost::minstd_rand rng;

  public:
    // Seed random number generator on construction
    RandomGenerator() : rng(time(0)) {}

    int uniform_int(int low, int hi);
    float uniform(float low, float hi);
  };

  /// Static method to access the singleton instance of the random
  /// number generator.
  ///
  RandomGenerator& pe_random();

} // namespace pe

#endif

#include <boost/random/uniform_int.hpp>
#include <boost/random/uniform_real.hpp>
#include <boost/random/variate_generator.hpp>

#include <pe/Core/Random.h>
#include <pe/Core/Thread.h>


// -----------------------------------------------------------
// Create a single instance of the Time Struct
// -----------------------------------------------------------

namespace {
  pe::RunOnce pe_random_once = PE_RUNONCE_INIT;
  boost::shared_ptr<pe::RandomGenerator> pe_random_ptr;
  void init_pe_random() {
    pe_random_ptr = boost::shared_ptr<pe::RandomGenerator>(new pe::RandomGenerator());
  }
}

pe::RandomGenerator& pe::pe_random() {
  pe_random_once.run( init_pe_random );
  return *pe_random_ptr;
}

// -----------------------------------------------------------
// RandomGenerator
// -----------------------------------------------------------

int pe::RandomGenerator::uniform_int(int low, int hi) {
  boost::uniform_int<> dist(low, hi);
  boost::variate_generator<boost::minstd_rand&, boost::uniform_int<> > uni(rng, dist);
  return uni();
}

float pe::RandomGenerator::uniform(float low, float hi) {
  boost::uniform_real<> dist(low, hi);
  boost::variate_generator<boost::minstd_rand&, boost::uniform_real<> > uni(rng, dist);
  return uni();
}


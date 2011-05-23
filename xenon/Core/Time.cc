// __BEGIN_LICENSE__
// Copyright (C) 2009 Michael J. Broxton
// All Rights Reserved.
// __END_LICENSE__

#include <xenon/Core/Time.h>
#include <xenon/Core/Stopwatch.h>
#include <boost/shared_ptr.hpp>

// -----------------------------------------------------------
// Create a single instance of the Time Struct
// -----------------------------------------------------------

namespace {
  xenon::RunOnce xenon_time_once = XENON_RUNONCE_INIT;
  boost::shared_ptr<xenon::XenonTime> xenon_time_ptr;
  void init_xenon_time() {
    xenon_time_ptr = boost::shared_ptr<xenon::XenonTime>(new xenon::XenonTime());
  }
}

double xenon::xenon_time() {
  xenon_time_once.run( init_xenon_time );
  return (*xenon_time_ptr)();
}

// ---------------------------------------------------------------------
// XenonTime
// ---------------------------------------------------------------------

xenon::XenonTime::XenonTime() {
  m_time = 0;    
  m_last_time = xenon::Stopwatch::microtime();
}

double xenon::XenonTime::operator()() {
  xenon::Mutex::Lock lock(m_mutex);
  long long new_time = xenon::Stopwatch::microtime();
  m_time += double(new_time - m_last_time) / 1e6;
  m_last_time = new_time;
  return m_time;
}

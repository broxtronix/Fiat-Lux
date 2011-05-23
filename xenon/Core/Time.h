// __BEGIN_LICENSE__
// Copyright (C) 2009 Michael J. Broxton
// All Rights Reserved.
// __END_LICENSE__

#ifndef __XENON_CORE_TIME__
#define __XENON_CORE_TIME__

#include <xenon/Core/Thread.h>

namespace xenon {

  // ---------------------------------------------------------------------
  // XenonTime
  // ---------------------------------------------------------------------

  class XenonTime {
    float m_time;
    long long m_last_time;
    xenon::Mutex m_mutex;

  public:
    XenonTime();
    double operator()();
  };

  /// Return the singleton instance of the PhosphorEssence time
  /// structure.  The time struct is created the first time this method
  /// is invoked and initialized to time = 0.  You should *always* access
  /// the time using this function.
  double xenon_time();

} // namespace xenon

#endif

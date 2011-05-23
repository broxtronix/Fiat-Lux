// __BEGIN_LICENSE__
// Copyright (C) 2006-2010 United States Government as represented by
// the Administrator of the National Aeronautics and Space Administration.
// All Rights Reserved.
// __END_LICENSE__

// All the Core singletons are consolidated here, to make their initialization
// more deterministic (since some of them depend on each other)

#ifndef __XENON_CORE_SYSTEM_H__
#define __XENON_CORE_SYSTEM_H__

namespace xenon {

  class Cache;
  class Log;
  class Settings;
  class StopwatchSet;

  // This cache is used by default for all new BlockImageView<>'s such as
  // DiskImageView<>.
  Cache& xenon_system_cache();

  // You should *always* use this method if you want to access Vision Workbench
  // system log, where all Vision Workbench log messages go.  For example:
  //     xenon_log().console_log() << "Some text\n";
  Log& xenon_log();

  // Global instance of Settings
  Settings& xenon_settings();

  // Global instance of StopwatchSet
  StopwatchSet& xenon_stopwatch_set();
}

#endif

#include <xenon/Core/System.h>
#include <xenon/Core/Cache.h>
#include <xenon/Core/Log.h>
#include <xenon/Core/Settings.h>
#include <xenon/Core/Stopwatch.h>

namespace {
  xenon::RunOnce settings_once      = XENON_RUNONCE_INIT;
  xenon::RunOnce resize_once        = XENON_RUNONCE_INIT;
  xenon::RunOnce stopwatch_set_once = XENON_RUNONCE_INIT;
  xenon::RunOnce system_cache_once  = XENON_RUNONCE_INIT;
  xenon::RunOnce log_once           = XENON_RUNONCE_INIT;

  xenon::Settings     *settings_ptr      = 0;
  xenon::StopwatchSet *stopwatch_set_ptr = 0;
  xenon::Cache        *system_cache_ptr  = 0;
  xenon::Log          *log_ptr           = 0;

  void init_settings() {
    settings_ptr = new xenon::Settings();
  }

  void resize_cache() {
    if (system_cache_ptr->max_size() == 0)
      system_cache_ptr->resize(settings_ptr->system_cache_size());
  }

  void init_system_cache() {
    system_cache_ptr = new xenon::Cache(0);
  }

  void init_stopwatch_set() {
    stopwatch_set_ptr = new xenon::StopwatchSet();
  }

  void init_log() {
    log_ptr = new xenon::Log();
  }
}

xenon::Settings &xenon::xenon_settings() {
  system_cache_once.run( init_system_cache );
  settings_once.run( init_settings );
  return *settings_ptr;
}

xenon::Cache &xenon::xenon_system_cache() {
  system_cache_once.run( init_system_cache );
  settings_once.run( init_settings );
  settings_ptr->reload_config();
  resize_once.run(resize_cache);
  return *system_cache_ptr;
}

xenon::StopwatchSet &xenon::xenon_stopwatch_set() {
  stopwatch_set_once.run( init_stopwatch_set );
  return *stopwatch_set_ptr;
}

xenon::Log &xenon::xenon_log() {
  log_once.run( init_log );
  return *log_ptr;
}

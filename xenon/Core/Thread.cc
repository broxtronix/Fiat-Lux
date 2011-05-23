// __BEGIN_LICENSE__
// Copyright (C) 2006-2010 United States Government as represented by
// the Administrator of the National Aeronautics and Space Administration.
// All Rights Reserved.
// __END_LICENSE__


#include <xenon/Core/Thread.h>
#include <xenon/config.h>

namespace xenon {
namespace thread {

  // These static variables are used to generate unique identifiers
  // for threads as identifiers are requested using the static
  // Thread::id() method.
  static xenon::uint64 xenon_thread_next_available_id = 0;

  // Both the mutex and the thread-local storage need to be available to all
  // destructors (in case they call Thread::id()). If the object being
  // destructed is static and defined in a different file, the destruction
  // order is undefined. That causes a destruction race. To prevent this race,
  // we use the construct-on-first-use idiom. See
  // http://www.parashift.com/c++-faq-lite/ctors.html#faq-10.15 for more info.
  static Mutex& xenon_thread_id_mutex() {
    static Mutex* m = new Mutex();
    return *m;
  }

  typedef boost::thread_specific_ptr<xenon::uint64> ptr_t;

  static ptr_t& xenon_thread_id_ptr() {
    static ptr_t* ptr = new ptr_t();
    return *ptr;
  }

}} // namespace xenon::thread

xenon::uint64 xenon::Thread::id() {

  // If the thread ID has not been accessed before, we initialize
  // it with a unique ID.
  if (thread::xenon_thread_id_ptr().get() == 0) {
    Mutex::Lock lock(thread::xenon_thread_id_mutex());
    thread::xenon_thread_id_ptr().reset(new xenon::uint64(thread::xenon_thread_next_available_id++));
  }

  // Then we return the result.
  xenon::uint64* result = thread::xenon_thread_id_ptr().get();
  return *result;
}

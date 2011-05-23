// __BEGIN_LICENSE__
// Copyright (C) 2006-2010 United States Government as represented by
// the Administrator of the National Aeronautics and Space Administration.
// All Rights Reserved.
// __END_LICENSE__

/// \file Core/Exception.cc
///
/// Error / exception handling facilities.
///
/// See Core/Exception.h for documentation.
///
#include <xenon/Core/Exception.h>
#include <xenon/Core/Features.h>

#include <cstdlib>

namespace {

  /// The default exception handler type and object, which throws
  /// the exceptions its given unless XENON_ENABLE_EXCEPTIONS is 0, in
  /// which case it prints the message and calls abort().
  static class DefaultExceptionHandler : public xenon::ExceptionHandler {
  public:
    virtual void handle( xenon::Exception const& e ) const XENON_NORETURN {
#if defined(XENON_ENABLE_EXCEPTIONS) && (XENON_ENABLE_EXCEPTIONS==1)
      e.default_throw();
#else
      xenon::xenon_out(xenon::ErrorMessage) << "Fatal error: " << e.what() << std::endl;
#endif
      std::abort();
    }
    virtual ~DefaultExceptionHandler() XENON_NOTHROW {}
  } _xenon_default_exception_handler;

  /// The application-wide exception handler pointer.
  static xenon::ExceptionHandler const* _xenon_exception_handler = &_xenon_default_exception_handler;

};

void xenon::set_exception_handler( xenon::ExceptionHandler const* eh ) {
  if( eh ) _xenon_exception_handler = eh;
  else _xenon_exception_handler = &_xenon_default_exception_handler;
}

void xenon::xenon_throw( xenon::Exception const& e ) {
  _xenon_exception_handler->handle( e );
  // We cannot return.
  std::abort();
}

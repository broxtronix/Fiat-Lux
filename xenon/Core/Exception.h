// __BEGIN_LICENSE__
// Copyright (C) 2006-2010 United States Government as represented by
// the Administrator of the National Aeronautics and Space Administration.
// All Rights Reserved.
// __END_LICENSE__


/// \file Exception.h
///
/// Exception classes and related functions and macros.
///
/// The Vision Workbench is intended in part to be used in flight
/// systems, experimental multiprocessor systems, or other
/// environments where exceptions may not be fully supported.  As a
/// result, the use of exceptions within the Vision Workbench is
/// tightly controlled.  In particular, the exception usage rules were
/// designed to minimize the impact on platforms that do not support
/// exceptions at all.  There is a standard Vision Workbench
/// "exception" class hierarchy which is used to describe errors and
/// can be used even on platforms that do not support the C++
/// exception system.
///
/// The xenon::Exception class serves as a base class for all XENONB error
/// types.  It is designed to make it easy to throw exceptions with
/// meaningful error messages.  For example, this invocation:
///
///  <TT>xenon_throw( xenon::Exception() << "Unable to open file \"" << filename << "\"!" );</TT>
///
/// might generate a message like this:
///
///  <TT>terminate called after throwing an instance of 'xenon::Exception'</TT>
///  <TT>     what():  Unable to open file "somefile.foo"! </TT>
///
/// A variety of standard derived exception types are provided; in the
/// above example, the exception should probably have been of type
/// xenon::IOErr.  Also, two macros, XENON_ASSERT(condition,exception) and
/// XENON_DEBUG_ASSERT(condition,exception), are provided, with the usual
/// assertion semantics.  The only difference is that the debug
/// assertions will be disabled for increased performance in release
/// builds when XENON_DEBUG_LEVEL is defined to zero (which happens by
/// default when NDEBUG is defined).
///
/// Note that in the example the exception was thrown by calling the
/// xenon_throw() function rather than by using the C++ throw statement.
/// On platforms that do support C++ exceptions the default behavior
/// for xenon_throw() is to throw the exception in the usual way.
/// However, the user can provide their own error-handling mechanism
/// if they choose.  For example, the default behavior when exceptions
/// are disabled is to print the error text to stderr and call
/// abort().
///
/// In general the only allowed usage of exceptions within the Vision
/// Workbench is throwing them using xenon_throw().  In particular, try
/// and catch blocks are generally prohibited, so exceptions can only
/// be used to report fatal errors that the library is unable to
/// recover from by itself.  Other uses of exceptions are allowed only
/// under a few special circumstances.  If a part of the Vision
/// Workbench depends on a third-party library that fundamentally
/// relies on exceptions, then that part of the Vision Workbench may
/// use exceptions as well.  However, in that case that entire portion
/// of the Vision Workbench must be disabled when exceptions are not
/// supported.  Similarly, if a part of the Vision Workbench that
/// provides a high-level service cannot reasonably be written without
/// the full use of exceptions, then this portion may also be disabled
/// on platforms without exceptions.  In both of these cases it must
/// be clearly documented that these features are not available on
/// platforms that do not support exceptions.  Finally, it is legal to
/// catch an exception within the library for the sole purpose of
/// re-throwing an exception with a more informative data type or
/// error message.  This purely cosmetic usage must be conditionally
/// compiled like this:
///  #if defined(XENON_ENABLE_EXCEPTIONS) && (XENON_ENABLE_EXCEPTIONS==1) )
/// Obviously this functionality will be disabled on platforms
/// that do not support exceptions.
///
/// Exceptions are enabled or disabled based on the value of the
/// XENON_ENABLE_EXCEPTIONS macro defined in xenon/config.h.  This value can be
/// set by passing the command line options --enable-exeptions (the
/// default) or --disable-exceptions to the configure script prior to
/// buliding the Vision Workbench.  This option also sets an automake
/// variable called ENABLE_EXCEPTIONS which may be used by the build
/// system to conditionally compile entire source files.
///
/// In either case the default behavior of xenon_throw() may be
/// overridden by calling set_exception_handler(), passing it a
/// pointer to a user-defined object derived from ExceptionHandler.
/// The user specifies the error-handling behavior by overriding the
/// abstract method handle().  When exceptions have not been disabled,
/// the Exception class and its children define a virtual method
/// default_throw() which the handler may call to have the exception
/// throw itself in a type-aware manner.
///
#ifndef __XENON_CORE_EXCEPTION_H__
#define __XENON_CORE_EXCEPTION_H__

#include <string>
#include <sstream>
#include <ostream>

#include <xenon/Core/Features.h>
#include <xenon/config.h>

#if defined(XENON_ENABLE_EXCEPTIONS) && (XENON_ENABLE_EXCEPTIONS==1)
#include <exception>
#define XENON_IF_EXCEPTIONS(x) x
#else
#define XENON_IF_EXCEPTIONS(x)
#endif

namespace xenon {

  /// The core exception class.
  struct Exception XENON_IF_EXCEPTIONS( : public std::exception )
  {

    /// The default constructor generates exceptions with empty error
    /// message text.  This is the cleanest approach if you intend to
    /// use streaming (via operator <<) to generate your message.
    Exception() XENON_NOTHROW {}

    virtual ~Exception() XENON_NOTHROW {}

    /// Copy Constructor
    Exception( Exception const& e ) XENON_NOTHROW
      XENON_IF_EXCEPTIONS( : std::exception(e) ) {
      m_desc << e.m_desc.str();
    }

    /// Assignment operator copies the error string.
    Exception& operator=( Exception const& e ) XENON_NOTHROW {
      m_desc.str( e.m_desc.str() );
      return *this;
    }

    /// Returns a the error message text for display to the user.  The
    /// returned pointer must be used immediately; other operations on
    /// the exception may invalidate it.  If you need the data for
    /// later, you must save it to a local buffer of your own.
    virtual const char* what() const XENON_NOTHROW {
      m_what_buf = m_desc.str();
      return m_what_buf.c_str();
    }

    /// Returns the error message text as a std::string.
    std::string desc() const { return m_desc.str(); }

    /// Returns a string version of this exception's type.
    virtual std::string name() const { return "Exception"; }

    void set( std::string const& s ) { m_desc.str(s); }
    void reset() { m_desc.str(""); }

    XENON_IF_EXCEPTIONS( virtual void default_throw() const { throw *this; } )

  protected:
      virtual std::ostringstream& stream() {return m_desc;}

  private:
    // The error message text.
    std::ostringstream m_desc;

    // A buffer for storing the full exception description returned by
    // the what() method, which must generate its return value from
    // the current value of m_desc.  The what() method provides no
    // mechanism for freeing the returned string, and so we handle
    // allocation of that memory here, internally to the exception.
    mutable std::string m_what_buf;
  };

  // Use this macro to construct new exception types that do not add
  // additional functionality.  If you can think of a clean way to do
  // this using templates instead of the preprocessor, please do.  For
  // now, we're stuck with this.
  //
  // Some functions need to return the *this pointer with the correct
  // subclass type, and these are defined in the macro below rather
  // than the base exception class above.   These are:
  //
  // Exception::operator=():
  // The assignment operator must return an instance of the subclass.
  //
  // Exception::operator<<():
  // The streaming operator (<<) makes it possible to quickly
  // generate error message text.  This is currently implemented
  // by simply forwarding invocations of this method to an
  // internal ostringstream.

  /// Macro for quickly creating a hierarchy of exceptions, all of
  /// which share the same functionality.
  #define XENON_DEFINE_EXCEPTION(exception_type,base)                             \
    struct exception_type : public base {                                      \
      XENON_EXCEPTION_API(exception_type)                                         \
    }

  // This sentinel catches users who forget to use XENON_EXCEPTION_API
  #define _XENON_EXCEPTION_SENTINEL(e) _YouForgot_XENON_EXCEPTION_API_OnException_ ## e

  // Macro for creating a hierarchy of exceptions that may have additional
  // functions or data. When using this macro, you must include the
  // XENON_EXCEPTION_API macro inside the braces
  #define XENON_DEFINE_EXCEPTION_EXT(exception_type,base)                         \
    struct _XENON_EXCEPTION_SENTINEL(exception_type) : public base {              \
      virtual std::string name() const = 0;                                    \
    };                                                                         \
    struct exception_type : public _XENON_EXCEPTION_SENTINEL(exception_type)

  #define XENON_EXCEPTION_API(exception_type)                                     \
    virtual std::string name() const { return #exception_type; }               \
    XENON_IF_EXCEPTIONS( virtual void default_throw() const { throw *this; } )    \
    template <class T>                                                         \
    exception_type& operator<<( T const& t ) { stream() << t; return *this; }

  /// Invalid function argument exception
  XENON_DEFINE_EXCEPTION(ArgumentErr, Exception);

  /// Incorrect program logic exception
  XENON_DEFINE_EXCEPTION(LogicErr, Exception);

  /// Invalid program input exception
  XENON_DEFINE_EXCEPTION(InputErr, Exception);

  /// IO failure exception
  XENON_DEFINE_EXCEPTION(IOErr, Exception);

  /// Arithmetic failure exception
  XENON_DEFINE_EXCEPTION(MathErr, Exception);

  /// Unexpected null pointer exception
  XENON_DEFINE_EXCEPTION(NullPtrErr, Exception);

  /// Invalid type exception
  XENON_DEFINE_EXCEPTION(TypeErr, Exception);

  /// Not found exception
  XENON_DEFINE_EXCEPTION(NotFoundErr, Exception);

  /// Unimplemented functionality exception
  XENON_DEFINE_EXCEPTION(NoImplErr, Exception);

  /// Operation aborted partway through (e.g. with ProgressCallback returning Abort)
  XENON_DEFINE_EXCEPTION(Aborted, Exception);


  /// The abstract exception handler base class, which users
  /// can subclass to install an alternative exception handler.
  class ExceptionHandler {
  public:
    virtual void handle( Exception const& e ) const XENON_NORETURN = 0;
    virtual ~ExceptionHandler() XENON_NOTHROW {}
  };

  /// Sets the application-wide exception handler.  Pass zero
  /// as an argument to reinstate the default handler.  The
  /// default behavior is to throw the exception unless the
  /// XENON_ENABLE_EXCEPTIONS macro in xenon/config.h was defined to 0
  /// at build time, in which case the default behavior is to
  /// print the error message at the ErrorMessage level and
  /// to call abort().
  void set_exception_handler( ExceptionHandler const* eh );

  /// Throws an exception via the Vision Workbench error
  /// handling mechanism, which may not actually involvle
  /// throwing an exception in the usual C++ sense.
  void xenon_throw( Exception const& e ) XENON_NORETURN;

} // namespace xenon

/// The XENON_ASSERT macro throws the given exception if the given
/// condition is not met.  The XENON_DEBUG_ASSERT macro does the same
/// thing, but is disabled if XENON_DEBUG_LEVEL is zero.  The default
/// value for XENON_DEBUG_LEVEL is defined in Debugging.h.
#define XENON_ASSERT(cond,excep) do { if(!(cond)) xenon::xenon_throw( excep ); } while(0)
#define XENON_LINE_ASSERT(cond) do { if(!(cond)) xenon::xenon_throw( xenon::LogicErr() << "Assertion failed (" << __FILE__ << ":" << __LINE__ << "): " << #cond); } while(0)
#if XENON_DEBUG_LEVEL == 0
#define XENON_DEBUG_ASSERT(cond,excep) do {} while(0)
#else
// Duplicate the definition to avoid extra macro expansion in recusion
#define XENON_DEBUG_ASSERT(cond,excep) do { if(!(cond)) xenon::xenon_throw( excep ); } while(0)
#endif

#endif // __XENON_CORE_EXCEPTION_H__

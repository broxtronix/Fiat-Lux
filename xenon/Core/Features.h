// __BEGIN_LICENSE__
// Copyright (C) 2011 Michael Broxton
// Stanford University
// All Rights Reserved.
//
// Some code herein derived from the NASA Vision Workbench
// Copyright (C) 2006-2010 United States Government as represented by
// the Administrator of the National Aeronautics and Space Administration.
// All Rights Reserved.
// __END_LICENSE__

// This file contains some useful macros and definitions so they don't get
// scattered everywhere.

#ifndef __XENON_CORE_FEATURES_H__
#define __XENON_CORE_FEATURES_H__

#include <xenon/config.h>

#if defined(XENON_COMPILER_HAS_ATTRIBUTE_DEPRECATED) && (XENON_COMPILER_HAS_ATTRIBUTE_DEPRECATED==1)
#define XENON_DEPRECATED __attribute__((deprecated))
#else
#define XENON_DEPRECATED
#endif

#if defined(XENON_COMPILER_HAS_ATTRIBUTE_NORETURN) && (XENON_COMPILER_HAS_ATTRIBUTE_NORETURN==1)
#define XENON_NORETURN __attribute__((noreturn))
#else
#define XENON_NORETURN
#endif

#if defined(XENON_COMPILER_HAS_ATTRIBUTE_WARN_UNUSED_RESULT) && (XENON_COMPILER_HAS_ATTRIBUTE_WARN_UNUSED_RESULT==1)
#define XENON_WARN_UNUSED __attribute__((warn_unused_result))
#else
#define XENON_WARN_UNUSED
#endif

#define XENON_NOTHROW XENON_IF_EXCEPTIONS(throw())

/// The master compile-time debugging level flag.  The default value
/// for XENON_DEBUG_LEVEL is guessed based on whether or not NDEBUG
/// is defined if the user has not specified it explicitly.
#ifndef XENON_DEBUG_LEVEL
#ifdef NDEBUG
#define XENON_DEBUG_LEVEL 0
#else
#define XENON_DEBUG_LEVEL 1
#endif
#endif

/// A quick macro for selectively disabling code in non-debug builds.
#if XENON_DEBUG_LEVEL == 0
#define XENON_DEBUG(x)
#else
#define XENON_DEBUG(x) x
#endif

#endif

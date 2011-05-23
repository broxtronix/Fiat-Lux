// __BEGIN_LICENSE__
// Copyright (C) 2006-2010 United States Government as represented by
// the Administrator of the National Aeronautics and Space Administration.
// All Rights Reserved.
// __END_LICENSE__


#ifndef __XENON_CORE_CONFIGPARSER_H__
#define __XENON_CORE_CONFIGPARSER_H__

#include <istream>

namespace xenon {
  class Settings;

  // Parse a stream containing a config file,
  // and sets options through given settings object
  // throws on error, prints to cerr on warning
  void parse_config(std::basic_istream<char>& stream, xenon::Settings&);

  // Parse a config file, and sets options through given settings object
  // throws on error, prints to cerr on warning
  void parse_config_file(const char* fn, xenon::Settings&);
}

#endif

// __BEGIN_LICENSE__
// Copyright (C) 2006-2010 United States Government as represented by
// the Administrator of the National Aeronautics and Space Administration.
// All Rights Reserved.
// __END_LICENSE__


#include <iomanip>
#include <xenon/Core/ProgressCallback.h>

namespace {
  xenon::ProgressCallback g_dummy_progress_callback_instance;
}

const xenon::ProgressCallback &xenon::ProgressCallback::dummy_instance() {
  return g_dummy_progress_callback_instance;
}

// Deprecrated Progress Bar
xenon::TerminalProgressCallback::TerminalProgressCallback( MessageLevel level, std::string pre_progress_text, uint32_t precision) : m_level(level), m_namespace(".progress"), m_pre_progress_text(pre_progress_text), m_last_reported_progress(-1), m_precision(precision), m_step(std::pow(10., -(int32_t(precision)+2))) {
  boost::replace_all(m_pre_progress_text,"\t","        ");
  if ( m_level <  InfoMessage )
    xenon_throw( ArgumentErr() << "TerminalProgressBar must be message level InfoMessage or higher." );

  // Calculating bar length
  m_bar_length = m_max_characters - static_cast<uint32>(m_pre_progress_text.size()) - 4 - 3;
  if ( m_precision > 0 )
    m_bar_length -= m_precision + 1; // 1 for decimal point
}

void xenon::TerminalProgressCallback::print_progress() const {
  if (fabs(m_progress - m_last_reported_progress) > m_step) {
    m_last_reported_progress = m_progress;
    int pi = static_cast<int>(m_progress * double(m_bar_length));
    std::ostringstream p;
    p << "\r" << m_pre_progress_text << "[";
    for( int i=0; i<pi; ++i ) p << "*";
    for( int i=m_bar_length; i>pi; --i ) p << ".";
    p << "] " << std::setprecision(m_precision) << std::fixed << (m_progress*100.0) << "%";
    xenon_out(m_level, m_namespace) << p.str() << std::flush;
  }
}

void xenon::TerminalProgressCallback::report_aborted(std::string why) const {
  Mutex::Lock lock(m_mutex);
  xenon_out(m_level, m_namespace) << " Aborted: " << why << std::endl;
}

void xenon::TerminalProgressCallback::report_finished() const {
  Mutex::Lock lock(m_mutex);
  uint32 cbar_length = m_max_characters - static_cast<uint32>(m_pre_progress_text.size()) -12;
  std::ostringstream p;
  for ( uint32 i = 0; i < cbar_length; i++ )
    p << "*";
  xenon_out(m_level, m_namespace) << "\r" << m_pre_progress_text
                               << "[" << p.str() << "] Complete!\n";
}


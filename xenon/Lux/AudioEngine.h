// __BEGIN_LICENSE__
// Copyright (C) 2009 Michael J. Broxton
// All Rights Reserved.
// __END_LICENSE__

#ifndef __LUX_AUDIO_ENGINE_H__
#define __LUX_AUDIO_ENGINE_H__

#include <xenon/Core/Thread.h>
#include <xenon/Lux/AudioClient.h>
#include <boost/circular_buffer.hpp>

// Aubio is used for real-time analysis of the music.
#include <aubio.h>
#include <aubioext.h>

namespace lux {

  // ---------------------------------------------------------------------------
  //                              Audio Engine
  // ---------------------------------------------------------------------------
  class AudioEngine : public AudioClient {
    xenon::Mutex m_mutex;
    int m_initialized;

    // Aubio data structure and storage

    smpl_t m_threshold;
    smpl_t m_silence;  
    uint_t m_median;
  
    fvec_t* m_ibuf;
    fvec_t* m_tempobuf;
    cvec_t* m_fftgrain;
    fvec_t* m_onset_kl;
    fvec_t* m_onset_complex;
    aubio_mfft_t *m_mfft;
    
    aubio_pvoc_t *m_phase_vocoder;
    aubio_pitchdetection_t *m_pitch_detection;
    aubio_pickpeak_t *m_peak_picker;
    aubio_onsetdetection_t *m_onset_detection_kl;
    aubio_onsetdetection_t *m_onset_detection_complex;
    aubio_tempo_t *m_tempo;
    int m_overlap_size;
    int m_channels;

    // "Public" buffers (which can be "drained" and returned as numpy
    // arrays in python.
    boost::circular_buffer<float> m_left_buffer;
    boost::circular_buffer<float> m_right_buffer;
    boost::circular_buffer<float> m_avg_buffer;    
    boost::circular_buffer<int> m_onset_buffer;
    boost::circular_buffer<float> m_pitch_buffer;
    boost::circular_buffer<int> m_tempo_tactus_buffer;
    boost::circular_buffer<int> m_tempo_onset_buffer;

    // Template class for copy raw data out of these buffers.  You do
    // not call this yourself.
    template <class T>
    T* malloc_and_copy(boost::circular_buffer<T> &buffer, int& size, bool clear) {
      xenon::Mutex::Lock lock(m_mutex);
      size = buffer.size();
      T* result = (T*)malloc(sizeof(T) * buffer.size());
      std::copy(buffer.begin(), buffer.end(), result);
      if (clear) buffer.clear();
      return result;
    }

  public:
    
    AudioEngine(std::string const& jack_endpoint_name);
    virtual ~AudioEngine();

    // Called by Jack as new audio frames arrive
    virtual int process_callback(nframes_t nframes);

    // ---------- ACCESSOR FUNCTIONS --------------
    //
    // Use these function carefully... they return malloc'd blocks of
    // memory that get inherited by Python.
    
    float* get_left_buffer(int &size, bool clear) { return malloc_and_copy(m_left_buffer, size, clear); }
    float* get_right_buffer(int &size, bool clear) { return malloc_and_copy(m_right_buffer, size, clear); }
    float* get_avg_buffer(int &size, bool clear) { return malloc_and_copy(m_avg_buffer, size, clear); }
    int* get_onset_buffer(int &size, bool clear) { return malloc_and_copy(m_onset_buffer, size, clear); }
    float* get_pitch_buffer(int &size, bool clear) { return malloc_and_copy(m_pitch_buffer, size, clear); }
    int* get_tempo_tactus_buffer(int &size, bool clear) { return malloc_and_copy(m_tempo_tactus_buffer, size, clear); }
    int* get_tempo_onset_buffer(int &size, bool clear) { return malloc_and_copy(m_tempo_onset_buffer, size, clear); }

    // Clear all buffers
    void clear_all();
  };
}

#endif // __AUDIOENGINE_H__

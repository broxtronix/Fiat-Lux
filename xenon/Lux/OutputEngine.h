// __BEGIN_LICENSE__
// Copyright (C) 2009 Michael J. Broxton
// All Rights Reserved.
// __END_LICENSE__

#ifndef __LUX_OUTPUT_ENGINE_H__
#define __LUX_OUTPUT_ENGINE_H__

#include <xenon/Core/Thread.h>
#include <xenon/Lux/AudioClient.h>
#include <Eigen/Dense>

namespace lux {

  // ---------------------------------------------------------------------------
  //                              Output Engine
  // 
  // This class conditions the audio before it heads off to the laser
  // amp.  It takes care of geometric corrections, overall brightness
  // adjustment & calibration, and it generates the safety interlock.
  // ---------------------------------------------------------------------------
  class OutputEngine : public AudioClient {
    xenon::Mutex m_mutex;
    int m_enable_period, m_enable_ctr, m_frames_dead, m_dead_time;
    Eigen::Matrix<float, 3, 3> m_transform_matrix;

    bool m_safety_first;

    bool m_preamp_calibration;
    float m_preamp_calibration_frequency;
    float m_preamp_calibration_gain;
    float m_preamp_calibration_offset;
    float m_calibration_time;

    bool m_laser_calibration;
    float m_laser_calibration_red_intensity;
    float m_laser_calibration_green_intensity;
    float m_laser_calibration_blue_intensity;
    float m_laser_calibration_x_frequency;
    float m_laser_calibration_y_frequency;

    bool m_swap_xy;
    bool m_invert_x;
    bool m_invert_y;
    bool m_enable_x;
    bool m_enable_y;

    bool m_blank_invert;
    bool m_blank_enable;
    bool m_output_enable;
    bool m_output_initialized;

    float m_size_multiplier;
    float m_red_intensity_multiplier;
    float m_red_intensity_offset;
    float m_green_intensity_multiplier;
    float m_green_intensity_offset;
    float m_blue_intensity_multiplier;
    float m_blue_intensity_offset;

    void generate_enable(sample_t *buf, nframes_t nframes);
    void transform(sample_t *ox, sample_t *oy);

  public:
    
    OutputEngine(std::string const& jack_endpoint_name);
    virtual ~OutputEngine();

    // Turn on pre-amp calibration mode
    void setPreampCalibration(int state) { m_preamp_calibration = state; }
    void setPreampCalibrationFrequency(float frequency) { m_preamp_calibration_frequency = frequency; }
    void setPreampCalibrationGain(float gain) { m_preamp_calibration_gain = gain; }
    void setPreampCalibrationOffset(float offset) { m_preamp_calibration_offset = offset; }

    // Turn on laser calibration mode
    void setLaserCalibration(int state) { m_laser_calibration = state; }
    void setLaserCalibrationRedIntensity(float gain) { m_laser_calibration_red_intensity = gain; }
    void setLaserCalibrationGreenIntensity(float gain) { m_laser_calibration_green_intensity = gain; }
    void setLaserCalibrationBlueIntensity(float gain) { m_laser_calibration_blue_intensity = gain; }
    void setLaserCalibrationXFrequency(float frequency) { m_laser_calibration_x_frequency = frequency; }
    void setLaserCalibrationYFrequency(float frequency) { m_laser_calibration_y_frequency = frequency; }

    // Output Settings
    void setSafetyFirst(int state) { m_safety_first = state; }
    void setSwapXY(int state) { std::cout << "setting swap to " << state << "\n"; m_swap_xy = state; }
    void setInvertX(int state) { m_invert_x = state; }
    void setInvertY(int state) { m_invert_y = state; }
    void setEnableX(int state) { m_enable_x = state; }
    void setEnableY(int state) { m_enable_y = state; }
    void setBlankInvert(int state) { m_blank_invert = state; }
    void setBlankEnable(int state) { m_blank_enable = state; }
    void setOutputEnable(int state) { m_output_enable = state; }

    // Hardware safety intelock.  The lasers will not receive any
    // control signals if this is set to false.
    void setOutputInitialized(int state) { m_output_initialized = state; }

    void setSizeMultiplier(float value);
    void redIntensityMultiplier(float value);
    void greenIntensityMultiplier(float value);
    void blueIntensityMultiplier(float value);
    void redIntensityOffset(float value);
    void greenIntensityOffset(float value);
    void blueIntensityOffset(float value);

    void setTransformMatrix(float a11, float a12, float a13,
                            float a21, float a22, float a23,
                            float a31, float a32, float a33);

    // Called by Jack as new audio frames arrive
    virtual int process_callback(nframes_t nframes);

    // Called by jack when the sample rate changes
    virtual int sample_rate_callback(nframes_t nframes);

  };
}

#endif // __AUDIOENGINE_H__

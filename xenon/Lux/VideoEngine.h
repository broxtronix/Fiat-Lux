#ifndef __LUX_VIDEO_ENGINE_H__
#define __LUX_VIDEO_ENGINE_H__

#include <xenon/Lux/AudioClient.h>
#include <xenon/Core/Thread.h>
#include <xenon/Math/Vector.h>
#include <string>
#include <iostream>

#ifdef __APPLE__
#include <xenon/Graphics/SyphonClient.h>
#endif 

namespace lux {

  class VideoEngine {
    xenon::Mutex m_mutex;
    int m_viewport_width, m_viewport_height;
    int m_record_frame_number;
    
    // Contouring parameters
    double m_contour_threshold;       // 0.2
    double m_contour_blur_sigma;      // 1.5
    double m_contour_min_area;        // 100 
    double m_contour_max_area;        // 640*480
    double m_contour_num_considered;  // 10
    int m_contour_mode;               // CV_RETR_EXTERNAL**  or CV_RETR_EXTERNAL
    int m_contour_method;             // CV_CHAIN_APPROX_SIMPLE** or CV_CHAIN_APPROX_NONE;

    std::vector<std::vector<xenon::Vector2> > m_contours_to_draw;
    
#ifdef __APPLE__
    xenon::graphics::XenonSyphonClient m_syphon_client;
#endif 

  public:

    VideoEngine(std::string application_name, std::string server_name);
    virtual ~VideoEngine() {} 

    void draw_gl();
    void draw_lasers();

    void resize_gl(int width, int height);

    // Set properties
    void setContourThreshold(float value) { m_contour_threshold = value; }
    void setContourBlurSigma(float value) { m_contour_blur_sigma = value; }
    void setContourMinArea(float value) { m_contour_min_area = value; }
    void setContourMaxArea(float value) { m_contour_max_area = value; }
    void setContourNumConsidered(int value) { m_contour_num_considered = value; }
    void setContourMode(int value) { m_contour_mode = value; }
    void setContourMethod(int value) { m_contour_method = value; }
  };

}

#endif // __LUX_VIDEO_ENGINE_H__

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

// OpenCV
#include <opencv/cv.h>

namespace lux {

  class VideoEngine {
    xenon::Mutex m_mutex;
    int m_viewport_width, m_viewport_height;
    int m_framebuffer_width, m_framebuffer_height;
    int m_record_frame_number;
    float m_aspect;
    GLuint m_framebuffer0;
    GLuint m_framebuffer_texture0;

    // Contouring parameters
    double m_contour_threshold;       // 0.2
    double m_contour_blur_sigma;      // 1.5
    double m_contour_min_area;        // 100 
    double m_contour_max_area;        // 640*480
    double m_contour_num_considered;  // 10
    int m_contour_mode;               // CV_RETR_EXTERNAL**  or CV_RETR_EXTERNAL
    int m_contour_method;             // CV_CHAIN_APPROX_SIMPLE** or CV_CHAIN_APPROX_NONE;
    float m_contour_frame_smoothing;
    int m_edge_detection_mode;
    cv::Mat m_previous_image;

    bool m_initialized;

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
    void initialize_gl();

    // Set properties
    void setContourThreshold(float value) { m_contour_threshold = value; }
    void setContourBlurSigma(float value) { m_contour_blur_sigma = value; }
    void setContourMinArea(float value) { m_contour_min_area = value; }
    void setContourMaxArea(float value) { m_contour_max_area = value; }
    void setContourNumConsidered(int value) { m_contour_num_considered = value; }
    void setEdgeDetectionMode(int value) { m_edge_detection_mode = value; }
    void setContourMode(int value) { m_contour_mode = value; }
    void setContourMethod(int value) { m_contour_method = value; }
  };

}

#endif // __LUX_VIDEO_ENGINE_H__

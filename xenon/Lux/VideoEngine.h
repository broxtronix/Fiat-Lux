#ifndef __LUX_VIDEO_ENGINE_H__
#define __LUX_VIDEO_ENGINE_H__

#include <xenon/Lux/AudioClient.h>
#include <string>
#include <iostream>

#ifdef __APPLE__
#include <xenon/Graphics/SyphonClient.h>
#endif 

namespace lux {

  class VideoEngine {

    
#ifdef __APPLE__
    xenon::graphics::XenonSyphonClient m_syphon_client;
#endif 

  public:

    VideoEngine(std::string application_name, std::string server_name);
    virtual ~VideoEngine() {} 

    void draw_gl();
    void resize_gl(int width, int height);
  };

}

#endif // __LUX_VIDEO_ENGINE_H__

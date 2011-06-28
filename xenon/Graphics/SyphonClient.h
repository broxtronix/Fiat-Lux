// Xenon Syphon Client
//
// Based off of ofxSyphonServer.h by astellato,vade,bangnoise on
// 11/6/10.
//
//  http://syphon.v002.info/license.php

#ifndef __XENON_SYPHON_CLIENT__
#define __XENON_SYPHON_CLIENT__

#import <xenon/Graphics/Texture.h>

namespace xenon {
namespace graphics {

  class XenonSyphonClient {
  protected:
    void *mClient;
    void* latestImage;
    Texture mTex;
    int width, height;
    bool bSetup;
    std::string name;
    
  public:
    XenonSyphonClient();
    ~XenonSyphonClient();
    
    void setup ();
    void setApplicationName(std::string appName);
    void setServerName(std::string serverName);
    
    void bind();
    void unbind();
    void draw();

    int getHeight();
    int getWidth();
    
    void draw(float x, float y, float w, float h);
    void draw(float x, float y);
    
  };
}} // namespace xenon::graphics

#endif __XENON_SYPHON_CLIENT__

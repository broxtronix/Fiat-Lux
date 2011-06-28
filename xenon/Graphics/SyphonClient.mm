// Xenon Syphon Client
//
// Based off of ofxSyphonServer.h by astellato,vade,bangnoise on
// 11/6/10.
//
//  http://syphon.v002.info/license.php

#import <xenon/Graphics/SyphonClient.h>
#import <xenon/Graphics/SyphonNameboundClient.h>
#import <Syphon/Syphon.h>

#ifdef __APPLE__
#include <OpenGL/gl.h>
#include <OpenGL/glu.h>
#include <AGL/agl.h>
#else // Linux
#include <GL/gl.h>
#include <GL/glu.h>
#endif

xenon::graphics::XenonSyphonClient::XenonSyphonClient() {
  bSetup = false;
}

xenon::graphics::XenonSyphonClient::~XenonSyphonClient() {
  NSAutoreleasePool* pool = [[NSAutoreleasePool alloc] init];
  
  [static_cast<SyphonNameboundClient*>(mClient) release];
  [pool drain];
}

void xenon::graphics::XenonSyphonClient::setup() {
  // Need pool
  NSAutoreleasePool* pool = [[NSAutoreleasePool alloc] init];
  
  mClient = [[SyphonNameboundClient alloc] init]; 
  bSetup = true;
  [pool drain];
}

void xenon::graphics::XenonSyphonClient::setApplicationName(std::string appName) {
  NSAutoreleasePool* pool = [[NSAutoreleasePool alloc] init];

  NSString *name = [NSString stringWithCString:appName.c_str() encoding:[NSString defaultCStringEncoding]];
  if(bSetup) {
    [static_cast<SyphonNameboundClient*>(mClient) setAppName:name];
  }

  [pool drain];
}
void xenon::graphics::XenonSyphonClient::setServerName(std::string serverName) {
  NSAutoreleasePool* pool = [[NSAutoreleasePool alloc] init];

  NSString *name = [NSString stringWithCString:serverName.c_str() encoding:[NSString defaultCStringEncoding]];
  if(bSetup) {
    [static_cast<SyphonNameboundClient*>(mClient) setName:name];
  }
  
  [pool drain];
}

void xenon::graphics::XenonSyphonClient::bind() {
  NSAutoreleasePool* pool = [[NSAutoreleasePool alloc] init];

  if(bSetup) {
    
    [static_cast<SyphonNameboundClient*>(mClient) lockClient];
    SyphonClient *client = [static_cast<SyphonNameboundClient*>(mClient) client];
    
    latestImage = [client newFrameImageForContext:CGLGetCurrentContext()];
    NSSize texSize = [static_cast<SyphonImage*>(latestImage) textureSize];
    
    // we now have to manually make our ofTexture's ofTextureData a proxy to our SyphonImage
    mTex.texData.textureID = [static_cast<SyphonImage*>(latestImage) textureName];
    mTex.texData.textureTarget = GL_TEXTURE_RECTANGLE_ARB;
    mTex.texData.width = texSize.width;
    mTex.texData.height = texSize.height;
    mTex.texData.tex_w = texSize.width;
    mTex.texData.tex_h = texSize.height;
    mTex.texData.tex_u = texSize.width;
    mTex.texData.tex_t = texSize.height;
    mTex.texData.glType = GL_RGBA;
    mTex.texData.pixelType = GL_UNSIGNED_BYTE;
    mTex.texData.bFlipTexture = NO;
    mTex.texData.bAllocated = YES;
    
    mTex.bind();
  }
  [pool drain];

}

// FOR DEBUGGING:
//
// void xenon::graphics::XenonSyphonClient::draw() {
//   NSAutoreleasePool* pool = [[NSAutoreleasePool alloc] init];

//   if(bSetup) {
    
//     [static_cast<SyphonNameboundClient*>(mClient) lockClient];
//     SyphonClient *client = [static_cast<SyphonNameboundClient*>(mClient) client];

//     latestImage = [client newFrameImageForContext:CGLGetCurrentContext()];
//     NSSize texSize = [static_cast<SyphonImage*>(latestImage) textureSize];
//     NSLog(@"DRAWING: %f %f\n", texSize.width, texSize.height);
    
//     // we now have to manually make our ofTexture's ofTextureData a proxy to our SyphonImage
//     mTex.texData.textureID = [static_cast<SyphonImage*>(latestImage) textureName];
//     mTex.texData.textureTarget = GL_TEXTURE_RECTANGLE_ARB;
//     mTex.texData.width = texSize.width;
//     mTex.texData.height = texSize.height;
//     mTex.texData.tex_w = texSize.width;
//     mTex.texData.tex_h = texSize.height;
//     mTex.texData.tex_u = texSize.width;
//     mTex.texData.tex_t = texSize.height;
//     mTex.texData.glType = GL_RGBA;
//     mTex.texData.pixelType = GL_UNSIGNED_BYTE;
//     mTex.texData.bFlipTexture = NO;
//     mTex.texData.bAllocated = YES;
    
//     mTex.draw(0,0,1,1);

//     // glEnable(GL_TEXTURE_RECTANGLE_ARB);
//     // glBindTexture(GL_TEXTURE_RECTANGLE_ARB, [static_cast<SyphonImage*>(latestImage) textureName]);
//     // glBegin(GL_QUADS);
//     // glTexCoord2f(0.0, 0.0);                      glVertex3f(0.0, -0.5, 0.0);
//     // glTexCoord2f(0.0, texSize.height);           glVertex3f(0.0, 0.5, 0.0);
//     // glTexCoord2f(texSize.width, texSize.height); glVertex3f(1.0, 0.5, 0.0);
//     // glTexCoord2f(texSize.width, 0.0);            glVertex3f(1.0, -0.5, 0.0);
//     // glEnd();
//     // glDisable(GL_TEXTURE_RECTANGLE_ARB);
    
//     [static_cast<SyphonNameboundClient*>(mClient) unlockClient];
//     [static_cast<SyphonImage*>(latestImage) release];
//     latestImage = nil;
//   }
//   [pool drain];
// }

void xenon::graphics::XenonSyphonClient::unbind() {
  NSAutoreleasePool* pool = [[NSAutoreleasePool alloc] init];
    
  if(bSetup) {
    mTex.unbind();

    [static_cast<SyphonNameboundClient*>(mClient) unlockClient];
    [static_cast<SyphonImage*>(latestImage) release];
    latestImage = nil;
  }
  [pool drain];
}

void xenon::graphics::XenonSyphonClient::draw(float x, float y, float w, float h) {
  bind();
  mTex.draw(x, y, w, h);
  unbind();
}

void xenon::graphics::XenonSyphonClient::draw(float x, float y) {
  draw(x,y, mTex.texData.width, mTex.texData.height);
}

int xenon::graphics::XenonSyphonClient::getHeight() {
  if (bSetup)
    return mTex.getHeight();
  else 
    return 512;
}

int xenon::graphics::XenonSyphonClient::getWidth() {
  if (bSetup) 
    return mTex.getWidth();
  else
    return 512;
}

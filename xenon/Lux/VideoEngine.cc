#include <xenon/Lux/VideoEngine.h>
#include <xenon/Graphics/Texture.h>

#ifdef __APPLE__
#include <OpenGL/gl.h>
#include <OpenGL/glu.h>
#include <AGL/agl.h>
#else // Linux
#include <GL/gl.h>
#include <GL/glu.h>
#endif

/*	Create checkerboard texture	*/
#define	checkImageWidth 64
#define	checkImageHeight 64
static GLubyte checkImage[checkImageHeight][checkImageWidth][4];
static GLuint texName;

xenon::graphics::Texture testTexture;

void makeCheckImage(void)
{
   int i, j, c;
    
   for (i = 0; i < checkImageHeight; i++) {
      for (j = 0; j < checkImageWidth; j++) {
         c = ((((i&0x8)==0)^((j&0x8))==0))*255;
         checkImage[i][j][0] = (GLubyte) c;
         checkImage[i][j][1] = (GLubyte) c;
         checkImage[i][j][2] = (GLubyte) c;
         checkImage[i][j][3] = (GLubyte) 255;
      }
   }
}

lux::VideoEngine::VideoEngine(std::string application_name, std::string server_name) {
  m_syphon_client.setup();
  m_syphon_client.setApplicationName(application_name);
  m_syphon_client.setServerName(server_name);
}

void lux::VideoEngine::draw_gl() {

  glClearColor(0.0,0.0,0.1,1.0);
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
  m_syphon_client.draw(-0.5,-0.5,1.0,1.0);
}

void lux::VideoEngine::resize_gl(int width, int height) {
  if (width == 0 || height == 0) {
    width = 512;  height = 512;
  }
  int min = width > height ? height : width;
  //  std::cout << "VIEWPORT: " << (width-min)/2 << " " << (height-min)/2 << " " << min << " " << min << "\n";
  glViewport((width-min)/2, (height-min)/2, min, min);
  glMatrixMode(GL_PROJECTION);
  glLoadIdentity();
  glOrtho (-1, 1, -1, 1, -1, 1);
  glMatrixMode(GL_MODELVIEW);
}



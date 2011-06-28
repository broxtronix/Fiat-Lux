#include <xenon/Lux/VideoEngine.h>
#include <xenon/Graphics/Texture.h>
#include <xenon/Core/Log.h>
#include <xenon/Core/Time.h>

#ifdef __APPLE__
#include <OpenGL/gl.h>
#include <OpenGL/glu.h>
#include <AGL/agl.h>
#else // Linux
#include <GL/gl.h>
#include <GL/glu.h>
#endif

// OpenCV
#include <opencv/cv.h>
#include <opencv/highgui.h>

// Libol
extern "C" { 
  #include "libol.h"
}


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
#ifdef __APPLE__
  m_syphon_client.setup();
  m_syphon_client.setApplicationName(application_name);
  m_syphon_client.setServerName(server_name);
#endif

  m_record_frame_number = 0;

  m_contour_threshold = 0.2;
  m_contour_blur_sigma =  1.5;
  m_contour_min_area = 10;
  m_contour_max_area = 640*480;
  m_contour_num_considered = 100;
  m_contour_mode = CV_RETR_EXTERNAL;
  m_contour_method = CV_CHAIN_APPROX_SIMPLE;
  m_edge_detection_mode = 0;  // 0 == THRESHOLD, 1 == ADAPTIVE_THRESHOLD, 2 == CANNY

  m_viewport_width = 512;
  m_viewport_height = 512;
  m_aspect = 1.0;

  m_initialized = false;
}

void lux::VideoEngine::initialize_gl() {

  glGenFramebuffersEXT(1, &m_framebuffer0);
  glGenTextures(1, &m_framebuffer_texture0);
  glBindTexture(GL_TEXTURE_2D, m_framebuffer_texture0);
  glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR);
  glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR);
  glBindTexture(GL_TEXTURE_2D, 0);

  m_initialized = true;
}

void lux::VideoEngine::resize_gl(int width, int height) {
  if (width == 0 || height == 0) {
    m_viewport_width = 512;  m_viewport_height = 512;
    m_aspect = 1;
  }

  m_viewport_width = width;
  m_viewport_height = height;
  m_aspect = float(width) / height;

  m_framebuffer_width = 512;
  m_framebuffer_height = 512;

  glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, m_framebuffer0);
  glBindTexture(GL_TEXTURE_2D, m_framebuffer_texture0);
  glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, 
               m_framebuffer_width, m_framebuffer_height, 
               0, GL_BGRA, GL_UNSIGNED_BYTE, NULL);
  glFramebufferTexture2DEXT(GL_FRAMEBUFFER_EXT, GL_COLOR_ATTACHMENT0_EXT,
                            GL_TEXTURE_2D, m_framebuffer_texture0, 0);

  // Make sure that the framebuffer is correctly configured.
  GLenum status = glCheckFramebufferStatusEXT(GL_FRAMEBUFFER_EXT);
  if (status != GL_FRAMEBUFFER_COMPLETE_EXT)
    xenon_throw(xenon::LogicErr() << "VideoEngine::resizeGL() - could not initialize framebuffer.\n");
  glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, 0);

  glClearColor(0.0, 0.0, 0.0, 0.0);
  glClearDepth(1.0);
  glDepthFunc(GL_LESS);
  glDisable(GL_DEPTH_TEST);
  glEnable(GL_BLEND);
  glBlendFunc (GL_SRC_ALPHA, GL_ONE);
}

// ---------------------------------------------------------------------------
//                             DRAWING ROUTINES
// ---------------------------------------------------------------------------

template <class T>
bool compareCvContours(T a, T b) {
  if (a.size() > b.size())
    return true;
  else 
    return false;
}


void lux::VideoEngine::draw_gl() {

  if (!m_initialized)
    return;

  // FIRST: DRAW INTO THE RENDER BUFFER (AT LOW RES) AND READ OUT THE PIXELS

  glViewport(0, 0, m_viewport_width, m_viewport_height);
  glMatrixMode(GL_PROJECTION);
  glLoadIdentity();
  glOrtho (-m_aspect, m_aspect, -1.0, 1.0, -1.0, 1.0);
  glMatrixMode(GL_MODELVIEW);
  glLoadIdentity();

  glClearColor(0.0,0.0,0.1,1.0);
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
#ifdef __APPLE__
  glColor4f(1.0, 1.0, 1.0, 1.0);
  m_syphon_client.draw(-0.5,-0.5,1.0,1.0);
#endif

  // SECOND: DRAW INTO THE RENDER BUFFER (AT LOW RES) AND READ OUT THE PIXELS
  
  glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, m_framebuffer0);
  glDrawBuffer(GL_COLOR_ATTACHMENT0_EXT);
  glReadBuffer(GL_COLOR_ATTACHMENT0_EXT);

  glViewport(0, 0, m_framebuffer_width, m_framebuffer_height);
  glMatrixMode(GL_PROJECTION);
  glLoadIdentity();
  glOrtho (-1.0, -1.0, -1.0, 1.0, -1.0, 1.0);
  glMatrixMode(GL_MODELVIEW);
  glLoadIdentity();

  glClearColor(0.0,0.0,0.1,1.0);
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
#ifdef __APPLE__
  // float syphon_aspect = m_syphon_client.getWidth() / m_syphon_client.getHeight();
  // std::cout << "Syphon aspect = " << syphon_aspect << "\n";
  //  m_syphon_client.draw(-1.0,-1.0/syphon_aspect,2.0,2.0/syphon_aspect);
  glColor4f(1.0, 1.0, 1.0, 1.0);
  m_syphon_client.draw(-1.0,-1.0,2.0,2.0);
#endif

  // Read back the image so that we can find its contours.
  cv::Mat image(m_framebuffer_height, m_framebuffer_width, CV_8UC4);
  glReadPixels(0,0,m_framebuffer_width, m_framebuffer_height,
               GL_BGRA, GL_UNSIGNED_BYTE, image.ptr());

  // Optionally, save frame to disk
  std::ostringstream ostr;    
  ostr << "/tmp/lux_frame_";
  for (int i = 1; i < 5; ++i) {
    if (int(m_record_frame_number / powf(10,i)) == 0) {
      ostr << "0";
    }
  }
  ostr << m_record_frame_number << ".jpg";
  //  std::cout << "Recording grayscale frame: " << ostr.str() << "\n";
  //  cv::imwrite(ostr.str(), image);

  glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, 0);

  // FINALLY : EXTRACT CONTOURS

  // Compute the threhold image.
  cv::Mat grayscale_image;
  cvtColor(image, grayscale_image, CV_RGB2GRAY);
  cv::GaussianBlur(grayscale_image, grayscale_image, cv::Size(11,11), m_contour_blur_sigma, m_contour_blur_sigma);
  
  // Average with the previous frame to smooth out the contours
  m_contour_frame_smoothing = 1.0;
  cv::Mat avg_image;
  if (m_previous_image.rows == grayscale_image.rows && m_previous_image.cols == grayscale_image.cols) {
    avg_image = m_contour_frame_smoothing * grayscale_image + (1-m_contour_frame_smoothing) * m_previous_image;
    m_previous_image = avg_image;
  } else {
    avg_image = grayscale_image;
    m_previous_image = grayscale_image;
  }

  if (m_edge_detection_mode == 1) { // ADAPTIVE_THRESHOLD
    cv::adaptiveThreshold(avg_image, avg_image, 255, cv::ADAPTIVE_THRESH_GAUSSIAN_C, 
                          cv::THRESH_BINARY, 3, m_contour_threshold * 2 - 1.0);
  } else if (m_edge_detection_mode == 2) { // CANNY
    cv::Canny(avg_image, avg_image, 0.5 * 255 * m_contour_threshold, 255 * m_contour_threshold);
  } else {                          // THRESHOLD
    cv::threshold(avg_image, avg_image, 255 * m_contour_threshold, 255, cv::THRESH_BINARY);
  }
  //  cv::imwrite(ostr.str(), avg_image);
  
  // OpenCV clobbers the contour image, so we make a copy of it here.
  std::vector<std::vector<cv::Point> > raw_contours;
  cv::findContours(avg_image, raw_contours, m_contour_mode, m_contour_method);

  // Sort contours from longest to shortest
  std::sort(raw_contours.begin(), raw_contours.end(), compareCvContours<std::vector<cv::Point> >);

  // put the contours from the linked list, into an array for sorting
  std::cout << "Processing " << raw_contours.size() << " raw contours.\n";
  std::vector<std::vector<cv::Point> >::iterator iter = raw_contours.begin();
  while (iter != raw_contours.end()) {
    //    std::cout << "\tRaw contour: " << iter->size() << "\n";

    float area = cv::contourArea(cv::Mat(*iter));
    if( (area > m_contour_min_area) && (area < m_contour_max_area) ) {

      // Rescale the contours 
      std::vector<xenon::Vector2> contour_2f;
      for (int i = 0; i < iter->size(); ++i) {
        xenon::Vector2 p;
        p[0] = float((*iter)[i].x) / m_framebuffer_width * 2.0 - 1.0;
        p[1] = float((*iter)[i].y) / m_framebuffer_height * 2.0 - 1.0;
        if (abs(p[0]) > 0.1 && abs(p[1]) > 0.1 && i % 1 == 0)
          contour_2f.push_back(p);
      }

      // And add it to the final contour list
      xenon::Mutex::Lock lock(m_mutex);
      if (m_contours_to_draw.size() < m_contour_num_considered)
        m_contours_to_draw.push_back(contour_2f);
    }
    ++iter;
  }

  // DRAW THE CONTOURS


  // xenon::xenon_out() << "Frame " << m_record_frame_number << ": " << m_contours_to_draw.size() << " contours.\n";
  // xenon::xenon_out() << "minarea: " << m_contour_min_area << "  max area " << m_contour_max_area << "   " 
  //                    << " contours to draw: " << m_contour_num_considered << "\n";
  glViewport(0, 0, m_viewport_width, m_viewport_height);
  glMatrixMode(GL_PROJECTION);
  glLoadIdentity();
  glOrtho (-m_aspect, m_aspect, -1.0, 1.0, -1.0, 1.0);
  glMatrixMode(GL_MODELVIEW);
  glLoadIdentity();
  glScalef(0.5,0.5,1.0);
  //  glTranslatef(1.0,0.0,0.0);
  glLineWidth(2.0);
  glColor4f(0.0, 1.0, 0.0, 1.0);
  for (int c = 0; c < m_contours_to_draw.size(); ++c) {
    // xenon::xenon_out() << "\tCount " << c << " has " << m_contours_to_draw[c].size() << "\n";
    glBegin(GL_LINE_LOOP);
    for (int cc = 0;  cc < m_contours_to_draw[c].size(); ++cc) {
      glVertex3f(m_contours_to_draw[c][cc][0], m_contours_to_draw[c][cc][1], 0);
      //   std::cout << "\t\t" << m_contours_to_draw[c][cc] << "\n";
    }
    glEnd();
  }
  m_record_frame_number++;

  
}


void lux::VideoEngine::draw_lasers() {  

  olLoadIdentity3();
  olLoadIdentity();
  olPerspective(60, 1, 1, 100);
  olTranslate3(0, 0, -3);
  
  olColor3(0.0,1.0,0.0);

  xenon::Mutex::Lock lock(m_mutex);
  //  std::cout << "there are " << m_contours_to_draw.size() << "\n";

  
  for (int c = 0; c < m_contours_to_draw.size(); ++c) {
    //    std::cout << "Drawing contour " << c << " with " << m_contours_to_draw[c].size() << " points\n";
    if (m_contours_to_draw[c].size() > 5) {
      olBegin(OL_POINTS);
      for (int cc = 0; cc < m_contours_to_draw[cc].size(); ++cc) {
        //      std::cout << "\t" << m_contours_to_draw[c][cc][0] << "  " << m_contours_to_draw[c][cc][1] << "\n";
        //        olVertex3(m_contours_to_draw[c][cc][0], m_contours_to_draw[c][cc][1], -1);
      }
      olEnd();
    }
  }
  m_contours_to_draw.clear();
}



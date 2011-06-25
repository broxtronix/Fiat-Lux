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
}

void lux::VideoEngine::draw_gl() {

  glClearColor(0.0,0.0,0.1,1.0);
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
#ifdef __APPLE__
  m_syphon_client.draw(-0.5,-0.5,1.0,1.0);
#endif

  std::ostringstream ostr;    
  ostr << "/tmp/lux_frame_";
  for (int i = 1; i < 5; ++i) {
    if (int(m_record_frame_number / powf(10,i)) == 0) {
      ostr << "0";
    }
  }
  ostr << m_record_frame_number << ".jpg";
  //  std::cout << "Recording frame: " << ostr.str() << "\n";

  cv::Mat image(m_viewport_height, m_viewport_width, CV_8UC1);
  glReadPixels(0,0,m_viewport_width, m_viewport_height,
               GL_LUMINANCE, GL_UNSIGNED_BYTE, image.ptr());

  // Compute the threhold image.
  //float thresh = pe_script_engine().get_parameter("vision_threshold");
  // cv::Mat grayscale_image;
  // cv::cvtColor(image, grayscale_image, CV_BGR2GRAY);
  cv::GaussianBlur(image, image, cv::Size(7,7), m_contour_blur_sigma, m_contour_blur_sigma);
  cv::threshold(image, image, 255 * m_contour_threshold, 255, cv::THRESH_BINARY);

  std::vector<std::vector<cv::Point> > raw_contours;
  
  // OpenCV clobbers the contour image, so we make a copy of it here.
  cv::Mat contour_image = image.clone();
  cv::findContours(contour_image, raw_contours, m_contour_mode, m_contour_method);

  // put the contours from the linked list, into an array for sorting
  std::vector<std::vector<cv::Point> >::iterator iter = raw_contours.begin();
  while (iter != raw_contours.end()) {

    float area = cv::contourArea(cv::Mat(*iter));
    if( (area > m_contour_min_area) && (area < m_contour_max_area) ) {

      // Rescale the contours 
      std::vector<xenon::Vector2> contour_2f;
      std::vector<cv::Point>::iterator contour_iter = iter->begin();
      while(contour_iter != iter->end()) {
        xenon::Vector2 p;
        p[0] = float(contour_iter->x) / m_viewport_width * 2.0 - 1.0;
        p[1] = float(contour_iter->y) / m_viewport_height * 2.0 - 1.0;
        contour_2f.push_back(p);
        ++contour_iter;
      }

      // And add it to the final contour list
      xenon::Mutex::Lock lock(m_mutex);
      if (m_contours_to_draw.size() < m_contour_num_considered)
        m_contours_to_draw.push_back(contour_2f);
    }
    ++iter;
  }

  //  cv::imwrite(ostr.str(), image);
  //  xenon::xenon_out() << "Frame " << m_record_frame_number << ": " << m_contours_to_draw.size() << " contours.\n";
  // for (int c = 0; c < contours.size(); ++c) {
  //   xenon::xenon_out() << "\tCount " << c << " has " << contours[c].size() << "\n";
  //   for (int cc = 0;  cc < contours[c].size(); ++cc) {
  //     std::cout << "\t\t" << contours[c][cc] << "\n";
  //   }
  // }
  m_record_frame_number++;
}

void lux::VideoEngine::draw_lasers() {
  

  olLoadIdentity3();
  olLoadIdentity();
  olPerspective(60, 1, 1, 100);
  olTranslate3(0, 0, -3);
  
  olColor3(0.0,1.0,0.0);

  // for(int i=0; i<2; i++) {
  //   if (i == 1)
  //     olColor3(0.0,1.0,0.0);
  //   else
  //     olColor3(0.0,1.0,0.0);
    
  //   olScale3(0.6, 0.6, 0.6);
    
  //   olRotate3Z(xenon::xenon_time() * M_PI * 0.1);
  //   olRotate3Y(xenon::xenon_time() * M_PI * 0.8);
  //   olRotate3X(xenon::xenon_time() * M_PI * 0.73);
    
  //   olBegin(OL_LINESTRIP);
  //   olVertex3(-1, -1, -1);
  //   olVertex3( 1, -1, -1);
  //   olVertex3( 1,  1, -1);
  //   olVertex3(-1,  1, -1);
  //   olVertex3(-1, -1, -1);
  //   olVertex3(-1, -1,  1);
  //   olEnd();

  //   olBegin(OL_LINESTRIP);
  //   olVertex3( 1,  1,  1);
  //   olVertex3(-1,  1,  1);
  //   olVertex3(-1, -1,  1);
  //   olVertex3( 1, -1,  1);
  //   olVertex3( 1,  1,  1);
  //   olVertex3( 1,  1, -1);
  //   olEnd();
    
  //   olBegin(OL_LINESTRIP);
  //   olVertex3( 1, -1, -1);
  //   olVertex3( 1, -1,  1);
  //   olEnd();
    
  //   olBegin(OL_LINESTRIP);
  //   olVertex3(-1,  1,  1);
  //   olVertex3(-1,  1, -1);
  //   olEnd();
  // }

  xenon::Mutex::Lock lock(m_mutex);
  //  std::cout << "there are " << m_contours_to_draw.size() << "\n";

  for (int c = 0; c < m_contours_to_draw.size(); ++c) {
    //    std::cout << "Drawing contour " << c << "\n";
    olBegin(OL_LINESTRIP);
    for (int cc = 0; cc < m_contours_to_draw[cc].size(); ++cc) {
      //      std::cout << "\t" << m_contours_to_draw[c][cc][0] << "  " << m_contours_to_draw[c][cc][1] << "\n";
    
      olVertex3(m_contours_to_draw[c][cc][0], m_contours_to_draw[c][cc][1], -1);
    }
    olEnd();
  }
  m_contours_to_draw.clear();
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

  m_viewport_width = width;
  m_viewport_height = height;
}



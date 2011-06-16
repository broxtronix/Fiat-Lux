#include "magicscope.h"

#define _BSD_SOURCE

#include <sys/time.h>
#include <stdio.h>
#include <errno.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <iostream.h> 
using namespace std;

#include <jack/jack.h>

#include <stdint.h>
#include <math.h>

typedef jack_default_audio_sample_t sample_t;
typedef jack_nframes_t nframes_t;

nframes_t rate;

sample_t max_size = 1.0f;
sample_t min_size = 0.2f;
sample_t boost = 8;

//float w = 110 * (2*M_PI);
float w = 523.251131f / 4.0f * (2*M_PI) / 1;
float pos = 0.0f;

#define MAX(a,b) (((a)<(b))?(b):(a))
#define MIN(a,b) (((a)>(b))?(b):(a))


MagicScope::MagicScope(std::string name) : m_sample_rate(0), m_buffer_size(0) {
  if ((m_client = jack_client_new (name.c_str())) == 0) {
    fprintf(stderr,"oh shit");
    exit(0);
//        xenon_throw( LogicErr() << "Failed to start MagicScope -- could not iniitialize Jack.  Is the Jack server running?" );
  }

  // set jack process callbacks
  jack_set_process_callback (m_client, MagicScope::static_process_callback, this);
  jack_set_buffer_size_callback (m_client, MagicScope::static_buffer_size_callback, this);
  jack_set_sample_rate_callback (m_client, MagicScope::static_sample_rate_callback, this);
  jack_on_shutdown (m_client, MagicScope::static_shutdown_callback, this);

  // register jack ports
	m_in_l = jack_port_register (m_client, "in_l", JACK_DEFAULT_AUDIO_TYPE, JackPortIsInput, 0);
	m_in_r = jack_port_register (m_client, "in_r", JACK_DEFAULT_AUDIO_TYPE, JackPortIsInput, 0);
	m_out_x = jack_port_register (m_client, "out_x", JACK_DEFAULT_AUDIO_TYPE, JackPortIsOutput, 0);
	m_out_y = jack_port_register (m_client, "out_y", JACK_DEFAULT_AUDIO_TYPE, JackPortIsOutput, 0);
	m_out_w = jack_port_register (m_client, "out_w", JACK_DEFAULT_AUDIO_TYPE, JackPortIsOutput, 0);

	if (jack_activate (m_client)) {
		fprintf (stderr, "cannot activate client");
//  		return 1;
	}

  // connect jack ports
  cout << jack_connect(m_client, "magicscope:out_x","simulator:in_x") << "\n";
  cout << jack_connect(m_client, "magicscope:out_y","simulator:in_y") << "\n";
  cout << jack_connect(m_client, "magicscope:out_w","simulator:in_g") << "\n";
//  cout << jack_connect(m_client, "system:capture_1","magicscope:in_l") << "\n";
//  cout << jack_connect(m_client, "system:capture_2","magicscope:in_r") << "\n";
  cout << jack_connect(m_client, "Soundflowerbed:out1","magicscope:in_l") << "\n";
  cout << jack_connect(m_client, "Soundflowerbed:out2","magicscope:in_r") << "\n";

  // set time values
  interval = 100;
  gettimeofday(&starttime, NULL);
  nextSwitch = 0;

/*  
  sample_t currentWave [512];
  sample_t nextWave [512];
	for (int frm = 0; frm < 512; frm++) {
    currentWave[frm] = 0;
    nextWave[frm] = 0;
  }
  */
}

MagicScope::~MagicScope() {
  jack_client_close (m_client);
}


int MagicScope::process_callback (nframes_t nframes)
{
  // fetch sample buffers from jack
	sample_t *i_l = (sample_t *) jack_port_get_buffer (m_in_l, nframes);
	sample_t *i_r = (sample_t *) jack_port_get_buffer (m_in_r, nframes);
	sample_t *o_x = (sample_t *) jack_port_get_buffer (m_out_x, nframes);
	sample_t *o_y = (sample_t *) jack_port_get_buffer (m_out_y, nframes);
	sample_t *o_w = (sample_t *) jack_port_get_buffer (m_out_w, nframes);

  // determine elapsed time
  struct timeval now;
  gettimeofday(&now, NULL);
  long seconds  = now.tv_sec  - starttime.tv_sec;
  long useconds = now.tv_usec - starttime.tv_usec;
  long timeElapsed = ((seconds) * 1000 + useconds/1000.0) + 0.5;
  printf("Elapsed time: %ld milliseconds\n", timeElapsed);

	nframes_t frm;

  if (timeElapsed > nextSwitch){
    printf("Switching\n");
    // switch shapes
    currentWave = nextWave;
  	for (frm = 0; frm < nframes; frm++) {
      sample_t l = *i_l++;
      sample_t r = *i_r++;
      printf("Frame: %4d,  Left: %.6f,  Right:%.6f\n",frm,l,r);
      nextWave[frm] = (l + r) / 2;
  	}
    nextSwitch += interval;
  }
  
  float fracComplete = (timeElapsed - (nextSwitch - interval)) / interval;
  
  printf("Frac Complete: %.3f\n",fracComplete);

  // old "circlescope" code
	for (frm = 0; frm < nframes; frm++) {
		sample_t val = nextWave[frm];

		val *= boost;
		val = MAX(MIN(val,1.0f),-1.0f);
		val = val * 0.5f + 0.5f;
		val *= (max_size - min_size);
		val += min_size;

		*o_w++ = 1.0f;
		*o_x++ = cosf(pos) * val;
		*o_y++ = sinf(pos) * val;

		pos += w / rate;
		while(pos >= (2*M_PI)) {
			pos -= (2*M_PI);
		}
	}

	return 0;
}

int MagicScope::buffer_size_callback (nframes_t nframes)
{
	printf ("the maximum buffer size is now %u\n", nframes);
	return 0;
}

int MagicScope::sample_rate_callback (nframes_t nframes)
{
	rate = nframes;
	printf ("Sample rate: %u/sec\n", nframes);
	return 0;
}

void MagicScope::shutdown_callback ()
{
	exit (1);
}

int main (int argc, char** argv) {
  MagicScope mc ("magicscope");
  while(1){ sleep(1); }
}

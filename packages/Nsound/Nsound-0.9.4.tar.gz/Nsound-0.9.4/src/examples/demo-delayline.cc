//-----------------------------------------------------------------------------
//
//  $Id: bebot.cc 887 2015-04-26 02:49:19Z weegreenblobbie $
//
//-----------------------------------------------------------------------------

#include <Nsound/NsoundAll.h>

#include <iostream>

using std::cout;
using std::cerr;
using std::endl;

using namespace Nsound;

int
main(void)
{
    AudioStream as1("california.wav");

    float64 sr = as1.getSampleRate();
    float64 dur = as1.getDuration();

    Wavefile::setDefaultSampleRate(sr);

    Generator gen(sr);

    DelayLine dl(sr, dur);

    Buffer dt_line = gen.drawLine(dur, 0.01, 0.25);

    Buffer out = dl.delay(as1[0], dt_line);

    out += as1[0];

    out.normalize();
    out *= 0.666;

    out << gen.silence(0.5);

    out >> "dt-cali.wav";

    return 0;
}

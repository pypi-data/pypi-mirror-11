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


AudioStream
stretch_to(const AudioStream & x, float64 new_duration)
{
    float64 x_dur = x.getDuration();

    float64 ratio = new_duration / x_dur;

    Stretcher st(x.getSampleRate());

    st.showProgress(true);

    return st.timeShift(x, ratio);
}


int
main(void)
{
    AudioStream x0("california.wav");

    float64 dur = x0.getDuration();

    AudioStream x1 = stretch_to(x0, 1.15 * dur);
    AudioStream x2 = stretch_to(x0, 1.30 * dur);

    // The longest one is x2, so add all of them to x2.

    cout
        << "x2.getLength() = " << x2.getLength() << "\n"
        << "x1.getLength() = " << x1.getLength() << "\n"
        << "x0.getLength() = " << x0.getLength() << "\n";

    x2.add(x0, 1.30 * dur - dur);
    x2.add(x1, 1.15 * dur - dur);

    for(uint32 i = 0; i < x0.getSampleRate() / 2.0; ++i)
    {
        x2 << 0.0;
    }

    x2.normalize();
    x2 *= 0.666;

    cout << "x2.getLength() = " << x2.getLength() << "\n";

    x2 >> "demo-st.wav";

    return 0;
}

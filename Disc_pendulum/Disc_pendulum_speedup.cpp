/*Copyright (C) 2019 Yi-Fan Shyu
* 
* Permission is hereby granted, free of charge, to any person obtaining a copy
* of this software and associated documentation files (the "Software"), to deal
* in the Software without restriction, including without limitation the rights
* to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
* copies of the Software, and to permit persons to whom the Software is furnished
* to do so, subject to the following conditions:
* 
* The above copyright notice and this permission notice shall be included in all
* copies or substantial portions of the Software.
* 
* THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
* IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
* FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
* COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
* IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
* WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/

#include <iostream>
#include <cmath>
#include <cstring>
#include <sstream>
#include <iomanip>
#include "communicate.h"
#include "vectorOperation.h"
using namespace std;

bool trywrite(char write[])
{
	if(write_to_client(write))
		return true;
	else
	{
		close();
		cout << "server error " << GetLastError() << endl;
		return false;
	}
}

bool tryread(char read[])
{
	if(read_from_client(read))
		return true;
	else
	{
		close();
		cout << "client error " << GetLastError() << endl;
		return false;
	}
}

inline vec springForce(vec axis, const long double& k, const long double& Len)
{
	return -k * (axis.mag() - Len) * axis.norm();
}

inline vec damping(vec v, vec r)
{
	return -50 * (dot(v, r) / r.mag()) * r.norm();
}

int main()
{
	create();
	char mess[500] = {0};
	stringstream ss;
	long double dt = 0, m = 0, k = 0, Len = 0, posx = 0, posy = 0, posz = 0;
	vec w, ballpos, ballv, last_ballv, balla, stickpos, g;
	vec f_ballpos, f_ballv, last_f_ballv, f_balla, f_stickpos;
	
	tryread(mess);
	ss << mess;
	ss >> mess;
	if(!strcmp(mess, "init"))
		ss >> m >> k >> Len >> posy;
	else
		return 1;
	ss.str("");	ss.clear();
	stickpos = vec(0, posy, 0);
	f_stickpos = vec(0, posy, 0);
	
	tryread(mess);
	ss << mess;
	ss >> mess;
	if(!strcmp(mess, "start"))
	{
		ss >> posy;
		w = vec(0, posy, 0);
		ss >> posy >> dt;
		g = vec(0, posy, 0);
		ss >> posx >> posy >> posz;
		ballpos = vec(posx, posy, posz);
		ss >> posx >> posy >> posz;
		f_ballpos = vec(posx, posy, posz);
		ballv = cross(w, ballpos);
		balla = g + (springForce((ballpos-stickpos), k, Len) + damping(ballv, ballpos-stickpos)) / m;
		f_balla = g + (springForce((f_ballpos-f_stickpos), k, Len) + damping(f_ballv, f_ballpos-f_stickpos)) / m 
						- 2 * cross(w, f_ballv) - cross(w, cross(w, f_ballpos));
	}
	else
		return 1;
	ss.str("");	ss.clear();
	
	ss << scientific << setprecision(18);
	int count = 0;
	dt = 0.00001L;
	while(true)
	{
		if(!tryread(mess))	break;
		ss << mess;
		ss >> mess;
		if(strcmp(mess, "c"))
			continue;
		ss >> count;
		ss.str("");	ss.clear();
		
		for(int i = 0 ; i < 1000 ; i++)
		{
			last_ballv = ballv;
			last_f_ballv = f_ballv;
			ballv = ballv + balla * dt;//
			f_ballv = f_ballv + f_balla * dt;
			ballpos = ballpos + (ballv+last_ballv)/2 * dt;
			f_ballpos = f_ballpos + (f_ballv+last_f_ballv)/2 * dt;//
			balla = g + (springForce((ballpos-stickpos), k, Len) + damping(ballv, ballpos-stickpos)) / m;
			f_balla = g + (springForce((f_ballpos-f_stickpos), k, Len) + damping(f_ballv, f_ballpos-f_stickpos)) / m 
						- 2 * cross(w, f_ballv) - cross(w, cross(w, f_ballpos));
		}
		count++;
		ss << 'c' << '$' << count << '$' << ballpos.x << '$' << ballpos.y << '$' << ballpos.z << '$'
			<< f_ballpos.x << '$' << f_ballpos.y << '$' << f_ballpos.z << '$';
		ss >> mess;
		while(!trywrite(mess));
		ss.str("");	ss.clear();
	}
	close();
}

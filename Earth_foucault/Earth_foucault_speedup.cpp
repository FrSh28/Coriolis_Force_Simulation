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
#define pi 3.14159265358979323846L

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

inline vec gravity(vec distance)
{
	return (-5158707301747.944L / distance.mag()) * distance.norm();
	//(9.80665 * (3600)^2 / 1000) * (6371)^2
}

inline vec springForce(vec axis, const long double& k, const long double& Len)
{
	return -k * (axis.mag() - Len) * axis.norm();
}

inline vec damping(vec v, vec r)
{
	return -5000 * (dot(v, r) / r.mag()) * r.norm();
}

int main()
{
	create();
	char mess[500] = {0};
	stringstream ss;
	long double dt = 0, m = 0, k = 0, Len = 0, posx = 0, posy = 0, posz = 0;
	vec w, ballpos, ballv, balla, stickpos;
	vec f_ballpos, f_ballv, f_balla, f_stickpos;
	
	tryread(mess);
	ss << mess;
	ss >> mess;
	if(!strcmp(mess, "init"))
		ss >> m >> k >> Len;
	else
		return 1;
	ss.str("");	ss.clear();
	
	tryread(mess);
	ss << mess;
	ss >> mess;
	if(!strcmp(mess, "start"))
	{
		ss >> posy >> dt;
		w = vec(0, posy, 0);
		ss >> posx >> posy >> posz;
		ballpos = vec(posx, posy, posz);
		ballv = cross(w, ballpos);
		ss >> posx >> posy >> posz;
		f_stickpos = vec(posx, posy, posz);
	}
	else
		return 1;
	ss.str("");	ss.clear();
	
	ss << scientific << setprecision(18);
	int count = 0;
	dt = 0.000001L;
	while(true)
	{
		if(!tryread(mess))	break;
		ss << mess;
		ss >> mess;
		if(strcmp(mess, "c"))
			continue;
		ss >> count;
		ss >> posx >> posy >> posz;
		ballpos = vec(posx, posy, posz);
		ss >> posx >> posy >> posz;
		stickpos = vec(posx, posy, posz);
		ss >> posx >> posy >> posz;
		f_ballpos = vec(posx, posy, posz);
		ss.str("");	ss.clear();
		balla = gravity(ballpos) + (springForce((ballpos-stickpos), k, Len) + damping(ballv, ballpos-stickpos)) / m;
		f_balla = gravity(f_ballpos) + (springForce((f_ballpos-f_stickpos), k, Len) + damping(f_ballv, f_ballpos-f_stickpos))/ m 
					- 2 * cross(w, f_ballv) - cross(w, cross(w, f_ballpos));
		
		for(int i = 0 ; i < 1000 ; i++)
		{
			ballv = ballv + balla * dt;//
			f_ballv = f_ballv + f_balla * dt;
			ballpos = ballpos + ballv * dt;
			f_ballpos = f_ballpos + f_ballv * dt;//
			stickpos = stickpos + cross(w, stickpos) * dt;
			balla = gravity(ballpos) + (springForce((ballpos-stickpos), k, Len) + damping(ballv, ballpos-stickpos)) / m;
			f_balla = gravity(f_ballpos) + (springForce((f_ballpos-f_stickpos), k, Len) + damping(f_ballv, f_ballpos-f_stickpos))/ m 
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

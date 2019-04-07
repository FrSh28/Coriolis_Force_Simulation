/*Copyright (C) 2018 Yi-Fan Shyu
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

class vec{
	public:
	long double x;
	long double y;
	long double z;
	
	vec():x(0), y(0), z(0)
	{}
	vec(long double a, long double b, long double c):x(a), y(b), z(c)
	{}
};

inline vec operator+(vec v1, vec v2)
{
	return vec(v1.x+v2.x, v1.y+v2.y, v1.z+v2.z);
}

inline vec operator-(vec v1, vec v2)
{
	return vec(v1.x-v2.x, v1.y-v2.y, v1.z-v2.z);
}

inline vec operator*(vec v, const long double& n)
{
	return vec(v.x*n, v.y*n, v.z*n);
}

inline vec operator/(vec v, const long double& n)
{
	return vec(v.x/n, v.y/n, v.z/n);
}

inline vec cross(vec v1, vec v2)
{
	return vec((v1.y*v2.z - v1.z*v2.y), (v1.z*v2.x - v1.x*v2.z), (v1.x*v2.y - v1.y*v2.x));
}

inline long double dot(vec v1, vec v2)
{
	return v1.x*v2.x + v1.y*v2.y + v1.z*v2.z;
}

inline long double mag(vec v)
{
	return sqrt(v.x*v.x + v.y*v.y + v.z*v.z);
}

inline vec norm(vec v)
{
	return v / mag(v);
}

inline vec springForce(vec axis, long double k, long double Len)
{
	return norm(axis) * -k * (mag(axis) - Len);
}

inline vec damping(vec v, vec r)
{
	return norm(r) * dot(v, r) / mag(r) * -50;
}

int main()
{
	create();
	char mess[500] = {0};
	stringstream ss;
	long double dt = 0, m = 0, k = 0, Len = 0, posx = 0, posy = 0, posz = 0;
	vec w, ballpos, ballv, balla, stickpos, g(0, -980.665, 0);
	vec f_ballpos, f_ballv, f_balla, f_stickpos;
	
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
		ss >> posy >> dt;
		w = vec(0, posy, 0);
		ss >> posx >> posy >> posz;
		ballpos = vec(posx, posy, posz);
		ss >> posx >> posy >> posz;
		f_ballpos = vec(posx, posy, posz);
		ballv = (f_ballpos-ballpos) / dt;
		ss >> posx >> posy >> posz;
		ballpos = vec(posx, posy, posz);
		ss >> posx >> posy >> posz;
		f_ballpos = vec(posx, posy, posz);
		balla = g + (springForce((ballpos-stickpos), k, Len) + damping(ballv, ballpos-stickpos)) / m;
		f_balla =  g + (springForce((f_ballpos-f_stickpos), k, Len) + damping(f_ballv, f_ballpos-f_stickpos))/ m 
						- cross(w, f_ballv)*2 - cross(w, cross(w, f_ballpos));
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
			ballpos = ballpos + ballv * dt;
			f_ballpos = f_ballpos + f_ballv * dt;
			ballv = ballv + balla * dt;
			f_ballv = f_ballv + f_balla * dt;
			balla = g + (springForce((ballpos-stickpos), k, Len) + damping(ballv, ballpos-stickpos)) / m;
			f_balla = g + (springForce((f_ballpos-f_stickpos), k, Len) + damping(f_ballv, f_ballpos-f_stickpos))/ m 
						- cross(w, f_ballv)*2 - cross(w, cross(w, f_ballpos));
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

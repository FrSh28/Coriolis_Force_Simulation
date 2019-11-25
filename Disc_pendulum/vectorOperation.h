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
#include <cstdlib>
#include <cmath>
using namespace std;

class vec{
	public:
	long double x;
	long double y;
	long double z;
	
	vec() : x(0), y(0), z(0)	{}
	vec(const long double& a, const long double& b, const long double& c) : x(a), y(b), z(c)	{}

	inline vec operator+(const vec& v)
	{
		return vec(x+v.x, y+v.y, z+v.z);
	}

	inline vec operator-(const vec& v)
	{
		return vec(x-v.x, y-v.y, z-v.z);
	}

	friend vec operator*(const vec& v, const long double& n)
	{
		return vec(v.x*n, v.y*n, v.z*n);
	}

	friend vec operator*(const long double& n, const vec& v)
	{
		return vec(v.x*n, v.y*n, v.z*n);
	}

	inline vec operator/(const long double& n)
	{
		return vec(x/n, y/n, z/n);
	}

	inline long double mag()
	{
		return sqrt(x*x + y*y + z*z);
	}

	inline vec norm()
	{
		return *this / this->mag();
	}

	friend vec cross(const vec& v1, const vec& v2)
	{
		return vec((v1.y*v2.z - v1.z*v2.y), (v1.z*v2.x - v1.x*v2.z), (v1.x*v2.y - v1.y*v2.x));
	}

	friend long double dot(const vec& v1,const vec& v2)
	{
		return v1.x*v2.x + v1.y*v2.y + v1.z*v2.z;
	}
	
	friend ostream& operator<<(ostream& os, const vec& v)
	{
		os << '(' << v.x << ", " << v.y << ", " << v.z << ')';
		return os;
	}
};

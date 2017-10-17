/*
* \file 		: cateye_basic.h
* \brief
*
* Project		:
* Purpose		: 
* Author		: MagicPixel	cyg1030@foxmail.com
* Created		: 2017-10-16 12:11
* Modified by	:
*/
 
#ifndef CATEYE_BASIC_H
#define CATEYE_BASIC_H

#include <cmath>
#include <string>
#include <sstream>


#if (defined WIN32 || defined _WIN32 || defined WINCE)
#  define CATEYE_EXPORT __declspec(dllexport)
#else
#  define CATEYE_EXPORT
#endif

#ifndef PI
#  define PI             ((double)3.141592653589793238462643)
#endif


inline std::string to_str(double i)
{
	std::stringstream ss;
	ss << i;
	return ss.str();
}

#endif // CATEYE_BASIC_H

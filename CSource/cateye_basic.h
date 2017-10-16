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

#include <math>
#include <string>



#if (defined WIN32 || defined _WIN32 || defined WINCE)
#  define CATEYE_EXPORT __declspec(dllexport)
#else
#  define CATEYE_EXPORT
#endif

#ifndef PI
#  define PI             ((double)3.141592653589793238462643)
#endif

#endif // CATEYE_BASIC_H

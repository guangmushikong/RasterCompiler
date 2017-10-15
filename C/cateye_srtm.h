/*
* \file 		: cateye_srtm.h
* \brief
*
* Project		:
* Purpose		: 
* Author		: MagicPixel	cyg1030@foxmail.com
* Created		: 2017-10-14 23:11
* Modified by	:
*/
 
#ifndef CATEYE_SRTM_H
#define CATEYE_SRTM_H

#define CATEYE 

class CATEYE Srtm
{
/**

Lon/Lat:	WGS84 Datum

Tile:	 	Tile Image Coordinate System TopLeft
(0, 0) ----------------->
	|
	|
	|
	|
	|
	v
*/
public:
	Srtm();
	~Srtm();

	/**!brief	Return tile by given lon/lat in WGS84 Datum
	
	\param[in]	lon
	\param[in]	lat
	\param[out]	mx
	\param[out]	my

	return 		void
	*/
	void LonLatToTile(double lon, double lat, int& tx, int& ty);

	/**!brief	Return tile & pixles by given lon/lat in WGS84 Datum
	
	\param[in]	lon
	\param[in]	lat
	\param[out]	mx
	\param[out]	my

	return 		void
	*/
	void LonLatToTilePixels(double lon, double lat, int& tx, int& ty
		double& px, double& py);

protected:


}
#endif // CATEYE_SRTM_H

/*
* \file 		: cateye_mercator.h
* \brief
*
* Project		:
* Purpose		: more details see gdal2tiles.py 
* Author		: MagicPixel	cyg1030@foxmail.com
* Created		: 2017-10-14 14:07
* Modified by	:
*/
 
#ifndef CATEYE_MERCATOR_H
#define CATEYE_MERCATOR_H

#define MAXZOOMLEVEL = 32

#define CATEYE 

class CATEYE Mercator
{
/**

Meters :	Mercator EPSG:900913

Lon/Lat:	WGS84 Datum

Raster:	 	Tile Image Coordinate System TopLeft
(0, 0) ----------------->
	|
	|
	|
	|
	|
	v

Pixels:		Tile Image Coordinate System BottomLeft
	^
	|
	|
	|
	|
	|
(0, 0) ------------------>
*/
public:
	Mercator(int tileSize = 256);
	~Mercator();

	/**!brief	Converts given lon/lat in WGS84 Datum to XY in Spherical 
				Mercator EPSG:900913
	
	\param[in]	lon
	\param[in]	lat
	\param[out]	mx
	\param[out]	my

	return 		void
	*/
	void LonLatToMeters(double lon, double lat, double& mx, double& my);

	/**!brief	Return tile by given lon/lat in WGS84 Datum
	
	\param[in]	lon
	\param[in]	lat
	\param[in]	zoom
	\param[out]	mx
	\param[out]	my

	return 		void
	*/
	void LonLatToTile(double lon, double lat, int zoom, int& tx, int& ty);

	/**!brief	Converts XY point from Spherical Mercator EPSG:900913 to 
				lat/lon in WGS84 Datum
	
	\param[in]	mx
	\param[in]	my
	\param[out]	lon
	\param[out]	lat

	return 		void
	*/
	void MetersToLonLat(double mx, double my, double& lon, double& lat);

	/**!brief  	Converts pixel coordinates in given zoom level of pyramid to 
				EPSG:900913

	\param[in]	px 			pixel for x
	\param[in]	py 			pixel for y
	\param[in]	zoom 		zoom level
	\param[out]	mx 			meters for x
	\param[out]	my 			meters for y

	\return 	void
	*/
	void PixelsToMeters(double px, double py, int zoom, double& mx, double& my);

	/**!brief 	Converts EPSG:900913 to pyramid pixel coordinates in given zoom 
				level

	\param[in]	mx 			meters for x
	\param[in]	my 			meters for y
	\param[in]	zoom 		zoom level
	\param[out]	px 			pixels for x
	\param[out]	py 			pixels for y

	\return 	void
	*/
	void MetersToPixels(double mx, double my, int zoom, double& px, double& py);

	/**!brief 	Returns a tile covering region in given pixel coordinates
	
	\param[in]	px 			pixels for x
	\param[in]	py 			pixels for y
	\param[out]	tx 			tiles for x
	\param[out]	ty 			tiles for y

	\return 	void
	*/
	void PixelsToTile(double px, double py, int& tx, int& ty);

	/**!brief 	Move the origin of pixel coordinates to top-left corner

	\param[in]	px 			pixels for x
	\param[in] 	py 			pixels for y
	\param[in]	zoom 		zoom for level
	\param[out]	rx 			raster for x 
	\param[out] ry 			raster for y
	
	\return 	void
	*/
	void PixelsToRaster(double px, double py, int zoom, double& rx, double& ry);

	/**!brief 	Move the origin of pixel coordinates to bottom-left corner

	\param[in]	rx 			raster for x 
	\param[in] 	ry 			raster for y
	\param[in]	zoom 		zoom for level
	\param[out]	px 			pixels for x
	\param[out]	py 			pixels for y

	\return 	void
	*/
	void RasterToPixels(double rx, double ry, int zoom, double& px, double& py);

	/**!brief 	Returns tile for given mercator coordinates

	\param[in]	mx 			meters for x
	\param[in]	my			meters for y
	\param[in]	zoom 		zoom for level
	\param[out]	tx 			tile for x
	\param[out]	ty 			tile for y

	\return 	void 
	*/
	void MetersToTile(double mx, double my, int zoom, int& tx, int& ty);

	/**!brief 	Returns bounds of the given tile in EPSG:900913 coordinates

	\param[in]	tx 			tile for x
	\param[in]	ty			tile for y
	\param[in]	zoom 		zoom for level
	\param[out]	bounds[4]	bounds = [minx, miny, maxx, maxy]

	\return 	void
	*/
	void TileMetersBounds(double tx, double ty, int zoom, double bounds[4]);

	/**!brief 	Returns bounds of the given tile in lon/lat using WGS84 datum

	\param[in]	tx 			tile for x
	\param[in]	ty 			tile for y
	\param[in]	zoom 		zoom for level
	\param[out]	bounds 		bounds = [minLon, minLat, maxLon, maxLat]

	\return 	void
	*/
	void TileLatLonBounds(int tx, int ty, int zoom, double bounds[4]);


	/**!brief 	Returns tile bounds of the given  lon/lat bounds using WGS84 datum

	\param[in]	lonLatBounds 			[minLon, minLat, maxLon, maxLat]
	\param[in]	zoom 					zoom for level
	\param[out]	tileBounds 				[minTx, minTx, maxTx, maxTy]

	\return 	void
	*/
	void LonLatBoundsToTiles(double lonLatBounds[4], int zoom, int tileBounds[4]);

	/**!brief 	Resolution (meters/pixel) for given zoom level (measured at 
				Equator)

	\param[in]	zoom 		zoom for level

	\return 	double
	*/
	double Resolution(int zoom);

	/**!brief 	Maximal scaledown zoom of the pyramid closest to the pixelSize.

	\param[in]	pixelSize 	pyramid resolution

	\return 	int
	*/
	int ZoomForPixelSize(double pixelSize);

	/**!brief	Converts TMS tile coordinates to Google Tile coordinates
	*/
	void GoogleTile(int tx, int ty, int zoom, int& gx, int& gy);

	/**!brief	Converts TMS tile coordinates to Microsoft QuadTree
	*/
	std::string QuadTree(int tx, int ty, int zoom);

protected:
	int _tileSize;
	double  _initialResolution;
	double _originShift;

}
#endif // CATEYE_MERCATOR_H



#include "cateye_srtm.h"

using namespace Cateye::RasterCompiler;

Srtm::Srtm()
{
	_resolution = 5.0;
}

Srtm::~Srtm()
{

}

void Srtm::LonLatToTile(double lon, double lat, int& tx, int& ty)
{
	tx = int((lon + 180.0) / 5.0) + 1;
	ty = int((60.0 - lat) / 5.0) + 1;
}

void Srtm::LonLatBoundToTiles(double lonLatBound[4], int tileBound[4])
{
	int minTx = 0, minTy = 0;
	LonLatToTile(lonLatBound[0], lonLatBound[1], minTx, minTy);
	int maxTx = 0, maxTy = 0;
	LonLatToTile(lonLatBound[2], lonLatBound[3], maxTx, maxTy);

	//note the tile coordinate is top-left, but the lon/lat is bottom-left
	tileBound[0] = minTx;
	tileBound[1] = minTy;
	tileBound[2] = maxTx;
	tileBound[3] = maxTy;
	//tileBound = { minTx, maxTy, maxTx, minTy };
}
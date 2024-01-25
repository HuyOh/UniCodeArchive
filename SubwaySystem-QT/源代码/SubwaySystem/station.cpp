#include "station.h"
#include<math.h>

/*
 * 计算距离
 * @param lat1 纬度
 * @param lng1 经度
 * @param lat2 纬度
 * @param lng2 经度
 * @return 距离 M
*/
int static calcuDistance(double lat1, double lng1, double lat2, double lng2)
{
    static double Pi = 3.145926535;     // 估计圆周率
    static double Earth_R = 6371.393;   // 平均地球半径

    // 经纬度角度转弧度
    lat1 = lat1  * Pi / 180;
    lat2 = lat2  * Pi / 180;
    lng1 = lng1  * Pi / 180;
    lng2 = lng2  * Pi / 180;

    // 求两点球心角的余弦值
    double cos_ = cos(lat2) * cos(lat1) * cos(lng2 -lng1) + sin(lat1) * sin(lat2);

    return Earth_R * acos(cos_) * 1000;
}

// 给类静态成员变量附初值
double Station::maxLatitude = 0;
double Station::maxLongitude = 0;
double Station::minLatitude = 90;
double Station::minLongitude = 180;

// 计算另一个站点与本站点的距离
int Station::distance(Station another)
{
    return calcuDistance(latitude, longitude, another.latitude, another.longitude);
}

// 构造函数1
Station::Station()
{

}

// 构造函数2
Station::Station(QString name_, double lng, double lat, QList<int> linesList):
    name(name_), longitude(lng), latitude(lat)
{
    linesSet = QSet<int>(linesList.begin(), linesList.end());
}

#ifndef STATION_H
#define STATION_H

#include<QString>
#include<QSet>
#include<QList>

class Station
{
private:
    int id;                      // 站点标识ID
    QString name;                // 站点名
    double longitude, latitude;  // 站点经,纬度
    QSet<int>linesSet;           // 站点所属地铁线路的集合
    // 用静态属性记录所有站点的边界位置，便于绘制地铁线路图
    static double minLongitude, minLatitude, maxLongitude, maxLatitude;   
    int distance(Station another);  // 求取站点another与本站点的距离
public:
    Station();  // 构造函数
    Station(QString name, double lng, double lat, QList<int>linesList); // 构造函数
    // 声明友元便于获取私有属性
friend class SubwayGraph;
};

#endif // STATION_H

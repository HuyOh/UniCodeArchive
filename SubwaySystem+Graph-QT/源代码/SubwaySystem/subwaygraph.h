#ifndef SUBWAYGRAPH_H
#define SUBWAYGRAPH_H

#include"station.h"
#include"Line.h"
#include<QHash>
#include <limits.h>

#define INFINITY __DBL_MAX__

// 图的节点
class Node{
public:
    int id;         // 邻接点id
    double distance;// 两点之间的距离
    // 构造函数
    Node(){};
    Node(int id_, double distance_):id(id_), distance(distance_){};
    // ">"运算符重载，用于构建小顶堆
    bool operator > (const Node& n)const { return distance > n.distance; }
};


class SubwayGraph
{
private:
    QString name;                           // 地铁名
    QVector<Station>stations;               // 地铁网络中所有的站点
    QVector<Line>lines;                     // 地铁网络中所有的线路
    // 用两个hash表提高访问地铁线和站点的效率
    QHash<QString,int>stationHash;          // 站点名到stations中存储位置的映射
    QHash<QString,int>lineHash;             // 线路名到lines中存储位置的映射
    QSet<Edge>edges;                        // 所有连接关系的集合
    QVector<QVector<Node>>graph;            // 地铁网络图结构，近似于邻接表
    void makeGraph();  // 生成图的邻接表结构
public:
    // 构造函数
    SubwayGraph(){};
    SubwayGraph(QString name_):name(name_){ };
    // 获取线路名Key在lineHash中的value
    int getLineIndex(QString lineName);
    // 获取站点名Key在stationHash中的value
    int getStationIndex(QString stationName);
    // 从文件中读取格式化的数据
    bool readData(QString fileName);
    // 更新所有站点的边界经纬度坐标
    void updatePos(double lng, double lat);
    // 往edges插入一条边，不考虑翻转
    bool insertEdge(int first, int last);
    // 清除数据
    void clearData();
    // 求时间最短线路
    bool transferMinTime(int start, int end, QList<int>&stationsList, QList<Edge>&edgesList);
    // 求换乘最少路线
    bool transferMinTransfer(int start, int end, QList<int>&stationsList, QList<Edge>&edgesList);
    // 求最少站点路线
    bool transferMinStation(int start, int end, QList<int>&stationsList, QList<Edge>&edgesList);
    // 根据站点索引列表的站点名列表
    QList<QString> getStations(QList<int>stationsIndexList);
    // 根据站点名获取其所属线路名的列表
    QList<QString> getLines(QString stationName);
    // 获取所有线路名的列表
    QList<QString> getAllLines();
    // 根据站点索引获取站点名
    QString getStationName(int i);
    // 根据边Edge获取线路
    QList<int> getLinesOfEdge(Edge edge);
    // 获取边Edge的颜色（正片叠底）
    QColor getEdgeColor(QList<int> linesIndex);
    // 获取经纬度坐标边界信息
    double minLongitude();
    double minLatitude();
    double maxLongitude();
    double maxLatitude();
    // 获取站点经度
    double getLongitude(int i);
    // 获取站点纬度
    double getLatitude(int i);
    // 根据线路索引获取线路名
    QString getLineName(int i);
    // 获取所有边的列表
    QList<Edge> getEdges();
    // 获取所有站点索引的列表
    QList<int> getAllStationsIndex();
    // 获取所有站点名的列表
    QList<QString> getAllStationsName();
    // 根据线路名获取该线路中所有站点名的列表
    QList<QString> getStationsOfLine(QString lineName);
    // 获取站点的线路索引列表
    QList<int>getLinesIndex(int i);
    // 插入一条线路
    bool pushLine(QString lineName, QColor color);
    // 插入一个站点
    bool pushStation(QSet<int>lineSet,QString name,double longi,double lati);
    // 插入一条边
    bool pushEdge(QList<int>linesIndex,Edge edge);
};

#endif // SUBWAYGRAPH_H

#ifndef LINE_H
#define LINE_H

#include"station.h"
#include <QColor>

typedef QPair<int,int> Edge;

class Line{
private:
    int id;                     // 线路标识id
    QString name;               // 线路名称
    QColor color;               // 线路颜色
    QSet<int>stationSet;        // 线路站点集合
    QSet<Edge>edges;            // 线路连接关系
public:
    // 构造函数
    Line(){ };
    // 构造函数
    Line(int id_, QString name_, QColor color_)
        :id(id_), name(name_), color(color_){};

    // 用声明友元替代一系列get...()函数，方便获取私有属性
    friend class SubwayGraph;
};

#endif // LINE_H


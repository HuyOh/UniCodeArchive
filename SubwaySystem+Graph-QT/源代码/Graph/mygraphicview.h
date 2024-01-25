#ifndef MYGRAPHICVIEW_H
#define MYGRAPHICVIEW_H

#include <QGraphicsView>
#include<QMouseEvent>

class Node;

class MyGraphicView : public QGraphicsView
{
    Q_OBJECT
public:
    explicit MyGraphicView(QWidget *parent = nullptr);
    void zoomout();    // 放大视图
    void zoomin();     // 缩小视图


protected:
    void mouseMoveEvent(QMouseEvent *event) override;    // 鼠标移动时间
    void wheelEvent(QWheelEvent *event) override;   // 鼠标滑动时间

signals:
    void mouseMovePoint(QPoint point);   // 鼠标移动信号

private:
    double scale_m;   // 当前的放大倍数
    double factor;   // 缩放指数
};

#endif // MYGRAPHICVIEW_H

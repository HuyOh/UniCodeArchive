#ifndef MYSUBWAYVIEW_H
#define MYSUBWAYVIEW_H

#include <QWidget>
#include<QGraphicsView>
#include<QMouseEvent>

class MySubwayView : public QGraphicsView
{

    Q_OBJECT
public:
    explicit MySubwayView(QWidget *parent = nullptr);  // 构造函数，设置了一些视图的属性

protected:
    void mousePressEvent(QMouseEvent *event) override;  // 鼠标点击事件
    void mouseMoveEvent(QMouseEvent *event) override;   // 鼠标移动事件
    void mouseReleaseEvent(QMouseEvent *event) override;  // 鼠标释放事件
    void wheelEvent(QWheelEvent *event) override;  // 鼠标滑动时间
public:
    void zoomout();  // 放大视图
    void zoomin();   // 缩小视图

private:
    double scale_m;   // 当前缩放倍数
    double factor;    // 缩放指数
    bool isMousePressed;  // 记录鼠标是否被点击

    // 用于实现视图拖拽功能
    QPointF centerAnchor;
    QPointF posAnchor ;

signals:
    void mouseMovePoint(QPoint point);  // 鼠标移动事件信号
};

#endif // MYSUBWAYVIEW_H

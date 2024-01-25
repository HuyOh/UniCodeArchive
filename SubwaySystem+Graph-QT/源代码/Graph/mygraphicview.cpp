#include "mygraphicview.h"

MyGraphicView::MyGraphicView(QWidget *parent) : QGraphicsView(parent)
{
    scale_m = 1.0;
    factor = 1.2;
    // 设置光标-->光标跟踪
    setCursor(Qt::CrossCursor);
    setMouseTracking(true);//跟踪鼠标位置
    setTransformationAnchor(QGraphicsView::AnchorUnderMouse);
    setResizeAnchor(QGraphicsView::AnchorUnderMouse);
}

void MyGraphicView::mouseMoveEvent(QMouseEvent *event)
{
    QGraphicsView::mouseMoveEvent(event);

    QPoint point = event->pos();

    emit mouseMovePoint(point);   // 在状态栏显示坐标
}

void MyGraphicView::wheelEvent(QWheelEvent *event)
{
    // 获取鼠标滚轮的距离
    int wheelDeltaValue = event->delta();

    if (wheelDeltaValue > 0){
        // 向上滚动，放大
        if(scale_m < 10){
            this->scale(factor, factor);
            scale_m *= factor;
        }
    }
    else{
        // 向下滚动，缩小
        if(scale_m > 0.1){
            this->scale(1.0 / factor, 1.0 / factor);
            scale_m /= factor;
        }
    }
}

void MyGraphicView::zoomout()
{
    if(scale_m < 10){
        this->scale(factor, factor);
        scale_m *= factor;
    }
}

void MyGraphicView::zoomin()
{
    if(scale_m > 0.1){
        this->scale(1.0 / factor, 1.0 / factor);
        scale_m /= factor;
    }
}


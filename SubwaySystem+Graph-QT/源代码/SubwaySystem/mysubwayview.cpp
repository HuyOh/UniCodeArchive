
//#include<QDebug>
#include "mysubwayview.h"



MySubwayView::MySubwayView(QWidget *parent):QGraphicsView(parent)
{
    scale_m = 1.0;
    factor = 1.2;
    // 设置光标-->光标跟踪
    setCursor(Qt::CrossCursor);
    setMouseTracking(true);//跟踪鼠标位置
    setTransformationAnchor(QGraphicsView::AnchorUnderMouse);
    setResizeAnchor(QGraphicsView::AnchorUnderMouse);
}

void MySubwayView::mousePressEvent(QMouseEvent *event)
{
    if(event->button() == Qt::LeftButton){
        QPoint point = event->pos();
        centerAnchor = mapToScene(event->pos()) - event->pos() + QPointF(width()/2,height()/2);
        posAnchor = event->pos();

//        qDebug()<<centerAnchor;
//        qDebug()<<QPointF(width()/2,height()/2);
//        qDebug()<<mapToScene(event->pos());
//        qDebug()<<posAnchor;

        isMousePressed = true;
//        emit mouseClick(std::move(point));
    }
    QGraphicsView::mousePressEvent(event);
}

void MySubwayView::mouseMoveEvent(QMouseEvent *event)
{
    QGraphicsView::mouseMoveEvent(event);

    QPoint point = event->pos();

    emit mouseMovePoint(point);   // 在状态栏显示坐标

    // 实现拖拽功能
    QPointF offsetPos = point - posAnchor;
    if(isMousePressed){
        centerOn(centerAnchor - offsetPos);
    }


}

void MySubwayView::mouseReleaseEvent(QMouseEvent *event)
{
    QGraphicsView::mouseReleaseEvent(event);
    isMousePressed = false;
}

void MySubwayView::wheelEvent(QWheelEvent *event)
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

void MySubwayView::zoomout()
{
    if(scale_m < 10){
        this->scale(factor, factor);
        scale_m *= factor;
    }
}

void MySubwayView::zoomin()
{
    if(scale_m > 0.1){
        this->scale(1.0 / factor, 1.0 / factor);
        scale_m /= factor;
    }
}


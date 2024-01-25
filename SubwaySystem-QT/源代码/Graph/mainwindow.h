#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include<QGraphicsEllipseItem>
#include<QGraphicsLineItem>
#include<QLabel>
#include<QVector>
#include"algraph.h"
#include "choosefile.h"

#define normalColor QColor("#00FFFF")    // 非正在被访问的节点的颜色
#define visitingColor QColor("#DEB887")  // 正在被访问的节点的颜色
#define NODE_SIZE 40      // 节点的大小

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT
private:
    Ui::MainWindow *ui; // ui（界面）指针
    int SCENE_WIDTH;    // 场景宽度
    int SCENE_HEIGHT;   // 场景高度
    MatrixGraph * mGraph;  // 后端邻接矩阵对象
    ALGraph* alGraph;     // 后端邻接表对象
    QLabel* labViewCord;   // 状态栏标签1——View坐标
    QLabel* labSceneCord;  // 状态栏标签2——Scene坐标
    QLabel* labMaker;    // 状态栏标签3——制作者
    QGraphicsScene* Scene;  // 场景对象
    QVector<QGraphicsEllipseItem*> nodes; // 前端显示的节点
    QVector<QGraphicsTextItem*> texts;  // 前端显示的节点标识，与节点一一对应
    QVector<QGraphicsLineItem*> edges;  // 前端显示的边
    QVector<QGraphicsLineItem*> arrows; //前端显示的箭头，一条边对应一个箭头的两条直线
    QList<QString> chooseStartNodes;  // 选择开始遍历节点的下拉列表内容
    QString answer;          // 实时存储遍历结果的字符串
    int visiting = -1;       // 当前正在访问的节点的索引

    void pushNode(int i);  // 插入一个节点
    void pushEdge(int from, int to);  // 插入一条边
    void pushArrow(int from, int to); // 插入一个箭头
    QPointF calculateNodePos(int i);  // 计算节点的坐标
    void calculateEdgePos(int from, int to, QPointF &fromPos, QPointF &toPos); // 计算边的坐标
    void calculateArrowPos(QPointF from, QPointF to, QPointF &arrow1, QPointF &arrow2); // 计算箭头的坐标
    void updateNodes(int i);   // 更新节点（正在访问的节点改变颜色，访问完的节点恢复颜色）
    void initialGraph();     // 初始化视图，并显示内置图结构
    void updateStartList();  // 更新显示 选择开始遍历节点的下拉列表内容
    void updateStack(int *stack,int top);  // 更新显示当前栈的情况
    void updateQueue(int *queue,int front,int rear);  // 更新显示当前队列的情况
    void updateALGraph();   // 更新显示图的邻接表结构
    void newGraph();     // 在视图中显示新的图结构
    void clear();  // 清除指针，回收内存
public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();
private slots:
    void on_mouseMovePoint(QPoint point);   // 鼠标移动
    void on_DFSRecursion_clicked();  // 递归法深度优先遍历按钮
    void on_BFSTraverse_clicked();   // 广度优先遍历按钮
    void on_DFSNonRecursion_clicked();  // 非递归法深度优先遍历按钮
    void on_exitAction_2_triggered();  // 退出程序按钮
    void on_zoomoutAction_triggered();  // 放大视图按钮
    void on_zoominAction_triggered();  // 缩小试图按钮
    void on_helpAction_triggered();  // 帮助页面按钮
    void on_aboutMakerAction_triggered();  // 关于页面按钮
    void on_chooseFileAction_triggered();  // 选择文件按钮
    void on_spinBox_valueChanged(int arg1);  // 延迟时间输入框内容改变
signals:
    void zoomout();   // 视图放大信号
    void zoomin();  // 视图缩小信号
};

#endif // MAINWINDOW_H

#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QGraphicsScene>
#include <QLabel>
#include <QMainWindow>
#include"subwaygraph.h"
#include"addstation.h"

QT_BEGIN_NAMESPACE
// 对应着UI文件中的MainWindow类
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT
public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();
private:
    Ui::MainWindow *ui;
    SubwayGraph* mySubway;   // 后端网络对象
    QLabel* labLongiLati;   // 状态栏标签1——经纬度
    QLabel* labViewCord;   // 状态栏标签2——View坐标
    QLabel* labSceneCord;  // 状态栏标签3——Scene坐标
    QLabel* labMaker;  // 状态栏标签4——制作者
    QGraphicsScene* Scene;  // 场景对象
    // 画一条边
    void drawEdge(Edge edge, bool flag = 0);
    // 画边的集合
    void drawEdges(QList<Edge>edges1, bool flag = 0, QList<Edge>edges2 = {});
    // 画一个站点
    void drawStation(int i, bool falg = 0, bool flag2 = 0);
    // 画站点的集合
    void drawStations(QList<int>stations1, bool flag = 0, QList<int>stations2 = {});
    // 用经纬度计算对应场景坐标
    QPointF calScenePos(double longi, double lati);
    // 用场景坐标计算经纬度
    QPointF calLongiLati(QPointF scenePos);
    // 获得线路集的字符串形式
    QString getLinesName(QList<int>linesIndex);
    // 更新起始路线和终点路线的下拉列表
    void updateLinesItem();
    // 更新起始站的下拉列表
    void updateStartStationsItem();
    // 更新终点站的下拉列表
    void updateEndStationsItem();
    // 初始化视图
    void initGraphics();
    // 画视图（将路径与网络区别显示）
    void drawGraphics(QList<int>stationsindex,QList<Edge>edges);
private slots:
    void on_mouseMovePoint(QPoint point);  // 鼠标移动
    void on_confirmBtn_clicked();  // 确认按钮
    void on_startLine_currentIndexChanged(const QString &arg1);  // 开始路线下拉列表当前内容改变
    void on_endLine_currentIndexChanged(const QString &arg1);  // 终点路线下拉列表当前内容改变
    void on_exitAction_triggered();   // 退出程序按钮
    void on_addAction_triggered();   // 动态添加按钮
    void on_zoomoutAction_triggered();  // 放大按钮
    void on_zoominAction_triggered();   // 缩小按钮
    void on_recoverAction_triggered();  // 恢复网络视图按钮
    void on_aboutMakerAction_triggered();  // 关于制作者页面按钮
    void on_helpAction_triggered();   // 帮助页面按钮
signals:
    void zoomout();   // 放大视图
    void zoomin();   // 缩小视图
};


#define MARGIN 30           //视图左边距
#define NET_WIDTH 2000      //网络图最大宽度
#define NET_HEIGHT 2000     //网络图最大高度
#define SCENE_WIDTH (MARGIN*2+NET_WIDTH)    //场景宽度
#define SCENE_HEIGHT (MARGIN*2+NET_HEIGHT)  //场景高度

#define EDGE_PEN_WIDTH 2    //线路边宽
#define NODE_HALF_WIDTH 3   //节点大小

#endif // MAINWINDOW_H

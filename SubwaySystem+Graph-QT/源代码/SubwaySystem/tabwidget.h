#ifndef TABWIDGET_H
#define TABWIDGET_H

#include<QListWidget>
#include"subwaygraph.h"
#include"Line.h"

namespace Ui {
class TabWidget;
}

class TabWidget : public QTabWidget
{
    Q_OBJECT

public:
    explicit TabWidget(SubwayGraph *mySubway_, QWidget *parent = nullptr);
    ~TabWidget();

private slots:
    void on_colorDlg_clicked();    // 颜色选择对话框按钮
    void setLineMessage(QColor color);  // 显示已添加的线路信息
    void on_addLineBtn_clicked();   // 添加线路页面按钮
    void on_addStationBtn_clicked();  // 添加站点页面按钮
    void on_addEdgeBtn_clicked();  // 添加连接关系页面按钮
private:
    Ui::TabWidget *ui;
    SubwayGraph *mySubway;  // 后端网络对象
    QString lineName;    // 输入的线路名
    QColor color;     // 选择的线路颜色

    void updataLinesList(QListWidget*listWidget);   // 更新线路选择下拉列表
    void updateAllStationsItem();       // 更新站点选择下拉列表

signals:
    emit void colorChoosed(QColor color);   // 颜色被选择信号
    emit void lineAdded();   // 线路被添加信号
    emit void stationAdded();  // 站点被添加信号
    emit void edgeAdded();  // 连接关系被添加信号
};

#endif // TABWIDGET_H

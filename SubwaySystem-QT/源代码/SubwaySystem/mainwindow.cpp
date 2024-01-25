#include "mainwindow.h"
#include "ui_mainwindow.h"
//#include<QDebug>
#include <qgraphicsitem.h>
#include<QGraphicsView>
#include <QButtonGroup>
#include <QMessageBox>
#include"tabwidget.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)  // 实例化了一个Ui的MainWindow窗口
{
    ui->setupUi(this);

    this->setWindowIcon(QIcon(":/icon/icon/mainWindowIcon.jpeg"));
    this->setWindowTitle(QString("上海地铁乘坐指南"));

    mySubway = new SubwayGraph(QString("上海地铁网络"));
    mySubway->readData(":/data/data/outLine.txt");       // 读取文本文件进行网络初始化

    labMaker = new QLabel("  maker：2052082王辉  ");
    labMaker->setMinimumWidth(100);
    ui->statusBar->addWidget(labMaker);

    labViewCord = new QLabel("View坐标：");
    labViewCord->setMinimumWidth(100);
    ui->statusBar->addWidget(labViewCord);

    labSceneCord = new QLabel("Scene坐标：");
    labSceneCord->setMinimumWidth(100);
    ui->statusBar->addWidget(labSceneCord);

    labLongiLati = new QLabel("经纬度");
    labLongiLati->setMinimumWidth(100);
    ui->statusBar->addWidget(labLongiLati);

    updateLinesItem();

    connect(this,&MainWindow::zoomout,ui->subwayView,&MySubwayView::zoomout);
    connect(this,&MainWindow::zoomin,ui->subwayView,&MySubwayView::zoomin);
    connect(ui->subwayView,SIGNAL(mouseMovePoint(QPoint)),this,SLOT(on_mouseMovePoint(QPoint)));

    initGraphics();
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::drawEdge(Edge edge, bool flag)
{
    QList<int> linesIndex = mySubway->getLinesOfEdge(edge);
    QColor color = mySubway->getEdgeColor(linesIndex);

    if(flag){
        color.setAlpha(30);
    }

    int s1 =edge.first, s2 =edge.second;
    QPointF pos1 = calScenePos(mySubway->getLongitude(s1),mySubway->getLatitude(s1));
    QPointF pos2 = calScenePos(mySubway->getLongitude(s2),mySubway->getLatitude(s2));


    QString tips = "途经：" + mySubway->getStationName(s1) + "-->" + mySubway->getStationName(s2) +
            "\n线路：" + getLinesName(linesIndex);

    QGraphicsLineItem* lineItem = new QGraphicsLineItem;
    lineItem->setPen(QPen(color,EDGE_PEN_WIDTH));
    lineItem->setCursor(Qt::WhatsThisCursor);
    lineItem->setPos(pos1);
    lineItem->setLine(0,0,pos2.x() - pos1.x(),pos2.y() - pos1.y());
    lineItem->setToolTip(tips);

    Scene->addItem(lineItem);
}

void MainWindow::drawEdges(QList<Edge> edges1, bool flag, QList<Edge>edges2)
{
    if(!flag){
        for(auto edge : edges1)
            drawEdge(edge);
    }
    else{
        for(auto edge : edges1){
            if(!edges2.contains(edge) && !edges2.contains(Edge(edge.second,edge.first)))
                drawEdge(edge,true);
            else
                drawEdge(edge);
        }
        for(auto edge : edges2){
            if(!edges1.contains(edge) && !edges1.contains(Edge(edge.second,edge.first)))
                drawEdge(edge);
        }
    }

}


void MainWindow::drawStation(int i, bool flag1, bool flag2)
{
    QString stationName = mySubway->getStationName(i);
    QList<int> linesIndex = mySubway->getLinesIndex(i);
    QString tips = "站点：" + stationName + "\n线路：" + getLinesName(linesIndex) +
            "\n东经：" + QString::number(mySubway->getLongitude(i),10,6) +
            "\n北纬：" + QString::number(mySubway->getLatitude(i),10,6);
    QPointF pos = calScenePos(mySubway->getLongitude(i),mySubway->getLatitude(i));
    QColor color = mySubway->getEdgeColor(linesIndex);
    if(flag1) {
        color.setAlpha(30);
    }

    QGraphicsEllipseItem* stationItem = new QGraphicsEllipseItem;
    stationItem->setPen(QPen(color));
    stationItem->setToolTip(tips);
    stationItem->setPos(pos);
    stationItem->setCursor(Qt::WhatsThisCursor);
    stationItem->setRect(-NODE_HALF_WIDTH,-NODE_HALF_WIDTH,NODE_HALF_WIDTH*2,NODE_HALF_WIDTH*2);

    Scene->addItem(stationItem);

    QGraphicsTextItem* name = new QGraphicsTextItem;
    name->setPlainText(stationName);
    name->setPos(pos);
    name->setFont(QFont("SimSun",5));
    name->setCursor(Qt::IBeamCursor);
    if(flag2) {
        name->setFont(QFont("Sim Sun",3,QFont::Light));
    }

    Scene->addItem(name);
}

void MainWindow::drawStations(QList<int> stations1, bool flag, QList<int>stations2)
{
    if(!flag){
        for(auto i : stations1){
            drawStation(i);
        }
    }
    else{
        for(auto i : stations1){
            if(!stations2.contains(i))
                drawStation(i,1,1);
            else
                drawStation(i);
        }
    }

}

QPointF MainWindow::calScenePos(double longi, double lati)
{
    QPointF pos;
    pos.setX((longi - mySubway->minLongitude()) / (mySubway->maxLongitude()-mySubway->minLongitude()) * NET_WIDTH + MARGIN);
    pos.setY(NET_HEIGHT - (lati - mySubway->minLatitude()) / (mySubway->maxLatitude() - mySubway->minLatitude()) * NET_HEIGHT + MARGIN);
    return pos;
}

QPointF MainWindow::calLongiLati(QPointF scenePos)
{
    QPointF pos;
    pos.setX((scenePos.x() - MARGIN) / NET_WIDTH * (mySubway->maxLongitude()-mySubway->minLongitude()) + mySubway->minLongitude());
    pos.setY((NET_HEIGHT + MARGIN - scenePos.y()) / NET_HEIGHT * (mySubway->maxLatitude() - mySubway->minLatitude()) + mySubway->minLatitude());
    return pos;
}

QString MainWindow::getLinesName(QList<int> linesIndex)
{
    QString linesName="";
    for(int i : linesIndex){
        linesName+=mySubway->getLineName(i);
    }
    return linesName;
}

void MainWindow::updateLinesItem()
{
    QList<QString> allLines = mySubway->getAllLines();
    //qDebug()<<allLines.size()<<"=";
    ui->startLine->clear();
    ui->endLine->clear();
    ui->startLine->addItems(allLines);
    ui->endLine->addItems(allLines);
}

void MainWindow::updateStartStationsItem()
{
    QString startLine = ui->startLine->currentText();
    QList<QString> startStationsName = mySubway->getStationsOfLine(startLine);
    ui->startStation->clear();
    ui->startStation->addItems(startStationsName);
}

void MainWindow::updateEndStationsItem()
{
    QString endLine = ui->endLine->currentText();
    QList<QString> endStationsName = mySubway->getStationsOfLine(endLine);
    ui->endStation->clear();
    ui->endStation->addItems(endStationsName);
}



void MainWindow::initGraphics()
{
    //QRect rect(-200,-100,400,200);
    //QRect rect(-SCENE_WIDTH/2,-SCENE_HEIGHT/2,SCENE_WIDTH/2,SCENE_HEIGHT/2);
    //QRect rect(-SCENE_WIDTH/2,-SCENE_HEIGHT/2,SCENE_WIDTH,SCENE_HEIGHT);
    QRect rect(0,0,SCENE_WIDTH,SCENE_HEIGHT);
    Scene = new QGraphicsScene(rect);
    ui->subwayView->setScene(Scene);
    ui->subwayView->setRenderHint(QPainter::Antialiasing);


    QGraphicsRectItem* item = new QGraphicsRectItem(rect);
    item->setFlags(QGraphicsItem::ItemIsFocusable|QGraphicsItem::ItemIsSelectable);

    QPen pen;
    pen.setWidth(2);
    item->setPen(pen);
    Scene->addItem(item);

    QList<Edge>edges = mySubway->getEdges();
    drawEdges(edges);

    QList<int> stationsIndex = mySubway->getAllStationsIndex();
    drawStations(stationsIndex);
}

void MainWindow::drawGraphics(QList<int> stationsIndex, QList<Edge> edges)
{
    //QRect rect(-200,-100,400,200);
    //QRect rect(-SCENE_WIDTH/2,-SCENE_HEIGHT/2,SCENE_WIDTH/2,SCENE_HEIGHT/2);
    //QRect rect(-SCENE_WIDTH/2,-SCENE_HEIGHT/2,SCENE_WIDTH,SCENE_HEIGHT);
    QRect rect(0,0,SCENE_WIDTH,SCENE_HEIGHT);
    Scene = new QGraphicsScene(rect);
    ui->subwayView->setScene(Scene);
    ui->subwayView->setRenderHint(QPainter::Antialiasing);

    QGraphicsRectItem* item = new QGraphicsRectItem(rect);
    item->setFlags(QGraphicsItem::ItemIsFocusable|QGraphicsItem::ItemIsSelectable);

    QPen pen;
    pen.setWidth(2);
    item->setPen(pen);
    Scene->addItem(item);

    QList<Edge>allEdges = mySubway->getEdges();
    QList<int> allStationsIndex = mySubway->getAllStationsIndex();
    drawEdges(allEdges, true, edges);
    drawStations(allStationsIndex, true, stationsIndex);
}

void MainWindow::on_mouseMovePoint(QPoint point)
{
    QString tip1 = "  View坐标：" + QString::number(point.x(),10) + "，" + QString::number(point.y(),10) + "  ";
    labViewCord->setText(tip1);

    QPointF pointScene = ui->subwayView->mapToScene(point);
    QString tip2 = "  Scene坐标：" + QString::number(pointScene.x(),10,0) + "，" + QString::number(pointScene.y(),10,0) + "  ";
    labSceneCord->setText(tip2);

    QPointF longiLati = calLongiLati(pointScene);
    QString tip3 = "  东经：" + QString::number(longiLati.x(),10,6) + "   北纬：" + QString::number(longiLati.y(),10,6) + "  ";
    labLongiLati->setText(tip3);
}


void MainWindow::on_confirmBtn_clicked()
{
    QString startStationName = ui->startStation->currentText();
    QString endStationName = ui->endStation->currentText();
    int startStationIndex = mySubway->getStationIndex(startStationName);
    int endStationIndex = mySubway->getStationIndex(endStationName);

    QString text = "";

    QList<int>stationsIndex;
    QList<Edge>edges;
    bool flag = true;
    if(ui->minDistanceBtn->isChecked()==true){
        flag = mySubway->transferMinTime(startStationIndex,endStationIndex,stationsIndex,edges);
        text += "共需乘坐 " + QString::number(stationsIndex.size()-1) + " 个站点\n";
    }
    else if(ui->minTransferBtn->isChecked()==true){
        flag = mySubway->transferMinTransfer(startStationIndex,endStationIndex,stationsIndex,edges);
        text += "共需换乘 " + QString::number(stationsIndex.size()-1) + " 次\n";
    }
    else{
        flag = mySubway->transferMinStation(startStationIndex,endStationIndex,stationsIndex,edges);
        text += "共需乘坐 " + QString::number(stationsIndex.size()-1) + " 个站点\n";
    }

    if(flag){
        QList<QString>stationsNames = mySubway->getStations(stationsIndex);

        int k = 1;
        for(auto i : stationsNames){
            QList<QString>linesName = mySubway->getLines(i);

            text += QString::number(k) +"：" + i + "  ";
            for(auto j : linesName){
                text += j + " ";
            }
            text +="\n";
            k++;
        }
        drawGraphics(stationsIndex, edges);
    }
    else{
        text = "无法乘坐地铁到达目的地，请重新选择！";
    }
    ui->textBrowser->setText(text);
}

void MainWindow::on_startLine_currentIndexChanged(const QString &arg1)
{
    Q_UNUSED(arg1);
    updateStartStationsItem();
}

void MainWindow::on_endLine_currentIndexChanged(const QString &arg1)
{
    Q_UNUSED(arg1);
    updateEndStationsItem();
}

void MainWindow::on_exitAction_triggered()
{
    qApp->quit();
}

void MainWindow::on_addAction_triggered()
{
    TabWidget *tabWidget = new TabWidget(mySubway);
    tabWidget->show();
    connect(tabWidget, &TabWidget::lineAdded, this, &MainWindow::updateLinesItem);
    connect(tabWidget,&TabWidget::edgeAdded,this,&MainWindow::initGraphics);
    connect(tabWidget,&TabWidget::edgeAdded,this,&MainWindow::updateStartStationsItem);
    connect(tabWidget,&TabWidget::edgeAdded,this,&MainWindow::updateEndStationsItem);
}

void MainWindow::on_zoomoutAction_triggered()
{
    emit zoomout();
}

void MainWindow::on_zoominAction_triggered()
{
    emit zoomin();
}

void MainWindow::on_recoverAction_triggered()
{
    initGraphics();
}

void MainWindow::on_aboutMakerAction_triggered()
{
    QString text = "姓名：王辉\n学校：Tongji University\n学号：2052082\n邮箱：2094848219@qq.com\nQT：5.14.2 Version";
    QMessageBox::information(this, "about maker",text);
}


void MainWindow::on_helpAction_triggered()
{
    QString text = QString("\n1. 您可以选择出发站和目标站，点击确定获取地铁出行指南，有最短距离、最少换乘和最少站点三种出行策略。\n") +
            QString("2. 最少换乘策略给出换乘站点，在地铁网络上用直线将出发站、换乘站和目标站连接。\n") +
            QString("3. 在状态栏，您可以看到鼠标所在位置的经纬度坐标、视图坐标系坐标和场景坐标系坐标。\n") +
            QString("4. 鼠标悬停在站点图标上，您可以获得该站点的有关信息。\n") +
            QString("5. 鼠标悬停在线路图标上，您可以获得该线路的相关信息。\n") +
            QString("6. 滑动鼠标滚轮，您可以放大或缩小视图；您也可以点击工具栏的放大和缩小按钮。\n") +
            QString("7. 点击动态添加按钮，您可以尝试在地铁网络上添加站点、线路；在本次程序运行期间，您将可以在地铁网络图上看到您所添加的内容，退出程序后，数据将被删除。\n") +
            QString("8. 点击回复视图按钮，视图将回复到获取乘坐指南前的状态。\n") +
            QString("9. 欢迎联系作者。感谢使用！");
    QWidget * helpWidget = new QWidget();
    helpWidget->setFixedSize(700,500);
    helpWidget->setWindowIcon(QIcon(":/icon/icon/help.jpeg"));
    helpWidget->setWindowTitle("使用帮助");
    QTextBrowser * helpBrowser = new QTextBrowser;
    helpBrowser->setText(text);
    helpBrowser->setFont(QFont("SimSun",12));
    helpBrowser->setFixedSize(700,500);
    helpBrowser->setParent(helpWidget);
    helpWidget->show();

}

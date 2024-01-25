#include "mainwindow.h"
#include "ui_mainwindow.h"

#include"matrixgraph.h"
#include"algraph.h"
//#include<QDebug>
#include <QFileDialog>
#include <QGraphicsEllipseItem>
#include <QMessageBox>
#include<QtMath>
#include "choosefile.h"


MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    this->setWindowIcon(QIcon(":/icon/net.jpeg"));
    this->setWindowTitle("MyGraph");

    // 以邻接矩阵的方式确定一个有向图
    mGraph = new MatrixGraph;
    //mGraph->print();

    // 生成邻接表形式
    alGraph = new ALGraph;
    alGraph->CreateG(mGraph);

    initialGraph();

    // 添加状态栏内容
    labMaker = new QLabel("  maker：2052082王辉  ");
    labMaker->setMinimumWidth(100);
    ui->statusbar->addWidget(labMaker);

    labViewCord = new QLabel("View坐标：");
    labViewCord->setMinimumWidth(100);
    ui->statusbar->addWidget(labViewCord);

    labSceneCord = new QLabel("Scene坐标：");
    labSceneCord->setMinimumWidth(100);
    ui->statusbar->addWidget(labSceneCord);

    ui->answerBroswer->setFont(QFont("SimSun",12));
    ui->processBrowser->setFont(QFont("SimSun",12));
    ui->alGraphBroswer->setFont(QFont("SimSun",10));

    connect(this,&MainWindow::zoomout,ui->graphicsView,&MyGraphicView::zoomout);
    connect(this,&MainWindow::zoomin,ui->graphicsView,&MyGraphicView::zoomin);
    connect(alGraph,&ALGraph::queueChanged,this,&MainWindow::updateQueue);
    connect(alGraph,&ALGraph::stackChanged,this,&MainWindow::updateStack);
    connect(ui->graphicsView,SIGNAL(mouseMovePoint(QPoint)),this,SLOT(on_mouseMovePoint(QPoint)));
    connect(alGraph, &ALGraph::nodeIVisited, this, &MainWindow::updateNodes);

}


void MainWindow::pushNode(int i)
{
    QPointF pos = calculateNodePos(i);
    QGraphicsEllipseItem *item = new QGraphicsEllipseItem();
    item->setPos(pos);
    item->setPen(normalColor);
    item->setBrush(normalColor);
    item->setRect(-NODE_SIZE/2,-NODE_SIZE/2,NODE_SIZE,NODE_SIZE);
    item->setData(i,alGraph->vexs_L[i].data);
    item->setToolTip(QString("%1号顶点").arg(i));
    item->setZValue(1);     // 设置层叠等级为1
    nodes.push_back(item);

    QGraphicsTextItem* text = new QGraphicsTextItem;
    text->setPlainText(QString(alGraph->vexs_L[i].data));
    text->setPos(pos - QPointF(11, 18));
    text->setFont(QFont("SimSun",20));
    text->setZValue(2);    // 设置层叠等级为2
    texts.push_back(text);
}

void MainWindow::pushEdge(int from, int to)
{
    QPointF fromPos, toPos;
    calculateEdgePos(from, to, fromPos, toPos);

    QGraphicsLineItem* edge = new QGraphicsLineItem;
    edge->setPen(QPen(normalColor,1));
    edge->setPos(fromPos);
    edge->setLine(0,0,toPos.x() - fromPos.x(),toPos.y() - fromPos.y());
    edge->setZValue(3);    // 设置层叠等级为3

    edges.push_back(edge);

    pushArrow(from, to);

}

void MainWindow::pushArrow(int from, int to)
{
    QPointF arrowPos1,arrowPos2,fromPos,toPos;
    calculateEdgePos(from,to,fromPos,toPos);
    calculateArrowPos(fromPos,toPos,arrowPos1,arrowPos2);

    QGraphicsLineItem* arrow1 = new QGraphicsLineItem;
    arrow1->setPen(QPen(normalColor,1));
    arrow1->setPos(toPos);
    arrow1->setLine(0,0,arrowPos1.x() - toPos.x(), arrowPos1.y() - toPos.y());
    arrow1->setZValue(3);    // 设置层叠等级为3
    arrows.push_back(arrow1);

    QGraphicsLineItem* arrow2 = new QGraphicsLineItem;
    arrow2->setPen(QPen(normalColor,1));
    arrow2->setPos(toPos);
    arrow2->setLine(0,0,arrowPos2.x() - toPos.x(), arrowPos2.y() - toPos.y());
    arrow2->setZValue(3);    // 设置层叠等级为3
    arrows.push_back(arrow2);
}

QPointF MainWindow::calculateNodePos(int i)
{
    double interval = 2*3.1416/alGraph->vexnum;
    qreal xt = qSin(interval * i) * 100 + Scene->width()/2;
    qreal yt = qCos(interval * i) * 100 + Scene->height()/2;
    return QPointF(xt,yt);
}

void MainWindow::calculateEdgePos(int from, int to, QPointF &fromPos, QPointF &toPos)
{
    fromPos = nodes[from]->pos();
    toPos = nodes[to]->pos();
    //fromPos = calculateNodePos(from);
    //toPos = calculateNodePos(to);
    int flag1 = (toPos.x() - fromPos.x())>0? 1:-1;
    int flag2 = (toPos.y() - fromPos.y())>0? 1:-1;

    double angle = qAbs(qAtan((toPos.y() - fromPos.y())/(toPos.x() - fromPos.x())));
    qreal offsetX = (NODE_SIZE) * qCos(angle) / 2;
    qreal offsetY = (NODE_SIZE) * qSin(angle) / 2;

    QPointF offset = QPointF(offsetX * flag1, offsetY *flag2);
    fromPos += offset;
    toPos -= offset;
}

void MainWindow::calculateArrowPos(QPointF from, QPointF to, QPointF &arrowPos1, QPointF &arrowPos2)
{
    double arrow_lenght_ = 10; //箭头长度，一般固定
    double arrow_degrees_ = 0.5; //箭头角度，一般固定

    double angle = atan2 (to.y() - from.y(), to.x() - from.x()) + M_PI;

    arrowPos1.setX(to.x() + arrow_lenght_ * cos(angle - arrow_degrees_));
    arrowPos1.setY(to.y() + arrow_lenght_ * sin(angle - arrow_degrees_));
    arrowPos2.setX(to.x() + arrow_lenght_ * cos(angle + arrow_degrees_));
    arrowPos2.setY(to.y() + arrow_lenght_ * sin(angle + arrow_degrees_));
}

void MainWindow::initialGraph(){

    updateStartList();

    ui->answerBroswer->clear();
    ui->processBrowser->clear();
    ui->alGraphBroswer->clear();
    updateALGraph();

     // 初始化场景对象
    SCENE_WIDTH = SCENE_HEIGHT = alGraph->vexnum * 50 ;
    QRect rect(0,0,SCENE_WIDTH,SCENE_WIDTH);
    Scene = new QGraphicsScene(rect);

    for(int i = 0; i < alGraph->vexnum; i++){
        pushNode(i);
    }

    for(int i = 0; i < alGraph->vexnum; i++){
        ArcNode* temp = alGraph->vexs_L[i].firstarc;
        while(temp != nullptr){
            pushEdge(i, temp->adjvex);
            temp = temp->nextarc;
        }
    }

    for(auto item : nodes){
        Scene->addItem(item);
    }
    for(auto text : texts){
        Scene->addItem(text);
    }
    for(auto edge : edges){
        Scene->addItem(edge);
    }
    for(auto arrow : arrows){
        Scene->addItem(arrow);
    }

    // 将场景设置给视图对象
    ui->graphicsView->setScene(Scene);
    ui->graphicsView->setRenderHint(QPainter::Antialiasing);
}

void MainWindow::on_chooseFileAction_triggered()
{
    chooseFile *fileWidget = new chooseFile();
    fileWidget->show();
    connect(fileWidget,&chooseFile::chooseFileConfirmed,this,&MainWindow::newGraph);
}


void MainWindow::updateStartList()
{
    chooseStartNodes.clear();
    for(int i = 0; i < alGraph->vexnum; i++){
        chooseStartNodes.push_back(QString(alGraph->vexs_L[i].data));
    }
    ui->comboBox->clear();
    ui->comboBox->addItems(chooseStartNodes);
}

void MainWindow::updateALGraph()
{
    QString str = "";
    for (int i = 0; i < alGraph->vexnum; i++) {  //打印邻接表
        str += QString(alGraph->vexs_L[i].data);
        ArcNode* p = alGraph->vexs_L[i].firstarc;
        while (p != NULL) {
            str += "-->" + QString(alGraph->vexs_L[p->adjvex].data);
            p = p->nextarc;
        }
        str += "\n";
    }
    ui->alGraphBroswer->setText(str);
    return;
}

void MainWindow::newGraph()
{
    this->clear();
    QString fileName;
    fileName = QFileDialog::getOpenFileName(this,"选择文件","../data/graph1.txt",tr("Text files (*.txt)"));
    if(!mGraph->makeMatrixGraph(fileName)){
        QString text = "打开文件发生错误或文本内容不符合规范！";
        QMessageBox::warning(this,"warning",text);
        return ;
    }
    else{
        QString text = "文件读取成功！";
        QMessageBox::information(this, "information",text);
        alGraph->CreateG(mGraph);
        SCENE_WIDTH = SCENE_HEIGHT = alGraph->vexnum * 50;
        QRect rect(0,0,SCENE_WIDTH,SCENE_WIDTH);
        Scene = new QGraphicsScene(rect);
        initialGraph();
    }
}

void MainWindow::clear()
{
    for(auto i : nodes){
        delete i;
    }
    nodes.clear();
    for(auto i : edges){
        delete i;
    }
    edges.clear();
    for(auto i : texts){
        delete i;
    }
    texts.clear();
    for(auto i : arrows){
        delete i;
    }
    arrows.clear();
}

void MainWindow::updateStack(int stack[], int top)
{
    QString str = "栈底| ";
    for(int i = 0; i< top; i++){
        str += QString(alGraph->vexs_L[stack[i]].data) + " | ";
    }
    ui->processBrowser->setText(str);
}

void MainWindow::updateQueue(int queue[], int front, int rear)
{
    QString str = "队头| ";
    while (rear != front) {
        str += QString(alGraph->vexs_L[queue[front]].data) + " | ";
        front = (front+1)%alGraph->vexnum;
    }
    str += "队尾";
    ui->processBrowser->setText(str);
}

void MainWindow::updateNodes(int i)
{
    if(visiting != -1){
        nodes[visiting]->setPen(normalColor);
        nodes[visiting]->setBrush(normalColor);
    }
    if(i != -1){
        nodes[i]->setPen(visitingColor);
        nodes[i]->setBrush(visitingColor);
        visiting =i;
        answer += " -> " + QString(alGraph->vexs_L[i].data);
        ui->answerBroswer->setText(answer);
    }

}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::on_mouseMovePoint(QPoint point)
{
    QString tip1 = "  View坐标：" + QString::number(point.x(),10) + "，" + QString::number(point.y(),10) + "  ";
    labViewCord->setText(tip1);
    QPointF pointScene = ui->graphicsView->mapToScene(point);
    QString tip2 = "  Scene坐标：" + QString::number(pointScene.x(),10,0) + "，" + QString::number(pointScene.y(),10,0) + "  ";
    labSceneCord->setText(tip2);
}


void MainWindow::on_DFSRecursion_clicked()
{
    //qDebug()<<"递归法深度优先遍历";
    visiting = -1;
    answer = "";
    ui->answerBroswer->clear();
    ui->processBrowser->clear();
    char start = ui->comboBox->currentText()[0].unicode();  // 获取开始遍历的顶点
    alGraph->DFSRecursion(start);
}

void MainWindow::on_BFSTraverse_clicked()
{
    //qDebug()<<"广度优先遍历";
    visiting = -1;
    answer = "";
    ui->answerBroswer->clear();
    ui->processBrowser->clear();
    char start = ui->comboBox->currentText()[0].unicode();  // 获取开始遍历的顶点
    alGraph->BFSTraverse(start);
}

void MainWindow::on_DFSNonRecursion_clicked()
{
    //qDebug()<<"非递归法深度优先遍历";
    visiting = -1;
    answer = "";
    ui->answerBroswer->clear();
    ui->processBrowser->clear();
    char start = ui->comboBox->currentText()[0].unicode();  // 获取开始遍历的顶点
    alGraph->DFSNonRecursion(start);

}

void MainWindow::on_exitAction_2_triggered()
{
    qApp->quit();
}

void MainWindow::on_zoomoutAction_triggered()
{
    emit zoomout();
}

void MainWindow::on_zoominAction_triggered()
{
    emit zoomin();
}

void MainWindow::on_helpAction_triggered()
{
    QString text = QString("\n1. 程序已经存在默认图结构，您可以通过选择我为您准备的.txt文件输入其它图结构；如您想要选择自己的.txt文件，文件内的文本需要严格符合格式要求。\n\n") +
            QString("2. 您可以选择三种遍历方式：递归法深度优先遍历、广度优先遍历、非递归法深度优先遍历。\n\n") +
            QString("3. 在状态栏，您可以看到鼠标所在位置视图坐标系坐标和场景坐标系坐标。\n\n") +
            QString("4. 滑动鼠标滚轮，您可以放大或缩小视图；您也可以点击工具栏的放大和缩小按钮。\n\n") +
            QString("5. 欢迎联系作者。感谢使用！");
    QWidget * helpWidget = new QWidget();
    helpWidget->setWindowIcon(QIcon(":/icon/help.jpeg"));
    helpWidget->setFixedSize(600,600);
    helpWidget->setWindowTitle("使用帮助");
    QTextBrowser * helpBrowser = new QTextBrowser;
    helpBrowser->setText(text);
    helpBrowser->setFont(QFont("SimSun",12));
    helpBrowser->setFixedSize(600,600);
    helpBrowser->setParent(helpWidget);
    helpWidget->show();
}

void MainWindow::on_aboutMakerAction_triggered()
{
    QString text = "姓名：王辉\n学校：Tongji University\n学号：2052082\n邮箱：2094848219@qq.com\nQT：5.14.2 Version";
    QMessageBox::information(this, "about maker",text);
}


void MainWindow::on_spinBox_valueChanged(int arg1)
{
    alGraph->delayTime = arg1;
}

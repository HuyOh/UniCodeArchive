#include "tabwidget.h"
#include "ui_tabwidget.h"
#include<QColorDialog>
#include <QMessageBox>
#include <QPainter>
//#include<QDebug>



TabWidget::TabWidget(SubwayGraph *mySubway_, QWidget *parent) :
    QTabWidget(parent),
    ui(new Ui::TabWidget)
{
    mySubway = mySubway_;
    ui->setupUi(this);
    this->setWindowIcon(QIcon(":/icon/icon/add.jpeg"));
    this->setWindowTitle(QString("动态添加"));
    this->setFixedSize(700,500);
    ui->textBrowser->setFixedSize(700,500);
    ui->textBrowser->setFont(QFont("SimSun",17));

    connect(this,SIGNAL(colorChoosed(QColor)),this,SLOT(setLineMessage(QColor)));

    connect(this,&TabWidget::lineAdded,this,[=](){
        updataLinesList(ui->listWidget);
        updataLinesList(ui->listWidget_2);
    });

    connect(this,&TabWidget::stationAdded,this,&TabWidget::updateAllStationsItem);

    updataLinesList(ui->listWidget);
    updataLinesList(ui->listWidget_2);

    updateAllStationsItem();


}

TabWidget::~TabWidget()
{
    delete ui;
}

void TabWidget::on_colorDlg_clicked()
{
    QColor color = QColorDialog::getColor();
    QBrush brush(color);
    QRect rect(0,0,ui->color->width(),ui->color->height());
    QPixmap pix(rect.width(),rect.height());
    QPainter p(&pix);
    p.fillRect(rect,brush);
    ui->color->setText(color.name());
    ui->color->setPixmap(pix);

    emit colorChoosed(color);
}

void TabWidget::setLineMessage(QColor color)
{
    QString lineName = ui->lineName->text();
    QString color_ = color.name();
    ui->lineMessage->setFont(QFont("SimSun",15));
    ui->lineMessage->setText(lineName + QString("\n\n") + color_);

    this->color = color;
    this->lineName = lineName;
}

void TabWidget::on_addLineBtn_clicked()
{
    //qDebug()<<mySubway->getAllLines().size();
    if(mySubway->pushLine(lineName,color)){
        QMessageBox::information(this,"information","添加路线成功!");
        //qDebug()<<mySubway->getAllLines().size();
        emit lineAdded();
    }
    else{
        QMessageBox::warning(this,"warning","已存在相同线路名或颜色，请重新添加！");
    }
}



void TabWidget::updataLinesList(QListWidget*listWidget)
{
    listWidget->clear();
    QList<QString> allLines = mySubway->getAllLines();
    for(auto line : allLines){
        QListWidgetItem *item = new QListWidgetItem(line);
        item->setFlags(item->flags()|Qt::ItemIsUserCheckable);
        item->setCheckState(Qt::Unchecked);
        listWidget->addItem(item);
    }
}

void TabWidget::updateAllStationsItem()
{
    QList<QString> allStationsName = mySubway->getAllStationsName();
    ui->stationsBox1->clear();
    ui->stationsBox1->addItems(allStationsName);
    ui->stationsBox2->clear();
    ui->stationsBox2->addItems(allStationsName);
}



void TabWidget::on_addStationBtn_clicked()
{
    QSet<int>lineSet;
    for(int i = 0;i<ui->listWidget->count();i++){
        if(ui->listWidget->item(i)->checkState() == Qt::Checked){
            lineSet.insert(mySubway->getLineIndex(ui->listWidget->item(i)->text()));
            //qDebug()<<ui->listWidget->item(i)->text();
        }
    }
    if(lineSet.size() == 0){
        QMessageBox::warning(this,"warning","您未选择所属线路，请重新添加！");
        return;
    }
    QString stationName = ui->stationNameEdit->text();
    double longi = ui->longiEdit->value();
    double lati = ui->latiEdit->value();

    if(mySubway->pushStation(lineSet,stationName,longi,lati)){
        QMessageBox::information(this,"information","添加站点成功!");
        emit stationAdded();
    }
    else{
        QMessageBox::warning(this,"warning","存在相同站点名或相同位置，请重新添加!");
    }

}

void TabWidget::on_addEdgeBtn_clicked()
{
    QList<int>lineIndex;
    for(int i = 0;i<ui->listWidget_2->count();i++){
        if(ui->listWidget_2->item(i)->checkState()==Qt::Checked){
            lineIndex.push_back(mySubway->getLineIndex(ui->listWidget_2->item(i)->text()));
            //qDebug()<<ui->listWidget_2->item(i)->text();
        }
    }
    if(lineIndex.size() == 0){
        QMessageBox::information(this,"warning","您未选择所属线路，请重新添加！");
        return;
    }
    Edge edge;
    edge.first = mySubway->getStationIndex(ui->stationsBox1->currentText());
    edge.second = mySubway->getStationIndex(ui->stationsBox2->currentText());
    //qDebug()<<edge.first<<"  "<<edge.second;
    if(mySubway->pushEdge(lineIndex,edge)){
        emit edgeAdded();
        QMessageBox::information(this,"information","连接关系添加成功！");
    }
    else{
        QMessageBox::warning(this,"warning","该连接关系已存在，请重新添加！");
    }
}

#include "mainwindow.h"

#include <QApplication>
#include <QDateTime>
#include <QSplashScreen>


int main(int argc, char *argv[])
{ 

    QApplication a(argc, argv);

    QPixmap pixmap(":/icon/icon/Metro.jpeg");
    QSplashScreen screen(pixmap);
    screen.show();

    QDateTime n=QDateTime::currentDateTime();
    QDateTime now;
    do{
        now=QDateTime::currentDateTime();
    } while (n.secsTo(now)<=1);//延时1秒

    MainWindow w;
    w.show();
    return a.exec();
}

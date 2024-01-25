
#include "algraph.h"
#include <QFile>
#include <QTextStream>
//#include<QDebug>


MatrixGraph::MatrixGraph()
{
    vertexNum = 5;
    edgeNum = 6;
    for(int i = 0; i < vertexNum; i++) // 给顶点列表赋初值
        vexs[i] = char('a' + i);
    for(int i = 0; i < vertexNum; i++){  // 边邻接矩阵赋值为false
        for(int j = 0; j < vertexNum; j++)
            arc[i][j] = false;
    }
    arc[0][1] = true;
    arc[0][2] = true;
    arc[1][3] = true;
    arc[2][4] = true;
    arc[2][3] = true;
    arc[3][4] = true;
}

void MatrixGraph::print()
{
    QString str = QString("");
    for(int i = 0; i < vertexNum; i++){
        str += QString(vexs[i]) + " ";
    }
    //qDebug()<<str;
    str = "";
    for(int i = 0; i <vertexNum; i++){
        for(int j = 0; j < vertexNum; j++){
            str += QString::number(arc[i][j]) + QString(" ");
        }
        //qDebug()<<str;
        str = QString("");
    }
}

int MatrixGraph::LocateVex(VertexType v)
{
    for(int i = 0; i < vertexNum; i++){
        if(vexs[i] == v)
            return i;
    }
    return -1;
}

bool MatrixGraph::makeMatrixGraph(QString fileName)
{
    char temp;

    QFile file(fileName);
    if(!file.open(QIODevice::ReadOnly | QIODevice::Text))
        return false;
    QTextStream in(&file);
    while(!in.atEnd()){
        in >> vertexNum;
        //qDebug()<<vertexNum;
        if(vertexNum > 20){  // 顶点数限制
            file.close();
            return false;
        }
        for(int i = 0; i < vertexNum; i++){       // 边邻接矩阵赋值为false
            for(int j = 0; j < vertexNum; j++){
                arc[i][j] = false;
            }
        }
        in >> edgeNum;
        //qDebug()<<edgeNum;
        in>>temp;  // 读取\n
        for(int i = 0; i < vertexNum; i++){
            in >> vexs[i]>>temp;
            //qDebug()<<vexs[i];
        }
        for(int i = 0; i < edgeNum; i++){
            char v1, v2;
            in>>v1>>temp>>v2>>temp;
            int k, j;
            k = LocateVex(v1);
            j = LocateVex(v2);
            if(k==-1 || j==-1){
                //qDebug()<<"顶点不存在";
                return false;
            }
            arc[k][j] = true;
        }
        file.close();
        return true;
    }
    file.close();
    return false;
}




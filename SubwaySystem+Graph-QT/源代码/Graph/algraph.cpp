#include "algraph.h"
#include <QApplication>
//#include<QDebug>
#include <QElapsedTimer>
#include <QEventLoop>
#include <QTime>


ALGraph::ALGraph(QObject *parent) : QObject(parent)
{
    vexnum = 0;
    arcnum = 0;
    for (int i = 0; i < MAX_VEX_NUM; i++) {
        vexs_L[i].data = -1; //初始值置为-1
        vexs_L[i].firstarc = nullptr;
    }
    return;

}

//析构函数
ALGraph::~ALGraph() {
    ArcNode* p;
    ArcNode* t;
    for (int i = 0; i < vexnum; i++) {
        p = vexs_L[i].firstarc;
        vexs_L[i].firstarc = nullptr;
        while (p != nullptr) {
            t = p;
            p = p->nextarc;
            delete t;  //释放内存
        }
    }
    return;
}

void ALGraph::clear()
{
    ArcNode* p;
    ArcNode* t;
    for (int i = 0; i < vexnum; i++) {
        p = vexs_L[i].firstarc;
        vexs_L[i].firstarc = nullptr;
        while (p != nullptr) {
            t = p;
            p = p->nextarc;
            delete t;  //释放内存
        }
    }
    return;
}

int ALGraph::LocateVex(VertexType v) {
    for(int i = 0; i < vexnum; i++){
        if(vexs_L[i].data == v)
            return i;
    }
    return -1;
}


//功能：根据邻接矩阵构造图的邻接表结构
//参数 无
//返回值 void
status ALGraph::CreateG(MatrixGraph *MGraph) {
    clear();
    this->vexnum = MGraph->vertexNum;
    this->arcnum = MGraph->edgeNum;

    for (int i = 0; i < vexnum; i++)
        vexs_L[i].data =   MGraph->vexs[i];

    ArcNode* arc; //弧节点工作空间
    VertexType v1, v2; //顶点
    for(int i = 0; i < this->vexnum; i++){
        for(int j = 0; j < this->vexnum; j++){
            if(MGraph->arc[i][j]==true){
                v1 = i;
                v2 = j;

                arc = new ArcNode; //申请一个弧节点内存
                if (!arc)exit(_OVERFLOW_);
                arc->adjvex = j;
                if (vexs_L[i].firstarc==nullptr) {
                    arc->nextarc = vexs_L[i].firstarc;
                    vexs_L[i].firstarc = arc;
                }
                else {
                    ArcNode* temp = vexs_L[i].firstarc;
                    while ((temp->nextarc) != nullptr)  //尾插法插入弧
                        temp = temp->nextarc;
                    arc->nextarc = nullptr;
                    temp->nextarc = arc;
                }
            }
        }
    }
    return OK;
}

//功能：打印邻接表
//返回值 void
void ALGraph::Print() {
    QString str = "";
    for (int i = 0; i < vexnum; i++) {  //打印邻接表
        str += QString(vexs_L[i].data);
        ArcNode* p = vexs_L[i].firstarc;
        while (p != NULL) {
            str += "-->" + QString::number(p->adjvex);
            p = p->nextarc;
        }
        // qDebug()<<str;
        str = "";
    }
    return;
}


//功能：深度优先访问
//参数：无
//返回值 bool
bool ALGraph::DFSRecursion(VertexType v) {
    int k = LocateVex(v);
    if(k == -1){  // 没有该顶点
        // qDebug()<<"不存在该顶点";
        return false;
    }
    for (int i = 0; i < vexnum; ++i){
        visited[i] = 0;
    }

    DFS(k);
    for (int i = 0; i < vexnum; i++) {  //找到一个未被访问的顶点
        if (visited[i] == 0) {
            DFS(i);  //下标即为顶点位置
        }
    }
    return true;
}

//功能：深度优先访问（递归
//参数：待访问的顶点位置
//返回值 void
void ALGraph::DFS(int vertexIndex) {
    ArcNode* p;
    // qDebug() << vertexIndex << " " <<vexs_L[vertexIndex].data;
    visited[vertexIndex] = 1;  //已被访问标记

    emit nodeIVisited(vertexIndex);
    sleep(delayTime);
    emit nodeIVisited(-1);

    p = vexs_L[vertexIndex].firstarc;
    while (p != NULL) {
        if (visited[p->adjvex] == 0) {
            DFS(p->adjvex);  //深度优先-递归
        }
        p = p->nextarc;
    }
    return;
}

bool ALGraph::DFSNonRecursion(VertexType v)
{
    int k = LocateVex(v);
    if(k == -1){  // 没有该顶点
        // qDebug()<<"不存在该顶点";
        return false;
    }
    for (int i = 0; i < vexnum; ++i)
        visited[i] = 0;
    DFS2(k);
    for (int i = 0; i < vexnum; i++) {  //找到一个未被访问的顶点
        if (visited[i] == 0) {
            DFS2(i);  //下标即为顶点位置
        }
    }
    return true;

}

void ALGraph::DFS2(int vertexIndex)
{
    int stack[MAX_VEX_NUM];
    int top = -1;
    emit stackChanged(stack,top);
    sleep(delayTime);

    int j, k;
    ArcNode *p;
    visited[vertexIndex] = true;

    emit nodeIVisited(vertexIndex);
    sleep(delayTime);
    emit nodeIVisited(-1);

    // qDebug()<< vertexIndex << " " << vexs_L[vertexIndex].data;
    stack[++top] = vertexIndex;
    emit stackChanged(stack,top);
    sleep(delayTime);
    while(top!=-1){
        j = stack[top];
        p = this->vexs_L[j].firstarc;
        while(p!=nullptr){
            while(p!=nullptr && visited[p->adjvex] ==1)
                p = p->nextarc;
            if(p == nullptr){
                break;
            }
            k = p->adjvex;
            stack[++top] = k;
            emit stackChanged(stack,top);
            sleep(delayTime);
            visited[k] = true;

            emit nodeIVisited(k);
            sleep(delayTime);
            emit nodeIVisited(-1);

            // qDebug()<< k << " " <<vexs_L[k].data;

            p = this->vexs_L[k].firstarc;
        }
        --top;
        emit stackChanged(stack,top);
        sleep(delayTime);
    }
}

bool ALGraph::BFSTraverse(VertexType v) {
    int k = LocateVex(v);
    if(k == -1){  // 没有该顶点
        // qDebug()<<"不存在该顶点";
        return false;
    }
    for (int i = 0; i < vexnum; i++)
        visited[i] = 0;
    BFS(k);
    for (int i = 0; i < vexnum; i++)   //找到一个未被访问的顶点
        if (visited[i] == 0) {
            BFS(i);  //下标即为顶点位置
        }
    return true;
}

void ALGraph::BFS(int vertexIndex) {
    ArcNode* p;
    int* Q = new int[vexnum];  //辅助循环队列
    int rear = 0, front = 0;  //队列头尾位置
    emit queueChanged(Q,front,rear);
    sleep(delayTime);

    // qDebug()<< vertexIndex << " "  << vexs_L[vertexIndex].data;
    visited[vertexIndex] = 1; //已被访问标记

    emit nodeIVisited(vertexIndex);
    sleep(delayTime);
    emit nodeIVisited(-1);

    Q[rear] = vertexIndex;  //访问过的顶点入队
    rear = (rear + 1) % vexnum;
    emit queueChanged(Q,front,rear);
    sleep(delayTime);

    while (rear != front) { //队不空
        vertexIndex = Q[front];  //出队
        front = (front + 1) % vexnum;
        emit queueChanged(Q,front,rear);
        sleep(delayTime);
        p = vexs_L[vertexIndex].firstarc;  //访问该顶点的第一个邻接顶点
        while (p != nullptr) {
            if (visited[p->adjvex] == 0) {  //如果未被访问过
                // qDebug() << p->adjvex << " " <<vexs_L[p->adjvex].data;
                emit nodeIVisited(p->adjvex);
                sleep(delayTime);
                emit nodeIVisited(-1);

                visited[p->adjvex] = 1; //已被访问标记


                Q[rear] = p->adjvex;  //访问过的顶点入队
                rear = (rear + 1) % vexnum;
                emit queueChanged(Q,front,rear);
                sleep(delayTime);
            }
            p = p->nextarc;
        }
    }
    delete[]Q;
    return;
}

void ALGraph::sleep(int sectime)
{
    QTime dieTime = QTime::currentTime().addMSecs(sectime);

    while (QTime::currentTime() < dieTime) {
        QCoreApplication::processEvents(QEventLoop::AllEvents, 100);
    }
}

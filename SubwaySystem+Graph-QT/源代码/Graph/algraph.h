#ifndef ALGRAPH_H
#define ALGRAPH_H

#include <QObject>
#include"matrixgraph.h"

#define OK          1
#define ERROR       0
#define TURE        1
#define FLASE       0
#define _OVERFLOW_ -1
typedef int status;

//邻接表的弧节点的存储结构
typedef struct ArcNode {
    int adjvex;   // 该弧指向的顶点的位置
    struct ArcNode* nextarc;   // 指向下一条弧的指针
}ArcNode;

//邻接表的顶点节点的存储结构
typedef struct VNode {
    VertexType data;
    ArcNode* firstarc;  // 指向第一条依附于该顶点的指针
}VNode,AdjList[MAX_VEX_NUM];

class ALGraph : public QObject
{
    Q_OBJECT
private:
    int vexnum, arcnum;   // 图的当前顶点数和弧数
    AdjList vexs_L;    // 邻接表的顶点向量
    bool visited[MAX_VEX_NUM];  // 标记已访问的顶点
    int delayTime = 200;  // 遍历时的延迟时间
public:  
    explicit ALGraph(QObject *parent = nullptr);  // 构造函数
    ~ALGraph();  // 析构函数：回收动态内存申请的空间
    void clear();  // 建立新图前删除指针，回收内存
    int LocateVex(VertexType v);  // 定位一个顶点的位置
    status CreateG(MatrixGraph* MGraph);  // 根据邻接矩阵构造图的临界链表
    void Print(); // 打印邻接表（用于调试）
    bool DFSRecursion(VertexType v);  // 从顶点v开始深度优先遍历
    // 功能：深度优先访问（递归
    // 参数：待访问的顶点位置
    void DFS(int vertexIndex);
    // 从顶点v开始非递归深度优先遍历
    bool DFSNonRecursion(VertexType v);
    // 功能：深度优先访问（非递归
    // 参数：待访问的顶点位置
    void DFS2(int vertexIndex); 
    bool BFSTraverse(VertexType v); // 从顶点v开始广度优先遍历
    // 广度优先遍历
    // 参数：待访问的顶点位置
    void BFS(int vertexIndex);
    void sleep(int sectime);  // 延时函数
friend class MainWindow;
signals:
    void nodeIVisited(int i);   // 发出顶点I被访问的信号
    void stackChanged(int *stack,int top);   // 发出栈更新的信号
    void queueChanged(int *queue,int front, int rear);  // 发出队列更新的信号
};

#endif // ALGRAPH_H

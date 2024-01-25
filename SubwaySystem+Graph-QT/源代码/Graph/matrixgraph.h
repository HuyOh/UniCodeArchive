#ifndef MATRIXGRAPH_H
#define MATRIXGRAPH_H

#include <QString>


#define MAX_VEX_NUM 20
typedef char VertexType;     // 顶点类型
typedef bool EdgeType;       // 无权图

class MatrixGraph
{
private:
    VertexType vexs[MAX_VEX_NUM]; // 顶点列表
    EdgeType arc[MAX_VEX_NUM][MAX_VEX_NUM]; // 邻接矩阵
    int vertexNum; // 当前顶点数
    int edgeNum;   // 当前边数
public:
    MatrixGraph();   // 构造函数，初始化了一个图
    void print();    // 打印邻接矩阵结构
    int LocateVex(VertexType v); // 功能：定位一个顶点的位置
    bool makeMatrixGraph(QString fileName);  // 读取文本文件并构造图
friend class ALGraph;
};

#endif // MATRIXGRAPH_H

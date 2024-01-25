#include "subwaygraph.h"
#include<QFile>
#include <QTextStream>
#include<queue>
//#include<QDebug>

// 生成图的邻接表
void SubwayGraph::makeGraph()
{
    graph.clear();
    graph = QVector<QVector<Node>>(stations.size(),QVector<Node>());
    for(Edge temp : edges){
        double distance_ = stations[temp.first].distance(stations[temp.second]);
        graph[temp.first].push_back(Node(temp.second,distance_));
        graph[temp.second].push_back(Node(temp.first,distance_));
    }
}

// 获取线路名Key在lineHash中的value
int SubwayGraph::getLineIndex(QString lineName)
{
    return lineHash[lineName];
}

// 获取站点名Key在stationHash中的calue
int SubwayGraph::getStationIndex(QString stationName)
{
    return stationHash[stationName];
}

bool SubwayGraph::readData(QString fileName)
{
/* 数据格式
id: 1
name: 1号线
colour: #E70012
fromTo: 富锦路 莘庄
totalStations: 28
1 富锦路	121.424661,31.39226
2 友谊西路	121.427726,31.381227
3 宝安公路	121.430975,31.369369
4 共富新村	121.433936,31.355004
5 呼兰路	121.437711,31.339703
6 通河新村	121.441498,31.331094
7 共康路	121.447455,31.318642
8 彭浦新村	121.448141,31.305883
9 汶水路	121.449858,31.292242
10 上海马戏城	121.452004,31.279846
11 延长路	121.455265,31.271409
12 中山北路	121.459128,31.258717
13 上海火车站	121.455523,31.249692
14 汉中路	121.459128,31.2414
15 新闸路	121.467882,31.238538
16 人民广场	121.472989,31.232814
17 黄陂南路	121.47329,31.222502
18 陕西南路	121.460115,31.217107
19 常熟路	121.451059,31.213033
20 衡山路	121.446725,31.20426
21 徐家汇	121.438056,31.191522
22 上海体育馆	121.436511,31.181903
23 漕宝路	121.43458,31.168097
24 上海南站	121.43046,31.154693
25 锦江乐园	121.414324,31.142059
26 莲花路	121.402994,31.130929
27 外环路	121.393167,31.120936
28 莘庄	121.385184,31.111237
*/
    QFile file(fileName);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
        return false;

    QTextStream in(&file);
    while (!in.atEnd()) {
        // 用于接收数据
        QString id, name, colour, color, totalStations, fromto, from, to;
        int stationNums;        // 每一条地铁线路的总站点数
        bool ok;                // 用于QString.toUInt()函数传参
        Line line;              // 实例化Line对象

        in>>id>>line.id;
        in>>name>>line.name;
        in>>colour>>color;
        int color_ = color.remove(0,1).toUInt(&ok,16);
        line.color.setRgba(color_);
        in>>fromto>>from>>to;
        in>>totalStations>>stationNums;

        int index1, index2, lastIndex; // 分别为地铁线和站点名在地铁站在lines和stations中的索引

        // 同一条地铁线可能有两条或两条以上线路。例如11号线，终点站分别为嘉定北和花桥。
        if(this->lineHash.contains(line.name)){
            index1 = this->lineHash[line.name];
        }
        else{
            // 哈希表的key（name）映射到line在vector<line>lines中的索引
            this->lineHash.insert(line.name, this->lines.size());
            index1 = this->lines.size();
            this->lines.push_back(line);
        }

        QString pos;
        for(int i=0;!in.atEnd()&&i<stationNums;i++){
            Station station;
            in>>station.id>>station.name>>pos;
            station.longitude = pos.split(",").first().toDouble();
            station.latitude = pos.split(",").last().toDouble();

            this->updatePos(station.longitude, station.latitude);

            if(this->stationHash.contains(station.name)){
                // 出现过相同站点
                index2 = this->stationHash[station.name];
            }
            else{
                // 哈希表的key（name）映射到station在vector<station>station中的索引
                this->stationHash[station.name] = this->stations.size();
                index2 = this->stations.size();
                this->stations.push_back(station);
            }

            this->lines[index1].stationSet.insert(index2);
            this->stations[index2].linesSet.insert(index1);

            if(i!=0){
                this->lines[index1].edges.insert(Edge(index2,lastIndex));
                this->lines[index1].edges.insert(Edge(lastIndex,index2));
                this->insertEdge(index2,lastIndex);
            }
            lastIndex = index2;
        }

        // 检查是否出现非法操作，是则清空所有数据
        bool flag = id=="id:" && name=="name:" && colour=="colour:"
                && fromto=="fromTo:" && totalStations=="totalStations:"
                && ok && !in.atEnd();

        if(!flag){
            this->clearData();
            file.close();
            return false;
        }
        in.readLine();    //读取一空行
    }
    file.close();

    this->makeGraph();
    return true;
}

// 更新所有站点的边界经纬度
void SubwayGraph::updatePos(double lng, double lat)
{
    Station::maxLongitude = qMax(Station::maxLongitude, lng);
    Station::minLongitude = qMin(Station::minLongitude, lng);
    Station::maxLatitude = qMax(Station::maxLatitude, lat);
    Station::minLatitude = qMin(Station::minLatitude, lat);
}

// 往edges插入一条边，(1,2)和（2,1）不重复插入
bool SubwayGraph::insertEdge(int first, int last)
{
    if(edges.contains(Edge(first,last))||edges.contains(Edge(last,first)))
        return false;
    else
        edges.insert(Edge(first,last));
    return true;
}

// 清除数据
void SubwayGraph::clearData()
{
    this->edges.clear();
    this->lines.clear();
    this->stations.clear();
    this->stationHash.clear();
    this->lineHash.clear();
    this->graph.clear();
}

// djstl算法求最短时间路线
bool SubwayGraph::transferMinTime(int start, int end, QList<int> &stationsList, QList<Edge> &edgesList)
{
    stationsList.clear();
    edgesList.clear();

    if(start==end){
        stationsList.push_back(end);
        stationsList.push_back(start);
        return true;
    }

    //djstl算法开始

    std::vector<int>path(stations.size(),-1);   // 路径更新辅助空间
    std::vector<double>distance(stations.size(),INFINITY); // 距离更新辅助空间

    distance[start]=0;
    std::priority_queue<Node,std::vector<Node>,std::greater<Node>>queue;
    queue.push(Node(start,0));

    while(!queue.empty()){
        auto top = queue.top();
        queue.pop();

        if(top.id==end)  // 找到了到达end站的最短路径
            break;

        for(int i=0;i<graph[top.id].size();i++){
            auto temp = graph[top.id][i];
            if(distance[top.id]+temp.distance<distance[temp.id]){
                distance[temp.id] = distance[top.id]+temp.distance;
                path[temp.id] = top.id;
                queue.push(Node(temp.id, distance[temp.id]));
            }
        }
    }

    if(path[end]==-1){   //无法到达目的地
        return false;
    }

    int k = end;
    while(path[k]!=-1){
        stationsList.push_front(k);
        edgesList.push_front(Edge(path[k],k));
        k = path[k];
    }
    stationsList.push_front(start);

    return true;
}


// 求最少换乘路线
bool SubwayGraph::transferMinTransfer(int start, int end, QList<int> &stationsList, QList<Edge> &edgesList)
{
    stationsList.clear();
    edgesList.clear();

    if(start==end){
        stationsList.push_back(end);
        stationsList.push_back(start);
        return true;
    }

    std::vector<bool>visited(lines.size(),false);  // 记录换乘过的线路
    std::vector<int>path(stations.size(),-1);
    path[start] = -2;
    std::queue<int>queue;
    queue.push(start);

    while (!queue.empty()) {
        int top = queue.front();
        queue.pop();
        for(auto l : stations[top].linesSet){
            if(!visited[l]){
                visited[l] = true;
                for(auto s:lines[l].stationSet){
                    if(path[s]==-1){
                        path[s] = top;
                        queue.push(s);
                    }
                }
            }
        }
    }

    if(path[end]==-1){
        return false;
    }

    int k = end;
    while(path[k]!=-2){
        stationsList.push_front(k);
        edgesList.push_front(Edge(path[k],k));
        k = path[k];
    }
    stationsList.push_front(start);

    return true;
}

bool SubwayGraph::transferMinStation(int start, int end, QList<int> &stationsList, QList<Edge> &edgesList)
{
    stationsList.clear();
    edgesList.clear();

    if(start==end){
        stationsList.push_back(end);
        stationsList.push_back(start);
        return true;
    }

    //djstl算法开始

    std::vector<int>path(stations.size(),-1);   // 路径更新辅助空间
    std::vector<int>stationsNum(stations.size(),10000); // 距离更新辅助空间

    stationsNum[start]=0;
    std::priority_queue<Node,std::vector<Node>,std::greater<Node>>queue;
    queue.push(Node(start,0));

    while(!queue.empty()){
        auto top = queue.top();
        queue.pop();

        if(top.id==end)  // 找到了到达end站的最短路径
            break;

        for(int i=0;i<graph[top.id].size();i++){
            auto temp = graph[top.id][i];
            if(stationsNum[top.id]+1 < stationsNum[temp.id]){
                stationsNum[temp.id] = stationsNum[top.id]+1;
                path[temp.id] = top.id;
                queue.push(Node(temp.id, stationsNum[temp.id]));
            }
        }
    }

    if(path[end]==-1){   //无法到达目的地
        return false;
    }

    int k = end;
    while(path[k]!=-1){
        stationsList.push_front(k);
        edgesList.push_front(Edge(path[k],k));
        k = path[k];
    }
    stationsList.push_front(start);

    return true;

}

QList<QString> SubwayGraph::getStations(QList<int> stationsIndexList)
{
    QList<QString>stationsList;
    for(int i=0;i<stationsIndexList.size();i++){
        stationsList.push_back(stations[stationsIndexList[i]].name);
    }
    return stationsList;
}

QList<QString> SubwayGraph::getLines(QString stationName)
{
    int i = getStationIndex(stationName);  //  获取站点名的哈希值
    QList<QString> linesName;
    for(auto j : stations[i].linesSet){
        linesName.push_back(lines[j].name);
    }
    return linesName;
}

QList<QString> SubwayGraph::getAllLines()
{
    QList<QString> allLines;
    for(auto line : lines){
        allLines.push_back(line.name);
    }
    return allLines;
}

QList<int> SubwayGraph::getLinesOfEdge(Edge edge)
{
    QList<int> linesIndex;
    int a1 = edge.first, a2 = edge.second;
    for(auto i : stations[a1].linesSet){
        if(stations[a2].linesSet.contains(i))
            linesIndex.push_back(i);
    }
    return linesIndex;
}

// 当一条边属于多条线路时，使用正片叠底的混色模式确定边的颜色
QColor SubwayGraph::getEdgeColor(QList<int> linesIndex)
{
    QColor color1(255,255,255);
    QColor color2;
    for(auto i : linesIndex){
        color2 = lines[i].color;
        color1.setRed(color1.red()*color2.red()/255);
        color1.setGreen(color1.green()*color2.green()/255);
        color1.setBlue(color1.blue()*color2.blue()/255);
    }
    return color1;
}

double SubwayGraph::minLongitude()
{
    return Station::minLongitude;
}

double SubwayGraph::minLatitude()
{
    return Station::minLatitude;
}

double SubwayGraph::maxLongitude()
{
    return Station::maxLongitude;
}

double SubwayGraph::maxLatitude()
{
    return Station::maxLatitude;
}

double SubwayGraph::getLatitude(int i)
{
    return stations[i].latitude;
}

QString SubwayGraph::getLineName(int i)
{
    return lines[i].name;
}

QList<Edge> SubwayGraph::getEdges()
{
    return edges.toList();
}

QList<int> SubwayGraph::getAllStationsIndex()
{
    QList<int> stationsIndex;
    for(auto i : stations){
        QString name = i.name;
        stationsIndex.push_back(getStationIndex(name));
    }
    return stationsIndex;
}

QList<QString> SubwayGraph::getAllStationsName()
{
    QList<QString> allStationsName;
    for(auto i : stations){
        allStationsName.push_back(i.name);
    }
    return allStationsName;
}

QList<QString> SubwayGraph::getStationsOfLine(QString lineName)
{
    QList<QString> stationsName;
    int i = getLineIndex(lineName);
    for(auto j : lines[i].stationSet){
        stationsName.push_back(stations[j].name);
    }
    return stationsName;
}

QList<int> SubwayGraph::getLinesIndex(int i)
{
    return stations[i].linesSet.toList();
}

bool SubwayGraph::pushLine(QString lineName, QColor color)
{
    for(auto line : lines){
        if(line.name == lineName || line.color == color){
            return false;
        }
    }
    Line line = Line(lines.size()+1,lineName,color);
    lineHash[lineName] = lines.size();
    lines.push_back(line);
    return true;
}

bool SubwayGraph::pushStation(QSet<int> lineSet, QString name, double longi, double lati)
{
    for(auto station :stations){
        if(station.name==name||(station.longitude==longi && station.latitude==lati))
            return false;
    }
    int id = stations.size();
    stationHash[name] = id;
    Station* station = new Station(name,longi,lati,lineSet.toList());
    station->id = id;
    stations.push_back(*station);
    for(auto i : lineSet){
        lines[i].stationSet.insert(id);
    }
    return true;
}

double SubwayGraph::getLongitude(int i)
{
    return stations[i].longitude;
}

QString SubwayGraph::getStationName(int i)
{
    return stations[i].name;
}

bool SubwayGraph::pushEdge(QList<int> linesIndex, Edge edge)
{

        edges.insert(edge);
        for(auto i : linesIndex){
            if(!lines[i].edges.contains(edge) || !lines[i].edges.contains(Edge(edge.second,edge.first))){
                lines[i].edges.insert(edge);
            }
            if(!lines[i].stationSet.contains(edge.first)){
                lines[i].stationSet.insert(edge.first);
            }
            if(!lines[i].stationSet.contains(edge.second)){
                lines[i].stationSet.insert((edge.second));
            }
            if(!stations[edge.first].linesSet.contains(i)){
                stations[edge.first].linesSet.insert(i);
            }
            if(!stations[edge.second].linesSet.contains(i)){
                stations[edge.second].linesSet.insert(i);
            }
        }
    makeGraph();
    return true;
}



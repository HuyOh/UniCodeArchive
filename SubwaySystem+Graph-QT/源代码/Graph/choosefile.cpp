#include "choosefile.h"
#include "ui_choosefile.h"

chooseFile::chooseFile(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::chooseFile)
{
    ui->setupUi(this);
    this->setWindowIcon(QIcon(":/icon/chooseFile.jpeg"));
    this->setWindowTitle("文件输入需知");
    QString str = "--开始(文本不包含此行)--\n";
    str += "6 10\na b c d e f\na b\na d\na f\nb c\nb d\nb e\nc f\nc e\ne c\nf c\n";
    str += "--结束(文本不包含此行)--\n\n";
    str += "如上例所示，您的文本内容必须符合以下规范：\n";
    str += "1.第一行为顶点数、边数，空格分隔；\n";
    str += "2.第二行为顶点字符，数量为第一行的顶点数，空格分隔；\n";
    str += "3.第三行到文本末为边，行数为第一行的边数，空格分隔：\n";
    str += "4.每一行末尾都没有空格！\n\n";
    str += "若输入不符合规范文本，程序可能发生错误并退出!!!\n";
    ui->noticeBrowser->setFont(QFont("SimSun",10));
    ui->noticeBrowser->setText(str);
}

chooseFile::~chooseFile()
{
    delete ui;
}

void chooseFile::on_comfirmBtn_clicked()
{
    this->close();
    emit chooseFileConfirmed();
}

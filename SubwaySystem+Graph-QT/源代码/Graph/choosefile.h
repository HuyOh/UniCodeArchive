#ifndef CHOOSEFILE_H
#define CHOOSEFILE_H

#include <QWidget>

/*
 * 这是一个提示窗口，给出了输入文本的的格式要求，从此窗口可以进入选择文件对话框。
 * 提示内容在构造函数chooseFile(QWidget *parent = nullptr)中可以做出修改。
*/

namespace Ui {
class chooseFile;
}

class chooseFile : public QWidget
{
    Q_OBJECT

public:
    explicit chooseFile(QWidget *parent = nullptr);
    ~chooseFile();

private slots:
    void on_comfirmBtn_clicked();

private:
    Ui::chooseFile *ui;
signals:
    void chooseFileConfirmed();  // 已知晓文本规范，确认选择文件信号。
};

#endif // CHOOSEFILE_H

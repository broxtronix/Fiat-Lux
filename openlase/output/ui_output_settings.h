/********************************************************************************
** Form generated from reading UI file 'output_settings.ui'
**
** Created: Thu Apr 28 02:38:50 2011
**      by: Qt User Interface Compiler version 4.7.2
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_OUTPUT_SETTINGS_H
#define UI_OUTPUT_SETTINGS_H

#include <QtCore/QVariant>
#include <QtGui/QAction>
#include <QtGui/QApplication>
#include <QtGui/QButtonGroup>
#include <QtGui/QCheckBox>
#include <QtGui/QComboBox>
#include <QtGui/QGraphicsView>
#include <QtGui/QGroupBox>
#include <QtGui/QHBoxLayout>
#include <QtGui/QHeaderView>
#include <QtGui/QLabel>
#include <QtGui/QMainWindow>
#include <QtGui/QMenu>
#include <QtGui/QMenuBar>
#include <QtGui/QPushButton>
#include <QtGui/QSlider>
#include <QtGui/QSpacerItem>
#include <QtGui/QSpinBox>
#include <QtGui/QStatusBar>
#include <QtGui/QVBoxLayout>
#include <QtGui/QWidget>

QT_BEGIN_NAMESPACE

class Ui_OutputSettingsDLG
{
public:
    QAction *actionSaveSettings;
    QAction *actionLoadSettings;
    QAction *actionQuit;
    QWidget *centralwidget;
    QVBoxLayout *verticalLayout_9;
    QHBoxLayout *horizontalLayout_14;
    QGraphicsView *projView;
    QVBoxLayout *verticalLayout_8;
    QPushButton *shutdown;
    QGroupBox *groupBox;
    QVBoxLayout *verticalLayout_6;
    QPushButton *outputTest;
    QCheckBox *outputEnable;
    QCheckBox *blankingEnable;
    QCheckBox *blankingInvert;
    QGroupBox *groupBox_2;
    QVBoxLayout *verticalLayout_7;
    QCheckBox *xEnable;
    QCheckBox *xInvert;
    QCheckBox *yEnable;
    QCheckBox *yInvert;
    QCheckBox *xySwap;
    QComboBox *aspectRatio;
    QCheckBox *aspectScale;
    QCheckBox *fitSquare;
    QPushButton *resetTransform;
    QGroupBox *groupBox_3;
    QVBoxLayout *verticalLayout_5;
    QCheckBox *enforceSafety;
    QSpacerItem *verticalSpacer;
    QGroupBox *groupBox_4;
    QHBoxLayout *horizontalLayout_13;
    QVBoxLayout *verticalLayout;
    QHBoxLayout *horizontalLayout;
    QSpacerItem *horizontalSpacer_5;
    QLabel *label;
    QSpacerItem *horizontalSpacer_6;
    QHBoxLayout *horizontalLayout_2;
    QSpacerItem *horizontalSpacer_3;
    QSpinBox *powerBox;
    QSpacerItem *horizontalSpacer_4;
    QHBoxLayout *horizontalLayout_3;
    QSpacerItem *horizontalSpacer;
    QSlider *powerSlider;
    QSpacerItem *horizontalSpacer_2;
    QVBoxLayout *verticalLayout_2;
    QHBoxLayout *horizontalLayout_4;
    QSpacerItem *horizontalSpacer_7;
    QLabel *label_2;
    QSpacerItem *horizontalSpacer_8;
    QHBoxLayout *horizontalLayout_5;
    QSpacerItem *horizontalSpacer_9;
    QSpinBox *offsetBox;
    QSpacerItem *horizontalSpacer_10;
    QHBoxLayout *horizontalLayout_6;
    QSpacerItem *horizontalSpacer_11;
    QSlider *offsetSlider;
    QSpacerItem *horizontalSpacer_12;
    QVBoxLayout *verticalLayout_3;
    QHBoxLayout *horizontalLayout_7;
    QSpacerItem *horizontalSpacer_13;
    QLabel *label_3;
    QSpacerItem *horizontalSpacer_14;
    QHBoxLayout *horizontalLayout_8;
    QSpacerItem *horizontalSpacer_15;
    QSpinBox *delayBox;
    QSpacerItem *horizontalSpacer_16;
    QHBoxLayout *horizontalLayout_9;
    QSpacerItem *horizontalSpacer_17;
    QSlider *delaySlider;
    QSpacerItem *horizontalSpacer_18;
    QVBoxLayout *verticalLayout_4;
    QHBoxLayout *horizontalLayout_10;
    QSpacerItem *horizontalSpacer_19;
    QLabel *label_4;
    QSpacerItem *horizontalSpacer_20;
    QHBoxLayout *horizontalLayout_11;
    QSpacerItem *horizontalSpacer_21;
    QSpinBox *sizeBox;
    QSpacerItem *horizontalSpacer_22;
    QHBoxLayout *horizontalLayout_12;
    QSpacerItem *horizontalSpacer_23;
    QSlider *sizeSlider;
    QSpacerItem *horizontalSpacer_24;
    QStatusBar *statusbar;
    QMenuBar *menuBar;
    QMenu *menuFile;

    void setupUi(QMainWindow *OutputSettingsDLG)
    {
        if (OutputSettingsDLG->objectName().isEmpty())
            OutputSettingsDLG->setObjectName(QString::fromUtf8("OutputSettingsDLG"));
        OutputSettingsDLG->resize(648, 854);
        OutputSettingsDLG->setDocumentMode(false);
        OutputSettingsDLG->setUnifiedTitleAndToolBarOnMac(false);
        actionSaveSettings = new QAction(OutputSettingsDLG);
        actionSaveSettings->setObjectName(QString::fromUtf8("actionSaveSettings"));
        actionLoadSettings = new QAction(OutputSettingsDLG);
        actionLoadSettings->setObjectName(QString::fromUtf8("actionLoadSettings"));
        actionQuit = new QAction(OutputSettingsDLG);
        actionQuit->setObjectName(QString::fromUtf8("actionQuit"));
        centralwidget = new QWidget(OutputSettingsDLG);
        centralwidget->setObjectName(QString::fromUtf8("centralwidget"));
        verticalLayout_9 = new QVBoxLayout(centralwidget);
        verticalLayout_9->setObjectName(QString::fromUtf8("verticalLayout_9"));
        horizontalLayout_14 = new QHBoxLayout();
        horizontalLayout_14->setObjectName(QString::fromUtf8("horizontalLayout_14"));
        projView = new QGraphicsView(centralwidget);
        projView->setObjectName(QString::fromUtf8("projView"));
        QSizePolicy sizePolicy(QSizePolicy::Expanding, QSizePolicy::Expanding);
        sizePolicy.setHorizontalStretch(0);
        sizePolicy.setVerticalStretch(0);
        sizePolicy.setHeightForWidth(projView->sizePolicy().hasHeightForWidth());
        projView->setSizePolicy(sizePolicy);

        horizontalLayout_14->addWidget(projView);

        verticalLayout_8 = new QVBoxLayout();
        verticalLayout_8->setObjectName(QString::fromUtf8("verticalLayout_8"));
        shutdown = new QPushButton(centralwidget);
        shutdown->setObjectName(QString::fromUtf8("shutdown"));

        verticalLayout_8->addWidget(shutdown);

        groupBox = new QGroupBox(centralwidget);
        groupBox->setObjectName(QString::fromUtf8("groupBox"));
        verticalLayout_6 = new QVBoxLayout(groupBox);
        verticalLayout_6->setObjectName(QString::fromUtf8("verticalLayout_6"));
        outputTest = new QPushButton(groupBox);
        outputTest->setObjectName(QString::fromUtf8("outputTest"));

        verticalLayout_6->addWidget(outputTest);

        outputEnable = new QCheckBox(groupBox);
        outputEnable->setObjectName(QString::fromUtf8("outputEnable"));

        verticalLayout_6->addWidget(outputEnable);

        blankingEnable = new QCheckBox(groupBox);
        blankingEnable->setObjectName(QString::fromUtf8("blankingEnable"));

        verticalLayout_6->addWidget(blankingEnable);

        blankingInvert = new QCheckBox(groupBox);
        blankingInvert->setObjectName(QString::fromUtf8("blankingInvert"));

        verticalLayout_6->addWidget(blankingInvert);


        verticalLayout_8->addWidget(groupBox);

        groupBox_2 = new QGroupBox(centralwidget);
        groupBox_2->setObjectName(QString::fromUtf8("groupBox_2"));
        verticalLayout_7 = new QVBoxLayout(groupBox_2);
        verticalLayout_7->setObjectName(QString::fromUtf8("verticalLayout_7"));
        xEnable = new QCheckBox(groupBox_2);
        xEnable->setObjectName(QString::fromUtf8("xEnable"));

        verticalLayout_7->addWidget(xEnable);

        xInvert = new QCheckBox(groupBox_2);
        xInvert->setObjectName(QString::fromUtf8("xInvert"));

        verticalLayout_7->addWidget(xInvert);

        yEnable = new QCheckBox(groupBox_2);
        yEnable->setObjectName(QString::fromUtf8("yEnable"));

        verticalLayout_7->addWidget(yEnable);

        yInvert = new QCheckBox(groupBox_2);
        yInvert->setObjectName(QString::fromUtf8("yInvert"));

        verticalLayout_7->addWidget(yInvert);

        xySwap = new QCheckBox(groupBox_2);
        xySwap->setObjectName(QString::fromUtf8("xySwap"));

        verticalLayout_7->addWidget(xySwap);

        aspectRatio = new QComboBox(groupBox_2);
        aspectRatio->setObjectName(QString::fromUtf8("aspectRatio"));

        verticalLayout_7->addWidget(aspectRatio);

        aspectScale = new QCheckBox(groupBox_2);
        aspectScale->setObjectName(QString::fromUtf8("aspectScale"));

        verticalLayout_7->addWidget(aspectScale);

        fitSquare = new QCheckBox(groupBox_2);
        fitSquare->setObjectName(QString::fromUtf8("fitSquare"));

        verticalLayout_7->addWidget(fitSquare);

        resetTransform = new QPushButton(groupBox_2);
        resetTransform->setObjectName(QString::fromUtf8("resetTransform"));

        verticalLayout_7->addWidget(resetTransform);


        verticalLayout_8->addWidget(groupBox_2);

        groupBox_3 = new QGroupBox(centralwidget);
        groupBox_3->setObjectName(QString::fromUtf8("groupBox_3"));
        verticalLayout_5 = new QVBoxLayout(groupBox_3);
        verticalLayout_5->setObjectName(QString::fromUtf8("verticalLayout_5"));
        enforceSafety = new QCheckBox(groupBox_3);
        enforceSafety->setObjectName(QString::fromUtf8("enforceSafety"));

        verticalLayout_5->addWidget(enforceSafety);

        verticalSpacer = new QSpacerItem(20, 0, QSizePolicy::Minimum, QSizePolicy::Expanding);

        verticalLayout_5->addItem(verticalSpacer);


        verticalLayout_8->addWidget(groupBox_3);


        horizontalLayout_14->addLayout(verticalLayout_8);


        verticalLayout_9->addLayout(horizontalLayout_14);

        groupBox_4 = new QGroupBox(centralwidget);
        groupBox_4->setObjectName(QString::fromUtf8("groupBox_4"));
        horizontalLayout_13 = new QHBoxLayout(groupBox_4);
        horizontalLayout_13->setObjectName(QString::fromUtf8("horizontalLayout_13"));
        verticalLayout = new QVBoxLayout();
        verticalLayout->setObjectName(QString::fromUtf8("verticalLayout"));
        horizontalLayout = new QHBoxLayout();
        horizontalLayout->setObjectName(QString::fromUtf8("horizontalLayout"));
        horizontalSpacer_5 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout->addItem(horizontalSpacer_5);

        label = new QLabel(groupBox_4);
        label->setObjectName(QString::fromUtf8("label"));

        horizontalLayout->addWidget(label);

        horizontalSpacer_6 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout->addItem(horizontalSpacer_6);


        verticalLayout->addLayout(horizontalLayout);

        horizontalLayout_2 = new QHBoxLayout();
        horizontalLayout_2->setObjectName(QString::fromUtf8("horizontalLayout_2"));
        horizontalSpacer_3 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout_2->addItem(horizontalSpacer_3);

        powerBox = new QSpinBox(groupBox_4);
        powerBox->setObjectName(QString::fromUtf8("powerBox"));
        powerBox->setMaximum(100);

        horizontalLayout_2->addWidget(powerBox);

        horizontalSpacer_4 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout_2->addItem(horizontalSpacer_4);


        verticalLayout->addLayout(horizontalLayout_2);

        horizontalLayout_3 = new QHBoxLayout();
        horizontalLayout_3->setObjectName(QString::fromUtf8("horizontalLayout_3"));
        horizontalSpacer = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout_3->addItem(horizontalSpacer);

        powerSlider = new QSlider(groupBox_4);
        powerSlider->setObjectName(QString::fromUtf8("powerSlider"));
        powerSlider->setMaximum(100);
        powerSlider->setOrientation(Qt::Vertical);

        horizontalLayout_3->addWidget(powerSlider);

        horizontalSpacer_2 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout_3->addItem(horizontalSpacer_2);


        verticalLayout->addLayout(horizontalLayout_3);


        horizontalLayout_13->addLayout(verticalLayout);

        verticalLayout_2 = new QVBoxLayout();
        verticalLayout_2->setObjectName(QString::fromUtf8("verticalLayout_2"));
        horizontalLayout_4 = new QHBoxLayout();
        horizontalLayout_4->setObjectName(QString::fromUtf8("horizontalLayout_4"));
        horizontalSpacer_7 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout_4->addItem(horizontalSpacer_7);

        label_2 = new QLabel(groupBox_4);
        label_2->setObjectName(QString::fromUtf8("label_2"));

        horizontalLayout_4->addWidget(label_2);

        horizontalSpacer_8 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout_4->addItem(horizontalSpacer_8);


        verticalLayout_2->addLayout(horizontalLayout_4);

        horizontalLayout_5 = new QHBoxLayout();
        horizontalLayout_5->setObjectName(QString::fromUtf8("horizontalLayout_5"));
        horizontalSpacer_9 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout_5->addItem(horizontalSpacer_9);

        offsetBox = new QSpinBox(groupBox_4);
        offsetBox->setObjectName(QString::fromUtf8("offsetBox"));
        offsetBox->setMaximum(100);

        horizontalLayout_5->addWidget(offsetBox);

        horizontalSpacer_10 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout_5->addItem(horizontalSpacer_10);


        verticalLayout_2->addLayout(horizontalLayout_5);

        horizontalLayout_6 = new QHBoxLayout();
        horizontalLayout_6->setObjectName(QString::fromUtf8("horizontalLayout_6"));
        horizontalSpacer_11 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout_6->addItem(horizontalSpacer_11);

        offsetSlider = new QSlider(groupBox_4);
        offsetSlider->setObjectName(QString::fromUtf8("offsetSlider"));
        offsetSlider->setMaximum(100);
        offsetSlider->setOrientation(Qt::Vertical);

        horizontalLayout_6->addWidget(offsetSlider);

        horizontalSpacer_12 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout_6->addItem(horizontalSpacer_12);


        verticalLayout_2->addLayout(horizontalLayout_6);


        horizontalLayout_13->addLayout(verticalLayout_2);

        verticalLayout_3 = new QVBoxLayout();
        verticalLayout_3->setObjectName(QString::fromUtf8("verticalLayout_3"));
        horizontalLayout_7 = new QHBoxLayout();
        horizontalLayout_7->setObjectName(QString::fromUtf8("horizontalLayout_7"));
        horizontalSpacer_13 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout_7->addItem(horizontalSpacer_13);

        label_3 = new QLabel(groupBox_4);
        label_3->setObjectName(QString::fromUtf8("label_3"));

        horizontalLayout_7->addWidget(label_3);

        horizontalSpacer_14 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout_7->addItem(horizontalSpacer_14);


        verticalLayout_3->addLayout(horizontalLayout_7);

        horizontalLayout_8 = new QHBoxLayout();
        horizontalLayout_8->setObjectName(QString::fromUtf8("horizontalLayout_8"));
        horizontalSpacer_15 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout_8->addItem(horizontalSpacer_15);

        delayBox = new QSpinBox(groupBox_4);
        delayBox->setObjectName(QString::fromUtf8("delayBox"));
        delayBox->setMaximum(20);

        horizontalLayout_8->addWidget(delayBox);

        horizontalSpacer_16 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout_8->addItem(horizontalSpacer_16);


        verticalLayout_3->addLayout(horizontalLayout_8);

        horizontalLayout_9 = new QHBoxLayout();
        horizontalLayout_9->setObjectName(QString::fromUtf8("horizontalLayout_9"));
        horizontalSpacer_17 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout_9->addItem(horizontalSpacer_17);

        delaySlider = new QSlider(groupBox_4);
        delaySlider->setObjectName(QString::fromUtf8("delaySlider"));
        delaySlider->setMaximum(20);
        delaySlider->setOrientation(Qt::Vertical);

        horizontalLayout_9->addWidget(delaySlider);

        horizontalSpacer_18 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout_9->addItem(horizontalSpacer_18);


        verticalLayout_3->addLayout(horizontalLayout_9);


        horizontalLayout_13->addLayout(verticalLayout_3);

        verticalLayout_4 = new QVBoxLayout();
        verticalLayout_4->setObjectName(QString::fromUtf8("verticalLayout_4"));
        horizontalLayout_10 = new QHBoxLayout();
        horizontalLayout_10->setObjectName(QString::fromUtf8("horizontalLayout_10"));
        horizontalSpacer_19 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout_10->addItem(horizontalSpacer_19);

        label_4 = new QLabel(groupBox_4);
        label_4->setObjectName(QString::fromUtf8("label_4"));

        horizontalLayout_10->addWidget(label_4);

        horizontalSpacer_20 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout_10->addItem(horizontalSpacer_20);


        verticalLayout_4->addLayout(horizontalLayout_10);

        horizontalLayout_11 = new QHBoxLayout();
        horizontalLayout_11->setObjectName(QString::fromUtf8("horizontalLayout_11"));
        horizontalSpacer_21 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout_11->addItem(horizontalSpacer_21);

        sizeBox = new QSpinBox(groupBox_4);
        sizeBox->setObjectName(QString::fromUtf8("sizeBox"));
        sizeBox->setMaximum(100);

        horizontalLayout_11->addWidget(sizeBox);

        horizontalSpacer_22 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout_11->addItem(horizontalSpacer_22);


        verticalLayout_4->addLayout(horizontalLayout_11);

        horizontalLayout_12 = new QHBoxLayout();
        horizontalLayout_12->setObjectName(QString::fromUtf8("horizontalLayout_12"));
        horizontalSpacer_23 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout_12->addItem(horizontalSpacer_23);

        sizeSlider = new QSlider(groupBox_4);
        sizeSlider->setObjectName(QString::fromUtf8("sizeSlider"));
        sizeSlider->setMaximum(100);
        sizeSlider->setOrientation(Qt::Vertical);

        horizontalLayout_12->addWidget(sizeSlider);

        horizontalSpacer_24 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout_12->addItem(horizontalSpacer_24);


        verticalLayout_4->addLayout(horizontalLayout_12);


        horizontalLayout_13->addLayout(verticalLayout_4);


        verticalLayout_9->addWidget(groupBox_4);

        OutputSettingsDLG->setCentralWidget(centralwidget);
        statusbar = new QStatusBar(OutputSettingsDLG);
        statusbar->setObjectName(QString::fromUtf8("statusbar"));
        OutputSettingsDLG->setStatusBar(statusbar);
        menuBar = new QMenuBar(OutputSettingsDLG);
        menuBar->setObjectName(QString::fromUtf8("menuBar"));
        menuBar->setGeometry(QRect(0, 0, 648, 22));
        menuFile = new QMenu(menuBar);
        menuFile->setObjectName(QString::fromUtf8("menuFile"));
        OutputSettingsDLG->setMenuBar(menuBar);

        menuBar->addAction(menuFile->menuAction());
        menuFile->addAction(actionSaveSettings);
        menuFile->addAction(actionLoadSettings);
        menuFile->addSeparator();
        menuFile->addAction(actionQuit);

        retranslateUi(OutputSettingsDLG);
        QObject::connect(powerSlider, SIGNAL(valueChanged(int)), powerBox, SLOT(setValue(int)));
        QObject::connect(offsetSlider, SIGNAL(valueChanged(int)), offsetBox, SLOT(setValue(int)));
        QObject::connect(delaySlider, SIGNAL(valueChanged(int)), delayBox, SLOT(setValue(int)));
        QObject::connect(sizeSlider, SIGNAL(valueChanged(int)), sizeBox, SLOT(setValue(int)));
        QObject::connect(sizeBox, SIGNAL(valueChanged(int)), sizeSlider, SLOT(setValue(int)));
        QObject::connect(delayBox, SIGNAL(valueChanged(int)), delaySlider, SLOT(setValue(int)));
        QObject::connect(offsetBox, SIGNAL(valueChanged(int)), offsetSlider, SLOT(setValue(int)));
        QObject::connect(powerBox, SIGNAL(valueChanged(int)), powerSlider, SLOT(setValue(int)));
        QObject::connect(shutdown, SIGNAL(clicked()), OutputSettingsDLG, SLOT(close()));
        QObject::connect(actionQuit, SIGNAL(activated()), OutputSettingsDLG, SLOT(close()));

        QMetaObject::connectSlotsByName(OutputSettingsDLG);
    } // setupUi

    void retranslateUi(QMainWindow *OutputSettingsDLG)
    {
        OutputSettingsDLG->setWindowTitle(QApplication::translate("OutputSettingsDLG", "Laser output configuration", 0, QApplication::UnicodeUTF8));
        actionSaveSettings->setText(QApplication::translate("OutputSettingsDLG", "&Save settings...", 0, QApplication::UnicodeUTF8));
        actionSaveSettings->setShortcut(QApplication::translate("OutputSettingsDLG", "Ctrl+S", 0, QApplication::UnicodeUTF8));
        actionLoadSettings->setText(QApplication::translate("OutputSettingsDLG", "&Load settings...", 0, QApplication::UnicodeUTF8));
        actionLoadSettings->setShortcut(QApplication::translate("OutputSettingsDLG", "Ctrl+O", 0, QApplication::UnicodeUTF8));
        actionQuit->setText(QApplication::translate("OutputSettingsDLG", "&Quit", 0, QApplication::UnicodeUTF8));
        shutdown->setText(QApplication::translate("OutputSettingsDLG", "Shut down", 0, QApplication::UnicodeUTF8));
        groupBox->setTitle(QApplication::translate("OutputSettingsDLG", "Blanking", 0, QApplication::UnicodeUTF8));
        outputTest->setText(QApplication::translate("OutputSettingsDLG", "Test", 0, QApplication::UnicodeUTF8));
        outputEnable->setText(QApplication::translate("OutputSettingsDLG", "Output enable", 0, QApplication::UnicodeUTF8));
        blankingEnable->setText(QApplication::translate("OutputSettingsDLG", "Blanking enable", 0, QApplication::UnicodeUTF8));
        blankingInvert->setText(QApplication::translate("OutputSettingsDLG", "Blanking invert", 0, QApplication::UnicodeUTF8));
        groupBox_2->setTitle(QApplication::translate("OutputSettingsDLG", "Scanning", 0, QApplication::UnicodeUTF8));
        xEnable->setText(QApplication::translate("OutputSettingsDLG", "X enable", 0, QApplication::UnicodeUTF8));
        xInvert->setText(QApplication::translate("OutputSettingsDLG", "X invert", 0, QApplication::UnicodeUTF8));
        yEnable->setText(QApplication::translate("OutputSettingsDLG", "Y enable", 0, QApplication::UnicodeUTF8));
        yInvert->setText(QApplication::translate("OutputSettingsDLG", "Y invert", 0, QApplication::UnicodeUTF8));
        xySwap->setText(QApplication::translate("OutputSettingsDLG", "Swap X && Y", 0, QApplication::UnicodeUTF8));
        aspectRatio->clear();
        aspectRatio->insertItems(0, QStringList()
         << QApplication::translate("OutputSettingsDLG", "1:1", 0, QApplication::UnicodeUTF8)
         << QApplication::translate("OutputSettingsDLG", "4:3", 0, QApplication::UnicodeUTF8)
         << QApplication::translate("OutputSettingsDLG", "16:9", 0, QApplication::UnicodeUTF8)
        );
        aspectScale->setText(QApplication::translate("OutputSettingsDLG", "Anamorphic input", 0, QApplication::UnicodeUTF8));
        fitSquare->setText(QApplication::translate("OutputSettingsDLG", "Shrink square", 0, QApplication::UnicodeUTF8));
        resetTransform->setText(QApplication::translate("OutputSettingsDLG", "Reset transform", 0, QApplication::UnicodeUTF8));
        groupBox_3->setTitle(QApplication::translate("OutputSettingsDLG", "Safety", 0, QApplication::UnicodeUTF8));
        enforceSafety->setText(QApplication::translate("OutputSettingsDLG", "Enforce safety", 0, QApplication::UnicodeUTF8));
        groupBox_4->setTitle(QApplication::translate("OutputSettingsDLG", "Analog settings", 0, QApplication::UnicodeUTF8));
        label->setText(QApplication::translate("OutputSettingsDLG", "Power", 0, QApplication::UnicodeUTF8));
        label_2->setText(QApplication::translate("OutputSettingsDLG", "Offset", 0, QApplication::UnicodeUTF8));
        label_3->setText(QApplication::translate("OutputSettingsDLG", "Delay", 0, QApplication::UnicodeUTF8));
        label_4->setText(QApplication::translate("OutputSettingsDLG", "Size", 0, QApplication::UnicodeUTF8));
        menuFile->setTitle(QApplication::translate("OutputSettingsDLG", "File", 0, QApplication::UnicodeUTF8));
    } // retranslateUi

};

namespace Ui {
    class OutputSettingsDLG: public Ui_OutputSettingsDLG {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_OUTPUT_SETTINGS_H

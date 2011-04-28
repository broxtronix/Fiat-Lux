/****************************************************************************
** Meta object code from reading C++ file 'output_settings.h'
**
** Created: Thu Apr 28 02:38:50 2011
**      by: The Qt Meta Object Compiler version 62 (Qt 4.7.2)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include "output_settings.h"
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'output_settings.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 62
#error "This file was generated using the moc from 4.7.2. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
static const uint qt_meta_data_OutputSettings[] = {

 // content:
       5,       // revision
       0,       // classname
       0,    0, // classinfo
      22,   14, // methods
       0,    0, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
       0,       // signalCount

 // slots: signature, parameters, type, tag, flags
      22,   16,   15,   15, 0x0a,
      52,   16,   15,   15, 0x0a,
      84,   16,   15,   15, 0x0a,
     116,   16,   15,   15, 0x0a,
     141,   16,   15,   15, 0x0a,
     166,   16,   15,   15, 0x0a,
     191,   16,   15,   15, 0x0a,
     216,   16,   15,   15, 0x0a,
     246,  240,   15,   15, 0x0a,
     286,   16,   15,   15, 0x0a,
     315,   16,   15,   15, 0x0a,
     342,   16,   15,   15, 0x0a,
     373,   15,   15,   15, 0x0a,
     397,   15,   15,   15, 0x0a,
     428,  422,   15,   15, 0x0a,
     461,  422,   15,   15, 0x0a,
     495,  422,   15,   15, 0x0a,
     528,  422,   15,   15, 0x0a,
     560,   15,   15,   15, 0x0a,
     594,  588,   15,   15, 0x0a,
     621,  588,   15,   15, 0x0a,
     647,  644,   15,   15, 0x0a,

       0        // eod
};

static const char qt_meta_stringdata_OutputSettings[] = {
    "OutputSettings\0\0state\0"
    "on_outputEnable_toggled(bool)\0"
    "on_blankingEnable_toggled(bool)\0"
    "on_blankingInvert_toggled(bool)\0"
    "on_xEnable_toggled(bool)\0"
    "on_yEnable_toggled(bool)\0"
    "on_xInvert_toggled(bool)\0"
    "on_yInvert_toggled(bool)\0"
    "on_xySwap_toggled(bool)\0index\0"
    "on_aspectRatio_currentIndexChanged(int)\0"
    "on_aspectScale_toggled(bool)\0"
    "on_fitSquare_toggled(bool)\0"
    "on_enforceSafety_toggled(bool)\0"
    "on_outputTest_pressed()\0"
    "on_outputTest_released()\0value\0"
    "on_powerSlider_valueChanged(int)\0"
    "on_offsetSlider_valueChanged(int)\0"
    "on_delaySlider_valueChanged(int)\0"
    "on_sizeSlider_valueChanged(int)\0"
    "on_resetTransform_clicked()\0event\0"
    "resizeEvent(QResizeEvent*)\0"
    "showEvent(QShowEvent*)\0pt\0"
    "pointMoved(ControlPoint*)\0"
};

const QMetaObject OutputSettings::staticMetaObject = {
    { &QMainWindow::staticMetaObject, qt_meta_stringdata_OutputSettings,
      qt_meta_data_OutputSettings, 0 }
};

#ifdef Q_NO_DATA_RELOCATION
const QMetaObject &OutputSettings::getStaticMetaObject() { return staticMetaObject; }
#endif //Q_NO_DATA_RELOCATION

const QMetaObject *OutputSettings::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->metaObject : &staticMetaObject;
}

void *OutputSettings::qt_metacast(const char *_clname)
{
    if (!_clname) return 0;
    if (!strcmp(_clname, qt_meta_stringdata_OutputSettings))
        return static_cast<void*>(const_cast< OutputSettings*>(this));
    return QMainWindow::qt_metacast(_clname);
}

int OutputSettings::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QMainWindow::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        switch (_id) {
        case 0: on_outputEnable_toggled((*reinterpret_cast< bool(*)>(_a[1]))); break;
        case 1: on_blankingEnable_toggled((*reinterpret_cast< bool(*)>(_a[1]))); break;
        case 2: on_blankingInvert_toggled((*reinterpret_cast< bool(*)>(_a[1]))); break;
        case 3: on_xEnable_toggled((*reinterpret_cast< bool(*)>(_a[1]))); break;
        case 4: on_yEnable_toggled((*reinterpret_cast< bool(*)>(_a[1]))); break;
        case 5: on_xInvert_toggled((*reinterpret_cast< bool(*)>(_a[1]))); break;
        case 6: on_yInvert_toggled((*reinterpret_cast< bool(*)>(_a[1]))); break;
        case 7: on_xySwap_toggled((*reinterpret_cast< bool(*)>(_a[1]))); break;
        case 8: on_aspectRatio_currentIndexChanged((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 9: on_aspectScale_toggled((*reinterpret_cast< bool(*)>(_a[1]))); break;
        case 10: on_fitSquare_toggled((*reinterpret_cast< bool(*)>(_a[1]))); break;
        case 11: on_enforceSafety_toggled((*reinterpret_cast< bool(*)>(_a[1]))); break;
        case 12: on_outputTest_pressed(); break;
        case 13: on_outputTest_released(); break;
        case 14: on_powerSlider_valueChanged((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 15: on_offsetSlider_valueChanged((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 16: on_delaySlider_valueChanged((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 17: on_sizeSlider_valueChanged((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 18: on_resetTransform_clicked(); break;
        case 19: resizeEvent((*reinterpret_cast< QResizeEvent*(*)>(_a[1]))); break;
        case 20: showEvent((*reinterpret_cast< QShowEvent*(*)>(_a[1]))); break;
        case 21: pointMoved((*reinterpret_cast< ControlPoint*(*)>(_a[1]))); break;
        default: ;
        }
        _id -= 22;
    }
    return _id;
}
QT_END_MOC_NAMESPACE

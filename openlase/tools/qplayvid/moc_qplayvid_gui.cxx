/****************************************************************************
** Meta object code from reading C++ file 'qplayvid_gui.h'
**
** Created: Fri Apr 22 02:17:53 2011
**      by: The Qt Meta Object Compiler version 62 (Qt 4.7.2)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include "qplayvid_gui.h"
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'qplayvid_gui.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 62
#error "This file was generated using the moc from 4.7.2. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
static const uint qt_meta_data_PlayerSetting[] = {

 // content:
       5,       // revision
       0,       // classname
       0,    0, // classinfo
       3,   14, // methods
       0,    0, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
       1,       // signalCount

 // signals: signature, parameters, type, tag, flags
      24,   15,   14,   14, 0x05,

 // slots: signature, parameters, type, tag, flags
      48,   42,   14,   14, 0x0a,
      70,   62,   14,   14, 0x0a,

       0        // eod
};

static const char qt_meta_stringdata_PlayerSetting[] = {
    "PlayerSetting\0\0newValue\0valueChanged(int)\0"
    "value\0setValue(int)\0enabled\0"
    "setEnabled(bool)\0"
};

const QMetaObject PlayerSetting::staticMetaObject = {
    { &QObject::staticMetaObject, qt_meta_stringdata_PlayerSetting,
      qt_meta_data_PlayerSetting, 0 }
};

#ifdef Q_NO_DATA_RELOCATION
const QMetaObject &PlayerSetting::getStaticMetaObject() { return staticMetaObject; }
#endif //Q_NO_DATA_RELOCATION

const QMetaObject *PlayerSetting::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->metaObject : &staticMetaObject;
}

void *PlayerSetting::qt_metacast(const char *_clname)
{
    if (!_clname) return 0;
    if (!strcmp(_clname, qt_meta_stringdata_PlayerSetting))
        return static_cast<void*>(const_cast< PlayerSetting*>(this));
    return QObject::qt_metacast(_clname);
}

int PlayerSetting::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QObject::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        switch (_id) {
        case 0: valueChanged((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 1: setValue((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 2: setEnabled((*reinterpret_cast< bool(*)>(_a[1]))); break;
        default: ;
        }
        _id -= 3;
    }
    return _id;
}

// SIGNAL 0
void PlayerSetting::valueChanged(int _t1)
{
    void *_a[] = { 0, const_cast<void*>(reinterpret_cast<const void*>(&_t1)) };
    QMetaObject::activate(this, &staticMetaObject, 0, _a);
}
static const uint qt_meta_data_PlayerUI[] = {

 // content:
       5,       // revision
       0,       // classname
       0,    0, // classinfo
      12,   14, // methods
       0,    0, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
       0,       // signalCount

 // slots: signature, parameters, type, tag, flags
      10,    9,    9,    9, 0x08,
      24,    9,    9,    9, 0x08,
      39,    9,    9,    9, 0x08,
      56,    9,    9,    9, 0x08,
      75,    9,    9,    9, 0x08,
      99,   93,    9,    9, 0x08,
     118,    9,    9,    9, 0x08,
     132,    9,    9,    9, 0x08,
     146,    9,    9,    9, 0x08,
     167,  161,    9,    9, 0x08,
     182,    9,    9,    9, 0x08,
     197,    9,    9,    9, 0x08,

       0        // eod
};

static const char qt_meta_stringdata_PlayerUI[] = {
    "PlayerUI\0\0modeChanged()\0splitChanged()\0"
    "updateSettings()\0updateSettingsUI()\0"
    "playStopClicked()\0pause\0pauseToggled(bool)\0"
    "stepClicked()\0timePressed()\0timeReleased()\0"
    "value\0timeMoved(int)\0loadSettings()\0"
    "saveSettings()\0"
};

const QMetaObject PlayerUI::staticMetaObject = {
    { &QMainWindow::staticMetaObject, qt_meta_stringdata_PlayerUI,
      qt_meta_data_PlayerUI, 0 }
};

#ifdef Q_NO_DATA_RELOCATION
const QMetaObject &PlayerUI::getStaticMetaObject() { return staticMetaObject; }
#endif //Q_NO_DATA_RELOCATION

const QMetaObject *PlayerUI::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->metaObject : &staticMetaObject;
}

void *PlayerUI::qt_metacast(const char *_clname)
{
    if (!_clname) return 0;
    if (!strcmp(_clname, qt_meta_stringdata_PlayerUI))
        return static_cast<void*>(const_cast< PlayerUI*>(this));
    return QMainWindow::qt_metacast(_clname);
}

int PlayerUI::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QMainWindow::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        switch (_id) {
        case 0: modeChanged(); break;
        case 1: splitChanged(); break;
        case 2: updateSettings(); break;
        case 3: updateSettingsUI(); break;
        case 4: playStopClicked(); break;
        case 5: pauseToggled((*reinterpret_cast< bool(*)>(_a[1]))); break;
        case 6: stepClicked(); break;
        case 7: timePressed(); break;
        case 8: timeReleased(); break;
        case 9: timeMoved((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 10: loadSettings(); break;
        case 11: saveSettings(); break;
        default: ;
        }
        _id -= 12;
    }
    return _id;
}
QT_END_MOC_NAMESPACE

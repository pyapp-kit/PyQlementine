if (%1 == Py_None) {
    %CPPSELF.setIconPathGetter(std::function<QString(QString)>{});
} else if (!PyCallable_Check(%1)) {
    PyErr_SetString(PyExc_TypeError,
                    "setIconPathGetter expects a callable or None");
    return {};
} else {
    // prevent GC; release when the std::function is destroyed
    Py_INCREF(%1);
    auto ref = std::shared_ptr<PyObject>(%1, [](PyObject* p) {
        if (Py_IsInitialized()) {
            PyGILState_STATE gil = PyGILState_Ensure();
            Py_DECREF(p);
            PyGILState_Release(gil);
        }
    });

    %CPPSELF.setIconPathGetter([ref](const QString& name) -> QString {
        PyGILState_STATE gil = PyGILState_Ensure();

        PyObject* pyName = PyUnicode_FromString(name.toUtf8().constData());
        PyObject* result =
            PyObject_CallFunctionObjArgs(ref.get(), pyName, nullptr);
        Py_DECREF(pyName);

        QString out;
        if (result) {
            // accept str or path-like (calls __str__ on pathlib.Path etc.)
            PyObject* strResult = PyObject_Str(result);
            if (strResult) {
                PyObject* bytes = PyUnicode_AsUTF8String(strResult);
                if (bytes) {
                    out = QString::fromUtf8(PyBytes_AsString(bytes));
                    Py_DECREF(bytes);
                }
                Py_DECREF(strResult);
            }
            Py_DECREF(result);
        } else {
            // print the Python exception rather than crashing
            PyErr_Print();
        }

        PyGILState_Release(gil);
        return out;
    });
}

// Wrapper to add missing QCoreApplication include for qlementine's EventFilters.
// The MenuEventFilter.hpp uses QCoreApplication::sendEvent without including it.
#include <QCoreApplication>
#include "style/EventFilters.cpp"

/*
   INDI Developers Manual
   Tutorial #1
   "Hello INDI"
   We construct a most basic (and useless) device driver to illustate INDI.
   Refer to README, which contains instruction on how to build this driver, and use it
   with an INDI-compatible client.
*/

/** \file simpledevice.h
    \brief Construct a basic INDI device with only one property to connect and disconnect.
    \author Jasem Mutlaq
    \example simpledevice.h
    A very minimal device! It also allows you to connect/disconnect and performs no other functions.
*/

#pragma once

#include "indifilterwheel.h"

class SA200 : public INDI::FilterWheel
{
public:
    SA200() = default;
    virtual ~SA200() = default;
    int direction = -1;
    
protected:
    bool Connect() override;
    bool Disconnect() override;
    const char *getDefaultName() override;
    bool SelectFilter(int);
    void TimerHit();
};
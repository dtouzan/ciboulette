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
    float R = 200.0;                          // R
    float length = 20.5;                      // length of sa200 to CCD/CMOS  
    int speed = 2;                            // miliseconds
    const float MOTOR_STEP = 0.087890625;     // step of degree
    
protected:
    bool Connect() override;
    bool Disconnect() override;
    const char *getDefaultName() override;
    bool SelectFilter(int);
    void TimerHit();
    void InitPins();                          // initializing PIN and wiringPi
    void Run(int);                            // motor run
    int GetDegree();                          // get degree block 1
    float GetR();                             // get R block 2
    float GetLength();                        // get length block 3
    int GetSpeed();                           // get speed block 4
    char *GetBlock(int);                      // get block 5 to 10
};
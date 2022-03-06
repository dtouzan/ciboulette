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
#include "indifilterinterface.h"
#include <stdio.h>
#include "indifilterwheel.h"

class SA200 : public INDI::FilterWheel
{
public:
    SA200() = default;
    virtual ~SA200() = default;
    int index = 0;
    float R = 200.0;                          // R
    float length = 20.5;                      // length of sa200 to CCD/CMOS  
    int speed = 2;                            // miliseconds
    const float MOTOR_STEP = 0.087890625;     // step of degree
    const int PINS[4] = {5,6,10,11};          // wiringPi pin
    const bool STEPS[8][4] = {
        {1, 0, 0, 0}, //0 [1,0,0,0]
        {1, 1, 0, 0}, //1 [1,1,0,0]
        {0, 1, 0, 0}, //2 [0,1,0,0]
        {0, 1, 1, 0}, //3 [0,1,1,0]
        {0, 0, 1, 0}, //4 [0,0,1,0]
        {0, 0, 1, 1}, //5 [0,0,1,1]
        {0, 0, 0, 1}, //6 [0,0,0,1]
        {1, 0, 0, 1}, //7 [1,0,0,1]
    };
    const bool STEPS_OUT[1][4] = {
        {0, 0, 0, 0},                         //0 [1,0,0,0] close led
    };
    
protected:
    bool Connect() override;                  // connect driver
    bool Disconnect() override;               // disconnect driver
    const char *getDefaultName() override;    // get name SA200
    bool SelectFilter(int);                   // select command
    void TimerHit();
    void InitPins();                          // initializing PIN and wiringPi
    void HalfStep(bool);                      // for motor run
    void Run(int);                            // motor run
    int GetDegree();                          // get degree block 1
    float GetR();                             // get R block 2
    float GetLength();                        // get length block 3
    int GetSpeed();                           // get speed block 4
    char *GetBlock(int);                      // get block 5 to 10
};
/*
   INDI Developers Manual
   Tutorial #1
   "Hello INDI"
   We construct a most basic (and useless) device driver to illustrate INDI.
   Refer to README, which contains instruction on how to build this driver, and use it
   with an INDI-compatible client.
*/

/** \file simpledevice.cpp
    \brief Construct a basic INDI device with only one property to connect and disconnect.
    \author Jasem Mutlaq
    \example simpledevice.cpp
    A very minimal device! It also allows you to connect/disconnect and performs no other functions.
*/

#include "indi_sa200.h"
#include <stdio.h>
#include <stdlib.h>
#include <iostream>   // std::cout
#include <string>     // std::string, std::to_string
#include <memory>

std::unique_ptr<SA200> simpleSA200(new SA200());
   
/**************************************************************************************
** Client is asking us to establish connection to the device
***************************************************************************************/
bool SA200::Connect()
{
    IDMessage(getDeviceName(), "SA200 connected successfully!");
    CurrentFilter      = 1;
    FilterSlotN[0].min = 1;
    FilterSlotN[0].max = 10;
    return true;
}

/**************************************************************************************
** Client is asking us to terminate connection to the device
***************************************************************************************/
bool SA200::Disconnect()
{
    IDMessage(getDeviceName(), "SA200 disconnected successfully!");
    return true;
}

/**************************************************************************************
** Client select to the device
***************************************************************************************/
bool SA200::SelectFilter(int f)
{
    int degree = 0;
    CurrentFilter = f;
    if (f >= FilterSlotN[0].min && f <= FilterSlotN[0].max) 
        {
            switch(f)
            {
                case 1: direction = direction * -1; break;
                case 2: degree = 1; break;
                case 3: degree = 5; break;
                case 4: degree = 10; break;
                case 5: degree = 15; break;
                case 6: degree = 30; break;
                case 7: degree = 45; break;
                case 8: degree = 90; break;
                case 9: degree = 180;  break;
                case 10: degree = 270;  break;
                default: degree = 1; break;
            }
        if (f > FilterSlotN[0].min && f <= FilterSlotN[0].max) 
            {
                degree = int(degree*direction);
                /* ====================== /!\ /!\ /!\ /!\ /!\=========================
                system("python3 script.py" + nomEntree );
                */
                std::string cmd = "sudo python3 ~/SA200/SA200Motor.py " + std::to_string(degree);
                /* ====================== /!\ /!\ /!\ /!\ /!\=========================*/
                system(cmd.c_str());
            }
        }
    SetTimer(500);
    return true;
}

/**************************************************************************************
** Client TimerHit
***************************************************************************************/
void SA200::TimerHit()
{
    SelectFilterDone(CurrentFilter);
}


/**************************************************************************************
** INDI is asking us for our default device name
***************************************************************************************/
const char *SA200::getDefaultName()
{
    return "SA200";
}
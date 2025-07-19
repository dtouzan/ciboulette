#pragma once

#include "libindi/indifocuser.h"
#include "libindi/indifocuserinterface.h"
#include "libindi/indipropertynumber.h"

class EAFpyFocuser : public INDI::Focuser
{
public:
    EAFpyFocuser();
    virtual ~EAFpyFocuser() = default;
    uint32_t ToTicks = 10;

    virtual const char *getDefaultName() override;

    virtual bool initProperties() override;
    virtual bool updateProperties() override;

    virtual void ISGetProperties(const char *dev) override;
    virtual bool ISNewNumber(const char *dev, const char *name, double values[], char *names[], int n) override;
    virtual bool ISNewSwitch(const char *dev, const char *name, ISState *states, char *names[], int n) override;
    virtual bool ISNewText(const char *dev, const char *name, char *texts[], char *names[], int n) override;
    virtual bool ISSnoopDevice(XMLEle *root) override;

protected:
    virtual bool saveConfigItems(FILE *fp) override;

    bool Connect() override;
    bool Disconnect() override;
    void InitPins();                          // initializing PIN GPIO

    virtual bool Handshake() override;

    virtual IPState MoveFocuser(FocusDirection dir, int speed, uint16_t duration);
    virtual IPState MoveRelFocuser(FocusDirection dir, uint32_t ticks);
    virtual bool AbortFocuser();

private:
    INDI::PropertyNumber DelayNP {1};
    
    // Focuser Speed (if variable speeds are supported)
    INDI::PropertySwitch FocusSpeedSP {2};
};

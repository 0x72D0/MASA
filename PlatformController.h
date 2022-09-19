#pragma once

#include <Encoder.h>

#include "pinout.h"
#include "Model.h"

class PlatformController
{
    public:

    PlatformController() : encoder(ENCODER_DT, ENCODER_CLK)
    {
        encoder.write(0);
    }

    void init(Model* model)
    {
        this->model = model;
    }


    void update()
    {
        int currentEncoder = encoder.read();

        if(currentEncoder < 0)
        {
            currentEncoder = 0;
            encoder.write(currentEncoder);
        }

        model->setEncoderInfo(currentEncoder/ENCODER_OFFSET);
    }

    private:

    const int ENCODER_OFFSET = 4;

    Encoder encoder;

    Model* model;
};
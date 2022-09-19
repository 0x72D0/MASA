#pragma once

class Model
{
    public:

    Model()
    {
        int currentSelectorIndex = 0;
    }

    void setEncoderInfo(int encoderPosition)
    {
        currentSelectorIndex = encoderPosition;
    }

    int getCursorPosition()
    {
        return currentSelectorIndex;
    }

    private:

    int currentSelectorIndex;
};
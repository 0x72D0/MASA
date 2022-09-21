#pragma once

#include "Profile.h"

class Model
{
    public:

    enum GraphicPage
    {
        MAIN=0,
        MONITOR,
        CONTROLLER
    };

    Model()
    {
        int currentSelectorIndex = 0;
        currentPage = GraphicPage::MAIN;
    }

    void setEncoderInfo(int encoderPosition)
    {
        currentSelectorIndex = encoderPosition;
    }

    int getCursorPosition()
    {
        return currentSelectorIndex;
    }

    GraphicPage getCurrentGraphicPage()
    {
        return currentPage;
    }

    private:

    enum GraphicPage currentPage;
    int currentSelectorIndex;
    Profile profile[10];
};
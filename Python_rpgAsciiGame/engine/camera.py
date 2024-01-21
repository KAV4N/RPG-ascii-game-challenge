class Camera:
    def __init__(self, focusOn = None,xView=20,yView=15):
        # player in the middle so 9-1 == 8/2==4
        self.xView = xView
        self.yView = yView

        self.xViewFromCenter = int((self.xView - 1) / 2)
        self.yViewFromCenter = int((self.yView - 1) / 2)

        self.focusOn = focusOn

    def moveCamera(self, yWorldLen, xWorldLen):
        playerPoz = self.focusOn.getTilePoz()

        yStartPoz = max(0, playerPoz[1] - self.getYViewFromCenter())
        yEndPoz = min(yWorldLen, yStartPoz + self.getYView())

        xStartPoz = max(0, playerPoz[0] - self.getXViewFromCenter())
        xEndPoz = min(xWorldLen, xStartPoz + self.getXView())

        if yEndPoz == yWorldLen:
            yStartPoz = max(0, yWorldLen - self.getYView())
        if xEndPoz == xWorldLen:
            xStartPoz = max(0, xWorldLen - self.getXView())
        return xStartPoz, yStartPoz,xEndPoz,yEndPoz

    def getXViewFromCenter(self):
        return self.xViewFromCenter

    def getYViewFromCenter(self):
        return self.yViewFromCenter

    def getYView(self):
        return self.yView

    def getXView(self):
        return self.xView

    def setXView(self,xView):
        self.xView = xView
        self.xViewFromCenter = int((self.xView - 1) / 2)

    def setYView(self, yView):
        self.yView = yView
        self.yViewFromCenter = int((self.yView - 1) / 2)

    def setFocus(self,obj):
        self.focusOn = obj




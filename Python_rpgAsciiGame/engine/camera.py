class Camera:
    def __init__(self, focusOn = None,xView=20,yView=15):
        # player in the middle so 9-1 == 8/2==4
        self.xView = xView
        self.yView = yView

        self.xViewFromCenter = int((self.xView - 1) / 2)
        self.yViewFromCenter = int((self.yView - 1) / 2)
        self.focusOn = focusOn

        self.xStartPoz = 0
        self.yStartPoz = 0
        self.xEndPoz = 0
        self.yEndPoz = 0

    def moveCamera(self, yWorldLen, xWorldLen):
        playerPoz = self.focusOn.getTilePoz()

        self.yStartPoz = max(0, playerPoz[1] - self.getYViewFromCenter())
        self.yEndPoz = min(yWorldLen, self.yStartPoz + self.getYView())

        self.xStartPoz = max(0, playerPoz[0] - self.getXViewFromCenter())
        self.xEndPoz = min(xWorldLen, self.xStartPoz + self.getXView())

        if self.yEndPoz == yWorldLen:
            self.yStartPoz = max(0, yWorldLen - self.getYView())
        if self.xEndPoz == xWorldLen:
            self.xStartPoz = max(0, xWorldLen - self.getXView())
        return self.xStartPoz, self.yStartPoz,self.xEndPoz,self.yEndPoz

    def getCurPozition(self):
        return self.xStartPoz, self.yStartPoz,self.xEndPoz,self.yEndPoz

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




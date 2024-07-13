import rumps

class mymenuapp(rumps.App):
    def __init__(self):
        super(mymenuapp,self).__init__("my app")

        self.icon = './icon/vpn-01.ico'

        self.menu =['hello','my name','test']

    @rumps.clicked('hello')
    def test(self,_):
        rumps.notification(subtitle="hi",message='saalaaaam',title="test test")


if __name__ == "__main__":
    mymenuapp().run()
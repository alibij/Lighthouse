import rumps
from AppKit import NSApplication, NSImage, NSWindow, NSMakeRect, NSButton, NSBezelStyleRounded, NSTextField, NSLayoutAttributeCenterX, NSWindowStyleMaskTitled, NSWindowStyleMaskClosable, NSWindowStyleMaskResizable, NSBackingStoreBuffered, NSApp, NSApplicationActivationPolicyRegular

from createConnection import main


class MyMenuApp(rumps.App):
    def __init__(self):
        # Initialize the application with a menu bar icon
        super(MyMenuApp, self).__init__("my app", icon='./icon/vpn-01.ico')

        # Define menu items
        self.menu = ['hello', 'my name', 'test']

        # Set the dock icon
        self.set_dock_icon('./icon/vpn-01.ico')

        # Set up the application to show the dock icon and activate it
        app = NSApplication.sharedApplication()
        app.setActivationPolicy_(NSApplicationActivationPolicyRegular)

        # Open a window when the app starts
        self.open_window()

    def set_dock_icon(self, icon_path):
        try:
            # Load the image and set it as the application icon
            image = NSImage.alloc().initWithContentsOfFile_(icon_path)
            if image:
                NSApplication.sharedApplication().setApplicationIconImage_(image)
                print("Dock icon set successfully.")
            else:
                print("Failed to load dock icon image.")
        except Exception as e:
            print(f"Error setting dock icon: {e}")

    def open_window(self):
        # Define the window dimensions
        rect = NSMakeRect(100, 100, 400, 300)

        window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            rect,
            NSWindowStyleMaskTitled | NSWindowStyleMaskClosable,
            NSBackingStoreBuffered,
            False
        )

        window.setTitle_("My App Window")

        # Create a button
        button = NSButton.alloc().initWithFrame_(NSMakeRect(100, 50, 200, 50))
        button.setTitle_("Connect")
        button.setBezelStyle_(NSBezelStyleRounded)
        button.setTarget_(self)
        button.setAction_("connect_clicked:")

        # Create a label to display the result
        self.result_label = NSTextField.alloc().initWithFrame_(
            NSMakeRect(100, 120, 200, 50))
        self.result_label.setEditable_(False)
        self.result_label.setSelectable_(True)
        self.result_label.setBezeled_(True)
        self.result_label.setDrawsBackground_(True)
        self.result_label.setAlignment_(NSLayoutAttributeCenterX)

        # Add button and label to the window
        window.contentView().addSubview_(button)
        window.contentView().addSubview_(self.result_label)

        # Show the window
        window.makeKeyAndOrderFront_(None)
        self.window = window

        # Activate the application
        NSApp.activateIgnoringOtherApps_(True)

    @rumps.clicked('hello')
    def on_hello(self, _):
        rumps.notification(title="test test", subtitle="hi",
                           message='saalaaaam')

    @rumps.clicked('test')
    def on_test(self, _):
        rumps.Window(message='', title='', default_text='',
                     ok=None, cancel=None, dimensions=(320, 160)).run()

    def connect_clicked_(self, sender):
        # Handle Connect button click
        xray_setting = {
            'socks': True,
            'http_port': 1081,
            'socks_port': 1080
        }
        try:
            # Replace with your actual function call
            result = main(xray_config=xray_setting)
            self.result_label.setStringValue_(str(result))
        except Exception as e:
            print(f"Error executing main function: {e}")


if __name__ == "__main__":
    MyMenuApp().run()

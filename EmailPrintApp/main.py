from components.index import *

#________________________________________________________________ Main ________________________________________________________________#

def main():
    '''
    The main entry point for the application.

    This function sets up the main window of the application, configures the UI,
    and starts the main event loop.
    '''
    global running
    global status

    set_window()

    timer_label.timer_label.pack_forget()

    # Main Frame Buttons Show #
    switch_frame(FRAME_MAIN)
    
    show_button_on_canvas(main_frame_btns)
    
    WINDOW.update()
    WINDOW.mainloop()

if __name__ == '__main__':

    main()
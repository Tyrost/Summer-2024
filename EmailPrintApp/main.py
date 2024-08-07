from components.assets import *

def main():
    global running
    global status

    set_window()

    timer_label.timer_label.pack_forget()

    # Main Frame Buttons Show #
    switch_frame(FRAME_MAIN)
    
    show_button_on_canvas(main_frame_btns)

    WINDOW.mainloop()

if __name__ == '__main__':

    main()  

'''
Initialize Main Interface:
    - Back Universal Buttons [Done]
    - Set Up, See mail, Run Buttons [Done]
    - Status Dynamic Tracker [Done]
Run Main Script:
    - Connect the main script to work Accuratley [Done]
    - Connecting to excel sheet []
    - Printing attachments to set printers []
Set Up Interface:
    - Set up printer []
    - Set email and google-generated password []
    - Set up excel sheet path []
Set Up Mail:
    - Set emails.json to display all emails in Mails []
'''
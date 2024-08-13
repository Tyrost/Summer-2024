from components.assets import *

def main():
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

'''
Initialize Main Interface:
    - Back Universal Buttons [Done]
    - Set Up, See mail, Run Buttons [Done]
    - Status Dynamic Tracker [Done]
Run Main Script:
    - Connect the main script to work Accuratley [Done]
    - Connecting to excel sheet [Done]
    - Printing attachments to set printers [] L
    - Read Email and Input Data to Excel if set [Done]
Set Up Interface:
    - Set up printer [Done]
    - Set email and google-generated password [Done]
    - Set up excel sheet path [Done]
Set Up Mail:
    - Set emails.json to display all emails in Mails [Cancelled]

Convert Script into executable file []
Have User download all program Dependencies []

'''
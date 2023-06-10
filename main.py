from tkinter import *
from tkinter import messagebox
import json


FONT = ('TimesNewRoman', 16)
collec_of_title = []
all_labels = []
all_bts = []
cols = None
card_title_input = None
card_cont_input = None
rows = None
left_scroll = None
right_scroll = None
card_label = None
collec_len = None
card_no = None
show_card = None


# ui
window = Tk()
window.config(width=600, height=600)
window.title('Flash-cards')
window.config(padx=50, pady=50)


#adding to file
def add_to_file():
    global collec_input, card_cont_input, card_title_input, collec_of_title

    collec_title = collec_input.get()
    card_title = card_title_input.get()
    card_cont = card_cont_input.get('1.0', END).strip('\n')

    if collec_title and card_title and card_cont :
        collec_of_title .append(collec_title)

        card_data = {
                    collec_title : [{ 'title' : card_title, 'content' : card_cont}]
                    }

        try:
            with open('cards.json', 'r') as file:
                data = json.load(file)
                
                if collec_title in data:
                    data[collec_title].extend(card_data[collec_title])

                else:
                    data.update(card_data)

            with open('cards.json', 'w') as file:
                json.dump(data, file, indent=4)

        except :
            with open('cards.json', 'w') as file:
                json.dump(card_data, file, indent=4)
                
        finally:
            card_title_input.delete(0, END)
            card_cont_input.delete('1.0', END)
    else:
        messagebox.showerror(title='Empty field values!', message='Fill all the fields !')


# to create cards
def create_card():
    global collec_input, card_cont_input, card_title_input, all_bts, all_labels

    for i in all_labels:
        i.grid_forget()

    for j in all_bts:
        j.grid_forget()

    canvas.grid_forget()
    
    window.config(padx=30 ,pady=0)

    title['font'] = ('TimesNewRoman', 16)
    title.grid(column=0, row=0)
    new_bt.grid(column=1, row=0)
    existing_bt.grid(column=2, row=0)

    # collection name
    collection = Label(text='Collection : ', font=FONT)
    collection.grid(column=0, row=1, pady=15)
    all_labels.append(collection)
    collec_input = Entry(width=20)
    collec_input.focus()
    collec_input.grid(column=1, row=1, pady=15)
    all_labels.append(collec_input)

    # input cards
    card_title = Label(text='Title : ', font=FONT)
    card_title.grid(column=0, row=2, pady=15)
    all_labels.append(card_title) 
    card_title_input = Entry(width=30)
    card_title_input.grid(column=1, row=2, pady=15)
    all_labels.append(card_title_input)

    card_cont = Label(text='Content : ', font=FONT)
    card_cont.grid(column=0, row=3)
    all_labels.append(card_cont) 
    card_cont_input = Text(width=25, height=8)
    card_cont_input.grid(column=1, row=3, pady=15)
    all_labels.append(card_cont_input)
    
    add_bt = Button(text='Add', font=FONT, command=add_to_file)
    add_bt.config(padx=30)
    add_bt.grid(column=1, row=4, padx=10, pady=15)
    all_bts.append(add_bt)

#existing bt
def view_existing():
    global all_bts, all_labels, cols, rows, card_no, show_card
    card_no = 2
    cols = -1
    rows = 1
    show_card = 0

    try:
        for i in all_labels:
            i.grid_forget()

        for j in all_bts:
            j.grid_forget()

        canvas.grid_forget()
        window.config(padx=30, pady=0)
        title['font'] = ('TimesNewRoman', 16)
        
        title.grid(column=0, row=0)
        new_bt.grid(column=1, row=0, pady=5)
        existing_bt.grid(column=2, row=0)

        with open('cards.json', 'r') as file:
            data = json.load(file)
            total_collection = len(data.keys()) 
            all_collection_keys =[i for i in data.keys()]
            

            def collec_func(collection_name):
                global card_label, right_scroll, left_scroll, collec_len

                collec_len = len(data[collection_name]) - 1

                for i in all_labels:
                    i.grid_forget()

                for j in all_bts:
                    j.grid_forget()

                canvas.grid_forget()
                collec_bt.grid_forget()
                new_bt.grid_forget()
                existing_bt.grid_forget()

                back_bt = Button(text="Back",font=FONT, command=view_existing)
                back_bt.grid(column=2, row=0,padx=20, pady=10)
                all_bts.append(back_bt)
                logo.config(file='front.png')
                card_label = Label(text=data[collection_name][0]['title'], image=logo, compound="center", anchor="center", font=('times', 30, 'bold'), justify=CENTER, wraplength=180)
                card_label.config(fg="white")
                card_label.grid(column=1, row=1)
                all_labels.append(card_label)
                
                def right_skip(card_no):
                    global left_scroll, right_scroll, card_label, collec_len, show_card
                    card_label['text'] = data[collection_name][card_no - 1 ]['title']

                    if card_no - 1 == collec_len:
                        right_scroll.config(state=DISABLED)
                    show_card += 1
                    right_scroll.config(command=lambda:right_skip(card_no + 1))
                    left_scroll.config(command=lambda:left_skip(card_no - 1))
                    left_scroll.config(state=NORMAL)

                    
                       
                def left_skip(card_no):
                    global left_scroll, right_scroll, card_label, collec_len, show_card
                    card_label['text'] = data[collection_name][card_no - 1 ]['title']

                    if card_no - 1 == 0:
                        left_scroll.config(state=DISABLED)
                    show_card -= 1
                    right_scroll.config(command=lambda:right_skip(card_no + 1))
                    left_scroll.config(command=lambda:left_skip(card_no - 1))
                    right_scroll.config(state=NORMAL)
                    


                left_scroll = Button(text='<<<' , command=left_skip, state=DISABLED)
                left_scroll.grid(column=0, row=2)
                
                all_bts.append(left_scroll)

                right_scroll = Button(text='>>>', command=lambda:right_skip(card_no))
                if card_no  > collec_len:
                        right_scroll.config(state=DISABLED)
                right_scroll.grid(column=2, row=2)
                all_bts.append(right_scroll)

                def show_cont(show_card):
                    global left_scroll, right_scroll, card_label, collec_len
                    card_label['text'] = data[collection_name][show_card]['content']

                show_bt = Button(text='Show', font=FONT, command=lambda:show_cont(show_card))
                show_bt.grid(column=1, row=2, pady=20)
                all_bts.append(show_bt)

            for _ in range (total_collection):
                cols +=1
                
                if cols > 2:
                    cols = 0
                    rows += 1

                collec_bt = Button(text=all_collection_keys[_], font=FONT, command= lambda k=_: collec_func(all_collection_keys[k]))
                collec_bt.grid(row=rows, column=cols, padx=40, pady=20)
                all_bts.append(collec_bt)
                 

    except:
        messagebox.showerror(title='FILE NOT FOUND', message="There no existing collection !")



# logo
canvas = Canvas(width=205, height=200)
logo = PhotoImage(file='cards--logo.png')
flash_logo = canvas.create_image(100, 100, image=logo)
canvas.grid(column=1, row=0)

title = Label(text='Flash Cards', font=('TimesNewRoman', 45, 'bold'))
title.grid(column=3, row=0)

new_bt = Button(text='New', font=FONT, command=create_card)
new_bt.config(padx=10)
new_bt.grid(column=1, row=1, columnspan=2, padx=15, pady=15)

existing_bt = Button(text='Existing', font=FONT, command=view_existing)
existing_bt.grid(column=2, row=1, columnspan=2, padx=15, pady=15)


window.mainloop()
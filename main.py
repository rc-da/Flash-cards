from tkinter import *
from tkinter import messagebox
import json

card_title_input = None
card_cont_input = None
collec_of_title = []
FONT = ('TimesNewRoman', 16)

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
    collec_of_title .append(collec_title)

    card_data = {
                'all_collection' : collec_of_title,
                 collec_title : [{ 'title' : card_title, 'content' : card_cont}]
                }

    try:
        with open('cards.json', 'r') as file:
            data = json.load(file)
            
            if collec_title in data:
                data['all_collection'].extend(card_data['all_collection'])
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


# to create cards
def create_card():
    global collec_input, card_cont_input, card_title_input

    canvas.grid_forget()
    
    window.config(padx=30 ,pady=0)

    title['font'] = ('TimesNewRoman', 16)
    title.grid(column=0, row=0)
    new_bt.grid(column=1, row=0)
    existing_bt.grid(column=2, row=0)

    # collection name
    collection = Label(text='Collection : ', font=FONT)
    collection.grid(column=0, row=1)
    collec_input = Entry(width=20)
    collec_input.focus()
    collec_input.grid(column=1, row=1)

    # input cards
    card_title = Label(text='Title : ', font=FONT)
    card_title.grid(column=0, row=2)
    card_title_input = Entry(width=30)
    card_title_input.grid(column=1, row=2)

    card_cont = Label(text='Content : ', font=FONT)
    card_cont.grid(column=0, row=3)
    card_cont_input = Text(width=25, height=8)
    card_cont_input.grid(column=1, row=3)
    
    add_bt = Button(text='Add', font=FONT, command=add_to_file)
    add_bt.config(padx=30)
    add_bt.grid(column=1, row=4)


#existing bt
def view_existing():
    canvas.grid_forget()
    window.config(padx=30,pady=0)
    title['font'] = ('TimesNewRoman', 16)
    title.grid(column=0, row=0)
    new_bt.grid(column=1, row=0)
    existing_bt.grid(column=2, row=0)

    try:
        with open('cards.json', 'r') as file:
            data = json.load(file)
            collection = data['all_collection']
            print(collection)
    except:
        messagebox.showerror(title='FILE NOT FOUND', message="There no existing collection !")



# logo
canvas = Canvas(width=205, height=200)
logo = PhotoImage(file='cards--logo.png')
flash_logo = canvas.create_image(100, 100, image=logo)
canvas.grid(column=1, row=0)

title = Label(text='Flash Cards', font=('TimesNewRoman', 45, 'bold'))
title.grid(column=3, row=0)

gap_ = Label(text='\t\t\t\n')
gap_.grid(column=1, row=1)

new_bt = Button(text='New', font=FONT, command=create_card)
new_bt.config(padx=10)
new_bt.grid(column=1, row=2, columnspan=2)

existing_bt = Button(text='Existing', font=FONT, command=view_existing)
existing_bt.grid(column=2, row=2, columnspan=2)


window.mainloop()
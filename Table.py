from tkinter import *
from tkinter import ttk
from tkinter import messagebox
global Edited_ID
Edited_ID = 0
def Update_Total_Label(label,table):
    data = fetch_table_data(table)
    amount = tax = total = comp1 = comp2 = 0.0
    for i in data:
        amount += float(i[6])
        tax_string = str(i[7]).split(" ")
        tax += float(tax_string[0])
        total += float(i[8])
        comp1 += float(i[9])
        comp2 += float(i[10])
    labels = [amount,tax,total,comp1,comp2]
    for i in range(len(label)):
        label[i]['text'] = str(labels[i])
def Match_Record(table,row_data):
    found = True
    for line in table.get_children():
        value = table.item(line)['values']
        if str(value[1]) == row_data[1] and str(value[4]) == row_data[4]:
            found = False
    return found
def Insert_into_table(row_data,table,row):
    if row % 2 == 0:
        tag = "even"
        back = "black"
        front = "white"
    else:
        tag = "odd"
        back = "white"
        front = "black"
    table.tag_configure(tag, background=back, foreground=front, font=("Times 16"))
    table.insert('', 'end', text="",
                         values=row_data, tags=tag)
                         
def fetch_table_data(table):
    data = []
    for line in table.get_children():
       rows = []
       for value in table.item(line)['values']:
           rows.append(value)
       data.append(rows)
    return data
def delete_whole(table,total_labels):
    for lines in table.get_children():
        table.delete(lines)
    Update_Total_Label(total_labels,table)
def delete(event,table,total_labels):
    ans = messagebox.askyesno("Confirmation Dialogue","Do you want to Delete?")
    if ans:
        row = table.focus()
        table.delete(row)
        table.update()
        data = fetch_table_data(table)
        delete_whole(table,total_labels)
        for i in range(len(data)):
            data[i][0] = str(i+1)
            Insert_into_table(data[i],table,i+1)
        Update_Total_Label(total_labels,table)

def Edit_Row(table,row_data,total_label):
    global Edited_ID
    final_List = [*[Edited_ID],*row_data]
    id = table.focus()
    print(id)
    table.item(id,text="",
                         values=tuple(final_List))
    Update_Total_Label(label=total_label,table=table)

def Set_Edit_Mode(event,table,entries,update_btn):
    global Edited_ID
    id = table.focus()
    row = table.item(id)['values']
    Edited_ID = row[0]
    update_btn['text'] = "Update"
    final_row = [row[1],row[3],row[4],row[5],row[9],row[10],row[2],row[7],row[7]]
    for i in range(len(entries)):
        if i == 0 or i == 2 or i == 6:
            entries[i].set(final_row[i])
        else:
            entries[i].delete(0,"end")
            entries[i].insert(0,final_row[i])
def Generate_Table(myFrame,width,title,x,y,fields,update_btn,total_labels):
    tableFrame = Frame(myFrame, width=770, height=300)
    tableFrame.pack()
    tableFrame.place(x=x, y=y)
    mylist = []
    for i in range(1,len(title)+1):
        mylist.append(i)
    scrollbar = ttk.Scrollbar(tableFrame, orient=VERTICAL)
    scrollbar.pack(side=RIGHT, fill=Y)

    treeStyle = ttk.Style()
    treeStyle.theme_use("classic")
    treeStyle.configure("Treeview", background="white", foreground="blue", fieldbackground="white", rowheight=35,
                        relief="raised", font=("Times 16 bold"),height=20)

    # TreeStyle.map("Treeview", background=[('selected', 'red')])

    # Creating Table
    table = ttk.Treeview(tableFrame, columns=(mylist), show="headings", style="Treeview",
                              yscrollcommand=scrollbar)
    index = 1
    for i in range(len(title)):
        table.heading(index, text=title[i])
        table.column(index, width=width[i])
        index += 1
    # tags
    table.tag_configure("row_color", background="black", foreground="white", font=("Times 12"))

    table.pack()
    # Salerydata.bind("<ButtonRelease-1>", PaySalery)
    table.bind("<Control-d>", lambda event, table=table,labels=total_labels: delete(event,table,labels))
    table.bind("<Control-e>", lambda event, table=table,entries =fields,update=update_btn: Set_Edit_Mode(event,table,entries,update))
    scrollbar.config(command=table.yview)
    return table
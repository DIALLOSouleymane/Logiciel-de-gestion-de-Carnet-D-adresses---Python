# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 22:36:20 2022





@authors: Souleymane DIALLO

"""


import os
from tkinter import *
from tkinter import ttk
import tkinter.messagebox as mb
import sqlite3

   
root = Tk()
root.title("Address Book")
root.geometry("800x510")
root.resizable(0,0)

# Titre
Titre = Label(root , text = "Address Book" ,
              font = ("broadway 22 bold") , bg="light green" , fg = "navy blue" )
Titre.grid(row = 0, column = 0)


class Carnet_address:
    
    def __init__(self, master):
        pass
        

    def Ajouter_contact(self):
        prenom = entreePrenom.get()
        nom = entreeNom.get()
        tel = EntreePhone.get()
        if prenom !='' and nom !='' and tel !='':
            
            # Controle pour une saisie de mail valide *************
            while True:
                try:
                    mail = Entreemail.get()
                    assert "@" and "." in mail
                    break
                except AssertionError:
                    mb.showerror('Error!', "Desolé, email invalide...")
                    break
        
        if prenom =='' or nom =='' or tel =='' or mail =='':
            mb.showerror('Error!', "Merci de remplir les differents champs!")
        elif ("@" and ".") not in mail:
            mb.showinfo('Guide!', "Merci de vous rassurer que le mail saisi contient \
                        les caractères <@> et <.> qui sont obligatoires...")
        else:
            # Connection pour l'Affichage sur sqlite
        
            connection = sqlite3.connect("sql_for_official_project.db")
            curseur = connection.cursor()
            curseur.execute("INSERT INTO contacts (`Nom`,`Prenom`, `Tel`,`Email`) values (?,?,?,?)",
                        (nom, prenom, tel, mail)), connection.commit()
            connection.close()
        
            # Affichage auto sur Treeview
            connection = sqlite3.connect("sql_for_official_project.db")
            curseur = connection.cursor()
            select = curseur.execute("SELECT*FROM contacts order by id desc")
            select = list(select)
            Affiche.insert("", END, values = select[0])
            connection.close()
            
            # Message de validation
            mb.showinfo("Enregistrement de contact",
                        "Votre contact a été enregistré avec succès ! ")
            
            # Nettoiement des entrees apres ajout:
            entreePrenom.delete(0, END)
            entreeNom.delete(0, END)
            EntreePhone.delete(0, END)
            Entreemail.delete(0, END)
    
    def Supprimer_contact(self):
        idSelect = Affiche.item(Affiche.selection())['values'][0]
        conn = sqlite3.connect("sql_for_official_project.db")
        cur = conn.cursor()
        delete = cur.execute("delete from contacts where id = {}".format(idSelect))
        conn.commit()
        Affiche.delete(Affiche.selection())
        
    def Trier_nom(self):
        # Suppression des données sur l'ecran
        for i in Affiche.get_children():
            Affiche.delete(i)
        # connection a la baseDonnee
        c = sqlite3.connect("sql_for_official_project.db")
        cur = c.cursor()
        select = cur.execute("select*from contacts order by Nom asc")
        c.commit()
        
        """for row in select:
            Affiche.insert("", END, values = row)
        c.close()"""
        Affiche.tag_configure('oddrow', background="white")
        Affiche.tag_configure('evenrow', background="lightblue")
    
        count = 0
        for record in select:
        	if record[0] % 2 == 0:
        		Affiche.insert(parent='', index='end', iid=count, text="",
                         values=(record[0], record[1], record[2], record[3],
                                 record[4]), tags=('evenrow',))
        	else:
        		Affiche.insert(parent='', index='end', iid=count, text="",
                         values=(record[0], record[1], record[2], record[3],
                                 record[4]), tags=('oddrow',))
    
        	count += 1
        connection.close()
        
    def Chercher_contact(self):
        
        nom = entreeNomSearch.get()
        prenom = entreePrenomSearch.get()
        c = sqlite3.connect("sql_for_official_project.db")
        cur = c.cursor()
        if nom =='' :
            mb.showerror('Error!',
                         "Merci de renseigner le champ nom, il est OBLIGATOIRE pour la recherche!")    
        else:
            if prenom == "":
                select = cur.execute("SELECT*FROM contacts where nom = (?)", (nom,))
                c.commit()
            else:
                select = cur.execute("SELECT*FROM contacts where (nom, prenom) = (?,?)",
                                     (nom,prenom,))
                c.commit()
                
            # Nettoiement de treeview pour afficher les resultats de recherche
            for i in Affiche.get_children():
                Affiche.delete(i)
                
            # Affichage des resultats
            """for row in select:
                Affiche.insert("", END, values = row)
            c.close()"""
            Affiche.tag_configure('oddrow', background="white")
            Affiche.tag_configure('evenrow', background="lightblue")
        
            count = 0
            for record in select:
            	if record[0] % 2 == 0:
            		Affiche.insert(parent='', index='end', iid=count, text="",
                             values=(record[0], record[1], record[2], record[3],
                                     record[4]), tags=('evenrow',))
            	else:
            		Affiche.insert(parent='', index='end', iid=count, text="",
                             values=(record[0], record[1], record[2], record[3],
                                     record[4]), tags=('oddrow',))
        
            	count += 1
            connection.close()
        
        
        
    def Afficher(self,event):
         idsel = Affiche.item(Affiche.selection())['values'][0]
         nomsel = Affiche.item(Affiche.selection())['values'][1]
         prenomsel = Affiche.item(Affiche.selection())['values'][2]
         phonesel = Affiche.item(Affiche.selection())['values'][3]
         mailsel = Affiche.item(Affiche.selection())['values'][4]
         
         # Label ***********
         lid = Label(root, text = "ID : " + str(idsel))
         lid.place(x = 5, y = 400)
         lnom = Label(root, text = "Nom : " + str(nomsel))
         lnom.place(x = 5, y = 420)
         lprenom = Label(root, text = "Prenom : " + str(prenomsel))
         lprenom.place(x = 5, y = 440)
         lphone = Label(root, text = "N° : " + str(phonesel))
         lphone.place(x = 5, y = 460)
         lmail = Label(root, text = "Email : " + str(mailsel))
         lmail.place(x = 5, y = 480)
         linfo = Text(root)
         linfo.place(x = 230, y = 400, width = 520, height = 100)
         linfo.insert(END, "Détails : " + "Le contact sélectionné est " + str(prenomsel) + " " + str(nomsel)\
                      +"\n\t Son numéro est : " + str(phonesel)\
                          +"\n\t Son addresse email est : " + str(mailsel))
         
    # modifier_contact

    def modifier_contact(self):
        entreePrenom.delete(0, END)
        entreeNom.delete(0, END)
        EntreePhone.delete(0, END)
        Entreemail.delete(0, END)
        
        sel = Affiche.focus()
        values = Affiche.item(sel, 'values')
        
        entreeNom.insert(0, values[1])
        entreePrenom.insert(0, values[2])
        EntreePhone.insert(0, values[3])
        Entreemail.insert(0, values[4])
        
        
    def Aide(self):
        mb.showinfo("Assistant de RECHERCHE",
                    "Pour chercher par nom :Veillez saisir le Nom du contact (en renseignant le champ nom), ensuite TAPEZ sur le boutton <<Chercher Contact>> ci-dessous")
        mb.showinfo("Assistant de RECHERCHE",
                    "Afin de réduire les résultats si plusieurs contatcts présentent le meme non,  Vous pouvez renseigner le prénom du contatct. (Option facultative...)")
    
    def AideGen(self):
        mb.showinfo("Assistant Général",
                    "Pour afficher un contact, veillez clicquez directement sur ce dernier...")
        mb.showinfo("Assistant Général",
                    "Pour modifier un contact, d'abord veillez clicquez sur ce dernier, \
                        ensuite veillez clicquez sur le boutton << Modifier Contact>> ...")
        mb.showinfo("Assistant Général",
                    "Idem pour supprimer un contact, d'abord veillez clicquez sur ce dernier, \
                        ensuite veillez clicquez sur le boutton << Supprimer Contact>> ...")
        
    
    def Quiter(self):
        root.destroy()
        

c = Carnet_address(root)


# Affichage Infos

# Scrollbar ***************
style = ttk.Style()
style.theme_use("default")
    #colors

style.configure("Treeview",
                background = "#D3D3D3",
                foreground = "black",
                rowheight = 25,
                fieldbackground = "#D3D3D3",
                )

 
#    couleur selection
style.map("Treeview", background = [("selected", "navy blue")])

Affiche = ttk.Treeview(root, columns=(1,2,3,4,5), height = 5, show = "headings")
Affiche.place(x = 230, y = 170, width = 530, height = 208 )
Affiche.heading(1, text = "N°")
Affiche.heading(2, text = "Nom")
Affiche.heading(3, text = "Prénom")
Affiche.heading(4, text = "Tel")
Affiche.heading(5, text = "Email")

Affiche.column(1, width = 20)
Affiche.column(2, width = 50)
Affiche.column(3, width = 70)
Affiche.column(4, width = 70)

# Scrollbar
scroll = Scrollbar(Affiche, orient = VERTICAL, command = Affiche.yview)
Affiche.config(yscrollcommand = scroll.set)
scroll.pack(side = RIGHT, fill = Y)


# Affichage des infos sur L'ecran
connection = sqlite3.connect("sql_for_official_project.db")
curseur = connection.cursor()
select = curseur.execute("select*from contacts")
#for ligne in select:
 #   Affiche.insert("", END, value = ligne)

# ********* Personnalisation de l'affichage ***************
Affiche.tag_configure('oddrow', background="white")
Affiche.tag_configure('evenrow', background="lightblue")

count = 0
for record in select:
	if record[0] % 2 == 0:
		Affiche.insert(parent='', index='end', iid=count, text="",
                 values=(record[0], record[1], record[2], record[3],
                         record[4]), tags=('evenrow',))
	else:
		Affiche.insert(parent='', index='end', iid=count, text="",
                 values=(record[0], record[1], record[2], record[3],
                         record[4]), tags=('oddrow',))

	count += 1
connection.close()


# Search 

nomSearch = Label(root , text = "Chercher par Nom :"  , bg="black" , fg = "white" )
nomSearch.place(x=450 , y=15 , width=140)
entreeNomSearch = Entry(root, bd = 3)
#entreeNomSearch.bind("<Return>", Chercher_nom)
entreeNomSearch.place(x=600 , y=15 , width=160)



prenomSearch = Label(root , text = "Saisir le prénom :"  , bg="black" , fg = "white" )
prenomSearch.place(x=450 , y=50 , width=140)
entreePrenomSearch = Entry(root, bd =3)
entreePrenomSearch.place(x=600 , y=50 , width=160)

# anchor with place ????

# Label identifiants

prenom = Label(root , text = "Prénom:" ,  bg="black" , fg = "white")
prenom.place(x=5 , y = 50 , width = 125)
entreePrenom = Entry(root, bd = 4, bg = "white", fg = "black")
entreePrenom.place(x = 140,  y =50 , width=300)




Nom = Label(root , text = "Nom:" , bg="black" , fg = "white")
Nom.place(x=5 , y=80 ,  width = 125 )
entreeNom = Entry(root, bd = 4, bg = "white", fg = "black")
entreeNom.place(x = 140,  y =80 , width=300)

phone = Label(root , text = "Telephone:" , bg="black" , fg = "white")
phone.place(x=5 , y=110 ,  width = 125 )
EntreePhone = Entry(root, bd = 4, bg = "white", fg = "black")
EntreePhone.place(x = 140,  y =110 , width=300)

mail = Label(root , text = "Email:" , bg="black" , fg = "white")
mail.place(x=5 , y=140 ,  width = 125 )
Entreemail = Entry(root, bd = 4, bg = "white", fg = "black")
Entreemail.place(x = 140,  y =140 , width=300)


    

# Ajout Bouttons

b1 = Button(root, text = "Ajouter Contact", bg = "light green", fg = "black", command = c.Ajouter_contact)
b1.place(x = 5, y = 170, width = 200)

b2 = Button(root, text = "Afficher Contact", bg = "light green", fg = "black", command = c.AideGen)
b2.place(x = 5, y = 200, width = 200)
Affiche.bind("<<TreeviewSelect>>", c.Afficher)

b3 = Button(root, text = "Chercher Contact (Nom) ", bg = "light green", fg = "black", command = c.Chercher_contact)
b3.place(x = 600, y = 85, width = 160)

b33 = Button(root, text = "Aide/Help (Search) ", bg = "light green", fg = "black", command = c.Aide)
b33.place(x = 600, y = 120, width = 160)

b4 = Button(root, text = "Trier par Nom", bg = "light green", fg = "black", command = c.Trier_nom)
b4.place(x = 5, y = 230, width = 200)

b5 = Button(root, text = "Modifier Contact", bg = "light green", fg = "black", command = c.modifier_contact)
b5.place(x = 5, y = 260, width = 200)

b5 = Button(root, text = "Supprimer Contact", bg = "light green", fg = "black",
            command = c.Supprimer_contact)
b5.place(x = 5, y = 290, width = 200)

b5 = Button(root, text = "Aide / Need any Help ?", bg = "light green", fg = "black", command = c.AideGen)
b5.place(x = 5, y = 320, width = 200)

b5 = Button(root, text = "Quiter App / Exit", bg = "light green", fg = "black", command = c.Quiter )
b5.place(x = 5, y = 350, width = 200)


root.mainloop()

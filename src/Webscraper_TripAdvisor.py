# -*- coding: utf-8 -*-


import requests
import os
import unicodedata
import validators
import threading
import json
#from tkinter import *
from tkinter import messagebox
import tkinter as tk

from bs4 import BeautifulSoup
from setuptools.package_index import HREF
from tinydb import TinyDB,Query,where
#from PIL import ImageTk, Image



class Web_scraping:
    
    '''
    Created on 18.04.2018 - 20.05.2018
    
    @author: anjawolf
    
    Data will be scraped from the Tripadvisors Website and stored in variables.
    '''
    def get_single_data(self,url):
        source_code = requests.get(url)
        source_code.decoding = ('utf-16BE')
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, "html.parser")

        #get all the hotel containers from current page
        hotel_containers = soup.find_all('div', class_= 'listing_title')
        reviewsPerPage = len(hotel_containers)


        #get the pageNumbers for all hotels in the chosen city
        pageNumbers = int(soup.find('div', class_= 'pageNumbers').find(class_='pageNum last taLnk ').text)
        counter = 1
        

        #Extract data from single hotel containers of page 1 
        for container in hotel_containers:
                
            for link in container.find_all('a', href=True):
                href = "https://www.tripadvisor.de" + str(link.get('href'))
                #pass it to the function where single data is scraped
                self.loop_through_review_pages(href)
                counter = counter + 1
                
        
        #create a new_url for each page of the hotel pages
        for index in range (reviewsPerPage,pageNumbers*reviewsPerPage, reviewsPerPage):
            
            data = url.split("g187309-")
            new_url = data[0]+"g187309-oa"+str(index)+'-'+data[1]
            #pass the new_url to the loop_trough_review_pages function
            self.loop_through_hotel_pages(new_url)
        
        
        #print ("Es wurden " + str(counter) + " textuelle von " + self.rating_amount.string + " Bewertungen abgegeben!")
     
        

    '''   
    @author: JohannesKnippel
    
    loop through the page of al hotels and store the new link of each hotel in variable
    then pass it to the function where it loops through each review container
    '''
    def loop_through_hotel_pages(self, loop_url):
        source_code = requests.get(loop_url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, "html.parser")
        
        #get all hotels but on the new_url
        hotel_containers = soup.find_all('div', class_= 'listing_title')
        reviewsPerPage = len(hotel_containers)
        
        #search trough all hotels on the page
        for container in hotel_containers:
                
            for link in container.find_all('a', href=True):
                href = "https://www.tripadvisor.de" + str(link.get('href'))
                #pass it to the function where single data is scraped
                self.loop_through_review_pages(href)
                
    
        '''
    Created on 18.04.2018 - 20.05.2018
    
    @author: anjawolf
    
    Data will be scraped from the Tripadvisors Website and stored in variables.
    '''
    def loop_through_review_pages(self,url):
        source_code = requests.get(url)
        source_code.decoding = ('utf-16BE')
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, "html.parser")
        
        self.item_name = soup.find('script', {'type': 'application/ld+json'})
        json_string = str(self.item_name.string)
        obj = json.loads(json_string)
        
        #get title of the hotel
        self.title = obj["name"]
        print ("Titel: " + self.title)

        #get overall rating of the hotel
        self.points = obj["aggregateRating"] ["ratingValue"]
        print ("Rating: " + self.points)

        review_containers = soup.find_all('div', class_= 'review-container')
        reviewsPerPage = len(review_containers)


        #get the amount pageNumbers for all reviews per hotels
        pageNumbers = int(soup.find('div', class_= 'pageNumbers').find(class_='pageNum last taLnk ').text)
        
        counter = 1
        

        #Extract data from single containers of first page
        for container in review_containers:
                
            for link in container.find_all('a', href=True):
                href = "https://www.tripadvisor.de" + str(link.get('href'))
                #pass it to the function where single data is scraped
                self.get_single_review_data(href)
                counter = counter + 1
                
        
        #create a new_url for each page of the reviews
        for index in range (reviewsPerPage,pageNumbers*reviewsPerPage, reviewsPerPage):
            
            data = url.split("Reviews-")
            new_url = data[0]+"Reviews-or"+str(index)+'-'+data[1]
            #pass the new_url to the loop_trough_review_pages function
            self.loop_through_reviews(new_url)
        
        
        #print ("Es wurden " + str(counter) + " textuelle von " + self.rating_amount.string + " Bewertungen abgegeben!")
     
       
    
    
    '''   
    @author: Anja Wolf
    loop through the hotel review pages and store the new link in variable
    then pass it to the function where single data is scraped
    '''
    def loop_through_reviews(self, loop_url):
        source_code = requests.get(loop_url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, "html.parser")
        
        #get all review containers but on the nuw_url
        review_containers = soup.find_all('div', class_= 'review-container')
        reviewsPerPage = len(review_containers)
        
        #search trough all reviews on the page
        for container in review_containers:
                
            for link in container.find_all('a', href=True):
                href = "https://www.tripadvisor.de" + str(link.get('href'))
                #pass it to the function where single data is scraped
                self.get_single_review_data(href)

    

    '''   
    @author: Anja Wolf
    
    Scrapes the data of one review. uses link of loop_through_review_pages()
    '''
    def get_single_review_data(self,review_url):     
        source_code2 = requests.get(review_url)
        plain_text2 = source_code2.text
        soup = BeautifulSoup(plain_text2, "html.parser")
        
        #intizialise and load the json from TA to search for relevant data     
        self.item_name = soup.find('script', {'type': 'application/ld+json'})
        json_string = str(self.item_name.string)
        obj = json.loads(json_string)
        
        #get title of the review
        self.title = obj["name"]
        print ("Titel: " + self.title)
        
        #get content of the review
        self.review = obj["reviewBody"]
        print ("Bewertung: " + self.review)

        #get rating of the review
        self.points = obj["reviewRating"] ["ratingValue"]
        print ("Rating: " + self.points)

        #load all relevant review, User, Picture data into database (table: REVIEWS, USERS, PICTURES)
        #self.parse_to_tinydb_us_rev_pic()
    


    '''    
    @author: JohannesKnippel
    
    TinyDB - Database. Function to handle exit of programm when pressing button on popup.Window
    '''
    def endProgram(self):
        exit()



    '''    
    @author: JohannesKnippel
    
    TinyDB - Database. Scraped Data from get_single_data() function will be parsed to a Database saved in .json-Format. These are all the Restaurant related data
    '''
    '''def parse_to_tinydb_rest(self):
        cwd = os.getcwd()
        try:
            #create the database or use the existing one
            db = TinyDB('db.json', sort_keys=True, indent=4, separators=(',', ': '))
            #create the tables inside the database
            tableReviews = db.table('REVIEWS')
            tableUsers = db.table('USERS')
            tablePictures = db.table('PICTURES')
            tableRestaurants = db.table('RESTAURANTS')
        
        except:
            print("Error opening file")    


        #check if there are already Restaurants in the table, if so, count the Restaurants and set R_ID. check also if the newly set R_ID already exists, if so, count and check again
        if tableRestaurants.contains((where('R_ID') > 0)):
            for ids3 in tableRestaurants:
                self.idRestaurant = self.idRestaurant + 1
                if tableRestaurants.contains((where('R_ID') == self.idRestaurant)):
                    # print ("next")
                    x = 1
                else:
                    print ("jetzt wird ein neues Restaurant mit RestaurantID : " + str(self.idRestaurant) + " eingefügt")
                    break
        else:
            self.idRestaurant = 1

        #HANDLE RESTAURANTS
        #check if there already exists an entry in the Restaurans-table with the same name and the same address (these two attributes don't change/are not variable so there is a more constant way to check for duplicates)
        if tableRestaurants.contains((where('RESTAURANTNAME') == self.name.string) & (where('PLZ_ORT') == self.locality.string)): 
            #pop up a message box
            msg = "Dieses Restaurant ist bereits in der Datenbank hinterlegt!"
            popup = tk.Tk()
            popup.wm_title("!")
            label = tk.Label(popup, text=msg)
            label.pack(side="top", fill="x", pady=10)
            B1 = tk.Button(popup, text="Okay und Beenden", command = self.endProgram)
            B1.pack()
            popup.mainloop()
        # if there is no such entry, parse the data into the corresponding table of the database and define the data to insert into database including an auto increment ID for each Table       
        else:
            #self.popularity2 = unicodedata.normalize('NFD', self.pupularity.text)
            print("Preis_Level: " + self.price_level)
            dataRestaurants = {'R_ID':self.idRestaurant, 'RESTAURANTNAME':self.name.string, 'PUNKTESKALA':self.overallPoints.div.span['content'], 'ANZAHL_BEWERTUNGEN':self.rating_amount.string, 'POPULARITAET':self.popularity.text, 'PREIS_LEVEL':self.price_level, 'KUECHE':self.cuisine.text, 'STRASSE':self.address.string, 'PLZ_ORT':self.locality.string, 'TELEFONNUMMER':self.phonenumber.text}
            tableRestaurants.insert_multiple([dataRestaurants]) 



    ''' 
    '''
    @author: JohannesKnippel
    
    TinyDB - Database. Scraped Data from get_single_review_data() function will be parsed to a Database saved in .json-Format. These are all the Review, Users and Pictures related data
    '''
            
    ''' def parse_to_tinydb_us_rev_pic(self):
        cwd = os.getcwd()
        try:
            #create the database or use the existing one
            db = TinyDB('db.json', sort_keys=True, indent=4, separators=(',', ': '))
            #create the tables inside the database
            tableReviews = db.table('REVIEWS')
            tableUsers = db.table('USERS')
            tablePictures = db.table('PICTURES')
            tableRestaurants = db.table('RESTAURANTS')
        
        except:
            print("Error opening file") 


        #AUTOINCREMENT U_ID: check if there are already Users in the table, if so, count the Users and set U_ID. check also if the newly set U_ID already exists, if so, count and check again
        if tableUsers.contains((where('U_ID') > 0)):
            for ids in tableUsers:
                self.idUser = self.idUser + 1
                if tableUsers.contains((where('U_ID') == self.idUser)):
                    #print ("next")
                    x = 1
                else:
                    print ("jetzt wird neuer User mit UserID : " + str(self.idUser) + " eingefügt")
                    break
        else:
            self.idUser = 1


        #AUTINCREMENT REV_ID: check if there are already Reviwes in the table, if so, count the Reviews and set REV_ID. check also if the newly set REV_ID already exists, if so, count and check again
        if tableReviews.contains((where('REV_ID') > 0)):
            for ids2 in tableReviews:
                self.idReview = self.idReview + 1
                if tableReviews.contains((where('REV_ID') == self.idReview)):
                    #print ("next")
                    x = 1
                else:
                    print ("jetzt wird neuer Review mit ReviewID : " + str(self.idReview) + " eingefügt")
                    break
        else:
            self.idReview = 1

        
        #HANDLE USERS
        #check if there already exists an entry in the USERS-table with the same name (this attribute doesn't change/is not variable so there is a more constant way to check for duplicates)
        if tableUsers.contains((where('BENUTZERNAME') == self.username) & (where('REV_ID') == self.idReview)): 
            #print a message
            msg = ("Der User" + self.username + " ist bereits in der Datenbank hinterlegt! Es wird weitergesucht...")
            print(msg)
        #if there is no such entry, parse the data into the corresponding table of the database and define the data to insert into database including an auto increment ID for each Table       
        else:
            dataUsers = {'U_ID':self.idUser, 'REV_ID':self.idReview, 'BENUTZERNAME':self.username, 'ANZAHL_REVIEWS':self.numberOfReviews, 'ANZAHL_LIKES':self.numberOfLikes}  
            tableUsers.insert(dataUsers)


        #HANDLE REVIEWS
        #check if there already exists an entry in the REVIEWSs-table with the same name and the same address (these two attributes don't change/are not variable so there is a more constant way to check for duplicates)
        if tableReviews.contains((where('TITEL') == self.title) & (where('BEWERTUNG') == self.review)): 
            #print a message
            msg = ("Dieses Review mit dem Titel: " + self.title + " wurde bereits in der Datenbank hinterlegt! Es wird weitergesucht...")
            print(msg)
        #if there is no such entry, parse the data into the corresponding table of the database and define the data to insert into database including an auto increment ID for each Table       
        else:
            dataReviews = {'R_ID':self.idRestaurant, 'U_ID':self.idUser, 'REV_ID':self.idReview, 'TITEL':self.title, 'BEWERTUNG':self.review, 'RATING':self.points.span.span['alt'].split()[0]}
            tableReviews.insert(dataReviews)


        #HANDLE PICTURES
        #check if there already exists an entry in the PICTURES-table with the same name and the same address (these two attributes don't change/are not variable so there is a more constant way to check for duplicates)
        if tablePictures.contains((where('QUELLE') == self.src)): 
            #pop up a message box
            msg = ("Dieses Bild mit dem Link: " + self.src + " wurde bereits in der Datenbank hinterlegt! Es wird weitergesucht...")
            print(msg)
        # if there is no such entry, parse the data into the corresponding table of the database and define the data to insert into database including an auto increment ID for each Table       
        else:  
            dataPictures = {'REV_ID':self.idReview, 'QUELLE':self.src} 
            tablePictures.insert(dataPictures)
'''



    '''
    @author: Skanny Morandi
   
    'opens a GUI that validates a given url-string and starts the scraping on button click
    '''
    ''' def start_GUI(self):


        roots = tk.Tk()
        roots.title('Tripadvisor Scraper')
        instruction = tk.Label(roots, text='Please provide Restaurant-Url\n')
        instruction.grid(row=0, column=0, sticky=tk.E)

        restaurant_label = tk.Label(roots, text='Restaurant-URL ')
        restaurant_label.grid(row=1, column=0, sticky=tk.W)
        restaurant_entry = tk.Entry(roots, width=100)
        restaurant_entry.grid(row=1, column=1, sticky=tk.W)
        restaurant_name_label = tk.Label(roots, text='Restaurant Name')
        restaurant_name_label.grid(row=2, column=0, sticky=tk.W)
        restaurant_city_label = tk.Label(roots, text='City')
        restaurant_city_label.grid(row=3, column=0, sticky=tk.W)
        restaurant_rating_label = tk.Label(roots, text='Average Rating')
        restaurant_rating_label.grid(row=4, column=0, sticky=tk.W)


        def preview_restaurant():
            base_restaurant_url_= "https://www.tripadvisor.de/Restaurant_Review"
            url_to_check = restaurant_entry.get()
            if  (not validators.url(url_to_check)) or \
                (base_restaurant_url_ not in url_to_check):

                messagebox.showwarning("Warning", "This seems not to be valid Tripadvisor restaurant URL")
            else:
                source_code = requests.get(url_to_check)
                source_code.decoding = ('utf-16BE')
                plain_text = source_code.text
                soup = BeautifulSoup(plain_text, "html.parser")

                prev_restuarant_name = soup.find('h1', {'class': 'heading_title'}).string

                prev_restaurant_rating = soup.find('div', {'class': 'rs rating'}).div.span['content']

                prev_restaurant_city = soup.find('span', {'class': 'locality'}).string[:-2]

                prev_restaurant_name_label = tk.Label(roots, text=prev_restuarant_name)
                prev_restaurant_name_label.grid(row=2, column=1, sticky=tk.W)
                prev_restaurant_city_label = tk.Label(roots, text=prev_restaurant_city)
                prev_restaurant_city_label.grid(row=3, column=1, sticky=tk.W)
                prev_restaurant_rating_label = tk.Label(roots, text=prev_restaurant_rating)
                prev_restaurant_rating_label.grid(row=4, column=1, sticky=tk.W)

                roots.pack_slaves()

        preview_button = tk.Button(roots, text='Preview', command=preview_restaurant)
        preview_button.grid(columnspan=3, sticky=tk.W)

        def go_scrape():
            self.get_single_data(restaurant_entry.get())

        scrape_button = tk.Button(roots, text='Start Scraping', command=go_scrape)

        scrape_button.grid(columnspan=5, sticky=tk.W)
        roots.mainloop()
'''

'''
@author: Skanny Morandi, JohannesKnippel
   
Main function, will be executed when starting the python-script
'''  
           
if __name__ == "__main__":
    
    ws = Web_scraping()
    #ws.get_single_data('https://www.tripadvisor.de/Hotels-g187309-oa30-Munich_Upper_Bavaria_Bavaria-Hotels.html')
    #ws.loop_through_review_pages('https://www.tripadvisor.de/Hotel_Review-g187309-d199637-Reviews-Hilton_Munich_Park-Munich_Upper_Bavaria_Bavaria.html')
    ws.get_single_data('https://www.tripadvisor.de/Hotels-g187309-oa30-Munich_Upper_Bavaria_Bavaria-Hotels.html')
    #ws.start_GUI()
    #example URL:
    # https://www.tripadvisor.de/Restaurant_Review-g946452-d8757235-Reviews-The_Forge_Tea_Room-Hutton_le_Hole_North_York_Moors_National_Park_North_Yorkshire_.html
    # https://www.tripadvisor.de/Restaurant_Review-g187309-d2656918-Reviews-Savanna-Munich_Upper_Bavaria_Bavaria.html




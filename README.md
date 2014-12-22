brownmenu
===
anrosent

### What does it do

This is a simple JSON REST API for the Brown University Dining hall offerings, currently only including The Ratty because it is the best. The data is made available by the university for viewing in iframes on the pages under http://www.brown.edu/Student_Services/Food_Services/eateries/. These iframes are views into a Google Spreadsheet, which is the source of all the data we can get here. 

### How does it do this

The file ```scrape.py``` implements the scraping logic, pulling items from the menu for each implemented dining hall for each meal of the week, and ```server.py``` is a Flask server that caches the week's worth of scraped data in memory on the first request every day, serving from the cache thereafter.

### Looking ahead

Some better persistence would be great, as the in-memory cache doesn't provide much in the way of historical analysis.

**ih datamadpt0420 project module 1:**

**Deliverable**: 	Create a table which can be called from the terminal and is available as csv file.

**Challenges**:\
  	            - unify information from different sources (API, web & database)\
			    - bring the information into a readable format\
			    - aggregate the information \
			    - create a pipeline

A table shall be created with the following content: number and percentage of jobs in different countries and areas. 
The basic information is given in a database in different tables. The country information is only given with country 
codes. The job information is given in encrypted codes. The areas are described with different words for the 
same meaning.

**Realization:** 

The project was realized in PyCharm and can be executed with a python script. 
The following programs, libraries… were used: SQL, Python, Pandas, BeautifulSoup, Numpy, WebScraping, RegEx, Argparse, Requests...


A raw table was created with SQL out of the given database. 
With Web Scraping (Beautiful Soup) a table with country codes and the respective country names was fetched from the internet and with the help of Regex it was converted into a python dictionary. With dictionary comprehension the country codes in the raw table where substituted with the country names. 
For every encrypted job code there is a internet url where you can find the corresponding job title. A list with all ‘job urls’ was created. With API all job titles could used to substitute the job codes

The areas were described with many words with the same meaning. All city related descriptions where changed to ‘urban’ and all countryside related descriptions where changed to ‘rural’. This was done by numpy conditions.

Then an additional column with the title ‘Quantity’ was added. This column is an one array with the length of the table. In a last table, the percentage of the jobs distribution is shown.

#!/usr/bin/env python
# coding: utf-8

# ## Importing Libraries
# 

# In[9]:





# In[1]:


import pandas as pd
import numpy as np

from matplotlib import pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import datetime as dt

import seaborn as sns

import warnings
warnings.filterwarnings("ignore")


# ### Loading Data Sets

# In[2]:


customer_data = pd.read_csv("olist_customers_dataset.csv")
orders_data = pd.read_csv("olist_orders_dataset.csv")
orders_items_data = pd.read_csv("olist_order_items_dataset.csv")
order_payments_data = pd.read_csv("olist_order_payments_dataset.csv")
order_review_data = pd.read_csv("olist_order_reviews_dataset.csv")
product_data = pd.read_csv("olist_products_dataset.csv")
sellers_data = pd.read_csv("olist_sellers_dataset.csv")
location_data = pd.read_csv("olist_geolocation_dataset.csv")
product_category_data = pd.read_csv("product_category_name_translation.csv")


# In[232]:


pd.set_option('display.max_columns', None)


# ### Data Understanding

# ##### Customer Data Set

# In[3]:


customer_data.head()


# In[4]:


customer_data.shape


# In[5]:


customer_data.info()


# In[6]:


customer_data.describe(include= "all")


# In[7]:


customer_data.isna().sum()


# In[83]:


customer_data["customer_zip_code_prefix"].value_counts().sort_values(ascending=False).head()


# In[ ]:





# In[8]:


fig, ax = plt.subplots(figsize=(10,10))
sns.countplot(x ='customer_state', data = customer_data ,  order=customer_data['customer_state'].value_counts().sort_values().index,ax = ax )


# Most of the Customers are from SP i.e São Paulo

# ####  Top 10 Cities

# In[103]:


customer_data["customer_city"].value_counts().sort_values(ascending = False).head(10)


# ### With the Help of this Data We can find the top States as per the Business Perspective

# #### ------------------------------------------------------------------------------------------------------------------ 

# ### Orders Data

# #### Now Using Orders Data to find More Details and Meaningful Insights

# In[11]:


orders_data.head()


# In[12]:


orders_data.info()


# In[13]:


orders_data.isna().sum()


# ###### We will be Replacing Null values with Forward fill Method for The "Ordered_delivered_customer_date" Column as we are working on this data set

# In[ ]:


orders_data["order_delivered_customer_date"] = orders_data["order_delivered_customer_date"].fillna(method = "ffill")


# In[63]:


orders_data["order_delivered_customer_date"] 


# In[92]:


orders_data["delivered_dates"] = orders_data['order_delivered_customer_date'].astype('datetime64[ns]')


# In[90]:


orders_data["Estimated_dates"] = orders_data["order_estimated_delivery_date"].astype('datetime64[ns]')


# #####  After Converting the Data type of these two columns into Data Time we will me Performing Operation on it

# In[95]:


orders_data["delivered_dates"] = pd.to_datetime(orders_data["delivered_dates"]).dt.date


# In[98]:


orders_data["Estimated_dates"] = pd.to_datetime(orders_data["Estimated_dates"]).dt.date


# ##### To Perform the Subtraction in Columnwise Operation it need to be In Same Format

# In[122]:


orders_data["Date_Diff"] = orders_data["Estimated_dates"] - orders_data["delivered_dates"]


# In[115]:


orders_data["Year"] = pd.DatetimeIndex(orders_data['Estimated_dates']).year


# In[129]:


orders_data["Year"] = orders_data["Year"].astype("str")


# In[124]:


orders_data["delivered_dates"] = orders_data['order_delivered_customer_date'].astype('datetime64[ns]')
orders_data["Estimated_dates"] = orders_data["order_estimated_delivery_date"].astype('datetime64[ns]')


# In[132]:


orders_data["Month"] = pd.DatetimeIndex(orders_data['Estimated_dates']).month


# ### Plotting a Graph to see The Difference in Estimated Time and Exact Time

# In[135]:


plt.figure(figsize=(20,10))
sns.lineplot(x='weekly', y='Date_Diff', data=orders_data, color="coral", linewidth=5,
            markers=True,dashes=False, estimator='mean')

plt.xlabel("Weeks", size=14)
plt.ylabel("Difference Days", size=14)
plt.title("Average Difference Days per Week",size=15, weight='bold')


# #### You can See a Drop and Rise in Graph based on Weeks Convert Them into Months For The Exact Results

# In[ ]:





# ## Items Data

# In[142]:


orders_items_data.head()


# In[145]:


orders_items_data.shape


# In[146]:


orders_items_data.isna().sum()


# #####  Merging Data 

# In[151]:


total_orders=pd.merge(orders_data, orders_items_data)


# #### Now After Merging Two Data Sets Orders_data and Orders_items_data we stored that in Total_Orders
# #### No we will be Using the Total_Orders dataset to merge it upon Product_data on top of Product_ID

# In[160]:


products = pd.merge(total_orders , product_data , on = "product_id")


# ######  Now shortened the Product ID Length for better visuals

# In[175]:


products["mini_id"] = products["product_id"].str[-8:]


# ### Plotting a graph to see top 10 Products

# In[195]:


plt.figure(figsize=(20,15))
sns.countplot(x='mini_id', data=products, palette='gist_earth', order=products['mini_id'].value_counts()[:10]              .sort_values().index).set_title("Top 10 Products", fontsize=20,weight='bold')
sns.set(font_scale = 2)


# In[201]:


products[products["mini_id"] == "314663af"]


# ##### Grouping a Product_Id and Product Category to see the  Product ID with it Category Name

# In[204]:


product_details =products.groupby(["mini_id" , "product_category_name"])["mini_id"].count().sort_values(ascending=False).head(10)


# In[205]:


product_details


# In[ ]:





# ### Sellers

# #### Merging Seller Data with Products on top of Seller ID

# In[217]:


seller_products = pd.merge(products , sellers_data , on ="seller_id" )


# ##### Shortening the Seller ID for Better Visuals

# In[224]:


seller_products["Sell_ID"] =  seller_products["seller_id"].str[-8:]


# ### Plotting a Pie Chart to Top Seller

# In[227]:


plt.figure(figsize=(10,10))
seller_products['Sell_ID'].value_counts()[:10].plot.pie(autopct='%1.1f%%',
        shadow=True, startangle=90, cmap='tab20')
plt.title("Top 10 Seller",size=14, weight='bold')
plt.show()


# In[ ]:





# #### Using Group By Function to Top Sellers Products Category

# In[233]:


Mostly = seller_products.groupby(["Sell_ID","product_category_name"])["Sell_ID"].count().sort_values(ascending = False).head(10)
Mostly


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





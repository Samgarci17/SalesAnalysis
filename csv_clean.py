import pandas as pd
import numpy as np
import re

df = pd.read_csv(r"C:\\Users\\samag\\Documents\\datasets\\amazon.csv")

summary = {
    "missing_values": df.isna().sum(),
    "empty_strings": (df == "").sum(),
    "total_missing_or_empty": (df.isna() | (df == "")).sum()
}
print(pd.DataFrame(summary))

#Split the category strings into a list
df['category'] = df['category'].str.split('|')
df['category'] = df['category'].apply(lambda x: '{' + ', '.join(x) + '}')

#Changed the values of the discounted_price col to floats from str and currency from rupee to dollar
pre_dprice_series = df['discounted_price'].str.replace(r'\D', '', regex=True)
post_dprice_series = []
for price in pre_dprice_series:
    price = float(price)
    price*=0.012
    price=round(price, 2)
    post_dprice_series.append(price)
df['discounted_price']=post_dprice_series

#Changed the values of the actual_price col to floats from str and currency from rupee to dollar
pre_aprice_series = df['actual_price'].str.replace(r'\D', '', regex=True)
post_aprice_series = []
for price in pre_aprice_series:
    price = float(price)
    price*=0.012
    price=round(price, 2)
    post_aprice_series.append(price)
df['actual_price']=post_aprice_series

#Changed the values of the discount_percentage col to floats from str and changed to percentage format
pre_disc_series = df['discount_percentage'].str.replace(r'\D', '', regex=True)
post_disc_series = []
for discount in pre_disc_series:
    discount = float(discount)
    discount/=100
    discount=round(discount,2)
    post_disc_series.append(discount)
df['discount_percentage']=post_disc_series

#Handled empty strings and changed the count type from str to int
pre_rating_series = df['rating'].str.replace(r'\D', '', regex=True)
pre_rating_series = pre_rating_series.replace("", 0).astype(int)  # Replace NaN with 0
df["rating"] = np.nan_to_num(pre_rating_series, nan=0).astype(int)
pre_rating_series = df["rating"]
post_rating_series = []
for rating in pre_rating_series:
    rating = round(int(rating)/10, 2)
    post_rating_series.append(rating)
df['rating']=post_rating_series

#Handled missing values and changed the count type from str to int
pre_rcount_series = df['rating_count'].str.replace(r'\D', '', regex=True)
pre_rcount_series = pre_rcount_series.fillna(0)  # Replace NaN with 0
df["rating_count"] = np.nan_to_num(pre_rcount_series, nan=0).astype(int)
pre_rcount_series = df["rating_count"]
post_rcount_series = []
for count in pre_rcount_series:
    try:
        count = int(count)
    except ValueError as e:
        print(f"An unexpected error occurred: {e}, {count}")
    post_rcount_series.append(count)
df['rating_count']=post_rcount_series

df['about_product'] = re.sub(r'[^a-zA-Z0-9\s.,]', '', df['about_product'])

df['user_id'] = df['user_id'].str.split(',')
df['user_id'] = df['user_id'].apply(lambda x: '{' + ', '.join(x) + '}')

df['user_name'] = df['user_name'].str.split(',')
df['user_name'] = df['user_name'].apply(lambda x: '{' + ', '.join(x) + '}')

df['review_id'] = df['review_id'].str.split(',')
df['review_id'] = df['review_id'].apply(lambda x: '{' + ', '.join(x) + '}')

df['review_title'] = df['review_title'].str.split(',')
df['review_title'] = df['review_title'].apply(lambda x: '{' + ', '.join(x) + '}')

df['review_content'] = df['review_content'].str.split(',')
df['review_content'] = df['review_content'].apply(lambda x: '{' + ', '.join(x) + '}')

df.to_csv("clean_amazon.csv", index=False)
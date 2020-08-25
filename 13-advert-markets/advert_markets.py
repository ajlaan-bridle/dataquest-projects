# %%
'''
Import the survey data and produce a frequency table for JobRoleInterest
'''
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

survey = pd.read_csv('./files/2017-fCC-New-Coders-Survey-Data.csv')

print(survey['JobRoleInterest'].value_counts(normalize=True))

# %%
'''
Extract columns related to specific job interests
and convert to boolean values
'''
job_interests = survey.iloc[:, 53:66].copy()
job_interests = job_interests.apply(lambda x: x == 1.0)
web_jobs = ['JobInterestBackEnd', 'JobInterestFrontEnd', 'JobInterestFullStack']
web_job_interests = job_interests[web_jobs].any(axis='columns')
mobile_job_interests = job_interests['JobInterestMobile']

web_mobile_job_interests = [
    ['Web', web_job_interests.sum() / web_job_interests.size * 100],
    ['Mobile', mobile_job_interests.sum() / mobile_job_interests.size * 100]
]
web_mobile_job_interests = pd.DataFrame(web_mobile_job_interests, columns=['type', 'perc']).reset_index()
sns.barplot(x='type', y='perc', data=web_mobile_job_interests)
plt.xlabel('')
plt.ylabel('Percentage')
plt.title('Interest in Web or Mobile Development')
plt.savefig('./files/web_mobile_interest.png')

# %%
'''
Extract subset of survey data containing only responses with
explicit interest in web or mobile development
'''
job_interests['JobRoleInterest'] = survey['JobRoleInterest'].str.lower().str.contains(r'web|mobile')
web_mobile_jobs = web_jobs + ['JobInterestMobile', 'JobRoleInterest']
sample = survey[job_interests[web_mobile_jobs].any(axis=1)]
sample.iloc[:, 53:69].head().to_markdown()

# %%
'''
Where respondants in the subset live
'''
sample['CountryLive'].value_counts()

# %%
sample['CountryLive'].value_counts(normalize=True) * 100

# %%
'''
Determine mean monthly spend per country
'''
# calculate spend per month
sample['MonthlySpend'] = sample['MonthsProgramming'].copy()
sample['MonthlySpend'].loc[sample['MonthlySpend'] == 0] = 1
sample['MonthlySpend'] = sample['MoneyForLearning'] / sample['MonthlySpend'].copy()

# drop rows with null MonthlySpend or CountryLive entries
sample.dropna(subset=['MonthlySpend', 'CountryLive'], inplace=True)

# this information is extracted again later
def top_4_mean_spend(df):
    mean_spend_by_country = df.groupby(['CountryLive']).agg('mean')['MonthlySpend']
    return mean_spend_by_country.loc[['United States of America', 'India', 'United Kingdom', 'Canada']]

top_4_mean_spend(sample)

# %%
'''
Box plot for US, UK, India, Canada monthly learning spend
'''
# this box plot is repeated later
def top_4_box_plot(df, filename: str):
    four_countries = df[df['CountryLive'].str.contains(r'United States of America|India|United Kingdom|Canada')]
    sns.boxplot(x='CountryLive', y='MonthlySpend', data=four_countries)
    plt.xticks(range(4), ['US', 'UK', 'India', 'Canada'])
    plt.xlabel('')
    plt.ylabel('Monthly spend ($)')
    plt.title('Monthly Spend Box Plots')
    plt.savefig(filename)

top_4_box_plot(sample, './files/box_plot_1.png')

# %%
'''
Progressively eliminate extreme outliers
'''
rows_to_drop = sample[sample['MonthlySpend'] > 40000]
sample.drop(rows_to_drop.index, inplace=True)

top_4_box_plot(sample, './files/box_plot_2.png')

# %%
# identify potential outliers from India to remove
cols = ['AttendedBootcamp', 'BootcampFinish', 'MoneyForLearning', 'MonthsProgramming', 'MonthlySpend']
sample[
    (sample['CountryLive'] == 'India') &
    (sample['MonthlySpend'] > 2500)
][cols].to_markdown()

# %%
# identify potential outliers from Canada to remove
sample[
    (sample['CountryLive'] == 'Canada') &
    (sample['MonthlySpend'] > 4500)
][cols].to_markdown()

# %%
# identify potential outliers from the US to remove
sample[
    (sample['CountryLive'] == 'United States of America') &
    (sample['MonthlySpend'] > 7000)
][cols].to_markdown()

# %%
# drop outlier rows
india_rows_drop = sample[
    (sample['CountryLive'] == 'India') &
    (sample['MonthlySpend'] > 2500)
]

canada_rows_drop = sample[
    (sample['CountryLive'] == 'Canada') &
    (sample['MonthlySpend'] > 4500)
]

usa_rows_drop = sample[
    (sample['CountryLive'] == 'United States of America') &
    (sample['MonthlySpend'] > 7000) &
    (sample['BootcampFinish'] != 1)
]

sample.drop(india_rows_drop.index, inplace=True)
sample.drop(canada_rows_drop.index, inplace=True)
sample.drop(usa_rows_drop.index, inplace=True)

# produce updated aggregate data
print(top_4_mean_spend(sample))
top_4_box_plot(sample, './files/box_plot_3.png')

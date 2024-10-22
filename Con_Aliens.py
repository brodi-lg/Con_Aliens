#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd

# Load the CSV file into a DataFrame

df_videos_WF = pd.read_csv('channel_videos.csv')



# In[2]:


#first attempt at getting a list of videos but it didn't return a view count or like count 
df_videos_WF


# In[3]:


#next extraction extraction with stats on view count and like count was saved as another df
df_videos_stats = pd.read_csv('video_statistics.csv')


# In[4]:


#checking if view count and like count  are there
df_videos_stats


# # CONCATENATING TWO DATAFRAMES

# In[6]:


df_new = df_videos_WF[['Tags']] #filtering the first data frame and retaining only tags


# In[7]:


#concatenating the first and second data frame

df_WF = pd.concat([df_new, df_videos_stats], axis=1)


# In[8]:


#standardizing 

df_WF.columns = df_WF.columns.str.lower().str.replace(" ", "_")


# In[9]:


#handling "No Tags" under the tags column and generating tags for these columns by parsing title column

no_tags_videos = df_WF[df_WF['tags'] == 'No Tags'] #filtering videos (and creating new df) where the tags column == No Tags

#function to create new tags by splitting the title into keywords
def generate_tags_from_title(title):
                                                        
    keywords = title.split()
    keywords = [word.lower() for word in keywords if len(word) > 2]  #filtering words that are longer than 2 letters
    return keywords

df_WF.loc[no_tags_videos.index,'tags'] = no_tags_videos['title'].apply(generate_tags_from_title)


# In[10]:


#storing file with generated tags to code tags into categories

file_name = 'updated_WF.xlsx'

df_WF.to_excel(file_name) 


# In[11]:


import ast 

Function to handle different tag formats
def convert_to_list(tags):
    if isinstance(tags, list):                        #if it is already a list
        return tags
    elif isinstance(tags, str):
        if tags.startswith('[') and tags.endswith(']'):
            try:
                
                return ast.literal_eval(tags)                   # convert it to an actual list
            except (ValueError, SyntaxError):
                
                pass                                             # If the conversion fails, treat it as a plain string
      
        return [tag.strip() for tag in tags.split(',')]           # Otherwise, it's a comma-separated string, so split it
    else:
        
        return []                                                # If it's neither a list nor a string, return an empty list


df_WF['tags'] = df_WF['tags'].apply(convert_to_list)             # Apply function to 'tags' column


df_WF['tags'] = df_WF['tags'].apply(lambda tags: sorted(tags) if isinstance(tags, list) else tags) #sorting tags

print(df_WF['tags'].apply(type))
      




# In[ ]:


#create dictionary of categories


categories = { "mind_control":["mind control hypnosis", "mind control", "consciousness", "mind upload", "brain activity"],
   "gene_editing":["dna", "gene editing", "ancient humans", "genetic diversity"],
   "aliens":["alien","martian", "flying saucers", "ufo", "bible", "biblical", "UFO", "ancient technology","alien videos", "extra terrestrials", "alien abduction", "ancient aliens", "Varghina UFO", "ufo videos", "ufo video", "ufo sightings", "ufos", "unidentified flying object"],
   "mystery":["time travel", "future","sergei","saqqara","gosford", "spheres", "mothman","piri", "ark","georgia", "kozyrev", "dorothy", "indrid", "agartha", "worlds","life", "time-slip", "gobekli", "time","lucid dreaming", "underwater ruins", "near death experience",
              "strange sounds", "afterlife", "parallel universe", "philosophers stone", "egypt","spontaneous human combustion","pyramid", "boulders", "betz sphere","michigan dogman", "ghost town","mels hole", "dark watchers","kaspar hauser","coincidences","northern california","atlantis","boobquake","emerald", "creatures", "giants", "mysteries", "reality","dog suicide","aztec culture","voynich code","ancient egypt","bennington triangle","rosalia lombardo","ghost plane","murder mystery", "max headroom hack"],
   "pol_con":["dark web", "project", "roswell", "gateway", "reverse", "hollow", "operation", "cicada", "malta", "patents","illuminati","weird", "moon", "darpa", "moon landing", "artificial intelligence", "conspiracy theories","conspiracies","cia","central intelligence agency", "nikola tesla", "adam and eve story", "pyramid", "simulation", "mysterious sounds",
                 "freemasonry", "knights templar", "templar's", "jfk", "deepest holes", "simulation theory","russia","apollo",
                 "jejune institute", "surveillance","mount rushmore", "cyberwarfare", "code", "secret space program", "cia declassified", "apollo 11", 
                 "Underground City", "nasa","cover-up", "secret", "deepfake", "jfk assassination", "sonic weapon", "area 51"],
   
   "doomsday":["mass extinction", "apocalypse", "extinction", "end times","psychic","nostradamus"],

   "occult":["horror movies","horror","shadow", "werewolves","exorcism", "exorcisms", "haunted", "lemuria", "superstition","paranormal","ghosts", "ghost hunting", "creepy","creepiest places"],

   "facts":["face mites", "terrifying discovery","weird science", "weird facts", "circleville","farts","strange science","ocean facts","science facts", 
                    "wire", "nanotechnology", "metric system", "what is asmr", "math facts", "asteroid","dinosaur","animal rain","interesting facts"],

   "space":["solar storm", "strange sounds","panspermia", "kuiper belt", "space", "gravity"],

   "misc":["funny","iphone","pregnant man","james pond", "breeze", "after", "read", "hang-out","thanks", "christmas", "hecklefish", "pajamas", "watch-along", "watch",] }


def categorize_tags(tags):

   if isinstance(tags, str):                        # checking again that 'tags' is a list, if not convert it
       tags_list = tags.split(', ')  # Split tags if they are a string
   else:
       tags_list = tags  # Tags are already a list
   
   assigned_categories = set()  # Initialize an empty set for storing matched categories
   
  
   for category, keywords in categories.items():
       if any(keyword.lower() in [tag.lower() for tag in tags_list] for keyword in keywords):
           assigned_categories.add(category)
   
   
   if not assigned_categories:               
       return 'None'
   

   return ', '.join(assigned_categories)


# In[ ]:


df_WF['categories'] = df_WF['tags'].apply(categorize_tags)  #apply function


# In[ ]:


#creating a priority list of categories to avoid titles being assigned to multiple categories
priority_list = ['aliens', 'mystery', 'pol_con', 'mind_control','gene_editing', 'doomsday', 'occult', 'facts', 'space,' 'misc'] 

def assign_primary_category(categories, priority_list):
   
    if isinstance(categories, str):                         #otherwise returns the first letter of the string 
        categories = categories.split(',')  # Split comma-separated categories into a list
    
    
    categories = [category.strip() for category in categories]

    for category in priority_list:
        if category in categories:
            return category
    
    
    return categories[0] if len(categories) > 0 else None  # Safe check
                        # Default to the first category if none in priority list


df_WF['primary_category'] = df_WF['categories'].apply(lambda x: assign_primary_category(x, priority_list))
df_WF


# In[ ]:





# # aggregation

# In[ ]:


df_WF.describe()


# In[ ]:


aggregated_df = df_WF.groupby('primary_category').agg({'view_count': ['sum', 'mean', 'max'],
    'like_count': ['sum', 'mean', 'max'], 'comment_count': ['sum', 'mean', 'max']}).reset_index()

aggregated_df


# In[ ]:


import matplotlib.pyplot as plt
import seaborn as sns

# Bar plot for total view count by primary category
sns.barplot(x='primary_category', y=('view_count', 'sum'), data=aggregated_df)
plt.title('Total View Count by Primary Category')
plt.xlabel('Primary Category')
plt.ylabel('Total Views')
plt.xticks(rotation=90)
plt.show()


# In[ ]:


#visualizing according to like count

sns.barplot(x='primary_category', y=('like_count', 'sum'), data=aggregated_df)
plt.title('Total Like Count by Primary Category')
plt.xlabel('Primary Category')
plt.ylabel('Total Likes')
plt.xticks(rotation=90)
plt.show()


# In[ ]:


#visualizing according to comment count
sns.barplot(x='primary_category', y=('comment_count', 'sum'), data=aggregated_df)
plt.title('Total Comment Count by Primary Category')
plt.xlabel('Primary Category')
plt.ylabel('Total Comments')
plt.xticks(rotation=90)
plt.show()


#  # LOWEST AND HIGHEST COUNTS OF LIKED VIDEOS

# In[ ]:


#lowest liked  ideos
lowest_likedDF = df_WF.sort_values(by='like_count').head(5)


# In[ ]:


#top five liked videos 
highest_likedDF = df_WF.sort_values(by='like_count', ascending=False).head(5)


# In[ ]:


#visualizing top 5 liked videos against thier categories

plt.bar(highest_likedDF['primary_category'], highest_likedDF['like_count'], color='orange')

plt.title('Top 5 Liked Videos by Primary Category')  #title of bar graph
plt.xlabel('Primary Category')
plt.ylabel('Like Count')
plt.xticks(rotation=45)   #rotate angle for better readability of labels


plt.tight_layout()   #display without overlap
plt.show()


# # MOST COMMENTED ON
# 

# In[ ]:


most_commentsDF = df_WF.sort_values(by='comment_count', ascending=False).head(5)


# In[ ]:


plt.bar(most_commentsDF['primary_category'], most_commentsDF['comment_count'], color='purple')

plt.title('Top 5 Commented on Videos by Primary Category')  #title of bar graph
plt.xlabel('Primary Category')
plt.ylabel('Comment Count')
plt.xticks(rotation=45)   #rotate angle for better readability of labels


plt.tight_layout()   #display without overlap
plt.show()


# In[ ]:


fewest_commentsDF= df_WF.sort_values(by = 'comment_count').head(5)


# # TOP 5 Viewed

# In[ ]:


highest_viewedDF = df_WF.sort_values(by='view_count', ascending=False).head(5)


# In[ ]:


plt.bar(highest_viewedDF ['primary_category'], highest_viewedDF ['view_count'], color='red')

plt.title('Top 5 Viewed Videos by Primary Category')  #title of bar graph
plt.xlabel('Primary Category')
plt.ylabel('View Count')
plt.xticks(rotation=45)   #rotate angle for better readability of labels


plt.tight_layout()   #display without overlap
plt.show()


# In[ ]:





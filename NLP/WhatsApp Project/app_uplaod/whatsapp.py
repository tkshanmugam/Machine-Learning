import numpy as np
import pandas as pd
import time
import emoji
import datetime
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt1
import seaborn as sns
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('vader_lexicon')
start = time. time()
plt.rcParams.update({'figure.figsize':(9,7), 'figure.dpi':150})
#file=pd.read_csv("rrr.txt", sep = "\t",encoding='utf8')
#df = pd.read_csv('rrr.txt', delimiter= '\s', index_col=False)
#filename='rr.txt'


class WhatsappFilrt:

    def __init__(self):
        pass

    def PreProcessing(self,filename):
        df = pd.read_csv(filename,header=None,error_bad_lines=False,encoding='utf8')
        if(len(df.columns)==2):
            df=df.drop(0)
            df=df.dropna(axis=0)
            df.columns=['Date','Text']
            Message=df["Text"].str.split("-",n=1,expand=True)
            df["Time"]=Message[0]
            Message1=Message[1].str.split(":",n=1,expand=True)
            df["Name"]=Message1[0]
            df["Text"]=Message1[1]
            df=df[["Date","Time","Name","Text"]]
            df=df.dropna(axis=0)
        elif(len(df.columns)==4):
            df=df.drop([2,3],axis=1)
            df=df.dropna(axis=0)
            df=df.drop(0)
            df.columns=['Date','Text']
            Message=df["Text"].str.split("-",n=1,expand=True)
            df["Time"]=Message[0]
            Message1=Message[1].str.split(":",n=1,expand=True)
            df["Name"]=Message1[0]
            df["Text"]=Message1[1]
            df=df[["Date","Time","Name","Text"]]
            df=df.dropna(axis=0)
        else:
            print(len(df.columns))
        return df



    def give_emoji_free_text(self,text):
        allchars = [str for str in text.decode('utf-8')]
        emoji_list = [c for c in allchars if c in emoji.UNICODE_EMOJI]
        clean_text = ' '.join([str for str in text.decode('utf-8').split() if not any(i in str for i in emoji_list)])
        return clean_text



    def deEmojify(self,inputString):
        return inputString.encode('ascii', 'ignore').decode('ascii')

    def assign_Emoji(self,text,dataset):
        for i, x in enumerate(text):
            if(x==0):
                dataset['Text'][i]='Emoji'
        return dataset
    def TalkerChecking(self,unique_Frequency_Talker,flirt_words,Talker_Filter_list):
        for i in unique_Frequency_Talker.index:
            if i in flirt_words:
                Talker_Filter_list.append(unique_Frequency_Talker[unique_Frequency_Talker.index==i])
        return Talker_Filter_list
    def LesserChecking(self,unique_Frequency_Lesser,flirt_words,Less_Filter_list):
        for i in unique_Frequency_Lesser.index:
            if i in flirt_words:
                Less_Filter_list.append(unique_Frequency_Lesser[unique_Frequency_Lesser.index==i])
        return  Less_Filter_list


    def Wholeprocess(self,dataset):
        result=[]
        result1=[]
        dataset=dataset.dropna(subset=['Date','Time','Name','Text'])
        dataset["Text"]=dataset['Text'].apply(lambda x : obj.give_emoji_free_text(str(x).encode('utf8')))
        dataset['Name']=dataset['Name'].apply(lambda x : obj.deEmojify(str(x).lower()))
        dataset['TW']=dataset['Text'].str.split().str.len()

        dataset.index=range(dataset.shape[0])



        dataset=obj.assign_Emoji(dataset.TW,dataset)


        dataset.index=range(dataset.shape[0])
        total_word_file=dataset['TW'].sum()

        "Finding top 3 chats with  words count "
        chater=dataset['Name'].value_counts().head(7).to_dict()


        "Finding More"
        Talker=dataset['Name'].value_counts().idxmax()
        Talker1=Talker.upper()
        print("More Talktative:", Talker.upper())
        result.append(Talker1)
        Less_Talker=dataset['Name'].value_counts().idxmin()
        Less_Talker1=Less_Talker.upper()
        print("Less Talktative:", Less_Talker.upper())
        result.append(Less_Talker1)


        Talker_chat= pd.DataFrame(dataset[dataset.Name==Talker])
        Less_chat= pd.DataFrame(dataset[dataset.Name==Less_Talker])

        unique_Frequency_Talker= pd.DataFrame(Talker_chat['Text'].str.split(' ', expand =True).stack().value_counts())
        unique_Frequency_Lesser= pd.DataFrame(Less_chat['Text'].str.split(' ', expand =True).stack().value_counts())

        unique_Frequency_Talker['Usage of word']=(unique_Frequency_Talker[0]/Talker_chat['TW'].sum())*100
        unique_Frequency_Lesser['Usage of word']=(unique_Frequency_Lesser[0]/Less_chat['TW'].sum())*100


        flirt_words=['kiss','hug','date', 'cute',
                       'beautiful', 'sexy', 'hot','adorable','uma', 'darling',
                       'fuck','porn', 'x', 'sex', 'matter', 'nipple', 'virgin', 'sperm',
                       'seduce', 'condom','kk']

            #Extracting flirt word
        Talker_Filter_list=[]

        Less_Filter_list=[]


            #print(Talker,Talker_Filter_list)




        #obj.TalkerChecking(unique_Frequency_Talker,flirt_words,Talker_Filter_list)
        try:

            Talker_Filter_list=pd.concat(obj.TalkerChecking(unique_Frequency_Talker,flirt_words,Talker_Filter_list))
            result1.append(Talker_Filter_list)
        except ValueError:
            print("Wonderfull no flirting by {}".format(Talker.upper()))

        try:
            Talker_Filter_list.columns=['Repeated_count','Frequency_Value']
            Talker_Filter_list['Flirt_Frequency']=(Talker_Filter_list['Repeated_count']/len(flirt_words))*100
            Talker_out=round(Talker_Filter_list['Flirt_Frequency'].sum()/Talker_Filter_list.shape[0],2)
            print("Flirting Percentage of{}:".format(Talker.upper()), Talker_out,"%")
            result.append(Talker_out)

        except AttributeError:
            pass


        #obj.LesserChecking(unique_Frequency_Lesser,flirt_words,Less_Filter_list)
            #print(Less_Talker,Less_Filter_list)

        try:
             Less_Filter_list= pd.concat(obj.LesserChecking(unique_Frequency_Lesser,flirt_words,Less_Filter_list))
             result1.append(Less_Filter_list)
        except ValueError:
            print("Wonderfull no flirting by {}".format(Less_Talker.upper()))

        try:
            Less_Filter_list.columns=['Repeated_count','Frequency_Value']
            Less_Filter_list['Flirt_Frequency']=(Less_Filter_list['Repeated_count']/len(flirt_words))*100
            Less_out=round(Less_Filter_list['Flirt_Frequency'].sum()/Less_Filter_list.shape[0],2)
            print("Flirting Percentage of{}:".format(Less_Talker.upper()), Less_out,"%")
            result.append(Less_out)

        except AttributeError:
            pass
        return result, result1
    def statsWhatsApp(self,dataset):
        stats=[]
        stats1=[]
        date_chart = pd.DataFrame(dataset["Date"].value_counts())
        plt.clf()
        #plt.rcParams.update({'figure.figsize':(9,7), 'figure.dpi':150})
        ax1=sns.countplot(x='Date',hue='Name', data=dataset)
        ax1.set_xticklabels(ax1.get_xticklabels(), rotation=40, ha="right")
        ax1.figure.savefig("static/output_image/date_chart_name.png")
        #stats.append(date_chart)
        most_active_date= dataset["Date"].value_counts().idxmax()
        stats.append(most_active_date)
        week_days= ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday']
        l=list(map(int, most_active_date.split('/')))
        day=datetime.date(l[2],l[0],l[1]).weekday()
        active_week_day=week_days[day]
        stats.append(active_week_day)
        active_hour_of_day= dataset["Time"].value_counts().idxmax()
        stats.append(active_hour_of_day)
        avg_no_of_msgs_per_day = round(dataset["Date"].count() / dataset["Date"].nunique())
        stats.append(avg_no_of_msgs_per_day )
        ##########################
        media =dataset[dataset["Text"] == " <media omitted>"]
        if len(media):
            media_count = pd.DataFrame(media["Name"].value_counts())
            #media_count.columns=['Count']
            media_share_freak = media["Name"].value_counts().idxmax()
            #stats1.append(media_count)
            stats1.append(media_share_freak)
        else:
            media_count = ""
            media_share_freak = "No Media were shared"
            #stats1.append(media_count)
            stats1.append(media_share_freak)

        ####################
        message_deleted =dataset[dataset["Text"] == " this message was deleted"]
        if len(message_deleted):
            msg_deleted_count = pd.DataFrame(message_deleted["Name"].value_counts())
            #msg_deleted_count.columns=['Count']
            msg_deleting_freak = message_deleted["Name"].value_counts().idxmax()
            #stats1.append(msg_deleted_count)
            stats1.append(msg_deleting_freak)
        else:
            msg_deleted_count = ""
            msg_deleting_freak = "No message was deleted"
            #stats1.append(msg_deleted_count)
            stats1.append(msg_deleting_freak)
        #################################
        voice_call=dataset[dataset["Text"]==" missed voice call"]
        if len(voice_call):
            voice_call_count = pd.DataFrame(voice_call["Name"].value_counts())
            #voice_call_count.columns=['Count']
            voice_calling_freak = voice_call["Name"].value_counts().idxmax()
            #stats1.append(voice_call_count)
            stats1.append(voice_calling_freak)
        else:
            voice_call_count = ""
            voice_calling_freak = "No Missed Voice Call"
            #stats1.append(voice_call_count)
            stats1.append(voice_calling_freak)
        ######################################
        video_call=dataset[dataset["Text"]==" missed video call"]
        if len(video_call):
            video_call_count = pd.DataFrame(video_call["Name"].value_counts())
            #video_call_count.columns=['Count']
            video_calling_freak = video_call["Name"].value_counts().idxmax()
            #stats1.append(video_call_count)
            stats1.append(video_calling_freak)
        else:
            video_call_count = ""
            video_calling_freak = "No Missed Video Call"
            #stats1.append(video_call_count)
            stats1.append(video_calling_freak)
        return date_chart,media_count,msg_deleted_count,voice_call_count,video_call_count,stats, stats1
    def sentimentalAnalysis(self,data):

        #downloading vader_lexicon for the process

        "Importing Necessary Packeage"
        from nltk.sentiment.vader import SentimentIntensityAnalyzer
        sid = SentimentIntensityAnalyzer()

        "Deleting null pr empty value"
        data.dropna(inplace=True)

        "Checking for a comment"
        #sid.polarity_scores(data['Text'][93])

        "Creating respective columns"

        data['scores'] = data['Text'].apply(lambda commentText: sid.polarity_scores(commentText))
        data['compound']  = data['scores'].apply(lambda score_dict: score_dict['compound'])
        data['Negtive']  = data['scores'].apply(lambda score_dict: score_dict['neg'])
        data['Postive']  = data['scores'].apply(lambda score_dict: score_dict['pos'])
        data['Neutral']  = data['scores'].apply(lambda score_dict: score_dict['neu'])

        "Creating final pos or neg using compound score"
        data['comp_score'] = data['compound'].apply(lambda c: 'pos' if c >=0 else 'neg')
        plt.clf()
        comp=sns.countplot(x = 'comp_score', hue = 'Name', data = data, palette = 'magma')
        comp.figure.savefig("static/output_image/posneg.png")
        "Checking how many pos and neg"
        posneg=pd.DataFrame(data['comp_score'].value_counts())
        return posneg
    def topicModelling(self,dataset):
        results=[]
        tfidf = TfidfVectorizer(max_df=0.95, min_df=2, stop_words='english')# Assign the value for max and min allowance stopwords
        dtm = tfidf.fit_transform(dataset['Text'])# Transforming commentText to tfdif formula
        nmf_model = NMF(n_components=5,random_state=42)#Assigning number of topics
        nmf_model.fit(dtm)#Tranforming Transformed commentText formula to NMF .This stores the output of 5 topic modelling topics
        #cc=nmf_model.components_
        for index,topic in enumerate(nmf_model.components_):# Now we are printing Top 10 words under each Topic
            #print(f'THE TOP 15 WORDS FOR TOPIC #{index}')
            result=([tfidf.get_feature_names()[i] for i in topic.argsort()[-10:]])
            #print(result)
            results.append([index,result])
        #print(results)
        topic_results = nmf_model.transform(dtm)
        dataset['Topic'] = topic_results.argmax(axis=1)#Assign respective topics to each commentTent


        topicmodelling=pd.DataFrame(results)
        return topicmodelling,dataset

    def wordcloud(self,dataset):
        comment_words = []
        stopword = stopwords.words('english')
        stopword.extend(['omitted', 'voice','missed','call','video','deleted','media','message'])
        wordcloudss="This function saves image"
        dataset.index=range(dataset.shape[0])
        for i in range(1,len(dataset)):
            comment_words.append(dataset['Text'][i])
        vv=" ".join(comment_words)
        #plt.rcParams.update({'figure.figsize':(9,7), 'figure.dpi':150})
        plt1.clf()
        wordcloud = WordCloud(width = 800, height = 800,
                                  background_color ='white',
                                  stopwords = stopword,
                                  min_font_size = 10).generate(vv)
        #plt.figure(figsize = (9, 7), facecolor = None)
        plt1.imshow(wordcloud)
        plt1.axis("off")
        #plt.tight_layout(pad = 0)
        plt1.savefig('static/output_image/wordcloud.png')
        #plt.show()
        #print("Successfully created")
        return wordcloudss

obj=WhatsappFilrt()

end = time. time()
print('Execution Time:',end - start)

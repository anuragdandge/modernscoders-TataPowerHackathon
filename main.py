
import googleapiclient.discovery
from textblob import TextBlob
# credentials
api_key = "AIzaSyAwOACQuQbx5xqXQ2z2mPGj_FusMJ0yet0"

# Client Created
youtube = googleapiclient.discovery.build(
    "youtube", "v3", developerKey=api_key)

# Searching for "renewable energy and sustainability" keyword
search_query = "renewable energy and sustainability"

search_id = youtube.search().list(
    q=search_query,
    part="snippet",
    maxResults=10
)

search_id_res = search_id.execute()
vid_list = []
vtitle_list = []

for searched_id in search_id_res.get("items", []):
    vid = searched_id["id"]["videoId"]
    vid_list.append(vid)

print(vid_list)

for vid in vid_list:
    print("Video ID = " + vid)

    video_response = youtube.videos().list(
        id=vid,
        part="snippet"
    ).execute()

    
    snippet = video_response['items'][0]['snippet']
    vtitle = snippet['title']
    print("\n Video Title " + vtitle)
    # Check if comments are enabled or disabled
    if snippet.get('commentModerationStatus') == "blocked":
        print("Comments are disabled for this video.")
    else:
        # print("Comments are enabled for this video.")
        search_comment_id = youtube.commentThreads().list(
            part="snippet,replies",
            videoId=vid,
            textFormat="plainText",
            maxResults=5
        )

        try:
            comment_response = search_comment_id.execute()
            for comment_thread in comment_response.get("items", []):
                cid = comment_thread["id"]
                autherId = comment_thread["snippet"]["topLevelComment"]["snippet"]["authorChannelId"]["value"]
                comment = comment_thread["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                print("\n Comment ID = " + cid)
                print("Author ID =  " +autherId )
                print("Comment = "+comment)
                analysis = TextBlob(comment)
                polarity = analysis.sentiment.polarity
                if polarity > 0.5:
                    sentiment = "Positive"
                elif polarity == 0.0:
                    sentiment = "Neutral"
                elif polarity < 0.5:
                    sentiment = "Negative"
                print("Sentiment: " + sentiment)
                print("Polarity: " + str(polarity) + "\n")    
            
                # print("++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        except googleapiclient.errors.HttpError as e:
            # Handle errors if comments retrieval fails
            print("Comments Disabled")

    print("----------------------------------------------------------------------------------------")

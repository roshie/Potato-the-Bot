from googleapiclient.discovery import build
api_key = 'AIzaSyAo_PE7p7V3BB8Uj76GbbXNqQi9csywKXM'
cse_id = "9c65d777e653a9ffc"

def google_search(search_term, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res

#result = google_search("Coffee", my_api_key, my_cse_id)





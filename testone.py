import requests
import json
from nltk.tokenize import word_tokenize

def fetch_data_from_api(api_url):
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            return data.get('data', {}).get('data', [])  # Access the nested 'data' field
        else:
            print(f"Failed to fetch data from API. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return None

def identify_sources(data):
    citations = []

    for item in data:
        response_text = item['response']
        sources = item.get('source', [])  # Ensure 'source' key is accessed correctly

        matched_sources = []
        for source in sources:
            source_context = source.get('context', '')
            source_id = source.get('id', '')
            source_link = source.get('link', '')

            # Tokenize the response text and source context
            response_tokens = word_tokenize(response_text.lower())
            source_tokens = word_tokenize(source_context.lower())

            # Check for common words between response and source
            common_words = set(response_tokens) & set(source_tokens)
            if common_words:
                matched_sources.append({'id': source_id, 'link': source_link})

        # Add citation if there are matched sources
        if matched_sources:
            citations.extend(matched_sources)

    return citations

# API endpoint
api_url = "https://devapi.beyondchats.com/api/get_message_with_sources"

# Fetch data from the API
data = fetch_data_from_api(api_url)
if data:
    # Identify sources for each message
    citations = identify_sources(data)

    # Generate citation output
    if citations:
        citation_output = []
        for citation in citations:
            citation_output.append({
                "id": citation["id"],
                "link": citation["link"]
            })

        print("Example Citation Output:")
        print(json.dumps(citation_output, indent=2))
    else:
        print("No citations found.")
else:
    print("Failed to fetch data from the API.")

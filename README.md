# evernote-sync-service

Easy to use evernote client service. I started this repo, because I wanted to use the Evernote API in my Go application, but Evernote does not provide any sdk for Go.

The project contains a lightweight python service running in a Docker container, with endpoints to fetch Evernote notebooks and notes. 

Usage
-----
```
docker run -e "EVERNOTE_CONSUMER_KEY=$EVERNOTE_CONSUMER_KEY" -e "EVERNOTE_CONSUMER_SECRET=$EVERNOTE_CONSUMER_SECRET" hairqles/evernote-sync-service
```

OAUTH
-----
1. Send a GET request *localhost:5000/authorize?callback=$your-callback-url*
```
{
    "authorize_url": $authorize_url
}
```

2. Redirect the user to $authorize_url. After the user authorized your application, Evernote will redirect the user back to $your-callback-url/oauth_token=$oauth_token=false

3. Parse $oauth_token and send a GET request to *localhost:5000/authenticate?oauth_verifier=$oauth_token*
```
{
    "auth_token": $auth_token
}
```

4. Save the $auth_token.
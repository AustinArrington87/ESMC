#%%
# Example post to ESMC API 

# Get OAuth token
import getOAuth
import postToESMC as api

token = getOAuth.getToken()

res = api.post('test.json',token)
# %%

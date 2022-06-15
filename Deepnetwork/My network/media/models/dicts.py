import json

posts = {0:"nothing"}
unaccept = {0:"nothing"}


with open("posts.txt", "w") as f:
    f.write(json.dumps(posts))
    
with open("unaccept.txt",'w') as f:
    f.write(json.dumps(unaccept))



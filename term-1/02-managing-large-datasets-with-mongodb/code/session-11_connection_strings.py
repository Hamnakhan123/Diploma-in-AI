# Session 11 · Atlas connection strings: build them safely and read them back
from urllib.parse import quote_plus, urlsplit, parse_qs

user = "hamna_app"
password = "K@rachi#2025"                  # special characters MUST be URL-encoded
cluster = "cluster0.ab1cd.mongodb.net"     # copied from Atlas > Connect > Drivers (example host)

uri = (f"mongodb+srv://{quote_plus(user)}:{quote_plus(password)}@{cluster}/kgs"
       "?retryWrites=true&w=majority&appName=KGSAnalytics")
print("Connection string:\n ", uri.replace(quote_plus(password), "<password>"))
print("\nEncoded password:", quote_plus(password), " (@ -> %40, # -> %23)")

parts = urlsplit(uri)
print("\nParsed back:")
print("  scheme   :", parts.scheme, "(+srv = look up the replica-set hosts in DNS)")
print("  user     :", parts.username)
print("  host     :", parts.hostname)
print("  database :", parts.path.lstrip("/"))
for k, v in parse_qs(parts.query).items():
    print(f"  option   : {k} = {v[0]}")

print("\nWhat +srv expands to (illustration): three replica-set members on port 27017")
for i in range(3):
    print(f"  {cluster.replace('cluster0.', f'cluster0-shard-00-0{i}.')}:27017")

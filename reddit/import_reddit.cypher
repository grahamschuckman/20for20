WITH $json as data
UNWIND data as record
MERGE (p:Post {post_id: record.id, author: coalesce(record.author, "Unknown"), title: record.title, date: record.timestamp, score: record.score, url: record.url, comments: record.comms_num, subreddit: record.subreddit})
MERGE (a:Author {author: coalesce(record.author, "Unknown")})
MERGE (p)-[:POSTED_BY]->(a)
MERGE (c:Channel {type:record.subreddit, subscribers: record.subscribers})
MERGE (p)-[:POSTED_IN]->(c)

echo "scan 'hwl6390', {COLUMNS => ['from', 'body'], FILTER => \"SingleColumnValueFilter('from', 'from', = ,'binary:pete.davis@enron.com')\"}" | hbase shell > pete_emails.txt

echo "disable 'hwl6390'" | hbase shell

echo "drop 'hwl6390'" | hbase shell

exit
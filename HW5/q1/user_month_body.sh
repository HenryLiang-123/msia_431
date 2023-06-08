echo "scan 'hwl6390', {COLUMNS => ['from', 'date', 'body'], FILTER => \"SingleColumnValueFilter('from', 'from', = ,'binary:pete.davis@enron.com') AND SingleColumnValueFilter('date', 'date', = ,'binary:2002-02')\"}" | hbase shell > pete_feb2002_emails.txt

echo "disable 'hwl6390'" | hbase shell

echo "drop 'hwl6390'" | hbase shell

exit
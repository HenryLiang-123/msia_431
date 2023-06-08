echo "scan 'hwl6390', {COLUMNS => ['date', 'body'], FILTER => \"SingleColumnValueFilter('date', 'date', = ,'binary:2002-02')\"}" | hbase shell > feb2002_emails.txt

echo "disable 'hwl6390'" | hbase shell

echo "drop 'hwl6390'" | hbase shell

exit
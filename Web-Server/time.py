#cgi调用
#简单的显示时间
from datetime import datetime
print('''\
<html>
<body>
<p>Generated {0}</p>
</body>
</html>'''.format(datetime.now()))
